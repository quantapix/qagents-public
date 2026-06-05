# data/specs/

**Kind:** convention-anchor
**Producer-of-record:** sessions (manual promote from
`data/tmp/<slug>-<date>.md` once a spec is cited by skills, docs, or
sibling specs — per the adopted-spec convention)
**Consumers:** every subproject's `CLAUDE.md` (cross-refs by relpath);
the `/open` / `/close` / `/do-claude-updates` skills; `managing/` (daily
`specs-audit.sh` pass — phase tally, tests conformance); future spec
authors who diff for prior decisions
**Schema:** one `<slug>-<date>.md` per spec at the directory root;
companion `<slug>-<date>-tests/` directory holds bash or pytest suites
(required once a spec has an implementable surface — see
`feedback_python_spec_tests_in_data_specs`)
**Refresh cadence:** per-session (promote when a spec is adopted)
**Write-lock posture:** `.data-write-lock` (manual lane) — promotion
is a single `git mv` inside `/close`

Specs are landed forever — even if the implementation is superseded
later, the original spec file is the historical anchor for "why X
shape." Completed plans that are no longer load-bearing (the kind
that would otherwise rot here) belong in `serving/history/` (or each
subproject's own `history/`), not in `data/specs/`. See
`feedback_serving_history_for_completed_plans`.

---

## Spec file shape — `<slug>-<date>.md`

Every spec under this directory carries the same load-bearing skeleton
so `managing/scripts/specs-audit.sh` can extract a phase tally without
heuristics. Pinned **prospectively** — existing specs are not flagged
for retrofit; new specs MUST conform.

```markdown
# <Title>

**Status:** <one of: in-flight | adopted | adopted (Phase N shipped) | superseded by <slug>-<date>>
**Date:** <YYYY-MM-DD>          ← authoring date; never updated post-adoption
**Scope:** <one sentence — qagents-wide | <sub>-only | cross-cutting (<list>)>
**Trigger:** <optional — what forced the spec; OK to omit>
**Tests:** <relpath to <slug>-<date>-tests/ once authored; "none — design-only" if no implementable surface>

---

## 1. <Motivation | Why now | Background>

…prose…

## 2. <Scope | Inventory | Today's pattern>

…what's in / out of scope; what exists pre-spec…

## 3. <Design | Mechanics | Shape>

…the load-bearing technical content…

## N. Phases

Every spec with an implementable surface lists its phases here as a
bulleted ledger. One line per phase, leading marker MUST be one of:

- **[shipped]** `<YYYY-MM-DD>` Phase <N> — <one-line summary>
- **[in-flight]** Phase <N> — <one-line summary> (touched <YYYY-MM-DD>)
- **[planned]** Phase <N> — <one-line summary>
- **[deferred]** Phase <N> — <one-line summary> (reason: <…>)

Marker tags are the audit surface. `specs-audit.sh` counts
`[shipped]/[in-flight]/[planned]/[deferred]` per spec; the daily
`checks/<date>.md` carries a tally section. Use `[shipped] <date>`
to record completion — that anchors burn-down trend in `reports/`.

Phase numbering is per-spec; Roman or Arabic both fine; "Phase 0"
common for groundwork.

## N+1. Acceptance criteria

Bulleted, testable. Each item maps 1:1 to a test in
`<slug>-<date>-tests/tests/` where possible. "Manual-acceptance"
items list the human-eyeball check; cite where the artifact lives.

## N+2. Open questions

Numbered. Marked `[VERIFY]` if waiting on external input (Anthropic
docs, third-party API, court ruling); marked `[RESOLVED <date>]`
inline once closed.

## N+3. References

Other `data/specs/*.md`, memory files (`memory/<name>.md` relpaths),
upstream docs (links), or PR / commit shas. Plain bullet list.
```

Sections 1–3 may be retitled freely (different specs frame their
opening differently); the **`**Status:**` / `**Date:**` / `**Scope:**`
header block**, the **`## Phases` ledger** with `[shipped]/[in-flight]/[planned]/[deferred]`
markers, and the **`## Acceptance criteria` section** are the load-bearing
parts. The audit reads them; everything else is prose.

### Status transitions

| from           | event                                      | to                                |
|----------------|--------------------------------------------|-----------------------------------|
| (n/a)          | first draft lands in `data/tmp/`           | `in-flight` (file lives in `data/tmp/`) |
| `in-flight`    | spec cited by ≥ 1 other doc + first commit | `adopted` (file `git mv`'d to `data/specs/`) |
| `adopted`      | first phase ships                          | `adopted (Phase N shipped)` (status-line edit, not new file) |
| any            | a successor spec lands                     | `superseded by <slug>-<date>` (status-line edit; file stays put) |

A spec at `adopted` with `[planned]` phases is **normal** — that's the
backlog managing/ tracks. A spec at `adopted` with all phases
`[shipped]` is **closed** — fine, leaves the audit's "uncompleted"
column at zero.

---

## Tests dir shape — `<slug>-<date>-tests/`

Every spec with an implementable surface ships a companion
`<slug>-<date>-tests/` directory. The shape is uniform so a single
`run.sh` invocation runs the suite from any caller (CI later, manual
now). `managing/scripts/specs-audit.sh` validates this shape;
missing pieces are correctness findings.

```
data/specs/<slug>-<date>-tests/
├── README.md       # required — purpose, run command, what's tested, what's deferred
├── run.sh          # required — executable; exits 0 on pass, non-zero on fail
├── tests/          # required — suite files
│   ├── …           # pytest:   test_<topic>.py + conftest.py (+ sys.path setup)
│   └── …           # bash:     t_<NN>_<topic>.sh  (numbered, sortable)
└── lib/            # optional — shared helpers (assert.sh for bash; or pytest fixtures)
```

### `README.md` contract

Four required sections; everything else is optional prose.

1. **Run** — exact command from repo root (`bash data/specs/<slug>-<date>-tests/run.sh`).
2. **Layout** — tree of `tests/` + `lib/` with one-line purpose per file.
3. **What's tested** — bullets keyed to spec section numbers.
4. **What's deferred** — bullets keyed to spec phases not yet shipped
   (e.g. "Phase 2 real-SDK call — gated on § 9.1").

### `run.sh` contract

- Shebang `#!/usr/bin/env bash`; `set -uo pipefail` (not `-e` — the
  runner sums failures itself).
- Resolves `QAGENTS_REPO_ROOT` from `$1` → env → `$(cd "$THIS_DIR/../../.." && pwd)`.
- Iterates `tests/` (sorted), runs each in a subshell with `LIB_DIR`
  exported, prints `─── <name> ───` then PASS/FAIL.
- Tail: `Total / Passed / Failed` line + per-fail list; `exit "$failed"`.
- For pytest harnesses: delegates to `pytest tests/` after resolving
  the venv (`$REPO/.venv/bin/python` → `python3.13`); the same
  Total/Failed contract applies via pytest's own exit code.

### `tests/` contract — one suite at a time

- **Bash** (default for shell-script implementations): files named
  `t_<NN>_<short_topic>.sh`, sourced from `${LIB_DIR}/lib.sh` (or
  `assert.sh`), exit non-zero on first failed assertion.
- **Pytest** (when implementation is Python): files named
  `test_<topic>.py`; `conftest.py` prepends the implementation root to
  `sys.path` so tests resolve `from <pkg> import …` without an editable
  install. No `pytest-asyncio` unless the suite genuinely needs it.

Pick one harness per spec — do not mix. The exemplars are
`data-charter-2026-05-17-tests/` (bash) and
`agent-sdk-adoption-2026-05-17-tests/` (pytest). The legacy flat
`open-close-skills-tests/` layout (no `tests/` subdir, `t_*.sh` at
root) is grandfathered; do not replicate it for new specs.

---

## Phase markers protocol — what `specs-audit.sh` extracts

The marker tags `[shipped]`/`[in-flight]`/`[planned]`/`[deferred]` at
the start of phase ledger bullets are the audit's machine-readable
surface. Spec authors maintain them; the daily watcher reads them.

- A phase moves to `[shipped] <YYYY-MM-DD>` when its acceptance
  criteria pass (tests green or manual-eyeball confirmed). Do not
  mark `[shipped]` for partial completion — partial is `[in-flight]`.
- A phase at `[in-flight]` for more than 14 calendar days is flagged
  by `specs-audit.sh` as a stall risk; managing/checker surfaces it
  as a correctness finding.
- A phase at `[planned]` with no `[in-flight]` predecessor in the
  same spec is fine — that's normal backlog.
- `[deferred]` requires a `(reason: …)` parenthetical; the audit
  lints for its presence.

A spec without a `## Phases` ledger is treated as "design-only" by
the audit (single implicit phase: the spec itself landed). That's
the right shape for retrospectives, naming conventions, etc. — no
tally entry, no test dir required.
