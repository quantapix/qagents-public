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
- `financial/` — market/trading shared-data hub; domain peer of `legal/`. Holds `parquet/`, `portfolios/`, `reports/`, `universe/`, `gics/`, `factors/`; consumers `trading/`, `analyzing/`, `accounting/`, `simulating/` cite by `../financial/<dir>/...`. Per-dir governance in each `financial/<dir>/CLAUDE.md`; `financial/parquet/CLAUDE.md` § Datasets owns the dataset roster. Shares the root `.data-write-lock`.
- `legal/` — private filing hub; authoritative source for `appealing/`, `pleading/`, `documenting/`. Layout not mirrored. CLAUDE.md content not published.

Shared-code hubs (cross-subproject code, sibling-of-subprojects):

- `code/` — repo-wide shared code, owned by no single subproject. Package roster (never mirrored here), spec pins, runnable-only-at-canonical, the `workspace:*` seam-law exception: `code/CLAUDE.md`.
- `lib/` — vendored upstream code; sibling of `code/`. Governance classes (vendored-pristine / vendored+patched / reference-only) + per-package `UPSTREAM.md`; today `lib/memsearch/` (§ memsearch) + `lib/heygen-skills/`.
- `hub/` — read-only upstream clones, **gitignored wholesale** (canonical-only, absent from worktrees); reference ground truth, never committed or imported as code. Five Lean4 guide-rail rows chartered (`studying/guide-rails.md`).

Subprojects share a domain only when stated (trading+analyzing: equities + defined-risk options; appealing+pleading+legal: dockets and rules). This file pins only cross-boundary conventions.

## Python venv (single, root-level)

One venv: **`<root>/.venv`** (Python 3.13); cross-subproject deps in root `pyproject.toml` extras (never mirrored here). Bootstrap/repair a checkout (idempotent): `bash scripts/bootstrap-machine.sh [--profile full|trading-lane] [--check]`; env drift: `scripts/parity.sh`, single owner of cross-workstation parity. Parity invocation traps (`--compare` ≠ `--gate`): `feedback_cross_cadence_grading_is_a_clock_check`. **Every editable points at CANONICAL** — a worktree `python -m <pkg>` runs canonical code AND canonical data paths, so a proof-of-fire witness can pass VACUOUSLY against an unmodified tree; assert `module.__file__` before trusting a red or a green. Instances + cures: memory `feedback_worktree_path_determines_working_tree`.

From repo root → `./.venv/bin/python …`; from a subproject → `../.venv/bin/python …`. System `/usr/bin/python3` (3.9) is never invoked. Bare `python3` is Homebrew's (3.14 since 2026-09, no third-party packages) — stdlib-only scripts only; anything importing a third-party or editable package pins the root venv at BOTH the shebang and every call site (an import-guard probing bare `python3` skips silently). ⚠ Xcode's interpreter can be licence-DEAD and `[ -x ]` cannot see it (`ns:qagents/240`); `simulating/`'s engine + MLX lane run the root venv (`[simulating]` extra, `full` profile only — a missing-extra fire fails loudly by design). Extra-addition discipline (declaring ≠ requesting; `uv run` rewrites the venv): `reference_root_venv_extras_and_uv`.

## Shell scripts — homebrew tool versions

Any shell script (cron-fired, operator-fired, or session-invoked) MUST resolve to homebrew-installed tools, not macOS system defaults. macOS ships bash 3.2.57 (no `mapfile`/`readarray`/`declare -A`/`${var^^}`), no GNU coreutils, BSD `sed`/`awk`/`date`.

