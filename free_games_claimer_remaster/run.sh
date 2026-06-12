#!/usr/bin/env bash
set -eo pipefail

# Convert addon options (/data/options.json) into exported env vars.
# Done in python with shlex.quote so passwords with special chars survive.
python3 - <<'EOF'
import json, shlex

opts = json.load(open("/data/options.json"))
lines = []

def add(key, val):
    if val is None or val == "":
        return
    if isinstance(val, bool):
        val = "true" if val else "false"
    lines.append(f"export {key}={shlex.quote(str(val))}")

for key, val in opts.items():
    if key == "env_vars":
        for item in val or []:
            add(item.get("name"), item.get("value"))
    else:
        add(key, val)

open("/tmp/fgc_env.sh", "w").write("\n".join(lines) + "\n")
EOF
# shellcheck disable=SC1091
source /tmp/fgc_env.sh
rm -f /tmp/fgc_env.sh

# Persist app data (browser profile, fgc.db, screenshots) in the addon's
# /data storage by symlinking the path the app expects.
if [ ! -L /fgc/data ]; then
    rm -rf /fgc/data
    ln -s /data /fgc/data
fi
mkdir -p /data/browser /data/screenshots

exec /usr/local/bin/docker-entrypoint.sh python3 main.py
