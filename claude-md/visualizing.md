# CLAUDE.md — visualizing/

Project-specific rules for the qagents axiomatization-graphing surface. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`. Don't
re-litigate those.

**Registered as a real subproject 2026-06-03** (was a gitignored POC sandbox).
Roster + status slot (kit `v0.4.3`) + `/open`/`/close` support all wired; the
whole-dir delete recipe is retired — work here lands on `main` like any
subproject. Authoritative contract: **`data/specs/visualizing-2026-06-03.md`**
(relocated from `data/tmp/` on first citation). Subproject memory:
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
  `data/visualizing/<domain>-catalog.json` (`legal-`/`financial-`). Phase 1 →
  the `visualizing/` extractor is sole owner; Phase ≥3 → ownership transfers to
  the `dau`/`dat` driver-emit (discrete cutover, never a both-write window). See
  `data/visualizing/CLAUDE.md`.

## 3. Layout

Organized by output **modality** (reorg 2026-06-03): one dir per render shape —
`graphs/` · `tables/` · `charts/` · `mixed3d/` · `scenes/` — each reading the
**same** modality-neutral `catalog.json` from the **shared, top-level**
`extractor/`. Only `graphs/` is implemented today; the other four are scaffolds.
The spec's (§ 6.x) flat dir prose predates this reorg — this § 3 is authoritative.

**Shared (top-level, modality-neutral):**

- `extractor/` — **the highest-value deliverable** (Python, system `python3`).
  `usc_to_catalog.py` (legal, build now) + `accounting_to_catalog.py` (financial,
  driver-emit-preferred — the `Universe/S<code>/<Axis>/` tree doesn't exist yet).
  The parser **reads the `dau`/`dat` score-gate certification artifact** for
  `tier`/`agreement`; it does **not** run a green `lake build` (spec § 11.0a).
  Stays top-level: `catalog.json` feeds **every** modality, not just `graphs/`.
- `specs/` — the three POC extraction specs (provenance for the consolidated
  spec's appendix). `shared/INPUTS.md` — pointers to the axiomatized data.

**`graphs/` — node-link modality** (the only one built; see `graphs/README.md`):

- `graphs/cytoscape.js/` — MIT cytoscape + fCoSE family vendored; the
  contract-native bake-off contender → becomes the mounted kit if it wins.
  `adapter/` is ours. `node_modules/` + `dist/` gitignored (per-worktree hydrate).
- `graphs/tensorboard/` — Apache tf-graph; **carried in git as of 2026-06-04**
  (the Phase-3 `rm -rf` was retracted — `graphs/bakeoff/VERDICT.md` Amended banner).
  Kept as the **layered-collapse companion**: click a metanode (Title/Cluster/Cell,
  or Axioms/Predicates/Theorems) → summarize to one box, native. Renders both modes
  via a standalone browser host (`sandbox/{host.ts,lattice.html,proof.html,serve.mjs}`,
  port 8138, no VSCode) over the wired examples; lattice uses the new
  `src/adapter/catalog-to-graphdef.ts`. Op-colored / fixed-shape — **not** token/
  agreement-color faithful (cytoscape stays the contract renderer). Gitignore keeps
  only build state (`node_modules/` + `dist/`) + `sandbox/*.json` runtime data.
  Gates: `pnpm test` (+ `catalog-adapter.test.ts`) + `pnpm sandbox:verify`.
- `graphs/blender/` — **RETIRED (GPL).** All-MIT clean-room salvage only
  (`tools/`); GPL `core/` deleted. `extract-usc.mjs` is a working
  **proof-DAG/leaf** extractor precursor (port its Facts→axiom / cite→statute
  logic, relicense). See `graphs/blender/UPSTREAM.md`. Nothing Blender-provenanced
  reaches `main`.
- `graphs/experiments/{01-node-graph,02-hierarchy}/` — early notes; folded as
  lenses (coverage-heat ≈ § 8 overlay), not contenders.
- `graphs/00..02-*.prompt.md` — proof-DAG-mode (secondary) / **leaf-tier** render
  design prompts, migrated from `proving/graphs/` 2026-06-03. The 3-class/4-edge
  contract is locked in spec § 4; these carry the implementation detail the spec
  did not reproduce (token palette, geometry, animation, a11y, and the
  `Failure[]` wiring contract `verifying/web/`'s `/proof-graph/02-debug/`
  consumes). The old Claude-Design-bundle handoff + single-engine assumption are
  superseded by the § 6/§ 7 bake-off + kit-mount.

**Modality scaffolds (`catalog.json` consumers, not yet built):**

- `tables/` — sortable/groupable grid of the lattice (a11y + export fallback).
- `charts/` — aggregate rollups (tier distribution, coverage/agreement bars).
- `mixed3d/` — spatial/3D lens for cross-title clustering; seeds
  `03-spatial-3d/` (migrated from `experiments/`, spec § 13, deferred).
- `scenes/` — baked replay animation + deterministic SVG export for
  `explaining/` (spec § 8; Phase 5).

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
tf-graph CSP-disqualified for the *public mount* (POC `unsafe-inline`, structural
to Polymer 3) but **carried in git** as the layered-collapse companion — the
`rm -rf` is retracted. Both now render both modes with click-a-cluster collapse
(see the `graphs/tensorboard/` bullet above). The force-vs-dagre *headline strategy*
is NOT decided between engines — it relocates into cytoscape as a layout preset
(§ 8), settled at Phase 4. Phase 4: fold cytoscape into both app shells via the
single unified kit-mount; `rm -rf` the Blender files (tf-graph stays). Phase 5:
replay animation + `explaining/` deterministic SVG export.

## 5. Seam discipline — JSON only

The only seam between `visualizing/` and the app shells / domain projects is
JSON (`catalog.json`, `graph.json` v1). **No cross-subproject imports**
(`feedback_cross_project_data_sharing`). No Lean parsing in the renderer; the
kit consumes JSON, the extractor produces it. `loader.js` is the never-fold
side-car — a schema change is a two-sided edit (spec § 3.1 / R5;
`proving-results-propagation-2026-05-09.md` § 2.3).

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

## 7. Status slot

`scripts/status_emit.mjs` writes `data/status/visualizing.json` (kit
`KIT_VERSION` pinned in lockstep with `@qagents/diagram-kit`). The card is
**hidden from the `/status` index** until a real mounted surface exists (Phase 4)
— the deep page `/status/visualizing/` still builds. Reverse the hide by adding
`visualizing` to a `STATUS_GROUPS` member array in `designing/web/src/content/
copy.ts` plus the e2e sweep in `tests/e2e/status.spec.ts`.
