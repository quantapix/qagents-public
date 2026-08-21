# CLAUDE.md — designing/

Project-specific rules for the Quantapix marketing site. Assumes Claude Code's
default guidance and the repo-root `qagents/CLAUDE.md`. Don't re-litigate those.

## 1. Naming

The company is **Quantapix**. The products are **Qnarre** and **Qresev**. Do
**not** use a retired brand name in any file under `designing/web/`, in copy, in filenames,
or in plan docs — even when the upstream Claude Design bundle uses it as an
umbrella brand. The composed token lint (`pnpm lint` → `code/web/scripts/lint-tokens.sh` + `web/lint-tokens.conf`, `BAN_SILCROW=1`) enforces this.

## 2. Design bundle is read-only; token SoT at rendering/brand/

`data/renders/designing-design/` is a Claude Design handoff bundle
(shared-data hub `data/renders/`), regenerated wholesale — **never
hand-edit**. Changes flow one direction: new bundle overwrites, we diff
and propagate.

**Token SoT (promoted 2026-06-10):**
`rendering/brand/tokens/quantapix/tokens.css` is canonical;
`web/src/styles/tokens.css` is a byte-identical copy (the composed lint's
`SOT_CMP` pair in `web/lint-tokens.conf` enforces parity; `pnpm verify`
fails on drift). Re-sync when a
new bundle ships: run rendering's two-drift intake sweep
(`rendering/CLAUDE.md` § 4) over `project/colors_and_type.css` (+ any
sub-bundle `assets/tokens.css`), land the swept result at the brand SoT
preserving the SoT-lineage header, `cp` byte-identical to
`web/src/styles/tokens.css`, then `pnpm verify`.

**Scope bound (DS1b/DS2):** `tokens-bridge.css` (kit aliases) stays
designing-owned. The brand-mark SVGs (`web/public/assets/brand/*.svg`,
since the 2026-07-07 promotion) are **consumed copies** of
`data/renders/designing/*.svg` from the rendering-owned vector lane
(`rendering/designs/designing-web/emit.mjs`) — never re-hand-author
here; re-run the emitter and re-copy. The promoted set is
quantapix-only — femfas is a sibling set; quantapix values are never
rewritten to accommodate it.

