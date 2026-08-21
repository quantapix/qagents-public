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

Authoritative contract family: `data/specs/publishing-2026-05-31/`.

## 2. What it owns / what it does not

**Owns:** the public-org staging tree `publishing/quantapix/` (migrated out of
`data/`); the `/publish` pipeline (sweep → collect → verify/redact → compile →
push); the external push surface `git push-quantapix`; drive Promise 1; the
redaction-clean gate before any push; the **@Quantapix YouTube channel**
material (`publishing/youtube/` — channel-page copy, brand/thumbnail/motion
prompts, upload specs). The channel-vs-content split (channel face here, the
50-video 5×10 arc in `explaining/`) is owned by `publishing/youtube/README.md`
§ Scope. The Janet identity master + voice config
stay in `explaining/avatar/` + `explaining/voice/` (HeyGen narration is
`explaining/`'s job); `youtube/` cites them, does not own them. The channel
*design sources* (JSX harnesses + canvas bundles) live at
`rendering/designs/publishing-youtube/` and the rendered deliverables at
`data/renders/publishing/`; request
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
→ push (operator-confirmed). Mechanics: the skill + `publish.sh`; staging layout
+ source mapping: `publishing/quantapix/CLAUDE.md`.

No cron lane — the drive cadence (weekly Fridays) is operator-run via
`/open publishing` → `/publish`; a cron lane stays documented-future.

## 5. Redaction is a hard gate, not advisory

A HARD blocklist hit (the private-address family + the SOFT opposing-party /
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

**Gate roster summary.** Gates **(1b)**/**(1c)**/**(1d)**/**(1e)** in `publish.sh`
are fail-closed CONTENT greps (collateral-docket family / cmux + herdr local state /
any contact email — sole public contact `https://github.com/quantapix`,
`resume/` exempt / **rooted internal paths**); rules **(D)**/**(D2)**/**(E)**/**(E2)**
in `sync_mirror.py` `path_blocklist_hit` are their PATH twins (a filename renders
publicly without appearing in any file's bytes); each gate ships a pinned test
(`t_17`–`t_21`).

**Gate (1e) — the SCOPE is the guard (2026-08-14).** A string shaped
`<subproject>/…` names the private tree's internal layout; it is invisible to the
primary sweep, whose HARD set matches docket/party/address/contact TOKENS and
whose Stage-2 path scrubbing strips only ABSOLUTE paths and runs only over
RENDERED mirrors — so a hand-authored README is read and has nothing to match.
**A blanket rooted-path bar would abort every push.** Two narrowings, both
load-bearing and both derived by measuring the tree: PATH scope excludes
`qagents-public/claude-md/` (21 files carry rooted paths as the *payload* —
publishing the CLAUDE.md graph IS publishing the structure) and
`github-metadata.json` (the bridge already `--exclude`s it, so gate scope now
equals push scope); REGEX scope is anchored on the subproject names plus the
`legal/` + `financial/` hubs, never "any rooted path", because `data/`, `code/`,
`lib/` and `hub/` paths are published on purpose in `skills/` and
`GOOD-FIRST-ISSUES.md`. `t_21` asserts both narrowings as behaviour **and
carries an anti-vacuity arm** — it reds if the excluded subtree stops matching,
since a mirror relocation would otherwise silently widen the blind spot into a
total-abort while the test still passed. The gate is **case-sensitive**: the
public kernel form `Proving/<Framework>/` survives only for that reason, and
APFS hides the difference locally (`feedback_case_insensitive_path_collision`).
Consequence to keep in view: the `claude-md/` exclusion means that subtree is
un-gated for this class **by construction** — `claude-md/proving.md` was
publishing the textual axis's barred golden-roster file by name, together with
the bar's rationale, and the only lever that reaches inside the subtree is a
`REWRITES` rule or a source-side edit. CURED 2026-08-21 by six `REWRITES` rules
plus a Stage-1b `OUTPUT_BARS` assertion inside `sync_mirror.py` `redact()` that
hard-exits when a rendered mirror still carries the token — because the rules
alone are vacuous against a NEW unruled sentence, which is exactly how three
fresh pointers appeared in one week. **Name the bar here, never the file:** this
file is itself published as `claude-md/publishing.md`, so a mention here ships
too, and `OUTPUT_BARS` now covers this source for that reason.

**A blocklist gate is necessary and never sufficient.** Every gate here is
token-scoped, not semantic, and that cuts two ways. Against *barred* content it
means a new wording evades the bar — so **still scrub the SOURCE artifact before
`/publish`** rather than trusting the gate. Against *false* content it means no
gate applies at all: the 2026-08-14 run found four falsifiable claims live on
public surfaces, all **true when written**, all falsified later by private-tree
work, all clean under every gate on every prior run. That class needs the
artifact tested against the *world*, which is what `ns:publishing/57`'s post-push
cold read is for; until it exists, `/publish` has no mechanical defence against a
page that is well-formed, un-barred, and no longer true.
Commit **metadata** stays outside every content gate
(`feedback_gate_covers_payload_not_envelope`) — closed for the one live producer
2026-07-31: `github_meta.py` commits with an explicit noreply identity override,
pinned by `t_20_sync_commit_identity.sh`.
Per-incident gate forensics + the token/exclusion rulings live in a committed,
**never-published** forensics file — path rule (C2) fail-closes any staged tree
carrying it. Its NAME is deliberately not written here: C2 bars the file from a
staged tree, not a mention of it inside another file's bytes, and this file is
published (`feedback_gate_covers_payload_not_envelope`).

**Four rules for any source→artifact seam** — mechanism-over-instruction ·
assert on the OUTPUT never the source · never spell a delimiter inside the
region it delimits · normalize whitespace before asserting on extracted
PDF/DOM text. This lane has the same exposure wherever internal material
shares a file with shipped material (every source subproject → public repo).
Derivation + the reusable fail-closed implementation:
`feedback_strip_instruction_is_not_a_mechanism` (siblings
`feedback_gate_covers_payload_not_envelope`, `feedback_gate_before_any_public_push`).

**A text-layer check cannot see the page.** The redaction lane's content scans
(`sync_mirror.py` HARD_PATTERNS, the staged-tree gates) read text — blind both to
what a rasterized page *shows* and to glyphs in the text layer that never render
inside the page box (a 9-for-9 pymupdf pass once cleared a filing whose caption was
clipping at the page edge). The converse — visually hidden but extractable — is
`feedback_graphical_redaction_failure_modes`; **neither check sees the other's
case.** Raster and look, or state explicitly that the gate covers text only.

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
gh-centric arm — `sync` (content) / `ensure` (existence) / `apply` (metadata
`gh repo edit`) / `verify`; sync mechanics + `SYNC_ROSTER` source map +
legacy-bridge supersession: `publishing/quantapix/CLAUDE.md` § 7. Repo
description/homepage/topics are thesis-governed in `quantapix/github-metadata.json`
— a `description` IS the GitHub OG card (strips its disclaimer), so it rides the
SAME gate as README prose (`github_meta.py scan` = `sync_mirror` blocklist +
`THESIS_LINT`, wired into `publish.sh` Phase 2c). `apply` mutates a public surface
→ operator-confirmed + pleading-gated (manifest `_status`). NB `cmd_apply` never
reads `_status` (procedural/bookkeeping gate only — a real apply carries the flip
same-session); metadata `apply` is cleanly separable from content `sync` (the
Friday `/publish` push). The gate persists for future string changes — re-clear,
flip `_status` back to DRAFT. Program family (gate-decision records):
`data/specs/publishing-2026-05-31/quantapix-thesis-github-2026-06-23/`.

**FINANCIALLY-CLEARED (financial sign-off, 2026-06-24).** `evaluating/` is the
sole grantor (advised by `accounting/`) of the financial-advice/securities gate —
the financial-domain analog of `pleading/`'s litigation gate, **orthogonal** to it
(where both apply, both clears are required). It is the blocking condition for
`qresev-public` (content push **and** `gh repo edit` metadata `apply`) and any
Qresev YouTube payload. `github_meta.py`'s `description`-strip thesis-floor lint is
the cross-repo half of the rider byte-equality check. Gate registry:
`.claude/skills/do-signoff/registry.tsv` (FINANCIALLY row); floor detail:
`evaluating/CLAUDE.md` §§ 4, 9.

## 6. Write-lock & session model

- **Branch-as-lock.** `/open publishing` creates branch `publishing` + worktree
  `<root>-wt/publishing/`. Every Edit/Write `file_path` begins
  with that worktree root (canonical-edit hook,
  `data/charters/qagents/session-lifecycle/CHARTER.md` § 2.3).
- **`data/status/publishing.json`** is written by `scripts/status_emit.mjs`, a
  fixed-path producer under `data/` — it acquires `.data-write-lock` per the
  universal manual-writer rule (root CLAUDE.md § "Shared-data write-lock") when
  writing canonical.
- **The external push** (`git push-quantapix`) is not a qagents-repo write — no
  qagents lock involved; its scratch clones live outside the tree.
- **`pending/publish-digests/`** is a gitignored, fork-internal buffer (mirrors
  `pending/dco-digests/`) — **at the worktree ROOT only**. Root `.gitignore`
  anchors `/pending/` plus `**/pending/tmp/`, so a collector resolving its output
  against the SUBPROJECT dir lands in a **tracked** path; closed at the mechanism
  (`publishing/.gitignore` now carries `pending/`), not by instructing collectors
  harder — and `.gitignore` never untracks what is already tracked
  (`ns:publishing/62`). It is **never** promoted by managing's verifier
  (registered in the verifier internal-set + `verify-pending.sh`'s
  `require_not_internal_pattern` deny-list). Discarded at close by default —
  but it is **not** in the close rescue-scan skip set, so every `/publish`
  session hits `--pre` exit 15 on these files. That refusal is worth one
  deliberate pass, not a reflex delete: a digest's section (a) carries findings
  the run did not apply (deferred enrichment, cross-subproject owed fixes), and
  those are lost with the file. Extract them into the close summary or a
  next-step **first**, then delete.

## 7. Status emit (`data/status/publishing.json`)

`scripts/status_emit.mjs` participates in the status contract (root CLAUDE.md
§ "Status hub"; KIT_VERSION lockstep + the widening closed `SubprojectId` set:
memory `project_diagram_kit`). It pins `KIT_VERSION` — read the constant in the
emitter, never a restatement. Four-state pill machine: `OK`
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
adversarial read. **Instance one** of the generic debate framework
(`data/charters/qagents/debate/CHARTER.md` — owns staffing, record naming, lane);
family `data/specs/messaging-hardening-debate-2026-06-06/`; gate standard
`data/charters/pleading/messaging-gate/litigation-safety-standard.md`.

- **Roles:** `publishing/` convenes; `shorting/` prosecutes (one top-tier-model
  subagent per vector); vector-owner subprojects defend; `managing/` judges;
  **`pleading/` holds a binding litigation-safety veto on every ruling**.
- **Lane:** Max-20x interactive, operator-run inside `/open publishing` (mirrors
  `/dco-manual`); the convener starts each round at v0.1. Recurring-round
  stewardship by `managing/`'s daily cron is deferred (debate charter § 2.7).
- **Round records** land at `data/debates/messaging-hardening-<date>.md` (tracked)
  and are **pre-gate triage** — a ruling reaches the promoted digest
  `data/messaging-rulings/<date>.md` **only after `pleading/` returns CLEARED**.
- **Advisory model:** the debate emits rulings; each owning subproject applies the
  public-surface edit in its **own** `/open <sub>` session. `publishing/` never
  mutates a sibling tree (§ 3 boundary posture).

## 10. Drives the designing /videos page (data-hub, not shared code)

`publishing/` is the producer-of-record for the @Quantapix video roster, so it
**drives** the `designing/web` `/videos` page the same way `donating/` drives
`/donate` — via a JSON hub, the only seam (no cross-subproject imports, root
CLAUDE.md language split).

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
  (`data/specs/open-close-dcu-2026-05-26/lift-encapsulated-fixes-2026-06-08/`, Mode A) for the
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
  the `cdnUrl` slug too. Source MP4s stay laptop-local (`explaining/videos/<slug>/cuts/`,
  gitignored) — the CDN object is the only durable public copy; cross-site
  contract `serving/CLAUDE.md` § 8. Mirror + worked example: `explaining/CLAUDE.md`
  § "Publish-key shape".
- **Release flow (gate-first).** Floor (always-loaded): **no public push before
  the applicable gate(s) CLEAR on the full payload as ONE piece** (title +
  description + tags + chapters + thumbnail + derived public CDN slug) — the
  **CDN upload is the FIRST public push**, gated identically to the YouTube
  upload, NOT a pre-gate "build" step (4.1 regression, 2026-06-30). Six-step
  recipe + the site-thumb second-copy/CloudFront-invalidation gotcha:
  `.claude/skills/youtube-sync/SKILL.md` § "Release flow".

## 11. The `/youtube-sync` pipeline (channel ↔ repo)

Sibling of `/publish`: `/publish` pushes the GitHub org, `/youtube-sync` pushes the
@Quantapix channel. SoT is `data/publishing/youtube-manifest.json` + per-video
`publishing/youtube/descriptions/<key>.txt` — metadata is edited in the repo, never
in Studio; `youtube_sync.py` diffs and `videos.update`s drift. Skill:
`.claude/skills/youtube-sync/SKILL.md`; engine + uploader + shared auth:
`publishing/scripts/youtube_{sync,upload,auth}.py`; deps in the root `[publishing]`
extra; OAuth one-time per `youtube/API-UPLOAD-SETUP.md`.

- **Two hard gates.** (1) **Signoff gates** (signoff-framework § 7): an entry's scope is
  the **R2 union — committed class floor ∪ per-entry flags** (`in_scope_gates()`, 2026-07-24).
  The floor comes from `data/publishing/r2-scope-map.json` keyed by the **topic prefix** of
  the manifest `key` (`T3`/`T4` → FINANCIALLY today), which is structurally mandatory in
  every catalog key and so cannot be forgotten (a ROOT-LEVEL ledger key — a non-episode
  cdn asset — derives its literal filename as its class and is registered PER-ASSET with
  an explicitly stated floor, since the push ledger covers every cdn push, not only
  episodes; 2026-07-31); the flags (`litigationFramed` → MESSAGING,
  `financialDomain` → FINANCIALLY) survive as **additive-only** widenings that may never
  narrow below the floor. An **unregistered class fails closed** (refuses the push) — a
  gate that defaulted an unknown topic to ungated would reintroduce the R2 vacuity attack.
  publishing PRODUCES that artifact and consumes it here; studying's Lean extractor is the
  other reader (`load_scope_map`, R9: only prose-lifted gates may be scope-mapped, so
  MESSAGING never appears in it). No cross-subproject import — both sides validate the same
  committed JSON independently. `signoff_blocker()` then refuses push/adopt-over/upload unless
  every in-scope gate's `signoffs[<gate-id>]` names a record on disk — a promoted
  `data/messaging-rulings/<date>.md` (pleading grants) or an
  `data/signoffs/FINANCIALLY/` record (relocated 2026-07-30; evaluating grants, accounting
  advises). publishing never self-grants. The MESSAGING half is the same § 11.2 floor the upload
  sheets ride. The old single `clearedBy`/inert `financiallyCleared` fields are
  retired (R17 atomic-lockstep migration, 2026-06-30). **IGA enforcement (R7):** inline-operator
  grants get `iga_verify.py`'s three refuse checks — contract, wiring, test:
  spec § 5.5. Owed: `github_meta.py` repo-content binding (needs the
  evaluating-owned FINANCIALLY `LEDGER.md`, R1). (2) The synthetic-content
  **altered-content disclosure has no API field** — it stays a manual Studio toggle
  per upload (`CHANNEL-INFO.md` § 9); an API upload is never compliance-complete on
  its own. A redaction/verb scan over `descriptions/` runs before any push.
- **Banner ↔ channel-info land together.** The live @Quantapix banner is a rendering deliverable (`render.sh publishing-youtube/channel-art-v2`); when its baked copy changes (e.g. a thesis cure), the live re-upload AND the matching `youtube/CHANNEL-INFO.md` (E1) wording are both publishing-owned and must land same-PR so banner + channel-info agree character-for-character.
- **First run = `--mode adopt`** (baselines the SoT from live so the diff is real),
  then `check` → resolve → `push`; `--mode stats` writes
  `data/publishing/youtube-stats.json`. `youtube_sync` does NOT touch `videos.json`
  — the /videos live-flip stays the `videos_emit.mjs` edit (§ 10).
- **CDN release gate (`CLEARANCE_COMMIT`).** `serving/scripts/upload-video.sh` refuses
  any `T<n>/` catalog key unless the caller sets `CLEARANCE_COMMIT` — the
  FINANCIALLY-CLEARED record's `granting_commit`. **The gate ENFORCES THE RECORD**
  (`ns:serving/82` landed; this bullet's former "an ANCESTRY check, not a record
  lookup" wording is false, and understating a gate is the dangerous direction — it
  invites treating clearance as ceremonial). Verified 2026-08-14: the commit must
  resolve, must equal the `granting_commit` of a record whose disposition is
  `CLEARED*` under the gate's registry-resolved `record-location` (missing registry ⇒
  refuse outright, never fall back to bare ancestry; disposition read in the same pass,
  so a BLOCKED record's commit can never release), and only then be an ancestor of
  HEAD. So the `verified-N/A` FINANCIALLY grant for a non-financial episode is
  **mechanically required**, not merely good practice.
  **What the ancestry-only era cost, which is still true and still load-bearing:**
  measured 2026-08-07 against `data/publishing/push-ledger.jsonl`, **4 of the 5 pushed
  T1/T2 episodes carried no FINANCIALLY record and shipped anyway**
  (`T1/01-hallucination-tax`, `T1/05-negative-verification`,
  `T1/07-civil-rico-walkthrough`, `T2/01-docket-record-disagree`; only
  `T1/02-semantic-search-limits` has one). Those four are **permanently uncovered** — the
  hardening is prospective and back-filling a grant would violate
  gate-before-first-push. Read that as history, never as what the gate allows today.
  ⚠ This paragraph has now been wrong in **both** directions across three corrections, so
  the standing advice is the one evaluating adopted: **read the script, not this
  paragraph.**
  Authoritative contract family: `data/specs/serving-2026-05-26/`
  (serving owns the script + the gate); this bullet is the
  publishing-side pointer the script's error message cites.