1. **Cron-lane PATH + portable-script recipes** — plist PATH ordering, bash-4+ avoidance, absolute-path homebrew features, audit patterns: memory `feedback_homebrew_over_system_for_qagents_scripts`; silent-abort pipeline/test traps: `reference_shell_script_test_gotchas`. **The invoking shell (zsh: no word-split), the PIPELINE (`$?` grades the last command) and the INTERPRETER are part of the measurement** — a scripted gate sets `set -o pipefail` AND names the interpreter carrying its deps (same file, items 6/10/11).
2. **Non-login shells skip `~/.zprofile` — probe BOTH kinds.** cmux panes, `ssh host <cmd>` and launchd run non-login shells (2026-08-06: `elan`+`lake` missing in every cmux pane — it cost the three Lean4 axes). Seat: `scripts/shell/qagents-env.zsh` via `install-shell-seat.sh` (`bootstrap-machine.sh` step 10). The **checker's own shell kind is part of the measurement** — re-run any PATH WARN under `zsh -i -c` before calling it a defect. Probe forms + live instances: `reference_non_login_shell_skips_zprofile`.
3. **Sibling-of-subprojects pkgs are *runnable* only at canonical.** Hardcode canonical (`<root>/<sibling>/<pkg>`) for shared sibling resources; keep cwd-derived `<sub>_ROOT` for output paths.
4. **NEW scripts pin the uutils subset** (lean4-rust-uniformity § 9 new-code rule): every new `date`/`stat`/`sort`/`wc`/`ls`/`mktemp` call site takes the brew `uutils-coreutils` pin — **per call site only** (first-on-PATH / `run_routine`-level prepends REJECTED, they flip every routine at once). Existing sites migrate only via the § 9 per-lane bake-off; seats `bootstrap-machine.sh` step 1b + parity `env.brew.uutils`.
5. **`scripts/dialect-lint.sh` is the reader** — FAIL-OPEN dialect classes; report-only on existing sites, `--new-code <ref>` fails. Classes, counts, migration path: the script's own header.
6. **A gate's POPULATION is part of the measurement — a text-scanning gate needs an anti-vacuity arm.** Fail closed on the unscanned COUNT; over a DERIVED surface (text layer, OCR, extract) witness the RECOVERED population against the source (a PDF's source is the span's page image, `quoted_string_check.py`'s RASTER class, never a re-extraction); **a guard in SOURCE is not a guard that is RUNNING** — probe the non-tree public surfaces (APIs, status pages, CDN objects, sites + their DERIVATIVES: reader → emit → served) off-host, and ask "should this be live at all", not "is it newly live": `reference_shell_script_test_gotchas` item 12, `feedback_marginal_exposure_needs_the_live_surface`.

## TypeScript (shared compiler bases)

Three root tsconfigs carry cross-target invariants. Subprojects extend one and add only `outDir`/`rootDir`/`include`/`exclude`:

- `tsconfig.base.json` — shared compiler flags only.
- `tsconfig.node.json` — Node16 + ES2022, no DOM. Node code (CLIs, CDK, kit packages).
- `tsconfig.webview.json` — ESNext + Bundler resolution, `DOM` lib, `noEmit: true`. Browser bundles fed to esbuild/Vite.

`<sub>/tsconfig.json` extends `../tsconfig.node.json`; webview surfaces add `<sub>/tsconfig.webview.json`. `designing/web/` + `documenting/web/` extend Astro's presets; vendored `lib/` is upstream-owned.

- **pnpm workspace + catalog** — single workspace at root: `pnpm-workspace.yaml` owns the member list, catalog, and `allowBuilds` (pnpm 11). Shape, root-script verbs, placeholder trap: `reference_pnpm11_allowbuilds`.
- **Playwright e2e (Astro sites)** — suites at `<sub>/web/tests/e2e/`; run `pnpm -C <sub>/web test:e2e`. Helpers, config shape + traps: `project_playwright_e2e_stack`. **Preview-port registry** (claim the next free port first): `code/playwright/PORTS.md`.
- **IDE + parallel sessions** — VSCode is a plain editor, no canonical-IDE claim; parallel Claude Code sessions are coordinated by **cmux** (`scripts/cmux-session.sh`): `project_cmux_coordinator`.

## Market-data contracts — OHLCV bars + GICS

Both are *shared data, not shared code*, and each has one downstream owner that this file never mirrors: the bar-column contract (`ts/o/h/l/c/v/adj_c`; consumers `trading/`+`analyzing/`+`accounting/`) → `financial/parquet/CLAUDE.md` § "Canonical OHLCV bar shape"; the GICS mapping (`financial/parquet/gics-symbols.parquet`, keyed by `symbol` — producer, reader roster, monotone-write rule, schema caveats) → `financial/gics/CLAUDE.md` + `mapping.md`. Adapters translate vendor field names at the boundary, never past the client module; nobody hand-writes the gics parquet.

## Session lifecycle — `/open`, `/close`, `/do-claude-updates`, `/do-steps`

