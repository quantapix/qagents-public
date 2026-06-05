# accounting — Lean4 axiomatic theorem-proving for portfolio evaluation

Sibling of `proving/`, `analyzing/`, `trading/`, `evaluating/`, `verifying/`. Cross-project rules: `../CLAUDE.md`.

The financial-domain parallel of `proving/`. Same three-layer split, different domain: instead of complaints under federal statutes, accounting/ proves portfolio-level judgments (TREND, MOMENTUM, OPTIONS-RISK, SECTOR, DRAWDOWN) over OHLCV bars + indicator series + GICS sector mappings.

## The split (mirror of proving/)

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Accounting/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one portfolio JSON + bar/indicator evidence (via `scripts/data_view.py`) | a single `Bool` (plus evidence + uncertainty) | Claude Code sub-agent (`context: fork`); MAY use memsearch's `memory-recall` skill. |
| **Driver** | `scripts/extract_facts.py` | manifest + portfolio | `Accounting/<Framework>/Facts.lean` (axioms) + audit JSON | `claude -p --model opus` invocations (default; `QAGENTS_PREDICATE_MODEL` overrides). |

The Lean kernel never reads OHLCV bars, indicator series, parquet, or JSON. The predicate sub-agents never write Lean. The driver is a thin coordinator with no financial reasoning of its own. The verifiable proof IS the Lean elaboration trace produced by `lake build`.

## Why this works

The three-layer split keeps memsearch scoped to natural-language artefacts (specs, portfolios, completed proofs — never Lean dependent types), keeps each predicate sub-agent's output domain narrow (one `Bool` + evidence), and reduces top-level judgments (`Trend.is_uptrend`, `Sector.has_violation`, `OptionsRisk.is_clean`, …) to pure structure-introduction proofs the kernel verifies. Audit trail is `examples/<id>/facts.json` — a reviewer challenges any predicate without re-running the kernel.

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
├── lean-toolchain                     pinned: leanprover/lean4:v4.30.0
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
    ├── hawk_sample/                   12-holding hawk portfolio + TREND+SECTOR+OPTIONS-RISK manifest matching QresevApp Lean trace
    ├── single_ticker_sample/          AAPL-only TREND minimal sanity sample
    └── balance_sample/                brand-anchor: 12-holding moderate PM, all 5 frameworks · 6 judgments · 24 axioms (7 real-call + 17 stub for v0)
```

## Workflow

1. **Author the formal framework** (Lean) — for a new framework, add `Accounting/<NewFramework>/{Types,Predicates,Statute,Theorems}.lean` and import them from `Accounting.lean`.
2. **Author predicate-function specs** — one markdown file per opaque predicate, under `predicates/<newframework>/`. Spec format is fixed (see `predicates/README.md`). Each spec is the system prompt for its sub-agent.
3. **Run the driver** against a portfolio:
   ```
   python3 scripts/extract_facts.py examples/hawk-sample/portfolio.json \
           --manifest examples/hawk-sample/manifest.json \
           --example-id hawk-sample [--stub]
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
5. Add `intro_` theorems assembling each structure from individual element proofs in `Accounting/<NewFramework>/Theorems.lean`.
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
7. **Axiomatize with Opus only.** Every LLM-backed extraction that produces a kept/committed result — the `extract_facts.py` predicate driver AND the `dat-{cell,reconciler,cross,debate}` fan-out agents — runs on **Opus**. haiku is forbidden for any retained artifact: the 2026-06-03 bake-off proved haiku fabricates numeric evidence while reporting it confidently (it invented a "subcommand missing" rationale that was value-correct by luck, and mis-calibrated `uncertainty`). The driver defaults to opus (`_PREDICATE_MODEL`); `QAGENTS_PREDICATE_MODEL` may only raise the tier, never drop to haiku for a committed run. The anti-poison guard (`_protocol_violation`) rejects + retries fabricated / number-less evidence and raises if it persists. Wave archives stamp `"model"`. See memory `feedback_predicate_model_opus_not_haiku`.

## Cross-project boundaries

