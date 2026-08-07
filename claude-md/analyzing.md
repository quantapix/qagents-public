# analyzing/CLAUDE.md

Market-inspection tooling (TypeScript; local-only viewer): DuckDB + Parquet, lightweight-charts v5, yfinance ingest, Alpaca IEX live feed. Cross-project conventions (TS strict + shared tsconfigs, canonical OHLCV bar shape, GICS hub, defined-risk options rule, status hub, language split) live in repo-root `CLAUDE.md` — not duplicated here.

## Charter — two roles (spec: `data/specs/analyzing-charter-2026-07-01/SPEC.md`)

Ratified by a 7-delegate cross-qagent debate (2026-07-01). Six adopted
amendment subspecs own their detail: `tape-provenance-2026-07-11/` (P8
provenance events + manifest lineage), `web-ui-trio-2026-07-11/` (role (b)
widened to chart-presentation driver; P4 host `analyzing/web/`),
`ta-schema-v2-2026-07-12/` (absorbed — next paragraph), the workflow pair
`workflow-coverage-2026-07-13/` (roster) + `workflow-ui-2026-07-13/` (the UI
phases U1a…U6), and `factor-overlay-2026-07-27/` (optional
factor-decomposition overlays; FV1–FV4 ALL shipped 2026-07-29/30).

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
- **(b) Local-only viewing surface + chart-presentation driver.** The Astro
  Node-SSR app at `analyzing/web/` (§ Web viewer below) — run-independent,
  ground-truth-only, the complement to `evaluating/`'s run-keyed Qresev.
  Since 2026-07-11 analyzing is also the **first consumer + requirements
  driver for every chart-like (`qchart`) presentation capability** — new
  capabilities prove on analyzing's real-tape mount (or record an explicit
  skip) before public mounts adopt them; driver ≠ owner — kits stay
  `visualizing/`'s (`web-ui-trio-2026-07-11/SPEC.md`).

**Invariants audited each close** (detail: spec §§ 1.1, 2.3, 3.5):

- Files-only seam, no served API — unconditional (Lean4 inv-5; charter
  acceptance A4; accounting `CLAUDE.md` § Cross-project boundaries).
- Viewer renders tape only, never kernel emissions (predicate `Bool`s,
  verdicts, proof-DAG, FINANCIALLY-CLEARED signal) — those are
  `evaluating/`'s alone.
- GICS + portfolios read-only here; separate per-PM books, never a pooled
  cross-PM NAV, never an order surface.
- Freshness manifest `financial/parquet/manifest.json` (P2) with tiered
  STALE teeth — spec § 2.3. Any published/exported analyzing chart is a
  FINANCIALLY-CLEARED subject (`evaluating/` grants, `accounting/` advises).

## Legacy extension tree — `src/`, `aggregators/` (retained, not shipped)

`analyzing/src/` is the pre-ruling VSCode-extension codebase (extension
host, webviews, `src/data/gics.ts`); `analyzing/aggregators/` holds its
117 indicator docs. Per the operator ruling 2026-07-12 **analyzing ships
no VSCode extension** — the live surfaces are the supplier scripts
(`scripts/`) and the web viewer (`web/`). The tree is retained as a
port source (`web/src/lib/aggregators.ts` mirrors the
`src/analysis/aggregators/` registry; TA parity canon lives in
`src/analysis/`, gated by `ta-lib-check`) and still passes `pnpm verify`;
it is never packaged, never the citation target for live behavior — the
live GICS reader is `web/src/lib/gics.ts`, not `src/data/gics.ts`.
Retire-vs-port is an open call, not an accident of drift.

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
ta-schema-v2 § 5 Phase D; INV-H applies; NEVER run ta_reference against it).
Own-universe lanes carry a tighter staleness surface: the manifest flags ANY
frontier divergence (`OWN_UNIVERSE_STALE_LAG_DAYS = 0`) plus a per-symbol
`frontiers` map, because an `as_of` of MAX hides a frozen sibling behind a
healthy leg. Informational, never a lockstep gate. Refresh — the manifest
step is part of this lane too:

```
python scripts/ingest.py --symbols-file ../financial/universe/indices.txt \
  --start 2023-01-01 --end <settled> --out-dir ../financial/parquet/indices --flat
python scripts/tape_manifest.py --parquet-root ../financial/parquet
```

