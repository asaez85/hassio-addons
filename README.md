# asaez85 Home Assistant Add-ons

Personal Home Assistant addon repository.

## Installation

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fasaez85%2Fhassio-addons)

Or add `https://github.com/asaez85/hassio-addons` manually in
Settings → Add-ons → Add-on Store → ⋮ → Repositories.

## Add-ons

### [Free Games Claimer Remaster](free_games_claimer_remaster/)

Automatically claims free games on the Epic Games Store, Amazon Prime Gaming,
GOG and Steam, on a schedule and unattended.

This is a packaging of
[Free-Games-Claimer-Remaster](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster)
by **[Paweł Adamiec](https://github.com/P-Adamiec)** — all credit for the
application goes to him. This repository only adapts his project to run as a
Home Assistant addon, including Raspberry Pi (aarch64) support:

- Builds on Debian bookworm with Chromium on ARM (Google Chrome on amd64).
- Extends nodriver's browser-connect timeout so Chromium's slow cold start
  on a Raspberry Pi doesn't abort the run.
- Maps addon options to the application's environment variables and persists
  browser sessions, database and screenshots across restarts and updates.
- A daily GitHub Action tracks upstream and publishes new addon versions
  automatically when Adamiec releases changes.

**Architectures:** `aarch64`, `amd64`

See the [addon documentation](free_games_claimer_remaster/DOCS.md) for
configuration details and the
[changelog](free_games_claimer_remaster/CHANGELOG.md) for version history.

## License

[AGPL-3.0](LICENSE), the same license as the upstream project.
