# accounting — Lean4 axiomatic theorem-proving for portfolio evaluation

Cross-project rules: `../CLAUDE.md`. The **numerical axis** of the three-kernel Lean4 architecture (root CLAUDE.md § "Lean4 axes"; `data/charters/studying/specs/lean4-charter-2026-06-10/SPEC.md` § 4); `/dat` is its instance of invariant 3 (top-tier LLMs in parallel, never manual). Scope charter: `data/charters/accounting/numerical-axis/CHARTER.md` (the `axiomatize-trading-2026-05-30` family is scope-resident there as an `owner-living-program`; domain-vs-mechanism carve in its § 3).

The financial-domain parallel of `proving/`. Same three-layer split, different domain: instead of complaints under federal statutes, accounting/ proves portfolio-level judgments (the five frameworks below) over OHLCV bars + indicator series + GICS sector mappings.

## The split (mirror of proving/)

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Accounting/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one portfolio JSON + bar/indicator evidence (via `scripts/data_view.py`) | a single `Bool` (plus evidence + uncertainty) | Claude Code sub-agent (`context: fork`); MAY use memsearch's `memory-recall` skill. |
| **Driver** | `scripts/extract_facts.py` | manifest + portfolio | `Accounting/<Framework>/Facts.lean` (axioms) + audit JSON | `claude -p` invocations; model resolved via the shared `code/lean_tools/model_floor.py` seat (top-tier default — Hard rule 7). |

The verifiable proof (the kernel/predicate/driver layering is enforced by the split table above + hard rules 1–3) IS the Lean elaboration trace produced by `lake build`.

## Frameworks

Each framework lives under `Accounting/<Framework>/` (kernel) + `predicates/<framework>/` (specs). Adding a new framework is a parallel exercise — see "Adding a new framework" below.

| Framework | Kernel | Specs | Top-level judgment(s) | Predicate count |
|---|---|---|---|---|
| **Trend** | `Accounting/Trend/` | `predicates/trend/` | `is_uptrend`, `is_downtrend` | 5 (sma_cross_up, slope_positive, r_squared_geq, adx_geq, volume_confirmation) |
| **Momentum** | `Accounting/Momentum/` | `predicates/momentum/` | `has_momentum` | 4 (rsi_in_range, macd_bullish_cross, roc_positive, momentum_percentile_geq) |
| **OptionsRisk** | `Accounting/OptionsRisk/` | `predicates/options-risk/` | `defined_risk_only`, `is_clean` | 6 (leg_allowed, covered_call_collateralized, protective_put_bounded, no_naked_short_options, debit_only, max_loss_bounded) |
| **Sector** | `Accounting/Sector/` | `predicates/sector/` | `has_violation`, `no_violations` | 3 (cap_respected, gics_mapped, sector_concentration_leq) |
| **Drawdown** | `Accounting/Drawdown/` | `predicates/drawdown/` | `drawdown_disciplined` | 3 (max_drawdown_leq, time_under_water_leq, recovery_within) |
| **Regime** | `Accounting/Regime/` | `predicates/regime/` | `regime_trending`, `regime_ranging`, `regime_high_vol`, `regime_compressed` (non-exclusive per-SYMBOL preconditions; each carries a `_refute` dual) | 11 (adx_trending_geq, adx_ranging_lt, above_sma200, faber_10m_invested, ma_slope_up, chop_leq, chop_geq, natr_pctile_geq, rv_pctile_geq, squeeze_on, squeeze_fired) |
| **ExitDiscipline** | `Accounting/ExitDiscipline/` | `predicates/exit-discipline/` | `exit_disciplined` (per-POSITION over `Holding`; four fired-signal prongs are REQUIRED NEGATIONS; `_refute` + per-signal `_refute_<sig>` duals; `time_stop_geq` standalone) | 6 (below_chandelier, sar_flip, supertrend_flip, donchian_exit_n, stop_distance_bounded, time_stop_geq) |
| **Debate** | `Accounting/Debate/` | — (specs pending, Phase 4) | `admissible_long` | see § Axiomatize-trading (bull-vs-bear gate) |

