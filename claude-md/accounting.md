# accounting — Lean4 axiomatic theorem-proving for portfolio evaluation

Cross-project rules: `../CLAUDE.md`. The **numerical axis** of the three-kernel Lean4 architecture (root CLAUDE.md § "Lean4 axes"; `data/specs/lean4-charter-2026-06-10/SPEC.md` § 4) — `/dat` is the numerical-axis instance of invariant 3: proofs driven by top-tier LLMs in parallel, never manual.

The financial-domain parallel of `proving/`. Same three-layer split, different domain: instead of complaints under federal statutes, accounting/ proves portfolio-level judgments (TREND, MOMENTUM, OPTIONS-RISK, SECTOR, DRAWDOWN) over OHLCV bars + indicator series + GICS sector mappings.

## The split (mirror of proving/)

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Accounting/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one portfolio JSON + bar/indicator evidence (via `scripts/data_view.py`) | a single `Bool` (plus evidence + uncertainty) | Claude Code sub-agent (`context: fork`); MAY use memsearch's `memory-recall` skill. |
| **Driver** | `scripts/extract_facts.py` | manifest + portfolio | `Accounting/<Framework>/Facts.lean` (axioms) + audit JSON | `claude -p --model opus` invocations (default — the latest top-tier model; `QAGENTS_PREDICATE_MODEL` overrides). |

The Lean kernel never reads OHLCV bars, indicator series, parquet, or JSON. The predicate sub-agents never write Lean. The driver is a thin coordinator with no financial reasoning of its own. The verifiable proof IS the Lean elaboration trace produced by `lake build`.

## Frameworks

Each framework lives under `Accounting/<Framework>/` (kernel) + `predicates/<framework>/` (specs). Adding a new framework is a parallel exercise — see "Adding a new framework" below.

| Framework | Kernel | Specs | Top-level judgment(s) | Predicate count |
|---|---|---|---|---|
| **Trend** | `Accounting/Trend/` | `predicates/trend/` | `is_uptrend`, `is_downtrend` | 5 (sma_cross_up, slope_positive, r_squared_geq, adx_geq, volume_confirmation) |
| **Momentum** | `Accounting/Momentum/` | `predicates/momentum/` | `has_momentum` | 4 (rsi_in_range, macd_bullish_cross, roc_positive, momentum_percentile_geq) |
| **OptionsRisk** | `Accounting/OptionsRisk/` | `predicates/options-risk/` | `defined_risk_only`, `is_clean` | 6 (leg_allowed, covered_call_collateralized, protective_put_bounded, no_naked_short_options, debit_only, max_loss_bounded) |
| **Sector** | `Accounting/Sector/` | `predicates/sector/` | `has_violation`, `no_violations` | 3 (cap_respected, gics_mapped, sector_concentration_leq) |
| **Drawdown** | `Accounting/Drawdown/` | `predicates/drawdown/` | `drawdown_disciplined` | 3 (max_drawdown_leq, time_under_water_leq, recovery_within) |

The kernel's predicate names are the contract that QresevApp's `/app` Lean trace consumes. Do not rename without updating `evaluating/web/src/islands/QresevApp.tsx` in lockstep.

## Layout

