# qagents-public — status

_Snapshot: 2026-11-13. Refreshed per release run during the
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
- The `claude-md/` graph re-renders from the private rule-sets on refresh. This
  round fifteen of the twenty-one published rule-files changed, most of them
  shortened by two optimization passes; the commit diff is the change record.

## What changed since the 2026-10-30 refresh

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

## Earlier: what changed in the 2026-10-30 refresh

- **A regex `git grep` is now refused in sessions.** On the macOS workstations
  a regex `git grep` scans every tracked binary through the system regex
  library. Peak memory reached tens of gigabytes, and this accounted for most
  of one workstation's recorded pressure events over three weeks. A session
  hook now denies a `git grep` call that lacks a flag skipping binaries or
  changing the matcher. The hook fails open, and it does not cover script call
  sites or sessions running outside the repo; the rule-set states both limits
  beside the rule.
- **Kernel builds run under a per-host governor.** Concurrent Lean runs had
  rebooted the laptops. The kernel lanes now enter Lean through a wrapper that
  takes a host-wide mutex, caps threads and priority, and refuses to start
  under memory-compressor pressure. The first pressure threshold sat below one
  laptop's idle reading and refused every start, so the default was raised
  after measurement. A later fix stops a governed job's child processes from
  outliving it.
- **A kernel job can run remotely under a hard memory cap.** A job ships whole
  to a LAN node and runs under a 24 GB cgroup limit the laptops cannot give.
  Two measured corrections came out of the witnesses. A soft memory band with
  swap disabled throttled a runaway 30 GB allocation for more than ten minutes,
  where the hard limit alone killed it in 13 seconds, so the soft band defaults
  to zero. The default out-of-memory policy turned the kernel's kill into an
  ordinary termination code with an empty record, so the scope now stays up
  long enough for the job to record its own memory events. A cold build ran
  about 2.5 times slower remotely, inside the expected range.
- **The recall watcher releases its model when idle.** It now unloads the
  embedding model after two idle minutes and reloads on the next file event.
  Measured on one workstation: 1.8 GB loaded, 162 MB after the first unload,
  220 to 800 MB after later reloads. The in-process target of under 150 MB was
  not met. Separately, the close step's orphan-watcher sweep had matched only
  the process form from before the recall migration, so for twenty days it
  reaped nothing while exiting 0. It matches the current form now.
- **The memory-index entry cap grades the whole entry.** The 150-character
  limit now reads one length definition across the entry.
- **The release lane's pre-push read covers the static site shell.** The probe
  read the replay API only. The shell is a different surface with a different
  failure path, so the push step now chains both, and a test fails if the shell
  argument is dropped.

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