Sessions start with `/open <project>`, end with `/close [--to-main]`. `/do-claude-updates` flushes queued cross-subproject CLAUDE.md hints; `/do-steps` works a project's next-steps slot inside an open session (spec `do-steps-2026-07-25`). Memory + CLAUDE.md optimization: `/dco-manual` standing, `/dco` cron parked (`data/charters/qagents/optimization/CHARTER.md`). **Single normative owner: `data/charters/qagents/session-lifecycle/CHARTER.md`** — the one-liners below render its anchors; on divergence trust the charter (§ 2.2).

- **Lock model** (charter § 2.1 / § lock-model): branch-presence IS the write-lock; `/open qagents` blocks all. The ONE lock-holder grammar is `^[a-z]+(-[0-9]+)?$`; slash-named refs (`lift/*`, `<node>/*`) never conflict.
- **Worktree path discipline (load-bearing)** (charter § 2.3 / § path-discipline): inside an `/open` session every `Edit`/`Write` path begins `<root>-wt/<branch>/` — a canonical edit lands on `main`, bypassing the lock. The hook sees tool calls only; subprocess writes (`sed -i`, redirects, heredocs) surface only at `close.sh --pre` exit 12. The check is **"is this coordinate the SUBJECT'S?" — tree, cwd, spelling, worktree NAME**, not a prefix: `feedback_worktree_path_determines_working_tree` + `reference_pretooluse_editwrite_hook_only_sees_tool_calls`.
- **Canonical-shared gitignored content** (charter § 2.4): `<sub>/.worktree-links`, symlinked by `scripts/open.sh`; writable from EVERY worktree. **Walkers dereference (`tar -h`, `rsync -aL`) or hard-refuse** — unenforced prose (`project_parquet_gitignored_ground_truth`, `ns:qagents/123`).
- **Untracked deliverables at `/close`** (charter § 2.3): Phase 7 wipes untracked files like gitignored ones. Ask what the session PRODUCED that is not committed, archived or sent; resolve a `??` by provenance, never by deleting to go green: `feedback_git_worktree_remove_wipes_gitignored`.
- **Bash discipline (load-bearing)** (charter § 2.2): close-lane bash uses absolute script paths only.
- **Close-gate exits** — charter § 2.6's table is the ONE enumeration, never mirrored here. ⚠ On a `qagents*` branch the binding write gate is **exit 30** (apply-allow license, `data/charters/qagents/session-lifecycle/apply-allow/`), not exit 14.
- **Cross-subproject writes · Stack · Sentinels · Adopted-spec convention** — charters only: session-lifecycle §§ 2.7 / 2.1 + spec-lifecycle § 2.7.
- **CLAUDE.md updates** (charter §§ 2.6 / 2.9): *immediate* (own CLAUDE.md, session branch) + *deferred hints* (`data/claude-updates/<branch>.md` → `/do-claude-updates`).
- **Backward + forward surfaces** (charter § 2.8): `/close` writes `data/summaries/close/<ISO>-<branch>.md` (never overwritten); `data/next-steps/<project>.md` is GENERATED from `ledger.ns_item_event` — write via the `ns-*` verbs only. Owner: `data/next-steps/CLAUDE.md`.

## Model policy — LLM model selection

Complex, long-running work (fan-outs, axiomatization, watchers, debates, overnight research) runs the **top-tier model**; this file never writes the alias. **Four seats hold the value:** interactive — `~/.claude/settings.json` `model` (the client's session picker overrides it); axiomatization — `code/lean_tools/model_floor.py` (one seat, three axes); cron — `run_routine.sh` `routine_policy_model`; lesser-tier sub-agents — their own frontmatter `model:`. Review/optimization fleets carry **no `model:` pins** (they inherit the orchestrator's) — except an out-of-repo `claude -p --add-dir <WT>` seat, which inherits neither the model nor any CLAUDE.md/MEMORY.md, so its caller passes `--model` from the lane's seat (`studying/scripts/dao_seat.py`). A bump edits those seats and re-keys the two value-pinning tests (`t_share_05_model_switch.sh`, `test_model_floor.py`). A budget-killed top-tier routine is **widened, never downgraded** to a lesser tier. Lesser models only where flagged: `sonnet` for bounded cron routines, `haiku` for mechanical closed-set classification and smoke runs. The unit is subscription quota, never API dollars; a lesser tier is a quota choice, not a measured quality floor. **Effort** is a per-lane control (`claude --effort`; the session control interactively), seated beside each lane's model seat; prefer top tier at lower effort to a lesser tier once the lane's own CLAUDE.md records the sweep. **Always bare tier aliases — never a pinned minor, never an older tier.** **Capability floor:** haiku is forbidden for any retained axiomatization artifact. Mechanism detail: memory `project_model_policy_latest_top_tier` + `feedback_predicate_model_opus_not_haiku`.

