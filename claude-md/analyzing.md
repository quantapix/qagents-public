# analyzing/CLAUDE.md

Market-inspection tooling (TypeScript; local-only viewer): DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed. Cross-project conventions (TS strict + shared tsconfigs, canonical OHLCV bar shape, GICS hub, defined-risk options rule, status hub, language split) live in repo-root `CLAUDE.md` — not duplicated here.

## Charter — two roles (spec: `data/specs/analyzing-charter-2026-07-01/SPEC.md`)

Ratified by a 7-delegate cross-qagent debate (2026-07-01). Five adopted
amendment subspecs own their detail: `tape-provenance-2026-07-11/` (P8
provenance events + manifest lineage — § "History preservation" below; kernel
gets ZERO provenance predicates ever), `web-ui-trio-2026-07-11/` (role (b)
widens to **chart-presentation driver**; P4 host = Astro Node-SSR local-only
`analyzing/web/`; the monitoring+analyzing+visualizing trio fortnight),
`ta-schema-v2-2026-07-12/` (absorbed — next paragraph), and the workflow pair
`workflow-coverage-2026-07-13/` (the accepted inspection-workflow roster) +
`workflow-ui-2026-07-13/` (the UI phases U1a/U1b/U2… that encapsulate it).

**Tape *shape* is chartered (2026-07-16):**
`data/charters/analyzing/tape-schema/CHARTER.md` is the single normative
source for the tape's shape (frozen-14 prefix, consumer-backed tiers,
aggregate/breadth/indices lanes) — cite it, never the absorbed `ta-schema-v2`
subspec. The supplier machinery (INV-H, INV-U, freshness manifest, provenance)
stays in `analyzing-charter-2026-07-01/` until it settles into the deferred
conditional `tape-supply` charter (ruling
`data/debates/analyzing-charter-consolidation-2026-07-16.md`; mint conditions
tracked at next-steps item 14).

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
  corporate actions. Classification is **compositional** (2026-07-16,
  `history_guard._classify_restatement`): each restatement decomposes into
  world-fact components `{split_like, dividend_like, volume_settle, residual}`
  — consumers read the component set, never the legacy scalar (any `residual`
  ⇒ scalar `irregular`; the producer emits facts, never a consumer verdict).
  Rescale uniformity (split/dividend) is judged over the column's **changed
  bars only** (2026-07-19): a corporate action rescales bars BEFORE its
  effective date, and mixing the unchanged post-ex-div tail into the ratio
  set mis-classed four routine dividends as `irregular`.
  The pre-write parquet is copied to
  `financial/parquet/.history-backup/<SYM>/<ISO>.parquet`.
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
last-5-per-symbol with **class-aware retention** (class tag in the filename; a
benign snapshot never evicts a non-benign one — R2), pruned at backup time.
The manifest (P2) additionally
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

