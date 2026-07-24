# CLAUDE.md — shorting/

Project-specific rules for the qagents adversarial-review subproject.
Assumes Claude Code's default guidance and the repo-root
`qagents/CLAUDE.md`. Don't re-litigate those.

## 1. Role — adversarial review, observe-only

`shorting/` reads the entire qagents tree and looks for things that are
fragile, wrong, over-promised, mis-aligned, or that will break under load
— "shorting positions," in the equities-analogy sense: places to bet
*against* the current state of the codebase. The output is a per-target
findings file under `shorting/positions/<target>/<date>.md`.

This is the **adversarial sibling of `managing/`**. `managing/` is
constructive (top-5 issues + top-10 tasks + completion %, calm voice,
report-then-recommend); `shorting/` is destructive (10 short positions
per target, explicitly hostile voice, no recommendations — just the
case for the short).

`shorting/` is **observe-only**, the same governance class as
`managing/`:

- Reads the whole qagents tree (every subproject + `data/` + `code/` +
  `lib/` + `legal/`).
- Writes only its own subtree — `shorting/positions/`,
  `shorting/shorten/` (the do-shorten lane, § 4a), `shorting/share/`
  (the do-share lane, § 4b), and `shorting/spread/` (the do-spread lane,
  § 4c) — plus the status-hub
  emit (`scripts/status_emit.mjs`, root-conventions pending lane).
- Never `git push`, `git commit`, `git add`, deploys, or mutates code in
  other subprojects.
- Never edits another subproject's `CLAUDE.md` to "respond to" a
  finding — findings are read by the human and routed back through
  `managing/` (see § 5 below).

## 2. Clean-context top-tier-model subagent — required, not optional

Each `shorting` run spawns one top-tier-model subagent **per target** in a clean
context. The subagent receives:

- The target name (e.g. `analyzing`, `qagents`, `publishing/quantapix`).
- The verbatim adversarial brief (from this file, § 3).
- The target's CLAUDE.md(s) and a directory listing — but **not** any
  prior `shorting/positions/<target>/*.md` files.

Why clean context per target: prior-run outputs bias a re-read toward
confirm-and-re-rank rather than re-discovery, and the parent session's
constructive framing softens the read. Each target gets a fresh hostile pass.

Implementation: the parent `/open shorting` session spawns one subagent per
in-scope target via the Agent tool (`subagent_type: general-purpose`,
`model` omitted — fleets inherit the orchestrator's model; root CLAUDE.md
§ Model policy). Each writes exactly one
`shorting/positions/<target>/<date>.md` and returns nothing else.

### 2.1 Default target scope — code-bearing + product-copy, not legal drafts

Default scope for an unparameterised `/open shorting` run: **every
subproject in the root CLAUDE.md roster except the legal-drafting pair**
(`appealing/`, `pleading/`) **and `shorting/` itself**, plus `qagents`
(root constellation) and `publishing/quantapix/` (public-facing staging
copy). The `legal/` corpus is likewise excluded. The roster is the source
of truth — new subprojects (e.g. `extending/`, `developing/`) enter scope
automatically.

Why the legal exclusion: legal drafts are adversarial by domain already —
their failure modes (court-rule compliance, evidentiary gaps) need a
domain-expert re-read, not a hostile structural critique — and
redaction-sensitive content quoted in a finding would land in
`shorting/positions/` outside the legal subprojects' redaction
guardrails. Opt-in by naming the target explicitly
(`/open shorting appealing`); the parent session asks for confirmation
before dispatching a subagent at an excluded target.

## 3. Adversarial brief (subagent prompt template)

Each subagent receives the same brief, parameterized only by target:

```
You are an adversarial reviewer. The target is `<target>`.

Read the target's CLAUDE.md, README, and source layout. Then write 10
"shorting positions" — concrete, specific, falsifiable claims about
why the target as currently designed will fail, leak value, embarrass
the user, or be discovered to be wrong.

Each position must include:
  - title (one line, hostile but precise)
  - one paragraph explaining the position
  - reproduction recipe: commands, file:line citations, or external
    checks that a sceptical reader can run to verify the failure mode
  - falsifier: what would make this position wrong (so the user knows
    when to close it)

Do not recommend fixes. Do not soften. Do not balance with strengths.
This is the bear case, by design — `managing/` carries the bull case.

Avoid easy targets: typos, missing tests for low-stakes code, "could
be more documented." A position must be specific to `<target>`'s
design, not generic advice.

Write to `shorting/positions/<target>/<date>.md`. No other output.
```

