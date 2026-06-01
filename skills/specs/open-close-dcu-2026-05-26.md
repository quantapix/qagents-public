# open / close / do-claude-updates — session-lifecycle spec

**Status:** adopted
**Date:** 2026-05-26
**Scope:** qagents-wide (the session-lifecycle skills + every subproject's
`.claude/settings.json`)
**Tests:** a companion bash suite (`-tests/`)

_Redacted public rendering. Operator absolute paths are genericized to
`<repo>` (the canonical checkout on `main`) and `<wt>` (the per-session
worktree root); the agent-memory dir is `<memory>`. The engineering content
— phase sequences, exit-code contracts, hook behavior, the glob-matcher rule
— is preserved verbatim, because that is the methodology this repo
publishes._

This spec folds a chain of five predecessor specs + one stale diagnostic
into a single contract and retires the predecessors (git log preserves
them).

---

## 1. Motivation

Single-maintainer git/worktree discipline tightened so that every session
starts with `/open <project>` and ends with `/close`. The session's branch
is the write-lock; closing rolls work back toward `main`. Memory writes and
CLAUDE.md updates ride on the close, not on ad-hoc commits. Cross-subproject
implications stage as hints for a later `/do-claude-updates` flush. The
whole shape ends up on `main` with Claude-authored commit messages and zero
manual git plumbing.

Five contracts the consolidated triad MUST satisfy:

1. **Three-layer model** — spec → mechanics (`scripts/{open,close,dcu}.sh`)
   → orchestrator (the SKILL.md files). Mechanics is the single source of
   truth for executable phases; SKILL.md carries only judgment steps + script
   invocations.
2. **Uniform footer** — every skill prints `<project> <verb> complete`
   followed by a markdown summary table, and writes the same content under
   `data/summaries/<verb>/`.
3. **Zero-prompt noop close** — `/open <sub>` followed immediately by
   `/close <sub>` fires zero permission prompts, leaves the git graph
   untouched, and writes only the close-footer summary file.
4. **Forward-only next-steps** — every project carries one
   `data/next-steps/<project>.md` slot listing what's left; resolution detail
   belongs in the append-only close summaries.
5. **Canonical-edit lock hook** — while a `<sub>` branch is held, edits to
   the canonical `<sub>/` tree are hard-blocked. The branch IS the
   write-lock; canonical edits would race it.

The lock is conventional, not enforced cross-process — branch-presence
checks guard the entry path. Acceptable for solo use; the canonical-edit
hook adds in-process enforcement.

## 2. Vocabulary

| Term | Definition |
|---|---|
| **canonical** | the repo checked out on `main`. The merge target. |
| **worktree** | a physical per-session checkout under the worktree root. |
| **agent-memory** | the separate git repo holding the memory topic files. |
| **project** | `qagents` (whole-repo) or a subproject slug. |
| **lock branch** | a branch named exactly `<project>` (or `<project>-N`). Branch existence IS the held lock. |
| **stack** | a linear chain `xxx → xxx-2 → xxx-3 → …`, each forked off its predecessor. |
| **sentinels** | gitignored root-anchored files (`.dot-claude-write-lock`, `.data-write-lock`); existence = held lock. |

## 3. Three-layer model

| Layer | Role |
|---|---|
| **Spec** | the design contract — names every guarantee, stop-and-ask case, exit code. Edited only on intentional contract changes. |
| **Mechanics** (`scripts/{open,close,dcu}.sh` + `scripts/lib/footer.sh`) | single source of truth for executable phases. All compound-bash, sweep loops, regex filters, sentinel handling, log routing. Subcommand-shaped so each step matches an allow-list entry. |
| **Orchestrator** (the SKILL.md files) | one or two script calls per phase, interleaved with judgment steps an LLM is best placed to do (summary, memory, CLAUDE.md edits, hints). Carries the per-skill bash-discipline + stop-and-ask table. |

### 3.1 Bash discipline (load-bearing)

Failing any of these re-introduces permission-prompt storms even with a
fully populated allow-list:

- **Absolute path to scripts** — never a relative form; each form requires a
  separate matcher.
- **No compound bash** — no `&&`, `||`, `;`, or `|` (including piping to
  `tail`). Read log files via the Read tool instead.
- **No `cd <abs-path> && git …`** — trips a hardcoded foreign-directory
  security prompt allow-listing can't silence. Use `git -C <abs-path> …`.
- **No raw re-verify after `--pre` ran** — `--pre` already wrote the diff +
  commit list to its log.
- **No `find` for known absolute paths.**
- **Temp files in `<wt>/pending/tmp/`** — gitignored, inside the worktree;
  the OS `/tmp/` is outside the allowed write boundary.

The structural fix for prompt-storms is "every routine compound becomes a
script subcommand" — broadening per-command allow-list entries alone is not
enough.