Two distinct evaluating-side lockstep contracts (verified 2026-07-16): a predicate RENAME must update `evaluating/web/src/islands/QresevApp.tsx` (the hawk Lean trace is embedded verbatim in its trace block); a framework ADD sweeps `FRAMEWORK_META` (`evaluating/web/src/lib/frameworks.ts`) + `EXPECTED_FRAMEWORKS` (`evaluating/web/tests/e2e/frameworks.spec.ts`) — QresevApp receives the roster as a prop, never QresevApp.tsx.

**Chartered expansion 6→11** (adopted 2026-07-12): Regime, Breadth, MeanReversion, ExitDiscipline, Hedging + extensions to Trend/Momentum/Sector/Drawdown/Debate — `data/specs/accounting-charter-expansion-2026-07-12/SPEC.md` (its § 6 Phases ledger is the landing record of truth). **P1 + P2 SHIPPED** (P1 2026-07-12: `data_view.py ta --cols` per-predicate widening gated by the closed `TA_V2_LANDED` registry — contract `predicates/README.md` § "ta-schema-v2 evidence columns" — + the `--veto-screen` `mdd252` rebase; P2: Regime 2026-07-13 + ExitDiscipline 2026-07-16, both kernel-first with real-tape positive/`refuses_` goldens, S-C2 gate green, family t_05/t_06; roster + judgment shapes in the Frameworks table above). **Next: P3 Hedging computable-now six (beta-sizing first;** θ from per-PM `risk_policy.md` YAML, never report constants). ExitDiscipline gotcha pinned in its specs: Donchian exits read the PRIOR-bar channel — an inclusive-window column can never be penetrated by its own bar's close (LEARNINGS ADOPT-SHARED). **Emit-enablement deferred** (kernel-first-without-UI is the supported state, § 2.2 principle): `report.py` LociJudgment/AXIOM_CITES + report/graph/loci.json for the regime + exit-discipline goldens + evaluating `FRAMEWORK_META` ride ONE sweep (kit union widened 2026-07-13; the accounting/evaluating legs remain — next-steps item 2). P6 BOUND on the K-C4 provenance ruling. Binding at adoption: `repair_structure_ok` refused by name (MF-3), no `sma50_gt_sma200` (family `tests/` t_01/t_02/t_03).

## Layout

```
accounting/
├── CLAUDE.md · NEXT_STEPS.md · .memsearch.toml · .worktree-links
├── lakefile.toml · lean-toolchain (pin matches proving/) · Accounting.lean · examples.lean
├── coverage.json                  universe-program rollup (trading-coverage/1; single owner of tier/encoded counts)
├── Accounting/
│   ├── Common/                    Types · Bar (canonical {ts,o,h,l,c,v,adj_c}) · Tactic (prove_element)
│   ├── {Trend,Momentum,OptionsRisk,Sector,Drawdown}/   Types · Predicates · Statute · Theorems · Hier/ · (Facts — generated, gitignored)
│   ├── Debate/                    6th framework — bull-vs-bear gate (§ Axiomatize-trading)
│   └── Universe/                  per-sector slices S<code> + Reconciled (AccountingUniverse lakefile roots)
├── predicates/                    README.md (contract + roster) + one dir per framework (+ hier/) + universe/
├── scripts/                       extract_facts.py · data_view.py · build_examples.sh · {lean_parse,lake_trace,report}.py ·
│                                  status_emit.py · dat.sh + dat-helpers/ · targeting ({sector_rank,confluence_prescreen,veto_screen,frontier}.py) ·
│                                  validate_common_mints.py · coverage_parity.py · universe_graph.py · test_predicate_guard.py  (bridge scorer = shared code/lean_tools/score_bridge.py)
├── examples/                      sample dirs — goldens (single_ticker/hawk/balance/anchor), options audits, hier decompositions; each = portfolio+manifest+setup+proof+{facts,report,graph,loci}.json
├── emits/lean_graph/              quantify-progress numerator + domain graph (generated)
└── waves/                         gitignored + S3-backed blind fan-out archives (§ Wave archive)
```

## Workflow

