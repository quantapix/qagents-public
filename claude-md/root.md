# qagents — Cross-project conventions

Subprojects under this repo:

- `analyzing/` — VSCode extension (TypeScript) for market inspection: DuckDB + Parquet, lightweight-charts v5, yfinance/Stooq ingest, Alpaca IEX live feed.
- `trading/` — Python portfolio-management agents: three PMs (aggressive/moderate/conservative) on Alpaca paper, orchestrated by Claude Code routines.
- `appealing/` — pro se federal appellate drafting. Markdown drafts; rendered PDFs flow to a private filing hub. CLAUDE.md content not mirrored — see `qagents-public/README.md` § "Litigation-domain CLAUDE.md\`s ... deliberately excluded".
- `pleading/` — pro se trial-court + status-affidavit + addendum drafting. Sibling of `appealing/`. Markdown drafts; rendered PDFs flow to the private filing hub. CLAUDE.md content not mirrored.
- `designing/` — Astro + React islands site for quantapix.com (S3 + CloudFront). Hosts `/status` aggregating per-subproject `data/status/<sub>.json`.
- `documenting/` — sibling of `designing/`; femfas.net v2 (Astro/S3/CloudFront).
- `monitoring/` — local-only **Astro Node-SSR web app** for Claude Code token analytics (was a VSCode extension, retired 2026-06-17); SQLite store via `better-sqlite3`, sibling of `analyzing/`'s DuckDB inspection tooling. Chartered consumer app of the **operational** Lean4 axis; never deployed.
- `proving/` — Lean4 axiomatic theorem-proving with LLM-backed predicate functions for the **legal** domain (civil RICO, Title VI, §§ 1981/1983/1985(3)). Backs `verifying/`.
- `accounting/` — financial-domain parallel of `proving/`: Lean4 + LLM-predicates for TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN frameworks. Reads OHLCV from `./data/<name>/` parquet. Backs `evaluating/`.
- `verifying/` — Astro+React shell + FastAPI server for **Qnarre**, the legal-complaint verifier UI. Three-zone `/app` island streams events from `proving/` via SSE.
- `evaluating/` — sibling of `verifying/` for **Qresev**, the stock/portfolio evaluator UI. Streams events from `accounting/` via SSE; UI hard-refuses any options leg outside the defined-risk allow-list (§ Defined-risk options). Owns the constellation **financial sign-off** — the FINANCIALLY-CLEARED gate (financial-domain analog of `pleading/`'s litigation-safety gate; sole grantor, `accounting/` advises). Spec: `data/specs/evaluating-financial-signoff-2026-06-24/SPEC.md`.
- `visualizing/` — graphing surface for the `proving/` + `accounting/` Lean4 axiomatizations; an animated page in Qnarre + Qresev via the kit-mount pattern; renders the **lattice** + a secondary proof-DAG. Spec: `data/specs/visualizing-2026-06-03/SPEC.md`.
- `studying/` — **operational-axis** Lean4 kernel (third of the three axes — § Lean4 axes) + owner of the cross-axis representation research and the `hub/` guide-rails (`studying/guide-rails.md`). First target: git axiomatization (consumer `monitoring/`). Index: `studying/focus-areas.md`. Spec: `data/specs/lean4-charter-2026-06-10/SPEC.md`.
- `explaining/` — video-explainer arc for Quantapix outreach. 50 scripts (5 topics × 10 subjects) narrated by an **AI presenter**; 10–15 min each. Master plan: `explaining/outline.md`. Output is scripts; stage 5 (composition / render) consumes `resolving/`.
- `resolving/` — DaVinci Resolve production-assistance. Skills + diagrams + Fusion authoring + typed Python wrapper at `resolving/davinci/`. Stage 5 of `explaining/`. Spec: `data/specs/resolving-2026-05-26/SPEC.md`.
- `blending/` — Blender 5.1 + Geometry Nodes production-assistance; Escher-inspired background plates for `explaining/` → `resolving/`. Typed `bpy` wrapper at `blending/blendr/`; motifs at `blending/motifs/`. Plan: `blending/PLAN.md`.
- `serving/` — AWS cloud-base; single source of truth for every AWS resource. CDK in TypeScript. Hosts the `@qagents/diagram-kit` workspace package (sibling-of-subprojects, not member-of-serving). Spec: `data/specs/serving-2026-05-26/SPEC.md`.
- `managing/` — daily watcher over the constellation. Cron-fired at 06:00 with the top-tier model; three subagents (checker / planner / reporter) emit dated `.md` under `checks/`, `tasks/`, `reports/`. **Observe-only** — no push/commit/deploys/mutations.
- `shorting/` — adversarial sibling of `managing/`. On-demand `/open shorting`; one top-tier-model subagent per target produces 10 numbered "shorting positions" under `shorting/positions/<target>/<date>.md`. **Observe-only**; routes findings to `managing/`.
- `donating/` — 6-month public donation drive (2026-06-01 → 2026-12-01). Source `donating/drive.md`; renders `data/donating/drive.json` (consumed by `designing/web` + `documenting/web`). Four exclusive-use buckets. Content-only.
- `publishing/` — open-source release subproject. Owns the public-org staging tree `publishing/quantapix/` and the `/publish` pipeline (sweep → redact → compile → push to `github.com/quantapix/*`). Owns drive Promise 1. Content-in / external-out (GitHub org via `git push-quantapix`); not observe-only. Spec: `data/specs/publishing-2026-05-31/SPEC.md`.
- `rendering/` — in-house render engine + brand source of truth; single owner of **brand-bearing, pre-rasterized** artifacts (images + videos) for the whole constellation. Image engine live (`rendering/engines/image/capture.mjs`); video engine post-first-cohort. Inputs at `rendering/designs/<consumer>/` + `rendering/brand/`; deliverables in `data/renders/<consumer>/`. Spec: `data/specs/rendering-2026-06-09/SPEC.md`.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets + cross-cutting machinery (`data/status/<sub>.json` status-emit slots, `data/schedules/`, `data/specs/`, `data/renders/`, `data/donating/`, …). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule); load-bearing spec `data/specs/data-charter-2026-05-17/SPEC.md`. Market/trading datasets promoted to the top-level `financial/` hub (below).
- `data/schedules/` — canonical macOS-launchd cron for **all** subprojects. Single `ROUTINES` array in `data/schedules/launchd/install.sh`; `run_routine.sh` is the per-fire wrapper. **Never** use cloud `/schedule` or `RemoteTrigger` — cowork sandbox can't mount the repo.
- `data/renders/` — rendered deliverables + legacy Claude Design handoff bundles. Migrated consumers hold **outputs only** at `data/renders/<consumer>/`; unmigrated bundles stay at `data/renders/<sub>-design/` (read-only, replaced wholesale on regen) until their rendering P4 slot. See `data/renders/MANIFEST.md`.
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `financial/parquet/` (OHLCV, `ta-reference/`, `gics-symbols.parquet`), `financial/portfolios/`, `financial/reports/`, `financial/gics/` (`build.py` + `mapping.md`). Consumers: `trading/`, `analyzing/`, `accounting/`. Cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md`; shares the root `.data-write-lock` (below). Spec: `data/specs/data-charter-2026-05-17/financial-hub-migration-2026-05-29/SPEC.md`.
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject. Today: `code/playwright/` (shared `@playwright/test` helpers), `code/remotion/` (`@qagents/remotion`; `explaining/` B-roll), `code/agent_sdk/` (`qagents.agent_sdk` — typed `claude-agent-sdk` wrapper; § Agent SDK lane), `code/qreel/` (`/reel <bundle>` bake pipeline; spec `data/specs/qreel-2026-05-28/SPEC.md`), `code/lean_graph/` (`qagents.lean_graph` — cross-axis Lean4-aware K-graph extractor for quantify-progress; spec `data/specs/lean4-charter-2026-06-10/quantify-progress-2026-06-14/SPEC.md`). Subproject-owned workspace packages stay in their subproject.
- `lib/` — vendored upstream code; sibling of `code/`. Today: `lib/memsearch/` (vendored+patched; see § memsearch for the qagents patch detail); `lib/heygen-skills/` (vendored-pristine, MIT). Governance classes: vendored-pristine / vendored+patched / reference-only. See per-package `UPSTREAM.md`.
- `hub/` — read-only upstream clones, regularly refreshed, **gitignored wholesale** (canonical-only, absent from worktrees); reference ground truth, never committed or imported as code. The five Lean4 guide-rail rows are chartered (`studying/guide-rails.md`; `data/specs/lean4-charter-2026-06-10/SPEC.md` § 6); other clones are ungoverned consumer conveniences.

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only conventions that cross a boundary; subproject-specific rules live in each subproject's own `CLAUDE.md`.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13); all cross-subproject deps in root `pyproject.toml` extras (`[trading]`/`[analyzing]`/`[dev]`/`[verifying]`/`[evaluating]`). Bootstrap from a fresh checkout:

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
./.venv/bin/pip install -e '.[trading,analyzing,dev]'
./.venv/bin/pip install -e ./trading --no-deps         # registers `shared` / `shared.lib`
./.venv/bin/pip install -e ./code/agent_sdk --no-deps  # registers `qagents.agent_sdk`
```

