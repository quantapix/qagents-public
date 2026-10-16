# qagents-public — status

_Snapshot: 2026-10-16. Refreshed per release run during the
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

## What changed since the 2026-10-11 refresh

- **A size-review item is filed only for growth.** The close step's size
  check used to file (or cite) a review item for any rule-file the session
  touched that sat within a fixed margin of its warn cap. It now does so only
  for a file the session itself grew into that margin. A session that edits a
  file already near the cap without growing it is no longer charged with the
  file's history.
- **The session that applies a relocation retires the review item.** Such an
  item used to clear as soon as any relocation run dated after the crossing
  existed, whether or not its moves were applied. It is now retired by the
  session that applies that run's moves, after the apply merges, and only
  when every listed file has a disposition. The run's own record names the
  item it opened and records the retirement; a test refuses an apply log on
  its own as evidence.
- **Unconsumed relocation work ages by the calendar as well.** An apply left
  unconsumed escalated after two later optimization passes, so during a
  stretch with no pass it never aged. It now also ages one interval per seven
  days without a pass, and a move made by the file's own owner counts as
  consumed.
- **The always-loaded cost is measured as injected bytes.** The context
  metric now ranks each rule-file by its size times the number of times it is
  injected, nested rule-files included, beside its on-disk size. A small file
  loaded into every session can cost more than a large one loaded once.
- **Two more report-only readings.** Every memory commit logs the net row
  change in the memory index, and below the soft cap the size helper prints
  the largest byte deltas since the last optimization anchor. Neither refuses
  anything or starts a pass; they exist so growth is measured between passes.
- **The operational kernel's daily sentinel now runs on both workstations.**
  Each copy reads only its own host's archived rounds, so with one seat the
  other host's rounds went unwatched.
- **The market-data hub gained a reference-series directory**, beside the
  bar, portfolio, report, universe, sector and factor directories.
- **The release lane refuses one more class of internal file by name.** A
  path rule now rejects a class of standing orchestrator-facing documents,
  and the glossary that travels with them, wherever either sits in a staged
  tree. The release collector's contract also lists the class as never a
  source: the collector is the channel through which such a document would
  reach a draft, and a dry render of the mirror cannot see that channel.

## Earlier: what changed in the 2026-10-11 refresh

- **Every session summary has one fixed place for its lessons.** The close
  gate used to accept any heading that mentioned learning; it now reads
  exactly one `## Lessons` section and refuses the commit without one. The
  section holds a cite into the shared learning ledger for each lesson worth
  carrying across the kernel lanes, a one-line reason for declining to mint
  one, or a bare `none`. A lesson written under any other heading is not
  read, so the gate now also says where to put it.
- **The size gate files its own follow-up.** When a session grows a
  rule-file to within a fixed margin of its warn cap, or past it, the close
  step itself now files — or cites, if one is open — the review item that
  routes the file to the relocation pass. It never refuses the close for
  this. It also prints a report-only before/after line for every rule-file
  the session grew, and the memory commit records each change in the index's
  size to the shared store, so growth is measured between optimization
  passes rather than reconstructed afterwards.
- **A clean exit from a scheduled fire is no longer read as a finished
  fire.** A fire whose child exits cleanly at the end of its turn while an
  artifact the routine declares is missing, or still a template, now gets
  its own outcome code and a line naming the missing file; the constellation
  watcher grades it as a fifth fire class. Separately, the non-interactive
  lane does not re-prompt a turn that ends on a status message while work is
  still owed, so the trading rule-set now forbids ending a turn that way, on
  top of its rule against expressing a gate as a wait.
- **Provenance records the effort seat's value, not the word "default".** An
  empty seat means the model's own default, which moves when the alias does,
  so a stamp that says only "default" would describe a different setting
  after the next alias change.
- **Custody of the three-kernel program moved to the whole-repo lane.** The
  cross-axis steward role, held since the charter by the subproject that owns
  the operational kernel, now sits with the session that holds the
  write-lock on every subproject. A toolchain bump lands as one whole-repo
  commit covering every pin, after which each axis replays its own example
  proofs; before the cutover, a bump that could not land as one commit was
  recorded as one commit per branch. The operational subproject keeps the
  cross-axis representation research.
- **Semantic recall is served by the in-repo Rust context layer** since
  2026-10-08. The vendored plugin's hooks call it unchanged; the old tree is
  kept for rollback only, for a fixed window.
- **A clearance needs a seat the clearing lane does not run.** When one lane
  clears a public-bound file list, the adversarial sibling now supplies an
  outside review seat: it writes that seat's brief from the file list and a
  comparison set alone, never from the caller's findings, and the record
  states the population compared and what was not looked at. The caller
  rules on it; the seat never clears anything.
- **The cron staging root is trusted by declaration.** For that one
  variable, presence is the aim: a writer does not inspect where it points,
  and exactly one setter exists. A hand-set value naming a checkout is an
  operator error, not a state any writer gates.
- **The release lane's gates moved in two places.** Every staged example
  directory now also runs the drafting lane's own guard by subprocess, and
  any non-zero result aborts the push. And the renderer's path scrub now
  normalises a relative `../` or `./` lead before matching, so a relative
  path into a private tree is scrubbed like a bare one; a test plants both
  forms against a live render.
- **The infrastructure lane's scheduled probes leave a receipt per fire** in
  the shared store, readable from any workstation, and its rule-set now
  states plainly that most declared log groups have no producer — telemetry
  that is declared is not telemetry that is running.
- **Earlier in this window (the 2026-10-02 run):** the subproject table was
  corrected on three rows (the watcher's commit posture, the retired review
  fleet, the market simulator's Lean carve), and the published close and
  hint-flush skills gained the exit rows they lacked.

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
when it last moved. Each run re-renders the `CLAUDE.md` graph and the
lifecycle skills + their specs. The memory topic-file tree and the recall
memos are allow-list pending (see above), not on any refresh clock.
Re-rankings, new subprojects, and new cross-subproject conventions land as
ordinary diffs; the commit log is the change record.
