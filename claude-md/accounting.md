# accounting — Lean4 axiomatic theorem-proving for portfolio evaluation

Sibling of `proving/`, `analyzing/`, `trading/`, `evaluating/`. Cross-project
rules: root `CLAUDE.md`. Backs the **Qresev** product — public slice at
`qresev-public`.

The financial-domain parallel of `proving/`. Same three-layer split,
different domain: instead of complaints under federal statutes, it proves
portfolio-level judgments (TREND, MOMENTUM, OPTIONS-RISK, SECTOR, DRAWDOWN)
over OHLCV bars + indicator series + GICS sector mappings.

## The split (mirror of proving/)

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Accounting/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls. |
| **Predicate functions** | `predicates/<framework>/*.md` | one portfolio JSON + bar/indicator evidence (via `scripts/data_view.py`) | a single `Bool` (plus evidence + uncertainty) | LLM sub-agent (`context: fork`). |
| **Driver** | `scripts/extract_facts.py` | manifest + portfolio | the framework's generated `Facts.lean` (axioms) + audit JSON | LLM invocations (Haiku by default). |

The Lean kernel never reads OHLCV bars, indicator series, parquet, or JSON.
The predicate sub-agents never write Lean. The driver is a thin coordinator
with no financial reasoning of its own. The verifiable proof IS the Lean
elaboration trace produced by `lake build`.

## Frameworks

| Framework | Kernel | Top-level judgment(s) | Predicates |
|---|---|---|---|
| **Trend** | `Accounting/Trend/` | `is_uptrend`, `is_downtrend` | 5 (sma_cross_up, slope_positive, r_squared_geq, adx_geq, volume_confirmation) |
| **Momentum** | `Accounting/Momentum/` | `has_momentum` | 4 (rsi_in_range, macd_bullish_cross, roc_positive, momentum_percentile_geq) |
| **OptionsRisk** | `Accounting/OptionsRisk/` | `defined_risk_only`, `is_clean` | 6 (leg_allowed, covered_call_collateralized, protective_put_bounded, no_naked_short_options, debit_only, max_loss_bounded) |
| **Sector** | `Accounting/Sector/` | `has_violation`, `no_violations` | 3 (cap_respected, gics_mapped, sector_concentration_leq) |
| **Drawdown** | `Accounting/Drawdown/` | `drawdown_disciplined` | 3 (max_drawdown_leq, time_under_water_leq, recovery_within) |

The kernel's predicate names are the contract the Qresev `/app` Lean trace
consumes — they do not get renamed without lockstep UI edits. A shared
`Accounting/Common/` carries opaque cross-framework types (Symbol, Bar,
Window, Portfolio, Holding, OptionLeg), the closed six-strategy `Strategy`
enum, the eleven-value `GicsSector` enum, and opaque bar accessors
mirroring the canonical `{ts, o, h, l, c, v, adj_c}` shape.

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** The kernel is pure.
2. **Predicate specs MUST NOT cite or read the kernel Lean files.** Their
   world is the portfolio JSON + bar evidence + spec rubric.
3. **The driver MUST NOT make financial judgments.** It routes calls and
   serialises results.
4. **`Facts.lean` is generated. Never hand-edit.** All are gitignored.
5. **Defined-risk only — non-negotiable.** Any options leg outside the six
   allowed strategies (`long_call`, `long_put`, `debit_spread_call`,
   `debit_spread_put`, `covered_call`, `protective_put`) is REFUSED at the
   predicate layer; the kernel encodes the same restriction at the type
   level via the closed `Strategy` enum. Both must remain in force.
6. **Bar shape canonical.** Any code that reads parquet uses the
   `{ts, o, h, l, c, v, adj_c}` columns; vendor names never leak past
   `scripts/data_view.py`.

## Cross-project boundaries

- **OHLCV bars** — read via `scripts/data_view.py` from the shared
  market-data parquet hub. Do NOT import the analyzer's TypeScript views or
  the trading Python directly.
- **Indicator math** — a Python TA-Lib reference is the ground truth;
  predicate sub-agents MAY shell out to it as a numerics escape hatch.
- **GICS sectors** — read from the shared symbol-keyed parquet via a thin
  loader.
- **Downstream consumer** — the Qresev web app calls the driver as a
  subprocess; it never imports the kernel Lean directly.

## Results propagation — `scripts/{lean_parse,lake_trace,report}.py`

Mirror of proving/'s propagation pipeline, adapted for the multi-judgment
accounting case. Each run produces a per-run report (with a `judgments[]`
list), a proof DAG byte-compatible with the proof-graph rendering kit, and
a status-hub diagram. `lake_trace.py` is a verbatim copy of proving's and
MUST be patched in lockstep; the deliberate accounting-side divergences
(lowercase axiom names, dotted conclusion heads for multi-judgment runs,
the multi-judgment loci roster) are not drift.

## Axiomatize-trading program

Extends the five hand-built frameworks to a phased, **sector-by-sector**
program over the whole S&P 500 universe, produced redundantly by Opus
subagent teams along ≥ 5 orthogonal **signal-family** axes (Trend /
Momentum / Volatility / Volume / CrossSection [+ InstrumentRisk]), then
reconciled. Cross-axis agreement, proved in the kernel via `Bridge.lean`
lemmas, IS the correctness signal — and it coincides with the practitioner's
**confluence** heuristic (independent indicator families agreeing).

- **Slice unit:** the `(GICS sector, axis)` cell; sector code → namespace.
  GICS is the drill-down spine. The corpus is the existing market-data
  parquet hub.
- **Golden reference:** the existing five frameworks on the worked
  examples, scored via golden-bridges (not exact-string — naming is a free
  variable, per the U.S. Code program's lesson).
- **Debate framework:** a new sixth kernel framework formalizes the
  trading side's bull-vs-bear gate "proven at every step". `admissible_long`
  is a structure with no constructor omitting any field — it requires the
  bull confluence claim, the kernel directional accept, a defined-risk-clean
  check, and the negation of every bear disqualifier. "Veto, not a vote"
  becomes a type-level property.
- **Lane:** programmatic batch (gated on the 2026-06-15 credit) + a
  manual-interactive bridge via the `/dat-manual` skill. Cells write to a
  gitignored sandbox, promoted only after a reconcile gate.
- **Status:** spec + scaffolding drafted; not yet runnable at scale —
  Phase-1 gating items remain.

## Toolchain notes

Lean pinned via `lean-toolchain` (matches `proving/`); no Mathlib
dependency. Lean4 authoring gotchas to apply when adding kernels: `private`
is reserved and can't be an `inductive` constructor name; a `: Prop`
structure can't carry Type-valued data fields — put classification data in
`def`s. `scripts/data_view.py` is pandas-only. The driver shells out to
Haiku by default (a cost choice, not a capability constraint).
