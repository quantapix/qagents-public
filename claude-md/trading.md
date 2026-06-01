# trading — portfolio-management agents

Three autonomous portfolio-management agents compete on a **paper-trading**
broker. Each starts with the same notional capital and aims to beat the
benchmark on a monthly basis. Part of the financial-domain slice published
at `qresev-public`. Cross-project conventions (shared with `analyzing/`)
live in the root `CLAUDE.md` — in particular the canonical OHLCV bar shape
`{ts, o, h, l, c, v, adj_c}`. Code here must not invent a divergent shape.

## Hard rules (never violate without explicit override)

1. **Paper only.** All broker calls route through the paper endpoint. Never
   call the live endpoint.
2. **Defined-risk options only.** Allowed: long calls, long puts, debit
   spreads (call or put), covered calls, protective puts. No naked shorts,
   credit spreads, iron condors, or any structure whose max loss cannot be
   computed at trade time. Enforced at two points — an authoring skill gates
   options *code*; a runtime analyzer sub-agent gates *every ticket*.
3. **Not day trading.** Holding horizons are days to months. The midday
   routine biases toward doing nothing; it acts only on a material new
   event.
4. **Risk gate before execution.** Every equity ticket clears a risk
   analyzer; every options ticket clears the options-risk analyzer *and* the
   risk analyzer, before an executor places it.
5. **Separate capital per agent.** The three agents never share positions,
   cash, or broker accounts. Each has its own key-pair, portfolio, strategy
   doc, and journal tree.
6. **Journal before quitting.** A routine that places or modifies a position
   appends its reasoning to a dated journal before exiting; if journaling
   fails, the run is failed.

## Model assignment

- Agent-level reasoning (strategy, trade selection, retros): the top
  individual tier.
- Sub-agents (tactical data pulls, order placement, risk math, journaling,
  news triage): the cost-appropriate smaller tiers per their agent
  definition. Never promote a sub-agent to the top tier without updating its
  definition and documenting the reason.

## Data sources

- Market data + primary news: the paper broker's data API — the only
  execution-path data source.
- Optional deep research: an external research provider, invoked only by the
  overnight-research and monthly-retro routines; if its key is unset, the
  caller falls back to a news-scanner + web search. Not called from intraday
  routines.

## Bull-vs-bear debate (decision skill)

Any agent can run a parallel **bull vs bear** AI-session debate on one
candidate symbol, then **hard-gate** the verdict through `accounting/`'s
Lean kernel before it becomes a ticket. Evidence is already-reported
data / news / trends plus the analyzing-side TA-reference parquet — no new
data source. The gate is a **veto, not a vote** (mirrors the options-risk
hard-refuse posture); a passing verdict still clears the risk analyzers
before placement. Gate coverage: the `Trend.is_uptrend` judgment over the
analyzing-side S&P 500 universe; it abstains on names outside it.

## Order ticket + journal + position schemas

Every proposed trade is a JSON ticket (`account`, `symbol`, `asset_class`,
`side`, `qty`, `order_type`, `limit_price`, `time_in_force`, `bracket`,
`thesis_tag`, `thesis`, `expected_exit`) before it hits the risk gate;
options tickets add a `legs` array plus a `structure` field naming one of
the six allowed strategies. Each dated journal has four sections appended
through the day (Morning Plan / Morning Execution / Midday / Close). Each
portfolio position uses one canonical field shape; field names are exact
(e.g. `entered_at`, never `entry_date`), and a refresh helper overwrites the
live fields while preserving the rest.

## Python module invocation

All Python helpers are invoked as modules so they share the package
namespace (`python -m shared.lib.<mod> <cmd> [flags]`). Commands accept
`--account {aggressive|moderate|conservative}` where relevant and emit JSON
on stdout. **Benchmark + alpha figures** must come from the performance
module, never estimated in chat — it reconciles fund vs benchmark in one
place so all three agents cite identical numbers. Typecheck edits with
`pyright` before declaring them done; `ruff check` for lint.

### Agent SDK wrapper

The typed wrapper around the programmatic SDK is used for cron-fired and
library-callable work; the SDK lane is cron-only today and routines opt in
by suffixing `:sdk` in the schedule. Full contract in the root `CLAUDE.md`.

## Scheduled routines

The 16 trading routines (3 agents × 5 cron routines + a leaderboard) are
registered through the canonical launchd scheduler; any routine can be
hand-run off-schedule. Producers haven't migrated to the cron-staging lane
yet — opportunistic, picked up when next touching a routine. State files
(portfolio, watchlist) stay canonical in both lanes since they're read by
the next same-day fire.

A cron-EC2 lane moves the routines off the laptop onto a shared instance,
enabled agent-by-agent with parity observation; all AWS-touching artifacts
are owned by `serving/`. Before the 2026-06-15 credit activation, each
scheduled programmatic fire bills at API per-token rates, so PM-timer
enablement is weighed against that cost window.

## Monthly retro + leaderboard

The monthly retro fires inside the close routine on the last trading day of
the calendar month, never elsewhere. The leaderboard artifact is the source
of truth; its "Fund return" column is cumulative-since-seed, not MTD —
trust the artifact column when chat summaries use "MTD" loosely.

## Status emit (`data/status/trading.json`)

`trading/scripts/status_emit.py` emits per-agent NAV + snapshot count +
portfolio freshness + total NAV + leaderboard age, with a cohort diagram
(3 agents → risk analyzer / options-risk analyzer → executor → paper
broker). The live pill flips on portfolio freshness. Self-contained.