**Sibling design-prompt discipline** → memory
`reference_design_bundle_craft_checklist` § 8 (2026-08-09, intake #7): a prompt
referencing an existing brand artifact embeds the SVG verbatim, never
re-describes the glyph. Read when commissioning a bundle.

## 3. Tokens are the only boundary for raw values

`web/src/styles/tokens.css` is the byte-identical brand-SoT copy (§ 2).
Everywhere else:

- No hex color literals in `.astro` / `.tsx` / `.ts` / `.css` (use `var(--token)`).
- No `font-family: "…"` string literals (use `var(--font-display|body|mono)`).
- No pixel literals for spacing (use `var(--space-N)`).

`pnpm lint` enforces (1) and (2). (3) is guided by review for now.
**Rule 5** also fails on a bare `var(--token)` whose token is never
defined — an undefined `var()` is invalid-at-computed-value and silently
drops the whole declaration to its initial value (an off-scale
`--space-7` once zeroed the LOUD card padding). `var(--x, fallback)` is
exempt (the fallback resolves). The scale is curated and non-linear
(no `--space-7`/`--space-14`); snap to a defined step, never add one to
`tokens.css`.

## 4. Copy lives in one module

All user-facing strings (product names, headlines, CTAs, mission, per-route
OG metadata) live in `web/src/content/copy.ts`. Don't inline copy into
pages/components.

**Voice.** Engineer-debugging-a-system register, same as femfas.net. No
marketing-fluff present-tense — describe system state factually, not as a
pitch. Qnarre + Qresev went live 2026-06-01; copy is present-tense for live
surfaces and future-modal only for genuinely unshipped ones.

**Per-route OG metadata.** `OG_META: Record<route, OGMeta>` in
`content/copy.ts` is the share-card source of truth; `Layout.astro`
consumes it via the `og` prop and emits absolute `og:image` +
`twitter:title|description|image` + `summary_large_image` card. Each new
page: add an `OG_META` entry, pass `og={OG_META['/<route>']}` to
`<Layout>`. Absolute URLs are built from `brand.baseUrl` — never hardcode
`https://quantapix.com` elsewhere. The 7 `public/assets/og-*.png` are
**rendering-owned, brand-bearing pre-rasterized artifacts**
(`rendering/CLAUDE.md` § 4). Design source lives at
`rendering/designs/designing-og/{manifest.json,og.html}`; deliverables flow
to `data/renders/designing/og/og-*.png` and designing *consumes* them by
copying into `public/assets/`.
Re-render after a tokens/copy change from the rendering harness:
`node rendering/engines/image/capture.mjs designing-og --offline` (verify with
`--check`), then `cp data/renders/designing/og/og-*.png web/public/assets/`
and redeploy. `/videos`+`/donate` reuse `og-home`; all `/status/*` reuse
`og-status`.
**Never-navigated head assets** — `og:image` targets, favicon, PWA icons and
manifest — are fetched by neither `pnpm verify` nor e2e, so a missing file is
invisible to every gate: `curl -sI` them and assert `200 image/png` after any
change to either namespace (favicon roster + rasterizer + `theme_color`
detail: memory `project_designing_web`).

**Disclaimer (concede-and-preempt) — single source, binding placement.**
The `disclaimer` export in `copy.ts` (`canon` + `legalRider` + `financialRider`)
is the ONE concede-and-preempt wording; never re-author per-page disclaimers.
It renders via `DisclaimerCallout.astro` (both apps), and its placement is
**pleading-binding**: the callout MUST sit adjacent to the verdict token (the
REPORT pipeline cell) — `/qnarre` (canon+legalRider), `/qresev`
(canon+financialRider), `/thesis` (canon only) — so the disclaimer travels with
any liftable "⊢ §…/VALID under §" string, not just intro prose. Sample-trace
streams must stay synthetic (no live-matter predicates) and carry a visible
`streamLabel`; e2e `public-messaging cures (Round 03)` + the site.spec blacklist
guard both directions. Binding record:
`data/specs/publishing-2026-05-31/quantapix-thesis-github-2026-06-23/PLEADING-GATE-DECISION-2026-06-23.md`.
`pleading/` owes the § 11.7 post-deploy cold-read after every deploy that
changes messaging (incl. the promotion deploy's R6 — naive-reader test on
the corrected figures + membrane).

**Barred-token guard (live 2026-07-31, ns designing/15 (c)):** `bash
web/scripts/barred-tokens.sh` — run before **every deploy**. An invocation of
documenting's path-agnostic `barred_tokens_guard.py` (canonical path — the
venv's pymupdf lives there), never a second implementation: it scans the
deployed **payload** (`dist/` + ALL of `public/`, PDF text included — a
source-tree grep structurally cannot reach `public/` assets), against
designing's own sha-keyed reviewed inventory
`web/scripts/barred_tokens_reviewed.json` (empty today — this site hosts no
legal PDFs). Exit 3 = unreviewed hit; a hit is a **review trigger for
`pleading/`, never an auto-delete**, and only a `pleading/`-reviewed sha
enters the inventory. Token set (incl. R14 widenings + the `leave to file`
carve-out) lives in documenting's guard and is inherited automatically —
widen the token there, don't widen the action. Sibling instrument + wording: the femfas.net surface's CLAUDE.md carries the matching collateral-docket bar section.

**Surface prose vs. hosted payload.** A verbatim filed paper published *as a
dated filed paper* does not make an assertion this surface is answerable for;
card text, leads, OG descriptions, `drive.json` strings, status slots and
public READMEs are present-tense publisher speech and do. A correction to a
characterization therefore runs **forward** (new prose), never backward into
an archive of dated filed papers. Authority:
`data/messaging-rulings/2026-07-26.md` R2 C1.

**Hub-backed pages are an exception — copy.ts holds chrome only.** Pages
that render against a sibling subproject's data-hub slot keep
substantive content in the hub JSON and reduce `copy.ts` to chrome
(overlines / labels / brand strings). Three surfaces today:

- `/status` ← `data/status/<sub>.json` (each subproject self-emits;
  see § 9).
- `/videos` ← `data/publishing/videos.json` (rendered from the
  `explaining/` roster + publishing's release state via
  `publishing/scripts/videos_emit.mjs`; publishing-owned — the roster is
  NOT in `copy.ts`, edit `videos_emit.mjs`). `copy.ts` holds only the
  `videos` chrome block. Loader `src/lib/videos-loader.ts`
  (`schemaVersion` guard `{1}` + placeholder fallback); thumbs at
  `web/public/video-thumbs/<id>.png`. Video embeds reference the absolute
  `videos.quantapix.com` CDN URL, never same-origin (§ 7).
- `/donate` ← `data/donating/drive.json` (rendered from
  `donating/drive.md` via `donating/scripts/emit.mjs`; donating-owned —
  every field flows through verbatim). `copy.ts` holds only section
  overlines (incl. `scopeOverline`). Designing-side render caveats:
  `recordCites` is a redacted federal-forums-only derivation (no state
  dockets/judges) — never hard-code a row count or expect state rows;
  the `contingencies` block is post-drive, outside the four buckets —
  render with that framing or omit, never as a drive-window expense.

This keeps the marketing surface trackable against external sources of
truth (`drive.md` rides the cross-filed § 1746 affidavit; status emits
are producer-owned), so drift is a single-file edit in the source-of-
truth subproject. Adding a field to a hub-backed surface: extend the
loader types (`src/lib/<x>-loader.ts`) + the emitter; never paraphrase
content into `copy.ts`.

**What counts as content, and why a diff can never catch the failure.** Any
string naming a **bucket, a channel state, an amount, or a court record** is
content — derive it from the hub, never write the literal. A hardcoded literal
survives the very deploy that changes the fact it states, and the page then
**disagrees with itself**: one section contradicting another section of the
same page is invisible to a diff review, which only ever sees the changed
lines. Three instances of the class to date, all cured: `/donate` Bucket 4
named "SCOTUS" in three hardcoded strings against the `drive.buckets[3]`
table (2026-08-07; fixed + deployed 2026-08-16 `91a069ade`/`298a6ff0a` —
labels AND the window/channel status line now derive from `drive.json`,
same-page consistency e2e in `site.spec.ts` guards both directions), and the
public contact email (2026-07-24 — `donating/CLAUDE.md` § 3 records its
three-layer shape). **Verification is a LIVE read of the rendered page,
checked against the rest of that same page** — never a diff, never a deploy
ID.

## 6. End-to-end tests (Playwright)

The site's canonical verifier is `pnpm verify` (lint + astro check +
build); a change isn't done until it's green locally.
Suite at `web/tests/e2e/{site,interactivity,videos,status}.spec.ts`
(status coverage detail: § 9); the shared stack (helpers, three chromium
projects, `webServer = build && preview` never dev, run/install commands)
is root `qagents/CLAUDE.md` § "Playwright e2e". Designing-specific:

