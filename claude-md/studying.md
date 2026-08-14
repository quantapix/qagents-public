# CLAUDE.md — studying/

Project-specific rules for the **operational-axis Lean4 kernel + cross-axis
representation research** subproject. Assumes Claude Code's default guidance
and the repo-root `qagents/CLAUDE.md`. Don't re-litigate those.
Scope charter: `data/charters/studying/operational-axis/CHARTER.md` — the whole
`lean4-charter-2026-06-10` family (root of the three-axis architecture; root
CLAUDE.md § "Lean4 axes") is scope-resident at
`data/charters/studying/specs/lean4-charter-2026-06-10/` as an
`owner-living-program` (neutral-steward ownership; § 3 carves the uscode +
market-tape domains out to `proving/textual-axis` + `accounting/numerical-axis`).

## 1. Purpose

Axiomatizes the *operational* domain — what happens daily in qagents, git
first. Consumer: `monitoring/` (local-only); debate pairing: coding v. testing
(`/dao`, P2). Pure-mathlib paths (Topology, MeasureTheory, Analysis,
CategoryTheory) are out of scope.

## 2. Workstream A — representation research (cross-axis)

How to effectively *represent* all three Lean4 workflows — kernel shape,
facts-generation contract, debate protocol, verification gate — drawing from
the standard examples in `hub/theorem_proving_in_lean4` and
`hub/reference-manual`. Deliverables (spec § 5.1, P1):

- `studying/representation.md` — maps each standard TPiL4 / reference-manual
  idiom to its qagents kernel counterpart, three axes as parallel columns.
  The document LLM proof-drivers are pointed at; replaces folklore. Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/representation-guide-2026-06-10/SPEC.md`.
- `studying/thesis.md` — the **canonical public-distillation source** (seven-step
  cross-axis method synthesis + hero-node label contract); public-facing sibling of
  internal `representation.md`. Rendered out by `publishing/` → quantapix.com
  `/thesis` + the `qgraph-wire/1` hero; never copied out by `studying/`. The three
  public pages (`/thesis`+`/qnarre`+`/qresev`) are governed as one messaging surface
  (spec § 10; `pleading/` binding). Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/quantapix-thesis-2026-06-22/SPEC.md`.
- Code-generation templates the debate lanes consume (`mem_*_cases`-style
  helpers, axiom-list witness patterns, `Facts.lean` skeletons), extracted
  with `hub/vscode-lean4` as **template source only** — never installed as
  an interactive proof surface (spec § 4.2; no manual proof driving, ever).
- **Hierarchical-predicate object classes** — the cross-axis vocabulary all
  three axes use is `representation.md` Ch. 13, owned by
  `data/charters/proving/specs/axiomatize-uscode-2026-05-29/hierarchical-predicates-2026-06-20/SPEC.md`
  (tactic layer is kernel-side Lean, never a plugin — charter § 4 pin R2.5).
- **Hierarchical predicates H0/H1 — applied to the operational axis** (sibling
  parity with proving/accounting). H0 = the Mathlib-free tactic substrate in the
  shared `Common/` namespace (path deliberately unnamed — C5-graded roster; find
  it by behaviour); H1 = the `Operating/Qagents/Hier/`
  cell decomposing `OpenedAs` (the axis's single LLM-judged predicate) with a
  term-only `Bridge.lean` oracle guard, shrinking the lone model call to the
  narrow `has-session-footer` leaf. Specs `predicates/operating/hier/`;
  K-graph probe `op.Qagents.opened_as_hier`.

- **Proof-carrying context injection — Phases A+B+C SHIPPED (C 2026-07-16: the
  fork-isolated `kernel-recall` pull skill, `studying/skills/kernel-recall/`).** Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/proof-context-injection-2026-07-09/SPEC.md`
  + ADOPT-AMEND debate record `proof-context-injection-2026-07-09` (data/debates/, HELD lane) (PRIVACY
  9-cond + NO-MANUAL-PROVING 4-cond). The machinery roster is the SPEC's — don't
  mirror it here; it is mid-migration to a `qx` shim (`ns:studying/39`). Two
  invariants bite: the live-check **state-key is a digest of the extractor INPUT
  SNAPSHOT — refs + worktree table + sentinel stats, never HEAD** (R2); and the
  surface is a **machine-context seam** — templates-class extension,
  non-precedential across axes, `monitoring/` stays the sole consumer app (R15).
  Ledger privacy: § 5.1.2(c) path-blocklist carries (committed-but-never-published
  — the `studying_entailment_ledger` Stage-4 rule in
  `publishing/scripts/sync_mirror.py`).

## 3. Workstream B — operational axiomatization (git first)

Map git (`hub/git` as ground truth) into Lean4 axioms, structured like
`proving/Proving/<Framework>/` and `accounting/Accounting/<Framework>/`,
closely following the template of `hub/cslib`. Lake package:
`studying/Operating/`, module root `Operating/` — module-relative paths below,
with the `Operating/{Git,Qagents}/` quartets (executing
subspec `data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-git-2026-06-10/SPEC.md`;
content emit co-located at `Operating/emits/`). The qagents angle is the point:
first theorems target *our* operational invariants —
branch-presence-as-write-lock exclusion, `/close` cascade safety,
canonical-vs-worktree divergence — with git's semantics as the axiom layer
beneath them. Proofs are driven by the coding-v.-testing `/dao` debate lane
(manual-interactive first: `/dao-manual`), never manually.

**HARD RULE — adversarial independence is the ONLY oracle; protect ALL FIVE channels
(2026-07-14; C5 added 2026-07-27).** A parried attack is evidence *only* if the attacker
did not know the proof and the proof was not pre-hardened against the attack list. Five
leak channels — C1 scratchpad, C2 orchestrator, C3 read-property, C4 memsearch, C5
shared canonical vocabulary — closing one buys nothing (spec-of-record:
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/SPEC.md` § 4a).
**The full firewall doctrine is `studying/dao-blindness.md`** — channel anatomy, the
brief channel (b′), the r07 lesson (a positive-scope contract graded by a
negative-list instrument), the `mandate_conflict.py` wiring and the cures.
ORCHESTRATOR-facing: read it before authoring any `/dao` round brief or running
`--blindness-audit`; neither that doc nor any path it names may appear in a blind
cell's brief.