```
accounting/
├── CLAUDE.md                          this file
├── .memsearch.toml                    per-subproject memsearch override
├── lakefile.toml                      Lake build config
├── lean-toolchain                     pinned: leanprover/lean4:v4.31.0
├── Accounting.lean                    root module — imports all five frameworks + Common
├── Accounting/Common/
│   ├── Types.lean                     opaque cross-framework types (Symbol, Bar, Window, Portfolio,
│   │                                   Holding, OptionLeg) + Strategy enum (six allowed) + GicsSector enum (eleven)
│   └── Bar.lean                       opaque accessors mirroring the canonical {ts, o, h, l, c, v, adj_c} shape
├── Accounting/Trend/                  Types · Predicates · Statute · Theorems · (Facts — generated, gitignored)
├── Accounting/Momentum/               same shape
├── Accounting/OptionsRisk/            same shape
├── Accounting/Sector/                 same shape
├── Accounting/Drawdown/               same shape
├── predicates/
│   ├── README.md                      contract + roster (TREND + MOMENTUM + OPTIONS-RISK + SECTOR + DRAWDOWN)
│   ├── trend/                         5 specs
│   ├── momentum/                      4 specs
│   ├── options-risk/                  6 specs (DETAILED — brand-critical)
│   ├── sector/                        3 specs
│   └── drawdown/                      3 specs
├── scripts/
│   ├── extract_facts.py               driver — manifest-driven, framework block selects output namespace
│   └── data_view.py                   helper: read OHLCV / TA-reference / sector / portfolio via pandas on data/<SYM>/*.parquet
└── examples/
    ├── hawk_sample/                   12-holding hawk + TREND+SECTOR+OPTIONS-RISK; matches QresevApp Lean trace
    ├── single_ticker_sample/          AAPL-only TREND minimal sanity sample
    ├── balance_sample/                brand-anchor: moderate PM, all 5 frameworks · 5 judgments · 20/20 real
    ├── anchor_sample/                 3-PM triad leg: Conservative PM; SECTOR no_violations_under anchorPolicy (0.25) · DRAWDOWN · OPTIONS-RISK clean · 16/16 real
    ├── options_audit_sample/          P3 per-leg audit → OptionsRisk.clean_audited · 6/6 real
    ├── options_audit_strict_sample/   P3 v2 structural audit → clean_audited_strict · 12/12 real
    ├── momentum_sample/ · momentum_hier_sample/ · momentum_hier_cat_sample/   MOMENTUM golden (CAT) + hier-decompose (P4)
    ├── trend_hier_sample/             TREND hier-decompose (stub): sma_cross_up → 5 SMA leaves / 2 routes (P4)
    └── trend_hier_cat_sample/         TREND real-Opus decompose (CAT, 5/5 real) — SUSTAINED route (P4)
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

To add a framework (say, LIQUIDITY for share-turnover-based liquidity bounds):

1. Pick the framework's elements (e.g. average daily volume threshold, bid-ask spread bound, days-to-trade-position metric).
2. Add `Accounting/<NewFramework>/Types.lean` with opaque domain types if existing ones don't fit.
3. Declare one opaque axiom per element in `Accounting/<NewFramework>/Predicates.lean`.
4. Compose them as `structure`s representing the top-level judgment in `Accounting/<NewFramework>/Statute.lean` (use `inductive` for disjunctive validity).
5. Add `<judgment>_intro` theorems assembling each structure from individual element proofs in `Accounting/<NewFramework>/Theorems.lean` (suffix form is normative for new code per `../studying/representation.md`; `data/specs/axiomatize-trading-2026-05-30/SPEC.md` § 4.4 + `dat-cell.md:37` mandate it against live fan-out practice).
6. Wire the new framework into `Accounting.lean`.
7. Author one markdown predicate spec per axiom under `predicates/<newframework>/`. Each spec MUST follow the contract in `predicates/README.md`.
8. Add a sample portfolio + manifest + setup + proof under `examples/<newframework>-sample/`. The manifest MUST include a `framework` block pointing to the new module's facts path / namespace.
9. Update the `predicates/README.md` roster section.
10. Update the table in this CLAUDE.md.
11. Update `evaluating/web/src/islands/QresevApp.tsx` `FRAMEWORKS` list if the framework is user-facing.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no `IO.Process.run`, no FFI. The kernel is pure.
2. **Predicate specs MUST NOT cite or read `Accounting/<Framework>/*.lean`.** Their world is the portfolio JSON + bar evidence + spec rubric.
3. **The driver MUST NOT make financial judgments.** It only routes calls and serialises results. Add fields to the JSON schema (or a new `framework` block field) rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** All `Accounting/<Framework>/Facts.lean` are gitignored.
5. **Defined-risk only — non-negotiable.** Any options leg outside the SIX allowed strategies (`long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`) is REFUSED at the predicate layer. The kernel encodes the same restriction at the type level via the closed `Accounting.Strategy` enum. Both must remain in force.
6. **Bar shape canonical.** Any code that reads parquet uses the `{ts, o, h, l, c, v, adj_c}` columns; vendor names (Alpaca's `t`, etc.) never leak past `scripts/data_view.py`.
7. **Axiomatize with the top-tier model only.** Every LLM-backed extraction that produces a kept/committed result — the `extract_facts.py` driver AND the `dat-{cell,reconciler,cross,debate}` fan-out agents — runs on the **latest top-tier model** (`opus`); haiku is forbidden for any retained artifact (2026-06-03 bake-off: haiku fabricates numeric evidence confidently). Driver defaults to opus (`_PREDICATE_MODEL`); `QAGENTS_PREDICATE_MODEL` may only raise the tier. The anti-poison guard (`_protocol_violation`) rejects + retries number-less evidence and raises if persistent; wave archives stamp `"model"`. Detail: memory `feedback_predicate_model_opus_not_haiku`.

## Cross-project boundaries

- **OHLCV bars** — read via `scripts/data_view.py` from the shared `financial/parquet/ohlcv-equities/<SYM>.parquet` hub. Do NOT import `analyzing/`'s TypeScript DuckDB views or `trading/`'s `shared.lib` Python directly. The legacy `data/<name>/bars_<tf>/` collection-layout fallbacks were retired per `data/specs/data-charter-2026-05-17/SPEC.md` § 5.6.
- **Indicator math** — `analyzing/scripts/ta_reference.py` (Python TA-Lib) is the ground truth. Predicate sub-agents MAY shell out to it as a Python escape hatch (per qagents/CLAUDE.md "Language split"). TA outputs land at `financial/parquet/ta-reference/<SYM>.parquet`.
- **GICS sectors** — `financial/parquet/gics-symbols.parquet` (read via DuckDB or via `python -m shared.lib.gics lookup` as a shell-out).
- **Downstream consumer** — `evaluating/web` (Qresev) calls `accounting/scripts/extract_facts.py` as a subprocess via `evaluating/server`; never imports `Accounting/<Framework>/*.lean` directly.
- **Financial sign-off** — `accounting/` **advises** the FINANCIALLY-CLEARED gate (it is the financial-domain truth source: framework/kernel verdicts) but is **not** the grantor. `evaluating/` is the sole grantor (`data/specs/evaluating-financial-signoff-2026-06-24/SPEC.md`); a green accounting verdict is an input to the gate, never the sign-off itself.

## When a predicate sub-agent uses memsearch

A predicate sub-agent MAY invoke `memsearch:memory-recall` (`context: fork`, nested isolation) for prior thresholds / refusals / sector-cap calls. Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (Stop-hook-written); the collection is scoped to this subproject by the patched `lib/memsearch/plugins/claude-code/hooks/common.sh`.

## Toolchain notes

- Lean pinned via `lean-toolchain` (matches `proving/`). No Mathlib dependency — add only if a future predicate composition needs real-analysis or measure-theoretic kernels.
- **Lean4 authoring gotchas** (bit proving's remedy-axis work; apply when adding `inductive`/`structure` kernels per "Adding a new framework"): `private` is reserved — it can't be an `inductive` constructor name (use `privateRight`-style); and a `: Prop` structure can't carry Type-valued (data) fields — put enforcer/classification data in `def`s, not Prop-structure fields. See memory `reference_lean4_keyword_collisions`.
- `scripts/data_view.py` is pandas-only (via root venv `[analyzing]` extras for pyarrow); no duckdb dependency.
- Driver shells out to `claude -p --model opus` by default (`_PREDICATE_MODEL`); top-tier-only + the `_protocol_violation` anti-poison guard are the operative contract (Hard rule #7).

**Driver smoke-test side effect.** `extract_facts.py` against an existing `examples/<id>/` overwrites all five artefacts in place by default — `git checkout -- examples/<id>/` before commit, or pass `--sandbox-out <dir>`. Detail: memory `feedback_driver_overwrites_example_artifacts`.

**Driver CLI surface — parity with proving's.** `extract_facts.py` carries `--reuse-facts` (re-emit from committed `facts.json`, no sub-agent calls), `--build`, `--sandbox-out`. **`--stub` is value-faithful** with `--example-id` (seeds canned values from `facts.json`); guard `t_08_stub_facts_faithful.sh` + memory `feedback_lean_toolchain_bump_verify_example_proofs`. The `evaluating/server/adapters/accounting.py` `--stub` workaround can migrate to `--reuse-facts` (`evaluating/CLAUDE.md` § 7 has the legacy path).

## Results propagation — `scripts/{lean_parse,lake_trace,report}.py`

Mirror of proving/'s propagation pipeline (`data/specs/proving-results-propagation-2026-05-09/SPEC.md`), adapted for the multi-judgment accounting case. Each `extract_facts.py` run produces three extra audit files under `examples/<id>/`:

- **`report.json`** — per-run join of facts + kernel verdict: `judgments[]` (top-level theorems exercised), `predicates[]` (per-fact roster: axiom binding, evidence, uncertainty, framework cite), `kernel.errors[]` (per-error `introRule.introField` locus joined to `axiomName` via positional intro-rule args).
- **`graph.json`** — proof DAG, byte-compatible with verifying/'s proof-graph kit `RicoFixture` shape (nodes per predicate-application/axiom/theorem; edges `applies`/`composes`/`inhabits`).
- **`loci.json`** — single `DiagramEmit` for the status hub: one root portfolio node, one sub-tree per top-level judgment, one rectangle per kernel-required element coloured by verdict.

Pipeline modules:
- `scripts/lean_parse.py` — regex-based Lean4 reader. Parses `axiom <name> : Prop` (snake_case names), `theorem <intro_*>` intro rules, and term/tactic-mode proof theorem bodies. Returns line-numbered records.
- `scripts/lake_trace.py` — verbatim copy of proving's `lake_trace.py`. Parses `lake build` / `lake env lean` stderr into typed `LakeError` records (type-mismatch, application-type-mismatch, kernel-error).
- `scripts/report.py` — pure data composer. Carries the `LociJudgment` roster (one per top-level kernel `def`/`structure` — 13 wired: the SECTOR CapPolicy duals `{has,no}_violation[s]_under`, `is_uptrend`/`is_downtrend`, `defined_risk_only`/`is_clean`, the P3 audits `clean_audited`/`clean_audited_strict`, `has_momentum`, `drawdown_disciplined`/`discipline_breached`) and the `AXIOM_CITES` map (predicate-axiom → framework label, e.g. `cap_respected` → `SECTOR`).

**Diff-check obligation against `proving/`.** `lake_trace.py` is a verbatim copy and MUST be patched in lockstep across the two trees. `lean_parse.py` and `report.py` share internals (`_strip_block_comments`, `_theorem_signatures`, `_tokenize_term_body`) with proving's counterparts — diff-check before patching either side. Deliberate accounting-side divergences (lowercase axiom names, dotted conclusion heads for multi-judgment runs, the multi-judgment `LociRoster` shape) are not drift — preserve them.

The driver invokes `lake build <proof_target>` (resolved from the manifest's `framework` block, e.g. `examples.hawk_sample.proof`) after writing the per-run `Accounting/Runs/<RunName>/Facts.lean` — NOT `lake env lean <file>`. The build form compiles transitive deps so the driver-emitted Facts.lean elaborates against the rest of the kernel without requiring the operator to run `lake build` first. Pass `--no-report` to skip the build+emit phase (raw facts.json only). Pass `--portfolio-label <name>` to set the loci diagram's root-node label (defaults to the portfolio JSON's `name`, title-cased).

## Open work (v0 → v1)

- ~~Sector `has_violation` hard-codes the 0.30 cap~~ **DONE 2026-06-16.** `Accounting.Sector` parametrised over `CapPolicy := GicsSector → Float` (`{has_violation,no_violations}_under p policy`; `Sector/Policies.lean`); portfolio-only forms = `defaultPolicy` (0.30) defeq specialisations. **Load-bearing: only the *concentration* (weight) cap is parametrised** — `max_drawdown_leq p 0.15` stays a UNIVERSAL defined-risk veto, never per-sector (2026-06-16 operator ruling).
- **Real-call flip pattern.** Mixed real/stub per run via `inputs.stub: true` per-call override; real `claude -p` calls need all four driver pieces (`--allowed-tools "Bash Read"`, `--permission-mode bypassPermissions`, `--add-dir $ROOT`, anti-poison preamble). Brand-anchor `balance_sample` (5 frameworks · 5 judgments · 20/20 real). Detail: memory `project_accounting_subproject` + `feedback_claude_p_subagent_real_call_pattern` + `accounting/NEXT_STEPS.md`.
- ~~per-leg options gate not composed into a judgment~~ **DONE 2026-06-23 (v1+v2).** Two additive OPTIONS-RISK judgments, both leaving `is_clean`/`defined_risk_only` byte-stable: **v1 `clean_audited`** (6/6 real) + **v2 `clean_audited_strict`** (folds 3 structure-bound predicates into `leg_structurally_clean`, strictly stronger via `clean_audited_strict_implies_audited`; 12/12 real). Deferred v3 → `data/next-steps/evaluating.md`; mechanics `NEXT_STEPS.md` P3.
- **Example proofs build target — `scripts/build_examples.sh`.** Bare `lake build` builds only the always-green libs (`Accounting` + `AccountingUniverse`); the `examples` lean_lib is NOT a default target (each `proof.lean` imports a gitignored ephemeral `Accounting/Runs/<X>/Facts.lean`, Hard rule 4, absent from a clean checkout). `build_examples.sh` is the green-everything command: regenerates every example's Facts.lean from committed `facts.json` (`extract_facts.py --reuse-facts --no-report`, deterministic, REPO-RELATIVE so the committed copy stays byte-identical) then builds libs + examples; `--regen-only` skips the build. (A single example still verifies via `lake env lean examples/<id>/proof.lean` once its Facts.lean exists.)
- **Hierarchical predicates — H0–H4 DONE 2026-06-21** (status of record: `../studying/representation.md` § 13.4). Decompose a flat golden into LLM-decided leaves + kernel-derived composites: `Accounting/Common/Tactic.lean` (`prove_element`, Mathlib-free, lockstep w/ `Proving/USC/Common/Tactic.lean`) + per-framework `<F>/Hier/` + `OptionsRisk/Hier/VetoSurvives.lean`. Decompose-by-default (`predicates/README.md` bullet 7); `report.py` emits `derived`+`decomposes`+`stats.telemetry`; flat goldens + QresevApp byte-stable. **THREE shapes** (golden-bridges CONFLUENT/sorry-free): (1) **Bool-composite** — Bool leaves closed by `prove_element`; sub-shapes: a DISJUNCTION over routes (MOMENTUM `macd_bullish_cross`, TREND `sma_cross_up`) and a CONJUNCTION-with-REQUIRED-NEGATION (TREND `volume_confirmation`, 2026-06-28 — the universe `Volume.Participated` mirror; the bear money-flow guard `¬ mfi_distribution` is a structure FIELD, "veto, not a vote"; the false leaf is emitted by the driver as `¬(…)`). (2) **Measurement-leaf** — ONE leaf measures a Nat magnitude, kernel does the bound compare via the EXPLICIT TERM `<f>_intro m h (by omega)` (NOT `prove_element`-closable — shared tactic stays diff-locked), shape `∃ m, leaf p m ∧ <compare>`; five leaves over all three bound directions (`max_drawdown_leq`/`sector_concentration_leq`/`cap_respected` ≤, `r_squared_geq` ≥, `rsi_in_range` two-sided centi-units). Scale rule: fractions→bps (×10000), 0..100 indices→centi (×100). Live-judgment elements land via a kernel composition lemma (`no_violations_from_bounded` / `is_uptrend_from_rsq` / `has_momentum_from_rsi`); standalone atoms (`sector_concentration_leq`, `volume_confirmation`) don't. Tests D16–D23 + D28–D32. Detail: specs § 15 / § 11 + `NEXT_STEPS.md` P4 + memory.

## Axiomatize-trading program (financial parallel of proving's axiomatize-uscode)

Spec: `data/specs/axiomatize-trading-2026-05-30/SPEC.md`. Extends the five hand-built frameworks to a phased, **sector-by-sector** program over the S&P 500, produced redundantly by top-tier-model subagent teams along ≥5 orthogonal **signal-family** axes (Trend / Momentum / Volatility / Volume / CrossSection [+ InstrumentRisk]), then reconciled. Cross-axis agreement proved in-kernel via `Bridge.lean` lemmas IS the correctness signal — the TA **confluence** heuristic. Tier-A = ≥3 axes' directional encodings bridge sorry-free.

- **Slice unit:** the `(GICS sector, axis)` cell; sector code → namespace `Accounting.Universe.S<code>` (`S45` = Info Tech, the `T18` analog). GICS is the drill-down spine. Corpus = the existing `financial/parquet/` hub (Phase 0 done; `financial/gics/build.py --categorize` → `categorization.json`).
- **Golden reference:** the existing 5 frameworks (`Accounting.{Trend,Momentum,OptionsRisk,Sector,Drawdown}`) on `examples/{single_ticker_sample,hawk_sample,balance_sample}/`, scored via golden-bridges (NOT exact-string — naming is a free variable, per the uscode 2026-05-29 lesson).
- **Debate framework (the bull-vs-bear payoff):** a NEW 6th framework `Accounting/Debate/` formalizes `trading/`'s bull-vs-bear gate "proven at every step". `admissible_long` is a `structure` (no field omittable) requiring bull confluence + kernel directional accept + `defined_risk_clean` + the **negation of every bear disqualifier** (volume divergence / volatility veto / overextension) — "veto, not a vote" as a type-level property. `debate.py gate --lean-proof` elaborates `intro_admissible_long`; every `evaluate_gate` refusal maps to a non-elaborating proof.
- **Lane:** **`/dat-manual` (Max-20x interactive subscription) is the standing lane** — the dedicated Agent-SDK credit was paused indefinitely 2026-06-15, so the SDK batch lane (spec § 7.3) buys nothing over the manual lane; treat it as deferred (memory `project_agent_sdk_wrapper`). The skill (`.claude/skills/dat-manual/`; mirrors `/dau-manual`) runs Slice + Reconcile + Debate; mechanical phases in `scripts/dat.sh`, LLM fan-out over `.claude/agents/dat-{cell,reconciler,cross,debate}.md` (dat-debate is new, rest ported from `dau-*`). Zero-prompt enforced by `dat.sh --permit-fanout` vs `scripts/dat-helpers/required-allow-patterns.txt` (exit 61); cells write sandboxed `pending/trading-cells/`, promoted only post-reconcile. `scripts/score_bridge.py` is a near-verbatim port of proving's (diff-check-lockstep, as `lake_trace.py`). **Calibration integrity (mirrors `/dau`):** never hand-patch a blind cell/bridge to manufacture agreement — fix the ground-truth defect and re-run blind; blind agreement is the only oracle (memory `feedback_dau_gap_clear_blind_reslice_not_handpatch`).
- **Status (durable state).** Phase 1–2 done; GICS universe complete (502 members, all 11 sectors). Canonical (operator-approved): `Accounting.Universe.Common` (collapse-bridged shared predicates, sorry-free) PLUS per-sector slices `Accounting.Universe.{S<code>.*, Reconciled.S<code>}` — explicit AccountingUniverse lakefile roots; `lake build AccountingUniverse` green, golden `Accounting` unaffected. Accepting Debates accumulate by symbol; veto refusals are correct outcomes (veto, not a vote). The drawdown veto (`max_drawdown_leq 0.15`) stays a **universal** defined-risk bound — NOT a CapPolicy trigger (CapPolicy parametrises only the orthogonal *concentration* cap). **Three-stage deterministic targeting** before any fan-out: `dat.sh --sector-rank` (11 ETFs by 126d RS vs SPY) → `--prescreen` (Trend∧Momentum survivors; `--check-universe` R4 guard exit 15) → `--veto-screen` (252d MaxDD ≤0.15 ∧ ATR-frac ≤0.05 — the actual Tier-A gate); `--frontier` joins all three; `--plan-cells <sector> --symbols <survivors>` targets waves. Per hard-rule-4 the per-run Debate `Facts.lean` stays generated; acceptances reproduce from the committed Reconciled tier + archived wave. Per-wave verdicts + Tier-A set + targeting/tape detail: memory `project_accounting_subproject` + close summaries + spec § 6.5/§ 11/§ 13 + `data/debates/axiomatize-method-2026-06-09.md`.
- **Wave archive (§ 12).** Blind fan-out sandboxes freeze to gitignored + S3-backed `accounting/waves/<wave-id>/` via `dat.sh --archive-wave` → `dat-helpers/archive_wave.py` (+ `WAVE.json`, `corpus_pin` = `categorization.json` `as_of`); `/dat-manual` Step 7 archives BEFORE promote/hold (test `t_07_archive_wave.sh`). Port of proving's `/waves` — **diff-check both `archive_wave.py` in lockstep.** S3 class `trading-waves` (`serving/scripts/archive-artifact.sh`).
- **Axis set (§ 6.2).** `DEFAULT_AXES` = 5 core + instrument-risk + liquidity (**7 per no-flag slice**); `CORE_AXES` stays the 5 the Tier-A ≥3-directional-quorum references (corroborators don't add to the quorum). Axes 8 Seasonality + 9 RiskQuantum **deferred**. Liquidity corroborator (`Tradable m` from `data_view.py bars`, failure = `bear_untradeable`): spec § 6.2 + `predicates/universe/_axes/liquidity.md`.
- **S3 backup MANDATORY per `/dat-manual` (operator standing rule).** Every invocation ends `dat.sh --archive-wave <wave-id> --push` — never archive-only (exit 14 if aws-vault locked; unlock + re-run). Catch-up `dat.sh --push-all [--verify]` (one MFA, idempotent, content-addressed); `--push-if-warm` is the SDK-lane default, manual keeps bare `--push`. Parity with `dau.sh` (`t_09_push_lane.sh`).
- **Progress visualization (debate RULED 2026-06-14; P1 slice DONE).** "How much is axiomatized" = per-axis **domain graph** (Half A, denominator) × the shared **Lean4-derivation graph** (Half B, numerator). Half B producer = shared `code/lean_graph/` (`qagents.lean_graph`); `accounting_axis` probes the 5 golden frameworks on `examples/{balance,hawk,single_ticker}_sample` (8 judgments, sorry-free). Run: `PYTHONPATH=code/lean_graph python3 -m qagents.lean_graph --axis numerical --root accounting --domain-graph emits/lean_graph/domain-numerical.json --out accounting/emits/lean_graph`; gate `code/lean_graph/tests/test_kgraph_accounting.py`.
  - **Half-A denominator producer (2026-06-24):** `accounting/scripts/universe_graph.py` (deterministic, root-venv pandas, no LLM; mirror of proving's `uscode_graph.py --cite-graph`) reads `financial/parquet/gics-symbols.parquet` → `emits/lean_graph/domain-numerical.json` (`qgraph-wire/1`, **526 `Symbol` nodes**, `member_of` edges) = LIVE |D| (opt-in `--domain-graph`, default falls back to calibration). Numerator = GOLDEN frameworks + 10 committed AUTOMATED per-symbol bridges (`<sym>_trend_implies_momentum` in `Universe/S{60,20,55,40}/Bridge.lean`, `golden=False`); accepting-Debate judgments stay generated+gitignored (hard-rule 4), NOT credited. **Live read: 11/526 = 2.09% (golden 0.19% + automated 1.90%), sorry-free.** Detail: spec `data/specs/lean4-charter-2026-06-10/quantify-progress-2026-06-14/SPEC.md` + memory `project_quantify_progress_effort`.

## Status emit (`data/status/accounting.json`)

`accounting/scripts/status_emit.py` (system `python3`, no venv) writes
the StatusEmit slot to `data/status/accounting.json`. Schema is
`@qagents/diagram-kit` v0.5.0. The producer is self-contained — no
cross-subproject imports. Surface produced (kit closed set):

- 1 `framework-roster` `DiagramEmit` (summary card, one node per
  framework, focused = `Accounting/<F>/` present)
- 1 `latest-run-loci` `DiagramEmit` read verbatim from
  `examples/<anchor>/loci.json` (the brand-anchor run with the richest
  framework × judgment coverage — currently `balance_sample`,
  5 frameworks · 5 judgments · 20/20 real-call)
- 4 `StatCardEmit`s (`run-stats.{total,accepted,rejected,latest}`) +
  1 `KpiStripEmit` (`run-stats`, layout `fixed-4`)
- **trading-program** (added 2026-06-24): 4 `StatCardEmit`s
  (`trading-program.{encoded,tier-a,sectors,universe}`) + 1 `KpiStripEmit`
  (`trading-program`, `fixed-4`) reading the committed rollup
  **`accounting/coverage.json`** (`trading-coverage/1`, dat-cross). **Scope
  parity with proving's `usc-program` strip** so designing/web renders both
  axes apples-to-apples: encoded symbols (10) tiered A/B/C (7/1/2), sectors
  (4/11), universe share (1.90%). Raw figures in
  `live.metrics.trading{EncodedSymbols,TierA,TierB,TierC,SectorsTouched,
  SectorUniverse,SymbolUniverse,UniversePct}`; skipped (no card) when
  `coverage.json` absent. **Two-file split (mirrors proving):** rollup
  `accounting/coverage.json` = 10 committed Universe Bridge encodings = 10/526 =
  1.90% (excludes golden) feeds the hub; numerator `emits/lean_graph/coverage.json`
  = 11/526 = 2.09% (live-|D| #print-axioms join, +1 golden AAPL) is the SEPARATE
  quantify-progress artifact — do not cross-wire; they differ by exactly the
  golden; `dat.sh --coverage-parity` (C6) enforces rollup-encoded ==
  numerator-non-golden. **Coverage-emit traps:** (1) `tier_totals` is drift-prone
  — DERIVE from the per-symbol enumeration; `derive_tier_counts` HARD-FAILS exit 3
  on drift (G3/C3; `--check-coverage` standalone gate). (1b) a `"encoded": false`
  row (veto-refused near-miss, no `Bridge.lean`, e.g. IEX) is tracked but EXCLUDED
  from the count (2026-06-26 C7 fix). (2) `extract_facts.py --reuse-facts --build`
  bumps `report.json` timestamps, which can silently move the status-emit "latest
  run" anchor + rename the consumer-pinned loci panel id — if regenerating only to
  refresh `loci.json`, keep that change and revert the incidental
  `report.json`/`graph.json` re-emit.
- 1 `recent-runs` `TableEmit` (≤ 10 rows from `examples/*/report.json`,
  one column per run with `verdict` pill + expand-row locus list)
- 1 `predicate-roster-latest` `TableEmit` (per-predicate atomic view of
  the anchor run, grouped by framework cite — `TREND` / `MOMENTUM` /
  `SECTOR` / `OPTIONS-RISK` / `DRAWDOWN`)
- `panels[]` declaring the deep-page render order

Defined-risk options invariant is reflected in `cardSummary`.
`productBrand: "Qresev"` matches the user-facing app name; deep-page
hover/links can use `latestProofGraphUrl =
https://qresev.quantapix.com/proof-graph/run/<id>/`.

**Two-lane writer + cron** — standard pattern per `data/specs/data-conventions-2026-05-06/SPEC.md` § 5.3 (cron lane via `QAGENTS_PENDING_ROOT`, manual lane acquires `.data-write-lock`). Fires daily at 05:32 local; ROUTINES entry in `data/schedules/launchd/install.sh`. Cron-EC2 migration (`data/specs/cron-ec2-migration-2026-05-19/SPEC.md`) is transport-only — script unchanged.
