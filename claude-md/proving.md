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

The per-framework roster (kernel · specs · source guide · statutory text for every golden — set = `ls -d Proving/*/` minus `USC/`, never a prose count; ns-181) lives in memory `reference_proving_doctrine_pins` § "Frameworks roster", which also carries the case-law doctrine pins and the top-level inductive shapes. **Those shape names are answer-shaped and are NOT restated here** (§ Golden SHAPES below).

**Golden SHAPES live in the barred golden-roster file, never here (relocated 2026-08-19).** Composite identifiers, field counts, which composite is a bridge target, and any contested doctrinal holding are ANSWER-SHAPED, and **this file is injected into every subagent's system prompt** — so prose here reaches every blind cell with no read, and no blindness channel grades a non-read (C1-C5/C7 all grade READS). That is the 2026-08-03 roster split one channel stronger: incorporation-by-reference became injection-by-default. Keep this section free of identifiers.

**AND THE INJECTED BLOCK IS SNAPSHOTTED AT SESSION START — FIXING THIS FILE DOES NOT FIX THE RUNNING SESSION (measured 2026-08-19, ledger seq 279).** A subagent spawned minutes AFTER the identifiers were stripped still quoted them verbatim, while `grep` on disk returned 0 for every one. Two consequences, both load-bearing: **(a) a wave must never be sliced in a session that started before the leak was cured** — the cells carry the stale snapshot and the wave is void exactly as if nothing had been fixed; open a NEW session first. **(b) The cure cannot be verified from inside the session that applied it** — an in-session context probe measures the SNAPSHOT, not the file, so it reports the defect uncured and is right about the snapshot and wrong about the tree. Verify on disk with `grep` (deterministic), and confirm the context half only from a fresh session.

**A BASIS IS A PROPERTY OF THE GOLDEN TARGET'S SHAPE, NOT OF THE BRIDGE'S SUCCESS (ledger seq 257, ADOPT-SHARED).** A sorry-free zero-gap bridge onto a ONE-FIELD target still scores `golden_enumeration` — that surface tests type-compatibility with *being named* a predicate act, never an element. **Before planning any wave meant to move a basis, COUNT THE GOLDEN TARGET'S FIELDS** (recorded in the barred roster file): one field ⇒ enumeration is the ceiling, and the honest move is to fix the golden, not re-run breadth. **NECESSARY, NOT SUFFICIENT (seq 269): the section must ALSO hold Tier-A THROUGH the re-slice, because `tier_a_basis` is a Tier-A-only field** — a section can pass its GoldenBridge with zero gaps and stamp nothing, the same wave having taken it A→B; the bridge and tier verdicts live in DIFFERENT bridges and disagree in exactly that direction. **THE CLAIM IS ABOUT THE BASIS FIELD, NOT THE COUNT** (corrected 08-18): **no re-slice can RAISE an existing `golden_enumeration` row to `golden_elements`** — that ceiling is the golden target's shape (seq 257) and raising it is golden AUTHORING, never breadth. But a roster row carrying NO basis CAN earn `golden_enumeration` on a re-slice. **Derive every split from `tier_totals`, never from a remembered population.** **AND A GOLDEN AUTHORED FOR A BASIS DOES NOT DELIVER ONE (2026-08-19, seq 278):** authoring makes `golden_elements` REACHABLE; only a BLIND re-slice can stamp it, and if the authoring wrote the shape into an injected file the very next wave is void — fix the file, COMMIT it, open a NEW session, verify BOTH objects, then slice — DELIVERED 2026-08-20 (seq 280), `A_golden_elements` 12→14.

The operative statutory text lives under `legal/uscode/`, never pasted into specs. Predicate sub-agents resolve a `usc_cite` via `scripts/uscode.py path|text|list` — index→corpus fallback + subsection normalization (L-029), so an arbitrary in-Code cite resolves without extending the curated `index.json` (`uscode.py lint` reports cite resolvability). **Cite-resolution hazards (bare-section ambiguity, the `NoteSlotError` note-slot refusal, the `corpus_render_census.py` oracle) → `predicates/README.md` § "Authoritative statutory text"** — read before authoring or debugging any cite resolution; live roster: `feedback_derived_corpus_is_unguarded_oracle`.

These hand-built frameworks are the **golden reference** — automated encodings are scored against them. The per-framework golden ROSTERS live in a separate file **barred to blind cells** (Hard rule 9); derivation + gap + mechanism detail: `reference_proving_doctrine_pins`.

## Axiomatizing the full U.S. Code (program)

