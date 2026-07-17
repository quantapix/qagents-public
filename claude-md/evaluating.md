# CLAUDE.md — evaluating/ (Qresev)

Project-specific rules for the Qresev app at `qresev.quantapix.com`. Sibling
of `verifying/` (Qnarre). Wraps the `accounting/` Lean4 + LLM-predicate
kernel — the financial-domain parallel of `proving/`. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`.

## 1. Layering — strict, like proving/

| Layer | Where | Reads | Writes |
|---|---|---|---|
| **Web shell** | `web/` (Astro + React island) | HTTP + SSE | rendered UI |
| **App server** | `server/` (FastAPI in qagents root .venv) | portfolio JSON, manifest | spawns accounting driver as subprocess |
| **Kernel** | `../accounting/` | manifest + portfolio | `Facts.lean` + audit JSON |

The web shell never imports from `../accounting/` or `../analyzing/`. The
server adapter calls the accounting driver as a subprocess and reads its
outputs. accounting/ reads its OHLCV via the shared `financial/parquet/`
hub (not analyzing's DuckDB directly) — so this subproject too only ever
sees `financial/` parquet and the adapter's subprocess outputs.

## 2. Design SoT + brand mechanism (Meridian since M4)

**Since 2026-07-11 (web-unification M4) the web rides the Meridian layer,
BRAND-VIA-HOST:** design SoT is the adopted CD-B bundle at
`rendering/designs/evaluating-web/` (Qresev slice + ADOPTION.md floors; the
old `data/renders/evaluating-design/` bundle + its two-drift sweep are
RETIRED for this site). Brand values never enter this tree:
`web/scripts/sync-meridian.mjs` (pre-hooks) host-copies the W5 css layers
from `code/web/css/meridian/`, the font trio from `rendering/brand/fonts/`,
and composes the dual-signal `/meridian-tokens.css` from the rendering SoT —
all gitignored under `public/`. `<body class="m-body m-app-qresev">` binds
the copper accent; tri-state theme via `@qagents/web/theme` (the
`color-scheme: dark` meta retired). Shared chrome/island shells come from
`@qagents/web` (W2 TopNav/BracketedQ/DisclaimerCallout; W4 TraceRail/ConfBar/
PredicatesTable/StructureView/ReportZone/useRunData) with copy from
`src/content/copy.ts` (fail-loud); app-owned and non-extractable: the
verdict⇄disclaimer SIBLING composition, the defined-risk audit, the
judgments roster, the Sparkline panels. **FINANCIALLY (R-T2):** the
defined-risk allow-list renders in the **copper accent wash — never
verdict-green** ("kernel refusal, never a safety guarantee"); refused legs
keep the fails treatment with ✗; the financialRider's per-leg visibility +
adjacency is asserted in `tests/e2e/theme.spec.ts`. Token boundary: no raw
values outside `public/tokens.css` (LAYOUT-ONLY since M4) + the generated
`public/meridian-tokens.css`; lint = the composed
`code/web/scripts/lint-tokens.sh` + `web/lint-tokens.conf` (old
`web/scripts/lint-tokens.sh` retired).

**Bundle-mounting pattern — RECOMPOSED strategy mount.**
`evaluating/web/public/graphs2/` mirrors `verifying/CLAUDE.md` § 8 (kit-owned
files, regen-wholesale, app-owned `pages.css` + never-fold `loader.js`,
head-slot linkage, re-sync recipe) with these deltas: `kit.js`
regen-wholesale from `visualizing/graphs/dist/kit-strategy.js` — graphs
DAG + `@qagents/charts` overlays/side-view + the `@qagents/compose` router
under one `QViz` global; plus `tokens-chart.css` (from
`visualizing/charts/kit/`). `loader.js` exposes `StrategyKit.mountRun({host,
overlayLayer, sideHost, graph, report, runId})`: mounts the DAG, backs the
router's opaque `RegionSource` with the `KitMount`
(regions/onLayout/onTapLeaf), adapts report.json → the charts `QReport` (only
predicates carrying `extras` yield overlay tiles), injects `resolveBars` =
`GET /api/runs/<id>/bars` (§ 6), preserves the
`postMessage({type:'sc:predicate-selected', sel})` contract for the `/app`
REPORT zone, and sets `body[data-ready]`. Per-run pages at
`web/src/pages/strategy-chart/run/[id]/`. The dist is gitignored
canonical-only and lags after a visualizing `/close` — **rebuild at canonical
first**, then cp; verify the re-sync **behaviorally**
(`window.__G2M__.counts()` / `expandAll()`), not by grep. Parity gate vs the
fused render is structural — e2e asserts the full report predicate set on the
DAG + the selection round-trip.

**`tokens-*.css` and `kit.js` are a LOCKSTEP pair — re-copy both or neither.**
A lifted token overlay is **inert** if this mount's `kit.js` predates the
consumer that reads the token: an undefined custom property resolves to `''` and
the kit falls through to its `||` fallback. Nothing catches this — `pnpm verify`
(typecheck + lint + build) relates a `public/` CSS file to a `public/` JS blob
not at all; both are opaque static assets. Bit us 2026-07-14: visualizing lifted
`--chart-overlay-projected` + `--edge-{feedback,veto}` byte-perfect, and all
three stayed dead against a stale `kit.js` — the projected ghost rendering in the
ACTUAL SERIES COLOR on a financial surface. Verify by asking the **live mount**
what it computed (`getComputedStyle(document.documentElement)` under `pnpm
preview`), never by asking the build whether it succeeded.
`[[feedback_two_token_mirrors_ship_two_palettes]]`

**lint-tokens caveat** — `public/graphs2/` is excluded via
`web/lint-tokens.conf` `EXCLUDE_DIRS` (disjoint kit-token namespace);
never hand-edit kit files to placate the lint.

**Empty-state overlay pointer-trap** — same check as `verifying/CLAUDE.md`
§ 8 on any mount edit (`[[reference_hidden_attr_overlay_pointer_trap]]`).

## 3. App surface is one big React island

`/app` is a single full-height React island
(`web/src/islands/QresevApp.tsx`) with three persistent zones: PORTFOLIO
(28%) · AGENT STREAM (36%) · EVALUATION REPORT (36%).

**Three patterns inherited from `verifying/`** (side-car `loader.js`,
per-run static pages via `getStaticPaths`, three-tab REPORT zone with
`?id=<runId>` showing Predicates / Structure / Strategy-graph). The
contracts come from `data/specs/proving-results-propagation-2026-05-09/SPEC.md`;
the worked references live at `verifying/CLAUDE.md` §§ 5, 7, 8 and the
evaluating-instance detail (`loader.js` schema adapter + the
`postMessage({type: 'sc:predicate-selected', sel})` selection forwarding)
is pinned in memory `project_proof_graph_kit_mount_pattern` Instance 2.
Structure-tab failure-loci block falls back to `kernel.errors[].raw`
when `termHasType` is empty.

**Quantapix Thesis disclaimer (T3).** `copy.ts` exports `disclaimer`
(`canon` + `financialRider`) — byte-identical to designing/web's `copy.ts`
SoT (distilled from `studying/thesis.md`). The shared `@qagents/web` DisclaimerCallout (bound here to
`disclaimer.financialRider`) renders it ADJACENT to the verdict token in
BOTH `LiveReportZone` and the static `ReportZone`, so the concession
travels with the verdict.
Preserve this on any REPORT-zone edit (`app.spec.ts` asserts it). § 11.6:
the `financialRider` is the operator/evaluating+accounting track, NOT
pleading's gate — and as of 2026-06-24 `evaluating/` **owns** that track
(§ 9, the FINANCIALLY-CLEARED gate). Cure: Round 03 T3 + cure 5,
`data/debates/quantapix-thesis-public-pages-2026-06-23.md`.

## 4. Defined-risk options — non-negotiable

The UI itself refuses to construct any options leg outside the allow-list
(long calls/puts, debit spreads, covered calls, protective puts). This
matches the qagents brand-level invariant from
`trading/shared/skills/options-risk/SKILL.md` and is enforced visually on
`/app` and `/frameworks` (allow-list in teal, refused-list in amber).

## 5. Frameworks scope

TREND · MOMENTUM · OPTIONS-RISK · SECTOR · DRAWDOWN. Each maps to an
`Accounting.<Framework>` module in the kernel. Adding a framework is
parallel to proving/'s "Adding a new framework" workflow — kernel first,
predicate roster second, UI chip third.

**Taxonomy seam** — mirrors `verifying/CLAUDE.md` § 6 with
`accounting/predicates/<id>/` as the authoritative set and
`FRAMEWORK_META[<id>] = { label, module }` (module, not cite) in
`web/src/lib/frameworks.ts`; all consumers go through `loadFrameworks()`.
Adding a framework = one entry after the matching predicate dir lands.

## 6. Server scope

v0.1 is **replay-only for POST** (sibling parity with verifying/). POST
`/api/runs` body is `{example_id}` from a closed allow-list
`{hawk_sample, single_ticker_sample, balance_sample}`
(`balance_sample` is the brand-anchor — 4 frameworks since the
2026-06-03 MOMENTUM drop; see its manifest comment); the adapter shells
`extract_facts.py --stub` against `accounting/examples/<id>/`,
overwriting `{report,graph,loci}.json` in place. accounting/'s driver
carries `--reuse-facts` + `--build` (proving parity), but `--stub` stays the
replay mode — cost-free predicate values, instant canned Bools against the
committed manifest. Driver also honors a per-call `inputs.stub: true`
override that forces stub on a single predicate even when global
`--stub` is off — additive. The driver then invokes **real** `lake build
examples.<id>.proof` (not `lake env lean`) so the kernel verdict is
genuine. Stub values are seeded from the example's committed `facts.json`,
keyed on `(spec, lean_call)`, whenever the adapter passes `--example-id` (it
does) — so a replay is value-faithful to the real Opus run that produced the
golden. If the kernel
rejects, the report exposes the Lean error verbatim. Read endpoints keep
the hybrid `_resolve_run_dir` shape
(`server/jobs/` first, then `accounting/examples/`) so any historical
live-job artefacts remain readable.

Endpoints: `POST /api/runs` · `GET /api/runs` (lists jobs + examples
with current verdicts) · `GET /api/runs/<id>/stream` (SSE, typed
events per propagation spec § 5.4) · `GET /api/runs/<id>/report` ·
`GET /api/runs/<id>/graph` · `GET /api/runs/<id>/loci` ·
`GET /api/runs/<id>/bars?ticker=&range=` (the recomposed strategy
mount's `resolveBars` seam — pyarrow over
`financial/parquet/ohlcv-equities/`, emits the charts-kit OHLCV wire
shape `{ts(ms),o,h,l,c,v}`; ranges `1m/3m/6m/1y/2y` only; EC2
provisioning of pyarrow + the parquet tree: `serving/CLAUDE.md` § 8.5).
The server makes no financial judgments and does not place orders. Qresev
evaluates; it does not execute.

CORS: `https://qresev.quantapix.com` + `http://localhost:4322`.

