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

## 2. Design bundle is read-only; regen workflow

`data/renders/evaluating-design/` (under the qagents shared-data hub
`data/renders/`) is the handoff bundle slot from Claude Design, regenerated
wholesale. Never hand-edit. The `Qresev App.html` prototype is the visual
source of truth.

When re-syncing tokens.css from the bundle (run from the repo root):

1. `cp data/renders/evaluating-design/project/colors_and_type.css evaluating/web/public/tokens.css`
2. **Two-drift sweep (mandatory — the bundle ships raw):** rewrite the
   header comment to the normalized shape (no retired brand names, evaluating-design
   provenance) and delete every Google-Fonts CDN `@import` (live + the
   commented usage line). Fonts are self-hosted via `@fontsource` in
   `Layout.astro` (superset of the CDN set), so the sweep is
   zero-regression. Acceptance: a case-insensitive grep for the retired brand name + the fonts CDN returns 0.
   Mirrors designing/CLAUDE.md § 2; retired when rendering/'s
   normalize-at-intake lands (rendering-spec debate EV2/DS1,
   `data/debates/rendering-spec-2026-06-09.md`).
3. `pnpm -C evaluating/web verify`

Tokens are identical to `designing/`'s normalized
`web/src/styles/tokens.css` below the header comment (provenance lines
differ — diff from `:root {` to verify). Qresev's brand-mark color
(amber-only BracketedQ) lives in SVG props, not in tokens.

**Bundle-mounting pattern — RECOMPOSED strategy mount (2026-06-11).**
The fused designer strategy-chart kit is retired (git history preserves
it). The kit at `evaluating/web/public/graphs2/` is the **composed
visualizing bundle**: `kit.js` = graphs-2 DAG + `@qagents/charts`
overlays/side-view + the `@qagents/compose` router under one `QViz`
global, regen-wholesale from `visualizing/graphs-2/dist/kit-strategy.js`
— never hand-edit. Beside it: `kit.css` + `tokens-proof.css` (kit-owned,
from `visualizing/graphs-2/kit/`; the kit overlay itself byte-mirrors the
brand SoT `rendering/brand/tokens/quantapix/overlay/proof-dark.css` — this
app consumes the **dark** slice, edits originate at the rendering SoT),
`tokens-chart.css` (from
`visualizing/charts/kit/`), `pages.css` (app-owned page chrome) and the
**app-owned never-fold `loader.js` side-car**
(`StrategyKit.mountRun({host, overlayLayer, sideHost, graph, report,
runId})`): lazy-injects kit.js, mounts the DAG, backs the router's
opaque `RegionSource` with the `KitMount` (regions/onLayout/onTapLeaf),
adapts report.json → the charts `QReport` (only predicates carrying
`extras` yield overlay tiles — they light up as the accounting run-emit
grows extras), injects `resolveBars` = `GET /api/runs/<id>/bars` (§ 7),
preserves the `postMessage({type:'sc:predicate-selected', sel})`
contract for the `/app` REPORT zone, and sets `body[data-ready]`.
Layout.astro carries the `<slot name="head" />`; per-run pages live at
`evaluating/web/src/pages/strategy-chart/run/[id]/`. Re-sync mirrors
`verifying/CLAUDE.md` § 8 (build graphs-2 → cp `kit-strategy.js` →
`pnpm verify` + e2e). The dist is gitignored canonical-only and lags after a
visualizing `/close`, so **rebuild it at canonical first**, then cp; verify the
re-sync **behaviorally** (`window.__G2M__.counts()` / `expandAll()`), not by
grep — a `derived:` marker false-positives on a pre-nesting bundle. Parity gate vs the fused render is structural —
the e2e suite asserts the full report predicate set on the DAG + the
selection round-trip.

**lint-tokens caveat.** `public/graphs2/` is excluded from
`evaluating/web/scripts/lint-tokens.sh` (both passes) — the kit bundle +
the kit-owned token-overlay DEFINITIONS legitimately carry raw values.
Never hand-edit kit files to placate the lint.

