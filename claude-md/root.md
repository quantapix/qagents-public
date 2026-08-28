# qagents — Cross-project conventions

Subprojects under this repo:

Each `<sub>/CLAUDE.md` is the single owner of its own mechanics + spec path; the roster below is the constellation index — name, discriminating role, and cross-boundary relationships only.

- `analyzing/` — market-inspection tooling (TypeScript, local-only viewer); `financial/parquet/` tape supplier.
- `trading/` — Python portfolio-management agents: three PMs (aggressive/moderate/conservative) on Alpaca paper.
- `appealing/` — pro se federal appellate drafting. Markdown drafts; rendered PDFs flow to a private filing hub. CLAUDE.md content not mirrored — see `qagents-public/README.md` § "Litigation-domain CLAUDE.md\`s ... deliberately excluded".
- `pleading/` — pro se trial-court + status-affidavit + addendum drafting. Sibling of `appealing/`. Markdown drafts; rendered PDFs flow to the private filing hub. CLAUDE.md content not mirrored.
- `designing/` — Astro site for quantapix.com; hosts `/status`, aggregating every `data/status/<sub>.json`.
- `documenting/` — sibling of `designing/`; femfas.net v2.
- `monitoring/` — local-only Claude Code token analytics; chartered consumer of the **operational** Lean4 axis, never deployed.
- `proving/` — **textual** Lean4 axis (§ Lean4 axes), legal domain; backs `verifying/`.
- `accounting/` — **numerical** Lean4 axis over the `financial/parquet/` hub; backs `evaluating/`.
- `verifying/` — Astro+React shell + FastAPI server for **Qnarre**, the legal-complaint verifier UI; streams `proving/` over SSE.
- `evaluating/` — sibling of `verifying/` for **Qresev**, the portfolio evaluator UI; streams `accounting/` over SSE. Sole grantor of the **FINANCIALLY-CLEARED** gate (`accounting/` advises).
- `visualizing/` — graphing surface for the `proving/` + `accounting/` axiomatizations; mounts into Qnarre + Qresev (§ Kit-mount pattern).
- `studying/` — **operational** Lean4 axis; neutral steward of the cross-axis research + the `hub/` guide-rails. Consumer `monitoring/`.
- `explaining/` — video-explainer arc for Quantapix outreach; output is scripts, whose stage 5 consumes `resolving/`.
- `resolving/` — DaVinci Resolve production-assistance; stage 5 of `explaining/`.
- `blending/` — Blender + Geometry Nodes background plates for `explaining/` → `resolving/`.
- `serving/` — AWS cloud-base; single source of truth for every AWS resource. Hosts `@qagents/diagram-kit` (sibling-of-subprojects, not member-of-serving).
- `managing/` — daily cron-fired watcher; its verifier promotes `pending/` (§ Shared-data write-lock). **Observe-only**; `managing/CLAUDE.md`.
- `shorting/` — adversarial sibling of `managing/`; positions lane + the chartered review fleets (`data/charters/shorting/review-lanes/CHARTER.md`). **Observe-only**; routes findings to `managing/`.
- `donating/` — public donation drive (2026-06-01 → 2026-12-01); renders `data/donating/drive.json` for `designing/web` + `documenting/web`. Content-only.
- `publishing/` — open-source release lane; owns the public-org staging tree + the `/publish` pipeline to `github.com/quantapix/*`. Content-in / external-out; **not** observe-only.
- `rendering/` — render engine + brand source of truth; single owner of **brand-bearing, pre-rasterized** artifacts constellation-wide. Deliverables in `data/renders/<consumer>/`.
- `extending/` — Claude Desktop extensions; MCP proxies over verifying:8787 / evaluating:8788, never a fourth Lean consumer. Ships via `publishing/`.
- `developing/` — native macOS + iOS SwiftUI clients for Qnarre + Qresev. Swift-only; never a fourth Lean consumer — live wiring rides the same 8787 / 8788 seams.
- `simulating/` — agent-based market simulation; 4th consumer of the `financial/` tape hub, factor-anchored on promoted `financial/factors/` copies; mounts visualizing charts. Never a Lean consumer (§ Language split); FINANCIALLY floor from birth.

