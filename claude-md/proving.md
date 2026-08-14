# proving — Lean4 axiomatic theorem-proving with LLM-backed predicates

Cross-project rules: `../CLAUDE.md`. The **textual axis** of the three-kernel Lean4 architecture (root CLAUDE.md § "Lean4 axes"; `data/charters/studying/specs/lean4-charter-2026-06-10/SPEC.md` § 4) — `/dau` is the textual-axis instance of invariant 3: proofs driven by top-tier LLMs in parallel, never manual. Scope charter: `data/charters/proving/textual-axis/CHARTER.md` (the `axiomatize-uscode-2026-05-29` family is scope-resident there; domain-vs-mechanism carve in its § 3).

## The split

The whole point of this subproject is **strict jurisdictional separation** between three layers. Do not blur them.

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Proving/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one complaint text + entity refs | a single `Bool` (plus evidence + uncertainty) | Claude Code sub-agent (`context: fork`); MAY use `memory-recall`. |
| **Driver** | `scripts/extract_facts.py` | manifest + complaint | `Proving/<Framework>/Facts.lean` (axioms) + audit JSON | `claude -p` invocations (model from the shared seat `code/lean_tools/model_floor.py`). |

The Lean kernel never reads natural language. The predicate sub-agents never write Lean. The driver is a thin coordinator with no legal reasoning of its own. The verifiable proof IS the Lean elaboration trace produced by `lake build`.

The normative kernel↔predicate↔driver workflow representation the `/dau` lane is pointed at is `../studying/representation.md` (studying owns the operational-axis kernel + the cross-axis representation research; charter P1 gate).

Why it works: a predicate's output domain is one Bool per call, so it fits inside a forked sub-agent; and once each predicate fact is an axiom, the validity theorem is a pure structure-introduction proof — type-checking guarantees the result *given the predicate truths*.

## Frameworks

Each framework lives under `Proving/<Framework>/` (kernel) + `predicates/<framework>/` (specs).

The per-framework roster (kernel · specs · source guide · statutory text for all nine goldens — Civil RICO, Title VI, CivilRights, Title IX, Title VII ×3, Rehab §504, Age Act, Title II Enf, ADA) lives in memory `reference_proving_doctrine_pins` § "Frameworks roster", which also carries the case-law doctrine pins and the top-level inductive shapes (`ValidCivilRicoComplaint`, `ValidTitleVIJudicialClaim`, …).

The operative statutory text lives under `legal/uscode/`, never pasted into specs. Predicate sub-agents resolve a `usc_cite` via `scripts/uscode.py path|text|list` — index→corpus fallback + subsection normalization (L-029), so an arbitrary in-Code cite resolves without extending the curated `index.json` (`uscode.py lint` reports cite resolvability). See `predicates/README.md` § "Authoritative statutory text". **Cite-resolution hazards (bare-section ambiguity, the `NoteSlotError` note-slot refusal, the `corpus_render_census.py` oracle) → `predicates/README.md` § "Authoritative statutory text"** (relocated 2026-08-09) — read before authoring or debugging any cite resolution; live roster: `feedback_derived_corpus_is_unguarded_oracle`.

These hand-built frameworks are the **golden reference** — automated encodings are scored against them. The per-framework golden ROSTERS live in `predicates/GOLDEN-ROSTERS.md`, **barred to blind cells** (Hard rule 9); derivation + gap + mechanism detail: `reference_proving_doctrine_pins`.

## Axiomatizing the full U.S. Code (program)

Spec: `data/charters/proving/specs/axiomatize-uscode-2026-05-29/SPEC.md`. Extends the hand-built frameworks to a phased, title-by-title program over all 54 titles, produced redundantly by top-tier-model subagent teams along **10 orthogonal axes** (5 core always fanned out + 5 opt-in via `--axes`; roster = spec § 6.1, single owner), then reconciled. Cross-strategy agreement, proved in the kernel via `Bridge.lean` lemmas, is the correctness signal for the LLM→Lean mapping (no other oracle exists).

