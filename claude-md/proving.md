# proving — Lean4 axiomatic theorem-proving with LLM-backed predicates

Sibling of `analyzing/`, `trading/`, `appealing/`, `designing/`, `documenting/`, `monitoring/`. Cross-project rules: `../CLAUDE.md`.

## The split

The whole point of this subproject is **strict jurisdictional separation** between three layers. Do not blur them.

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Proving/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one complaint text + entity refs | a single `Bool` (plus evidence + uncertainty) | Claude Code sub-agent (`context: fork`); MAY use memsearch's `memory-recall` skill. |
| **Driver** | `scripts/extract_facts.py` | manifest + complaint | `Proving/<Framework>/Facts.lean` (axioms) + audit JSON | `claude -p` invocations (model = `QAGENTS_PREDICATE_MODEL`, default **opus**). |

The Lean kernel never reads natural language. The predicate sub-agents never write Lean. The driver is a thin coordinator with no legal reasoning of its own. The verifiable proof IS the Lean elaboration trace produced by `lake build`.

## Why this works

1. memsearch sees only natural-language artefacts. It never tries to embed Lean dependent types.
2. Predicate functions have a **very narrow output domain** (one Bool per call) — they fit comfortably inside a forked sub-agent.
3. Lean's kernel verifies composition. Once each predicate fact is recorded as an axiom, the validity theorem is a pure structure-introduction proof. If it type-checks, the result is mathematically guaranteed *given the predicate truths*.
4. The audit trail is the JSON in `examples/<id>/facts.json` — every predicate output, with evidence quotes and uncertainty.

## Frameworks

Each framework lives under `Proving/<Framework>/` (kernel) + `predicates/<framework>/` (specs).