**Privacy floor — Promise 3 satisfied by construction.** Replay-only
means no user portfolio data reaches LLM or kernel; the only portfolio
ever processed is the curated `examples/<id>/portfolio.json` which is
already PII-free (synthetic holdings). Donating drive's POST refusal
binding (`../donating/drive.md` Promise 3) honored without any
redaction code. Revisit if admin-gated freeform POST lands.

## 7. Hosting target

Local dev: `astro dev` on `:4322` + `uvicorn` on `:8788`. Prod: static shell
on S3+CloudFront at `qresev.quantapix.com`, server on EC2 behind Caddy at
`api.qresev.quantapix.com` (per `data/specs/serving-2026-05-26/SPEC.md` § 2 decision 3).

**Static-shell deploy** — bucket `qresev.quantapix.com`, CloudFront
`E2PFH4Z95BT169`, wildcard `*.quantapix.com` cert. Invocation:
`aws-vault exec qagents-deploy -- pnpm -C evaluating/web deploy`
(rides `serving/scripts/deploy-site.sh` + `serving/sites/qresev.quantapix.com.env`).
Single managed IAM policy at `serving/policies/qagents-deploy.json`.
Cross-site contract in `serving/CLAUDE.md` § 8.

**e2e (Playwright).** Suite at `evaluating/web/tests/e2e/` on **port 4324**;
stack shape is the root-CLAUDE.md § Playwright contract. Live mode:
`PW_BASE_URL=https://qresev.quantapix.com pnpm test:e2e` — against the
deployed shell + `api.qresev.quantapix.com` FastAPI. `api.spec.ts` is gated
on `PW_BASE_URL` (no FastAPI under `astro preview`); the API origin defaults
to `base.replace(qresev. → api.qresev.)`, override via `QRESEV_API_ORIGIN=…`.

