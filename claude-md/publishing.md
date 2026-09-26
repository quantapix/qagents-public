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
push); the external push surface; drive Promise 1; the
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
CLAUDE.md graph. Outbound is the public GitHub org only (§ 5 — `gh`-driven).

`publishing/` is **not observe-only** (unlike `managing/`/`shorting/`): it writes
its own subtree and pushes to the external org. But it **never** commits/pushes
the *qagents* repo outside `scripts/close.sh` (the interactive-lane audit gate),
and **never** mutates any sibling subproject's tree.

## 4. The `/publish` pipeline

Triggered by the `/publish` skill (`.claude/skills/publish/SKILL.md`, a thin
orchestrator over `scripts/publish.sh` + the collector fan-out). Five phases:
preflight → sweep (one `publish-collector` per source subproject) → verify/redact
(HARD gate) → compile → push (operator-confirmed). Mechanics: the skill +
`publish.sh`; staging layout + source mapping: `publishing/quantapix/CLAUDE.md`.

No cron lane — the drive cadence (weekly Fridays) is operator-run via
`/open publishing` → `/publish`; a cron lane stays documented-future.

## 5. Redaction is a hard gate, not advisory

A blocklist hit (the private-address family + the opposing-party / counsel /
docket / agency-PII set) anywhere in the candidate tree **aborts**
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
(`t_17`–`t_21`). A third kind sits INSIDE the renderer: `sync_mirror.py`
`OUTPUT_BARS` (Stage 1b, asserted in `redact()`, pinned by `t_22`) refuses to
emit a mirror still carrying a per-source barred token — the only lever that
reaches the gate-(1e)-excluded `claude-md/` subtree, and the only one that sees a
token arriving in a sentence no `REWRITES` rule was written for. Its CLASS-wide
sibling `LIVE_MATTER_BARS` (Stage 1c, `t_26`, 2026-09-18) refuses live-matter
SHORT forms in any published CLAUDE.md — every other gate reads NAMES, so a
green suite over `claude-md/` was a statement about names, not about matter; a
lane over live matter publishes by SHAPE, its state in an unpublished sibling.

**Two arms landed 2026-09-15 (Round 05 L-B1/L-B2, `ns:publishing/77`+`/78`).**
(i) The content sweep reads the ONE admitted `.lean` location as well as `*.md`,
and the path rule bars a live-matter example id in the path — each catches a
case the other structurally cannot. `t_23`. (ii) Stage 2's prefix rules scrub
the BARE form for the private-hub family and KEEP it for the subproject /
public-hub names; the keep set is declared, so an unconsidered new prefix
defaults private (`sync_mirror.py --check-path-subs`, both polarities, `t_24`).
**Only a two-polarity test can say a cure went too far.** The collateral-docket
bar also gained a generic form arm, still narrow to that family. Measurements:
`project_publishing_subproject` (2026-09-15).

**Gate (1e) — the SCOPE is the guard (2026-08-14).** Two measured narrowings
(PATH scope excludes `claude-md/` + `github-metadata.json`; REGEX scope is
anchored on subproject + hub names, never "any rooted path"), asserted as
behaviour with an anti-vacuity arm by `t_21`. Full derivation, the
case-sensitivity carve, and the excluded-subtree consequence are recorded in
the never-published forensics file described later in this § — read its
gate-(1e) section before editing the gate's PATH/REGEX scope or `t_21`.
**Standing rule, and it
binds EVERY source in `sync_mirror.py`'s `PUBLISHED_CLAUDE_MD` roster, not just
this file: describe a restriction, never name the restricted file** — the mirror
ships whatever the source says, and documenting a bar is exactly the context in
which a barred file gets named. A source that acquires such a mention needs its
own `OUTPUT_BARS` key: keying the bar to one source made it a guard narrower
than its grant (2026-08-21), and a REWRITES rule alone is silent against a NEW
unruled sentence. A third source was keyed 2026-09-15 (`ns:publishing/78`) after
its claim rode at least three pushes unseen — the 2026-08-21 widening had added
the one source that had been CAUGHT, not the class, which is the same defect one
level up. **When the bar protects a person rather than a file, bar the COUPLING
and not the name**: a deliberately public name must SURVIVE the render, so the
pinning test (`t_25`) asserts both directions and an over-broad cure reds.

