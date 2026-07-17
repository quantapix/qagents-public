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
kit (`@qagents/graphs`, § 3) serves Qnarre + Qresev + monitoring (+ the designing
`/thesis` mount).

Two render modes, one kit:

- **Lattice** (primary) — the catalog: coverage × agreement × tier over
  `catalog.json`. Headline is **agreement**, not a proof trace.
- **Proof-DAG** (secondary) — the existing single-complaint render (`graph.json`
  v1, the locked 3-class / 4-edge contract = the leaf tier). Must not regress the
  Qnarre `/app` verifier debug overlay. **Wire/kit invariants a session must not
  violate** (construction detail in propagation spec § 2.3 + `graphs/README.md`):
  additive `derived` node + `decomposes` edge; the kit folds `derived`→`predicate`
  and each composite becomes a collapsible **container ComponentKind** — **no
  NodeKind/EdgeKind widening, never crosses the wire seam**; a `derived-underivable`
  failure carries `derivedNode` + empty `axiomName`, attributed via `failByNode`
  (not `failByAxiom`); containers default collapsed; v1 graphs without H3 render
  byte-identically. The `dist/` bundles are gitignored canonical-only build state
  — rebuild at canonical BEFORE `/close`
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

**`graphs/` — the node-link modality = the uniform kit, mounted in the § 1 apps**
(`@qagents/graphs`, pnpm workspace member):
render-neutral core (`qgraph/1` model + `collapse.project()` + layout/style/axes
+ merge/inductive/method) + adapters (`fromCatalog`/`fromProof`/`fromNodeLink`/
`fromConstellation`) + **ONE backend — cytoscape + fcose** — + `src/kit/mount.ts`
(the mount API: `mountProof`/`mountCatalog`/`mountNodeLink`/`mountConstellation`,
regions/onLayout/onTapLeaf — the compose RegionSource surface) + `sandbox/`
browser gates. **The layered branch (tf-graph derivative) was ELIMINATED
2026-07-02** (`graphs-2026-07-02/SPEC.md` § 4; `feedback_retire_dont_tombstone`);
ordering is owned by **fcose constraint mechanisms** (flow-edge + per-view
rank-kind derived — `PROOF_RANK_KINDS`, T8 shipped 2026-07-11; § 3 of that spec). `kit/build.mjs` builds
**three** IIFE dist bundles (global `QViz`): `dist/kit-proof.js` (graphs + the
charts SVG-only `QViz.charts.*` namespace for the `/lattice` rollups+trends
panel, charts-2026-07-02 § 7.1 →
`verifying/web/public/graphs2/kit.js`) + `dist/kit-strategy.js`
(graphs+charts+compose → `evaluating/web/public/graphs2/kit.js`) +
`dist/kit-graphs.js` (domain-neutral node-link → `monitoring/web/public/graphs/
kit.js` + the designing hero). verifying/evaluating keep the historical
`graphs2` mount name; monitoring renamed to `graphs/` (2026-07-11).
Re-sync = rebuild + cp into the app dirs + the app's `pnpm verify` / e2e.
Authoritative detail: `graphs/README.md`. See § 4. Also in-dir:
`00..02-*.prompt.md` — the proof-DAG leaf-tier design prompts (token palette,
geometry, animation, a11y, and the `Failure[]` wiring contract `verifying/web/`'s
`/proof-graph/02-debug/` consumes). The 2026-06-03..11 POC
engines (cytoscape.js / tensorboard / bakeoff / blender) live only in git
history; survivor: `graphs/sandbox/scale_catalog.py`.

