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

The operative statutory text lives under `legal/uscode/`, never pasted into specs. Predicate sub-agents resolve a `usc_cite` via `scripts/uscode.py path|text|list` — index→corpus fallback + subsection normalization (L-029), so an arbitrary in-Code cite resolves without extending the curated `index.json` (`uscode.py lint` reports cite resolvability). See `predicates/README.md` § "Authoritative statutory text". **A bare section number is NOT unique within a title** — Title 42 has five files named `205.md`, Title 18 five named `2.md` — and `usc_cite` cannot discriminate them (every duplicate carries the same one). `identifier` can: a real section has one, a note heading rendered as a section file has it EMPTY. The resolver prefers non-empty-`identifier` candidates and **fails loud** on >1 survivor rather than taking `sorted(glob)[0]`, which had `42 USC § 209` answering `ch50`'s flood-insurance note instead of the PHS section in `ch6A` (2026-07-29, `7f51b3aee`; 11 coverage cites were resolving to a phantom, 4 of them Tier-A). Those 11 owe a blind re-slice — a resolver fix cannot retroactively make a past agreement mean anything, and they are NOT in `remediation-roster.json`, which partitions by wave class rather than corpus defect.

These hand-built frameworks are the **golden reference** — automated encodings are scored against them. Per-golden derivation + gap + mechanism detail: `predicates/README.md` + close summaries + memory `reference_proving_doctrine_pins`.

## Axiomatizing the full U.S. Code (program)

Spec: `data/charters/proving/specs/axiomatize-uscode-2026-05-29/SPEC.md`. Extends the hand-built frameworks to a phased, title-by-title program over all 54 titles, produced redundantly by top-tier-model subagent teams along **10 orthogonal axes** (5 core always fanned out + 5 opt-in via `--axes`; roster = spec § 6.1, single owner), then reconciled. Cross-strategy agreement, proved in the kernel via `Bridge.lean` lemmas, is the correctness signal for the LLM→Lean mapping (no other oracle exists).

