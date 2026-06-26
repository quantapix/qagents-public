# qagents-public — status

_Snapshot: 2026-06-26. Refreshed weekly (Fridays) during the
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

## What changed since the last refresh (2026-06-19)

- **A seventh charter invariant was added to the three-kernel architecture —
  gate uniformity.** The cross-kernel coherency gate (a fixed set of structural
  checks every framework must pass) is now charter law across all three Lean4
  kernels — textual, numerical, and operational — not just a per-kernel
  convenience. Both product kernels landed their coherency gate-parity slices
  this window; the gate is now uniform, which is the same "one rule, swept
  across every surface in lockstep" property the conventions in this repo
  exist to publish.
- **A second clearance gate was charted — a financial sign-off, orthogonal to
  the litigation-safety gate.** Any public surface that evaluates or implies a
  financial decision now requires an explicit financially-cleared sign-off from
  the evaluator subproject (advised by the financial kernel), in addition to —
  not instead of — the existing litigation-safety clearance. Where both apply,
  both must clear. This is the AI-checking-AI gate pattern (theme 7) widened to
  a second domain.
- **Both product kernels deepened their hierarchical-predicate decomposition.**
  The legal kernel ran a decompose-by-default scale wave with a load-bearing
  oracle guard (search automation may never discharge an agreement lemma) and
  added an eighth golden framework; the financial kernel reached sibling-parity
  on depth, added a third hierarchical framework, and promoted further
  per-sector slices. Detail lives in the legal-domain and financial-domain
  public repos.
- **The verifier's replay surface narrowed to synthetic examples only.** Under
  the thesis floor, the public verifier app now replays only synthetic fixtures
  — no run drawn from any live matter is reachable, and the static public build
  is stricter still (one synthetic worked example). A leak-guard test forces the
  excluded ids to 404.
- **The release pipeline moved all GitHub work behind a single tool.** Repo
  content, metadata (description/homepage/topics), existence, and verification
  now go through one gh-centric arm; a repo description is treated as public OG
  copy and rides the same redaction + thesis gate as README prose.

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
