# qagents-public

> The redacted mirror of the AI-assistant working context behind the
> Quantapix engineering practice — `CLAUDE.md` rule-set + auto-memory
> topic files + selected memsearch daily memos, refreshed weekly from
> the private working tree.

A weekly-refreshed window into how a sole developer plus an expert AI
assistant collaborate inside a single monorepo across twenty-four
sibling subprojects. The artifact this repo publishes is *not* the
implementation code — that lives in the per-subproject public repos.
It is the **rule set** the assistant reads at every session start,
the topic files it loads on demand, and the daily engineering memos
curated alongside.

- Parent organisation: <https://github.com/quantapix>
- Engineering output: <https://quantapix.com>
- Motivational record: <https://femfas.net>

## Why this repo

The 2026 bet: what is worth publishing is no longer the implementation
code (LLMs commodify that). It is the **`CLAUDE.md` rule-set + memory + recall** 
that lets a sole developer collaborate with an AI
assistant across twenty-four non-overlapping subprojects without
contradicting itself. Eight themes carry that bet; a founding case
study closes the section.

### 1. The asymmetry qagents exploits

Two empirical observations about working with AI assistants in large,
varied codebases:

1. AI assistants make mistakes — especially "little" mistakes (a
   renamed import nobody re-greps for, a doc that drifts from the
   code it documents, a field added to one of three siblings, a
   memory entry that contradicts a newer one). In a complex
   constellation these accumulate faster than any human can notice
   them.
2. AI assistants excel at *finding* the same kind of mistakes —
   given the right context window. Inconsistencies, contradictions,
   orphaned references, neglected pieces — these are the exact
   failure modes an LLM is good at surfacing, **if and only if** it
   sees the relevant pieces side-by-side.

qagents is architected around this asymmetry. The same engine that
introduces the small mistakes is the engine that surfaces and fixes
them — but only if its context window contains the right slice of
the working tree. That last clause is the entire engineering problem
this repo publishes.

### 2. Core competencies + inter-project tension resolution

The private repo runs **twenty-four** sibling subprojects under a single
root. They share a venv, a pnpm workspace, a Lean toolchain, and a
Git tree — but they explicitly do *not* share code. The boundary rule
("No cross-subproject imports — ever") is load-bearing.

Each subproject has its own `CLAUDE.md`. That file carries:

- **Core competencies** — the rules + invariants + caveats only this
  subproject's authors should care about. Where the canonical OHLCV
  parquet lives. How the Lean kernel composes. Which defined-risk
  options strategies are allowed. Which docket the current motion
  lands in.
- **Boundary surfaces** — the seams this subproject exposes outward.
  A status JSON slot, a JSON schema, a kit-mount contract. What
  other subprojects can rely on; what they cannot.

The root `CLAUDE.md` only pins **the conventions that cross subproject
boundaries** — the language split, the canonical bar shape, the GICS
mapping, the data-hub-not-shared-code rule, the session lifecycle,
the status hub. It does *not* re-litigate anything that lives in a
per-subproject `CLAUDE.md`.

Inter-project tensions — a renamed field on the shared bar shape, a
new options strategy, a status-hub schema bump — get resolved by
**a single session that holds the write-lock on every affected
subproject**. That session reads every relevant `CLAUDE.md`, proposes
a coordinated edit, debates it (theme 3), and applies. The lock is
the guarantee that nobody else is editing the same surfaces in
parallel.

### 3. Spec → debate → implement → finalize

The non-trivial unit of work in qagents is a **spec**, not a commit.

```
  propose              debate                implement               finalize
 tmp proposal  ──►  AI vs AI critique  ──►  surgical edits + tests  ──►  promoted spec
                                                                         |
                                                                         v
                                                  cited by skills + per-subproject CLAUDE.mds
```

Each phase has a different actor:

1. **Propose.** A session drafts a spec into the tmp area. Status:
   "in-flight". The spec describes the design, the constraints, the
   tradeoffs, the rejected alternatives. Often the proposer is *one*
   expertise — the subproject's own context.
