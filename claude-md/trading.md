# qagents/trading — Project Conventions

Three autonomous portfolio-management agents compete on Alpaca paper trading. Each starts with $100k and aims to beat SPY on a monthly basis. This file holds project-wide conventions that every PM and sub-agent must follow.

Cross-project conventions (shared with `analyzing/`) live in the repo root `qagents/CLAUDE.md` — in particular, the canonical OHLCV bar shape (`ts, o, h, l, c, v, adj_c`). Code here must not invent a divergent shape.

## Hard rules (never violate without explicit user override)

1. **Paper only.** All Alpaca calls must route through the paper base URL. Never call the live endpoint.
2. **Defined-risk options only.** Allowed structures: long calls, long puts, debit spreads (call or put), covered calls, protective puts. No naked shorts, credit spreads, iron condors, or any structure whose max loss cannot be computed at trade time. Enforced at two points: the `options-risk` skill (`shared/skills/options-risk/`) gates *authoring* of options code; the `options-risk-analyzer` sub-agent gates *every ticket* at runtime. Both must remain in force.
3. **Not day trading.** Holding horizons are days to months (see each PM's `strategy.md`). The midday routine biases toward doing nothing; only act on a material new event.
4. **Risk gate before execution.** Every equity ticket is cleared by `risk-analyzer`, every options ticket by `options-risk-analyzer` *and* `risk-analyzer`, before `trade-executor` places it.
5. **Separate capital per PM.** The three PMs never share positions, cash, or Alpaca accounts. Each has its own paper key-pair, `portfolio.json`, strategy doc, and journal tree.
6. **Journal before quitting.** A routine that places or modifies a position must append the reasoning to `journal/YYYY-MM-DD.md` before exiting. If journaling fails, treat the run as failed.

## Model assignment

- PM-level reasoning (strategy, trade selection, retros): the **latest top-tier model** (`opus`).
- Sub-agents (tactical data pulls, order placement, risk math, journaling, news triage): **Haiku 4.5** or **Sonnet 4.6** per their agent definition in `.claude/agents/`.
- Never promote a sub-agent to the top tier without updating its agent definition and documenting the reason.

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
`gate`); advocates `bull-debater` / `bear-debater` (Sonnet 4.6). The gate
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

Options tickets add a `legs` array with `strike`, `expiry`, `option_type`, `side`, `qty` per leg, plus a `structure` field (`long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`).

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

`qagents.agent_sdk` (at `code/agent_sdk/qagents/agent_sdk/`) is the typed wrapper around `claude-agent-sdk` for cron-fired and library-callable Claude work; the SDK lane is **cron-only** today and routines opt in by suffixing `:sdk` in `data/schedules/launchd/install.sh` ROUTINES. Full contract — install, public-API stability surface, billing — in root `CLAUDE.md` § "Programmatic Claude — Agent SDK lane" and `data/specs/agent-sdk-adoption-2026-05-17/SPEC.md`.

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
`data/specs/data-conventions-2026-05-06/SPEC.md` § 10.8 (pick up when next
touching a PM prompt, the per-PM close-journal / overnight-research
skills under `agents/<pm>/.claude/skills/`, the `journal-writer` /
`performance-reporter` sub-agents under `.claude/agents/`, or the
`leaderboard` routine — which is `python -m shared.lib.performance
leaderboard` + `performance-reporter`, *not* a `shared/skills/` entry;
`shared/skills/` holds `options-risk` + `backtest-runner` +
`bull-bear-debate`). Contract lives in the root
`qagents/CLAUDE.md` "Shared-data write-lock" section. State files
(`portfolio.json`, `watchlist.md`) stay canonical in both lanes — they're
read by the next same-day cron fire and can't stage behind managing's
once-daily verifier (spec § 6).

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

### Cron-EC2 lane (`data/specs/cron-ec2-migration-2026-05-19/SPEC.md`)

Moves the 16 trading routines (5 × 3 PMs + leaderboard) off the operator's
laptop onto `qagents-app-1`. The trading session owns the per-PM
`routines.toml` cells, the one-time per-PM state-cache rsync into
`/srv/qagents-state/trading/<pm>/`, and the phase-by-phase enablement of
conservative → moderate → aggressive → leaderboard timers (Phases 2–5 of
the spec). All AWS-touching artifacts (CDK, EC2 scripts, IAM, SSM, log
groups) are `serving/`-owned — tracked in `serving/CLAUDE.md § 8.6`.
Trading never touches AWS state directly.

**Phase 2 PM-rollout procedure.** Infrastructure on `qagents-app-1` is
operationally live as of 2026-05-23 Stage 2; per-PM SSM kill-switches
`/qagents/cron/trading/<pm>/enabled` default to `false`. Rollout order
is conservative → moderate → aggressive with one-week parity observation
between PMs. Full operational steps (state-cache rsync, SSM flip,
install/deploy/systemctl-enable sequence) in `serving/CLAUDE.md § 8.6`.

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