**`charts/` — quantitative modality (BUILT; `@qagents/charts` workspace member;
authoritative contract `data/specs/visualizing-2026-06-03/charts-2026-07-02/SPEC.md`,
debated + adopted `data/debates/charts-mixed3d-2026-07-02.md`):** the render-neutral
`qchart/1` closed-set series model + `validate()`; two adapters (`fromCatalog`
aggregate rollups · `fromReport` per-framework overlays + `predicate-selected` OHLCV
`sideView`) with the **defined-risk REFUSED enforced at the `fromReport` boundary**,
not just visually; five vanilla-SVG emitters (strict-CSP-clean + byte-stable export
for `explaining/`) + a lightweight-charts v5 backend behind one `ChartBackend`
interface. Phase-2 routing mount into Qresev shipped (§ 5.1). **`qcatalog-trend/1`**
= append-only JSONL trend seam (extractor appends one rollup per `--out` run,
lock-protected canonical, never `pending/`) + `fromCatalogTrend`. **`projected?`** =
ghost-rendered strictly-future bars (`TimeseriesSeries.projected?`, producer-authored,
`append` actuals supersede); `hasProjected()` = the FINANCIALLY face-change probe
(public mount ⇒ re-scan + signoff). `QViz.charts.*` lives in kit-proof
(`entries/charts-svg.ts`, SVG-only) for the verifying `/lattice` panel; kit-strategy
keeps flat charts exports. indicators are DATA never kit code (§ 4). **C8
framework-union** (§ 4.1 carries the standing invariant): `Framework` is a closed
mapped union over the OPEN `WireFramework`, `fromReport` degrades an unmapped id
(`degraded:true`, never a TypeError); ships in **kit-strategy only**, so C8's
host-copy debt is `evaluating/` alone. **Cross-owner W-ledger remainders:** C3
verifying `/lattice` mount · C4 accounting extras reshape + evaluating FINANCIALLY
re-scan · C5 analyzing adoption · C6 financial rollups mount.

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
- `scenes/` — baked replay animation + frame export for `explaining/` (spec § 8;
  Phase 5). Frame capture rides the cytoscape kit (headless Playwright —
  `sandbox/serve.mjs` + `__CY__.png()`/`exportSVG`).

**M0 node-link reader (2026-06-17).** `fromNodeLink(wire, view)` reads the
`qgraph-wire/1` networkx envelope (shared `code/lean_graph` + `uscode_graph`
serializer): mandatory `KIND_MAP`/`REL_MAP` normalizers (`validate()` does NOT
enforce kind enums), a `cl:`-prefixed cluster→Component forest derived from
`cluster`/`cluster_kind` (node-id ↔ cluster-path collide by design), and
dangling-`anchors` tolerance (the cross-axis anchor points out of the K-graph).
`axesFor('operational')` → `OPERATIONAL_AXES` (the 7 git axes).
NO `model.ts` widening (type-decls fold onto `axiom`; `Section`→existing kind).
Drives the monitoring/ operational mounts (live) + later the uscode mount
in verifying/ (M2). Debate record:
`data/debates/uscode-graph-monitoring-pipeline-2026-06-16.md`.

**Method-DAG hero (designing `/thesis`).** Moved off HOME to `/thesis` 2026-07-07
(HOME switched to the membrane module; the dormant `designing/web/public/graphs2/`
fixture awaits designing's content de-dup). An authored interactive INDUCTIVE DAG
exercising three general, byte-compat node-link capabilities: cluster-as-node edges
(`nodelink.ts`), expansion-state merge (`core/merge.ts`), inductive clusters
(`core/inductive.ts`) + role→shape + `MountKitOpts` knobs. Encoding + standing
graph-def grammar live in **parent SPEC § 15** (operator-reviewed; firewall
A-ONLY, merged `S→T` forbidden). Authored `etype ∈ {flow,use,feedback,veto}` with
role-inferred USE default (`method.ts`/`elements.ts`). fcose ordering constraints
survive collapse states (**W7, 2026-07-07** — expanded-compound endpoints re-target
onto childless members, `MEMBER_CAP` 8; deterministic merged wiring via
`MountKitOpts.seed`; regression bed `graphs/test/flow-constraints.test.ts` +
`sandbox/w7-check.mjs`). **Single render** — one cytoscape-fcose source serves the
silent hero video and the `/thesis` mount, same designing-owned `hero-graph.json`
(with `loader.js`). 7-chapter animation contract
`data/specs/visualizing-2026-06-03/thesis-hero-2026-07-07/SPEC.md`, capture bundle
`scenes/thesis-hero/`; open work = next-steps items 9–12, public MP4 deferred on W8.

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
`data/charters/studying/specs/lean4-charter-2026-06-10/constellation-graph-2026-06-17/SPEC.md` § 8.

## 4. Phased roadmap (spec § 12)

Phases 0–3 ✅ (registration · catalog extractor `qcatalog/1` · cytoscape
web-port · scale bake-off) — POC engines superseded + removed 2026-06-11 (§ 3
carries the bake-off-preservation detail); the cytoscape CSP patch lives on as
the graphs `pnpm patch` (Phase 4).
**Phase 4 RE-SCOPED → built from scratch as the kit** (G0–G6 DONE + gated +
MOUNTED; single cytoscape-fcose backend, see § 3 + `graphs-2026-07-02/SPEC.md`).
cytoscape ships as npm deps + a `pnpm patch` (CSP fix), NOT vendored-source. Implementation/gate detail (test counts, per-app
mount provenance) lives in `graphs/README.md` +
`project_visualizing_subproject`. **Phase 5** (next): replay animation +
`explaining/` frame export on the cytoscape capture path (settle-based
determinism — seeded fcose + constraints; raster acceptance = SSIM, never
byte-equality).

## 4.1 Standing kit contracts (easy to break silently)

- **The proof conformance anchor is SYNTHETIC and stays that way.**
  `graphs/test/fixtures/graph-v1-doe_acme.json` = proving's real `sample` (Doe v.
  Acme) emit + an authored § 1961(1) refusal (`sandbox/gen-doe-acme-fixture.py`); it
  replaced an earlier real-matter fixture 2026-07-13. This tree is a
  publish candidate — **no real docket matter (evidence quotes, party names) may
  land in it.** The synthetic proving examples all carry `failures: 0`, which is why the
  refusals are injected; if proving ever
  emits a genuinely refusing synthetic, adopt its `graph.json` and delete the
  injection.
