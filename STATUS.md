# qagents-public — status

_Snapshot: 2026-06-05. Refreshed weekly (Fridays) during the
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
  conventions) + the subproject mirrors (the two Lean kernels, the
  market-inspection + portfolio-management surfaces, the two app shells, the
  infrastructure surface, the constellation watcher, the Lean4-lattice graphing
  surface, and the release subproject itself) + the three shared-hub convention
  docs. See [`claude-md/README.md`](./claude-md/README.md) for exactly which
  subprojects publish and which are deferred.
- **`skills/`** — the four session-lifecycle + optimization skills (`open`,
  `close`, `do-claude-updates`, `do-claude-optimizations`) as redacted SKILL.md
  bodies, plus the adopted specs they implement. These are the executable shape of
  the worktree-as-lock discipline (theme 4) and the context-window-optimization
  discipline (theme 5) the README describes.

## What changed since the last refresh (2026-06-01)

- **Both formal kernels now pin the same Lean toolchain in lockstep.** The study
  surface flagged a drift between the two kernels; both were re-pinned to a single
  current-stable Lean release. The cloud build image now serves both kernels with
  no per-build toolchain switch. The redacted `claude-md/` mirrors for the two
  kernels and the infrastructure surface reflect the unified pin.
- **The financial kernel's per-wave cell decomposition widened from five axes to
  seven** (adding an instrument-risk axis and a liquidity axis to the default
  fan-out). This is a refinement of how each wave is sliced for parallel evaluation;
  the five published frameworks (TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN)
  are unchanged. Detail lives in the financial-domain public repo.
- **The legal kernel added a fourth framework golden** through the U.S.-Code
  axiomatization program's manual fan-out lane, held in sandbox pending promotion.
  This is the contributor-facing program described in the README's donation-drive
  section; detail lives in the legal-domain public repo.
- **The public-org deploy bridge is now version-controlled.** The push wrapper that
  syncs this staging tree out to the public org was vendored into the infrastructure
  subproject's scripts directory (out of a former standalone setup repo), so the
  whole release path is now under source control and redaction-gated end to end.

## What's scaffolded (fills in on later refreshes)

- **`memory/`** — the redacted auto-memory topic-file mirror. README in place;
  topic files land on a later weekly refresh.
- **`memsearch/`** — curated, opt-in daily memos. README in place; memos land on
  the quarterly batch sweep.
- The remaining publishable subproject `CLAUDE.md` mirrors (the video, site, study,
  and meta-observer surfaces).

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
