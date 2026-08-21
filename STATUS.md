# qagents-public — status

_Snapshot: 2026-08-21. Refreshed weekly (Fridays) during the
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

## What changed since the last refresh (2026-08-14)

- **All three formal kernels pulled answer-shaped content out of their own
  rule-files.** Each kernel's rule-file is injected into every subagent's
  prompt, which means a sentence written there reaches a blind reviewer with
  no read — and no blindness check grades a non-read. The legal-domain kernel
  relocated its golden shapes (composite identifiers, field counts, which
  composite a bridge targets) into a separate, reviewer-barred roster file;
  the operational and financial kernels split their own answer keys out in the
  same window. This is the earlier incorporation-by-reference split taken one
  channel further: incorporation became injection-by-default.
- **The legal-domain kernel gained another hand-built framework** — a federal
  trafficking chapter, authored as a golden reference against which automated
  encodings are scored.
- **The publish lane grew an output assertion, not just more rules.** The
  rule-set mirror already carried rewrite rules that strip barred tokens at
  render time, but a rules-only guard is vacuous against a *new* sentence
  nobody wrote a rule for. The renderer now asserts over its own rendered
  output and hard-exits naming the offending line if a barred token survives.
  Both arms of the proof-of-fire were witnessed: a clean source exits zero, an
  injected unruled sentence exits non-zero.
- **The published skill mirror was measured against its sources for the first
  time.** It is hand-authored and had no drift check, so nothing detected when
  a source moved out from under it. Four published claims were found stale and
  are corrected in this round: a session-agenda section that no longer exists,
  a gate's matching rule published in its pre-fix form, a model pin the source
  had already removed, and a size cap attributed to the wrong gate. A witnessed
  drift check — not a one-time re-render — is the actual fix, and it is not
  built yet.
- **The cross-subproject hint queue was flushed four times**, folding queued
  implications from the financial, site-authoring, video-production and
  simulation surfaces into the rule-sets that own them.

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
