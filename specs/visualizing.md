# visualizing — graphing the Lean4 axiomatization

A condensed, public rendering of the `visualizing/` design spec. It defines the
animated/interactive graph surface that ships inside the **Qnarre**
(`verifying/`) and **Qresev** (`evaluating/`) apps to make the Lean4
axiomatization legible — for both the legal corpus (`proving/`) and the
financial corpus (`accounting/`), through one domain-neutral kit.

## Objective

Visualize the axiomatization **along its independent axes** and display the
layered **(coverage × agreement × tier)** result as a single picture. The same
machine serves both domains; only the vocabulary differs.

- **Coverage** — what is axiomatized vs. not.
- **Agreement** — whether independently-derived "blind" cells agree with the
  hand-built golden references (the trust signal).
- **Tier** — how strong each agreement is, on a graded ladder
  (`A-full` → `A` → `B` → holds-only-under-stated-gaps).

## The one hard contract: a domain-neutral `catalog.json`

Layout is per-engine; the **data contract is not.** Every engine consumes one
interchange file plus a fixed node/edge taxonomy and status semantics. The
single highest-value deliverable is the **catalog extractor** that turns the
two corpora into that interchange — it survives any later engine swap.

**Node taxonomy** (structural → cell → agreement → leaf):

| Tier | Node | Meaning |
|---|---|---|
| structural | Title / Chapter / Section (legal) · Sector (financial) | synthesized by the loader, not stored |
| structural | Cluster | grouping of related cells |
| **cell** | one blind **(title, cluster, axis)** unit — financial: **(sector, axis)** | the unit of independent derivation |
| **agreement** | Bridge | cell ↔ golden, axis ↔ axis — the cross-cutting trust edge |
| reference | Golden structure | the hand-built reference |
| reconcile | Common / Reconciled element | shared elements lifted across slices |
| **leaf** | Axiom / Predicate / Theorem | the locked leaf-tier trio |

**Dimensions every engine must encode:** Axis (categorical — color or lane),
Tier (ordinal — saturation/badge), Agreement (green / amber / red, **the
headline** — diverging and low-tier bridges must be loud), plus cluster,
blind-vs-golden, and coverage.

**Edge taxonomy:** structural (`contains`, `decomposes`); agreement (`bridge`,
the cross-cutting trust edges); `reconciles`; and the proof-level set
(`applies` / `composes` / `inhabits` / `disjunctionCase`) drawn only in
proof-DAG mode. Direction convention: **`from` depends on `to`**.

**Status semantics:** `value: Bool` = predicate truth; `uncertainty ∈
{low, medium, high}` maps to opacity; a `failures[]` list marks predicate-false
nodes that blocked elaboration (the debug-overlay's reason for being).

## The two render modes (one kit)

1. **Lattice mode (primary)** — renders the whole catalog as a compound/metanode
   nesting: clusters hold cells, cells hold their `{axiom, predicate, theorem}`
   leaves, bridges are the cross-cutting agreement edges. Lenses recolor by
   axis / tier / agreement. This answers *where and whether* something is
   axiomatized.
2. **Proof-DAG mode (secondary)** — renders one example's proof graph with the
   debug overlay, answering *how one claim elaborates*. This is what the Qnarre
   verifier surface needs today; the engine must not regress it.

Both modes share the leaf-tier renderer; lattice mode wraps it in the
structural / cell / bridge layers.

## Domains, same machine

- **Legal (`proving/`):** blind cells fan out over **10 orthogonal axes** (5
  core always-on: Elements / Deontic / Ontology / Procedure / Structure; 5
  opt-in: Remedy / Scienter / Sanction / Intertemporal / Evidentiary). Bridges
  prove cross-axis and blind-to-golden agreement; tiers grade each bridge.
- **Financial (`accounting/`):** the blind axes are **6 signal families**
  `{Trend, Momentum, Volatility, Volume, CrossSection, InstrumentRisk}`; the 5
  hand-built frameworks `{Trend, Momentum, OptionsRisk, Sector, Drawdown}` are
  golden references scored against the blind cells via golden-bridge theorems.
  The structural grouping is the sector namespace (no cluster tier).

## Engine decision

Three earlier VSCode-extension proof-of-concepts were retargeted to an in-app web
surface (Astro + React islands). A scale-run bake-off chose **cytoscape** as the
contract-faithful, public-mount renderer (scale headroom + strict-CSP pass).
**tf-graph is kept** as the layered-collapse companion (click a cluster → collapse
to one box) — that summarization is load-bearing — via a small catalog→graphdef
adapter. A Blender node-look bet was **retired** (GPL — cannot ship). The durable
artifacts, regardless of renderer, are the **catalog extractor** and the tuned
**layout/lens recipe**.

---

*Derived from the private `visualizing/` design spec; see
[github.com/quantapix](https://github.com/quantapix) — the org is the contact
channel (issues + Discussions), and there is no contact email.*