Spec partitioning:

- `site.spec.ts` — routes / brand / 404 / nav / external-link safety /
  PII blacklist (retired brand names, operator address/phone/email).
- `frameworks.spec.ts` — locks the accounting/-derived 5-row taxonomy
  contract. `EXPECTED_FRAMEWORKS` mirrors `FRAMEWORK_META` in
  `web/src/lib/frameworks.ts` — edit both in lockstep when a framework
  lands. Predicate counts use a floor (`minPreds`).
- `strategy-chart.spec.ts` — recomposed kit-mount (`data-ready` +
  cytoscape canvas) on three spot-check runs
  (`balance_sample`/`hawk_sample`/`single_ticker_sample`) + the
  structural parity gate (report predicate set ↔ DAG nodes) + the
  `sc:predicate-selected` round-trip + `<head>` linkage of the
  graphs2 CSS set.
- `app.spec.ts` — `client:only` island hydration, 5-chip set + click +
  the OPTIONS-RISK lock panel.
- `api.spec.ts` — live-only; `ALLOWED_IDS` mirrors `ALLOWED_EXAMPLE_IDS`
  in `server/main.py` AND `extending/servers/qresev-mcp/src/allowlist.ts` — a
  **triple** since extending landed 2026-07-04, all exhaustive by design; edit
  in lockstep (the extending parity test fails until all three match).

