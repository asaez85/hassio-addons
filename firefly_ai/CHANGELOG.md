## 1.0.0

- Initial packaging of
  [FireflyIII-AI-Categorizer](https://github.com/ejagombar/FireflyIII-AI-Categorizer)
  (by Eddie Gombar) as a Home Assistant addon (aarch64 + amd64), based on the
  upstream `ghcr.io/ejagombar/fireflyiii-ai-categorizer:latest` multi-arch image.
- Publishes the web UI / webhook endpoint on host port 3000 and maps addon
  options to the app's environment variables (a small `jq` entrypoint reads
  `/data/options.json`). Settings saved in the web UI persist under `/data`.