From repo root → `./.venv/bin/python …`. From a subproject → `../.venv/bin/python …`. `proving/` and `accounting/` use system `python3` — neither needs the venv. (`monitoring/` is TypeScript-only — no Python.)

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

Single workspace at root: `pnpm-workspace.yaml` declares `analyzing`, `monitoring/web`, `designing/web`, `documenting/web`; shared dev tools via catalog (`"typescript": "catalog:"`). `onlyBuiltDependencies` at workspace level (`better-sqlite3`, `esbuild`). Root scripts: `pnpm {typecheck,build,verify}` → `pnpm -r --if-present <name>`.

### Playwright e2e (Astro sites)

Suites at `<sub>/web/tests/e2e/`; shared helpers at `code/playwright/`. Each `playwright.config.ts` runs three projects (chromium-desktop / -mobile / -reduced-motion); `webServer = pnpm build && pnpm preview` — never the dev server. Run: `pnpm -C <sub>/web test:e2e`. First-time: `test:e2e:install`.

### IDE: stable VSCode

Canonical IDE is stable VSCode. `analyzing/`'s VSCode extension uses N-API bindings — unaffected by Electron ABI switches. (monitoring's web app runs under plain Node — `pnpm rebuild better-sqlite3` on any Node-ABI mismatch.)

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