1. **Author the formal framework** (Lean) — for a new framework, add `Accounting/<NewFramework>/{Types,Predicates,Statute,Theorems}.lean` and import them from `Accounting.lean`.
2. **Author predicate-function specs** — one markdown file per opaque predicate, under `predicates/<newframework>/`. Spec format is fixed (see `predicates/README.md`). Each spec is the system prompt for its sub-agent.
3. **Run the driver** against a portfolio:
   ```
   python3 scripts/extract_facts.py examples/hawk_sample/portfolio.json \
           --manifest examples/hawk_sample/manifest.json \
           --example-id hawk_sample [--stub]
   ```
   The manifest's `framework` block selects where Facts.lean is written (e.g. `Accounting/Runs/HawkSample/Facts.lean`) and which namespace prefix to use.
4. **Verify**:
   ```
   lake build
   ```
   Then `lake env lean examples/<id>/proof.lean` to verify the per-example proof. If `lake build` succeeds, the kernel is well-formed; if the example proof elaborates, the portfolio formally satisfies the chosen judgments *given* the predicate-function outputs.

## Adding a new framework

Full 11-step procedure → `predicates/README.md` § "Adding a new framework" (the declared spec-format home): kernel scaffold, `Accounting.lean` wiring, per-axiom specs, `examples/<newframework>-sample/`, and the README-roster + this-file-table + `evaluating/web/src/lib/frameworks.ts` `FRAMEWORK_META` sweep.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no `IO.Process.run`, no FFI. The kernel is pure.
2. **Predicate specs MUST NOT cite or read `Accounting/<Framework>/*.lean`.** Their world is the portfolio JSON + bar evidence + spec rubric.
3. **The driver MUST NOT make financial judgments.** It only routes calls and serialises results. Add fields to the JSON schema (or a new `framework` block field) rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** All `Accounting/<Framework>/Facts.lean` are gitignored.
5. **Defined-risk only — non-negotiable.** Any options leg outside the SIX root-chartered strategies (root CLAUDE.md § Defined-risk options) is REFUSED at the predicate layer. The kernel encodes the same restriction at the type level via the closed `Accounting.Strategy` enum. Both must remain in force.
6. **Bar shape canonical.** Any code that reads parquet uses the `{ts, o, h, l, c, v, adj_c}` columns; vendor names (Alpaca's `t`, etc.) never leak past `scripts/data_view.py`.
7. **Axiomatize with the top-tier model only.** Every LLM-backed extraction that produces a kept/committed result — the `extract_facts.py` driver AND the `dat-{cell,reconciler,cross,debate}` fan-out agents — runs on the latest top-tier model; haiku is forbidden for any retained artifact. Model resolves from the ONE shared seat `code/lean_tools/model_floor.py` (`QAGENTS_AXIOMATIZE_MODEL`; legacy `QAGENTS_PREDICATE_MODEL` honored second, raise-only — root § Model policy). The anti-poison guard (`_protocol_violation`) rejects + retries number-less evidence and raises if persistent; wave archives stamp `"model"`. Bake-off rationale + gate: memory `feedback_predicate_model_opus_not_haiku`.
8. **Blind-fanout confluence is the ONLY correctness oracle — and it has FOUR leak channels** (2026-07-14; runtime + architecture properties, shared by all three axes). (a) *Filesystem (write):* the runtime hands every subagent the **same** writable session scratchpad — **not** per-cell — and its system prompt actively tells agents to use it. All cell scratch goes under its own disjoint `<out>/.scratch/`. (b) *Orchestrator:* stating a substantive finding in a fan-out prompt destroys blindness just as thoroughly — **name the METHOD, never the ANSWER**; adjudications belong to the **reconciler**, never the cells, and reporting the resulting "convergence" is an **echo of your own prompt**. (c) *The READ side — the one that actually fired:* (a) relocates *writes*; **blindness is a READ property**. Cells fan out concurrently into one worktree, sibling quartets sit under `pending/trading-cells/`, and the allow-list grants `Bash(grep|cat|ls|find)` + `Read(qagents-wt/**)` — a root-level `grep -r` lands in a sibling's work **by accident**, no rule broken, nothing logged. The read rule *already existed* in `dat-cell.md` and **nothing enforced it** — a rule is a promise. Incidental vectors count: root sweeps, `git status`/`diff`, and frozen `waves/<id>/` archives (a prior wave's answers, displaced in time). (d) *memsearch recall:* indexes daily logs carrying prior reconciler adjudications — a cross-**run** leak that survives every filesystem fix. **Banned for cells.** Both (a)+(b) voided a full day on the textual axis (~3M tokens) — the encodings were green, sound and defensible, which is exactly why an oracle bug is worse than an input bug: **it is invisible in the output.** Remedy for any breached wave is a fresh blind **re-slice** — you cannot re-certify an *agreement* metric by attacking or re-scoring it. Contracts: `.claude/agents/dat-{cell,reconciler,debate}.md`; memory `feedback_blind_fanout_oracle_channels`; open work: ns-13/ns-14.
9. **A green build is not proof — `autoImplicit` must stay OFF.** `lakefile.toml` sets `autoImplicit = false, relaxedAutoImplicit = false` on both kernel `lean_lib`s (`Accounting`, `AccountingUniverse`). With it ON, an unqualified `Common` type (no `open Accounting.Universe.Common`) is silently bound as a **phantom implicit type variable**: the module builds green while its axioms range over an invented type and mean nothing — and a **bridge between two phantom-typed composites discharges vacuously**, so any Tier-A resting on it measured *nothing* (not "mis-measured" — **unfounded**). Never remove the option to make a file pass. *(Audited 2026-07-14 at the 4.32 bump: accounting had the hole but **zero** actual violations — all 135 jobs green under the guard, so no accounting tier is phantom-founded. Unlike proving, which had 17 such files.)*

