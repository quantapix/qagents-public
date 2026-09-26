# qagents-public — status

_Snapshot: 2026-09-26. Refreshed per release run during the
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
  bodies, plus the adopted specs they implement. These are the executable shape of
  the worktree-as-lock discipline (theme 4) and the context-window-optimization
  discipline (theme 5) the README describes.
- The `claude-md/` graph widened on the 2026-07-20 refresh from the
  product-focused core to the full publishable set: the local-only analytics
  app, the operational-axis kernel, both public sites' authoring surfaces, the
  video-production chain, and the adversarial sibling all now publish their
  rule-sets. Three subprojects remain deferred and one is an open editorial
  call; the subtree README names each and why.
- The `claude-md/` graph re-renders from the private rule-sets on every
  refresh. This round most of the published set moved, several substantially;
  the commit diff is the change record.

## What changed since the 2026-09-19 refresh

- **The rule-set was audited against the model vendor's own guidance for
  working with the assistant, and the gaps were closed at their owners.** Model
  selection now sits in four named seats, one per lane, with effort as a
  separate per-lane control beside each, so a tier change is a small number of
  known edits rather than a hunt. Every script that imports a third-party
  package pins the project interpreter at both the shebang and the call site,
  because the system's default interpreter changed underneath the repo and an
  import guard that probes the wrong one skips silently.
- **The hint-flush lane can no longer grow a rule-file past its size budget.**
  A queued hint that would push a rule-file into the soft band now needs an
  offsetting trim in the same commit. So does a hint that restates text already
  living in the file's documented overflow home. The session-close gate
  re-grades the same population on whole-repo branches, so the in-session check
  is a convenience, not the only seat.
- **The shared-data write-lock protocol moved to the data hub's own rule-file.**
  The root file keeps a one-paragraph anchor. One rule carried over with it:
  decide whether a write is canonical from how its target was *aimed*, never by
  comparing paths, because a path comparison that is right from the main
  checkout is wrong from a worktree copy.
- **The operational kernel's blind cells now launch outside the working tree**,
  so they receive neither the rule-file nor the memory index. That is measured
  by a probe on every CLI version change, never assumed. A test that must stay
  red until a later session parks in a pending directory rather than the live
  battery, because the close gate has no expected-red lane.
- **A deploy is treated as a publication event.** A stale deployed build is
  invisible to every repository-side gate, so the only evidence of what a
  running service serves is a live read. The live probe now grades its own
  controls, since a refusal-only record cannot fail.
- **The trading side's scheduled routines are paused by an operator ruling**,
  and the paused set has a single owning file with a per-routine re-arm recipe.
  The constellation watcher also learned a fourth class of fire outcome, a
  safeguard refusal, which it no longer confuses with a clean short run or a
  kill.
- **The release lane gained a gate for its own examples directory.** The one
  location where kernel example files may publish now admits a closed set of
  file types, content-scans every data file there, and requires a per-list
  manifest to verify before any push phase runs.

## Earlier: what changed in the 2026-09-19 refresh

- **The lifecycle skills stopped telling a reader to hand-edit a generated
  file.** The forward-only next-steps slot has for some time been a render of
  a shared ledger store, but two of the published skills still described
  resolving an item as deleting it from the file — the one act the close gate
  now refuses. Both skills, and the private sources they mirror, now say to
  retire the item through the ledger verb. Four smaller stale claims in the
  same subtree were corrected with them: the session-open entry forms, the
  hint-flush lane's missing exit codes (including a new size gate), and one
  exit code's history stated backwards.
- **The redaction gate reads more than markdown now.** The one location where
  formal-kernel source may publish is swept for barred content alongside the
  markdown, and the path rule refuses an example whose directory name
  identifies a live matter. Each arm catches a case the other structurally
  cannot. A new test plants each path-prefix rewrite in both directions,
  because only a two-polarity test can say a cure went too far.
- **Refresh cadence is stated as it is.** This file, the org page, and two
  subtree READMEs still said "weekly" after the runs stopped being weekly;
  they now say "per release run".

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
unreadable without them. A live
markdown redaction gate sweeps every `*.md` in the candidate tree before any push —
a HARD blocklist hit aborts the compile and push, and an empty candidate tree is a
failure, not a vacuous pass. The engineering content — conventions, exit-code
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
when it last moved. Each run re-renders the `CLAUDE.md` graph and the
lifecycle skills + their specs. The memory topic-file tree and the recall
memos are allow-list pending (see above), not on any refresh clock.
Re-rankings, new subprojects, and new cross-subproject conventions land as
ordinary diffs; the commit log is the change record.