**Empty-state overlay pointer-trap (check on any mount edit).** An absolute/inset
empty-state overlay must scope its visibility to `.empty:not([hidden])` — a bare
`.empty{display:flex}` author rule silently defeats the UA `[hidden]{display:none}`,
leaving the overlay visible with `pointer-events:auto` over the live cytoscape
canvas so the graph is uninteractive (monitoring hit + fixed this 2026-06-19).
e2e that drives the kit via its JS API won't catch it — add an overlay
`toBeHidden()` guard on live mount. Detail: `[[reference_hidden_attr_overlay_pointer_trap]]`.

## 3. Tokens / copy — same as Qnarre

No raw values outside `web/public/tokens.css`. Copy in `web/src/copy.ts`.

## 4. App surface is one big React island

`/app` is a single full-height React island
(`web/src/islands/QresevApp.tsx`) with three persistent zones: PORTFOLIO
(28%) · AGENT STREAM (36%) · EVALUATION REPORT (36%).

**Three patterns inherited from `verifying/`** (side-car `loader.js`,
per-run static pages via `getStaticPaths`, three-tab REPORT zone with
`?id=<runId>` showing Predicates / Structure / Strategy-graph). The
contracts come from `data/specs/proving-results-propagation-2026-05-09/SPEC.md`;
the worked references live at `verifying/CLAUDE.md` §§ 5, 7, 8 and the
evaluating-instance detail (`loader.js` schema adapter + the
`postMessage({type: 'sc:predicate-selected', sel})` selection forwarding;
the fused-kit `t_clean`/`t_legs` id-remap retired with the 2026-06-11
recompose — § 2) is pinned in memory
`project_proof_graph_kit_mount_pattern` Instance 2.
Structure-tab failure-loci block falls back to `kernel.errors[].raw`
when `termHasType` is empty.

**Quantapix Thesis disclaimer (T3).** `copy.ts` exports `disclaimer`
(`canon` + `financialRider`) — byte-identical to designing/web's `copy.ts`
SoT (distilled from `studying/thesis.md`). `QresevApp.tsx`'s internal
`DisclaimerCallout` (React mirror of designing/web's Astro component; amber
accent) renders it ADJACENT to the verdict token in BOTH `LiveReportZone`
and the static `ReportZone`, so the concession travels with the verdict.
Preserve this on any REPORT-zone edit (`app.spec.ts` asserts it). § 11.6:
the `financialRider` is the operator/evaluating+accounting track, NOT
pleading's gate — and as of 2026-06-24 `evaluating/` **owns** that track
(§ 10, the FINANCIALLY-CLEARED gate). Cure: Round 03 T3 + cure 5,
`data/debates/quantapix-thesis-public-pages-2026-06-23.md`.

## 5. Defined-risk options — non-negotiable

The UI itself refuses to construct any options leg outside the allow-list
(long calls/puts, debit spreads, covered calls, protective puts). This
matches the qagents brand-level invariant from
`trading/shared/skills/options-risk/SKILL.md` and is enforced visually on
`/app` and `/frameworks` (allow-list in teal, refused-list in amber).

## 6. Frameworks scope

TREND · MOMENTUM · OPTIONS-RISK · SECTOR · DRAWDOWN. Each maps to an
`Accounting.<Framework>` module in the kernel. Adding a framework is
parallel to proving/'s "Adding a new framework" workflow — kernel first,
predicate roster second, UI chip third.

**Taxonomy seam.** `accounting/predicates/<id>/` is the authoritative
framework set. `web/src/lib/frameworks.ts` is evaluating/'s single
declaration site: `FRAMEWORK_META[<id>] = { label, module }` is the only
per-framework data this project owns; the predicate count comes from
the filesystem and the "updated" date from `git log`. Every consumer
(`index.astro`, `frameworks.astro`, `app.astro` → `QresevApp.tsx`) goes
through `loadFrameworks()`. Adding a framework = one entry in
`FRAMEWORK_META` after the matching `accounting/predicates/<id>/` dir
lands. Mirrors verifying/CLAUDE.md §6.

## 7. Server scope

