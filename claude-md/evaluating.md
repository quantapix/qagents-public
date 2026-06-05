# CLAUDE.md — evaluating/ (Qresev)

Project-specific rules for the Qresev app at `qresev.quantapix.com`. Sibling
of `verifying/` (Qnarre). Wraps the (forthcoming) `accounting/` Lean4 +
LLM-predicate kernel — the financial-domain parallel of `proving/`. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`.

## 1. Layering — strict, like proving/

| Layer | Where | Reads | Writes |
|---|---|---|---|
| **Web shell** | `web/` (Astro + React island) | HTTP + SSE | rendered UI |
| **App server** | `server/` (FastAPI in qagents root .venv) | portfolio JSON, manifest | spawns accounting driver as subprocess |
| **Kernel** | `../accounting/` (forthcoming) | manifest + portfolio | `Facts.lean` + audit JSON |

The web shell never imports from `../accounting/` or `../analyzing/`. The
server adapter calls the accounting driver as a subprocess and reads its
outputs. Per the qagents/CLAUDE.md "two open choices" answer, accounting/
reads its OHLCV via the shared `data/` parquet hub (not analyzing's DuckDB
directly) — so this subproject too only ever sees `data/` parquet and the
adapter's subprocess outputs.

## 2. Design bundle is read-only; regen workflow

`data/renders/evaluating-design/` (under the qagents shared-data hub
`data/renders/`) is the handoff bundle slot from Claude Design, regenerated
wholesale. Never hand-edit. The `Qresev App.html` prototype is the visual
source of truth.

When re-syncing tokens.css from the bundle (run from the repo root):

1. `cp data/renders/evaluating-design/project/colors_and_type.css evaluating/web/public/tokens.css`
2. `pnpm -C evaluating/web verify`

Tokens are byte-identical to `designing/`. Qresev's brand-mark color
(amber-only BracketedQ) lives in SVG props, not in tokens.

**Bundle-mounting pattern — strategy-chart kit.**
The kit at `evaluating/web/public/strategy-chart/` (kit.js + kit.css +
tokens-chart.css verbatim from `data/renders/evaluating-design/`) plus
the consumer-owned `loader.js` side-car is the first instance of the
verifying/web/ template here. Layout.astro carries the `<slot
name="head" />`; per-run pages live at
`evaluating/web/src/pages/strategy-chart/run/[id]/`. See
`verifying/CLAUDE.md` § 8 for the canonical reference and the bundle
re-sync workflow. A TS-module port to
`evaluating/web/src/lib/strategy-chart/` is deferred until either
(a) a second consumer needs the kit, or (b) SSE wiring needs to call
into the kit reactively.

**lint-tokens caveat.** strategy-chart's `kit.css` ships literal
`font-family` strings deliberately so SVG screenshot rasterizers
resolve them (HANDOFF.md § "Caveats" item 1; `var(--font-mono)` doesn't
work as an SVG presentation attribute). `evaluating/web/scripts/lint-tokens.sh`
excludes `--exclude-dir=strategy-chart` from both passes. Future
regen-wholesale kits with the same constraint follow the same
exclusion pattern; never hand-edit the kit's CSS to placate the lint.

## 3. Tokens / copy — same as Qnarre

No raw values outside `web/public/tokens.css`. Copy in `web/src/copy.ts`.

## 4. App surface is one big React island

`/app` is a single full-height React island
(`web/src/islands/QresevApp.tsx`) with three persistent zones: PORTFOLIO
(28%) · AGENT STREAM (36%) · EVALUATION REPORT (36%).

**Three patterns inherited from `verifying/`** (side-car `loader.js`,
per-run static pages via `getStaticPaths`, three-tab REPORT zone with
`?id=<runId>` showing Predicates / Structure / Strategy-graph). The
contracts come from `data/specs/proving-results-propagation-2026-05-09.md`;
the worked references live at `verifying/CLAUDE.md` §§ 5, 7, 8 and the
evaluating-instance detail (loader.js schema adapter, `proves_options_clean`/
`hawk_legs_clean` → `t_clean`/`t_legs` id-remap for `SC.layoutHawk`,
`postMessage({type: 'sc:predicate-selected', sel})` selection forwarding)
is pinned in memory `project_proof_graph_kit_mount_pattern` Instance 2.
Structure-tab failure-loci block falls back to `kernel.errors[].raw`
when `termHasType` is empty.

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
(`balance_sample` is the 5-framework brand-anchor); the adapter shells
`extract_facts.py --stub` against `accounting/examples/<id>/`,
overwriting `{report,graph,loci}.json` in place. accounting/'s driver
now carries `--reuse-facts` + `--build` (proving parity, since ffa30e46),
but `--stub` stays the replay mode — cost-free predicate values, instant
canned Bools against the committed manifest. Driver also honors a per-call `inputs.stub: true`
override that forces stub on a single predicate even when global
`--stub` is off — additive. The driver then invokes **real** `lake build
examples.<id>.proof` (not `lake env lean`) so the kernel verdict is
genuine. Stub predicate values are designed to match the canonical
ACCEPTED trace; if the kernel rejects, the report exposes the Lean
error verbatim. Read endpoints keep the hybrid `_resolve_run_dir` shape
(`server/jobs/` first, then `accounting/examples/`) so any historical
live-job artefacts remain readable.

Endpoints: `POST /api/runs` · `GET /api/runs` (lists jobs + examples
with current verdicts) · `GET /api/runs/<id>/stream` (SSE, typed
events per propagation spec § 5.4) · `GET /api/runs/<id>/report` ·
`GET /api/runs/<id>/graph` · `GET /api/runs/<id>/loci`. The server
makes no financial judgments and does not place orders. Qresev
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
`api.qresev.quantapix.com` (per `data/specs/serving-2026-05-26.md` § 2 decision 3).

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
- `strategy-chart.spec.ts` — kit-mount canvas (`svg.sc-svg`) on three
  spot-check runs (`balance_sample`/`hawk_sample`/`single_ticker_sample`)
  + `<head>` linkage of tokens-chart.css + kit.css + kit.js + loader.js.
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
rewrites `settings.toml` on toolchain activation (both kernels unified to
`leanprover/lean4:v4.30.0` on 2026-06-05 — formerly a per-build switch
between qresev's v4.30.0-rc2 and qnarre's v4.29.1), so without it lake dies
~0.04s in on a read-only-fs write and every live run returns a spurious
REJECTED with empty `kernel.errors` (fixed 2026-06-01).

The Lean toolchain (`leanprover/lean4:v4.30.0`, 2.5 GB) installs
once at EC2 boot via `bootstrap-ec2.sh`. accounting/ is mathlib-free
so this is the only kernel dependency. Memory:
[[project_ec2_lean_kernel_install]] + [[feedback_kernel_rotation_cache_hazard]].

## 9. Scope boundary

This subproject does not import from `analyzing/`, `trading/`, `verifying/`,
or `designing/`. The only allowed reach is the server adapter calling
`../accounting/scripts/...` as a subprocess (and reading `data/`-namespaced
parquet via the kernel, not the web shell).

## Status emit (`data/status/evaluating.json`)

`evaluating/scripts/status_emit.py` writes the Qresev app-shell diagram +
live-state to `data/status/evaluating.json` for the qagents-wide Status
page on quantapix.com. The slot's `productBrand: 'Qresev'` flips the card
label to `Qresev` (amber accent). Defined-risk options invariant must be
reflected in `cardSummary`. Status pill `OK` when both the static shell
deploys green AND `api.qresev.quantapix.com/api/health` returns 200. Schema:
`@qagents/diagram-kit`; plan: `designing/web/PLAN-status-page.md`.
Self-contained — no sibling-subproject imports.
