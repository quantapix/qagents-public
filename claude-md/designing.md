# CLAUDE.md — designing/

Project-specific rules for the Quantapix marketing site. Assumes Claude Code's
default guidance and the repo-root `qagents/CLAUDE.md`. Don't re-litigate those.

## 1. Naming

The company is **Quantapix**. The products are **Qnarre** and **Qresev**. Do
**not** use a retired brand name in any file under `designing/web/`, in copy, in filenames,
or in plan docs — even when the upstream Claude Design bundle uses it as an
umbrella brand. The lint script (`web/scripts/lint-tokens.sh`) enforces this.

## 2. Design bundle is read-only; token SoT at rendering/brand/

`data/renders/designing-design/` is a Claude Design handoff bundle
(shared-data hub `data/renders/`), regenerated wholesale — **never
hand-edit**. Changes flow one direction: new bundle overwrites, we diff
and propagate.

**Token SoT (promoted 2026-06-10):**
`rendering/brand/tokens/quantapix/tokens.css` is canonical;
`web/src/styles/tokens.css` is a byte-identical copy (`lint-tokens.sh`
rule 4 enforces parity; `pnpm verify` fails on drift). Re-sync when a
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

**Sibling design-prompt discipline.** A Claude Design prompt referencing
an existing brand artifact (`logo*.svg`) MUST say "embed
`designing/web/public/assets/brand/<file>.svg` verbatim" — never
re-describe the glyph (describing invites regeneration drift).
Acceptance: the bundle's wordmark SVG diffs against the source with only
viewBox-scale differences.

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
Because `og:image` targets are never navigated, neither `pnpm verify` nor
the e2e PDF-reachability sweep catches a missing PNG — `curl -sI` the live
`og:image` URLs and assert `200 image/png` after any OG-asset-namespace change.

**Favicon / PWA head assets**
are the same never-navigated class: `Layout.astro` head carries `icon`
(SVG) + `apple-touch-icon` + `manifest` (`/site.webmanifest`); icons +
manifest live under `public/assets/brand/`, rasterized from the app's
`app-icon.svg` via Playwright Chromium (no `rsvg`/`magick` locally).
`pnpm verify` / e2e never fetch them — `curl -sI` after any change.
Theme color is `theme_color` in the webmanifest, **not** a
`<meta name="theme-color">` (the meta needs a hex literal that rule-2 lint
forbids; the JSON manifest is unscanned).

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
- `lint-tokens.sh` — pre-build lint (no hex literals outside `tokens.css`,
  no upstream-bundle brand leaks); designing-owned per-site lint, to be
  composed over the shared base `code/lint/lint-tokens-base.sh`
  (web-unification R-T5).

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

`/status` (index; 6 cards hidden — see "Hidden cards" below) +
`/status/<sub>/` (deep page, dynamic via `getStaticPaths`) are live and
Playwright-verified. Build-time bake: the page reads
`data/status/<sub>.json` slots through `src/lib/status-loader.ts` (Zod
validation, kitVersion drift guard, synthetic placeholder fallback on
missing/malformed JSON — build never fails on a missing slot).

- **Schema** (kit-owned): `@qagents/diagram-kit` — root `qagents/CLAUDE.md`
  § "Status hub" owns the contract; `src/lib/status-loader.ts` carries the
  live `PRESENT_KIT_VERSION` + `ACCEPTED_KIT_VERSIONS` (SoT — never
  re-enumerate elsewhere). Closed display-mode set + 3-layer model:
  `data/specs/display-modes-2026-05-07/SPEC.md`.
- **Thematic groups (adopted 2026-05-06).** `/status` renders 3 group
  sections in fixed order: **Quantapix** (umbrella; neutral accent) →
  **Qnarre** (verifying ← proving; teal accent; depends-on serving) →
  **Qresev** (evaluating ← accounting · analyzing · trading; amber accent;
  depends-on serving). Source of truth: `STATUS_GROUPS` in
  `src/content/copy.ts`. Card count math (as of 2026-07-07): 12 + 2 + 4 = 18.
  Don't move cards across groups without an explicit decision.
- **Hidden cards (reversible).** Six subprojects are omitted from
  `STATUS_GROUPS.members` to reduce marketing-surface noise: `resolving`,
  `blending`, `monitoring`, `appealing`, `pleading`, `visualizing`.
  `STATUS_CARDS`, `OG_META`, and `KNOWN_SUBS` entries all remain — `/status/<sub>/`
  deep pages still build. Reversal is a one-line edit to the matching
  `members[]` array in `copy.ts` plus the e2e fixture sweep
  (KNOWN_SUBS + GROUPS + total-count assertion in `tests/e2e/status.spec.ts`).
- **Six display modes (deep page).** Kinds + field shapes: kit `types.ts`
  + `data/specs/display-modes-2026-05-07/SPEC.md`. Designing-side:
  card-summary slot stays diagram-only (`summaryDiagramId` never points at
  another kind); inspector hides on non-diagram panes via
  `.content:not([data-active-kind="diagram"]) :global(.status-inspector)`.
- **Components** (`src/components/status/*.astro`): one per emit kind plus
  index card / pill / URL-hash chip-selector / global inspector; prop
  detail lives in each file. Designing-specific invariants: teal/amber
  accents reserved for Qnarre/Qresev (others neutral); `StatusDiagram`
  carries NO inline
  `<script>` (see "Page-level interactivity wiring"); `StatusDashboard`
  renders `children[]` `bare`; `StatusInspector` is one global node the
  kit's `attachInteractivity` finds via `root.ownerDocument` fallback.
