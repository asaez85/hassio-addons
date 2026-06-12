# Free Games Claimer Remaster

Automatically claims free games on the Epic Games Store, Amazon Prime Gaming,
GOG and Steam.

## Credits

All application code is
[Free-Games-Claimer-Remaster](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster)
by **Paweł Adamiec** ([@P-Adamiec](https://github.com/P-Adamiec)), a Python
rewrite of vogler/free-games-claimer using `nodriver` for stealth browser
automation. This addon merely packages his project so it can be installed as
a Home Assistant addon and run on Raspberry Pi (aarch64) as well as amd64.
Please report application bugs upstream and consider supporting the author.

## Setup

1. Fill in the credentials for the stores you want in the addon options
   (leave the rest empty).
2. Set `STORES` to a comma-separated list, e.g. `epic,prime,gog`.
3. Start the addon.
4. Open the web UI (port 7080) to watch the browser. The first run usually
   needs manual help: captchas and 2FA prompts must be solved in the noVNC
   window. Sessions are persisted afterwards, so later runs are unattended.

## Options

| Option | Description |
|--------|-------------|
| `SHOW` | Show the browser in the VNC window (recommended `true`) |
| `WIDTH` / `HEIGHT` | Virtual display resolution |
| `SCHEDULER_HOURS` | Hours between automatic runs (default 12) |
| `STORES` | Comma-separated stores: `epic`, `prime`, `gog`, `steam`, `gamerpower` |
| `EG_*` | Epic Games credentials; `EG_OTPKEY` is the TOTP "Manual Entry Key" for automatic 2FA |
| `PG_*` | Amazon Prime Gaming credentials |
| `GOG_*` | GOG credentials |
| `STEAM_*` | Steam credentials (only if `steam` is in `STORES`) |
| `DISCORD_WEBHOOK` | Discord webhook URL for notifications |
| `NOTIFY` | Apprise URL (Telegram, email, …) for notifications |
| `VNC_PASSWORD` | Optional password for the noVNC web UI |
| `DEBUG` | Verbose logging |
| `DRYRUN` | Go through the motions without actually claiming |
| `env_vars` | Extra environment variables (name/value pairs) for advanced options like `PG_OTPKEY`, `GOG_NEWSLETTER`, `FANATICAL_*`… |

## Data

Browser session, SQLite database and screenshots persist in the addon's
private data storage across restarts and updates. Uninstalling the addon
removes them (you would need to log in again after reinstalling).

## Updating to a newer upstream version

The addon builds from a commit of the upstream repository
(P-Adamiec/Free-Games-Claimer-Remaster) pinned in the `Dockerfile`
(`FGC_COMMIT`). To pick up upstream changes, update that hash and bump
`version` in `config.yaml`, then update the addon in Home Assistant.