**EC2 server deploy** — `aws-vault exec qagents-deploy -- bash
serving/scripts/deploy-app.sh qresev`. Tarball = `evaluating/server/` +
the sibling accounting/ kernel (composition owned by `deploy-app.sh`).
Rotation mechanics, `.lake` cache migration, systemd NAMESPACE preflight,
elan/toolchain bootstrap: `serving/CLAUDE.md` § 8.5
(live-state drift tracked in `data/next-steps/serving.md`). Qresev-facing
trap: the unit's `ReadWritePaths` must include `/srv/qagents/.elan` — the
elan shim rewrites `settings.toml` on activation, so without it lake dies
~0.04s in and every live run returns a spurious REJECTED with empty
`kernel.errors`. [[project_ec2_lean_kernel_install]]
[[feedback_kernel_rotation_cache_hazard]]

## 8. Scope boundary

This subproject does not import from `analyzing/`, `trading/`, `verifying/`,
or `designing/`. The only allowed reach is the server adapter calling
`../accounting/scripts/...` as a subprocess (and reading
`financial/`-namespaced parquet via the kernel, not the web shell).

## 9. Financial sign-off — `evaluating/` is the constellation grantor

`evaluating/` owns the **financial sign-off** (the FINANCIALLY-CLEARED gate) —
the financial-domain analog of `pleading/`'s litigation-safety gate. Adopted
2026-06-24 from a lifted publishing charter; spec
`data/specs/evaluating-financial-signoff-2026-06-24/SPEC.md`. It is the single
gate that clears (or blocks), on financial-advice / securities-liability
grounds, any **public** surface that evaluates, recommends, or implies a
financial decision. `evaluating/` is the **sole grantor**; `accounting/`
**advises** (frameworks/kernel truth), it does not grant.

