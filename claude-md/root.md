# qagents — Cross-project conventions

Subprojects under this repo:

Each `<sub>/CLAUDE.md` is the single owner of its own mechanics + spec path; the roster below is the constellation index — name, discriminating role, and cross-boundary relationships only.

- `analyzing/` — market-inspection tooling (TypeScript; local-only viewer): DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed. `financial/parquet/` tape supplier.
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
- `managing/` — daily watcher over the constellation. Cron-fired at 06:00 with the top-tier model; four subagents (checker / planner / reporter / verifier); the verifier promotes `pending/` (§ Shared-data write-lock). **Observe-only** — no push/deploys/mutations; commits + the S5 authority push (verify-pending.sh ff-syncs then pushes `main` to the `github` authority after its audit commits — non-fatal, never forced/deploy) limited to the § 5.3 audit lane.
- `shorting/` — adversarial sibling of `managing/`. On-demand from `/open shorting`: the per-target positions lane (10 numbered "shorting positions", `shorting/positions/<target>/<date>.md`) + the chartered do-shorten / do-share / do-spread review fleets (`shorting/{shorten,share,spread}/<date>/`; `data/charters/shorting/review-lanes/CHARTER.md`). **Observe-only**; routes findings to `managing/`.
- `donating/` — 6-month public donation drive (2026-06-01 → 2026-12-01). Renders `data/donating/drive.json` (consumed by `designing/web` + `documenting/web`). Four exclusive-use buckets. Content-only.
- `publishing/` — open-source release subproject. Owns the public-org staging tree `publishing/quantapix/` and the `/publish` pipeline (sweep → redact → compile → push to `github.com/quantapix/*`). Owns drive Promise 1. Content-in / external-out; **not** observe-only.
- `rendering/` — in-house render engine + brand source of truth; single owner of **brand-bearing, pre-rasterized** artifacts (images + videos) for the whole constellation. Image engine live; video engine post-first-cohort. Deliverables in `data/renders/<consumer>/`.
- `extending/` — Claude Desktop extensions + enablement; spec-of-record `data/specs/extending-2026-07-13/SPEC.md` (consolidated family). Two halves: EXTEND — `servers/{qnarre,qresev}-mcp/` Node stdio MCP servers (thin proxies over verifying:8787 / evaluating:8788; never a fourth Lean consumer) as `.mcpb` bundles via the `publishing/` lane; ENABLE — `enablement/` Desktop-adoption assets + the dual-multiplexer lane (cmux local cockpit / herdr remote LAN multiplexer — detail in the spec family). Content-in / external-out via publishing.
- `developing/` — native macOS + iOS SwiftUI clients for Qnarre + Qresev; XcodeGen + SPM monorepo (`project.yml` is SoT). Never a fourth Lean consumer; future live wiring goes over the verifying:8787 / evaluating:8788 seams. Swift-only.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets + cross-cutting machinery (`status/`, `schedules/`, `specs/`, `renders/`, `donating/`, …). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule); spec `data/specs/data-charter-2026-05-17/SPEC.md`. Market/trading datasets live in the top-level `financial/` hub (below).
- `data/schedules/` — canonical macOS-launchd cron for **all** subprojects. Single `ROUTINES` array in `data/schedules/launchd/install.sh`; `run_routine.sh` is the per-fire wrapper. **Never** use cloud `/schedule` or `RemoteTrigger` — cowork sandbox can't mount the repo.
- `data/renders/` — rendered deliverables + legacy design handoff bundles: migrated consumers hold **outputs only** at `data/renders/<consumer>/`; unmigrated bundles stay at `data/renders/<sub>-design/` (read-only, wholesale-regen). See `data/renders/MANIFEST.md`.
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `parquet/` (OHLCV, `ta-reference/`, `gics-symbols.parquet`), `portfolios/`, `reports/`, `universe/`, `gics/`. Consumers: `trading/`, `analyzing/`, `accounting/`; cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md`; shares the root `.data-write-lock` (below).
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject (sibling-of-subprojects). Packages: `playwright/` · `remotion/` · `agent_sdk/` · `qreel/` · `lean_graph/` · `lean_tools/` · `lint/` · `web/` · `ledger/` · `flow_graph/`. Per-package purpose + spec pins + runnable-only-at-canonical note: `code/CLAUDE.md`. (`code/` membership via `workspace:*` is the chartered exception to the "no cross-subproject imports" seam law — it governs only subproject↔subproject edges; detail: `code/CLAUDE.md` § Seam-law exception.)
- `lib/` — vendored upstream code; sibling of `code/`. Today: `lib/memsearch/` (vendored+patched; see § memsearch for the qagents patch detail); `lib/heygen-skills/` (vendored-pristine, MIT). Governance classes: vendored-pristine / vendored+patched / reference-only. See per-package `UPSTREAM.md`.
- `hub/` — read-only upstream clones, regularly refreshed, **gitignored wholesale** (canonical-only, absent from worktrees); reference ground truth, never committed or imported as code. Five Lean4 guide-rail rows chartered (`studying/guide-rails.md`); other clones are ungoverned conveniences.

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only conventions that cross a boundary; subproject-specific rules live in each subproject's own `CLAUDE.md`.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13); all cross-subproject deps in root `pyproject.toml` `[project.optional-dependencies]` extras (the extras list lives there — don't mirror it here). Bootstrap from a fresh checkout:

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
./.venv/bin/pip install -e '.[trading,analyzing,dev]'
./.venv/bin/pip install -e ./trading --no-deps         # registers `shared` / `shared.lib`
./.venv/bin/pip install -e ./code/agent_sdk --no-deps  # registers `qagents.agent_sdk`
./.venv/bin/pip install -e ./code/ledger --no-deps     # registers `qagents.ledger`
./.venv/bin/pip install -e ./code/flow_graph --no-deps # registers `qagents.flow_graph`
```