The voice override (hostile-but-precise) is session-scoped to
`shorting/` only — same pattern as the YouTube voice override for
`explaining/`. It does not propagate to other subprojects' files.

## 4. Output layout

```
shorting/
  CLAUDE.md
  positions/<target>/<YYYY-MM-DD>.md   one file per run; never overwritten
  shorten/<YYYY-MM-DD>/                do-shorten lane (§ 4a)
  share/<YYYY-MM-DD>/                  do-share lane (§ 4b)
  spread/<YYYY-MM-DD>/                 do-spread lane (§ 4c)
  scripts/                             status_emit.mjs
  .claude/                             settings.json; skills → ../../.claude/skills
```

Each positions `<date>.md` carries exactly 10 numbered positions plus the
run's target, model, and parent-branch metadata at the top. Never overwrite
— a later date is a follow-up read, not a replacement. Lane dirs are one
per run, likewise never overwritten.

### 4a. do-shorten lane — `shorting/shorten/<date>/`

Constellation-wide charter + spec coherency/conciseness review (first run
2026-07-02): clean-context unit reviewers + a synthesis pass emit per-unit
reports, a consolidated `BLUEPRINT.md`, and an `apply-shorten.md` action
prompt. Same observe-only governance + managing-routing as `positions/`.
Skill `/do-shorten`. Normative:
`data/charters/shorting/review-lanes/CHARTER.md` § lane-shorten; absorbed
anchor `data/charters/shorting/specs/do-shorten-2026-07-02/SPEC.md`.

### 4b. do-share lane — `shorting/share/<date>/`

Cross-axis sharing + learnings review of the axiomatize program
(proving/dau · accounting/dat · studying/dao; first run 2026-07-04): one
investigator per axis + a cross-axis unit over specs AND implementations
AND tests; emits per-unit reports, `BLUEPRINT.md`, `apply-share.md`. The
apply sessions it prompts maintain the `axiomatize-shared` subspec, the
cross-axis LEARNINGS ledger, and the G1–G7 conformance matrix. Same
governance as 4a. Skill `/do-share`. Normative: § lane-share; absorbed
anchor `data/charters/shorting/specs/do-share-2026-07-04/SPEC.md`.

### 4c. do-spread lane — `shorting/spread/<date>/`

Capacity + relocation review of the critical-context surfaces + the dco
shrink machinery — the counterweight to `/dco` (first run 2026-07-04).
Thesis: spread (Extract / Split / Demote) before shrink; spread never
deletes. Same governance as 4a. Skill `/do-spread`. Normative:
§ lane-spread; absorbed anchor
`data/charters/shorting/specs/do-spread-2026-07-04/SPEC.md`.

## 5. Hand-off to `managing/`

`managing/` reads `shorting/positions/<target>/<date>.md` files in its
daily run and decides which positions to:

- Promote into a `managing/checks/<date>.md` finding (evidence-backed,
  needs action).
- Note in `managing/reports/<date>.md` as "investigated, dismissed
  with reason".
- Ignore (out of scope, off-target, already covered).

The decision lives in `managing/`, not `shorting/`. `shorting/` does
not file issues or PRs; its only job is to surface the bear case in a
form `managing/` can route. Cross-reference flow:

```
shorting/ (find) ──► managing/ (decide) ──► subproject /open session (act)
```

This split is deliberate: separating discovery from triage lets
`shorting/` be hostile without that hostility leaking into actionable
work plans.

## 6. Scope boundary

This subproject does not import from `analyzing/`, `trading/`,
`proving/`, etc., and they do not import from here. The only outbound
dependency is *content* — adversarial findings that flow into
`managing/`'s daily watch.

## 7. Refresh cadence

On-demand — no cron lane. The operator invokes `/open shorting` (or a lane
skill) for a fresh read; the session writes its dated outputs and closes.