Spec: `data/charters/proving/specs/axiomatize-uscode-2026-05-29/SPEC.md`. Extends the hand-built frameworks to a phased, title-by-title program over every non-appendix title (denominator = `categorization.json` `title_count` less appendices, ruled 08-18 § I(a); never a prose count), produced redundantly by top-tier-model subagent teams along **10 orthogonal axes** (5 core always fanned out + 5 opt-in via `--axes`; roster = spec § 6.1, single owner), then reconciled. Cross-strategy agreement — `Bridge.lean` implications discharged under DECLARED correspondence axioms (the kernel checks the discharge, never the axioms) — is the correctness signal (no other oracle exists).

- **Ground truth:** full USC markdown at the canonical USC text mirror (gitignored, ~65.7k sections, `tools/corpus_build.py --all`) + the canonical USC text mirror. `corpus/` + `xml/` are symlinked into every worktree via the canonical USC text mirror.
- **Naming / Lean-shapes / predicate-shapes** frozen in spec §§ 3–5 (authoring contract: `predicates/README.md` § "USC-program authoring contract"); per-(title,axis) namespace `Proving.USC.T<NN>.<Axis>`; shared cross-title predicates collapse to `Proving.USC.Common` (guarded by an equivalence Bridge). Code: `Proving/USC/Common/` + `predicates/usc/_axes/<axis>.md` (10 axis briefings) + the `ProvingUSC` lean_lib.
- **§ 1962(c) calibration anchor (hand-built, kernel-green):** all 6 axes under `Proving/USC/T18/<Axis>/` + `Bridge.lean` + `Reconciled/T18.lean` (`Bridge.s1962c_tierA` = spec § 8.3 Tier-A). The template cell-agents mirror and the fan-out's scoring reference.
- **Calibration metric is BRIDGE-BASED.** Agreement-vs-golden is measured by **golden-bridges** (`Proving/USC/T{18,42}/GoldenBridge.lean`): the blind cell's composite implies the golden composite under declared correspondence axioms, sorry-free in the kernel (mechanics + tier ladder: spec §§ 4.6/8/9.4). Score ONLY via the shared G2 guard `code/lean_tools/score_bridge.py --lexicon agreement --root proving` (no `sorryAx`; tier from the `_modulo_gaps` suffix; omitted golden elements as named `gap_*` hypotheses). `scripts/calibrate_golden.py` = hand-built name-matched cells ONLY (exact-string is unwinnable for blind agents).
- **Lane:** manual-interactive via the **`/dau-manual`** skill (`.claude/skills/dau-manual/`; mirrors `/dco-manual`) — the SDK batch lane is paused (root CLAUDE.md § Agent SDK lane). Mechanics, targeting gate, re-earn backlog, wave archive/backup: spec § 7.5 + § 10.1 + the SKILL; tests `data/charters/proving/specs/axiomatize-uscode-2026-05-29/tests/`.
- **Wave-planning authority is the UNION of every seat's archives.** `proving/waves/` is gitignored canonical-only, mirrored **per source host**, so it is a PARTIAL view on every workstation and `remediation_census.py` reads a wave this seat cannot see as backlog. **The pre-wave peer-sync + census procedure and the `proving:axiom-state` sentinel read (operational half moved there 2026-08-27, S-4), plus backlog direction + the blindness-classifier rules → `.claude/skills/dau-manual/SKILL.md` § Pre-wave** — read the per-reason partition, the stale-exemption record, the slice-width lesson, and the `--contract-file` grading rule there BEFORE any roster regen, re-slice decision, or classifier edit. Normative: spec § 10.1; measurements + never-merge rationale: `feedback_per_host_ground_truth_is_a_partial_view`.
- **Wave backup: LAN-primary, never wave-blocking** — operator ruling L-122 (`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/LEARNINGS.md` row L-122); wave-end mechanics, queue-non-debt, verify verbs + verdict ladder: spec § 10.1 (→ artifact-archive spec § 2).
- **Status · authoritative build + olean-closure gates · G3b · the hierarchical oracle-guard exit ladder → `proving/gates.md`** (moved verbatim, spread 2026-08-27 S-1). Orchestrator read — open it before promoting a wave, running the authoritative build, diagnosing a `score_bridge.py` exit (4/6/7), or reading a G3b refusal (exit 8); a blind cell's brief never names it.
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

4. **Verify**: `lake build Proving ProvingUSC` — bare `lake build` is red-by-design (`proving/gates.md`). Elaborate one example via `lake env lean examples/<id>/proof.lean` once Facts.lean exists.

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

