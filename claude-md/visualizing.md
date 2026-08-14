# CLAUDE.md — visualizing/

Project-specific rules for the qagents axiomatization-graphing surface. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`. Don't
re-litigate those.

**Registered subproject (2026-06-03).** Authoritative contract:
**`data/charters/visualizing/specs/visualizing-2026-06-03/SPEC.md`** —
scope-resident since 2026-07-20 under the `owner-living-program` residency
class (declared in the family header + `residency.txt`; every open phase
marker carries a `(frontier: …)` ref — an un-roadmapped marker de-matures the
family). Scope charter: **`data/charters/visualizing/graphing-surface/CHARTER.md`**.
Subproject memory: `project_visualizing_subproject`.

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
  loader**, never stored. Full shape in the spec § 3.1. **Vocabulary custody
  (G10 "studying proposes, visualizing versions"), spec § 3.1a:** the operational
  `axis` set is 48 tokens (44 + the 4 `Ctx*` context-ops tokens, 2026-07-27) —
  version of record `extractor/validate_catalog.py`
  `AXES`, lockstep twin `graphs/src/core/model.ts` `Axis`; qrounds/1
  `kind`/`attack_style` enums + the leaf-level `leanRef` join are pinned there
  too. `OPERATIONAL_AXES` (the render-palette roster) stays the 7 git axes until
  the 36-cell emit mounts (next-steps item 29).
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
  `usc_to_catalog.py` (legal, built); `accounting_to_catalog.py` (financial,
  built 2026-08-01 — walks `Universe/S<code>/<Axis>/` + `coverage.json`;
  the symbol→(sector,axis) coverage fold spec lives in its docstring).
  The § 11.0a certification seam is BUILT (2026-08-10): the scorer
  `code/lean_tools/score_bridge.py` (NOT `proving/scripts/` — C19 moved it)
  emits a **`qcert/1`** record via `--out` (pass or fail), and the extractor
  reads it via `--cert` — certified theorems override the naming heuristic, a
  FAILED certification renders `agreement:"diverge"` (never silence); no
  artifact → naming heuristic + `tier:"unknown"` cells, unchanged. The
  COMMITTED emit is the lanes' (ns:proving/148 / ns:accounting/96); until one
  lands the fallback stands.
  Stays top-level: `catalog.json` feeds **every** modality, not just `graphs/`.
- `rounds/` — the **qrounds/1 two-sided rounds contract** (custody ruled to
  visualizing, do-share P0-8 2026-07-18): `qrounds.schema.json` +
  `qrounds-standing.schema.json` + the `qblindness{,-corrected}.schema.json`
  pair (do-share run 7 R-3, 2026-08-04) + `validate_rounds.py` (stdlib,
  exit-coded 0/2/4/5) over each axis's `…/examples/*/rounds/`. Two invariants a
  session must not break: a `#corrected` blindness record supersedes its base
  without overwriting it and **the base is not reapable**; the JSON-Schema
  subset is CLOSED and self-enforcing (exit 2 on any keyword `_check` does not
  implement), so widening it is a three-part change — interpreter arm +
  `_UNDERSTOOD` entry + known-bad witness. Retention ruling, `_target_stems`
  diff-lock, exit codes, fixtures: `rounds/README.md`.
- `specs/` — the three POC extraction specs (provenance for the consolidated
  spec's appendix). `shared/INPUTS.md` — pointers to the axiomatized data.

**`graphs/` — the node-link modality = the uniform kit, mounted in the § 1 apps**
(`@qagents/graphs`, pnpm workspace member): render-neutral core (`qgraph/1`
model + `collapse.project()` + layout/style/axes + merge/inductive/method) +
five adapters + **ONE backend — cytoscape + fcose** — + `src/kit/mount.ts` (the
`mount*` API + regions/onLayout/onTapLeaf — the compose RegionSource surface) +
`sandbox/` browser gates; per-file roster: `graphs/README.md` § Layout.
Ordering is owned by **fcose constraint mechanisms** (flow-edge +
per-view rank-kind derived — `PROOF_RANK_KINDS`, T8 shipped 2026-07-11;
`graphs-2026-07-02/SPEC.md` § 3/§ 4). `kit/build.mjs` builds
**four** IIFE dist bundles (global `QViz`): `dist/kit-proof.js` (graphs + the
charts SVG-only `QViz.charts.*` namespace for the `/lattice` rollups+trends
panel, charts-2026-07-02 § 7.1 →
`verifying/web/public/graphs/kit.js`) + `dist/kit-strategy.js`
(graphs+charts+compose → `evaluating/web/public/graphs/kit.js`) +
`dist/kit-graphs.js` (domain-neutral node-link → `monitoring/web/public/graphs/
kit.js`) + `dist/kit-charts.js` (charts-only SVG surface, no DAG/LW/fromReport
— so no C8 framework-union leg; the supported mount class for charts-only
consumers, first `simulating/web/public/charts/kit.js`; depth-2026-08-12 § 5.2
made the R12 alternative a supported class). designing removed its dormant hero mount wholesale and is **no longer
a `kit-graphs.js` consumer** — the `/thesis` live mount returns with the hero
arc (next-steps items 9/15).
`fromFlow`/`mountFlow` (constellation flow graph, kit-graphs bundle ONLY;
Option-B fold, renderer computes nothing, the kit never reads
`graph.bottlenecks[]`) — spec `flow-adapter-2026-07-16/SPEC.md`.
Re-sync = rebuild + cp into the app dirs + the app's `pnpm verify` / e2e.
Authoritative detail: `graphs/README.md` (incl. the in-dir `00..02-*.prompt.md`
proof-DAG leaf-tier design prompts). See § 4.

**`charts/` — quantitative modality (BUILT; `@qagents/charts` workspace member;
authoritative contract `data/charters/visualizing/specs/visualizing-2026-06-03/charts-2026-07-02/SPEC.md`,
debated + adopted `debate record `charts-mixed3d-2026-07-02` (data/debates/, HELD lane)`):** the render-neutral
`qchart/1` closed-set series model + `validate()`; two adapters (`fromCatalog`
aggregate rollups · `fromReport` per-framework overlays + `predicate-selected` OHLCV
`sideView`) with the **defined-risk REFUSED enforced at the `fromReport` boundary**,
not just visually; five vanilla-SVG emitters (strict-CSP-clean + byte-stable export
for `explaining/`) + a lightweight-charts v5 backend behind one `ChartBackend`
interface. Phase-2 routing mount into Qresev shipped (§ 5.1). The
`qcatalog-trend/1` append-only trend seam + `fromCatalogTrend`, and `projected?`
ghost bars — whose `hasProjected()` probe is the FINANCIALLY face-change trigger
(public mount ⇒ re-scan + signoff) — are specified in that SPEC §§ 6 / 13.4.
`QViz.charts.*` lives in kit-proof
(`entries/charts-svg.ts`, SVG-only) for the verifying `/lattice` panel; kit-strategy
keeps flat charts exports. indicators are DATA never kit code (§ 4). **C8
framework-union** (invariant: § 4.1) ships in **kit-strategy only**, so its
host-copy debt is `evaluating/` alone. **Cross-owner W-ledger remainders live in
the charts SPEC's ledger** — trust the SPEC rows, not this line.

**Modality scaffolds (`catalog.json` consumers):**

- `tables/` — (scaffold) sortable/groupable grid of the lattice (a11y + export fallback).
- `mixed3d/` — the **interactive-3D** modality (Three.js, MIT; `@qagents/mixed3d`
  workspace member; `scenes/` = baked Blender-provenance media, firewalled):
  render-neutral `q3d/1` kit, kinds `pointcloud | surfacegrid | panelset |
  ribbonset`. **Authoritative contract (re-chartered 2026-07-02)
  `data/charters/visualizing/specs/visualizing-2026-06-03/mixed3d-2026-07-02/SPEC.md`**
  (PRIVACY gate PC1–PC6): phase order INVERTED — M1 surfacegrid kit + M2
  monitoring cost mount first, embedding pointcloud lens LAST (R1 kill criterion).
  M1 + projected-cells + M9 ribbonset are SHIPPED (enumeration + gates in the
  spec + next-steps item 16); M2 is monitoring-owned + chartered-not-scheduled;
  the `pointcloud`/`panelset` backends throw until M5/M3. Seeds `03-spatial-3d/`.
- `scenes/` — baked replay animation + frame export for `explaining/` (spec § 8;
  Phase 5). Frame capture rides the cytoscape kit (headless Playwright —
  `sandbox/serve.mjs` + `__CY__.png()`/`exportSVG`).

**M0 node-link reader (2026-06-17).** Adapter internals (`fromNodeLink`/`mountNodeLink`; monitoring mounts live, verifying uscode = M2) → `graphs/README.md` § "M0 node-link reader" (relocated apply-spread 2026-07-28).

**Method-DAG hero (designing `/thesis`).** An authored interactive INDUCTIVE DAG
exercising three general, byte-compat node-link capabilities: cluster-as-node
edges (`nodelink.ts`), expansion-state merge (`core/merge.ts`), inductive
clusters (`core/inductive.ts`) + role→shape + `MountKitOpts` knobs; authored
`etype ∈ {flow,use,feedback,veto}` (`method.ts`/`elements.ts`). Encoding +
standing graph-def grammar + the W7 constraint mechanism live in **parent SPEC
§ 15** (firewall A-ONLY, merged `S→T` forbidden; regression bed
`graphs/test/flow-constraints.test.ts`, `sandbox/w7-check.mjs`). **Single
render** — one cytoscape-fcose source (`hero-graph.json` + `loader.js`) serves
both the silent hero video and the `/thesis` mount once designing re-adds it;
7-chapter animation contract `…/visualizing-2026-06-03/thesis-hero-2026-07-07/
SPEC.md`, capture bundle `scenes/thesis-hero/`; open work = next-steps items
9/11/15, MP4 deferred on W8. **W6 method-projection producer SHIPPED 2026-08-06**
(design + both phases): `extractor/method_projection.py` + `validate_method.py`
emit + gate `data/visualizing/method-{legal,financial}.json` (instance fixtures
over the committed catalogs; hero NEVER regenerated; zero kit changes). Two
findings outlive the build — nested merge groups are OUTSIDE the mount's
variant-composition contract (the four-kernel § 15 swap is a HERO device;
kit-side hardening = ns:visualizing/50), and the financial directional gate is
TOKEN-based and refuses until a FINANCIALLY record exists. Detail (G1–G5, the 10
known-bad witnesses, the § 6 amendment):
`…/visualizing-2026-06-03/method-projection-2026-08-06/SPEC.md`.

**Constellation modality (M) + cluster-lens.** studying's SECOND operational
input — the qagents monorepo + `~/.claude` memory as one non-hierarchical graph
(`graph.kind="constellation"`; producer `studying/scripts/extract_constellation.py`,
golden `studying/Operating/emits/constellation/golden.json`). Option B: M's
scoped node/edge kinds ride the open attrs bag — **NO `NodeKind`/`EdgeKind`
union widening** (Option C re-opens R2's held-open veto). Adapter/mount
mechanics, the cluster-lens ring + SoT, and the M1 picture-floor knobs:
`graphs/README.md` § "Constellation (M) + the M1 picture floor". Constellation
is **dark-only** (`tokens-constellation.css` DARK SoT, no light twin);
monitoring owns `/constellation` + the mechanical kit-dist re-host-copy
(next-steps items 21 + 7). Spec:
`data/charters/studying/specs/lean4-charter-2026-06-10/constellation-graph-2026-06-17/SPEC.md` § 8.

## 4. Phased roadmap (spec § 12)

Phases 0–3 ✅; **Phase 4 RE-SCOPED → built from scratch as the kit** (G0–G6 DONE
+ gated + MOUNTED; single cytoscape-fcose backend, § 3 +
`graphs-2026-07-02/SPEC.md`). Implementation/gate detail lives in
`graphs/README.md` + `project_visualizing_subproject`.
**Phase 5** (next): replay animation + `explaining/` frame export on the
cytoscape capture path (settle-based determinism — seeded fcose + constraints;
raster acceptance = SSIM, never byte-equality).

## 4.1 Standing kit contracts (easy to break silently)

- **Caps-key discipline (MODALITY gate V-U2).** All three kits expose a closed,
  deep-equal-pinned caps record — `chartsCaps()` (9 keys — `componentSlots` is
  the first NUMERIC key + `watermark`, 2026-07-27; `distributionOrient`,
  2026-08-12), `m3dCaps()` (6 keys —
  `ribbonset:true` since the CH-2 mint 2026-07-29; `playback` `false`, flips at P1), `graphsCaps()`
  (`{navigator}`, `graphs/test/navigator.test.ts`). Every future capability filing
  MUST declare its additive caps key in the filing text — consumers key upgrade
  triggers on that key, never on version/feature-sniffing.
- **The component ΔE floor is a PROXY for R2, and it is loose at its own
  boundary** — `charts/test/palette.test.ts`'s ΔE2000 ≥ 18 check does NOT
  deliver the green/red/amber verdict exclusion it claims. What does is the
  **hue arc 175–330**, which lives in `rendering/brand/BRAND.md` § CH-2 and in
  **no test**; never tighten the lightness band. Case + the boundary witness:
  `feedback_proxy_floor_loose_at_its_boundary`.
- **"M1" names three different milestones — always qualify it.** `graphs` M1
  (constellation cluster-lens + picture-floor knobs, § 3 — shipped
  2026-06-14..17), `mixed3d` M1 (surfacegrid kit, § 3 — shipped 2026-07-05/06),
  and `code/web` M1 (web-unification, not visualizing-owned). A bare "M1
  prettiness floor" gated `ns:monitoring/3` + `ns:studying/3` for weeks — it read
  as mixed3d M1 while the graphs M1 it meant had shipped. Write "graphs M1" /
  "mixed3d M1", never bare.
- **Declared-token gate (the third gate class, 2026-07-20).** The parity gates
  compare the two DECLARED mirrors; they cannot see a token the CODE reads that
  neither declares (`--chart-pane-h` shipped that way — read at the LW backend,
  declared nowhere, `''` forever, every gate green). `{charts,mixed3d}/test/
  declared-tokens.test.ts` now assert every `'--…'` string literal in src is a
  declared token (DEFAULT_TOKENS[_3D] ∪ SERIES_TOKENS; family prefixes admitted
  iff members are declared). A px dimension is never an overlay token — the
  pane-h read was deleted, not declared.
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
  (`seriesToken()`). **No chrome, furniture, or annotation token is reachable from
  any role** — that absence IS the contract. **Never widen a role to reach a
  furniture token, and never add a colour by handing hosts a raw token name — add
  a role.** `seriesColor()` is role-first with a legacy-`styleRef` fallback; an
  *undeclared* series never defaults into the ramp. Palette (rendering-owned) +
  the `lintSeriesTokens()` palette-SET gate:
  the retired `charts-role-palette-2026-07-14` family, next-steps item 26.

## 5. Seam discipline — JSON only

The only seam between `visualizing/` and the app shells / domain projects is
JSON (`catalog.json`, `graph.json` v1). **No cross-subproject imports**
(share data, not code — root CLAUDE.md § Status hub seam rule). No Lean parsing in the renderer; the
kit consumes JSON, the extractor produces it. `loader.js` is the never-fold
side-car — a schema change is a two-sided edit (spec § 3.1 / R5;
`data/charters/proving/results-propagation/schema-of-record.md`).

## 5.1 Modality boundary + composition (locked 2026-06-08)

`data/charters/visualizing/specs/visualizing-2026-06-03/charts-2026-07-02/SPEC.md` § 1 (carried locks L1–L4). Subproject-local
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
  root/qagents concern. R1 (no domain logic, no kit internals) · R2 (placement
  reads the DAG's published node-region map, a kit *output*, and positions
  absolutely — never named DOM slots) · R3 (bars via an injected `resolveBars`,
  the run-emit's job — no parquet in the renderer); architecture + gates:
  `compose/README.md`. App shells **mount** the composed bundle via the
  kit-mount side-car; they never route between kits themselves
  (`evaluating/web/`: the graphs kit's `KitMount` backs `RegionSource`, Qresev's
  `GET /api/runs/<id>/bars` is the injected `resolveBars`, bundle =
  `kit-strategy.js`; overlay tiles light up as accounting's run-emit grows
  per-predicate `extras`).
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
  since the 2026-07-14 re-point). Every `{graphs,charts,mixed3d}/kit/tokens-*.css`
  is a **byte-identical mirror** of
  `rendering/brand/tokens/quantapix/overlay/{lattice,proof,chart}-{dark,light}.css`
  + `q3d-dark.css` — DO NOT edit in-kit; edit the SoT then re-copy. graphs +
  charts carry dark+light kit-side; **mixed3d is dark-only** (rendering mints the
  pair at M2, and the mirror-test loop gains the light tuple back then); theme
  selection is at the app's mount-dir copy
  (`graphs/` for every consumer). Tier ramp is frozen at
  `{a-full,a,b,modulo,unknown}` — **no `--tier-uncovered`**; an uncovered cell is
  `tier:unknown` + `coverage:false` (studying emit is SoT-aligned; adding the
  value is a non-goal).

- **The token chain has THREE hops and each drifts silently** — a missing token
  NEVER errors (`''` → dropped property, wrong local fallback, or
  `new THREE.Color('')`, **which is white**). Hop 1 (SoT → kit mirror) + hop 2
  (kit CSS ↔ charts `DEFAULT_TOKENS` / mixed3d `DEFAULT_TOKENS_3D`; graphs has no
  map, browser-only) are gated by `{graphs,charts,mixed3d}/test/tokens.test.ts`
  (byte-diff + key-set AND value equality; skips when `rendering/` is absent —
  the kits ship standalone via `publishing/`). `DEFAULT_TOKENS` ≡ the **DARK**
  slice (operator 2026-07-14: `explaining/` bakes dark, light is browser-only).
  Hop 3 (kit → app mount copy) is **UNGATED**, cross-subproject, each app's own
  `/close` (next-steps items 7 + 21) — charts/mixed3d `dom.ts` degrades to the
  sanctioned map, so a stale host copy is the right colour but still stale. Full
  failure model: `feedback_two_token_mirrors_ship_two_palettes`.

- **T10 deviations seat = `rendering/designs/visualizing-lattice/manifest.json`,
  key `deviations` — NOT `sanctioned_deviations`.** That bundle seats the WHOLE
  kit family (charts · mixed3d · graphs), so its `deviations[].file` paths point
  outside it. The wrong key greps clean and reads as "not declared" — it held
  ns:visualizing/5 gated for seven weeks past its trigger
  (`feedback_gate_must_name_the_right_subsystem` case 5). Declared:
  `DEFAULT_TOKENS`, `DEFAULT_TOKENS_3D`, `--font-mono`.
  `managing/scripts/brand-drift.sh` gates the first two; the third is uncovered
  and its sanction rests on a premise no gate watches — ns:managing/34.

## 7. rendering/ seam (rendering-spec debate, Round 01 — 2026-06-09)

Standing bounds VZ1–VZ5 + T10 → `data/charters/visualizing/graphing-surface/CHARTER.md` § rendering-seam (relocated apply-spread 2026-07-28); the one bullet a non-seam session can trip stays here: **overlay VALUE changes are ATOMIC ⇒ lift-UP to `qagents`** — SoT change + kit re-copy + headless map in ONE whole-repo commit, never separate `/close`s (mirrors rendering/CLAUDE.md § 4b; net-new overlays may land SoT-first).

## 8. Status slot

`scripts/status_emit.mjs` writes `data/status/visualizing.json` (kit
`KIT_VERSION` pinned in lockstep with `@qagents/diagram-kit`). The card is
**hidden from the `/status` index** — the kit's mounted surfaces live inside
Qnarre/Qresev/monitoring, not on a quantapix.com surface, so the card stays
hidden until designing rules otherwise; the deep page `/status/visualizing/`
still builds. Reverse the hide by adding
`visualizing` to a `STATUS_GROUPS` member array in `designing/web/src/content/
copy.ts` plus the e2e sweep in `tests/e2e/status.spec.ts`.