- **Cluster-naming contract (W3) — a producer obligation that FAILS SILENTLY.** A
  method wire's LLM compound MUST end in `.LLM` and its kernel compound in `.Kernel`
  (suffix-matched; `LLM_SUFFIX`/`KERNEL_SUFFIX`/`isLlmCluster` in `core/method.ts`).
  `isMethodView` reads a `predicate` leaf inside a `.LLM` cluster as the method-DAG
  signature, and `flowConstraints` excludes `.LLM`-side cluster edges from the spine.
  Rename either and the graph still renders — it just loses the method signature and
  the spine. **C-pillar exception:** Conclusions has NO Input, NO Predicates, NO
  Quantapix, NO feedback; nothing may require them per-pillar (SPEC § 15).
- **`graph.merge` is PLURAL** (W3): a bare `MergeSpec` or a `MergeSpec[]`; groups
  toggle independently and must be **disjoint** (`mergeSpecs()` throws — the first
  fold would remove the component the second still expects). Singular is the N=1 case,
  byte-identical.
- **Charts `Framework` is a closed MAPPED union over an OPEN wire** (C8): accounting
  lands kernels before consumers map them, so `fromReport` degrades an unmapped
  framework (`degraded:true`, empty chart) rather than throwing. `hedging` shares the
  `optionsChart` builder with `options-risk` — it extends the defined-risk refusal
  boundary and must never get a softer one.
- **qchart/1.3 — ROLE drives colour; `styleRef` is legacy** (debate
  `charts-series-dial-2026-07-14` R2). A series declares a **role** (`price` |
  `indicator` | `volume` | `band`, + `slot 1..6`) and the KIT owns the token
  (`seriesToken()`). **No chrome, furniture, or annotation token is reachable from any
  role** — that absence IS the contract: it is what makes painting a data series with
  `--chart-overlay-grid` (decorative, 1.21:1) or `--chart-overlay-marker` (breach red)
  *unrepresentable* rather than merely discouraged. It had to be, because the open
  `styleRef` set let every host do exactly that — analyzing painted 8 series from 5
  slots, and the kit's own `report.ts`/`trend.ts` do it too. **Never widen a role to
  reach a furniture token, and never add a colour by handing hosts a new raw token
  name — add a role.** `seriesColor()` is role-first with a legacy-`styleRef`
  fallback, so the role palette (rendering-owned, `data/tmp/charts-role-palette-2026-07-14.md`)
  **self-activates on mint**; an *undeclared* series must never default into the ramp
  (that would silently re-colour every legacy chart on mint day — pinned by a test).
  `lintSeriesTokens()` is the migration lever; `charts/test/palette.test.ts` gates the
  palette as a SET (AA · ΔE≥18 from the ghost · pairwise), not token-by-token.

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
  kit-mount side-car — they never route between kits themselves. The
  `evaluating/web/` mount: the graphs kit's `KitMount` backs `RegionSource` in the
  app loader, the Qresev server's `GET /api/runs/<id>/bars` is the injected
  `resolveBars`, and the mount is the composed `kit-strategy.js` bundle. Overlay
  tiles light up as the accounting run-emit grows per-predicate `extras` (drift
  discipline pairs that emit reshape with the consumer sweep).