- **OHLCV bars** — read via `scripts/data_view.py` from the shared `financial/parquet/ohlcv-equities/<SYM>.parquet` hub. Do NOT import `analyzing/`'s TypeScript DuckDB views or `trading/`'s `shared.lib` Python directly. The legacy `data/<name>/bars_<tf>/` collection-layout fallbacks were retired per `data/specs/data-charter-2026-05-17.md` § 5.6.
- **Indicator math** — `analyzing/scripts/ta_reference.py` (Python TA-Lib) is the ground truth. Predicate sub-agents MAY shell out to it as a Python escape hatch (per qagents/CLAUDE.md "Language split"). TA outputs land at `financial/parquet/ta-reference/<SYM>.parquet`.
- **GICS sectors** — `financial/parquet/gics-symbols.parquet` (read via DuckDB or via `python -m shared.lib.gics lookup` as a shell-out).
- **Downstream consumer** — `evaluating/web` (Qresev) calls `accounting/scripts/extract_facts.py` as a subprocess via `evaluating/server`; never imports `Accounting/<Framework>/*.lean` directly.

## When a predicate sub-agent uses memsearch

A predicate sub-agent MAY invoke the `memsearch:memory-recall` skill (which itself runs `context: fork` again — nested isolation). Useful queries:

- "What threshold did I use for r_squared_geq on similar mid-cap baskets?" — for `trend/r-squared-geq`.
- "Have I previously refused a credit-spread setup pleaded as a debit spread?" — for `options-risk/debit-only`.
- "What was the prior-quarter Tech-cap call against the same hawk portfolio?" — for `sector/cap-respected`.

Prior decisions live in `.memsearch/memory/YYYY-MM-DD.md` (auto-written by the Stop hook). The collection is scoped to this subproject by the patched `lib/memsearch/plugins/claude-code/hooks/common.sh`.

## Toolchain notes

