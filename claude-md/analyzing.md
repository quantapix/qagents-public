# analyzing

VSCode extension (TypeScript) for market inspection: an embedded
analytical SQL engine over a columnar Parquet store, lightweight-charts
v5, ingest from public market-data sources, and a live IEX feed. Part of
the financial-domain slice published at `qresev-public`. Cross-project
conventions (TS strict + shared tsconfigs, the canonical OHLCV bar shape,
the GICS hub, the defined-risk options rule, the status hub, the language
split) live in the root `CLAUDE.md` — not duplicated here.

## Batch ingest + TA reference

`scripts/ingest.py` and `scripts/ta_reference.py` each carry an additive
batch mode alongside the original single-symbol form, plus a `--flat` mode
for writing into the canonical market-data hub:

- `ingest.py --symbols A,B,C --out-dir DIR` — one multi-symbol download,
  splits the column MultiIndex per symbol; per-symbol failures are isolated
  into a summary `failed[]`, not aborting.
- `ingest.py … --flat` — same fetch shape, writes `<DIR>/<SYM>.parquet`
  (no per-symbol subdir). The post-charter canonical invocation.
- `ta_reference.py --in-dir DIR --symbols A,B,C` — reads the per-symbol
  parquet, writes a TA-reference parquet alongside it. `--flat` requires an
  explicit `--out-dir`.

The parquet hub is **gitignored ground truth** living in the canonical
checkout (worktrees symlink to it). Run a full refresh from canonical so
the writes land in the real store, not a worktree-local copy; the hub is
mirrored off-site via a versioned archive class.

Both batch scripts also accept `--symbols-file FILE` (one symbol per line;
comments + blanks skipped; deduped) in place of the comma list — the path
for driving the full S&P 500 universe, which is committed as a canonical
list (constituents ∪ anchor sector ETFs). `ingest.py` chunks the fetch at
64 symbols/request and isolates per-chunk failures, so a 500-symbol run
never rides one giant download. Batch mode prints one summary JSON on
stdout and per-symbol ndjson on stderr; exit code is 0 if any symbol
succeeded.

Both scripts honor the `.data-write-lock` convention conditionally: the
lock is acquired only when the resolved output path falls under the
**canonical** repo's `data/` or `financial/` hub (the single root lock
serializes both). Worktree-local writes — the common case — skip the lock
since they don't race canonical writers.

## Status emit (`data/status/analyzing.json`)

`analyzing/scripts/status_emit.mjs` is the live producer for analyzing's
slot in the `/status` hub. Self-contained — no sibling-subproject imports;
the only inputs are filesystem scans of the parquet hub plus the short
commit hash. Today's emit carries:

- one `DiagramEmit` (`extension-architecture`) — ingest sources +
  live feed → SQL-engine + Parquet → extension → charts;
- one `DashboardEmit` (`data-coverage`) composing a fixed-4 `KpiStrip`
  (OHLCV symbol count, TA-reference count, GICS-mapping presence,
  newest-bar mtime), a `FilterChipGroupEmit` (symbol search + TA-ref state
  chips), and a per-symbol `TableEmit` (one row per OHLCV parquet); the
  filter-chip header earns its place once the universe crosses the row
  count where a search + state filter is warranted;
- a live-state pill driven by parquet-store presence + freshness
  (`NOT_YET_LIVE` when the OHLCV dir is empty, `DEGRADED` when the newest
  bar is > 7 days old, otherwise `BUILDING` while the activity-bar views
  are still in progress; promote to `OK` once those land).

The next natural extension is a backtest-summary `DashboardEmit` once a
backtest runner ships.
