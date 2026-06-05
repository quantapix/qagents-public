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

Authoritative contract: `data/specs/publishing-2026-05-31.md`.

## 2. What it owns / what it does not

**Owns:** the public-org staging tree `publishing/quantapix/` (migrated out of
`data/`); the `/publish` pipeline (sweep → collect → verify/redact → compile →
push); the external push surface `git push-quantapix`; drive Promise 1; the
redaction-clean gate before any push; the **@Quantapix YouTube channel**
material (`publishing/youtube/` — channel-page copy, brand/thumbnail/motion
prompts, upload specs — plus the rendered channel-art bundle at
`data/renders/publishing-design/`), migrated out of `explaining/videos/`
2026-06-02. The split is **channel vs. content**: the channel face (handle,
banner, About, thumbnail system, brand kit, upload specs) is publishing's; the
50-video 5×10 arc itself stays in `explaining/`. The Janet identity master +
voice config stay in `explaining/voice/` (HeyGen narration is `explaining/`'s
job); `youtube/` cites them, does not own them.

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
orchestrator over `scripts/publish.sh` + the Opus collector fan-out). Five
phases: preflight → sweep (Opus fan-out, one `publish-collector` per source
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
(`data/specs/publishing-2026-05-31-tests/tests/t_10_publish_gate.sh`).

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
  `data/specs/canonical-edit-hook-tightening-2026-05-28.md`).
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
§ "Status hub"). Pins `KIT_VERSION = '0.4.2'`. Four-state pill machine: `OK`
(last `/publish` clean) / `BUILDING` (run in flight) / `DEGRADED` (last run
aborted on the redaction/drift gate — privacy floor held, release stale) /
`NOT_YET_LIVE` (pre-first-publish). Summary diagram = the five-stage pipeline;
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
│   ├── LAUNCH-COHORT-RESPEC-2026-06-04.md   # Claude Design rerun hand-off (delivered)
│   ├── LAUNCH-COHORT-UPLOAD-2026-06-06.md   # paste-ready Studio payloads for 1.1/1.5/1.7/2.1
│   └── prompts/01..06.md     # brand kit / themes / thumbs / motion / priority-10 / Escher bed
├── scripts/
│   ├── publish.sh            # /publish mechanics (gate + diff + push)
│   ├── status_emit.mjs       # writes data/status/publishing.json
│   ├── sync-mirror.sh        # redact one source file into qagents-public/ (thin wrapper)
│   └── sync_mirror.py        # the redaction engine behind sync-mirror.sh
└── .claude/
    ├── settings.json         # allow-list (writes-self + git push-quantapix + read-all)
    ├── settings.local.json   # gitignored
    ├── skills -> ../../.claude/skills
    └── agents/
        └── publish-collector.md   # per-source Opus collector subagent
```
