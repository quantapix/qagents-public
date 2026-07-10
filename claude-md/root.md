# qagents — Cross-project conventions

Subprojects under this repo:

Each `<sub>/CLAUDE.md` is the single owner of its own mechanics + spec path; the roster below is the constellation index — name, discriminating role, and cross-boundary relationships only.

- `analyzing/` — VSCode extension (TypeScript) for market inspection: DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed. `financial/parquet/` tape supplier + local-only viewer.
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
- `managing/` — daily watcher over the constellation. Cron-fired at 06:00 with the top-tier model; four subagents (checker / planner / reporter / verifier); the verifier promotes `pending/` (§ Shared-data write-lock). **Observe-only** — no push/commit/deploys/mutations.
- `shorting/` — adversarial sibling of `managing/`. On-demand `/open shorting`; one top-tier-model subagent per target produces 10 numbered "shorting positions" under `shorting/positions/<target>/<date>.md`. **Observe-only**; routes findings to `managing/`.
- `donating/` — 6-month public donation drive (2026-06-01 → 2026-12-01). Renders `data/donating/drive.json` (consumed by `designing/web` + `documenting/web`). Four exclusive-use buckets. Content-only.
- `publishing/` — open-source release subproject. Owns the public-org staging tree `publishing/quantapix/` and the `/publish` pipeline (sweep → redact → compile → push to `github.com/quantapix/*`). Owns drive Promise 1. Content-in / external-out; **not** observe-only.
- `rendering/` — in-house render engine + brand source of truth; single owner of **brand-bearing, pre-rasterized** artifacts (images + videos) for the whole constellation. Image engine live; video engine post-first-cohort. Deliverables in `data/renders/<consumer>/`.
- `extending/` — Claude Desktop extensions + enablement. Two halves: EXTEND — `servers/{qnarre,qresev}-mcp/` Node stdio MCP servers (thin proxies over verifying:8787 / evaluating:8788; allow-listed replay, gates mirrored, never a fourth Lean consumer) as `.mcpb` bundles via the `publishing/` lane; ENABLE — `enablement/` Desktop-adoption assets. Content-in / external-out via publishing.
- `developing/` — native macOS (and next iOS) SwiftUI clients for Qnarre + Qresev; XcodeGen + SPM monorepo (`project.yml` is SoT). Never a fourth Lean consumer; future live wiring goes over the verifying:8787 / evaluating:8788 seams. Swift-only; adopted 2026-07-07.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets + cross-cutting machinery (`data/status/<sub>.json` status-emit slots, `data/schedules/`, `data/specs/`, `data/renders/`, `data/donating/`, …). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule); load-bearing spec `data/specs/data-charter-2026-05-17/SPEC.md`. Market/trading datasets promoted to the top-level `financial/` hub (below).
- `data/schedules/` — canonical macOS-launchd cron for **all** subprojects. Single `ROUTINES` array in `data/schedules/launchd/install.sh`; `run_routine.sh` is the per-fire wrapper. **Never** use cloud `/schedule` or `RemoteTrigger` — cowork sandbox can't mount the repo.
- `data/renders/` — rendered deliverables + legacy Claude Design handoff bundles. Migrated consumers hold **outputs only** at `data/renders/<consumer>/`; unmigrated bundles stay at `data/renders/<sub>-design/` (read-only, replaced wholesale on regen) until their rendering P4 slot. See `data/renders/MANIFEST.md`.
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `financial/parquet/` (OHLCV, `ta-reference/`, `gics-symbols.parquet`), `financial/portfolios/`, `financial/reports/`, `financial/universe/`, `financial/gics/` (`build.py` + `mapping.md`). Consumers: `trading/`, `analyzing/`, `accounting/`. Cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md`; shares the root `.data-write-lock` (below).
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject. Today: `code/playwright/` (shared `@playwright/test` helpers), `code/remotion/` (`@qagents/remotion`; `explaining/` B-roll), `code/agent_sdk/` (`qagents.agent_sdk` — typed `claude-agent-sdk` wrapper; § Agent SDK lane), `code/qreel/` (`/reel <bundle>` bake pipeline; spec `data/specs/qreel-2026-05-28/SPEC.md`), `code/lean_graph/` (`qagents.lean_graph` — cross-axis Lean4-aware K-graph extractor for quantify-progress; spec `data/specs/lean4-charter-2026-06-10/quantify-progress-2026-06-14/SPEC.md`). Subproject-owned workspace packages stay in their subproject.
- `lib/` — vendored upstream code; sibling of `code/`. Today: `lib/memsearch/` (vendored+patched; see § memsearch for the qagents patch detail); `lib/heygen-skills/` (vendored-pristine, MIT). Governance classes: vendored-pristine / vendored+patched / reference-only. See per-package `UPSTREAM.md`.
- `hub/` — read-only upstream clones, regularly refreshed, **gitignored wholesale** (canonical-only, absent from worktrees); reference ground truth, never committed or imported as code. The five Lean4 guide-rail rows are chartered (`studying/guide-rails.md`; `data/specs/lean4-charter-2026-06-10/SPEC.md` § 6); other clones are ungoverned consumer conveniences.

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only conventions that cross a boundary; subproject-specific rules live in each subproject's own `CLAUDE.md`.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13); all cross-subproject deps in root `pyproject.toml` `[project.optional-dependencies]` extras (the extras list lives there — don't mirror it here). Bootstrap from a fresh checkout:

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
./.venv/bin/pip install -e '.[trading,analyzing,dev]'
./.venv/bin/pip install -e ./trading --no-deps         # registers `shared` / `shared.lib`
./.venv/bin/pip install -e ./code/agent_sdk --no-deps  # registers `qagents.agent_sdk`
```