- **Ground truth:** full USC markdown at the canonical USC text mirror (gitignored, ~65.7k sections, `tools/corpus_build.py --all`) + the canonical USC text mirror. `corpus/` + `xml/` are symlinked into every worktree via the canonical USC text mirror.
- **Naming / Lean-shapes / predicate-shapes** frozen in spec §§ 3–5 (authoring contract: `predicates/README.md` § "USC-program authoring contract"); per-(title,axis) namespace `Proving.USC.T<NN>.<Axis>`; shared cross-title predicates collapse to `Proving.USC.Common` (guarded by an equivalence Bridge). Code: `Proving/USC/Common/` + `predicates/usc/_axes/<axis>.md` (10 axis briefings) + the `ProvingUSC` lean_lib.
- **§ 1962(c) calibration anchor (hand-built, kernel-green):** all 6 axes under `Proving/USC/T18/<Axis>/` + `Bridge.lean` + `Reconciled/T18.lean` (`Bridge.s1962c_tierA` = spec § 8.3 Tier-A). The template cell-agents mirror and the fan-out's scoring reference.
- **Calibration metric is BRIDGE-BASED.** Agreement-vs-golden is measured by kernel-checked **golden-bridges** (`Proving/USC/T{18,42}/GoldenBridge.lean`): the blind cell's composite implies the golden composite under declared correspondence axioms, sorry-free (mechanics + tier ladder: spec §§ 4.6/8/9.4). Score ONLY via the shared cross-axis G2 oracle guard `code/lean_tools/score_bridge.py --lexicon agreement --root proving`, never a local copy: it certifies no `sorryAx`, reads the tier from a `_modulo_gaps` theorem-name suffix, and surfaces each omitted golden element as a named `gap_*` hypothesis. `scripts/calibrate_golden.py` is a regression check for hand-built name-matched cells ONLY — exact-string is unwinnable for blind agents.
- **Lane:** manual-interactive via the **`/dau-manual`** skill (`.claude/skills/dau-manual/`; mirrors `/dco-manual`) — the SDK batch lane is paused (root CLAUDE.md § Agent SDK lane). Mechanics, targeting gate, re-earn backlog, wave archive/backup: spec § 7.5 + § 10.1 + the SKILL; tests `data/charters/proving/specs/axiomatize-uscode-2026-05-29/tests/`.
- **Wave-planning authority is the UNION of every seat's archives.** `proving/waves/` is gitignored canonical-only, mirrored **per source host**, so it is a PARTIAL view on every workstation and `remediation_census.py` reads a wave this seat cannot see as backlog. Before any roster regen: `scripts/dau.sh --sync-peer-waves` (→ read-only `proving/waves-peer/<seat>/`, **never merged into `waves/`**), then census — and **`ls` the peer symlink first**, because the sync writes CANONICAL while the census resolves `waves-peer` against the WORKTREE, so a green sync proves nothing (measured: 29% phantom backlog). Read `host_scope` before believing any figure; `invisible_waves` names only what NO seat holds. **BACKLOG DIRECTION IS SET BY THE BLINDNESS CLASSIFIER, NOT BY THE ENCODING — read the per-reason partition, never the headline** (2026-08-10, ns-149). `_REVIEW_MANDATED` exempts on `review_channels ⊆ {C5}` ∧ `c5_rungs ⊆ {names,types}` — a **whitelist of the channels a compliant agent may raise**, which goes stale each time a channel is added, and fails silently as a re-slice obligation on sections that just earned Tier-A. **ONE entry is stale, not two — door (a) was REFUTED 2026-08-11** (debate `ns-transition-enforcement` / `backlog-unblock-sequencing` R4): the reconciler's C1 came from a bare `ls` of the shared scratchpad, which `dau-reconciler.md` **expressly bars** ("the probe is itself the violation") and which names that very wave, so the classifier graded it CORRECTLY and that wave's cert had already adjudicated it — calling the proposed cure "a laundered pass." What is stale is **C7 firing on a blind cell reading its OWN axis briefing + the SPEC §§3-5 conventions**, its two mandated inputs, so with `--contract-file` the exemption is unreachable for every compliant cell (seq 237); it has never fired in the field (all 12 certs record `contract_file_passed: false`) but is structurally guaranteed on any L-042 fallback wave, where the flag is mandatory. **And T20's move was +6 added / 3 reason-changed / 0 removed, NOT "+9 added" — the cause was SLICE WIDTH, not the classifier:** `latest[(title,sid)]` keys off the wave's own `title_slices`, only 3 of its 9 sections were owed, and **a slice ⊆ the roster cannot add a row, by construction** (the cure, ns-150). What survives of the classifier question is a REMEDY mismatch: a re-slice re-encodes CELLS, so reconciler misconduct wants a `wave:reconciler` re-adjudication class. **`--contract-file` is a grading-changing flag, not hygiene** — pass it only on an L-042 fallback wave (contract inlined ⇒ C2 needs subtraction); a verdict from wrong params is re-run against the same frozen evidence, never hand-adjusted. Normative: spec § 10.1; measurements + never-merge rationale: `feedback_per_host_ground_truth_is_a_partial_view`. Since 2026-08-06 the cron sentinel `proving:axiom-state` (05:10 daily, `scripts/axiom_state_check.sh`) runs sync + census-freshness + backup-lag + cert-staleness + G7-attest + battery-consumption arms and stamps `waves-peer/.sync-as-of` — read its latest fire log before any wave (baseline-DIFF exit: standing reds are in the per-arm lines, not the exit code); design + gate conditions: `debate record `axiom-routine-review-2026-08-06` (data/debates/, HELD lane)`.
- **Wave backup: LAN-primary, never wave-blocking** — operator ruling L-122 (`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/LEARNINGS.md` row L-122); wave-end mechanics, queue-non-debt, verify verbs + verdict ladder: spec § 10.1 (→ artifact-archive spec § 2).
- **Status:** Phases 0–1 done; Phase 2 calibration anchor + waves promoted to canonical (approach-B `Proving.USC.<Title>.*` sub-namespaces; cross-title Common-collapse; corpus rollup `proving/coverage.json`). Phases 3–4 (SDK-funded bulk scaling) are **paused, not cancelled** (root CLAUDE.md § Agent SDK lane). **Per-wave detail + remaining-section roster + current state live in spec § 10.1 + the close summaries — never duplicated here.** Two load-bearing invariants: cell Lean files MUST use FULL-path imports (`reference_lean_isolation_probe_full_path_imports`); the authoritative build target is **`lake build Proving ProvingUSC`** — BOTH libs (bare `lake build` is red-by-design on REJECTED examples; `ProvingUSC` alone excludes every golden's `Theorems.lean`) — run it before promoting, never trust a cell's self-report. **Pair it with `check_olean_closure.py`: a green build says nothing about a file no root reaches** — root a new subtree's `Theorems` explicitly, since bridges import `.Statute` (`feedback_unrooted_lean_file_is_never_elaborated`).
- **Hierarchical-predicate depth layer (H0–H4 landed).** Flat opaque predicates decompose into LLM-decided leaf predicates + kernel-derived composites over a three-tier model stratification. **Oracle guard (load-bearing):** search automation (`grind`/`aesop`) NEVER discharges a `Bridge`/`GoldenBridge` agreement lemma — `score_bridge.py`'s `reject_automation_in_bridge` enforces it syntactically (**exit 4**, ahead of `sorryAx`). The archive-time `--oracle-guard-dir` sweep **skips dot-prefixed agent scratch and PRINTS the skip count**; promotable paths are still swept, so a bridge living only in scratch is never promoted. Full detail: `…/hierarchical-predicates-2026-06-20/SPEC.md` §§ 13/13.1; status of record `../studying/representation.md` § 13.4.
- **Graph projections (Half-A domain graph).** `scripts/uscode_graph.py --cite-graph` emits the **`qgraph-wire/1` node-link envelope** (deterministic Axis-5 §-citation graph, `graph.axis=textual`), consumed by BOTH the graphs kit's `fromNodeLink` reader AND `qagents.lean_graph`'s `anchor()` |D| join. Flags, gitignored `proving/graphs/`, tests: `…/graph-projections-2026-06-14/SPEC.md` § 4.2.

## Layout (essentials)

`Proving.lean` (root module) · `lakefile.toml` · `lean-toolchain` (pinned — § Toolchain notes) · `Proving/<Framework>/{Types,Predicates,Statute,Theorems}.lean` (+ generated, gitignored `Facts.lean`) · `predicates/<framework>/` (one spec per opaque predicate) · `examples/<id>/` (per-run artefacts, below). `scripts/`: `extract_facts.py` (driver) · `lake_trace.py` (two error-line orderings, 4.29 vs 4.30+) · `lean_parse.py` (regex proof-file parser) · `uscode.py` (path/text/list lookup) · `uscode_graph.py` (Axis-5 §-citation graph).

## Workflow

1. **Author the formal framework** (Lean) — for a new framework, add `Proving/<NewFramework>/{Types,Predicates,Statute,Theorems}.lean` and import from `Proving.lean`.
2. **Author predicate specs** under `predicates/<newframework>/`. Spec format is fixed (see `predicates/README.md`).
3. **Run the driver**:
   ```
   python3 scripts/extract_facts.py examples/<id>/complaint.md \
           --manifest examples/<id>/manifest.json --example-id <id> [--build]
   ```
   The manifest's `framework` block selects where Facts.lean is written, the namespace prefix, and the `proof_target` lake target. `--build` emits `report.json` + `graph.json` + `loci.json` per the propagation spec. `--reuse-facts --example-id <id>` skips the predicate sub-agents and re-emits from the existing `facts.json`.

4. **Verify**: `lake build Proving ProvingUSC` — bare `lake build` is red-by-design (§ Status). Elaborate one example via `lake env lean examples/<id>/proof.lean` once Facts.lean exists.

The driver prints one `· <spec> ... <value>  (<uncertainty>)` line per predicate in **all three modes** (`--stub`/`--reuse-facts`/production); adapters (`verifying/server/adapters/proving.py._classify`) rely on that shape being identical across modes.

**`--stub` caveat for REJECTED examples.** `--stub` defaults every predicate to `True`, so it would overwrite committed REJECTED reports with synthetic ACCEPTED and (never reading `manifest.inputs.*`) conceal a manifest drifted from its complaint. **Guard-enforced** (L-030): a committed (non-`--sandbox-out`) `--stub` run against a `REJECTED` example **refuses** (exit 2) unless `--force-stub` — use `--reuse-facts` for any replay over a REJECTED run. Timeouts preserve paid work (retry + `facts.partial.json`). Tested by `scripts/test_driver_hardening.py`; `feedback_proving_stub_defaults_true`.

## Per-run artefacts (`examples/<id>/`)

When invoked with `--build`, the driver emits:

| file | what | consumer |
|---|---|---|
| `facts.json` | per-predicate `{value, evidence, uncertainty}` records — the audit trail | reviewer; `report.json` builder |
| `Facts.lean` | the framework's generated axioms; also written to `Proving/<Framework>/Facts.lean` | `lake build` |
| `report.json` | full run record: predicates + kernel verdict + per-error locus (intro-rule + field). Schema in propagation spec § 2.1 | `verifying/web/`'s `/api/runs/<id>/report`; status-emit aggregator |
| `graph.json` | proof DAG (node kinds + `applies`/`composes`/`inhabits`/`disjunctionCase` edges + `failures[]`; shape = propagation spec § 2.3) | graphs kit `/proof-graph/run/<id>/` via `verifying/web/public/graphs/loader.js` |
| `loci.json` | single `DiagramEmit` rendering the kernel's intro-rule shape with verdict-coloured slots | `data/status/proving.json` `diagrams[1]` |

`report.json` joins via `kernel.errors[].axiomName` ↔ `predicates[].axiomName` so a UI can light up the failing predicate row red.

**Schema is locked at the consumer boundary.** Two live readers adapt `graph.json` (full-word `kind`, no positions, evidence arrays, string uncertainty): `verifying/web/public/graphs/loader.js` and `visualizing/graphs/src/adapters/proof.ts` `fromProof`. Any change to `graph.json` field names or `kind` values is a **two-sided edit** — bump `data/charters/proving/results-propagation/schema-of-record.md` and update BOTH readers together.

Enforcing tests: the propagation suite at **`data/specs/proving-results-propagation-2026-05-09/tests/`** plus `verifying/web/tests/e2e/proof-graph.spec.ts` and `visualizing/graphs/test/proof-conformance.test.ts`. **Never cite case numbers from this file — derive them from that `cases/` dir; this paragraph THREE TIMES pointed maintainers at ghosts** (F25). The suite **no longer mutates the tree** (mutating cases redirect via `--sandbox-out`/`QAGENTS_PENDING_ROOT`; **`git status` must be clean after a run**), so **a failure there IS yours.** Before repointing any assertion read that suite's `README.md` § "Suite health": three cases guard privacy floors and must never be satisfied by widening an allow-list.

**Sibling parity with `accounting/`.** Before any **cross-tree lockstep patch** over the proving↔accounting shared internals (`lean_parse.py`/`report.py` diff-check-not-mirror, byte-compatible `graph.json`, shared `score_bridge.py`, S3 push lanes, deliberate accounting-side divergences) → read `…/axiomatize-shared-2026-07-04/matrix.md` § 7.

**Adding a new statute / framework.** Authoring recipe (kernel quartet → `Proving.lean` wire → predicate specs → sample → `LociRoster` registration → roster update): `predicates/README.md` § "Adding a new framework — authoring contract".

## Wave-time doctrine → `.claude/skills/dau-manual/SKILL.md` § Pre-wave

Relocated 2026-08-09 (P5 proving read, ns:qagents/146): the 2026-07-14
five-defects record and its three outliving rules (an audit CERTIFIES, never
CURES; soundness ≠ blindness; re-classification loses to a fresh blind
re-slice), the gate-vs-mandate class + the FIVE wave conditions, the
roster-detectors/echo-adjudications discipline, and the the canonical USC text mirror
curated-scope corollary. Read it before ANY wave — it sits in the wave lane's
own skill, which is where every wave starts. Live wave partition stays
`remediation-roster.json`, never prose counts.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no FFI. Kernel is pure.
2. **Predicate specs MUST NOT cite or read `Proving/<Framework>/*.lean`.** Their world is the complaint text + spec rubric.
3. **The driver MUST NOT make legal judgments.** Add fields to JSON schema or a new `framework` block field rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** The `.gitignore` enumerates `Proving/<Framework>/Facts.lean` **explicitly per framework** (not globbed) — when adding a framework, add its entry, else a `--build` run commits the ephemeral copy. Only `examples/*/Facts.lean` is tracked (the verifiable proof artefact).
5. **memsearch never indexes `Proving/<Framework>/*.lean`.** Lean files excluded by design (memsearch only scans `.md`/`.markdown`).
6. **Predicates live under `predicates/<framework>/`.** Manifest spec paths use the subdirectory.
7. **Blind-fanout agreement is the ONLY correctness oracle — protect ALL THREE channels.** (a) *Filesystem:* the runtime hands every subagent the SAME writable session scratchpad (it is **not** per-cell) — all cell scratch goes under its own disjoint `<out>/.scratch/`; the session scratchpad is off-limits. This channel stays CONTRACTUAL — **RULED 2026-08-12** (terminal `op:cell-isolation-permit-ruling` cleared): per-cell worktrees are dead at THREE harness layers (`agent-<hex>` naming; `EnterWorktree` CREATE bar; `EnterWorktree` ENTER refuses session-worktree cwds), the cure is PARKED upstream-pending, and the live structural work is the decoupled act-time guard lane (structural-guards spec, studying family) — `reference_agent_worktree_isolation_blocked_in_qagents`, ns-51. (b) *Orchestrator:* stating a substantive finding in a prompt destroys blindness just as thoroughly — **name the METHOD, never the ANSWER**; adjudications go to the **reconciler**, never the cells. (c) *Shared vocabulary:* a cell may `#check` a `Common` constant it **names**; it may never **enumerate** the namespace (no roster dump, `#print prefix`, env walk, olean or source) — SPEC § 5.3 R6 reserves that vocabulary for the reconciler, and a cell that has seen the roster yields echo, not agreement. Two standing responses: **when two cells break the same rule independently, fix the WORDING first**, and a **disclosed** breach earns a cheap re-run, never a penalty that teaches concealment. **SEVEN** channels + rationale + incident record: memory `feedback_blind_fanout_oracle_channels`. Contracts: `.claude/agents/dau-{cell,reconciler}.md`, `dau-parallel-scaling-2026-07-09/PROMPTS.md` § Orchestrator blindness discipline.
8. **A green build is not proof — `autoImplicit` must stay OFF.** `lakefile.toml` sets `autoImplicit = false, relaxedAutoImplicit = false` on **both** `lean_lib`s. With it ON, an unqualified `Common` type is silently bound as a **phantom implicit type variable**: the module builds green while its axioms range over an invented type, and a **bridge between two phantom-typed composites discharges vacuously** — any Tier-A resting on it measured *nothing* (unfounded, not mis-measured). Never remove the option to make a file pass.
9. **The golden ROSTERS are barred to blind cells, and live apart so the bar cannot be violated by inattention.** `predicates/GOLDEN-ROSTERS.md` holds all nine per-framework rosters; `predicates/README.md` is the **roster-free** spec-format contract and is safe for a cell to read in full. They were one file until 2026-08-03, when all 5 cells of a wave read the golden roster **by following their contract**. Licensed readers: humans + the reconciler class. The incident, the third-column severity rationale, and why a SPLIT beats a banner: `feedback_blind_fanout_oracle_channels`. **Never re-merge the two files, and when adding any doc the cell contract will cite, check what else lands in the same file** — incorporation-by-reference imports the whole file.

## Predicate sub-agent memsearch use

A predicate sub-agent MAY invoke the `memory-recall` skill (itself `context: fork`). Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop hook auto-writes; predicate names preserved verbatim); collection is per-subproject via the patched `lib/memsearch` `common.sh`.

