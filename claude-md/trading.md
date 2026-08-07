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
7. **Stop-losses on every equity buy**, per each PM's `risk_policy.md`. Use bracket orders. **Coverage is a claim about the BROKER, not about the ticket** — `midday-review` verifies it every day via `python -m shared.lib.risk coverage --account <pm> --orders-file <orders> --orders-status all`, which compares held quantity against live sell-stop quantity. **Fetch with `--status all`, and `--orders-status` is required** (2026-08-07): a bracket's stop leg hangs off its parent, the parent is terminal once the entry fills, so `--status open` omits both and every bracket-protected position reads naked. Under any other fetch a naked reading is `verdict: unknown`, never a breach — and on a real breach the remedy is no longer "submit the stop NOW": a duplicate stop against a resting bracket cancels the live legs via OCO, which on 2026-08-05 destroyed two of aggressive's take-profit legs and opened a ~26 s naked window. **If the broker refuses, stop and re-verify — do not improvise around the refusal**; that is the route the 08-05 damage actually took. `portfolio.json`'s `bracket.stop_loss` is the stop the PM *intended*; moderate's QQQ carried one for the whole 6h33m it sat naked on 2026-07-31 (fill landed 90 s after `open-execution` wrote it up as unfilled; the "submit the stop if and when it fills" follow-up never ran).
8. **`risk_policy.md` is edited only during `monthly-retro`**, with the change justified in `retros/YYYY-MM.md`. **The retro fires INSIDE `close-journal` on the month's last session and nowhere else** — decide month-end with `python -m shared.lib.performance next-session` (`is_last_session_of_month`), never by a weekday proxy, and never defer to "tonight's retro": there is no such fire, and July 2026's moderate retro was lost exactly that way.

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

Options tickets add a `legs` array with `strike`, `expiry`, `option_type`, `side`, `qty` per leg, plus a `structure` field — one of the defined-risk structures owned by root `qagents/CLAUDE.md` § Defined-risk options. Any ticket with a short-call leg (covered_call, composed collar) also carries `pairing: {"covering_shares": <n>}` **and** `pairing_id` (below), and must clear the book-level coverage check (`python -m shared.lib.risk composition`; enforced by `options-risk-analyzer` Step 2.5 per `data/specs/accounting-charter-expansion-2026-07-12/SPEC.md` § 8 T-C2 — leg-wise validation alone is not sufficient).

## Leg-pairing id + fills ledger (portfolio-schema v-next)

Built 2026-08-06/07 under `op:fills-ledger-ruling`. Requirements R1–R5 are the
consumer's, not ours — `accounting/predicates/hedging/BOUND-schema-requirements.md`
(consumers: `put_spread_band_ok`, `collar_bounds_computable`,
`hedge_cost_budget_leq`); read it before changing any field here.

**`pairing_id` is minted at TICKET time and never reconstructed** —
`python -m shared.lib.fills mint-id --account <pm> --underlying <sym>` — and goes
on the ticket, on every `positions[]` option leg it opens, and on every ledger
row. A pairing inferred afterwards (same underlying, same day, opposite sides) is
a guess, and the composition carve's clause (2) turns on whether a short leg is
*actually* covered: a wrong guess reads as cleared without having been cleared.
It must survive a **partial** close, or a half-closed collar reads as an
uncovered short.