Shared-data hubs (no code, read-only unless regenerating):

- `data/` — cross-project datasets + cross-cutting machinery (`status/`, `schedules/`, `specs/`, `renders/`, `donating/`, …). Charter + audit table: `data/CLAUDE.md` (closed-set kinds, three-question gate, single-owner rule). Market/trading datasets are in `financial/` (below).
- `data/schedules/` — canonical macOS-launchd cron for **all** subprojects. **Never** cloud `/schedule` or `RemoteTrigger` — the cowork sandbox can't mount the repo. **ROUTINES is a set of dependency chains, not independent fires** — a mid-chain HOST change breaks the handoff and a same-host RETIME silently re-aims every reader, both while every fire exits 0: `data/schedules/CLAUDE.md`.
- `data/renders/` — rendered deliverables + legacy design handoff bundles; see `data/renders/MANIFEST.md`.
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `parquet/`, `portfolios/`, `reports/`, `universe/`, `gics/`, `factors/`; consumers `trading/`, `analyzing/`, `accounting/`, `simulating/` cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md` (the dataset roster drifted twice when mirrored here — `financial/parquet/CLAUDE.md` § Datasets is its single owner). Shares the root `.data-write-lock`.
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject. Package roster (never mirrored here), spec pins, runnable-only-at-canonical, the `workspace:*` seam-law exception: `code/CLAUDE.md`.
- `lib/` — vendored upstream code; sibling of `code/`. Governance classes (vendored-pristine / vendored+patched / reference-only) + per-package `UPSTREAM.md`; today `lib/memsearch/` (§ memsearch) + `lib/heygen-skills/`.
- `hub/` — read-only upstream clones, **gitignored wholesale** (canonical-only, absent from worktrees); reference ground truth, never committed or imported as code. Five Lean4 guide-rail rows chartered (`studying/guide-rails.md`).

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only cross-boundary conventions.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13); cross-subproject deps in root `pyproject.toml` extras (never mirrored here). Bootstrap/repair a checkout (idempotent): `bash scripts/bootstrap-machine.sh [--profile full|trading-lane] [--check]`; env drift: `scripts/parity.sh`, single owner of cross-workstation parity. Parity invocation traps (`--compare` ≠ `--gate`): `feedback_cross_cadence_grading_is_a_clock_check`. **Every editable points at CANONICAL** — a worktree `python -m <pkg>` runs canonical code AND canonical data paths, so a proof-of-fire witness can pass VACUOUSLY against an unmodified tree; assert `module.__file__` before trusting a red or a green. Instances + cures: memory `feedback_worktree_path_determines_working_tree`.

From repo root → `./.venv/bin/python …`; from a subproject → `../.venv/bin/python …`. The `proving/`/`accounting/` drivers + status emitters run system `python3` (accounting's pandas helpers are the venv exception); `simulating/`'s engine + MLX lane run the root venv (`[simulating]` extra, `full` profile only — a missing-extra fire fails loudly by design). Extra-addition discipline — `--check` on the firing host, sweep the CLASS against the profile union (declaring ≠ requesting), and `uv run` rewrites the venv (pass `--no-project`/`--isolated`): `reference_root_venv_extras_and_uv`.

## Shell scripts — homebrew tool versions

Any shell script (cron-fired, operator-fired, or session-invoked) MUST resolve to homebrew-installed tools, not macOS system defaults. macOS ships bash 3.2.57 (no `mapfile`/`readarray`/`declare -A`/`${var^^}`), no GNU coreutils, BSD `sed`/`awk`/`date`.

1. **Cron-lane PATH + portable-script recipes** — plist PATH ordering, bash-4+ avoidance, absolute-path homebrew features, audit patterns: memory `feedback_homebrew_over_system_for_qagents_scripts`; silent-abort pipeline/test traps: `reference_shell_script_test_gotchas`. **The invoking shell AND the pipeline are part of the measurement** — `$?` reports the last command in a PIPELINE (a blocking gate piped to `tail` prints `exit=0` over a true exit 9), and zsh does not word-split (an unquoted `$VAR` reaches argparse as ONE argument): any lane that SCRIPTS a gate sets `set -o pipefail`.
2. **Non-login shells skip `~/.zprofile` — probe BOTH kinds.** cmux panes, `ssh host <cmd>` and launchd run non-login shells (2026-08-06: `elan`+`lake` missing in every cmux pane — it cost the three Lean4 axes). Seat: `scripts/shell/qagents-env.zsh` via `install-shell-seat.sh` (`bootstrap-machine.sh` step 10). The **checker's own shell kind is part of the measurement** — re-run any PATH WARN under `zsh -i -c` before calling it a defect. Probe forms + live instances: `reference_non_login_shell_skips_zprofile`.
3. **Sibling-of-subprojects pkgs are *runnable* only at canonical.** Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths.
4. **NEW scripts pin the uutils subset** (lean4-rust-uniformity § 9 new-code rule): every new `date`/`stat`/`sort`/`wc`/`ls`/`mktemp` call site takes the brew `uutils-coreutils` pin — **per call site only** (first-on-PATH / `run_routine`-level prepends REJECTED, they flip every routine at once). Existing sites migrate only via the § 9 per-lane bake-off; seats `bootstrap-machine.sh` step 1b + parity `env.brew.uutils`.
5. **`scripts/dialect-lint.sh` is the reader** — FAIL-OPEN dialect classes; report-only on existing sites, `--new-code <ref>` fails. Classes, counts, migration path: the script's own header.

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. Node code (CLIs, CDK, kit packages).
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's presets; vendored `lib/` is upstream-owned.

- **pnpm workspace + catalog** — single workspace at root: `pnpm-workspace.yaml` owns the member list, catalog, and `allowBuilds` (pnpm 11). Shape, root-script verbs, placeholder trap: `reference_pnpm11_allowbuilds`.
- **Playwright e2e (Astro sites)** — suites at `<sub>/web/tests/e2e/`; run `pnpm -C <sub>/web test:e2e`. Helpers, config shape + traps: `project_playwright_e2e_stack`. **Preview-port registry** (claim the next free port first): `code/playwright/PORTS.md`.
- **IDE + parallel sessions** — VSCode is a plain editor, no canonical-IDE claim; parallel Claude Code sessions are coordinated by **cmux** (`scripts/cmux-session.sh`): `project_cmux_coordinator`.

## Canonical OHLCV bar shape

The bar-column contract (`ts/o/h/l/c/v/adj_c`) shared by all three consumers (`trading/`, `analyzing/`, `accounting/`) lives in `financial/parquet/CLAUDE.md` § "Canonical OHLCV bar shape" — the hub is its single source of truth. Adapters translate vendor field names at the boundary; never leak them past the client module.

## GICS sector / industry classification

GICS mapping is *shared data, not shared code*: parquet at `./financial/parquet/gics-symbols.parquet` keyed by `symbol`. Readers: `analyzing/web/src/lib/gics.ts` (DuckDB view `gics`) + `python -m shared.lib.gics`. Neither side writes the parquet — seed/refresh via `financial/gics/build.py`; schema + caveats: `financial/gics/mapping.md`.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`, `/do-steps`