## Toolchain notes

- **Lean** pinned via `lean-toolchain` to **`v4.32.0`** (lockstep with `accounting/` + `studying/` per root CLAUDE.md § Lean4 axes inv-4 — ACCEPTED **and** REJECTED example proofs replayed on every axis at every bump). The sibling pins, the non-obvious replay recipe (`lake build Proving` does **not** build a framework's `Facts` olean, so every example fails with `object file … does not exist` — which looks exactly like a toolchain break and is not one), and the per-branch-lockstep deviation: memory `feedback_lean_toolchain_bump_verify_example_proofs` § "v4.32.0 bump".
- **No Mathlib dependency** — keeps `lake build` fast, and confirmed by the 2026-06-20 hierarchical-predicates debate (R4): the lift is a **gated per-axis opt-in, never global**, and proving stays Mathlib-free (no legal-doctrine lemma in Mathlib). Tactic substrate is core-only: `Proving/USC/Common/Tactic.lean` (`prove_element`; `@[doctrine]` = `@[grind →]` intro rules; `aesop` absent/struck).
- **Python ≥ 3.10** for the driver (system `python3`, no venv); **Claude CLI** on `$PATH`.
- **Claude `-p` flag set for predicate sub-agents** — today text-reasoning-only (no Bash). When predicates need external tools: derive the flag set from the live drivers (`extract_facts.py` `_run_claude`; model floor `code/lean_tools/model_floor.py`).
- **Model is top-tier, hard-enforced (not a cost choice).** Production (predicate-invoking) runs of `extract_facts.py` **hard-fail (exit 3)** on any non-top-tier model token unless `--allow-smoke-model`; `--stub`/`--reuse-facts` are exempt. Accepted set + default = the shared seat `code/lean_tools/model_floor.py` (never enumerated here); policy = root CLAUDE.md § Model policy + `feedback_predicate_model_opus_not_haiku`. `dau` USC agents carry **no frontmatter pins** — they inherit the orchestrator's model. Two driver guards (`invoke_predicate`, tested by `scripts/test_predicate_guard.py`): **A** rejects+retries a result claiming it couldn't read the complaint or carrying no evidence (NOT substantive legal negation — a legitimate False here); **B** band-normalizes uncertainty then treats `high` as a review FLAG, never an auto-reject (high is honest on a knife-edge).

**Driver smoke-test side effect.** Without `--sandbox-out`, `extract_facts.py --example-id <id>` overwrites `examples/<id>/{Facts.lean,facts,report,graph,loci}.json` and rebuilds — use **`--sandbox-out <dir>`** for ANY smoke test, cell run, or test case (`--reuse-facts` reads the committed dir regardless). The hazard was a *default*, not a gap, so the driver **fail-closes**: with `QAGENTS_PENDING_ROOT` set, a run without `--sandbox-out` exits 2. **Any test invoking the driver or an emitter MUST redirect.** `feedback_driver_overwrites_example_artifacts`.

## Open work

- **`LociRoster` gap (gated on an example run):** the USC-program `Prohibited.*` §1962 judgments have no complaint run exercising them, so a roster renders "— · not exercised" until one exists. Two flat Title VII goldens use `substantive=None` deliberately. Residual: ns-32(b). Persisting golden gotcha: the Title IX severity axiom keeps the upstream spelling `SexualHarassmentSevereePervasive` (spec filename matches).
- **`predicates/usc/common/**` stays § 5.3-firewalled** — session-authored only, never a `/dau-manual` wave surface. If a mint dangles a `Spec:` path, re-derive the roster by scanning `Proving/USC/Common/Predicates.lean` doc-comments — never from prose.
- **A roster field means its DEFINITION, not its name — twice.** (a) `clause`/`note` rows are NOT corpus-blocked: `remediation_census.py`'s `POST_FIX = "2026-07-15"` gates on ENCODING DATE, the render defects were cured 2026-07-14 with the corpus regenerated `--all` that day, and `ns:proving/142`'s regen has a **zero** intersection — re-sliceable (debate `backlog-unblock-sequencing-2026-08-11`, after this file asserted the opposite for four weeks). Derive the partition **BY ROW**: `clause` 25 + `note` 25 double-counts the 11 carrying both. (b) A row's `tiers` is the **standing coverage tier** from earlier promoted encodings, **never the wave's yield** — per-wave A/B/C lives in `coverage-history.jsonl`, and `tier_counts` is not a `WAVE.json` field. Misread as yield twice in one session (2026-08-11: a wave reported A5/B5/C1 whose row reads **A0/B11/C0**).
- **`check_olean_closure` is NOT red** — read a failure as "both libs not built" FIRST. Its verdict follows your last build, not the roots (this file asserted 16 phantom "unrooted" files on that mistake). **The same reading is owed to G7's TREE arm**, which reads constants and so reports `elaboration/resolution failed (rc 1)` for every golden's `Theorems` on an unbuilt tree — indistinguishable from a real `sorryAx` finding, and the default state of a worktree opened that morning (hit 2026-08-09; `lake build Proving ProvingUSC` cleared it, 9,245 theorems attesting clean). Any arm whose input is the BUILD reports the build's absence in the vocabulary of its own subject. **Exit 6** = precondition unmet (since 2026-08-08 that includes "no build output at all", which used to exit 2 and contradict this script's own contract); **exit 5** is the real finding. `dau.sh --promote-tail` propagates the two distinctly — flattening them is what produced those phantoms.
- **Every example is un-stubbed as of 2026-08-08** (ns-37 retired; 110 → 0). A `--stub` run stays an UNAUDITED artefact (§ Workflow caveat — it cannot fail, so it cannot detect): the un-stub caught a defendant named nowhere in its complaint. A mechanical literal cross-check for that class is **all false positives** (abbreviation/case/punctuation) — pre-flight, never a gate. `feedback_proving_stub_defaults_true`.