**Recording a grant.** Each granted/blocked sign-off lands as a dated record in the
spec's **§ 9 sign-off ledger** (`data/specs/evaluating-financial-signoff-2026-06-24/signoffs/<date>-<subject>.md`),
kept in evaluating's own family — never in `pleading/`'s `messaging-rulings/` (the
§ 5 orthogonality). First entry: `signoffs/2026-06-30-4.1-ta-bestiary.md`. A consumer
cites it (manifest + release commit) before any public push. The generic version of
this machinery is **ADOPTED**: the `/do-signoff <gate> <subject>` skill
(`.claude/skills/do-signoff/` — FINANCIALLY-CLEARED is its first governing instance,
resolver refuses unless the session IS the grantor) over the governance-layer spec
`data/specs/signoff-framework-2026-06-30/SPEC.md`, with provable `lake build`
verification (studying S-T10 `SignoffCoverage`). Grant a FINANCIALLY surface with
`/do-signoff FINANCIALLY <subject>` from this session; the 4.1 record carries the
§ 5 structured core as the worked example. See `[[project_signoff_framework]]`.

**Scope:** spec § 3 (FINALIZED) — Qresev surfaces + any public surface
evaluating stocks/portfolios/options with actionable framing; internal
artifacts and a returns-free `/donate` are out.

**FINANCIALLY-CLEARED iff (§ 4 of the spec):** the `financialRider` is present +
adjacent to **every** TREND/MOMENTUM/OPTIONS-RISK/SECTOR/DRAWDOWN verdict token
(not just an intro); no actionable-counsel language ("advice"/"recommendation"/
"buy"/"sell"/"should"/return-promise/"guarantee" — the rider's own *negated*
uses are exempt); the allow-list is framed "a kernel refusal, not a safety
guarantee" (never "safe"); `disclaimer.canon` is verbatim; the rider is
**byte-equal** to the `disclaimer.financialRider` export across all faces, and
the `description`-strip face is concession-safe standalone. Intra-app faces are
asserted by `app.spec.ts`; cross-repo faces by the publishing `github_meta.py`
lint. **Video payloads** with on-screen verdict tokens: full rider baked-persistent
per the signoff-framework registry row + § 3 inv-7 (source-layer check, before
the master render — `[[feedback_gate_source_before_expensive_render]]`).

**A green mechanical gate is NOT a grant (load-bearing).** The scanners
(`lib/scan_financial.sh`) and explaining's `phase0_preflight.py --rider-floor`
prove rider *presence + byte-equality* only. Neither can see **CLEAR-5 (R10)** —
binding each framework verdict token to a committed `accounting/` run-emit — which
is a **judged** clause (skill § 5). `--rider-floor` also reads `_design.tsx` + a
hand-maintained per-topic `VERDICT_COMPONENTS` list, never `design.md`, though
`design.md` **is** a reviewed face whose sha enters `content_sha256`. 3.6
`live-evaluator-walkthrough` is the worked counterexample: mechanically green,
**BLOCKED** 2026-07-10 (`signoffs/2026-07-10-3.6-live-evaluator-walkthrough.md`).
Necessary, never sufficient.

**CLEAR-5 run-binding rule (video payloads).** A verdict token on a frame that
**names an example run** binds to *that run's* emit; a token naming no run (a
cameo, or a synthetic book) binds to the committed framework. `balance_sample`
emits **four** frameworks / five judgments — no MOMENTUM (manifest: "not honestly
provable here"), DRAWDOWN = `discipline_breached` — and **no example emits all
five**. The correct on-screen grammar for an absent framework is 3.3
`G6Triad33`'s three-valued cell (`pos` / `neg`+word / `none` = `— not claimed`,
same weight as a verdict). See `[[project_cohort3_financial_signoff_rider_floor]]`.

**Orthogonal to `pleading/` (load-bearing):** never a substitute for the
litigation gate. Where both apply, a surface needs **both** clears; a green
`pleading/` line is not a financial sign-off and vice-versa (messaging-debate
§ 11.6). `evaluating/` is the **V8 owner/gate** in the messaging-hardening
debate (`shorting/` prosecutes; `pleading/` retains the litigation vectors).

## 10. Status emit (`data/status/evaluating.json`)

`evaluating/scripts/status_emit.py` writes the Qresev app-shell diagram +
live-state to `data/status/evaluating.json` for the qagents-wide Status
page on quantapix.com. The slot's `productBrand: 'Qresev'` flips the card
label to `Qresev` (amber accent). Defined-risk options invariant must be
reflected in `cardSummary`. Status pill `OK` when both the static shell
deploys green AND `api.qresev.quantapix.com/api/health` returns 200.
