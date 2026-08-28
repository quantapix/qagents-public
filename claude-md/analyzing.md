# analyzing/CLAUDE.md

Market-inspection tooling (TypeScript; local-only viewer): DuckDB + Parquet, lightweight-charts v5, yfinance ingest, Alpaca IEX live feed. Cross-project conventions (TS strict + shared tsconfigs, canonical OHLCV bar shape, GICS hub, defined-risk options rule, status hub, language split) live in repo-root `CLAUDE.md` — not duplicated here.

## Charter — two roles (spec family: `data/specs/analyzing-charter-2026-07-01/`)

Ratified by a 7-delegate cross-qagent debate (2026-07-01); all amendment
phases have shipped and the SPEC bodies were reaped. Subspec dirs:
`tape-provenance-2026-07-11/` + `ta-schema-v2-2026-07-12/` (both absorbed —
next paragraph), `workflow-coverage-2026-07-13/` + `workflow-ui-2026-07-13/`
(live, viewer), `tape-cron-2026-08-09/` (live — lane registration / enable;
its exit contract binds in the tape-supply charter). The web-ui-trio (role (b) widening; P4 host
`analyzing/web/`) + factor-overlay (FV1–FV4) amendments have NO subspec dir —
record: `data/debates/adopted/factor-overlay-2026-07-27.md`.

**Two charters, both single normative sources — cite them, never the
absorbed subspecs:**
- **Tape *shape*** (2026-07-16): `data/charters/analyzing/tape-schema/CHARTER.md`
  — frozen-14 prefix, consumer-backed tiers, aggregate/breadth/indices lanes.
- **Tape *supply*** (scope-minted 2026-08-21 under R2's conditional mint, the
  2026-08-18 a2 ruling): `data/charters/analyzing/tape-supply/CHARTER.md` —
  INV-H (incl. the `reconciled` tier + the CLOSED-at-five partition), INV-U,
  the P2 freshness manifest, P8 provenance, the refresh lane's exit contract.
  Deliberately EXCLUDED (the options-chain/D-1 dataset LANDED 2026-08-25 —
  contract + activation state: `data/charters/analyzing/tape-schema/options-chain-d1.md`;
  recorder `analyzing/scripts/options_chain.py`) and still living here + in the spec family: INV-W /
  the whole sub-daily lane (§ below) and the options-chain/D-1 dataset.

- **(a) Market-data supplier.** Named owner/producer of the historical
  aggregate tape — `financial/parquet/ohlcv-equities/` (`ingest.py --flat`) +
  `ta-reference/` (`ta_reference.py --flat`) — over the ~527-symbol
  S&P-500 ∪ anchor-ETF universe, on the schemas the tape-schema charter locks
  (§ above; bar shape: `financial/parquet/CLAUDE.md`). Ground
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
  `visualizing/`'s (`web-ui-trio-2026-07-11/`).

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

Pre-ruling VSCode-extension codebase + its 117 indicator docs. Per the
operator ruling 2026-07-12 **analyzing ships no VSCode extension** — the live
surfaces are `scripts/` + `web/`. Retained as a port source only
(`web/src/lib/aggregators.ts` mirrors `src/analysis/aggregators/`; TA parity
canon in `src/analysis/`, gated by `ta-lib-check`) and still passes
`pnpm verify`; **never packaged, never the citation target for live
behavior** — the live GICS reader is `web/src/lib/gics.ts`, never
`src/data/gics.ts`. Retire-vs-port is an open call, not drift.

## Batch ingest + ta_reference