## 4. Uniform output pattern

Every skill ends, on success, with the same two-block footer:
`<project> <verb> complete` + a summary table (Branch / Target / Worktree /
Commits / Paths touched / Time), followed by an **Outstanding
(carry-forward)** block that is never omitted (render `(none)` for an empty
set). Each block is also captured under `data/summaries/<verb>/`
(`<YYYY-MM-DD>T<HHMM>-<branch>.md`, local time, minute precision). For
`close`, the LLM's narrative summary lives above a separator; the footer is
appended below by the script. `--to-main` emits a final leaf-named footer
(user-visible) plus silent per-hop footers at each intermediate level
(forensic).

## 5. Per-skill mechanics + judgment

### 5.1 `/open <project>`

Pre-checks (mechanical): project is known; canonical is a git repo on
`main`; canonical dirty state is classified (cron-only state auto-swept +
committed with a dated message, real dirty → exit 12); orphan worktrees
swept only if every file matches the residue allow-list; warn (non-blocking)
on stale `pending/` + a stale data-write-lock; lock-compat refusal
(whole-repo vs subproject); compute the new branch + parent (smallest free
`<project>-N`). Provisioning: `git worktree add`; symlink the venv +
scope-gated env files + **materialize every `.worktree-links` manifest**
(§ 8.14); `pnpm install` if a workspace member; **next-steps briefing read**
(render the slot rows for the footer; whole-repo reads only its own slot to
avoid context bloat); print the entry command; print the footer + write the
summary file.

Exit codes: 10 lock-conflict · 11 unknown-project · 12 real-dirty · 13
not-a-repo · 20 unknown.

### 5.2 `/close [<branch>] [--to-main]`

**Phase 0a — noop short-circuit** (`--noop-check`): exit 0 (noop — zero
commits ahead AND clean worktree) skips Phases 1–6 entirely and jumps to
teardown + verify; the footer is the entire close artifact. Exit 1 →
proceed.

**Phase 1 — pre-flight** (`--pre`): resolve worktree; stack-top check;
dirty classification both sides (sweep cron-only state, refuse on real);
inspect the merge (commits + diffstat → log); hub-overlap scan (HIGH-risk
parallel writes → exit 13); cross-subproject scope scan (foreign writes →
exit 14; memsearch state skipped); CLAUDE.md size discipline (warn at the
soft cap, exit 16 at the hard cap); gitignored-binary rescue scan (exit 15,
honoring per-subproject `.close-protected-paths` overlays).

**Phase 2 — session summary** (judgment): save the LLM-authored narrative
(what / why / learned, not a transcript).

**Phase 3 — agent-memory update** (judgment): acquire the dot-claude
sentinel; update memories per the index discipline (watch the index size —
it truncates around a fixed line count at session start); commit + release
via the script.

**Phase 4 — CLAUDE.md updates** (judgment, two paths): (4a) immediate —
re-read every touched CLAUDE.md, fix stale phrasings, prefer
trim/consolidate near the cap; (4b) broader-cascade hints — write a
free-form hint file only if there are genuine cross-subproject implications.

**Phase 5 — mandatory status emit** (`--status-emit`): regenerate the
status-hub slot; whole-repo fans out. Exit 42/43/44.

**Phase 5.5 — mandatory next-steps gate** (`--next-steps`, per § 6): scan
merge-range commit messages for item cites; verify each cited item is
deleted from the slot. Exit 24/25; skipped silently when no items cited.

**Phase 6 — commit session work** (judgment writes the message): commit via
the script (returns nothing-to-commit if clean).

**Phase 7 — merge + teardown** (`--finish [--to-main]`): the memsearch stash
dance (only if needed); merge `--ff-only` → fallback `--no-ff`; auto-resolve
memsearch-only conflicts to the richer side; unlink symlinks; `worktree
remove` + `branch -d` + `prune`; cascade up the stack with a per-hop footer
under `--to-main`.

**Phase 8 — verify + footer** (`--verify <target>`): post-close inspection
(last commit, branch list, worktree list, orphan-dir scan).

Exit codes: 10 stack-top · 11 resolve · 12 dirty-classify · 13 hub-overlap ·
14 cross-subproject · 15 rescue · 16 claude-md-size · 17 merge · 18
stash-pop · 19 sentinel · 21 branch-d · 22 commit-memory · 24/25 next-steps ·
42–44 status-emit · 20 unknown.

### 5.3 `/do-claude-updates` (alias `/dcu`)