## Dated narratives are ARMED ephemeral lanes (since 2026-08-06)

`AUDIT-*.md` / `BATCH-*.md` / `reviews/*.md` are `ephemeral` ttl **30**;
`DOSTEPS-*.md` / `PLAN-*.md` are ttl **7** (`data/specs/do-retire-2026-07-26/lanes.tsv`,
the single source of truth — never a remembered figure). Practical consequence
for authors: **a new audit narrative lives one to four weeks on disk.** Freeze
the verdict into its wave record / `waves/<id>/audit/` / a CLAUDE.md standing
section (§ 8b discipline) and promote sole-copy evidence via
`scripts/retire-evidence-promote.sh` **before** anything relies on the
narrative; git + `archive.blob` + `waves/<id>/audit/` are the retention, the
file is not.

## Status emit (`data/status/proving.json`)

Full contract (producer, `panels[]` order, `usc-program` KpiStrip, `coverage.json` derived-invariant + gates C10/C11, `PUBLIC_EXAMPLE_IDS` synthetic-only gate, two-lane writer, cron): `project_proving_subproject__emit`.

## Redaction (`scripts/redact_complaints.py` + `scripts/redact_artefacts.py`)

**Two-stage, source-first.** `scripts/redact_complaints.py` redacts the SOURCE `examples/*/complaint.md` to the **uniform-strict / FBI-director-letter standard** (keep every `X v. Y` citation + government bodies; scrub all other personal names, private medical entities, residential addresses). A clean source means a fresh `--build` CANNOT re-leak a quote. Every example complaint; idempotent + self-auditing. Run before any fresh derivation; public court-filing PDFs are NOT a safe text source — `fitz` extracts the layer *under* graphical redaction boxes (`feedback_graphical_redaction_failure_modes`).

Predicate sub-agents quote `complaint.md` + `manifest.inputs.*` verbatim into evidence strings, which flow through `examples/<id>/*.json` + `Facts.lean` → `status_emit.py` → public status page — a **separate channel** from `documenting/scripts/check_redactions.py`, which never sees proving's JSON outputs.

`scripts/redact_artefacts.py` (downstream belt-and-suspenders): `reference_proving_redact_artefacts_script.md`.
