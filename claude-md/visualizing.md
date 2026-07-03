# CLAUDE.md — visualizing/

Project-specific rules for the qagents axiomatization-graphing surface. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`. Don't
re-litigate those.

**Registered subproject (2026-06-03).** Authoritative contract:
**`data/specs/visualizing-2026-06-03/SPEC.md`**. Subproject memory:
`project_visualizing_subproject`.

## 1. What this is

The graphing surface for the `proving/` (legal) + `accounting/` (financial)
Lean4 axiomatizations. **Not** a VSCode extension — an animated/interactive
**page in Qnarre (`verifying/web/`) + Qresev (`evaluating/web/`)** via the
kit-mount pattern (`project_proof_graph_kit_mount_pattern`). One domain-neutral
kit **consolidates** the two mounted today (proof-graph + strategy-chart).

Two render modes, one kit:

- **Lattice** (primary) — the catalog: coverage × agreement × tier over
  `catalog.json`. Headline is **agreement**, not a proof trace.
- **Proof-DAG** (secondary) — the existing single-complaint render (`graph.json`
  v1, the locked 3-class / 4-edge contract = the leaf tier). Must not regress the
  Qnarre `/app` verifier debug overlay. **Additive H3 layer (R10, 2026-06-20):**
  hierarchical-predicate runs also carry a `derived` node + `decomposes` edge
  (propagation spec § 2.3); the kit folds `derived`→`predicate` (NO `model.ts`
  kind-union widening) so it renders "computed" (no `value`), and keeps
  `decomposes` in the elaboration view. Present only on decomposed runs — a v1
  graph without them renders byte-identically. A `derived-underivable` failure
  carries `derivedNode` + an **empty `axiomName`**, so the kit attributes it via
  a `failByNode` map (keyed on node id), not `failByAxiom` (`proof.ts`; spec
  § 2.3). **Composite NESTING (handoff 2026-06-21):** in the elaboration view each
  `derived` composite gets its own collapsible **container** (a `derived`
  *ComponentKind* — a CONTAINER kind, not a NodeKind widening; never crosses the
  wire seam) built from its decomposition subtree (the composite node + its
  `decomposes`-target axioms + the predicates that `inhabit` them), parented on the
  Predicates kind-plate. Containers start **collapsed** (`mount.ts` seeds the
  default `CollapseState`) so the proof opens showing composites; a composite's
  leaves appear only on expand — the hierarchy is structural, not just
  `decomposes` lines through one flat plate. Still byte-compat: a graph with no
  `derived` nodes builds zero containers. The `dist/` bundles are **gitignored canonical-only build state** —
  never committed; rebuild at canonical so the apps re-sync a current build
  (`node graphs/kit/build.mjs`). **Close discipline:** rebuild the canonical
  dist BEFORE `/close` — worktree removal does NOT regenerate it, so it lags the
  merged source and bit the consumer side twice on 2026-06-21
  (`reference_graphs2_dist_stale_after_visualizing_close`).

## 2. The one hard contract — `catalog.json` (domain-neutral)

The only cross-engine mandate is the shared data layer; layout is per-engine.

- **Schema:** `qcatalog/1` — `cells` / `bridges` / `leaves` only. Structural
  compounds (Title / Chapter / Cluster / Section / Sector) are **derived by the
  loader**, never stored. Full shape in the spec § 3.1.
- **A cell** is one blind `(title, cluster, axis)` unit (financial:
  `(sector, axis)`, no cluster). **Section is a leaf sub-grain, not a cell.**
- **Golden refs are addressable cells** (`blindOrGolden:"golden"`); no separate
  collection. `failures[]` is **proof-DAG-only** — in the lattice a contested
  cell is `agreement:"diverge"` + low `tier`.
- **Path / ownership (data-hub, single-owner-per-phase):**
  `data/visualizing/<domain>-catalog.json` (`legal-`/`financial-`; the third
  `operational-` domain is live from axiomatize-git Phase 1 but CO-LOCATED at
  `studying/Operating/emits/` — NO `data/` copy ever, `monitoring/` reads the
  kernel tree directly; representation-guide § 4 / R6). Phase 1 →
  the `visualizing/` extractor is sole owner; Phase ≥3 → ownership transfers to
  the `dau`/`dat` driver-emit (discrete cutover, never a both-write window). See
  `data/visualizing/CLAUDE.md`.

## 3. Layout

Organized by output **modality** (reorg 2026-06-03): one dir per render shape —
`graphs/` · `tables/` · `charts/` · `mixed3d/` · `scenes/` — each reading the
**same** modality-neutral `catalog.json` from the **shared, top-level**
`extractor/`. `graphs/` + `charts/` are implemented; `tables/` · `mixed3d/` ·
`scenes/` are scaffolds. The spec's (§ 6.x) flat dir prose predates this reorg —
this § 3 is authoritative. (Until 2026-07-02 the kit lived at `graphs-2/` beside
a prompts-only `graphs/`; the consolidation merged them —
`data/specs/visualizing-2026-06-03/graphs-2026-07-02/SPEC.md`.)

**Shared (top-level, modality-neutral):**

- `extractor/` — **the highest-value deliverable** (Python, system `python3`).
  `usc_to_catalog.py` (legal, build now) + `accounting_to_catalog.py` (financial,
  driver-emit-preferred — the `Universe/S<code>/<Axis>/` tree doesn't exist yet).
  The parser **reads the `dau`/`dat` score-gate certification artifact** for
  `tier`/`agreement`; it does **not** run a green `lake build` (spec § 11.0a).
  Stays top-level: `catalog.json` feeds **every** modality, not just `graphs/`.
- `specs/` — the three POC extraction specs (provenance for the consolidated
  spec's appendix). `shared/INPUTS.md` — pointers to the axiomatized data.

**`graphs/` — the node-link modality = the uniform kit, MOUNTED in four apps**
(`@qagents/graphs`, pnpm workspace member; was `graphs-2/` until 2026-07-02):
render-neutral core (`qgraph/1` model + `collapse.project()` + layout/style/axes
+ merge/inductive/method) + adapters (`fromCatalog`/`fromProof`/`fromNodeLink`/
`fromConstellation`) + **ONE backend — cytoscape + fcose** — + `src/kit/mount.ts`
(the mount API: `mountProof`/`mountCatalog`/`mountNodeLink`/`mountConstellation`,
regions/onLayout/onTapLeaf — the compose RegionSource surface) + `sandbox/`
browser gates. **The layered branch (tf-graph derivative) was ELIMINATED
2026-07-02** (`graphs-2026-07-02/SPEC.md` § 4;
`feedback_retire_dont_tombstone`): `backends/layered/`, the `layered` LayoutSpec
kind + `cytoscape-dagre`, `MountKitOpts.backend`/`compound`, `layered.test.ts`,
`scenes/hero-frames.mjs` — all deleted; ordering is owned by **fcose constraint
mechanisms** (flow-edge-derived today, § 3 of that spec). `kit/build.mjs` builds
**three** IIFE dist bundles (global `QViz`): `dist/kit-proof.js` (graphs only →
`verifying/web/public/graphs2/kit.js`) + `dist/kit-strategy.js`
(graphs+charts+compose → `evaluating/web/public/graphs2/kit.js`) +
`dist/kit-graphs.js` (domain-neutral node-link → `monitoring/web/public/graphs2/
kit.js` + the designing hero). App mount dirs keep the historical `graphs2` name.
Re-sync = rebuild + cp into the app dirs + the app's `pnpm verify` / e2e.
Authoritative detail: `graphs/README.md`. See § 4. Also in-dir:
`00..02-*.prompt.md` — the proof-DAG leaf-tier design prompts (migrated from
`proving/graphs/` 2026-06-03; token palette, geometry, animation, a11y, and the
`Failure[]` wiring contract `verifying/web/`'s `/proof-graph/02-debug/` consumes;
their Claude-Design-bundle handoff framing is superseded). The 2026-06-03..11 POC
engines (cytoscape.js / tensorboard / bakeoff / blender) live only in git
history; survivor: `graphs/sandbox/scale_catalog.py`.

**`charts/` — quantitative modality (BUILT, Phase 1 2026-06-08; `@qagents/charts`
workspace member):** the render-neutral `qchart/1` kit — closed-set series model
(`timeseries`/`bar`/`curve`/`payoff`/`distribution`) + `validate()`; two adapters
(`fromCatalog` aggregate rollups · `fromReport` per-framework overlays +
`predicate-selected` OHLCV `sideView`, with the defined-risk REFUSED enforced at
the `fromReport` boundary not just visually); five vanilla-SVG family emitters
(strict-CSP-clean + byte-stable export for `explaining/`); a lightweight-charts v5
backend (dynamic-imported live OHLCV side-view + candlestick) behind one
`ChartBackend` interface (spec § 7 L1). Gated: `pnpm -C visualizing/charts {test,
typecheck, sandbox:verify, sandbox:verify:csp, sandbox:export}`. Holds the migrated
design prompts (`00`/`01`/`02-*.prompt.md`, from `evaluating/notes/` 2026-06-08).
Phase-2 routing-layer mount into Qresev SHIPPED 2026-06-11 (§ 5.1).
**Re-chartered 2026-07-02 — authoritative contract is now
`data/specs/visualizing-2026-06-03/charts-2026-07-02/SPEC.md`** (debated +
adopted, `data/debates/charts-mixed3d-2026-07-02.md`): LW-charts v5 widens to
multi-series/panes(price+3)/markers/upsert-`append` (qchart/1.1 additive +
`chartsCaps()` probe); indicators are DATA never kit code; § 5 pins the
accounting extras reshape target (C4, chart-key-presence dormancy); § 6 adds
the `qcatalog-trend/1` append-only rollup log (in-session lock-protected
appends, never `pending/`); § 7 mount map (verifying `/lattice` panel via
`QViz.charts.*` in kit-proof; Qresev tile activation = face change →
FINANCIALLY re-scan). The migration spec deletes at the W1 citation sweep.

**Modality scaffolds (`catalog.json` consumers, not yet built):**

- `tables/` — sortable/groupable grid of the lattice (a11y + export fallback).
- `mixed3d/` — the **interactive-3D** modality (Three.js, MIT; `scenes/` =
  baked Blender-provenance media, firewalled): render-neutral `q3d/1` kit,
  kinds `pointcloud | surfacegrid | panelset` (charts-in-3D = opaque
  fully-resolved SVG payloads, composed via a compose `PanelSink` at M3, never
  parsed). **Re-chartered 2026-07-02 — authoritative contract is
  `data/specs/visualizing-2026-06-03/mixed3d-2026-07-02/SPEC.md`** (debated +
  adopted; PRIVACY gate PC1–PC6): phase order INVERTED — M1 surfacegrid kit +
  M2 monitoring cost mount first (its re-home gate cleared 2026-06-17;
  `hourlyBreakdown` stranded), embedding pointcloud lens LAST (R1 kill
  criterion carried). Seeds `03-spatial-3d/`. The migration spec deletes at
  the W1 citation sweep.
- `scenes/` — baked replay animation + frame export for `explaining/` (spec § 8;
  Phase 5). Frame capture rides the cytoscape kit (headless Playwright —
  `sandbox/serve.mjs` + `__CY__.png()`/`exportSVG`; the pure-Node layered
  snapshot path was deleted with the layered branch, 2026-07-02).

**M0 node-link reader (done 2026-06-17).** `fromNodeLink(wire, view)` reads the
`qgraph-wire/1` networkx envelope (shared `code/lean_graph` + `uscode_graph`
serializer): mandatory `KIND_MAP`/`REL_MAP` normalizers (`validate()` does NOT
enforce kind enums), a `cl:`-prefixed cluster→Component forest derived from
`cluster`/`cluster_kind` (node-id ↔ cluster-path collide by design), and
dangling-`anchors` tolerance (the cross-axis anchor points out of the K-graph).
`axesFor('operational')` → `OPERATIONAL_AXES` (the 7 git axes; was the M0 blocker).
NO `model.ts` widening (type-decls fold onto `axiom`; `Section`→existing kind).
Drives the monitoring/ operational mount (next M0 item) + later the uscode mount
in verifying/ (M2). Report: `data/tmp/uscode-graph-monitoring-pipeline-2026-06-16/
REPORT.md` § 3; debate `data/debates/uscode-graph-monitoring-pipeline-2026-06-16.md`.

**Method-DAG hero — three general node-link capabilities (done 2026-06-25).**
Built for the designing/ homepage+thesis hero (an authored, interactive INDUCTIVE
method DAG), all general + byte-compat for wires that omit them — full encoding
reference in **`data/specs/visualizing-2026-06-03/SPEC.md` § 15**: (1) **cluster-as-
node edges** (`nodelink.ts` `source_kind`/`target_kind:"cluster"` → the `cl:`
Component; model/collapse/backend already permitted compound endpoints); (2)
**expansion-state merge** (`graph.merge`, `core/merge.ts`; LEAF + INDUCTIVE modes;
`mount.ts` tracks a `merged` flag); (3) **inductive clusters** (`graph.inductive`
seeds 2 normal + 1 generator; `core/inductive.ts` `addInductiveChild`/
`realizeInductive`; per-role `PARTS`/`MIN` grammar scoped to host subtree) + role→
shape (circle/star/triangle/hexagon) + `MountKitOpts.showLabels`/`nodeScale`/
`legend()`. The hero FIXTURE (`hero-graph.json`) + `loader.js` are designing-owned
(lifted there 2026-06-25); the kit is visualizing's.

**Predicate-calculus encoding refinement (2026-06-26).** The LLMs' predicate
dependency is now explicit: each `Input`-fed LLM (A/R/P, never C) is a non-terminal
compound holding an inductive **`Predicates +`** cluster (new role `predicate`, ◇
diamond — added to `inductive.ts` PARTS/MIN, `mount.ts` ROLE_SHAPE+legend,
`elements.ts`); the per-pillar `Predicates → destination` edge is **cluster→cluster**
onto PROMOTED single-leaf destination sub-clusters (A:Axioms / R:Concepts+Propositions /
P:Theorems). Two kit generalizations rode in: `realizeInductive` is now
**generator-SCOPED** (won't wire the non-inductive destinations), and `applyMerge` folds
each trigger's **WHOLE subtree** (descendant-fold + `cl:`-keyed rewire) — both
byte-compat for flat/non-method wires (112 tests green incl. `test/hero-method.test.ts`;
sandbox 23/23 + CSP). Spec § 15 carries the full reference. The designing-side
`hero-graph.json` rewrite **landed 2026-07-01** (single-terminal ◇ Predicates in each
A/R/P LLM, never C; refreshed `kit.js` from `kit-graphs.js`; Mode-A lift-across, left
STAGED in the live designing worktree for its session to commit — next-steps item
10b(b)). The canonical dist re-host-copy into the OTHER consumers
(verifying/evaluating/monitoring `kit.js`) still lands at close/merge (dist is
gitignored canonical-only — `reference_graphs2_dist_stale_after_visualizing_close`).

**Single-render hero (re-decided 2026-07-02).** The dual-render plan (layered
Remotion walk / cytoscape thesis page) died with the layered branch: **one
cytoscape-fcose source** serves both the silent hero video (headless capture per
expand/merge state — next-steps item 12 pipeline) and the `/thesis` interactive
mount. Same `hero-graph.json`, one backend.

**Method-DAG grammar + flow/use + fcose constraints (2026-06-27, layered parts
retired 2026-07-02).** **Graph-def corrections** (live operator review): firewall
is **A-ONLY** (`Predicates→Axioms` — predicates can only DECIDE axioms); R/P
connect via the **LLM compound** (`R/LLM→Concepts+Propositions`,
`P/LLM→Theorems`); Input drills into Predicates only in A; merged grammar `S→T`
forbidden, **`proof→theorem` (P→T)** not T→P, axiom fed by nothing; `merge.ts`
clamps `Concepts→(Propositions descendant)` to the boundary. **flow/use edges**
(`elements.ts`): USE = `dst∈{structure,theorem} AND src∈{proposition,structure,
theorem,proof}` (the merged Propositions-bubble composition = Lean4 tactic
search) — thin/dashed/`--halo`; everything else FLOW — thick/solid/`--edge`.
**fcose flow-constraints** = `relativePlacementConstraint` from forward flow
edges (back-edges dropped by DFS — the Quantapix→LLM feedback return must not
pin the LLM below Quantapix), **overview-only** (degenerates when a constrained
leaf sits in an EXPANDED compound kernel → guard bails when any kernel opens);
the kernel-spine `alignmentConstraint` is computed but not emitted (same
degeneration). Explicit `feedback` edge class + rank constraints = the successor
track (graphs-2026-07-02 § 3/§ 10 debate). **Fixture simplification**
(`test/fixtures/hero-method.json`): Predicates = single TERMINAL node per LLM (no
inductive cluster); split kernels = TERMINAL leaves (no expansion); inductive
machinery lives ONLY in the merged kernel. **NEXT: debug the merged Kernel.**
The clean-room tf-graph compound port (`compound.ts`) that fixed the Rules
tangle was deleted with the layered branch — the layered-layout LOCK item is
moot.

**Constellation modality (M) + cluster-lens (done 2026-06-17).** studying's
SECOND operational input — the qagents monorepo + `~/.claude` memory as one
non-hierarchical graph (`graph.kind="constellation"`; producer
`studying/scripts/extract_constellation.py`, golden
`studying/Operating/emits/constellation/golden.json`). `fromConstellation` +
`mountConstellation` implement **Option B** of
`data/tmp/uscode-graph-monitoring-pipeline-2026-06-16/constellation-amendment-2026-06-17.md`
§ 2 (RESOLVED): M's scoped node/edge kinds ride the open attrs bag
(`attrs.kindClass`/`relKind`) folded onto distinct `qgraph/1` carriers — **NO
`NodeKind`/`EdgeKind` union widening** (that is Option C; re-opens R2's held-open
veto). The general **M1 cluster-lens** (`colorLens:'cluster'` + `clusterTokens`
`--cluster-*` ring) is M's headline (communities are its visual; no `--axis-*`).
The `--rel-*` edge palette is a HOST-overlay token class (monitoring's operational
overlay, like the 7 `--axis-*`; NOT the rendering-SoT lattice/proof mirrors). The
`--cluster-*` ring, **as of 2026-06-18, IS in the lattice brand overlay SoT** —
Claude Design's Variant A "Spectral arc" (teal→amber sweep, re-indexed 0..11) was
adopted into `rendering/brand/tokens/quantapix/overlay/lattice-{dark,light}.css` +
the kit mirrors so the cluster lens reads the same palette everywhere; monitoring's
`tokens-constellation.css` keeps the DARK SoT (constellation is dark-only, no light
twin). It rode in with three cluster-lens styling knobs — `--halo-alpha` (community
compound tint), `--edge-trust-{lo,mid,hi}` (bridge opacity ramp), `--hub-glow` (hub
underlay bloom) — wired into the cytoscape backend (`elements.ts`; `parseGlow` +
`numTok` with graceful fallbacks so proof, which omits them, is unaffected). Design
provenance + the render slice live in rendering's `designs/` (the visualizing-lattice
slice; see its README + manifest). The
**M1 picture floor** (REPORT § 4) shipped 2026-06-17 alongside: four
opt-in `StyleSpec`/`MountKitOpts` knobs — `sizeBy:'degree'|'centrality'`
(normalized `degN`/`cenN` ramp on leaves; compounds auto-size), `labelMinDegree`
(declutter: hide low-degree labels, `.lbl` hover-reveal), `edgeRouting` (from the
`LayeredGraph.render?.edges` hint), and `overviewDepth` (`collapseToDepth`
wiring). Lattice/proof defaults are untouched (no regression); `mountConstellation`
defaults to `sizeBy:'degree'`+`labelMinDegree:3`. Halos + a kit-side inspector are
explicitly OUT (community compounds already box-and-tint; inspector is host
chrome). monitoring owns the `/constellation` view (landed 2026-06-17) + the
mechanical kit-dist re-host-copy (next-steps § C item 8). Spec:
`data/specs/lean4-charter-2026-06-10/constellation-graph-2026-06-17/SPEC.md` § 8.

## 4. Phased roadmap (spec § 12)

Phase 0 ✅ registration. Phase 1 ✅ catalog extractor for T18
(`extractor/usc_to_catalog.py` → `qcatalog/1`; financial deferred until
axiomatize-trading builds `Universe/S<code>/<Axis>/`). **Phase 2 ✅ cytoscape
web-port** + **Phase 3 ✅ scale bake-off** — POC engines superseded + removed
2026-06-11 (§ 3, which carries the bake-off-preservation detail); the cytoscape
CSP patch lives on as the graphs `pnpm patch` (Phase 4).
**Phase 4 RE-SCOPED → built from scratch as the kit** (G0–G6 DONE + gated +
MOUNTED; the two-backend charter was superseded 2026-07-02 by
`data/specs/visualizing-2026-06-03/graphs-2026-07-02/SPEC.md` — **single
cytoscape-fcose backend**, layered eliminated, dir `graphs-2/` → `graphs/`,
package `@qagents/graphs`). cytoscape ships as npm deps + a `pnpm patch` (CSP
fix), NOT vendored-source. Implementation/gate detail (test counts, per-app
mount provenance) lives in `graphs/README.md` +
`project_visualizing_subproject`. **Phase 5** (next): replay animation +
`explaining/` frame export on the cytoscape capture path (settle-based
determinism — seeded fcose + constraints; raster acceptance = SSIM, never
byte-equality).

## 5. Seam discipline — JSON only

The only seam between `visualizing/` and the app shells / domain projects is
JSON (`catalog.json`, `graph.json` v1). **No cross-subproject imports**
(`feedback_cross_project_data_sharing`). No Lean parsing in the renderer; the
kit consumes JSON, the extractor produces it. `loader.js` is the never-fold
side-car — a schema change is a two-sided edit (spec § 3.1 / R5;
`proving-results-propagation-2026-05-09.md` § 2.3).

## 5.1 Modality boundary + composition (locked 2026-06-08)

`data/specs/visualizing-2026-06-03/charts-migration-2026-06-08/SPEC.md` § 3/§ 7. Subproject-local
by decision (L4) — **not** promoted to root `CLAUDE.md`.

- **One modality per visual primitive class.** Node-link topology (cells,
  predicates, theorems, edges) → **graphs** (`graphs/`). A quantity mapped onto
  a value/time axis (timeseries, bar, curve, payoff, distribution, candlestick)
  → **charts** (`charts/`). 3D/spatial surfaces → **mixed3d**. A kit renders
  exactly one modality and is **unaware of the others** — no inter-kit
  anchor/coordinate seam.
- **Composition is a visualizing-owned routing layer** (`visualizing/compose/`,
  `@qagents/compose` — **BUILT Phase 2 2026-06-08**), a `visualizing/`-level
  package sibling of the modality kits — **not** a `code/` hub and **not** a
  root/qagents concern. The router owns cross-modality placement + typed event
  wiring (DAG `predicate-selected` → charts `sideView`); it holds no domain logic
  and no kit internals (R1). It depends on `@qagents/charts` (drives it) but
  consumes the graphs kit through an **opaque `RegionSource` interface** — kits stay
  mutually unaware. **R2 lock:** placement reads the DAG's published node-region
  map (a kit *output*), positions absolutely (not named DOM slots); pure core in
  `compose/src/placement.ts`. **R3 lock:** bars resolve via an injected
  `resolveBars` (the run-emit's job; no parquet in the renderer). Gated
  (`pnpm -C visualizing/compose {test,typecheck,sandbox:verify,sandbox:verify:csp}`)
  over a fake DAG + fake run-emit. App shells (`verifying/web/`, `evaluating/web/`,
  re-homed `analyzing/`/`monitoring/`) **mount** the composed bundle via the
  kit-mount side-car — they never route between kits themselves. **The
  `evaluating/web/` mount SHIPPED 2026-06-11**: the graphs kit's `KitMount` backs
  `RegionSource` in the app loader; the Qresev server's `GET /api/runs/<id>/bars`
  is the injected `resolveBars`; the fused kit is replaced by the composed
  `kit-strategy.js` bundle; structural parity + selection-contract e2e gates
  green. Overlay tiles light up as the accounting run-emit grows per-predicate
  `extras` (drift discipline pairs that emit reshape with the consumer sweep).
- **The "strategy-chart kit" is two modalities fused** and gets decomposed: the
  strategy DAG stays in `graphs/`; the overlays + side-view move to `charts/`;
  the Qresev mount is recomposed via the router (Phase 2), not a fused kit.

## 6. Conventions

- Terse `x/y/xs/ys` dialect, minimal comments (house style).
- License hygiene is load-bearing: the MIT cytoscape chain is the only
  third-party surface (the Apache tf-graph salvage exited with the layered
  branch, 2026-07-02); **nothing with Blender provenance reaches `main`**
  (`feedback_no_third_party_license_entanglement`).
- Python: root venv by absolute path is NOT needed — the extractor uses system
  `python3` (the `proving/`/`accounting/` convention; reads JSON/artifacts, not
  numerics).
- Tokens: the kit reads tokens, never literals — add a `tokens-lattice.css`
  overlay per app (axis palette / tier ramp / agreement green-amber-red); never
  redefine base tokens. **Overlay SoT = `rendering/` since 2026-06-16**
  (brand-polishing § 3b, variant A): `graphs/kit/tokens-{lattice,proof}{,-light}.css`
  are byte-identical mirrors of `rendering/brand/tokens/quantapix/overlay/
  {lattice,proof}-{dark,light}.css` — DO NOT edit in-kit; edit the SoT then
  re-copy (graphs/README.md "Brand token overlays"). The graphs kit is the only dual
  `core+dark+light` consumer (C-VZ2); theme selection is at the app's committed
  `<app>/web/public/graphs2/` copy. Tier ramp is frozen at `{a-full,a,b,modulo,
  unknown}` — **no `--tier-uncovered`**; an uncovered cell is `tier:unknown` +
  `coverage:false` (studying emit is SoT-aligned; adding the value is a non-goal).

## 7. rendering/ seam (rendering-spec debate, Round 01 — 2026-06-09)

Joined VZ1–VZ5 (record `data/debates/rendering-spec-2026-06-09.md`; CLEARED
digest `data/debates/cleared/rendering-spec-2026-06-09.md`; reconciled spec
`data/tmp/rendering-2026-06-09/SPEC.md` → `data/specs/` at P0). Standing bounds:

- **The kit is the only lattice/proof-DAG renderer** (VZ4): rendering/ mounts
  the kit or consumes kit-emitted SVG; it never re-implements layout from
  `catalog.json`/`graph.json`. `scenes/` stays visualizing-owned content
  production; rasterization/composition ride rendering/'s engines downstream.
- **Brand reaches the kits only via the host shells' build-time token copies**
  (VZ1/T4); no kit-side token file, no fetch — runtime `rendering/brand/` fetch
  forbidden. The visualizing-lattice slice under rendering's `designs/` is net-new
  (landed 2026-06-18; no `visualizing-design` bundle ever existed); zero P4
  migration cost.
- **Acceptance split** (VZ3/T5): vector from resolve-at-emit sources →
  byte-stable golden (gated: charts `sandbox:export`; the graphs
  `layered.test.ts` golden retired with the layered branch 2026-07-02 — graph
  frame capture is raster/SSIM via the cytoscape path); raster → SSIM/pixel-diff,
  never byte-equality.
- **T10 self-flags APPLIED 2026-06-09:** any kit-emitted SVG resolves
  `--font-mono` at emit (overlays define it; `var()` never enters an emitted
  document); charts `DEFAULT_TOKENS` is a declared sanctioned deviation
  (header note in `charts/src/style/style.ts`) — register under manifest
  `sanctioned_deviations` when the design source lands in rendering/; the P5
  `managing/` drift check covers both.
- **Defined-risk backstop** (VZ5): `brand/BRAND.md` cites
  `charts/src/adapter/report.ts`'s `fromReport` refusal boundary; refused legs
  never produce a series, so no rendered artifact can depict them as
  constructible.

## 8. Status slot

`scripts/status_emit.mjs` writes `data/status/visualizing.json` (kit
`KIT_VERSION` pinned in lockstep with `@qagents/diagram-kit`). The card is
**hidden from the `/status` index** until a real mounted surface exists (Phase 4)
— the deep page `/status/visualizing/` still builds. Reverse the hide by adding
`visualizing` to a `STATUS_GROUPS` member array in `designing/web/src/content/
copy.ts` plus the e2e sweep in `tests/e2e/status.spec.ts`.
