# data/specs/

**Kind:** convention-anchor
**Producer-of-record:** sessions (manual promote from
`data/tmp/<slug>-<date>{.md,/}` once a spec is cited by skills, docs, or
sibling specs — per the adopted-spec convention)
**Consumers:** every subproject's `CLAUDE.md` (cross-refs by relpath);
the `/open` / `/close` / `/do-claude-updates` skills; `managing/` (daily
`specs-audit.sh` pass — phase tally, tests conformance, layout lint);
future spec authors who diff for prior decisions
**Schema:** one `<slug>-<date>/` **family directory** per spec at the
directory root, holding `SPEC.md` (+ optional `TODO.md`, `tests/`,
subspec dirs) — per `specs-family-layout-2026-06-10/SPEC.md`. The
family layout is the only valid shape (the dual-format migration
window closed at Phase 4, 2026-06-10); a flat root entry is a LAYOUT
correctness finding.
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

## Family directory shape — `<slug>-<date>/`

One directory per spec family (root spec + its tests + its
amendments/subspecs and *their* tests + a running-observations
`TODO.md`). Full contract: `specs-family-layout-2026-06-10/SPEC.md`
§ 3; load-bearing summary:

```
data/specs/<slug>-<date>/            # family; name = root spec's slug-date, frozen
├── SPEC.md                          # the root spec; ≤ 1,000 lines (hard cap)
├── TODO.md                          # optional — running observations
├── tests/                           # root spec's suite; required once implementable
│   ├── README.md
│   ├── run.sh
│   ├── cases/                       # suite files (bash t_<NN>_*.sh or pytest)
│   └── lib/                         # optional shared helpers
└── <subslug>-<date>/                # amendment / optional subspec; zero or more
    ├── SPEC.md                      # ≤ 1,000 lines; carries **Parent:** ../SPEC.md
    ├── TODO.md                      # optional
    └── tests/                       # same shape as the root tests/
```

- The family directory is named after the **root spec's** slug-date and
  frozen at creation — amendments never rename it (slug-date stays the
  audit's age/ledger anchor; worktree checkouts reset mtime —
  `feedback_slug_date_over_mtime_for_audits`).
- Every subdirectory is either `tests/` or a subspec dir containing
  `SPEC.md`. Nesting is exactly two levels (family root + subspecs);
  a subspec that needs its own subspec becomes a new family. Subspec
  names drop the family slug prefix and carry their own date.
- Loose supporting artifacts (diagrams, sample JSON) are allowed at
  family/subspec root. Phase markers are parsed from SPEC.md **only**.
- **Amendment vs. new family:** a document is a subspec iff its
  `**Trigger:**` names the family's root spec as the thing being
  amended/extended. Sibling programs and framework *instances*
  (debates run under `debate-framework`, calibration pilots) stay
  separate families. When ambiguous, default to a new family.
- **Citation form:** root `data/specs/<slug>-<date>/SPEC.md`; subspec
  `data/specs/<slug>-<date>/<subslug>-<date>/SPEC.md`; tests
  `data/specs/<slug>-<date>/tests/`. Prose shorthand "spec
  `<slug>-<date>`" stays valid.

## SPEC.md shape

Every SPEC.md (root or subspec) carries the same load-bearing skeleton
so `managing/scripts/specs-audit.sh` can extract a phase tally without
heuristics.

