# analyzing/CLAUDE.md

VSCode extension (TS) for market inspection: DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed. Cross-project conventions (TS strict + shared tsconfigs, canonical OHLCV bar shape, GICS hub, defined-risk options rule, status hub, language split) live in repo-root `CLAUDE.md` — not duplicated here.

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

The parquet hub is **gitignored ground truth** living in the canonical
checkout (worktrees symlink to it; see `financial/parquet/CLAUDE.md`
§ "Gitignored ground truth"). Run a full refresh from canonical so the
writes land in the real store, not a worktree-local copy; it is S3-backed
via the `parquet` archive class (`data/specs/serving-2026-05-26/artifact-archive-s3-2026-05-29/SPEC.md`).

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

Both scripts honor the `.data-write-lock` convention from
`data/specs/data-conventions-2026-05-06/SPEC.md` § 5.3 conditionally: the lock
is acquired only when the resolved output path falls under **canonical**
repo's `data/` **or** `financial/` (the single root `.data-write-lock`
serializes both hubs; the market parquet hub moved to top-level
`financial/` per `data/specs/data-charter-2026-05-17/financial-hub-migration-2026-05-29/SPEC.md`).
Worktree-local writes (the common case — e.g. running this from
`qagents-wt/analyzing/`) skip the lock since they don't race with
canonical writers. Cron-lane (`QAGENTS_PENDING_ROOT`) routing is
intentionally **not** wired today; add it when a launchd routine
actually fires either script.

## Status emit (`data/status/analyzing.json`)

`analyzing/scripts/status_emit.mjs` is the live producer for analyzing's
slot in the qagents-wide `/status` hub. Pins `KIT_VERSION` in-script
(0.5.0 today; sweep in lockstep on kit bumps — cross-subproject
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
  `financial/parquet/ohlcv-equities/<SYM>.parquet`. The filter-chip
  header is the `display-modes-2026-05-07.md` Phase 4 outcome (resolved
  2026-05-30 — the ~526-symbol universe crossed the `serving/CLAUDE.md`
  § 7 search+state-filter threshold); `extension-architecture` stays a
  genuine node-edge `DiagramEmit` (not tabular);
- `LiveState` pill driven by parquet-store presence + freshness:
  `NOT_YET_LIVE` when ohlcv dir is empty, `DEGRADED` when newest bar
  > 7 days old, otherwise `BUILDING` (data layer live; activity-bar
  Symbols/Sectors/Portfolios → ChartPanel + AggregatePanel still
  Phase 2.x). Promote to `OK` once the activity-bar views land; the
  consumer (`designing/web/src/lib/status-loader.ts`) is unchanged.

Manual invocation (today, only path) writes `data/status/analyzing.json`
directly. If/when this script becomes cron-fired (under
`data/schedules/launchd/run_routine.sh`), `QAGENTS_PENDING_ROOT` will be
set in the env and the writer should route through `pending/data/status/
analyzing.json` per `data/specs/data-conventions-2026-05-06/SPEC.md` § 5.3
(verifier validates JSON shape + `kitVersion`/`subproject` keys).
Manual-lane writers acquire `.data-write-lock` before mutating
canonical `data/`.

Full closed-set contract + display-mode catalog at
`data/specs/display-modes-2026-05-07/SPEC.md`. The next natural extension
(per § 7.4) is a backtest-summary `DashboardEmit` — KpiStrip of last-N
PnL + FilterChipGroup on strategy + Table of trades — once a backtest
runner ships under `analyzing/`.
