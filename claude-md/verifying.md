# verifying — Qnarre app shell

Project-specific rules for the **Qnarre** app at `qnarre.quantapix.com`.
Sibling of `evaluating/` (Qresev). Wraps the `proving/` Lean4 +
LLM-predicate kernel. Cross-project rules: root `CLAUDE.md`.

## 1. Layering — strict, like proving/

Three layers, no crossing:

| Layer | Where | Reads | Writes |
|---|---|---|---|
| **Web shell** | `web/` (Astro + React island) | HTTP + SSE from the server | rendered UI |
| **App server** | `server/` (FastAPI in the root venv) | uploaded complaint, manifest | spawns the proving/ driver as a subprocess; streams events |
| **Kernel** | `../proving/` (untouched) | manifest + complaint | `Facts.lean` + audit JSON |

The web shell never imports from `../proving/`. The server adapter calls
the proving driver as a subprocess and reads its outputs. This honors the
root-level rule: web TypeScript does not reach into Python kernels, and the
kernel's layering invariants stay intact.

## 2–4. Design bundle, tokens, copy

The design handoff bundle (under the shared render-cache hub) is
regenerated wholesale; never hand-edit. Tokens are byte-identical to the
umbrella site — Qnarre does not get its own palette; the brand-mark color
difference lives in the SVG props, not in tokens. No hex colors / font
strings / pixel literals outside `web/public/tokens.css` — refer to
`var(--token)` everywhere. Copy lives in one module (`web/src/copy.ts`),
never inlined into pages/components.

## 5. App surface is one big React island

`/app` is a single full-height React island with three persistent zones:
INPUT · AGENT STREAM · REPORT. Static marketing pages stay Astro. The
island talks to the FastAPI server over SSE. The REPORT zone has three tabs
(Predicates / Structure / Proof graph) when the URL carries a run id; the
Proof-graph tab embeds the per-run kit view in an iframe so the kit's
interactions stay isolated from the island's React state. Without a run id,
the island falls back to bundled demo data so the marketing preview works
without a live server.

## 6. Framework scope + taxonomy seam

Qnarre verifies legal complaints under one of: civil RICO §§ 1961–1968,
Title VI §§ 2000d et seq., §§ 1981/1983/1985(3). Adding a framework is a
parallel exercise driven by `../proving/` first; the UI gains a chip only
after the predicate roster lands. `proving/predicates/<id>/` is the
authoritative framework set; `web/src/lib/frameworks.ts` is the single
declaration site (label + cite per framework) — the predicate count comes
from the filesystem and the "updated" date from `git log`.

## 7. Server scope

v0.1 is **replay-only**. `POST /api/runs` takes an `{example_id}` from a
closed allow-list of curated, in-tree (already-redacted) examples. The
adapter shells the proving driver in reuse-facts + build mode against the
committed example dir; no predicate sub-agent calls run (the committed
facts are the input); only `lake build` runs live (~2s, $0/run).

Endpoints: `POST /api/runs` · `GET /api/runs` (allow-list with current
verdicts + predicate counts) · `GET /api/runs/<id>/stream` (typed SSE
events) · `GET /api/runs/<id>/report` · `GET /api/runs/<id>/graph`.

**Privacy floor — satisfied by construction.** Replay-only means no user
complaint text reaches the LLM or the kernel; the only complaint ever
processed is the curated, already-redacted example. The drive's
freeform-POST refusal binding is therefore honored without any
redaction-sweep code at this layer. Revisit when an admin-gated freeform
POST lands — that path requires the document-redaction rule set already in
use for the public-filing staging.

## 8. Proof-graph kit (Lean4 DAG visualisation)

The proof-graph rendering kit — predicate-pill / axiom-rectangle /
theorem-hexagon visual contract over a deterministic seeded layout — ships
with the static build:

- `/proof-graph/` — lobby + cards linking to the demos and any live runs.
- `/proof-graph/01-rico/` — a fictional *Doe v. Acme* § 1962(c) happy path.
- `/proof-graph/02-debug/` — synthetic-failure variant restyling into the
  three failure modes (predicate-False, predicate-Undecided, kernel-error).
- `/proof-graph/run/<id>/` (+ `/debug/`) — per-run views over real example
  graph fixtures; `getStaticPaths` scans the example archive at build time.

Kit code lives at `web/public/proof-graph/`: diagram-overlay tokens,
primitive styles, the `ProofGraph` namespace, the canonical fixture, and a
**side-car `loader.js`** that adapts a producer-emitted `graph.json` into
the kit's render contract. The loader lives separately because the bundle
is regenerated wholesale; **never fold `loader.js` into `kit.js`**. Pages
inject the kit CSS via the layout's head slot.

## 9. Hosting + e2e

Local dev: Astro on a dev port + uvicorn behind a Vite proxy. Prod: static
shell on S3 + CloudFront at `qnarre.quantapix.com`, server on a shared EC2
instance behind a reverse proxy at `api.qnarre.quantapix.com`. Same code in
both modes; only the API origin changes. The static-shell deploy rides the
shared deploy script + per-site env; a single managed IAM policy covers all
sites. Playwright e2e runs three projects against a built+previewed shell
offline, or against the deployed shell when a base URL is set; the
framework-taxonomy and API-allow-list specs mirror their source-of-truth
declarations and edit in lockstep.

## 10–11. Scope boundary + status emit

This subproject does not import from `analyzing/`, `trading/`,
`evaluating/`, or `designing/`. The only allowed reach across subprojects
is the server adapter calling the proving driver as a subprocess.
`scripts/status_emit.py` writes the Qnarre app-shell diagram + live state;
the pill is `OK` when both the static shell and the API health endpoint
return 200, degrades when one is up, errors when neither is.
Self-contained — no sibling-subproject imports.
