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
prompts, upload specs). The
split is **channel vs. content**: the channel face (handle, banner, About,
thumbnail system, brand kit, upload specs) is publishing's; the 50-video 5×10
arc itself stays in `explaining/`. The Janet identity master + voice config
stay in `explaining/avatar/` + `explaining/voice/` (HeyGen narration is
`explaining/`'s job); `youtube/` cites them, does not own them. The channel
*design sources* (JSX harnesses + canvas bundles) live at
`rendering/designs/publishing-youtube/` and the rendered deliverables at
`data/renders/publishing/` (`data/specs/rendering-2026-06-09/SPEC.md`); request
re-renders via `rendering/scripts/render.sh publishing-youtube`, never a
hand-rolled capture script.

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
the same load-bearing privacy floor `donating/` § 7 names. **Blind spot
(source-scrubbing still required):** the inherited redactor strips STATE
dockets/judges/PII but KEEPS federal dockets (federal *merits* dockets are
publishable), so a surface-specific bar on one collateral federal-docket
family — enumerated in a private ruling, never on a public surface — was NOT
caught by the primary gate; a 2026-07-05 leak into a public weekly/ledger
surface was the proof. `publish.sh` gate **(1b)** now backstops that class
with a targeted content grep, pinned by a companion regression test.
Gate (1b) is token-scoped, not semantic — **still scrub the SOURCE artifact
before `/publish`**; `/publish` is not a safety net for federal-collateral
material a new wording could evade.

**Gate (1b) greps CONTENT; a barred token in a FILENAME evaded it (2026-07-10).**
A path renders publicly (repo tree + blob URL) without appearing in any file's
bytes. The live instance is the auto-memory tree, whose topic files are *named*
after their subject. Closed at the one seat that already walks every path:
`sync_mirror.py` `path_blocklist_hit` **rule (D)**, which back-stops both the
staging tree and `publishing/resume/` via `--scan-tree`, and fails **closed**
(abort, not silent drop). Regression pinned by a companion test. NB a `\b`
word boundary does **not** separate on `_`, so rule (D) uses explicit
alphanumeric boundaries; the `publish.sh` content twin must be swept in
lockstep if a `_`-delimited body token ever matters.

**Memory-slice ruling (2026-07-10).** Drive Promise 1 advertises a weekly
redacted mirror of `~/.claude/.../memory/`. It has **never been populated** —
`qagents-public/memory/` holds only its README, and `sync_mirror.py` has no
memory roster (the sweep is documented, never wired). So the 2026-07-10
donating hint's dichotomy ("gate 1b is blocking, or these are live leak
candidates") resolves to **neither**. 27 private memory files carry the barred
family; 4 carry it in the filename. Ruling: **exclusion, not redaction** — an
entry whose *subject* is the bar cannot be scrubbed of it and stay useful. When
the roster is authored it MUST be a curated **allow-list** (opt-in), never a
deny-sweep; rule (D) + gate (1b) make the pipeline fail-closed either way. The
public README no longer claims a mirror that does not exist. And `sync` only *masks* an already-published
leak (a superseding commit); the barred blobs survive in public git history until
a **history rewrite + force-push** (orphan-reset when 0 forks/PRs) purges them —
the GitHub analog of the S3-wipe. The gate is wired before the push and pinned by
the companion test
(`data/specs/publishing-2026-05-31/tests/cases/t_10_publish_gate.sh`).

**The candidate tree is markdown, so the gate scans markdown.**
`publishing/scripts/sync_mirror.py` Stage 3 applies the blocklist patterns as
it renders each CLAUDE.md / memory mirror. `publish.sh` runs
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

**`gh` does all GitHub work (2026-06-23).** `scripts/github_meta.py` is the single
gh-centric arm: `sync` (content — `gh repo clone` → `rsync -aL` → commit →
`git push` over gh's HTTPS credential helper; `SYNC_ROSTER` source map incl.
`resume`; excludes `.git`/`CLAUDE.md`/`github-metadata.json`; org-profile
top-level-only), `ensure` (existence), `apply` (metadata `gh repo edit`), `verify`.
Repo description/homepage/topics are thesis-governed in `quantapix/github-metadata.json`
— a `description` IS the GitHub OG card (strips its disclaimer), so it rides the
SAME gate as README prose (`github_meta.py scan` = `sync_mirror` blocklist +
`THESIS_LINT`, wired into `publish.sh` Phase 2c). `apply` mutates a public surface
→ operator-confirmed + pleading-gated (manifest `_status`). NB `cmd_apply` never
reads `_status` (procedural/bookkeeping gate only — a real apply carries the flip
same-session); metadata `apply` is cleanly separable from content `sync` (the
Friday `/publish` push). The gate persists for future string changes — re-clear,
flip `_status` back to DRAFT. The legacy `git push-quantapix` bridge is superseded
for the `/publish` path (still exists for manual use — `serving/CLAUDE.md` § 9).
Program: the Quantapix-Thesis-on-GitHub spec
(`data/specs/publishing-2026-05-31/quantapix-thesis-github-2026-06-23/SPEC.md`).

**FINANCIALLY-CLEARED (financial sign-off, 2026-06-24).** `evaluating/` is the
sole grantor (advised by `accounting/`) of the financial-advice/securities gate —
the financial-domain analog of `pleading/`'s litigation gate, **orthogonal** to it
(where both apply, both clears are required). It is the blocking condition for
`qresev-public` (content push **and** `gh repo edit` metadata `apply`) and any
Qresev YouTube payload. `github_meta.py`'s `description`-strip thesis-floor lint is
the cross-repo half of the § 4 byte-equality check. Spec:
`data/specs/evaluating-financial-signoff-2026-06-24/SPEC.md`.

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
├── CLAUDE.md / README.md / PLAN.md
├── .publish-state            # tracked one-line pill state (§ 7)
├── .worktree-links           # inbox + resume/*.pdf (canonical-backed, gitignored)
├── quantapix/                # public-org staging tree (see quantapix/CLAUDE.md)
├── youtube/                  # @Quantapix channel material — index: youtube/README.md
├── resume/                   # github.com/quantapix/resume source (README.md + resume.html)
├── inbox/                    # gitignored private receipt/usage PDFs (never published)
├── pending/messaging-debate/ # pre-gate debate staging (§ 9)
├── scripts/                  # publish.sh · github_meta.py · iga_verify.py
│                             # sync_mirror.py/sync-mirror.sh · status_emit.mjs · videos_emit.mjs
│                             # youtube_{auth,upload,sync,manifest}.py
└── .claude/                  # settings + skills symlink + publish-collector agent
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
- **Release flow (gate-first; no step until the prior clears).** The **CDN upload
  is the FIRST public push** — the S3 object is fetchable at
  `videos.quantapix.com/<key>` the instant it lands (immutable cache), reachable by
  URL even before it is linked from /videos. So it is gated **identically to the
  YouTube upload**, NOT a pre-gate "build" step. The mistake to never repeat:
  uploading the cut to S3 before the payload clears (4.1, 2026-06-30 — the chain
  pushed the CDN object ahead of `evaluating/`'s sign-off). Order:
  1. **Master finalized** (explaining) + thumbnail rendered.
  2. **Applicable gate(s) CLEAR on the full payload** — title + description + tags +
     chapters + thumbnail + the **derived public CDN slug** (the slug renders on
     /videos *and* is publicly reachable, so a blocked verb can't hide in the URL) —
     as ONE piece, **before any public push** (CDN upload included):
     a **financial-domain** video (Topic 3 / Topic 4 / any Qresev payload) needs
     `evaluating/` **FINANCIALLY-CLEARED** (sole grantor, `accounting/` advises — § 5);
     a **litigation-framed** video needs `pleading/` messaging CLEAR; where both
     apply, **both** are required. Cite each attestation in the manifest entry's
     `signoffs{}` map (keyed by registry gate-id — `signoffs["FINANCIALLY"]` /
     `signoffs["MESSAGING"]` → the record-path; signoff-framework § 7) **and** the
     release commit (`Signed-off-by-gate: <gate>=<record>`). The pre-migration
     free-text form (4.2's "evaluating-cleared" commit cite) is superseded by the
     map — `youtube_sync.py`/`youtube_upload.py` `signoff_blocker()` machine-refuses
     a push whose in-scope gate lacks an on-disk record.
  3. **Publishing mints the key**, stages `descriptions/<key>.txt` + the manifest
     entry (`youtubeId: null` = built-not-uploaded); redaction/verb sweep clean.
  4. **CDN upload** (`serving/scripts/upload-video.sh <cut> T<n>/<slug>.mp4`) — the
     first public push, gated by step 2.
  5. **YouTube upload** (unlisted-first) → Studio altered-content toggle → public flip.
  6. **Live-flip:** `videos_emit.mjs` `status: 'live'` + fill `cdnUrl`/`youtubeUrl`,
     re-run; `explaining/` records the release in `meta.json` (the § 4 standing rule
     there — explaining-owned, never publishing).

  **Site-thumb gotcha:** `designing/web/public/video-thumbs/<id>.png` is a
  SECOND, independently-deployed copy of the `rendering` `priority-10` render —
  clearing the YouTube payload does NOT clear it; it can serve stale/blocked art
  live on `quantapix.com/video-thumbs/<id>.png` (CloudFront-cached) on its own. On
  any framing change refresh BOTH, lift the site thumb across to the designing
  worktree (§ 10 above; it's designing-owned), and **CloudFront-invalidate** the
  thumb path. Close publishing first (videos.json live-flip → main) before
  designing syncs + builds, else /videos shows the new thumb but stale `upcoming`.

## 11. The `/youtube-sync` pipeline (channel ↔ repo)

Sibling of `/publish`: `/publish` pushes the GitHub org, `/youtube-sync` pushes the
@Quantapix channel. SoT is `data/publishing/youtube-manifest.json` + per-video
`publishing/youtube/descriptions/<key>.txt` — metadata is edited in the repo, never
in Studio; `youtube_sync.py` diffs and `videos.update`s drift. Skill:
`.claude/skills/youtube-sync/SKILL.md`; engine + uploader + shared auth:
`publishing/scripts/youtube_{sync,upload,auth}.py`; deps in the root `[publishing]`
extra; OAuth one-time per `youtube/API-UPLOAD-SETUP.md`.

- **Two hard gates.** (1) **Signoff gates** (signoff-framework § 7): each entry's
  scope flags (`litigationFramed` → MESSAGING, `financialDomain` → FINANCIALLY) put
  it in a gate's scope, and `signoff_blocker()` refuses push/adopt-over/upload unless
  every in-scope gate's `signoffs[<gate-id>]` names a record on disk — a promoted
  `data/messaging-rulings/<date>.md` (pleading grants) or an
  `evaluating-financial-signoff/signoffs/` record (evaluating grants, accounting
  advises). publishing never self-grants. (4.2's FINANCIALLY record landed
  2026-07-04 and it is live; the currently blocked slot is **3.6** — financial
  scope, first-grant owed.) The MESSAGING half is the same § 11.2 floor the upload
  sheets ride. The old single `clearedBy`/inert `financiallyCleared` fields are
  retired (R17 atomic-lockstep migration, 2026-06-30). **IGA enforcement (R7, landed
  2026-07-03):** when a cited record is an inline-operator grant (`granted_via:
  inline-operator`, publishing SPEC § 5.5), `signoff_blocker()` additionally runs
  `iga_verify.py` — committed-blob re-verify against the push commit (`git rev-parse
  <push-commit>:<path>`, never the worktree), `grantor == registry sole-grantor`, and a
  cron/SDK-lane refuse. Ceremony records (all shipped to date) + MESSAGING are a strict
  no-op. Also swept in `publish.sh` over each prose-lifted gate's `LEDGER.md`. Test
  `t_16_iga_enforcement.sh` (15). Owed: `github_meta.py` repo-content binding (needs the
  evaluating-owned FINANCIALLY `LEDGER.md`, R1) + serving `upload-video.sh` sha emit.
  (2) The synthetic-content
  **altered-content disclosure has no API field** — it stays a manual Studio toggle
  per upload (`CHANNEL-INFO.md` § 9); an API upload is never compliance-complete on
  its own. A redaction/verb scan over `descriptions/` runs before any push.
- **Banner ↔ channel-info land together.** The live @Quantapix banner is a rendering deliverable (`render.sh publishing-youtube/channel-art-v2`); when its baked copy changes (e.g. a thesis cure), the live re-upload AND the matching `youtube/CHANNEL-INFO.md` (E1) wording are both publishing-owned and must land same-PR so banner + channel-info agree character-for-character.
- **First run = `--mode adopt`** (baselines the SoT from live so the diff is real),
  then `check` → resolve → `push`; `--mode stats` writes
  `data/publishing/youtube-stats.json`. `youtube_sync` does NOT touch `videos.json`
  — the /videos live-flip stays the `videos_emit.mjs` edit (§ 10).