v0.1 is **replay-only for POST** (sibling parity with verifying/). POST
`/api/runs` body is `{example_id}` from a closed allow-list
`{hawk_sample, single_ticker_sample, balance_sample}`
(`balance_sample` is the brand-anchor — 4 frameworks since the
2026-06-03 MOMENTUM drop; see its manifest comment); the adapter shells
`extract_facts.py --stub` against `accounting/examples/<id>/`,
overwriting `{report,graph,loci}.json` in place. accounting/'s driver
now carries `--reuse-facts` + `--build` (proving parity, since ffa30e46),
but `--stub` stays the replay mode — cost-free predicate values, instant
canned Bools against the committed manifest. Driver also honors a per-call `inputs.stub: true`
override that forces stub on a single predicate even when global
`--stub` is off — additive. The driver then invokes **real** `lake build
examples.<id>.proof` (not `lake env lean`) so the kernel verdict is
genuine. Since accounting `8960465a` (the `--stub` value-faithfulness
fix evaluating/ surfaced 2026-06-05) stub values are seeded from the
example's committed `facts.json`, keyed on `(spec, lean_call)`, whenever
the adapter passes `--example-id` (it does) — so a replay is value-faithful
to the real Opus run that produced the golden. If the kernel
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
shape `{ts(ms),o,h,l,c,v}`; ranges `1m/3m/6m/1y/2y` only. `pyarrow`
rides `evaluating/requirements.txt` — the rotation's pip step is the
ONLY venv-extension path, the `[evaluating]` extra never reaches EC2.
The parquet itself is shipped out-of-band: tar
`financial/parquet/ohlcv-equities/` →
`s3://qagents-artifacts/releases/qresev/ohlcv-equities.tar.gz` →
SSM-extract to `/srv/qagents/financial/parquet/` — re-run on data
refresh, the deploy tarball never carries it. Done 2026-06-12). The
server makes no financial judgments and does not place orders. Qresev
evaluates; it does not execute.

CORS: `https://qresev.quantapix.com` + `http://localhost:4322`.

**Privacy floor — Promise 3 satisfied by construction.** Replay-only
means no user portfolio data reaches LLM or kernel; the only portfolio
ever processed is the curated `examples/<id>/portfolio.json` which is
already PII-free (synthetic holdings). Donating drive's POST refusal
binding (`../donating/drive.md` Promise 3) honored without any
redaction code. Revisit if admin-gated freeform POST lands.

## 8. Hosting target

Local dev: `astro dev` on `:4322` + `uvicorn` on `:8788`. Prod: static shell
on S3+CloudFront at `qresev.quantapix.com`, server on EC2 behind Caddy at
`api.qresev.quantapix.com` (per `data/specs/serving-2026-05-26/SPEC.md` § 2 decision 3).

**Static-shell deploy** — bucket `qresev.quantapix.com`, CloudFront
`E2PFH4Z95BT169`, wildcard `*.quantapix.com` cert. Invocation:
`aws-vault exec qagents-deploy -- pnpm -C evaluating/web deploy`
(rides `serving/scripts/deploy-site.sh` + `serving/sites/qresev.quantapix.com.env`).
Single managed IAM policy at `serving/policies/qagents-deploy.json`.
Cross-site contract in `serving/CLAUDE.md` § 8.

**e2e (Playwright).** Suite at `evaluating/web/tests/e2e/`; shared
helpers at `code/playwright/shared.ts`. Three projects (chromium-
desktop / -mobile / -reduced-motion); `webServer = pnpm build && pnpm
preview` on **port 4324** (4321 = documenting, 4322 = designing, 4323 =
verifying). Run from `evaluating/web/`:

- `pnpm test:e2e` — offline against built+previewed Astro shell.
- `pnpm test:e2e:install` — one-time chromium download.
- `PW_BASE_URL=https://qresev.quantapix.com pnpm test:e2e` — against the
  deployed shell + `api.qresev.quantapix.com` FastAPI. `api.spec.ts` is
  gated on `PW_BASE_URL` (no FastAPI under `astro preview`); the API
  origin defaults to `base.replace(qresev. → api.qresev.)` and can be
  overridden via `QRESEV_API_ORIGIN=…`.

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
  in `server/main.py` — both are exhaustive by design, edit in lockstep.

