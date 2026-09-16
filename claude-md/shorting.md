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
- Writes only its own subtree — `shorting/positions/`, `shorting/shorten/`
  (RETIRED, § 4a), `shorting/share/` (the sole live do-* lane, § 4b) and
  `shorting/spread/` (FROZEN history, § 4c) — plus the status-hub
  emit (`scripts/status_emit.mjs`, root-conventions pending lane) and the
  ONE chartered parent-session-only ROUTING exception
  (`data/charters/shorting/review-lanes/CHARTER.md` § common, invariant
  I1): § 3-class charter todos under `data/charters/<scope>/todos/`.
- Writes **its own charter tier** — `data/charters/shorting/**` — under the
  shared `.data-write-lock`, for ratified amendments only (the
  `data/charters/CLAUDE.md` § Amendment lane: a `data/tmp/` draft, ratified
  by debate or operator ruling, applied by the owner scope's session).
  **Amending one's own charter is not "routing"** and was never covered by
  the exception above: LEDGER 15 landed this way on 2026-09-10 and LEDGER 16
  on 2026-09-15 before anyone noticed the enumeration did not name the
  surface. Operator ruling 2026-09-15. Observe-only is unchanged — this is a
  write to shorting's OWN governance, never to a target's.
  Warn-cap `spread-review owed` items now file to the **qagents** slot
  (session-lifecycle § 2.8 E4 as re-pointed; shorting sessions are no
  longer the warn-cap scribe). A debate this subproject convenes
  writes its record to `data/debates/` (2026-07-14 precedent; the
  `/close` lift lane handles the foreign write).
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
(root constellation), `publishing/quantapix/` (public-facing staging
copy), and — a **named target since spread-merge-2026-08-09** (the
positions-lane independence grant, review-lanes § 4) — the
**optimization machinery** (`scripts/dco.sh` + `scripts/dco-helpers/`, the
dco skills/agents incl. the SPREAD-OP investigators,
`data/charters/qagents/optimization/`): the merged self-review trades the
old counterweight-lane independence for closed-loop latency, so this lane
owes the machinery a per-target adversarial read, not a glance. The
`legal/` corpus is likewise excluded. The roster is the source
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
  shorten/<YYYY-MM-DD>/                RETIRED do-shorten lane (§ 4a)
  share/<YYYY-MM-DD>/                  do-share lane (§ 4b)
  spread/<YYYY-MM-DD>/                 FROZEN do-spread history (§ 4c; live lane: data/summaries/spread/)
  reviews/<slug>-<YYYY-MM-DD>/         operator-directed one-off review reports (not a chartered
                                       lane). Two shapes so far. (a) RATIFIED: pairs with a
                                       data/debates/<slug>-<date>.md record — 2026-08-21 three-axis
                                       overhaul reviews (v2-post-debate is the standing artifact),
                                       2026-09-09 hub-goldens plan. (b) PROGRESS: units + FINDINGS.md
                                       of rulable recommendations, no debate — 2026-09-15 hub-goldens
                                       (rulings taken in-session, recorded at RULINGS.md in the run
                                       dir). Either shape: § adversarial binds it (§ 2.1a), a unit
                                       writes one report and nothing else, and no ns-* write verb runs
  appeals/<docket>/                    operator-directed adversarial-brief loop (not a chartered
                                       lane; four iterations 2026-09-05 → 09-07, CLOSED; § 4d)
  scripts/                             status_emit.mjs; quoted_string_check.py (re-verifies every
                                       quoted record passage against its pinned page — the one check
                                       that catches a brief quoting text the filed appendix no longer
                                       shows while the pin still resolves; five triage classes in its
                                       header, earned by five of its own bugs)
  .claude/                             settings.json; skills → ../../.claude/skills
```

Each positions `<date>.md` carries exactly 10 numbered positions plus the
run's target, model, and parent-branch metadata at the top. Never overwrite
— a later date is a follow-up read, not a replacement. Lane dirs are one
per run, likewise never overwritten.

### 4a. do-shorten lane — `shorting/shorten/<date>/` — **RETIRED 2026-07-28**

**Not a live lane.** Retired by `/do-retire` ruling **R-3**; R-4 purged the
run artifacts. Rationale, Exhibit A, and the R-18 confirmation:
`data/specs/do-retire-2026-07-26/` + memory `project_do_retire_spec.md`
(whose § 5.4-vs-§ 4a disposition is a CONTESTED operator REQUEST). The skill
and charter § lane-shorten survive on disk **until P5 fires**. An operator
may still direct a scoped run of the charter shape while the artifacts
exist (2026-08-08 precedent), but that is an explicit per-run revival, not
a standing offer.

Lane mechanism is not restated here — normative:
`data/charters/shorting/review-lanes/CHARTER.md` § lane-shorten (subject,
scope, partition, reviewer brief, output layout, skill contract, gotchas).
Same observe-only governance + managing-routing as `positions/`; absorbed
anchor `data/charters/shorting/specs/do-shorten-2026-07-02/SPEC.md`.

### 4b. do-share lane — `shorting/share/<date>/`

Cross-axis sharing + learnings review of the axiomatize program
(proving/dau · accounting/dat · studying/dao; first run 2026-07-04): one
investigator per axis + a cross-axis unit over specs AND implementations
AND tests; emits per-unit reports, `BLUEPRINT.md`, `apply-share.md`. The
apply sessions it prompts maintain the `axiomatize-shared` subspec, the
cross-axis LEARNINGS ledger, and the G1–G7 conformance matrix. Since
2026-08-23 the lane also re-grades the **overhaul-compliance matrix**
(needs × axes, seeded from the three 2026-08-21 v2 overhaul reports) every
run, pins an adjudication snapshot at step 1, and treats ratified
reviews/debates since the prior run as primary intake — all normative at
§ lane-share. Same
governance as 4a. Skill `/do-share`. Normative: § lane-share; absorbed
anchor `data/charters/shorting/specs/do-share-2026-07-04/SPEC.md`.

### 4c. do-spread lane — ABSORBED into qagents/optimization (frozen history)

The capacity + relocation review (first run 2026-07-04) was absorbed into
the dco pass as the **SPREAD-OP** on 2026-08-09 (spread-merge-2026-08-09;
subspec `data/charters/qagents/specs/dco-2026-05-26/spread-merge-2026-08-09/SPEC.md`).
Live contract: `data/charters/qagents/optimization/CHARTER.md` § 2.12; new
run dirs land at `data/summaries/spread/<ISO>/`; the skill retired (invoke
`/dco-manual spread`). `shorting/spread/` stays frozen where it landed
(registry-retired, never reaped); the absorbed anchor
`data/charters/shorting/specs/do-spread-2026-07-04/SPEC.md` is the history
rendering. Adversarial review of the merged machinery is now the positions
lane's named target (§ 2.1).

### 4d. appeals lane — `shorting/appeals/<docket>/` — CLOSED 2026-09-07

Operator-directed adversarial-brief loop over the operator's own appellate
briefs. **Not a chartered lane**: the § 2.1 legal exclusion was waived by
explicit direction, substance is routed to `appealing/` and never filed from
here, and the operator's `new-evidence-for-RA/` drops are not lane output.
Four iterations ran 2026-09-05 → 09-07; the loop is CLOSED on shorting's side.
**Bounded per-run revival, operator-ruled 2026-09-09 (P0-8 of
`data/debates/axiomatize-hub-goldens-2026-09-09.md`; the § 4a-style
per-run shape):** exactly two runs — (1) one v5 adversary simulation
against the 1152 brief **as filed**
(the private filing hub — what the
appellees actually have). ⚠ The "every MA paper is pending, read the OPERATIVE
set" clause is SUPERSEDED (SPEC § 3 R-2): **all 30 submissions were DOCKETED
9/10** — 1224's #7–#9 stamped on every page, 1152's #16–#42 by manual clerk
entry and labelled "Proposed" pending RE#16, with 0 of 214 pages stamped and no
stamped copy that will ever arrive. So the filed PDF IS the operative text here;
for 1152, state (ii) is the docket label on RE#16, not a document.
**Run 1 is `harvest_lint`- and RE#16-gated, never dated** (R-3; a simulated
appellee brief that argues from a withdrawal tests nothing), runs in
`/open shorting` after B12 (review-lanes § 2.1a, P0-16), and is preceded by the
operator's morning docket check. (2) The day-of their-pin verification arm
(`scripts/quoted_string_check.py` over the REAL appellee briefs) is **keyed on
SERVICE, never on a docketed due date**: earliest possible service 10/8, the
clerk's due date 10/16, and RE#16's disposition can re-key it. No interview, no
revision map, no filing; outputs under `appeals/`; substance routes to
`appealing/` as before. The lane closes again after the 1152 reply files —
**earliest 10/22, ≈ 10/30 on the docketed date, ≤ 11/2 if mailed**.
Per-iteration method and the record lessons: memory
`project_shorting_subproject` (§§ 2026-09-05 … appeals iteration 4) +
`project_appealing_subproject__log_2026_09`; the lane's own artifacts
(`00-Correction-Ledger-<date>.md`, `00-Operator-Theory-<date>.md` — the
drafting floor, `replies-v*/`, `responses-v4/`, `research-v*/`) stay in tree.

Four standing rules bind any adversarial pass over a subject its owner is
still writing, this lane's history being where they were earned:
**`data/charters/shorting/review-lanes/CHARTER.md` § 2.1a (§ adversarial)**
— the ratchet (a finding demands RESTATEMENT; only the owner withdraws an
assertion), symmetric verification (audit from iteration 1; grade the
argument, not the pin count), one copy with history as a git lookup, and the
extract rule. Granted 2026-09-15 as LEDGER 16 on operator ruling P0-16, which
also ruled the section binds the **positions** lane. The charter is the sole
copy; this § registers the lane and does not restate the rules. The
per-iteration method and the record lessons stay at memory
`project_shorting_subproject` (§§ 2026-09-05 … appeals iteration 4) +
`project_appealing_subproject__log_2026_09`.

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

**`managing/checks/` is a 7-day CARRIER, not an archive.** Since the
2026-07-29 do-retire P2 reap, all three promote targets rotate on a
7-day TTL (`data/specs/do-retire-2026-07-26/lanes.tsv`:
`managing/{reports,checks,tasks}/*`, `ephemeral`, archived to
`archive.blob`). A promoted finding is therefore durable only if the
**citing** side carries the substance — an ns item body, a charter, a
spec — because the `checks/` file it points at will be gone in a week
and a cite to it will dangle (`retire.sh --check-cites`, exit 46).
Promote AND land the substance somewhere that survives.

## 6. Scope boundary

This subproject does not import from `analyzing/`, `trading/`,
`proving/`, etc., and they do not import from here. The only outbound
dependency is *content* — adversarial findings that flow into
`managing/`'s daily watch.

## 7. Refresh cadence

On-demand — no cron lane. The operator invokes `/open shorting` (or a lane
skill) for a fresh read; the session writes its dated outputs and closes.
