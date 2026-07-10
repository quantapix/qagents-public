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

## 2. Design bundle is read-only; regen workflow

`data/renders/verifying-design/` (under the qagents shared-data hub
`data/renders/`) is the handoff bundle slot from Claude Design, regenerated
wholesale. Never hand-edit. The `Qnarre App.html` prototype is the visual
source of truth; `web/` is the production port.

When re-syncing tokens.css from the bundle (run from the repo root):

1. `cp data/renders/verifying-design/project/colors_and_type.css verifying/web/public/tokens.css`
2. Normalize — the designing § 2 two-drift sweep, **mandatory**: replace the
   raw retired-brand-name header with the provenance header already in the deployed
   file, and delete the Google-Fonts CDN `@import` block (fonts are
   self-hosted via `@fontsource` in `Layout.astro`). Shipping the raw copy
   re-imports the banned brand string + the CDN-timing flake (rendering-spec
   debate, ruling V2: `data/debates/rendering-spec-2026-06-09.md`).
3. `pnpm -C verifying/web verify`

Token *values* are identical to `designing/`'s normalized
`web/src/styles/tokens.css` — Qnarre does not get its own palette.
This per-consumer sweep retires when this bundle migrates to `rendering/`
intake (its P4 slot — root CLAUDE.md § `data/renders/`). The brand-mark
color difference (teal-only Qnarre BracketedQ vs. the umbrella's
teal-left/amber-right) lives in the SVG props, not in tokens.

## 3. Tokens are the only boundary for raw values

Same rule as `designing/`. No hex colors / font strings / pixel literals
outside `web/public/tokens.css`. Refer to `var(--token)` everywhere else.

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
thesis floor: `{sample, titlevi_sample}`. No `<live-matter>_*` example is
replayable — those are the operator's actual dockets ("worked examples
... not drawn from any live matter", `disclaimer.legalRider`; Round 04
debate `data/debates/quantapix-thesis-github-2026-06-23.md` G2). The
static public build is stricter still — RICO-synthetic only
(`web/src/lib/public-runs.ts`); the replay API also serves the synthetic
Title VI sample. Edit `ALLOWED_EXAMPLE_IDS` (`server/main.py`),
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
typed per `data/specs/proving-results-propagation-2026-05-09/SPEC.md` (adopted)
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
this layer. Revisit when admin-gated freeform POST lands; admin-gated
freeform requires the rule set from `legal/public/` staging (already in
use for `documenting/`).

## 8. Proof-graph kit (Lean4 DAG visualisation) — graphs-2 mount (G6)

Since 2026-06-11 the proof-graph surface renders via the domain-neutral
**graphs-2 kit** from `visualizing/` (the unified kit-mount that also
backs Qresev's strategy mount — visualizing spec
`data/specs/visualizing-2026-06-03/graphs2-2026-06-07/SPEC.md` G6). Routes:

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
  (cells collapsed, agreement lens, `tokens-lattice.css`).

**F1 thesis-floor gate (named-never-worked).** The textual axis is *named,
never worked* in any public material, and no public worked example is drawn
from a live matter (`disclaimer.legalRider`; SoT `studying/thesis.md`). So the
public build's only worked proof-DAG run page is the **synthetic civil-RICO
sample** (`sample`). `web/src/lib/public-runs.ts` (`isPublicWorkedRun`) is the
single gate: it drops every non-RICO example (only `rico` is in
`frameworks.ts` `PUBLIC_DEMOED`) and every `<live-matter>_*` example (live matter,
incl. `rico-hier`). Both run pages' `getStaticPaths` AND the lobby's live-run
scan call it; the same gate backs the `/app` island chips (non-demoed →
"encoded · not demoed", no verdict/Boolean) and `LiveReportZone`. Round 04
debate `data/debates/quantapix-thesis-github-2026-06-23.md` G2; pleading/
binding (cleared 2026-06-24 — `PLEADING-GATE-DECISION-2026-06-23.md` in the
same spec family). The replay API is gated to the same floor (§ 7); residual
(intentional): it also serves the synthetic non-RICO `titlevi_sample`.

Kit files live at `verifying/web/public/graphs2/`:

- `kit.js` — the graphs-2 IIFE bundle (global `QViz`: `mountProof` /
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
  lattice})`: lazy-injects `kit.js` when the host enters the viewport
  (the visualizing § 10 payload rule), mounts `QViz`, wires the
  tap-a-leaf inspector, sets `body[data-ready]` (the e2e anchor), and
  publishes `window.__G2M__`. Schema seams live HERE — never in kit.js.

**Layout head slot.** Pages inject the three CSS files via
`Layout.astro`'s `<slot name="head" />`. General rule:
`[[feedback_layout_head_slot_for_per_page_links]]`.

**Re-sync from a rebuilt kit** (run from the repo root):

1. `pnpm -C visualizing/graphs typecheck && pnpm -C visualizing/graphs gates`
2. `node visualizing/graphs/kit/build.mjs`
3. `cp visualizing/graphs/dist/kit-proof.js verifying/web/public/graphs2/kit.js`
4. `cp visualizing/graphs/kit/{kit.css,tokens-proof.css,tokens-lattice.css} verifying/web/public/graphs2/`
5. `pnpm -C verifying/web verify` + `pnpm -C verifying/web test:e2e`.

**lint-tokens caveat.** `public/graphs2/` is excluded from
`scripts/lint-tokens.sh` (both passes) — the kit bundle + the kit-owned
token-overlay DEFINITIONS legitimately carry raw values, same exclusion
class as Qresev's kit dir. Never hand-edit kit files to placate lint.

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

**Static-shell deploy** — bucket `qnarre.quantapix.com`, wildcard
`*.quantapix.com` cert. Invocation: `aws-vault exec qagents-deploy -- pnpm
-C verifying/web deploy` (rides `serving/scripts/deploy-site.sh` +
`serving/sites/qnarre.quantapix.com.env`). Cross-site contract, CF functions,
404 mapping, IAM: `serving/CLAUDE.md` § 8.

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
  blacklist (retired brand names, operator address/phone/email).
- `frameworks.spec.ts` — locks the proving/-derived 3-row taxonomy
  contract. `EXPECTED_FRAMEWORKS` here mirrors `FRAMEWORK_META` in
  `web/src/lib/frameworks.ts` — edit both in lockstep when a statute lands.
  Predicate counts use a floor (`minPreds`) so adding a predicate file
  doesn't break the spec.
- `proof-graph.spec.ts` — lobby cardinality + graphs-2 kit-mount
  (`data-ready` + cytoscape canvas) on `01-rico`, `02-debug`, the single
  F1-gated `sample` run (+ its `/debug/`), and `/lattice/`. Carries the F1
  leak-guard: `FORBIDDEN_RUNS` (`<live-matter>_*`, `titlevi_sample`) must 404 and
  never appear on the lobby (mirrors `isPublicWorkedRun` in `web/src/lib/
  public-runs.ts`).
- `app.spec.ts` — `client:only` island hydration, chip set + click behaviour,
  plus the F1 floor: RICO-only demoed (default chip), non-demoed chips render
  "encoded · not demoed" with no verdict/Boolean, the synthetic demo ends
  REJECT, and the disclaimer is a sibling of every verdict.
- `api.spec.ts` — live-only; `ALLOWED_IDS` here mirrors
  `ALLOWED_EXAMPLE_IDS` in `server/main.py` — both are exhaustive by
  design, edit in lockstep.

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
