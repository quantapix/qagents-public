# CLAUDE.md — blending/

Project-specific rules for the qagents Blender production-assistance
subproject. Assumes Claude Code's default guidance and the repo-root
`qagents/CLAUDE.md`. Don't re-litigate those.

Status emit: real producer at `blending/scripts/status_emit.py`
(stdlib Python, runs from system `python3`, NOT Blender's bundled
interpreter — it only reads the filesystem). Emits motif-registry
readiness + the explaining/ consumer roster + render-cache counts per
the root § "Status hub" contract.

## 1. Scope

`blending/` is a **comprehensive, license-clean Blender Python wrapper**
(`blendr`) plus motif consumers and authoring docs. The wrapper
provides programmatic access to Blender's full bpy surface via
subprocess invocation; Geometry Nodes is the load-bearing layer.
Same shape as `resolving/`: typed Python wrapper component plus
skills + diagrams + step-by-step authoring docs.

The Escher motif library (`blending/motifs/`) is **one consumer** of
the wrapper, not its reason for existing.

Geometry Nodes generates 3D geometry that Cycles or EEVEE renders
to PNG/MP4 frames flowing into `resolving/`'s Fusion comp as B-roll
plates (not interchangeable with Fusion — different layer of the
pipeline).

Scope boundaries:

- **In scope.** Programmatic Blender control via the `blendr` wrapper:
  scene/object/mesh/curve construction, modifiers, materials + shader
  graphs, Geometry Nodes graph authoring + execution, compositor
  graphs, Cycles/EEVEE/Workbench render presets, animation
  (keyframes/drivers), import/export adapters (glTF, OBJ, FBX, USD,
  Alembic), asset libraries, headless `--background --python`
  invocation, JSON-driven scene specs, output files written under
  `blending/renders/`.
- **Out of scope.** Character animation, simulation (cloth/fluid/rigid
  body), full feature-film rigs, real-time game-engine workflows,
  Blender add-on packaging (`.zip` for `Edit > Preferences >
  Add-ons`), GUI add-ons. Consumers (today `explaining/`; later
  `verifying/`, `evaluating/`) come in through the § 7 seam only.

## 2. Layout

```
blending/
├── CLAUDE.md            # this file
├── PLAN.md              # project master (vision + milestone ledger)
├── blendr/              # typed Python wrapper component
│   ├── PLAN.md          # wrapper sub-plan
│   ├── pyproject.toml   # standalone (NOT in root pyproject — see § 3)
│   ├── README.md
│   ├── src/blendr/      # connect / app / scene / object / mesh / curve /
│   │                    # modifier / material / shader / gn / compositor /
│   │                    # render / animation / io / asset / text / image /
│   │                    # recipes / errors / _cli / _stubs/bpy.pyi
│   ├── tools/           # gen_stubs.py + gen_nodes.py
│   ├── examples/        # runnable spec files
│   └── tests/           # unit / integration / acceptance
├── motifs/              # Escher motif library — consumer of blendr
├── scenes/              # Wave-3 full-shot builders (§ 6.5) + fixtures/
├── skills/              # production skills (SKILL.md each)
├── diagrams/            # GN node-tree force graphs
├── scripts/             # render_gn_diagrams.py + render_plate.py (one-command
│                        #   render/mux/MANIFEST delivery — W19) + status_emit.py
└── renders/             # gitignored output sink
```

## 3. Python: Blender's bundled Python, not the qagents venv

Blender 5.1.2 ships its own Python 3.13 with the `bpy` module
hard-bound to that interpreter. `bpy` is **not** importable from the
qagents root venv (`./.venv`); the C-extension is built against
Blender's exact Python ABI. So:

- Wrapper code lives in `blending/blendr/src/blendr/` and is executed
  by Blender's interpreter via
  `/Applications/Blender.app/Contents/MacOS/Blender --background
  --python <entry>` invocation. It is NOT installed into `./.venv`
  for runtime.
- The wrapper's `pyproject.toml` declares dependencies for static
  type-checking (pyright runs against generated `bpy` stubs in
  `src/blendr/_stubs/`), not runtime — runtime deps are zero.
- Consumer subprojects (`explaining/`) invoke through subprocess
  (the `--python-expr` + `runpy.run_module` form — § 7; Blender's
  `--python` flag takes a file path, not `-m module`):

      blender --background \
              --python-expr "<sys.path bootstrap + \
                  runpy.run_module('motifs._cli', ...)>" \
              -- --spec <spec.json> --out <out-dir>

  Communication is JSON-in / files-out. Same boundary the
  `resolving/davinci/` wrapper uses against Resolve.
