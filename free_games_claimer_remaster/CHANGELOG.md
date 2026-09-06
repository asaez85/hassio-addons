## 1.0.8

- Upstream sync to [`8b96d61c`](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster/commit/8b96d61cb6d0154152913ca84aa0d85426d0a631): v1.8: Verify Epic claims, fix browser start, warn on unknown settings

## 1.0.7

- Upstream sync to [`1e2b38f9`](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster/commit/1e2b38f945b9371641c64a62cff1d5fb65df96c0): v1.6: Ubisoft and Fab stores, reverse proxy VNC links

## 1.0.6

- Upstream sync to [`9e5222be`](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster/commit/9e5222beddb806d7a9ee1d01bd47ed501d9474c9): v1.5: Epic login and Latest tag fix

## 1.0.5

- Upstream sync to [`38080559`](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster/commit/38080559c2d556431c391ce2bef974fd28619f9b): v1.4: AliExpress check-in improvements, fingerprinting & store fixes, etc.

## 1.0.4

- Upstream sync to [`cca49923`](https://github.com/P-Adamiec/Free-Games-Claimer-Remaster/commit/cca4992354215cef8807b748575af797606627f4): docs: add Ch4r0ne shoutout and VNC_IP to changelog

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