A refresh is all four, in order (charter § 2.3 lockstep + P2; the breadth
step is ta-schema-v2 Phase C — equities-only per `financial/universe/anchors.txt`,
single implementation of the McClellan/ZBT recurrences [A-C2], materialized
to `financial/parquet/breadth/breadth.parquet`, lockstepped by the manifest
on `as_of`): the
manifest step rewrites `financial/parquet/manifest.json` (freshness
sidecar — see `financial/parquet/CLAUDE.md` § "Freshness sidecar") and,
given `--refresh-summary`, emits the P8 provenance events. Batch mode
prints one summary JSON on stdout — the key set (and the `pre_sha` /
`post_sha` / `backup_path` fields non-clean entries carry) is pinned by
`tape-provenance-2026-07-11/SPEC.md` § 1, which is exactly what
`--refresh-summary` replays — plus ndjson per-symbol on stderr.

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
  **Materiality, measured 2026-08-05** (353 restatements, backups replayed
  through `talib.OBV` — the `ta_reference.py:126` call): `dividend_like` is
  EXACTLY invariant for OBV (it rewrites `adj_c`; OBV reads raw `c`), and
  `volume_settle` shifts OBV by a CONSTANT from the restated bar forward, so
  every OBV increment / slope / divergence read after that bar is unchanged
  (level shift median 1.6e-05, max 2.3e-02, zero sign flips over 349 symbols).
  **No warn tier is warranted for either class**; NOT bounded by that
  measurement — a level read whose window spans the restated bar, and repeated
  settles landing on the SAME bar. Detail + method: ns:analyzing/12.
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

**Provenance (P8, shipped 2026-07-11 — mechanism owner:
`tape-provenance-2026-07-11/SPEC.md`, which owns the spool / `uuid5`-dedupe /
backup-retention detail):** `ingest.py`'s summary is replayed by
`tape_manifest.py --refresh-summary` into the shared ledger store
`analyzing:tape-refresh`, appended **after** `.data-write-lock` releases,
never gating the refresh; `rewritten` rows carry the exact
`--allow-history-rewrite` `allow_set` — the durable "on the record".
`.history-backup/` prune is **class-aware**: a benign snapshot never evicts a
non-benign one (R2). Pins: the manifest's `prev_content_sha` + `non_clean[]`
digest keep accounting's wave gate **file-authoritative** (store = audit
superset, never a gate); `content_sha` is ONE function
(`tape_manifest.file_sha256` / `dataset_content_sha`) feeding both manifest
pin and event lineage; **no provenance/freshness predicate ever enters
`Facts.lean`** (permanent).

Tests: `../.venv/bin/pytest scripts/test_history_guard.py scripts/test_tape_manifest.py -q`
(hermetic) + the live-tape half of `data/specs/analyzing-charter-2026-07-01/tests/run.sh`.
`ta_reference.py` needs no guard — it is a pure derivation, so a blocked symbol
keeps its old bars and its TA recomputes identically.

Both scripts follow the configurable-output-path lock rule (root `CLAUDE.md`
§ "Shared-data write-lock"): `.data-write-lock` iff the resolved output is
canonical. The planned P3 cron writes direct-to-canonical under the lock —
never through `pending/` (charter spec § 2.5).

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
(ns-17; the § 7 orphan-gate twin in repo-root `scripts/sync-ground-truth.sh`
— NOT under `analyzing/scripts/`; owner: workstation-parity spec).
Live residual: next-steps item 14 (enforcement legs complete 2026-07-29).

## Web viewer — `analyzing/web/` (P4 host, role (b))

Astro **Node-SSR local-only** app (charter § 3.2; web-ui-trio § 3 pins
monitoring's proven shape). **127.0.0.1:4327 only** (port registry
`code/playwright/PORTS.md`), never deployed, absent from every deploy lane
(A10). Run: `pnpm -C analyzing/web dev` (or `build && preview`):

- **Symbol mount** (executes charts C5): pane 0 candlestick + volume
  (overlay scale) + SMA20/50/200 overlays, pane 1 RSI, pane 2 MACD
  (2 lines + histogram), pane 3 ADX+ATR — the R-C5 pane budget exactly
  (`data-panes` records it for the e2e floor). **Viewer toggles
  (ta-schema-v2 § 6, Phase C):** a band picker swaps pane-0 line pairs
  (Bollinger / Keltner-TTM / Donchian / SuperTrend — pairs swap, never
  stack; fills + per-segment coloring are chartered qchart requests) and a
  pane-3 picker swaps ADX+ATR ↔ ±DI in place.
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

