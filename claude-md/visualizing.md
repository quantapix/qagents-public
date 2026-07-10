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
kit (`@qagents/graphs`, § 3) already serves both apps + monitoring.

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
  `derived` nodes builds zero containers. The `dist/` bundles are gitignored
  canonical-only build state — rebuild at canonical BEFORE `/close`
  (`node graphs/kit/build.mjs`; worktree removal does NOT regenerate them, so they
  lag the merged source — `reference_graphs2_dist_stale_after_visualizing_close`).

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
`extractor/`. `graphs/` + `charts/` + `mixed3d/` (M1) are implemented; `tables/`
· `scenes/` are scaffolds. The spec's (§ 6.x) flat dir prose predates this reorg —
this § 3 is authoritative.

**Shared (top-level, modality-neutral):**

- `extractor/` — **the highest-value deliverable** (Python, system `python3`).
  `usc_to_catalog.py` (legal, built); the financial twin is deferred until
  axiomatize-trading builds `Universe/S<code>/<Axis>/` (driver-emit-only until then).
  The parser **reads the `dau`/`dat` score-gate certification artifact** for
  `tier`/`agreement`; it does **not** run a green `lake build` (spec § 11.0a).
  Stays top-level: `catalog.json` feeds **every** modality, not just `graphs/`.
