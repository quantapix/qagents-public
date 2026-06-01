# evaluating — Qresev app shell

Project-specific rules for the **Qresev** app at `qresev.quantapix.com`.
Sibling of `verifying/` (Qnarre). Wraps the `accounting/` Lean4 +
LLM-predicate kernel — the financial-domain parallel of `proving/`.
Cross-project rules: root `CLAUDE.md`.

## 1. Layering — strict, like proving/

| Layer | Where | Reads | Writes |
|---|---|---|---|
| **Web shell** | `web/` (Astro + React island) | HTTP + SSE | rendered UI |
| **App server** | `server/` (FastAPI in the root venv) | portfolio JSON, manifest | spawns the accounting driver as a subprocess |
| **Kernel** | `../accounting/` | manifest + portfolio | `Facts.lean` + audit JSON |

The web shell never imports from `../accounting/` or `../analyzing/`. The
server adapter calls the accounting driver as a subprocess and reads its
outputs; the kernel reads its OHLCV via the shared parquet hub, not the
analyzer's views — so this subproject only ever sees shared parquet and the
adapter's subprocess outputs.

## 2–4. Design bundle, tokens, copy, app surface

The design handoff bundle is regenerated wholesale; never hand-edit. Tokens
are byte-identical to the umbrella site; Qresev's brand-mark color lives in
the SVG props, not in tokens. No raw values outside `web/public/tokens.css`;
copy in `web/src/copy.ts`. `/app` is a single full-height React island with
three persistent zones: PORTFOLIO · AGENT STREAM · EVALUATION REPORT. It
inherits three patterns from `verifying/` — the side-car `loader.js`,
per-run static pages via `getStaticPaths`, and the three-tab REPORT zone
keyed on a run id (Predicates / Structure / Strategy-graph).

**Strategy-chart kit.** The chart-rendering kit (kit.js + kit.css +
tokens verbatim from the design bundle) plus the consumer-owned `loader.js`
side-car is the second instance of the proof-graph template; see
`verifying.md` § 8 for the canonical reference and the bundle re-sync
workflow. The kit ships literal font-family strings deliberately so SVG
screenshot rasterizers resolve them, so the token lint excludes the kit
directory — never hand-edit the kit CSS to placate the lint.

## 5. Defined-risk options — non-negotiable

The UI itself refuses to construct any options leg outside the allow-list
(long calls/puts, debit spreads, covered calls, protective puts). This
matches the framework-level invariant and is enforced visually on `/app`
and `/frameworks` (allow-list in one accent, refused-list in another).

## 6. Frameworks scope + taxonomy seam

TREND · MOMENTUM · OPTIONS-RISK · SECTOR · DRAWDOWN, each mapping to an
`Accounting.<Framework>` module. Adding a framework is parallel to proving/'s
workflow — kernel first, predicate roster second, UI chip third.
`accounting/predicates/<id>/` is the authoritative set; `web/src/lib/frameworks.ts`
is the single declaration site (label + module per framework).

## 7. Server scope

v0.1 is **replay-only for POST** (sibling parity with verifying/). `POST
/api/runs` takes an `{example_id}` from a closed allow-list of curated
examples (including the five-framework brand anchor); the adapter shells the
driver in stub mode (cost-free canned predicate Bools against the committed
manifest), then invokes a **real** `lake build` so the kernel verdict is
genuine. Stub values are designed to match the canonical ACCEPTED trace; if
the kernel rejects, the report exposes the Lean error verbatim. The server
makes no financial judgments and places no orders — Qresev evaluates; it
does not execute.

Endpoints: `POST /api/runs` · `GET /api/runs` · `GET /api/runs/<id>/stream`
(typed SSE) · `GET /api/runs/<id>/report` · `GET /api/runs/<id>/graph` ·
`GET /api/runs/<id>/loci`.

**Privacy floor — satisfied by construction.** Replay-only means no user
portfolio data reaches the LLM or the kernel; the only portfolio ever
processed is the curated, synthetic-holdings example. The drive's POST
refusal binding is honored without any redaction code. Revisit if an
admin-gated freeform POST lands.

## 8. Hosting + e2e

Local dev: Astro on a dev port + uvicorn. Prod: static shell on S3 +
CloudFront at `qresev.quantapix.com`, server on a shared EC2 instance
behind a reverse proxy at `api.qresev.quantapix.com`. The static-shell
deploy rides the shared deploy script + per-site env. Playwright e2e runs
three projects against a built+previewed shell offline, or the deployed
shell when a base URL is set; the framework-taxonomy and API-allow-list
specs mirror their source-of-truth declarations and edit in lockstep.

**EC2 server deploy** tarballs the server + the sibling kernel, uploads to
the artifacts bucket, and SSM-rotates on the shared instance, preserving the
incremental Lean build cache across redeploys. The systemd unit's
read-write paths must cover the kernel build dirs (a namespace preflight
hard-fails on any missing path). The Lean toolchain installs once at
instance boot; the kernel is mathlib-free, so that's the only kernel
dependency.

## 9. Scope boundary + status emit

This subproject does not import from `analyzing/`, `trading/`, `verifying/`,
or `designing/`. The only allowed reach is the server adapter calling the
accounting driver as a subprocess. `scripts/status_emit.py` writes the
Qresev app-shell diagram + live state; the defined-risk invariant is
reflected in the card summary; the pill is `OK` when both the static shell
deploys green and the API health endpoint returns 200. Self-contained.
