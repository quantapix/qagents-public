# analyzing/CLAUDE.md

VSCode extension (TS) for market inspection: DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed. Cross-project conventions (TS strict + shared tsconfigs, canonical OHLCV bar shape, GICS hub, defined-risk options rule, status hub, language split) live in repo-root `CLAUDE.md` — not duplicated here.

## Charter — two roles (spec: `data/specs/analyzing-charter-2026-07-01/SPEC.md`)

Ratified by a 7-delegate cross-qagent debate (2026-07-01). Three adopted
amendments (each subspec owns its detail): `tape-provenance-2026-07-11/`
(P8 provenance events + manifest lineage — § "History preservation" below;
kernel gets ZERO provenance predicates ever), `web-ui-trio-2026-07-11/`
(role (b) widens to **chart-presentation driver**; P4 host = Astro Node-SSR
local-only `analyzing/web/`; the monitoring+analyzing+visualizing trio
fortnight), and `ta-schema-v2-2026-07-12/` (TA schema v2 — **frozen-14
prefix, additive consumer-backed tiers**; Phases A–D shipped 2026-07-12:
+42 TA cols (56 total, `scripts/ta_custom.py` via `ta_reference.compute()`),
breadth → `financial/parquet/breadth/`, ^VIX/^VIX3M indices lane; debated
ADOPT-AMEND, record `data/debates/ta-charter-expansion-2026-07-12.md`;
open item D-1 = options-chain/IV tape).

**The schema contract has matured into a charter (2026-07-16):**
`data/charters/analyzing/tape-schema/CHARTER.md` is now the single normative
source for the tape's *shape* (frozen-14 prefix, consumer-backed tiers,
aggregate/breadth/indices lanes) — cite it, not the absorbed `ta-schema-v2`
subspec. Ratified by `data/debates/analyzing-charter-consolidation-2026-07-16.md`,
which **deferred** a `tape-supply` charter (the supplier machinery — INV-H,
the new INV-U guard, freshness manifest, provenance — changed materially
2026-07-16 and P3 is unshipped; it re-mints as a conditional charter once it
settles). The supplier invariants stay in `analyzing-charter-2026-07-01/`
meanwhile.

- **(a) Market-data supplier.** Named owner/producer of the historical
  aggregate tape — `financial/parquet/ohlcv-equities/` (`ingest.py --flat`) +
  `ta-reference/` (`ta_reference.py --flat`) — over the ~527-symbol
  S&P-500 ∪ anchor-ETF universe on locked schemas (OHLCV `ts,o,h,l,c,v,adj_c`;
  the frozen-14-prefix TA canon — 56 cols since schema-v2 Phases A+B1). Ground
  truth for `accounting/`'s kernel (file reads
  via `data_view.py`, never imports) and `trading/`'s decision-support reads
  (the live/order path stays on `alpaca_client.py`, never the tape).