From repo root → `./.venv/bin/python …`. From a subproject → `../.venv/bin/python …`. The `proving/`/`accounting/` drivers + status emitters run on system `python3`; accounting's pandas helpers (`data_view.py`, `universe_graph.py`) are the venv exception. (`monitoring/` is TypeScript-only — no Python.)

Machine provisioning/repair (venv + editables + profile marker + elan + pnpm, idempotent): `bash scripts/bootstrap-machine.sh [--profile full|trading-lane] [--check]`; env drift detection: `scripts/parity.sh` (`data/specs/workstation-parity-2026-07-21/SPEC.md` — single owner of cross-workstation parity).

## Shell scripts — homebrew tool versions

Any shell script (cron-fired, operator-fired, or session-invoked) MUST resolve to homebrew-installed tools, not macOS system defaults. macOS ships bash 3.2.57 (no `mapfile`/`readarray`/`declare -A`/`${var^^}`), no GNU coreutils, BSD `sed`/`awk`/`date`.

1. **Cron lane PATH** — `data/schedules/launchd/install.sh` plist template lists `/opt/homebrew/bin` first; `--enable` regenerates every plist.
2. **Portable scripts as belt-and-suspenders** — avoid bash-4+ features, prefer POSIX flags; homebrew-only features by absolute path (`/opt/homebrew/bin/gdate`). Recipes + audit patterns: memory `feedback_homebrew_over_system_for_qagents_scripts`.
3. **Sibling-of-subprojects pkgs are *runnable* only at canonical.** Worktrees check out `code/`/`lib/`/`serving/` source but not gitignored build state. Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths.

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. Node code (CLIs, CDK, kit packages).
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's presets. Vendored `lib/` is upstream-owned.

### pnpm workspace + catalog

