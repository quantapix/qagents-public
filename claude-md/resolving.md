# CLAUDE.md — resolving/

Project-specific rules for the qagents DaVinci Resolve production
subproject. Assumes Claude Code's default guidance and the repo-root
`qagents/CLAUDE.md`. Don't re-litigate those.

## 1. Scope

`resolving/` is the production-assistance subproject for assembling
video content in DaVinci Resolve Studio. It is **not** just a Python
wrapper — the wrapper is one component among several. The full scope:

- **Skills** that drive scripted production: A-roll authoring, B-roll
  selection/curation, Fusion node-tree authoring, color/grade
  application, audio loudness pass, render-farm operation,
  subtitle/loudness QA. Each skill is invokable from a consumer
  subproject (§ 3). Catalog at `skills/` — the roster,
  per-skill force-graph diagram ledger, and chain pseudocode live in
  `skills/README.md` (single owner — don't restate them here). The
  branded outro is NOT a Fusion skill — it bakes a flat Pillow plate
  in `explaining/`'s `phase3_outro.py` (see
  `reference_resolve_fusion_compositing_gotchas`). Lift spec:
  `data/specs/resolving-2026-05-26/skills-lift-2026-05-15/SPEC.md`.
- **Step-by-step instructions** for in-Resolve operations that are
  hard to script through the API (Fusion-tree authoring patterns,
  cache management, project-version migration, render-queue triage).
- **Typed Python wrapper** at `resolving/davinci/` — consumed by the
  skills above + by the per-phase `phase*_*.py` drivers in
  `explaining/`. Locked decisions (15 items): consolidated spec § 4; the
  `davinci.fusion` surface (typed Comp/Tool, primitives, keyframes,
  `.setting` I/O + golden normaliser):
  `data/specs/resolving-2026-05-26/fusion-scripting-2026-05-27/SPEC.md`.
  Recipe shapes, golden capture, and the F7 offline-import smoke: spec
  § 12.2 + § 4 decisions 23–24 + § 11 (P1..P6 + M1..M10 ledger).

The consolidated subproject design contract is
`data/specs/resolving-2026-05-26/SPEC.md` — it folds the retired
`resolving/PLAN.md` (project master) and `resolving/davinci/PLAN.md`
(locked wrapper sub-plan) into one canonical file. § 3 carries the
project-wide decision log (amendable); § 4 carries the wrapper decision
log (LOCKED — amendments require a new dated spec); § 11 carries the
P1..P6 + M1..M10 phases ledger. Spec § 3 decision 9 (2026-07-04) makes
**Blender the third first-class plate engine** (kinds `still`/`loop`/`clip`
on the `composite_overlay` seam; skill S11 `compose-blender-scene` +
`davinci.recipes.decorate_scene_clip` shipped 2026-07-04) — contract at
`data/specs/resolving-2026-05-26/blender-compose-2026-07-04/SPEC.md`,
render side at `data/specs/blending-scenes-2026-07-04/SPEC.md`.

## 2. Layout

```
resolving/
├── CLAUDE.md            # this file (subproject conventions; design contract at data/specs/resolving-2026-05-26/SPEC.md)
├── davinci/             # typed Python wrapper component
│   ├── README.md        # consumer-facing intro + Quick start
│   └── docs/manuals/    # vendored Blackmagic manuals + extracts
├── skills/              # production skills (SKILL.md each), invoked by name; per-skill diagram.svg beside each
├── scripts/             # subproject-local utilities — render_fusion_diagrams.py + status_emit.mjs
└── .claude/
    ├── settings.json    # committed permission allow/deny
    └── skills           # symlink → ../../.claude/skills
```

Per-skill diagram artefacts live beside their `SKILL.md`
(`diagram.prompt.md` + rendered `diagram.svg` — a skill dir is
self-contained); the `diagrams/` sibling is the reserved whole-pipeline
production-lifecycle slot (P6, planned — spec § 11.1). Re-emit per-skill
diagrams with `python3 resolving/scripts/render_fusion_diagrams.py` from
the worktree root.

