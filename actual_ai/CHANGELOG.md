## 1.0.0

- Initial packaging of [actual-ai](https://github.com/sakowicz/actual-ai)
  (by Szymon Sakowicz) as a Home Assistant addon (aarch64 + amd64), based on
  the upstream `sakowicz/actual-ai:2.4.1` multi-arch image.
- Maps addon options to the app's environment variables and persists the
  downloaded budget cache across restarts under `/data`.
