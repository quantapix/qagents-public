# qagents-public — status

_Snapshot: 2026-07-31. Refreshed weekly (Fridays) during the
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
- The `claude-md/` graph refreshed against a heavy week: twenty of the
  twenty-one published rule-sets changed, several substantially (the
  constellation watcher, the market-inspection surface, the kernel graphing
  surface, and the operational-axis kernel most of all).

## What changed since the last refresh (2026-07-24)

- **A twenty-fifth subproject was created.** Deep agent-based market
  simulation: an engine plus a local on-device model-fit lane and a local-only
  UI that is never deployed. It reads promoted factor artifacts under a written
  consumer contract rather than importing anything, and it is generative-
  descriptive by charter — it models market structure, it does not forecast.
  It carries the financial signoff floor from its first commit rather than
  acquiring one later.
- **The formal-kernel charter went from seven invariants to eight.** The new one
  is proof-of-fire: every mechanical gate must ship a committed known-bad
  witness that it demonstrably rejects. A gate that has never been observed to
  fire is not evidence, however green it reads. Several existing gates were
  re-examined against it in the same window.
- **All three kernels ran waves.** The textual axis promoted two more statutory
  chapters, one of them a second blind re-slice of a chapter it had already
  covered, under a stricter evidence rule. The numerical axis landed a
  tape-of-record pin — a host running against a stale market tape now fails
  loudly instead of quietly comparing against a different one — and its
  coverage rows gained a git-visible corpus identity. The operational axis
  completed a four-theorem set about its own context operations.
- **The launch-directory permission hole was closed.** A session launched from
  an unexpected working directory could previously miss the deny rules that
  scope its writes; the deny mirror and the agent-definition link are now
  provisioned together when the session is created.
- **The recall lane was repaired.** The vendored plugin was re-vendored and its
  local patch set re-applied; one patch fixed a root-derivation bug that had
  left semantic recall silently returning nothing. Writers had moved to a new
  root convention months earlier and the reader had not followed — the lane was
  green the whole time.
- **The context-optimization pass shrank its own inputs.** A deferred-hint flush
  consumed seven queued cross-subproject hint files in one pass.

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

Three additional bars are enforced as fail-closed pairs rather than single
greps: a bar on one collateral docket family, a bar on session-multiplexer local
state (which carries branch names, transcript paths, and prompt previews), and a
bar on contact addresses. Each has a content scanner over file bytes *and* a
path scanner over file names, because a barred token in a path renders publicly
in the repo tree without ever appearing inside a file. All three abort the
publish rather than silently dropping the offending file. Each ships its own
pinned regression test — the gates are themselves subject to the proof-of-fire
rule described above. As of 2026-07-24 no contact email appears on any public
surface in this organisation; the organisation page is the sole contact channel,
so questions are answered in public. A collateral federal-appeal docket number
was added to the hard-blocked set on 2026-07-31; the spelled-out court name
without the number remains publishable.

## Cadence

Weekly (Fridays) from the `CLAUDE.md` graph and the lifecycle skills + their
specs. The memory topic-file tree and the recall memos are allow-list pending
(see above), not on a refresh clock.
Re-rankings, new subprojects, and new cross-subproject conventions land as ordinary
diffs; the commit log is the change record.