Single workspace at root: `pnpm-workspace.yaml` owns the member list (don't mirror it here), the shared-dev-tool catalog (`"typescript": "catalog:"`), and the native post-install build allow-list (`allowBuilds`, pnpm 11). Root scripts: `pnpm {typecheck,build,verify}` → `pnpm -r --if-present <name>`.

### Playwright e2e (Astro sites)

Suites at `<sub>/web/tests/e2e/`; shared helpers at `code/playwright/`. Each `playwright.config.ts` runs three projects (chromium-desktop / -mobile / -reduced-motion); `webServer = pnpm build && pnpm preview` — never the dev server. Run: `pnpm -C <sub>/web test:e2e`. First-time: `test:e2e:install` — but run the browser install **once at canonical**, never per-worktree (a worktree's cache registration dies at `/close` and the next install GCs + re-downloads ~165 MB; mechanism: memory `reference_playwright_browser_cache_worktree_gc`).

**Preview-port registry** (claim the next free port before adding an Astro e2e suite; single owner — no two configs may collide): `code/playwright/PORTS.md`.

**Reduced-motion emulation** — a bare `reducedMotion: 'reduce'` under a project's `use:` is NOT a Playwright TestOption; it is silently ignored. Emulation only applies via `use: { contextOptions: { reducedMotion: 'reduce' } }`. Per-site fix-me list (which suites still carry the ignored bare key): memory `project_playwright_e2e_stack`.

### IDE + parallel-session coordinator (cmux)

VSCode (stable) is a plain editor — no canonical-IDE claim (`analyzing/` ships no VSCode extension; operator ruling 2026-07-12). Parallel Claude Code sessions are coordinated by **cmux** (`/Applications/cmux.app`, brew cask; wrapper `scripts/cmux-session.sh`; socket defaults `cmuxOnly`, else typed exit 26) — spec `data/specs/extending-2026-07-13/cmux-coordinator-2026-07-12/SPEC.md`. (monitoring's web app runs under plain Node — Node-ABI mismatch: see monitoring/CLAUDE.md's better-sqlite3 rebuild note.)

## Canonical OHLCV bar shape

The bar-column contract (`ts/o/h/l/c/v/adj_c`) shared by all three consumers (`trading/`, `analyzing/`, `accounting/`) lives in `financial/parquet/CLAUDE.md` § "Canonical OHLCV bar shape" — the hub is its single source of truth. Adapters translate vendor field names at the boundary; never leak them past the client module.

## GICS sector / industry classification

GICS mapping is *shared data, not shared code*: parquet at `./financial/parquet/gics-symbols.parquet` keyed by `symbol`. Sector strings are the 11 canonical GICS long-form names.

- Readers: `analyzing/src/data/gics.ts` (DuckDB view `gics`) + `python -m shared.lib.gics`. Neither side writes the parquet — seed/refresh via `financial/gics/build.py`; schema + caveats: `financial/gics/mapping.md`.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`

Sessions start with `/open <project>` and end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints. The memory + CLAUDE.md optimization lane (`/dco-manual` standing; `/dco` cron parked) is chartered at `data/charters/qagents/optimization/CHARTER.md`. **Single normative owner: `data/charters/qagents/session-lifecycle/CHARTER.md`** — the one-liners below render its anchors; on any divergence, trust the charter (mechanics/orchestrator layers: charter § 2.2).

- **Lock model** (charter § 2.1 / § lock-model): branch-presence IS the write-lock; `<project>`/`<project>-N` blocks conflicting `/open`s, `/open qagents` blocks all. The session-branch grammar `^[a-z]+(-[0-9]+)?$` is the ONE lock-holder definition; slash-named refs (`lift/*`, `<node>/*`) are never lock conflicts.
- **Worktree path discipline (load-bearing)** (charter § 2.3 / § path-discipline): inside any `/open` session, every `Edit`/`Write` `file_path` MUST begin with the worktree root `<root>-wt/<branch>/` — a canonical `<root>/...` edit lands on `main`, silently bypassing the lock. Enforced by `scripts/hooks/no-canonical-edit-while-locked.sh`; reads may use canonical; cron-lane fires (no session branch) write canonical cwd-relative paths. See `feedback_worktree_path_determines_working_tree`.
- **Canonical-shared gitignored content** (charter § 2.4): declared per owner in `<sub>/.worktree-links`, symlinked into worktrees by `scripts/open.sh` (only pure-gitignored dirs). **Walkers must dereference (`tar -h`, `rsync -aL`) or hard-refuse** — `find` does not descend a symlinked dir (memory `project_parquet_gitignored_ground_truth`).
- **Bash discipline (load-bearing)** (charter § 2.2): close-lane bash uses absolute script paths only — each path form needs a separate allow-list matcher.
- **Cross-subproject writes** (charter § 2.7): a `close.sh` exit-14 foreign write is resolved via `scripts/lift.sh` (live spec: `data/specs/open-close-dcu-2026-05-26/lift-encapsulated-fixes-2026-06-08/SPEC.md`).
- **Stack** (charter § 2.1): strict — `<project>-N` parents on `<project>-(N-1)`. Closes cascade up; `--to-main` walks the stack to `main`.
- **Sentinels** (charter § 2.1): `.dot-claude-write-lock` (`/close` memory phase, `/dco`) + `.data-write-lock` (§ Shared-data write-lock; also `/dco`), root-anchored, gitignored; `/dcu` rides its own branch merge, no sentinel.
- **CLAUDE.md updates** (charter § 2.6 / charter § 2.9): *immediate* (project's own CLAUDE.md on session branch) + *deferred hints* (`data/claude-updates/<branch>.md`; `/do-claude-updates` judges later).
- **Adopted-spec convention** (`data/charters/qagents/spec-lifecycle/CHARTER.md` § 2.7): in-flight `data/tmp/` specs relocate to the family dir `data/specs/<slug>-<date>/SPEC.md` once cited — the only valid `data/specs/` shape.
- **Session summaries** (charter § 2.8): `/close` writes `data/summaries/close/<YYYY-MM-DD>T<HHMM>-<branch>.md` — versioned, never overwritten.
- **Per-project next-steps** (charter § 2.8): `data/next-steps/<project>.md` forward-only slot — a GENERATED render of `ledger.ns_item_event`; write via `python -m qagents.ledger ns-{add,retire,rephrase,move}`, never by hand (detail belongs to close summaries); resolution-verb commit cites (`resolves ns-item N` — the verb is mandatory) fire the close-time `--next-steps` gate (exits 24/25); `/open` renders the slot as the footer's Outstanding rows.

## Model policy — LLM model selection

Complex, long-running work (subagent fan-outs, axiomatization, watchers, debates, collectors, overnight research) runs the **top-tier model** — never a pinned older tier. In practice that is **Opus 4.8** (`opus` alias): the absolute-latest tier (Fable 5) exhausts the Max-20x subscription quota within days. Review/optimization subagent fleets (dco, shorting positions, do-shorten/do-share/do-spread) carry **no `model:` pins** and inherit the model the orchestrator was invoked with — invoke the orchestrator on opus when Max-20x quota is tight (operator ruling 2026-07-05; memory `project_model_policy_latest_top_tier`). When a sustainable new top tier ships, sweep the pins; prose says "top-tier model", not a name. The three axiomatization lanes (`/dau`/`/dat`/`/dao`) resolve their model from ONE seat — `code/lean_tools/model_floor.py` (`QAGENTS_AXIOMATIZE_MODEL` flips all three; legacy `QAGENTS_PREDICATE_MODEL` honored second); sweep THAT switch, not per-axis pins. Lesser models only where flagged: `sonnet` for bounded cron routines (intraday trading reviews, journaling, leaderboard), `haiku` for mechanical closed-set classification (`managing` verifier) and throwaway smoke runs. Cron model selection uses **bare tier aliases** (`opus`/`sonnet`/`haiku`) — never pinned minor versions. `run_routine.sh` fail-closes the lane: refuses `ANTHROPIC_API_KEY` billing (deliberate override `QAGENTS_ALLOW_API_BILLING=1`) and refuses any Fable model, no override (manual `/dau-manual` sessions bypass the wrapper); guard test `data/specs/cron-ec2-migration-2026-05-19/tests/cases/t_11_billing_guard.sh`. **Capability floor:** haiku is forbidden for any retained axiomatization artifact; amendments are per-leaf-class only, via the five-point bake-off gate (default stays top-tier, exit-3-enforced in the driver) — gate criteria + bake-off history + `proving/scripts/bakeoff_tier1.py` ledger: memory `feedback_predicate_model_opus_not_haiku`. Cron-lane budget caps (`MAX_BUDGET_USD`, `routines.toml` `max_budget_usd`) sit at opus-4.7-era sizing — widen them, never downgrade the model.

## Programmatic Claude — Agent SDK lane

The Agent SDK lane is **parked** — Anthropic dropped SDK credits from the Max-20x subscription (2026-06-15); the `:sdk` fleet reverted 2026-06-30 and every routine runs the default `claude --print` lane. **Root § Agent SDK lane owns this status** (other units point here). Standing label (operator ruling 2026-07-16): all SDK usage is **"to-be-re-considered in the future"** — never a live dependency; it is a flow-graph **parked target** (`ext:agent-sdk-credit`, excluded from every bottleneck/dependency metric — flow-graph spec § 5.3) and no session spends further effort on SDK contingency planning until an official Anthropic reversal. Mentions, code, and tests are retained as-is. When SDK access returns: the typed Python wrapper is `code/agent_sdk/` (`qagents.agent_sdk`; shared by `trading/` + `managing/`); routines opt back in by restoring the `:sdk` suffix on routine names in `data/schedules/launchd/install.sh` ROUTINES. Adoption spec: `data/specs/agent-sdk-adoption-2026-05-17/SPEC.md`; see the ROUTINES comment + `feedback_managing_suppress_sdk_findings`. Ledger at `data/agent-sdk-ledger/` still tracks usage. On official Anthropic reversal, `git log -S ext:agent-sdk-credit -- data/next-steps/` recovers the parked items and flipping `data/next-steps/terminals/ext-agent-sdk-credit.md` to `state: open` un-parks them everywhere.

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) the shared `data/` **and** `financial/` hubs only while holding `<root>/.data-write-lock` (one lock serializes both).

**Shared ledger store (Postgres — qred LAN primary) is the canonical mechanism for new shared ledger-like data** (single shared file, many appenders) — ledger-shaped surfaces start as a store table + single-writer rendered git projection, never a new hand-appended shared file. Single owner: `data/specs/shared-ledger-store-2026-07-09/SPEC.md` (§ 2, § 5, § 13.4).

- Cron-fired writes never touch `data/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync. The verifier is a **closed-set allow-list** classifier — register a new `pending/` producer path in lockstep in `managing/.claude/agents/verifier.md` + `verify-pending.sh require_known_canonical_subtree`, else its files land in `unclassified[]`, never promoted. Spec: `data/specs/pending-promotion-scope-2026-05-28/SPEC.md`.
- Everything else — manual fixed-path writers (atomic create + EXIT-trap release), configurable-output-path scripts (lock **iff** the target is canonical `data/`/`financial/`), the `QAGENTS_PENDING_ROOT` cron/manual branch — per `data/specs/data-conventions-2026-05-06/SPEC.md` § 4/§ 5.3 (single owner).

## Subproject `.claude/` shape (consistent pattern)

Every subproject that runs Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed allow/deny + the standard hook set (three `PreToolUse` + `WorktreeCreate` refuse-by-default / `WorktreeRemove` log-only; roster: `data/claude-settings/sources/baseline.hooks.json`). **Generated, not hand-edited** — edit `data/claude-settings/sources/`, re-run `scripts/claude-settings/build.py` (drift: `--check`). Runtime permissions = user scope `~/.claude/settings.json` (cwd-only load) ∪ cwd-project scope; allow entries need a trailing `*` on a literal prefix. Spec: `data/charters/qagents/specs/claude-settings-unification-2026-06-06/SPEC.md` + `reference_claude_code_allow_glob_no_empty_match`.
- `<sub>/.claude/settings.local.json` — user-local overrides (gitignored); the `dco-settings` weekly harvest (parked with the SDK lane) proposes additive-only edits to `data/claude-settings/sources/` — the source tier, never generated files.
- `<sub>/.claude/skills` → symlink to `../../.claude/skills`.
- `<sub>/.claude/agents/` — optional per-subproject sub-agent definitions.

## Skill placement rules

- `./.claude/skills/` — cross-project skills (auto-loaded via each subproject's `skills` symlink).
- **Subproject-scoped skills** (not auto-loaded; invoked explicitly):
  - `trading/shared/skills/` — trading-only.
  - `trading/agents/<pm>/.claude/skills/` — PM-scoped.
  - the private filing hub — Combined RA agent team (1 coordinator + 10 volume agents); callable by drafting siblings (`appealing/`, `pleading/`).

## memsearch — semantic memory across qagents sessions

Vendored at `lib/memsearch/` as a Claude Code plugin. Install + per-subproject `qagents patch` (eight patches) + backend detail in `lib/memsearch/CLAUDE.md` § "qagents integration"; recall skill is namespaced `memsearch:memory-recall`. Retained invariants: **markdown is source of truth** (`<sub>/.memsearch/memory/YYYY-MM-DD.md`; Milvus is a derived, rebuildable index; tree gitignored); **worktree logs survive `/close`** (`qs memsearch copyback` — substrate crate engine); **recall is fork-isolated** (`context: fork`).

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

One server today: `heygen` (http, OAuth — requires Chrome; toolspace `mcp__heygen__*`; HeyGen Creator plan) — config at `explaining/.mcp.json`; vendored skills under `lib/heygen-skills/` (MIT), symlinked from `.claude/skills/`.

**Subproject-scoped, not repo-rooted.** `.mcp.json` lives at `<sub>/.mcp.json` — Claude Code walks up from launching cwd, so `/open <sub>` finds only its own MCP. Today only `explaining/.mcp.json` is wired; `<sub>/.claude/settings.json` allow-lists `mcp__<server>__*` to enable them.

DaVinci Resolve scripting goes through the typed Python wrapper at `resolving/davinci/` (no MCP).

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (schema owner v0.7.0, `SubprojectId` closed set = 24 subs); `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS/Python imports — the JSON hub is the only seam.

- **Whole-slot failure trap (every `/close --status-emit`):** a SINGLE contract-violating field drops the ENTIRE slot to placeholder on prod (field examples: memory `project_diagram_kit`). Producers **coerce booleans to a string/number and OMIT a metric rather than emit `null`**; never ask the consumer (`designing/web/src/lib/status-loader.ts`, Zod-validated) to loosen its schema.
- **Public surface — synthetic fixtures only:** every slot renders publicly at `quantapix.com/status/<sub>`, so a producer whose inputs can carry real matter MUST filter to synthetic/allow-listed fixtures (mirror `verifying/server/main.py ALLOWED_EXAMPLE_IDS`) — never real dockets/positions (`<live-matter>_*`). Fleet rule + owed close-time denylist scan: `data/specs/data-status-rename-2026-05-17/SPEC.md` § 11; memory `reference_operational_axis_public_surface_privacy`.
- Producer/orchestrator/close-time-emit/pending-aware-cron/KIT_VERSION-lockstep + the eight-surface add-a-subproject sweep: memory `project_diagram_kit` § "Root § Status hub". Specs: `data/specs/data-status-rename-2026-05-17/SPEC.md` § 4/§ 4.3 + `data/charters/qagents/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`.

## Kit-mount pattern

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`; three live instances mount the ONE domain-neutral graphs kit (`@qagents/graphs`) at `graphs/` — verifying + evaluating + monitoring (the legacy `graphs2/` mount-dir name is now **retired constellation-wide 2026-07-22** — these three consumers + analyzing renamed, `designing/` renamed its `/thesis` hero mount then removed its dormant method-DAG mount wholesale, and the shared `code/web/assets/mount-skeleton.js` `kitSrc` default flipped `/graphs2/`→`/graphs/`). A mount's `tokens-*.css` and its `kit.js` are a **lockstep pair** — re-copy both or neither: a token overlay lifted without its bundle is inert (undefined custom property → `||` fallback, silently, every gate green). Full instance roster (incl. monitoring's `/proof` mount) + regen-wholesale/rebuild-canonical-dist/`getComputedStyle`-verify/commit-vs-gitignore discipline + schema/edge-kinds: memory `project_proof_graph_kit_mount_pattern`.

## Lean4 axes — three kernels, one architecture

Three orthogonal axes, never sharing domain/ground-truth/consumer: **textual** `proving/` (`legal/uscode/`; plaintiff v. defendant; → `verifying/`), **numerical** `accounting/` (`financial/parquet/`; bulls v. bears; → `evaluating/`), **operational** `studying/` (git first; `hub/git`; coding v. testing; → `monitoring/`, local-only). Seven invariants headline (axiomatic kernel + LLM `Facts.lean` + `lake build` gate; **no human proof-driving, ever**; parallel top-tier debate under closed oracle channels; toolchain lockstep; one consumer per axis; `visualizing/`+kit-mount presentation; G1–G7 hard-gated each wave) live in memory `project_lean4_three_axis_charter` § "Root § Lean4 axes". Spec `data/charters/studying/specs/lean4-charter-2026-06-10/SPEC.md` § 4 + the `axiomatize-shared-2026-07-04/` declared-child subspec (COMMON mechanism + LEARNINGS ledger + G1–G7 matrix). **Per-axis scope charters (2026-07-17):** `data/charters/studying/operational-axis/CHARTER.md` (neutral steward of the whole cross-axis `lean4-charter` family), `data/charters/proving/textual-axis/CHARTER.md`, `data/charters/accounting/numerical-axis/CHARTER.md`.

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools. The allow-list refusal is one input to `evaluating/`'s **FINANCIALLY-CLEARED** gate (§ subproject list, `evaluating/`), which signs off any public surface that evaluates or implies a financial decision — a kernel refusal, never a safety guarantee.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` multi-remote setup live in `serving/CLAUDE.md` § 8–§ 10 (single owner — deploy script, four-remote roster, aws-vault + Keychain, local network `qblk`/`qred`/`qyel`; never duplicated here or in subproject CLAUDE.mds). Cross-machine session exchange rides the same qblk/qred mirrors as the symmetric leaf-`/push` / hub-`/pull` cycle (`<node>/<topic>` refs; hub = sole merge-point): `data/specs/push-pull-redesign-2026-07-18/SPEC.md`.

## Language split

- Rust for the session-lifecycle substrate: `code/substrate/` (crate
  `qagents-substrate`, bin `qs`) is the FIRST of two in-repo Rust authoring
  surfaces; it implements the session-lifecycle mechanics layer (charter
  `data/charters/qagents/session-lifecycle/`) and nothing else. New Rust
  surfaces require their own charter-lane ruling. External Rust CLIs
  (rtk/herdr/worktrunk) stay arm's-length binaries, never workspace members.
- Rust for the context-transformation layer: `code/context/` (crate
  `qagents-context`, bin `qx`) is the SECOND in-repo Rust authoring surface; it
  implements context injection (the PCI lane's mechanism layer — contract owner
  stays the PCI spec family), conservative output shortening, and the semantic-
  memory (memsearch) replacement
  (specs `rust-context-2026-07-22` + `rust-memsearch-2026-07-22`) and nothing else.
- TypeScript for anything in `analyzing/src/`; a Python microservice is analyzing's allowed escape hatch for heavy numerics (e.g. `analyzing/scripts/ta_reference.py` uses TA-Lib as ground truth).
- Python for everything in `trading/`.
- Never reach across: trading Python doesn't import analyzing, analyzing TS doesn't import trading.
