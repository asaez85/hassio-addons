#!/usr/bin/env sh
# Home Assistant addon entrypoint for FireflyIII-AI-Categorizer.
#
# Maps the addon options (/data/options.json) to the environment variables the
# upstream Go app reads, then execs the server. Configuration precedence in the
# app is: UI settings (saved to /data/config.json) > environment variables >
# built-in defaults. So these options are convenient seeds/defaults; anything
# you change later in the web UI is persisted to /data and wins.
set -eu

OPTIONS="/data/options.json"

if [ -f "$OPTIONS" ]; then
    # Export every scalar option (string/number/bool), skipping nulls/empties so
    # the app keeps its own defaults for anything left blank. jq renders bools as
    # true/false and numbers as plain text, exactly what the app expects.
    for key in $(jq -r 'to_entries[]
            | select(.value | type | (. != "array" and . != "object"))
            | .key' "$OPTIONS"); do
        val="$(jq -r --arg k "$key" '.[$k]' "$OPTIONS")"
        if [ -n "$val" ] && [ "$val" != "null" ]; then
            export "$key=$val"
        fi
    done

    # Free-form passthrough for anything not exposed as a named option.
    count="$(jq -r '(.env_vars // []) | length' "$OPTIONS")"
    i=0
    while [ "$i" -lt "$count" ]; do
        name="$(jq -r --argjson i "$i" '.env_vars[$i].name // empty' "$OPTIONS")"
        value="$(jq -r --argjson i "$i" '.env_vars[$i].value // ""' "$OPTIONS")"
        [ -n "$name" ] && export "$name=$value"
        i=$((i + 1))
    done
fi

# Keep the internal port fixed at 3000 so the addon's port mapping and the
# "Open Web UI" button stay valid regardless of options.
export PORT=3000
# Persist app settings under the addon's /data volume (this is the image
# default, set explicitly so it survives any env passthrough).
export CONFIG_FILE="${CONFIG_FILE:-/data/config.json}"

echo "[firefly-ai addon] starting; provider=${AI_PROVIDER:-openai} ui=${ENABLE_UI:-true} port=${PORT}"
exec /app/firefly-ai-categorize