## Cross-project boundaries

- **OHLCV bars** — read via `scripts/data_view.py` from the shared `financial/parquet/ohlcv-equities/<SYM>.parquet` hub. Do NOT import `analyzing/`'s TypeScript DuckDB views or `trading/`'s `shared.lib` Python directly.
- **Indicator math** — `analyzing/scripts/ta_reference.py` (Python TA-Lib) is the ground truth. Predicate sub-agents MAY shell out to it as a Python escape hatch (per qagents/CLAUDE.md "Language split"). TA outputs land at `financial/parquet/ta-reference/<SYM>.parquet`.
- **GICS sectors** — `financial/parquet/gics-symbols.parquet` (read via DuckDB or via `python -m shared.lib.gics lookup` as a shell-out).
- **Downstream consumer** — `evaluating/web` (Qresev) calls `accounting/scripts/extract_facts.py` as a subprocess via `evaluating/server`; never imports `Accounting/<Framework>/*.lean` directly.
- **Financial sign-off** — `accounting/` **advises** the FINANCIALLY-CLEARED gate (framework/kernel verdicts) but is **not** the grantor; `evaluating/` is the sole grantor (`data/specs/evaluating-financial-signoff-2026-06-24/SPEC.md`).

## When a predicate sub-agent uses memsearch

A predicate sub-agent MAY invoke `memsearch:memory-recall` (`context: fork`, nested isolation) for prior thresholds / refusals / sector-cap calls. Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop-hook-written); the collection is scoped to this subproject by the patched `lib/memsearch/plugins/claude-code/hooks/common.sh`.

## Toolchain notes