**Sibling parity with `accounting/`.** Before any **cross-tree lockstep patch** over the proving↔accounting shared internals (`report.py` diff-check-not-mirror; `lean_parse.py` + `provenance_lint.py` are thin shims over shared `code/lean_tools/` since 2026-08-15 — patch the shared module; byte-compatible `graph.json`, shared `score_bridge.py`, S3 push lanes, deliberate accounting-side divergences) → read `…/axiomatize-shared-2026-07-04/matrix.md` § 7.

**Adding a new statute / framework.** Authoring recipe (kernel quartet → `Proving.lean` wire → predicate specs → sample → `LociRoster` registration → roster update): `predicates/README.md` § "Adding a new framework — authoring contract".

## Wave-time doctrine → `.claude/skills/dau-manual/SKILL.md` § Pre-wave

Relocated 2026-08-09 (ns:qagents/146). Read it before ANY wave (pre-spawn
arms incl. the ruling-carry detector, the 08-21 manifest shape, the D6 probe
lane). Live wave partition stays `remediation-roster.json`, never prose counts.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no FFI. Kernel is pure.
2. **Predicate specs MUST NOT cite or read `Proving/<Framework>/*.lean`.** Their world is the complaint text + spec rubric.
3. **The driver MUST NOT make legal judgments.** Add fields to JSON schema or a new `framework` block field rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** The `.gitignore` enumerates `Proving/<Framework>/Facts.lean` **explicitly per framework** (not globbed) — when adding a framework, add its entry, else a `--build` run commits the ephemeral copy. Only `examples/*/Facts.lean` is tracked (the verifiable proof artefact).
5. **memsearch never indexes `Proving/<Framework>/*.lean`.** Lean files excluded by design (memsearch only scans `.md`/`.markdown`).
6. **Predicates live under `predicates/<framework>/`.** Manifest spec paths use the subdirectory.
7. **Blind-fanout agreement is the ONLY correctness oracle — protect ALL THREE channels.** (a) *Filesystem:* the runtime hands every subagent the SAME writable session scratchpad (it is **not** per-cell) — all cell scratch goes under its own disjoint `<out>/.scratch/`; the session scratchpad is off-limits. This channel stays CONTRACTUAL — **RULED 2026-08-12** (terminal `op:cell-isolation-permit-ruling` cleared): per-cell worktrees are dead at THREE harness layers (`agent-<hex>` naming; `EnterWorktree` CREATE bar; `EnterWorktree` ENTER refuses session-worktree cwds), the cure is PARKED upstream-pending, and the decoupled act-time guard lane LANDED in full (C1+C4 arms 2026-08-12, C5-enum+C7 2026-08-14 — R2-when-armed, matrix § 2c; SKILL Step 3 arms it, `--reconcile` for the licensed phase) — `reference_agent_worktree_isolation_blocked_in_qagents`, ns-51. (b) *Orchestrator:* stating a substantive finding in a prompt destroys blindness just as thoroughly — **name the METHOD, never the ANSWER**; adjudications go to the **reconciler**, never the cells. (c) *Shared vocabulary:* a cell may `#check` a `Common` constant it **names**; it may never **enumerate** the namespace (no roster dump, `#print prefix`, env walk, olean or source) — SPEC § 5.3 R6 reserves that vocabulary for the reconciler, and a cell that has seen the roster yields echo, not agreement. Two standing responses: **when two cells break the same rule independently, fix the WORDING first**, and a **disclosed** breach earns a cheap re-run, never a penalty that teaches concealment. **SEVEN** channels + rationale + incident record: memory `feedback_blind_fanout_oracle_channels`. Contracts: `.claude/agents/dau-{cell,reconciler}.md`, `dau-parallel-scaling-2026-07-09/PROMPTS.md` § Orchestrator blindness discipline.
8. **A green build is not proof — `autoImplicit` must stay OFF.** `lakefile.toml` sets `autoImplicit = false, relaxedAutoImplicit = false` on **both** `lean_lib`s. With it ON, an unqualified `Common` type is silently bound as a **phantom implicit type variable**: the module builds green while its axioms range over an invented type, and a **bridge between two phantom-typed composites discharges vacuously** — any Tier-A resting on it measured *nothing* (unfounded, not mis-measured). Never remove the option to make a file pass.
9. **The golden ROSTERS are barred to blind cells, and live apart so the bar cannot be violated by inattention.** A single barred file holds every per-framework roster; the separate spec-format contract is **roster-free** and safe for a cell to read in full. They were one file until 2026-08-03, when all 5 cells of a wave read the golden roster **by following their contract**. Licensed readers: humans + the reconciler class. The incident, the third-column severity rationale, and why a SPLIT beats a banner: `feedback_blind_fanout_oracle_channels`. **Never re-merge the two files, and when adding any doc the cell contract will cite, check what else lands in the same file** — incorporation-by-reference imports the whole file.