- **Live-site mode**: `PW_BASE_URL=https://quantapix.com pnpm -C web test:e2e`
  flips `baseURL` to the deployed site and skips the local `webServer`
  block via object-spread conditional. Run after every deploy.
- Site spec covers routes / OG meta / blacklist (retired brand names + contact leaks)
  / external-link safety; interactivity spec covers Nav `aria-current`,
  HeroHeadline, footer presence, reduced motion.

When adding interactive UI: prefer a vanilla inline `<script>` controller
over a React island for simple state (Astro scoped CSS doesn't reach
React-rendered elements — silent failure); reserve islands for complex
state. Test-guard recipe (networkidle + double-rAF before a React-installed
keydown handler) lives in memory `feedback_react_island_hydration_race`.

## 7. Hosting + deploy (S3 + CloudFront)

AWS S3 + CloudFront, mirroring `documenting/web/` exactly:

- Bucket: `quantapix.com` (us-east-1)
- CloudFront distribution: `E27NQG9Y1ZPLGH`
- Cache policy: `*.html` short cache (300s, must-revalidate), everything
  else immutable (1y).

**Large binary media.** Serve from the CDN, keep a local backup mirror —
single owner `serving/CLAUDE.md` § 8 (`upload-video.sh`,
`videos.quantapix.com`, <5 MB `public/` rule, gitignored local mirror via
`designing/web/.worktree-links`). Designing e2e: `tests/e2e/site.spec.ts`'s
`large media URLs` block HEADs the CDN URL unconditionally (no skip-on-404,
no `PW_BASE_URL`).