Complex, long-running work (subagent fan-outs, axiomatization, watchers, debates, collectors, overnight research) runs the **latest top-tier model** — never a pinned older tier. Today that is Opus 4.8: alias `opus` (agent frontmatter / Agent tool), `claude-opus-4-8` (CLI `--model` / SDK pins). When a new top tier ships, sweep the pins; prose should say "top-tier model", not a model name. Lesser models are acceptable only where flagged: `claude-sonnet-4-6` for routine bounded cron routines (intraday trading reviews, journaling, leaderboard), `haiku` for mechanical closed-set classification (`managing` verifier) and throwaway smoke runs. Capability floor: haiku is forbidden for any retained axiomatization artifact (2026-06-03 bake-offs; `feedback_predicate_model_opus_not_haiku`). **Per-leaf-class downgrade gate (2026-06-20 R2.3):** under hierarchical predicates the floor is *measured* — the default for every leaf-extraction class stays Opus (exit-3-enforced in the driver), and a leaf *class* becomes cheaper-model-eligible only after a per-class five-point bake-off clears; the "leaves must be Haiku-decidable" form is rejected. Capability ordering across leaves is **non-monotonic**, so eligibility is strictly per-leaf-class, never model-wide. Full gate criteria + the `proving/scripts/bakeoff_tier1.py` gate-ledger live in `feedback_predicate_model_opus_not_haiku`. Cron-lane budget caps (`MAX_BUDGET_USD`, `routines.toml` `max_budget_usd`) sit at opus-4.7-era sizing — if top-tier routines exit on caps, widen them, never downgrade the model.

