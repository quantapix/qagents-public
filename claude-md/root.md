# qagents — Cross-project conventions

Subprojects under this repo:

Each `<sub>/CLAUDE.md` is the single owner of its own mechanics + spec path; the roster below is the constellation index — name, discriminating role, and cross-boundary relationships only.

- `analyzing/` — market-inspection tooling (TypeScript; local-only viewer): DuckDB + Parquet, lightweight-charts v5, yfinance ingest, Alpaca IEX live feed. `financial/parquet/` tape supplier.
- `trading/` — Python portfolio-management agents: three PMs (aggressive/moderate/conservative) on Alpaca paper, orchestrated by Claude Code routines.
- `appealing/` — pro se federal appellate drafting. Markdown drafts; rendered PDFs flow to a private filing hub. CLAUDE.md content not mirrored — see `qagents-public/README.md` § "Litigation-domain CLAUDE.md\`s ... deliberately excluded".
- `pleading/` — pro se trial-court + status-affidavit + addendum drafting. Sibling of `appealing/`. Markdown drafts; rendered PDFs flow to the private filing hub. CLAUDE.md content not mirrored.
- `designing/` — Astro + React islands site for quantapix.com (S3 + CloudFront). Hosts `/status` aggregating per-subproject `data/status/<sub>.json`.
- `documenting/` — sibling of `designing/`; femfas.net v2 (Astro/S3/CloudFront).
- `monitoring/` — local-only **Astro Node-SSR web app** for Claude Code token analytics; SQLite store, sibling of `analyzing/`'s DuckDB inspection tooling. Chartered consumer app of the **operational** Lean4 axis; never deployed.
- `proving/` — Lean4 axiomatic theorem-proving with LLM-backed predicate functions for the **legal** domain (civil RICO, Title VI, §§ 1981/1983/1985(3)). Backs `verifying/`.
- `accounting/` — financial-domain parallel of `proving/`: Lean4 + LLM-predicates for TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN frameworks. Reads OHLCV from the `financial/parquet/` hub. Backs `evaluating/`.
- `verifying/` — Astro+React shell + FastAPI server for **Qnarre**, the legal-complaint verifier UI. Three-zone `/app` island streams events from `proving/` via SSE.
- `evaluating/` — sibling of `verifying/` for **Qresev**, the stock/portfolio evaluator UI. Streams events from `accounting/` via SSE; UI hard-refuses any options leg outside the defined-risk allow-list (§ Defined-risk options). Owns the constellation **FINANCIALLY-CLEARED** gate (sole grantor; `accounting/` advises).
- `visualizing/` — graphing surface for the `proving/` + `accounting/` Lean4 axiomatizations; an animated page in Qnarre + Qresev via the kit-mount pattern; renders the **lattice** + a secondary proof-DAG.
- `studying/` — **operational-axis** Lean4 kernel (third of the three axes — § Lean4 axes) + owner of the cross-axis representation research and the `hub/` guide-rails. First target: git axiomatization (consumer `monitoring/`).
- `explaining/` — video-explainer arc for Quantapix outreach. 50 scripts (5 topics × 10 subjects) narrated by an **AI presenter**; 10–15 min each. Output is scripts; stage 5 (composition / render) consumes `resolving/`.
- `resolving/` — DaVinci Resolve production-assistance. Skills + Fusion authoring + typed Python wrapper at `resolving/davinci/`. Stage 5 of `explaining/`.
- `blending/` — Blender 5.1 + Geometry Nodes production-assistance; Escher-inspired background plates for `explaining/` → `resolving/`. Typed `bpy` wrapper at `blending/blendr/`.
- `serving/` — AWS cloud-base; single source of truth for every AWS resource. CDK in TypeScript. Hosts the `@qagents/diagram-kit` workspace package (sibling-of-subprojects, not member-of-serving).
- `managing/` — daily watcher over the constellation. Cron-fired at 06:00 with the top-tier model; four subagents (checker / planner / reporter / verifier); the verifier promotes `pending/` (§ Shared-data write-lock). **Observe-only** — no push/deploys/mutations; its commits and the S5 authority push are confined to the § 5.3 audit lane (mechanics: `managing/CLAUDE.md`).
- `shorting/` — adversarial sibling of `managing/`. On-demand from `/open shorting`: the per-target positions lane plus the chartered do-shorten / do-share / do-spread review fleets (`data/charters/shorting/review-lanes/CHARTER.md`). **Observe-only**; routes findings to `managing/`.
- `donating/` — 6-month public donation drive (2026-06-01 → 2026-12-01). Renders `data/donating/drive.json` (consumed by `designing/web` + `documenting/web`). Four exclusive-use buckets. Content-only.
- `publishing/` — open-source release subproject. Owns the public-org staging tree `publishing/quantapix/` and the `/publish` pipeline (sweep → redact → compile → push to `github.com/quantapix/*`). Owns drive Promise 1. Content-in / external-out; **not** observe-only.
- `rendering/` — in-house render engine + brand source of truth; single owner of **brand-bearing, pre-rasterized** artifacts (images + videos) for the whole constellation. Image engine live; video engine post-first-cohort. Deliverables in `data/renders/<consumer>/`.
- `extending/` — Claude Desktop extensions + enablement. Two halves: EXTEND — `servers/{qnarre,qresev}-mcp/` Node stdio MCP servers (thin proxies over verifying:8787 / evaluating:8788; never a fourth Lean consumer), shipped as `.mcpb` bundles via the `publishing/` lane; ENABLE — Desktop-adoption assets + the dual-multiplexer lane (cmux / herdr). Content-in / external-out via publishing.
- `developing/` — native macOS + iOS SwiftUI clients for Qnarre + Qresev; XcodeGen + SPM monorepo (`project.yml` is SoT). Never a fourth Lean consumer; future live wiring goes over the verifying:8787 / evaluating:8788 seams. Swift-only.
- `simulating/` — deep agent-based market simulation (Python engine + local MLX LLM fit lane; Astro Node-SSR **local-only** UI, never deployed). Factor-anchored on `financial/factors/` promoted copies (accounting produces; simulating is the licensed second reader under the C-1..C-6 consumer contract); 4th consumer of the `financial/` tape hub; mounts visualizing charts + mixed3d on the Meridian rails. Never a Lean consumer; generative-descriptive, never a forecast/alpha engine — FINANCIALLY floor from birth.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets + cross-cutting machinery (`status/`, `schedules/`, `specs/`, `renders/`, `donating/`, …). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule — single owner). Market/trading datasets live in the top-level `financial/` hub (below).
- `data/schedules/` — canonical macOS-launchd cron for **all** subprojects. Single `ROUTINES` array in `data/schedules/launchd/install.sh`; `run_routine.sh` is the per-fire wrapper. **Never** use cloud `/schedule` or `RemoteTrigger` — cowork sandbox can't mount the repo. **ROUTINES is a set of dependency chains, not independent fires** — successive fires hand off through tracked repo state (trading's `premarket-brief` → `open-execution` is the type case), so a host change mid-chain breaks the handoff even when every individual fire succeeds. That is the premise the seat model's CONTINUITY rule rests on.
- `data/renders/` — rendered deliverables + legacy design handoff bundles: migrated consumers hold **outputs only** at `data/renders/<consumer>/`; unmigrated bundles stay at `data/renders/<sub>-design/` (read-only, wholesale-regen). See `data/renders/MANIFEST.md`.
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `parquet/` (OHLCV, `ta-reference/`, `gics-symbols.parquet`), `portfolios/`, `reports/`, `universe/`, `gics/`, `factors/`. Consumers: `trading/`, `analyzing/`, `accounting/`, `simulating/` (read-only: tape + promoted `factors/`); cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md`; shares the root `.data-write-lock` (below).
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject (sibling-of-subprojects). Packages: `playwright/` · `remotion/` · `agent_sdk/` · `qreel/` · `lean_graph/` · `lean_tools/` · `lint/` · `web/` · `ledger/` · `flow_graph/`. Per-package purpose + spec pins + runnable-only-at-canonical note: `code/CLAUDE.md`. (`code/` membership via `workspace:*` is the chartered exception to the "no cross-subproject imports" seam law — it governs only subproject↔subproject edges; detail: `code/CLAUDE.md` § Seam-law exception.)
- `lib/` — vendored upstream code; sibling of `code/`. Today: `lib/memsearch/` (vendored+patched; see § memsearch for the qagents patch detail); `lib/heygen-skills/` (vendored-pristine, MIT). Governance classes: vendored-pristine / vendored+patched / reference-only. See per-package `UPSTREAM.md`.
- `hub/` — read-only upstream clones, regularly refreshed, **gitignored wholesale** (canonical-only, absent from worktrees); reference ground truth, never committed or imported as code. Five Lean4 guide-rail rows chartered (`studying/guide-rails.md`); other clones are ungoverned conveniences.

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only conventions that cross a boundary.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13); all cross-subproject deps in root `pyproject.toml` `[project.optional-dependencies]` extras (the extras list lives there — don't mirror it here). Bootstrap/repair a checkout — venv + the four `--no-deps` editables (`./trading` → `shared`/`shared.lib`; `./code/agent_sdk`, `./code/ledger`, `./code/flow_graph` → `qagents.*`) + profile marker + elan + pnpm, idempotent: `bash scripts/bootstrap-machine.sh [--profile full|trading-lane] [--check]`; env drift detection: `scripts/parity.sh` — the single owner of cross-workstation parity, and the thing to read (and extend) when a host diverges.

From repo root → `./.venv/bin/python …`. From a subproject → `../.venv/bin/python …`. The `proving/`/`accounting/` drivers + status emitters run on system `python3`; accounting's pandas helpers (`data_view.py`, `universe_graph.py`, the `scripts/factor_*.py` lane) are the venv exception. `simulating/`'s engine + MLX fit lane run the root venv (`[simulating]` extra; `full` profile only — a missing-extra fire fails loudly by design). **A new extra lands a file, not an environment** — finish any `pyproject.toml` extra addition with `bootstrap-machine.sh --check` on the host that will fire the lane, or a week of missing-extra fires reads as a quiet lane rather than a stale host.

## Shell scripts — homebrew tool versions

Any shell script (cron-fired, operator-fired, or session-invoked) MUST resolve to homebrew-installed tools, not macOS system defaults. macOS ships bash 3.2.57 (no `mapfile`/`readarray`/`declare -A`/`${var^^}`), no GNU coreutils, BSD `sed`/`awk`/`date`.

1. **Cron-lane PATH + portable-script recipes** — plist PATH ordering, bash-4+ avoidance, absolute-path homebrew features, audit patterns: memory `feedback_homebrew_over_system_for_qagents_scripts`; silent-abort pipeline/test traps: `reference_shell_script_test_gotchas`.
2. **Sibling-of-subprojects pkgs are *runnable* only at canonical.** Worktrees check out `code/`/`lib/`/`serving/` source but not gitignored build state. Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths.

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. Node code (CLIs, CDK, kit packages).
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's presets. Vendored `lib/` is upstream-owned.

### pnpm workspace + catalog

Single workspace at root: `pnpm-workspace.yaml` owns the member list, catalog, and `allowBuilds` (pnpm 11). Shape + root-script verbs + the placeholder trap: memory `reference_pnpm11_allowbuilds`.

### Playwright e2e (Astro sites)

Suites at `<sub>/web/tests/e2e/`; run `pnpm -C <sub>/web test:e2e`. Shared helpers, config shape + traps: memory `project_playwright_e2e_stack`. **Preview-port registry** (claim the next free port first): `code/playwright/PORTS.md`.

### IDE + parallel-session coordinator (cmux)

VSCode is a plain editor — no canonical-IDE claim. Parallel Claude Code sessions are coordinated by **cmux** (wrapper `scripts/cmux-session.sh`): memory `project_cmux_coordinator`.

## Canonical OHLCV bar shape

The bar-column contract (`ts/o/h/l/c/v/adj_c`) shared by all three consumers (`trading/`, `analyzing/`, `accounting/`) lives in `financial/parquet/CLAUDE.md` § "Canonical OHLCV bar shape" — the hub is its single source of truth. Adapters translate vendor field names at the boundary; never leak them past the client module.

## GICS sector / industry classification

GICS mapping is *shared data, not shared code*: parquet at `./financial/parquet/gics-symbols.parquet` keyed by `symbol`. Sector strings are the 11 canonical GICS long-form names.

- Readers: `analyzing/web/src/lib/gics.ts` (DuckDB view `gics`) + `python -m shared.lib.gics`. Neither side writes the parquet — seed/refresh via `financial/gics/build.py`; schema + caveats: `financial/gics/mapping.md`.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`, `/do-steps`

