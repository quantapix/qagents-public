# qagents/trading — Project Conventions

Three autonomous portfolio-management agents compete on Alpaca paper trading. Each starts with $100k and aims to beat SPY on a monthly basis. This file holds project-wide conventions that every PM and sub-agent must follow.

Cross-project conventions live in the repo root `qagents/CLAUDE.md`. The canonical OHLCV bar shape is owned by `financial/parquet/CLAUDE.md` § "Canonical OHLCV bar shape" — code here must not invent a divergent shape.

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

- PM-level reasoning (strategy, trade selection, retros): the **latest top-tier model**.
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

`shared/skills/bull-bear-debate/` runs a parallel bull-vs-bear AI-session
debate on one candidate symbol (advocates `bull-debater` / `bear-debater`),
then hard-gates the verdict through `accounting/`'s Lean kernel before it can
become a ticket. Mechanics + evidence sources in `shared/lib/debate.py`
(`bundle` + refuse-closed `gate`); no new data source. The gate is a **veto,
not a vote** (mirrors the options-risk hard-refuse posture); a passing verdict
still clears `risk-analyzer` (+ `options-risk-analyzer`) → `trade-executor`.
Gate coverage: TREND `is_uptrend` over the analyzing S&P 500 parquet universe
(canonical `financial/parquet` worktree symlink); abstains on names outside it.

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

Options tickets add a `legs` array with `strike`, `expiry`, `option_type`, `side`, `qty` per leg, plus a `structure` field — one of the defined-risk structures owned by root `qagents/CLAUDE.md` § Defined-risk options. Any ticket with a short-call leg (covered_call, composed collar) also carries `pairing: {"covering_shares": <n>}` and must clear the book-level coverage check (`python -m shared.lib.risk composition`; enforced by `options-risk-analyzer` Step 2.5 per `data/specs/accounting-charter-expansion-2026-07-12/SPEC.md` § 8 T-C2 — leg-wise validation alone is not sufficient).

## Journal entry schema

Each `journal/YYYY-MM-DD.md` has four sections appended through the day:

1. **Morning Plan** — watchlist, draft tickets, macro framing (from `premarket-brief`).
2. **Morning Execution** — actual fills, deviations from plan, reasons (from `open-execution`).
3. **Midday** — portfolio state snapshot, any adjustments (from `midday-review`).
4. **Close** — EOD marks, day return vs SPY, lessons (from `close-journal`).

The `journal-writer` sub-agent appends these sections; PMs draft the content.

## Python module invocation

All Python helpers are invoked as modules — `python -m shared.lib.<name> <cmd> [flags]` — so they share the package namespace (current set: `ls shared/lib/`; conventions in `shared/CLAUDE.md`). Commands accept `--account {aggressive|moderate|conservative}` where relevant and emit JSON on stdout for programmatic parsing.

**SPY benchmark + alpha figures** must come from `python -m shared.lib.performance daily --account <pm>` (or `leaderboard`), never estimated in chat. The module fetches 15-min-delayed SIP via Alpaca and reconciles fund vs SPY in one place. The daily report exposes `spy_day_return` and `day_alpha_bps` directly so all three PMs cite identical numbers; `spy_unavailable: true` is the explicit "halt and back-fill at next run" signal — never paraphrase a SPY number from news scans when it's set. `n_snapshots` is the running history length; below 30, stamp Sharpe/Sortino with the noisy-history disclaimer.

`python -m shared.lib.performance snapshot` refreshes positions + cash from Alpaca by default before appending a `nav_history` entry. Pass `--no-refresh` only when the caller has already merged broker state into `portfolio.json`; otherwise the snapshot may use stale `market_value`.

Typecheck edits with `pyright <file>` before declaring them done — config is in `pyproject.toml`. `ruff check <file>` for lint.

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

