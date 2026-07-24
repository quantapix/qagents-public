# qagents-public — status

_Snapshot: 2026-07-24. Refreshed weekly (Fridays) during the
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
- The `claude-md/` graph widened on the 2026-07-20 refresh from the
  product-focused core to the full publishable set: the local-only analytics
  app, the operational-axis kernel, both public sites' authoring surfaces, the
  video-production chain, and the adversarial sibling all now publish their
  rule-sets. Three subprojects remain deferred and one is an open editorial
  call; the subtree README names each and why.

## What changed since the last refresh (2026-07-10)

- **A second Rust authoring surface was minted.** The session-lifecycle
  mechanics layer finished its phased migration out of shell into a native
  binary — each verb ported, dual-run against the original on an exhaustive
  matrix, cut over behind a path-stable shim, and the superseded shell
  libraries deleted in one commit once the last caller was gone. A second
  crate now covers the context-transformation layer: injection, conservative
  output shortening, and semantic recall. Two surfaces, chartered; a third
  would need its own ruling.
- **Cross-machine session lifecycle became symmetric.** Exactly one machine
  merges per cycle, and which one is decided by the verb being run rather than
  by the hardware. Everything else packages, pushes a namespaced topic ref, and
  fast-forwards. Memory flows one direction only. The replaced model had worked
  only by accident.
- **Gating state became machine-readable.** The dependency graph across every
  subproject's forward-looking slot is now assembled on demand from structured
  clauses instead of read out of prose, with an explicit registry for external
  blockers and a parked class excluded from bottleneck metrics.
- **Ledger-shaped shared data moved to a store.** Surfaces with many appenders
  now start as a table with a single writer rendering a git projection, rather
  than as another hand-appended shared file. The forward-looking slots
  themselves were the first cutover.
- **The kernel graphing mount finished a constellation-wide rename**, and one
  site dropped out as a consumer entirely after its remaining mount was found
  dormant and removed rather than carried. Three consumers remain.
- **All three formal kernels ran waves in-window** — the textual axis
  re-earning chapter after chapter under a stricter evidence rule, the
  numerical axis holding its frontier under freshly gated market-tape
  provenance checks, and the operational axis proving its own
  context-operations conventions. Detail lives in the product repos.

## What's not populated, and why that is a ruling

- **`memory/`** and **`memsearch/`** carry their READMEs and nothing else. That
  is a decision, not a backlog: an entry whose *subject* is a redaction bar
  cannot be scrubbed of it and stay useful, so those mirrors will only ever be
  populated from a curated opt-in allow-list — never a deny-sweep over the whole
  tree. Until that allow-list is authored, the correct size of these subtrees is
  zero.

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

Two additional bars are enforced as fail-closed pairs rather than single greps:
each has a content scanner over file bytes *and* a path scanner over file names,
because a barred token in a path renders publicly in the repo tree without ever
appearing inside a file. Both abort the publish rather than silently dropping
the offending file. As of 2026-07-24 no contact email appears on any public
surface in this organisation; the organisation page is the sole contact channel,
so questions are answered in public.

## Cadence

Weekly (Fridays) from the `CLAUDE.md` graph and the lifecycle skills + their
specs. The memory topic-file tree and the recall memos are allow-list pending
(see above), not on a refresh clock.
Re-rankings, new subprojects, and new cross-subproject conventions land as ordinary
diffs; the commit log is the change record.
