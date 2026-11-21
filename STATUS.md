# qagents-public — status

_Snapshot: 2026-11-21. Refreshed per release run during the
2026-06-01 → 2026-12-01 drive window._

This is the release-narrative status of the umbrella methodology repo: what the
current cut carries, what's deferred, and the refresh cadence. It is a companion
to the [README](./README.md), not a substitute.

## Overall

**Product-focused cut, steadily widening.** This repo publishes the redacted
AI-assistant working context behind the practice — the `CLAUDE.md` rule-set, the
session-lifecycle skills, and the adopted contracts behind them. The current
round ships the redacted `CLAUDE.md` graph plus the lifecycle skills; the memory
and recall trees are allow-list pending and are on no refresh clock at all —
that is a ruling, not a backlog, and it is stated in full below.

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
  bodies, plus condensed renders of the charters they implement. These are the executable shape of
  the worktree-as-lock discipline (theme 4) and the context-window-optimization
  discipline (theme 5) the README describes.
- The `claude-md/` graph widened on the 2026-07-20 refresh from the
  product-focused core to the full publishable set: the local-only analytics
  app, the operational-axis kernel, both public sites' authoring surfaces, the
  video-production chain, and the adversarial sibling all now publish their
  rule-sets. Two subprojects remain deferred, one is an open editorial call, and three
  have not been assessed; the subtree README names each and why.
- The `claude-md/` graph re-renders from the private rule-sets on refresh; the commit diff is the change record.

## What changed since the 2026-11-13 refresh

- **The operational kernel's fingerprint counts tracked files only.** Inside a
  work tree, the file population that hashes the kernel is now the
  version-controlled sources under the kernel package. A file the version-control
  system does not track no longer enters the hash, so it cannot move the
  fingerprint away from its recorded stamp.
- **Dated review narratives are never removed by hand.** The reaper archives each
  one and runs a citation check before it goes. A narrative whose verdict has been
  overtaken is marked superseded in place instead of being deleted.
- **The watcher's ready queue reads facts per instance first.** An instance's own
  start or outcome line serves that instance alone. A shared line serves only the
  instances that carry none of their own, so it is filed only when every instance
  shares the fact.

## Earlier: what changed in the 2026-11-13 refresh

- **Two earlier statements here were wrong, and are corrected rather than
  edited in place.** The 2026-10-23 entry said a session bound to a new lock
  has its file writes refused anywhere in another lock's worktree. That holds
  for the assistant's own file tools only. A write made through a shell
  command (an in-place edit, a redirect, a copy or a move) is not seen by the
  hook, which reads the command text and not its targets; it surfaces only at
  the close gate. The operator accepted that gap by ruling, and the open skill
  now states it beside the rule, together with a second one: stale bindings
  are never swept, and are inert once their worktree is gone. The same entry
  said the context metric splits injected rule text into root, index,
  per-lane and remainder parts. The per-lane part read zero in every
  population, by construction: per-lane rule-files reach a session as a
  different record type from the class being split. The row now reads that
  record type, and a census line prints the population it measured.
- **The relocation review's growth trigger fires on growth only.** A surface
  at or over the size threshold that has not grown since the anchor is now
  recorded as evidence, not a hit. The anchor itself moves only on an apply
  session's commits on the main line, so a later booking by a subproject
  cannot reset it. The runway readout also prints a 72-hour growth rate
  beside the whole-window mean, after a two-day burst sat unseen under a slow
  nine-day average. Firing still uses the window rate.
- **The review's apply log closed two more holes.** A dropped item is
  terminal and carries only its reason. A hand-back consumed by the shrink
  pass is booked as its own row, because the reader honours rows only and
  twelve such hand-backs had been named in prose. The digesters also read the
  newest run that holds an apply log, so a pass fired before its own review's
  apply no longer loses the previous run's carries.
- **A second watcher reaper had the same stale match.** The session-end stop
  hook looked for the pre-migration process form, so it found nothing while
  exiting 0, the same hole the close-time sweep had until the last refresh. It
  is the only reaper that reaches a duplicate watcher on a directory that
  still exists. One such duplicate held about a gigabyte of compressed memory
  against under 3 MB resident, which counts against the kernel governor's
  memory-pressure gate while a resident-size survey shows nothing. A witness
  test fails on the old line.
- **The kernel governor's thread cap on the laptops went from four to
  eight.** A cold build of the legal-domain kernel ran 17–24 % faster on two
  laptops with memory-compressor occupancy flat. The four-core LAN nodes keep
  four.
- **The programmatic lane's external blocker has cleared.** The vendor-side
  change the parked lane was waiting on has landed. The lane stays parked
  until the operator flips it; nothing in the cron fleet changed this round.

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

Operator home paths are genericized; AWS account / resource / device
identifiers and case-specific example IDs are stripped. The short nicknames of
the developer's own workstations do appear in the rule-set — they carry no
network address and are kept because the multi-host scheduling rules are
unreadable without them. A live redaction gate sweeps every file the push carries, whatever its
extension, before any push — a HARD blocklist hit aborts the compile and
push, a binary file is refused unless it has a named allow row, and a scan
that reads zero files is a failure, not a vacuous pass. The engineering content — conventions, exit-code
contracts, hook behavior, phase ledgers — is preserved, because that is the
methodology this repo exists to publish.

Several additional bars are enforced as fail-closed pairs rather than single
greps — among them a bar on one collateral docket family, a bar on
session-multiplexer local state (which carries branch names, transcript
paths, and prompt previews), a bar on contact addresses, and a bar on rooted
internal paths. Each has a content scanner over file bytes *and* a path
scanner over file names, because a barred token in a path renders publicly
in the repo tree without ever appearing inside a file. A separate path rule
admits formal-kernel source files only under an examples directory and
refuses them everywhere else, so a kernel file nobody thought about fails
closed. Every one aborts the publish rather than silently dropping the
offending file. Each ships its own
pinned regression test — the gates are themselves subject to the proof-of-fire
rule described above. As of 2026-07-24 no contact email appears on any public
surface in this organisation; the organisation page is the sole contact channel,
so questions are answered in public. A collateral federal-appeal docket number
was added to the hard-blocked set on 2026-07-31; the spelled-out court name
without the number remains publishable.

A fourth kind of guard sits inside the renderer rather than at the gate: it
asserts over its own rendered output and hard-exits, naming the line, if a
barred form survives. Rewrite rules alone are silent against a sentence nobody
wrote a rule for; an assertion on the output is not.

## Cadence

Refreshed per release run, not on a fixed schedule — gaps of two to four
weeks have happened, and this repo's commit history is the authority on
when it last moved. Each run re-renders the `CLAUDE.md` graph, less any
mirror held for review, and the
lifecycle skills + their specs. The memory topic-file tree and the recall
memos are allow-list pending (see above), not on any refresh clock.
Re-rankings, new subprojects, and new cross-subproject conventions land as
ordinary diffs; the commit log is the change record.