**`python -m shared.lib.fills`** — per-PM append-only options premium ledger at
`agents/<pm>/fills.jsonl` (`record`/`list`/`spend`/`structure`/`mint-id`).
Options only; R4 reads the share count from `positions[]` alongside the legs.
Two properties that are not negotiable: **never pruned at position close** (a
pruned ledger serves everything else and fails once, ~a year in, when
`hedge_cost_budget_leq`'s first 252-day window needs a closed position), and a
malformed row makes `read_fills` **raise, not skip** (a skipped row lowers a
spend figure, and a spend quietly too low clears a budget that was breached).
Corrections are compensating rows, never edits.

Not the Postgres ledger store (root § write-lock), which routes *shared* files
with many appenders. This is three files, one appender each, already fenced by
`assert_account_matches_cwd`.

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
pairing_id        # options only; minted at ticket time (§ Leg-pairing id)
entry_premium     # options only; SIGNED net premium of this leg at entry
                  #   (debit negative, credit positive) — a collar is a debit
                  #   OR a credit depending on strikes, and the max-loss
                  #   arithmetic changes sign with it, so an unsigned magnitude
                  #   cannot serve. Fees included.
```

`refresh_portfolio_from_alpaca` in `shared.lib.performance` overwrites the *live* fields (`qty`, `avg_entry_price`, `market_value`, `unrealized_pl`, `side`, `asset_class`, `current_price`, `unrealized_plpc`) and preserves the rest — `pairing_id` and `entry_premium` are PM-authored, never live, and survive every refresh. Field names are exact — never use `entry_date`, never carry the alpaca-py enum repr (`PositionSide.LONG` / `AssetClass.US_EQUITY`).

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
`run_routine.sh` writes `qagents-cost` and `qagents-routine exit=` after the
dispatch returns, so a routine grepping its own log always sees it truncated.
Check a *sibling* fire instead; `exit=0 skipped=not-seat-holder` means declined
**on this host**, not "did not run anywhere". Log schema, exit codes 70-75,
pmset deltas: memory `reference_run_routine_observability.md`.

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

**The old "un-waivable gates" were Linux-target requirements, moot on a laptop
seat** — plaintext Linux OAuth, degraded repo hooks (the reason sparse checkout
excluded `legal/`), TZ drift, co-location: all dissolved unearned once both
candidate hosts were macOS laptops (same spec, "Three safety gates dissolve").
Reinstate verbatim only if a headless node ever returns.

**What still binds a session here:**

- **A tenure change lands only in the 21:00–21:59 LOCAL changeover hour**
  (§ Scheduled routines above — the CONTINUITY invariant). Between the push
  and 21:00 the lane is DARK and loud (`CHANGEOVER-DEFERRED`, `exit=75`).
- **Session ↔ cron overlap is FENCED (2026-08-02) — and the fence points at
  you.** § 12 covered host↔host handover only; SESSION-EXCLUSION (§ 12.2.2) is
  the same-host half. While an `/open trading` session holds the write-lock,
  every trading cron fire on that host **refuses**: `qagents-session-fence
  REFUSED`, `exit=76`, nothing spent. The lock it reads is the session BRANCH
  itself (`trading` / `trading-N` / `qagents`), so it releases when you
  `/close`. Practical consequence: **a session left open across a trading day
  darkens that day's chain** — close before 22:00 (`overnight-research`), or
  `touch <root>/.session-fence-override` if you are certain
  nothing is writing the PM trees. Roster is `trading` alone
  (`SESSION_FENCE_PROJECTS`).
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
  **No env override, by design** — the `QAGENTS_TRADING_ALLOW_CROSS_ACCOUNT=1` hatch was
  removed 2026-07-14 (a var a prompt can `export` is no fence). Cross-PM *reads* go
  through the unfenced `read_portfolio`; a cross-PM write would need an explicit function.
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
missing Morning Plan). **Wired into all five routines since 2026-08-02** — it had been
stated here but implemented in `premarket-brief` alone, and the other four improvised.
Two consequences now mechanical:

- **`overnight-research` uses `--next-session`, never `--date <today>`.** It fires
  22:00–23:00 ET the night *before* the session it serves, so "today" is the wrong
  day and on a Sunday is not a session at all. The improvised form left the only
  two stub journals in the tree (moderate 2026-07-19 + 07-26, both Sundays).
- **`journal open` refuses a non-session date (exit 9)**, `--allow-closed` to
  backfill. Note the deliberate asymmetry with `append_snapshot`: that guard fails
  CLOSED (unknown calendar ⇒ no mark, because it writes a derived number), this one
  fails OPEN (unknown ⇒ create it, because an empty file is harmless and a refused
  real session is not). `performance.session_state` is the tri-state read; don't
  collapse it into `is_trading_session`.

**A journal body must not repeat its own section heading** — `append_section` writes
the `## <Section>`, strips a leading echo from the body, and folds any subtitle into
the heading. The "already present" test is line-anchored, not a substring: `## Close`
also matched `## Closed positions`, which would file a Close section as an `### Update`
at end of file, under whatever section came last.

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

**A missing summary on a SESSION day is a finding, not a no-op (exit 10, 2026-08-02).**
`costs fill` used to return `written: false` with exit 0, which reads as success. On
2026-07-29 aggressive's close-journal died on an `API Error: 529 Overloaded` after
$0.56, leaving no Close section and no summary; the next morning's premarket-brief
caught the missing NAV mark and backfilled it, but nothing noticed the missing
narrative — and `costs fill`, the last fire of the day and the one holding the cost
in its hand, declined to write and reported no problem. It now refuses loudly so the
non-zero exit reaches managing checker commitment #6. Closed/unknown days keep the
quiet return. **The cost is never lost** — `costs day` reconstructs it from the logs;
the refusal is about the absent artifact. **Do not backfill the narrative**: a Close
section written days later is not a contemporaneous record, and manufacturing one is
the same failure class the session-calendar guard exists to prevent. Record the gap.

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