Sessions start with `/open <project>` and end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints; `/do-steps` works a project's next-steps slot inside an already-open session (spec `do-steps-2026-07-25`). The memory + CLAUDE.md optimization lane (`/dco-manual` standing; `/dco` cron parked) is chartered at `data/charters/qagents/optimization/CHARTER.md`. **Single normative owner: `data/charters/qagents/session-lifecycle/CHARTER.md`** — the one-liners below render its anchors; on any divergence, trust the charter (mechanics/orchestrator layers: charter § 2.2).

- **Lock model** (charter § 2.1 / § lock-model): branch-presence IS the write-lock; `<project>`/`<project>-N` blocks conflicting `/open`s, `/open qagents` blocks all. The session-branch grammar `^[a-z]+(-[0-9]+)?$` is the ONE lock-holder definition; slash-named refs (`lift/*`, `<node>/*`) are never lock conflicts.
- **Worktree path discipline (load-bearing)** (charter § 2.3 / § path-discipline): inside any `/open` session, every `Edit`/`Write` `file_path` MUST begin with the worktree root `<root>-wt/<branch>/` — a canonical `<root>/...` edit lands on `main`, silently bypassing the lock. Enforced by `scripts/hooks/no-canonical-edit-while-locked.sh`; reads may use canonical; cron-lane fires (no session branch) write canonical cwd-relative paths. See `feedback_worktree_path_determines_working_tree`.
- **Canonical-shared gitignored content** (charter § 2.4): declared per owner in `<sub>/.worktree-links`, symlinked into worktrees by `scripts/open.sh` (only pure-gitignored dirs). **Walkers must dereference (`tar -h`, `rsync -aL`) or hard-refuse** — `find` does not descend a symlinked dir (memory `project_parquet_gitignored_ground_truth`).
- **Bash discipline (load-bearing)** (charter § 2.2): close-lane bash uses absolute script paths only — each path form needs a separate allow-list matcher.
- **Cross-subproject writes · Stack · Sentinels · Adopted-spec convention** — cold anchors, rendered in the charters only: session-lifecycle charter §§ 2.7 / 2.1 + spec-lifecycle charter § 2.7.
- **CLAUDE.md updates** (charter § 2.6 / charter § 2.9): *immediate* (project's own CLAUDE.md on session branch) + *deferred hints* (`data/claude-updates/<branch>.md`; `/do-claude-updates` judges later).
- **Backward + forward surfaces** (charter § 2.8): `/close` writes `data/summaries/close/<YYYY-MM-DD>T<HHMM>-<branch>.md` (versioned, never overwritten); `data/next-steps/<project>.md` is the forward-only GENERATED render of `ledger.ns_item_event` — write via the `python -m qagents.ledger ns-*` verbs, never by hand, and let a resolution-verb commit cite fire the close-time `--next-steps` gate. Verbs, numbering, flow clauses, terminals, cite grammar, gate exit codes: `data/next-steps/CLAUDE.md` (single owner).

## Model policy — LLM model selection

Complex, long-running work (subagent fan-outs, axiomatization, watchers, debates, collectors, overnight research) runs the **top-tier model** — never a pinned older tier. In practice that is the **`opus` alias**: the absolute-latest tier (Fable 5) exhausts the Max-20x subscription quota within days. Review/optimization subagent fleets (dco, shorting positions, do-shorten/do-share/do-spread) carry **no `model:` pins** and inherit the model the orchestrator was invoked with — invoke the orchestrator on opus when quota is tight (operator ruling 2026-07-05). Prose says "top-tier model", not a name; when a sustainable new top tier ships, sweep the pins. The three axiomatization lanes (`/dau`/`/dat`/`/dao`) resolve from ONE seat — `code/lean_tools/model_floor.py` (`QAGENTS_AXIOMATIZE_MODEL`); sweep THAT switch, not per-axis pins. Lesser models only where flagged: `sonnet` for bounded cron routines, `haiku` for mechanical closed-set classification (`managing` verifier) and throwaway smoke runs; cron selection uses **bare tier aliases** (`opus`/`sonnet`/`haiku`), never pinned minors. **Capability floor:** haiku is forbidden for any retained axiomatization artifact (amendments are per-leaf-class only, via the bake-off gate). Mechanism detail (cron billing/Fable fail-close + its two exit codes + override + guard-test path, budget caps — widen them, never downgrade the model, single-seat internals + legacy env var, bake-off criteria/history, per-surface sweep roster): memory `project_model_policy_latest_top_tier` + `feedback_predicate_model_opus_not_haiku`.

## Programmatic Claude — Agent SDK lane

The Agent SDK lane is **parked** — Anthropic dropped SDK credits from the Max-20x subscription (2026-06-15); every routine runs the default `claude --print` lane. **Root § Agent SDK lane owns this status.** Standing label (operator ruling 2026-07-16): all SDK usage is **"to-be-re-considered in the future"** — never a live dependency, a flow-graph **parked target** (`ext:agent-sdk-credit`, excluded from every bottleneck/dependency metric — flow-graph spec § 5.3); no session spends further effort on SDK contingency planning until an official Anthropic reversal. Mentions, code, and tests are retained as-is (wrapper `code/agent_sdk/`, adoption spec, usage ledger, ROUTINES comment): memory `project_agent_sdk_wrapper`. **Un-park recipe:** restore the `:sdk` suffix on routine names in `data/schedules/launchd/install.sh` ROUTINES, and flip `data/next-steps/terminals/ext-agent-sdk-credit.md` to `state: open` (`git log -S ext:agent-sdk-credit -- data/next-steps/` recovers the parked items).

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) the shared `data/` **and** `financial/` hubs only while holding `<root>/.data-write-lock` (one lock serializes both).