`scripts/ingest.py` and `scripts/ta_reference.py` both have an additive
batch mode alongside the original single-symbol form, plus a `--flat`
mode added by the `data/specs/data-charter-2026-05-17/` family for writing
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
**There is exactly ONE refresh chain, and this file does not own its
length.** Cron and manual/backfill run the same steps in the same order; the
single owner is `scripts/tape_refresh.py build_steps()` (rendered as the
`tape-cron-2026-08-09/` family's § 3 step table). Today it is **six** — equities
ingest → ta_reference → breadth → indices ingest → intraday ingest →
manifest+provenance — but read the count off `build_steps()`, never off prose:
this file restated it twice and BOTH went stale ("five" here, "four" below) the
day intraday-ingest landed. One exception to the chain's window discipline:
**intraday ingest rides `--rolling`, every other step rides `START`** (INV-W).

## Sub-daily tape — INV-W (`scripts/intraday_guard.py`)

`ingest.py --tf 1m|5m|15m|1h` rides its **own** universe
(`financial/universe/intraday.txt` — 23 since 2026-08-16: 6 broad-market + 11
sector SPDRs + 6 single names for simulating's D1.5m/D5.3 rungs, so **no longer
a subset of `anchors.txt`**) and its own dataset dir, on the `indices`
own-universe pattern. **Membership is INV-W-urgent** — coverage begins the day
a name lands and can never be backfilled past the ~30-day 1m lookback, so a
granted name lands the day it is granted. `ohlcv-equities/` is the frozen daily shape and never
mixes resolutions. **NEVER run `ta_reference.py` against it** — the frozen-14
canon's warm-up and semantics are daily-calibrated, so `rsi14` over minute
bars silently means something else.

**INV-W: an intraday request must lie inside the vendor's retention window on
both axes** — span (per request) and lookback. Measured live, not copied from
docs: 1m = 8d/30d (7d→1950 bars, 8d→2340, 9d→empty), 5m+15m = 60/60, 1h =
730/730; the bound is INCLUSIVE (an earlier 7d guess was a false refusal of a
servable window). It exists because the vendor answers an out-of-window
sub-daily request with an **empty frame**, which `ingest.py` reads as
`failed[] frozen=True` — a coverage regression blaming the vendor for a window
we chose, at exit 3. The tell does not look like the cause, so the window is
checked before the fetch and the refusal carries its own arithmetic.

`--rolling` computes a servable window (`ROLLING_SPAN_DAYS`, deliberately below
the hard limit so a wake-coalesced late fire still lands in-window); its
ANCHOR is the chain's `resolve_end` via `--rolling-anchor` (b71c79064) —
without it every post-close fire stopped one session short (vendor
end-exclusive) and the dataset-uniform lag read green on every arm. **The
retention wall bounds the REQUEST, not the tape:** INV-H's merge leaves bars
older than `--start` as `E_out`, so a repeatedly-fired lane accumulates
indefinitely — verified live (two runs, 08-03..08-06 then 08-05..08-10 → 5
trading days × 390 RTH bars/symbol, no duplicates). It can never *backfill*
behind the wall, so coverage begins the day the lane starts firing.

`history_guard` is resolution-aware via a `tf` argument defaulting to `1d`
(daily behaviour byte-identical): the `volume_settle` frontier conjunct
tightens from 10d to 2d (10 days of minute bars is ~3,900 bars — wide enough
to invert the arm from fail-closed to fail-open), and evidence labels
(`lost_first`/`restated_first`/…) keep time-of-day, because `tape_refresh`'s
expected-blocked signature keys on them and date-truncated labels let two
different same-day gaps share one key. Tests: `scripts/test_intraday_guard.py`
(17 witnesses; the four load-bearing arms each observed RED via sabotage).

**SHIPPED 2026-08-10** (operator ruling; named consumer **`simulating/`**, in
flight — the ruling to land ahead of it is recorded in the tape-schema charter
§ 2.4). `financial/parquet/ohlcv-intraday/` is a registered own-universe
dataset. **Registration is FIVE sites, not four** (the fifth was missed at ship
and cost `ns:analyzing/37` — the dataset existed on the seat alone, unmirrored
and invisible to the orphan gate): `.worktree-links` + `parquet/.gitignore`
rows, `OWN_UNIVERSE_DATASETS` entry with its lockstep arm in lockstep, an
`intraday-ingest` step in the `tape_refresh.py` chain (between indices and
manifest) riding `--rolling` never `START`, **and the `scripts/sync-ground-truth.sh`
tape roster**. Note the fourth arm is only *emitted* when the dataset dir
exists, so an unregistered-or-absent dataset reads `lockstep.ok: true` on every
host that lacks it. Sub-daily staleness is judged on the **session**,
not the bar (`SUBDAILY_DATASETS` → `dataset_snapshot(stale_on_date=True)`):
with the 0-day own-universe threshold, a symbol whose last bar is one minute
behind the frontier would otherwise report `lag_days: 0` — noise dressed as a
finding. That branch is defensive and still VACUOUS on live data (every
shipped symbol shared one last-bar timestamp again on 08-16), so it carries a
hermetic witness rather than living untested.

The volatility-index lane refreshes separately (own cadence, own universe —
tape-schema charter § 2.4; INV-H applies; NEVER run ta_reference against it).
Own-universe lanes carry a tighter staleness surface: the manifest flags ANY
frontier divergence (`OWN_UNIVERSE_STALE_LAG_DAYS = 0`) plus a per-symbol
`frontiers` map, because an `as_of` of MAX hides a frozen sibling behind a
healthy leg. Informational, never a lockstep gate; the manifest step is part
of this lane too.

The 18:00 post-close cron lane and the manual/backfill recipe are the same chain in the
same order — owner `build_steps()` (§ Batch ingest above); lane identity +
exit contract in § History preservation below; breadth-lane detail (anchor-ETF
exclusion, one materialized recurrence implementation, `as_of` lockstep) in
tape-schema charter § 2.4. The
manifest step rewrites `financial/parquet/manifest.json` (freshness
sidecar — see `financial/parquet/CLAUDE.md` § "Freshness sidecar") and,
given `--refresh-summary`, emits the P8 provenance events. Batch mode
prints one summary JSON on stdout — the key set (and the `pre_sha` /
`post_sha` / `backup_path` fields non-clean entries carry) is pinned by
the tape-supply charter § provenance (absorbed from
`tape-provenance-2026-07-11/`), which is exactly what
`--refresh-summary` replays — plus ndjson per-symbol on stderr.

## History preservation (INV-H) + Universe membership (INV-U) → the tape-supply charter

Both guard corpora are chartered (folded 2026-08-21 from the interim
`analyzing/tape-guards.md`, now a pointer): INV-H's window-scoped merge +
per-symbol verdicts (the compositional restatement classification, the
CLOSED-at-five partition with its amendment record + falsifier, the
`reconciled` tier, the OBV materiality measurement, the per-symbol
`--allow-history-rewrite` record), the P8 provenance pins, the cron-lane exit
contract, INV-U's monotone membership + the THREE-step universe lane + ∅-held
= UNKNOWN (exit 4). Read `data/charters/analyzing/tape-supply/CHARTER.md`
§§ 2.1–2.5 before touching `history_guard.py`, `universe_guard.py`,
`ingest.py` write paths, accepting a rewrite, or diagnosing an exit 3. Exit
codes: `0` all written · `1` all failed · `3` ≥ 1 symbol blocked by the guard.

**Vendor-attrition class — RULED 2026-08-18, CLOSED 2026-08-25.** `blocked[]`
climbed 1 → 100 over the 08-11..08-18 fires and most of it was FETCH TIME, not
deletion; the forensics (the closed lost-DATE set, the 61-of-100 re-fetch, the
425-of-527 NaN frontier that `as_of` and `lockstep` both read healthy) are in
`data/summaries/close/2026-08-18T1731-analyzing.md`. Both rulings it produced
(`c41c31457`) are charter content now — the post-close 18:00 ET lane with its
`late_fire` session window (§ exit-contract) and INV-H's `reconciled` tier
(§ inv-h). DEPLOYED on both seat hosts 2026-08-25 and the fetch-time hypothesis
CONFIRMED: the first post-close fire wrote 523 clean, `blocked[]` runs 2–3/fire
since. The residue is individual symbol facts, watched at `ns:analyzing/50`
(EQR vendor degradation; ^VIX3M re-frozen 888→1 since ≤08-21 — a true vendor
outage this time, not our artifact; reads arm 2026-09-08). EA is
retired-in-place (`sp500-retired.txt`) — its 08-04 frontier is expected. Watch
`behind_frontier.count` and the warn-level `reconciled[]` bucket: a tape whose
gaps are papered over daily must not read as clean. `ns:analyzing/43` retired
2026-08-25.

## Web viewer — `analyzing/web/` (P4 host, role (b))

Astro **Node-SSR local-only** app (charter § 3.2; web-ui-trio § 3 pins
monitoring's proven shape). **127.0.0.1:4327 only** (port registry
`code/playwright/PORTS.md`), never deployed, absent from every deploy lane
(A10). Run: `pnpm -C analyzing/web dev` (or `build && preview`):

- **Symbol mount** (executes charts C5): pane 0 candlestick + volume
  (overlay scale) + SMA20/50/200 overlays, pane 1 RSI, pane 2 MACD
  (2 lines + histogram), pane 3 ADX+ATR — the R-C5 pane budget exactly
  (`data-panes` records it for the e2e floor). **Viewer toggles** (pins:
  this section + `web/tests/e2e/`): a band picker swaps pane-0 line pairs
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

- **Seam pins + `/api` roster + e2e floors → `analyzing/web/CLAUDE.md`**
  (moved verbatim, spread 2026-08-17 M-Y2 — path-scoped: it loads for
  exactly the sessions that edit `web/src/**`). Read it before editing any
  route / component / `/api` endpoint / e2e suite: the data seam (envelope
  shapes, A12 never-a-supplier rule, hermetic root overrides), kit-delivery
  host-copies (discard, never rescue), the e2e floors, the U1a…U6 standing
  laws + cross-cutting seams (`labels.ts` · `events.ts` · `TA_COLS` ·
  `aggregators.ts` UTC), and the chart-colour never-host-authored rule.
- **inv-5 (A8)** = § Charter invariants above, restated for this surface: no
  kernel emission, no verdict, no actionable framing (charter § 3.5).

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
  fallback = newest-bar mtime > 7 d); else `OK`.

Pending-aware; fired daily by the 05:25 `qagents:status-emit-all` fleet and at
each `/close --status-emit`; manual canonical writes acquire
`.data-write-lock` (fleet convention: root `CLAUDE.md` § "Status hub").

Full closed-set contract + display-mode catalog: the kit types
(`serving/diagrams/kit/src/types.ts`).