**A mirror-side cure is a SUBSCRIPTION, not a fix.** When the form is minted by a
rule living in a *source* subproject, the cost recurs on every re-mirror and the
first uncaught wording aborts that week's push. **When the collector cures the
same class twice, the finding belongs at the SOURCE owner's slot, not here**
(measured 2026-08-14, routed `ns:donating/19`). Scope it to HAND-AUTHORED PUBLIC
surfaces: an INTERNAL record legitimately names the code it reports on,
translating path→name is the `publish-collector`'s job, and (1e) is the
fail-closed backstop — **never file rooted paths in a source subproject's
internal records as that subproject's defect**; escalate only where the
collector CANNOT translate. What IS owed at source: no live artifact may
*instruct* a future author to use the barred form — **when a publish bar
changes, sweep the EXAMPLES in every authoring template, not just the prose
stating the rule** (a boilerplate HEADER repeated across a series is the same
class, cured from the template forward). Worked case (117 source vs 0 mirror,
the back-catalogue rider, both minting engines): `donating/CLAUDE.md` § 3.

**A blocklist gate is necessary and never sufficient.** Every gate here is
token-scoped, not semantic, and that cuts two ways. Against *barred* content a
new wording evades the bar — so **still scrub the SOURCE artifact before
`/publish`**. Against *false* content no gate applies at all: the recurring
class is a claim **true when written**, falsified later by private-tree work,
clean under every gate on every prior run. It needs the artifact tested against
the *world* — `ns:publishing/57`'s post-push cold read (population re-measured
per run, never a pinned count); first arm `scripts/cold_read.sh` +
`cold-read-claims.tsv` (2026-09-15), semantic rows still hand reads.
Commit **metadata** stays outside every content gate
(`feedback_gate_covers_payload_not_envelope`) — closed for `github_meta.py`
2026-07-31 (explicit noreply identity override, `t_20`).
Per-incident gate forensics + the token/exclusion rulings live in a committed,
**never-published** forensics file — path rule (C2) fail-closes any staged tree
carrying it; its NAME is withheld here under the standing rule above.

**Four rules for any source→artifact seam** — mechanism-over-instruction ·
assert on the OUTPUT never the source · never spell a delimiter inside the
region it delimits · normalize whitespace before asserting on extracted
PDF/DOM text. This lane has the same exposure wherever internal material
shares a file with shipped material (every source subproject → public repo).
Derivation + the reusable fail-closed implementation:
`feedback_strip_instruction_is_not_a_mechanism` (siblings
`feedback_gate_covers_payload_not_envelope`, `feedback_gate_before_any_public_push`).

**A text-layer check cannot see the page.** The content scans read text — blind
to what a rasterized page *shows* and to text-layer glyphs that never render in
the page box (a 9-for-9 pymupdf pass once cleared a filing clipping at the page
edge); the converse is `feedback_graphical_redaction_failure_modes`. **Neither
check sees the other's case** — raster and look, or state the gate covers text
only.

**The candidate tree is markdown, so the gate scans markdown.**
`publishing/scripts/sync_mirror.py` Stage 3 applies the blocklist patterns as
it renders each CLAUDE.md / memory mirror. `publish.sh` runs
`sync_mirror.py --scan-tree <tree>` as the PRIMARY gate — a HARD-only sweep
(the markdown gate's SOFT class is empty: every pattern aborts) over **every `*.md`** under the candidate tree (the hand-authored READMEs,
`STATUS.md` files, and the `skills/` subtree included), and it *refuses to pass
over an empty tree*. It skips `CLAUDE.md`-named files (staging governance — not
pushed; `github_meta.py sync` excludes them) and carves out the
developer's own public name via `sync_mirror.py` `ALLOW_PHRASES` while keeping
the litigation linkage HARD-blocked. The `check_redactions.py --tree` PDF gate
stays wired after it as defense-in-depth (stray `*.pdf`). The resume tree
(`publishing/resume/`) is gated by the same sweep. Gate-before-push ordering is
pinned by `t_10_publish_gate.sh`.

