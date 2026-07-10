# proving — Lean4 axiomatic theorem-proving with LLM-backed predicates

Cross-project rules: `../CLAUDE.md`. The **textual axis** of the three-kernel Lean4 architecture (root CLAUDE.md § "Lean4 axes"; `data/specs/lean4-charter-2026-06-10/SPEC.md` § 4) — `/dau` is the textual-axis instance of invariant 3: proofs driven by top-tier LLMs in parallel, never manual.

## The split

The whole point of this subproject is **strict jurisdictional separation** between three layers. Do not blur them.

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Proving/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one complaint text + entity refs | a single `Bool` (plus evidence + uncertainty) | Claude Code sub-agent (`context: fork`); MAY use memsearch's `memory-recall` skill. |
| **Driver** | `scripts/extract_facts.py` | manifest + complaint | `Proving/<Framework>/Facts.lean` (axioms) + audit JSON | `claude -p` invocations (model = `QAGENTS_PREDICATE_MODEL`, default **opus** — the latest top-tier model). |

The Lean kernel never reads natural language. The predicate sub-agents never write Lean. The driver is a thin coordinator with no legal reasoning of its own. The verifiable proof IS the Lean elaboration trace produced by `lake build`.

The normative kernel↔predicate↔driver workflow representation the `/dau` lane is pointed at is `../studying/representation.md` (studying owns the operational-axis kernel + the cross-axis representation research; charter P1 gate).

## Why this works

1. Predicate functions have a **very narrow output domain** (one Bool/call) — they fit inside a forked sub-agent.
2. Lean's kernel verifies composition: once each predicate fact is an axiom, the validity theorem is a pure structure-introduction proof — type-checking guarantees the result *given the predicate truths*.

## Frameworks

Each framework lives under `Proving/<Framework>/` (kernel) + `predicates/<framework>/` (specs).

The per-framework roster (kernel · specs · source guide · statutory text for all nine goldens — Civil RICO, Title VI, CivilRights, Title IX, Title VII ×3, Rehab §504, Age Act, Title II Enf, ADA) is relocated to memory `reference_proving_doctrine_pins` § "Frameworks roster" (apply-spread proving-1), which also carries the per-framework case-law doctrine pins.

The operative statutory text lives under `legal/uscode/`, not pasted into specs. Predicate sub-agents resolve a `usc_cite` via `scripts/uscode.py path|text|list` — index→corpus fallback + subsection normalization (`§ 1962(c)` → base section; L-029), so an arbitrary in-Code cite resolves without extending the curated `index.json` (`uscode.py lint` reports predicate-spec cite resolvability). See `predicates/README.md` § "Authoritative statutory text".

These hand-built frameworks are the **golden reference** for the broader program — automated encodings are scored against them. Per-golden derivation + gap + mechanism detail: `predicates/README.md` + close summaries + memory `reference_proving_doctrine_pins`.

## Axiomatizing the full U.S. Code (program)

Spec: `data/specs/axiomatize-uscode-2026-05-29/SPEC.md`. Extends the three hand-built frameworks to a phased, title-by-title program over all 54 titles, produced redundantly by top-tier-model subagent teams along **10 orthogonal axes** (spec § 6.1): **5 core** always fanned out (Elements / Deontic / Ontology / Procedure / Structure) + **5 specialized / opt-in** via `--axes` (Remedy / Scienter / Sanction / Intertemporal / Evidentiary), then reconciled. Cross-strategy agreement, proved in the kernel via `Bridge.lean` lemmas, is the correctness signal for the LLM→Lean mapping (no other oracle exists).