From repo root → `./.venv/bin/python …`. From a subproject → `../.venv/bin/python …`. The `proving/`/`accounting/` drivers + status emitters run on system `python3`; accounting's pandas helpers (`data_view.py`, `universe_graph.py`) are the venv exception. (`monitoring/` is TypeScript-only — no Python.)

## Shell scripts — homebrew tool versions

Any shell script (cron-fired, operator-fired, or session-invoked) MUST resolve to homebrew-installed tools, not macOS system defaults. macOS ships bash 3.2.57 (no `mapfile`/`readarray`/`declare -A`/`${var^^}`), no GNU coreutils, BSD `sed`/`awk`/`date`.

1. **Cron lane PATH** — `data/schedules/launchd/install.sh` plist template lists `/opt/homebrew/bin` first; `--enable` regenerates every plist.
2. **Portable scripts as belt-and-suspenders** — outside the cron lane, avoid `mapfile` (use `while IFS= read -r line; do …; done < <(cmd)`), prefer POSIX flags. For homebrew-only features (e.g. `date -d '3 days ago'`), invoke by absolute path (`/opt/homebrew/bin/gdate`).
3. **Sibling-of-subprojects pkgs are *runnable* only at canonical.** Worktrees check out `code/`/`lib/`/`serving/` source but not gitignored build state. Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths.

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. VSCode extension hosts + Node code.
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's presets. Vendored `lib/` is upstream-owned.

### pnpm workspace + catalog

Single workspace at root: `pnpm-workspace.yaml` owns the member list (subproject webs + `code/*` + `serving/*` + `visualizing/*` — don't mirror it here), the shared-dev-tool catalog (`"typescript": "catalog:"`), and the native post-install build allow-list (`allowBuilds`, pnpm 11; legacy `onlyBuiltDependencies` kept in lockstep). Root scripts: `pnpm {typecheck,build,verify}` → `pnpm -r --if-present <name>`.

### Playwright e2e (Astro sites)

Suites at `<sub>/web/tests/e2e/`; shared helpers at `code/playwright/`. Each `playwright.config.ts` runs three projects (chromium-desktop / -mobile / -reduced-motion); `webServer = pnpm build && pnpm preview` — never the dev server. Run: `pnpm -C <sub>/web test:e2e`. First-time: `test:e2e:install`.

**Preview-port registry** (claim the next free port before adding an Astro e2e suite; single owner — no two configs may collide): `code/playwright/PORTS.md`.

### IDE: stable VSCode

Canonical IDE is stable VSCode. `analyzing/`'s VSCode extension uses N-API bindings — unaffected by Electron ABI switches. (monitoring's web app runs under plain Node — `pnpm rebuild better-sqlite3` on any Node-ABI mismatch.)