2. **Debate.** Either (a) a sibling session with different subproject
   context critiques it, or (b) parallel subagents draft competing
   designs (the "twin-plan review" pattern: each subagent writes its
   variant; the parent session converges them axis-by-axis with an
   "Appendix-A retirement" section calling out what got dropped).
   The asymmetry from theme 1 is in full force here: the critic AI
   is *not* the proposer AI in any meaningful sense — different
   subproject `CLAUDE.md`, different topic-file load-out, different
   skill set. It sees what the proposer missed.
3. **Implement.** Surgical edits per the spec. A skill enforces the
   discipline — surface assumptions, match existing style, clean
   only your own orphans, don't silently pick between
   interpretations. A second skill pairs tests with each fix. A
   five-iteration test loop runs the implementation against smoke /
   edges / integration / conformance / regression — each iteration
   is a clean-context subagent that doesn't carry the prior
   failures' framing forward.
4. **Finalize.** The spec is promoted from tmp into the specs
   directory; tests land in a sibling tests directory. The session's
   close writes a dated summary. The spec is now cited by skills +
   subproject `CLAUDE.md`s; the tmp entry must be deleted in the same
   commit (the daily watcher flags any "adopted-orphan").

Two further details:

- **AI checking AI is the rule, not the exception.** A spec reviewed
  only by the proposer is treated as unreviewed. Code changed
  without a code-review pass or a cloud-review invocation is flagged
  at session close.
- **The debate is auditable.** Every spec carries its rejected
  alternatives in-band ("considered X, dropped because Y");
  twin-plan Appendix-A entries name the loser. The audit trail is
  the design document, not a separate decision log.

### 4. Parallel sessions via worktrees

The coordination primitive in qagents is **git itself**. There is no
central scheduler, no lock server, no message bus. There is one rule:
**branch presence IS the write-lock.**

- `/open <project>` creates a branch named `<project>` (or
  `<project>-N` if `<project>-N-1` already exists — stacked) AND a
  worktree. A second session attempting `/open <project>` blocks
  because the branch already exists. A whole-repo open blocks if any
  subproject session is open.
- `/close` summarises the session, applies the immediate `CLAUDE.md`
  edits to the project's own surface, queues cross-subproject hints
  into a deferred file (picked up later by `/do-claude-updates`
  once the contention window has closed), and cascades the merge up
  the stack.
- A second sentinel — `.data-write-lock` at the repo root, atomic
  create / `rm` on exit-trap — serialises writes to the shared-data
  hub across sessions. Only `/close` and `/do-claude-updates` hold
  it.
- The cron lane (SDK routines fired by a launchd scheduler) never
  touches the canonical data hub directly. It stages into a
  gitignored buffer mirroring the canonical path layout; a daily
  verifier holds the lock once a day and rsyncs the buffer into
  canonical.

Parallelism in practice: up to one whole-repo session and N
non-overlapping subproject sessions concurrently, each in its own
worktree, each with its own `CLAUDE.md` graph loaded. Cross-cutting
work serialises through the branch-lock; within-subproject work
parallelises freely. A single laptop, no external coordinator.

### 5. Context-window optimisation

A `CLAUDE.md` over ~600 lines / 30KB silently truncates at session
load. The memory index over 200 lines does the same. These caps are
not soft; they are hard ceilings on what the assistant sees at turn
zero. Every session that runs over an unoptimised tree is running
with a partial map of its own working context.

qagents treats context optimisation as a first-class engineering
concern, on the same level as test coverage:

- **The memory index is an index, not a memory.** It holds one line
  per topic, ≤150 chars, under the 200-line cap. Detail lives in
  topic files (`feedback_*.md`, `project_*.md`, `reference_*.md`)
  loaded on demand. The index is curated, not appended-to.