## Programmatic Claude — Agent SDK lane

Cron-fired and library-callable Claude work goes through the typed Python wrapper at `code/agent_sdk/` (`qagents.agent_sdk`; verified against `claude-agent-sdk==0.2.82`). Shared by `trading/` and `managing/`. Routines opt into SDK-mode by suffixing the routine name with `:sdk` in `data/schedules/launchd/install.sh` ROUTINES; the default `claude --print` lane stays as-is otherwise. Adoption spec: `data/specs/agent-sdk-adoption-2026-05-17/SPEC.md`. SDK-mode draws the same Max-20x subscription limits as the default `claude --print` lane — the planned dedicated SDK credit was paused indefinitely 2026-06-15 (`reference_agent_sdk_credit_200_mo`; contingent, reverses if a new plan ships). Ledger at `data/agent-sdk-ledger/` still tracks usage.

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) the shared `data/` **and** `financial/` hubs only while holding `<root>/.data-write-lock` (one lock serializes both).

- Cron-fired writes never touch `data/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync. The verifier is a **closed-set allow-list** classifier — register a new `pending/` producer path in lockstep in `managing/.claude/agents/verifier.md` + `verify-pending.sh require_known_canonical_subtree`, else its files land in `unclassified[]`, never promoted. Spec: `data/specs/pending-promotion-scope-2026-05-28/SPEC.md`.
- Manual writers (fixed-path producers — `financial/gics/build.py`, `<sub>/scripts/status_emit.*`) acquire the lock unconditionally with atomic create (`set -C` + redirect), write holder id, release with `rm` on EXIT trap.
- Configurable-output-path scripts (`--out-dir`/`--out`, e.g. `analyzing/scripts/{ingest.py,ta_reference.py}`) acquire the lock **iff** the absolute target falls under canonical `data/` **or** `financial/`. Worktree-local `data/`/`financial/` writes skip the lock — they don't race canonical writers.
- Producers branch on `QAGENTS_PENDING_ROOT`: set (cron) → write `pending/<rel>`, no lock; unset (manual) → acquire lock, write canonical.

Spec: `data/specs/data-conventions-2026-05-06/SPEC.md`.

## Subproject `.claude/` shape (consistent pattern)

Every subproject that runs Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed permission allow/deny + the two
  `PreToolUse` hooks (`no-cd-git.sh`, `no-canonical-edit-while-locked.sh`).
  **Generated, not hand-edited** — edit `data/claude-settings/sources/` and
  re-run `scripts/claude-settings/build.py` (drift caught by `--check`). The
  universal allow baseline lives in **user scope** `~/.claude/settings.json`
  (cwd-only load); runtime permissions = user ∪ cwd-project scope — permit
  gates must union both files. Allow-list entries need a trailing `*` on a
  fully-literal prefix (`build.py --lint` rejects mid-globs). See
  `data/specs/claude-settings-unification-2026-06-06/SPEC.md` + memory
  `reference_claude_code_allow_glob_no_empty_match`.
- `<sub>/.claude/settings.local.json` — user-local overrides (gitignored); the
  weekly `dco-settings` lane harvests recurring patterns out of it into the
  generated sources.
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

- **Per-subproject scope (qagents patch).** Patched `common.sh` prefers `CLAUDE_PROJECT_DIR` over `git rev-parse --show-toplevel` — each subproject gets its own Milvus collection and `<sub>/.memsearch/memory/` daily-log tree. Preserve the **five** `qagents patch` blocks across upstream re-syncs (grep `qagents patch\|_stop_debug`; detail in `memsearch-worktree-wipe-2026-05-28.md`). **Vendored edits don't reach the live install** — after touching hooks, sync the `~/.claude/plugins/cache/memsearch-plugins/memsearch/<ver>/hooks/` copy (or `/plugin update`) in the same session (spec § 3.4).
- **Backend.** ONNX `bge-m3` local. Milvus Lite is single-writer; switch `milvus.uri` in `~/.memsearch/config.toml` for concurrent sessions.
- **Markdown is source of truth.** `<sub>/.memsearch/memory/YYYY-MM-DD.md` is the durable record (Milvus re-indexes from it); the whole `**/.memsearch/memory/` tree is gitignored local state, never tracked.
- **Worktree logs survive `/close`** — copied back to canonical first (`scripts/lib/memsearch-copyback.sh`, append-merge by `## Session` block). See `data/specs/open-close-dcu-2026-05-26/memsearch-worktree-wipe-2026-05-28/SPEC.md`.
- **Recall is fork-isolated** — `context: fork` keeps the curated digest out of the main context.

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