- **Ground truth:** full USC markdown at the canonical USC text mirror (gitignored, ~65.7k sections, `tools/corpus_build.py --all`) + the canonical USC text mirror. `corpus/` + `xml/` are symlinked into every worktree via the canonical USC text mirror.
- **Naming / Lean-shapes / predicate-shapes** frozen in spec §§ 3–5 (authoring contract in `predicates/README.md` § "USC-program authoring contract"); per-(title,axis) namespace `Proving.USC.T<NN>.<Axis>`; shared cross-title predicates collapse to `Proving.USC.Common` (guarded by an equivalence Bridge). Code: `Proving/USC/Common/` + `predicates/usc/_axes/<axis>.md` (the 10 axis briefings) + the `ProvingUSC` lean_lib.
- **§ 1962(c) calibration anchor (hand-built, kernel-green):** all 6 axes under `Proving/USC/T18/<Axis>/` + `Bridge.lean` + `Reconciled/T18.lean` (`Bridge.s1962c_tierA` = spec § 8.3 Tier-A). The template cell-agents mirror and the fan-out's scoring reference.
- **Calibration metric is BRIDGE-BASED.** Agreement-vs-golden is measured by kernel-checked **golden-bridges** (`Proving/USC/T{18,42}/GoldenBridge.lean`): the blind cell's composite implies the golden composite under declared correspondence axioms, sorry-free (mechanics + tier ladder: spec §§ 4.6/8/9.4). Score ONLY via the shared cross-axis G2 oracle guard `code/lean_tools/score_bridge.py --lexicon agreement --root proving` — never a local copy; invoked through `dau.sh --score` + `dau-{reconciler,cross}.md`, certifies no `sorryAx`, reads the tier from a `_modulo_gaps` theorem-name suffix, and Tier-B/C gaps surface the omitted golden element as a named `gap_*` hypothesis. `scripts/calibrate_golden.py` is a regression check for hand-built name-matched cells ONLY — exact-string is unwinnable for blind agents.
- **Lane:** manual-interactive via the **`/dau-manual`** skill (`.claude/skills/dau-manual/`; mirrors `/dco-manual`) — the SDK batch lane is paused (root CLAUDE.md § Agent SDK lane). Mechanics, targeting gate, re-earn backlog, wave archive/backup: spec § 7.5 + § 10.1 + the SKILL; tests `data/charters/proving/specs/axiomatize-uscode-2026-05-29/tests/`.
- **Wave backup: LAN-primary, never wave-blocking** — operator ruling L-122 (`data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/LEARNINGS.md` row L-122); wave-end mechanics, queue-non-debt, verify verbs + verdict ladder: spec § 10.1 (→ artifact-archive spec § 2).
- **Status:** Phases 0–1 done; Phase 2 calibration anchor + waves promoted to canonical (approach-B `Proving.USC.<Title>.*` sub-namespaces; cross-title Common-collapse; corpus rollup `proving/coverage.json`). Phases 3–4 (SDK-funded bulk scaling) are **paused, not cancelled** (root CLAUDE.md § Agent SDK lane). **Per-wave detail + remaining-section roster + current state live in spec § 10.1 + the close summaries — never duplicated here.** Two load-bearing invariants: cell Lean files MUST use FULL-path imports (`reference_lean_isolation_probe_full_path_imports`); authoritative build target is **`lake build Proving ProvingUSC`** — BOTH libs (bare `lake build` is red-by-design on REJECTED examples; `ProvingUSC` alone excludes every hand-built golden's `Theorems.lean`) — run it before promoting, never trust a cell's self-reported build. **Pair it with `scripts/check_olean_closure.py`: a green build says nothing about a file no root reaches** — root a new subtree's `Theorems` explicitly, since bridges import `.Statute`, not `.Theorems` (`feedback_unrooted_lean_file_is_never_elaborated`).
- **Hierarchical-predicate depth layer (H0–H4 landed).** Flat opaque predicates decompose into LLM-decided leaf predicates + kernel-derived composites, over a three-tier model stratification. **Oracle guard (load-bearing):** search automation (`grind`/`aesop`) NEVER discharges a `Bridge`/`GoldenBridge` agreement lemma — `score_bridge.py`'s `reject_automation_in_bridge` enforces it syntactically (**exit 4**, ahead of `sorryAx`). Full depth-layer detail (tiers, leaves/derivation/tactic, bake-off gate, debates, H1 cell): `data/charters/proving/specs/axiomatize-uscode-2026-05-29/hierarchical-predicates-2026-06-20/SPEC.md` §§ 13/13.1; status of record `../studying/representation.md` § 13.4.
- **Graph projections (Half-A domain graph).** `scripts/uscode_graph.py --cite-graph` emits the **`qgraph-wire/1` node-link envelope** (deterministic Axis-5 §-citation graph, `graph.axis=textual`), consumed by BOTH the graphs kit's `fromNodeLink` reader AND `qagents.lean_graph`'s `anchor()` |D| join. Flags, gitignored `proving/graphs/`, tests: `data/charters/proving/specs/axiomatize-uscode-2026-05-29/graph-projections-2026-06-14/SPEC.md` § 4.2.

## Layout (essentials)

`Proving.lean` (root module, imports both frameworks) · `lakefile.toml` · `lean-toolchain` (pinned — § Toolchain notes) · `Proving/<Framework>/{Types,Predicates,Statute,Theorems}.lean` (+ generated, gitignored `Facts.lean`) · `predicates/<framework>/` (one markdown spec per opaque predicate) · `examples/<id>/` (per-run artefacts, below). `scripts/`: `extract_facts.py` (driver) · `lake_trace.py` (two error-line orderings, 4.29 vs 4.30+) · `lean_parse.py` (regex proof-file structural parser) · `uscode.py` (path/text/list lookup) · `uscode_graph.py` (Axis-5 §-citation graph).

## Workflow

1. **Author the formal framework** (Lean) — for a new framework, add `Proving/<NewFramework>/{Types,Predicates,Statute,Theorems}.lean` and import from `Proving.lean`.
2. **Author predicate specs** under `predicates/<newframework>/`. Spec format is fixed (see `predicates/README.md`).
3. **Run the driver**:
   ```
   python3 scripts/extract_facts.py examples/<id>/complaint.md \
           --manifest examples/<id>/manifest.json --example-id <id> [--build]
   ```
   The manifest's `framework` block selects where Facts.lean is written, the namespace prefix, and the `proof_target` lake target. `--build` emits `report.json` + `graph.json` + `loci.json` per `data/specs/proving-results-propagation-2026-05-09/SPEC.md`. `--reuse-facts --example-id <id>` skips the predicate sub-agents and re-emits from the existing `facts.json`.

4. **Verify**: `lake build Proving ProvingUSC` — bare `lake build` is red-by-design (§ Status). Elaborate one example via `lake env lean examples/<id>/proof.lean` once Facts.lean exists.

The driver prints one `· <spec> ... <value>  (<uncertainty>)` line per predicate in **all three modes** (`--stub`/`--reuse-facts`/production); adapters (`verifying/server/adapters/proving.py._classify`) rely on that shape being identical across modes.

**`--stub` caveat for REJECTED examples.** `--stub` defaults every predicate to `True`, so it would overwrite committed REJECTED reports with synthetic ACCEPTED and (never reading `manifest.inputs.*`) conceal a manifest drifted from its complaint. **Guard-enforced** (L-030): a committed (non-`--sandbox-out`) `--stub` run against a `REJECTED` example **refuses** (exit 2) unless `--force-stub` — use `--reuse-facts` for any replay over a REJECTED run. Timeouts/mid-run failures preserve paid work (retry + `facts.partial.json` flush). Tested by `scripts/test_driver_hardening.py`; mechanics: `feedback_proving_stub_defaults_true`.

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

**Schema is locked at the consumer boundary.** Two live readers adapt `graph.json` (full-word `kind`, no positions, evidence arrays, string uncertainty): `verifying/web/public/graphs/loader.js` and `visualizing/graphs/src/adapters/proof.ts` `fromProof`. Any change to `graph.json` field names or `kind` values is a **two-sided edit** — bump `data/specs/proving-results-propagation-2026-05-09/SPEC.md` § 2.3 and update BOTH readers together.

Enforcing tests: the propagation suite under `tests/cases/` plus `verifying/web/tests/e2e/proof-graph.spec.ts` and `visualizing/graphs/test/proof-conformance.test.ts`. **Never cite case numbers from this file — derive them from `tests/cases/`; this paragraph twice pointed maintainers at ghosts** (F25). The suite **no longer mutates the tree** (mutating cases redirect via `--sandbox-out`/`QAGENTS_PENDING_ROOT`; **`git status` must be clean after a run**), so **a failure there IS yours.** Before repointing any assertion read `tests/README.md` § "Suite health": three cases guard privacy floors and must never be satisfied by widening an allow-list.

**Sibling parity with `accounting/`.** Before any **cross-tree lockstep patch** over the proving↔accounting shared internals (`lean_parse.py`/`report.py` diff-check-not-mirror, byte-compatible `graph.json`, shared `score_bridge.py`, S3 push lanes, deliberate accounting-side divergences) → read `data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-shared-2026-07-04/matrix.md` § 7.

**Adding a new statute / framework.** Authoring recipe (kernel quartet → `Proving.lean` wire → predicate specs → sample → `LociRoster` registration → roster update): `predicates/README.md` § "Adding a new framework — authoring contract".

## The gates that silently didn't hold (2026-07-14 — read before any wave)

Five defects each passed a gate while meaning nothing (all closed). Recurring shape: **a gate you don't verify against an independent source is not a gate.** Operative rules = Hard rules 7–8 below (orchestrator-as-blindness-channel = 7b, orthogonality-by-construction = 7a); per-defect mechanics in the memories — `feedback_derived_corpus_is_unguarded_oracle` (only an XML-vs-render census is an oracle; re-earn = next-steps 41) · `feedback_autoimplicit_phantom_types` (incl. `lake clean` after flipping any compiler option) · `reference_lean_isolation_probe_full_path_imports` (the probe must be a CLEAN ROOM; never accept a cell's self-reported `lake_build=ok`).

