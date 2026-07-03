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

1. memsearch sees only natural-language artefacts — never Lean dependent types.
2. Predicate functions have a **very narrow output domain** (one Bool/call) — they fit inside a forked sub-agent.
3. Lean's kernel verifies composition: once each predicate fact is an axiom, the validity theorem is a pure structure-introduction proof — type-checking guarantees the result *given the predicate truths*.
4. The audit trail is `examples/<id>/facts.json` — every predicate output with evidence quotes + uncertainty.

## Frameworks

Each framework lives under `Proving/<Framework>/` (kernel) + `predicates/<framework>/` (specs).

| Framework | Kernel | Specs | Source guide | Statutory text |
|---|---|---|---|---|
| **Civil RICO** (18 U.S.C. §§ 1961–1968; § 1962(a)(b)(c)(d) + § 1964(c) standing) | `Proving/Rico/` | `predicates/rico/` | `legal/guides/rico_guide_jenner-block_2021.pdf` | the canonical USC text mirror |
| **Title VI** (42 U.S.C. §§ 2000d et seq.; intentional, disparate impact, retaliation) | `Proving/TitleVI/` | `predicates/titlevi/` | `legal/guides/title-vi_manual_doj_2017.pdf` | the canonical USC text mirror |
| **CivilRights** (42 U.S.C. §§ 1981, 1983, 1985(3); equal contracting, color-of-law, civil-rights conspiracy) | `Proving/CivilRights/` | `predicates/civilrights/` | `legal/guides/s1983_treatise_fjc_2014.pdf` (Schwartz/FJC); `s1981_overview_crs_2023.pdf`; `civilrights_overview_crs_2012.pdf` (cross-cutting + § 1985) | the canonical USC text mirror |
| **Title IX** (20 U.S.C. §§ 1681–1688; sex discrimination in federally funded education — intentional *Cannon*, disparate impact admin-only, retaliation *Jackson*, deliberate-indifference harassment *Gebser*/*Davis*) | `Proving/TitleIX/` | `predicates/titleix/` (21) | — | the canonical USC text mirror |
| **Title VII** (42 U.S.C. ch21 subch. VI; THREE goldens under `Proving/TitleVII/`: §2000e-5(f)(1) mixed public+private enforcement [root ns]; §2000e-6(a) AG pattern-or-practice [`.PatternOrPractice`]; §2000e-16(c) federal-sector [`.FederalSector`]) | `Proving/TitleVII/` (+ `/PatternOrPractice`, `/FederalSector`) | `predicates/titlevii/` (19) | — | the canonical USC text mirror |
| **Rehab §504** (29 U.S.C. § 794; disability discrimination in federally assisted OR conducted programs — intentional "solely by reason of" *Darrone*, failure-to-accommodate / meaningful access *Choate*/*Davis*, disparate impact admin-only, retaliation; **sibling** of Title VI: `disability` ground + federally-conducted prong + "otherwise qualified" gate) | `Proving/Rehab504/` | `predicates/rehab504/` (19) | — | the canonical USC text mirror |
| **Age Act** (42 U.S.C. §§ 6101–6107; age discrimination in federally assisted programs — intentional §6102, disparate impact admin-only, retaliation; **sibling** of Title VI: `age` ground + §6103(b)/(c) carve-out schedule as first-class coverage element) | `Proving/AgeAct/` | `predicates/ageact/` (17) | — | the canonical USC text mirror |
| **Title II Enf** (42 U.S.C. § 2000a-5(b); ENFORCEMENT-mechanism golden — the three-judge-court track + single-judge fallback for an AG pattern-or-practice action; **procedural**, not a discrimination claim: chief-judge addressee + panel composition + "in every way expedited" duty + direct Supreme-Court appeal as first-class elements) | `Proving/TitleIIEnf/` | `predicates/titleiienf/` (10) | — | the canonical USC text mirror |
| **ADA** (42 U.S.C. ch126; Title I employment §§12111/12112, Title II public services §§12131/12132, Title III public accommodations §§12181/12182, §12203 retaliation; **sibling** of Rehab §504 but THREE title-specific coverage regimes — employer / public entity / public-accommodation operator — and "on the basis of" (I/III) / "by reason of" (II) causation, dropping §504's "solely"; impact judicially enforceable ⇒ NO admin-only split; 6-route `ValidADAComplaint`) | `Proving/ADA/` | `predicates/ada/` (24) | — | the canonical USC text mirror |

The operative statutory text lives under `legal/uscode/`, not pasted into specs. Predicate sub-agents resolve a `usc_cite` via `scripts/uscode.py path|text|list` against the canonical USC text mirror. See `predicates/README.md` § "Authoritative statutory text".

These hand-built frameworks are the **golden reference** for the broader program — automated encodings are scored against them. Goldens after CivilRights arrived via the **golden-expansion path** (blind Tier-B `gap_*` → hand-built golden supplying the second witness → re-bridge Tier-A sorry-free); the eighth (ADA, 2026-06-24) is the first **golden-FIRST** build (kernel + specs ahead of any blind wave, so its bridging USC wave is forward work, not a re-bridge). Per-golden derivation + gap + mechanism detail: `predicates/README.md` + close summaries + memory `reference_proving_doctrine_pins`.

## Axiomatizing the full U.S. Code (program)

Spec: `data/specs/axiomatize-uscode-2026-05-29/SPEC.md`. Extends the three hand-built frameworks to a phased, title-by-title program over all 54 titles, produced redundantly by top-tier-model subagent teams along **10 orthogonal axes** (spec § 6.1): **5 core** always fanned out (Elements / Deontic / Ontology / Procedure / Structure) + **5 specialized / opt-in** via `--axes` (Remedy / Scienter / Sanction / Intertemporal / Evidentiary), then reconciled. Cross-strategy agreement, proved in the kernel via `Bridge.lean` lemmas, is the correctness signal for the LLM→Lean mapping (no other oracle exists).

- **Ground truth:** full USC markdown at the canonical USC text mirror (gitignored, ~65.7k sections, `tools/corpus_build.py --all`) + title categorization at the canonical USC text mirror. `corpus/` + `xml/` are symlinked into every worktree via the canonical USC text mirror — no manual `ln -s` needed.
- **Naming / Lean-shapes / predicate-shapes** frozen in spec §§ 3–5 (authoring contract in `predicates/README.md` § "USC-program authoring contract"); per-(title,axis) Lean namespace `Proving.USC.T<NN>.<Axis>`; shared cross-title predicates collapse to `Proving.USC.Common` (guarded by an equivalence Bridge). Code: `Proving/USC/Common/` (shared lib) + `predicates/usc/_axes/<axis>.md` (the 10 axis briefings; see `predicates/usc/_axes/README.md`) + `ProvingUSC` lean_lib in `lakefile.toml`.
- **§ 1962(c) calibration anchor (hand-built, kernel-green):** all 6 axes under `Proving/USC/T18/<Axis>/` + `Bridge.lean` + `Reconciled/T18.lean` (`Bridge.s1962c_tierA` = spec § 8.3 Tier-A; Procedure/Remedy demonstrate the § 5.3 `Common` collapse). The template cell-agents mirror and the fan-out's scoring reference.
- **Calibration metric is BRIDGE-BASED.** Agreement-vs-golden is measured by kernel-checked **golden-bridges** (`Proving/USC/T{18,42}/GoldenBridge.lean`): the blind cell's composite implies the golden composite under declared correspondence axioms, discharged sorry-free (spec §§ 4.6/8/9.4). Score via the shared cross-axis G2 oracle guard `code/lean_tools/score_bridge.py --lexicon agreement --root proving` (certifies no `sorryAx`; reads the tier from a `_modulo_gaps` theorem-name suffix; the proving-local fork was retired 2026-06-27 per coherency C19 — invoked through `dau.sh --score`, `dau-{reconciler,cross}.md`, never a local copy); Tier-B/C gaps surface the omitted golden element as a named `gap_*` hypothesis. `scripts/calibrate_golden.py` is retained ONLY as a regression check for hand-built name-matched cells — exact-string is unwinnable for blind agents (naming is a free variable).
- **Lane:** manual-interactive via the **`/dau-manual`** skill (`.claude/skills/dau-manual/`; mirrors `/dco-manual`) is the **current lane** — the SDK *batch* lane's dedicated credit was paused 2026-06-15 (contingent; batch path spec'd at § 7.3 — `reference_agent_sdk_credit_200_mo`), so it has no cost edge over manual today. Mechanical phases in `scripts/dau.sh` (`--pre`/`--permit-fanout`/`--plan-cells`/`--collect`/`--score`/`--report`); LLM fan-out over `.claude/agents/dau-{cell,reconciler,cross}.md`. Zero-prompt fan-out enforced by `scripts/dau.sh --permit-fanout` against `scripts/dau-helpers/required-allow-patterns.txt` (exit 61). Cells write to `pending/uscode-cells/` (sandboxed via `extract_facts.py --sandbox-out`; ephemeral, prunable once archived), promoted only after the reconcile gate; at the promotion gate `scripts/dau.sh --archive-wave <wave-id>` freezes the blind sandbox into the gitignored, S3-backed `proving/waves/<wave-id>/` (immutable per-fan-out dir; `WAVE.json` manifest; symlinked into worktrees via `proving/.worktree-links`; S3 class `usc-waves`). Spec § 7.5 + § 12; tests `data/specs/axiomatize-uscode-2026-05-29/tests/`.
- **Status:** Phases 0–1 done; Phase 2 calibration anchor + waves promoted to canonical (approach-B `Proving.USC.<Title>.*` sub-namespaces; cross-title Common-collapse; corpus rollup `proving/coverage.json`). **Per-wave detail + remaining-section roster + current state live in spec § 10.1 + § 12 + the close summaries — never duplicated here.** Two load-bearing invariants: cell Lean files MUST use FULL-path imports (`reference_lean_isolation_probe_full_path_imports`); authoritative build target is `lake build ProvingUSC` (bare `lake build` is red-by-design on REJECTED examples) — run it before promoting, never trust a cell's self-reported build. Phases 3–4 (SDK-funded bulk scaling) are **paused, not cancelled**; the program continues on `/dau-manual` meanwhile.
- **Hierarchical-predicate depth layer (2026-06-20; H0–H4 landed — status of record `../studying/representation.md` § 13.4).** A depth amendment UNDER the 10 axes: flat opaque predicates decompose into case-law **leaf predicates** (LLM-decided) + kernel-**derived** high-level predicates joined by **procedural axioms/theorems**, discharged by `Proving/USC/Common/Tactic.lean`'s `prove_element` — the LLM extracts leaves, the kernel derives the composite via proof search. **Oracle guard (load-bearing):** search automation (`grind`/`aesop`) NEVER discharges a `Bridge`/`GoldenBridge` agreement lemma (term-only); `score_bridge.py`'s `reject_automation_in_bridge` enforces it syntactically (**exit 4**, ahead of `sorryAx`; test `…/tests/cases/t_11_hier_oracle_guard.sh`, mirrors accounting's `t_17`). Model **stratification**: Tier 0 kernel-decides (zero LLM) / Tier 1 Opus leaf-extraction (default, exit-3; a leaf class downgrades to a cheaper model only after the five-point bake-off gate clears — `scripts/bakeoff_tier1.py`; eligibility is per-leaf-class, NON-MONOTONIC across leaves, never model-wide) / Tier 2 Opus proof-driving. Spec `data/specs/axiomatize-uscode-2026-05-29/hierarchical-predicates-2026-06-20/SPEC.md` (§§ 13/13.1); debates `data/debates/axiomatize-hierarchical-predicates-2026-06-20{,-r02}.md`; H1 cell `Proving/USC/T18/Hier/`. Owed cross-axis amendments listed there.
- **Graph projections (Half-A domain graph).** `scripts/uscode_graph.py --cite-graph` (stdlib, system `python3`) builds the deterministic Axis-5 §-citation graph (one node per operative section keyed by `usc_cite` + Title▸Chapter cluster + directed cross-ref `links`), emitting the **`qgraph-wire/1` node-link envelope** (`graph.axis=textual`, `domain=legal`, `privacy=public-ok`) consumed by BOTH the graphs-2 `fromNodeLink` reader (mounts in `verifying/`; monitoring M2) AND `qagents.lean_graph`'s `anchor()` |D| join (reads only `nodes`). Default emit = T18/T42 slice (~10k sections); `--all-titles` = the full 62,831-section universe. `python -m qagents.lean_graph --axis textual --domain-graph graphs/structure/graph.json` flips textual coverage from the calibration denominator to live |D|; `--centrality-out` feeds the deferred `section_prescreen.py`. `proving/graphs/` is gitignored regenerable. Tests: `scripts/test_uscode_graph.py`. Spec: `data/specs/axiomatize-uscode-2026-05-29/graph-projections-2026-06-14/SPEC.md` § 4.2.

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

Spec roster (authoritative breakdown in `predicates/README.md`): RICO 28, Title VI 17, CivilRights 14, Title IX 21, Rehab §504 19, Age Act 17, Title II Enf 10, ADA 24.

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

**`--stub` caveat for REJECTED examples.** `--stub` defaults every predicate to `True` — it overwrites committed REJECTED reports with synthetic ACCEPTED. Use `--reuse-facts` for any replay over a REJECTED run. Pinned: `feedback_proving_stub_defaults_true`.

## Per-run artefacts (`examples/<id>/`)

When invoked with `--build`, the driver emits:

| file | what | consumer |
|---|---|---|
| `facts.json` | per-predicate `{value, evidence, uncertainty}` records — the audit trail | reviewer; `report.json` builder |
| `Facts.lean` | the framework's generated axioms; also written to `Proving/<Framework>/Facts.lean` | `lake build` |
| `report.json` | full run record: predicates + kernel verdict + per-error locus (intro-rule + field). Schema in propagation spec § 2.1 | `verifying/web/`'s `/api/runs/<id>/report`; status-emit aggregator |
| `graph.json` | proof DAG (predicate-pill / axiom-rectangle / theorem-hexagon nodes; `applies` / `composes` / `inhabits` / `disjunctionCase` edges; `failures[]` for the debug overlay). Byte-compatible with `verifying/web/public/proof-graph/fixture-rico.js` | proof-graph kit `/proof-graph/run/<id>/` |
| `loci.json` | single `DiagramEmit` rendering the kernel's intro-rule shape with verdict-coloured slots | `data/status/proving.json` `diagrams[1]` |

`report.json` joins via `kernel.errors[].axiomName` ↔ `predicates[].axiomName` so a UI can light up the failing predicate row red. `graph.json` shares the same fixture shape as the bundled Doe v. Acme demo.

**Schema is locked at the consumer boundary.** `verifying/web/public/proof-graph/loader.js` adapts `graph.json` (full-word `kind`, no positions, evidence arrays, string uncertainty) into the kit's renderable shape. Any change to `graph.json` field names or `kind` values is a two-sided edit — bump the spec at `data/specs/proving-results-propagation-2026-05-09/SPEC.md` § 2.3 and update the loader together. Tests 38 + 41-43 enforce both halves.

**Sibling parity with `accounting/`.** `accounting/scripts/{lean_parse,lake_trace,report}.py` mirror this pipeline (`lake_trace.py` verbatim; `lean_parse.py`+`report.py` share internals); `accounting/examples/<id>/graph.json` is byte-compatible with the same `RicoFixture` shape. The bridge scorer is **no longer a per-axis fork**: proving consumes the shared `code/lean_tools/score_bridge.py` (C19, 2026-06-27); accounting's fork migration is the pending C5 slice (its `dat.sh`/`dat-{reconciler,cross}` still call the local copy until then), so the shared module is the diff-check counterpart once both land — until then proving's fork is GONE, do not re-create it. Lockstep also covers the **S3 push lanes** (`dau.sh`/`dat.sh` `--push-all`/`--push-if-warm`/`aws_session_warm` + `t_08`/`t_09`). Diff-check any remaining shared script (`lean_parse`/`lake_trace`/`report`) against the counterpart before landing, and leave the deliberate accounting-side divergences alone (lowercase axiom names, dotted conclusion heads, its own `LociRoster` shape, push-pin source + archive class).

## What we encode

Per-framework doctrine pins — the case-law each kernel element encodes (*Boyle*/*Reves*/*Salinas*/*Holmes* for RICO; *Sandoval*/*Arlington Heights*/*Jackson* for Title VI; *Comcast*/*Monroe*/*Monell*/*Griffin* for CivilRights) — live in memory `reference_proving_doctrine_pins` and the predicate specs, along with the top-level inductive shapes (`ValidCivilRicoComplaint`, `ValidTitleVIJudicialClaim`, …).

## Adding a new statute / framework

1. Pick the section. Identify its elements.
2. Add `Proving/<NewFramework>/Types.lean` if existing types don't fit.
3. Declare opaque axioms in `Proving/<NewFramework>/Predicates.lean`.
4. Compose as `structure`s in `Proving/<NewFramework>/Statute.lean` (use `inductive` for disjunctive validity).
5. Add `<judgment>_intro` theorems in `Proving/<NewFramework>/Theorems.lean` (suffix form is normative for new code per `../studying/representation.md`).
6. Wire into `Proving.lean`.
7. Author markdown specs under `predicates/<newframework>/` per the contract.
8. Add a sample under `examples/<newframework>-sample/` with a manifest `framework` block.
9. Register a `LociRoster` for each top-level theorem in `scripts/report.py`. Skipping this silently under-reports — `lake build` stays green but `loci.json` emits a "no roster" placeholder and the status-page locus panel renders empty (accounting's `report.py JUDGMENTS` dict has the same gating shape).
10. Update `predicates/README.md` roster + this CLAUDE.md table.

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

- **Lean** pinned via `lean-toolchain` to `v4.31.0` (current stable; lockstep with `accounting/lean-toolchain` per the root CLAUDE.md single-pin rule).
- **No Mathlib dependency** — keeps `lake build` fast. Confirmed by the 2026-06-20 hierarchical-predicates debate (R4): the no-Mathlib lift is a **gated per-axis opt-in, never global**, and proving stays Mathlib-free (no legal-doctrine lemma in Mathlib). Tactic substrate is core-only: `Proving/USC/Common/Tactic.lean` (`prove_element`; the `@[doctrine]` set = `@[grind →]` intro rules; `grind` is core v4.30, `aesop` absent/struck).
- **Python ≥ 3.10** for the driver (system `python3`, no venv).
- **Claude CLI** must be on `$PATH`.
- **Claude `-p` flag set for predicate sub-agents** — today text-reasoning-only (no Bash). When predicates need external tools, adopt accounting's flag set + driver-injected "REAL-CALL MODE" preamble per `feedback_claude_p_subagent_real_call_pattern`.
- **Model is top-tier, hard-enforced (not a cost choice).** Production (predicate-invoking) runs of `extract_facts.py` **hard-fail (exit 3)** on any non-top-tier `QAGENTS_PREDICATE_MODEL` (accepted tokens: `opus`; default `opus`) unless `--allow-smoke-model` is passed; `--stub`/`--reuse-facts` are exempt (they never call the model). All axiomatization — hand-built examples + the `dau` USC agents (frontmatter `model: opus`) — runs the latest top-tier model by policy (the 2026-06-03 RICO-example bake-off measured haiku as a capability constraint for trust, not just cost — `feedback_predicate_model_opus_not_haiku`). The driver carries two guards (`invoke_predicate`, tested by `scripts/test_predicate_guard.py`): **Guard A** rejects+retries a result that claims it couldn't read the complaint or carries no evidence (NOT substantive legal negation — that's a legitimate False here); **Guard B** band-normalizes uncertainty then treats `high` as a review FLAG, never an auto-reject (high is honest on a real knife-edge).

**Driver smoke-test side effect.** Without `--sandbox-out`, `scripts/extract_facts.py --example-id <id>` overwrites `examples/<id>/{Facts.lean,facts.json,report.json,graph.json,loci.json}` and runs a fresh `lake build`. Use **`--sandbox-out <dir>`** for any smoke test or axiomatize-uscode cell run — it redirects all per-run artefacts to `<dir>` and restores the canonical `Proving/<Framework>/Facts.lean` after `--build`. `--reuse-facts` reads its source from the committed `examples/<id>/`, independent of `--sandbox-out`. NOT yet mirrored to accounting's driver (still clobbers). Detail + spotter rule: `feedback_driver_overwrites_example_artifacts`.

## Open work

- Sample manifests only exercise one act / one action; complete proofs need per-element calls. Either expand manifest or generalise predicate to accept a list.
- `examples/sample_proof.lean` has one `sorry` for per-act racketeering coverage; `examples/titlevi-sample/proof.lean` has one `sorry` for per-action retaliation coverage.
- Driver: the `rico/is-racketeering-activity` rubric pins the three tests haiku skipped — §1961(1) enumeration, Rule 9(b) omission-vs-affirmative-mailing, the §§1503/1512 federal-proceeding nexus (state Family Court conduct fails).
- **`LociRoster` gaps:** TitleVI + CivilRights rosters landed 2026-06-24 (4 example complaints render 12/12/7/7 nodes); RICO + all six post-CivilRights goldens + ADA (`ADA_LOCI_TITLE1_ACCOMMODATION`, headline Title I failure-to-accommodate track over `Title1Coverage`; `examples/ada_sample/` ACCEPTED) + the hier examples have rosters (two flat Title VII goldens use `substantive=None`). Remaining gap is *gated on an example run*: the USC-program `Prohibited.*` §1962 judgments have no complaint run exercising them, so a roster renders nothing until one exists (same "— · not exercised" shape as `rico_hier`'s kernel-DERIVED elements — the rich hier view is the in-depth proof-graph, not this panel).
- Persisting golden gotchas (frameworks table + spec § 10.1 + the 2026-06-09/06-11 close summaries): the Title IX harassment-severity axiom keeps the upstream spelling `SexualHarassmentSevereePervasive` (spec filename matches); the `{rehab504,ageact}` samples were `--stub`-built.

## Status emit (`data/status/proving.json`)

`proving/scripts/status_emit.py` (system `python3`, no venv) writes `data/status/proving.json`. Schema lives in `@qagents/diagram-kit` v0.5.0 (producer pins `KIT_VERSION`; sweep in lockstep on bumps). The surface aggregates from `examples/*/report.json` — a `framework-roster` `DiagramEmit`, a `run-stats` `KpiStripEmit` + 4 `StatCardEmit`s (status pill OK when a run is seen in the last 7 days), a `recent-runs` `TableEmit` (last ≤ 10, expand row enumerates each rejection locus), the latest-run loci `DiagramEmit` (embeds `loci.json` verbatim), a `predicate-roster-latest` `TableEmit`, and `live.metrics.latestProofGraphUrl` → `qnarre.quantapix.com/proof-graph/run/<id>/[debug/]`. The **`usc-program` `KpiStripEmit`** (sections-encoded / Tier-A / titles / %-of-universe) is the ONE panel conveying axiomatize-uscode *program* progress — reads `proving/coverage.json` `tier_totals` (the `dau-cross` rollup), NOT `examples/`; absent → no panel. Denominators pinned: `62,831` sections (graph-projections § 4.2), `58` titles; flat `live.metrics.usc*` only (StatusEmit metrics must be flat scalars). **`coverage.json` trap (durable fix LANDED 2026-06-25):** `tier_totals` used to be hand-maintained — it drifted above the per-section enumeration AND double-counted cross-lens-duplicate cites (a section encoded under two sub-namespaces, e.g. §1503 under both `18-PredicateActs` and `18-Obstruction`). The honest number is DISTINCT cites at BEST tier. `scripts/derive_coverage_totals.py` now DERIVES it: `--check` (exit 3 on drift; gated by dau test `t_13`) verifies, default write-back rewrites `tier_totals` from `titles[*].sections[*]`. Run it after any wave promotion that touches `coverage.json` (it's a no-op when already consistent). `dau-helpers/archive_wave.py` `_tally_from_sections` is the WAVE.json-headline sibling — same cite-dedup, so per-wave headlines can't drift above the global total. The authoritative encoded-section count is whatever `python3 scripts/derive_coverage_totals.py --check` reports against `proving/coverage.json` (`tier_totals.encoded_sections`, best-tier distinct cites; C12, `cross-axis-coherency-2026-06-26`) — never pin a prose figure here. **Gate enforcement (C10/C11, 2026-06-26):** `dau.sh --archive-wave` now HARD-gates the canonical rollup before freezing a wave — `derive_coverage_totals.py --check` (G3 drift → exit 3) + `scripts/validate_common_mints.py` (G5: every `Common` mint cites ≥2 witnesses + no duplicate-name re-mint → exit 5); `DAU_COVERAGE_FILE=NONE` skips it for the archive-mechanics test lane. `panels[]` order: framework-roster → run-stats → usc-program → recent-runs → loci → predicate-roster-latest. **Renaming a panel id (esp. the loci diagram, renamed 4×) is a consumer-test change**: pair with the designing `PROVING_PANELS` e2e sweep (`status.spec.ts`) same-PR — producer-driven, designing can't pin it (`feedback_emit_migration_consumer_test_drift`).

Producer never reads Lean files — walks `examples/*/report.json` + the latest `loci.json`. The "latest" anchor prefers the most recent run with a non-empty `complaint.docket` (a toy fixture cannot displace a docketed verification; falls back to absolute latest); `recent-runs` still shows every run. **Anchor gotcha:** a roster-only regen via `extract_facts.py --reuse-facts --build` bumps `report.json` timestamps and can silently move this anchor (renaming the loci panel id — a consumer change); keep such regens to `loci.json`, revert `report.json`/`graph.json`.

**Two-lane writer (cron + manual)** per `data/specs/data-conventions-2026-05-06/SPEC.md` § 5.3. Branches on `QAGENTS_PENDING_ROOT`: cron lane writes `${QAGENTS_PENDING_ROOT}/data/status/proving.json`, no lock; `verify-pending.sh` rsyncs into canonical under the lock and hard-fails (exit 7, pre-lock) on any pass-list path missing the `pending/` prefix. Manual lane acquires the root-anchored `.data-write-lock`, writes canonical, releases on exit. Both lanes write atomically. Orchestrator: `scripts/build-status-all.mjs`.

**Cron schedule** registered as `com.qagents.proving-status-emit` in `data/schedules/launchd/install.sh`'s `ROUTINES` array (`proving:status-emit:05:30:0,1,2,3,4,5,6`); script-direct in `run_routine.sh` (no Claude invocation); re-run `--enable` after editing `ROUTINES`. The cron-EC2 lane (`data/specs/cron-ec2-migration-2026-05-19/SPEC.md`) is transport-only — the script stays unchanged.

## Redaction (`scripts/redact_complaints.py` + `scripts/redact_artefacts.py`)

**Two-stage, source-first (since 2026-06-04).** The durable fix is upstream: `scripts/redact_complaints.py` redacts the SOURCE `examples/*/complaint.md` to the **uniform-strict / FBI-director-letter standard** (keep every `X v. Y` citation + government bodies; scrub all other personal names, private medical entities, residential addresses). A clean source means a fresh `--build` CANNOT re-leak a quote. Covers every example complaint; idempotent + **self-auditing** (case-insensitive DENYLIST + honorific-residue scan). Run before any fresh derivation; public court-filing PDFs are NOT a safe text source — `fitz` extracts the layer *under* graphical redaction boxes (`feedback_graphical_redaction_failure_modes`).

Predicate sub-agents quote `complaint.md` + `manifest.inputs.*` verbatim into evidence strings, which flow through `examples/<id>/{facts,report,graph,loci}.json` + `Facts.lean` → `status_emit.py` → public status page. This is a **separate channel** from `documenting/scripts/check_redactions.py`; the PDF gate does not see proving/'s JSON outputs.

`scripts/redact_artefacts.py` is the downstream belt-and-suspenders: a deterministic, idempotent literal-substring + regex pass over the generated RICO artefact set, allow-list aligned with the public-record redaction standard; for already-verified runs it preserves Bool/uncertainty audit integrity without a model rerun. Byte-form / JSON-escape-depth detail: `reference_proving_redact_artefacts_script.md`.
