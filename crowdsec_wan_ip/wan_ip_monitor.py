#!/usr/bin/env python3
"""CrowdSec WAN IP Updater.

Periodically resolves the public WAN IP and, when it changes, notifies the
remote VPS whitelist updater with the previous and the new IP.

Configuration is read from /data/options.json when running as a Home Assistant
add-on, otherwise from environment variables (see the README).
"""

import json
import logging
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlparse

LOG = logging.getLogger("crowdsec_wan_ip")

DEFAULT_RESOLVERS = [
    "https://api.ipify.org?format=json",
    "https://ifconfig.me/ip",
    "https://icanhazip.com",
]


def load_config() -> dict:
    """Load options from HA add-on options.json or env variables."""
    options = {}
    options_path = Path("/data/options.json")
    if options_path.exists():
        try:
            with options_path.open() as fh:
                options = json.load(fh)
            LOG.debug("Loaded configuration from %s", options_path)
        except (json.JSONDecodeError, OSError) as exc:
            LOG.warning("Could not read %s: %s", options_path, exc)

    def opt(name: str, default=None, cast=None):
        value = options.get(name)
        if value is None or value == "":
            value = os.environ.get(f"CROWDSEC_WAN_IP_{name.upper()}", default)
        if cast is not None and value is not None:
            try:
                value = cast(value)
            except (TypeError, ValueError) as exc:
                LOG.warning("Invalid value for %s (%r): %s", name, value, exc)
                value = default
        return value

    def as_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v) for v in value if v]
        return [str(v) for v in str(value).split(",") if v]

    def as_bool(value):
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        return str(value).lower() in {"1", "true", "yes", "on"}

    return {
        "check_interval_minutes": opt("check_interval_minutes", 5, int),
        "resolver_urls": as_list(opt("resolver_urls", DEFAULT_RESOLVERS)),
        "update_mode": opt("update_mode", "webhook"),
        "notify_on_initial_run": as_bool(opt("notify_on_initial_run", True)),
        "webhook_url": opt("webhook_url", ""),
        "webhook_token": opt("webhook_token", ""),
        "webhook_timeout_seconds": opt("webhook_timeout_seconds", 30, int),
        "webhook_retries": opt("webhook_retries", 3, int),
        "ssh_host": opt("ssh_host", ""),
        "ssh_port": opt("ssh_port", 22, int),
        "ssh_user": opt("ssh_user", "crowdsec-updater"),
        "ssh_key_path": opt("ssh_key_path", "/config/crowdsec_wan_ip_ssh_key"),
        "ssh_command": opt("ssh_command", "update-crowdsec-whitelist"),
        "ssh_options": as_list(
            opt(
                "ssh_options",
                ["-o StrictHostKeyChecking=accept-new", "-o BatchMode=yes", "-o ConnectTimeout=10"],
            )
        ),
        "state_file": Path(opt("state_file", "/data/last_wan_ip")),
    }


def validate_ip(value: str) -> str:
    """Return normalized IPv4/IPv6 string or raise ValueError."""
    value = value.strip()
    addr = ip_address(value)
    return str(addr)


def fetch_ip(resolver_urls: list[str], timeout: int = 10) -> str | None:
    """Resolve the current public IP from the configured list of services."""
    for url in resolver_urls:
        ip = _fetch_from_url(url, timeout)
        if ip is not None:
            try:
                return validate_ip(ip)
            except ValueError as exc:
                LOG.warning("Resolver %s returned invalid IP %r: %s", url, ip, exc)
    return None


def _fetch_from_url(url: str, timeout: int) -> str | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace").strip()
        if not raw:
            return None
        # Services such as ipify return JSON.
        if raw.startswith("{"):
            try:
                data = json.loads(raw)
                if isinstance(data, dict) and "ip" in data:
                    return data["ip"].strip()
            except json.JSONDecodeError:
                pass
        return raw
    except (urllib.error.URLError, socket.timeout, OSError) as exc:
        LOG.debug("Failed to query %s: %s", url, exc)
        return None


def read_last_ip(state_file: Path) -> str | None:
    if not state_file.exists():
        return None
    try:
        content = state_file.read_text().strip()
        return validate_ip(content) if content else None
    except (OSError, ValueError) as exc:
        LOG.warning("Could not read previous IP from %s: %s", state_file, exc)
        return None


def write_last_ip(state_file: Path, ip: str) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(ip + "\n")


