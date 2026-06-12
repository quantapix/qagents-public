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
  Qnarre `/app` verifier debug overlay.

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
+ adapters (`fromCatalog`/`fromProof`) + two backends (cytoscape/layered) +
`src/kit/mount.ts` (the G6 mount API: `mountProof`/`mountCatalog`, regions/
onLayout/onTapLeaf — the compose RegionSource surface) + `sandbox/` browser
gates. **Superseded `graphs/` engines 2026-06-11** (§ 13 parity gate re-passed:
49 unit, sandbox 18/18, strict-CSP, scale 1k/5k/10k all-seeds-salient).
`kit/build.mjs` builds the two IIFE dist bundles (global `QViz`):
`dist/kit-proof.js` (graphs only → `verifying/web/public/graphs2/kit.js`) +
`dist/kit-strategy.js` (graphs+charts+compose → `evaluating/web/public/graphs2/
kit.js`). Re-sync = rebuild + cp into the app dirs + the app's `pnpm verify` /
e2e. Authoritative detail: `graphs-2/README.md`. See § 4.

## 4. Phased roadmap (spec § 12)

Phase 0 ✅ registration. Phase 1 ✅ catalog extractor for T18
(`extractor/usc_to_catalog.py` → `qcatalog/1`; financial deferred until
axiomatize-trading builds `Universe/S<code>/<Axis>/`). **Phase 2 ✅ cytoscape
web-port** — the contract-native contender stood up in `graphs/cytoscape.js/
sandbox/` (a self-contained ESM island, not yet the Astro fold-in): both render
modes (lattice via `catalog-to-cy.mjs` + proof-DAG via `graph-to-cy.mjs`, § 5),
three lenses (§ 8), leaf-tier LOD (vendored `expand-collapse`), and the shared
provenance inspector (§ 6.3 R7). Four headless verifies (`npm run test:catalog`
+ `sandbox:verify{,:lenses,:proof}`) gate it; tf-graph stays in its harness (no
Astro port). **Phase 3 ✅ scale bake-off** (`graphs/bakeoff/`): `scale_catalog.py`
(deterministic T18→N synthetic catalogs + seeded diverge cells),
`cytoscape.js/sandbox/scale-screen.mjs` (1k/5k/10k: full-expand fcose 25/87/191 ms,
heap 38/83/323 MB, all seeds salient), and a **strict-CSP gate** (`verify-csp.mjs`,
`sandbox:verify:csp`) that cytoscape **passes** via one carried vendor patch
(UPSTREAM.md § Phase 4 — drops the unconditional `position:relative` `<style>`).
**Verdict (amended 2026-06-04, `graphs/bakeoff/VERDICT.md`):** cytoscape wins as
the **contract-faithful / public-mount** renderer (scale + strict-CSP pass);
tf-graph CSP-disqualified for the public mount but carried in git as the
layered-collapse companion (detail in the `graphs/tensorboard/` bullet, § 3).
**Phase 4 RE-SCOPED → built from scratch as `graphs-2/`**
(spec `data/specs/visualizing-2026-06-03/graphs2-2026-06-07/SPEC.md`, promoted
2026-06-10): a render-neutral TS kit (one
`qgraph/1` model + one `collapse.project()` algorithm + two backends behind one
`Backend` interface — cytoscape public/CSP-clean + clean-room layered companion;
both adapters + both collapse impls subsumed into the core). **G0–G6 DONE +
gated** (49 unit tests; `sandbox:verify` 18/18 render+gesture; strict-CSP pass;
scale 1k/5k/10k pass) — see `graphs-2/README.md`. cytoscape ships as npm deps +
a `pnpm patch` (CSP fix), NOT vendored-source. **G6 SHIPPED 2026-06-11** (Mode-A
parallel sessions, not `/open qagents`): `dist/kit-{proof,strategy}.js` mounted
at `verifying/web/public/graphs2/` (proof-DAG pages + new `/lattice`) +
`evaluating/web/public/graphs2/` (recomposed strategy mount via `@qagents/
compose`); both app e2e suites green; `graphs/` engines removed on the re-passed
parity gate. Phase 5: replay animation + `explaining/` deterministic SVG export
(layered backend's exportSVG is already byte-stable).

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
  redefine base tokens.

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
  forbidden. `designs/visualizing-lattice/` is net-new (no `visualizing-design`
  bundle exists); zero P4 migration cost.
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