- `specs/` — the three POC extraction specs (provenance for the consolidated
  spec's appendix). `shared/INPUTS.md` — pointers to the axiomatized data.

**`graphs/` — the node-link modality = the uniform kit, MOUNTED in four apps**
(`@qagents/graphs`, pnpm workspace member):
render-neutral core (`qgraph/1` model + `collapse.project()` + layout/style/axes
+ merge/inductive/method) + adapters (`fromCatalog`/`fromProof`/`fromNodeLink`/
`fromConstellation`) + **ONE backend — cytoscape + fcose** — + `src/kit/mount.ts`
(the mount API: `mountProof`/`mountCatalog`/`mountNodeLink`/`mountConstellation`,
regions/onLayout/onTapLeaf — the compose RegionSource surface) + `sandbox/`
browser gates. **The layered branch (tf-graph derivative) was ELIMINATED
2026-07-02** (`graphs-2026-07-02/SPEC.md` § 4; `feedback_retire_dont_tombstone`);
ordering is owned by **fcose constraint mechanisms** (flow-edge-derived today,
§ 3 of that spec). `kit/build.mjs` builds
**three** IIFE dist bundles (global `QViz`): `dist/kit-proof.js` (graphs + the
charts SVG-only `QViz.charts.*` namespace for the `/lattice` rollups+trends
panel, charts-2026-07-02 § 7.1 →
`verifying/web/public/graphs2/kit.js`) + `dist/kit-strategy.js`
(graphs+charts+compose → `evaluating/web/public/graphs2/kit.js`) +
`dist/kit-graphs.js` (domain-neutral node-link → `monitoring/web/public/graphs2/
kit.js` + the designing hero). App mount dirs keep the historical `graphs2` name.
Re-sync = rebuild + cp into the app dirs + the app's `pnpm verify` / e2e.
Authoritative detail: `graphs/README.md`. See § 4. Also in-dir:
`00..02-*.prompt.md` — the proof-DAG leaf-tier design prompts (token palette,
geometry, animation, a11y, and the `Failure[]` wiring contract `verifying/web/`'s
`/proof-graph/02-debug/` consumes). The 2026-06-03..11 POC
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
adopted, `data/debates/charts-mixed3d-2026-07-02.md`). **W1 + C1 + C2 SHIPPED
2026-07-05:** W1 supersession sweep (both 2026-06-08 migration specs deleted,
citations re-targeted, `charts-2026-07-02/tests/` conformance suite);
**C1 kit widening** — qchart/1.1 additive model (`display`/`pane`/`role`,
`markers`, vertical `Threshold.orient`, `log` scale, NaN warm-up gaps, upsert
`append` seam, `chartsCaps()` probe) + the full LW-charts v5 backend
(multi-series, indicator panes price+3, volume-in-pane-0, markers, price/vertical
lines, streaming — `attributionLogo:false` for strict CSP, R-C1 gated) + the
`fromReport` `indicators[]` pane-routed reads + `hasChartExtras` FC2 dormancy
predicate; **C2 trend seam** — `qcatalog-trend/1` append-only JSONL (extractor
appends one rollup record per `--out` run, lock-protected canonical writes,
never `pending/`) + `fromCatalogTrend` (coverage/tier/corpus/agreement over
time). indicators are DATA never kit code (§ 4). **Projected bars SHIPPED
2026-07-06 (`charts-2026-07-02/SPEC.md` § 13, operator amendment):** qchart/1.2
additive `TimeseriesSeries.projected?` — ghost-rendered strictly-future bars
(renamed from operator's "options" — collides with defined-risk options),
producer-authored, `append` actuals supersede; `hasProjected()` = the FINANCIALLY
face-change probe (public mount ⇒ re-scan + signoff). `QViz.charts.*` namespace lives
in kit-proof (`entries/charts-svg.ts`, SVG-only) for the verifying `/lattice`
panel; kit-strategy keeps flat charts exports. **Cross-owner remainders on the
W-ledger:** C3 verifying `/lattice` mount · C4 accounting extras reshape +
evaluating FINANCIALLY re-scan · C5 analyzing adoption · C6 financial rollups
mount. The migration spec was deleted at the W1 sweep (its shipped ledger is the
new spec's § 9).

**Modality scaffolds (`catalog.json` consumers):**

- `tables/` — (scaffold) sortable/groupable grid of the lattice (a11y + export fallback).
- `mixed3d/` — the **interactive-3D** modality (Three.js, MIT; `@qagents/mixed3d`
  workspace member; `scenes/` = baked Blender-provenance media, firewalled):
  render-neutral `q3d/1` kit, kinds `pointcloud | surfacegrid | panelset`
  (charts-in-3D = opaque fully-resolved SVG payloads, composed via a compose
  `PanelSink` at M3, never parsed). **Re-chartered 2026-07-02 — authoritative
  contract is `data/specs/visualizing-2026-06-03/mixed3d-2026-07-02/SPEC.md`**
  (debated + adopted; PRIVACY gate PC1–PC6): phase order INVERTED — M1
  surfacegrid kit + M2 monitoring cost mount first (its re-home gate cleared
  2026-06-17; `hourlyBreakdown` stranded), embedding pointcloud lens LAST (R1
  kill criterion carried). **M1 SHIPPED 2026-07-05:** `q3d/1` model + validate
  (`var()`-payload reject, missing-`privacy` reject) + `fromGrid` (fail-closed
  privacy, sparse/fill/index) + `fromCatalogSurface` (aggregate height-field,
  VZ4-pinned) + one Three.js backend + `dist/kit-3d.js` (IIFE global `Q3D`);
  gated `pnpm -C visualizing/mixed3d gates` (39 unit + 10 headless-WebGL verify
  + strict CSP + `sandbox:frames` SSIM ≥ 0.98 over 8 committed frames).
  **Projected cells SHIPPED 2026-07-06 (spec § 9, operator amendment):**
  q3d/1.1 additive `surfacegrid.projected?: boolean[][]` mask + `qgrid/1` cell
  `projected?` flag — ghost `--q3d-projected` color (never a ramp step), hover
  `(projected)`, `tap-cell.projected`; absent ≡ all-actual, byte-compat. M2
  (monitoring cost mount) is monitoring-owned + chartered-not-scheduled; the
  `pointcloud`/`panelset` backends throw until M5/M3. Seeds `03-spatial-3d/`.
  The migration spec was deleted at the W1 sweep (2026-07-05).
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
in verifying/ (M2). Debate record:
`data/debates/uscode-graph-monitoring-pipeline-2026-06-16.md`.

**Method-DAG hero (designing `/thesis`; SPEC § 15 is the encoding
reference).** (The designing HOME hero switched to the membrane module
2026-07-06/07 and no longer mounts this DAG; the method DAG now lives on
`/thesis`. The dormant fixture in `designing/web/public/graphs2/` awaits
designing's content de-dup pass.) An authored interactive INDUCTIVE method DAG on three general
node-link capabilities, all byte-compat for wires that omit them: (1) **cluster-
as-node edges** (`nodelink.ts` `source_kind`/`target_kind:"cluster"` → the `cl:`
Component); (2) **expansion-state merge** (`core/merge.ts` `graph.merge`, LEAF +
INDUCTIVE modes; `applyMerge` folds each trigger's WHOLE subtree, `cl:`-keyed
rewire); (3) **inductive clusters** (`core/inductive.ts` `graph.inductive`; per-
role `PARTS`/`MIN` grammar scoped to host subtree; `realizeInductive` is
generator-SCOPED) + role→shape (circle/star/triangle/hexagon/◇) +
`MountKitOpts.showLabels`/`nodeScale`/`legend()`. Standing graph-def encoding
(operator-reviewed): Predicates is a single TERMINAL ◇ node per Input-fed LLM
(A/R/P, never C); firewall is **A-ONLY** (`Predicates→Axioms`); R/P connect via
the LLM compound (`R/LLM→Concepts+Propositions`, `P/LLM→Theorems`);
`proof→theorem` (P→T), axiom fed by nothing, merged `S→T` forbidden (`merge.ts`
clamps `Concepts→(Propositions descendant)`). cytoscape edge split (2026-07-05, debate W1/W2 +
use-order operator amendment): the AUTHORED `etype ∈ {flow,use,feedback,veto}`
(edge attrs-bag; `refutes`→veto default; omission = the role inference: USE =
BOTH endpoint roles `∈ {proposition,structure,theorem,proof}` — direction-
agnostic (`method.ts isUseEdge`; S→P/T→P are use) — thin/dashed/`--halo`;
everything else FLOW — thick/solid/`--edge`; `elements.ts`).
Both hero fixtures author the Kernel→Quantapix→LLM legs `feedback` (dashed OPEN
return path, `--edge-feedback` w/ graceful fallback; C pillar has none). fcose
constraints = `relativePlacementConstraint`, priority #1 forward FLOW
(top→bottom) + priority #2 REVERSED USE (used part above user; dropped on any
flow conflict); feedback/veto impose no order; DFS back-edge drop = unmarked
fallback only; `lintEdgeClasses` (order-independent, warn-only) owns the loop
check; **per-collapse-state (W7 shipped 2026-07-07)** — an expanded-compound
endpoint re-targets onto its childless members (`MEMBER_CAP` 8), so constraints
survive kernel-open + merged states (the overview-only bail is retired; deter-
ministic merged wiring via `MountKitOpts.seed` / sandbox `?seed=`). Regression
bed: `graphs/test/flow-constraints.test.ts` + the sandbox method constraint
gate + `sandbox/w7-check.mjs`.
**Single render:** one cytoscape-fcose source serves both the silent hero video
(headless capture per expand/merge state) and the `/thesis` interactive mount —
same `hero-graph.json` (designing-owned, with `loader.js`), one backend.
**7-chapter animation chartered + delivered** (2026-07-07): capture bundle +
adopted Claude Design deliverables at `scenes/thesis-hero/`; contract at
`data/specs/visualizing-2026-06-03/thesis-hero-2026-07-07/SPEC.md`. Open
work: next-steps items 9–12; the designing-owned Phase 3 (`/thesis`
thesis-steps mount) shipped 2026-07-07 — Phase 5 (public MP4) stays
deferred on W8.

**Constellation modality (M) + cluster-lens.** studying's SECOND operational
input — the qagents monorepo + `~/.claude` memory as one non-hierarchical graph
(`graph.kind="constellation"`; producer `studying/scripts/extract_constellation.py`,
golden `studying/Operating/emits/constellation/golden.json`). `fromConstellation`
+ `mountConstellation` implement **Option B**: M's scoped node/edge kinds ride the
open attrs bag (`attrs.kindClass`/`relKind`) folded onto distinct `qgraph/1`
carriers — **NO `NodeKind`/`EdgeKind` union widening** (Option C re-opens R2's
held-open veto). The **M1 cluster-lens** (`colorLens:'cluster'` + `--cluster-*`
ring) is M's headline; that ring **is in the rendering lattice-overlay SoT**
(`rendering/brand/tokens/quantapix/overlay/lattice-{dark,light}.css`, kit mirrors)
— the `--rel-*` edge palette is a HOST-overlay class (monitoring's operational
overlay), and constellation is **dark-only** (`tokens-constellation.css` DARK SoT,
no light twin). The M1 picture-floor knobs (`sizeBy`/`labelMinDegree`/`edgeRouting`/
`overviewDepth`) are opt-in `StyleSpec`/`MountKitOpts`; lattice/proof defaults are
untouched. monitoring owns `/constellation` + the mechanical kit-dist re-host-copy
(next-steps item 8). Spec:
`data/specs/lean4-charter-2026-06-10/constellation-graph-2026-06-17/SPEC.md` § 8.

## 4. Phased roadmap (spec § 12)

Phase 0 ✅ registration. Phase 1 ✅ catalog extractor for T18
(`extractor/usc_to_catalog.py` → `qcatalog/1`; financial deferred, § 3). **Phase 2 ✅ cytoscape
web-port** + **Phase 3 ✅ scale bake-off** — POC engines superseded + removed
2026-06-11 (§ 3, which carries the bake-off-preservation detail); the cytoscape
CSP patch lives on as the graphs `pnpm patch` (Phase 4).
**Phase 4 RE-SCOPED → built from scratch as the kit** (G0–G6 DONE + gated +
MOUNTED; single cytoscape-fcose backend, layered eliminated — the two-backend
charter was superseded 2026-07-02; details in § 3 + `graphs-2026-07-02/SPEC.md`).
cytoscape ships as npm deps + a `pnpm patch` (CSP fix), NOT vendored-source. Implementation/gate detail (test counts, per-app
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

`data/specs/visualizing-2026-06-03/charts-2026-07-02/SPEC.md` § 1 (carried locks L1–L4). Subproject-local
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
**hidden from the `/status` index** — the kit's mounted surfaces live inside
Qnarre/Qresev/monitoring, not on a quantapix.com surface, so the card stays
hidden until designing rules otherwise; the deep page `/status/visualizing/`
still builds. Reverse the hide by adding
`visualizing` to a `STATUS_GROUPS` member array in `designing/web/src/content/
copy.ts` plus the e2e sweep in `tests/e2e/status.spec.ts`.
