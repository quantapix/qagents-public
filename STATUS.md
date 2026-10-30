# qagents-public — status

_Snapshot: 2026-10-30. Refreshed per release run during the
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
  round a small part of the published set moved; the commit diff is the change
  record.

## What changed since the 2026-10-23 refresh

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

## Earlier: what changed in the 2026-10-23 refresh

- **A session opened from inside another session is bound to its new lock.**
  When a session provisions a second project from inside its own worktree,
  the new session is now recorded against the new lock. Two hooks then refuse
  its file writes, and its history-writing git commands (commit, merge,
  rebase, reset, checkout and the rest), anywhere in another lock's worktree.
  Each refuses only on positive evidence, and a session launched from the
  canonical checkout binds nothing. The open skill tells a bound session to
  move its working directory before any write: from the old directory, a
  relative write or commit lands on the other session's branch.
- **The three formal kernels moved to Lean v4.35.0 together**, with the
  market simulator's driver layer following. The release removed three
  trusted-evaluation constants that eleven of the operational kernel's
  committed attack fixtures named, so the fixtures were maintained in the
  same change. The rule-set now states that a toolchain bump's attack-corpus
  half is graded by the kernel's own attack judge over every fixture on both
  toolchains, compared file for file, and never by whether the library
  builds.
- **An optimization pass trimmed sixteen rule-files on 2026-10-18.** All
  sixteen are in the published set, and most mirrors in this cut are shorter
  for it.
- **The relocation review's apply log has a closed grammar.** Each row now
  names exactly one review item and a disposition from a fixed set: cured,
  consumed, owner-done, struck or dropped. The first three must cite a
  commit, or the reader prints a finding and the row keeps aging. The session
  that applies the moves also retires each owed review item the blueprint
  dispositioned, and records that beside the routing item's retirement.
- **The context metric attributes injected rule text by surface.** Its
  report-only output now splits the injected-instructions class into the
  root rule-file, the memory index, the per-lane rule-files and an
  unattributed remainder. Attribution goes by the injected file's own header,
  not its path, and the parts sum to the class total. Separately, the
  over-long index-hook check now has one definition shared by the close-time
  warning and the sweep, and the sweep no longer reads a deadline date as the
  date of a fact.
- **The shared ledger store no longer has a cloud database.** The managed
  instance it was migrated off was destroyed on 2026-10-19. The store runs on
  a LAN primary, with a second workstation as backup and restore-verify peer.
- **The site's framework-count figure reads the status hub.** Since
  2026-10-19 the quantapix.com statistic strip sums the two product kernels'
  own reported framework counts, and its test reads the hub rather than a
  literal.
- **Two retired spec renders were removed from `skills/specs/`.** The charter
  renders replaced them earlier; the release sync now also deletes files that
  exist only on the public side.

Earlier refreshes are recorded in this repo's commit history.

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
