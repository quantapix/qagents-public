# qagents/trading — Project Conventions

Three autonomous portfolio-management agents compete on Alpaca paper trading. Each starts with $100k and aims to beat SPY on a monthly basis. This file holds project-wide conventions that every PM and sub-agent must follow.

Cross-project conventions (shared with `analyzing/`) live in the repo root `qagents/CLAUDE.md` — in particular, the canonical OHLCV bar shape (`ts, o, h, l, c, v, adj_c`). Code here must not invent a divergent shape.

## Hard rules (never violate without explicit user override)

1. **Paper only.** All Alpaca calls must route through the paper base URL. Never call the live endpoint.
2. **Defined-risk options only.** The structure allow-list and both enforcement points (authoring skill `shared/skills/options-risk/`; runtime gate `options-risk-analyzer` on every ticket) are owned by root `qagents/CLAUDE.md` § Defined-risk options. Both gates must remain in force; a gate failure is a decision input, never an error to retry around.
3. **Not day trading.** Holding horizons are days to months (see each PM's `strategy.md`). The midday routine biases toward doing nothing; only act on a material new event.
4. **Risk gate before execution.** Every equity ticket is cleared by `risk-analyzer`, every options ticket by `options-risk-analyzer` *and* `risk-analyzer`, before `trade-executor` places it.
5. **Separate capital per PM.** The three PMs never share positions, cash, or Alpaca accounts. Each has its own paper key-pair, `portfolio.json`, strategy doc, and journal tree.
6. **Journal before quitting.** A routine that places or modifies a position must append the reasoning to `journal/YYYY-MM-DD.md` before exiting. If journaling fails, treat the run as failed.
7. **Stop-losses on every equity buy**, per each PM's `risk_policy.md`. Use bracket orders.
8. **`risk_policy.md` is edited only during `monthly-retro`**, with the change justified in `retros/YYYY-MM.md`.

## Model assignment

- PM-level reasoning (strategy, trade selection, retros): the **latest top-tier model** (`opus`).
- Sub-agents (tactical data pulls, order placement, risk math, journaling, news triage): cheaper models (sonnet/haiku split per root model policy) as pinned in each agent definition in `.claude/agents/`.
- Never promote a sub-agent to the top tier without updating its agent definition and documenting the reason.

The sub-agent roster lives once at the project level in `.claude/agents/` and is shared by every PM (each PM's charter notes only its own usage emphasis):

| Need | Sub-agent |
|---|---|
| Quotes, bars, options chains for specific tickers | `market-data-fetcher` |
| Triage Alpaca news for a ticker list | `news-scanner` |
| Deep, cited macro/sector/company research (overnight + monthly only) | `deep-researcher` |
| Gate an equity or options ticket against risk policy | `risk-analyzer` |
| Compute max-loss / Greeks for a proposed options structure | `options-risk-analyzer` |
| Place a validated ticket on Alpaca paper | `trade-executor` |
| Append a journal entry | `journal-writer` |
| Daily / monthly performance report vs SPY | `performance-reporter` |

## Per-PM layout

Every `agents/<pm>/` dir carries the same file set (semantics owned here; each PM charter lists only its scope line):

- `strategy.md` — living strategy doc; edited at `monthly-retro` only.
- `risk_policy.md` — hard limits; YAML front-matter parsed by `shared/lib/risk.py`; edited at `monthly-retro` only (hard rule 8).
- `watchlist.md` — active watchlist; maintained by `overnight-research`.
- `portfolio.json` — local source of truth for cash, positions, NAV history; reconciled against Alpaca at each `close-journal`.
- `journal/YYYY-MM-DD.md` — one per trading day (Morning Plan, Morning Execution, Midday, Close).
- `summaries/YYYY-MM-DD.md` — short end-of-day summary.
- `retros/YYYY-MM.md` — monthly retrospective with concrete strategy deltas.
- `research/YYYY-MM-DD.md` — dated deep-research output (overnight + monthly).

## Data sources

- Market data + primary news: Alpaca (`python -m shared.lib.alpaca_client`). This is the only execution-path data source.
- Optional deep research: Perplexity via `shared/lib/perplexity_client.py`, invoked only by `overnight-research` and `monthly-retro`. If `PERPLEXITY_API_KEY` is unset, the sub-agent returns `{available: false}` and the caller falls back to `news-scanner` + Claude WebSearch. Do not call Perplexity from intraday routines.

## Bull-vs-bear debate (decision skill)

`shared/skills/bull-bear-debate/` lets any PM run a parallel **bull vs
bear** AI-session debate on one candidate symbol, then **hard-gate** the
verdict through `accounting/`'s Lean kernel before it becomes a ticket.
Evidence is already-reported data/news/trends (`watchlist.md` + journal +
`news-scanner`) plus the analyzing-side TA-reference parquet — no new data
source. Mechanics in `shared/lib/debate.py` (`bundle` + refuse-closed
`gate`); advocates `bull-debater` / `bear-debater` (model pinned in their agent
definitions). The gate
is a **veto, not a vote** (mirrors the options-risk hard-refuse posture);
a passing verdict still clears `risk-analyzer` (+ `options-risk-analyzer`)
→ `trade-executor`. Gate coverage: TREND `is_uptrend` over the analyzing
S&P 500 parquet universe (~526 symbols, via the canonical
`financial/parquet` worktree symlink); abstains on names outside it.

## Order ticket schema

Every proposed trade is represented as a JSON ticket before it hits the risk gate:

```json
{
  "account": "aggressive|moderate|conservative",
  "symbol": "AAPL",
  "asset_class": "equity|option",
  "side": "buy|sell",
  "qty": 10,
  "order_type": "market|limit|stop|stop_limit",
  "limit_price": 187.50,
  "time_in_force": "day|gtc",
  "bracket": { "take_profit": 195.00, "stop_loss": 180.00 } ,
  "thesis_tag": "momentum|value|mean-reversion|hedge|income|event|core",
  "thesis": "One- to three-sentence rationale.",
  "expected_exit": "Condition or date."
}
```

Options tickets add a `legs` array with `strike`, `expiry`, `option_type`, `side`, `qty` per leg, plus a `structure` field — one of the defined-risk structures owned by root `qagents/CLAUDE.md` § Defined-risk options.

## Journal entry schema

Each `journal/YYYY-MM-DD.md` has four sections appended through the day:

1. **Morning Plan** — watchlist, draft tickets, macro framing (from `premarket-brief`).
2. **Morning Execution** — actual fills, deviations from plan, reasons (from `open-execution`).
3. **Midday** — portfolio state snapshot, any adjustments (from `midday-review`).
4. **Close** — EOD marks, day return vs SPY, lessons (from `close-journal`).

The `journal-writer` sub-agent appends these sections; PMs draft the content.

## Python module invocation

All Python helpers are invoked as modules so they share the package namespace:

```
python -m shared.lib.alpaca_client <cmd> [flags]
python -m shared.lib.performance <cmd> [flags]
python -m shared.lib.options_math <cmd> [flags]
python -m shared.lib.risk <cmd> [flags]
python -m shared.lib.perplexity_client <cmd> [flags]
```

All commands accept `--account {aggressive|moderate|conservative}` where relevant and emit JSON on stdout for programmatic parsing.

**SPY benchmark + alpha figures** must come from `python -m shared.lib.performance daily --account <pm>` (or `leaderboard`), never estimated in chat. The module fetches 15-min-delayed SIP via Alpaca and reconciles fund vs SPY in one place. The daily report exposes `spy_day_return` and `day_alpha_bps` directly so all three PMs cite identical numbers; `spy_unavailable: true` is the explicit "halt and back-fill at next run" signal — never paraphrase a SPY number from news scans when it's set. `n_snapshots` is the running history length; below 30, stamp Sharpe/Sortino with the noisy-history disclaimer.

`python -m shared.lib.performance snapshot` refreshes positions + cash from Alpaca by default before appending a `nav_history` entry. Pass `--no-refresh` only when the caller has already merged broker state into `portfolio.json`; otherwise the snapshot may use stale `market_value`.

Typecheck edits with `pyright <file>` before declaring them done — config is in `pyproject.toml`. `ruff check <file>` for lint.

### Agent SDK wrapper — `qagents.agent_sdk`

`qagents.agent_sdk` (at `code/agent_sdk/qagents/agent_sdk/`) is the typed wrapper around `claude-agent-sdk` for cron-fired and library-callable Claude work. Root `CLAUDE.md` § "Programmatic Claude — Agent SDK lane" owns lane status (paused/reverted); full contract in `data/specs/agent-sdk-adoption-2026-05-17/SPEC.md`.

## Position schema (portfolio.json)

Every `agents/<pm>/portfolio.json` `positions[]` entry uses one canonical shape, in this field order:

```
symbol            # ticker, uppercased
asset_class       # "equity" | "option"
side              # "long" | "short"
qty               # number; contracts for options
avg_entry_price   # per-share / per-contract
current_price     # last mark from Alpaca; null if unknown
market_value      # qty * current_price
unrealized_pl
unrealized_plpc
thesis_tag        # momentum|value|mean-reversion|hedge|income|event|core
thesis            # optional long-form rationale
entered_at        # YYYY-MM-DD (NOT entry_date)
order_id          # Alpaca order id of the opening fill
bracket           # { take_profit, stop_loss, ... }
bracket_status    # optional free-form annotation
```

`refresh_portfolio_from_alpaca` in `shared.lib.performance` overwrites the *live* fields (`qty`, `avg_entry_price`, `market_value`, `unrealized_pl`, `side`, `asset_class`, `current_price`, `unrealized_plpc`) and preserves the rest. Field names are exact — never use `entry_date`, never carry the alpaca-py enum repr (`PositionSide.LONG` / `AssetClass.US_EQUITY`).

## Scheduled routines

The 16 trading LaunchAgents (3 PMs × 5 cron routines + leaderboard) are
registered through the canonical qagents launchd scheduler at
`data/schedules/`. Per-routine spec rows live in `data/schedules/cron_triggers.md`;
hand-run any routine off-schedule via
`data/schedules/launchd/run_routine.sh trading/<pm> <routine>` (e.g.
`trading/aggressive overnight-research`). Per-run logs at
`data/schedules/launchd/logs/trading-<pm>-<routine>-*.log`. Operator
runbook at `data/schedules/Notes.md`.

### Cron-lane vs manual-lane producer contract (`pending/` migration)

Trading producers haven't migrated yet — opportunistic per
`data/specs/data-conventions-2026-05-06/SPEC.md` § 10 step 8 (pick up when
next touching any PM prompt, per-PM skill, or trading sub-agent). Contract
in root `qagents/CLAUDE.md` § "Shared-data write-lock". State files
(`portfolio.json`, `watchlist.md`) stay canonical in both lanes — read by
the next same-day cron fire, can't stage behind the once-daily verifier
(spec § 6).

**Cron-lane path discipline (load-bearing).** A cron fire runs
`run_routine.sh` → `claude --print "/<routine>"` with cwd already at the
canonical `trading/agents/<pm>` dir. The skills name outputs cwd-relative
(`watchlist.md`, `research/YYYY-MM-DD.md`) — write them **exactly there**,
to canonical cwd-relative paths. The root `qagents/CLAUDE.md`
worktree-path-discipline rule ("every Edit/Write `file_path` MUST begin
with `<root>-wt/<branch>/`") is **interactive-`/open`-only**
and MUST NOT be applied here: there is no session branch, so prefixing a
`qagents-wt/<branch>/` root fabricates a stray directory whose output is
orphaned and never promoted (caused the 2026-06-02 moderate miss — files
landed in `qagents-wt/trading-13/`, absent from the daily-promotion commit).

### Cron-EC2 lane

`data/specs/cron-ec2-migration-2026-05-19/SPEC.md` moves the 16 trading
routines off the operator's laptop onto `qagents-app-1`. Trading owns the
per-PM `routines.toml` cells, the one-time state-cache rsync into
`/srv/qagents-state/trading/<pm>/`, and per-PM enablement in rollout order
conservative → moderate → aggressive → leaderboard (spec Phases 2–5;
current status in the spec's Phase ledger). All AWS-touching artifacts are
`serving/`-owned (`serving/CLAUDE.md` § 8.6); trading never touches AWS
state directly.

## Monthly retro + leaderboard

- **Monthly retro fires inside `close-journal` on the last trading day of the calendar month, never elsewhere.** First trading day of the next month must not re-trigger it. Premarket-briefs occasionally carry stale "monthly-retro <date>" forward-references the morning after a retro fired — ignore unless the hook itself misbehaved.
- **Leaderboard artifact**: `financial/reports/leaderboard.md` is the source of truth. Column header is **"Fund return" = cumulative-since-seed**, not MTD. Routine chat summaries sometimes use "MTD" loosely; on the first/last trading day of a month the two values diverge from cum return — trust the artifact column.

## Cost accounting

Each `summaries/YYYY-MM-DD.md` ends with a cost line:
```
Cost: Claude $X.XX (top-tier $A / Sonnet $B / Haiku $C), Perplexity $Y.YY, total $Z.ZZ
```
Claude Code emits per-run token usage; Perplexity returns usage in its response body. The `performance-reporter` sums these.

## Status emit (`data/status/trading.json`)

Producer: `trading/scripts/status_emit.py` (system `python3`, no venv;
`KIT_VERSION` pinned in-script — sweep with all pins on kit bumps,
never restate the literal in prose): per-PM NAV +
snapshot count + portfolio.json age + total NAV + leaderboard age,
with a `pm-cohort` diagram (3 PMs → risk-analyzer / options-risk-analyzer
→ trade-executor → Alpaca paper). `live.status` flips OK / DEGRADED /
NOT_YET_LIVE on portfolio.json freshness (<72 h). Honors
`QAGENTS_PENDING_ROOT` for the cron lane. Contract: root
`qagents/CLAUDE.md` § "Status hub".