- Headless tests at `blending/blendr/tests/integration/` also invoke
  Blender as a subprocess and assert against the rendered output (PNG
  hash, frame count, EXIF). They run from the qagents venv but call
  out to the Blender binary. Gated by `BLENDR_ITESTS=1`.

Type-check + test tooling sits in root `pyproject.toml`'s
`[blending-dev]` extra (zero runtime deps); `BLENDR_BLENDER_PATH`
env overrides the Blender binary path. See
`project_blending_subproject` memory for the install/regen recipe.

## 4. License hygiene (load-bearing)

The wrapper has **zero third-party code in its dependency tree** —
runtime or vendored. Every line of code in `blendr/` is our own,
designed from first principles against Blender's public API.

- **Runtime deps:** Python 3.13 stdlib + the subprocess-invoked
  Blender binary. Nothing else.
- **Stubs:** generated by us via `tools/gen_stubs.py` (introspects
  `bpy.types` inside Blender's bundled Python). The output artifact
  (`src/blendr/_stubs/bpy.pyi`) is our work product.
- **Geometry Nodes DSL:** designed from first principles against
  Blender's public Python API (see
  `feedback_no_third_party_license_entanglement`). We **do not read**
  the source code of any GN-DSL project (geonodes, geometry-script,
  NodeToPython, bpystubgen, blender-stubs, fake-bpy-module, etc.)
  while authoring our own.
- **Dev-only tools:** pyright, pytest, ruff are acceptable — they
  operate **on** our code without being linked into it. They live in
  `[blending-dev]` extras; never shipped, never imported at runtime.
- **Subprocess boundary against GPL host:** Blender (GPL-3.0) is
  invoked as a subprocess across a JSON / files boundary. Subprocess +
  structured-data invocation is **not** derivative work under any
  reasonable reading; same boundary `resolving/davinci/` uses against
  DaVinci Resolve.

## 5. Geometry Nodes architecture (the load-bearing layer)

The wrapper authors GN graphs declaratively. `blendr.gn.tree`
provides typed dataclasses (`Node`/`Link`/`GeoTree`/`SocketRef`);
`blendr.gn.types` provides socket-as-class types
(`Geometry`/`Mesh`/`Curve`/`Vector`/`Float`/...); `blendr.gn.nodes`
is the hand-written runtime API (`NodeSignature`/`make_node`/
`validate_socket_types`) backed by the generated `blendr.gn._catalog`
data file (overwritten by `tools/gen_nodes.py` against the local
Blender introspection); `blendr.gn.nodes_types` holds the
`NodeSignature` dataclass in its own module to break the
`nodes ↔ _catalog` import cycle; `blendr.gn.translator` performs the
`GeoTree → bpy.types.NodeTree` mutation at execution time. The same
`GeoTree` is also the input to `blendr.shader.apply_to_material` and
`blendr.compositor.apply_to_scene_compositor` — one DSL across three
node-tree systems.

Why declarative: GN graphs are the production-defining surface (as
Fusion node-trees are in `resolving/`); typed-Python specs are
git-diffable (vs the opaque `.blend`), drive the `blending/diagrams/`
force graphs, compose from primitives without Blender-UI re-authoring,
and validate cycles + socket types client-side (`GraphCycleDetected` /
`SocketTypeMismatch`) **before** the translator runs — Blender crashes
are not an allowed failure mode. Spec pointer: § 9.

Naming convention: GN node names use ASCII identifiers
(`escher_tess_p4m`, `penrose_stairs_loop4`), not Blender's default
"Geometry Nodes.001" auto-numbering. Motif identifiers are the public
surface.

## 6. Escher motif library — what's allowed

Lives at `blending/motifs/` (NOT inside `blendr/` — motifs are
consumers of the wrapper). Escher's catalog is in copyright until
~2042 (NL post-mortem 70y per `reference_escher_relativity_rights.md`).
Same rule as the rest of qagents: **derivative-not-copy.** What this
lane produces:

- **Tessellations** — recursive tilings of a fundamental domain
  (parallelogram / hexagon / tri-quad), with our own procedural shape
  primitives. No named Escher figures (no lizards, no birds, no fish
  in their characteristic Escher silhouette).
- **Penrose stairs** — 4-corner-loop staircase, derived geometry.
  No center-figure rendering of Escher's *Relativity*.
- **Hyperbolic disk pattern** — Poincaré disk with our own ornament,
  not Escher's *Circle Limit* primitives.
- **Recursive ornament** — self-similar pattern at 2-3 scales,
  geometry-nodes driven, NOT vectorized from any Escher print.