- **Ground truth:** full USC markdown at the canonical USC text mirror (gitignored, ~65.7k sections, `tools/corpus_build.py --all`) + title categorization at the canonical USC text mirror. `corpus/` + `xml/` are symlinked into every worktree via the canonical USC text mirror — no manual `ln -s` needed.
- **Naming / Lean-shapes / predicate-shapes** frozen in spec §§ 3–5 (authoring contract in `predicates/README.md` § "USC-program authoring contract"); per-(title,axis) Lean namespace `Proving.USC.T<NN>.<Axis>`; shared cross-title predicates collapse to `Proving.USC.Common` (guarded by an equivalence Bridge). Code: `Proving/USC/Common/` (shared lib) + `predicates/usc/_axes/<axis>.md` (the 10 axis briefings; see `predicates/usc/_axes/README.md`) + `ProvingUSC` lean_lib in `lakefile.toml`.
- **§ 1962(c) calibration anchor (hand-built, kernel-green):** all 6 axes under `Proving/USC/T18/<Axis>/` + `Bridge.lean` + `Reconciled/T18.lean` (`Bridge.s1962c_tierA` = spec § 8.3 Tier-A; Procedure/Remedy demonstrate the § 5.3 `Common` collapse). The template cell-agents mirror and the fan-out's scoring reference.
- **Calibration metric is BRIDGE-BASED.** Agreement-vs-golden is measured by kernel-checked **golden-bridges** (`Proving/USC/T{18,42}/GoldenBridge.lean`): the blind cell's composite implies the golden composite under declared correspondence axioms, discharged sorry-free (spec §§ 4.6/8/9.4). Score via the shared cross-axis G2 oracle guard `code/lean_tools/score_bridge.py --lexicon agreement --root proving` (certifies no `sorryAx`; reads the tier from a `_modulo_gaps` theorem-name suffix; the proving-local fork was retired 2026-06-27 per coherency C19 — invoked through `dau.sh --score`, `dau-{reconciler,cross}.md`, never a local copy); Tier-B/C gaps surface the omitted golden element as a named `gap_*` hypothesis. `scripts/calibrate_golden.py` is retained ONLY as a regression check for hand-built name-matched cells — exact-string is unwinnable for blind agents (naming is a free variable).
- **Lane:** manual-interactive via the **`/dau-manual`** skill (`.claude/skills/dau-manual/`; mirrors `/dco-manual`) is the **current lane** (the SDK batch lane is paused with the dedicated credit — root CLAUDE.md § Agent SDK lane; batch path spec § 7.3). Mechanical phases in `scripts/dau.sh` (`--pre`/`--permit-fanout`/`--plan-cells`/`--collect`/`--score`/`--report`); LLM fan-out over `.claude/agents/dau-{cell,reconciler,cross}.md`. Zero-prompt fan-out enforced by `scripts/dau.sh --permit-fanout` against `scripts/dau-helpers/required-allow-patterns.txt` (exit 61). Cells write to `pending/uscode-cells/` (sandboxed via `extract_facts.py --sandbox-out`; ephemeral, prunable once archived), promoted only after the reconcile gate; at the promotion gate `scripts/dau.sh --archive-wave <wave-id>` freezes the blind sandbox into the gitignored, S3-backed `proving/waves/<wave-id>/` (immutable per-fan-out dir; `WAVE.json` manifest; symlinked into worktrees via `proving/.worktree-links`; S3 class `usc-waves`). Spec § 7.5 + § 12; tests `data/specs/axiomatize-uscode-2026-05-29/tests/`. **Phase 4M scale-up (ADOPTED 2026-07-09):** parallel `proving-N` breadth lanes on a disjoint title/chapter partition + staged cell-width escalation (12→25→40) + serial collapse lane draining the tracked `proving/common-held.json` helds ledger — subspec `dau-parallel-scaling-2026-07-09/` in the family (prompts `PROMPTS.md` T0–T7; lane rules in `dau-manual/SKILL.md` § Parallel lanes). `--plan-cells --sections`: bare section numbers now resolve chapter dirs before `_*` catch-alls (the `_orphan/` shadow was fixed 2026-07-10, t_04-guarded); chapter-qualified refs (`ch1/2`) remain the explicit form. Second wave in an already-promoted chapter re-homes to the nested `.Ch<NN>.Part2.<Axis>` sibling subgroup (SKILL Step 7).
- **Status:** Phases 0–1 done; Phase 2 calibration anchor + waves promoted to canonical (approach-B `Proving.USC.<Title>.*` sub-namespaces; cross-title Common-collapse; corpus rollup `proving/coverage.json`). **Per-wave detail + remaining-section roster + current state live in spec § 10.1 + § 12 + the close summaries — never duplicated here.** Two load-bearing invariants: cell Lean files MUST use FULL-path imports (`reference_lean_isolation_probe_full_path_imports`); authoritative build target is `lake build ProvingUSC` (bare `lake build` is red-by-design on REJECTED examples) — run it before promoting, never trust a cell's self-reported build. Phases 3–4 (SDK-funded bulk scaling) are **paused, not cancelled**; the program continues on `/dau-manual` meanwhile.
- **Hierarchical-predicate depth layer (H0–H4 landed).** Flat opaque predicates decompose into LLM-decided leaf predicates + kernel-derived composites. Model **stratification**: Tier 0 kernel-decides (zero LLM) / Tier 1 Opus leaf-extraction (default, exit-3) / Tier 2 Opus proof-driving. **Oracle guard (load-bearing):** search automation (`grind`/`aesop`) NEVER discharges a `Bridge`/`GoldenBridge` agreement lemma — `score_bridge.py`'s `reject_automation_in_bridge` enforces it syntactically (**exit 4**, ahead of `sorryAx`). Full depth-layer detail (leaves/derivation/tactic, bake-off gate, debates, H1 cell): `data/specs/axiomatize-uscode-2026-05-29/hierarchical-predicates-2026-06-20/SPEC.md` §§ 13/13.1; status of record `../studying/representation.md` § 13.4.
- **Graph projections (Half-A domain graph).** `scripts/uscode_graph.py --cite-graph` emits the **`qgraph-wire/1` node-link envelope** (deterministic Axis-5 §-citation graph, `graph.axis=textual`), consumed by BOTH the graphs-2 `fromNodeLink` reader (mounts in `verifying/`; monitoring M2) AND `qagents.lean_graph`'s `anchor()` |D| join. Build, `--all-titles`, `--centrality-out`, gitignored `proving/graphs/`, tests: `data/specs/axiomatize-uscode-2026-05-29/graph-projections-2026-06-14/SPEC.md` § 4.2.