Scripts under `web/scripts/` (per-site, kept here):

- `setup-bucket-hardening.sh` — per-site bucket hardening (serving § 8;
  one-shot, idempotent).

Token-boundary lint (`pnpm lint`) is **composed over the shared base**
`code/web/scripts/lint-tokens.sh` (web-unification R-T5 / M5b, adopted
2026-07-22) — `pnpm lint` = `bash ../../code/web/scripts/lint-tokens.sh
lint-tokens.conf`. The site's checks live in `web/lint-tokens.conf`
(retired-brand-name ban, hex/font-literal bans, `thesis-steps` exclude, undefined-var
guard, and TWO `SOT_CMP` byte gates: `tokens.css`↔brand-SoT and, since
2026-07-31, `public/thesis-steps/thesis-dark.css`↔the rendering overlay SoT —
so an overlay VALUE change is an atomic rendering+designing co-land, same rule
as the visualizing kits); `BAN_DERIVED=0` keeps the pre-existing
`color-mix`/`rgba` wash literals passing (no check dropped).

Deploy goes through the central `serving/scripts/deploy-site.sh
quantapix.com` (invoked by `pnpm -C designing/web deploy`); IAM policy,
canonical templates (`serving/templates/`), the new-distribution OAC +
rewrite-Function + 403/404 checklist, and the cross-site deploy contract
(credential workflow, full-replace shape, `AWS_VAULT` detection,
trailing-slash rule) are all `serving/CLAUDE.md` § 8 — single owner,
don't re-litigate here.

**Deploy + live verification**:

```
aws-vault exec qagents-deploy -- pnpm -C designing/web deploy
PW_BASE_URL=https://quantapix.com pnpm -C designing/web test:e2e
```

**Merge main before deploying a hub-backed surface (§ 4).** The hub
loaders (`videos-loader.ts` / `status-loader.ts` / `donate-loader.ts`)
read the **worktree's** `data/<topic>/*.json`, not canonical, so a
`designing` branch opened before a sibling's `/close` ships a stale slot
silently. Before deploying a hub-slot render: `git log HEAD..main` +
`git merge main` if the sibling's close is missing. See memory
`feedback_merge_main_before_deploying_hub_backed_surface`.

## 8. Scope boundary

This subproject does not import from `analyzing/` or `trading/`, and vice-versa
(root CLAUDE.md language-split rule). If we ever need shared data, follow the
parquet-at-`./data/<name>/` pattern.

The rule is **absolute — no temporary staging, no Phase-A code-import, no
workspace-package-as-data-shim**: sibling state reaches designing/web only
via `data/<topic>/<sub>.json`. Sole shared-code seam: `@qagents/diagram-kit`
(workspace package; rationale `serving/CLAUDE.md` § 6).

## 9. Status page (`/status`) — implemented

`/status` (index; see "Hidden cards" below) +
`/status/<sub>/` (deep page, dynamic via `getStaticPaths`) are live and
Playwright-verified. Build-time bake: the page reads
`data/status/<sub>.json` slots through `src/lib/status-loader.ts` (Zod
validation, kitVersion drift guard, synthetic placeholder fallback on
missing/malformed JSON — build never fails on a missing slot).

