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
subspec dirs). The family layout is the only valid shape; a flat root
entry is a LAYOUT correctness finding.
**Refresh cadence:** per-session (promote when a spec is adopted)
**Write-lock posture:** `.data-write-lock` (manual lane) — promotion
is a single `git mv` inside `/close`

**Single normative owner: `data/charters/qagents/spec-lifecycle/CHARTER.md`**
— this stub keeps only the machine-consumed shapes needed at the moment of
touching the dir; every rule below is a render of a charter section (tagged),
and on any divergence the charter wins.

Specs are landed forever — even when superseded, the original spec is the
historical anchor for "why X is shaped this way" (charter § 1). Completed
plans that are no longer load-bearing belong in `serving/history/` (or a
subproject's own `history/`), not here
(`feedback_serving_history_for_completed_plans`). Mature, owned, shipped
machinery graduates to a `data/charters/<scope>/<slug>/` charter; the
absorbed family stays put carrying the absorption marker (charter § 2.4).

**Residence is a location transition, not a status** (charter § 2.4,
charter-scopes-2026-07-16): a closed + solely-owned + unreserved + uncoupled
family may relocate `data/specs/<fam>/ → data/charters/<scope>/specs/<fam>/`
(one whole-family `git mv`, body byte-unchanged); an in-flight amendment or
reactivation **de-migrates** it back here. New specs never land scope-side —
`data/tmp/` promotion always targets `data/specs/` (unchanged).

---

## Family shape (charter § 2.1)

```
data/specs/<slug>-<date>/            # family; name = root spec's slug-date, frozen
├── SPEC.md                          # ≤ 1,000 lines (hard cap; charter § 2.2)
├── TODO.md                          # optional — running observations (charter § 2.6)
├── tests/                           # README.md + run.sh + cases/ (+ lib/) — charter § 2.5
└── <subslug>-<date>/                # subspec; SPEC.md carries **Parent:** ../SPEC.md
    └── (SPEC.md, TODO.md, tests/)   # nesting is exactly two levels
```

Every family subdir is `tests/` or a `SPEC.md`-bearing subspec; ruled
exemptions live in `data/charters/qagents/spec-lifecycle/carve-outs.txt`
(+ signoff dirs derived from `.claude/skills/do-signoff/registry.tsv`).
A document is a subspec iff its `**Trigger:**` names this family's root
spec; framework *instances* are never subspecs; when ambiguous, new
family (charter § 2.8).

## SPEC.md header + phase markers (charter §§ 2.2–2.3)

Header block directly under the title, then `---`:

```markdown
**Status:** <in-flight | adopted | adopted (Phase N shipped) |
             superseded by <slug>-<date> |
             relocated into <family> as a child |
             absorbed into data/charters/<scope>/<slug>/ <YYYY-MM-DD>>
**Date:** <YYYY-MM-DD>          ← authoring date; never updated post-adoption
**Parent:** ../SPEC.md          ← subspecs ONLY; roots must omit
**Scope:** <one sentence>
**Trigger:** <optional>
**Tests:** <tests/ | none — design-only | charter suite relpath post-absorption>
```

Phase-ledger bullets lead with `**[shipped]** <date>` / `**[in-flight]**`
(> 14d = stall finding) / `**[planned]**` / `**[deferred]** … (reason: …)`.
No `## Phases` ledger = design-only. Both the header trio and the markers
are lint-enforced pre-landing (`/close --lint-specs`, exit 45) and daily
(`managing/scripts/specs-audit.sh`) — charter § 2.10.

## Status transitions (charter § 2.4)

| from | event | to |
|---|---|---|
| (n/a) | first draft lands in `data/tmp/` | `in-flight` |
| `in-flight` | cited by ≥ 1 other doc + first commit | `adopted` (promoted to family form) |
| `adopted` | first phase ships | `adopted (Phase N shipped)` |
| any | successor spec lands | `superseded by <slug>-<date>` (family stays put) |
| `adopted` | folded into another family | `relocated into <family> as a child` |
| `adopted` (all shipped) | ratified charter absorbs the family | `absorbed into data/charters/<scope>/<slug>/ <date>` — header-block edits only; body byte-unchanged; family stays put forever |
| `in-flight` (charter amendment) | ratified amendment applied | `absorbed into … <date>` from birth, as a subspec of the charter's anchor family |

## Citation forms (charter § 2.9)

Root `data/specs/<slug>-<date>/SPEC.md`; subspec
`data/specs/<slug>-<date>/<subslug>-<date>/SPEC.md`; tests
`data/specs/<slug>-<date>/tests/`; prose shorthand "spec `<slug>-<date>`".
Post-absorption the charter is the single current-contract citation.
The tests exemplar is `pending-promotion-scope-2026-05-28/tests/` (bash).