## Layout (essentials)

```
proving/
├── Proving.lean                    root module — imports both frameworks
├── lakefile.toml
├── lean-toolchain                  pinned: leanprover/lean4:v4.31.0
├── Proving/<Framework>/{Types,Predicates,Statute,Theorems}.lean
│                                   Facts.lean is GENERATED + gitignored
├── predicates/<framework>/         markdown specs (one per opaque predicate)
├── scripts/
│   ├── extract_facts.py            driver — reads `framework` block from manifest
│   ├── lake_trace.py               two error-line orderings (4.29 vs 4.30+)
│   ├── lean_parse.py               regex-based proof-file structural parser
│   ├── uscode.py                   path/text/list lookup against legal/uscode/
│   └── uscode_graph.py             Axis-5 §-citation graph (Half-A live |D| domain graph)
└── examples/<id>/                  per-run artefacts (see below)
```

Spec roster: authoritative breakdown in `predicates/README.md` (update it + the frameworks table above when adding a framework).

## Workflow

1. **Author the formal framework** (Lean) — for a new framework, add `Proving/<NewFramework>/{Types,Predicates,Statute,Theorems}.lean` and import from `Proving.lean`.
2. **Author predicate specs** under `predicates/<newframework>/`. Spec format is fixed (see `predicates/README.md`).
3. **Run the driver**:
   ```
   python3 scripts/extract_facts.py examples/<id>/complaint.md \
           --manifest examples/<id>/manifest.json --example-id <id> [--build]
   ```
   The manifest's `framework` block selects where Facts.lean is written and which namespace prefix to use. `--build` runs `lake build <proof_target>` and emits `report.json` + `graph.json` + `loci.json` per `data/specs/proving-results-propagation-2026-05-09/SPEC.md`. The lake target is taken from `manifest.framework.proof_target`. `--reuse-facts --example-id <id>` skips predicate sub-agents and re-emits artefacts from existing `examples/<id>/facts.json`.