## Programmatic Claude — Agent SDK lane

This § owns the status: the Agent SDK lane is **parked** (Max-20x SDK credits dropped 2026-06-15); every routine runs the default `claude --print` lane. Standing operator ruling 2026-07-16: never a live dependency, a parked flow target (`ext:agent-sdk-credit`), no contingency planning until an official reversal. Retained code/tests + un-park recipe: `project_agent_sdk_wrapper`. **Second failure mode of the `--print` lane:** the CLI and the desktop app hold SEPARATE credentials — a stale CLI login refuses `claude -p` (exit 1, refusal on STDOUT blaming the organisation) while `claude auth status` reads healthy; it darkens every `ROUTINES` row and all three axes' fact extractors at once. Probe `scripts/model-lane-check.sh`; cure `claude auth login`: `reference_claude_cli_and_desktop_hold_separate_credentials`.

## Shared-data write-lock — `.data-write-lock`

Write `data/` + `financial/` only while holding canonical `.data-write-lock` (one lock, both hubs); cron lanes stage into `pending/` instead (sole direct-writer: the chartered `analyzing:tape-refresh` exception); new shared ledger-like data starts as a store table, never a hand-appended file. Full protocol — the store rule, `pending/` promotion, lock acquisition, and the decide-by-AIM rule: **`data/CLAUDE.md` § 7 (single owner; extracted from here 2026-09-21 by operator ruling, `ns:qagents/230`(b))**.

## Subproject `.claude/` shape (consistent pattern)

Every subproject running Claude Code sessions uses this layout:

- `<sub>/.claude/settings.json` — committed allow/deny + the standard hook set (the one enumeration is `data/claude-settings/sources/baseline.hooks.json`). **Generated, not hand-edited** — edit `data/claude-settings/sources/`, re-run `scripts/claude-settings/build.py` (drift: `--check`). Permission scoping, the allow-glob trap, worktree-root launch-cwd guards: `data/charters/qagents/specs/claude-settings-unification-2026-06-06/SPEC.md` §§ 3/4.5 + `reference_claude_code_allow_glob_no_empty_match`.
- `<sub>/.claude/settings.local.json` — user-local overrides (gitignored); `<sub>/.claude/skills` → symlink to `../../.claude/skills`; `<sub>/.claude/agents/` — optional per-subproject sub-agent definitions.

**A `<sub>/CLAUDE.md` has three readers you did not plan for.** (1) Several are
PUBLISHED (`PUBLISHED_CLAUDE_MD` in `publishing/scripts/sync_mirror.py`) and
gate (1e) excludes that subtree by construction — so **describe a restriction,
never name the restricted file** — and **register a LANE by SHAPE**, keeping its
live state in an unpublished sibling the file points to (`ns:publishing/84`); documenting a bar is exactly the context in
which a barred file gets named. (2) It reaches every subagent in SYSTEM
CONTEXT, unrecorded — on the blind-fanout axes it is cell prompt content
(`ns:accounting/127`). (3) **Trimming a
published one is not a local act** — `sync_mirror.py` `REWRITES` matches
VERBATIM source substrings to strip party names, dockets and live-matter ids,
so any reword unmatches it and the render fails closed at `/publish` time, in
someone else's session. Run `sync_mirror.py --check-rewrites` (read-only) after
such a trim; a DROPPED sentence is safe, a RE-ADDED one is not
self-reporting.

## Skill placement rules

