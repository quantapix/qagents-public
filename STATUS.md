# qagents-public — status

_Snapshot: 2026-06-12. Refreshed weekly (Fridays) during the
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

## What changed since the last refresh (2026-06-05)

- **A third formal kernel was chartered — the operational axis.** The
  constellation now runs three orthogonal Lean4 kernels: textual (federal
  statutes, behind Qnarre), numerical (market data, behind Qresev), and
  operational (version-control state, consumed by the local monitoring
  surface). A single charter pins six invariants across all three, including
  "no manual proof driving, ever" — proofs are driven by AI assistants in a
  parallel debate lane, with the kernel as the only judge — and a three-way
  toolchain lockstep. The operational kernel's first invariant theorem (the
  branch-as-write-lock exclusion rule from theme 4 of the README) was proved
  this week through that debate lane.
- **The constellation grew to twenty-two subprojects.** A rendering
  subproject went live as the single owner of brand-bearing pre-rasterized
  artifacts (the release subproject is its first consumer), and the kernel
  graphing surface joined the published roster. The status-hub schema, the
  session-lock registry, and the nightly optimization fan-out all widened to
  twenty-two in lockstep — three surfaces, one coordinated sweep, which is
  the point of the conventions this repo publishes.
- **Model policy pinned: the latest top-tier model for complex,
  long-running work.** Subagent fan-outs, axiomatization waves, watchers,
  and collectors never run on a pinned older tier; lesser models are
  allowed only where flagged (bounded cron routines, mechanical closed-set
  classification). The redacted root mirror carries the rule.
- **The spec tree finished its family-layout migration.** Every adopted spec
  now lives in a family directory (spec + subspecs + companion tests) under
  a single dated slug — the flat legacy shape is retired. The
  spec → debate → implement → finalize loop in the README now lands its
  artifacts in one uniform shape.
- **Permission settings became generated artifacts.** Per-subproject
  assistant-permission files are now compiled from a single source tree by
  one build script (drift caught by a `--check` mode), with a weekly
  harvest lane that promotes recurring local allow-patterns into the
  generated sources. Additive-only: the harvest never weakens a deny.
- **The debate framework was promoted from instance to convention.** The
  recurring AI-vs-AI review pattern (theme 7) now has a named generic
  framework with pinned roles, forfeit rules, and gate semantics; round
  records land in a shared tracked hub. Two more instances ran this window,
  including an adversarial messaging-hardening round applied across four
  public surfaces.
- **Both product kernels advanced.** The legal kernel made a set of
  employment-discrimination goldens driver-operational and promoted two
  held waves; the financial kernel widened its shared predicate base and
  promoted its first per-sector Tier-A slice. Detail lives in the
  legal-domain and financial-domain public repos.

## What's scaffolded (fills in on later refreshes)

- **`memory/`** — the redacted auto-memory topic-file mirror. README in place;
  topic files land on a later weekly refresh.
- **`memsearch/`** — curated, opt-in daily memos. README in place; memos land on
  the quarterly batch sweep.
- The remaining publishable subproject `CLAUDE.md` mirrors (the video, site,
  study, and meta-observer surfaces).

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

## Cadence

Weekly (Fridays) from four private sources — the `CLAUDE.md` graph, the lifecycle
skills + their specs, the memory topic-file tree, and selected recall memos.
Re-rankings, new subprojects, and new cross-subproject conventions land as ordinary
diffs; the commit log is the change record.