- **`CLAUDE.md` files cite, they don't inline.** A new convention
  goes into a dated spec; the `CLAUDE.md` paragraph naming it is one
  sentence + a relative path. Mechanics live in scripts; rules live
  in `CLAUDE.md`s; reasoning lives in specs.
- **`/do-claude-optimizations`** is a nightly assistant pass that
  fans out one digester subagent per `CLAUDE.md` (root +
  per-subproject) plus a memory-index subagent — around two dozen
  in parallel — followed by one sequential cross-cutting digester.
  Each proposes concrete edit-tool-ready trims to bring its target
  back under the load-truncation caps. The coordinator merges into
  an apply plan; the apply phase is mechanical. Goal: every
  `CLAUDE.md` reload-survives the next session.
- **memsearch is the fork-isolated recall lane.** Per-subproject
  vector collections + per-subproject daily memo trees. Recall runs
  in a forked context so the curated digest doesn't pollute the main
  session's window. The daily memos themselves are markdown
  source-of-truth; the vector index is regeneratable cache.

The publishable shape of this — the snapshots in `claude-md/`,
`memory/`, `memsearch/` (see "Layout" below) — is the *result* of
these disciplines, not their description. This README explains the
disciplines; the snapshots show what they produce.

### 6. Coordination primitives — what crosses, what doesn't

The boundaries that aren't `CLAUDE.md` text but are still
load-bearing — data hubs, sentinel write-locks, scoped MCP servers —
get the full treatment in the "Cross-subproject conventions" section
below. The asymmetry is: code is per-subproject; data hubs cross.

A third primitive crosses the same way a data hub does: the **kit-mount**
pattern. One domain-neutral graphing kit ships as vanilla JS into three
product surfaces — the two verifier UIs build-inline it; the local-only
monitoring app mounts it at request time over private live data. The kit is
the shared seam; none of the three imports another's code.

### 7. AI-checking-AI patterns

Beyond theme 3's spec debate, six runtime checks rely on AI
assistants inspecting each other's work:

1. **Specialised subagents.** Read-only file/symbol exploration,
   read-only architecture planning, diff-correctness review, the
   four-subagent context-optimisation pass, plus per-subproject
   sub-agents (e.g. a runtime defined-risk enforcement agent for the
   trading side; a coordinator + ten volume agents for federal
   record-appendix assembly).
2. **Test loops with clean-context subagents.** Each iteration of
   the five-iteration test loop runs in a fresh subagent, so prior
   iterations' false framings don't carry forward.
3. **Cross-subproject hint judging.** Edits to one subproject's
   `CLAUDE.md` queue hints in a deferred file describing the
   cross-subproject implications. A later session (different
   context, holds the write-lock on every `CLAUDE.md`) judges each
   hint — apply or skip — based on the current state of the affected
   files. The queue absorbs contention; the judge resolves it
   asynchronously.
4. **A constellation watcher** runs as a cron-fired daily subagent
   constellation (checker / planner / reporter / verifier) emitting
   dated artifacts. Observe-only in the sense that matters — it
   performs no deploys and mutates no subproject's working tree. It
   does commit, and it does fast-forward and push the main branch to
   the authority remote, but strictly inside its own audit lane and
   never forced. Outputs flow back into the operator queue.
5. **An adversarial sibling** runs on demand in two shapes. The first
   is the per-target positions lane: one subagent per target produces
   ten numbered findings written from the position of someone who
   *wants* the system to fail. The second is a set of three chartered
   review fleets — one that pressures the charter and spec corpus for
   coherency and concision, one that reviews the formal-kernel program
   across all three axes for shared machinery and cross-axis learnings,
   and one that acts as the counterweight to the shrink pass: before
   anything is trimmed, its content must be *spread* down the
   disclosure ladder rather than discarded. Every fleet is
   observe-only — it writes a blueprint and an action prompt, and the
   actual edits happen out of band in a session that holds the
   write-lock.
6. **Cloud multi-agent review** is operator-fired and aggregates
   findings from multiple independent reviewer agents on the current
   branch or a pull request.