- **(b) Local-only viewing surface + chart-presentation driver.** Re-homes as
  an Astro Node-SSR local-only app at `analyzing/web/` (127.0.0.1, never
  deployed; monitoring's posture) mounting `visualizing/`'s vanilla-JS kits,
  driven by the `AggregateSelection` drill-down (GICS sector ▸ industry ▸
  symbol; portfolio ▸ holdings). Run-independent, ground-truth-only — the
  complement to `evaluating/`'s run-keyed Qresev. Since 2026-07-11 analyzing
  is also the **first consumer + requirements driver for every chart-like
  (`qchart`) presentation capability** — new capabilities prove on analyzing's
  real-tape mount (or record an explicit skip) before public mounts adopt
  them; driver ≠ owner — kits stay `visualizing/`'s
  (`web-ui-trio-2026-07-11/SPEC.md`).

**Invariants audited each close** (detail: spec §§ 1.1, 2.3, 3.5):

- Files-only seam, no served API — unconditional (Lean4 inv-5; accounting
  Hard rule #6).
- Viewer renders tape only, never kernel emissions (predicate `Bool`s,
  verdicts, proof-DAG, FINANCIALLY-CLEARED signal) — those are
  `evaluating/`'s alone.
- GICS + portfolios read-only here; separate per-PM books, never a pooled
  cross-PM NAV, never an order surface.
- Freshness manifest `financial/parquet/manifest.json` (P2) with tiered
  STALE teeth — spec § 2.3. Any published/exported analyzing chart is a
  FINANCIALLY-CLEARED subject (`evaluating/` grants, `accounting/` advises).

## Batch ingest + ta_reference

`scripts/ingest.py` and `scripts/ta_reference.py` both have an additive
batch mode alongside the original single-symbol form, plus a `--flat`
mode added by `data/specs/data-charter-2026-05-17/SPEC.md` § 5 for writing
into the canonical `financial/parquet/` hub:

- Legacy per-symbol-subdir layout (no `--flat`): `ingest.py` writes
  `<DIR>/<SYM>/<SYM>.parquet`; `ta_reference.py --in-dir DIR` reads it and
  writes `<DIR>/<SYM>/ta_reference.parquet` in place.
- `ingest.py --symbols A,B,C --out-dir financial/parquet/ohlcv-equities --flat`
  — one yfinance multi-symbol download (MultiIndex split via
  `df.xs(sym, axis=1, level=1)`), writes `<DIR>/<SYM>.parquet`; per-symbol
  failures isolated into the summary `failed[]`. Post-charter canonical form.
- `ta_reference.py --in-dir financial/parquet/ohlcv-equities --out-dir financial/parquet/ta-reference --symbols A,B,C --flat`
  — reads `<in-dir>/<SYM>.parquet`, writes `<out-dir>/<SYM>.parquet`;
  `--flat` requires explicit `--out-dir`. Symbol case normalized at argparse.

The parquet hub is gitignored ground truth in the canonical checkout —
worktrees symlink to it, S3-backed (see `financial/parquet/CLAUDE.md`).
Run full refreshes from canonical so writes land in the real store.
**Worktree caveat (bit 2026-07-12):** the per-*dataset* symlinked dirs pass
writes through to canonical, but the hub-root `manifest.json` is a symlinked
*file* — `tape_manifest.py`'s atomic `os.replace` swaps the symlink itself
for a worktree-local file, silently leaving canonical stale. When running
the manifest step from a worktree, point it at the canonical root:
`--parquet-root <root>/financial/parquet`.

Both batch scripts also accept `--symbols-file FILE` (one symbol per
line; `#` comments + blank lines skipped; deduped) in place of the
`--symbols` comma list — the path for driving the full S&P 500 universe.
The canonical universe is committed at `financial/universe/sp500.txt`
(S&P 500 constituents ∪ anchor ETFs incl the 11 sector SPDRs; see
`financial/universe/CLAUDE.md`). `ingest.py` chunks the yfinance fetch
at `CHUNK = 64` symbols/request and isolates per-chunk download failures
into `failed[]`, so a 500-symbol run never rides one giant download.
Full refresh:

```
python scripts/ingest.py --symbols-file ../financial/universe/sp500.txt \
  --start 2023-01-01 --end <today> --out-dir ../financial/parquet/ohlcv-equities --flat \
  > /tmp/refresh-summary.json
python scripts/ta_reference.py --in-dir ../financial/parquet/ohlcv-equities \
  --out-dir ../financial/parquet/ta-reference --symbols-file ../financial/universe/sp500.txt --flat
python scripts/breadth.py --parquet-root ../financial/parquet
python scripts/tape_manifest.py --parquet-root ../financial/parquet \
  --refresh-summary /tmp/refresh-summary.json
```

The volatility-index lane refreshes separately (own cadence, own universe —
ta-schema-v2 § 5 Phase D; INV-H applies; NEVER run ta_reference against it):

```
python scripts/ingest.py --symbols-file ../financial/universe/indices.txt \
  --start 2023-01-01 --end <settled> --out-dir ../financial/parquet/indices --flat
```

A refresh is all four, in order (charter § 2.3 lockstep + P2; the breadth
step is ta-schema-v2 Phase C — equities-only per `financial/universe/anchors.txt`,
single implementation of the McClellan/ZBT recurrences [A-C2], materialized
to `financial/parquet/breadth/breadth.parquet`, lockstepped by the manifest
on `as_of`): the
manifest step rewrites `financial/parquet/manifest.json` (freshness
sidecar — see `financial/parquet/CLAUDE.md` § "Freshness sidecar") and,
given `--refresh-summary`, emits the P8 provenance events. Batch mode
prints one summary JSON on stdout (ingest:
`{tf,start,end,refreshed_at,allow_set,universe_sha,exit_code,written,failed,blocked,rewritten,restated}`
— non-clean entries carry `pre_sha`/`post_sha`/`backup_path`;
ta_reference: `{in_dir,written,failed}`) and ndjson per-symbol on stderr.

## History preservation — INV-H (`scripts/history_guard.py`)

**Charter invariant (spec § 2.6, acceptance A9): a refresh is monotone in
coverage.** It may add bar dates and may restate existing bars, but it MUST
NEVER reduce the set of bar dates the tape holds for a symbol.

Cut 2026-07-11 after a vendor ticker-repoint silently truncated SATS
877 → 1 bar at exit 0 (full incident: spec § 2.6). Every write is now a
**window-scoped merge**, never a truncation: with window `W=[start,end)`,
on-disk dates `E` and incoming `I ⊆ W`, the result is `(E \ W) ∪ I` —
out-of-window history survives; a narrow-`--start` re-run backfills
instead of amputating.

Per-symbol verdicts in the summary:

- `clean` / `new` — written.
- `restated` — values changed on shared dates. **Written, not refused**: with
  `auto_adjust=False` Yahoo still applies splits retroactively to raw OHLC, and
  dividends rewrite `adj_c`; blocking those would wedge the tape on routine
  corporate actions. Classified `split_like` (one uniform ratio across all bars) /
  `dividend_like` (`adj_c` only) / `irregular` (eyeball this one). The pre-write
  parquet is copied to `financial/parquet/.history-backup/<SYM>/<ISO>.parquet`.
- `regression` — the vendor dropped in-window bars we already hold ⇒ **REFUSED**.
  The parquet is left byte-identical, the symbol lands in `blocked[]`, and the run
  **exits 3** (fails the P3 cron arm; aborts `dat.sh` Step 0.5 *before* a wave
  rebases on a truncated tape).

Accepting a genuine ticker reset is explicit and **per-symbol**:
`--allow-history-rewrite SATS` (token `ALL` = deliberate full re-base). There is
no blanket disable — the operator decides per symbol, on the record, or the tape
does not change. An accepted reset overwrites **wholesale**, never merged:
splicing a pre-corporate-action series onto a post-action security fabricates
price continuity and poisons every indicator computed over it. Never "repair" a
blocked symbol by gluing an archived series onto it.

Exit codes: `0` all written · `1` all failed · `3` ≥1 symbol blocked by the guard.

**Provenance (P8, shipped 2026-07-11 — `tape-provenance-2026-07-11/SPEC.md`):**
the per-symbol verdicts no longer die on stdout — `ingest.py`'s summary is
replayed by `tape_manifest.py --refresh-summary` into the shared ledger store,
`logs.record` stream `analyzing:tape-refresh` (via `qagents.ledger.log()`;
spool-backed under `pending/ledger/`, appended **after** `.data-write-lock`
releases, never gating the refresh). One row per non-clean symbol + one
per-refresh summary row; deterministic `uuid5(refreshed_at, symbol, dataset)`
client_uids make a retry replay idempotent. Rows carry `pre_sha`/`post_sha`
lineage and, for `rewritten`, the exact `--allow-history-rewrite` `allow_set` —
the durable "on the record" for accepted resets. `.history-backup/` holds
last-5-per-symbol (pruned at backup time). The manifest (P2) additionally
carries `prev_content_sha` + a `non_clean[]` digest so accounting's wave gate
stays file-authoritative (store = audit superset, never a gate). The
`content_sha` implementation is ONE function (`tape_manifest.file_sha256` /
`dataset_content_sha`) feeding both the manifest pin and the event lineage.
Kernel-side bar (permanent): no provenance/freshness predicate ever enters
`Facts.lean`.

Tests: `../.venv/bin/pytest scripts/test_history_guard.py scripts/test_tape_manifest.py -q`
(hermetic) + the live-tape half of `data/specs/analyzing-charter-2026-07-01/tests/run.sh`.
`ta_reference.py` needs no guard — it is a pure derivation, so a blocked symbol
keeps its old bars and its TA recomputes identically.

Both scripts follow the configurable-output-path lock rule (root `CLAUDE.md`
§ "Shared-data write-lock"): `.data-write-lock` iff the resolved output falls
under canonical `data/`/`financial/`; worktree-local writes skip it. The
planned P3 cron writes direct-to-canonical under the lock — never through
`pending/` (charter spec § 2.5).

## Web viewer — `analyzing/web/` (P4 host, role (b))

Astro **Node-SSR local-only** app (charter § 3.2 re-home; web-ui-trio § 3
pins monitoring's proven shape). **127.0.0.1:4327 only** (port registry
`code/playwright/PORTS.md`), never deployed, absent from every deploy lane
(A10). Run: `pnpm -C analyzing/web dev` (or `build && preview`). Shipped
T2+T3 (P4a+P4b) 2026-07-11:

- **Symbol mount** (executes charts C5): pane 0 candlestick + volume
  (overlay scale) + SMA20/50/200 overlays, pane 1 RSI, pane 2 MACD
  (2 lines + histogram), pane 3 ADX+ATR — the R-C5 pane budget exactly
  (`data-panes` records it for the e2e floor). **Viewer toggles
  (ta-schema-v2 § 6, Phase C):** a band picker swaps pane-0 line pairs
  (Bollinger / Keltner-TTM / Donchian / SuperTrend — pairs swap, never
  stack; fills + per-segment coloring are chartered qchart requests) and a
  pane-3 picker swaps ADX+ATR ↔ ±DI in place; `/api/ta` serves the
  19-column charted subset (`TA_COLS` in `src/lib/tape.ts` is the pin).
- **AggregateSelection drill-down** (charter § 3.3): `/sectors` ▸
  `/sector/<S>` ▸ `/industry/<S>/<I>` (GICS spine via
  `gics-symbols.parquet`) and `/portfolios` ▸ `/portfolio/<slug>` —
  equal-weight composite line (LW) + coverage/weight-vs-cap bars (SVG
  backend; portfolio caps from the book's own `max_single_position_pct`).
  **Composite cohort honesty:** symbols with <80% of the cohort's max bar
  count are `excluded[]` and reported, never silently composited (the
  1-bar-SATS class of series would otherwise collapse the composite).
  **Books render separately, never pooled** (trading Hard rule #5) —
  option legs disclosed but never charted here (Qresev-only).
- **STALE chip** = host chrome (charts § 2): `FreshnessChip.astro` reads
  the P2 manifest (same truth the `/api` envelopes stamp) on every chart
  page; UNKNOWN fail-soft.

- **Data seam:** `src/lib/{tape,gics,portfolios,aggregate}.ts` read the
  hubs via DuckDB/YAML at request time; `/api/bars/<SYM>` returns the
  charts § 2 envelope `{bars, asOf?, stale?}` (freshness from
  `manifest.json`, UNKNOWN-safe), `/api/ta/<SYM>` the columnar TA
  companion (NaN warm-up = JSON null; duckdb-node surfaces parquet NaN as
  null — never `Number()` it into a fake 0), `/api/aggregate?level=…` the
  composite payload. **A12: the `/api` endpoints are intra-subproject
  viewer plumbing, never a supplier seam** — no other qagents process may
  call them (grep-audited with A4 at close). `QAGENTS_TAPE_ROOT` /
  `QAGENTS_PORTFOLIOS_ROOT` override the roots (hermetic e2e).
- **Kit delivery:** `scripts/sync-charts.mjs` (predev/prebuild) host-copies
  canonical `visualizing/graphs/dist/kit-strategy.js` → `public/graphs2/kit.js`
  (fail-soft: absent dist ⇒ empty-state, never a hard fail) + the
  `kit.css`/`tokens-chart.css` overlays from their **tracked sources** in
  `visualizing/{graphs,charts}/kit/`. The mount probes `chartsCaps()` so
  a stale copy degrades loudly. Consumes only the built `QViz` API (A7).
  **`public/graphs2/` is gitignored wholesale** — every file in it is a
  host-copy, so at `/close` the rescue gate (exit 15) lists them: **discard,
  never rescue**; `pnpm dev`/`build` regenerates all three. Same for
  `test-results/`.
- **e2e:** `pnpm -C analyzing/web test:e2e` — three chromium projects on
  port 4327 against the committed fixtures (two-symbol tape + GICS map +
  `testbook` portfolio); floors: 127.0.0.1 guard, § 2 envelope shape,
  NaN-warm-up alignment + all-null-series render, `data-ready` terminal
  states, LW canvas + SVG bar renders, STALE chip on every chart page,
  R-C5 pane cap (`data-panes` = 4), composite cohort honesty, never-pooled
  book language.
- **U1a `[shipped 2026-07-17]`** (workflow-ui § 9): the IA shell landed.
  `NavShell` (Layout-mounted flat 5-group nav — Inspect/Market live,
  Rank/Books/Tape phased-disabled; active-group marker resolves on live leaf
  routes incl. disabled Books). `/` reworked to group-cards; the symbol finder
  re-homed to `/inspect`. `/market` WF-3 (indices ^VIX/^VIX3M term-structure +
  SPY anchor regime strip, **skeleton-first server-render**). NEW seams:
  `/api/indices` (indices dataset only, no ta twin, per-dataset
  `tapeFreshness('indices')`); `src/lib/{labels.ts,citedLine.ts,regime.ts,nav.ts}`;
  `DisclosureFrame`. **The label catalog is now THE seam** — every user-facing
  event/state/threshold string passes `labels.ts`; `scripts/vocab-audit.mjs`
  mechanically enforces the IR-2 denylist + a fail-loud live lockstep harvest
  (accounting Lean ids + evaluating `FRAMEWORK_META`) + the `mirror-registry.md`
  cross-ref (typed `mirrors:`) + the citedLine grep. Run `pnpm vocab:audit`
  (folded into `verify`, owed at close). Threshold lines go through `citedLine`
  (uncited = build error). Symbol-page pickers (band/pane3) are URL-state
  (deep-link + `replaceState` writeback + unknown-param notice). `TA_COLS`
  widened `+chop14/natr14/hv_cc20/bbw20`. Next: U1b (WF-2 events + `/api/events`
  + oscillator/flow swap; next-steps item 11).
- **inv-5 (A8):** the viewer renders ground-truth tape only — no kernel
  emission, no verdict, no actionable framing. Anything exported off this
  surface becomes a FINANCIALLY-CLEARED subject (charter § 3.5).
- Meridian skin + `code/web` primitives land at T6 (web-ui-trio § 4). **T6 is
  NOT gated on monitoring** (corrected 2026-07-14 — the old "after monitoring's
  M6 fold" framing was wrong; monitoring's slot says "Nothing blocks here").
  Its two `rendering/`-side blockers both **CLEARED 2026-07-14**: the
  charts-overlay decision (rendering minted `overlay/chart-{dark,light}.css`;
  visualizing re-pointed `charts/kit/tokens-chart{,-light}.css` to byte-mirror
  it — **the light leg is net-new**) and the `--m-analyzing-*` accent mint
  (8 derivatives, both legs). **T6/M6 are now actionable** — next-steps item 7.
- **Chart colour is never host-authored.** `web/public/graphs2/` is gitignored
  generated host-copies (`sync-charts.mjs`); forking a kit stylesheet is barred.
  Series colour rides the kit's `role` → closed `seriesToken()` map. **Never
  conscript a chrome/furniture token as a data slot** — `symbol/[symbol].astro`
  does exactly that today (8 series from 5 tokens; `--chart-overlay-grid`, a
  decorative token at **1.20:1**, paints the volume histogram and every band
  pair — a data series below the a11y floor on both legs). Unwind at
  next-steps item 15, once the role tokens mint. **`--m-analyzing` is chrome
  only, never a series colour** — it is ΔE 11.2 from the projection ghost
  against a binding ΔE ≥ 18 floor (charts-series-dial debate, T1 REJECT).

## Status emit (`data/status/analyzing.json`)

`analyzing/scripts/status_emit.mjs` is the live producer for analyzing's
slot in the qagents-wide `/status` hub. Pins `KIT_VERSION` in-script
(0.7.0 today; sweep in lockstep on kit bumps — cross-subproject
contract: `qagents/CLAUDE.md` § "Status hub"). Self-contained — no
sibling-subproject imports; the only inputs are filesystem scans of
`financial/parquet/` plus `git rev-parse --short HEAD`. Today's emit
carries:

- one `DiagramEmit` (`extension-architecture` — genuine node-edge, never
  tabular) and one `DashboardEmit` (`data-coverage`): fixed-4 `KpiStrip`
  (OHLCV symbol count, TA-ref count, GICS presence, newest-bar mtime) +
  `FilterChipGroupEmit` (`coverage-filter`, `bindsTo: symbol-coverage`) +
  per-symbol `TableEmit` (`symbol-coverage`);
- `LiveState` pill: `NOT_YET_LIVE` (empty ohlcv dir); `DEGRADED` (manifest
  state STALE/DEGRADED — § 2.3 tiers incl. broken lockstep; pre-manifest
  fallback = newest-bar mtime > 7 d); else `BUILDING`. The `BUILDING → OK`
  promotion rides trio T6 (spec P4 ledger) — role (b) itself shipped 2026-07-11.

Pending-aware (`QAGENTS_PENDING_ROOT || REPO`, status-emit-cron-fleet
convention — root `CLAUDE.md` § "Status hub"); fired daily by the 05:25
`qagents:status-emit-all` fleet and at each `/close --status-emit`. Manual
canonical writes acquire `.data-write-lock`.

Full closed-set contract + display-mode catalog:
`data/specs/display-modes-2026-05-07/SPEC.md`.
