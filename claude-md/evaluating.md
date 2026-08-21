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
`rendering/designs/evaluating-web/` (Qresev slice + ADOPTION.md floors;
supersedes `data/renders/evaluating-design/`). Brand values never enter this tree:
`web/scripts/sync-meridian.mjs` (pre-hooks) host-copies the W5 css layers
from `code/web/css/meridian/`, the font trio from `rendering/brand/fonts/`,
and composes the dual-signal `/meridian-tokens.css` from the rendering SoT —
all gitignored under `public/`. `<body class="m-body m-app-qresev">` binds
the copper accent; tri-state theme via `@qagents/web/theme`. Shared
chrome/island shells come from
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
`code/web/scripts/lint-tokens.sh` + `web/lint-tokens.conf`.

**Bundle-mounting pattern — RECOMPOSED strategy mount.** Full recipe for
**re-hosting the strategy mount** — `StrategyKit.mountRun` signature,
`KitMount`↔compose-router `RegionSource` wiring, `report.json`→charts
`QReport`, `resolveBars` = `GET /api/runs/<id>/bars` (§ 6), the
`postMessage` REPORT-zone contract, per-run pages, and the behavioral
re-sync check + structural parity gate — lives in memory
`project_proof_graph_kit_mount_pattern` Instance 2. Mirrors
`verifying/CLAUDE.md` § 8; the dist is gitignored canonical-only and lags a
visualizing `/close`, so **rebuild at canonical first**, then cp.

**`tokens-*.css` and `kit.js` are a LOCKSTEP pair — re-copy both or neither**
(root § Kit-mount pattern owns the generic inert-overlay mechanism). It bit us
here 2026-07-14 — a projected ghost in the ACTUAL SERIES COLOR on a financial
surface. Verify by asking the **live mount** what it computed
(`getComputedStyle(document.documentElement)` under `pnpm preview`), never the
build. `[[feedback_two_token_mirrors_ship_two_palettes]]`

**lint-tokens caveat** — `public/graphs/` is excluded via
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
contracts come from the `data/specs/proving-results-propagation-2026-05-09/` family;
the worked references live at `verifying/CLAUDE.md` §§ 5, 7, 8 and the
evaluating-instance detail (§ 2's `loader.js` schema adapter + selection
forwarding) is pinned in memory `project_proof_graph_kit_mount_pattern` Instance 2.
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
`debate record `quantapix-thesis-public-pages-2026-06-23` (data/debates/, HELD lane)`.

## 4. Defined-risk options — non-negotiable

The UI itself refuses to construct any options leg outside the allow-list
(long calls/puts, debit spreads, covered calls, protective puts). This
matches the qagents brand-level invariant from
`trading/shared/skills/options-risk/SKILL.md` and is enforced visually on
`/app` and `/frameworks` — Meridian copper-wash for the allow-list, fails-wash
+ ✗ for refused legs (§ 2 R-T2; the legacy `.teal`/`.amber` class names survive
only as pinned e2e selector anchors).

**COMPOSITION CARVE — ruled 2026-08-01 (ns:evaluating/16), binding on the
FINANCIALLY gate.** A multi-leg structure named OUTSIDE the six-value `Strategy`
inductive (`accounting/Accounting/Common/Types.lean:65`) does **not** widen the
allow-list, and the enum is NOT extended, **iff** both hold:

1. **Decomposition** — every leg is independently an allow-list `Strategy` value;
   and
2. **Cover** — every short leg is covered by a position the *same book* actually
   holds. Cover is a fact about the portfolio, never about the label.

A **collar** satisfies both: `CoveredCall` (long stock + short call) ∧
`ProtectivePut` (long stock + long put) on one underlying. The name never enters
the kernel; `Strategy` stays six-valued and `strategy_closed`
(`OptionsRisk/Hier/VetoSurvives.lean:36`) is untouched. **`collar_bounds_computable`
in accounting's Hedging BOUND P3 roster (`Hedging/Predicates.lean:22`) is
therefore admissible as a bound over an already-allowed two-leg composition** —
accounting's BOUND remainder is ungated by this ruling.

Clause 2 is the whole content of the carve, and it is **not new** — it restates
`options-risk/SKILL.md` § "Book-level coverage (composition is not leg-wise
safe)", which already names the *composed collar* as a short-call ticket that
must pass `shared.lib.risk composition`. Boundary case, stated so the carve has
one: a short call + long put **without the underlying** is a synthetic short —
its short leg has no cover, it fails (2), and it is refused however it is
described. That refusal is the per-leg veto working (`noNaked` is a field with
no default), which is why the carve is safe to state rather than assume — a
composed structure no rule names is exactly the shape that reads as cleared
without ever having been cleared.

Extending `Strategy` remains a brand-level change (SKILL.md hard rule: update
`trading/CLAUDE.md` + the gate skill first).

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
overwriting `{report,graph,loci}.json` in place. `--stub` is the replay
mode — cost-free predicate values, instant canned Bools against the committed
manifest. The driver then invokes **real** `lake build examples.<id>.proof`
(not `lake env lean`) so the kernel verdict is genuine. Stub values are seeded from the example's committed `facts.json`,
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
`api.qresev.quantapix.com` (per the `data/specs/serving-2026-05-26/` family).