```markdown
# <Title>

**Status:** <one of: in-flight | adopted | adopted (Phase N shipped) | superseded by <slug>-<date>>
**Date:** <YYYY-MM-DD>          ← authoring date; never updated post-adoption
**Parent:** ../SPEC.md          ← subspecs ONLY (always that literal relpath); roots must omit
**Scope:** <one sentence — qagents-wide | <sub>-only | cross-cutting (<list>)>
**Trigger:** <optional — what forced the spec; OK to omit>
**Tests:** <`tests/` once authored; "none — design-only" if no implementable surface>

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
`tests/cases/` where possible. "Manual-acceptance"
items list the human-eyeball check; cite where the artifact lives.

## N+2. Open questions

Numbered. Marked `[VERIFY]` if waiting on external input (Anthropic
docs, third-party API, court ruling); marked `[RESOLVED <date>]`
inline once closed.

## N+3. References

Other `data/specs/*/SPEC.md`, memory files (`memory/<name>.md`
relpaths), upstream docs (links), or PR / commit shas. Plain bullet list.
```

Sections 1–3 may be retitled freely (different specs frame their
opening differently); the **`**Status:**` / `**Date:**` / `**Scope:**`
header block** (+ `**Parent:**` on subspecs), the **`## Phases` ledger**
with `[shipped]/[in-flight]/[planned]/[deferred]` markers, and the
**`## Acceptance criteria` section** are the load-bearing parts. The
audit reads them; everything else is prose.

**1,000-line hard cap:** `wc -l` on any SPEC.md must be ≤ 1,000.
Over-cap is a correctness finding (managing checker). The cap covers
SPEC.md only; TODO.md, tests, and artifacts are uncounted. The escape
valves are "shorten" and "carve a meaningful subspec" — never "raise
the cap" and never a mechanical cut at line 1,000 (the root keeps the
header block, motivation, core design, the **original Phases ledger
intact**, acceptance criteria, and a one-line pointer per carved
subspec).

### Status transitions

| from           | event                                      | to                                |
|----------------|--------------------------------------------|-----------------------------------|
| (n/a)          | first draft lands in `data/tmp/`           | `in-flight` (file lives in `data/tmp/`) |
| `in-flight`    | spec cited by ≥ 1 other doc + first commit | `adopted` (draft `git mv`'d into `data/specs/` family form) |
| `adopted`      | first phase ships                          | `adopted (Phase N shipped)` (status-line edit, not new file) |
| any            | a successor spec lands                     | `superseded by <slug>-<date>` (status-line edit; family stays put) |

A spec at `adopted` with `[planned]` phases is **normal** — that's the
backlog managing/ tracks. A spec at `adopted` with all phases
`[shipped]` is **closed**. A family is closed when the root and every
subspec are closed.

## TODO.md — running observations (optional)

Per family root and per subspec. The structural home for "we noticed X
but it isn't worth a spec change yet" — reviewed first by whoever
drafts the next amendment.

- **Shape:** dated bullets, append-only between amendments:
  `- <YYYY-MM-DD> <observation / amendment seed / test gap>`. No phase
  markers (SPEC.md-only).
- **Consumption:** consumed (or judged-wrong) items are **deleted** in
  the amendment commit (retire-don't-tombstone).
- **Not a backlog:** anything actionable today goes to
  `data/next-steps/<sub>.md` or a `[planned]` phase.
- **Audit posture:** tally-only (count + oldest-item date); growth past
  ~100 lines is a consistency smell, not a correctness finding.

---

## tests/ shape

Every SPEC.md with an implementable surface ships a sibling `tests/`
directory (family-level for the root spec, subspec-level for a
subspec — suite granularity matches SPEC.md granularity). The shape is
uniform so a single `run.sh` invocation runs the suite from any caller.
`managing/scripts/specs-audit.sh` validates this shape; missing pieces
are correctness findings.

```
<…>/tests/
├── README.md       # required — purpose, run command, what's tested, what's deferred
├── run.sh          # required — executable; exits 0 on pass, non-zero on fail
├── cases/          # required — suite files
│   ├── …           # pytest:   test_<topic>.py + conftest.py (+ sys.path setup)
│   └── …           # bash:     t_<NN>_<topic>.sh  (numbered, sortable)
└── lib/            # optional — shared helpers (assert.sh for bash; or pytest fixtures)
```

### `README.md` contract

Four required sections; everything else is optional prose.

1. **Run** — exact command from repo root
   (`bash data/specs/<family>/tests/run.sh`, or subspec-nested).
2. **Layout** — tree of `cases/` + `lib/` with one-line purpose per file.
3. **What's tested** — bullets keyed to spec section numbers.
4. **What's deferred** — bullets keyed to spec phases not yet shipped.

### `run.sh` contract

- Shebang `#!/usr/bin/env bash`; `set -uo pipefail` (not `-e` — the
  runner sums failures itself).
- Resolves `QAGENTS_REPO_ROOT` from `$1` → env → relative fallback
  (family-level `tests/`: `$(cd "$THIS_DIR/../../../.." && pwd)`;
  subspec-level adds one more `..`).
- Iterates `cases/` (sorted), runs each in a subshell with `LIB_DIR`
  exported, prints `─── <name> ───` then PASS/FAIL.
- Tail: `Total / Passed / Failed` line + per-fail list; `exit "$failed"`.
- For pytest harnesses: delegates to `pytest cases/` after resolving
  the venv (`$REPO/.venv/bin/python` → `python3.13`); the same
  Total/Failed contract applies via pytest's own exit code.

### `cases/` contract — one suite at a time

- **Bash** (default for shell-script implementations): files named
  `t_<NN>_<short_topic>.sh`, sourced from `${LIB_DIR}/lib.sh` (or
  `assert.sh`), exit non-zero on first failed assertion.
- **Pytest** (when implementation is Python): files named
  `test_<topic>.py`; `conftest.py` prepends the implementation root to
  `sys.path` so tests resolve `from <pkg> import …` without an editable
  install. No `pytest-asyncio` unless the suite genuinely needs it.

Pick one harness per spec — do not mix. The exemplar is
`specs-family-layout-2026-06-10/tests/` (bash). Legacy
`<slug>-<date>-tests/` dirs (inner suite dir named `tests/` instead of
`cases/`) remain valid until their family migrates.

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
- A SPEC.md over 1,000 lines is an over-cap correctness finding; a
  root-level entry that is neither `CLAUDE.md` nor a family dir, a
  family subdir that is neither `tests/` nor a `SPEC.md`-bearing
  subspec, a subspec missing `**Parent:**` (or a root carrying one),
  or nesting deeper than two levels is a layout correctness finding.

A spec without a `## Phases` ledger is treated as "design-only" by
the audit (single implicit phase: the spec itself landed). That's
the right shape for retrospectives, naming conventions, etc. — no
tally entry, no test dir required.