**Propagation contract:** working a `/status/<axis>/` substance panel → read
memory `project_designing_web` § "Status panels + producer contract".

- **Schema** (kit-owned): `@qagents/diagram-kit` — root `qagents/CLAUDE.md`
  § "Status hub" owns the contract; `src/lib/status-loader.ts` carries the
  live `PRESENT_KIT_VERSION` + `ACCEPTED_KIT_VERSIONS` (SoT — never
  re-enumerate elsewhere). Closed display-mode set + 3-layer model: spec
  family `data/specs/display-modes-2026-05-07/`.
- **Thematic groups (adopted 2026-05-06).** `/status` renders 3 group
  sections in fixed order: **Quantapix** (umbrella; neutral accent) →
  **Qnarre** (verifying ← proving; teal accent; depends-on serving) →
  **Qresev** (evaluating ← accounting · analyzing · trading; amber accent;
  depends-on serving). Source of truth: `STATUS_GROUPS` in
  `src/content/copy.ts`; card total = the `status.spec.ts` assertion, never
  restated here. Don't move cards across groups without a decision.
- **Hidden cards (reversible).** Several subprojects are omitted from
  `STATUS_GROUPS.members` to reduce marketing-surface noise; the live roster +
  per-sub reason is the comment block directly above `STATUS_GROUPS` in
  `copy.ts`, never re-enumerated here. `STATUS_CARDS`, `OG_META`, and
  `KNOWN_SUBS` entries all remain — `/status/<sub>/` deep pages still build.
  Reversal is a one-line edit to the matching `members[]` array in `copy.ts`
  plus the e2e fixture sweep (KNOWN_SUBS + GROUPS + total-count assertion in
  `tests/e2e/status.spec.ts`).
- **Panel/emit detail spread to memory** — six display modes, status
  components, page-level `attachInteractivity` wiring, bridge tokens,
  copy blocks, `status.spec.ts` coverage, and the producer contract for
  all 6 emit kinds: memory `project_designing_web` § "Status panels +
  producer contract". Invariants that bite outside a status session:
  teal/amber accents are reserved for Qnarre/Qresev (others neutral);
  `StatusDiagram` carries NO inline `<script>` (`attachInteractivity`
  wires in `pages/status/[sub].astro`'s page-level `<script>` — Astro 5
  dev breaks on the component-inline form,
  `feedback_astro_dev_import_type_scanner`).

The Status page is the canonical surface for the engineer-debugging voice
(§ 4) — system state, factual present-tense, no marketing fluff.

## 10. LOUD production app (web-next promoted 2026-07-07)

`designing/web/` IS the adopted Claude Design "LOUD" treatment (dark,
statistic-forward home; live membrane hero), promoted from the `web-next/`
staging sibling 2026-07-07 (content de-dup deferred). Records: debate record
`web-next-promotion-2026-07-07` (`data/debates/`, HELD lane; R1–R6) + pleading re-clear
`data/messaging-rulings/2026-07-07.md`. Package `quantapix-web`; e2e port
4322. Specs: `data/specs/designing-loud-redesign-2026-06-19/` (family),
`data/charters/designing/specs/designing-hero-membrane-2026-07-06/SPEC.md`.

- **Home-hero messaging gate (BINDING, pleading-signed 2026-07-07).**
  *The home hero — whatever artifact occupies it — MUST hold a current
  `pleading/` messaging re-clear (the 2026-07-07 record is the current
  one). The convention pins the **requirement**, never a specific
  artifact.* A hero-artifact swap voids the prior clearance
  (clearance binds the artifact, not the slot —
  `feedback_public_surface_count_and_clearance_scope`). Floor source:
  thesis spec § 4.1/§ 4.2,
  `data/charters/studying/specs/lean4-charter-2026-06-10/quantapix-thesis-2026-06-22/SPEC.md`.
