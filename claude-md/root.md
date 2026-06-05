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
- `visualizing/` — graphing surface for the `proving/` + `accounting/` Lean4 axiomatizations; an animated page in Qnarre (`verifying/web/`) + Qresev (`evaluating/web/`) via the kit-mount pattern (one kit consolidates the two mounted today). Renders the **lattice** (coverage × agreement × tier) over a domain-neutral `catalog.json` (`data/visualizing/<domain>-catalog.json`) + a secondary proof-DAG; cytoscape-vs-tf-graph bake-off, Blender bet retired (GPL). Spec: `data/specs/visualizing-2026-06-03.md`.
- `studying/` — Lean4 expert-track study + OSS contribution roadmap. Index: `studying/focus-areas.md`. Toolchain pinned to `proving/lean-toolchain` + `accounting/lean-toolchain`. Pure-mathlib paths out of scope.
- `explaining/` — video-explainer arc for Quantapix outreach. 50 scripts (5 topics × 10 subjects) narrated by an **AI presenter** over animated cards/text + D3.js / Cytoscape.js; 10–15 min each. Master plan: `explaining/outline.md`. Output is scripts; stage 5 (composition / Fusion / render) consumes `resolving/`.
- `resolving/` — DaVinci Resolve production-assistance. Skills + diagrams + Fusion authoring + typed Python wrapper at `resolving/davinci/`. Stage 5 of `explaining/`. Spec: `data/specs/resolving-2026-05-26.md`.
- `blending/` — Blender 5.1.1 + Geometry Nodes production-assistance. Escher-inspired background plates consumed by `explaining/` → `resolving/` Fusion comp. Same shape as `resolving/`: typed `bpy` wrapper at `blending/blendr/`. Motifs at `blending/motifs/`. Plan: `blending/PLAN.md`.
- `serving/` — AWS cloud-base; single source of truth for every AWS resource. CDK in TypeScript; ~$20–25/mo at v0.1. Hosts the `@qagents/diagram-kit` workspace package (sibling-of-subprojects, not member-of-serving). Spec: `data/specs/serving-2026-05-26.md`.
- `managing/` — daily watcher over the constellation. Cron-fired at 06:00 with Opus; three subagents (checker / planner / reporter) emit dated `.md` under `checks/`, `tasks/`, `reports/`. **Observe-only** — no push/commit/deploys/mutations.
- `shorting/` — adversarial sibling of `managing/`. On-demand `/open shorting`; one Opus subagent per target produces 10 numbered "shorting positions" under `shorting/positions/<target>/<date>.md`. **Observe-only**; routes findings to `managing/`.
- `donating/` — 6-month public donation drive (2026-06-01 → 2026-12-01). Source `donating/drive.md`; monthly ledger `donating/ledger/YYYY-MM.md`; renders `data/donating/drive.json` (consumed by `designing/web` + `documenting/web`). Four exclusive-use buckets (Claude Max 20× / Midpage MCP / AWS / SCOTUS). Content-only.
- `publishing/` — open-source release subproject. Owns the public-org staging tree `publishing/quantapix/` and the `/publish` pipeline (sweep → redact → compile → push to `github.com/quantapix/*`). Owns drive Promise 1. Content-in / external-out (GitHub org via `git push-quantapix`); not observe-only. Spec: `data/specs/publishing-2026-05-31.md`.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets + cross-cutting machinery (`data/status/<sub>.json` status-emit slots, `data/schedules/`, `data/specs/`, `data/renders/`, `data/donating/`, …). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule); load-bearing spec `data/specs/data-charter-2026-05-17.md`. Market/trading datasets promoted to the top-level `financial/` hub (below).
- `data/schedules/` — canonical macOS-launchd cron for **all** qagents subprojects. Single `ROUTINES` array in `data/schedules/launchd/install.sh`; `run_routine.sh <sub> <routine>` is the per-fire wrapper; logs at `launchd/logs/`. **Never** use cloud `/schedule` or `RemoteTrigger` — cowork sandbox can't mount the repo.
- `data/renders/` — wholesale-regenerated Claude Design handoff bundles (HTML/CSS/JS), one per subproject at `data/renders/<sub>-design/`. Read-only; replaced wholesale on regen. See `data/renders/MANIFEST.md`.
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `financial/parquet/` (OHLCV `ohlcv-equities/`, `ta-reference/`, `gics-symbols.parquet`), `financial/portfolios/` (PM + client forms + `schema.md`), `financial/reports/` (leaderboard), `financial/gics/` (`build.py` + `mapping.md`). Consumers: `trading/`, `analyzing/`, `accounting/`. Writers: trading PMs + manual (portfolios/reports), `financial/gics/build.py` + `analyzing/scripts/{ingest,ta_reference}.py` (parquet). Cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md`; shares the root `.data-write-lock` (below). Promoted out of `data/` per `data/specs/data-charter-2026-05-17.md` § 5 + `data/specs/financial-hub-migration-2026-05-29.md`.
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject. Today: `code/playwright/` (shared `@playwright/test` helpers), `code/remotion/` (`@qagents/remotion`; `explaining/` B-roll), `code/agent_sdk/` (`qagents.agent_sdk` — typed `claude-agent-sdk` wrapper; § Agent SDK lane), `code/qreel/` (marketplace plugin + `qreel` pkg — `/reel <bundle>` bakes one bundle to a captioned + loudness-normalized MP4 via Resolve; composes `resolving/`+`explaining/`+`blending/`; spec `data/specs/qreel-2026-05-28.md`). Subproject-owned workspace packages stay in their subproject.
- `lib/` — vendored upstream code; sibling of `code/`. Today: `lib/memsearch/` (vendored+patched; see § memsearch for the qagents patch detail); `lib/heygen-skills/` (vendored-pristine, MIT). Governance classes: vendored-pristine / vendored+patched / reference-only. See per-package `UPSTREAM.md`.

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only conventions that cross a boundary; subproject-specific rules live in each subproject's own `CLAUDE.md`.

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
3. **Sibling-of-subprojects pkgs are *runnable* only at canonical.** A worktree checks out `code/`/`lib/`/`serving/` tracked source but not their gitignored build state (`node_modules`/`.venv`/built deps) — so a script reaching sibling tooling via `$<SUB>_ROOT/../<sibling>/<pkg>` breaks. Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths (cf. `explaining/scripts/render-broll.sh` REMOTION_DIR).

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. VSCode extension hosts + Node code.
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's presets. Vendored `lib/` is upstream-owned.

### pnpm workspace + catalog

Single workspace at root: `pnpm-workspace.yaml` declares `analyzing`, `monitoring`, `designing/web`, `documenting/web`; shared dev tools via catalog (`"typescript": "catalog:"`). `onlyBuiltDependencies` at workspace level (`better-sqlite3`, `esbuild`). Root scripts: `pnpm {typecheck,build,verify}` → `pnpm -r --if-present <name>`.

### Playwright e2e (Astro sites)

Suites at `<sub>/web/tests/e2e/`; shared helpers at `code/playwright/`. Each `playwright.config.ts` runs three projects (chromium-desktop / -mobile / -reduced-motion); `webServer = pnpm build && pnpm preview` — never the dev server. Run: `pnpm -C <sub>/web test:e2e`. First-time: `test:e2e:install`.

### IDE: stable VSCode

Canonical IDE is stable VSCode. After switching variants, `monitoring/`'s `better-sqlite3` is V8/NAN-bound to its Electron — first F5 throws `NODE_MODULE_VERSION` mismatch; fix `cd monitoring && pnpm run rebuild:native`. `analyzing/` is unaffected (`@duckdb/node-api` is N-API, ABI-stable).

## Canonical OHLCV bar shape

Every place we produce/consume bar data — analyzing ingest Parquet, analyzing Alpaca feed (REST + WebSocket), `trading/shared/lib/alpaca_client.py bars` — uses the same column set:

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

GICS mapping is *shared data, not shared code*: parquet at `./financial/parquet/gics-symbols.parquet` keyed by `symbol` (columns `gics_{sector,industry_group,industry,sub_industry,code}` + `name`, `source`, `as_of`). Sector strings are the 11 canonical GICS long-form names. Producer + schema doc at `financial/gics/` (`build.py` + `mapping.md`); output path moved per `data/specs/data-charter-2026-05-17.md` § 5.

- Seed / refresh: `./.venv/bin/python financial/gics/build.py --default|--symbols|--symbols-file`. yfinance is the seed source.
- Analyzing reads via `analyzing/src/data/gics.ts` (registers DuckDB view `gics`).
- Trading reads via `python -m shared.lib.gics {lookup|sectors|concentration}`.
- Neither side writes to the parquet — updates go through `build.py`. Full schema and caveats in `financial/gics/mapping.md`.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`

