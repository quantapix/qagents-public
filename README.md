# qagents-public

> Umbrella for the AI-assisted authorship conventions that govern the
> Quantapix engineering practice. The redacted `CLAUDE.md` graph of
> the private working repository, refreshed weekly.

A weekly-refreshed window into how a sole developer plus an expert AI
assistant collaborate inside a single monorepo across twelve sibling
subprojects. The artifact this repo publishes is *not* the
implementation code — that lives in the per-subproject public
repos. It is the **rule set** the assistant reads at every
session start: which subproject owns which surface, where the
write-locks are, which conventions cross boundaries, and which
explicitly do not.

- Parent organisation: <https://github.com/quantapix>
- Engineering output: <https://quantapix.com>
- Motivational record: <https://femfas.net>

## What this repo is

The private repo is structured as twelve sibling subprojects under a
single root, each with its own `CLAUDE.md` carrying the rules that
govern AI-assisted work inside that subproject. A root `CLAUDE.md`
pins only the conventions that cross subproject boundaries. This
repo mirrors that graph in redacted form — the same boundary rules,
the same data-hub seams, the same language-split discipline.

## Sibling subprojects (twelve, one venv, one workspace)

| Subproject | Role |
|---|---|
| `analyzing/` | VSCode extension (TypeScript) for market inspection — DuckDB + Parquet, lightweight-charts v5, ingest from public OHLCV sources. |
| `trading/` | Python portfolio-management agents — three PMs (aggressive / moderate / conservative) on a paper-trading broker, orchestrated by AI-assisted routines. |
| `monitoring/` | VSCode extension sibling of `analyzing/` — LW-Charts + Three.js surface; shared SQLite schema. |
| `appealing/` + `pleading/` | Pro se federal + state legal drafting. Markdown drafts; rendered PDFs flow to a filing hub. |
| `proving/` | Lean4 axiomatic theorem-proving with LLM-backed predicate functions for the legal domain. Backs Qnarre. |
| `accounting/` | Lean4 + LLM-predicates for the financial domain (five frameworks: TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN). Backs Qresev. |
| `verifying/` | Astro + React shell + FastAPI server for **Qnarre**, the legal-complaint verifier UI. Streams events from `proving/` over SSE. |
| `evaluating/` | Sibling of `verifying/` for **Qresev**, the stock/portfolio evaluator UI. Streams events from `accounting/` over SSE. |
| `designing/` | Astro + React islands site for quantapix.com. Hosts the `/status` page that aggregates per-subproject status emits. |
| `documenting/` | Sibling of `designing/`; femfas.net. |
| `studying/` | Lean4 expert-track study + OSS contribution roadmap. |
| `explaining/` | 50-script video-explainer arc narrated by Janet. |
| `serving/` | AWS cloud-base. Single source of truth for every AWS resource. |
| `managing/` | Daily watcher over the constellation. Observe-only — no commits, no deploys, no mutations. |
| `donating/` | The six-month public donation drive backing the framework (2026-06-01 → 2026-12-01). |

## Cross-subproject conventions worth publishing

The conventions below cross subproject boundaries. They are the
rules the assistant has to remember without re-reading the whole
codebase.

### Language split

- TypeScript for the VSCode extensions and the Astro sites.
- Python for the trading agents and the kernel drivers.
- Lean4 for the formal kernels (`proving/`, `accounting/`).
- A Python microservice is allowed as an escape hatch for heavy
  numerics. Never reach across: trading Python does not import
  from analyzing TypeScript; analyzing TS does not import from
  trading.

### Canonical OHLCV bar shape

Every place that produces or consumes bar data uses the same column
set: `{ ts, o, h, l, c, v, adj_c }`. No `t` instead of `ts`, no
missing `adj_c`, no vendor field names past the client module.
Adapters translate at the boundary.

### GICS sector classification

Mapping is shared data, not shared code: a Parquet file keyed by
symbol with the canonical GICS hierarchy. Analyzers and traders
read via thin loaders; neither writes. Refresh runs through a
single seed script.

### Defined-risk options

Code that constructs, evaluates, or submits options orders is
restricted to: `long_call`, `long_put`, `debit_spread_call`,
`debit_spread_put`, `covered_call`, `protective_put`. Enforced at
both authoring time (a skill) and runtime (an agent). Applies to
analyzer-side tooling too.

### Data hubs, not shared code

When two subprojects need the same data, the data lives at a
canonical path under `data/<name>/` (Parquet or JSON), with each
subproject reading via a thin per-side loader. Subprojects do not
import each other's code. Two examples currently:

- A status-hub JSON slot per subproject, aggregated by the
  designing/ site at build time.
- The donation-drive JSON consumed by both Astro sites.

### Session lifecycle

Sessions start with `/open <project>` and end with `/close`. The
branch presence IS the write-lock; conflicting parallel sessions on
the same scope are blocked by branch existence. Cross-subproject
edits queue as deferred hints picked up later by `/do-claude-updates`.

### Status hub

Every subproject writes a status JSON describing the panels it
exposes; the designing/ site reads every slot at build time and
renders `/status`. No cross-subproject TypeScript imports — the
JSON hub is the only seam. This is the canonical example of
*data-hub-not-shared-code*.

## What you will not find here

- The private working tree itself (twelve subprojects, the
  filing hub, the redacted legal drafts).
- Per-subproject implementation code — that lives in the
  per-subproject public repos.
- Anything tied to ongoing litigation that has not already entered
  the federal-court public record.

## Cadence

Refreshed weekly from the private working tree's root and
per-subproject `CLAUDE.md` files. Re-rankings, new subprojects, and
new cross-subproject conventions are committed as ordinary diffs —
the commit log is the change record.

## Contact

[`quantapix@gmail.com`](mailto:quantapix@gmail.com)

## License

Apache-2.0 (`LICENSE.txt`). Code-class repo — Lean axioms,
predicate stubs, and framework code are reused under the standard
Apache patent grant.
