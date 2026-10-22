#!/usr/bin/env sh
set -e

echo "[INFO] Starting CrowdSec WAN IP Updater add-on..."
exec python3 /app/wan_ip_monitor.py
