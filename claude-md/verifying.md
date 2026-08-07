# CLAUDE.md — verifying/ (Qnarre)

Project-specific rules for the Qnarre app at `qnarre.quantapix.com`. Sibling
of `evaluating/` (Qresev). Wraps the `proving/` Lean4 + LLM-predicate kernel.
Assumes Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`.
Don't re-litigate those.

## 1. Layering — strict, like proving/

Three layers, no crossing:

| Layer | Where | Reads | Writes |
|---|---|---|---|
| **Web shell** | `web/` (Astro + React island) | HTTP + SSE from server | rendered UI |
| **App server** | `server/` (FastAPI in qagents root .venv) | uploaded complaint, manifest | spawns proving/ driver as subprocess; streams events |
| **Kernel** | `../proving/` (untouched) | manifest + complaint | `Facts.lean` + audit JSON |

The web shell never imports from `../proving/`. The server adapter
(`server/adapters/proving.py`) calls the proving driver as a subprocess and
reads its outputs. This honors the repo-root rule: web TS does not reach into
Python kernels, and the kernel's layering invariants stay intact.

## 2. Design SoT + brand mechanism (Meridian since M4)

**Since 2026-07-11 (web-unification M4) the web rides the Meridian layer,
BRAND-VIA-HOST:** design SoT is the adopted CD-B bundle at
`rendering/designs/verifying-web/` (10 sheets + ADOPTION.md floors; supersedes
`data/renders/verifying-design/`). Brand values never enter this tree:
`web/scripts/sync-meridian.mjs`
(predev/prebuild/prelint hooks) host-copies the W5 css layers from
`code/web/css/meridian/`, the font trio from `rendering/brand/fonts/`, and
composes the dual-signal `/meridian-tokens.css` from
`rendering/brand/tokens/meridian/{light,dark}.css` — all gitignored under
`public/`. `<body class="m-body m-app-qnarre">` binds the teal accent;
tri-state theme (System | Light | Dark) via `@qagents/web/theme` +
the shared TopNav's ThemeSegment.
Shared chrome/island shells come from `@qagents/web` (W2 TopNav/BracketedQ/
DisclaimerCallout; W4 TraceRail/ConfBar/PredicatesTable/StructureView/
ReportZone/useRunData) with copy injected from `src/content/copy.ts`
(fail-loud); the F1/demoed gating + verdict⇄disclaimer SIBLING composition
stay app-owned in `QnarreApp.tsx`.

## 3. Tokens are the only boundary for raw values

No hex colors / font strings outside the token-definition files
(`public/tokens.css` — LAYOUT-ONLY since M4: spacing/type-size/motion/z —
and the generated `public/meridian-tokens.css`). Refer to `var(--m-*)` /
`var(--token)` everywhere else. Lint = the composed
`code/web/scripts/lint-tokens.sh` + `web/lint-tokens.conf` (hex +
font-family + derived-alpha ban + undef-var guard + retired-brand-name ban).
`public/graphs/` stays
excluded (disjoint kit-token namespace, R-T2) — the kit canvas + overlays
are DARK in both legs; only page chrome flips.

## 4. Copy lives in one module

`web/src/content/copy.ts`. Don't inline copy into pages/components.

## 5. App surface is one big React island

`/app` is a single full-height React island (`web/src/islands/QnarreApp.tsx`)
with three persistent zones: INPUT (28%) · AGENT STREAM (36%) · REPORT (36%).
Static marketing pages (`/`, `/frameworks`, `/about`) stay Astro. The island
talks to the FastAPI server via SSE.

The REPORT zone has three tabs (Predicates / Structure / Proof graph)
when the URL carries `?id=<runId>`. The Proof-graph tab embeds
`/proof-graph/run/<id>/` (or `/<id>/debug/` when the kernel verdict is
REJECTED) in an iframe so the kit's interactions stay isolated from
QnarreApp's React state. Without `?id=`, the island falls back to the
existing demo data so the marketing-app preview keeps working without
a live server.

## 6. Defined-risk and statute scope

Qnarre verifies legal complaints under one of: civil RICO §§ 1961–1968,
Title VI §§ 2000d et seq., §§ 1981/1983/1985(3). Adding a framework is a
parallel exercise driven by `../proving/` first; the UI gains a new chip
only after the predicate roster lands.

**Taxonomy seam.** `proving/predicates/<id>/` is the authoritative
framework set. `web/src/lib/frameworks.ts` is verifying/'s single
declaration site: `FRAMEWORK_META[<id>] = { label, cite }` is the only
per-framework data this project owns; the predicate count comes from
the filesystem and the "updated" date from `git log`. Every consumer
(`index.astro`, `frameworks.astro`, `app.astro` → `QnarreApp.tsx`) goes
through `loadFrameworks()`. Adding a federal statute = one entry in
`FRAMEWORK_META` after the matching `proving/predicates/<id>/` dir lands.

## 7. Server scope

v0.1 is **replay-only**. POST `/api/runs` body is `{example_id}` from a
closed allow-list, narrowed to **synthetic examples only** under the F1
thesis floor: `{sample, titlevi_sample, titlevii_fedsector_refused}`. No
`<live-matter>_*` example is replayable — live matter, per the F1 gate (§ 8).
The static public build is stricter still — RICO-synthetic only
(`web/src/lib/public-runs.ts`); the replay API also serves the synthetic
Title VI sample and the synthetic Title VII federal-sector example
(`titlevii_fedsector_refused`, added 2026-08-01 — the first GENUINELY
refusing example: real predicate Falses on the exhaustion family, kernel
REJECTED at locus `h_federal_administrative_exhaustion`, so the API can
serve a true kernel refusal rather than the kit's injected-refusal
rendering fiction; proving mirrors the id into `status_emit.py`
`PUBLIC_EXAMPLE_IDS` SECOND, never first — ns:proving/40).
Edit `ALLOWED_EXAMPLE_IDS` (`server/main.py`),
`ALLOWED_IDS` (`api.spec.ts`), AND `extending/servers/qnarre-mcp/src/allowlist.ts`
in lockstep — a **triple** since extending landed 2026-07-04; the extending
parity test fails until all three match (§ 9.5).
The adapter shells `extract_facts.py --reuse-facts --build` against
`proving/examples/<id>/`, overwriting `{report,graph,loci}.json` in
place. No predicate sub-agent calls (committed `facts.json` is the
input); only `lake build` runs live (~2s, $0/run). Run dirs are
canonical `examples/<id>/` only — no per-job staging.

Endpoints: `POST /api/runs` · `GET /api/runs` (allow-list with current
verdicts + predicate counts) · `GET /api/runs/<id>/stream` (SSE events
typed per `data/specs/proving-results-propagation-2026-05-09/SPEC.md`
§ 5.4: `predicateResult` / `factsWritten` /
`lakeBuildStarted` / `lakeBuildResult`) · `GET /api/runs/<id>/report` ·
`GET /api/runs/<id>/graph` (consumed by the kit loader at
`/proof-graph/run/<id>/`).

CORS: `https://qnarre.quantapix.com` + `http://localhost:4321`.

