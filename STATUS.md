# qagents-public — status

_Snapshot: 2026-08-28. Refreshed weekly (Fridays) during the
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

## What changed since the last refresh (2026-08-21)

- **All three formal kernels finished pulling answer-shaped content out of
  their own rule-files, and one of them found the same leak on a second
  channel.** A kernel's rule-file is injected into every subagent's prompt, so
  a sentence written there reaches a blind reviewer with no read — and no
  blindness check grades a non-read. Each kernel's reference material now lives
  behind a reviewer bar rather than in the injected file. What is publishable
  is the bar and the reason a split beats a banner: a banner asks a reader not
  to look at something it has already shown them. What is not publishable is
  the filename, any section inside it, or an inventory of what a reader would
  find there — this status file said too much on that last point in the
  previous round and the sentence has been removed rather than softened.
- **The same class turned up on a live channel, not just in a file.** The
  financial kernel's blind-cell harness was found publishing each cell's live
  transcript to a surface the cells were barred from, and a gate wired only
  into the acting verb let the reading verbs route around refused state. The
  rule that came out of it generalises past this lane: gate the read verb, not
  only the act verb.
- **A one-week regression proved that a render-time assertion is not a source
  guard.** The output assertion added last round — the renderer refuses to emit
  a mirror still carrying a barred token, naming the offending line — fired this
  round on a rule-file that had been cured seven days earlier. An unrelated
  maintenance pass had written the barred form back in while documenting the
  bar, which is exactly the context the previous round identified as the
  dangerous one. The assertion did its job and the publish stopped. The finding
  is that the only thing standing between the two events was a weekly manual
  run in a different scope.
- **The hand-authored surfaces in this repo have no equivalent of that
  assertion, and six claims were found that were true when written and are false
  now.** A framework roster that had expanded twice; a review-fleet count that
  had gone from three to two when one lane was absorbed into another pass; a
  capability described as forthcoming that had shipped; a front-matter promise
  of two subtrees this repo does not contain; a curation process described in
  the present tense that has never once run; and a prose count of statutory
  titles that the source kernel had ruled must never be stated as prose. None is
  a redaction failure and no blocklist could see any of them: a blocklist tests
  an artifact against a token list, and this class needs the artifact tested
  against the world. All six are corrected in this round.
- **A per-item audit measures diligence, not control of the generator.** The
  operational kernel swept its own taxonomy this round: most members held, a
  handful were demoted, and three escapees turned up in shapes the taxonomy has
  no slot for. The conclusion recorded was to grade the next artifact produced
  rather than the size of the sweep — a sweep that finds new shapes has
  measured its author's diligence, not the generator's behaviour.
- **The cross-subproject hint queue was flushed and a capacity-review pass ran
  out of band**, folding queued implications back into the rule-sets that own
  them.

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

A fourth kind of guard sits inside the renderer rather than at the gate: it
asserts over its own rendered output and hard-exits, naming the line, if a
barred form survives. Rewrite rules alone are silent against a sentence nobody
wrote a rule for; an assertion on the output is not.

## Cadence

Weekly (Fridays) from the `CLAUDE.md` graph and the lifecycle skills + their
specs. The memory topic-file tree and the recall memos are allow-list pending
(see above), not on a refresh clock.
Re-rankings, new subprojects, and new cross-subproject conventions land as ordinary
diffs; the commit log is the change record.