**Evidence archive + gate/instrument doctrine → `studying/gates.md`**
(ORCHESTRATOR-facing; never cite it in a blind cell's brief — its non-naming
rule travels with the text). Read § Evidence archive before freezing or
verifying a round's evidence or diagnosing an archive-loss alarm (the
`studying/waves/` archive, `archive_integrity.py`, the host-prefix coordinate
rule); read § Gates before running `spec_battery.sh`, landing a chartered
artifact, or authoring an allow-list fixture (G7-KERNEL whole-tree axiom
closure, fixture-integrity sweep, shape-gate discipline, the existence-checked
closure-wrapper rule).

**Family completion records → `studying/families.md`** — the full per-family
blocks (status, consequences, live rules, CTX negative-result custody); read a
family's block there before resuming or extending it. Compact roster
(`…` = `data/charters/studying/specs/lean4-charter-2026-06-10`, as elsewhere here):

| family | status | spec |
|---|---|---|
| git v2 index/staging | T4a/T4b proved | `data/specs/index-staging-v2-2026-06-19/` |
| axiomatize-posix | Phases 0–4 SHIPPED; family CLOSED (Phase 5 deferred by design) | `…/axiomatize-posix-2026-07-08/SPEC.md` |
| axiomatize-llm-ops | COMPLETE on ranked set; S-T8/S-T9 hook gating proved (spec § 11) | `…/axiomatize-llm-ops-2026-06-18/SPEC.md` |
| git↔session bridge | complete (spec § 10); `DcuBridge` extends cross-session | `data/debates/git-session-bridge{,-sharpening}-2026-06-21.md` |
| `/lift` pre-condition model | model landed (`LiftSafety.lean`); coverage promotion deferred | `data/specs/open-close-dcu-2026-05-26/lift-cross-agent-2026-06-24/` |
| signoff S-T10 | proved; framework P3 alone remains | `…/signoff-verification-2026-06-30/SPEC.md` |
| constellation graph M | observation graph, privacy:local-only | `…/constellation-graph-2026-06-17/SPEC.md` § 5 |
| Pending + WtLinks safety invariants | both GREEN on the numerator | `Operating/Session/{Pending,WtLinks}.lean` |
| state review 2026-07-03 | discharged; two standing rules (see families.md) | `studying/reviews/state-review-2026-07-03.md` |
| dao-scheduling | the standing run plan (P0–P7) | `…/dao-scheduling-2026-07-10/SPEC.md` + `PROMPTS.md` |
| axiomatize-ledger | COMPLETE on ranked set; R-T6 event-gated | `…/axiomatize-ledger-2026-07-10/SPEC.md` |
| axiomatize-context-ops | CTX-T1..T4 CLOSED; per-round state `ns:studying/60` | `…/axiomatize-context-ops-2026-07-22/SPEC.md` |
| structural-guards | FAMILY-ADOPTED 2026-08-12 (steward act; rung ladder + matrix § 2c grid + § 4 admissibility law); P2 live at `ns:studying/121`; § 5 kernel layer BOUND (SK-1 subspec) | `…/structural-guards-2026-08-12/SPEC.md` |