**`gh` does all GitHub work (2026-06-23).** `scripts/github_meta.py` is the single
gh-centric arm — `sync` / `ensure` / `apply` (metadata `gh repo edit`) /
`verify`. A repo `description` IS the GitHub OG card (strips its disclaimer), so
it rides the SAME gate as README prose (`github_meta.py scan` = `sync_mirror`
blocklist + `THESIS_LINT`, `publish.sh` Phase 2c). `apply` mutates a public
surface → operator-confirmed + pleading-gated. Sync mechanics, `SYNC_ROSTER`, the
`_status` gate: `publishing/quantapix/CLAUDE.md` § 7; gate-decision records:
`data/specs/publishing-2026-05-31/quantapix-thesis-github-2026-06-23/`.

**FINANCIALLY-CLEARED (2026-06-24).** `evaluating/` is the sole grantor (advised
by `accounting/`), **orthogonal** to `pleading/`'s litigation gate — where both
apply, both clears are required. It blocks `qresev-public` (content push **and**
metadata `apply`) and any Qresev YouTube payload. `github_meta.py`'s
`description`-strip thesis-floor lint is the cross-repo half of the rider
byte-equality check. Registry: `.claude/skills/do-signoff/registry.tsv`; floor:
`evaluating/CLAUDE.md` §§ 4, 9.

**A declared hold window adds a publication BOUND, and a gate that carries
it.** While a Lean axis builds kernel material over a jurisdiction whose
matters are still open, nothing axiomatize-shaped about that material
publishes until the hold lifts — no kernel module, no theorem statement or
predicate spec shaped to a new framework, no synthetic twin cut to its shape.
Captioning cures REDACTION, not this: the bar reads on **names**, because a
namespace, a module name and a public page can jointly supply what no single
one states, which is why a content-only rule cannot close it. What MAY
publish, on `pleading/`'s conditions: primary-law corpus units taken whole
from the official source, counts with their POPULATION stated, and a method
note naming corpus units. Mechanism over instruction: the Stage-4 path rule
admits `.lean` under an `examples/` segment **only** and refuses it
everywhere else, so a kernel file nobody thought about fails CLOSED
(over-refusing costs a missing file; under-refusing publishes a theory); the
content twins bar a generic appellate docket form — generic, because an
enumeration fails open on the next one — and the axis's jurisdiction kernel
namespace. Pinned by `t_23`. Re-opening any of this is a publishing-convened,
`pleading/`-gated round.

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
- **`pending/publish-digests/`** is a gitignored, fork-internal buffer — **at the
  worktree ROOT only** (`publishing/.gitignore` carries `pending/`,
  `ns:publishing/62`); **never** promoted by managing's verifier (internal-set +
  `verify-pending.sh` `require_not_internal_pattern`). It is **not** in the close
  rescue-scan skip set, so every `/publish` session hits `--pre` exit 15 on these
  files — one deliberate pass, not a reflex delete: a digest's section (a)
  carries findings the run did not apply (deferred enrichment, cross-subproject
  owed fixes). Extract them into the close summary or a next-step **first**,
  then delete.

## 7. Status emit (`data/status/publishing.json`)

`scripts/status_emit.mjs` participates in the status contract (root CLAUDE.md
§ "Status hub"; KIT_VERSION lockstep: `project_diagram_kit` — read the constant
in the emitter, never a restatement). Four-state pill machine: `OK`
(last `/publish` clean) / `BUILDING` (run in flight) / `DEGRADED` (last run
aborted on the redaction/drift gate — privacy floor held, release stale) /
`NOT_YET_LIVE` (pre-first-publish; first live push 2026-06-12). The pill
resolves from the tracked one-line state file `publishing/.publish-state`
(`<PILL> [reason]`, written by the `/publish` lane — emitter defaults to
`NOT_YET_LIVE` without it). Summary diagram = the five-stage pipeline;
`TableEmit` = the repo roster. Close-time emit is mandatory
(`/close --status-emit publishing` resolves the producer via `close.sh`).