**Static-shell deploy** — `aws-vault exec qagents-deploy -- pnpm -C evaluating/web deploy`
(rides `serving/scripts/deploy-site.sh` + `serving/sites/qresev.quantapix.com.env`).
Bucket/cert, CloudFront, IAM policy, cross-site contract: `serving/CLAUDE.md` § 8.

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
  lands. Predicate counts use a floor (`minPreds`). `FRAMEWORK_META` is
  also a declared audit-time comparison source for analyzing's
  vocab-audit lockstep scan (workflow-coverage E-U1) — renames/refactors
  of that file's shape fail-loud downstream (the scan errors on an empty
  harvest), so breakage is visible, not silent.
- `strategy-chart.spec.ts` — recomposed kit-mount (`data-ready` +
  cytoscape canvas) on three spot-check runs
  (`balance_sample`/`hawk_sample`/`single_ticker_sample`) + the
  structural parity gate (report predicate set ↔ DAG nodes) + the
  `sc:predicate-selected` round-trip + `<head>` linkage of the
  graphs CSS set.
- `app.spec.ts` — `client:only` island hydration, 5-chip set + click +
  the OPTIONS-RISK lock panel.
- `theme.spec.ts` — M4 tri-state theme + the FINANCIALLY per-leg R-T2
  floors (§ 2), plus the **two-child flex-row gap sweep** (added
  2026-08-01, ns:evaluating/14) — DISCOVERING, not a selector list.
  `space-between` is distribution, never spacing: pair it with an explicit
  `gap`. Sweep mechanism, narrow-viewport idiom, both-apps cure roster,
  witness discipline: `[[project_qnarre_qresev_apps]]` § "Two-child
  flex-header zero-gap trap".
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
2026-06-24 from a lifted publishing charter; gate registry row:
`.claude/skills/do-signoff/registry.tsv` (FINANCIALLY). It is the single
gate that clears (or blocks), on financial-advice / securities-liability
grounds, any **public** surface that evaluates, recommends, or implies a
financial decision. `evaluating/` is the **sole grantor**; `accounting/`
**advises** (frameworks/kernel truth), it does not grant.

**Recording a grant.** Each granted/blocked sign-off lands as a dated record in the
FINANCIALLY slot of the signoff hub (`data/signoffs/FINANCIALLY/<date>-<subject>.md`;
relocated 2026-07-30 from the spec family's § 9 ledger, do-retire P3 step 1) —
never in `pleading/`'s `messaging-rulings/` (the
§ 5 orthogonality). First entry: `2026-06-30-4.1-ta-bestiary.md`. A consumer
cites it (manifest + release commit) before any public push. A record's
`payload.content_sha256` is a **roll-up over the record's `faces[]` table** — one
level up from `data/publishing/push-ledger.jsonl`'s same-named field (which hashes
the pushed binary itself); never join the two by field name (studying L-127;
wording precedent: `studying/scripts/extract_signoff_facts.py` header).

**Bind a GENERATED face NORMALIZED, never by raw sha256** (`do-signoff` SKILL
§ 3.6): `write_record.sh --json-face slot=… --strip-keys …` makes the jq-canonical
clock-stripped payload the condition, raw hash as provenance — so a daily emit
stops lapsing the grant on its granting day while a real tier/figure edit still
does. **A strip list must reach EVERY clock, and twice it did not.** `--strip-keys`
deletes recursively by key NAME, so it cannot reach a clock sharing its key with
substantive values — use the id-scoped **`KEY@ID`** form (`value@run-stats.latest`;
a bare `value` would strip every reviewed metric — `ns:evaluating/29`). And it must
strip **BOTH halves of a derived pair**: `status_pill()` returns `(pill, reason)`,
and stripping only the reason left the binding tracking the same clock through
`live.status`, alternating red/green with the `[managing]` verify lane from the day
after the re-bind (`ns:evaluating/36`). Each cure ships a **known-bad** arm
(`tests/run.sh` 8a′/8a‴) asserting the insufficient form does NOT hold — without
it a fix is green on a fixture and still lapses in the field. A strip list is a
standing blind spot: if a stripped field gains financial content, drop its entry in
the same commit. Converse ruling: run counts + the rolling runs window stay
**BOUND** — activity is not clock, so the accounting slot re-arms on every run, and
the consumer **cites the record** rather than re-verifying the live slot at deploy.
**Two standing grantor rulings, both `do-signoff/SKILL.md` § 8:** a face edit
DISCHARGING a hard pre-push condition of the same record does not re-arm it (else
every prescriptive condition is self-defeating — `ns:evaluating/35`); and producer
faces stay pinned RAW with false reds accepted, since a producer moves only when
edited while a generated face moves daily (`ns:evaluating/29`). Cite SKILL.md § 8
for the § 3.6 rules — the spec body is reaped, only `tests/` survives.

