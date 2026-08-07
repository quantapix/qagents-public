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

`studying/` is the **third Lean4 axis** (root § "Lean4 axes" owns the shared
architecture): it axiomatizes the *operational* domain — what happens daily in
qagents, git first. It also owns the **cross-axis representation research** and
the `hub/` guide-rails that keep all three kernels honest. Consumer:
`monitoring/` (local-only); debate pairing: coding v. testing (`/dao`, P2).
Pure-mathlib paths (Topology, MeasureTheory, Analysis, CategoryTheory) are out
of scope.

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
  + ADOPT-AMEND record `data/debates/proof-context-injection-2026-07-09.md` (PRIVACY
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
leak channels — C1 scratchpad, C2 orchestrator, C3 read-property, C4 memsearch, **C5
shared canonical vocabulary** (any enumeration of `Operating/Operating/Common/` — a cell
that has seen the roster produces echo, not evidence; graded `names`/`types` REVIEW vs
`roster` BREACH) (spec-of-record:
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/SPEC.md` § 4a) —
closing one buys nothing; (a)/(b) below detail C1/C2, the two that live in this
orchestrator's own hands.

**(c) *Mechanized, and it must run IN-SESSION.*** `dao.sh --blindness-audit <id>`
(`/dao-manual` Step 7b) runs the shared auditor `code/lean_tools/transcript_audit.py`
(GRADES C1–C5; C6 reconciler licensing, C7 contract-referenced docs) over the round's
cells, freezing the verdict at `Operating/examples/<id>/rounds/blindness-<NN>.json`;
exits 62 breach / 63 unauditable. Mechanism, retention figure, `--contract-file`,
axis-specific rooting and gate `t_11` are owned by
`…/blindness-firewall-2026-07-25/SPEC.md` — cite it, never a number here. Four
consequences bind the lane. **Retention is SHORT and NON-MONOTONE**, so an un-audited
round becomes *permanently unauditable*, not merely unchecked; the only remedy is a
full blind re-slice (P0-5(iv)), and "audit the history later" is not a plan. Any
`clean` recorded before 2026-07-27 means clean on **C1–C4 only** — read the rung, not
just the verdict. **A verdict can be about the WRONG SUBJECT, and that reads exactly
like a real one** — act on the verb's "CHECK IT NAMES THIS SESSION" print; a
wrong-subject verdict is NULL, not lenient, and `--supersede` freezes
`blindness-<NN>.corrected-<k>.json` beside the base (never rewritten) while `--book`
reads the highest corrected as authoritative. And **reading a BREACH is
discrimination, not arithmetic: read the matched text and the RUNG, never the count;
never rewrite a frozen verdict** — the known shared-instrument false-positive classes
are `ns:proving/89`/`110`/`112`, and the wrong-subject anatomy plus its cross-axis
reciprocals are `ns:studying/64`. When a contract bars a read with no sanctioned
substitute, add the narrow answer rather than relax the bar (`dao.sh
--claim-attack-name <id> <name>` → `free`/`taken`, exit 0/65, never a roster; gate
`t_13`).
(a) *Filesystem:* the runtime hands every subagent the SAME
writable session scratchpad — agent scratch goes under its own disjoint
`<out>/.scratch/`; the session scratchpad is off-limits
(`.claude/agents/dao-{coding,testing}.md` § Scratch isolation). (b) *Orchestrator:*
from round 2 the orchestrator holds both sides' results — routing one side's finding
into the other's prompt makes the next green an echo; **name the METHOD, never the
ANSWER**. **(b′) THE BRIEF CHANNEL — channel-independent, and stated that way on
purpose.** *Every blindness rule constrains what the CELL may CHOOSE; none
constrains what the BRIEF may REQUIRE* — and an instructed read arrives at the cell
as an instruction, not a violation, so it is the one breach a cell cannot
self-police. It fires on whatever channel the brief NAMES: r01 pointed at a sibling
EXAMPLE → C3 (2026-07-31, seq 173); r04 named an instrument by MODULE PATH, a
C5-roster member → BREACH rung `roster` (2026-08-02, seq 192); r05/r06 proved the
same conflict can be authored one level up, in the INSTRUCTIONS (seq 196). **Filing
r01 as a C3 anecdote is exactly why r04 recurred** — hence the general form here and
three dated instances rather than three rules. Cures: state instrument requirements
BEHAVIOURALLY ("audit closures with an existence-checked wrapper; a bare
`collectAxioms` returns an empty closure for an unknown constant" carries the whole
requirement and names nothing); convey artifact shape by inlining the pattern or
citing `studying/templates/`, never by pointing a blind cell at a sibling's committed
proof/attack artifact; **grep your own brief AND your own instructions for any repo
path before spawning, and ask which channel would grade it** — mechanically since
2026-08-04 via `code/lean_tools/mandate_conflict.py` (exit 9 blocks the spawn; a hit
is a review obligation on the author, since it cannot tell prohibition from
direction). A leaked round's Lean may be sound yet **VOID as evidence** — no tier, no
standing promotion, no coverage number (both proving lanes broke this 2026-07-14,
~3M tokens of green work discarded). Guard: `…/dao-scheduling-2026-07-10/PROMPTS.md`
§ Orchestrator blindness discipline (P1 step 5 self-check); memory
`feedback_blind_fanout_oracle_channels`.

**Evidence archive (`studying/waves/` — the dao archive half, 2026-07-31,
ns:qagents/107 co-land).** Blindness-audit evidence freezes to the gitignored,
LAN/S3-backed `studying/waves/<example-id>-r<NN>/` via `dao.sh --blindness-audit`
→ `transcript_audit.py --archive-evidence` (raw `agent-*.jsonl` + `manifest.json`;
replay via `--regrade <manifest>`), in the SAME freeze-first step as the round
verdict; gate `t_11` carries the evidence arm. **Nothing evidence-shaped is ever
committed** — a committed
evidence file is a C5 answer-roster, and any proposal to commit evidence
re-opens the PRIVACY gate (`data/debates/transcript-retention-2026-07-30.md`
R1/R8). **An archive is EVIDENCE ONLY once something checks it is there — seven
frozen verdicts turned out to have none (2026-08-06, `ns:studying/77`).** Every
lane read `rounds/*.json` and none ever looked underneath, so the evidence was
unguarded by construction, and the only guard was a rule a human had to recall at
citation time — which three committed item bodies then broke, in both directions
([[feedback_a_remembered_rule_is_not_a_guard]]). `scripts/archive_integrity.py`
now runs inside `dao.sh --standing` (witness `t_21`): the PRESENCE arm is
declarable via `Operating/examples/evidence-losses.json` — **a declared loss WARNs
on every run, which is what keeps it visible; declaration is not absolution** —
and the SUBJECT arm (archive roster must EQUAL the verdict's agent set) is never
declarable, because a verdict computed from the wrong cells is null, not lost.
**Four of the seven were never lost at all — and the census that called them lost
is the cautionary half of this § (2026-08-06).** They sit on the **`qyel`** backup
prefix, agent sets matching their verdicts exactly: those rounds RAN on the other
workstation. The census enumerated by TREE **on one host** and reported
absence-here as gone. Real permanent losses are THREE (`ctx_recall`, pre-dating
the archiver). So **a gate has a COORDINATE SYSTEM, not a target set** —
"scope by tree" fixes membership and leaves host, instrument version and corpus
vintage silently partial ([[feedback_completeness_is_relative_to_a_coordinate_system]]);
and **mechanizing a rule fixes who remembers it, not whether the question was
scoped right.** Read a declared loss as *"absent on this host"* until a peer
prefix is checked, and never harden a loss claim without one — declarations WARN
rather than mute precisely so a wrong one stays recoverable.
**Round STRUCTURE has a validator** — `visualizing/rounds/validate_rounds.py`
(stdlib, system `python3`; exits 0/2/4/5 pass/usage/structural/join-orphan)
checks `Operating/examples/*/rounds/` against the `qrounds/1` schema pair; its
`_target_stems` is the declared diff-check sibling of
`fold_standing.py::_target_stems` (S-85) — keep them in lockstep. Wired into
the lane 2026-08-01: `dao.sh --standing`/`--report` call it before fold/report and a
red exit BLOCKS both (gate `t_14`). **`--standing` itself now runs AFTER the
blindness verdict, not before it** (`/dao-manual` Step 7c, 2026-08-06): folding
first promoted standing off a round whose oracle had not run, and **nothing that
promotes may run before the oracle that can void it** — the general form of the
already-cured `ns:studying/59` judge-books defect. Rounds stay committed append-only: the archive
holds evidence ONLY — no wave freeze, no `--archive-wave`, no `--push`. Per operator
ruling L-122 (cold-S3 non-debt) there is no tunnel ritual — the archive rides the
qred-nightly → qblk → S3 daily ship. Backup lockstep (rule owned by
`serving/CLAUDE.md` § 10): **empty `studying/waves` hard-refuses**, absent is a plain
skip — so the dir is born POPULATED by the first evidence write, never pre-created.

**git v2 — index/staging.** Spec `data/specs/index-staging-v2-2026-06-19/SPEC.md`
(extends `…/axiomatize-git-2026-06-10/SPEC.md`): the `Operating/Git/` index substrate
+ T4 promotion-discipline (the `data/tmp → data/specs` adopted-spec analogue),
T4a/T4b proved by `/dao-manual`.

**axiomatize-posix — the SUBSTRATE target beneath git (files/processes/exit-codes;
Phases 0–4 SHIPPED, family CLOSED, Phase 5 deferred by design).** `Operating/Posix/`
quartet + six `Operating/Qagents/` bridge cells, one per spec § 3 primitive, each a
safety PROPERTY with an inhabitable breach dual; `GateGreen`'s per-lane decomposition
is the second hierarchical cell → H2–H4. Scope bound and modeled-fixture posture are
the spec's (`…/axiomatize-posix-2026-07-08/SPEC.md` §§ 2/5).

**axiomatize-llm-ops — COMPLETE on its ranked invariant set** (S-T2 index bijection,
S-T3 provenance authority, S-T4 ownership totality; spec
`…/axiomatize-llm-ops-2026-06-18/SPEC.md`, Round-1 record
`data/debates/axiomatize-llm-ops-2026-06-18.md`). `Operating/Session/` is NOT a 4th
axis; the emit-privacy, off-numerator and redaction-gate rules are the spec's.

**The git↔session decomposition bridge (spec § 10, complete).** A session-lifecycle
skill is a DERIVED predicate decomposing into already-proved git operations + a
narrow residue (S-T5/S-T6/S-T7 + the `/open`/`/close`/`/lift` bridge cells, all
`Operating/Session/*Bridge.lean` + `Isolation.lean` + `DelegatedLanding.lean`); the
`/do-claude-updates` `DcuBridge` cell EXTENDS the family to a cross-session skill
(`syn_dcu` GREEN). The one rule worth carrying here: an operational-axis adopt round
MUST seat the explicit qagents conditioning axioms as a first-class input — **raw git
is the substrate, never the ceiling** — and the § 10.8 register that holds them grows
leaf-by-leaf at the consuming skill (anti-vacuity). Records
`data/debates/git-session-bridge{,-sharpening}-2026-06-21.md`.

**`/lift` pre-condition model — studying OWNS + authors the entire lift spec**
(`/open qagents` does the `lift.sh`/`close.sh` implementation + bash testing). A
donor-side-only eligibility model is inadequate for a two-party cross-session
protocol; the amendment is
`data/specs/open-close-dcu-2026-05-26/lift-cross-agent-2026-06-24/SPEC.md` (R1–R3).
Axiomatic model `Operating/Session/LiftSafety.lean` — `LiftSafe` REFINES
`LiftBridge.LiftSkill`; metric-neutral. Promoting it to a coverage-bearing S-T6
`/lift` example is the deferred proving step.

**Action-gating hooks — S-T8 + S-T9 (proved).** `Operating/Session/HookGate.lean`
models the ACTION stream (outbound tool calls) + the `PreToolUse` hooks that gate
them, the dual of § 2d's context stream. Load-bearing: **a project-scope hook does
NOT fire on a spawned subagent's call** (user-scope settings only). Spec § 11 of
`axiomatize-llm-ops-2026-06-18`.

**Provable signoff verification — S-T10 `SignoffCoverage` (governance dual of S-T8).**
Kernel cell `Operating/Qagents/Signoff.lean` (governance primitives, NOT `Session/`);
studying owns the verification amendment `…/signoff-verification-2026-06-30/SPEC.md`
under the cross-cutting signoff framework
(`data/specs/signoff-framework-2026-06-30/SPEC.md`), which owns the coverage basis,
the observation posture, the phase ledger (P3 alone remains) and CLEAR-3's P2f
discharge-typing (`face_class_confusion_uncleared`, gate `t_07`); redaction gate
`scripts/check_signoff_redactions.py`; live-leg status at `ns:studying/88`
(`ns:studying/25` retired — a stale pointer here is what a dangling `(frontier: …)`
looks like one surface over). The one
rule that must be read here because it binds every gate on every axis: a gate's
**mechanical** scanners prove rider presence / byte-equality / clause absence but
CANNOT prove the judged bindings (e.g. FINANCIALLY CLEAR-5: verdict-token ↔
run-emit), so a green `--rider-floor` / `scan_financial.sh` is necessary, never
sufficient (3.6 was mechanically green, substantively refused, 2026-07-10) — R1/R15
in operational terms.

**Constellation graph M.** A second instance-level graph: the whole monorepo + the
separate `~/.claude` memory repo as one non-hierarchical networkx `MultiDiGraph` —
the partitioning exercise the uscode tree and tiny K-graph cannot give
(`scripts/extract_constellation.py` + the `graph-extract-constellation` skill +
synthetic golden). It is an **observation** graph and `privacy:local-only` (R9); the
numerator, `lake build` and emit-gitignore rules are spec-owned
(`…/constellation-graph-2026-06-17/SPEC.md` § 5).

**Operational safety invariants — pending-promotion + worktree-links
(2026-07-07).** Two standalone PROPERTIES proved by the `/dao` lane (NOT skill
bridges — no flat golden), both GREEN, on the coverage numerator, breach duals
inhabitable: `Operating/Session/Pending.lean` `PromotionTotality` (cron-lane
`pending/` → canonical CLOSED-SET allow-list classifier + the
`unclassified_not_promoted` default-skip — no unregistered path reaches
canonical; `syn_pending`, pending-promotion-scope-2026-05-28); and
`Operating/Session/WtLinks.lean` `WorktreeLinkSafe` (a declared
`.worktree-links` glob is symlink-safe IFF its canonical target is
pure-gitignored — zero tracked files; `syn_wtlinks`, session-lifecycle
charter § 2.4).

**Full-project state review 2026-07-03 — mostly discharged.** Record + residue:
`studying/reviews/state-review-2026-07-03.md`, the 6-counsel debate
`data/debates/studying-state-review-2026-07-03.md`, `ns:studying/30`. Two rules
outlive them. (1) Coverage maps from CONSTRUCTIVE proved-target moves ONLY, never
appear-only — the P2-5 provenance guard LOUDLY refuses an uncertified-basis cell's
Tier-A down to B rather than inflate; the local-only `emit_catalog.py` basis (R13
`open_ct`) and the public pill's conservative 20/22 hold-out are two blessed bases,
never corrected to each other. (2) **The hold-out is a RULING (operator 2026-07-22,
L-118): the blind-cert badge gates on CUMULATIVE `standing.adversarial === 0`, so a
historically landed attack disqualifies a cell permanently and the public figure
stays 20/22.** The latest-round-scoped 22/22 was REJECTED, not deferred; reversing it
needs a fresh operator ruling, never a gate edit (recorded at the gate site in
`status_emit.mjs`).

**dao-scheduling program (2026-07-10) — the standing run plan.**
`data/charters/studying/specs/lean4-charter-2026-06-10/dao-scheduling-2026-07-10/SPEC.md`
+ `PROMPTS.md` (P0–P7) adopt proving's Phase-4M scheduling discipline, target-scoped
for `/dao` rounds: § 3 frontier ranks the backlog, § 12.1 is the calendar. Consult
it; don't mirror it here — and read coverage + pill numbers from
`Operating/emits/lean_graph/coverage.json` + the status emit, never from prose.
**axiomatize-ledger — COMPLETE on its ranked set** (R1–R4 shipped 2026-07-10/11;
R-T6 DEFERRED event-gated). Subspec `…/axiomatize-ledger-2026-07-10/SPEC.md`
(t_01–t_03 3/3): the shared-ledger-store RDB semantics
(`data/specs/shared-ledger-store-2026-07-09/SPEC.md`) as an `Operating/Rdb/`
substrate quartet + five `Qagents/Ledger{Append,Replay,Spool,Render,Adopt}.lean`
bridge cells, all GREEN with inhabitable breach duals; fixture posture, privacy and
numerator rules are the subspec's §§ 5/7, and the five `op.Rdb.*` probes +
`ledger-concepts` cite parser live in `code/lean_graph`.

**axiomatize-context-ops — Leg B + W1 SHIPPED 2026-07-22; W2 COMPLETE 2026-07-31
(frontier row 11). The CTX-T1..T4 bridge-cell set is CLOSED.** Spec
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-context-ops-2026-07-22/SPEC.md`
+ record `data/debates/axiomatize-context-ops-2026-07-22.md`; PCI § 7 item 6 is the
folded Leg A. The § 4 table (the four `Operating/Qagents/Ctx*.lean` cells, their
claims + breach duals, the no-new-substrate rule) and § 9.2 (the nine W1 attacks
K1–K9 against the orchestrator-authored kernel, repaired same-round — read it before
touching `ctx_verdict`/`ctx_shorten`) are the record; live per-round state and what
r07 owes are `ns:studying/60`. Don't mirror either here.
**CTX-T3 `ctx_recall` is closed on a NEGATIVE RESULT and must not be re-opened as a
repair round** — the normative record and the two conditions binding any re-seat live
in the NEGATIVE RESULT section of `Operating/Operating/Qagents/CtxRecall.lean`; read
it there, never restate it from memory. Committed witnesses are the evidence and are
never deleted to make the cell look clean.
**CTX-T4 `ctx_degrade`** (`Qagents/CtxDegrade.lean` DegradedHonesty; duals grounded in
the memsearch `reset` finding): **only r03 is evidence rather than echo**, and the
per-round bookkeeping is `ns:studying/60`'s — read it there. Three consequences
outlive the rounds and generalize past this family.
**K1 (the kill) — every conditioning axiom carries an ESCAPE PREDICATE:** an
unconditioned seat whose conclusion is the NEGATION of a breach dual makes that dual
UNINHABITABLE — the kernel refutes its own breach and the detection lifter proves
anything; never state a seat whose domain is the dual's domain. **A GAP-PROBE INVERTS
THE JUDGE'S POLARITY, and it will recur:** an `EXPECTED-DIAGNOSTIC` asserts an
ABSENCE, so closing the gap makes the probe elaborate green and the attack lane reads
green-on-annotated as `LANDED` — the round that FIXES a named gap reds itself. There
is no DISCHARGED verdict; retire the probe into a standing discharge record (drop the
directive, keep the measurement — the anchored `^-- EXPECTED-DIAGNOSTIC:` matcher
lets the note still MENTION it in prose). And **the modeled fixture OVER-EMITS**, so
a green § D is not evidence the declaration discipline works and every seat here is
DROPPABLE.
Tier stays modeled Tier-B family-wide and **no blind-cert is claimed anywhere in it**,
though not for a uniform reason: `ctx_verdict`/`ctx_shorten` carry an adverse
read-side record, while `ctx_degrade` r03 is CLEAN and is held at B by its open
attacks plus the P2-5 provenance refusal.
Live rules: the R3 emit/derive law (negative closures are EMITTED facts or the dual is
disarmed — W6/CLEAR-3f); modeled Tier-B unless per-cell blind-certified; committed
GREEN duals are per-wave deliverables; AXES custody — new catalog axis tokens route to
visualizing BEFORE the wave, cells stay off-emit until landed (H-3/H-4); `--ctx-check`
does NOT enforce the Leg-B miner-content bar (authoring discipline). **Leg B** =
`scripts/ctx_miner.py` (frozen pattern set, no LLM) + gate `t_02_miner_floors`, report
local-only under the § 5 C-1..C-5 floors; its first run inverted the graduation
question — adding rows beats graduating rows 2–6 (spec § 9.1).

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
was simply unlisted. Still open, reported not reproduced: the G1 probe is built from a
column-0 `^(theorem|lemma)` grep, so a Prop-valued `def` is outside its reach.

**The instruction layer is a channel too — this file once MANDATED a C5 breach
(blocking `ctx_degrade` r05–r07; seq 196), restated behaviourally 2026-08-05.** A
brief-side cure cannot reach a conflict authored in the INSTRUCTIONS: r06 removed
every brief-side cause and the channel stayed open. `mandate_conflict.py` now reports
no conflict over this file + both cell contracts — re-run it after editing either.
The still-unruled C5 rung (is reading ONE named kernel module `roster`-grade at all
when `dao-testing.md` says the kernel is FAIR GAME?) and the landed
`--blindness-audit` round scoping (witness `t_20`) are live at `ns:studying/60`;
the `--standing`-upstream-of-the-audit step order was CURED 2026-08-06 (Step 7c
reorder — § Evidence archive above), though the fold's breach-refusal stays
prose-only until the routine-review R1 `--round-close` verb lands
(`studying/reviews/routine-review-2026-08-06.md` § 3.2).

**G7-KERNEL — the whole-tree axiom-closure arm (2026-08-05; witness `t_19`; ledger
seq 205/206).** **A soundness gate scoped by ROSTER audits exactly what someone
remembered to add, so what it misses is selected for by the same forgetting**
([[feedback_roster_scoped_gate_misses_what_nobody_added]]). Both arms here were
roster-scoped, and since `sorry` is a WARNING at rc 0 a `sorryAx` in an unlisted
kernel cell left `--judge` GREEN on every arm — reproduced by injection before
fixing. `--judge` now sweeps the whole kernel TREE; a non-0/2 attest exit is RED,
never skipped, for the same shape-rule reason `native_decide` forced one. Two shared
`attest_axioms.py` defects fixed with it are cross-axis (comment-stripping, so prose
can't mint ghost targets; and `--scan-dir`'s silent drop of files not `relative_to`
the `--root`, now a loud refusal) — the proving fallout is `ns:proving/115`. **A
silently smaller attested set is the one failure mode a soundness gate cannot have.**

**Fixture integrity has its own sweep, separate from `--judge`
(`scripts/fixture_integrity_sweep.sh`, 2026-08-02).** `--judge` is PER-EXAMPLE, so a
CLOSED example is never judged and its fixtures are unguarded by construction — that
is how six `ctx_recall` attack files sat non-elaborating for days with every gate
green (`ns:studying/70`). The sweep answers only "does the fixture build", leaves
adjudication to `--judge`, separates `EXPECTED-DIAGNOSTIC` parries from real
breakage, and reads breakage from the EXIT CODE — never by grepping output for the
word "error", which misreads any fixture whose own report text contains it. Exit 3 on
any break; read counts from a run, not from here. Its harness guard counts VERDICTS,
not output lines, because **a sweep that reports success over a set it never checked
is the same vacuity class the sweep exists to catch.** It RUNS from
`spec_battery.sh` since 2026-08-06 — shipping an instrument does not run it, and an
unrun sweep is the gap re-made. Whole-TREE and deliberately not in the dao lane:
per-round scoping is the defect it answers. A missing sweep exits 2 there —
**absence is not a pass.** The battery also seats the hermetic
`QAGENTS_LEDGER_DSN=NONE` sentinel, as does every family `run.sh` (a suite invoked
directly bypasses the aggregator), each with an armed-choke-point assertion;
witness `t_04_ambient_dsn_seat` enumerates by the battery's OWN glob, which is how
it caught a ninth suite the seating pass had missed.

**Shape-gate discipline (load-bearing — the ns-34/ns-38 silent-red class).**
Each spec-family suite (`data/charters/studying/specs/**/tests/run.sh`) is
exercised only when its OWN `run.sh` is invoked, so a gate goes **silently
red** when a chartered artifact (cell / template / schema) lands without
updating that gate's expected-set. Two obligations: (1) landing any chartered
artifact MUST update its shape-gate's expected-set **in the same change**;
(2) run the loud aggregating battery `studying/scripts/spec_battery.sh` (globs
every family `tests/run.sh`, exits non-zero on any red, dumps the failing
suite's output) before `/close` — never trust that the one family you touched
is the only one that drifted. A NEW family with a `tests/run.sh` is auto-discovered by the glob. Adjacent trap: a
gate whose accumulator is only asserted in a wrapper `main()` is green-but-dead
([[feedback_pytest_ck_accumulator_laundered_pass]]).
**Both `spec_battery.sh` and `dao.sh` prepend elan to PATH for CHILD processes**
(2026-08-01): an absolute `$LAKE` covers a script's own calls, but the G7 attest
helper and the `t_05` build gate run `lake` BY NAME through subprocess, so a caller
whose shell lacks elan got a FALSE RED wearing the face of a kernel regression.

**Allow-list fixtures MUST collect closures through an EXISTENCE-CHECKED
wrapper, never bare `Lean.collectAxioms`** — bare `collectAxioms` returns an EMPTY
closure for a constant that does not exist, so the universal fixture shape skips
every guard on an unknown pin and reports success (L-135; 102 sites swept
2026-08-01). The sanctioned wrapper checks existence at the point of collection and
is monad-polymorphic (some fixtures are `run_cmd`/`CommandElabM`, not `CoreM`
`#eval`); it lives in the shared `Common/` namespace — **find it by that behaviour.
This file deliberately no longer names its module and a brief must not either**
(§ 3 (b′): naming it here is what made every allow-list round breach by
construction, seq 196; the rung itself is still unruled — `ns:studying/60`). One
bare call is deliberately retained as a control probe asserting the empty-on-unknown
behaviour still holds; do not "fix" it. **A null result from such a sweep means
nothing until per-site reachability is proved** — make the wrapper throw
unconditionally, revert every other site, and confirm each one reds.

## 4. Guide-rails — `hub/` governance

`studying/guide-rails.md` is the committed manifest over the five Lean4
guide-rail clones in the root-level `hub/` (read-only upstream clones,
gitignored wholesale, canonical-only at `<root>/hub/`).
Refresh is manual from `/open studying` sessions via
`studying/scripts/hub_refresh.sh` (`--check` = the charter's P0 test; check
the docs-vs-pin skew note in the manifest at each refresh). Adding a row is
a manifest + script + spec amendment. The former lean4 side-clone
convention is retired (charter D3) — lean4 source citations use upstream
GitHub URLs.

## 5. Toolchain — three-way lockstep

`studying/lean-toolchain` is pinned in lockstep with `proving/lean-toolchain` +
`accounting/lean-toolchain` (the pin value is the file itself + the `guide-rails.md`
skew note — not restated here). Any bump moves all three and replays each kernel's
example proofs (`feedback_lean_toolchain_bump_verify_example_proofs`). **Studying
carries TWO pins**, not one: `studying/lean-toolchain` *and*
`studying/Operating/lean-toolchain` (the Operating package is the actual kernel) —
both move together or `elan` resolves differently depending on cwd. **"One commit" is
not always achievable — record the deviation when it isn't:** when the three
subprojects are each held by their own open session, the bump lands as one commit per
branch, in lockstep in time, each independently verified. Verify each axis separately
and say so; do not let the three drift across a day.

**The pin is CWD-DEPENDENT (2026-07-14).** `elan` reads `lean-toolchain` from the
*current directory*, so a bare `lean` invoked from anywhere without a pin file (a
sandbox probe dir, `/tmp`) silently falls back to elan's **default** toolchain. It
voided real textual-axis work (anatomy: memory
`reference_lean_isolation_probe_full_path_imports`). Always `lake env` from the
package root, or
`elan run leanprover/lean4:<pin> lean`. A file-in-the-root is not a pin for any process
whose cwd is elsewhere.

## 6. Source authority

`studying/focus-areas.md` is the **single source** for the ranked focus
areas, their difficulty ratings, reading order, active threads to track, and
the skip list — each area tagged to Workstream A or B. Don't fork the
syllabus into multiple files; edit the same file — the commit log is the
change record.

## 7. Public-facing derivation

`focus-areas.md` is the **authoritative source** for the public
`qstudying-public` README, but `studying/` no longer renders or copies it
out. The public README is rendered by the `publishing/` subproject during
`/publish` (redaction + voice guardrails applied; drive Promise 1; spec
`data/specs/publishing-2026-05-31/SPEC.md`). Edit `focus-areas.md` here and
let the next `/publish` pick it up. See
`feedback_public_facing_source_render_split.md`.

## 8. Scope boundary

No imports from `analyzing/`, `trading/`, or any other code-bearing
subproject; no cross-kernel imports (`proving/`/`accounting/`) and no
importing the consumer (`monitoring/`) — the seam is files, never code. The
only outbound dependency is *content*: focus-area summaries via
`publishing/`, the emitted workflow JSON `monitoring/` mounts (day-one per
the round-1 ruling, `data/debates/representation-guide-2026-06-10.md`), and
the code-generation templates at `studying/templates/` the debate lanes
read at prompt-assembly time (never imported or built).

## Status emit (`data/status/studying.json`)

`studying/scripts/status_emit.mjs` participates in the qagents-wide Status page
contract. The pill computes the charter P2 gate from the tree (spec § 5.3) and
honestly degrades to `NOT_YET_LIVE` if a checkout lacks the example artifacts.
The slot carries the real toolchain pin (read from `studying/lean-toolchain`),
focus-area count, and lane metrics. Schema: `@qagents/diagram-kit`; contract:
`qagents/CLAUDE.md` § "Status hub". Self-contained — no sibling-subproject
imports. Counting-bases NOTE: Σ `standing.json` `holds` (all standing files,
posix_* substrate + signoff included) and the emit's `theoremsProved` (column-0
`theorem`/`lemma` declarations in the `EXAMPLES`-roster proof.lean files,
gated on fully-adjudicated) are BOTH correct on different bases — neither is
ever corrected to the other (do-share 2026-07-15 reconciliation). Read the
current values from the tree/emit, not from here.
