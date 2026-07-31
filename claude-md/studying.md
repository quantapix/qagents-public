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
  parity with proving/accounting). H0 = the Mathlib-free tactic substrate
  `Operating/Common/Tactic.lean`; H1 = the `Operating/Qagents/Hier/`
  cell decomposing `OpenedAs` (the axis's single LLM-judged predicate) with a
  term-only `Bridge.lean` oracle guard, shrinking the lone model call to the
  narrow `has-session-footer` leaf. Specs `predicates/operating/hier/`;
  K-graph probe `op.Qagents.opened_as_hier`.

- **Proof-carrying context injection — Phases A+B+C SHIPPED (C 2026-07-16: the
  fork-isolated `kernel-recall` pull skill, `studying/skills/kernel-recall/`).** Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/proof-context-injection-2026-07-09/SPEC.md`
  + ADOPT-AMEND record `data/debates/proof-context-injection-2026-07-09.md`
  (PRIVACY 9-cond + NO-MANUAL-PROVING 4-cond; predecessor
  `…/axiomatized-ops-context-memory-2026-06-27/SPEC.md` Phase 3 / PRIVACY
  re-clear untouched — condition 9). The machinery roster (`live_check.sh`, the
  three `emit_*`/`check_*` scripts, the SessionStart hook, `close.sh --ctx-check`
  exits 46/47, the `/open` async spawn) is the SPEC's — don't mirror it here; it
  is also mid-migration to a `qx` shim (`ns:studying/39`). Two invariants bite:
  the live-check **state-key is a digest of the extractor INPUT SNAPSHOT — refs
  + worktree table + sentinel stats, never HEAD** (R2); and the surface is a
  **machine-context seam** — templates-class extension, non-precedential across
  axes, `monitoring/` stays the sole consumer app (R15). Ledger privacy:
  § 5.1.2(c) path-blocklist carries (committed-but-never-published — the
  `studying_entailment_ledger` Stage-4 rule in `publishing/scripts/sync_mirror.py`).

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
(`/dao-manual` Step 7b) runs the shared five-channel auditor
`code/lean_tools/transcript_audit.py` over the round's cells and freezes the verdict at
`Operating/examples/<id>/rounds/blindness-<NN>.json`; exits 62 breach / 63 unauditable.
**Transcript retention is ~10 days AT BEST — observed as short as ~1–2 days
(2026-07-30, `studying/AUDIT-ns55-readjudication-2026-07-30.md`)**, so an un-audited
wave becomes *permanently unauditable*, not merely unchecked — the only remedy is a
full blind re-slice (P0-5(iv)), and "audit the history later" is not a plan. Any
`clean` recorded before 2026-07-27 means clean on **C1–C4 only** — C5 did not exist;
read the rung, not just the verdict. Both cell contracts ride `--contract-file`
(2026-07-30, ns-53), so an inlined-contract fallback prompt no longer saturates C2.
Gate `t_11` (two committed known-bads + a clean cell that must NOT be convicted + a
review fixture pinning that contract subtraction fires without swallowing a
non-contract leak). *Rooting is axis-specific:* dao roots the audit at `examples/`, not
`examples/<id>`, because dao's two sides share one example dir with disjoint FILE
surfaces — a sibling axis must re-derive its own rooting rather than paste dao's.
**Reading a BREACH (first wave-time runs, 2026-07-29):** the verdict is mechanical, the
discrimination is yours. Both `ctx_recall` rounds scored BREACH on C3 hits that are the
KNOWN shared-instrument false positives — the root-sweep rule scores cwd and cannot see
a scoped target or a pathspec, plus a `//` normalisation artefact — owned by
`ns:proving/89`. Read the matched text and the rung, never the count; never rewrite a
frozen verdict. ONE hit was genuine — the testing contract barred `git status` while
giving a cell no sanctioned way to check an attack-filename collision against
prior-round files it may not read. CURED 2026-07-30 (ns-54): `dao.sh
--claim-attack-name <id> <name>` answers existence of ONE name (`free`/`taken`,
exit 0/65, never a roster; gate `t_13`), and the testing contract points at it — the
audit stays noisy on OTHER shapes until `ns:proving/89` F3 lands, never on this one. (a) *Filesystem:* the runtime hands every subagent the SAME
writable session scratchpad — agent scratch goes under its own disjoint
`<out>/.scratch/`; the session scratchpad is off-limits
(`.claude/agents/dao-{coding,testing}.md` § Scratch isolation). (b) *Orchestrator:*
from round 2 the orchestrator holds both sides' results — routing one side's finding
into the other's prompt makes the next green an echo; **name the METHOD, never the
ANSWER**. **(b′) The brief can author a C3 breach the cell cannot self-police
(2026-07-31, `ctx_degrade` r01; ledger seq 173).** Every C3 rule bars the cell from
CHOOSING a sibling read; none bars the orchestrator from INSTRUCTING one, and an
instructed read arrives as an instruction, not a violation. That round's brief said
"the sibling `ctx_shorten/proof.lean` shows the SHAPE of a `gap_*` probe" — the cell
complied, disclosed it, and the frozen verdict came back BREACH on that single event
while every other conviction was the known root-sweep FP class. dao roots at
`examples/` precisely so a sibling EXAMPLE is the leak unit, so brief and instrument
contradicted each other. **Convey shape by inlining the pattern or citing
`studying/templates/`, never by pointing a blind cell at a sibling's committed
proof/attack artifact.** A leaked round's Lean may be sound yet **VOID as evidence** — no tier, no
standing promotion, no coverage number (both proving lanes broke this 2026-07-14,
~3M tokens of green work discarded). Guard: `…/dao-scheduling-2026-07-10/PROMPTS.md`
§ Orchestrator blindness discipline (P1 step 5 self-check); memory
`feedback_blind_fanout_oracle_channels`.

**Evidence archive (`studying/waves/` — the dao archive half, landed
2026-07-31, ns:qagents/107 co-land).** Blindness-audit evidence freezes to the
gitignored, LAN/S3-backed `studying/waves/<example-id>-r<NN>/` via
`dao.sh --blindness-audit` → `transcript_audit.py --archive-evidence` (raw
`agent-*.jsonl` copies + `manifest.json`; replay via `--regrade <manifest>`),
in the SAME freeze-first step as the round verdict; gate `t_11` carries the
evidence arm. **Nothing evidence-shaped is ever committed** — a committed
evidence file is a C5 answer-roster, and any proposal to commit evidence
re-opens the PRIVACY gate (`data/debates/transcript-retention-2026-07-30.md`
R1/R8). Rounds stay committed append-only: the archive holds evidence ONLY —
no wave freeze, no `--archive-wave`, no `--push`. Operator ruling L-122
(cold-S3 non-debt — ledger row in
`…/axiomatize-shared-2026-07-04/LEARNINGS.md`) now has its studying surface,
carried here: no tunnel ritual — the archive rides the qred-nightly → qblk →
S3 daily ship. Backup lockstep (graduated 2026-07-31): `studying` left
`PROSPECTIVE_WAVE_SOURCES` and `capability.sh have_waves()` gained the matching
arm — **empty `studying/waves` hard-refuses** (half-migrated signature), absent
is a plain skip, and the dir is born POPULATED by the first evidence write,
never pre-created empty. Pinned by workstation-parity `t_14`.

**git v2 — index/staging.** Spec
`data/specs/index-staging-v2-2026-06-19/SPEC.md` (extends
`…/axiomatize-git-2026-06-10/SPEC.md`): the
`Operating/Git/` index substrate (`Index`/`Staged`/`RecordsIndex`/`Captures`) +
T4 promotion-discipline (the `data/tmp → data/specs` adopted-spec analogue,
`PromotionDiscipline`/`PromotionBreached`), T4a/T4b proved by `/dao-manual`.

**axiomatize-posix — the SUBSTRATE target (Phases 0–4 SHIPPED, family CLOSED —
Phase 5 broad-corpus deferred by design).** The layer BENEATH git
(files/processes/exit-codes): `Operating/Posix/` quartet + six
`Operating/Qagents/` bridge cells, one per spec § 3 primitive (LockCreate ·
RenameWrite · TrapRelease · SymlinkTeardown · PathContainment · GateAlgebra),
each a safety PROPERTY with an inhabitable breach dual. Live rules: `posix_*`
examples are modeled synthetic fixtures — no live extractor (§ 5),
`--golden-check` no-op PASS on `modeled:true`; scope stays the six § 3
primitives, NOT a POSIX-utility corpus. The `GateGreen` per-lane decomposition
is the second hierarchical cell → H2–H4 reached in the decomposition-discipline
sense (representation.md § H0–H4; model bake-off N/A-by-modeling, L-053s). Spec
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-posix-2026-07-08/SPEC.md`.

**axiomatize-llm-ops — COMPLETE on its ranked invariant set** (S-T2 index
bijection, S-T3 provenance authority, S-T4 ownership totality; spec
`…/axiomatize-llm-ops-2026-06-18/SPEC.md`, Round-1 record
`data/debates/axiomatize-llm-ops-2026-06-18.md`). Live rules that survive the
ship: the `Operating/Session/` domain is NOT a 4th axis; real-tree extractor
runs write ONLY to gitignored `Operating/emits/live/` (exit-9 on a tracked
target); S-T4 stays OFF the K-graph coverage numerator (observation posture —
only synthetic goldens tracked); redaction gate
`scripts/check_session_redactions.py`.

**The git↔session decomposition bridge (spec § 10, complete).** A
session-lifecycle skill is a DERIVED predicate decomposing into already-proved
git operations + a narrow residue (S-T5/S-T6/S-T7 + the `/open`/`/close`/`/lift`
bridge cells, all `Operating/Session/*Bridge.lean` + `Isolation.lean`
+ `DelegatedLanding.lean`). The `/do-claude-updates` `DcuBridge` cell (2026-07-07)
EXTENDS the skill-bridge family beyond the § 10 single-session vertical sequence
to the cross-session CLAUDE.md-maintenance skill — proved-git-T2 cascade
(merge-to-main) + the DCU-LOCK dual-sentinel + the QUEUE-1 hint-queue drain + one
Tier-1 hint-adjudication residue; `syn_dcu` GREEN. Live rules: an operational-axis adopt round MUST
seat the explicit qagents conditioning axioms as a first-class input (raw git
is the substrate, never the ceiling); the § 10.8 conditioning-axiom register
is canonical and grows leaf-by-leaf at the consuming skill (anti-vacuity).
Records `data/debates/git-session-bridge{,-sharpening}-2026-06-21.md`.

**`/lift` pre-condition model (studying owns the lift spec).** Per operator
directive studying OWNS + authors the entire lift spec (the `/open qagents`
session does the `lift.sh`/`close.sh` implementation + bash testing). The
donor-side-only eligibility model was inadequate for a two-party cross-session
protocol; studying-owned amendment
`data/specs/open-close-dcu-2026-05-26/lift-cross-agent-2026-06-24/SPEC.md`
(R1–R3 recipient eligibility + `route-to-owner` + the lift-set resolving base
OQ3). Axiomatic model `Operating/Session/LiftSafety.lean` — `LiftSafe`
REFINES `LiftBridge.LiftSkill`; a metric-neutral kernel cell (no fixture, no
status-pill bump). Promoting it to a coverage-bearing S-T6 `/lift` example is
the deferred proving step.

**Action-gating hooks — S-T8 gated-action coverage + S-T9 subagent gate-scope
monotonicity (proved).** `Operating/Session/HookGate.lean` models the
ACTION stream (outbound tool calls) + the `PreToolUse` hooks that gate them —
the dual of § 2d's context stream. Load-bearing: a project-scope hook does NOT
fire on a spawned subagent's call (user-scope settings only). Conditioning
axioms HOOK-1/2/3 + TOOL-1 + COST-1; spec § 11 of `axiomatize-llm-ops-2026-06-18`.

**Provable signoff verification — S-T10 `SignoffCoverage` (governance dual of
S-T8).** Kernel cell `Operating/Qagents/Signoff.lean` (governance primitives,
NOT `Session/`); studying owns the verification amendment
`…/signoff-verification-2026-06-30/SPEC.md` under
the cross-cutting signoff framework (`data/specs/signoff-framework-2026-06-30/SPEC.md`).
Live rules: coverage is over LEDGERED pushes only (completeness = the
independent S3/CloudFront inventory diff, outside Lean); green is NOT a safety
claim; OBSERVATION posture — lane metrics in `status_emit.mjs`, never the
K-graph numerator; redaction gate `scripts/check_signoff_redactions.py`. A gate's
**mechanical** scanners prove rider presence / byte-equality / clause absence;
they CANNOT prove the judged bindings (e.g. FINANCIALLY CLEAR-5: verdict-token ↔
run-emit) — a green `--rider-floor` / `scan_financial.sh` is necessary, never
sufficient (3.6 was mechanically green, substantively refused, 2026-07-10). This
is R1/R15 in operational terms.
**CLEAR-3 is DISCHARGE-TYPED (P2f, 2026-07-21)** — non-widening kernel theorem
`face_class_confusion_uncleared`; the three STANDING FACTS-1 negative-closure
obligations + typing + gate `t_07` live in spec § 10 P2f (path above).
P0–P2f shipped 2026-06-30/07-03/07-21; P3 alone remains (spec § 10). Live-leg
status tracked at `ns:studying/25` — don't mirror it here.

**Constellation graph M.** A second instance-level graph (alongside the
snapshot graph): the whole monorepo + the separate `~/.claude` memory repo as
one non-hierarchical networkx `MultiDiGraph`, the partitioning exercise the
uscode tree and tiny K-graph cannot give (`scripts/extract_constellation.py` +
the `graph-extract-constellation` skill + synthetic golden). Live invariants:
an **observation** graph — never enters the coverage numerator, never gates
`lake build`; `privacy:local-only` (R9) — live emit gitignored at
`Operating/emits/live/constellation.json`, never under canonical `data/` or a
`/publish` sweep; only the synthetic golden is tracked. Spec
`data/charters/studying/specs/lean4-charter-2026-06-10/constellation-graph-2026-06-17/SPEC.md`.

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

**Full-project state review 2026-07-03 — mostly discharged.** Record +
residue: `studying/reviews/state-review-2026-07-03.md`, the 6-counsel debate
`data/debates/studying-state-review-2026-07-03.md`, and `ns:studying/30`.
Two rules outlive them. (1) Coverage maps from CONSTRUCTIVE proved-target
moves ONLY, never appear-only — the P2-5 provenance guard LOUDLY refuses an
uncertified-basis cell's Tier-A down to B rather than inflate; the local-only
`emit_catalog.py` basis (R13 `open_ct`) and the public pill's conservative
20/22 hold-out are two blessed bases, never corrected to each other.
(2) **The hold-out is a RULING, not an open question (operator, 2026-07-22;
L-118): the blind-cert badge gates on CUMULATIVE `standing.adversarial === 0`,
so a historical landed-then-repaired attack disqualifies a cell permanently and
the public figure stays 20/22.** The latest-round-scoped alternative (22/22) was
REJECTED, not deferred; reversing it needs a fresh operator ruling, never a gate
edit (recorded at the gate site in `status_emit.mjs`). Rationale: a cell that
ever had something land is repairable, not un-landable.

**dao-scheduling program (2026-07-10) — the standing run plan.**
`data/charters/studying/specs/lean4-charter-2026-06-10/dao-scheduling-2026-07-10/SPEC.md` +
`PROMPTS.md` (P0–P7) adopt proving's Phase-4M scheduling discipline (SPEC +
frontier + model/effort matrix + dated actual-vs-estimate rows; LEARNINGS
L-057s), target-scoped for `/dao` rounds. § 3 frontier ranks the backlog;
§ 12.1 is the calendar. **axiomatize-ledger — COMPLETE on its ranked set
(R1–R4 shipped 2026-07-10/11, A1–A4 met; R-T6 DEFERRED event-gated, § 3.6).**
Subspec
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-ledger-2026-07-10/SPEC.md`
(t_01–t_03 3/3): the shared-ledger-store RDB semantics
(`data/specs/shared-ledger-store-2026-07-09/SPEC.md`) as an `Operating/Rdb/`
substrate quartet + five `Qagents/Ledger{Append,Replay,Spool,Render,Adopt}.lean`
bridge cells, all GREEN with inhabitable breach duals.
Live rules: modeled fixtures, 0 LLM leaves (L-051s lane; L-053s caveat); NO
live DB extractor in v1 (privacy § 5); rdb cells ON the coverage numerator
(spec § 7 supersedes the ns-29 off-numerator note); five `op.Rdb.*` K-graph
probes + the `ledger-concepts` cite parser (code/lean_graph). Coverage + pill
numbers live in `Operating/emits/lean_graph/coverage.json` + the status emit —
the § 3 frontier is the ranked backlog; consult it, don't mirror it here.

**axiomatize-context-ops — Leg B + W1 SHIPPED 2026-07-22; W2 COMPLETE 2026-07-31 (frontier row 11). The CTX-T1..T4 bridge-cell set is CLOSED.**
**CTX-T3 `ctx_recall` is closed on a NEGATIVE RESULT and must not be re-opened as a
repair round** — clause (iii) of `RecallIsolation` is not axiomatizable as a
fork-mechanism guarantee. Normative record + the two conditions binding any re-seat
(a NON-ENUMERATING fixture; escapes with an INHABITED NEGATIVE CASE) live in the
NEGATIVE RESULT section of `Operating/Operating/Qagents/CtxRecall.lean` — read it
there, never restate it from memory. Ledger seq 167; committed witnesses
(`attack/r0{1,2,3}_*`, `rounds/0{1,2,3}.json`) are the evidence and are never deleted
to make the cell look clean. Two residues the rounds proved: REFUSE-1 carries the
identical disease (warn-only "scanner flagged, pipeline shipped" is `False` by axiom),
and every seat here is DROPPABLE because the modeled fixture over-emits.
**CTX-T4 `ctx_degrade` GREEN 2026-07-31** (`Qagents/CtxDegrade.lean` DegradedHonesty —
declared consumers, per-consumer degraded semantic, destructive-refuses/reporting-labels
conformance; duals grounded in the memsearch `reset` finding). Judge GREEN, 15 attacks
0 LANDED, C:11 A:7, **Tier-B on an uncertified basis — the round's blindness verdict is
BREACH, so no tier, no standing promotion, no coverage number rests on it.** Round 02's
seven ranked gaps: `ns:studying/60` (do not re-derive the two prose defects marked
`CORRECTED round 01`).
**Leg B:** `scripts/ctx_miner.py` (frozen pattern set, no LLM) + gate `t_02_miner_floors`;
report local-only under the § 5 C-1..C-5 floors. Its first run inverted the
graduation question — **adding rows beats graduating rows 2–6** (spec § 9.1).
**W1:** `Qagents/{CtxTypes,CtxVerdict,CtxShorten}.lean` + modeled `ctx_verdict`/`ctx_shorten`,
judge GREEN both. **Read spec § 9.2 before touching either cell:** the round landed NINE
attacks against the orchestrator-authored kernel (K1–K9), repaired same-round. Standing
consequences that bind future work:
· **K1 (the kill) — every conditioning axiom carries an ESCAPE PREDICATE.** An
  unconditioned seat whose conclusion is the NEGATION of a breach dual makes that dual
  UNINHABITABLE: the kernel refutes its own breach, and the detection lifter proves
  anything. `ctxInject_gated` is now conditioned on `PushGated`. Never state a seat
  whose domain is the dual's domain.
· **K3–K7 — emit the closure the PRIMARY dual's bite needs** (guarding the secondary
  passes every gate), **credit it to the right dual in prose**, and **withdraw rather
  than patch** a refuted seat. Per-attack detail: spec § 9.2.
· **K8/K9 are OPEN W2 decisions, recorded not taken** — the three are at `ns:studying/38`(b).
Tier stays modeled Tier-B; a C3 read-side breach is on the record for every cell in
this family, so no blind-cert is claimed anywhere in it. Adoption context (the four `Operating/Qagents/Ctx*.lean`
bridge cells CTX-T1..T4, their claims + breach duals, and the no-new-substrate
rule) is the spec § 4 table — don't mirror it here.
Live rules: the R3 emit/derive law (negative closures are EMITTED facts or the
dual is disarmed — W6/CLEAR-3f); modeled Tier-B unless per-cell blind-certified;
committed GREEN duals are per-wave deliverables; AXES custody — new catalog axis
tokens route to visualizing BEFORE the wave, cells stay off-emit until landed
(H-3/H-4 law); the `--ctx-check` scanner does NOT enforce the Leg-B
miner-content bar (authoring discipline). Spec
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-context-ops-2026-07-22/SPEC.md`
+ record `data/debates/axiomatize-context-ops-2026-07-22.md`; PCI § 7 item 6 is
the folded Leg A.

**Shape-gate discipline (load-bearing — the ns-34/ns-38 silent-red class).**
Each spec-family suite (`data/charters/studying/specs/**/tests/run.sh`) is
exercised only when its OWN `run.sh` is invoked, so a gate goes **silently
red** when a chartered artifact (cell / template / schema) lands without
updating that gate's expected-set. Two obligations: (1) landing any chartered
artifact MUST update its shape-gate's expected-set **in the same change**;
(2) run the loud aggregating battery `studying/scripts/spec_battery.sh` (globs
every family `tests/run.sh`, exits non-zero on any red, dumps the failing
suite's output) before `/close` — never trust that the one family you touched
is the only one that drifted. A NEW family with a `tests/run.sh` is
auto-discovered by the glob. Adjacent trap: a gate whose accumulator is only
asserted in a wrapper `main()` is green-but-dead ([[feedback_pytest_ck_accumulator_laundered_pass]]).

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

`studying/lean-toolchain` is pinned in lockstep with `proving/lean-toolchain`
+ `accounting/lean-toolchain` (the pin value is the file itself + the
`guide-rails.md` skew note — not restated here). Any bump moves all three and
replays each kernel's example proofs
(`feedback_lean_toolchain_bump_verify_example_proofs`).

**Studying carries TWO pins**, not one: `studying/lean-toolchain` *and*
`studying/Operating/lean-toolchain` (the Operating package is the actual kernel).
Both move together or `elan` resolves differently depending on cwd — see the
cwd-dependency note below.

**"One commit" is not always achievable — record the deviation when it isn't.**
When the three subprojects are each held by their own open session
(branch-as-write-lock), the bump lands as one commit per branch, in lockstep
in time, each independently verified (done at the 2026-07-14 v4.31.0→v4.32.0
bump — proving `25f8cf201`, accounting `4d7cfb548`, studying `4b81cc650`).
Verify each axis separately and say so; do not let the three drift across a day.

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