| Framework | Kernel | Specs | Source guide | Statutory text |
|---|---|---|---|---|
| **Civil RICO** (18 U.S.C. §§ 1961–1968; § 1962(a)(b)(c)(d) + § 1964(c) standing) | `Proving/Rico/` | `predicates/rico/` | `legal/guides/rico_guide_jenner-block_2021.pdf` | the canonical USC text mirror |
| **Title VI** (42 U.S.C. §§ 2000d et seq.; intentional, disparate impact, retaliation) | `Proving/TitleVI/` | `predicates/titlevi/` | `legal/guides/title-vi_manual_doj_2017.pdf` | the canonical USC text mirror |
| **CivilRights** (42 U.S.C. §§ 1981, 1983, 1985(3); equal contracting, color-of-law, civil-rights conspiracy) | `Proving/CivilRights/` | `predicates/civilrights/` | `legal/guides/s1983_treatise_fjc_2014.pdf` (Schwartz/FJC); `s1981_overview_crs_2023.pdf`; `civilrights_overview_crs_2012.pdf` (cross-cutting + § 1985) | the canonical USC text mirror |
| **Title IX** (20 U.S.C. §§ 1681–1688; sex discrimination in federally funded education — intentional *Cannon*, disparate impact admin-only, retaliation *Jackson*, deliberate-indifference harassment *Gebser*/*Davis*) | `Proving/TitleIX/` | _kernel-only (predicate specs/example/LociRoster pending — see Open work)_ | — | the canonical USC text mirror |

The operative statutory text lives under `legal/uscode/`, not pasted into specs. Predicate sub-agents resolve a `usc_cite` via `scripts/uscode.py path|text|list` against the canonical USC text mirror. See `predicates/README.md` § "Authoritative statutory text".

These four hand-built frameworks are the **golden reference** for the broader program below — automated encodings are scored against them. Title IX was added 2026-06-05 via the `/dau-manual` golden-expansion path: a blind 20 U.S.C. § 1681 fan-out bridged to the Title VI golden only at Tier-B with an *irreducible* `gap_groundCorrespondence` (sex sits outside Title VI's closed `{race,color,nationalOrigin}` enum), so Title IX is a **sibling** of Title VI, not an instance — warranting its own golden with a `sex`-bearing `ProtectedGround` + the § 1681(a)(1)-(9) nine-exception carve-out as a first-class coverage element. The same blind cell re-bridges to the new `Proving.TitleIX.*` golden at **Tier-A** sorry-free (wave `2026-06-05-t20-titleix`).

## Axiomatizing the full U.S. Code (program)

Spec: `data/specs/axiomatize-uscode-2026-05-29.md`. Extends the three hand-built frameworks to a phased, title-by-title program over all 54 titles, produced redundantly by Opus subagent teams along **10 orthogonal axes** (expanded 6→10 on 2026-06-01, spec § 6.1): **5 core** always fanned out (Elements / Deontic / Ontology / Procedure / Structure) + **5 specialized / opt-in** via `--axes` (Remedy / Scienter / Sanction / Intertemporal / Evidentiary), then reconciled. Cross-strategy agreement, proved in the kernel via `Bridge.lean` lemmas, is the correctness signal for the LLM→Lean mapping (no other oracle exists).

- **Ground truth (delivered 2026-05-29):** full USC markdown at the canonical USC text mirror (gitignored, ~65.7k sections, `tools/corpus_build.py --all`) + title categorization at the canonical USC text mirror (`tools/build_categorization.py`). `corpus/` + `xml/` are symlinked-from-canonical into every worktree via the canonical USC text mirror (`scripts/open.sh`, spec `data/specs/open-close-dcu-2026-05-26.md` § 8.14) — no manual `ln -s` needed.
- **Naming / Lean-shapes / predicate-shapes** frozen in spec §§ 3–5 (authoring contract in `predicates/README.md` § "USC-program authoring contract"); per-(title,axis) Lean namespace `Proving.USC.T<NN>.<Axis>`; shared cross-title predicates collapse to `Proving.USC.Common` (guarded by an equivalence Bridge). Code: `Proving/USC/Common/` (shared lib) + `predicates/usc/_axes/<axis>.md` (the 10 axis briefings; see `predicates/usc/_axes/README.md`) + `ProvingUSC` lean_lib in `lakefile.toml`.
- **§ 1962(c) calibration anchor (hand-built, kernel-green):** all 6 axes encoded under `Proving/USC/T18/<Axis>/` + `Bridge.lean` + `Reconciled/T18.lean`. `Bridge.s1962c_tierA` witnesses the spec § 8.3 Tier-A condition (Elements/Deontic/Ontology corroborate, all pairwise bridges discharge with no `sorryAx`); Procedure/Remedy demonstrate the § 5.3 shared-predicate collapse to `Common`. This anchor is the template cell-agents mirror and the reference the fan-out is scored against.
- **Calibration metric is BRIDGE-BASED (revised 2026-05-29).** Agreement-vs-golden is measured by kernel-checked **golden-bridges** (`Proving/USC/T{18,42}/GoldenBridge.lean`): the blind cell's composite implies the golden composite under declared correspondence axioms, discharged sorry-free (spec §§ 4.6/8/9.4). Score via `scripts/score_bridge.py` (certifies no `sorryAx` via `#print axioms`; reads Tier-A-full vs Tier-B/C-gap from a `_modulo_gaps` theorem-name suffix). `scripts/calibrate_golden.py` (exact predicate-head set recall; Elements anchor 7/7) is retained ONLY as a regression check for hand-built, name-matched cells — the 2026-05-29 wave proved exact-string is unwinnable for blind agents (naming is a free variable). Tier-B/C gaps surface the omitted golden element as a named `gap_*` hypothesis (e.g. `NotAStateInstrumentality`, `NotAbsolutelyImmune`).
- **Lane:** Agent SDK batch (gated 2026-06-15 credit; subsumes agent-sdk Phase 2) + manual-interactive bridge via the **`/dau-manual`** skill (`.claude/skills/dau-manual/`; mirrors `/dco-manual`). Mechanical phases in `scripts/dau.sh` (`--pre`/`--permit-fanout`/`--plan-cells`/`--collect`/`--score`/`--report`); LLM fan-out over `.claude/agents/dau-{cell,reconciler,cross}.md`. Zero-prompt fan-out enforced by `scripts/dau.sh --permit-fanout` against `scripts/dau-helpers/required-allow-patterns.txt` (exit 61). Cells write to `pending/uscode-cells/` (sandboxed via `extract_facts.py --sandbox-out`), promoted only after the reconcile gate. **Wave archive (§ 12, implemented 2026-06-01):** at the promotion gate `scripts/dau.sh --archive-wave <wave-id>` (→ `scripts/dau-helpers/archive_wave.py`) freezes the blind sandbox into the gitignored, S3-backed `proving/waves/<wave-id>/` (one immutable dir per fan-out; `WAVE.json` manifest; `/waves/` gitignored + symlinked into worktrees via `proving/.worktree-links`; serving-side S3 class `usc-waves` deferred to `data/claude-updates/serving.md`). The four surviving historical waves are back-filled there; the live `pending/uscode-cells/` sandbox is the ephemeral working buffer, prunable once archived. Spec § 7.5 + § 12; tests `data/specs/axiomatize-uscode-2026-05-29-tests/`.
- **Status:** Phases 0–1 (foundation + conventions/briefings/Common) done. Phase 2 calibration anchor + waves promoted to canonical — approach-B `Proving.USC.<Title>.*` sub-namespaces coexisting with the hand-built anchors. **All three hand-built golden frameworks (RICO / §1981 / Title VI) independently reproduced by blind 10-axis fan-outs** (RICO `T18.Rico*` all four §1962 subsections + §1964(c) standing Tier-A; §1981 `T42.EqualRights` Tier-A; Title VI `T42.TitleVI` Tier-B-modulo, the `gap_*` residuals being judicial doctrine absent from §601 statutory text). 2026-06-04 lane is **opus-locked**; the three re-slices held+archived under `proving/waves/2026-06-04-t{18-rico,42-eqrights,42-titlevi}-opus` (evidence-only, canonical anchors unchanged). Cross-title `dau-cross` Common-collapse landed at `Proving.USC.Common.CrossWaveSpecAlgebra` (a `ProvingUSC` lakefile root) — specialized-axis algebras (scienter/sanction/evidentiary/intertemporal/remedy-standing) collapsed into `Common`. Corpus rollup `proving/coverage.json`. **Per-wave detail (cells, bridge tallies, Tier-A/B/C splits, defect fixes) lives in spec § 10.1 + § 12 + the close summaries — never duplicated here.** Cell Lean files MUST use FULL-path imports (`reference_lean_isolation_probe_full_path_imports`). Authoritative build target is `lake build ProvingUSC` (bare `lake build` is red-by-design on REJECTED examples) — always run it before promoting; never trust a cell's self-reported build. Remaining Phase 2: fan out more sections of titles 18 & 42 (T42 ch21 ~80 non-golden sections, ~13 admin/EEOC §2000e-4/-6/-8..-15; other T18 chapters). Phases 3–4 gated on the 2026-06-15 SDK credit.

## Layout (essentials)

```
proving/
├── Proving.lean                    root module — imports both frameworks
├── lakefile.toml
├── lean-toolchain                  pinned: leanprover/lean4:v4.30.0
├── Proving/<Framework>/{Types,Predicates,Statute,Theorems}.lean
│                                   Facts.lean is GENERATED + gitignored
├── predicates/<framework>/         markdown specs (one per opaque predicate)
├── scripts/
│   ├── extract_facts.py            driver — reads `framework` block from manifest
│   ├── lake_trace.py               two error-line orderings (4.29 vs 4.30+)
│   ├── lean_parse.py               regex-based proof-file structural parser
│   └── uscode.py                   path/text/list lookup against legal/uscode/
└── examples/<id>/                  per-run artefacts (see below)
```

Spec roster: RICO 28 specs (14 common + 4 c + 3 a + 3 b + 4 d), Title VI 17 specs (7 coverage + 2 intentional + 5 disparate-impact + 3 retaliation), CivilRights 14 specs (4 § 1981 + 5 § 1983 + 5 § 1985(3)).

## Workflow

1. **Author the formal framework** (Lean) — for a new framework, add `Proving/<NewFramework>/{Types,Predicates,Statute,Theorems}.lean` and import from `Proving.lean`.
2. **Author predicate specs** under `predicates/<newframework>/`. Spec format is fixed (see `predicates/README.md`).
3. **Run the driver**:
   ```
   python3 scripts/extract_facts.py examples/<id>/complaint.md \
           --manifest examples/<id>/manifest.json --example-id <id> [--build]
   ```
   The manifest's `framework` block selects where Facts.lean is written and which namespace prefix to use. `--build` runs `lake build <proof_target>` and emits `report.json` + `graph.json` + `loci.json` per `data/specs/proving-results-propagation-2026-05-09.md`. The lake target is taken from `manifest.framework.proof_target`. `--reuse-facts --example-id <id>` skips predicate sub-agents and re-emits artefacts from existing `examples/<id>/facts.json`.

4. **Verify**: `lake build`. If succeeds, kernel is well-formed. To verify a specific example proof, elaborate with `lake env lean examples/<id>/proof.lean` once Facts.lean has been generated.

The driver prints one `· <spec> ... <value>  (<uncertainty>)` line per predicate in **all three modes** (`--stub` / `--reuse-facts` / production), interleaved with mode-specific banners. Adapters parsing the stream (e.g. `verifying/server/adapters/proving.py._classify`) can rely on this line shape unchanged across modes.

**`--stub` caveat for REJECTED examples.** `--stub` defaults every predicate to `True`, which on the REJECTED RICO examples overwrites the committed REJECTED reports with synthetic ACCEPTED. Use `--reuse-facts` (replays the committed `facts.json` verbatim) for any UI / regression replay over a REJECTED run. Pinned: `feedback_proving_stub_defaults_true`.

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

**Schema is locked at the consumer boundary.** `verifying/web/public/proof-graph/loader.js` adapts `graph.json` (full-word `kind`, no positions, evidence arrays, string uncertainty) into the kit's renderable shape. Any change to `graph.json` field names or `kind` values is a two-sided edit — bump the spec at `data/specs/proving-results-propagation-2026-05-09.md` § 2.3 and update the loader together. Tests 38 + 41-43 enforce both halves.

**Sibling parity with `accounting/`.** `accounting/scripts/{lean_parse,lake_trace,report}.py` mirror this pipeline for the financial-domain frameworks; `accounting/examples/<id>/graph.json` is byte-compatible with the same `RicoFixture` shape (renders via the kit unchanged). `lake_trace.py` is a verbatim copy across the two trees; `lean_parse.py` and `report.py` share internals (`_strip_block_comments`, `_theorem_signatures`, `_tokenize_term_body`). Patches to any of those MUST be diff-checked against the counterpart before landing. Deliberate divergences live on the accounting side: lowercase axiom names + dotted conclusion heads (multi-judgment runs) and a different `LociRoster` shape — leave those alone.

## What we encode (one paragraph each)

**RICO** (`Proving/Rico/`) encodes § 1961 definitions (enterprise — *Boyle* AIF — pattern, unlawful debt, culpable person), § 1962(c) (operation-or-management per *Reves*), § 1962(a) investment, § 1962(b) acquisition, § 1962(d) conspiracy (*Salinas*), and § 1964(c) standing (*Holmes* / *Anza* proximate cause + 4-year limitations per *Agency Holding* / *Rotella*). Top-level `ValidCivilRicoComplaint` is `inductive` over the four substantive subsections.

**Title VI** (`Proving/TitleVI/`) encodes common coverage (§ 601 + DOJ Manual § V), intentional discrimination (*Sandoval*; direct + *Arlington Heights* + *McDonnell-Douglas*), disparate impact (§ 602; admin-only per *Sandoval*), and retaliation (*Jackson v. Birmingham*). `ProtectedGround` is an `inductive` enum (race/color/nationalOrigin); `JudiciallyEnforceableTheory`/`AdministrativelyEnforceableTheory` as `def`s encode the *Sandoval* split formally. `ValidTitleVIJudicialClaim` is the inductive that omits disparate impact.

**CivilRights** (`Proving/CivilRights/`) encodes § 1981 (racial-class plaintiff incl. *McDonald* reverse-race + *Saint Francis*; *General Bldg. Contractors* intent; *Domino's Pizza* contract identification; **but-for race causation per *Comcast* (2020)**); § 1983 (under-color *Monroe/Lugar/West v. Atkins*; *Gonzaga* federal-statutory rights; § 1983 "person" *Will/Monell/Hafer*; *Mt. Healthy/Monell* moving-force; absence of absolute immunity *Stump/Imbler/Tenney/Briscoe* — qualified immunity NOT decided by predicate layer); § 1985(3) (meeting-of-minds *Twombly* + intra-corporate; class-based animus *Griffin/Bray/Carpenters*). § 1985(1)/(2) NOT yet encoded.

## Adding a new statute / framework

1. Pick the section. Identify its elements.
2. Add `Proving/<NewFramework>/Types.lean` if existing types don't fit.
3. Declare opaque axioms in `Proving/<NewFramework>/Predicates.lean`.
4. Compose as `structure`s in `Proving/<NewFramework>/Statute.lean` (use `inductive` for disjunctive validity).
5. Add `intro_` theorems in `Proving/<NewFramework>/Theorems.lean`.
6. Wire into `Proving.lean`.
7. Author markdown specs under `predicates/<newframework>/` per the contract.
8. Add a sample under `examples/<newframework>-sample/` with a manifest `framework` block.
9. Register a `LociRoster` for each top-level theorem in `scripts/report.py` (mirror RICO subsections at lines ~142-191). Skipping this silently under-reports — `lake build` stays green and `report.json` is produced, but `loci.json` emits a "no roster" placeholder and the status-page locus panel renders empty. Sibling pattern: accounting's `report.py JUDGMENTS` dict has the same gating shape.
10. Update `predicates/README.md` roster + this CLAUDE.md table.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no FFI. Kernel is pure.
2. **Predicate specs MUST NOT cite or read `Proving/<Framework>/*.lean`.** Their world is the complaint text + spec rubric.
3. **The driver MUST NOT make legal judgments.** Add fields to JSON schema or a new `framework` block field rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** Both files are gitignored.
5. **memsearch never indexes `Proving/<Framework>/*.lean`.** Lean files excluded by design (memsearch only scans `.md`/`.markdown`).
6. **Predicates live under `predicates/<framework>/`.** Manifest spec paths use the subdirectory.

## Predicate sub-agent memsearch use

A predicate sub-agent MAY invoke the `memory-recall` skill (which itself runs `context: fork`). Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop hook auto-writes via custom `summarize.txt` template preserving predicate names verbatim). Collection is per-subproject via the patched `lib/memsearch/plugins/claude-code/hooks/common.sh`.

## Toolchain notes

- **Lean** pinned via `lean-toolchain` to `v4.30.0` (current stable; lockstep with `accounting/lean-toolchain` per the root CLAUDE.md single-pin rule).
- **No Mathlib dependency** in initial scaffold — keeps `lake build` fast.
- **Python ≥ 3.10** for the driver (system `python3`, no venv).
- **Claude CLI** must be on `$PATH`.
- **Claude `-p` flag set for predicate sub-agents** — today text-reasoning-only (no Bash). When predicates need external tools (USC lookup, scholar fetches), adopt accounting's flag set + driver-injected "REAL-CALL MODE" preamble per `feedback_claude_p_subagent_real_call_pattern`; without the preamble, haiku sub-agents fall back to stub-mode hallucinations even when the data hub is populated.
- **Model is opus, hard-enforced (not a cost choice).** Production (predicate-invoking) runs of `extract_facts.py` **hard-fail (exit 3)** on any non-opus `QAGENTS_PREDICATE_MODEL` unless `--allow-smoke-model` is passed; `--stub`/`--reuse-facts` are exempt (they never call the model). All axiomatization — hand-built examples + the `dau` USC cell/reconciler/cross agents (frontmatter `model: opus`) — is opus-only by policy (operator directive 2026-06-04). The 2026-06-03 RICO-example haiku-vs-opus bake-off (22 RICO §1962(c) predicates, ungated, only `--model` differs) measured haiku as a **capability constraint for trust**, not just cost: haiku fabricated a "cannot verify the complaint text without reading the allegations" hedge on a complaint it was handed (the text-domain twin of accounting's "missing subcommand"), and that lone high-uncertainty flag landed on the fabrication; opus produced **0** such hedges and flagged `high` only on genuinely-hard calls. The driver carries two guards (`invoke_predicate`, tested by `scripts/test_predicate_guard.py`): **Guard A** rejects+retries a result that claims it couldn't read the complaint or carries no evidence (NOT substantive legal negation — that's a legitimate False here), **Guard B** band-normalizes uncertainty then treats `high` as a review FLAG, never an auto-reject (high is honest on a real knife-edge). See `feedback_predicate_model_opus_not_haiku`.

**Driver smoke-test side effect.** Without `--sandbox-out`, `scripts/extract_facts.py --example-id <id>` overwrites `examples/<id>/{Facts.lean,facts.json,report.json,graph.json,loci.json}` (worktree-absolute paths + fresh `lake build`). Use **`--sandbox-out <dir>`** for any smoke test or axiomatize-uscode cell run: it redirects all per-run artefacts to `<dir>` and restores the canonical `Proving/<Framework>/Facts.lean` after `--build`, leaving the committed tree untouched (verified: `--reuse-facts --sandbox-out` replays a committed REJECTED run into a sandbox with identical verdict, git-clean). `--reuse-facts` reads its source from the committed `examples/<id>/`, independent of `--sandbox-out`. Without the flag and smoking outside `/open proving`: `git checkout -- examples/<id>/` before committing. NOT yet mirrored to accounting's driver (deferred — accounting's `extract_facts.py` still clobbers). Detail + spotter rule: `feedback_driver_overwrites_example_artifacts`.

## Open work

- Sample manifests only exercise one act / one action; complete proofs need per-element calls. Either expand manifest or generalise predicate to accept a list.
- `examples/sample_proof.lean` has one `sorry` for per-act racketeering coverage; `examples/titlevi-sample/proof.lean` has one `sorry` for per-action retaliation coverage.
- Driver now defaults to **opus** (bake-off finding above). The harder predicates (`rico/continuous`, `rico/proximate-cause`, `titlevi/intentional-discrimination`, `titlevi/adverse-disparate-impact`) benefit most. **`rico/is-racketeering-activity` is a measured rubric-hardening target** — the bake-off showed it noisy per-act (haiku↔opus disagreed 6/22 on it, and even haiku↔haiku run-to-run differs), the proving analog of accounting's macd knife-edge. The verdict stays robust (the load-bearing `culpable-person` + `proximate-cause` rejections agree across models), but the rubric should pin the §1961(1)-enumeration + Rule 9(b) + federal-proceeding-nexus tests so the per-act Bool stops drifting.
- No `LociRoster` is registered for the Title VI / CivilRights subsections — their `loci.json` emit as "no roster" placeholders (0 nodes). Only RICO subsections produce a populated loci diagram. Adding rosters would make those status-page panels render.
- **Title IX golden is kernel-only** (added 2026-06-05). `Proving/TitleIX/{Types,Predicates,Statute,Theorems}.lean` is hand-built + kernel-green + sorry-free + wired into the `Proving` lib, and serves the calibration golden-bridge role. The remaining "Adding a new statute / framework" steps to make it driver-operational are open: predicate specs under `predicates/titleix/` (one per opaque predicate), an `examples/titleix-sample/` manifest + sample, and a `LociRoster` in `scripts/report.py`, plus the `predicates/README.md` roster row. None are needed for its golden-reference (bridge target) role.

## Proof-graph visualisation prompts (migrated → `visualizing/graphs/`)

The proof-graph render-design prompts (predicate-pill / axiom-rectangle / theorem-hexagon node contract, four edge kinds `applies` / `composes` / `inhabits` / `disjunctionCase`, keyed off the Doe v. Acme § 1962(c) fixture) **moved to `visualizing/graphs/` on 2026-06-03** under the consolidation in `data/specs/visualizing-2026-06-03.md` — `proving/` is Lean + Python only; the rendering design belongs to `visualizing/` (which now owns the unified kit). The locked 3-class / 4-edge contract is reproduced in that spec § 4; the `Failure` wiring shape lives at `visualizing/graphs/02-debug-overlay.prompt.md` § "Wiring contract".

`proving/`'s only obligation is the **cross-subproject JSON seam, unchanged**: the audit-JSON / `graph.json` v1 shape from `scripts/extract_facts.py` (schema `data/specs/proving-results-propagation-2026-05-09.md` § 2.3) plus that `Failure` shape. `verifying/web/`'s `/proof-graph/02-debug/` route consumes it to surface *which* predicate Bool blocked *which* intro rule's hypothesis — distinguishing substantive negative findings (predicate-False) from verifier-quality issues (predicate-Undecided) from kernel term bugs (kernel-error).

## Status emit (`data/status/proving.json`)

`proving/scripts/status_emit.py` (system `python3`, no venv) writes `data/status/proving.json`. Schema lives in `@qagents/diagram-kit` v0.4.1 (sweep `KIT_VERSION` in lockstep on bumps). Surface (aggregates from `examples/*/report.json`):

- **`framework-roster` `DiagramEmit`** (summary card) — one node per Lean module.
- **`run-stats` `KpiStripEmit`** + 4 `StatCardEmit`s — totals, accepted, rejected, latest-run age. Status pill turns OK when a run is observed in the last 7 days.
- **`recent-runs` `TableEmit`** — last ≤ 10 runs sorted by `runFinishedAt`; expand row enumerates each kernel rejection's locus.
- **Latest-run loci `DiagramEmit`** — embeds `loci.json` verbatim.
- **`predicate-roster-latest` `TableEmit`** — per-predicate atomic view, grouped by subsection.
- **`live.metrics.latestProofGraphUrl`** points the deep-page card at `qnarre.quantapix.com/proof-graph/run/<id>/[debug/]`.

`panels[]` declares deep-page render order: framework-roster → kpiStrip → recent-runs → latest-run loci → predicate-roster-latest. Producer never reads Lean files directly — walks `examples/*/report.json` + (for the loci diagram) `examples/<latest>/loci.json`. The "latest" anchor (loci diagram, predicate roster, latest stat card, `live.metrics.latestRun*`) prefers the most recent run with a non-empty `complaint.docket` so a toy regression fixture (e.g. `sample` / `titlevi_sample`) cannot displace a docketed verification; `recent-runs` table still shows every run. Falls back to absolute latest if no docketed run exists.

**Two-lane writer (cron + manual)** per `data/specs/data-conventions-2026-05-06.md` § 5.3. Branches on `QAGENTS_PENDING_ROOT`: cron lane writes `${QAGENTS_PENDING_ROOT}/data/status/proving.json` and never touches the lock; verifier subagent + `data/schedules/launchd/verify-pending.sh` rsyncs into canonical under the lock. `verify-pending.sh` rejects (exit 7, before lock acquisition) any pass-list `path` missing the `pending/` prefix — canonical destination is always `${path#pending/}`, so a prefix-less emit is a hard fail rather than a destructive rsync that wipes canonical (closes the 2026-05-18 06:00 incident; commit `3350cdb`). Manual lane acquires the root-anchored `.data-write-lock` via atomic `O_CREAT|O_EXCL`, writes canonical, releases on exit. Both lanes write atomically (`<path>.json.tmp` then `os.replace`). Orchestrator: `scripts/build-status-all.mjs`.

**Cron schedule** registered as `com.qagents.proving-status-emit` in `data/schedules/launchd/install.sh`'s `ROUTINES` array (`proving:status-emit:05:30:0,1,2,3,4,5,6` — daily at 05:30 local, 30 min before managing's 06:00 daily). `status-emit` is a script-direct routine in `run_routine.sh` — no Claude invocation. Re-run `--enable` after editing `ROUTINES` to materialise the LaunchAgent plist. The cron-EC2 lane (`data/specs/cron-ec2-migration-2026-05-19.md`) moves this firing onto EC2; operational concerns route to `data/specs/serving-2026-05-26.md § 10 Phase 7`. The script itself stays unchanged — the migration is transport-only.

## Redaction (`scripts/redact_complaints.py` + `scripts/redact_artefacts.py`)

**Two-stage, source-first (since 2026-06-04).** The durable fix is upstream: `scripts/redact_complaints.py` redacts the SOURCE `examples/*/complaint.md` (the ground truth predicate sub-agents read) to the **uniform-strict / FBI-director-letter standard** — keep every `X v. Y` legal citation + government bodies; scrub every personal name to a neutral role placeholder + all private medical entities + all residential addresses. Because the source is clean, a fresh `--build` CANNOT re-leak whatever a sub-agent quotes. It covers every example complaint. It is idempotent and **self-auditing**: a case-insensitive DENYLIST + honorific-residue scan (caught the uppercase `¶8.x` party block + a counsel email that a case-sensitive pass missed). `scripts/redact_artefacts.py` remains the downstream belt-and-suspenders over generated artefacts.


Predicate sub-agents quote `complaint.md` + `manifest.inputs.*` verbatim into evidence strings, which flow through `examples/<id>/{facts,report,graph,loci}.json` + `Facts.lean` → `status_emit.py` → public status page. This is a **separate channel** from `documenting/scripts/check_redactions.py` (which sweeps the private redaction staging tree); the PDF gate does not see proving/'s JSON outputs.

`scripts/redact_artefacts.py` is a deterministic literal-substring + regex cleanup pass over the generated artefact set — the downstream belt-and-suspenders behind the source-first redaction. Real names + addresses + counsel + judicial officers + the private medical entities and their officers replaced with neutral placeholders. Idempotent; re-runnable. For already-verified runs, surgical text-substitution preserves Bool/uncertainty audit integrity and skips a ~24-predicate × 2-subsection Haiku rerun.

**Caveat for fresh `--build` runs**: predicate sub-agents quote whatever `complaint.md` holds, so the source must be pre-redacted — run `scripts/redact_complaints.py` (above) before any fresh derivation. Note the public court-filing PDFs are NOT a safe text source: `fitz` extracts the text layer *under* the graphical redaction boxes (the names survive — `feedback_graphical_redaction_failure_modes`). Byte-form / JSON-escape-depth implementation detail of the artefact pass lives in `reference_proving_redact_artefacts_script.md`.