4. **Verify**: `lake build`. If succeeds, kernel is well-formed. To verify a specific example proof, elaborate with `lake env lean examples/<id>/proof.lean` once Facts.lean has been generated.

The driver prints one `· <spec> ... <value>  (<uncertainty>)` line per predicate in **all three modes** (`--stub` / `--reuse-facts` / production); adapters (e.g. `verifying/server/adapters/proving.py._classify`) rely on this line shape unchanged across modes.

**`--stub` caveat for REJECTED examples.** `--stub` defaults every predicate to `True` — it would overwrite committed REJECTED reports with synthetic ACCEPTED. This is now **guard-enforced** (L-030): a committed (non-`--sandbox-out`) `--stub` run against an example whose committed `report.json` verdict is `REJECTED` **refuses** (exit 2) unless `--force-stub`. Use `--reuse-facts` for any replay over a REJECTED run. Pinned: `feedback_proving_stub_defaults_true`. **Timeout/failure preserves paid work (L-030):** a `claude -p` `TimeoutExpired` is caught in `_run_claude` (a handled failed attempt, not an opaque crash) and any predicate failure mid-run writes the completed results to `facts.json` (sandbox) or a `facts.partial.json` sidecar (committed) rather than discarding them. Guards tested by `scripts/test_driver_hardening.py`.

## Per-run artefacts (`examples/<id>/`)

When invoked with `--build`, the driver emits:

| file | what | consumer |
|---|---|---|
| `facts.json` | per-predicate `{value, evidence, uncertainty}` records — the audit trail | reviewer; `report.json` builder |
| `Facts.lean` | the framework's generated axioms; also written to `Proving/<Framework>/Facts.lean` | `lake build` |
| `report.json` | full run record: predicates + kernel verdict + per-error locus (intro-rule + field). Schema in propagation spec § 2.1 | `verifying/web/`'s `/api/runs/<id>/report`; status-emit aggregator |
| `graph.json` | proof DAG (predicate-pill / axiom-rectangle / theorem-hexagon nodes; `applies` / `composes` / `inhabits` / `disjunctionCase` edges; `failures[]` for the debug overlay). Adapted by `verifying/web/public/graphs2/loader.js` (graph.json v1) | graphs-2 kit `/proof-graph/run/<id>/` |
| `loci.json` | single `DiagramEmit` rendering the kernel's intro-rule shape with verdict-coloured slots | `data/status/proving.json` `diagrams[1]` |

`report.json` joins via `kernel.errors[].axiomName` ↔ `predicates[].axiomName` so a UI can light up the failing predicate row red.

**Schema is locked at the consumer boundary.** `verifying/web/public/graphs2/loader.js` adapts `graph.json` (full-word `kind`, no positions, evidence arrays, string uncertainty) into the graphs-2 kit's renderable shape. Any change to `graph.json` field names or `kind` values is a two-sided edit — bump the spec at `data/specs/proving-results-propagation-2026-05-09/SPEC.md` § 2.3 and update the loader together. Tests 38 + 41-43 enforce both halves.

