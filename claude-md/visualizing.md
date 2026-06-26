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
  (`node graphs-2/kit/build.mjs`). **Close discipline:** rebuild the canonical
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
`extractor/`. `graphs/` (→ `graphs-2/`) + `charts/` are implemented; `tables/`
· `mixed3d/` · `scenes/` are scaffolds. The spec's (§ 6.x) flat dir prose predates
this reorg — this § 3 is authoritative.

**Shared (top-level, modality-neutral):**

- `extractor/` — **the highest-value deliverable** (Python, system `python3`).
  `usc_to_catalog.py` (legal, build now) + `accounting_to_catalog.py` (financial,
  driver-emit-preferred — the `Universe/S<code>/<Axis>/` tree doesn't exist yet).
  The parser **reads the `dau`/`dat` score-gate certification artifact** for
  `tier`/`agreement`; it does **not** run a green `lake build` (spec § 11.0a).
  Stays top-level: `catalog.json` feeds **every** modality, not just `graphs/`.
- `specs/` — the three POC extraction specs (provenance for the consolidated
  spec's appendix). `shared/INPUTS.md` — pointers to the axiomatized data.

**`graphs/` — node-link modality, design prompts only** (renderer = `graphs-2/`):

- **SUPERSEDED + REMOVED 2026-06-11 (G6, § 13 parity gate re-passed):**
  `graphs/cytoscape.js/`, `graphs/tensorboard/`, `graphs/bakeoff/`,
  `graphs/blender/`, `graphs/experiments/` — all subsumed by `graphs-2/` and
  deleted (`feedback_retire_dont_tombstone`; git history + the graphs2 spec +
  `VERDICT.md`-in-history preserve the bake-off). The scale-gate generator
  survived the cut at `graphs-2/sandbox/scale_catalog.py`.
- `graphs/00..02-*.prompt.md` — proof-DAG-mode (secondary) / **leaf-tier** render
  design prompts, migrated from `proving/graphs/` 2026-06-03. The 3-class/4-edge
  contract is locked in spec § 4; these carry the implementation detail the spec
  did not reproduce (token palette, geometry, animation, a11y, and the
  `Failure[]` wiring contract `verifying/web/`'s `/proof-graph/02-debug/`
  consumes). The old Claude-Design-bundle handoff + single-engine assumption are
  superseded by the § 6/§ 7 bake-off + kit-mount.

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
Phase-2 routing-layer mount into Qresev SHIPPED 2026-06-11 (§ 5.1). See
`charts/README.md` + `data/specs/visualizing-2026-06-03/charts-migration-2026-06-08/SPEC.md`.

**Modality scaffolds (`catalog.json` consumers, not yet built):**

- `tables/` — sortable/groupable grid of the lattice (a11y + export fallback).
- `mixed3d/` — the **spatial/3D** modality: a render-neutral `q3d/1` Three.js kit
  (pointcloud + surfacegrid families) over the spatial-3d lattice lens **and**
  `monitoring/`'s Three.js cost surface on its browser re-home. Seeds
  `03-spatial-3d/` (migrated from `experiments/`). **Deferred** (gated on
  cross-title coverage + monitoring's re-home). See `mixed3d/README.md` +
  `data/specs/visualizing-2026-06-03/mixed3d-migration-2026-06-08/SPEC.md`.
- `scenes/` — baked replay animation + deterministic SVG export for
  `explaining/` (spec § 8; Phase 5).

**`graphs-2/` — the Phase-4 kit, MOUNTED in both apps** (NOT a modality dir):
render-neutral core (`qgraph/1` model + `collapse.project()` + layout/style/axes)
+ adapters (`fromCatalog`/`fromProof`/`fromNodeLink`) + two backends (cytoscape/
layered) + `src/kit/mount.ts` (the G6 mount API: `mountProof`/`mountCatalog`/
`mountNodeLink`, regions/onLayout/onTapLeaf — the compose RegionSource surface) +
`sandbox/` browser gates. **Superseded `graphs/` engines 2026-06-11** (§ 13 parity
gate re-passed: 59 unit, sandbox 18/18, strict-CSP, scale 1k/5k/10k
all-seeds-salient). `kit/build.mjs` builds **three** IIFE dist bundles (global
`QViz`): `dist/kit-proof.js` (graphs only → `verifying/web/public/graphs2/kit.js`)
+ `dist/kit-strategy.js` (graphs+charts+compose → `evaluating/web/public/graphs2/
kit.js`) + `dist/kit-graphs.js` (domain-neutral node-link → `monitoring/web/public/
graphs2/kit.js`, M0). Re-sync = rebuild + cp into the app dirs + the app's
`pnpm verify` / e2e. Authoritative detail: `graphs-2/README.md`. See § 4.

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
`hero-graph.json` rewrite + canonical dist re-host-copy land at close/merge (dist is
gitignored canonical-only — `reference_graphs2_dist_stale_after_visualizing_close`).

**Dual-render hero (planned).** The first-page hero is a **silent Remotion** walk of the
7 Quantapix-Thesis steps built from the **layered backend** (the tensorboard-derivative:
fixed routing → deterministic `exportSVG` per expand/merge state, ideal fixed-frame
snapshots); the **thesis page** hosts the **cytoscape** interactive mount. Same
`hero-graph.json`, two backends (`MountKitOpts.backend:'layered'|'cytoscape'`).

**tf-graph compound LAYOUT — WIP, port resurrection next (2026-06-26).** The encoding +
graph definition are DONE + verified (above). The layered backend's tf-graph layout
(`backends/layered/compound.ts` — recursive scope boxes + edge routing, opt-in
`MountKitOpts.compound`) reads cleanly in the Assumptions pillar but **tangles in Rules**
(feedback node mis-placed, hand-rolled routing unrecoverable with >1 cross-edge).
Operator decision: stop hand-rolling — **resurrect the original tf-graph port** (deleted
in `7a466014`; recover from `7a466014^:visualizing/graphs/tensorboard/`; upstream
`hub/tensorboard`) and run it against the now-verified graph for proven routing. STUDY
the algorithm, never ship Polymer (`feedback_no_third_party_license_entanglement`).
Detail: next-steps item 10. Designing fixture landing + dist re-host-copy BLOCKED on
layout lock.

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
CSP patch lives on as the graphs-2 `pnpm patch` (Phase 4).
**Phase 4 RE-SCOPED → built from scratch as `graphs-2/`**
(spec `data/specs/visualizing-2026-06-03/graphs2-2026-06-07/SPEC.md`, promoted
2026-06-10): a render-neutral TS kit (one
`qgraph/1` model + one `collapse.project()` algorithm + two backends behind one
`Backend` interface — cytoscape public/CSP-clean + clean-room layered companion;
both adapters + both collapse impls subsumed into the core). **G0–G6 DONE + gated +
MOUNTED** in both apps (the three `dist/kit-{proof,strategy,graphs}.js` bundles,
§ 3); cytoscape ships as npm deps + a `pnpm patch` (CSP fix), NOT vendored-source.
G0–G6 implementation/gate detail (test counts, per-app mount provenance) lives in
`graphs-2/README.md` + `project_visualizing_subproject`. **Phase 5** (next): replay
animation + `explaining/` deterministic SVG export (layered backend's exportSVG is
already byte-stable).

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
  predicates, theorems, edges) → **graphs** (`graphs-2/`). A quantity mapped onto
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
  consumes graphs-2 through an **opaque `RegionSource` interface** — kits stay
  mutually unaware. **R2 lock:** placement reads the DAG's published node-region
  map (a kit *output*), positions absolutely (not named DOM slots); pure core in
  `compose/src/placement.ts`. **R3 lock:** bars resolve via an injected
  `resolveBars` (the run-emit's job; no parquet in the renderer). Gated
  (`pnpm -C visualizing/compose {test,typecheck,sandbox:verify,sandbox:verify:csp}`)
  over a fake DAG + fake run-emit. App shells (`verifying/web/`, `evaluating/web/`,
  re-homed `analyzing/`/`monitoring/`) **mount** the composed bundle via the
  kit-mount side-car — they never route between kits themselves. **The
  `evaluating/web/` mount SHIPPED 2026-06-11**: graphs-2's `KitMount` backs
  `RegionSource` in the app loader; the Qresev server's `GET /api/runs/<id>/bars`
  is the injected `resolveBars`; the fused kit is replaced by the composed
  `kit-strategy.js` bundle; structural parity + selection-contract e2e gates
  green. Overlay tiles light up as the accounting run-emit grows per-predicate
  `extras` (drift discipline pairs that emit reshape with the consumer sweep).
- **The "strategy-chart kit" is two modalities fused** and gets decomposed: the
  strategy DAG stays in `graphs-2/`; the overlays + side-view move to `charts/`;
  the Qresev mount is recomposed via the router (Phase 2), not a fused kit.

## 6. Conventions

- Terse `x/y/xs/ys` dialect, minimal comments (house style).
- License hygiene is load-bearing: keep MIT (cytoscape) and Apache (tf-graph)
  salvage separate; **nothing with Blender provenance reaches `main`**
  (`feedback_no_third_party_license_entanglement`).
- Python: root venv by absolute path is NOT needed — the extractor uses system
  `python3` (the `proving/`/`accounting/` convention; reads JSON/artifacts, not
  numerics).
- Tokens: the kit reads tokens, never literals — add a `tokens-lattice.css`
  overlay per app (axis palette / tier ramp / agreement green-amber-red); never
  redefine base tokens. **Overlay SoT = `rendering/` since 2026-06-16**
  (brand-polishing § 3b, variant A): `graphs-2/kit/tokens-{lattice,proof}{,-light}.css`
  are byte-identical mirrors of `rendering/brand/tokens/quantapix/overlay/
  {lattice,proof}-{dark,light}.css` — DO NOT edit in-kit; edit the SoT then
  re-copy (graphs-2/README.md "Brand token overlays"). graphs-2 is the only dual
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
  byte-stable golden (gated: graphs-2 `layered.test.ts`, charts
  `sandbox:export`); raster → SSIM/pixel-diff, never byte-equality.
- **T10 self-flags APPLIED 2026-06-09:** graphs-2 emits resolved `--font-mono`
  on SVG text (overlays define it; `var()` never enters an emitted document —
  asserted in test); charts `DEFAULT_TOKENS` is a declared sanctioned deviation
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