- Lean pinned via `lean-toolchain` (matches `proving/`). No Mathlib dependency — add only if a future predicate composition needs real-analysis or measure-theoretic kernels.
- **Lean4 authoring gotchas** (bit proving's remedy-axis work; apply when adding `inductive`/`structure` kernels per "Adding a new framework"): `private` is reserved — it can't be an `inductive` constructor name (use `privateRight`-style); and a `: Prop` structure can't carry Type-valued (data) fields — put enforcer/classification data in `def`s, not Prop-structure fields. See memory `reference_lean4_keyword_collisions`.
- `scripts/data_view.py` is pandas-only (via root venv `[analyzing]` extras for pyarrow); no duckdb dependency.
- Driver shells out to `claude -p --model opus` by default (`_PREDICATE_MODEL`, `QAGENTS_PREDICATE_MODEL` may only raise the tier). Opus-only + the `_protocol_violation` anti-poison guard are the operative contract — see Hard rule #7 and memory `feedback_predicate_model_opus_not_haiku` for the 2026-06-03 bake-off rationale.

**Driver smoke-test side effect.** `extract_facts.py` against an existing `examples/<id>/` overwrites all five artefacts using worktree-absolute paths; smoke-testers must `git checkout -- examples/<id>/` before commit. Durable fix is the `--sandbox-out <dir>` flag, **ported into accounting's driver 2026-06-01** (commit `ffa30e46`, the axiomatize-trading Phase-1 set — `_rel()` helper + save/restore around the build + reuse-source-from-committed-dir): pass `--sandbox-out` to redirect per-run artefacts and leave `examples/<id>/` pristine. The **default** (no `--sandbox-out`) still writes in place, so a default-path smoke-test against an existing example still needs `git checkout -- examples/<id>/` before commit. Full mechanics + spec-test-harness regression vector in memory `feedback_driver_overwrites_example_artifacts`.

**Driver CLI surface — parity reached with proving's (2026-06-01).** `accounting/scripts/extract_facts.py` now carries `--reuse-facts` (skip predicate sub-agent calls, re-emit from committed `facts.json`), `--build`, and `--sandbox-out`, ported as the axiomatize-trading Phase-1 set (commit `ffa30e46`). The old `evaluating/server/adapters/accounting.py` `--stub` workaround can migrate to `--reuse-facts` for CLI parity with the verifying adapter; `evaluating/CLAUDE.md` § 7 still documents the legacy path until that adapter is updated. **`--stub` is value-faithful (2026-06-05):** with `--example-id` it seeds canned values from the example's committed `facts.json` keyed on `(spec, lean_call)` (precedence `inputs.expected` > committed facts > the hawk-tuned `_stub_value_for` table, which is now fallback-only). This fixes the polarity-blind table flipping `balance_sample`'s `time_under_water` breach back to True → spurious REJECT (memory `feedback_lean_toolchain_bump_verify_example_proofs`; guard `t_08_stub_facts_faithful.sh`).

## Results propagation — `scripts/{lean_parse,lake_trace,report}.py`

Mirror of proving/'s propagation pipeline (`data/specs/proving-results-propagation-2026-05-09.md`), adapted for the multi-judgment accounting case. Each `extract_facts.py` run produces three extra audit files under `examples/<id>/`:

- **`report.json`** — per-run join of facts + kernel verdict. Top-level `judgments[]` lists every top-level theorem the proof exercised (e.g. hawk_sample proves `is_uptrend` + `has_violation` + `is_clean`); `predicates[]` is the per-fact roster with axiom-name binding, evidence, uncertainty + framework cite; `kernel.errors[]` carries per-error `introRule.introField` locus joined back to `axiomName` via the proof's positional intro-rule arguments.
- **`graph.json`** — proof DAG, byte-compatible with the verifying/ proof-graph kit's `RicoFixture` shape (one node per predicate-application + axiom + theorem; edges `applies`/`composes`/`inhabits`). Lets a future Qresev proof-graph kit render any real run without a schema diff.
- **`loci.json`** — single `DiagramEmit` for the status hub. One root portfolio node; one sub-tree per top-level judgment exercised; one rectangle per kernel-required element coloured by per-element verdict.

Pipeline modules:
- `scripts/lean_parse.py` — regex-based Lean4 reader. Parses `axiom <name> : Prop` (snake_case names), `theorem <intro_*>` intro rules, and term/tactic-mode proof theorem bodies. Returns line-numbered records.
- `scripts/lake_trace.py` — verbatim copy of proving's `lake_trace.py`. Parses `lake build` / `lake env lean` stderr into typed `LakeError` records (type-mismatch, application-type-mismatch, kernel-error).
- `scripts/report.py` — pure data composer. Carries the `LociJudgment` roster (one per top-level kernel `def`/`structure`: `is_uptrend`, `is_downtrend`, `has_violation`, `no_violations`, `defined_risk_only`, `is_clean`, `has_momentum`, `drawdown_disciplined` — all 8 wired since balance_sample lands) and the `AXIOM_CITES` map (predicate-axiom → framework label, e.g. `cap_respected` → `SECTOR`).

**Diff-check obligation against `proving/`.** `lake_trace.py` is a verbatim copy and MUST be patched in lockstep across the two trees. `lean_parse.py` and `report.py` share internals (`_strip_block_comments`, `_theorem_signatures`, `_tokenize_term_body`) with proving's counterparts — diff-check before patching either side. Deliberate accounting-side divergences (lowercase axiom names, dotted conclusion heads for multi-judgment runs, the multi-judgment `LociRoster` shape) are not drift — preserve them.

The driver invokes `lake build <proof_target>` (resolved from the manifest's `framework` block, e.g. `examples.hawk_sample.proof`) after writing the per-run `Accounting/Runs/<RunName>/Facts.lean` — NOT `lake env lean <file>`. The build form compiles transitive deps so the driver-emitted Facts.lean elaborates against the rest of the kernel without requiring the operator to run `lake build` first. Pass `--no-report` to skip the build+emit phase (raw facts.json only). Pass `--portfolio-label <name>` to set the loci diagram's root-node label (defaults to the portfolio JSON's `name`, title-cased).

## Open work (v0 → v1)

- Sector framework's `has_violation` v0 hard-codes the default cap (0.30) for a clean QresevApp Lean-trace match. Future work: parametrise over a per-portfolio CapPolicy so different sectors carry different caps (the Predicates layer already supports per-sector caps via the third `cap_respected` argument).
- **Real-call flip pattern.** Mixed real/stub predicates per run via `inputs.stub: true` per-call override. Real `claude -p` calls require all four driver pieces (`--allowed-tools "Bash Read"`, `--permission-mode bypassPermissions`, `--add-dir $ROOT`, plus driver-injected anti-poison preamble overriding stub-mode auto-memory). Brand-anchor is `balance_sample` (5 frameworks · 6 judgments · 24 axioms). Per-run state, ticker coverage, and gating dependencies for new frameworks (peer-universe ETFs, sector weight-aggregation, portfolio-equity-curve subcommand) tracked in memory `project_accounting_subproject` + `accounting/NEXT_STEPS.md` + per-session close summaries. Load-bearing flag rationale: memory `feedback_claude_p_subagent_real_call_pattern`.
- `predicates/options-risk/leg_allowed.md` is the per-leg gate; the manifest's hawk-sample skips per-leg `leg_allowed` calls and relies on the portfolio-level `no_naked_short_options` + `debit_only` to discharge `defined_risk_only`. v1 should enumerate per-leg `leg_allowed` calls and prove `is_clean` more granularly (matching the runtime gate's auditing behaviour).
- The example proofs are not yet wired into `lake build` (lakefile builds only the `Accounting` library). To verify an example end-to-end, elaborate the proof file directly with `lake env lean examples/<id>/proof.lean` after the driver has produced Facts.lean — this is what `extract_facts.py` does internally to capture the lake trace for `report.json`.

## Axiomatize-trading program (financial parallel of proving's axiomatize-uscode)

Spec: `data/specs/axiomatize-trading-2026-05-30.md`. Extends the five hand-built frameworks to a phased, **sector-by-sector** program over the whole S&P 500 universe, produced redundantly by Opus subagent teams along ≥5 orthogonal **signal-family** axes (Trend / Momentum / Volatility / Volume / CrossSection [+ InstrumentRisk]), then reconciled. Cross-axis agreement proved in the kernel via `Bridge.lean` lemmas IS the correctness signal — and it coincides with the TA practitioner's **confluence** heuristic (independent indicator families agreeing). Tier-A = ≥3 axes' directional encodings bridge sorry-free.

- **Slice unit:** the `(GICS sector, axis)` cell; sector code → namespace `Accounting.Universe.S<code>` (`S45` = Info Tech, the `T18` analog). GICS is the drill-down spine (sector → industry group → industry → sub-industry → symbol). Corpus = the existing `financial/parquet/` hub (Phase 0 effectively done; only `financial/gics/build.py --categorize` → `categorization.json` is added).
- **Golden reference:** the existing 5 frameworks (`Accounting.{Trend,Momentum,OptionsRisk,Sector,Drawdown}`) on `examples/{single_ticker_sample,hawk_sample,balance_sample}/`, scored via golden-bridges (NOT exact-string — naming is a free variable, per the uscode 2026-05-29 lesson).
- **Debate framework (the bull-vs-bear payoff):** a NEW 6th framework `Accounting/Debate/` formalizes `trading/`'s bull-vs-bear gate "proven at every step". `admissible_long` is a `structure` with no constructor omitting any field — requires the bull confluence claim + kernel directional accept + `defined_risk_clean` + the **negation of every bear disqualifier** (volume divergence / volatility veto / overextension). "Veto, not a vote" becomes a type-level property; `debate.py gate --lean-proof` elaborates `intro_admissible_long`; every `evaluate_gate` refusal maps to a non-elaborating proof. Stronger than today's JSON gate (which has no bear term). The volume/volatility/cross-section axis briefings emit exactly those bear divergence judgments the reconciler records.
- **Lane:** Agent SDK batch (gated 2026-06-15 credit) + manual-interactive bridge via the **`/dat-manual`** skill (`.claude/skills/dat-manual/`; mirrors `/dau-manual`). Mechanical phases in `scripts/dat.sh` (`--pre`/`--permit-fanout`/`--plan-cells`/`--collect`/`--score`/`--report`); LLM fan-out over `.claude/agents/dat-{cell,reconciler,cross,debate}.md` (cross/reconciler/cell ported from `dau-*`; **dat-debate is new**). Zero-prompt enforced by `dat.sh --permit-fanout` against `scripts/dat-helpers/required-allow-patterns.txt` (exit 61). Cells write to `pending/trading-cells/` (sandboxed), promoted only after the reconcile gate. `scripts/score_bridge.py` is a near-verbatim port of proving's (same diff-check-lockstep obligation as `lake_trace.py`).
- **Status (durable state).** Phase 1–2 done; GICS universe completed (502 members, all 11 sectors). Structural invariant: a single-sector wave can never reach Tier-A (only Trend/Momentum/CrossSection are directional; CrossSection stays PROVISIONAL until cross-sector `dat-cross`, so a lone sector has ≤2 confirmed directional axes < the ≥3 quorum). Canonical promotion (operator-approved) is `common/` only — `Accounting.Universe.Common.{Types(+Member,Benchmark), Predicates}` (18 collapse-bridged shared predicates as of the 2026-06-04 wave, +`SlopePositive`); per-sector Tier-B verdicts stay in sandbox. `--debate` **first run 2026-06-04** (KO, Tier-B) — `intro_admissible_long` correctly **refuse-closed** (`allowed=false`, no `sorry`); an *accepting* Debate still awaits a ≥3-bullish-axis tape. Two 3-sector waves (`2026-06-02-tech-staples-energy`, `2026-06-04-tech-energy-staples`) both 0 Tier-A = the tape (universe-wide Trend⟂Momentum divergence), not the topology. **`categorization.json` is the 22-symbol mega-cap pilot subset, NOT the 502-symbol parquet hub** — S15/S55/S60 empty; a full-universe wave needs `build.py --categorize` over more symbols first. Per-wave verdicts + tape-vs-topology detail in memory `project_accounting_subproject` + close summaries + spec § 11–12.
- **Wave archive (§ 12, IMPLEMENTED 2026-06-01).** Blind fan-out sandboxes are now frozen to gitignored + S3-backed `accounting/waves/<wave-id>/` — `dat.sh --archive-wave <wave-id>` → `dat-helpers/archive_wave.py` (mechanical copy + `WAVE.json`; sector-slice→namespace, axes, symbols, `corpus_pin` = `categorization.json` `as_of`). `.gitignore` `/waves` + `.worktree-links` `waves` + `/dat-manual` Step 7 hook + test `t_07_archive_wave.sh` (24 assertions). Direct port of proving's `/waves`; **diff-check both `archive_wave.py` files in lockstep.** Class `trading-waves` S3 arm shipped serving-side 2026-06-02 (`serving/scripts/archive-artifact.sh`, pairs with `usc-waves`) — `--push` now lands. The S45 wave's sandbox was already wiped before this landed — **unrecoverable** (the motivating data-loss; § 11.1).
- **Axis investigation (§ 6.2, recommendation 2026-06-01).** Mirroring uscode's 6→10, three opt-in specialized axes are **recommended but deferred to post-Phase-2**: Axis 7 Liquidity/Tradability (CLAUDE.md's own LIQUIDITY; strongest, adopt Phase 2.5), Axis 8 Seasonality/Multi-timeframe (Intertemporal analog), Axis 9 RiskQuantum/Position-sizing (Sanction analog). A signal-confidence "Evidentiary" analog was **rejected** (meta-over-axes, not independent). **Axis 6 InstrumentRisk + Axis 7 Liquidity PROMOTED to the established default run-set 2026-06-05** (operator decision): `dat.sh` `DEFAULT_AXES` = the 5 core + instrument-risk + liquidity (**7 axes per no-flag slice**); `CORE_AXES` stays the 5 the Tier-A ≥3-directional-quorum language references; `--with-instrument-risk` is now a legacy no-op (dedupe-guarded). Promotion gate was satisfied — the S45 `GoldenBridge.lean` AAPL+NVDA Trend bridges discharge sorry-free (the 2026-06-04 wave). Axis 8 Seasonality + Axis 9 RiskQuantum stay **deferred** (no briefing authored; `archive_wave.py KNOWN_AXES` lists all three). Liquidity briefing (`predicates/universe/_axes/liquidity.md`) derives the `Tradable m` corroborator — gate on a price-axis Bullish, computed from `data_view.py bars` since liquidity is absent from ta-reference; failure = `bear_untradeable`.
- **S3 backup MANDATORY per `/dat-manual` (operator standing rule 2026-06-05).** Every invocation ends with `scripts/dat.sh --archive-wave <wave-id> --push` — never archive-only. The push rides the operator aws-vault lane (class `trading-waves`, exit 14 if creds locked / `archive-artifact.sh` absent); unlock + re-run rather than closing the wave S3-less.

## Status emit (`data/status/accounting.json`)

`accounting/scripts/status_emit.py` (system `python3`, no venv) writes
the StatusEmit slot to `data/status/accounting.json`. Schema is
`@qagents/diagram-kit` v0.4.0. The producer is self-contained — no
cross-subproject imports. Surface produced (kit closed set):

- 1 `framework-roster` `DiagramEmit` (summary card, one node per
  framework, focused = `Accounting/<F>/` present)
- 1 `latest-run-loci` `DiagramEmit` read verbatim from
  `examples/<anchor>/loci.json` (the brand-anchor run with the richest
  framework × judgment coverage — currently `balance_sample`,
  5 frameworks · 6 judgments · real-call TREND + MOMENTUM)
- 4 `StatCardEmit`s (`run-stats.{total,accepted,rejected,latest}`) +
  1 `KpiStripEmit` (`run-stats`, layout `fixed-4`)
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

**Two-lane writer + cron** — standard pattern per `data/specs/data-conventions-2026-05-06.md` § 5.3 (cron lane via `QAGENTS_PENDING_ROOT`, manual lane acquires `.data-write-lock`). Fires daily at 05:32 local; ROUTINES entry in `data/schedules/launchd/install.sh`. Cron-EC2 migration (`data/specs/cron-ec2-migration-2026-05-19.md`) is transport-only — script unchanged.