- **Page-level interactivity wiring.** `attachInteractivity` is invoked
  in `pages/status/[sub].astro`'s page-level `<script>`, NOT inside
  `StatusDiagram.astro` — Astro 5's dev pipeline breaks on the
  component-inline form (memory `feedback_astro_dev_import_type_scanner`).
- **Bridge tokens**: `src/styles/tokens-bridge.css` aliases the semantic
  token names (`--color-fg-strong`, `--color-surface-2`, `--color-brand-
  teal-soft`, etc.) that the kit's `tokens-diagrams.css` expects but the
  marketing-bundle `tokens.css` doesn't define. Imported in
  `Layout.astro` right after `tokens.css`. Don't fold these into
  `tokens.css` — that file is a byte-identical copy of the promoted brand
  SoT (§ 2); `tokens-bridge.css` itself stays designing-owned (DS1b).
- **Copy** lives in `src/content/copy.ts`: `status` block + `STATUS_CARDS`
  per-subproject map + per-route `OG_META` entries. Nav array in
  `copy.ts` carries the `/status` entry — `Nav.astro` iterates, no edit
  needed.
- **Tests**: `tests/e2e/status.spec.ts` covers card count (matches
  "Card count math"; revert with "Hidden cards"), pill color+icon, chip
  selector, hash nav, SVG title+desc, single-panel/no-chips fallback,
  reduced-motion, plus a "diagrams render as designed" describe block
  enforcing the 2026-05-04 root-cause regressions (edgeless aspect h/w >
  0.25, node fills resolve via bridge tokens on `:root`, labels visible,
  node-click populates the inspector with rendered HTML). New routes are
  walk + OG-meta checked in `tests/e2e/site.spec.ts`.

The Status page is the canonical surface for the engineer-debugging voice
(§ 4) — system state, factual present-tense, no marketing fluff.

**Producer contract (all 6 emit kinds).** Adding/altering any panel —
diagram, table, statCard, kpiStrip, filterChip group, dashboard — is a
producer-only change in `<sub>/scripts/status_emit.*` against the
kit-owned emit types (field shapes: kit `types.ts` +
`data/specs/display-modes-2026-05-07/SPEC.md`); re-run
`pnpm build:status`. Designing-side invariants:

- Every node needs populated `details` HTML — the inspector renders via
  `set:html` (unsanitized; trusted producer code only), and empty
  `details` leaves it blank on click.
- `panels[]` (`{kind, id}` refs) overrides the default render order
  (dashboards → diagrams → tables → statCards → kpiStrips →
  filterChips); statCards referenced only from a KpiStrip's `cards[]`
  stay out of `panels[]` (double-surface).
- A producer panel migration drifts the consumer e2e — update the
  chip-count/order arrays in `tests/e2e/status.spec.ts` in the same PR
  (`feedback_emit_migration_consumer_test_drift`).

## 10. LOUD production app (web-next promoted 2026-07-07)

`designing/web/` IS the adopted Claude Design "LOUD" treatment (dark,
statistic-forward home; live membrane hero), promoted from the `web-next/`
staging sibling 2026-07-07 (content de-dup deferred). Records: debate
`data/debates/web-next-promotion-2026-07-07.md` (R1–R6) + pleading re-clear
`data/messaging-rulings/2026-07-07.md`. Package `quantapix-web`; e2e port
4322. Specs: `data/specs/designing-loud-redesign-2026-06-19/SPEC.md`,
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
- **Thesis-steps animation (`/thesis`, Phase 3 shipped 2026-07-07).**
  `public/thesis-steps/{thesis-steps.js,thesis-dark.css}` — the ported
  thesis-hero delivery module + a byte-identical copy of the
  rendering-owned `--step-*` overlay SoT
  (`rendering/brand/tokens/quantapix/overlay/thesis-dark.css`).
  Caption + rail render in dedicated slots OUTSIDE the canvas; chapter
  titles live in the module (byte-exact contract with
  `studying/thesis.md`). Hard floors (claim-free vocabulary, open ch-7
  legs, silent, tokens-only): spec
  `data/charters/visualizing/specs/visualizing-2026-06-03/thesis-hero-2026-07-07/SPEC.md` § 3.
  The public MP4 bake stays Phase-5-deferred (W8 gate) — the page mounts
  the live module only.
- **Tokens.** § 2/§ 3 apply (byte-identical brand-SoT copy, incl. lint
  rule 4). LOUD-only raw values live in `tokens-next.css` (pure
  `var()`/`color-mix`, no hex); mask gradients use the `black` keyword to
  clear the hex lint; `lint-tokens.sh` carries `--exclude-dir=graphs2` +
  `--exclude-dir=thesis-steps` (kit / delivery-module mounts with their
  own token-definition files).
- **Graphs-2 kit mount (dormant on `/`).** `public/graphs2/` still
  serves the kit bundle (`kit.js`, regen-wholesale from
  `visualizing/graphs` dist `kit-graphs.js`) + `loader.js` + the
  method-DAG `hero-graph.json` (kit-mount pattern). The home hero mounts
  the membrane, not the kit
  — the fixture is dormant but stays messaging-guarded by
  `interactivity.spec.ts`'s METHOD_VOCAB block; removal is deferred to
  the content de-dup pass. On any fixture lift, sweep the e2e guard
  (`feedback_emit_migration_consumer_test_drift`).
- **Background variant** is **glass** (operator-chosen 2026-06-21): dark wash
  + breathing teal/amber blobs (`Ground`) + gradient-shimmer numerals
  (`StatStrip`). NB the fixed `Ground` (`z-index:-1`) needs the base canvas bg
  on `html`, not an opaque `body` — else it paints behind and is invisible.
- **Verify** with `pnpm -F quantapix-web verify` + `test:e2e`; deploy via
  § 7 (the `deploy` script + live-site e2e).