**Sibling parity with `accounting/`.** `accounting/scripts/{lean_parse,lake_trace,report}.py` mirror this pipeline (`lake_trace.py` verbatim; `lean_parse.py`+`report.py` share internals); `accounting/examples/<id>/graph.json` is byte-compatible `graph.json` (propagation spec § 2.3). The bridge scorer is **no longer a per-axis fork**: proving consumes the shared `code/lean_tools/score_bridge.py` (C19, 2026-06-27); accounting's fork migration is the pending C5 slice (its `dat.sh`/`dat-{reconciler,cross}` still call the local copy until then), so the shared module is the diff-check counterpart once both land. Lockstep also covers the **S3 push lanes** (`dau.sh`/`dat.sh` `--push-all`/`--push-if-warm`/`aws_session_warm` + `t_08`/`t_09`). Diff-check any remaining shared script (`lean_parse`/`lake_trace`/`report`) against the counterpart before landing, and leave the deliberate accounting-side divergences alone (lowercase axiom names, dotted conclusion heads, its own `LociRoster` shape, push-pin source + archive class).

## What we encode

Per-framework doctrine pins (the case-law each kernel element encodes) + the top-level inductive shapes (`ValidCivilRicoComplaint`, `ValidTitleVIJudicialClaim`, …) live in memory `reference_proving_doctrine_pins` + the predicate specs.

## Adding a new statute / framework

Authoring recipe (kernel quartet → `Proving.lean` wire → predicate specs → sample → `LociRoster` registration → roster/table update) lives in `predicates/README.md` § "Adding a new framework — authoring contract".

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no FFI. Kernel is pure.
2. **Predicate specs MUST NOT cite or read `Proving/<Framework>/*.lean`.** Their world is the complaint text + spec rubric.
3. **The driver MUST NOT make legal judgments.** Add fields to JSON schema or a new `framework` block field rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** Both files are gitignored. The `.gitignore` enumerates `Proving/<Framework>/Facts.lean` **explicitly per framework** (not globbed) — when adding a framework, add its entry, else a `--build` run commits the ephemeral copy. Only `examples/*/Facts.lean` is tracked (the verifiable proof artefact).
5. **memsearch never indexes `Proving/<Framework>/*.lean`.** Lean files excluded by design (memsearch only scans `.md`/`.markdown`).
6. **Predicates live under `predicates/<framework>/`.** Manifest spec paths use the subdirectory.

## Predicate sub-agent memsearch use

A predicate sub-agent MAY invoke the `memory-recall` skill (itself `context: fork`). Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop hook auto-writes; predicate names preserved verbatim); collection is per-subproject via the patched `lib/memsearch` `common.sh`.

## Toolchain notes

- **Lean** pinned via `lean-toolchain` to `v4.31.0` (current stable; lockstep with `accounting/` + `studying/` per root CLAUDE.md § Lean4 axes inv-4 — three-way, one commit, example proofs replayed).
- **No Mathlib dependency** — keeps `lake build` fast. Confirmed by the 2026-06-20 hierarchical-predicates debate (R4): the no-Mathlib lift is a **gated per-axis opt-in, never global**, and proving stays Mathlib-free (no legal-doctrine lemma in Mathlib). Tactic substrate is core-only: `Proving/USC/Common/Tactic.lean` (`prove_element`; the `@[doctrine]` set = `@[grind →]` intro rules; `grind` is core v4.30, `aesop` absent/struck).
- **Python ≥ 3.10** for the driver (system `python3`, no venv).
- **Claude CLI** must be on `$PATH`.
- **Claude `-p` flag set for predicate sub-agents** — today text-reasoning-only (no Bash). When predicates need external tools, adopt accounting's flag set + driver-injected "REAL-CALL MODE" preamble per `feedback_claude_p_subagent_real_call_pattern`.
- **Model is top-tier, hard-enforced (not a cost choice).** Production (predicate-invoking) runs of `extract_facts.py` **hard-fail (exit 3)** on any non-top-tier `QAGENTS_PREDICATE_MODEL` (accepted tokens: `opus`; default `opus`) unless `--allow-smoke-model` is passed; `--stub`/`--reuse-facts` are exempt (they never call the model). All axiomatization — hand-built examples + the `dau` USC agents (frontmatter `model: opus`) — runs the latest top-tier model by policy (the 2026-06-03 RICO-example bake-off measured haiku as a capability constraint for trust, not just cost — `feedback_predicate_model_opus_not_haiku`). The driver carries two guards (`invoke_predicate`, tested by `scripts/test_predicate_guard.py`): **Guard A** rejects+retries a result that claims it couldn't read the complaint or carries no evidence (NOT substantive legal negation — that's a legitimate False here); **Guard B** band-normalizes uncertainty then treats `high` as a review FLAG, never an auto-reject (high is honest on a real knife-edge).

