# qagents-public — status

_Snapshot: 2026-06-01. Refreshed weekly (Fridays) during the
2026-06-01 → 2026-12-01 drive window._

This is the release-narrative status of the umbrella methodology repo: what
the first cut carries, what's deferred, and the refresh cadence. It is a
companion to the [README](./README.md), not a substitute.

## Overall

**First cut, product-focused.** This repo publishes the redacted
AI-assistant working context behind the practice — the `CLAUDE.md` rule-set,
the session-lifecycle skills, and (later) the memory + recall trees. This
round ships the subset behind the two shipping products plus the core
infrastructure; the rest of the graph fills in on weekly refreshes.

## What's live this round

- **`claude-md/`** — the redacted CLAUDE.md graph: `root.md` (cross-subproject
  conventions) + nine subproject mirrors (the two Lean kernels, the
  market-inspection + portfolio-management surfaces, the two app shells, the
  infrastructure surface, the constellation watcher, and the release
  subproject itself) + the three shared-hub convention docs. See
  [`claude-md/README.md`](./claude-md/README.md) for exactly which
  subprojects publish and which are deferred.
- **`skills/`** — the four session-lifecycle + optimization skills (`open`,
  `close`, `do-claude-updates`, `do-claude-optimizations`) as redacted
  SKILL.md bodies, plus the two adopted specs they implement
  (`open-close-dcu-*`, `dco-*`). These are the executable shape of the
  worktree-as-lock discipline (theme 4) and the context-window-optimization
  discipline (theme 5) the README describes.

## What's scaffolded (fills in on later refreshes)

- **`memory/`** — the redacted auto-memory topic-file mirror. README in
  place; topic files land on a later weekly refresh.
- **`memsearch/`** — curated, opt-in daily memos. README in place; memos land
  on the quarterly batch sweep.
- The remaining publishable subproject CLAUDE.md mirrors (the video, site,
  study, and meta-observer surfaces).

## What's excluded (never published)

The litigation-domain surfaces (the appeals / pleading / filing-hub
CLAUDE.mds) — too easy for federal-record drift, even redacted. Public-facing
legal material routes through the femfas.net site instead.

## Redaction posture

Operator home paths are genericized to `<repo>` / `<wt>` / `<memory>`; AWS
account / resource / device identifiers, case-specific example IDs, and
host-specific identifiers are stripped. The engineering content — conventions,
exit-code contracts, hook behavior, phase ledgers — is preserved, because
that is the methodology this repo exists to publish. A redaction gate runs
over the candidate tree before any push.

## Cadence

Weekly (Fridays) from four private sources — the CLAUDE.md graph, the
lifecycle skills + their specs, the memory topic-file tree, and selected
recall memos. Re-rankings, new subprojects, and new cross-subproject
conventions land as ordinary diffs; the commit log is the change record.