**G1 axiom floor — RULED + SHIPPED 2026-08-03 (per-cell declared opt-in; witness
`t_18`).** Three classes, previously one grep alternation that called them all
unsoundness: `sorryAx` (unsoundness) and `Lean.ofReduce{Bool,Nat}`/`Lean.trustCompiler`
(trust-base extension) are never declarable; **`Classical.choice`/`Quot.sound` are two
of Lean's three standard axioms, are NOT unsound, and are refused only until the
example declares `manifest.axiomFloor.allowClassical`.** The old form banned one
standard axiom, silently permitted the other, and announced the ban with a false
claim. Classification lives in `_classify_axiom_closure` behind a `DAO_SOURCE_ONLY`
source guard so `t_18` drives the REAL function, not a copy. Two escapes closed with
it, both INHERITED (the old alternation missed them equally): **`native_decide` mints
a FRESH PER-DECLARATION axiom (`<thm>._native.native_decide.ax_1_1`), so the match
must be a SHAPE rule — no literal roster can ever name it** — and `Lean.ofReduceNat`
was simply unlisted. **The G1 probe's REACH defect is CURED 2026-08-12
(`ns:studying/120` retired): `_g1_probe_lean` enumerates by the environment's MODULE
TAG — every constant the example's modules contribute, internal included, two
populations reported per run — replacing the column-0 grep that reached 143 of
ctx_degrade's constants. Witness `t_30`; false-refusal 0/35 over the live roster
(matrix § 2b record, which also pins the trap that voids a careless measurement:
`lake env lean` reads stale oleans silently, so any G1 measurement without a
preceding `lake build` is VOID).** FOUR escape forms are witnessed in that one example, and the
first two are one class — a declaration form that mints no environment entry, or mints a
constant the source never NAMES, discharges obligations where no closure audit can look:
(1) an ANONYMOUS `example` (r08, `6f63e7e62`) contributes NO constant, so it is
unreachable by the grep, by `#print axioms`, by the allow-list roster arm and by G7
alike; (2) a `structure` mints `Snapshot.mk.injEq`, absent from the file's text and
carrying `propext` ALONE (r09); (3) a Prop-valued `def` is outside the keyword roster —
formerly "reported not reproduced", now reproduced with live members (r10–r11); (4) a
`private` declaration mangles to `_private.<module>.0.<ns>.<name>` and fails BOTH
conjuncts of every prefix-anchored filter, with five live constants of the module
rejected today (r11). **So "enumerate by the ENVIRONMENT" is necessary and NOT
sufficient — the FILTER is the other half of the instrument, and form (4) defeats an
environment instrument while (1)–(3) defeat source ones.** Consequence measured at r08
and still the sharpest statement of why: the example's classical footprint was **10, not
the 8 its prose enumerated**, because a footprint counted over NAMED declarations is
blind BY CONSTRUCTION to an anonymous `example` carrying the same dependence — the gap
and the mismeasurement had ONE cause, so finding either finds both. When extending the
probe, derive BOTH the population and the filter from the module, and state the
population a claim is quantified over whenever the two differ (`ns:studying/50`
sharpening 6). The formerly-uncomfortable interim state — full coverage existing only
in the adversary's `attack/r10_module_axiom_floor_sweep.lean`, consumed by no gate —
ended with the 2026-08-12 rebuild: the judge's own probe now carries an equivalent
module-tag enumeration; the attack sweep stays as the adversarial twin.

**The instruction layer is a channel too — this file once MANDATED a C5 breach
(blocking `ctx_degrade` r05–r07; seq 196), restated behaviourally 2026-08-05.** A
brief-side cure cannot reach a conflict authored in the INSTRUCTIONS: r06 removed
every brief-side cause and the channel stayed open. `mandate_conflict.py` now reports
no conflict over this file + both cell contracts — re-run it after editing either.
The C5 rung was RULED 2026-08-08 (see § Allow-list fixtures below) and the
`--blindness-audit` round scoping landed (witness `t_20`); the step order was CURED
2026-08-06 (Step 7c reorder), and **the fold's breach-refusal is now MECHANICAL —
`--standing` exit 69, plus the `--round-close` verb chaining 7b→7c→7d→9 (R1,
2026-08-08; witness `t_24`).** Per-round state stays `ns:studying/60`.


## 4. Guide-rails — `hub/` governance