- Lean pinned via `lean-toolchain` (matches `proving/`). No Mathlib dependency — add only if a future predicate composition needs real-analysis or measure-theoretic kernels.
- **Lean4 authoring gotchas** (bit proving's remedy-axis work; apply when adding `inductive`/`structure` kernels per "Adding a new framework"): `private` is reserved — it can't be an `inductive` constructor name (use `privateRight`-style); and a `: Prop` structure can't carry Type-valued (data) fields — put enforcer/classification data in `def`s, not Prop-structure fields. See memory `reference_lean4_keyword_collisions`.
- `scripts/data_view.py` is pandas-only (via root venv `[analyzing]` extras for pyarrow); no duckdb dependency.

**Driver smoke-test side effect.** `extract_facts.py` against an existing `examples/<id>/` overwrites all five artefacts in place by default — `git checkout -- examples/<id>/` before commit, or pass `--sandbox-out <dir>`. Detail: memory `feedback_driver_overwrites_example_artifacts`.

**Driver CLI surface — parity with proving's.** `extract_facts.py` carries `--reuse-facts` (re-emit from committed `facts.json`, no sub-agent calls), `--build`, `--sandbox-out`. **`--stub` is value-faithful** with `--example-id` (seeds canned values from `facts.json`); guard `t_08_stub_facts_faithful.sh` + memory `feedback_lean_toolchain_bump_verify_example_proofs`. **D8 timeout hardening (2026-07-12):** claude + lake subprocesses bounded (`DAT_CLAUDE_TIMEOUT_S`/`DAT_LAKE_TIMEOUT_S` test overrides); TimeoutExpired = retryable failed attempt, never raw propagation; late failure preserves paid results (sandbox `facts.json` / committed `facts.partial.json` sidecar); lake timeout → exit=124 through the normal REJECTED line (adapter shape stable); NO stub-refusal (deliberate divergence from proving — t_08). Guard `t_37_driver_timeout_hardening.sh`.

## Results propagation — `scripts/{lean_parse,lake_trace,report}.py`

Mirror of proving/'s propagation pipeline (`data/specs/proving-results-propagation-2026-05-09/SPEC.md`), adapted for the multi-judgment accounting case. Each `extract_facts.py` run produces three extra audit files under `examples/<id>/`:

- **`report.json`** — per-run join of facts + kernel verdict: `judgments[]` (top-level theorems exercised), `predicates[]` (per-fact roster: axiom binding, evidence, uncertainty, framework cite), `kernel.errors[]` (per-error `introRule.introField` locus joined to `axiomName` via positional intro-rule args).
- **`graph.json`** — proof DAG, byte-compatible with verifying/'s proof-graph kit `RicoFixture` shape (nodes per predicate-application/axiom/theorem; edges `applies`/`composes`/`inhabits`).
- **`loci.json`** — single `DiagramEmit` for the status hub: one root portfolio node, one sub-tree per top-level judgment, one rectangle per kernel-required element coloured by verdict.

Pipeline modules:
- `scripts/lean_parse.py` — regex-based Lean4 reader. Parses `axiom <name> : Prop` (snake_case names), `theorem <intro_*>` intro rules, and term/tactic-mode proof theorem bodies. Returns line-numbered records.
- `scripts/lake_trace.py` — verbatim copy of proving's `lake_trace.py`. Parses `lake build` / `lake env lean` stderr into typed `LakeError` records (type-mismatch, application-type-mismatch, kernel-error).
- `scripts/report.py` — pure data composer. Carries the `LociJudgment` roster (one per top-level kernel `def`/`structure`; 13 wired — the roster in `report.py` is the single owner) and the `AXIOM_CITES` map (predicate-axiom → framework label, e.g. `cap_respected` → `SECTOR`).

**Diff-check obligation against `proving/`.** `lake_trace.py` is a verbatim copy and MUST be patched in lockstep across the two trees. `lean_parse.py` and `report.py` share internals (`_strip_block_comments`, `_theorem_signatures`, `_tokenize_term_body`) with proving's counterparts — diff-check before patching either side. Deliberate accounting-side divergences (lowercase axiom names, dotted conclusion heads for multi-judgment runs, the multi-judgment `LociRoster` shape) are not drift — preserve them.

The driver invokes `lake build <proof_target>` (resolved from the manifest's `framework` block, e.g. `examples.hawk_sample.proof`) after writing the per-run `Accounting/Runs/<RunName>/Facts.lean` — NOT `lake env lean <file>` (the build form compiles transitive deps, so the emitted Facts.lean elaborates without a prior manual `lake build`). Pass `--no-report` to skip the build+emit phase (raw facts.json only). Pass `--portfolio-label <name>` to set the loci diagram's root-node label (defaults to the portfolio JSON's `name`, title-cased).

## Landed mechanisms & patterns (v1 notes)

- **CapPolicy.** `Accounting.Sector` is parametrised over `CapPolicy := GicsSector → Float` (`{has_violation,no_violations}_under p policy`; `Sector/Policies.lean`; portfolio-only forms = `defaultPolicy` 0.30 defeq specialisations); only the *concentration* (weight) cap is policy-parametrised — see § Axiomatize-trading for the universal drawdown veto.
- **Real-call flip pattern.** Mixed real/stub per run via `inputs.stub: true` per-call override; real `claude -p` calls need all four driver pieces (`--allowed-tools "Bash Read"`, `--permission-mode bypassPermissions`, `--add-dir $ROOT`, anti-poison preamble). Brand-anchor = `balance_sample`. Detail: memory `project_accounting_subproject` + `feedback_claude_p_subagent_real_call_pattern` + `accounting/NEXT_STEPS.md`.
- **Example proofs build target — `scripts/build_examples.sh`.** Bare `lake build` builds only the always-green libs (`Accounting` + `AccountingUniverse`); the `examples` lean_lib is NOT a default target (each `proof.lean` imports a gitignored ephemeral `Accounting/Runs/<X>/Facts.lean`, Hard rule 4, absent from a clean checkout). `build_examples.sh` is the green-everything command: regenerates every example's Facts.lean from committed `facts.json` (`extract_facts.py --reuse-facts --no-report`, deterministic, REPO-RELATIVE so the committed copy stays byte-identical) then builds libs + examples; `--regen-only` skips the build. (A single example still verifies via `lake env lean examples/<id>/proof.lean` once its Facts.lean exists.)
- **Hierarchical predicates.** Status of record: `../studying/representation.md` § 13.4. Accounting-local invariants: `Accounting/Common/Tactic.lean` (`prove_element`, Mathlib-free) stays diff-locked with `Proving/USC/Common/Tactic.lean`; decompose-by-default per `predicates/README.md` bullet 7; measurement leaves close via the explicit term `<f>_intro m h (by omega)`, never `prove_element`; flat goldens + QresevApp stay byte-stable. Shape taxonomy + scale rules: hierarchical-predicates spec § 5/§ 11/§ 15; tests D16–D23 + D28–D32.

## Axiomatize-trading program (financial parallel of proving's axiomatize-uscode)

Spec: `data/charters/accounting/specs/axiomatize-trading-2026-05-30/SPEC.md`. Extends the five hand-built frameworks to a phased, **sector-by-sector** program over the S&P 500, produced redundantly by top-tier-model subagent teams along the ≥5 orthogonal **signal-family** axes (§ Axis set below), then reconciled. Cross-axis agreement proved in-kernel via `Bridge.lean` lemmas IS the correctness signal — the TA **confluence** heuristic. Tier-A = ≥3 axes' directional encodings bridge sorry-free.

- **Slice unit:** the `(GICS sector, axis)` cell; sector code → namespace `Accounting.Universe.S<code>` (`S45` = Info Tech, the `T18` analog). GICS is the drill-down spine. Corpus = the existing `financial/parquet/` hub (`financial/gics/build.py --categorize` → `categorization.json`).
- **Golden reference:** the existing 5 frameworks on `examples/{single_ticker_sample,hawk_sample,balance_sample}/`, scored via golden-bridges (NOT exact-string — naming is a free variable, per the uscode 2026-05-29 lesson).
- **Debate framework:** a NEW 6th framework `Accounting/Debate/` formalizes `trading/`'s bull-vs-bear gate "proven at every step". `admissible_long` is a `structure` (no field omittable) requiring bull confluence + kernel directional accept + `defined_risk_clean` + the **negation of every bear disqualifier** (volume divergence / volatility veto / overextension) — "veto, not a vote" as a type-level property. The consumer wire — `debate.py gate --lean-proof` elaborating `intro_admissible_long` so every `evaluate_gate` refusal maps to a non-elaborating proof — is Phase 4, not yet landed (`debate-2026-05-30/SPEC.md` § 11).
- **Lane:** `/dat-manual` (Max-20x interactive) is the standing lane; the SDK batch lane (spec § 7.3) is deferred (root CLAUDE.md § Agent SDK lane owns status). The skill (`.claude/skills/dat-manual/`; mirrors `/dau-manual`) runs Slice + Reconcile + Debate; mechanical phases in `scripts/dat.sh`, LLM fan-out over `.claude/agents/dat-{cell,reconciler,cross,debate}.md`. Zero-prompt enforced by `dat.sh --permit-fanout` vs `scripts/dat-helpers/required-allow-patterns.txt` (exit 61); cells write sandboxed `pending/trading-cells/`, promoted only post-reconcile. The bridge scorer is the **shared** `code/lean_tools/score_bridge.py` (invoked `--root accounting --lexicon confluence`; the accounting fork was retired per C5, mirroring proving's C19 — diff-check-lockstep now applies only to `lake_trace.py`). **Calibration integrity (mirrors `/dau`):** never hand-patch a blind cell/bridge to manufacture agreement — fix the ground-truth defect and re-run blind; blind agreement is the only oracle (memory `feedback_dau_gap_clear_blind_reslice_not_handpatch`).
- **Status (durable state).** Canonical (operator-approved): `Accounting.Universe.Common` (collapse-bridged shared predicates, sorry-free) PLUS per-sector slices `Accounting.Universe.{S<code>.*, Reconciled.S<code>}` — explicit AccountingUniverse lakefile roots; `lake build AccountingUniverse` green, golden `Accounting` unaffected. Accepting Debates accumulate by symbol; veto refusals are correct outcomes (veto, not a vote). The drawdown veto (`max_drawdown_leq 0.15`) stays a **universal** defined-risk bound, NOT a CapPolicy trigger (§ Open work / CapPolicy). **Three-stage deterministic targeting** before any fan-out: `dat.sh --sector-rank` (11 ETFs by 126d RS vs SPY) → `--prescreen` (Trend∧Momentum survivors; `--check-universe` R4 guard exit 15) → `--veto-screen` (252d MaxDD ≤0.15 ∧ ATR-frac ≤0.05 — the actual Tier-A gate); `--frontier` joins all three; `--plan-cells <sector> --symbols <survivors>` targets waves. Per hard-rule-4 the per-run Debate `Facts.lean` stays generated; acceptances reproduce from the committed Reconciled tier + archived wave. Per-wave verdicts + Tier-A set + targeting/tape detail: memory `project_accounting_subproject` + close summaries + spec § 6.5/§ 11/§ 13 + `data/debates/axiomatize-method-2026-06-09.md`.
- **Cadence plan (2026-07-10; LIVE since W0 2026-07-11).** `data/charters/accounting/specs/axiomatize-trading-2026-05-30/dat-cadence-scaling-2026-07-10/SPEC.md` — the Phase-4M analog with the domain INVERTED: accounting is demand-constrained (the tape gates admission, not agent capacity), so it schedules detection+response, never capacity. G0 deterministic tape-refresh + `--frontier` gate (0 LLM; Tue/Fri + every session open; Friday tape current through Sunday; ingest **exit 3 = INV-H truncated-tape abort — never success, never retried past**, spec § 9.7; the frontier read is honest only with the promoted set pinned — since 2026-07-12 `dat.sh --frontier` defaults `--promoted`/`--promoted-names` from the rollup `coverage.json` and resolves the root venv itself, so the bare wrapper IS the G0 verb; an explicit flag overrides) → breadth wave ≤2 trading days from a TIER-A-ELIGIBLE flip (batch everything actionable into ONE wave/tape) → depth increment otherwise (D1–D4 measurement leaves, then structural LEARNINGS adoptions + the `/2` migration). Model/effort matrix § 6 (targeting = Tier-0/free; cells Opus-high; reconcilers Opus-xhigh; Fable only as the differential probe on burst waves); paste-ready `PROMPTS.md` P0–P8. Never chase the numerator — Tier-A count is a tape outcome; the controllable metrics are detection/wave latency, depth coverage, gate greenness.
- **Wave archive (§ 12).** Blind fan-out sandboxes freeze to gitignored + S3-backed `accounting/waves/<wave-id>/` via `dat.sh --archive-wave` → `dat-helpers/archive_wave.py` (+ `WAVE.json`, `corpus_pin` = `categorization.json` `as_of`); `/dat-manual` Step 7 archives BEFORE promote/hold (test `t_07_archive_wave.sh`). Port of proving's `/waves` — **diff-check both `archive_wave.py` in lockstep.** S3 class `trading-waves` (`serving/scripts/archive-artifact.sh`).
- **Axis set (§ 6.2).** `DEFAULT_AXES` = 5 core + instrument-risk + liquidity (**7 per no-flag slice**); `CORE_AXES` stays the 5 the Tier-A ≥3-directional-quorum references (corroborators don't add to the quorum). Axes 8 Seasonality + 9 RiskQuantum **deferred**. Liquidity corroborator (`Tradable m` from `data_view.py bars`, failure = `bear_untradeable`): spec § 6.2 + `predicates/universe/_axes/liquidity.md`.
- **S3 backup MANDATORY per `/dat-manual` (operator standing rule).** Every invocation ends `dat.sh --archive-wave <wave-id> --push` — never archive-only (exit 14 if aws-vault locked; unlock + re-run). Catch-up `dat.sh --push-all [--verify]` (one MFA, idempotent, content-addressed); `--push-if-warm` is the SDK-lane default, manual keeps bare `--push`. Parity with `dau.sh` (`t_09_push_lane.sh`).
- **Progress visualization.** "How much is axiomatized" = per-axis **domain graph** (Half A, denominator) × the shared **Lean4-derivation graph** (Half B, numerator). Half B producer = shared `code/lean_graph/` (`qagents.lean_graph`); `accounting_axis` probes the 5 golden frameworks on `examples/{balance,hawk,single_ticker}_sample` (8 judgments, sorry-free). Run: `PYTHONPATH=code/lean_graph python3 -m qagents.lean_graph --axis numerical --root accounting --domain-graph accounting/emits/lean_graph/domain-numerical.json --out accounting/emits/lean_graph`; gate `code/lean_graph/tests/test_kgraph_accounting.py`.
  - **Half-A denominator producer (2026-06-24):** `accounting/scripts/universe_graph.py` (deterministic, root-venv pandas, no LLM) reads `financial/parquet/gics-symbols.parquet` → `emits/lean_graph/domain-numerical.json` (`qgraph-wire/1`, **526 `Symbol` nodes**, `member_of` edges) = LIVE |D| (opt-in `--domain-graph`, default falls back to calibration). Numerator = GOLDEN frameworks + committed AUTOMATED per-symbol bridges (`<sym>_trend_implies_momentum` in `Universe/S{60,20,55,40}/Bridge.lean`, `golden=False`); accepting-Debate judgments stay generated+gitignored (hard-rule 4), NOT credited (the two-file coverage split + live read are pinned in § Status emit below). Detail: spec `data/charters/studying/specs/lean4-charter-2026-06-10/quantify-progress-2026-06-14/SPEC.md` + memory `project_quantify_progress_effort`.

## Status emit (`data/status/accounting.json`)

`accounting/scripts/status_emit.py` (system `python3`, no venv) writes the StatusEmit slot; kit version is the producer's `KIT_VERSION` pin (swept in lockstep per root § Status hub). Full kit-closed-set surface roster, `productBrand: "Qresev"` + `latestProofGraphUrl`, and the two-lane writer + 05:32 cron: memory `[[project_accounting_subproject__infra]]` § Status emit surface.

**Load-bearing invariants (stay inline):**

- **Two-file split (mirrors proving):** rollup `accounting/coverage.json` = committed Universe Bridge encodings (excludes golden) feeds the hub; numerator `emits/lean_graph/coverage.json` (live-|D| #print-axioms join, +golden) is the SEPARATE quantify-progress artifact — do not cross-wire; they differ by exactly the golden.
- **C6 coverage-parity:** `dat.sh --coverage-parity` (C6) enforces rollup-encoded == numerator-non-golden.
- **Coverage-emit traps:** (1) `tier_totals` is drift-prone — DERIVE from the per-symbol enumeration; `derive_tier_counts` HARD-FAILS exit 3 on drift (G3/C3; `--check-coverage` standalone gate). (1b) a `"encoded": false` row (veto-refused near-miss, no `Bridge.lean`, e.g. IEX, CPT) is tracked but EXCLUDED from the count (2026-06-26 C7 fix). (1c) `tier_totals` also carries `A_golden`/`A_cross` (L-038 Tier-A basis split, axiomatize-shared SPEC § 5.1; per-symbol `tier_a_basis:"golden"|"cross-axis"`, absent ⇒ cross-axis, NOT the free-text `basis` key) — DERIVED by `derive_tier_counts`, invariant `A_golden+A_cross==A`, guarded in the G3 gate only when the rollup carries the keys. Interim `A_golden=0` (symbols[] = the non-golden numerator set); schema STAYS `trading-coverage/1` (additive), the `/2` bump is DEFERRED to the bundled mint-witness + golden-fold-in migration — do NOT bump `/2` for the split alone. (2) `extract_facts.py --reuse-facts --build` bumps `report.json` timestamps, which can silently move the status-emit "latest run" anchor + rename the consumer-pinned loci panel id — if regenerating only to refresh `loci.json`, keep that change and revert the incidental `report.json`/`graph.json` re-emit.