- **Data seam:** `src/lib/{tape,gics,portfolios,aggregate,factors}.ts` read
  the hubs via DuckDB/YAML/JSON at request time; `/api/bars/<SYM>` returns
  the charts § 2 envelope `{bars, asOf?, stale?}` (freshness from
  `manifest.json`, UNKNOWN-safe), `/api/ta/<SYM>` the columnar TA
  companion (NaN warm-up = JSON null; duckdb-node surfaces parquet NaN as
  null — never `Number()` it into a fake 0), `/api/aggregate?level=…` the
  composite payload, `/api/factors/<SYM>` the FV1 closed-key factor
  envelope (latest promoted `financial/factors/` vintage ONLY — C-3; C-2
  triple stamped; E-4: no rung/fit-quality field ever crosses the seam;
  U4 privacy pins verbatim), `/api/factors/cohort` the FV3 cohort twin
  (mean + IQR of member contributions over cohort ∩ fitted via
  `lib/cohorts.ts`; excluded[] honesty), `/api/factors/ribbons` the FV4
  qribbon/1 wire (widths PRODUCER-computed in `lib/factorRibbons.ts`,
  both scopes; **finite-only trimmed window** — q3d validate rejects
  NaN, an empty window is a labeled 404). Overlay math is pure in
  `lib/factorPaths.ts` (CH-F2(a) adj-close paths + cohort rebased-1.0
  index; ε viewer-derived, suspended labeled on a stale tape § 2.7);
  `readAdjCloses` is server-only so the `/api/bars` envelope stays
  byte-identical. The symbol/sector/portfolio `?factors=` pickers carry
  factor *ids* only (no ε on cohorts); overlay renders stamp
  `data-factor-overlay` behind the `componentSlots`/`ribbonset` caps
  probes. **A12: the `/api` endpoints are
  intra-subproject viewer plumbing, never a supplier seam** — no other
  qagents process may call them (grep-audited with A4 at close).
  `QAGENTS_TAPE_ROOT` / `QAGENTS_PORTFOLIOS_ROOT` / `QAGENTS_FACTORS_ROOT`
  override the roots (hermetic e2e).
- **Kit delivery:** `scripts/sync-charts.mjs` (predev/prebuild) host-copies
  canonical `visualizing/graphs/dist/kit-strategy.js` → `public/graphs/kit.js`
  (fail-soft: absent dist ⇒ empty-state, never a hard fail) + the
  `kit.css`/`tokens-chart.css` overlays from their **tracked sources** in
  `visualizing/{graphs,charts}/kit/`. The mount probes `chartsCaps()` so
  a stale copy degrades loudly. Consumes only the built `QViz` API (A7).
  **`public/graphs/` is gitignored wholesale** — every file in it is a
  host-copy, so at `/close` the rescue gate (exit 15) lists them: **discard,
  never rescue**; `pnpm dev`/`build` regenerates all of them. Same for the
  `sync-meridian.mjs` host-copies (`public/meridian/`,
  `public/meridian-tokens.css`, `public/fonts/`) and `test-results/`.
- **e2e:** `pnpm -C analyzing/web test:e2e` — three chromium projects on
  port 4327 against the committed fixture tree (AAA/BBB/EVT tape +
  indices ^VIX/^VIX3M + breadth + hand-authored manifest + GICS map +
  `testbook`/`testbook2` portfolios + synthetic factor vintage
  `fixtures/factors/2026-07-03/`, AAA/BBB fitted, EVT unfitted). Floors mirror the pins in this
  section (127.0.0.1 guard, § 2 envelope shape, NaN warm-up + all-null
  render, `data-ready` terminal states, STALE chip, `data-panes` = 4,
  cohort honesty, never-pooled book language).
- **Workflow-UI phases U1a…U6 + T6 — ALL `[shipped]`.** The per-phase pin
  ledger lives in workflow-ui § 9.1 (+ §§ 14–16 layout/route pins, § 5.5 T6
  chrome bar) — read § 9.1 BEFORE editing any route / component / `/api`
  endpoint under `web/src/`. Cross-cutting seams a non-UI session can still
  trip: `src/lib/labels.ts` (THE label seam — every user-facing event/state/
  threshold string passes it; `pnpm vocab:audit` owed at close; threshold
  lines via `citedLine`, uncited = build error); `src/lib/events.ts` (the
  ONE event-extraction seam, K-C11); `TA_COLS` in `src/lib/tape.ts` (THE
  charted-subset pin — widened only per the workflow-ui § 9 schedule, never
  ad hoc); `src/lib/aggregators.ts` (every timestamp-binding query runs
  `SET TimeZone='UTC'` first — MF-5).
- **inv-5 (A8)** = § Charter invariants above, restated for this surface: no
  kernel emission, no verdict, no actionable framing (charter § 3.5).
- **Chart colour is never host-authored** — forking a kit stylesheet is
  barred (host-copies: § Kit delivery above). Series colour rides the kit's
  closed `role` → `seriesToken()` map. **Never conscript a
  chrome/furniture token as a data slot.** **`--m-analyzing` is chrome only,
  never a series colour** (ΔE 11.2 vs the binding ΔE ≥ 18 ghost floor;
  series-dial T1 REJECT).

## Status emit (`data/status/analyzing.json`)

`analyzing/scripts/status_emit.mjs` is the live producer for analyzing's
slot in the qagents-wide `/status` hub. Pins `KIT_VERSION` in-script
(0.8.0 today; sweep in lockstep on kit bumps — cross-subproject
contract: `qagents/CLAUDE.md` § "Status hub"). Self-contained — no
sibling-subproject imports; the only inputs are filesystem scans of
`financial/parquet/` plus `git rev-parse --short HEAD`. Today's emit
carries:

- one `DiagramEmit` (`viewer-architecture` — genuine node-edge, never
  tabular) + one `DashboardEmit` (`data-coverage`: fixed-4 `KpiStrip`,
  `coverage-filter` chips bound to the per-symbol `symbol-coverage` table);
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