## Predicate sub-agent memsearch use

A predicate sub-agent MAY invoke the `memory-recall` skill (itself `context: fork`). Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop hook auto-writes; predicate names preserved verbatim); collection is per-subproject via the patched `lib/memsearch` `common.sh`.

## Toolchain notes

- **Lean** pinned via `lean-toolchain` — **read the pin from that FILE, never from prose (this bullet included, which is why it names no version).** Lockstep with `accounting/` + `studying/` per root CLAUDE.md § Lean4 axes inv-4. Sibling pins, the replay recipe (ACCEPTED **and** REJECTED proofs on every axis at every bump; a generated-`Facts`-olean trap mimics a toolchain break), the per-branch deviation: `feedback_lean_toolchain_bump_verify_example_proofs`.
- **No Mathlib dependency; core-only tactic substrate** at `Proving/USC/Common/Tactic.lean` (`prove_element`; `@[doctrine]` = `@[grind →]` intro rules; `aesop` struck). A lift is a **gated per-axis opt-in, never global**; rulings R4/R7 + rationale: `…/hierarchical-predicates-2026-06-20/SPEC.md` § 13.
- **Python ≥ 3.10** for the driver (system `python3`, no venv); **Claude CLI** on `$PATH`. Predicate sub-agents are text-reasoning-only today; derive the live `-p` flag set from `extract_facts.py` `_run_claude`, never from prose.
- **Model is top-tier, hard-enforced (not a cost choice).** Production (predicate-invoking) runs of `extract_facts.py` **hard-fail (exit 3)** on any non-top-tier token unless `--allow-smoke-model`; `--stub`/`--reuse-facts` are exempt. Accepted set + default = the shared seat `code/lean_tools/model_floor.py`, **never enumerated here**; `dau` USC agents carry no frontmatter pins (they inherit the orchestrator's). Policy: root CLAUDE.md § Model policy. The two `invoke_predicate` guards (**A** genuineness, **B** uncertainty band-then-FLAG), their domain-specific shape, and why blind-copying accounting's misfires: `feedback_predicate_model_opus_not_haiku`; pinned by `scripts/test_predicate_guard.py`.

**Driver smoke-test side effect.** Without `--sandbox-out`, `extract_facts.py --example-id <id>` overwrites the committed `examples/<id>/` artefacts (§ Per-run artefacts) — use **`--sandbox-out <dir>`** for ANY smoke test, cell run, or test case (`--reuse-facts` reads the committed dir regardless). The driver **fail-closes**: with `QAGENTS_PENDING_ROOT` set, a run without `--sandbox-out` exits 2. **Any test invoking the driver or an emitter MUST redirect.** `feedback_driver_overwrites_example_artifacts`.

## Open work

- **`LociRoster` gap (gated on an example run):** the USC-program `Prohibited.*` §1962 judgments have no complaint run exercising them, so a roster renders "— · not exercised" until one exists. Two flat Title VII goldens use `substantive=None` deliberately. Residual: ns-32(b). Persisting golden gotcha: one Title IX severity axiom keeps an upstream MISSPELLING, and its spec filename matches it — the exact token is answer-shaped and is recorded only in the barred roster file, deliberately not restated here.
- **`predicates/usc/common/**` stays § 5.3-firewalled** — session-authored only, never a `/dau-manual` wave surface. If a mint dangles a `Spec:` path, re-derive the roster by scanning `Proving/USC/Common/Predicates.lean` doc-comments — never from prose.
- **Open-work reading rules (roster-field definitions · `check_olean_closure` polarity) → `.claude/skills/dau-manual/SKILL.md` § Pre-wave**; the exit-code semantics are demoted into `code/lean_tools/attest_axioms.py`'s own header — read them where the tool speaks.
- **No example is stub-built** (ns-37 retired) — an invariant to re-derive, not a date to trust, since any new example can falsify it silently. Why a `--stub` artefact stays UNAUDITED: § Workflow caveat + `feedback_proving_stub_defaults_true`.

## Dated narratives are ARMED ephemeral lanes (since 2026-08-06)

`AUDIT-*.md` / `BATCH-*.md` / `reviews/*.md` / `DOSTEPS-*.md` / `PLAN-*.md` are
reaped on the ttls in `data/specs/do-retire-2026-07-26/lanes.tsv` (the single
source of truth — never a remembered figure). Practical consequence for
authors: **a new audit narrative lives one to four weeks on disk.** Freeze
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