### 8. Programmatic Claude — the cron lane

Most assistant work in qagents is interactive (the operator types at
a prompt; subagents fan out from there). A growing fraction is
programmatic — cron-fired routines that don't have an operator in
the loop:

- The programmatic lane is **parked**. The separately funded SDK credit
  pool was withdrawn, the opt-in fleet reverted, and every cron routine
  now runs the default non-interactive print lane against the
  interactive subscription. The wrapper, the ledger, the routine
  definitions and their tests are all retained as-is; nothing has been
  deleted, and a single suffix restores the lane if access returns.
  Until then it is treated as an external blocker with a registry
  entry, deliberately excluded from every bottleneck metric so a parked
  dependency cannot distort the dependency graph.
- **The cron wrapper fails closed on billing.** It refuses to run
  against an API key unless an explicit override is set, and it refuses
  the highest-cost model tier outright with no override at all. Model
  selection uses bare tier aliases, never pinned minor versions, so a
  tier sweep is one edit. Budget caps are widened, never traded for a
  weaker model.
- Three audited LLM-call lanes ride the donation drive's primary
  subscription line:
  - **Tier A** — interactive assistant sessions. Operator at the
    keyboard.
  - **Tier B** — programmatic SDK routines. These currently draw the
    same Claude Max 20× subscription limits as the interactive lane; a
    separately funded SDK credit pool was funded, then withdrawn — the
    lane is parked, not planned. Cron-fired routines ride this.
  - **Tier C** — optional API-rate overage. Default off; stays
    inside the AI-assistant bucket if enabled. Cross-bucket use is
    forbidden — the donation drive's JSON manifest pins the
    enforcement flag.
- An adoption ledger tracks per-routine migration notes, token-cost
  deltas, and regression catches.

### Founding case study: federal-record-as-spec

The first non-trivial system specced in qagents was a federal
civil-rights case. The case is the proof-of-concept for the entire
architecture: a system that *refuses to let you cheat* — every
factual claim has to reduce to a verifiable predicate; every
predicate has to be backed by a quoted source; every theorem is
checked by a kernel that does no I/O. Lean4 enforces this for the
legal-domain kernel; the same pattern enforces it for the
financial-domain kernel (five frameworks: TREND / MOMENTUM /
OPTIONS-RISK / SECTOR / DRAWDOWN). A third kernel now applies the same
pattern to the *operational* domain — axiomatizing the version-control
conventions the constellation itself runs on (the branch-as-write-lock
rule of theme 4 is its first proved theorem). Its consumer is the
local-only monitoring web app, fed over the same files/SSE seam the other
two kernels use. The kernels never share
domain, ground truth, or consumer; the charter pins **seven** invariants,
including "no manual proof driving, ever" — every proof is driven by AI
assistants debating in parallel, with the kernel as the only judge — and, most
recently, gate uniformity: every kernel must pass the same fixed set of
cross-kernel coherency checks with a hard exit code, not an advisory log.

The two products ship the same kernel against different statutes and
different OHLCV. The public verifier endpoints accept **redacted
input only**; no real names, dockets, account numbers, or PII flow
to the servers or the assistants. The donation drive carries a hard
privacy floor on this.

The publishable mirror in this repo carries the *methodology* that
produced those kernels — the `CLAUDE.md` graph that encoded the
predicates, the memory entries that tracked the debates, the
memsearch memos that recovered the rejected alternatives. The
kernels themselves live in the per-product public repos.

## Layout

```
qagents-public/
  README.md                       this file
  LICENSE                         Apache 2.0 — code lane (Lean axioms, drivers, TS/Python)
  LICENSE-MIT                     MIT — prose + AI-agentic workflows (the three subtrees below)
  claude-md/                      redacted CLAUDE.md graph
    root.md                       redacted root CLAUDE.md
    <sub>.md                      one per included subproject (see table below)
    data/                         shared-hub conventions (not subprojects)
      data.md / specs.md / tmp.md
  skills/                         session-lifecycle + optimization skills
    open/close/do-claude-updates/do-claude-optimizations/SKILL.md
    specs/                        the adopted specs those skills cite
  memory/                         redacted topic-file mirror
    MEMORY.md                     redacted index
    feedback_*.md                 engineering / authorship discipline
    project_*.md                  subproject snapshots
    reference_*.md                public-facing pointers
  memsearch/                      curated daily memos
    <sub>/YYYY-MM-DD.md           one per opt-in publishable day
```

