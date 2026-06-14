# Firefly III AI Categorizer

Automatically categorizes your [Firefly III](https://www.firefly-iii.org)
transactions using an LLM. This is a Home Assistant packaging of
[**FireflyIII-AI-Categorizer**](https://github.com/ejagombar/FireflyIII-AI-Categorizer)
by [Eddie Gombar](https://github.com/ejagombar) — all credit for the
application goes to him. This addon only wraps his official multi-arch Docker
image so it runs as a Home Assistant addon on Raspberry Pi (aarch64) and amd64.

## How it works

Unlike a scheduled categorizer, this app is **webhook-driven**. It runs a small
web service (with a dashboard) that Firefly III calls whenever a transaction is
created. It looks only at **withdrawals without a category**, asks the LLM to
classify them, and writes the category back to Firefly III. Each result gets a
tag (prefix `ai` by default) reflecting its confidence: `CLASSIFIED`, `ASSUMED`
or `NEEDS_REVIEW`. The dashboard also lets you batch-process the existing
backlog of uncategorized transactions and manually review the doubtful ones.

## Quick start

1. **Start the addon**, then open it from **Settings → Add-ons →
   Firefly III AI Categorizer → Open Web UI** (or browse to
   `http://<your-HA-ip>:3000`).
2. On the **Settings** page enter:
   - Your **Firefly III URL** (e.g. `https://firefly.example.com`).
   - A **Personal Access Token** — create it in Firefly III under
     **Options → Profile → OAuth → Personal Access Tokens**.
   - Your **AI provider** and its API key (OpenAI, Gemini or DeepSeek).
   Settings are saved to `/data/config.json` and persist across restarts/updates.
3. **Create the webhook in Firefly III** (Automation → Webhooks → New):
   - **Title:** AI Categorizer (anything)
   - **Trigger:** *After transaction creation*
   - **Response:** *Transaction details*
   - **Delivery:** *JSON*
   - **URL:** `http://<your-HA-ip>:3000/webhook`
4. Create a test withdrawal in Firefly III and watch the addon log — it should
   receive the webhook and categorize it.

> You can also seed the configuration from the addon **Configuration** tab
> (options below) instead of the Settings page. Note the app's precedence:
> **values saved in the web UI override the addon options**, which in turn
> override the built-in defaults. If you set something here and later change it
> in the UI, the UI value wins.

## Networking & security

- The addon publishes **port 3000** on the Home Assistant host. The same port
  serves both the dashboard and the `/webhook` endpoint Firefly III posts to.
- **This app has no built-in authentication.** Keep it on your local network —
  do **not** port-forward 3000 to the internet. If you need remote access, put
  it behind an authenticating reverse proxy.
- If your Firefly III runs as another Home Assistant addon on the same host,
  point the webhook at the host IP and port 3000 as above.

## Options

### Firefly III connection

| Option | Description |
|--------|-------------|
| `FIREFLY_URL` | Base URL of your Firefly III instance. |
| `FIREFLY_PERSONAL_TOKEN` | A Firefly III Personal Access Token. |

### AI provider

Set `AI_PROVIDER` to `openai`, `gemini` or `deepseek` and fill the matching key:

| Provider | Key | Model option (default) |
|----------|-----|------------------------|
| openai | `OPENAI_API_KEY` | `OPENAI_MODEL` (`gpt-4o-mini`), optional `OPENAI_BASE_URL` for compatible APIs |
| gemini | `GEMINI_API_KEY` | `GEMINI_MODEL` (`gemini-2.5-flash`) |
| deepseek | `DEEPSEEK_API_KEY` | `DEEPSEEK_MODEL` (`deepseek-chat`) |

`OPENAI_BASE_URL` also lets you point the OpenAI provider at any
OpenAI-compatible endpoint (e.g. a local model, OpenRouter, Groq).

### Behaviour & processing

| Option | Description |
|--------|-------------|
| `ENABLE_UI` | Serve the web dashboard. Default `true`. |
| `TAG_PREFIX` | Prefix for the tags the app writes. Default `ai`. |
| `WORKER_CONCURRENCY` | Parallel webhook jobs. Default `1`. |
| `BATCH_CONCURRENCY` | Parallel jobs during a batch run. Default `5`. |
| `HISTORY_CONTEXT_LIMIT` | How many similar past transactions to feed the LLM as examples. Default `5`. |
| `HISTORY_LOOKBACK_DAYS` | How far back to search for those examples. Default `90`. |
| `HISTORY_CACHE_TTL` | How long to cache history lookups, e.g. `10m`. Default `10m`. |

### Advanced

Anything not exposed above can be passed through `env_vars`:

```yaml
env_vars:
  - name: SOME_UPSTREAM_VAR
    value: "some-value"
```

See the [upstream README](https://github.com/ejagombar/FireflyIII-AI-Categorizer)
for the full list of environment variables.

## Data

The addon stores the app's `config.json` (your saved settings) under the
addon's persistent `/data` volume, so it survives restarts and updates.

## Credits

Application by **[Eddie Gombar](https://github.com/ejagombar)** —
[FireflyIII-AI-Categorizer](https://github.com/ejagombar/FireflyIII-AI-Categorizer),
AGPL-3.0 licensed. This repository only packages it as a Home Assistant addon.