**Shared ledger store (Postgres — qred LAN primary) is the canonical mechanism for new shared ledger-like data** (single shared file, many appenders) — ledger-shaped surfaces start as a store table + single-writer rendered git projection, never a new hand-appended shared file. Three consequences that are the operative part: the store is authoritative and the git projection is retained (never store-only — a deleted projection breaks any gate reading it); the projection has exactly ONE writer; and a new shared-append surface needs a table, not a file. Reader-side detail: `code/ledger/`.

- Cron-fired writes never touch `data/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync. The verifier is a **closed-set allow-list** classifier — register a new `pending/` producer path in lockstep in `managing/.claude/agents/verifier.md` + `verify-pending.sh require_known_canonical_subtree`, else its files land in `unclassified[]`, never promoted.
- Everything else takes the lock on these terms: manual fixed-path writers acquire it by atomic create and release it from an EXIT trap; configurable-output-path scripts acquire it **iff** the resolved target is canonical `data/`/`financial/`; a writer on the `QAGENTS_PENDING_ROOT` branch is staging, not writing canonical, and takes no lock.

## Subproject `.claude/` shape (consistent pattern)

Every subproject that runs Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed allow/deny + the standard hook set (roster: `data/claude-settings/sources/baseline.hooks.json` — the one enumeration; PreToolUse guards, SessionStart ctx + cwd-WARN, worktree pair). **Generated, not hand-edited** — edit `data/claude-settings/sources/`, re-run `scripts/claude-settings/build.py` (drift: `--check`). Runtime-permission scoping + the allow-glob trap: `data/charters/qagents/specs/claude-settings-unification-2026-06-06/SPEC.md` § 3 + `reference_claude_code_allow_glob_no_empty_match`; the worktree-root launch-cwd guards (deny mirror + agents link, provisioned by `qs open`) are § 4.5 of the same spec.
- `<sub>/.claude/settings.local.json` — user-local overrides (gitignored).
- `<sub>/.claude/skills` → symlink to `../../.claude/skills`.
- `<sub>/.claude/agents/` — optional per-subproject sub-agent definitions.

## Skill placement rules

- `./.claude/skills/` — cross-project skills (auto-loaded via each subproject's `skills` symlink).
- **Subproject-scoped skills** (not auto-loaded; invoked explicitly):
  - `trading/shared/skills/` — trading-only.
  - `trading/agents/<pm>/.claude/skills/` — PM-scoped.
  - the private filing hub — Combined RA agent team (1 coordinator + 10 volume agents); callable by drafting siblings (`appealing/`, `pleading/`).

## memsearch — semantic memory across qagents sessions

Vendored at `lib/memsearch/` as a Claude Code plugin (v0.4.16 since 2026-07-30). Install + per-subproject `qagents patch` (nine patches) + backend detail in `lib/memsearch/CLAUDE.md` § "qagents integration"; recall skill is namespaced `memsearch:memory-recall`. Retained invariants: **markdown is source of truth** (`<sub>/.memsearch/memory/YYYY-MM-DD.md`; Milvus is a derived, rebuildable index; tree gitignored); **worktree logs survive `/close`** (`qs memsearch copyback` — substrate crate engine); **recall is fork-isolated** (`context: fork`).

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

`.mcp.json` is subproject-scoped, never repo-rooted (cwd walk-up; rationale + apply pattern: memory `reference_mcp_subproject_scoped_via_file_location`). Today only `explaining/.mcp.json` is wired (`heygen` — detail: `explaining/CLAUDE.md`); DaVinci Resolve scripting is the typed wrapper at `resolving/davinci/`, no MCP.

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (schema owner v0.8.0, `SubprojectId` closed set = 25 subs); `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS/Python imports — the JSON hub is the only seam.

