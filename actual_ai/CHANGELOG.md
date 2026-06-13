## 1.1.0

- Pin the bundled `@actual-app/api`/`@actual-app/core` client to
  `26.7.0-nightly.20260612` to match an Actual Budget **Edge** server. The
  upstream image ships the 26.6.0 stable client, which is older than the
  Edge budget schema and fails with `SyncError: invalid-schema`
  (`no such column: bank_sync_status`). Adjust the `ACTUAL_API_VERSION`
  build arg if your Edge server schema moves on.

## 1.0.0

- Initial packaging of [actual-ai](https://github.com/sakowicz/actual-ai)
  (by Szymon Sakowicz) as a Home Assistant addon (aarch64 + amd64), based on
  the upstream `sakowicz/actual-ai:2.4.1` multi-arch image.
- Maps addon options to the app's environment variables and persists the
  downloaded budget cache across restarts under `/data`.