Manual flush — runs from canonical on `main`, clean, no args. Pre-flight
(`--pre`): canonical clean; queue non-empty; lock-compat (no session
branches); provision a dedicated worktree. Then (judgment): read every
CLAUDE.md in the worktree (note sizes); for each hint file, decide
whether/where it applies (zero, one, or several edits; "skip with
justification" is valid), apply surgically, **delete the consumed hint file
regardless** ("consumed" = "reviewed in full context"), and commit per hint.
Malformed hints stay on disk and surface in the report. Then merge +
teardown + footer. Exit codes: 10 lock · 12 canonical · 13 queue-empty · 17
merge · 20 unknown. The flush lane sets a bypass env var so the
canonical-edit hook permits writes inside its own worktree at merge time.

## 6. next-steps mandate (close-time gate)

Each project carries one `data/next-steps/<project>.md` slot, with sections
A (owned, ready now), B (owned, gated on external), C (cross-cutting with
detail insight — transitional).

**Forward-only rule.** Items are **deleted** when resolved — never archived
in a trailing "Resolved" section. Resolution detail lives in the append-only
close summaries. The two surfaces have orthogonal jobs: the slot is forward
("what's left", overwritten in place); the close summaries are backward
("what got done", append-only).

**Numbering discipline.** Items numbered 1..N monotonically across all
sections; **do not renumber survivors on deletion** — numbers anchor
commit-message cites, so gaps are load-bearing.

**Cite syntax + gate.** The gate scans the merge range for case-insensitive
cites of the form `(closes|resolves|completes)? (next-steps item|ns-item)
N(, M)*` (with an optional `(data/next-steps/<other>.md)` paren-override);
bare `item N` is rejected. The cited set is the union across the range. The
gate verifies each cited item is absent at the branch tip; missing
deletions → exit 25; a missing slot file when items are cited → exit 24; no
cites → skip with exit 0. Whole-repo branches default to the whole-repo
slot.

## 7. Per-subproject settings — canonical zero-prompt block

Every `<sub>/.claude/settings.json` carries a verbatim allow-list block
(paths substituted per subproject). It is the single source of truth for
"what the lifecycle scripts need". The full block lists, per subproject, the
script entry points, the Write/Edit slots for summaries / hints / temp
files, the read-only git verbs, and the broad Read coverage — each in both a
literal and a stacked-suffix (`<sub>-*`) variant.

### 7.1–7.2 The glob-matcher rule (load-bearing)

In allow-list path patterns, `*` matches **one-or-more** chars within a
segment, **not zero**. So any rule of shape `<prefix>*/<…>` silently misses
the bare-`<prefix>` case — when both a literal and a stacked-suffix variant
exist (e.g. `managing` and `managing-2`), list them as **two** entries. The
same rule applies to `git -C * <verb>` — `*` does not match path segments
containing slashes, so parent paths are listed explicitly. A representative
slice (paths shown generically):

```jsonc
// script entry points — separate matchers per path variation
"Bash(<repo>/scripts/close.sh:*)",
"Bash(<wt>/<sub>/scripts/close.sh:*)",
"Bash(<wt>/<sub>-*/scripts/close.sh:*)",
// Write slots — literal + stacked-suffix per the glob rule
"Write(<wt>/<sub>/data/summaries/close/**)",
"Write(<wt>/<sub>-*/data/summaries/close/**)",
"Write(<wt>/<sub>/pending/tmp/**)",
// read-only git verbs (the bare-verb form matches any args)
"Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)",
"Bash(git worktree:*)", "Bash(git rev-list:*)",
// explicit parent paths for the -C form
"Bash(git -C <repo>:*)", "Bash(git -C <wt>/<sub>:*)"
```

### 7.3 Observe-only subprojects

The watcher + its adversarial sibling + the donation subproject carry an
additional **deny** block (`git push` / `commit` / `reset` / `checkout` /
`rm` / `mv`, plus subproject-specific extras). The deny doesn't block the
close script's *internal* commit (subprocess opacity — only direct LLM tool
calls are gated), so the close script remains the sanctioned commit lane.

### 7.4 What the block omits (intentional)

No `rm` allow; no relative-path entries; no global `Write`; no `find` at the
LLM-tool layer.

## 8. Cross-cutting subsystems

- **8.1 Cron-fired dirty state.** A scheduler keeps firing the watcher +
  trading routines against canonical during sessions; the predictable churn
  (status artifacts, portfolios, journals, memsearch daily logs, watcher
  outputs) is auto-swept with a dated commit at both `/open` and `/close`;
  real dirty stops and asks.
- **8.2 Canonical-edit lock hook.** A `PreToolUse(Edit|Write)` hook resolves
  the target's absolute path; if it's under a canonical `<sub>/` tree (not
  under the worktree root) and a matching lock branch exists, it hard-blocks.
  Exception lanes honor a bypass env var (the flush lane at merge time, the
  optimization lane under a whole-repo lock, cron lanes from canonical).
  Subproject settings must carry the hook too — subproject sessions don't
  load root settings.
