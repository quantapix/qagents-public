# data/specs/

**Kind:** convention-anchor
**Producer-of-record:** sessions (manual promote from an in-flight
`data/tmp/<slug>-<date>.md` once a spec is cited by skills, docs, or sibling
specs)
**Consumers:** every subproject's `CLAUDE.md` (cross-refs by relpath); the
session-lifecycle skills; the daily watcher's spec audit; future spec
authors who diff for prior decisions
**Refresh cadence:** per-session (promote when a spec is adopted)
**Write-lock posture:** the data write-lock (promotion is a single `git mv`
inside `/close`)

Specs are landed forever — even if the implementation is later superseded,
the original spec file is the historical anchor for "why X shape." Completed
plans that are no longer load-bearing belong in a subproject's own
`history/`, not here.

## Spec file shape — `<slug>-<date>.md`

Every spec carries the same load-bearing skeleton so the audit can extract a
phase tally without heuristics. Pinned **prospectively** — existing specs
are not retrofitted; new specs MUST conform. A header block (`Status` /
`Date` / `Scope` / optional `Trigger` / `Tests`), then prose sections (1–3,
retitled freely), then a `## Phases` ledger and a `## Acceptance criteria`
section.

The header `Status` is one of: `in-flight` | `adopted` |
`adopted (Phase N shipped)` | `superseded by <slug>-<date>`. `Date` is the
authoring date, never updated post-adoption.

## Phases ledger — the audit surface

Every spec with an implementable surface lists its phases as a bulleted
ledger, one line per phase, leading marker one of:

- **[shipped]** `<date>` Phase N — <summary>
- **[in-flight]** Phase N — <summary> (touched `<date>`)
- **[planned]** Phase N — <summary>
- **[deferred]** Phase N — <summary> (reason: …)

The markers are machine-readable. A phase at `[in-flight]` for more than 14
calendar days is flagged as a stall risk. `[deferred]` requires a `(reason:
…)` parenthetical. A spec without a `## Phases` ledger is treated as
"design-only" (the spec itself landed) — the right shape for
retrospectives + naming conventions.

### Status transitions

| from | event | to |
|---|---|---|
| (n/a) | first draft lands in `data/tmp/` | `in-flight` |
| `in-flight` | cited by ≥ 1 other doc + first commit | `adopted` (file `git mv`'d here) |
| `adopted` | first phase ships | `adopted (Phase N shipped)` |
| any | a successor spec lands | `superseded by <slug>-<date>` |

## Tests dir shape — `<slug>-<date>-tests/`

Every spec with an implementable surface ships a companion tests directory
with a uniform shape: a required `README.md` (run command, layout,
what's-tested keyed to spec sections, what's-deferred keyed to phases), a
required executable `run.sh` (resolves the repo root, iterates the suite,
prints a Total/Passed/Failed tail, exits with the failure count), and a
`tests/` dir. Pick one harness per spec — bash (`t_<NN>_<topic>.sh`) or
pytest (`test_<topic>.py` + a `conftest.py` that sets up the import path) —
do not mix.
