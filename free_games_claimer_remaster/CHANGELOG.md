## 1.0.3

- Build from the upstream repository (P-Adamiec/Free-Games-Claimer-Remaster)
  and credit the author properly.

## 1.0.2

- Extend nodriver's browser connect timeout (~2.75 s → ~2 min) so Chromium's
  cold start on Raspberry Pi doesn't fail with "Failed to connect to browser".

## 1.0.1

- Fix base image: hardcode Debian bookworm (the default HA Alpine base has no
  apt and can't install Chromium/TurboVNC).

## 1.0.0

- Initial packaging of Free-Games-Claimer-Remaster as a Home Assistant addon
  (aarch64 + amd64).