This first cut is **product-focused**: the `CLAUDE.md` mirrors and
session-lifecycle skills behind the two shipping products plus the core
infrastructure, not yet the full graph. The `claude-md/` and `skills/`
subtrees are live; `memory/` and `memsearch/` carry their READMEs and nothing
else — a ruling rather than a backlog, restated below. Formerly described as
filling in on
later weekly refreshes. At steady state the graph runs to a few hundred
files (the full subproject + infrastructure `CLAUDE.md` set, ~200–250 memory
topic files, and ~50 aggressively-pruned memsearch daily memos). See
[`claude-md/README.md`](./claude-md/README.md) for exactly which
subprojects publish this round and which are deferred.

Litigation-domain `CLAUDE.md`s (the appeals / pleading / legal-hub
surface) are deliberately excluded — too easy for federal-record
drift, even redacted.

## Sibling subprojects (twenty-four, one venv, one workspace)

| Subproject     | Role                                                                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `analyzing/`   | **Market-inspection tooling (TypeScript), local-only viewer** — DuckDB + Parquet, charting, ingest from public OHLCV sources.                       |
| `trading/`     | Python portfolio-management agents — three PMs (aggressive / moderate / conservative) on a paper-trading broker, orchestrated by AI-assisted routines. |
| `monitoring/`  | Local-only Astro Node-SSR web app for AI-assistant token analytics (was a VSCode extension, retired). 100% TypeScript; SQLite store. Consumes the operational Lean4 axis. |
| `appealing/`   | Pro se federal appellate drafting. Markdown drafts; rendered PDFs flow to a private filing hub.                                                        |
| `pleading/`    | Sibling of `appealing/` — trial-court / status-affidavit / addendum drafting.                                                                          |
| `proving/`     | Lean4 axiomatic theorem-proving with LLM-backed predicate functions for the legal domain. Backs Qnarre.                                                |
| `accounting/`  | Lean4 + LLM-predicates for the financial domain (five frameworks: TREND / MOMENTUM / OPTIONS-RISK / SECTOR / DRAWDOWN). Backs Qresev.                  |
| `verifying/`   | Astro + React shell + FastAPI server for **Qnarre**, the legal-complaint verifier UI. Streams events from `proving/` over SSE.                         |
| `evaluating/`  | Sibling of `verifying/` for **Qresev**, the stock/portfolio evaluator UI. Streams events from `accounting/` over SSE.                                  |
| `visualizing/` | Graphing surface for the formal kernels — renders the cross-domain lattice + a proof-DAG; mounted into both product UIs via the kit-mount pattern.     |
| `designing/`   | Astro + React islands site for quantapix.com. Hosts the `/status` page that aggregates per-subproject status emits.                                    |
| `documenting/` | Sibling of `designing/`; femfas.net.                                                                                                                   |
| `studying/`    | The third Lean4 kernel — the **operational** axis (git as the first axiomatized system; consumed by `monitoring/`). Also owns the cross-axis representation research. |
| `explaining/`  | 50-script video-explainer arc narrated by an AI presenter.                                                                                             |
| `resolving/`   | DaVinci Resolve production-assistance — typed Python wrapper + Fusion authoring skills. Stage 5 of `explaining/`.                                      |
| `blending/`    | Blender + Geometry Nodes production-assistance — typed Python wrapper. Background plates consumed by `resolving/`.                                     |
| `serving/`     | AWS cloud-base. Single source of truth for every AWS resource.                                                                                         |
| `managing/`    | Daily watcher over the constellation. Observe-only — no commits, no deploys, no mutations.                                                             |
| `shorting/`    | Adversarial sibling of `managing/`. Pressure-tests the system from a hostile vantage; observe-only; findings route into the watcher.                   |
| `donating/`    | The six-month public donation drive backing the framework (2026-06-01 → 2026-12-01).                                                                   |
| `publishing/`  | The open-source release subproject — owns the public-org staging tree and the `/publish` pipeline (sweep → redact → compile → push). Produces these repos. |
| `rendering/`   | In-house render engine + brand source of truth — the single owner of pre-rasterized brand artifacts (images live, video next) consumed across the constellation; multiple consumers live (site share-cards, channel art, the kernel-lattice graph). |
| `extending/`   | Desktop-assistant extensions + adoption enablement. Ships thin stdio MCP servers that proxy the two product surfaces (allow-listed replay, kernel refusal rules mirrored, never an additional kernel consumer), packaged through the release lane. |
| `developing/`  | Native macOS (and next iOS) SwiftUI clients for the two products. A generated-project + package-manager monorepo; never an additional kernel consumer — future live wiring rides the existing product seams. |

