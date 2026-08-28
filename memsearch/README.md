# memsearch/

A curated selection of daily engineering memos that the AI assistant
writes alongside the auto-memory tree. Per-subproject and **opt-in**: a
memo reaches this subtree only because its author marked it publishable,
one memo at a time.

**This subtree is empty, and that is the expected state rather than a
backlog.** The opt-in marker is the only way in, and nothing has been
opted in. The design is deliberate: a deny-sweep over a private memo tree
is the wrong mechanism for this material, because a memo whose *subject*
is a redaction bar cannot be scrubbed of it and stay useful. Until an
author opts a memo in, the correct size of this directory is zero. The
shape below documents what it would look like if that changes; it is not
a promise about a schedule.

See the [umbrella README](../README.md) for the broader thesis.
Sibling subtrees: [`claude-md/`](../claude-md/), [`skills/`](../skills/),
[`memory/`](../memory/), [`specs/`](../specs/).

## What memsearch is

memsearch is a semantic-memory layer that runs alongside the AI
assistant: a vector index built from markdown daily memos. Each
working day in each subproject can produce a memo summarising what
got designed, debugged, decided, or rejected. The memos are
markdown source-of-truth; the vector index is regeneratable cache.

Architecturally, memsearch is **fork-isolated recall**: when the
assistant queries it mid-session, the search runs in a forked
context, the relevant memo snippets get summarised back, and the
curated digest doesn't pollute the main session's context window.
That isolation is what makes memsearch usable across a constellation
of this size without context-window blowup.

## What this subtree publishes

The publishable subset of those memos. The bar is high — the memo
has to tell a **self-contained engineering story**: a debug, a
design pivot, a spec-vs-implementation reconciliation, a debate
between two parallel-subagent plans, the moment a memory entry was
created from a surprise.

Bookkeeping memos ("today I committed three small fixes") don't
publish. Day-of-routine-grind memos don't publish. Memos that name
private participants by filename don't publish.

The default is **exclude**.

## Opt-in mechanism

A memo is published when its author marks it explicitly:

```markdown
<!-- publish: yes -->
```

at the top of the memo file. That comment is the operator's
**affirmative attestation** that the memo has been swept for the
redaction rules below. Without the comment, the memo stays private
even if the date directory is otherwise being mirrored.

The attestation is load-bearing because daily memos summarise the
day's commits and edits, and commit messages or filenames can
incidentally name private participants. Putting the attestation on
the memo rather than at the directory level makes redaction a
per-memo decision.

## Layout

```
memsearch/
  <sub>/                       one per subproject with publishable memos
    YYYY-MM-DD.md              redacted daily memo for that subproject + day
```

Only subprojects with at least one published memo appear. A
subproject with zero opt-ins simply has no directory.

## Lifecycle

Memos that are not opted in stay private — they served their purpose
when they were written (the assistant searched them, found context, used
the context) and do not need to live in the public mirror.

A memo's publication is not permanent. If a later sweep judges that
a previously published memo no longer tells a useful story
(superseded by a spec, the bug it documents was reverted, the design
pivot was itself pivoted away from), it can be removed in a
subsequent batch.

## Redaction

In addition to the general redaction rules (see
[`../claude-md/README.md`](../claude-md/README.md#redaction)):

- **Opposing-party names, children's names, private addresses,
  docket numbers.** Stripped. The opt-in comment is the attestation
  this sweep has happened.
- **Commit hashes and file paths from the day's work.** Subproject-
  relative paths inside a public subproject are fine; rooted paths
  into private subprojects (e.g. into the litigation surface) are
  stripped or paraphrased.
- **Names of in-flight specs that haven't been promoted yet.**
  Either wait for the spec to land in the public specs surface, or
  paraphrase the design question without naming the slug.

Memos that cannot be safely redacted are not opted in.

## Refresh cadence

Quarterly batch sweep. The operator reviews the quarter's memos,
marks the publishable ones with `<!-- publish: yes -->`, runs the
sync script (which copies marked memos + runs the redaction sweep),
and promotes via the push wrapper.

This is the slowest cadence in the repo. The rule-set mirror refreshes
weekly because it mirrors state that changes weekly; the memory mirror
is allow-list pending and on no clock at all; the daily memos either
turn out to be worth publishing or they don't, and that judgement is
easier to make in a batch than in real time.

## How to read

Browse by subproject. Within a subproject, browse chronologically.
Each memo is a snapshot of *that day's* engineering thinking —
what got worked on, what got decided, what got rejected. The
collection is not a continuous narrative; it is a sequence of
self-contained stories tagged by date.

The memos that publish are the ones with reusable engineering
insight — they are *examples* of the methodology the umbrella
README describes, not its specification.

## License

MIT — see `../LICENSE-MIT` at the umbrella root. Prose and
AI-agentic workflow files fall under the MIT side of the two-license
pair.