Sessions start with `/open <project>` and end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints.

- **Spec:** `data/specs/open-close-dcu-2026-05-26.md` (consolidated triad; covers zero-prompt noop close, canonical-edit lock hook, per-hop cascade summaries, forward-only `data/next-steps/<sub>.md` + close-time gate + open briefing-read). Mechanics in `scripts/{open,close,dcu}.sh` + shared footer `scripts/lib/footer.sh`; skills at `.claude/skills/{open,close,do-claude-updates}/SKILL.md` are thin orchestrators. Logs at `pending/logs/`. **Bash discipline (load-bearing):** the close skill uses absolute paths only (`<root>/scripts/close.sh ...`) — never `./` or `scripts/...` — each path form needs a separate allow-list matcher.
- **Lock model:** branch-presence IS the write-lock. `<project>` (or stacked `<project>-N`) blocks parallel `/open`s of conflicting scope. `/open qagents` blocks all subproject opens.
- **Worktree path discipline (load-bearing):** inside any `/open <project>` session — `<sub>` **or** whole-repo `qagents` — every `Edit`/`Write` `file_path` MUST begin with the worktree root `<root>-wt/<branch>/`. A canonical `<root>/...` edit lands on `main`, not the session branch, silently bypassing the lock. Holds for every tracked dir — shared hubs (`data/`, `lib/`, `scripts/`, root `CLAUDE.md`) and `code/`+`lib/`+`serving/` alike (`git worktree add` checks them out in full); only gitignored build state (`node_modules`/`.venv`) is canonical-only (see § Shell scripts pt 3). `scripts/hooks/no-canonical-edit-while-locked.sh` enforces it (gates canonical Edit/Write while any worktree is held; allow-list = sentinels + `pending/`; bypass `QAGENTS_BYPASS_CANONICAL_LOCK=1`). Reads may use canonical. **Cron-lane carve-out:** applies ONLY to interactive `/open` sessions; autonomous `run_routine.sh` → `claude --print` fires have no session branch and run with cwd at the canonical subproject dir — they write canonical cwd-relative paths, never a `qagents-wt/<branch>/` root (a fabricated one orphans output, cf. the 2026-06-02 `trading-13` recovery). Spec: `data/specs/canonical-edit-hook-tightening-2026-05-28.md`. See `feedback_worktree_path_determines_working_tree`, `feedback_data_dir_present_in_worktrees`.
- **Canonical-shared gitignored content (`.worktree-links`):** large regenerable canonical-only ground truth (parquet, USC `corpus`/`xml`, explaining + Blender renders, CDN video mirror) is declared per owner in `<sub>/.worktree-links` (one glob/line) and symlinked into **every** worktree by `scripts/open.sh` (`git worktree add` doesn't materialise gitignored paths). Symlinks-into-canonical are teardown-safe (close.sh rescue skips them). Only **pure-gitignored** dirs (no tracked files) are symlinkable. Spec: `data/specs/open-close-dcu-2026-05-26.md` § 8.14.
- **Stack:** strict — `<project>-N` parents on `<project>-(N-1)`. Closes cascade up; `--to-main` walks the stack to `main`.
- **Sentinels:** `.dot-claude-write-lock` and `.data-write-lock` (root-anchored, gitignored), held only inside `/close` and `/do-claude-updates`.
- **CLAUDE.md updates:** *immediate* (project's own CLAUDE.md on session branch) + *deferred hints* (cross-subproject prose in `data/claude-updates/<branch>.md`; `/do-claude-updates` judges later).
- **Adopted-spec convention:** in-flight at `data/tmp/<slug>-<date>{/SPEC.md,.md}`; relocate to `data/specs/<slug>-<date>.md` once cited. Full lifecycle + tests-dir shape: `data/specs/CLAUDE.md` + `data/tmp/CLAUDE.md`.
- **Session summaries:** `/close` writes `data/summaries/<YYYY-MM-DD>T<HHMM>-<branch>.md` — versioned, never overwritten.
- **Per-project next-steps:** `data/next-steps/<project>.md` forward-only "what's left" surface (20 slots). Items deleted on resolution (no `Resolved` tail — that role belongs to close summaries). Commit cites `(closes|resolves|completes)? (next-steps item|ns-item) N` trigger the close-time `--next-steps` gate; exits 24 (slot missing) / 25 (cited items still present). `/open <project>` renders the slot's items as the footer's Outstanding rows.

## Programmatic Claude — Agent SDK lane

Cron-fired and library-callable Claude work goes through the typed Python wrapper at `code/agent_sdk/qagents/agent_sdk/` (imported as `qagents.agent_sdk`; verified against `claude-agent-sdk==0.2.82`). Shared by `trading/` and `managing/`. Routines opt into SDK-mode by suffixing the routine name with `:sdk` in `data/schedules/launchd/install.sh` ROUTINES; the default `claude --print` lane stays as-is otherwise. Adoption spec: `data/specs/agent-sdk-adoption-2026-05-17.md`. Billing rides the $200/mo Claude Max-20x SDK credit; ledger at `data/agent-sdk-ledger/`.

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) the shared `data/` **and** `financial/` hubs only while holding `<root>/.data-write-lock` (one lock serializes both).

- Cron-fired writes never touch `data/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync. The verifier is a **closed-set allow-list** classifier — a new `pending/` producer's path must be registered in lockstep in two places (`managing/.claude/agents/verifier.md` allow-list + `data/schedules/launchd/verify-pending.sh require_known_canonical_subtree`), else its files land in `unclassified[]`, never promoted. Internal-only output uses the verifier internal-set + `require_not_internal_pattern` deny-list. Spec: `data/specs/pending-promotion-scope-2026-05-28.md`.
- Manual writers (fixed-path producers — `financial/gics/build.py`, `<sub>/scripts/status_emit.*`) acquire the lock unconditionally with atomic create (`set -C` + redirect), write holder id, release with `rm` on EXIT trap.
- Configurable-output-path scripts (`--out-dir`/`--out`, e.g. `analyzing/scripts/{ingest.py,ta_reference.py}`) acquire the lock **iff** the absolute target falls under canonical `data/` **or** `financial/` (one root `.data-write-lock` serializes both). Worktree-local `data/`/`financial/` writes skip the lock — they don't race canonical writers.
- Producers branch on `QAGENTS_PENDING_ROOT`: set (cron) → write `pending/<rel>`, no lock; unset (manual) → acquire lock, write canonical.

Spec: `data/specs/data-conventions-2026-05-06.md`.

## Subproject `.claude/` shape (consistent pattern)

Every subproject that runs Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed permission allow/deny, plus a
  `PreToolUse(Bash)` hook wiring `scripts/hooks/no-cd-git.sh` (blocks
  `cd <dir> && git …`, which trips an un-silenceable foreign-hook security
  prompt); root `.claude/settings.json` carries the same hook. Allow-list
  entries need a trailing `*` on a fully-literal prefix (`Bash(scripts/*)`);
  a mid-glob before the colon (`Bash(scripts/*.sh:*)`) is inert and silently
  never matches. See memory `reference_claude_code_allow_glob_no_empty_match`.
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

- **Per-subproject scope (qagents patch).** Patched `common.sh` prefers `CLAUDE_PROJECT_DIR` over `git rev-parse --show-toplevel` — each subproject gets its own Milvus collection and `<sub>/.memsearch/memory/` daily-log tree. Preserve the `qagents patch` block across upstream re-syncs.
- **Backend.** ONNX `bge-m3` local. Milvus Lite is single-writer; switch `milvus.uri` in `~/.memsearch/config.toml` for concurrent sessions.
- **Markdown is source of truth.** `<sub>/.memsearch/memory/YYYY-MM-DD.md` is the durable record (Milvus re-indexes from it); the whole `**/.memsearch/memory/` tree is gitignored local state, never tracked.
- **Worktree logs survive `/close`.** Interactive `/open <sub>` sessions write logs in the worktree's gitignored tree, which `git worktree remove` would wipe; `/close` copies them back to canonical first (`scripts/lib/memsearch-copyback.sh`, append-merge by `## Session` block, no re-index). See `data/specs/memsearch-worktree-wipe-2026-05-28.md`.
- **Recall is fork-isolated** — `context: fork` keeps the curated digest out of the main context.

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

| Server | Type | Endpoint | Toolspace | Purpose |
|---|---|---|---|---|
| `heygen` | http | `https://mcp.heygen.com/mcp/v1/` (OAuth) | `mcp__heygen__*` | Avatar / voice / video against HeyGen Creator plan |

Vendored skills under `lib/heygen-skills/` (MIT); `heygen-{avatar,video}` symlinked from `.claude/skills/`. HeyGen OAuth requires Chrome (Safari ITP fails).

**Subproject-scoped, not repo-rooted.** `.mcp.json` lives at `<sub>/.mcp.json` — Claude Code walks up from launching cwd, so `/open <sub>` finds only its own MCP. Today only `explaining/.mcp.json` is wired; `<sub>/.claude/settings.json` allow-lists `mcp__<server>__*` to enable them.

DaVinci Resolve scripting goes through the typed Python wrapper at `resolving/davinci/` (no MCP).

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (`serving/diagrams/kit/src/types.ts`); `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS/Python imports — the JSON hub is the only seam.

- **Schema owner:** `@qagents/diagram-kit` v0.4.3 (`SubprojectId` widened to 21; emit shape unchanged from v0.4.0). 6-kind `PanelRef` union closed-set pinned in `data/specs/display-modes-2026-05-07.md`.
- **Producers:** `<sub>/scripts/status_emit.{ts,py,mjs}`; atomic write (`.tmp` → `mv`/`os.replace`). Each producer pins a `KIT_VERSION` constant; sweep in lockstep on kit `package.json` bumps. The close-time validator only checks `kitVersion` is a non-empty string, so drift is silent — `designing/web/src/lib/status-loader.ts` carries the live `ACCEPTED_KIT_VERSIONS` set as the safety net during transitions.
- **Orchestrator:** `pnpm build:status` → `scripts/build-status-all.mjs` (producer failure non-fatal; placeholder fallback keeps build green). Bootstrap empty slots: `pnpm build:status:placeholders`.
- **Consumer:** `designing/web/src/lib/status-loader.ts` (Zod-validated; malformed JSON → placeholder).
- **Close-time emit (`/close --status-emit`, mandatory):** every `/close <branch>` runs `scripts/close.sh --status-emit <branch>` before the session commit — resolves the producer per subproject, runs it, validates via `scripts/validate-status-emit.mjs` (vanilla-JS field validator, no zod dep). Subprojects without a producer must carry `<!-- status-emit: opt-out — reason: ... -->` in their `CLAUDE.md` or exit 43. Whole-repo `qagents`/`qagents-N` fans out via `build-status-all.mjs`. Spec: `data/specs/data-status-rename-2026-05-17.md` § 4.
- **Adding a subproject:** sweep eight surfaces in one PR — `SubprojectId` in the kit, `KNOWN_SUBS` in the loader, `STATUS_CARDS` + `STATUS_GROUPS` + `OG_META` in `designing/web/src/content/copy.ts`, `PRODUCERS` in `scripts/build-status-all.mjs`, `SUBS` in `scripts/write-status-placeholders.mjs`, the e2e fixture `KNOWN_SUBS` + `GROUPS` in `designing/web/tests/e2e/status.spec.ts`, `KNOWN_SUBS` in `scripts/validate-status-emit.mjs` (the close `--status-emit` validator → exit 44 if absent), and the `status_emit_producer()` case map in `scripts/close.sh` (resolves the producer → exit 43 if no arm, even when `build-status-all.mjs` PRODUCERS has the entry). A brand-new subproject with no mounted surface stays **hidden** from `/status` — add it to `KNOWN_SUBS`/`STATUS_CARDS`/`OG_META` but NOT `STATUS_GROUPS` or the e2e visible set (resolving/blending/monitoring/appealing/pleading precedent). Bump kit minor version on the additive widening (see `project_diagram_kit` memory) — and in the same PR move **both** `PRESENT_KIT_VERSION` and `ACCEPTED_KIT_VERSIONS` in `designing/web/src/lib/status-loader.ts` to the new version, else the new-version emit drifts silently to a placeholder card (see `feedback_status_emit_kit_version_silent_drift`).

Second instance of the data-hub-not-shared-code pattern: `data/donating/drive.json` (producer `donating/`; consumers `designing/web` + `documenting/web`).

## Kit-mount pattern (bi-instantiated 2026-05-15)

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`, get linked via `Layout.astro`'s `<slot name="head" />`, and are mounted per-run by `getStaticPaths` scanning `<sibling>/examples/*/{graph,report}.json`. Two instances:

1. `verifying/web/public/proof-graph/` — `proving/`'s RICO / Title VI / CivilRights graphs (`verifying/CLAUDE.md` § 8).
2. `evaluating/web/public/strategy-chart/` — `accounting/`'s TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN graphs (`evaluating/CLAUDE.md` § 4).

Both regen-wholesale from `data/renders/<sub>-design/`; `loader.js` is the never-fold side-car. Schema + edge-kind detail: memory `project_proof_graph_kit_mount_pattern`.

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` three-remote setup (`github` / `aws` / `qblk`) live in `serving/CLAUDE.md` § 8 + § 9 (deploy script, aws-vault + Keychain, bucket hardening, CodeCommit gotchas). Don't duplicate AWS config here or in subproject CLAUDE.mds.

## Language split

- TypeScript for the VSCode extension and anything in `analyzing/src/`.
- Python for everything in `trading/`.
- A Python microservice is an allowed escape hatch from analyzing for heavy numerics (e.g. `analyzing/scripts/ta_reference.py` uses TA-Lib as ground truth).
- Never reach across: trading Python doesn't import analyzing, analyzing TS doesn't import trading.