Sessions start with `/open <project>`, end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints; `/do-steps` works a project's next-steps slot inside an open session (spec `do-steps-2026-07-25`). Memory + CLAUDE.md optimization: `/dco-manual` standing, `/dco` cron parked (`data/charters/qagents/optimization/CHARTER.md`). **Single normative owner: `data/charters/qagents/session-lifecycle/CHARTER.md`** — the one-liners below render its anchors; on divergence trust the charter (§ 2.2).

- **Lock model** (charter § 2.1 / § lock-model): branch-presence IS the write-lock; `<project>`/`<project>-N` blocks conflicting `/open`s, `/open qagents` blocks all. The session-branch grammar `^[a-z]+(-[0-9]+)?$` is the ONE lock-holder definition; slash-named refs (`lift/*`, `<node>/*`) are never lock conflicts.
- **Worktree path discipline (load-bearing)** (charter § 2.3 / § path-discipline): inside any `/open` session, every `Edit`/`Write` `file_path` MUST begin with `<root>-wt/<branch>/` — a canonical edit lands on `main`, silently bypassing the lock. `scripts/hooks/no-canonical-edit-while-locked.sh` sees Edit/Write **tool calls only**, so subprocess writes (`sed -i`/`tee`/redirects/heredocs) fire nothing and test green; `close.sh --pre` exit 12 catches them only at close. Reads may use canonical; cron-lane fires write canonical cwd-relative paths. The check is not "path prefix" but **"is this coordinate the SUBJECT'S?" — tree, cwd, spelling**. Corollaries (the PERMITTED-destination case, repo verbs resolving a tracked path from CWD, peer worktrees), instances + recovery: `feedback_worktree_path_determines_working_tree` + `reference_pretooluse_editwrite_hook_only_sees_tool_calls`.
- **Canonical-shared gitignored content** (charter § 2.4): declared per owner in `<sub>/.worktree-links`, symlinked into worktrees by `scripts/open.sh` (ruling 2026-08-07, ns:qagents/120). **Walkers must dereference (`tar -h`, `rsync -aL`) or hard-refuse** — `find` does not descend a symlinked dir (`project_parquet_gitignored_ground_truth`); that rule is UNENFORCED prose, and the linked trees are writable from EVERY worktree. Loss instance + standing asks: `ns:qagents/123`.
- **Bash discipline (load-bearing)** (charter § 2.2): close-lane bash uses absolute script paths only — each path form needs a separate allow-list matcher.
- **Close-gate exits** — charter § 2.6's table is the ONE enumeration, never mirrored here; read it before authoring against one (three rows were added 2026-08-23 — **30**/**31**/**32**; the table carries their conditions, and mirroring them here is what let one of them go stale).
- **Cross-subproject writes · Stack · Sentinels · Adopted-spec convention** — cold anchors, in the charters only: session-lifecycle §§ 2.7 / 2.1 + spec-lifecycle § 2.7.
- **CLAUDE.md updates** (charter §§ 2.6 / 2.9): *immediate* (project's own CLAUDE.md on the session branch) + *deferred hints* (`data/claude-updates/<branch>.md`, judged later by `/do-claude-updates`).
- **Backward + forward surfaces** (charter § 2.8): `/close` writes `data/summaries/close/<ISO>-<branch>.md` (versioned, never overwritten); `data/next-steps/<project>.md` is the forward-only GENERATED render of `ledger.ns_item_event` — write via the `ns-*` verbs, never by hand; a resolution-verb commit cite fires the close-time `--next-steps` gate. Owner: `data/next-steps/CLAUDE.md`.

## Model policy — LLM model selection

Complex, long-running work (fan-outs, axiomatization, watchers, debates, overnight research) runs the **top-tier model** (today the **`opus` alias**). Review/optimization fleets carry **no `model:` pins** (they inherit the orchestrator's). The three axiomatization lanes resolve from ONE seat (`code/lean_tools/model_floor.py`) — sweep it, not per-axis pins. Lesser models only where flagged: `sonnet` for bounded cron routines, `haiku` for mechanical closed-set classification and smoke runs. **Always bare tier aliases — never a pinned minor, never an older tier.** **Capability floor:** haiku is forbidden for any retained axiomatization artifact. Mechanism detail (quota rationale, billing fail-close, budget caps, `QAGENTS_AXIOMATIZE_MODEL`, sweep roster): memory `project_model_policy_latest_top_tier` + `feedback_predicate_model_opus_not_haiku`.

## Programmatic Claude — Agent SDK lane

This § owns the status: the Agent SDK lane is **parked** (Max-20x SDK credits dropped 2026-06-15); every routine runs the default `claude --print` lane. Standing operator ruling 2026-07-16: never a live dependency, a parked flow target (`ext:agent-sdk-credit`), no contingency planning until an official reversal. Retained code/tests + un-park recipe: `project_agent_sdk_wrapper`.

## Shared-data write-lock — `.data-write-lock`

Each subproject writes (a) its own subdir freely (branch-as-write-lock) and (b) the shared `data/` **and** `financial/` hubs only while holding `<root>/.data-write-lock` (one lock serializes both).

**Shared ledger store (Postgres — qred LAN primary) is the canonical mechanism for new shared ledger-like data** (single shared file, many appenders): such surfaces start as a store table + single-writer rendered git projection, never a hand-appended shared file — and a projection needs a WRITE PATH, not just a render verb. **ACK a write by READING IT BACK, never by arithmetic on a count** (an UPDATE verb leaves the count FLAT while succeeding); "exactly ONE writer" is serialization in TIME, not mechanism, so two same-day closes meet on the projection as a merge conflict. Rationale, traps, reader side: `project_shared_ledger_store_postgres` + `code/ledger/`.

- Cron-fired writes never touch `data/`/`financial/` directly — they stage into `pending/` (gitignored buffer mirroring canonical paths); `managing/`'s daily verifier does the lock-protected rsync. **One chartered exception:** the `analyzing:tape-refresh` lane (script-direct) writes canonical `financial/parquet/` DIRECTLY under `.data-write-lock`, never through `pending/` — owner `data/specs/analyzing-charter-2026-07-01/tape-cron-2026-08-09/` (exit contract: `data/charters/analyzing/tape-supply/CHARTER.md` § exit-contract). The verifier is a **closed-set allow-list** classifier — register a new `pending/` producer path in lockstep (`managing/.claude/agents/verifier.md` + `verify-pending.sh require_known_canonical_subtree`) or its files land `unclassified[]`, unpromoted.
- Everything else: fixed-path writers acquire the lock by atomic create and release it from an EXIT trap; configurable-output-path scripts acquire it **iff** the resolved target is canonical `data/`/`financial/`; a writer on the `QAGENTS_PENDING_ROOT` branch is staging, not writing canonical, and takes no lock.
- **Decide from how the target was AIMED, never by comparing paths.** `REPO_ROOT.parent / "financial"` is right from canonical and wrong from a worktree copy (there `REPO_ROOT.parent` IS the worktree), so an explicitly `--root`-aimed worktree write is misclassified as canonical and drops a spurious lock the next writer then fails on. Explicit `--root` (branch-as-lock) and `QAGENTS_PENDING_ROOT` (staging) take NO lock; only the aim-less canonical default locks. Arm worth copying: an aimed write must neither take nor touch a stale lock file.

## Subproject `.claude/` shape (consistent pattern)

Every subproject running Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed allow/deny + the standard hook set (the one enumeration is `data/claude-settings/sources/baseline.hooks.json`). **Generated, not hand-edited** — edit `data/claude-settings/sources/`, re-run `scripts/claude-settings/build.py` (drift: `--check`). Permission scoping, the allow-glob trap, worktree-root launch-cwd guards: `data/charters/qagents/specs/claude-settings-unification-2026-06-06/SPEC.md` §§ 3/4.5 + `reference_claude_code_allow_glob_no_empty_match`.
- `<sub>/.claude/settings.local.json` — user-local overrides (gitignored); `<sub>/.claude/skills` → symlink to `../../.claude/skills`; `<sub>/.claude/agents/` — optional per-subproject sub-agent definitions.

**A `<sub>/CLAUDE.md` has two readers you did not plan for.** (1) Several are
PUBLISHED (`PUBLISHED_CLAUDE_MD` in `publishing/scripts/sync_mirror.py`) and
gate (1e) excludes that subtree by construction — so **describe a restriction,
never name the restricted file**; documenting a bar is exactly the context in
which a barred file gets named. (2) It reaches every subagent in SYSTEM
CONTEXT, which no graded channel sees and no transcript records — on the
blind-fanout axes, prose added here is prompt content for the cells (`proving/`
discharged; `accounting/` open at `ns:accounting/127`).

## Skill placement rules

- `./.claude/skills/` — cross-project (auto-loaded via each subproject's `skills` symlink).
- **Subproject-scoped** (not auto-loaded; invoked explicitly):
  - `trading/shared/skills/` — trading-only.
  - `trading/agents/<pm>/.claude/skills/` — PM-scoped.
  - the private filing hub — Combined RA agent team (1 coordinator + 10 volume agents); callable by drafting siblings (`appealing/`, `pleading/`).

## memsearch — semantic memory across qagents sessions

Vendored at `lib/memsearch/` as a Claude Code plugin (v0.4.16 since 2026-07-30). Markdown is the source of truth. Install, the ten `qagents patch`es, backend + retained invariants: `lib/memsearch/CLAUDE.md` § "qagents integration". Recall: `memsearch:memory-recall`.

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

`.mcp.json` is subproject-scoped, never repo-rooted (cwd walk-up; rationale + apply pattern: memory `reference_mcp_subproject_scoped_via_file_location`). Today only `explaining/.mcp.json` is wired (`heygen`); DaVinci Resolve scripting is the typed wrapper at `resolving/davinci/`, no MCP.

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (schema owner v0.8.0, `SubprojectId` closed set = 25); `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS/Python imports — the JSON hub is the only seam.

- **Whole-slot failure trap (every `/close --status-emit`):** a SINGLE contract-violating field drops the ENTIRE slot to placeholder on prod — coercion rules, field examples, consumer posture: `project_diagram_kit`.
- **Public surface — synthetic fixtures only:** every slot renders publicly at `quantapix.com/status/<sub>`, so a producer whose inputs can carry real matter MUST filter to synthetic/allow-listed fixtures (mirror `verifying/server/main.py ALLOWED_EXAMPLE_IDS`) — never real dockets/positions (`<live-matter>_*`). Fleet rule + close-time denylist scan: `reference_operational_axis_public_surface_privacy`.
- Producer/orchestrator/close-time-emit/pending-aware-cron/KIT_VERSION-lockstep + the eight-surface add-a-subproject sweep: `project_diagram_kit` § "Root § Status hub". Spec: `data/charters/qagents/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`.

## Kit-mount pattern

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`. **FIVE live mounts, not all one kit**, and a mount need not be the composed bundle. A mount's `tokens-*.css` + `kit.js` are a **lockstep pair**; guards assert PER SHEET with an anti-vacuity arm; the unit of isolation is per MOUNT, not per file. Rebuild the canonical dist before any re-host-copy, grade staleness by **HASH** never mtime, and grep bundles with `grep -a` (bare `grep` lies `0`). Roster, regen/verify discipline, guard translation, traps: memory `project_proof_graph_kit_mount_pattern`.

## Lean4 axes — three kernels, one architecture

Three orthogonal axes, never sharing domain/ground-truth/consumer: **textual** `proving/` (`legal/uscode/`; plaintiff v. defendant; → `verifying/`), **numerical** `accounting/` (`financial/parquet/`; bulls v. bears; → `evaluating/`), **operational** `studying/` (git first; `hub/git`; coding v. testing; → `monitoring/`, local-only). Standing rules for all three: **(i) a claim that a rule is MECHANIZED is a claim about a CALL SITE — cite it or write "by discipline"**; a site that EMITS an instruction is not one that PERFORMS it, and a CELL CONTRACT or SKILL recipe an agent runs verbatim IS a call site — invisible to every grep over `*.sh`, so when a shared tool's refusal surface changes, sweep `.claude/agents/*.md` and the SKILL recipes, not just the drivers. **(ii) A gate change is not landed until the surface that AUTHORS the graded artifact says the same thing** — a compliant agent obeying a stale contract keeps producing what the new gate refuses, and grading it grades the instruction it was given. **(iii) No agent may assert ground truth is ABSENT without a failable ENUMERATION of what is present** — a NOT-FOUND read is not an absence, and an absence claim costs nothing to make. Chief invariant: **no human proof-driving, ever**; the other seven (incl. **proof-of-fire** — every mechanical gate ships a committed known-bad witness): `project_lean4_three_axis_charter`. Spec `data/charters/studying/specs/lean4-charter-2026-06-10/SPEC.md` § 4 + `axiomatize-shared-2026-07-04/`. **Per-axis scope charters:** `data/charters/{studying/operational-axis,proving/textual-axis,accounting/numerical-axis}/CHARTER.md` (studying = neutral steward).

## Defined-risk options — cross-project rule

Code that constructs/evaluates/submits options orders is restricted to: `long_call`, `long_put`, `debit_spread_call`, `debit_spread_put`, `covered_call`, `protective_put`. Enforced by `trading/shared/skills/options-risk/SKILL.md` (authoring) and `trading/.claude/agents/options-risk-analyzer.md` (runtime); neither optional. Applies to analyzing-side tools. **COMPOSITION CARVE** (2026-08-01): a composed multi-leg structure neither widens the allow-list nor extends `Strategy` **iff** every leg is independently allow-listed **and** every short leg is book-covered — worked cases + the boundary: `evaluating/CLAUDE.md` § 4 (sole FINANCIALLY grantor). The allow-list refusal is one input to the **FINANCIALLY-CLEARED** gate — a kernel refusal, never a safety guarantee.

## AWS deploys & multi-remote git push

S3 + CloudFront Astro deploys and the `git push-all` multi-remote setup live in `serving/CLAUDE.md` § 8–§ 10 (single owner; never duplicated downstream). Cross-machine session exchange rides the same qblk/qred mirrors as the symmetric leaf-`/push` / hub-`/pull` cycle (`<node>/<topic>` refs; hub = sole merge-point) — mechanics owned by `data/charters/qagents/push-pull/CHARTER.md`.

## Language split

- Rust — exactly two in-repo authoring surfaces: `code/substrate/`
  (`qagents-substrate`, bin `qs`) is the session-lifecycle mechanics layer
  (charter `data/charters/qagents/session-lifecycle/`); `code/context/`
  (`qagents-context`, bin `qx`) is context injection (PCI mechanism layer —
  contract owner stays the PCI spec family), output shortening, and the
  memsearch replacement (specs `rust-context-2026-07-22` +
  `rust-memsearch-2026-07-22`). Per-crate detail: `code/CLAUDE.md`. New Rust
  surfaces need their own charter-lane ruling; external Rust CLIs
  (rtk/herdr/worktrunk) stay arm's-length binaries, never workspace members.
- Lean4 is the three axes' kernel language (§ Lean4 axes) **plus**, since the
  2026-08-09 drivers adoption, a general-purpose language for `simulating/`
  only (`simulating/driver/`, follower toolchain pin). The carve does not widen
  the axis set: simulating stays "never a Lean consumer", the kernel/oracle bar
  is unchanged, and `simulating/driver/**` is EXCLUDED for every axis lane
  (never a template/corpus/prompt-context/pattern-donor — the reverse-corpus
  bar). Any other subproject wanting Lean4 needs its own ruling.
- TypeScript for anything in `analyzing/src/`; a Python microservice is analyzing's allowed escape hatch for heavy numerics (`analyzing/scripts/ta_reference.py` uses TA-Lib as ground truth). Python for everything in `trading/`. Never reach across: trading Python doesn't import analyzing, analyzing TS doesn't import trading.