Three rules outlive the incident: **an audit CERTIFIES, it never CURES** (a certified-blind wave still owes its corpus-defect/phantom re-earn — ns-41's `sections_re_earned` gate); **soundness and blindness are separate properties**; and a re-classification of an aged-off encoding LOSES to a fresh blind re-slice of that cite (§ 1981, 2026-07-23). Live wave partition is `remediation-roster.json`, never prose counts (`AUDIT-ns54-transcript-2026-07-16.md`).

**The re-slice class is RUNG-AWARE — do not read a `review` as a finding about your wave (2026-07-29, `3a3186af6`).** A compliant cell *cannot* score `clean`: the L-138 mandated `cp .../Common/{Types,Predicates,Tactic}.olean` always raises C5 rung (i), so every wave verdict floors at `review`. While `review` was unconditionally in `NEEDS_RESLICE_CLASSES`, every section a re-earn wave REPAIRED went straight back onto the roster — measured on `2026-07-28-l1-t18-ch1-reearn`, whose § 20 had just *earned* Tier-A on the re-slice that re-owed it. `review_mandated` now splits it, and the split reads the audit EVIDENCE, never a claim: the cert must state `review_channels ⊆ {C5}` **and** `c5_rungs ⊆ {names,types}` **and** no `breach_channels`. **Absent evidence reads as substantive** — so a Step-6.5 cert that omits those fields silently costs its wave a re-slice it did not earn. Emit them (`dau-manual/SKILL.md` Step 6.5). Conservative direction is deliberate: cost a re-slice, never certify one.

**But grade the INSTRUMENT before the wave (2026-07-31, ledger 174).** `transcript_audit.py --agent-out` takes the transcript **file stem** (`agent-<id>`); a bare agent id is silently ignored, `own_out` binds `null` for every agent, and the run emits a fully plausible wave-level **`breach`** — each cell's own `<out>` scored as a sibling-artifact path, a `--licensed-agent` reconciler's canonical reads convicted C3+C5 `roster`. The tell is `own_out: null` in the JSON; re-run with stems. This is the one case the "freeze the verdict BEFORE acting on the exit code" rule does not cover: it guards against *losing* an adverse verdict, not against a *fabricated* one, so a frozen-and-obeyed false breach obliges sections that just earned Tier-A into a re-slice. Retain both runs and name the cause — supersede in the open, never overwrite.

**Corollary for the canonical USC text mirror:** it is a **curated scope, not a mirror** — a full `uslm_to_md.py --title N --chapter C` regen of a partially-curated chapter *expands* it (83 spurious files, once). Use `--section`.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no FFI. Kernel is pure.
2. **Predicate specs MUST NOT cite or read `Proving/<Framework>/*.lean`.** Their world is the complaint text + spec rubric.
3. **The driver MUST NOT make legal judgments.** Add fields to JSON schema or a new `framework` block field rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** The `.gitignore` enumerates `Proving/<Framework>/Facts.lean` **explicitly per framework** (not globbed) — when adding a framework, add its entry, else a `--build` run commits the ephemeral copy. Only `examples/*/Facts.lean` is tracked (the verifiable proof artefact).
5. **memsearch never indexes `Proving/<Framework>/*.lean`.** Lean files excluded by design (memsearch only scans `.md`/`.markdown`).
6. **Predicates live under `predicates/<framework>/`.** Manifest spec paths use the subdirectory.
7. **Blind-fanout agreement is the ONLY correctness oracle — protect ALL THREE channels.** (a) *Filesystem:* the runtime hands every subagent the SAME writable session scratchpad (it is **not** per-cell) — all cell scratch goes under its own disjoint `<out>/.scratch/`; the session scratchpad is off-limits. (b) *Orchestrator:* stating a substantive finding in a prompt destroys blindness just as thoroughly — **name the METHOD, never the ANSWER**; adjudications go to the **reconciler**, never the cells. (c) *Shared vocabulary:* a cell may `#check` a `Common` constant it **names**; it may never **enumerate** the namespace (no roster dump, `#print prefix`, env walk, olean or source) — SPEC § 5.3 R6 reserves that vocabulary for the reconciler, and a cell that has seen the roster yields echo, not agreement. An oracle bug is worse than an input bug because it is **invisible in the output**. Two standing responses: **when two cells break the same rule independently, fix the WORDING first**, and a **disclosed** breach earns a cheap re-run, never a penalty that teaches concealment — void artifacts are **quarantined into the wave archive, never deleted**. Six channels + incident record: memory `feedback_blind_fanout_oracle_channels`. Contracts: `.claude/agents/dau-{cell,reconciler}.md`, `dau-parallel-scaling-2026-07-09/PROMPTS.md` § Orchestrator blindness discipline.
8. **A green build is not proof — `autoImplicit` must stay OFF.** `lakefile.toml` sets `autoImplicit = false, relaxedAutoImplicit = false` on **both** `lean_lib`s. With it ON, an unqualified `Common` type is silently bound as a **phantom implicit type variable**: the module builds green while its axioms range over an invented type, and a **bridge between two phantom-typed composites discharges vacuously** — any Tier-A resting on it measured *nothing* (unfounded, not mis-measured). Never remove the option to make a file pass.

## Predicate sub-agent memsearch use

A predicate sub-agent MAY invoke the `memory-recall` skill (itself `context: fork`). Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop hook auto-writes; predicate names preserved verbatim); collection is per-subproject via the patched `lib/memsearch` `common.sh`.