`studying/guide-rails.md` is the committed manifest over the five Lean4
guide-rail clones in root-level `hub/` (root CLAUDE.md § Shared-code hubs owns
the hub's read-only + gitignored posture). Refresh is manual from an
`/open studying` session via `studying/scripts/hub_refresh.sh` (`--check` = the
charter's P0 test; read the docs-vs-pin skew note at each refresh). Adding a
row is a manifest + script + spec amendment. lean4 source citations use
upstream GitHub URLs (side-clone convention retired, charter D3).

## 5. Toolchain — three-way lockstep

`studying/lean-toolchain` is pinned in lockstep with `proving/lean-toolchain` +
`accounting/lean-toolchain` (the pin value is the file itself + the `guide-rails.md`
skew note — not restated here). Any bump moves all three and replays each kernel's
example proofs (`feedback_lean_toolchain_bump_verify_example_proofs`). **Studying
carries TWO pins**, not one: `studying/lean-toolchain` *and*
`studying/Operating/lean-toolchain` (the Operating package is the actual kernel) —
both move together or `elan` resolves differently depending on cwd. **"One commit"
is not always achievable — record the deviation:** when each axis is held by its
own open session the bump lands one commit per branch, in lockstep in time, each
independently verified. Say so; never let the three drift across a day.

**The pin is CWD-DEPENDENT (2026-07-14).** `elan` reads `lean-toolchain` from the
*current directory*, so a bare `lean` run anywhere without a pin file (a sandbox probe
dir, `/tmp`) silently falls back to elan's **default** toolchain — it voided real
textual-axis work (anatomy: `reference_lean_isolation_probe_full_path_imports`).
Always `lake env` from the package root, or `elan run leanprover/lean4:<pin> lean`. A
file-in-the-root is not a pin for any process whose cwd is elsewhere.

## 6. Source authority

`studying/focus-areas.md` is the **single source** for the ranked focus
areas, their difficulty ratings, reading order, active threads to track, and
the skip list — each area tagged to Workstream A or B. Don't fork the
syllabus into multiple files; edit the same file — the commit log is the
change record.

**Dated narratives are ARMED ephemeral lanes (since 2026-08-06).** `AUDIT-*.md` and
`weekly/*.md` are `ephemeral` (ttl in `data/specs/do-retire-2026-07-26/lanes.tsv`,
the single source of truth — never a remembered figure). A new audit narrative lives
about a week on disk: freeze the verdict into its rounds file or a CLAUDE.md standing
section, and promote sole-copy evidence via `scripts/retire-evidence-promote.sh`,
**before** anything relies on it. Git + `archive.blob` are the retention; the file is
not.

## 7. Public-facing derivation

The public `qstudying-public` README is rendered from `focus-areas.md` (§ 6) by
`publishing/` during `/publish` (redaction + voice guardrails; drive Promise 1;
spec `data/specs/publishing-2026-05-31/`) — `studying/` never renders or copies
it out. See `feedback_public_facing_source_render_split.md`.

## 8. Scope boundary

No imports from `analyzing/`, `trading/`, or any other code-bearing
subproject; no cross-kernel imports (`proving/`/`accounting/`) and no
importing the consumer (`monitoring/`) — the seam is files, never code. The
only outbound dependency is *content*: focus-area summaries via
`publishing/`, the emitted workflow JSON `monitoring/` mounts (day-one per
the round-1 ruling, debate record `representation-guide-2026-06-10` — data/debates/, HELD lane), and
the code-generation templates at `studying/templates/` the debate lanes
read at prompt-assembly time (never imported or built).

## Status emit (`data/status/studying.json`)

`studying/scripts/status_emit.mjs` participates in the qagents-wide Status page
contract. The pill computes the charter P2 gate from the tree (spec § 5.3) and
honestly degrades to `NOT_YET_LIVE` if a checkout lacks the example artifacts.
The slot carries the real toolchain pin (read from `studying/lean-toolchain`),
focus-area count, and lane metrics. Schema `@qagents/diagram-kit`; contract
`qagents/CLAUDE.md` § "Status hub". Counting-bases NOTE: Σ `standing.json`
`holds` (all standing files,
posix_* substrate + signoff included) and the emit's `theoremsProved` (column-0
`theorem`/`lemma` declarations in the `EXAMPLES`-roster proof.lean files,
gated on fully-adjudicated) are BOTH correct on different bases — neither is
ever corrected to the other (do-share 2026-07-15 reconciliation). Read the
current values from the tree/emit, not from here.

**ROUND COUNT — the same two-bases shape, RULED for public use (2026-08-08,
`ns:studying/97`(d)).** Two denominators for "how many `/dao` rounds": every
`rounds/<NN>.json` on disk, and the emit's `daoRounds`, which counts only
`EXAMPLES`-roster entries that are `met` (fully adjudicated). **Any PUBLIC
statement uses `daoRounds`** — a public count must be gated on adjudication, as
the blind-cert pill is; this axis withdrew a public claim 2026-07-14 over an
unearned figure. The disk count is internal and never published; read both
from a run.
