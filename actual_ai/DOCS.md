# Actual AI

Automatically categorizes your [Actual Budget](https://actualbudget.org)
transactions using an LLM. This is a Home Assistant packaging of
[**actual-ai**](https://github.com/sakowicz/actual-ai) by
[Szymon Sakowicz](https://github.com/sakowicz) — all credit for the
application goes to him. This addon only wraps his official multi-arch
Docker image so it runs as a Home Assistant addon on Raspberry Pi
(aarch64) and amd64.

## How it works

The addon runs as a long-lived service with an internal cron scheduler.
On the schedule you set (and optionally on startup) it connects to your
Actual Budget server, looks at uncategorized transactions, asks the LLM to
categorize them, and writes the category back. Classified transactions get
the `GUESSED_TAG` note; the ones it could not classify get `NOT_GUESSED_TAG`.

## Quick start

1. In Actual Budget, open **Settings → Show advanced settings** and copy the
   **Sync ID** of the budget you want categorized — that is your
   `ACTUAL_BUDGET_ID`.
2. Set `ACTUAL_SERVER_URL` (defaults to `https://actualbudget.asaezs.com`)
   and `ACTUAL_PASSWORD` (your Actual server password).
3. Pick an `LLM_PROVIDER` and fill in the matching API key (see below).
4. Start the addon and watch the log. With `classifyOnStartup` in
   `FEATURES` (the default) it runs once immediately.

> **Note:** by default the addon **does** write changes. To do a no-op test
> run first, add `dryRun` to `FEATURES` — it will log what it would do
> without modifying anything.

## Options

### Actual Budget

| Option | Description |
|--------|-------------|
| `ACTUAL_SERVER_URL` | URL of your Actual Budget server. |
| `ACTUAL_PASSWORD` | Server password. |
| `ACTUAL_BUDGET_ID` | The budget **Sync ID** (Settings → Advanced). |
| `ACTUAL_E2E_PASSWORD` | End-to-end encryption password, if your budget is encrypted. Leave empty otherwise. |

### Scheduling & behaviour

| Option | Description |
|--------|-------------|
| `CLASSIFICATION_SCHEDULE_CRON` | Cron expression for periodic runs. Default `0 */4 * * *` (every 4 h). |
| `FEATURES` | List of feature flags to enable (see below). |
| `NOT_GUESSED_TAG` | Note tag for transactions it could not classify. Default `#actual-ai-miss`. |
| `GUESSED_TAG` | Note tag for classified transactions. Default `#actual-ai`. |

**Available `FEATURES`:**

- `classifyOnStartup` — run a classification pass as soon as the addon starts.
- `syncAccountsBeforeClassify` — run the Actual bank sync before classifying.
  ⚠️ Off by default: it bank-syncs **every** account that has sync configured,
  and one failing account (e.g. an old/disabled one) crashes the whole run.
  Only enable it if all your synced accounts are healthy.
- `rerunMissedTransactions` — re-process transactions previously tagged as missed.
- `suggestNewCategories` — let the LLM create new categories/groups when nothing fits.
- `dryRun` — log proposed changes without applying them.
- `freeWebSearch` — DuckDuckGo-based merchant lookup (no API key needed).
- `webSearch` — ValueSerp-based merchant lookup (requires `VALUESERP_API_KEY`).
- `disableRateLimiter` — turn off the built-in request throttling.

### LLM provider

Set `LLM_PROVIDER` to one of `openai`, `anthropic`, `openrouter`,
`google-generative-ai`, `ollama`, `groq`, and fill in the matching key/model:

| Provider | Key | Model option (default) |
|----------|-----|------------------------|
| openai | `OPENAI_API_KEY` | `OPENAI_MODEL` (`gpt-4.1-mini`) |
| anthropic | `ANTHROPIC_API_KEY` | `ANTHROPIC_MODEL` (`claude-3-5-sonnet-latest`) |
| openrouter | `OPENROUTER_API_KEY` | `OPENROUTER_MODEL` (`deepseek/deepseek-v3.2`) |
| google-generative-ai | `GOOGLE_GENERATIVE_AI_API_KEY` | `GOOGLE_GENERATIVE_AI_MODEL` (`gemini-1.5-flash`) |
| groq | `GROQ_API_KEY` | `GROQ_MODEL` (`llama-3.3-70b-versatile`) |
| ollama | _(none)_ | `OLLAMA_MODEL` (`llama3.1`), `OLLAMA_BASE_URL` |

### Advanced

Anything not exposed as a named option above can be passed through
`env_vars`, e.g. `PROMPT_TEMPLATE`, `LLM_TIMEOUT_MS`, `REQUESTS_PER_MINUTE`,
`OPENAI_BASE_URL`, or `NODE_TLS_REJECT_UNAUTHORIZED=0` for a self-signed
Actual server certificate:

```yaml
env_vars:
  - name: LLM_TIMEOUT_MS
    value: "180000"
  - name: NODE_TLS_REJECT_UNAUTHORIZED
    value: "0"
```

See the [upstream README](https://github.com/sakowicz/actual-ai) for the
full list of environment variables.

## Budget cache

The addon keeps the app's budget cache **ephemeral** (re-downloaded on every
run) instead of persisting it. This is intentional: the cache stores a run
lock whose PID is always `1` inside the container, so a persisted lock would
make the addon refuse to start after a crash/restart ("Refusing to use shared
dataDir"). Re-downloading is cheap and also avoids stale-schema errors when
the Actual server migrates its schema.

## Credits

Application by **[Szymon Sakowicz](https://github.com/sakowicz)** —
[sakowicz/actual-ai](https://github.com/sakowicz/actual-ai), MIT licensed.
This repository only packages it as a Home Assistant addon.