- **8.3 Rescue-scan false-positive filter.** The gitignored-binary scan
  skips symlinks-into-canonical (the venv, env files, every `.worktree-links`
  target), the per-worktree settings override, and the temp buffer. Exact
  list, not a heuristic.
- **8.4 Memsearch hooks.** Worktree-side dirty pre-cleaned before teardown;
  canonical-side dirty scoped-stashed before merge + popped after; merge
  conflicts on a memsearch daily log auto-resolved to the richer side
  (non-trivial divergence → exit 18); cross-subproject scope skips any
  memsearch path.
- **8.5 `pending/tmp/`** — in-worktree, gitignored buffer for commit-message
  bodies authored before a script invocation.
- **8.6 Date-grouped logs** under `pending/logs/<date>/`, filename sanitized.
- **8.7 CLAUDE.md size discipline** — warn at the soft cap, fail at the hard
  cap, counted on every CLAUDE.md in the merge diff. The optimization
  companion addresses the upstream problem: keep CLAUDE.mds shrinking.
- **8.8 Cross-subproject scope allowlist** — own dir + named root files +
  the shared hubs; re-run inside `--finish` so an earlier exit on an
  unrelated phase can't slip foreign writes through.
- **8.10 Lock semantics during in-flight close** — the branch isn't deleted
  until teardown, so the lock is held for the entire duration of `/close`.
- **8.11 venv symlink staging** — the commit step excludes the venv symlink
  from a bulk add.
- **8.12 Orphan-worktree sweep at `/open`** — only when the entire dir
  matches the residue allow-list; anything else is logged and left.
- **8.13 Per-subproject `.close-protected-paths`** — declare gitignored
  paths critical enough to surface in the rescue scan with recovery
  procedures; the backstop for content created in a real worktree dir before
  canonical has it.
- **8.14 Canonical-shared gitignored content — `.worktree-links` manifests.**
  `git worktree add` never materializes gitignored paths, and `worktree
  remove` wipes any a worktree created locally. Large, regenerable,
  **canonical-only ground truth** (market parquet, the U.S. Code corpus,
  render outputs, Blender renders, the CDN video mirror) is declared in a
  per-subproject manifest (one glob per line, no globstar — the shell has
  none) and symlinked into **every** worktree at `/open`, teardown-safe by
  construction. A dir is symlinkable **iff** it holds no tracked files
  (otherwise the checkout is a real dir and the symlink nests inside it). The
  matching gitignore pattern MUST be **no-trailing-slash** — in a worktree
  the path is a *symlink*, and a directory-only (`dir/`) or file-leaf pattern
  never matches a symlink, so the symlink would surface as untracked, get
  swept into the work commit, trip the cross-subproject gate, and block
  teardown. Migrating previously-tracked content is delicate: untrack + merge
  deletes canonical's working copy, so the sequence is gitignore +
  `git rm --cached` on the branch → preserve copies to canonical `pending/`
  → close to main → restore from `pending/` to the now-gitignored paths.

## 9. Reference data

The known-projects list, the workspace members that need `pnpm install` at
open time, and the hub paths used for shared-write conflict detection
(HIGH-risk: the portfolios + reports hubs → exit 13; routine: the filing hub
+ a few shared parquet/markdown paths → WARN).

## 10. Phases

- **[shipped]** `2026-05-26` Phase 0 — spec consolidation; five predecessor
  specs + one stale diagnostic + their test dirs retired (history in git
  log); cross-refs swept.
- **[planned]** Phase 1 — an optimization-pass walk over the next-steps
  slots (three staleness flavors: by-resolution, by-supersession, by-
  ownership-handoff).
- **[planned]** Phase 2 — the watcher's spec audit grows an owner column +
  filter; section C of each next-steps slot dissolves on adoption.
- **[deferred]** Phase 3 — an optional report-only mode that re-emits an old
  session's footer from the logs (reason: not load-bearing; defer until a
  real need surfaces).
- **[shipped]** `2026-05-31` Phase 4 — canonical-shared gitignored content
  via `.worktree-links` manifests (§ 8.14); generalized the hardcoded
  parquet symlink block across all projects; the now-inert sidecar-leak
  guard retired.

## 11. Acceptance criteria

Eighteen criteria, each mapped to a bash test: spec hygiene; three-layer
model preserved; uniform footer; per-verb summary subdirs; stop-and-ask
exit-code coverage; CLAUDE.md size discipline; the noop short-circuit
subcommand; the canonical-edit hook present + wired; the next-steps cite
parse + gate exit codes + whole-repo target; the `/open` briefing read; the
slot contract doc + the audit-table row; predecessors retired; the
`.worktree-links` materialization (glob-expansion, skip-unmatched, no
globstar); the sidecar-leak guard retired.