**Universe membership — INV-U (`scripts/universe_guard.py`, shipped 2026-07-16):**
membership is monotone too. A `sp500.txt` DROP is refused by default
(`--allow-universe-drop` per decision; a **held-symbol** drop hard-refuses,
TG-1); removal is retire-in-place. `scripts/universe_refresh.py` writes
append-only snapshots `financial/universe/sp500/<as_of>.txt`, advances the
current pointer, and appends `sp500-retired.txt`; the Wikipedia membership
diff is human-reviewed by design. Tests: `scripts/test_universe_guard.py`.
The manifest's drop assertion widens by the **retired-and-still-held** set, not
by a tolerance: `tape_manifest.retired_held_symbols()` intersects
`sp500-retired.txt` with the parquets actually on disk and reports it as
`manifest.retired_held[]`, so a retire-in-place stays green while a genuine
silent drop still reds `count_matches_universe` — even in the same refresh
(ns-17; the § 7 orphan-gate twin in `scripts/sync-ground-truth.sh`).
Enforcement follow-ons + the `tape-supply` charter mint: next-steps item 14.

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
  charted subset (`TA_COLS` in `src/lib/tape.ts` is the pin).
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
  canonical `visualizing/graphs/dist/kit-strategy.js` → `public/graphs/kit.js`
  (mount dir renamed `graphs2/` → `graphs/`, operator ruling 2026-07-21)
  (fail-soft: absent dist ⇒ empty-state, never a hard fail) + the
  `kit.css`/`tokens-chart.css` overlays from their **tracked sources** in
  `visualizing/{graphs,charts}/kit/`. The mount probes `chartsCaps()` so
  a stale copy degrades loudly. Consumes only the built `QViz` API (A7).
  **`public/graphs/` is gitignored wholesale** — every file in it is a
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
- **U1a+U1b `[shipped 2026-07-17]` / U2a+U2b `[shipped 2026-07-19/20]`**
  (workflow-ui § 9 — full ship detail lives in that spec's § 9.1 ledger;
  retained here are the load-bearing operational pins only):
  - **The label catalog is THE seam** — every user-facing event/state/
    threshold string passes `src/lib/labels.ts`; `scripts/vocab-audit.mjs`
    enforces the IR-2 denylist + fail-loud live lockstep harvest (accounting
    Lean ids + evaluating `FRAMEWORK_META`) + `mirror-registry.md` cross-ref
    (typed `mirrors:`) + the citedLine grep + K-C11 events-seam confinement.
    `pnpm vocab:audit` (folded into `verify`), owed at close. Threshold lines
    go through `citedLine` (uncited = build error).
  - **`src/lib/events.ts` is the ONE event-extraction seam** (K-C11;
    consumes the tape solely via `readBars`/`readTa`, A-U1) → `/api/events`.
    Picker state is URL-state (deep-link + `replaceState` writeback +
    unknown-param notice); pickers swap panes in place — `data-panes` stays 4.
  - `/market` = WF-3 (indices term-structure + SPY anchor strip; `/api/indices`
    reads the indices dataset only, no ta twin) + WF-4 breadth (MARKER-strength
    frame, survivorship + per-family `n_effective` co-render, materialized-only
    ZBT state — no kernel mirrors). `/tape` = manifest fields only,
    metadata-only backup listing (A-U2), decidability table; never wave-lane
    content (K-C4 — denylist carries `wave-gate`/`tape-provenance-check`);
    `/api/tape` is a **closed-key envelope** `{manifest, backups, decidability}`
    (K-C10).
  - WF-8 drawdown leaves: mdd252 renders under the ONE K-C8 cc-half catalog
    entry on every surface; `rec_bars` NaN-under-water = the labeled breach
    state, never 0; dat veto-screen 0.15/0.05 render as register-cited
    flat-series lines (the kit's horizontal Threshold binds pane 0 only —
    pane-targeted thresholds filed upstream). Book curve = class-2 host-lib
    `src/lib/drawdown.ts` (NO /api endpoint — the § 4.1 roster stays closed);
    formula TEXT renders WITH its register row (K-C9); book-route labels are
    `holdingsSafe`-flagged + floored via `data-catalog-id` (T-C16); MF-1
    subject statement under stable test id (T-C17).
  - `TA_COLS` (in `src/lib/tape.ts`) is THE charted-subset pin — widened only
    per the § 9 schedule (U1a +chop14/natr14/hv_cc20/bbw20; U1b
    +sar/st_dir/don_up55/don_lo10/sma5/rsi2 +obv/mfi14/adosc/pctb20 [the § 12
    amendment]; U2b +mdd252/tuw252/rec_bars/chand_long22). Fixtures: EVT
    (event-dense, 413 bars w/ drawdown tail — every catalog kind fires) +
    breadth fixture + hand-authored fixture manifest (E-U7).
- **U3a `[shipped 2026-07-21]`** (workflow-ui § 9): the aggregate-registry
  port. `src/lib/aggregators.ts` is the HOST-side emitter of the extension
  registry's SQL shapes (semantics pinned by python-duckdb goldens — family
  `cases/golden_rank_sql.py`; the extension module keeps its own). Every
  timestamp-binding query runs `SET TimeZone='UTC'` first (the MF-5
  UTC-session contract — tz-aware ts vs naive `$start` in a local session
  silently drops the first UTC-midnight bar). `/api/rank?metric=&cohort=&dir=`
  serves the WF-5 frontier cross-section (raw value + PERCENT_RANK at the
  DATASET's frontier ts — never a wall-clock window; `excluded[]` cohort
  honesty). Metric vocabulary is CLOSED (`roc63|roc252|rs63|natr`) and
  refuses the drawdown columns (workflow-ui § 14.2 law 4 — the K-C8 escape
  pin). The `/market` regime classifier now emits `regime.high-vol`
  (OWN_PCTILE trailing-252 own-percentile of natr14/hv_cc20 ≥ 0.70,
  register-cited; class-2 — never derived in page/lib TS from the TA slice).