- **Schema owner:** `@qagents/diagram-kit` v0.5.0 (`SubprojectId` widened to 22 — adds `rendering`). 6-kind `PanelRef` union closed-set pinned in `data/specs/display-modes-2026-05-07/SPEC.md`.
- **Producers:** `<sub>/scripts/status_emit.{ts,py,mjs}`; atomic write (`.tmp` → `mv`/`os.replace`). Each producer pins a `KIT_VERSION` constant; sweep ALL pins in lockstep on kit `package.json` bumps (pins drift silently — T11). The close-time validator only checks `kitVersion` is a non-empty string — `designing/web/src/lib/status-loader.ts` carries the live `ACCEPTED_KIT_VERSIONS` set as the safety net during transitions.
- **Orchestrator:** `pnpm build:status` → `scripts/build-status-all.mjs` (producer failure non-fatal; placeholder fallback keeps build green). Bootstrap empty slots: `pnpm build:status:placeholders`.
- **Consumer:** `designing/web/src/lib/status-loader.ts` (Zod-validated; malformed JSON → placeholder).
- **Close-time emit (`/close --status-emit`, mandatory):** every `/close <branch>` runs the subproject's producer + `scripts/validate-status-emit.mjs` before the session commit. No producer → the sub's `CLAUDE.md` must carry `<!-- status-emit: opt-out — reason: ... -->` or exit 43. Whole-repo branches fan out via `build-status-all.mjs`. Spec: `data/specs/data-status-rename-2026-05-17/SPEC.md` § 4.
- **Pending-aware producers + steady-state cron:** every `status_emit.*` writes under `QAGENTS_PENDING_ROOT || REPO` (node) / `_resolve_out()` (python) — `||` truthiness, never `??`, so a set-but-empty env falls back to canonical (else a cron fire scatters cwd-relative slots lock-free). A daily `qagents:status-emit-all:05:25` cron re-emits the whole fleet in pending mode (promoted by managing's 06:00 verifier), so `/status` slots don't decay between infrequent closes; close-time `--status-emit` stays the per-session refresh. New producers MUST be pending-aware from the start. Spec: `data/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`.
- **Adding a subproject:** sweep eight surfaces in one PR — kit `SubprojectId`; loader `KNOWN_SUBS`; `STATUS_CARDS`+`STATUS_GROUPS`+`OG_META` (`designing/web/src/content/copy.ts`); `PRODUCERS` (`scripts/build-status-all.mjs`); `SUBS` (`scripts/write-status-placeholders.mjs`); the e2e fixture (`designing/web/tests/e2e/status.spec.ts`); `KNOWN_SUBS` (`scripts/validate-status-emit.mjs`); the `status_emit_producer()` case map (`scripts/close.sh`). No mounted surface → stay **hidden**: skip `STATUS_GROUPS` + the e2e visible set only. Bump kit minor and move **both** `PRESENT_KIT_VERSION` + `ACCEPTED_KIT_VERSIONS` in the loader in the same PR (`feedback_status_emit_kit_version_silent_drift`). Exemplar: the 2026-06-10 `rendering` widening (`rendering-2026-06-09.md` § 9).

Second instance of the data-hub-not-shared-code pattern: `data/donating/drive.json` (producer `donating/`; consumers `designing/web` + `documenting/web`).

## Kit-mount pattern

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`, get linked via `Layout.astro`'s `<slot name="head" />`, and are mounted per-run by `getStaticPaths` scanning `<sibling>/examples/*/{graph,report}.json`. Since the graphs-2 G6 unification (2026-06-11), three live instances mount the ONE domain-neutral graphs-2 kit at `<app>/web/public/graphs2/`:

1. `verifying/web/public/graphs2/` — proof-DAG pages + `/lattice`; `proving/`'s framework graphs (`verifying/CLAUDE.md` § 8).
2. `evaluating/web/public/graphs2/` — recomposed strategy mount, additionally composed with `@qagents/charts` + `@qagents/compose`; `accounting/`'s framework graphs (`evaluating/CLAUDE.md` § 2).
3. `monitoring/web/public/graphs2/` — operational `/operational` + `/constellation` mounts; `studying/`'s operational K-graph + constellation graph (`monitoring/CLAUDE.md` § Operational-axis consumer). Two departures from 1–2: its `kit.js` is **gitignored + generated fail-soft** (sync hook host-copies the canonical dist; empty-state if absent), and it reads at **request time** via an `/api` twin (private live data), never build-inlined via `getStaticPaths`.

All three regen-wholesale from `visualizing/graphs-2/dist/kit-{proof,strategy,graphs}.js` (NOT from `data/renders/<sub>-design/`); `loader.js` is the never-fold side-car. The old designer kits (`proof-graph/`, `strategy-chart/`) + `visualizing/graphs/` engines are removed. Schema + edge-kind detail: memory `project_proof_graph_kit_mount_pattern`.

## Lean4 axes — three kernels, one architecture

Three orthogonal axes, never sharing domain/ground-truth/consumer: **textual** `proving/` (`legal/uscode/`; plaintiff v. defendant; → `verifying/`), **numerical** `accounting/` (`financial/parquet/`; bulls v. bears; → `evaluating/`), **operational** `studying/` (git first; `hub/git`; coding v. testing; → `monitoring/`, local-only). Invariants (spec `data/specs/lean4-charter-2026-06-10/SPEC.md` § 4): (1) axiomatic kernel + LLM-generated `Facts.lean` + `lake build` as the gate; (2) **no manual proof driving, ever, by a human** — no human steps a proof at an editor surface, but tactics elaborated head-lessly by `lake build` (`prove_element`, core `grind`, an LLM/debate-lane-proposed script) are inv-3, not manual; `hub/vscode-lean4` is template source only; tactic code is kernel-side Lean (`Common/Tactic.lean`), never a Claude plugin — a plugin/skill carries proof-driving *knowledge* only (2026-06-20 R2.4/R2.5); (3) proofs driven by top-tier LLMs in parallel in the debate framework (`/dau`/`/dat`/`/dao`); (4) three-way toolchain lockstep, one commit, example proofs replayed; (5) one consumer per axis, seam = files/SSE, refusal rules mirrored from axioms, never relaxed UI-side; (6) presentation via `visualizing/` modalities + kit-mount only; (7) every axiomatization driver hard-gates all seven coherency gates G1–G7 with exit codes on every wave/round — advisory logs are conformance violations (spec `data/specs/lean4-charter-2026-06-10/cross-axis-coherency-2026-06-26/SPEC.md`). `studying/` owns the representation guide + `hub/` guide-rails.

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools. The allow-list refusal is one input to `evaluating/`'s **FINANCIALLY-CLEARED** gate (§ subproject list, `evaluating/`), which signs off any public surface that evaluates or implies a financial decision — a kernel refusal, never a safety guarantee.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` three-remote setup (`github` / `aws` / `qblk`) live in `serving/CLAUDE.md` § 8 + § 9 (deploy script, aws-vault + Keychain, bucket hardening, CodeCommit gotchas) — single owner; never duplicated here or in subproject CLAUDE.mds.

## Language split

- TypeScript for the VSCode extension and anything in `analyzing/src/`.
- Python for everything in `trading/`.
- A Python microservice is an allowed escape hatch from analyzing for heavy numerics (e.g. `analyzing/scripts/ta_reference.py` uses TA-Lib as ground truth).
- Never reach across: trading Python doesn't import analyzing, analyzing TS doesn't import trading.
