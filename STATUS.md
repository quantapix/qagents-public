# qagents-public — status

_Snapshot: 2026-07-10. Refreshed weekly (Fridays) during the
2026-06-01 → 2026-12-01 drive window._

This is the release-narrative status of the umbrella methodology repo: what the
current cut carries, what's deferred, and the refresh cadence. It is a companion
to the [README](./README.md), not a substitute.

## Overall

**Product-focused cut, steadily widening.** This repo publishes the redacted
AI-assistant working context behind the practice — the `CLAUDE.md` rule-set, the
session-lifecycle skills, and (filling in) the memory + recall trees. The current
round ships the redacted `CLAUDE.md` graph behind the two shipping products plus
the core infrastructure surfaces; the memory and recall trees fill in on weekly
refreshes.

## What's live this round

- **`claude-md/`** — the redacted `CLAUDE.md` graph: `root.md` (cross-subproject
  conventions) + the subproject mirrors (the formal kernels, the
  market-inspection + portfolio-management surfaces, the two app shells, the
  infrastructure surface, the constellation watcher, the kernel graphing
  surface, and the release subproject itself) + the three shared-hub convention
  docs. See [`claude-md/README.md`](./claude-md/README.md) for exactly which
  subprojects publish and which are deferred.
- **`skills/`** — the four session-lifecycle + optimization skills (`open`,
  `close`, `do-claude-updates`, `do-claude-optimizations`) as redacted SKILL.md
  bodies, plus the adopted specs they implement. These are the executable shape of
  the worktree-as-lock discipline (theme 4) and the context-window-optimization
  discipline (theme 5) the README describes.

## What changed since the last refresh (2026-06-26)

- **The three formal kernels bumped their shared toolchain in lockstep.** All
  three Lean kernels moved to the same next toolchain point-release in one
  coordinated change, with every example proof replayed green — the concrete
  payoff of pinning one toolchain across three axes so a single cloud build
  image serves them with no per-build switch.
- **The clearance sign-off generalized into a registry-backed framework, and a
  third gate was added.** What was a single financial sign-off last round is
  now a generic, machine-checked clearance machinery: each gate has one
  sole-grantor subproject and writes a dated, re-verifiable attestation, and a
  push whose in-scope gate lacks a record is refused. A third gate —
  operational-privacy — joined the litigation-safety and financial gates.
- **The release pipeline made the CDN upload a gated public push.** Uploading a
  video cut to the content-delivery bucket is now treated as the first public
  push, gated identically to the channel upload — closing a gap where an object
  could be world-reachable by URL before its payload cleared sign-off.
- **Both product kernels continued hierarchical-predicate decomposition.**
  Depth increased across several frameworks on both the legal and financial
  sides, with new per-sector slices promoted; detail lives in the two
  product public repos.
- **One watcher subproject retired its programmatic (SDK) routines**, folding
  back to the interactive lane — consistent with the paused SDK credit pool.

## What's scaffolded (fills in on later refreshes)

- **`memory/`** — the redacted auto-memory topic-file mirror. README in place;
  topic files land on a later weekly refresh.
- **`memsearch/`** — curated, opt-in daily memos. README in place; memos land on
  the quarterly batch sweep.
- The remaining publishable subproject `CLAUDE.md` mirrors (the video, site,
  study, and meta-observer surfaces).

## What's excluded (never published)

The litigation-domain surfaces (the appeals / pleading / filing-hub `CLAUDE.md`s) —
too easy for federal-record drift, even redacted. Public-facing legal material
routes through the femfas.net site instead.

## Redaction posture

Operator home paths are genericized; AWS account / resource / device identifiers,
case-specific example IDs, and host-specific identifiers are stripped. A live
markdown redaction gate sweeps every `*.md` in the candidate tree before any push —
a HARD blocklist hit aborts the compile and push, and an empty candidate tree is a
failure, not a vacuous pass. The engineering content — conventions, exit-code
contracts, hook behavior, phase ledgers — is preserved, because that is the
methodology this repo exists to publish.

## Cadence

Weekly (Fridays) from four private sources — the `CLAUDE.md` graph, the lifecycle
skills + their specs, the memory topic-file tree, and selected recall memos.
Re-rankings, new subprojects, and new cross-subproject conventions land as ordinary
diffs; the commit log is the change record.
