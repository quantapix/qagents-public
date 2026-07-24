# CLAUDE.md — explaining/

Project-specific rules for the Quantapix video-explainer arc. Assumes Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`.

## 1. Purpose

50 videos = 5 topics × 10 subjects each, 10–15 min each, narrated by **Janet** over animated cards/text + D3.js / Cytoscape.js graphics. Output is **scripts** plus per-episode production drivers; rendering runs downstream through the § 4 pipeline. 5 topics fixed (see `outline.md`); subjects redirectable by user; do not unilaterally rename/reorder once committed.

**Runtime envelope is finished runtime, not narration-only.** Janet-2 (locked HeyGen voice; `voice/janet/heygen-config.md`) reads at ~280 wpm at default speed — target ~6–7 min narration for a 13-min finished envelope; the remainder is Resolve padding. Pause-rich pacing (em-dashes, mid-question ellipses, numbered lists) drives Janet-2 to ~175 wpm at ~1.6× credit cost per word — use deliberately, not by accident in dense beats. Per-beat table + credit budget: `reference_janet_2_pause_rich_pacing` + `reference_heygen_credit_budget_50_video_arc`.

## 2. The 5 profile areas

Every video carries one or two profile-area tags:

- **P1** — rigorous proofs for LLM "reasoning" (`proving/`, `accounting/`)
- **P2** — legal applications (`appealing/`, `pleading/`, `legal/`, `verifying/`)
- **P3** — financial applications (`analyzing/`, `accounting/`, `evaluating/`, `trading/`)
- **P4** — grounding competing TA approaches (`analyzing/`, `monitoring/`)
- **P5** — agentic software development (`qagents/`, `lib/memsearch/`, sub-agents)

A subject without a P-tag is not ready to script.

## 3. Brand sync — non-negotiable

The two websites (`designing/web/` quantapix.com, `documenting/web/` femfas.net v2) and the two apps (`verifying/` Qnarre, `evaluating/` Qresev) must look and feel like the same family as the videos.

- D3 / Cytoscape themes read brand tokens from `rendering/` (brand SoT; no hex literals in script-rendering code). **Token + title-face split by cohort (operator ruling 2026-07-09, full Meridian — `data/specs/claude-design-prompts-2026-07-09/SPEC.md`):** cohort-3 forward + the 2.3/3.6 re-skin read `rendering/brand/tokens/meridian/{light,dark}.css` (`--m-*`; petrol/porcelain per-episode legs) — title face is **Newsreader** (serif display), chrome Instrument Sans, trace Spline Sans Mono. Published pre-cohort-3 material stays on `rendering/brand/core/tokens.css` with Space Grotesk (`FONT.display`) titles. The silent-fallback rule stands: never spec a face the loader doesn't ship — all six families are bundled (`code/remotion/src/fonts.ts` + `rendering/brand/fonts/fonts.css`).
- Wordmark, accent shapes, closing-card lockup match the live sites.
- Retired brand names never appear (see `feedback_quantapix_naming`).
- Voice/pacing for **narration content + on-screen body copy** matches the calm, declarative cadence of the site copy. No marketing exclamations.
- **Quantapix-Thesis messaging floor (every public video — narration + on-screen card; binds all 50, including already-published renders — a prior clearance predating the floor does NOT survive it).** Source `studying/thesis.md`; riders `designing/web/src/content/copy.ts` `disclaimer.{canon,legalRider,financialRider}`. Legal verdicts in **CONCEDE-AND-PREEMPT** voice ("a conclusion follows from the stated predicates and axioms," never "true/proven/adjudicated"); worked legal demos are **synthetic Doe v. Acme** only — mirror Qnarre's public allow-list (`verifying/server/main.py` `ALLOWED_EXAMPLE_IDS`); **never name a `<live-matter>_*` example**. Financial verdicts carry the due-diligence rider; the concession must be **baked onto the rasterized verdict card** (G5/G6), not only spoken. `pleading/` holds the binding MESSAGING veto. Channel-canonical baked strings (concession tail; 2-clause financial footer) are pinned by the cohort-3 debate in `data/messaging-rulings/2026-07-03.md` — **BUT the evaluating FINANCIALLY gate is STRICTER**: Qresev framework-verdict cards bake the **four-sentence `RIDER_FULL` byte-equal to `evaluating/web/src/content/copy.ts` `disclaimer.financialRider`**, never the 2-clause tag (source-gated per episode by `phase0_preflight.py` § 0.5 — hard-fail on drift or any verdict comp missing it). Episode ordinals are **topic-local** — never a global "video N of fifty". **R11 topic-5 ownership framing (`data/messaging-rulings/2026-07-09.md`, Option A):** public framing is **operational** — one engineer + an AI assistant; no surface states/implies two humans **built** the work, discloses any second person's **ownership/investment** stake, references the equity transfer, or claims **sole ownership** ("sole developer/founder" clears, "sole owner" barred); the AI "Janet" persona is disclosed as AI-synthesized wherever it appears. Audit trail + full string history: quantapix-thesis spec §§ 4.1+10.4 (`data/charters/studying/specs/lean4-charter-2026-06-10/quantapix-thesis-2026-06-22`) + memory `project_explaining_subproject`.
- **`design.md` is a gated signoff FACE, and on-screen verdicts bind to the run they name (3.6 block, 2026-07-10).** (a) A bundle's `design.md` sha binds into the FINANCIALLY record's `content_sha256` alongside `script.md` + the locked title (signoff-framework § 3.6) — re-editing it VOIDS the grant; its rider spec states the four-sentence `RIDER_FULL` verbatim (never the tag), a component must not under-implement its `design.md`, and `phase0_preflight.py` § 0.5 reads `design.md` too (whitespace-normalized), so the reviewed face can't drift below floor while the gate stays green. (b) If a beat names an `accounting/examples/<id>` run, every framework-verdict token in that beat binds to **that run's emit** (CLEAR-5) — no committed example emits all five frameworks, so a five-green single-run radar is not renderable; use 3.3's `G6Triad33` three-valued grammar (pos / neg-with-domain-word / honest-empty `— not claimed`, same box + weight). Fixture vocabulary must be **real kernel vocabulary** (`accounting/predicates/`; build target `examples.<id>.proof`), never invented ids. Mechanical `--rider-floor` green attests presence/byte-equality, never CLEAR-5 (judged).
- **Exception — YouTube channel art layer.** Channel banner, titles, and thumbnails intentionally depart from calm voice (loud, single-word anchors); scoped to that art layer only — never narration, in-video copy, website copy, or the public README. All YouTube **channel** material now lives in `publishing/` (see § 4); spec `publishing/youtube/DESIGN-SYSTEM.md` § "Voice override" + memory `feedback_youtube_voice_override`.

## 4. Deliverable shape

```
explaining/
  CLAUDE.md, outline.md (5×10 master plan)
  scripts/<topic>/<n.m>-<subject-slug>/  (POSITION; one of the 50 — neutral subject id, title is NEVER in the path)
    meta.json          position metadata (spec explaining-shorts-social-2026-06-15 § 4): subject slug,
                       debate-locked long+short titles, version index (null=flat single-version). Resolver
                       reads this for flat-vs-vN, never probes the tree. Title is METADATA, not a path.
    long/              the full 13-min derivation (single version → FLAT; a 2nd version promotes to long/v1 + long/v2)
      script.md        Janet narration with timing + card cues + graphic spec
    short/             the dedicated ≤2-min vertical social cut (only for positions carrying a short)
      script.md        own hook+payoff script (NOT a re-cut of the long form — spec § 2.1)
      heygen-aroll.md  dedicated 9:16 take payload   phase9_shorts.py  thin off-Resolve driver (SLUG + TAKES)
    --- the rest live under long/ (and channel-wide shared modules at scripts/ root) ---
    design.md          Claude Design prompts (input record; G1..G7 + cards + B-roll enrichment as siblings)
    resolve.md         DaVinci Resolve A/B coordination, wrapper + S1..S10 binding
    SHOOTING.md        production gate + cut→render→publish sequence
    heygen-aroll.md    per-beat HeyGen call payloads
    retime_markers.py  cue→phrase-anchored .srt resolver via shared `scripts/_anchor.py` (cues anchor by phrase text, not seg index — re-renders re-segment)
    _layout.py         per-episode-local + decoration-agnostic PIP wipe layout; `compute_layout` writes `.wipe-layout.json` (phase1→phase3), so both lanes share ONE sidecar
    phase{0,1,2,3,5,6,8,9}_*.py per-phase drivers (channel-wide; `phase2_caption.py` = qreel Q0-B captioning). **TWO-LANE PIP decoration (qreel spec § 10):** Resolve 21.0 leaks the source on a scripted comp over a sourced clip → phase1+phase3 fork into THIN per-episode variants: lane A (default, headless off-Resolve) / lane B (`/reel --stage-only`, Fusion). Shorts are purpose-drafted (`data/specs/explaining-shorts-social-2026-06-15/SPEC.md`; `short/phase9_shorts.py` thin over `scripts/_shorts.py`; `/shorts/` = manual YouTube flow).
    scripts/_{assemble,decorate,decorate_offresolve,decorate_fusion}.py  scripts-level lane-common phase1/phase3 modules (siblings of `_anchor.py`/`_shorts.py`; `long/` thin drivers import via `sys.path.insert(parents[3])`). Full lane split + per-episode constants + per-function API + the `_assemble.assemble_common`/injected-`layout` seams in memory `project_explaining_subproject` + `project_qreel_plugin`.
    phase3_outro.py    branded end-screen outro (decoration-tail, runs after phase3_decorate). Slug-derived + per-episode `outro.json` (next ep/title/thumb). Composites a flat 1920×1080 plate with **Pillow** (Inter + next-video thumbnail tile + Subscribe pill; bottom corners kept clear for YouTube's native end screen) → ffmpeg 20s ProRes → appended as a plain clip (no Fusion comp). Fusion was abandoned (missing-font renders + still/video Merge-Size quirk) — see `reference_resolve_fusion_compositing_gotchas`.
    outro.json         per-episode outro data (next_episode/next_title/next_thumb; optional accent_hex/outro_seconds/body_tail_trim_s — the last pulls the outro earlier to cut a lingering trailing close-card, opaque-plate overlap; 1.1=2.0s)
    FUSION-NOTES.md    per-episode S5/S6/S7 keyframe + SFX + subtitle authoring aid (locked 2026-05-15 with 1.5+2.1)
    PRODUCTION.md      operator runsheet (12-phase layered-scaffolding per `data/charters/explaining/specs/production-phasing-2026-05-19/SPEC.md`)
  artifacts/<slug>/    per-video Claude Design bundles (episode-local)
  videos/              per-video production assets ONLY (channel material moved to publishing/youtube/ 2026-06-02)
    <slug>/long/{takes,auditions,cuts,cues,captions}/  per-episode long binaries (mp4/mov/wav/srt gitignored)
    <slug>/long/markers.{csv,md}                       tracked word-boundary ground truth (under the variant dir)
    <slug>/short/{takes,cuts,captions}/                dedicated short binaries (takes/short/ = the 9:16 short take)
  avatar/                   real-Janet HeyGen production set (LOCKED 2026-05-11): README.md registry (image ↔ avatar_id cross-link + pose-rotation policy) + 3 trained source stills + Janet-1.jpg identity reference — detail in § "Janet identity" below
  voice/                    superseded AI-generated masters kept for provenance (build chain v2 → v3 → v3.1 incl. Gemini/Firefly audit trail; lineage in voice/janet/master-meta.json)
    janet/                  channel-wide voice config (master-meta.json § lineage + heygen-config.md)
```

The `.mp4`/`.mov`/`.wav`/`.srt` patterns under `videos/*/{long,short}/{takes,auditions,cuts,cues,captions}/` are gitignored render outputs (per-take `.srt` = HeyGen `subtitle_url` download; `captions/master.srt` offset-assembled by `phase2_caption.py`). Worktrees symlink these leaf dirs via `explaining/.worktree-links` (session-lifecycle CHARTER § 2.4). **Only `markers.csv`/`markers.md` under `<slug>/long/` stay tracked** — the git-durable word boundaries the Remotion `.tsx` ports anchor to (`retime_markers.py` regenerates through the symlink). HeyGen `get_video` recovery viable ~7 days post-render; `.close-protected-paths` backs up a brand-new slug. Pinned in `feedback_git_worktree_remove_wipes_gitignored`.

**Gitignored-binary S3 backup** (`backup-cues.sh`; `SHOOTING.md` gate before takes-complete). Spec `clips-backup-s3-2026-05-24`.

**Pipeline (locked 2026-05-06; MCP-driven 2026-05-07; B-ROLL-FIRST reorder 2026-07-11 — operator ruling):**

| Stage | Tool | Driver |
|---|---|---|
| 1. Script | Claude (`script.md`) | this subproject |
| 2. Per-video Design bundle | Claude Design (`design.md` → `artifacts/<slug>/`) | this subproject |
| 3. B-roll — authored, assembled, quality-gated | Remotion (locked 2026-05-07) — React + brand tokens (+ Blender plate lane where declared) | `@qagents/remotion` workspace pkg at `code/remotion/`; per-video components at `explaining/artifacts/<slug>/components/`; cue render per the cue-render contract below (rendering-owned manifest engine → per-cue ProRes 4444) |
| 4. Janet narration + lipsync — fires ONLY after the stage-3 gate | HeyGen Photo Avatar IV / V | `mcp__heygen__*` via `.mcp.json` + `.claude/skills/heygen-{avatar,video}` |
| 5. Composition + subtitles + loudness + render | DaVinci Resolve Studio | Per-video drivers consuming `resolving/` (wrapper `resolving/davinci/` + skills S1..S10). Driver shape: the `phase{0,1,2,3,5,6,8,9}_*.py` scripts described above (deliverable-shape entry); spec `data/charters/explaining/specs/production-phasing-2026-05-19/SPEC.md`. |
| 6. Publish | `s3://qagents-videos/<topic>/<file>.mp4` → `https://videos.quantapix.com/<topic>/<file>.mp4` (immutable) | `aws-vault exec qagents-deploy -- bash serving/scripts/upload-video.sh <local> <topic>/<file>.mp4` |

**B-roll-first gate (channel-wide, all future videos; operator ruling 2026-07-11).** Once a script is written and cleared, the next production step is the B-ROLL, not narration: author + register the full comp set (G-comps + cards + GM comp) and assemble a silent b-roll preview at `script.md` target windows; **no HeyGen take fires until the supporting material is complete, coherent, and of compelling visual quality** (operator review of the assembled preview is the gate — a-roll credits are the expensive, re-shoot-hostile leg). Pre-take comps anchor to `script.md` windows (intent); `markers.csv` re-anchor happens after takes — the cue-render contract below is unchanged for the FINAL render. First build under this gate: 1.2 (exemplar `artifacts/1.2-semantic-search-limits/`).

**The preview is PIP-BLIND — overlay the PIP box before lifting the gate (1.2, 2026-07-11).** The silent preview composites no Janet PIP and no captions (V6), so occlusion of the `x≥1512 ∧ y≥392` keep-out and the V6 caption band is *structurally invisible* at the gate; a lifted gate does NOT mean the b-roll survives compositing. Before lifting, draw the keep-out (`ffmpeg drawbox`) and re-check every comp's payoff — the check the bundle's own `design.md` floor already demands. Incident + mechanics: `feedback_broll_preview_is_pip_blind`.

**Grade the timeline colour, not just the comps (channel-wide, 2026-07-11).** `_assemble.py` must pin `colorSpaceTimeline`/`colorSpaceOutput` to `Rec.709 Gamma 2.4` / SDR 100 alongside `color_science_mode` — science-mode alone leaves Resolve scene-linear and crushes near-blacks past eyeballing. Never fix a black-gate failure by lightening the bed; check the render's actual ground pixel against `BG_BASE` first. Mechanism: `resolving/CLAUDE.md` § 5 item 7 + `reference_resolve_color_managed_scene_crushes_blacks`.

**App-UI episode HOLD (2026-07-11 → unified-app-UI ship, expected ~2026-07-24).** Any episode whose b-roll depicts the app UI (shell wireframes, three-zone layouts, SSE panes, walkthrough frames) holds FINAL production — comp re-render, takes, composition, publish — until the new UI ships, then re-skins its app-UI comps against the REAL shell (never a simulated guess). Held: **2.3** (phase-7 done, pre-publish), **3.6** (pre-cue), **2.4** (cohort-3). Non-UI material for held episodes may proceed under the b-roll-first gate.

ElevenLabs deferred — see `reference_janet_video_stack`. **Subtitles render from the episode's input SRT** (terms correct by construction — no STT) via `phase2_caption.py`; Resolve's STT is the no-input-SRT fallback only. **Segmented caption bake (2026-06-04):** `master.srt` (YouTube sidecar + bake source) bakes into transparent ProRes 4444 overlays — plain alpha, never a take-hosted Fusion comp (the 21.0 source-leak class); under the off-Resolve PIP layout (V1–V5 = bed/B-roll/Janet-lower/Janet-upper/chrome) captions land on **V6**. See `reference_resolve_subtitle_api_textplus_from_srt` + `reference_resolve_fusion_compositing_gotchas`. **Caption-contrast floor (all 50; 2026-07-11):** baked captions MUST contrast with what's behind them — **never white/near-white text over a light bed/B-roll**. Ink is a per-episode theme decision derived from the episode's `BG_BASE`/theme leg (porcelain → dark ink + light keyline; dark/petrol → light ink; no episode inherits another cohort's caption constants); phase-6/8 review checks legibility over the lightest frame the captions cross. **Finished-master loudness is a `/reel` (qreel) post-render ffmpeg loudnorm pass, not the phase drivers** — `code/qreel/` + `data/specs/qreel-2026-05-28/SPEC.md`.

**Publish-key shape — title-as-metadata (standing rule 2026-06-15).** When **publishing an episode**: three decoupled names (neutral `<n.m>-<subject-slug>` position-id path, debate-locked title metadata, publish-derived public key) let a title change without a rename cascade; publishing gates the DERIVED public key. Mechanism (long/short key form, R-S4 `-short` suffix, cdnUrl-slug scan): shorts spec `explaining-shorts-social-2026-06-15` § 4 + `publishing/CLAUDE.md` § 10. Source MP4s stay laptop-local (`videos/<slug>/cuts/`, gitignored); cross-site contract `serving/CLAUDE.md` § 8. **Every `T<n>/` catalog upload requires `CLEARANCE_COMMIT`** (a FINANCIALLY-CLEARED record's `granting_commit`, ancestor of HEAD — `upload-video.sh` exit-3s otherwise) **whether or not the episode is financial**: non-financial episodes need a verified-N/A `/do-signoff` from `/open evaluating` first (template: the 4.1 all-clauses-n/a record).

**Release record is explaining-owned — write it from `/open explaining`, never from publishing (binds all 50; standing rule 2026-06-30).** Once a variant is CDN-published, the **explaining** session holding the branch records it into the episode's `meta.json`: set `variants.<long|short>.produced: true` and add a `released` block (`date`, `cdn_key`, `url`) mirroring the immutable CDN key publishing minted. `publishing/` mutating this sibling tree trips the canonical-edit hook + close-time exit-14 gate (§ 3 / worktree-path discipline), so the write MUST live in an `/open explaining` session (or a lift-across); publishing mints+gates the key and hands it back, never edits `meta.json`. Mirror for the short variant when its cut ships.

**Short in-feed thumbnail = a video frame, not the custom thumb.** When **producing a Short**, bake the thumbnail design as a ~0.5 s opening hold at the head of the cut (Shorts feed/shelf ignore `thumbnails.set`); still set the 16:9 thumb (rendering's short-thumb + publishing's `thumbnails.set`) for search/shares. Detail: shorts spec `explaining-shorts-social-2026-06-15` § 2.7.

**Two B-roll lanes (locked 2026-05-15; plate-spec revised 2026-06-08; Wave-3 scenes live 2026-07-04).** Per-video graphics are predominantly Remotion-authored (stage 3); a bundle MAY also declare a Blender plate slot. Invariants: **one Blender plate per episode → one `blender_plate.json`** sibling to `design.md` (the `<gN>_pattern.json` scheme is retired), committed early even as a stub so blending's `status_emit` sees demand; **author full-fidelity plates** (opacity/desaturation are resolving dimming concerns); the Resolve comp resolves the plate through `data/renders/blending-design/MANIFEST.md` (`_manifest_plate_asset(slug, kind=…)`), **never a hard-coded hash**; kinds `still|loop|clip`, `design.md` states the motion class (`PlateSpec.kind` + `at_marker`). Full spec/builder/compose detail: `data/charters/blending/specs/blending-motif-wave2-2026-06-08/SPEC.md` § 3.2 + `data/specs/blending-scenes-2026-07-04/SPEC.md` + `data/specs/resolving-2026-05-26/blender-compose-2026-07-04/SPEC.md` + memory `project_blending_subproject`.

**Remotion B-roll cue render contract (locked 2026-05-17).** Every composition's **cue frames anchor to `videos/<slug>/markers.csv` `take_seconds × fps`**, never script.md beats (script.md = intent, markers.csv = the take's word-boundary ground truth via `retime_markers.py`); re-anchor before render. Render via `rendering/scripts/render.sh explaining-cards` — the rendering-owned manifest engine (roster `rendering/designs/explaining-cards/manifest.json`) → ProRes 4444 RGBA at `videos/<slug>/long/cues/long/<marker_key>.mov` (consumer `scripts/_assemble.py`). JSX stays explaining-owned under `artifacts/<slug>/components/` (registered in `code/remotion/src/Root.tsx`); explaining authors+registers the comp, then **`rendering/` adds the matching `manifest.json comps[]` entry** (per-episode handoff — an explaining-branch write to the manifest trips exit 14; manifest is the single roster SoT). Full pattern + flags in `[[reference_remotion_port_pattern]]`. **Janet-PIP keep-out (channel-wide, all 50):** `set_pip` scales the 9:16 take to 360 px wide → 640 px tall, occlusion **x≥1512 / y≥392**; keep payoff left of x≈1500 or wrap. See `[[feedback_broll_pip_safe_band]]`.

**No-black-frame floor (channel-wide, all 50; 2026-06-26 after 4.2).** Long-form full-frame visual = B-roll card cues on V2 (gap precedes each card); the **V1 bed** behind them MUST be opaque, the episode's own theme colour, and span the full body (size off `_body_end(tl)`, never `tl.end_frame`) or uncovered frames flash Resolve's black canvas. **Gate:** `scripts/check_black_frames.py` in phase6 + phase8 fails any black span — wire into every episode. Mechanics: `reference_explaining_render_silent_master` + `project_explaining_cohort_theme_ab`.

**Opening sequence — thumbnail flash → established cold open (channel-wide; 2026-06-26).** Episode opens on its 16:9 thumbnail as a ~0.5s opaque full-frame branded flash (Janet + title, no PIP; narration under it; covers the frame-0 gap), hard cut to the cold open on ESTABLISHED content (`OPEN_HOLD` → `_assemble.deintro_cue` freeze-hold, post-hold timing bit-identical so narration-sync is preserved). `decorate_open_thumb` + `phase3_outro` are idempotent. Mechanics: `reference_explaining_render_silent_master`.

**Brand fonts + wordmark lockup (channel-wide; 2026-06-26/29).** Cards render Space Grotesk via `FONT.display`; `phase3_outro.py` draws the Q-glyph + "Quantapix" lockup. The faces are REAL only because a **SHARED loader** (`code/remotion/src/fonts.ts` + `Root.tsx`; woff2 at `code/remotion/public/fonts/`) registers them — **don't re-add a per-episode loader** (the wordmark swap IS per-episode; the PIP "Janet" plate stays Inter). Mechanics: `[[reference_remotion_port_pattern]]`.

**Asset partitioning rule (Fusion-first).** Before drafting any video-asset prompt (Claude Design, HeyGen, image gen, Remotion), partition per `resolving/CLAUDE.md` § 6 — anything Fusion synthesizes natively is NOT a prompt ask; reduce the matrix first. Worked example + memory: `data/charters/explaining/specs/background-prompts-2026-05-09/SPEC.md` § 2 + `feedback_fusion_first_video_generation`.

**Frame rate is 30 fps end-to-end** (locked 2026-05-08); never hardcode a rate in new per-episode driver constants — the `resolving/davinci/` wrapper is rate-agnostic (`resolving/CLAUDE.md` § 5). Hist. 25-fps PAL: `reference_heygen_mp4_fps`.

**HeyGen take handles — MANDATORY, fail-closed (channel-locked 2026-06-02; gated 2026-06-25).** Every take MUST fire with the § 0.1 silence-handles: `script` wrapped `Start clip. 🕐 <verbatim narration> 🕐 End clip.` (recipe in each `heygen-aroll.md` § 0.1). HeyGen trims leading/trailing silence, so an UNPADDED take has no dissolve idle and silently breaks `_anchor.anchor_trim`, `retime_markers.py` seg-strip, and phase1 PIP dissolves — unusable. Gate before firing (`check_clip_handles.py --aroll`) and after download (`--srt videos/<slug>/long/takes/9x16`); `phase0_preflight.py` runs the same check (canonical SRTs only, `-v\d+` excluded). Recipe + incident: `reference_heygen_silence_handle_recipe`.

**Avatar engine.** Photo Avatar IV vs V is a **fidelity tier, not a gate** — V is API-available on `photo_avatar`; `digital_twin` uplifts identity fidelity at either engine, does not unlock V. Channel routes by cost/fidelity tradeoff per take. Pinned in `reference_heygen_avatar_iv_v_engine_pivot`.

**MCP servers** wired at `explaining/.mcp.json` (subproject-scoped; see `reference_mcp_subproject_scoped_via_file_location`). `explaining/.claude/settings.json` allows `mcp__heygen__*`. HeyGen requires `/mcp` OAuth on first use (Chrome — Safari ITP fails). Resolve scripting goes through `resolving/` (no MCP) — wrapper at `resolving/davinci/`; requires Resolve Studio running with External scripting = Local on first connect.

**Prompt-iteration discipline.** Lift a richer-than-asked Claude Design read into round N+1 (`feedback_design_round_richer_than_prompt_promote`); when prompts name typographic detail as deliverable, add an explicit DO-include carve-out to every per-tool "no text" negative list (`feedback_image_gen_subject_matter_text_carveout`).

**YouTube channel material is owned by `publishing/`, not here (moved 2026-06-02; see § 3 Exception).** Design-system prompts + Studio paste-text at `publishing/youtube/`; channel-art design sources at `rendering/designs/publishing-youtube/`, rendered deliverables at `data/renders/publishing/`. Split = channel (publishing) vs. content (explaining: scripts/graphics/narration + the Janet master under `voice/`/`avatar/`).

**Janet identity — LOCKED 2026-05-11 (real-Janet production set).** Three HeyGen Photo Avatars (priority 1 hand-down / 2 hand-up / 3 tight-crop PIP), rotated per beat-archetype. Voice `q03EFCokNol7UHaF1YAQ` (Janet-2, Design-a-Voice); `frozen_after_acceptance=true` — any avatar_id change is a channel-rebrand. Registry, identity anchor, rotation policy, superseded-AI-master provenance: `avatar/README.md` + memory `project_explaining_subproject`.

**AI disclosure posture (locked at v3 promotion).** No visible generator marks on the channel face; disclose via the platform altered-content toggle + description text naming the stack (Gemini + Firefly + HeyGen + Remotion + Resolve). Detail + sparkle-removal technique in `feedback_gemini_sparkle_synthid_unprompiable`.

## 5. Anchor everything

Every script must cite the qagents file(s) it claims to be about (e.g. `proving/Proving/RICO/Pattern.lean`, `financial/parquet/gics-symbols.parquet`, `analyzing/aggregators/`). If you can't anchor the claim in the repo, drop the claim. Memory pins are valid anchors when the file isn't written yet, but flag those clearly.

## 6. Public-facing derivation

`outline.md` is the **authoritative source** for the public `qexplaining-public`
README, but `explaining/` no longer renders or copies it out. The public README is
rendered by the `publishing/` subproject during `/publish` (it sweeps `outline.md`,
applies the redaction + voice guardrails, and pushes to `github.com/quantapix`).
`explaining/` owns `outline.md`; the render-and-push duty moved to `publishing/`
(drive Promise 1; spec `data/specs/publishing-2026-05-31/SPEC.md`). Edit `outline.md`
here and let the next `/publish` pick it up. See
`feedback_public_facing_source_render_split`.

## Status emit (`data/status/explaining.json`)

`explaining/scripts/status_emit.mjs` participates in the qagents-wide Status page contract (KIT_VERSION pinned in the producer — re-sweep on every kit bump). Status pill is permanently `NOT_YET_LIVE` in v1 — explaining is a script repo; rendering happens downstream. Schema: `@qagents/diagram-kit`; contract: `qagents/CLAUDE.md` § "Status hub". Self-contained — no sibling-subproject imports.

Summary diagram is the Stage 1–6 pipeline (script → Claude Design → Remotion → HeyGen → DaVinci Resolve → S3/CloudFront). The producer also emits the `tables?: TableEmit[]` 5×10 arc-matrix, derived from `outline.md` + on-disk per-episode artifacts. Rows grouped by topic; refreshes automatically at every close.