## Toolchain notes

- **Lean** pinned via `lean-toolchain` to **`v4.32.0`** (bumped 2026-07-14; lockstep with `accounting/` + `studying/` per root CLAUDE.md § Lean4 axes inv-4 — ACCEPTED **and** REJECTED example proofs replayed on every axis at every bump). `studying` carries **two** pins; `accounting/dev-mathlib` stays at v4.30.0 (separate mathlib experiment, not one of the three kernels). The charter's "one commit" lockstep is impossible under per-subproject locks — it lands one commit per branch, lockstep in time, each verified separately.
  - **Replay recipe (non-obvious).** `lake build Proving` does **not** build a framework's `Facts` olean — `Facts.lean` is generated and sits outside the lib's import closure. Stage the tracked `examples/<id>/Facts.lean` to the manifest's `framework.facts_path`, `lake build <Framework>.Facts` **explicitly**, then `lake env lean examples/<id>/proof.lean`. Skip the explicit module build and every example fails with `object file … does not exist`, which looks exactly like a toolchain break and is not one.
- **No Mathlib dependency** — keeps `lake build` fast, and confirmed by the 2026-06-20 hierarchical-predicates debate (R4): the lift is a **gated per-axis opt-in, never global**, and proving stays Mathlib-free (no legal-doctrine lemma in Mathlib). Tactic substrate is core-only: `Proving/USC/Common/Tactic.lean` (`prove_element`; `@[doctrine]` = `@[grind →]` intro rules; `aesop` absent/struck).
- **Python ≥ 3.10** for the driver (system `python3`, no venv).
- **Claude CLI** must be on `$PATH`.
- **Claude `-p` flag set for predicate sub-agents** — today text-reasoning-only (no Bash). When predicates need external tools: `feedback_claude_p_subagent_real_call_pattern`.
- **Model is top-tier, hard-enforced (not a cost choice).** Production (predicate-invoking) runs of `extract_facts.py` **hard-fail (exit 3)** on any non-top-tier model token unless `--allow-smoke-model`; `--stub`/`--reuse-facts` are exempt. Accepted set + default = the shared seat `code/lean_tools/model_floor.py` (never enumerated here); policy + bake-off record = root CLAUDE.md § Model policy + `feedback_predicate_model_opus_not_haiku`. `dau` USC agents carry **no frontmatter pins** — they inherit the orchestrator's model. The driver carries two guards (`invoke_predicate`, tested by `scripts/test_predicate_guard.py`): **Guard A** rejects+retries a result that claims it couldn't read the complaint or carries no evidence (NOT substantive legal negation — that's a legitimate False here); **Guard B** band-normalizes uncertainty then treats `high` as a review FLAG, never an auto-reject (high is honest on a real knife-edge).

**Driver smoke-test side effect.** Without `--sandbox-out`, `extract_facts.py --example-id <id>` overwrites `examples/<id>/{Facts.lean,facts,report,graph,loci}.json` and rebuilds — use **`--sandbox-out <dir>`** for ANY smoke test, cell run, or test case; `--reuse-facts` reads the committed dir regardless. The hazard was a *default*, not a gap, so the driver **fail-closes**: with `QAGENTS_PENDING_ROOT` set a run without `--sandbox-out` exits 2. **Any test that invokes the driver or an emitter MUST redirect.** Detail: `feedback_driver_overwrites_example_artifacts`.

## Open work

- **`LociRoster` gap (gated on an example run):** the USC-program `Prohibited.*` §1962 judgments have no complaint run exercising them, so a roster renders "— · not exercised" until one exists. Two flat Title VII goldens use `substantive=None` deliberately. Residual: next-steps 32(b).
- Persisting golden gotchas: the Title IX harassment-severity axiom keeps the upstream spelling `SexualHarassmentSevereePervasive` (spec filename matches).
- **Canonical `Common` axioms citing absent spec paths — the five heavy ones are AUTHORED (2026-07-30); six low-consumption paths still dangle** (next-steps 77 — **not fixable from a breadth lane**; `predicates/usc/common/**` is § 5.3-firewalled). Re-derive the roster by scanning `Proving/USC/Common/Predicates.lean` doc-comments for `Spec:` paths — never read it here.
- **`check_olean_closure` is NOT red** — read a failure as "both libs not built" FIRST. Its verdict follows your last build, not the roots (this file asserted 16 phantom "unrooted" files on that mistake until 2026-07-27). **Exit 6** = precondition unmet, names the un-built lib; **exit 5** is the real finding.
- **Stub-built fixtures are UNAUDITED fixtures.** The two PUBLIC examples were un-stubbed + kernel-verified 2026-07-10; the rest are 100% `uncertainty: "stubbed"` (canned `True`, empty evidence) — **never cite one as ground truth.** Live roster + un-stub plan: next-steps item 37.

## Status emit (`data/status/proving.json`)

Full status-emit contract (producer, `panels[]` order, `usc-program` KpiStrip, `coverage.json` derived-invariant + gates C10/C11, `PUBLIC_EXAMPLE_IDS` synthetic-only gate, two-lane writer, cron) lives in memory `project_proving_subproject__emit`.

## Redaction (`scripts/redact_complaints.py` + `scripts/redact_artefacts.py`)

**Two-stage, source-first.** `scripts/redact_complaints.py` redacts the SOURCE `examples/*/complaint.md` to the **uniform-strict / FBI-director-letter standard** (keep every `X v. Y` citation + government bodies; scrub all other personal names, private medical entities, residential addresses). A clean source means a fresh `--build` CANNOT re-leak a quote. Covers every example complaint; idempotent + **self-auditing**. Run before any fresh derivation; public court-filing PDFs are NOT a safe text source — `fitz` extracts the layer *under* graphical redaction boxes (`feedback_graphical_redaction_failure_modes`).

Predicate sub-agents quote `complaint.md` + `manifest.inputs.*` verbatim into evidence strings, which flow through `examples/<id>/{facts,report,graph,loci}.json` + `Facts.lean` → `status_emit.py` → public status page — a **separate channel** from `documenting/scripts/check_redactions.py`, which never sees proving/'s JSON outputs.

`scripts/redact_artefacts.py` (downstream belt-and-suspenders): `reference_proving_redact_artefacts_script.md`.