**EC2 server deploy** — `aws-vault exec qagents-deploy -- bash
serving/scripts/deploy-app.sh qresev`. Tarballs `evaluating/server/` +
sibling kernel (`accounting/{scripts,predicates,examples,Accounting,
lake-manifest.json,lakefile.toml,lean-toolchain,Accounting.lean,
examples.lean}`), uploads to `s3://qagents-artifacts/releases/qresev/`,
SSM-rotates on `qagents-app-1` (resolve by `tag:Name`, never a hardcoded
instance id — the AMI-drift recreate cycle churns it). The rotation
preserves `accounting/.lake/` from `accounting.previous/` so the
incremental build cache survives redeploys. systemd unit must have
`PATH=/srv/qagents/.elan/bin:...`, `ELAN_HOME=/srv/qagents/.elan`, and
`ReadWritePaths` covering `accounting/{examples,Accounting,.lake}` **and
`/srv/qagents/.elan`** — NAMESPACE preflight hard-fails (status=226) on
any missing path. The `.elan` entry is load-bearing: the elan shim
rewrites `settings.toml` on toolchain activation, so without it lake dies
~0.04s in on a read-only-fs write and every live run returns a spurious
REJECTED with empty `kernel.errors`.

The Lean toolchain (`leanprover/lean4:v4.30.0`, 2.5 GB) installs
once at EC2 boot via `bootstrap-ec2.sh`. accounting/ is mathlib-free
so this is the only kernel dependency. Memory:
[[project_ec2_lean_kernel_install]] + [[feedback_kernel_rotation_cache_hazard]].

## 9. Scope boundary

This subproject does not import from `analyzing/`, `trading/`, `verifying/`,
or `designing/`. The only allowed reach is the server adapter calling
`../accounting/scripts/...` as a subprocess (and reading
`financial/`-namespaced parquet via the kernel, not the web shell).

## 10. Financial sign-off — `evaluating/` is the constellation grantor

`evaluating/` owns the **financial sign-off** (the FINANCIALLY-CLEARED gate) —
the financial-domain analog of `pleading/`'s litigation-safety gate. Adopted
2026-06-24 from a lifted publishing charter; spec
`data/specs/evaluating-financial-signoff-2026-06-24/SPEC.md`. It is the single
gate that clears (or blocks), on financial-advice / securities-liability
grounds, any **public** surface that evaluates, recommends, or implies a
financial decision. `evaluating/` is the **sole grantor**; `accounting/`
**advises** (frameworks/kernel truth), it does not grant.

**Scope (§ 3 of the spec):** Qresev surfaces (live app, `qresev-public` README +
STATUS + metadata `description`, the `/qresev` product page + OG card) and any
other public surface evaluating stocks/portfolios/options with actionable
framing (public `trading/`/`analyzing/` artifacts; a Qresev-framed
`explaining/` video). `/donate` is out unless it implies returns; internal
artifacts are out.

**FINANCIALLY-CLEARED iff (§ 4 of the spec):** the `financialRider` is present +
adjacent to **every** TREND/MOMENTUM/OPTIONS-RISK/SECTOR/DRAWDOWN verdict token
(not just an intro); no actionable-counsel language ("advice"/"recommendation"/
"buy"/"sell"/"should"/return-promise/"guarantee" — the rider's own *negated*
uses are exempt); the allow-list is framed "a kernel refusal, not a safety
guarantee" (never "safe"); `disclaimer.canon` is verbatim; the rider is
**byte-equal** to the `disclaimer.financialRider` export across all faces, and
the `description`-strip face is concession-safe standalone. Intra-app faces are
asserted by `app.spec.ts`; cross-repo faces by the publishing `github_meta.py`
lint.

**Orthogonal to `pleading/` (load-bearing):** never a substitute for the
litigation gate. Where both apply, a surface needs **both** clears; a green
`pleading/` line is not a financial sign-off and vice-versa (messaging-debate
§ 11.6). `evaluating/` is the **V8 owner/gate** in the messaging-hardening
debate (`shorting/` prosecutes; `pleading/` retains the litigation vectors).

## Status emit (`data/status/evaluating.json`)

`evaluating/scripts/status_emit.py` writes the Qresev app-shell diagram +
live-state to `data/status/evaluating.json` for the qagents-wide Status
page on quantapix.com. The slot's `productBrand: 'Qresev'` flips the card
label to `Qresev` (amber accent). Defined-risk options invariant must be
reflected in `cardSummary`. Status pill `OK` when both the static shell
deploys green AND `api.qresev.quantapix.com/api/health` returns 200. Schema:
`@qagents/diagram-kit`; plan: `designing/web/PLAN-status-page.md`.
Self-contained — no sibling-subproject imports.