- `./.claude/skills/` — cross-project (auto-loaded via each subproject's `skills` symlink).
- **Subproject-scoped** (not auto-loaded; invoked explicitly): `trading/shared/skills/` (trading-only) + `trading/agents/<pm>/.claude/skills/` (PM-scoped).

## memsearch — semantic memory across qagents sessions

Vendored Claude Code plugin at `lib/memsearch/`; Markdown is the source of truth. Install, version, `qagents patch`es, backend + retained invariants: `lib/memsearch/CLAUDE.md` § "qagents integration". Recall: `memsearch:memory-recall`.

## MCP servers — scoped to subproject via `<sub>/.mcp.json`

`.mcp.json` is subproject-scoped, never repo-rooted (cwd walk-up; rationale + apply pattern: memory `reference_mcp_subproject_scoped_via_file_location`). Today only `explaining/.mcp.json` is wired (`heygen`).

## Federal statutes — ground truth via canonical USC text

All federal statutory citations (predicate specs, Lean axioms/theorems, motion drafts) reference canonical USC markdown vendored under the private filing hub, never hand-pasted. Predicate specs cite by `usc_cite` + relpath; Lean axioms carry a one-line comment naming the statutory section.

## Status hub — `data/status/<sub>.json` (cross-subproject contract)

Every subproject writes a `data/status/<sub>.json` slot matching `StatusEmit` in `@qagents/diagram-kit` (schema owner v0.8.0, `SubprojectId` closed set = 25); `designing/web/` reads every slot at build time and renders `/status`. No cross-subproject TS/Python imports — the JSON hub is the only seam.

- **Whole-slot failure trap (every `/close --status-emit`):** a SINGLE contract-violating field drops the ENTIRE slot to placeholder on prod: `project_diagram_kit`.
- **Public surface — synthetic fixtures only:** every slot renders publicly at `quantapix.com/status/<sub>`, so a producer whose inputs can carry real matter MUST filter to synthetic/allow-listed fixtures (mirror `verifying/server/main.py ALLOWED_EXAMPLE_IDS`) — never real dockets/positions (`<live-matter>_*`). Fleet rule + close-time denylist scan: `reference_operational_axis_public_surface_privacy`.
- **Public surface — no gate reads the PROSE.** A slot's `cardSummary`/`headline` publishes verbatim and is read by NO `/publish` gate and by no signoff grant, so a dated promise, a count or a capability claim there is a public claim its author alone keeps true. **A published forward-looking DATE is a DEBT** — when it moves, the correction names EVERY artifact that carried it, GREPPED not recalled, and the replacement is graded by TIER: a session-summary statement RETIRES a published date but cannot PUBLISH one — assert none rather than a weak one. Why no gate sees it, plus two live instances: `project_publishing_subproject`, `ns:verifying/20`, `ns:evaluating/44`.
- Producer/orchestrator/close-time-emit/pending-aware-cron/KIT_VERSION-lockstep + the eight-surface add-a-subproject sweep: `project_diagram_kit` § "Root § Status hub". Spec: `data/charters/qagents/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`.

## Kit-mount pattern

Sibling-of-Lean-kernel rendering kits ship as vanilla JS into `<sub>/web/public/<kit>/`. **Not all one kit**, and a mount need not be the composed bundle. A mount's `tokens-*.css` + `kit.js` are a **lockstep pair**; guards assert PER SHEET with an anti-vacuity arm; the unit of isolation is per MOUNT, not per file. Rebuild the canonical dist before any re-host-copy, grade staleness by **HASH** never mtime, and grep bundles with `grep -a` (bare `grep` lies `0`). Roster, regen/verify discipline, guard translation, traps: memory `project_proof_graph_kit_mount_pattern`.

## Lean4 axes — three kernels, one architecture

Three orthogonal axes, never sharing domain/ground-truth/consumer: **textual** `proving/` (`legal/uscode/` + the MA primary-law corpus (private mirror); plaintiff v. defendant; → `verifying/`), **numerical** `accounting/` (`financial/parquet/`; bulls v. bears; → `evaluating/`), **operational** `studying/` (git first; `hub/git`; coding v. testing; → `monitoring/`, local-only). Standing rules (i)–(iv) — MECHANIZED names a CALL SITE; a gate change lands only where the graded artifact is AUTHORED; ABSENT needs a failable ENUMERATION; a SEATED ruling buys COMPLIANCE, never corroboration: `project_lean4_three_axis_charter` § "Standing rules for all three axes". Lean 4 is a lesser-known language to the model: axis cell prompts give the cell the Lean 4 language reference (the guide-rail rows). Chief invariant: **no human proof-driving, ever**; the other seven (incl. **proof-of-fire** — every mechanical gate ships a committed known-bad witness): `project_lean4_three_axis_charter`. Spec `data/charters/studying/specs/lean4-charter-2026-06-10/SPEC.md` § 4 + `axiomatize-shared-2026-07-04/`. **Per-axis scope charters:** `data/charters/{studying/operational-axis,proving/textual-axis,accounting/numerical-axis}/CHARTER.md` (studying = neutral steward).

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