**Privacy floor — Promise 3 satisfied by construction.** Replay-only
means no user complaint text reaches LLM or kernel; the only complaint
ever processed is the curated `examples/<id>/complaint.md` which is
already redacted in tree. The donating drive's `POST /api/runs`
refusal binding (`../donating/drive.md` Promise 3, 2026-06-01 →
2026-12-01) is therefore honored without any redaction-sweep code at
this layer. Revisit when admin-gated freeform POST lands.

## 8. Proof-graph kit (Lean4 DAG visualisation) — graphs mount (G6)

Since 2026-06-11 the proof-graph surface renders via the domain-neutral
**graphs kit** from `visualizing/` (the unified kit-mount that also
backs Qresev's strategy mount — visualizing spec
`data/charters/visualizing/specs/visualizing-2026-06-03/graphs-2026-07-02/SPEC.md` G6). Routes:

- `/proof-graph/` — lobby + cards linking to the two demos and the F1-gated
  live runs (see below).
- `/proof-graph/01-rico/` — Doe v. Acme § 1962(c) happy path over the
  committed `proving/examples/sample/graph.json`.
- `/proof-graph/02-debug/` — same DAG, three injected failure modes
  (predicate-False, predicate-Undecided, kernel-error) synthesized by
  `ProofGraphKit.makeSynthetic`; the value lens + failure borders
  restyle the same layout.
- `/proof-graph/run/<id>/` + `/<id>/debug/` — per-run views over real
  `proving/examples/<id>/graph.json` fixtures via `getStaticPaths`,
  **F1-gated** (see below); REJECTED runs surface a debug-overlay link
  in the header.
- `/lattice/` — the axiomatization catalog (coverage × agreement × tier)
  over `data/visualizing/legal-catalog.json`, same kit in catalog mode
  (cells collapsed, agreement lens, `tokens-lattice.css`). Also hosts the
  **C3 rollups + trends panel** (see below).