## Canonical OHLCV bar shape

The bar-column contract (`ts/o/h/l/c/v/adj_c`) shared by all three consumers (`trading/`, `analyzing/`, `accounting/`) lives in `financial/parquet/CLAUDE.md` § "Canonical OHLCV bar shape" — the hub is its single source of truth. Adapters translate vendor field names at the boundary; never leak them past the client module.

## GICS sector / industry classification

GICS mapping is *shared data, not shared code*: parquet at `./financial/parquet/gics-symbols.parquet` keyed by `symbol`. Sector strings are the 11 canonical GICS long-form names.

- Readers: `analyzing/src/data/gics.ts` (DuckDB view `gics`) + `python -m shared.lib.gics {lookup|sectors|concentration}`.
- Neither side writes the parquet — seed/refresh via `./.venv/bin/python financial/gics/build.py` (yfinance seed). Schema + caveats: `financial/gics/mapping.md`.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`

Sessions start with `/open <project>` and end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints.

- **Spec:** `data/specs/open-close-dcu-2026-05-26/SPEC.md` (consolidated triad). Mechanics in `scripts/{open,close,dcu}.sh` + shared footer `scripts/lib/footer.sh`; the skills are thin orchestrators. A `close.sh` exit-14 cross-subproject write is resolved via `scripts/lift.sh` (`data/specs/open-close-dcu-2026-05-26/lift-encapsulated-fixes-2026-06-08/SPEC.md`). Logs at `pending/logs/`. **Bash discipline (load-bearing):** the close skill uses absolute paths only (`<root>/scripts/close.sh ...`) — never `./` or `scripts/...` — each path form needs a separate allow-list matcher.
- **Lock model:** branch-presence IS the write-lock. `<project>` (or stacked `<project>-N`) blocks parallel `/open`s of conflicting scope. `/open qagents` blocks all subproject opens.
- **Worktree path discipline (load-bearing):** inside any `/open <project>` session — `<sub>` **or** whole-repo `qagents` — every `Edit`/`Write` `file_path` MUST begin with the worktree root `<root>-wt/<branch>/`. A canonical `<root>/...` edit lands on `main`, silently bypassing the lock. Holds for every tracked dir, shared hubs and `code/`+`lib/`+`serving/` alike; only gitignored build state (`node_modules`/`.venv`) is canonical-only (§ Shell scripts pt 3). Enforced by `scripts/hooks/no-canonical-edit-while-locked.sh` (allow-list = sentinels + `pending/`; bypass `QAGENTS_BYPASS_CANONICAL_LOCK=1`). Reads may use canonical. **Cron-lane carve-out:** autonomous `run_routine.sh` → `claude --print` fires have no session branch — they write canonical cwd-relative paths, never a `qagents-wt/<branch>/` root. Spec: `data/specs/open-close-dcu-2026-05-26/canonical-edit-hook-tightening-2026-05-28/SPEC.md`. See `feedback_worktree_path_determines_working_tree`.
- **Canonical-shared gitignored content (`.worktree-links`):** large regenerable canonical-only ground truth (parquet, USC corpus, renders, CDN video mirror) is declared per owner in `<sub>/.worktree-links` (one glob/line) and symlinked into every worktree by `scripts/open.sh`. Symlinks-into-canonical are teardown-safe; only **pure-gitignored** dirs (no tracked files) are symlinkable. Spec: `data/specs/open-close-dcu-2026-05-26/SPEC.md` § 8.14.
- **Stack:** strict — `<project>-N` parents on `<project>-(N-1)`. Closes cascade up; `--to-main` walks the stack to `main`.
- **Sentinels:** `.dot-claude-write-lock` and `.data-write-lock` (root-anchored, gitignored), held only inside `/close` and `/do-claude-updates`.
- **CLAUDE.md updates:** *immediate* (project's own CLAUDE.md on session branch) + *deferred hints* (cross-subproject prose in `data/claude-updates/<branch>.md`; `/do-claude-updates` judges later).
- **Adopted-spec convention:** in-flight at `data/tmp/<slug>-<date>{/SPEC.md,.md}`; relocate to the family dir `data/specs/<slug>-<date>/SPEC.md` once cited. Family layout is the only valid `data/specs/` shape (migration completed 2026-06-10). Full lifecycle + family/tests shape: `data/specs/CLAUDE.md` + `data/tmp/CLAUDE.md`.
- **Session summaries:** `/close` writes `data/summaries/<YYYY-MM-DD>T<HHMM>-<branch>.md` — versioned, never overwritten.
- **Per-project next-steps:** `data/next-steps/<project>.md` forward-only "what's left" surface; items deleted on resolution (resolution detail belongs to close summaries). Commit cites `(next-steps item|ns-item) N` trigger the close-time `--next-steps` gate (exits 24/25). `/open <project>` renders the slot as the footer's Outstanding rows.

## Model policy — LLM model selection

Complex, long-running work (subagent fan-outs, axiomatization, watchers, debates, collectors, overnight research) runs the **top-tier model** — never a pinned older tier. In practice that is **Opus 4.8** (`opus` alias / `claude-opus-4-8`): the absolute-latest tier (Fable 5) exhausts the Max-20x subscription quota within days. Review/optimization subagent fleets (dco, shorting positions, do-shorten/do-share/do-spread) carry **no `model:` pins** and inherit the model the orchestrator was invoked with — invoke the orchestrator on opus when Max-20x quota is tight (operator ruling 2026-07-05; memory `project_model_policy_latest_top_tier`). When a sustainable new top tier ships, sweep the pins; prose says "top-tier model", not a name. The three axiomatization lanes (`/dau`/`/dat`/`/dao`) resolve their model from ONE seat — `code/lean_tools/model_floor.py` (`QAGENTS_AXIOMATIZE_MODEL` flips all three; legacy `QAGENTS_PREDICATE_MODEL` honored second); sweep THAT switch, not per-axis pins. Lesser models are acceptable only where flagged: `sonnet` for routine bounded cron routines (intraday trading reviews, journaling, leaderboard), `haiku` for mechanical closed-set classification (`managing` verifier) and throwaway smoke runs. Cron model selection uses **bare tier aliases** (`opus`/`sonnet`/`haiku`) — never pinned minor versions — so the scheduled lane always rides the current tier. `run_routine.sh` fail-closes it: refuses `ANTHROPIC_API_KEY` billing (subscription-only; deliberate override `QAGENTS_ALLOW_API_BILLING=1`) and refuses any Fable model (no override; manual `/dau-manual` axiomatize runs bypass this wrapper, so `QAGENTS_AXIOMATIZE_MODEL=fable` review sessions are unaffected). Guard test: `data/specs/cron-ec2-migration-2026-05-19/tests/cases/t_11_billing_guard.sh`. **Capability floor:** haiku is forbidden for any retained axiomatization artifact; the floor is *measured* and amendable per-leaf-class via a five-point bake-off gate — capability ordering is non-monotonic across leaves (eligibility strictly per-leaf-class, never model-wide; default stays top-tier, exit-3-enforced in the driver). Full gate criteria + bake-off history (2026-06-03 / 2026-06-20 R2.3) + `proving/scripts/bakeoff_tier1.py` ledger: memory `feedback_predicate_model_opus_not_haiku`. Cron-lane budget caps (`MAX_BUDGET_USD`, `routines.toml` `max_budget_usd`) sit at opus-4.7-era sizing — if top-tier routines exit on caps, widen them, never downgrade the model.

## Programmatic Claude — Agent SDK lane

Cron-fired and library-callable Claude work goes through the typed Python wrapper at `code/agent_sdk/` (`qagents.agent_sdk`; verified against `claude-agent-sdk==0.2.82`). Shared by `trading/` and `managing/`. Routines opt into SDK-mode by suffixing the routine name with `:sdk` in `data/schedules/launchd/install.sh` ROUTINES; the default `claude --print` lane stays otherwise. Adoption spec: `data/specs/agent-sdk-adoption-2026-05-17/SPEC.md`. The SDK lane is **parked** — Anthropic dropped SDK credits from the Max-20x subscription (2026-06-15) and the `:sdk` fleet reverted 2026-06-30. Every routine runs the default `claude --print` lane; restore the trailing `:sdk` tokens when SDK access returns. **Root § Agent SDK lane owns this status** (other units point here). See the `install.sh` ROUTINES comment + `feedback_managing_suppress_sdk_findings`. Ledger at `data/agent-sdk-ledger/` still tracks usage.

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) the shared `data/` **and** `financial/` hubs only while holding `<root>/.data-write-lock` (one lock serializes both).

- Cron-fired writes never touch `data/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync. The verifier is a **closed-set allow-list** classifier — register a new `pending/` producer path in lockstep in `managing/.claude/agents/verifier.md` + `verify-pending.sh require_known_canonical_subtree`, else its files land in `unclassified[]`, never promoted. Spec: `data/specs/pending-promotion-scope-2026-05-28/SPEC.md`.
- Manual writers (fixed-path producers — `financial/gics/build.py`, `<sub>/scripts/status_emit.*`) acquire the lock unconditionally with atomic create (`set -C` + redirect), write holder id, release with `rm` on EXIT trap.
- Configurable-output-path scripts (`--out-dir`/`--out`, e.g. `analyzing/scripts/{ingest.py,ta_reference.py}`) acquire the lock **iff** the absolute target falls under canonical `data/` **or** `financial/`. Worktree-local `data/`/`financial/` writes skip the lock — they don't race canonical writers.
- Producers branch on `QAGENTS_PENDING_ROOT`: set (cron) → write `pending/<rel>`, no lock; unset (manual) → acquire lock, write canonical.