- **The "strategy-chart kit" is two modalities fused** and gets decomposed: the
  strategy DAG stays in `graphs/`; the overlays + side-view move to `charts/`;
  the Qresev mount is recomposed via the router (Phase 2), not a fused kit.

## 6. Conventions

- Terse `x/y/xs/ys` dialect, minimal comments (house style).
- License hygiene is load-bearing: the MIT cytoscape chain is the only
  third-party surface; **nothing with Blender provenance reaches `main`**
  (`feedback_no_third_party_license_entanglement`).
- Python: root venv by absolute path is NOT needed — the extractor uses system
  `python3` (the `proving/`/`accounting/` convention; reads JSON/artifacts, not
  numerics).
- Tokens: the kit reads tokens, never literals — add a `tokens-lattice.css`
  overlay per app (axis palette / tier ramp / agreement green-amber-red); never
  redefine base tokens. **Overlay SoT = `rendering/` for ALL THREE kits**
  (graphs since 2026-06-16, brand-polishing § 3b variant A; charts + mixed3d
  since the 2026-07-14 re-point, next-steps item 23). Every
  `{graphs,charts,mixed3d}/kit/tokens-*.css` is a **byte-identical mirror** of
  `rendering/brand/tokens/quantapix/overlay/{lattice,proof,chart,q3d}-{dark,light}.css`
  — DO NOT edit in-kit; edit the SoT then re-copy. All three now carry dark+light
  (graphs is no longer the sole dual consumer); theme selection is at the app's
  mount-dir copy (`graphs2/`; monitoring `graphs/`). Tier ramp is frozen at
  `{a-full,a,b,modulo,unknown}` — **no `--tier-uncovered`**; an uncovered cell is
  `tier:unknown` + `coverage:false` (studying emit is SoT-aligned; adding the
  value is a non-goal).

- **The token chain has THREE hops and each one drifts silently — two are now
  gated, one is not.** A missing token NEVER errors: it resolves to `''` and
  either drops the property, takes a wrong local fallback, or (mixed3d)
  reaches `new THREE.Color('')`, **which is white**. Both known drifts shipped
  for days under fully green gates.
  1. **SoT → kit mirror** — gated by `{graphs,charts,mixed3d}/test/tokens.test.ts`
     (byte-diff; skips when `rendering/` is absent, since the kits ship standalone
     via `publishing/`). *This hop had gone stale:* rendering shipped
     `--edge-feedback`/`--edge-veto` on 2026-07-07 and the graphs mirror never got
     them, so the W9 edge distinction had never once rendered.
  2. **kit CSS ↔ `DEFAULT_TOKENS`** (charts) / `DEFAULT_TOKENS_3D` (mixed3d) — the
     browser reads the overlay, the headless exporter reads the map, and they must
     agree. Gated by the same `tokens.test.ts` (key-set AND value equality).
     `DEFAULT_TOKENS` ≡ the **DARK** slice (operator ruling 2026-07-14: the
     `explaining/` frame export bakes dark; the light slice is browser-only).
     *This hop had gone stale:* `--chart-overlay-projected` / `--q3d-projected`
     landed in the maps 2026-07-06 and never in the overlays. graphs has no map
     (browser-only) — nothing to drift.
  3. **kit → app mount copy** — **UNGATED**, cross-subproject, each app's own
     `/close` (next-steps items 7 + 21). `dom.ts` in charts + mixed3d now falls
     back to the sanctioned map when the host copy lacks a token, so a stale host
     copy degrades to the right color instead of white — but it is still stale.

## 7. rendering/ seam (rendering-spec debate, Round 01 — 2026-06-09)

Joined VZ1–VZ5 (record `data/debates/rendering-spec-2026-06-09.md`; CLEARED
digest `data/debates/adopted/rendering-spec-2026-06-09.md`). Standing bounds:

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
  byte-stable golden (gated: charts `sandbox:export`); graph frame capture is
  raster/SSIM via the cytoscape path; raster → SSIM/pixel-diff, never
  byte-equality.
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