The `appealing/` and `pleading/` rows describe the private subprojects
that exist in the working tree; their `CLAUDE.md`s do **not** publish
here. Public-facing material from that work routes through
`documenting/` instead.

## Cross-subproject conventions worth publishing

The conventions below cross subproject boundaries. They are the rules
the assistant has to remember without re-reading the whole codebase.

### Language split

- TypeScript for the Astro sites, the local-only analytics app, the
  market-inspection tooling, and the cloud-infrastructure definitions.
- Python for the trading agents and the kernel drivers.
- Lean4 for the formal kernels (`proving/`, `accounting/`, `studying/`)
  — three orthogonal axes: textual (federal statutes), numerical (market
  data), operational (version-control state). All three pin the **same**
  Lean toolchain version in lockstep — a single current-stable release —
  so a shared cloud build image serves them with no per-build toolchain
  switch.
- A Python microservice is allowed as an escape hatch for heavy
  numerics. Never reach across: trading Python does not import from
  analyzing TypeScript; analyzing TS does not import from trading.

### Canonical OHLCV bar shape

Every place that produces or consumes bar data uses the same column
set: `{ ts, o, h, l, c, v, adj_c }`. No `t` instead of `ts`, no
missing `adj_c`, no vendor field names past the client module.
Adapters translate at the boundary.

### GICS sector classification

Mapping is shared data, not shared code: a Parquet file keyed by
symbol with the canonical GICS hierarchy. Analyzers and traders read
via thin loaders; neither writes. Refresh runs through a single seed
script.

### Defined-risk options

Code that constructs, evaluates, or submits options orders is
restricted to: `long_call`, `long_put`, `debit_spread_call`,
`debit_spread_put`, `covered_call`, `protective_put`. Enforced at
both authoring time (a skill) and runtime (an agent). Applies to
analyzer-side tooling too.

### Data hubs, not shared code

When two subprojects need the same data, the data lives at a
canonical path under the shared-data hub (Parquet or JSON), with each
subproject reading via a thin per-side loader. Subprojects do not
import each other's code. Four examples currently:

- A status-hub JSON slot per subproject, aggregated by `designing/`
  at build time.
- The donation-drive JSON consumed by both Astro sites.
- The GICS symbol parquet read by analyzers and traders.
- The video-roster JSON produced by the release subproject and consumed
  by the quantapix.com `/videos` page.

The shared-data hub is governed by a five-kind closed-set charter
(`data-hub` / `convention-anchor` / `render-cache` / `status-emit` /
`letter-binding`) plus a three-question gate (kind, producer-of-record,
consumers). Two subprojects reaching for the same code module rather
than a data hub is flagged by the daily watcher.

### Session lifecycle