**A host that can reach the repo is not a host that can trade.** Git does
not carry trading's state on its own: the tape (`financial/parquet/`) and
the creds (`trading/.env`) are **gitignored**, laptop-local; each PM's live
`portfolio.json` is **TRACKED** but only as fresh as the last push — so a
checkout that fires a routine without the holder's latest push reasons
over a pre-session book and writes it back over the real one.
Before any seat/host move, sync + hash-match all three (the 2026-07-14
seat drill caught exactly this pre-flip). 2026-07-23 added the converse:
**a host that has the tape and the creds still cannot trade on a stale
checkout** — qyel passed every gate, including `seat_preflight` GREEN
24/24, and reported "no Morning Plan existed today" because its `main`
predated the plan commit by 96 minutes. Tracked state matters as much as
gitignored state. (A dead `py_vollib` that `pip check` read clean also
blocked Greeks; both `parity.sh` and `capability.sh` gained import
witnesses 2026-07-27.)

**THE ROUTINE ROSTER IS A SET OF DEPENDENCY CHAINS, NOT INDEPENDENT
FIRES.** `overnight-research → premarket-brief → open-execution →
midday-review → close-journal → leaderboard` is one chain per PM, and the
medium it hands state along is **tracked files in this repo** (the
journal, `portfolio.json`, `watchlist.md`). A chain must therefore run
start-to-finish on ONE host. The seat gate proved exclusivity and
capability but not this — so a flip pushed mid-morning on 2026-07-23
split a day across both laptops and a pre-committed AMD ticket was never
placed, with every gate verdict correct and nothing raising a finding.
Mechanized since as the seat's third invariant, **CONTINUITY**: a tenure
may only BEGIN in the 21:00–21:59 local changeover hour, and the incoming
host fast-forwards `main` to the authority or refuses (`exit=75`;
`data/specs/node-return-lane-2026-07-14/SPEC.md` § 12). Practical
consequence for this subproject: **a seat flip no longer takes effect
when it is pushed** — flip in the evening, never during a trading day.

**Do not diagnose the health of the fire you are running inside.**
`run_routine.sh` writes `qagents-cost` and `qagents-routine exit=` after
the dispatch returns, so a routine grepping its own log always sees it
truncated and can only conclude it crashed. To check a *sibling* fire,
grep that sibling's log for `qagents-routine exit=` — and note
`exit=0 skipped=not-seat-holder` means the routine was correctly declined
**on this host**, not that it did not run anywhere. On a two-host lane
those are different facts and only the first is locally visible; that
distinction is exactly what the 2026-07-23 journals got wrong.

The 16 trading LaunchAgents (3 PMs × 5 cron routines + leaderboard) are
registered through the canonical qagents launchd scheduler at
`data/schedules/`. **Schedule times are owned by the `ROUTINES` array in
`data/schedules/launchd/install.sh`** (post-D1 2026-07-25);
`data/schedules/cron_triggers.md` is trading-lane *narration* (timing
rationale, per-routine prose) — read it for why, never for when.
Hand-run any routine off-schedule via
`data/schedules/launchd/run_routine.sh trading/<pm> <routine>` (e.g.
`trading/aggressive overnight-research`). Per-run logs at
`data/schedules/launchd/logs/trading-<pm>-<routine>-*.log`. Operator
runbook at `data/schedules/Notes.md`.

### Cron-lane vs manual-lane producer contract (`pending/` migration)

Trading producers haven't migrated to `pending/` yet — pick the migration up
opportunistically when next touching any PM prompt, per-PM skill, or trading
sub-agent. Contract in root `qagents/CLAUDE.md` § "Shared-data write-lock".
State files (`portfolio.json`, `watchlist.md`) stay canonical in both lanes —
read by the next same-day cron fire, they can't stage behind the once-daily
verifier (`data/specs/data-conventions-2026-05-06/SPEC.md` § 6).

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

### Relocation lane — DONE, onto the qyel seat (not a LAN node)

**Relocated 2026-07** (re-derived 2026-07-27). The cron lane runs on
**qyel — a macOS laptop holding
its own subscription seat**, not a headless herdr/EC2 node: qblk/qred cannot
hold a seat at all. qpur is freed, which was the entire driver (§ 0 — it could
not leave the WiFi while it served cron). Live program + mechanism:
`data/specs/node-return-lane-2026-07-14/SPEC.md` (seat gate, § 12 changeover
discipline, S5 write-back). The herdr-transport spec
(`cron-ec2-migration-2026-05-19/trading-herdr-sessions-2026-07-14/SPEC.md`) is
retained as the design record, trued 2026-07-27; debate record:
`data/debates/trading-node-relocation-2026-07-14.md`.

