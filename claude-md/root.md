# qagents — Cross-project conventions

Subprojects under this repo:

- `analyzing/` — VSCode extension (TypeScript) for market inspection: DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed.
- `trading/` — Python portfolio-management agents: three PMs (aggressive/moderate/conservative) on Alpaca paper, orchestrated by Claude Code routines.
- `appealing/` — pro se federal appellate drafting. Markdown drafts; rendered PDFs flow to a private filing hub. CLAUDE.md content not mirrored — see `qagents-public/README.md` § "Litigation-domain CLAUDE.md\`s ... deliberately excluded".
- `pleading/` — pro se trial-court + status-affidavit + addendum drafting. Sibling of `appealing/`. Markdown drafts; rendered PDFs flow to the private filing hub. CLAUDE.md content not mirrored.
- `designing/` — Astro + React islands site for quantapix.com (S3 + CloudFront). Hosts `/status` aggregating per-subproject `data/status/<sub>.json`.
- `documenting/` — sibling of `designing/`; femfas.net v2 (Astro/S3/CloudFront).
- `monitoring/` — VSCode extension sibling of `analyzing/`; LW-Charts + Three.js surface; shared SQLite schema with a Python CLI fallback.
- `proving/` — Lean4 axiomatic theorem-proving with LLM-backed predicate functions for the **legal** domain (civil RICO, Title VI, §§ 1981/1983/1985(3)). Backs `verifying/`.
- `accounting/` — financial-domain parallel of `proving/`: Lean4 + LLM-predicates for TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN frameworks. Reads OHLCV from `./data/<name>/` parquet. Backs `evaluating/`.
- `verifying/` — Astro+React shell + FastAPI server for **Qnarre**, the legal-complaint verifier UI. Three-zone `/app` island streams events from `proving/` via SSE.
- `evaluating/` — sibling of `verifying/` for **Qresev**, the stock/portfolio evaluator UI. Streams events from `accounting/` via SSE; UI hard-refuses any options leg outside the six-strategy defined-risk allow-list.
- `studying/` — Lean4 expert-track study + OSS contribution roadmap. Index: `studying/focus-areas.md`. Toolchain pinned to `proving/lean-toolchain` + `accounting/lean-toolchain`. Pure-mathlib paths out of scope.
- `explaining/` — video-explainer arc for Quantapix outreach. 50 scripts (5 topics × 10 subjects) narrated by an **AI presenter** over animated cards/text + D3.js / Cytoscape.js graphics; 10–15 min per video. Master plan: `explaining/outline.md`. Output is scripts; stage 5 (composition / Fusion / render) consumes `resolving/`.
- `resolving/` — DaVinci Resolve production-assistance. Skills + diagrams + Fusion authoring + typed Python wrapper at `resolving/davinci/`. Stage 5 of `explaining/`. Plan: `resolving/PLAN.md`.
- `blending/` — Blender 5.1.1 + Geometry Nodes production-assistance. Escher-inspired background plates consumed by `explaining/` → `resolving/` Fusion comp. Same shape as `resolving/`: typed Python wrapper at `blending/blendr/` (`bpy` via headless `--background --python`; JSON-spec / files-out boundary). Motifs at `blending/motifs/`. Plan: `blending/PLAN.md`.
- `serving/` — AWS cloud-base. Single source of truth for every AWS resource. CDK in TypeScript; ~$20–25/mo run-rate at v0.1. Plan + locked decisions at `serving/PLAN.md`. Hosts the `@qagents/diagram-kit` workspace package (sibling-of-subprojects, not member-of-serving).
- `managing/` — daily watcher over the constellation. Cron-fired at 06:00 with Opus; three subagents (checker / planner / reporter) emit dated `.md` under `checks/`, `tasks/`, `reports/`. **Observe-only** — no git push/commit/deploys/mutations.
- `shorting/` — adversarial sibling of `managing/`. On-demand `/open shorting`; one Opus subagent per target produces 10 numbered "shorting positions" under `shorting/positions/<target>/<date>.md`. **Observe-only**; findings route to `managing/`.
- `donating/` — 6-month public donation drive (2026-06-01 → 2026-12-01). Source `donating/drive.md`; monthly ledger at `donating/ledger/YYYY-MM.md`; render to `data/donating/drive.json` consumed by `designing/web` + `documenting/web`. Four exclusive-use buckets (AI-assistant subscription / legal-research MCP / AWS / federal docketing). Content-only.
- `publishing/` — open-source release subproject. Owns the public-org staging tree `publishing/quantapix/` and the `/publish` pipeline (sweep → redact → compile → push to the public GitHub org). Owns the drive's open-sourcing promise; no other subproject carries open-sourcing duty. Content-in / external-out (the public org); not observe-only.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets (`financial/parquet/`, `financial/portfolios/`, `financial/reports/`, `data/status/<sub>.json` status-emit slots). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule); load-bearing spec at `data/specs/data-charter-2026-05-17.md`.
- `data/schedules/` — canonical macOS-launchd cron for **all** qagents subprojects. Single `ROUTINES` array in `data/schedules/launchd/install.sh`; `run_routine.sh <sub> <routine>` is the per-fire wrapper; logs at `launchd/logs/`. **Never** use cloud `/schedule` or `RemoteTrigger` — cowork sandbox can't mount the repo.
- `data/renders/` — wholesale-regenerated Claude Design handoff bundles (HTML/CSS/JS), one per subproject at `data/renders/<sub>-design/`. Read-only; replaced wholesale on regen. See `data/renders/MANIFEST.md`.
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject. Today: `code/playwright/` (shared `@playwright/test` helpers), `code/remotion/` (`@qagents/remotion` workspace package for `explaining/`'s B-roll pipeline), `code/agent_sdk/` (Python `qagents.agent_sdk` namespace package — typed wrapper around `claude-agent-sdk`, used by `trading/` and `managing/`). Subproject-owned workspace packages stay in their subproject.
- `lib/` — vendored upstream code; sibling of `code/`. Today: `lib/memsearch/` *(vendored+patched, qagents patch in `plugins/claude-code/hooks/common.sh` prefers `CLAUDE_PROJECT_DIR` for per-subproject Milvus)*; `lib/heygen-skills/` *(vendored-pristine, MIT)*. Governance classes: vendored-pristine / vendored+patched / reference-only. See per-package `UPSTREAM.md`.

Subprojects share a domain only when stated (trading+analyzing share equities + defined-risk options; appealing + pleading + legal share dockets and rules). This file pins only conventions that cross a boundary; subproject-specific rules live in each subproject's own `CLAUDE.md`.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13). All cross-subproject deps in root `pyproject.toml` under extras `[trading]`, `[analyzing]`, `[dev]`, `[verifying]`, `[evaluating]`. Bootstrap from a fresh checkout:

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
./.venv/bin/pip install -e '.[trading,analyzing,dev]'
./.venv/bin/pip install -e ./trading --no-deps         # registers `shared` / `shared.lib`
./.venv/bin/pip install -e ./code/agent_sdk --no-deps  # registers `qagents.agent_sdk`
```

From repo root → `./.venv/bin/python …`. From a subproject → `../.venv/bin/python …`. `monitoring/` is stdlib-only; `proving/` and `accounting/` use system `python3` — none of them need the venv.

## Shell scripts — homebrew tool versions

Any shell script (cron-fired, operator-fired, or session-invoked) MUST resolve to homebrew-installed tools, not macOS system defaults. macOS ships bash 3.2.57 (no `mapfile`/`readarray`/`declare -A`/`${var^^}`), no GNU coreutils, BSD `sed`/`awk`/`date`.

1. **Cron lane PATH** — `data/schedules/launchd/install.sh` plist template lists `/opt/homebrew/bin` first; `--enable` regenerates every plist.
2. **Portable scripts as belt-and-suspenders** — outside the cron lane, avoid `mapfile` (use `while IFS= read -r line; do …; done < <(cmd)`), prefer POSIX flags. For homebrew-only features (e.g. `date -d '3 days ago'`), invoke by absolute path (`/opt/homebrew/bin/gdate`).
3. **Sibling-of-subprojects pkgs are canonical-only.** `code/`, `lib/`, and `serving/` live at canonical and are absent from worktrees. A per-subproject script that reaches a sibling via `$<SUB>_ROOT/../<sibling>/<pkg>` breaks in worktrees (resolves to `qagents-wt/<sub>/<sibling>/<pkg>`, which doesn't exist). Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths so writes still bind to whichever tree invoked the script. Surfaced via `explaining/scripts/render-broll.sh` (REMOTION_DIR).

Audit (tool versions): `grep -rn -E '(mapfile|readarray|declare -A|gdate|gsed|gawk|find -newermt)' --include='*.sh'`.
Audit (sibling paths): `grep -rn -E '\$[A-Z_]+_ROOT/\.\./(code|lib|serving)/' --include='*.sh'`.

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. VSCode extension hosts + Node code.
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's own presets. Vendored `lib/` is upstream-owned. **No git submodules** — vendoring + pins replaced them on 2026-04-30.

### pnpm workspace + catalog

Single workspace at root: `pnpm-workspace.yaml` declares `analyzing`, `monitoring`, `designing/web`, `documenting/web`; shared dev tools via catalog (`"typescript": "catalog:"`). `onlyBuiltDependencies` at workspace level (`better-sqlite3`, `esbuild`). Root scripts: `pnpm {typecheck,build,verify}` → `pnpm -r --if-present <name>`.

### Playwright e2e (Astro sites)

Suites at `<sub>/web/tests/e2e/`; shared helpers at `code/playwright/`. Each `playwright.config.ts` runs three projects (chromium-desktop / -mobile / -reduced-motion); `webServer = pnpm build && pnpm preview` — never the dev server. Run: `pnpm -C <sub>/web test:e2e`. First-time: `test:e2e:install`.

### IDE: stable VSCode

Canonical IDE is stable VSCode. After switching variants, `monitoring/`'s `better-sqlite3` is V8/NAN-bound to its Electron — first F5 throws `NODE_MODULE_VERSION` mismatch; fix is `cd monitoring && pnpm run rebuild:native`. `analyzing/` is unaffected (`@duckdb/node-api` is N-API, ABI-stable).

## Canonical OHLCV bar shape

Every place we produce or consume bar data — analyzing ingest Parquet, analyzing Alpaca feed (REST + WebSocket), `trading/shared/lib/alpaca_client.py bars` — uses the same column set:

| field   | type                 | notes                              |
|---------|----------------------|------------------------------------|
| `ts`    | ISO-8601 UTC string (or `timestamp(us, UTC)` in Parquet) | UTC, microsecond precision in storage |
| `o`     | float64              | open                               |
| `h`     | float64              | high                               |
| `l`     | float64              | low                                |
| `c`     | float64              | close (unadjusted)                 |
| `v`     | int64                | volume                             |
| `adj_c` | float64              | split/div-adjusted close; equals `c` when source returns raw bars |

No `t` instead of `ts`, no missing `adj_c`, no renames. Adapters translate at the boundary — never leak vendor field names past the client module.

## GICS sector / industry classification

Both projects use the GICS hierarchy. Mapping is *shared data, not shared code*: parquet at `./financial/parquet/gics-symbols.parquet` keyed by `symbol`, columns `gics_sector`, `gics_industry_group`, `gics_industry`, `gics_sub_industry`, `gics_code` (plus `name`, `source`, `as_of`). Sector strings are the 11 canonical GICS long-form names. Producer + schema doc stay at `financial/gics/` (`build.py` + `mapping.md`); output path moved per `data/specs/data-charter-2026-05-17.md` § 5.

- Seed / refresh: `./.venv/bin/python financial/gics/build.py --default|--symbols|--symbols-file`. yfinance is the seed source.
- Analyzing reads via `analyzing/src/data/gics.ts` (registers DuckDB view `gics`).
- Trading reads via `python -m shared.lib.gics {lookup|sectors|concentration}`.
- Neither side writes to the parquet — updates go through `build.py`. Full schema and caveats in `financial/gics/mapping.md`.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`

Sessions start with `/open <project>` and end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints.

- **Spec:** `data/specs/open-close-dcu-2026-05-26.md` (consolidated triad — supersedes five retired predecessor specs; covers zero-prompt noop close, the canonical-edit lock hook, per-hop cascade summaries, and forward-only per-project `data/next-steps/<sub>.md` + a close-time gate + open briefing-read). Mechanics in `scripts/{open,close,dcu}.sh` + shared footer at `scripts/lib/footer.sh`; skills at `.claude/skills/{open,close,do-claude-updates}/SKILL.md` are thin orchestrators. Logs at `pending/logs/`.
- **Lock model:** branch-presence IS the write-lock. `<project>` (or stacked `<project>-N`) blocks parallel `/open`s of conflicting scope. `/open qagents` blocks all subproject opens.
- **Worktree path discipline:** inside any `/open <project>` session every Edit/Write `file_path` MUST begin with the worktree root — editing a canonical path lands the change on `main`, silently bypassing the lock. A PreToolUse hook enforces this.
- **Stack:** strict — `<project>-N` parents on `<project>-(N-1)`. Closes cascade up; `--to-main` walks the stack to `main`.
- **Sentinels:** `.dot-claude-write-lock` and `.data-write-lock` (root-anchored, gitignored), held only inside `/close` and `/do-claude-updates`.
- **CLAUDE.md updates:** *immediate* (project's own CLAUDE.md on session branch) + *deferred hints* (cross-subproject prose in `data/claude-updates/<branch>.md`; `/do-claude-updates` judges later).
- **Adopted-spec convention:** in-flight at `data/tmp/<slug>-<date>{/SPEC.md,.md}`; once cited by skills/docs, relocate to `data/specs/<slug>-<date>.md`. Spec file + tests dir shape pinned in `data/specs/CLAUDE.md`; proposal lifecycle in `data/tmp/CLAUDE.md`.
- **Session summaries:** `/close` writes `data/summaries/<YYYY-MM-DD>T<HHMM>-<branch>.md` — versioned, never overwritten.
- **Per-project next-steps:** `data/next-steps/<project>.md` is a forward-only "what's left" surface; items are deleted on resolution; a close-time gate fires on commits that cite a next-steps item.

The `open` / `close` / `do-claude-updates` / `do-claude-optimizations` skill
bodies + their adopted specs are published in this repo's `skills/` subtree.

## Programmatic Claude — Agent SDK lane

Cron-fired and library-callable Claude work goes through the typed Python wrapper at `code/agent_sdk/qagents/agent_sdk/` (imported as `qagents.agent_sdk`; verified against `claude-agent-sdk==0.2.82`; public API at `__init__.py`). Shared by `trading/` and `managing/`. Routines opt into SDK-mode by suffixing the routine name with `:sdk` in `data/schedules/launchd/install.sh` ROUTINES; the default `claude --print` lane stays as-is until a routine is migrated. Adoption spec: `data/specs/agent-sdk-adoption-2026-05-17.md`. Billing rides the $200/mo Claude Max-20x SDK credit; ledger at `data/agent-sdk-ledger/`.

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) `data/` only while holding `<root>/.data-write-lock`.

- Cron-fired writes never touch `data/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync.
- Manual writers (fixed-path producers — `financial/gics/build.py`, `<sub>/scripts/status_emit.*`) acquire the lock unconditionally with atomic create (`set -C` + redirect), write holder identifier, release with `rm` on EXIT trap.
- Configurable-output-path scripts (`--out-dir`/`--out`, e.g. `analyzing/scripts/{ingest.py,ta_reference.py}`) resolve the target to an absolute path and acquire the lock **iff** it falls under `<canonical_repo_root>/data/`. Worktree-local `data/` writes skip the lock — they don't race canonical writers. The canonical-root walker handles both worktree (`.git` file → parse `gitdir:` → walk up three parents) and canonical (`.git` dir → parent).
- Producers branch on `QAGENTS_PENDING_ROOT`: set (cron lane) → write to `pending/<rel>`, no lock; unset (manual) → acquire lock, write canonical.

Spec: `data/specs/data-conventions-2026-05-06.md`.

## Subproject `.claude/` shape (consistent pattern)

Every subproject that runs Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed permission allow/deny, plus a
  `PreToolUse(Bash)` hook wiring `scripts/hooks/no-cd-git.sh` (blocks
  `cd <dir> && git …`, which trips an un-silenceable foreign-hook security
  prompt). Root `.claude/settings.json` carries the same hook.
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

Vendored at `lib/memsearch/` as a Claude Code plugin. Install: `/plugin marketplace add <root>/lib/memsearch`, `/plugin install memsearch`, `/reload-plugins`. Recall skill is namespaced: `memsearch:memory-recall`.

- **Per-subproject scope (qagents patch).** Patched `common.sh` prefers `CLAUDE_PROJECT_DIR` over `git rev-parse --show-toplevel` — each subproject gets its own Milvus collection and `<sub>/.memsearch/memory/` daily-log tree. Search `qagents patch` to find the block; preserve across upstream re-syncs.
- **Backend.** ONNX `bge-m3` local. Milvus Lite is single-writer; switch `milvus.uri` in `~/.memsearch/config.toml` for concurrent sessions.
- **Markdown is source of truth.** `<sub>/.memsearch/memory/YYYY-MM-DD.md` is the durable record (the vector index re-indexes from it); the whole `**/.memsearch/memory/` tree is gitignored local state. Interactive sessions write logs in the worktree's gitignored tree, which `git worktree remove` would wipe; `/close` copies them back to canonical first.
- **Recall is fork-isolated** — `context: fork` keeps the curated digest out of the main context.

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

| Server | Type | Endpoint | Toolspace | Purpose |
|---|---|---|---|---|
| `heygen` | http | `https://mcp.heygen.com/mcp/v1/` (OAuth) | `mcp__heygen__*` | Avatar / voice / video against HeyGen Creator plan |

Vendored skills under `lib/heygen-skills/` (MIT); `heygen-{avatar,video}` symlinked from `.claude/skills/`. HeyGen OAuth requires Chrome (Safari ITP fails).

**Subproject-scoped, not repo-rooted.** `.mcp.json` lives at `<sub>/.mcp.json` — Claude Code walks up from launching cwd, so `/open <sub>` finds only its own MCP. Today only `explaining/.mcp.json` is wired. `<sub>/.claude/settings.json` allow-lists `mcp__<server>__*` so tools are usable.

DaVinci Resolve scripting goes through the typed Python wrapper at `resolving/davinci/` (no MCP).

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (`serving/diagrams/kit/src/types.ts`). `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS or Python imports — the JSON hub is the only seam.

- **Schema owner:** `@qagents/diagram-kit` v0.4.2 (additively widens `SubprojectId` to cover every subproject incl. `publishing`; emit shape unchanged from v0.4.0). 6-kind `PanelRef` union closed-set pinned in `data/specs/display-modes-2026-05-07.md`.
- **Producers:** `<sub>/scripts/status_emit.{ts,py,mjs}`; atomic write (`.tmp` → `mv`/`os.replace`). Each producer pins a `KIT_VERSION` constant; sweep in lockstep on kit `package.json` bumps. The close-time validator only checks `kitVersion` is a non-empty string, so drift is silent — `designing/web/src/lib/status-loader.ts` carries the live `ACCEPTED_KIT_VERSIONS` set as the safety net during transitions.
- **Orchestrator:** `pnpm build:status` → `scripts/build-status-all.mjs` (producer failure non-fatal; placeholder fallback keeps build green).
- **Bootstrap empty slots:** `pnpm build:status:placeholders`.
- **Consumer:** `designing/web/src/lib/status-loader.ts` (Zod-validated; malformed JSON → placeholder).
- **Close-time emit (`/close --status-emit`, mandatory):** every `/close <branch>` runs `scripts/close.sh --status-emit <branch>` before the session commit, which resolves the producer per subproject, runs it, and validates via `scripts/validate-status-emit.mjs` (vanilla-JS field validator, no zod dep — runs from root). Subprojects without a producer must carry `<!-- status-emit: opt-out — reason: ... -->` in their `CLAUDE.md` or exit 43. Whole-repo `qagents`/`qagents-N` fans out via `build-status-all.mjs`. Spec: `data/specs/data-status-rename-2026-05-17.md` § 4.
- **Adding a subproject:** extend `SubprojectId` in the kit, `KNOWN_SUBS` in the loader, `STATUS_CARDS` + `STATUS_GROUPS` + `OG_META` in `designing/web/src/content/copy.ts`, `PRODUCERS` in `scripts/build-status-all.mjs`, `SUBS` in `scripts/write-status-placeholders.mjs`, plus the e2e fixture `KNOWN_SUBS` + `GROUPS` in `designing/web/tests/e2e/status.spec.ts` (no type-level coupling — sweep in the same PR). All 6 surfaces in lockstep — bump kit minor version on the additive widening.

Canonical example of the data-hub-not-shared-code pattern. Second instance: `data/donating/drive.json` (one producer in `donating/`, two consumers in `designing/web` + `documenting/web`).

## Kit-mount pattern (bi-instantiated 2026-05-15)

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/` (kit.js + loader.js side-car + kit.css + tokens-*.css), get linked via `Layout.astro`'s `<slot name="head" />`, and are mounted per-run by `getStaticPaths` scanning `<sibling>/examples/*/{graph,report}.json`. Two instances today:

1. `verifying/web/public/proof-graph/` — `proving/`'s RICO / Title VI / CivilRights graphs (`verifying/CLAUDE.md` § 8).
2. `evaluating/web/public/strategy-chart/` — `accounting/`'s TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN graphs (`evaluating/CLAUDE.md` § 4).

Both consume `<sibling>/examples/<id>/graph.json` with the same kit-side schema (`kind: predicate | axiom | theorem`; edge kinds `applies` / `composes` / `inhabits`; `failures[]` for debug overlay). Both regen-wholesale from `data/renders/<sub>-design/` and copy into `<sub>/web/public/<kit>/` at re-sync time; `loader.js` is the never-fold side-car. Memory: `project_proof_graph_kit_mount_pattern`.

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools too.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` three-remote setup (`github` / `aws` / `qblk`) live in `serving/CLAUDE.md` § 8 + § 9 (deploy script, aws-vault + Keychain workflow, bucket hardening, CodeCommit gotchas). Do not duplicate AWS config here or in subproject CLAUDE.mds.

## Language split

- TypeScript for the VSCode extension and anything in `analyzing/src/`.
- Python for everything in `trading/`.
- A Python microservice is allowed as an escape hatch from analyzing for heavy numerics (e.g. `analyzing/scripts/ta_reference.py` uses Python TA-Lib as ground truth).
- Never reach across: trading Python does not import from analyzing, and analyzing TS does not import from trading.
