#!/usr/bin/env python3
"""Home Assistant addon entrypoint for actual-ai.

Converts the addon options (/data/options.json) into the environment
variables the upstream app reads, persists the budget cache across
restarts, and then execs the upstream app exactly as `npm run prod` does
(`node dist/app.js` from /opt/node_app/app).
"""
import json
import os
import sys

OPTIONS_PATH = "/data/options.json"
APP_DIR = "/opt/node_app/app"
# Upstream hardcodes dataDir = "/tmp/actual-ai/"; symlink it into /data so the
# downloaded budget (and the run lock) survive restarts and avoid a full
# re-download on every boot.
DATA_DIR_LINK = "/tmp/actual-ai"
PERSIST_DIR = "/data/actual-cache"


def load_options():
    try:
        with open(OPTIONS_PATH) as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def build_env(opts):
    env = dict(os.environ)

    for key, val in opts.items():
        if key == "env_vars":
            # Free-form passthrough for anything not exposed as a named option.
            for item in val or []:
                name = item.get("name")
                value = item.get("value")
                if name:
                    env[str(name)] = "" if value is None else str(value)
            continue

        if key == "FEATURES":
            # The app expects a JSON array string, e.g. ["classifyOnStartup"].
            env["FEATURES"] = json.dumps(list(val or []))
            continue

        if val is None or val == "":
            # Skip empties so the app falls back to its own defaults.
            continue

        if isinstance(val, bool):
            env[key] = "true" if val else "false"
        else:
            env[key] = str(val)

    return env


def persist_data_dir():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    # Replace any pre-existing /tmp/actual-ai with a symlink to /data.
    if os.path.islink(DATA_DIR_LINK):
        if os.readlink(DATA_DIR_LINK) == PERSIST_DIR:
            return
        os.unlink(DATA_DIR_LINK)
    elif os.path.exists(DATA_DIR_LINK):
        import shutil
        shutil.rmtree(DATA_DIR_LINK, ignore_errors=True)
    os.symlink(PERSIST_DIR, DATA_DIR_LINK)


def main():
    opts = load_options()
    env = build_env(opts)
    persist_data_dir()

    os.chdir(APP_DIR)
    provider = env.get("LLM_PROVIDER", "(default)")
    print(f"[actual-ai addon] starting; provider={provider}, "
          f"cron='{env.get('CLASSIFICATION_SCHEDULE_CRON', '')}', "
          f"features={env.get('FEATURES', '[]')}", flush=True)
    os.execvpe("node", ["node", "dist/app.js"], env)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[actual-ai addon] failed to start: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
