# memory/

The intended redacted mirror of the AI-assistant auto-memory tree — the
topic files the assistant writes during sessions and loads back across
sessions to stay coherent.

See the [umbrella README](../README.md) for the broader thesis.
Sibling subtrees: [`claude-md/`](../claude-md/),
[`memsearch/`](../memsearch/).

## Status — placeholder, not yet populated

**No topic files are published here yet.** This subtree currently holds
only this README. The redaction roster that would select and rewrite
publishable entries has not been authored, and no sweep runs.

The blocker is a design question, not a scheduling one. A handful of
private entries exist precisely to record a court-ordered bar on
publishing a particular collateral docket family. An entry whose whole
subject is that bar cannot be scrubbed of the bar and remain useful —
so redaction is the wrong instrument for it. When this subtree ships it
will be gated by a **curated allow-list** (entries opt in) rather than a
deny-sweep (entries opt out), and the release pipeline refuses, by
construction, to publish a file whose name or body carries the barred
family.

Everything below describes the shape that mirror will take.

## What auto-memory is

The AI assistant maintains a persistent, file-based memory across
sessions. It writes short topic files (one fact or one piece of
guidance per file) into a memory directory under its own state tree.
The next session loads an index at turn zero and pulls relevant topic
files on demand.

Without this layer, every session would start cold and re-derive
context from scratch. With it, the assistant accumulates a
project-specific working memory: the operator's preferences, the
project's load-bearing decisions, references to external systems, the
voice register, the conventions that aren't yet codified in a
`CLAUDE.md`.

The discipline that makes this work: **the index is an index, not a
memory.** One line per topic, ≤150 chars, under the 200-line cap that
silently truncates a too-long index at session load. Detail lives in
the topic files; the index points to them.

## Planned layout

```
memory/
  MEMORY.md               redacted index (same filename as the canonical)
  feedback_*.md           guidance the operator has given about how to work
  project_*.md            ongoing-project context (decisions, milestones, plans)
  reference_*.md          pointers to external systems (docs, URLs, gotchas)
  index_*.md              domain sub-indexes, when one domain outgrows the index
```

A further namespace (`user_*`) is reserved by the auto-memory system
for operator profile entries but is currently empty.

## The namespaces

Each topic file carries frontmatter (name, description, type). The
description is what the index line summarises; the type drives where
the assistant looks for it.

- **`feedback_*`** — Guidance the operator has given about how to
  approach work. Both corrections ("don't mock the database in these
  tests") and validations ("yes, that bundled PR was the right
  call"). Saved when the operator explicitly approves or pushes back,
  with a `**Why:**` line and a `**How to apply:**` line so the
  assistant can judge edge cases. This is both the largest namespace
  and the broadest publishable one — a large majority of its entries
  are public-safe engineering / authorship discipline. The rest touch
  litigation workflow, redaction-blocklist mechanics, or
  operator-personal posture and stay private.
- **`project_*`** — Ongoing context: who is doing what, why, by
  when. Decisions, milestones, scope notes. Most entries publish; the
  remainder are litigation-specific. Each
  carries the same `**Why:**` / `**How to apply:**` shape as feedback
  entries so future sessions can judge whether the memory is still
  load-bearing.
- **`reference_*`** — Pointers to external systems and third-party
  resources. URLs, public docs, API gotchas, vendor quirks. Most
  entries publish; the remainder cite private dockets, cloud-identity
  specifics, or per-host paths.
- **`index_*`** — Domain sub-indexes. When one domain accumulates
  enough topic files that its lines crowd the top-level index, those
  lines move into a sub-index and the top-level index keeps a single
  pointer to it. A sub-index is an index of indexes, not a new kind of
  memory; it exists to hold the top-level file under the cap that would
  otherwise truncate it at session load. Whether a given sub-index
  publishes follows its domain — the litigation one does not.

The published set will be curated, not exhaustive. An entry that names
private participants, private paths, or private infrastructure is
either redacted to remove those references or dropped from the public
mirror entirely. The proportions above describe the private
tree; how many of each ship is settled when the allow-list is authored.
Deliberately no absolute counts: a pinned figure here would drift
silently against a tree that grows every session, and the number is
not the point.

## `MEMORY.md` — the index

The index is the entry point. One line per topic file, kebab-case
slug, short description after the dash. Sample shape:

```markdown
- [Title](feedback_<slug>.md) — one-line hook
- [Other Title](project_<slug>.md) — one-line hook
```

The index is curated. Stale or superseded entries get removed rather
than appended around. New entries get added in semantic groupings,
not chronologically.

## How entries link

Topic files link to related topic files with `[[name]]` references,
where `name` is the other file's frontmatter slug. The linkage forms
a small graph: a feedback entry about "prefer pnpm over npm" links to
a reference entry about "kit consumers ensure dist via pre-X hooks";
the latter links back. The assistant follows these on demand when
relevant.

A `[[name]]` that doesn't match an existing file is not an error — it
marks a topic worth writing later.

## Redaction

Each file in this subtree is a copy of a private memory file with
private content stripped. In addition to the general redaction rules
(see [`../claude-md/README.md`](../claude-md/README.md#redaction)):

- **Memory entries citing private paths.** Strip rooted paths past
  the subproject name. "See the legal filing hub" survives; the
  rooted path does not.
- **Memory entries citing private participants.** Opposing-party
  names, children's names, private addresses, docket numbers — all
  stripped.
- **`user_*` entries.** Excluded entirely from this mirror. The
  namespace is reserved for operator profile entries that are
  inherently personal.

On present estimates a majority of the private tree is publishable
under those rules — but the figure is an estimate, not a count of
anything shipped, because nothing has shipped.

## Refresh cadence

None yet — see [Status](#status--placeholder-not-yet-populated). Once
the allow-list lands the cadence is weekly: the private auto-memory
tree stays the source of truth and this subtree mirrors it. The sync
script runs the redaction sweep + a never-publish path bar before each
publish; promotion to GitHub happens through a separate push wrapper.

The index changes more often than the topic files — adding a new
entry typically means writing one new file and adding one line to
the index. Trimming superseded entries means removing the file and
the line in the same edit.

## How to read

Start with `MEMORY.md`. Scan the namespace prefixes — `feedback_*`
lines describe how the assistant should approach work in this
project; `project_*` lines describe what the project actually *is*;
`reference_*` lines point at external resources; an `index_*` line is
a doorway into a domain that outgrew the top-level index, and is worth
following first when that domain is what you came for. Click through to
a topic file when its one-line description names something relevant.

The collection is heterogeneous on purpose. It mirrors how the
assistant actually uses it: load the index, pull relevant entries
on demand, leave the rest unloaded until needed.

## License

MIT — see `../LICENSE-MIT` at the umbrella root. Prose and
AI-agentic workflow files fall under the MIT side of the two-license
pair.