def trigger_update(config: dict, old_ip: str | None, new_ip: str) -> bool:
    """Notify the VPS updater. Return True if the notification succeeded."""
    mode = config["update_mode"]
    if mode == "webhook":
        return _trigger_webhook(config, old_ip, new_ip)
    if mode == "ssh":
        return _trigger_ssh(config, old_ip, new_ip)
    LOG.error("Unknown update_mode: %s", mode)
    return False


def _trigger_webhook(config: dict, old_ip: str | None, new_ip: str) -> bool:
    url = config["webhook_url"]
    if not url:
        LOG.error("webhook_url is not configured")
        return False

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        LOG.error("Invalid webhook_url scheme: %s", parsed.scheme)
        return False

    payload = {
        "old_ip": old_ip,
        "new_ip": new_ip,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    body = json.dumps(payload).encode("utf-8")

    retries = max(1, config.get("webhook_retries", 3))
    timeout = config.get("webhook_timeout_seconds", 30)

    for attempt in range(1, retries + 1):
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        token = config.get("webhook_token", "")
        if token:
            req.add_header("Authorization", f"Bearer {token}")

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                response_body = resp.read().decode("utf-8", errors="replace")[:500]
            LOG.info("Webhook accepted by VPS (HTTP %s): %s", status, response_body)
            return True
        except urllib.error.HTTPError as exc:
            response_text = exc.read().decode("utf-8", errors="replace")[:500]
            LOG.warning(
                "Webhook attempt %s/%s failed: HTTP %s %s",
                attempt,
                retries,
                exc.code,
                response_text,
            )
        except (urllib.error.URLError, socket.timeout, OSError) as exc:
            LOG.warning("Webhook attempt %s/%s failed: %s", attempt, retries, exc)

        if attempt < retries:
            time.sleep(2 ** attempt)

    LOG.error("Webhook failed after %s attempts", retries)
    return False


def _trigger_ssh(config: dict, old_ip: str | None, new_ip: str) -> bool:
    host = config["ssh_host"]
    if not host:
        LOG.error("ssh_host is not configured")
        return False

    key_path = config["ssh_key_path"]
    if not Path(key_path).exists():
        LOG.error("SSH private key not found at %s", key_path)
        return False

    cmd = [
        "ssh",
        *config["ssh_options"],
        "-i", key_path,
        "-p", str(config["ssh_port"]),
        f"{config['ssh_user']}@{host}",
        config["ssh_command"],
        old_ip or "",
        new_ip,
    ]

    LOG.info("Running SSH update command: %s", " ".join(cmd))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode == 0:
            LOG.info("SSH update succeeded: %s", result.stdout.strip())
            return True
        LOG.error(
            "SSH update failed (exit %s): stdout=%s stderr=%s",
            result.returncode,
            result.stdout.strip(),
            result.stderr.strip(),
        )
        return False
    except subprocess.TimeoutExpired:
        LOG.error("SSH update command timed out")
        return False
    except FileNotFoundError:
        LOG.error("ssh client is not installed in the container")
        return False


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def run_once(config: dict) -> None:
    state_file = config["state_file"]
    current_ip = fetch_ip(config["resolver_urls"])
    if current_ip is None:
        LOG.error("Could not determine current WAN IP")
        return

    last_ip = read_last_ip(state_file)
    LOG.info("Current WAN IP: %s (last known: %s)", current_ip, last_ip)

    if current_ip == last_ip:
        return

    is_initial = last_ip is None
    if is_initial and not config["notify_on_initial_run"]:
        LOG.info("Initial run: storing IP without notifying VPS")
        write_last_ip(state_file, current_ip)
        return

    LOG.info("WAN IP change detected: %s -> %s", last_ip, current_ip)
    if trigger_update(config, last_ip, current_ip):
        write_last_ip(state_file, current_ip)
    else:
        LOG.error("Update notification failed; will retry on next check")


def main() -> None:
    setup_logging()
    config = load_config()

    interval = max(1, config["check_interval_minutes"]) * 60
    LOG.info(
        "CrowdSec WAN IP Updater started (mode=%s, interval=%sm)",
        config["update_mode"],
        config["check_interval_minutes"],
    )

    try:
        while True:
            run_once(config)
            LOG.debug("Sleeping %s seconds", interval)
            time.sleep(interval)
    except KeyboardInterrupt:
        LOG.info("Shutdown requested")
        sys.exit(0)


if __name__ == "__main__":
    main()