## 3. Downstream consumers

- `explaining/` — first consumer; 50 Janet-narrated videos, stage 5
  of the pipeline (`explaining/CLAUDE.md` § Pipeline). The per-video
  `phase*_*.py` drivers consume the davinci wrapper.
- `verifying/`, `evaluating/` — likely later consumers for short
  demo clips. Same wrapper, same skills.

No subproject imports code from `resolving/` directly. Cross-subproject
contracts are file-on-disk: the wrapper is installed via the root
`pyproject.toml` extras group `[davinci]` (consumed by venv users), and
skill invocations go through Claude Code's skill mechanism. See the
root § "Language split" — Python in this subproject; no TS surface.

## 4. Boundary with `explaining/`

`explaining/` owns the **content** of each video (script.md, design.md,
resolve.md, SHOOTING.md per the dir-per-video shape). `resolving/`
owns the **mechanics** of getting that content onto a Resolve
timeline + through Fusion + out as an MP4. The split is:

- `explaining/scripts/<topic>/<n.m>-<slug>/` — per-video content +
  the per-phase `phase*_*.py` drivers (shape owned by
  `explaining/CLAUDE.md` § 4; spec
  `data/charters/explaining/specs/production-phasing-2026-05-19/SPEC.md`).
- `resolving/skills/` + `resolving/davinci/` — the verbs those drivers
  call.
- per-skill `SKILL.md` + `diagram.svg` (whole-pipeline `diagrams/` is
  P6) — the human-readable map of the verb space.

If a per-video need turns out to be reusable, lift the verb into a
skill or wrapper helper here; don't fork it across `<n.m>-<slug>/`
dirs.

**HeyGen 9:16-only contract (locked 2026-05-10).** Per
`explaining/voice/janet/heygen-config.md` § "9:16-only render rule",
Janet HeyGen renders ship at 9:16 only — no native-aspect 16:9 take
arrives. The long-form 16:9 timeline (S2
`assemble-talking-head-with-broll`) imports the keyed-from-chroma 9:16
take and routes through a Fusion comp that places Janet on a 16:9
canvas (corner-PIP, lower-third, or split-screen against a 16:9 brand
plate). S3 `assemble-shorts-vertical` is unchanged — 9:16 take direct
to V1. Per-episode `phase*_*.py` drivers source from `takes/9x16/`,
never `takes/16x9/`. Same dual-aspect pattern as
`reference_resolve_dual_aspect_two_timelines`.

## 5. Frame-rate + Resolve gotchas (cross-cutting)

The wrapper bakes in the Resolve gotchas that bite every consumer:

1. **Start frame reset** — timelines default to frame 108000 (slate);
   wrapper resets to `00:00:00:00`.
2. **MarkIn/MarkOut on render** — required or render is single-frame.
3. **Source FPS detect-and-match** — project rate must match the
   imported source or Resolve conform-warps silently. HeyGen output
   has shipped at both 25 fps PAL and 30 fps, so do not hardcode
   either rate anywhere new. The wrapper itself is rate-agnostic —
   it reads `MediaPoolItem.fps` and validates against `Timeline.fps`.
4. **Bare `ResolveApiReturnedFalsy`?** — two known causes (the
   Project-Manager window blocks all scripting; audio-only WAV clips
   need an explicit `end_frame`): read `davinci/docs/gotchas.md`
   §§ 6–7 before debugging further.
5. **`LoadProject` refuses a project that is already current** —
   short-circuit `use()` when `current().name == name`. Detail:
   `reference_resolve_scripting_gotchas` #9.
6. **Color-managed projects crush near-blacks silently** — pin
   `color_space_timeline` + `color_space_output`, not just
   `color_science_mode`; `_assemble.py` does. Detail + the pixel
   evidence: `reference_resolve_color_managed_scene_crushes_blacks`.