Spec: `data/specs/data-conventions-2026-05-06/SPEC.md`.

## Subproject `.claude/` shape (consistent pattern)

Every subproject that runs Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed allow/deny + the three `PreToolUse` hooks (`no-cd-git.sh`, `no-canonical-edit-while-locked.sh`, matcher-scoped `heygen-require-clip-handles.py`) + the `WorktreeCreate` (refuse-by-default → `/open`) / `WorktreeRemove` (log-only) hooks. **Generated, not hand-edited** — edit `data/claude-settings/sources/`, re-run `scripts/claude-settings/build.py` (drift: `--check`). Runtime permissions = user scope `~/.claude/settings.json` (cwd-only load) ∪ cwd-project scope; allow entries need a trailing `*` on a literal prefix. Spec: `data/specs/claude-settings-unification-2026-06-06/SPEC.md` + `reference_claude_code_allow_glob_no_empty_match`.
- `<sub>/.claude/settings.local.json` — user-local overrides (gitignored); the weekly `dco-settings` lane harvests recurring patterns into the generated sources.
- `<sub>/.claude/skills` → symlink to `../../.claude/skills`.
- `<sub>/.claude/agents/` — optional per-subproject sub-agent definitions.

## Skill placement rules

- `./.claude/skills/` — cross-project skills (auto-loaded via each subproject's `skills` symlink).
- **Subproject-scoped skills** (not auto-loaded; invoked explicitly):
  - `trading/shared/skills/` — trading-only.
  - `trading/agents/<pm>/.claude/skills/` — PM-scoped.
  - the private filing hub — Combined RA agent team (1 coordinator + 10 volume agents); callable by drafting siblings (`appealing/`, `pleading/`).

## memsearch — semantic memory across qagents sessions

Vendored at `lib/memsearch/` as a Claude Code plugin. Install + per-subproject `qagents patch` (six blocks) + backend detail in `lib/memsearch/CLAUDE.md` § "qagents integration"; recall skill is namespaced `memsearch:memory-recall`. Retained invariants: **markdown is source of truth** (`<sub>/.memsearch/memory/YYYY-MM-DD.md`; Milvus is a derived, rebuildable index; the tree is gitignored, never tracked); **worktree logs survive `/close`** (copied back to canonical first via `scripts/lib/memsearch-copyback.sh`); **recall is fork-isolated** (`context: fork` keeps the digest out of main context).

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

| Server | Type | Endpoint | Toolspace | Purpose |
|---|---|---|---|---|
| `heygen` | http | `https://mcp.heygen.com/mcp/v1/` (OAuth) | `mcp__heygen__*` | Avatar / voice / video against HeyGen Creator plan |

Vendored skills under `lib/heygen-skills/` (MIT); symlinked from `.claude/skills/`. HeyGen OAuth requires Chrome.

**Subproject-scoped, not repo-rooted.** `.mcp.json` lives at `<sub>/.mcp.json` — Claude Code walks up from launching cwd, so `/open <sub>` finds only its own MCP. Today only `explaining/.mcp.json` is wired; `<sub>/.claude/settings.json` allow-lists `mcp__<server>__*` to enable them.

DaVinci Resolve scripting goes through the typed Python wrapper at `resolving/davinci/` (no MCP).

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (`serving/diagrams/kit/src/types.ts`); `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS/Python imports — the JSON hub is the only seam.

- **Schema owner:** `@qagents/diagram-kit` v0.7.0 (`SubprojectId` widened to 24 — adds `developing`). 6-kind `PanelRef` union closed-set pinned in `data/specs/display-modes-2026-05-07/SPEC.md`.
- **Producers:** `<sub>/scripts/status_emit.{ts,py,mjs}`; atomic write (`.tmp` → `mv`/`os.replace`). Each producer pins a `KIT_VERSION` constant; sweep ALL pins in lockstep on kit `package.json` bumps (pins drift silently — T11). The close-time validator only checks `kitVersion` is a non-empty string — `designing/web/src/lib/status-loader.ts` carries the live `ACCEPTED_KIT_VERSIONS` set as the safety net during transitions.
- **Orchestrator:** `pnpm build:status` → `scripts/build-status-all.mjs` (producer failure non-fatal; placeholder fallback keeps build green). Bootstrap empty slots: `pnpm build:status:placeholders`.
- **Consumer:** `designing/web/src/lib/status-loader.ts` (Zod-validated; malformed JSON → placeholder). **Whole-slot failure mode:** a SINGLE contract-violating field drops the ENTIRE slot to placeholder on prod, not just that field — e.g. a `metrics` value that isn't `string | number` (boolean/`null` `leanGraph*` from `code/lean_graph`) or a node `shape` outside the kit enum. Producers coerce booleans to a string/number and OMIT a metric rather than emit `null`; never ask the consumer to loosen its schema.
- **Public surface — synthetic fixtures only:** every slot renders publicly at `quantapix.com/status/<sub>`, so a producer whose inputs can carry real matter MUST filter to synthetic/allow-listed fixtures (mirror `verifying/server/main.py ALLOWED_EXAMPLE_IDS`) — never real dockets/positions (`<live-matter>_*`). Fleet rule + owed close-time denylist scan: `data/specs/data-status-rename-2026-05-17/SPEC.md` § 11; memory `reference_operational_axis_public_surface_privacy`.
- **Close-time emit (`/close --status-emit`, mandatory):** every `/close <branch>` runs the subproject's producer + `scripts/validate-status-emit.mjs` before the session commit. No producer → the sub's `CLAUDE.md` must carry `<!-- status-emit: opt-out — reason: ... -->` or exit 43. Whole-repo branches fan out via `build-status-all.mjs`. Spec: `data/specs/data-status-rename-2026-05-17/SPEC.md` § 4.
- **Pending-aware producers + steady-state cron:** every `status_emit.*` writes under `QAGENTS_PENDING_ROOT || REPO` (node) / `_resolve_out()` (python) — `||` truthiness, never `??`, so a set-but-empty env falls back to canonical (else a cron fire scatters cwd-relative slots lock-free). A daily `qagents:status-emit-all:05:25` cron re-emits the whole fleet in pending mode (promoted by managing's 06:00 verifier), so `/status` slots don't decay between infrequent closes; close-time `--status-emit` stays the per-session refresh. New producers MUST be pending-aware from the start. Spec: `data/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`.
- **Adding a subproject:** sweep the **eight surfaces** (kit `SubprojectId` → loader `KNOWN_SUBS` → `copy.ts` → `build-status-all.mjs` → placeholder writer → e2e fixture → validator → `close.sh` case map), plus the hidden-surface rule and the `PRESENT_KIT_VERSION`/`ACCEPTED_KIT_VERSIONS` lockstep (`feedback_status_emit_kit_version_silent_drift`) — full enumeration + exemplar: `data/specs/data-status-rename-2026-05-17/SPEC.md` § 4.3.

Same data-hub-not-shared-code pattern: `data/donating/drive.json` (producer `donating/`; consumers `designing/web` + `documenting/web`).

## Kit-mount pattern

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`, get linked via `Layout.astro`'s `<slot name="head" />`, and are mounted per-run by `getStaticPaths` scanning `<sibling>/examples/*/{graph,report}.json`. Since the graphs G6 unification (2026-06-11), three live instances mount the ONE domain-neutral graphs kit (`visualizing/graphs/`, pkg `@qagents/graphs`) at `<app>/web/public/graphs2/` (the mount-dir keeps the legacy `graphs2` name):

1. `verifying/web/public/graphs2/` — proof-DAG pages + `/lattice`; `proving/`'s framework graphs (`verifying/CLAUDE.md` § 8).
2. `evaluating/web/public/graphs2/` — recomposed strategy mount, additionally composed with `@qagents/charts` + `@qagents/compose`; `accounting/`'s framework graphs (`evaluating/CLAUDE.md` § 2).
3. `monitoring/web/public/graphs2/` — operational `/operational` + `/constellation` mounts; `studying/`'s operational K-graph + constellation graph. Departures from 1–2 (gitignored fail-soft `kit.js`, request-time `/api` reads, never `getStaticPaths`): `monitoring/CLAUDE.md` § Operational-axis consumer.

All three regen-wholesale from `visualizing/graphs/dist/kit-{proof,strategy,graphs}.js` (NOT from `data/renders/<sub>-design/`); `loader.js` is the never-fold side-car. Schema + edge-kind detail: memory `project_proof_graph_kit_mount_pattern`.

## Lean4 axes — three kernels, one architecture

Three orthogonal axes, never sharing domain/ground-truth/consumer: **textual** `proving/` (`legal/uscode/`; plaintiff v. defendant; → `verifying/`), **numerical** `accounting/` (`financial/parquet/`; bulls v. bears; → `evaluating/`), **operational** `studying/` (git first; `hub/git`; coding v. testing; → `monitoring/`, local-only). Seven invariants (spec `data/specs/lean4-charter-2026-06-10/SPEC.md` § 4 — amendment history + the `Common/Tactic.lean`/plugin-knowledge distinction live there, not restated here) — headlines: (1) axiomatic kernel + LLM-generated `Facts.lean` + `lake build` as the gate; (2) **no human proof-driving, ever** (head-less `lake build` tactics are not manual); (3) proofs driven by top-tier LLMs in parallel via the debate framework (`/dau`/`/dat`/`/dao`); (4) three-way toolchain lockstep, one commit, example proofs replayed; (5) one consumer per axis, seam = files/SSE, refusal rules mirrored from axioms and never relaxed UI-side; (6) presentation via `visualizing/` + kit-mount only; (7) every driver hard-gates all seven coherency gates G1–G7 with exit codes each wave/round (spec `data/specs/lean4-charter-2026-06-10/cross-axis-coherency-2026-06-26/SPEC.md`; the axis-neutral COMMON mechanism + the cross-axis LEARNINGS ledger wired into every `/dau`/`/dat`/`/dao` + the dated G1–G7 conformance matrix live in the declared-child subspec `axiomatize-shared-2026-07-04/`). `studying/` owns the representation guide + `hub/` guide-rails.

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools. The allow-list refusal is one input to `evaluating/`'s **FINANCIALLY-CLEARED** gate (§ subproject list, `evaluating/`), which signs off any public surface that evaluates or implies a financial decision — a kernel refusal, never a safety guarantee.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` three-remote setup (`github` / `aws` / `qblk`) live in `serving/CLAUDE.md` § 8 + § 9 (deploy script, aws-vault + Keychain, bucket hardening, CodeCommit gotchas) — single owner; never duplicated here or in subproject CLAUDE.mds.

## Language split

- TypeScript for the VSCode extension and anything in `analyzing/src/`.
- Python for everything in `trading/`.
- A Python microservice is an allowed escape hatch from analyzing for heavy numerics (e.g. `analyzing/scripts/ta_reference.py` uses TA-Lib as ground truth).
- Never reach across: trading Python doesn't import analyzing, analyzing TS doesn't import trading.