Sessions start with `/open <project>` and end with `/close`. The
branch presence IS the write-lock; conflicting parallel sessions on
the same scope are blocked by branch existence. Cross-subproject
edits queue as deferred hints picked up later by
`/do-claude-updates`.

### Status hub

Every subproject writes a status JSON describing the panels it
exposes; the `designing/` site reads every slot at build time and
renders `/status`. No cross-subproject TypeScript imports — the JSON
hub is the only seam. This is the canonical example of
*data-hub-not-shared-code*.

## What you will not find here

- The private working tree itself (twenty-four subprojects, the filing
  hub, the redacted legal drafts).
- Per-subproject implementation code — that lives in the
  per-subproject public repos (`qnarre-public`, `qresev-public`,
  `qstudying-public`, `qexplaining-public`, `qdonating-public`).
- Anything tied to ongoing litigation that has not already entered
  the federal-court public record.
- The redaction blocklist — that file is private by design, so this
  repo itself stays safe to mirror.

## Cadence

Refreshed weekly from four private sources:

- The root + per-subproject `CLAUDE.md` graph → `claude-md/`.
- The `open` / `close` / `do-claude-updates` / `do-claude-optimizations`
  skill bodies + their adopted specs → `skills/`. These are the
  executable shape of the session-lifecycle (theme 4) and
  context-optimisation (theme 5) disciplines this README describes.
- The auto-memory topic-file tree → `memory/`.
- Selected daily memsearch memos opted in by the operator →
  `memsearch/` (quarterly batch sweep).

Re-rankings, new subprojects, and new cross-subproject conventions
are committed as ordinary diffs — the commit log is the change
record. The README itself changes monthly when the team, the thesis,
the public-repo roster, or the contact channel changes.

## Donation drive

The framework's six-month public donation drive runs 2026-06-01 →
2026-12-01, with Open Source Collective as the intended fiscal sponsor.
Four exclusive-use buckets: the AI-assistant subscription, a third-party
MCP service line, AWS, and a SCOTUS petition-fee bucket. Public
ledger at <https://opencollective.com/qagents>. The first
fiscal-sponsorship application (submitted 2026-05-23) was declined
2026-06-03 on community-involvement grounds; the drive is holding the
channel float and re-applying ~end of June 2026. Details, monthly
ledgers, and weekly digests in the sibling repo `qdonating-public`.

**Open to outside contributors.** The U.S. Code axiomatization program
— Lean4 theorems backed by LLM-evaluated predicates over the full Code
(~65,700 sections, all 54 titles) — is open to collaborators. It works
over public federal statutes only, so it carries no privacy-floor
surface; it is the natural place to build the project in the open. The
project today is a single developer working with AI assistance, now
opening this effort to contributors. Start at
[`qnarre-public/CONTRIBUTING.md`](https://github.com/quantapix/qnarre-public/blob/main/CONTRIBUTING.md)
and open an issue on that repo to claim a unit. It links a curated starter
set of nine tasks, each a verified defect with acceptance criteria and
reproducible counts. (Discussions are not enabled here, and the nine are not
yet filed as individual issues.)

## Contact

[github.com/quantapix](https://github.com/quantapix) — open an issue on any repo
in the org. Answered in public; there is no contact email.

## License

Two-license pair, mirroring the convention across the `qagents-*`
public repos:

- **`LICENSE`** — Apache 2.0. Covers any code lane (Lean axioms,
  predicate stubs, drivers, TypeScript / Python utilities reused
  from the private working tree). Apache 2.0's patent grant is the
  right protection for the code-side artifacts.
- **`LICENSE-MIT`** — MIT. Covers prose and AI-agentic workflows:
  the `CLAUDE.md` rule-set, the memory topic files, the memsearch
  daily memos, and any `.claude/` agent or skill definitions
  surfaced here. MIT is short, permissive, and well-suited to the
  hybrid prose-and-config category.

Default: MIT for `*.md` and `.claude/` content; Apache 2.0 for
everything under a code-lane subdirectory. The README declares the
split file-by-file when ambiguous.