**Driver smoke-test side effect.** Without `--sandbox-out`, `scripts/extract_facts.py --example-id <id>` overwrites `examples/<id>/{Facts.lean,facts,report,graph,loci}.json` and runs a fresh `lake build` — use **`--sandbox-out <dir>`** for any smoke test or axiomatize-uscode cell run (redirects per-run artefacts, restores canonical `Proving/<Framework>/Facts.lean` after `--build`). `--reuse-facts` reads the committed `examples/<id>/`, independent of `--sandbox-out`. Not yet mirrored to accounting's driver (still clobbers). Detail + spotter rule: `feedback_driver_overwrites_example_artifacts`.

## Open work

- **`LociRoster` gap (gated on an example run):** the USC-program `Prohibited.*` §1962 judgments have no complaint run exercising them, so a roster renders nothing until one exists (same "— · not exercised" shape as `rico_hier`'s kernel-DERIVED elements — the rich hier view is the in-depth proof-graph, not this panel). Two flat Title VII goldens use `substantive=None` deliberately.
- Persisting golden gotchas: the Title IX harassment-severity axiom keeps the upstream spelling `SexualHarassmentSevereePervasive` (spec filename matches); the `{rehab504,ageact}` samples were `--stub`-built.

## Status emit (`data/status/proving.json`)

Full status-emit contract relocated to memory `project_proving_subproject__emit` (apply-spread C-1, 2026-07-05): `proving/scripts/status_emit.py` producer, `panels[]` order, the `usc-program` KpiStrip, `coverage.json` derived-invariant + gate enforcement (C10/C11), public-surface synthetic-only gate (`PUBLIC_EXAMPLE_IDS`), two-lane writer, and the cron schedule.

## Redaction (`scripts/redact_complaints.py` + `scripts/redact_artefacts.py`)

**Two-stage, source-first.** `scripts/redact_complaints.py` redacts the SOURCE `examples/*/complaint.md` to the **uniform-strict / FBI-director-letter standard** (keep every `X v. Y` citation + government bodies; scrub all other personal names, private medical entities, residential addresses). A clean source means a fresh `--build` CANNOT re-leak a quote. Covers every example complaint; idempotent + **self-auditing** (case-insensitive DENYLIST + honorific-residue scan). Run before any fresh derivation; public court-filing PDFs are NOT a safe text source — `fitz` extracts the layer *under* graphical redaction boxes (`feedback_graphical_redaction_failure_modes`).

Predicate sub-agents quote `complaint.md` + `manifest.inputs.*` verbatim into evidence strings, which flow through `examples/<id>/{facts,report,graph,loci}.json` + `Facts.lean` → `status_emit.py` → public status page. This is a **separate channel** from `documenting/scripts/check_redactions.py`; the PDF gate does not see proving/'s JSON outputs.

`scripts/redact_artefacts.py` is the downstream belt-and-suspenders: a deterministic, idempotent literal-substring + regex pass over the generated RICO artefact set, allow-list aligned with the public-record redaction standard; for already-verified runs it preserves Bool/uncertainty audit integrity without a model rerun. Byte-form / JSON-escape-depth detail: `reference_proving_redact_artefacts_script.md`.