- **Membrane hero.** `public/hero-membrane/hero-membrane.js` (vanilla
  canvas module, `QxHeroMembrane.mount`, lazy-loaded `is:inline` from
  `index.astro`). Carry-conditions from the 2026-07-07 re-clear: the
  module stays **textless** (no canvas text API), and the host
  `aria-label`/caption carry no claim verb — any re-sync that adds
  either re-opens the gate.
- **Stat strip (5 slots, resolved 2026-07-07).** `home.stats` in
  `copy.ts`. Slots 1 + 5 are pleading-cleared **verbatim** — a wording
  change is a new artifact, re-clear required. Slot-5 verb lock:
  "axiomatized" (encoding verb), never proven/derived/established;
  its `<1%` figure excludes the local-only operational axis. Slot-4
  (videos live) is build-time hub-fed from `data/publishing/videos.json`
  `stats.live` via `videos-loader` (landed 2026-07-10); `copy.ts` holds
  a placeholder fallback.
  **Slot-5 is likewise hub-fed since 2026-07-24** — `src/lib/corpus-coverage.ts`
  measures it over the two PUBLIC axes' status slots; `copy.ts` keeps `<1%` as
  the both-placeholder fallback. That module is the single owner of the three
  slot-5 locks — operational axis never summed, withheld `uscTierA/B/C` never
  read, cleared wording rendered while the measured aggregate stays < 1% — and
  they are enforced in code, not by convention; field names, ruling
  carry-condition cites and the ns-54 withholding rationale: memory
  `project_designing_web` § "State as of 2026-07-24". **The slot-5 e2e
  assertion (`tests/e2e/interactivity.spec.ts`) is the clearance tripwire** —
  when it fails, the fix is a pleading re-clear of the new wording, NEVER a
  loosened expectation. Add a public axis here only if its producer already
  emits both counts; a new emit field is strictly riskier than reading one that
  ships (root § Status hub whole-slot failure trap).
- **Thesis-steps animation (`/thesis`).** Touching `/thesis` or
  `public/thesis-steps/` → read memory `project_designing_web`
  § "Thesis-steps delivery module" (floors + byte-exact contract).
- **Method-DAG drill-down (`/thesis`, W10 — live 2026-08-16).**
  `public/graphs/` is a kit-mount host-copy set (root § Kit-mount pattern
  applies): `kit.js` regen-wholesale from canonical
  `visualizing/graphs/dist/kit-graphs.js` (rebuild dist first, grade by hash)
  + `tokens-proof.css` as its LOCKSTEP token overlay + `kit.css`; authored
  `hero-graph.json` (never regenerated) is the landing state,
  `method-{legal,financial}.json` are wholesale re-copies of
  `data/visualizing/` siblings (drill-down states); `loader.js` is the
  app-owned never-fold side-car. Chrome strings in `copy.ts thesis.methodGraph`
  (claim-free vocabulary). E2e: `interactivity.spec.ts` "Method DAG" block
  incl. the per-sheet token guard.
- **Tokens.** § 2/§ 3 apply (byte-identical brand-SoT copy, incl. lint
  rule 4). LOUD-only raw values live in `tokens-next.css` (pure
  `var()`/`color-mix`, no hex); mask gradients use the `black` keyword to
  clear the hex lint; the composed lint conf (`web/lint-tokens.conf`) carries
  `EXCLUDE_DIRS=(thesis-steps graphs)` (host-copied mounts with their own
  token-definition files).
- **Background variant** is **glass** (operator-chosen 2026-06-21): dark wash
  + breathing teal/amber blobs (`Ground`) + gradient-shimmer numerals
  (`StatStrip`). NB the fixed `Ground` (`z-index:-1`) needs the base canvas bg
  on `html`, not an opaque `body` — else it paints behind and is invisible.
- **Verify** with `pnpm -F quantapix-web verify` + `test:e2e`; deploy via
  § 7 (the `deploy` script + live-site e2e).