**C3 aggregate charts panel (charts-2026-07-02 § 7.1, ns verifying/7).** A
toggle-opened overlay panel ON `/lattice` (no new route — a new route enters
the F1 leak-guard sweep and buys nothing). The `rollups` status-bar button
paints corpus-level rollups (`QViz.charts.fromCatalog` → tier distribution /
axis coverage / agreement, 3 SVG bar charts) + trends (`fromCatalogTrend` over
`data/visualizing/legal-catalog-trend.jsonl`). The charts SVG surface rides
`kit.js` (the `QViz.charts.*` namespace in `dist/kit-proof.js`; `charts.*`
because the flat global already carries graphs' `fromCatalog`); it self-themes
dark like the DAG canvas (kit defaults — no `--chart-*` overlay copied). Panel
chrome is app-owned in `pages.css` (`.rollups-panel`/`.chart-cell`, display
scoped to `:not([hidden])`). **Degenerate-trend guard is host-side** (`trend.ts`
delegates it): the trend half stays empty-state until ≥ 2 trend records exist
AND a dimension has moved — today 1 emit (all `tier:unknown`) → empty-state, so
a flat 100%-unknown line never ships next to the F1 language. Inherits
`/lattice`'s F1/named-never-worked posture verbatim + the PLEADING-REVIEW
binding; catalog cells are corpus-level (no `<live-matter>_*`). e2e: the `C3 rollups`
describe in `proof-graph.spec.ts`.

**F1 thesis-floor gate (named-never-worked).** The textual axis is *named,
never worked* in any public material, and no public worked example is drawn
from a live matter (`disclaimer.legalRider`; SoT `studying/thesis.md`). So the
public build's only worked proof-DAG run page is the **synthetic civil-RICO
sample** (`sample`). `web/src/lib/public-runs.ts` (`isPublicWorkedRun`) is the
single gate: it drops every non-RICO example (only `rico` is in
`frameworks.ts` `PUBLIC_DEMOED`) and every `<live-matter>_*` example (live matter,
incl. `rico-hier`). Both run pages' `getStaticPaths` AND the lobby's live-run
scan call it; the same gate backs the `/app` island chips (non-demoed →
"encoded · not demoed", no verdict/Boolean) and `LiveReportZone`. Provenance:
Round 04 G2 (`data/debates/quantapix-thesis-github-2026-06-23.md`); pleading/
cleared 2026-06-24 (`data/specs/publishing-2026-05-31/quantapix-thesis-github-2026-06-23/PLEADING-FINAL-GATE-2026-06-24.md`).
The replay API is gated to the same floor (§ 7); residual
(intentional): it also serves the synthetic non-RICO `titlevi_sample`.

**These host-copies can go STALE AT CANONICAL, and nothing detects it** — the
lockstep-pair rule governs re-copying both halves together, never freshness, and
`scripts/open.sh` hydrates a worktree from *current* source while canonical
carries whatever its last build left, so the copy a `/close` is about to delete
can be the *more current* one. A rescue-gate hit under `web/public/` is
therefore never automatically discardable: hash-compare before disposing. Lived
instance (2026-07-30 meridian copies), the disposal procedure, and the cheap
hashing fix: memory `project_proof_graph_kit_mount_pattern` § "Rescue-gate hits
are not automatically discardable".

Kit files live at `verifying/web/public/graphs/`:

- `kit.js` — the graphs IIFE bundle (global `QViz`: `mountProof` /
  `mountCatalog` → a `KitMount` with lenses, collapse gestures, regions,
  `exportSVG`). **Regen-wholesale** from
  `visualizing/graphs/dist/kit-proof.js` — never hand-edit.
- `kit.css` + `tokens-proof.css` + `tokens-lattice.css` — kit-owned
  host styles + the per-app token overlays, copied verbatim from
  `visualizing/graphs/kit/`. The kit overlays are themselves
  byte-mirrors of the brand SoT at `rendering/brand/tokens/quantapix/
  overlay/{lattice,proof}-dark.css` (this app consumes the **dark**
  slice) — edits originate at the rendering SoT, never these copies.
- `pages.css` — **app-owned** page-shell styles (zones, pills,
  inspector; the `--proof-*` vars absorbed from the retired designer
  kit). Not part of the kit re-sync.
- `loader.js` — **app-owned never-fold side-car**. Exposes
  `ProofGraphKit.mountRun({host, graph, inspector, debug, synthetic,
  lattice, nav, navLabels})`: lazy-injects `kit.js` when the host enters the
  viewport (the visualizing § 10 payload rule), mounts `QViz`, wires the
  tap-a-leaf inspector, sets `body[data-ready]` (the e2e anchor), and
  publishes `window.__G2M__`. Schema seams live HERE — never in kit.js.

**Navigator pane (navigator-2026-07-20 §§ 3/5 adoption, ns verifying/9).**
Each graph-mount page carries an app-owned `<aside class="zone-nav"
id="proof-nav">`; `mountRun` passes `nav`/`navLabels` through and, gated on
`QViz.graphsCaps().navigator` (presence, never version-sniff — § 3.6), calls
`QViz.renderNav(nav, m, …)` so the kit renders an ARIA tree into it and wires
the § 3.5 unified selection bus (tree ↔ canvas ↔ inspector). Styling is
app-owned in `pages.css` (`.zone-nav .qgnav-*`, ported from the code/web
scaffold — verifying is a bespoke mount, not a scaffold consumer). The
`.app:has(.zone-nav)` grid adds a left nav column; nav-less pages render
byte-identical. Phone (≤900px) hides the pane (`display:none`) — the DOM/text
stays for the F1 leak-guard. A stale `kit.js` (pre-navigator) degrades to no
pane, never an error. e2e: the `navigator pane` describe in
`proof-graph.spec.ts` extends the F1 forbidden-runs floor to the nav tree text.

**Layout head slot.** Pages inject the three CSS files via
`Layout.astro`'s `<slot name="head" />`. General rule:
`[[feedback_layout_head_slot_for_per_page_links]]`.

**This mount is DARK-ONLY and owes NO light overlay (operator-ruled
2026-08-07).** The kit ships `tokens-{lattice,proof}-light.css` and
`ns:visualizing/7` has twice listed them as owed here; they are not. R-T2 (§ 3)
is the rule — kit canvas + overlays stay DARK in both legs, only page chrome
flips — and `theme.spec.ts` enforces it (`.zone-canvas` kernel-dark under
`colorScheme: 'light'`). Copying a light overlay in would land a tracked file
nothing links and R-T2 forbids linking: the inert-overlay hazard inverted,
silent, every gate green. The remaining light-leg debt is **evaluating's alone**.
Correcting reciprocal: `ns:visualizing/51`. Re-propose only by re-opening R-T2
itself, which is a debate-lane change touching § 3, `theme.spec.ts` and
evaluating's twin — never a "for parity" copy.

**No `tokens-chart.css` here is deliberate**, not a third missing overlay:
`kit.js` carries the `QViz.charts.*` namespace for the C3 `/lattice` panel, and
charts resolves `s.tok(…) || DEFAULT_TOKENS[…]`, so the panel self-themes dark
by design.

**Re-sync from a rebuilt kit** (run from the repo root):

1. `pnpm -C visualizing/graphs typecheck && pnpm -C visualizing/graphs gates`
2. `node visualizing/graphs/kit/build.mjs` — always run it (canonical `dist/` is
   gitignored and lags `src/`), but **grade staleness by `md5`, never by mtime**:
   a `visualizing/graphs` commit newer than `dist/` does NOT imply a stale
   bundle. 2026-08-07: two commits (W6 Phase 1+2) postdated the build and the
   rebuild was byte-identical — W6 never touched the kit entry graph, so only
   the *mount* was stale.
3. `cp visualizing/graphs/dist/kit-proof.js verifying/web/public/graphs/kit.js`
4. `cp visualizing/graphs/kit/{kit.css,tokens-proof.css,tokens-lattice.css} verifying/web/public/graphs/`
5. `pnpm -C verifying/web verify` + `pnpm -C verifying/web test:e2e`.

**Steps 3 and 4 are a lockstep pair — never one without the other.** The
overlay and the bundle drift independently: a token added to
`tokens-*.css` does nothing until `kit.js` is re-copied from a fresh
canonical `dist/` (`colorTok(tok, '--edge-feedback', '--edge')` fails SOFT
to the fallback — no error, no lint, no failing test; bitten 2026-07-14).
After any token lift, grep the mounted `kit.js` (`grep -a`) for the new
token name before treating the lift as landed.

**Empty-state overlay pointer-trap (check on any mount edit).** Scope the
overlay to `.empty:not([hidden])` — a bare `.empty{display:flex}` defeats the
UA `[hidden]` rule and pointer-traps the live cytoscape canvas; add an overlay
`toBeHidden()` e2e guard on live mount. Detail:
`[[reference_hidden_attr_overlay_pointer_trap]]`.

## 9. Hosting target

Local dev: `astro dev` on `:4321` + `uvicorn` on `:8787` with a Vite proxy.
Prod: static shell on S3+CloudFront at `qnarre.quantapix.com`, server on EC2
behind Caddy at `api.qnarre.quantapix.com` (per `data/specs/serving-2026-05-26/SPEC.md` § 2
decision 3). Same code in both modes; only the API origin in
`astro.config.mjs` env changes.

**Static-shell deploy** — `aws-vault exec qagents-deploy -- pnpm
-C verifying/web deploy` (rides `serving/scripts/deploy-site.sh` +
`serving/sites/qnarre.quantapix.com.env`). Bucket/cert, cross-site contract,
CF functions, 404 mapping, IAM: `serving/CLAUDE.md` § 8.

## 9.5. e2e (Playwright)

Suite at `verifying/web/tests/e2e/` on **port 4326**; stack shape (three
projects, `webServer`, run commands) is the root-CLAUDE.md § Playwright
contract. Live mode: `PW_BASE_URL=https://qnarre.quantapix.com pnpm test:e2e`
— against the deployed shell + `api.qnarre.quantapix.com` FastAPI.
`api.spec.ts` is gated on `PW_BASE_URL` (no FastAPI under `astro preview`);
the API origin defaults to `base.replace(qnarre. → api.qnarre.)`, override via
`QNARRE_API_ORIGIN=…`.

Spec partitioning:

- `site.spec.ts` — routes / brand / 404 / nav / external-link safety / PII
  blacklist (retired brand names, operator address/phone/email), plus the **flex-row
  spacing floor**: a DISCOVERING sweep (not a selector list) over every
  `display:flex` + `justify-content:space-between` row on 8 routes — the three
  static pages, `/app` hydrated, and the kit mounts — asserting `b.left -
  a.right >= 4px` between same-line children and that no child escapes a
  non-scrollable parent. `space-between` is distribution, never spacing: with
  no `gap` two grown children degenerate to 0px and read as overlapping text
  while every overflow gate stays green, because **overlap is not overflow**.
  Witness (keep it working): removing the `.stream-head` gap must red at phone
  width with `stream-head: gap 0.0px between children 0 and 1`.
- `frameworks.spec.ts` — locks the proving/-derived 3-row taxonomy
  contract. `EXPECTED_FRAMEWORKS` here mirrors `FRAMEWORK_META` in
  `web/src/lib/frameworks.ts` — edit both in lockstep when a statute lands.
  Predicate counts use a floor (`minPreds`) so adding a predicate file
  doesn't break the spec.
- `proof-graph.spec.ts` — lobby cardinality + graphs kit-mount
  (`data-ready` + cytoscape canvas) on `01-rico`, `02-debug`, the single
  F1-gated `sample` run (+ its `/debug/`), and `/lattice/`. Carries the F1
  leak-guard: `FORBIDDEN_RUNS` (`<live-matter>_*`, `titlevi_sample`,
  `titlevii_fedsector_refused`) must 404 and never appear on the lobby
  (mirrors `isPublicWorkedRun` in `web/src/lib/public-runs.ts`). Every
  replay-API-servable non-RICO id belongs in that list — API-servable and
  publicly-worked are different floors, and only the second is F1-gated.
- `app.spec.ts` — `client:only` island hydration, chip set + click behaviour,
  plus the F1 floor: RICO-only demoed (default chip), non-demoed chips render
  "encoded · not demoed" with no verdict/Boolean, the synthetic demo ends
  REJECT, and the disclaimer is a sibling of every verdict.
- `theme.spec.ts` — M4 Meridian tri-state theme (dual-signal flip both ways +
  persistence, System clears the override, kernel-dark canvas in the light
  leg per R-T2, Newsreader display ramp).
- `api.spec.ts` — live-only; `ALLOWED_IDS` here is leg 2 of the § 7
  allow-list lockstep triple.

## 10. Scope boundary

This subproject does not import from `analyzing/`, `trading/`, `evaluating/`,
or `designing/`. The only allowed reach across subprojects is the server
adapter calling `../proving/scripts/extract_facts.py` as a subprocess.

## 11. Status emit (`data/status/verifying.json`)

`verifying/scripts/status_emit.py` writes the Qnarre app-shell diagram +
live-state to `data/status/verifying.json` for the qagents-wide Status
page on quantapix.com. The slot's `productBrand: 'Qnarre'` flips the
quantapix.com card label to `Qnarre` (teal accent). Status pill `OK` when
both `https://qnarre.quantapix.com/` and
`https://api.qnarre.quantapix.com/api/health` return 200 (probe is a 5s
urllib GET). `WARN` if one is up and the other isn't; `ERROR` if neither.