## 8. Layout

`quantapix/` public-org staging tree (own CLAUDE.md) · `youtube/` channel
material (index `youtube/README.md`) · `resume/` the out-of-roster
github.com/quantapix/resume source · `inbox/` gitignored private receipt/usage
PDFs, never published · `pending/messaging-debate/` GITIGNORED pre-gate debate
buffer, wiped at `/close` (§ 9; the tracked round record carries anything load-bearing) · `.publish-state` tracked one-line pill (§ 7) ·
`.worktree-links` canonical-backed gitignored links (inbox + resume PDFs) ·
`.claude/` settings + skills symlink + `publish-collector` · `hub-goldens/`
per-list manifests for the synthetic public track (never published; own
README). `scripts/`:
`publish.sh` · `github_meta.py` · `iga_verify.py` ·
`sync_mirror.py`/`sync-mirror.sh` · `status_emit.mjs` · `videos_emit.mjs` ·
`youtube_{auth,upload,sync,manifest}.py` · `hub_goldens_list.py`.

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
- **Lane:** operator-run inside `/open publishing`; the convener starts each
  round at v0.1. Recurring-round stewardship by `managing/`'s daily cron is
  deferred (debate charter § 2.7).
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
- **Public-key derivation (publishing owns).** Derived at publish time from the
  debate-locked title, never the subject-slug path; the redaction sweep gates the
  DERIVED key. Detail: `.claude/skills/youtube-sync/SKILL.md` § Public-key derivation.
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
  the **R2 union — committed class floor ∪ per-entry flags** (`in_scope_gates()`): the
  floor from `data/publishing/r2-scope-map.json` keyed by the manifest `key`'s topic
  prefix (structurally mandatory, so it cannot be forgotten); flags widen only, never
  narrow; an **unregistered class fails closed** (an ungated default is the R2 vacuity
  attack). Schema, readers, R9, per-asset classes: `data/publishing/CLAUDE.md`.
  `signoff_blocker()` then refuses push/adopt-over/upload unless every in-scope gate's
  `signoffs[<gate-id>]` names a record on disk — a promoted
  `data/messaging-rulings/<date>.md` (pleading grants; the same § 11.2 floor the upload
  sheets ride) or a `data/signoffs/FINANCIALLY/` record (evaluating grants, accounting
  advises). publishing never self-grants. **IGA enforcement (R7):** inline-operator
  grants get `iga_verify.py`'s three refuse checks — contract, wiring, test:
  spec § 5.5. Owed: `github_meta.py` repo-content binding (needs the
  evaluating-owned FINANCIALLY `LEDGER.md`, R1). (2) The synthetic-content
  **altered-content disclosure has no API field** — it stays a manual Studio toggle
  per upload (`CHANNEL-INFO.md` § 9); an API upload is never compliance-complete on
  its own. A redaction/verb scan over `descriptions/` runs before any push.
- **Banner ↔ channel-info land together** (same PR) — `youtube/README.md` § Banner ↔ channel-info lockstep.
- **First run = `--mode adopt`** (baselines the SoT from live so the diff is real),
  then `check` → resolve → `push`; `--mode stats` writes
  `data/publishing/youtube-stats.json`. `youtube_sync` does NOT touch `videos.json`
  — the /videos live-flip stays the `videos_emit.mjs` edit (§ 10).
- **CDN release gate (`CLEARANCE_COMMIT`).** `serving/scripts/upload-video.sh` refuses
  any `T<n>/` catalog key unless `CLEARANCE_COMMIT` equals the `granting_commit` of a
  `CLEARED*` FINANCIALLY record (registry-resolved; missing registry ⇒ refuse; then
  ancestor of HEAD) — so a `verified-N/A` grant for a non-financial episode is
  **mechanically required**. **This paragraph has been wrong in BOTH directions
  across three corrections — read the script, not this paragraph.** Ancestry-only-era
  history: `ns:publishing/46`. Contract family `data/specs/serving-2026-05-26/`
  (serving owns script + gate); this bullet is the publishing-side pointer the
  script's error message cites.
