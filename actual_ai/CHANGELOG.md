## 1.1.3

- Upstream sync to [`2.4.2`](https://github.com/sakowicz/actual-ai/releases/tag/2.4.2)

## 1.1.2

- Drop `syncAccountsBeforeClassify` from the default `FEATURES`. That feature
  triggers Actual's bank sync for every account with sync configured, and a
  single failing account (e.g. an old/disabled one) throws and crashes the
  process before any categorization runs. actual-ai does not need to bank-sync;
  transactions arrive through your normal flow. Re-add it only if all your
  synced accounts are healthy.

## 1.1.1

- Stop persisting the budget cache under `/data`. The cache stored a run lock
  with `pid=1`, which is always "alive" inside the container and made the
  addon deadlock on restart with "Refusing to use shared dataDir". The cache
  is now ephemeral (wiped on each start), which also avoids stale-schema
  errors. Re-downloading the budget each run is cheap.

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
