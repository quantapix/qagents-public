# analyzing/CLAUDE.md

VSCode extension (TS) for market inspection: DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed. Cross-project conventions (TS strict + shared tsconfigs, canonical OHLCV bar shape, GICS hub, defined-risk options rule, status hub, language split) live in repo-root `CLAUDE.md` — not duplicated here.

## Charter — two roles (spec: `data/specs/analyzing-charter-2026-07-01/SPEC.md`)

Ratified by a 7-delegate cross-qagent debate (2026-07-01):

- **(a) Market-data supplier.** Named owner/producer of the historical
  aggregate tape — `financial/parquet/ohlcv-equities/` (`ingest.py --flat`) +
  `ta-reference/` (`ta_reference.py --flat`) — over the ~527-symbol
  S&P-500 ∪ anchor-ETF universe on locked schemas (OHLCV `ts,o,h,l,c,v,adj_c`;
  the 14-col TA canon). Ground truth for `accounting/`'s kernel (file reads
  via `data_view.py`, never imports) and `trading/`'s decision-support reads
  (the live/order path stays on `alpaca_client.py`, never the tape).
- **(b) Local-only viewing surface.** Re-homes as a browser TS surface
  (charts-migration L2; local-only, never publicly deployed) mounting
  `visualizing/`'s vanilla-JS kits, driven by the `AggregateSelection`
  drill-down (GICS sector ▸ industry ▸ symbol; portfolio ▸ holdings).
  Run-independent, ground-truth-only — the complement to `evaluating/`'s
  run-keyed Qresev.

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

- `ingest.py --symbols A,B,C --out-dir DIR` — one yfinance multi-symbol
  download, splits the column MultiIndex via `df.xs(sym, axis=1, level=1)`,
  writes `<DIR>/<SYM>/<SYM>.parquet` per symbol (legacy layout).
  Per-symbol failures isolated (collected into the summary JSON's
  `failed[]`, not aborting).
- `ingest.py --symbols A,B,C --out-dir financial/parquet/ohlcv-equities --flat`
  — same fetch shape, writes `<DIR>/<SYM>.parquet` (no per-symbol
  subdir). Post-charter canonical invocation.
- `ta_reference.py --in-dir DIR --symbols A,B,C` — reads
  `<DIR>/<SYM>/<SYM>.parquet`, writes `<DIR>/<SYM>/ta_reference.parquet`
  (legacy in-place layout). Symbol case normalized at argparse time.
- `ta_reference.py --in-dir financial/parquet/ohlcv-equities --out-dir financial/parquet/ta-reference --symbols A,B,C --flat`
  — reads `<in-dir>/<SYM>.parquet`, writes `<out-dir>/<SYM>.parquet`.
  `--flat` requires explicit `--out-dir`.

The parquet hub is gitignored ground truth in the canonical checkout —
worktrees symlink to it, S3-backed (see `financial/parquet/CLAUDE.md`).
Run full refreshes from canonical so writes land in the real store.

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
  --start 2023-01-01 --end <today> --out-dir ../financial/parquet/ohlcv-equities --flat
python scripts/ta_reference.py --in-dir ../financial/parquet/ohlcv-equities \
  --out-dir ../financial/parquet/ta-reference --symbols-file ../financial/universe/sp500.txt --flat
```

Batch mode prints one summary JSON on stdout (`{tf,start,end,written,failed}`
for ingest; `{in_dir,written,failed}` for ta_reference) and ndjson per-symbol
on stderr. Exit code is 0 if any symbol succeeded; non-zero only if all failed.

Both scripts follow the configurable-output-path lock rule (root `CLAUDE.md`
§ "Shared-data write-lock"): `.data-write-lock` iff the resolved output falls
under canonical `data/`/`financial/`; worktree-local writes skip it. The
planned P3 cron writes direct-to-canonical under the lock — never through
`pending/` (charter spec § 2.5).

## Status emit (`data/status/analyzing.json`)

`analyzing/scripts/status_emit.mjs` is the live producer for analyzing's
slot in the qagents-wide `/status` hub. Pins `KIT_VERSION` in-script
(0.7.0 today; sweep in lockstep on kit bumps — cross-subproject
contract: `qagents/CLAUDE.md` § "Status hub"). Self-contained — no
sibling-subproject imports; the only inputs are filesystem scans of
`financial/parquet/` plus `git rev-parse --short HEAD`. Today's emit
carries:

- one `DiagramEmit` (`extension-architecture`) — yfinance/Stooq +
  Alpaca IEX → DuckDB+Parquet → extension → lightweight-charts v5;
- one `DashboardEmit` (`data-coverage`) composing a fixed-4 `KpiStrip`
  (OHLCV symbol count, TA-Lib reference count, GICS-mapping presence,
  newest-bar mtime), a `FilterChipGroupEmit` (`coverage-filter` —
  symbol search + TA-ref state chips, `bindsTo: symbol-coverage`), and a
  per-symbol `TableEmit` (`symbol-coverage`) with one row per
  `financial/parquet/ohlcv-equities/<SYM>.parquet`;
  `extension-architecture` stays a genuine node-edge `DiagramEmit`
  (not tabular);
- `LiveState` pill from parquet presence + freshness: `NOT_YET_LIVE` (empty
  ohlcv dir), `DEGRADED` (newest bar > 7 days), else `BUILDING`. Promote to
  `OK` when role (b) — the re-homed browser viewing surface — ships (spec § 3.4).

Pending-aware (`QAGENTS_PENDING_ROOT || REPO`, status-emit-cron-fleet
convention — root `CLAUDE.md` § "Status hub"); fired daily by the 05:25
`qagents:status-emit-all` fleet and at each `/close --status-emit`. Manual
canonical writes acquire `.data-write-lock`.

Full closed-set contract + display-mode catalog:
`data/specs/display-modes-2026-05-07/SPEC.md`.