**The `serving/scripts/upload-video.sh` release gate now ENFORCES THE RECORD —
`ns:serving/82` landed, re-read 2026-08-10.** This § has been wrong about this gate
twice before, in both directions. Read the script, not this paragraph, before
relying on it.

What it does today: on **any** `T<n>/` key it requires `CLEARANCE_COMMIT` to (a)
resolve to a real commit, (b) **equal the `granting_commit` of an actual record with a
`CLEARED*` disposition** under the gate's `record-location` — resolved from
`.claude/skills/do-signoff/registry.tsv`, refusing rather than falling back if the
registry is missing, and reading the disposition in the same pass so a BLOCK's commit
can never satisfy a release — and only then (c) that it is an ancestor of HEAD.

**This floors T1/T2.** The gate keys on the `T<n>/` key prefix and never consults
`r2-scope-map.json`, so `requiredGates: []` there no longer means "no gate at the
push" — see the standing ruling below, which owns the rest of this reasoning.
The residual is the standing completeness caveat, not a T1/T2 one: an out-of-band
`aws s3 cp` bypasses the chokepoint entirely, emits no push-ledger fact, and passes
nothing (`managing`'s inventory diff carries that half).

**Standing ruling — do NOT widen `data/publishing/r2-scope-map.json` T1/T2 to
`["FINANCIALLY"]`** (operator 2026-08-07; re-affirmed on narrowed grounds 2026-08-10,
relocated here from the retired `ns:evaluating/28` so it outlives the item). `[]` is a
**scope** statement: T1 (proof-method) and T2 (docket-legal) content is genuinely
outside § 3. Two reasons not to revisit it. (i) Widening would red the coverage proof
for four already-pushed episodes — `T1/01-hallucination-tax`,
`T1/05-negative-verification`, `T1/07-civil-rico-walkthrough`,
`T2/01-docket-record-disagree`, none carrying a FINANCIALLY record — and back-filling
records for shipped content violates gate-before-first-push (§ 3.5) by construction.
Those four stay permanently uncovered; the hardening is prospective, and that is the
right outcome, not a gap to fill. (ii) The push floor the widening was once wanted for
now exists elsewhere: the gate keys on the `T<n>/` prefix, so the map no longer carries
that weight. `requiredGates` governs the coverage proof only, where `[]` is honest.
Filing a **verified-N/A** `/do-signoff FINANCIALLY <subject>` for a non-financial
episode (disposition CLEARED, scope "out of § 3 financial scope") is therefore now
**how a T1/T2 episode gets released at all** through the sanctioned path — no longer
merely good practice. The generic version of
this machinery is **ADOPTED**: the `/do-signoff <gate> <subject>` skill
(`.claude/skills/do-signoff/` — FINANCIALLY-CLEARED is its first governing instance,
resolver refuses unless the session IS the grantor) over the governance-layer spec
family `data/specs/signoff-framework-2026-06-30/`, with provable `lake build`
verification (studying S-T10 `SignoffCoverage`). Grant a FINANCIALLY surface with
`/do-signoff FINANCIALLY <subject>` from this session; the 4.1 record carries the
§ 5 structured core as the worked example. See `[[project_signoff_framework]]`.

**Scope** (FINALIZED): Qresev surfaces + any public surface
evaluating stocks/portfolios/options with actionable framing; internal
artifacts and a returns-free `/donate` are out.

**FINANCIALLY-CLEARED iff:** the criteria ride the § 4 defined-risk floor
above (this file is their owner; registry row:
`.claude/skills/do-signoff/registry.tsv`). The two an
evaluating session must not regress in-app: the `financialRider` is present +
adjacent to **every** framework verdict token (not just an intro), and the
allow-list is framed "a kernel refusal, not a safety guarantee" (never "safe").
Intra-app faces asserted by `app.spec.ts`; cross-repo by the publishing
`github_meta.py` lint.

**A green mechanical gate is NOT a grant (load-bearing).** The scanners
(`lib/scan_financial.sh`) and explaining's `phase0_preflight.py --rider-floor`
prove rider *presence + byte-equality* only. Neither can see **CLEAR-5 (R10)** —
binding each framework verdict token to a committed `accounting/` run-emit — which
is a **judged** clause (skill § 5). Necessary, never sufficient. Worked
counterexample (3.6 `live-evaluator-walkthrough`: mechanically green, BLOCKED
2026-07-10, cleared same day after explaining's cure `ddfbed82` — the CLEARED
record is `data/signoffs/FINANCIALLY/2026-07-10-3.6-live-evaluator-walkthrough.md`;
a BLOCKED record never leaves the gitignored buffer) + the CLEAR-5 run-binding
rule (names-a-run ⇒ that run's emit · names-no-run ⇒ the committed framework ·
absent framework ⇒ the three-valued `none` cell) + run-emit facts:
`[[project_cohort3_financial_signoff_rider_floor]]`.

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