- **Whole-slot failure trap (every `/close --status-emit`):** a SINGLE contract-violating field drops the ENTIRE slot to placeholder on prod — coercion rules, field examples, consumer posture: memory `project_diagram_kit`.
- **Public surface — synthetic fixtures only:** every slot renders publicly at `quantapix.com/status/<sub>`, so a producer whose inputs can carry real matter MUST filter to synthetic/allow-listed fixtures (mirror `verifying/server/main.py ALLOWED_EXAMPLE_IDS`) — never real dockets/positions (`<live-matter>_*`). Fleet rule + owed close-time denylist scan: memory `reference_operational_axis_public_surface_privacy`.
- Producer/orchestrator/close-time-emit/pending-aware-cron/KIT_VERSION-lockstep + the eight-surface add-a-subproject sweep: memory `project_diagram_kit` § "Root § Status hub". Spec: `data/charters/qagents/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`.

## Kit-mount pattern

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`; three live instances mount the ONE domain-neutral graphs kit (`@qagents/graphs`) at `graphs/` — verifying + evaluating + monitoring. A mount's `tokens-*.css` and its `kit.js` are a **lockstep pair** — re-copy both or neither: a token overlay lifted without its bundle is inert (undefined custom property → `||` fallback, silently, every gate green). Full instance roster (incl. monitoring's `/proof` mount) + regen-wholesale/rebuild-canonical-dist/`getComputedStyle`-verify/commit-vs-gitignore discipline + schema/edge-kinds: memory `project_proof_graph_kit_mount_pattern`.

## Lean4 axes — three kernels, one architecture

Three orthogonal axes, never sharing domain/ground-truth/consumer: **textual** `proving/` (`legal/uscode/`; plaintiff v. defendant; → `verifying/`), **numerical** `accounting/` (`financial/parquet/`; bulls v. bears; → `evaluating/`), **operational** `studying/` (git first; `hub/git`; coding v. testing; → `monitoring/`, local-only). Chief invariant: **no human proof-driving, ever** — the other seven (axiomatic kernel + LLM `Facts.lean` + `lake build` gate, blind top-tier debate, toolchain lockstep, one consumer per axis, `visualizing/`+kit-mount presentation, G1–G7 hard-gated each wave, and **proof-of-fire** — every mechanical gate ships a committed known-bad witness it must reject; reachability, not pass count; added 2026-07-27) live in memory `project_lean4_three_axis_charter` § "Root § Lean4 axes". Spec `data/charters/studying/specs/lean4-charter-2026-06-10/SPEC.md` § 4 + the `axiomatize-shared-2026-07-04/` declared-child subspec (COMMON mechanism + LEARNINGS ledger + G1–G7 matrix). **Per-axis scope charters (2026-07-17):** `data/charters/studying/operational-axis/CHARTER.md` (neutral steward of the whole cross-axis `lean4-charter` family), `data/charters/proving/textual-axis/CHARTER.md`, `data/charters/accounting/numerical-axis/CHARTER.md`.

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools. The allow-list refusal is one input to `evaluating/`'s **FINANCIALLY-CLEARED** gate (§ subproject list, `evaluating/`), which signs off any public surface that evaluates or implies a financial decision — a kernel refusal, never a safety guarantee.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` multi-remote setup live in `serving/CLAUDE.md` § 8–§ 10 (single owner — deploy script, four-remote roster, aws-vault + Keychain, local network `qblk`/`qred`/`qyel`; never duplicated here or in subproject CLAUDE.mds). Cross-machine session exchange rides the same qblk/qred mirrors as the symmetric leaf-`/push` / hub-`/pull` cycle (`<node>/<topic>` refs; hub = sole merge-point) — mechanics owned by `data/charters/qagents/push-pull/CHARTER.md`.

## Language split

- Rust — exactly two in-repo authoring surfaces, each scoped to one job and
  nothing else: `code/substrate/` (crate `qagents-substrate`, bin `qs`) is the
  session-lifecycle mechanics layer (charter
  `data/charters/qagents/session-lifecycle/`); `code/context/` (crate
  `qagents-context`, bin `qx`) is context injection (PCI mechanism layer —
  contract owner stays the PCI spec family), output shortening, and the
  memsearch replacement (specs `rust-context-2026-07-22` +
  `rust-memsearch-2026-07-22`). Per-crate detail: `code/CLAUDE.md`. New Rust
  surfaces require their own charter-lane ruling; external Rust CLIs
  (rtk/herdr/worktrunk) stay arm's-length binaries, never workspace members.
- TypeScript for anything in `analyzing/src/`; a Python microservice is analyzing's allowed escape hatch for heavy numerics (e.g. `analyzing/scripts/ta_reference.py` uses TA-Lib as ground truth).
- Python for everything in `trading/`.
- Never reach across: trading Python doesn't import analyzing, analyzing TS doesn't import trading.