Anti-cues to bake into every prompt that uses these motifs: "no named
human figures", "no recognizable Escher figure silhouettes", "no
direct copy of any *Relativity* / *Ascending and Descending* / *Drawing
Hands* / *Circle Limit III* / *Belvedere* composition center", "mark
swappable: yes".

## 6.5. Scenes lane — Wave 3 (immersive animation)

`blending/scenes/` (sibling of `motifs/`, builders `scenes.<name>`
registered via its own `scenes/_cli.py` bridge) owns **full shots** —
geometry/GN + materials + lighting + camera path + keyframed animation
+ optional compositor look pass — vs motifs' background-plate
geometry. Locked in `data/specs/blending-scenes-2026-07-04/`:
custom-generated scripts
are the *authoring* path only, production always goes through a
registered builder + JSON spec (a per-episode variation is a param or
a `data` file, never a forked `.py`); blendr renders image sequences
only, video containers are muxed by `scripts/render_plate.py --mux`
(ffmpeg subprocess — D4 intact); data-driven scenes take a consumer-
emitted JSON via the spec's `data` key (pinned schemas per subject;
blending never computes domain values); `loop: true` renders must be
seamless (first/last-frame delta gate); deliverable kinds are
`still | loop | clip` (MANIFEST column); scene renders stay
**verdict-free** (no `⊢`/verdict/rider tokens baked into Blender
output — those live on downstream card layers). Consumption contract:
`resolving/skills/compose-blender-scene/SKILL.md` — the
`blender-compose-2026-07-04` subspec dir was reaped whole (do-retire S9).

## 7. Output → explaining/ pipeline

Renders land in `blending/renders/<motif>/<spec_hash>/render.png`
(still) or `frame_NNNN.png` (animation), gitignored, with
`result.json` alongside. `renders/` is declared canonical-shared in
`blending/.worktree-links` (root § session-lifecycle, charter § 2.4).
They ride to S3 via the
`data/renders/<sub>-design/` manifest pattern only when an
`explaining/` per-video bundle calls them B-roll plates. The seam is
two things:

1. JSON spec authored by an `explaining/` per-video `design.md` →
2. PNG/MP4 sequence consumed by `resolving/`'s Fusion comp at compose
   time (skill `compose-*` pulls from
   `blending/renders/<motif>/...`).

Motif builders are wired into `blendr._cli`'s registry by the
consumer-side bridge at `blending/motifs/_cli.py` — the wrapper stays
Escher-blind (D7); adding a motif is one helper there, not a wrapper
change. Invocation form: § 3 (also documented in
`data/renders/blending-design/MANIFEST.md` § Trigger Surface +
`skills/escher-tessellation/SKILL.md` § Wrapper calls).

`blending/` does not deliver final video; it delivers plates.
Compositing, color, and audio stay with `resolving/`.

First-consumer mapping table lives in
`data/renders/blending-design/MANIFEST.md`.

## 8. Skill placement

- Cross-project skills auto-load via the `blending/.claude/skills`
  symlink — root § "Skill placement rules"; nothing blending-specific.
- `blending/`-only skills live at `blending/skills/` and are NOT
  auto-loaded; they're invoked by name from `explaining/`'s per-video
  flow or `resolving/`'s compose-* chain.

Skill catalog (motif plates + Wave-3 scene skills) is owned by
`blending/skills/README.md` — 11 skills as of 2026-07-13; don't
restate the roster here. All three motif bridges carry cohort-tone
params (`film_transparent` + `*_color` RGBA), added 2026-07-10 for
the Meridian re-skins. Skill-authoring manual-crosscheck rule (locked
2026-05-24): `blending/skills/README.md` § Manual crosscheck.

**Cohort-tone params + tinting (all bridges).** The `film_transparent`
+ `*_color` (RGBA) params sit **outside** the `RenderSpec` — hash-stable,
so a re-tint does not change the render hash. Re-tint param sets are
committed as refspecs at `motifs/fixtures/`. The bpy mechanism (shared
`_tint_realized_geometry` splice in `motifs/_cli.py`, `.name` node
matching, linear-RGB base_color) is pinned in memory
`project_blending_subproject` — read it before touching a bridge tint.

## 9. Pointers

- Spec family `data/specs/blendr-2026-05-10/`: SPEC.md body reaped
  (do-retire S9 2026-08-08; git or `retire.sh --restore`). Live
  contract = its `tests/` + §§ 3–6.5 here.
- Anti-Escher copyright check: `reference_escher_relativity_rights.md`
  (user memory).
- Pattern reference: `resolving/CLAUDE.md` (same shape, different host
  application).