- **U3b `[shipped 2026-07-21]`** (workflow-ui § 9): the IA flip + the
  §§ 14–16 layout retrofits. ALL FIVE nav groups live (`nav.ts`). NEW `/rank`
  (WF-5 frontier cross-section server-rendered via `aggregators.ts`;
  metric/cohort/dir URL-state, closed vocabularies — drawdown metrics and
  `book:` cohorts refuse as unknown values; `ScreenTable` = the Z3 figure in
  a legend `DisclosureFrame`, numeric-only cells) and `/books` (two
  `SpineList` spines — rows identity + leaf links ONLY, no numeric figure,
  never a totals row; conditions@U5/compare@U6 phased "not yet"; zero
  canvas/svg on the hub). Five-zone grammar mechanized: `data-zone` markup on
  every workflow page; `labels.ts` `isStateBearing` (mirrors ∪ state-family
  list) drives the § 14.2 law-8 frames — the symbol Z2 tile band and BOTH
  drawdown tile rows now sit inside legend frames; the symbol page gained a
  Z1 question + Z2 tiles (regime word via `classifyRegime`, per-dataset
  as-of stamps) + a Z4 recent-events list served by the `events.ts`
  accessors (`symbolEvents`/`latestEvent`/`recentEvents` — the C3 seam;
  vocab-audit K-C11 allow-list = exactly the `/api/events` endpoint + the
  symbol page). `/inspect` rows carry direct WF-8 drawdown links. Inline
  empty-state strings live in the catalog. Floors: `layout.spec.ts`
  (AU-10/AU-13/AU-15), `nojs.spec.ts` (AU-11 — `javaScriptEnabled:false`,
  never a 4th Playwright project), `rank/books` specs. Components:
  `TileRow`/`StatTile`/`LeafTabs`/`CitationsFooter`/`ScreenTable`/
  `SpineList`. Fixture `testbook2` (owns `options_structures_allowed` +
  `beta_target`; `testbook` stays keyless). Per-sector breadth stays
  unshipped by design (no materialized source — workflow-ui family TODO.md;
  the § 2.2 + roster clauses were amended in place 2026-07-21: struck with a
  revival path via a breadth.py materialization spec).
- **U4 `[shipped 2026-07-21]`** (workflow-ui § 9): WF-6 + the qgrid producer.
  `/rank/correlation` — two sections, one mount each: the pairwise matrix
  (registered ROLLING_CORR bound to the frontier-anchored last window+1
  sessions + a host window-full gate — a pair with < window overlapping
  returns is undecidable, never a short-window r; C5 summary =
  meanPairwise/minPair/maxPair NAMED fields from `src/lib/corr.ts`, never
  page-side; numeric-only `MatrixTable` in its legend frame) and rolling
  beta (registered ROLLING_BETA vs SPY; the book's own `beta_target` as
  register-cited reference lines — values only, NO in/out-of-band state
  word until `hedge_sizing_beta_bounded` exists). Scope is SINGLE-BOOK only
  (T-C18 — one shared `parseBookScope`; multi-book 400-refused). `/api/corr`
  + `/api/beta` + **`/api/grid/{rank,corr}`** — the constellation's first
  real-market-data `qgrid/1` producer: `privacy:'local-only'` stamped, 403
  `privacy-refusal` on ANY `?privacy=` negotiation, ≤ 50k-cell budget; NO
  beta grid kind (the 2D beta chart is already time-resolved — MF-16).
  Surfacegrid mounts live on `/rank` + `/rank/correlation` (kit-3d built by
  sync-charts' fail-soft ensure; hidden-until-mounted; PC1 literal client
  match — the corr-page fetch is always-on so the AW-5 stripped-payload →
  `data-error` floor runs kit-independent). `sync-charts.mjs` generalized to
  a src→dest pair list (+`kit-3d.js` canonical, `tokens-3d.css` tracked).
  `portfolios.ts` gained the additive `betaTarget` read (the beta-band half
  of the U5 reader widening, pre-landed per § 2.2/§ 15.1). e2e 342 green.
- **U5 `[shipped 2026-07-21]`** (workflow-ui § 9): WF-9 conditions board.
  `/portfolio/<slug>/conditions` — `ConditionBoard` IS the Z2 answer band
  AND the marker-framed figure (third byte-pinned constant
  `DISCLOSURE_MARKER_CONDITIONS`, roster-verbatim; vocab-audit harvests all
  three, fail-loud). `src/lib/conditions.ts` is the WF-9 derivation seam
  (trend c-vs-sma200 with cross-dataset frontier-match honesty; write-gate
  under pinned 20/25/70 register-cited constants; vol values
  descriptive-only; book beta 252d × cost-basis weights VALUES-ONLY — the
  `hedge_sizing_beta_bounded` mirror row stays owed, blocker recorded in
  workflow-ui TODO.md). `/api/conditions/<slug>` never round-trips the
  legend; `StructureLegend` (T-C14 distinct container; T-C13 empty state)
  is the SOLE structure-vocabulary container — leg rows are symbol+qty only
  (trading copy review CLEAR-WITH-AMENDMENTS, both applied). **Reader fix:**
  `portfolios.ts` now reads `risk_policy.{beta_target,
  options_structures_allowed, daily_drawdown_pause_pct,
  monthly_drawdown_halt_pct}` — the U4 top-level `beta_target` read silently
  missed every real book (schema pins the keys under `risk_policy`);
  top-level fallback kept. e2e 396 green.
