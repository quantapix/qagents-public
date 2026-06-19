# CLAUDE.md — publishing/

Project-specific rules for the qagents open-source release subproject. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`. Don't
re-litigate those.

## 1. Purpose

`publishing/` is the **single owner** of open-sourcing the qagents framework —
drive Promise 1 (`donating/drive.md` § 4). It renders, redacts, compiles, and
pushes the public `github.com/quantapix/*` repos. After this subproject, **no
other subproject carries any open-sourcing responsibility** — each keeps only
its own internal `data/status/<sub>.json` emit.

Authoritative contract: `data/specs/publishing-2026-05-31/SPEC.md`.

## 2. What it owns / what it does not

**Owns:** the public-org staging tree `publishing/quantapix/` (migrated out of
`data/`); the `/publish` pipeline (sweep → collect → verify/redact → compile →
push); the external push surface `git push-quantapix`; drive Promise 1; the
redaction-clean gate before any push; the **@Quantapix YouTube channel**
material (`publishing/youtube/` — channel-page copy, brand/thumbnail/motion
prompts, upload specs), migrated out of `explaining/videos/` 2026-06-02. The
split is **channel vs. content**: the channel face (handle, banner, About,
thumbnail system, brand kit, upload specs) is publishing's; the 50-video 5×10
arc itself stays in `explaining/`. The Janet identity master + voice config
stay in `explaining/avatar/` + `explaining/voice/` (HeyGen narration is
`explaining/`'s job); `youtube/` cites them, does not own them. The channel
*design sources* (JSX harnesses + canvas bundles) live at
`rendering/designs/publishing-youtube/` and the rendered deliverables at
`data/renders/publishing/` since rendering/ P1 (2026-06-10,
`data/specs/rendering-2026-06-09/SPEC.md`) — publishing is rendering's first
consumer; request re-renders via `rendering/scripts/render.sh
publishing-youtube`, never a hand-rolled capture script.

**Does not own:** drive content (`donating/drive.md` is the source of truth —
publishing reads it, never edits it); the hosted verification service (Promise
3 — `serving/`+`verifying/`+`evaluating/`); axiom authoring (Promise 2 —
`proving/`+`accounting/`); the internal status hub (each subproject self-emits);
Astro-site deploys (`designing/web`+`documenting/web` via `serving/` § 8).

## 3. Boundary posture

Content-in / external-out — the same shape `donating/` has, plus a push surface.
`publishing/` imports no sibling code and none import from it (root CLAUDE.md
language-split rule). Inbound is **content only** — public-safe renderings of
`studying/`, `explaining/`, `proving/`, `accounting/`, `donating/`, and the root
CLAUDE.md graph. Outbound is the public GitHub org via `git push-quantapix` only.

`publishing/` is **not observe-only** (unlike `managing/`/`shorting/`): it writes
its own subtree and pushes to the external org. But it **never** commits/pushes
the *qagents* repo outside `scripts/close.sh` (the interactive-lane audit gate),
and **never** mutates any sibling subproject's tree.

## 4. The `/publish` pipeline

Triggered by the `/publish` skill (`.claude/skills/publish/SKILL.md`, a thin
orchestrator over `scripts/publish.sh` + the top-tier-model collector fan-out). Five
phases: preflight → sweep (top-tier-model fan-out, one `publish-collector` per source
subproject, Max-20x interactive billing) → verify/redact (HARD gate) → compile
→ push (operator-confirmed). Full mechanics: spec § 5; staging-tree layout +
source mapping: `publishing/quantapix/CLAUDE.md`.

No cron lane at v0.1 — the drive cadence (weekly Fridays) is operator-run via
`/open publishing` → `/publish`. A cron lane is documented-future (spec § 10 P4),
not v0.1.

## 5. Redaction is a hard gate, not advisory

A HARD blocklist hit (the Hickory address family + the SOFT opposing-party /
counsel / docket / agency-PII set) anywhere in the candidate tree **aborts**
the compile/push. `publishing/` inherits `documenting/`'s redaction rules
(`documenting/letters/REDACTION.md` + the `HARD_PATTERNS`/`SOFT_PATTERNS` in
`documenting/scripts/check_redactions.py`); it invents none and relaxes none —
the same load-bearing privacy floor `donating/` § 7 names. The gate is wired
before the push and pinned by the companion test
(`data/specs/publishing-2026-05-31/tests/cases/t_10_publish_gate.sh`).

**The candidate tree is markdown, so the gate must scan markdown.**
`publishing/scripts/sync_mirror.py` Stage 3 applies the blocklist patterns as
it renders each CLAUDE.md / memory mirror. **The markdown gate is live
(2026-06-05; the prior vacuous-pass gap is closed):** `publish.sh` runs
`sync_mirror.py --scan-tree <tree>` as the PRIMARY gate — a HARD+SOFT sweep
over **every `*.md`** under the candidate tree (the hand-authored READMEs,
`STATUS.md` files, and the `skills/` subtree included), and it *refuses to pass
over an empty tree*. It skips `CLAUDE.md`-named files (staging governance — not
pushed; the bridge `--exclude='CLAUDE.md'`s them) and carves out the
developer's own public name via `sync_mirror.py` `ALLOW_PHRASES` while keeping
the litigation linkage HARD-blocked. The `check_redactions.py --tree` PDF gate
stays wired after it as defense-in-depth (stray `*.pdf`). The resume tree
(`publishing/resume/`) is gated by the same sweep. Gate-before-push ordering is
pinned by `t_10_publish_gate.sh`.

## 6. Write-lock & session model

- **Branch-as-lock.** `/open publishing` creates branch `publishing` + worktree
  `<root>-wt/publishing/`. Every Edit/Write `file_path` begins
  with that worktree root (canonical-edit hook,
  `data/specs/open-close-dcu-2026-05-26/canonical-edit-hook-tightening-2026-05-28/SPEC.md`).
- **`data/status/publishing.json`** is written by `scripts/status_emit.mjs`, a
  fixed-path producer under `data/` — it acquires `.data-write-lock` per the
  universal manual-writer rule (root CLAUDE.md § "Shared-data write-lock") when
  writing canonical.
- **The external push** (`git push-quantapix`) is not a qagents-repo write — no
  qagents lock involved; its scratch clones live outside the tree.
- **`pending/publish-digests/`** is a gitignored, fork-internal buffer (mirrors
  `pending/dco-digests/`). It is **never** promoted by managing's verifier
  (registered in the verifier internal-set + `verify-pending.sh`'s
  `require_not_internal_pattern` deny-list). Discarded at close by default.

## 7. Status emit (`data/status/publishing.json`)

`scripts/status_emit.mjs` participates in the status contract (root CLAUDE.md
§ "Status hub"). Pins a `KIT_VERSION` constant (the producer's pin is the
source of truth — 0.5.0 since the 2026-06-10 rendering widening; swept in
lockstep on kit bumps). Four-state pill machine: `OK`
(last `/publish` clean) / `BUILDING` (run in flight) / `DEGRADED` (last run
aborted on the redaction/drift gate — privacy floor held, release stale) /
`NOT_YET_LIVE` (pre-first-publish; first live push 2026-06-12). The pill
resolves from the tracked one-line state file `publishing/.publish-state`
(`<PILL> [reason]`, written by the `/publish` lane — emitter defaults to
`NOT_YET_LIVE` without it). Summary diagram = the five-stage pipeline;
`TableEmit` = the repo roster. Close-time emit is mandatory
(`/close --status-emit publishing` resolves the producer via `close.sh`).

## 8. Layout

```
publishing/
├── CLAUDE.md                 # this file
├── README.md                 # quickstart: what /publish does, the repo roster
├── PLAN.md                   # rollout phases (spec § 10 as a checklist)
├── quantapix/                # the public-org staging tree (see quantapix/CLAUDE.md)
├── youtube/                  # @Quantapix channel material (see youtube/README.md)
│   ├── README.md             # scope + provenance + index
│   ├── DESIGN-SYSTEM.md      # channel design-system index (was explaining/videos/README.md)
│   ├── CHANNEL-INFO.md       # paste-into-YouTube-Studio copy
│   ├── YOUTUBE-SPECS.md      # format / dimensions / safe-area / file-naming
│   ├── STUDIO-FILL-IN.md     # operator walkthrough mapping copy onto the Studio form
│   ├── RESPEC-LIGHT-LIVE-2026-06-07.md      # system-wide re-prompt: light palette + real-Janet skin tone + master-res export
│   ├── RESPEC-THUMBS-DEPTH-2026-06-08.md    # thumbnail-only: depth/dynamism toolkit + 6 launch thumbs light (fixes "too flat")
│   ├── LAUNCH-COHORT-RESPEC-2026-06-04.md   # Claude Design rerun hand-off (delivered)
│   ├── LAUNCH-COHORT-UPLOAD-2026-06-06.md   # paste-ready Studio payloads for 1.1/1.5/1.7/2.1
│   └── prompts/01..06.md     # brand kit / themes / thumbs / motion / priority-10 / Escher bed
├── scripts/
│   ├── publish.sh            # /publish mechanics (gate + diff + push)
│   ├── status_emit.mjs       # writes data/status/publishing.json
│   ├── videos_emit.mjs       # writes data/publishing/videos.json (drives designing/web /videos — see § 10)
│   ├── sync-mirror.sh        # redact one source file into qagents-public/ (thin wrapper)
│   └── sync_mirror.py        # the redaction engine behind sync-mirror.sh
└── .claude/
    ├── settings.json         # allow-list (writes-self + git push-quantapix + read-all)
    ├── settings.local.json   # gitignored
    ├── skills -> ../../.claude/skills
    └── agents/
        └── publish-collector.md   # per-source top-tier-model collector subagent
```

## 9. Messaging-hardening debate (publishing/ convenes)

`publishing/` convenes the recurring **messaging-hardening debate** — a
structured multi-agent pass that makes the public surfaces (quantapix.com,
femfas.net, the GitHub org, the @Quantapix channel) defensible against a cold,
adversarial read. It is **instance one** of the generic debate framework
(`data/specs/debate-framework-2026-06-09/SPEC.md`); its own contract:
`data/specs/messaging-hardening-debate-2026-06-06/SPEC.md` (adopted 2026-06-06).

- **Roles:** `publishing/` convenes; `shorting/` prosecutes (one top-tier-model subagent
  per vector); vector-owner subprojects defend; `managing/` judges; **`pleading/`
  holds a binding litigation-safety veto on every ruling** (spec § 4, § 7 Q1).
- **Lane:** Max-20x interactive, operator-run inside `/open publishing` (mirrors
  `/dco-manual`); the convener starts each round at v0.1. If the debate persists
  past round 1, `managing/`'s daily cron stewards the recurring rounds (framework
  § 6.2 — deferred, details TBD).
- **Round records** land in the shared hub
  `data/debates/messaging-hardening-<date>.md` (tracked; framework § 4, spec-like
  `<slug>-<date>` naming — migrated 2026-06-09 out of the former
  `publishing/debates/<date>/round-NN-rulings.md`). These are **pre-gate triage**
  — per spec § 6 a ruling reaches the promoted digest
  `data/messaging-rulings/<date>.md` **only after `pleading/` returns CLEARED**.
- **Advisory model (§ 7 Q2):** the debate emits rulings; each owning subproject
  applies the public-surface edit in its **own** `/open <sub>` session.
  `publishing/` never mutates a sibling tree (§ 3 boundary posture).
- **Wiring state:** the `data/messaging-rulings/` data-charter registration
  (first CLEARED digest 2026-06-08) and the `pending/*-debate/**` buffer
  registration (`managing/.claude/agents/verifier.md` internal-set +
  `verify-pending.sh`) are both done; rulings apply from a `managing/` session.

## 10. Drives the designing /videos page (data-hub, not shared code)

`publishing/` is the producer-of-record for the @Quantapix video roster, so it
**drives** the `designing/web` `/videos` page the same way `donating/` drives
`/donate` — via a JSON hub, the only seam (no cross-subproject imports, root
CLAUDE.md language split). Third instance of the data-hub-not-shared-code pattern
(after `data/status/` and `data/donating/`).

- **Producer:** `publishing/scripts/videos_emit.mjs` → `data/publishing/videos.json`
  (schema + governance: `data/publishing/CLAUDE.md`). The 5×10 roster (titles +
  profile tags) tracks `explaining/outline.md`; the per-video **release state**
  (status `live`/`upcoming`, `cdnUrl`, `youtubeUrl`, `thumb`) is publishing's own
  state, edited in the emitter. Atomic write; the `.data-write-lock` is held by
  `/close` (matching `status_emit.mjs` / donating's emitter).
- **Consumer:** `designing/web/src/lib/videos-loader.ts` → `src/pages/videos.astro`
  (collapsible chapters + @Quantapix channel hint + featured preview/latest).
  Thumbnails live at `designing/web/public/video-thumbs/<id>.png`.
- **Boundary (§ 3):** the consumer files are `designing/`-owned. publishing
  authors them but **lifts-across** to the `designing` worktree
  (`data/specs/open-close-dcu-2026-05-26/lift-encapsulated-fixes-2026-06-08/SPEC.md` § 6, Mode A) for the
  designing session to verify + commit — publishing never closes carrying a
  sibling tree's hunks. The `data/publishing/*` hub + the emitter stay on the
  publishing branch (allowlisted shared hub, not foreign).
- **Public-key derivation (publishing owns).** The public key publishing
  emits/uploads — `T<topic>/<NN>-<title-slug>.mp4` (long) /
  `T<topic>/<NN>-<short-title-slug>-short.mp4` (short; the `-short` suffix keeps
  long/short collision-free even when titles diverge — debate R-S4) — is
  **derived at publish time from the debate-locked title** (`meta.json` /
  `outline.md`), NOT from `explaining/`'s neutral subject-slug dir path (which
  never appears publicly). Title is metadata, the path slug is an opaque id, so a
  title change never triggers a rename cascade. publishing gates the **derived**
  key, not just the title metadata — the redaction + verb-blocklist sweep scans
  the `cdnUrl` slug too. Mirror + worked example: `explaining/CLAUDE.md`
  § "Publish-key shape".
- **Release flow:** a cut goes live → upload to S3 (`serving/scripts/upload-video.sh
  <cut> T<n>/<slug>.mp4`) + YouTube, then flip `status: 'live'` + fill
  `cdnUrl`/`youtubeUrl` in the emitter and re-run it. A litigation-framed video
  rides the **messaging gate**: the full payload (title + description + tags +
  chapters + thumbnail + the public CDN slug — `cdnUrl` renders on /videos, so a
  blocked verb can't hide in the URL) must `pleading/`-CLEAR as one piece before
  upload. **Site-thumb gotcha:** `designing/web/public/video-thumbs/<id>.png` is a
  SECOND, independently-deployed copy of the `rendering` `priority-10` render —
  clearing the YouTube payload does NOT clear it; it can serve stale/blocked art
  live on `quantapix.com/video-thumbs/<id>.png` (CloudFront-cached) on its own. On
  any framing change refresh BOTH, lift the site thumb across to the designing
  worktree (§ 10 above; it's designing-owned), and **CloudFront-invalidate** the
  thumb path. Close publishing first (videos.json live-flip → main) before
  designing syncs + builds, else /videos shows the new thumb but stale `upcoming`.
