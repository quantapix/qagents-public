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
  re-clear untouched — condition 9). Machinery: `scripts/live_check.sh`
  (canonical-side; ledger-pinned targets; **state-key = digest of the extractor
  input snapshot — refs + worktree table + sentinel stats, never HEAD** (R2);
  clean-tree eligibility; pidfile singleton; atomic `result.json`) +
  `scripts/emit_live_check.py` (term-only check file, exit-9 privacy anchor) +
  `scripts/emit_context_manifest.py` (≤40 lines/2KB, emit-time fail-closed
  self-scan) + `scripts/check_context_redactions.py` (kernel-derived denylist;
  `--dotted-only` = downstream-sweep mode) + SessionStart hook
  `studying/scripts/hooks/session-start-ctx.sh` (registered in
  `data/claude-settings/sources/baseline.hooks.json`; pilot scope
  `studying*`/`qagents*` in-script) + `close.sh --ctx-check` (exits 46/47) +
  `/open`-time async spawn in `scripts/open.sh`. The surface is a
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

**HARD RULE — adversarial independence is the ONLY oracle; protect ALL FOUR channels
(2026-07-14).** A parried attack is evidence *only* if the attacker did not know the
proof and the proof was not pre-hardened against the attack list. Four leak channels —
C1 scratchpad, C2 orchestrator, C3 read-property, C4 memsearch (spec-of-record:
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/SPEC.md` § 4a) —
closing one buys nothing; (a)/(b) below detail C1/C2, the two that live in this
orchestrator's own hands. (a) *Filesystem:* the runtime hands every subagent the SAME
writable session scratchpad — agent scratch goes under its own disjoint
`<out>/.scratch/`; the session scratchpad is off-limits
(`.claude/agents/dao-{coding,testing}.md` § Scratch isolation). (b) *Orchestrator:*
from round 2 the orchestrator holds both sides' results — routing one side's finding
into the other's prompt makes the next green an echo; **name the METHOD, never the
ANSWER**. A leaked round's Lean may be sound yet **VOID as evidence** — no tier, no
standing promotion, no coverage number (both proving lanes broke this 2026-07-14,
~3M tokens of green work discarded). Guard: `…/dao-scheduling-2026-07-10/PROMPTS.md`
§ Orchestrator blindness discipline (P1 step 5 self-check); memory
`feedback_blind_fanout_oracle_channels`.

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
**CLEAR-3 is DISCHARGE-TYPED (P2f, 2026-07-21).** A clearance record anchors at
TWO levels — a roll-up `payload.content_sha256` AND a `faces[]` table — while the
push-ledger records the BYTES that landed on a surface (one face). Joining the two
scalars by name made a properly-cleared CDN push read as a FALSE `UngatedPush`.
`BindsPayload` = roll-up ∨ face-at-the-class-the-push-discharges (`Discharge` enum
+ `BindsFace` + `DischargedAt`, the last a committed surface→class map reaching the
kernel as a FACT in the `GatedBy` pattern); non-widening is the kernel theorem
`face_class_confusion_uncleared`, never a convention. **Three FACTS-1 obligations
travel with it** — the NEGATIVE discharge closure for an unclassified push, the
CLASS-KEYED face closure, and no `rollup` face class. Drop any one and the CLEAR-3
BREACH lens silently stops biting while coverage stays fail-closed and `lake build`
stays green; gate `t_07`.
Remaining: P3 only (spec § 10; frontier ns:studying/25) — wire the publishing
§ 10 build gate + `upload-video.sh` emit and the atomic `clearedBy →
signoffs{}` migration; P0–P2f shipped 2026-06-30/07-03/07-21. The **live** cell is
blocked on an evaluating-owned input defect, not on studying: `granting_commit` is
the unfilled placeholder `"pending-grant-commit"` in 14/17 FINANCIALLY records, so
CLEAR-1 emits no `Precedes` fact (`ns:evaluating/13`).

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
(2026-07-07).** Two standalone operational safety PROPERTIES proved by the
`/dao` lane (NOT skill bridges — no flat golden): `Operating/Session/
Pending.lean` — `PromotionTotality` over the cron-lane `pending/` → canonical
CLOSED-SET allow-list classifier + the `unclassified_not_promoted` default-skip
safety (no unregistered path reaches canonical; `syn_pending`,
pending-promotion-scope-2026-05-28); and `Operating/Session/
WtLinks.lean` — `WorktreeLinkSafe` (a declared `.worktree-links` glob is
symlink-safe IFF its canonical target is pure-gitignored — zero tracked files) +
the `safe_target_untracked` payoff + the `unsafe_of_tracked` refusal / `UnsafeLink`
breach dual (`syn_wtlinks`, session-lifecycle charter § 2.4). Both GREEN, on the coverage
numerator, breach duals inhabitable.

**Full-project state review 2026-07-03 — mostly discharged.**
`studying/reviews/state-review-2026-07-03.md` (5 HIGHs + fix plan P0–P4 +
metric set M-1…M-10) + the 6-counsel debate record
`data/debates/studying-state-review-2026-07-03.md` (21 rulings, ADOPT-AMEND).
P0 + docs + the 2026-07-10 hardening sweep + the 2026-07-13 W3 partial
(K-2/D-6/E-1/E-3/M-5 + numeric-lift audit) landed — detail in the review doc.
Residue (next-steps item 30): the former custody-gated-on-visualizing items
UN-GATED 2026-07-20 (visualizing ratified the qcatalog/qrounds vocabulary —
validator `AXES` + kit `Axis` at **44** operational tokens, corpus-reconciled;
the routed "+29" proposal was stale/insufficient; visualizing filed its
reciprocal item 29). **30(b) catalog-roster leg LANDED 2026-07-20:**
`emit_catalog.py` restructured into DERIVED (22 file-clean cells, leaves
auto-extracted) + CURATED (14 multi-file/cited cells) = **36 cells / 133
leaves** (was 7); `validate_catalog.py` two-sided PASS; t_07 green (cells=36
covered=31); tiers 22-A/9-B/5-unknown — the 7 uncertified-basis cells
(posix bridges + signoff) LOUDLY refused Tier-A → B via the P2-5 provenance
guard (integrity: coverage is CONSTRUCTIVE-proof-target-only, never appear-only,
so no inflation). NOTE: catalog is local-only; its Tier-A for the two
K-1-repaired cells (`syn_close`/`syn_delegated`, R13 `open_ct` basis) is a
DIFFERENT basis than the public pill's conservative 20/22 hold-out — the two
bases are never corrected to each other. **The hold-out is now a RULING, not
an open question (operator, 2026-07-22; L-118 adopted): the blind-cert badge
stays gated on CUMULATIVE `standing.adversarial === 0`, so a historical
landed-then-repaired attack disqualifies a cell permanently and the public
figure stays 20/22.** The latest-round-scoped alternative (which would read
22/22) was REJECTED, not deferred; reversing it is a public-figure change
needing a fresh operator ruling, never a gate edit. Recorded at the gate site
in `status_emit.mjs`. Rationale worth keeping: a cell that ever had something
land has been shown to be repairable, not un-landable. Remaining 30(b) sub-legs: H-4 rounds-schema (qrounds/1) re-apply,
R11 register TSV + R13 metrics.json envelope, M-6 STALE pill. Still
deferred-landable: P-6 / M-6 producer / D-7b. K-rounds all landed 2026-07-17
(frontier § 8 W3b/W3c rows).

**dao-scheduling program (2026-07-10) — the standing run plan.**
`data/charters/studying/specs/lean4-charter-2026-06-10/dao-scheduling-2026-07-10/SPEC.md` +
`PROMPTS.md` (P0–P7) adopt proving's Phase-4M scheduling discipline (SPEC +
frontier + model/effort matrix + dated actual-vs-estimate rows; LEARNINGS
L-057s), target-scoped for `/dao` rounds. § 3 frontier ranks the backlog;
§ 12.1 is the calendar. **axiomatize-ledger — COMPLETE on its ranked set
(R1–R4 shipped 2026-07-10/11, A1–A4 met).** Subspec
`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-ledger-2026-07-10/SPEC.md` +
t_01–t_03 suite 3/3: the shared-ledger-store RDB semantics
(`data/specs/shared-ledger-store-2026-07-09/SPEC.md`) as an `Operating/Rdb/`
substrate quartet + five `Qagents/Ledger{Append,Replay,Spool,Render,Adopt}.lean`
bridge cells (R-T1..R-T5 GREEN; R-T6 DEFERRED event-gated, § 3.6); all rounds
GREEN incl. the R4 differential-probe re-judge; breach duals inhabitable.
Live rules: modeled fixtures, 0 LLM leaves (L-051s lane; L-053s caveat); NO
live DB extractor in v1 (privacy § 5); rdb cells ON the coverage numerator
(spec § 7 supersedes the ns-29 off-numerator note); five `op.Rdb.*` K-graph
probes + the `ledger-concepts` cite parser (code/lean_graph). Coverage + pill
numbers live in `Operating/emits/lean_graph/coverage.json` + the status emit —
the § 3 frontier is the ranked backlog; consult it, don't mirror it here.

**axiomatize-context-ops — Leg B + W1 SHIPPED 2026-07-22 (frontier row 11; W2 = next GO).**
**Leg B:** `scripts/ctx_miner.py` (frozen pattern set, no LLM) + gate `t_02_miner_floors`;
report local-only under the § 5 C-1..C-5 floors. Its first run inverts the entailment
ledger's own question — the top concepts by avoidable re-derivation cost are all
UNLEDGERED, so **adding rows beats graduating rows 2–6** (spec § 9.1).
**W1:** `Qagents/{CtxTypes,CtxVerdict,CtxShorten}.lean` + modeled `ctx_verdict`/`ctx_shorten`,
judge GREEN both. **Read spec § 9.2 before touching either cell:** the round landed NINE
attacks against the orchestrator-authored kernel (K1–K9), repaired same-round. Standing
consequences that bind future work:
· **K1 (the kill) — every conditioning axiom carries an ESCAPE PREDICATE.** An
  unconditioned seat whose conclusion is the NEGATION of a breach dual makes that dual
  UNINHABITABLE: the kernel refutes its own breach, and the detection lifter proves
  anything. `ctxInject_gated` is now conditioned on `PushGated` (the `Operating.Rdb`
  `SeqBacked` shape). Never state a seat whose domain is the dual's domain.
· **K3/K4 — emit the closure the PRIMARY dual's bite needs, and credit it correctly.**
  Guarding the secondary dual passes every gate. And a closure credited to the wrong dual
  in prose invites a later author to drop the load-bearing fact.
· **K5/K6/K7 — withdraw, don't patch.** `Counted` is a MARK not a count (the empty
  renderer is conservative — SPOOL-2 conservation-not-liveness); the A-1 cost story was
  relocated not escaped (`cost_bound_seat` is the identity, the cost lane is DISJOINT from
  the property); a MEASURED load-free conditioning axiom was deleted, not defended.
· **K8/K9 are OPEN W2 decisions, recorded not taken** — CTX-T1 today *certifies* a snapshot
  on which a stale certificate crossed (ineligible rows), and the seat is droppable because
  the modeled fixture OVER-EMITS. Do not take either under repair pressure.
Tier stays modeled Tier-B; a C3 read-side breach is on the record, so no blind-cert is
claimed for either cell. Original adoption context follows. The
2026-07-21 extending reviews (`data/specs/{rtk-review,memsearch-pg-review}-2026-07-21/`)
routed to studying as kernel targets: four `Operating/Qagents/Ctx*.lean` bridge
cells — CTX-T1 VerdictTotality (typed inject/withhold/refuse over the PCI push
gates) · CTX-T2 ShorteningConservativeness (closed-set classification, unclassified
⇒ passthrough never drop, counted omission, gap-pinned `never_worse`) · CTX-T3
RecallIsolation (the C4 seat as a fact) · CTX-T4 DegradedHonesty (per-consumer
`refuse|label|serve`; consumer CONTRACT only, non-precedential) — **no new
substrate** (shared enums in `Qagents/CtxTypes.lean`); breach duals grounded in
lived failures (rtk silent-drop, memsearch reset-drops-fallback, the C4 breach).
Live rules: the R3 emit/derive law (negative closures are EMITTED facts or the
dual is disarmed — W6/CLEAR-3f); modeled Tier-B unless per-cell blind-certified;
committed GREEN duals are per-wave deliverables; AXES custody — new catalog axis
tokens route to visualizing BEFORE the wave, cells stay off-emit until landed
(H-3/H-4 law); Leg-B miner is qagents-transcripts-only, report local under § 5
C-1..C-5 (the `--ctx-check` scanner does NOT enforce the miner-content bar —
authoring discipline). Spec
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
sandbox probe dir, `/tmp`) silently falls back to elan's **default** toolchain. This
voided real work on the textual axis: cells validated against 4.32 while the kernel
was pinned at 4.31, and a bare `lean` **rejected the kernel's oleans with
`incompatible header`** — which a cell then "worked around" by recompiling the shared
`Common` from source, i.e. validating against a compiler the kernel does not use. Its
green meant nothing. Always `lake env` from the package root, or
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