**Most of the old "un-waivable gates" were Linux-target requirements and are
moot on a laptop seat** — reinstate them verbatim if a headless node ever
returns. Sparse checkout excluding `legal/` was mandated because repo hooks
*fail open on Linux*, so subtraction was the only enforcement; on macOS they
run, and qyel carries the full canonical checkout. TZ pinning is satisfied by
construction (same macOS launchd lane, same ET local time). Co-location is
satisfied — all three PMs and the leaderboard on one host.

**What still binds a session here:**

- **A tenure change lands only in the 21:00–21:59 LOCAL changeover hour**
  (§ Scheduled routines above — the CONTINUITY invariant). Between the push
  and 21:00 the lane is DARK and loud (`CHANGEOVER-DEFERRED`, `exit=75`).
- **Session ↔ cron overlap is NOT yet fenced** (`ns:trading/1`). § 12 covers
  host↔host handover only; an `/open trading` session and the cron lane on the
  *same* host still write `portfolio.json` / `watchlist.md` / journals with no
  lease between them, and those are read-after-write within one trading day.
  Assume nothing protects you here.
- `.claude/**`, `risk_policy.md` and `strategy.md` remain outside any
  machine-writable allow-list. AWS-touching artifacts stay `serving/`-owned.

## Monthly retro + leaderboard

- **Monthly retro fires inside `close-journal` on the last trading day of the calendar month, never elsewhere.** First trading day of the next month must not re-trigger it. Premarket-briefs occasionally carry stale "monthly-retro <date>" forward-references the morning after a retro fired — ignore unless the hook itself misbehaved.
- **Leaderboard artifact**: `financial/reports/leaderboard.md` is the source of truth. Column header is **"Fund return" = cumulative-since-seed**, not MTD. Routine chat summaries sometimes use "MTD" loosely; on the first/last trading day of a month the two values diverge from cum return — trust the artifact column.

## Session guard + write-fence (mechanical, not advisory)

Two hard rules are enforced in `shared/lib/`, not by prompt discipline — both after
the 2026-07-14 audit found them already breached in committed artifacts:

- **Write-fence.** A PM writes only its own tree. `_common.assert_account_matches_cwd`
  refuses (exit 7) any `--account` that disagrees with the `agents/<pm>` directory the
  routine is running in; it guards `write_portfolio`, `journal append/open/summary` and
  `costs fill`. Hard rule 5 (separate capital) had already been broken once —
  `conservative/journal/2026-07-01.md` carried a verbatim copy of *moderate's* close.
  Escape hatch for genuine cross-PM readers (leaderboard) + tests:
  `QAGENTS_TRADING_ALLOW_CROSS_ACCOUNT=1`.
- **Session calendar.** `performance.is_trading_session` (Alpaca's calendar,
  fails closed) gates `snapshot` and `daily`. **A closed day produces no NAV mark, no
  day-return, no alpha, and no model spend.** Marking a shut tape is what produced the
  phantom-alpha and fabricated-session incidents of 06-19/07-03. Check it first:
  `python -m shared.lib.performance
  is-session --date <d>`. Backfilling a day the calendar is genuinely wrong about needs
  an explicit `--allow-closed`.

**Every routine opens its journal before it starts spending** —
`python -m shared.lib.journal open --account <pm> --date <today>`. A mid-run kill then
degrades to a thin journal instead of none at all (2026-07-14: moderate's premarket-brief
burned its whole budget and wrote nothing, leaving `open-execution` to fire against a
missing Morning Plan).

## Cost accounting

Each `summaries/YYYY-MM-DD.md` ends with a cost line, back-filled by the `leaderboard`
routine (16:45 — the last fire of the day; a routine cannot report its own cost, since
the figure only exists once its process has exited):

```
python -m shared.lib.costs fill --account <pm>     # writes the line
python -m shared.lib.costs day  --account <pm>     # just report it
```

The source is the `qagents-cost cost_usd=…` line that `run_routine.sh` appends to
every per-run log. Runs with no cost line (crashes, cap kills, pre-telemetry logs)
are reported as `unpriced_runs`, never silently counted as $0.

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