- **U6 `[shipped 2026-07-21]`** (workflow-ui § 9 — **all U-rows complete**;
  T6 = the remaining row, next-steps item 7): WF-11 compare. Three route
  shapes (`/sector/<S>/compare` · `/industry/<S>/<I>/compare` ·
  `/portfolio/<slug>/compare`) share `CompareView`; `CompareGrid` is layout
  chrome ONLY — every cell is a server-built `qchart/1` payload
  (`src/lib/compare.ts`, trailing-63 window) rendered via `QViz.SvgBackend`;
  zero host-authored `<svg>` (family grep, quote-scoped). `cols=` closed to
  1–2 of `TA_COLS ∪ {c}` minus the drawdown columns (K-C8 escape pin);
  panelset stays BOUND on visualizing M3 — the 2D grid IS the deliverable.
  Cells embed the legend line as SVG `<desc>` (saved-SVG honesty); the
  visible in-SVG caption is filed as an SvgBackend widening of the charts
  C9 `watermark` filing (hint queued, consumer WF-11). **Kit script order
  matters:** `/graphs/kit.js` must load BEFORE any component's inline mount
  script in document order (classic scripts — the sector-page precedent).
  e2e 441 green.
- **inv-5 (A8):** the viewer renders ground-truth tape only — no kernel
  emission, no verdict, no actionable framing. Anything exported off this
  surface becomes a FINANCIALLY-CLEARED subject (charter § 3.5).
- **T6 `[shipped 2026-07-21]`** (web-ui-trio § 4 / workflow-ui § 5.5 — the
  chrome-confined Meridian pass; ZERO `src/pages/**` edits, all prior floors
  unchanged, e2e 450 green): `.m-app-analyzing` steel scene role minted into
  `code/web` scene-roles (counterpoint qresev copper; accent = CHROME only);
  NEW `scripts/sync-meridian.mjs` (monitoring sibling — W5 layers + fonts +
  composed dual-signal `meridian-tokens.css`); `Layout.astro` on the layer
  contract with `m-body m-app-analyzing`; `NavShell` + tri-state
  `ThemeSegment` (IA/testids verbatim; wraps at narrow widths); `public/
  tokens.css` = a pure var()-to-var() BRIDGE (`--page-*` → the Meridian
  slice, re-declared on the app class so the accent substitutes where it
  exists; chips → holds/undetermined/fails) — zero raw color values remain;
  `sync-charts.mjs` writes the COMPOSED dual-signal `tokens-chart.css` from
  BOTH kit legs at the mount path pages already link (light default, dark
  media, data-theme wins both ways — never a host fork). `@qagents/web`
  workspace dep added; lint conf gained meridian/fonts excludes +
  `meridian-tokens.css` TOKEN_FILES row.
- **Chart colour is never host-authored.** `web/public/graphs/` is gitignored
  generated host-copies (`sync-charts.mjs`); forking a kit stylesheet is
  barred. Series colour rides the kit's closed `role` → `seriesToken()` map.
  **Never conscript a chrome/furniture token as a data slot** —
  `symbol/[symbol].astro` still does (a shipped data series sits below the
  a11y floor on both legs; unwind at next-steps item 15 once the role tokens
  mint). **`--m-analyzing` is chrome only, never a series colour** (ΔE 11.2
  vs the binding ΔE ≥ 18 ghost floor; series-dial T1 REJECT).

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
  fallback = newest-bar mtime > 7 d); else `OK` (the `BUILDING → OK`
  promotion landed with trio T6 2026-07-21 — all workflow-ui phases shipped).

Pending-aware (`QAGENTS_PENDING_ROOT || REPO`, status-emit-cron-fleet
convention — root `CLAUDE.md` § "Status hub"); fired daily by the 05:25
`qagents:status-emit-all` fleet and at each `/close --status-emit`. Manual
canonical writes acquire `.data-write-lock`.

Full closed-set contract + display-mode catalog:
`data/specs/display-modes-2026-05-07/SPEC.md`.