Every skill that touches Resolve calls these in via the wrapper —
they are not optional. Pinned in
`reference_resolve_scripting_gotchas` and `reference_heygen_mp4_fps`.

## 5.5. Fusion-skill manual crosscheck (locked 2026-05-24)

Before shipping any `resolving/skills/<name>/SKILL.md` that documents
manual Fusion-authoring steps, verify each named node, parameter, and
apply-mode against `/Applications/DaVinci Resolve/DaVinci Resolve
Manual.pdf` (or the extracts under `resolving/davinci/docs/manuals/`).
Treat the manual as ground truth — not memory, not the v1 catalog's
existing prose. The 2026-05-24 audit caught copy-paste-consistent
hallucinations across all eight v1-catalog files (wrong node kinds,
invented properties, dead design-token paths — token SoT is
`rendering/` brand tokens, never a hardcoded path in skill prose).
Pinned in `feedback_fusion_skill_authoring_manual_crosscheck`.

**Runtime introspection is the final authority over the manual.** The
2026-05-29 golden capture caught `Glow` input-name errors that survived
the manual crosscheck — the real inputs are `XGlowSize`/`YGlowSize` (no
`GlowSize`) and `Red/Green/BlueScale` (no `*ColorScale`). Before trusting
a recipe's `set_input` names, dump the live tool's `GetInputList()` (or
capture a golden `.setting`) on the installed build. Same lesson for
capability claims: `SubtitleTrack.import_srt()` exists in source but
returns falsy at runtime (SRT-import-as-subtitle-track is unavailable via
scripting) — so `burn_in()` reads the SRT *file* directly. Verify against
a running Resolve, not the manual or `docs/api.md`. See
`reference_resolve_scripting_gotchas` § 4.

**Full-frame overlays bake to transparent ProRes, never host on a clip
(live-verified 2026-06-03).** A Fusion comp renders its output ONLY on a
*sourceless* generator; a comp on ANY sourced clip renders the source and
drops the overlay (the "two Janets" leak). Bake recipes, `burn_in`, full
diagnosis + disproven hypotheses: `davinci/docs/gotchas.md` § 4.

**PIP decoration is OFF-RESOLVE (locked 2026-06-07, build 21.0.0.48).** A
sourced-clip comp leaks its carrier even with `set_pip`, so the corner-PIP
element / wipe / chrome bake off-Resolve and composite as plain alpha media;
the Fusion `compose-pip-corner` / `compose-wipe-transition` node trees are
the interactive `## Manual` fallback only. Recipes + render gotchas:
`davinci/docs/gotchas.md` § 5; spec:
`data/specs/resolving-2026-05-26/headless-decoration-2026-06-07/SPEC.md`.

## 6. Asset partitioning rule (Fusion-first; locked 2026-05-09)

Cross-consumer guidance for any subproject that uses `resolving/` as a
rendering stage: before drafting **any** video-asset prompt (Claude
Design, HeyGen, image generators, Remotion components), partition the
deliverable's elements and ask the upstream generator only for content
Fusion can't synthesize natively.

Single owner of the rule, both lists (Fusion-native vs
generator-eligible), and the "not mechanical — it needs judgment per
asset class" caveat: `feedback_fusion_first_video_generation`. The
Fusion-native side is realized in the per-episode `phase*_*.py` drivers
calling `resolving/skills/compose-*` recipes.

Worked example: `data/charters/explaining/specs/background-prompts-2026-05-09/SPEC.md` § 2
(24-asset matrix collapsed to Fusion-composable primitives; its
12-plate remainder later superseded by the `blending/` plate lane).

## 7. Status emit slot

Producer `resolving/scripts/status_emit.mjs` writes
`data/status/resolving.json` per the root § "Status hub" contract
(placeholder shape — counts SKILL.md files under `skills/`; no
production-lifecycle diagram yet). Pinned to `@qagents/diagram-kit`
KIT_VERSION; sweep in lockstep on kit bumps. Spec:
`data/specs/data-status-rename-2026-05-17/SPEC.md` § 4.3 Cat-1.
