# memory/

The redacted mirror of the AI-assistant auto-memory tree — the topic
files the assistant writes during sessions and loads back across
sessions to stay coherent. Refreshed weekly from the private source.

See the [umbrella README](../README.md) for the broader thesis.
Sibling subtrees: [`claude-md/`](../claude-md/),
[`memsearch/`](../memsearch/).

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

## Layout

```
memory/
  MEMORY.md               redacted index (same filename as the canonical)
  feedback_*.md           guidance the operator has given about how to work
  project_*.md            ongoing-project context (decisions, milestones, plans)
  reference_*.md          pointers to external systems (docs, URLs, gotchas)
```

A fourth namespace (`user_*`) is reserved by the auto-memory system
for operator profile entries but is currently empty.

## The three namespaces

Each topic file carries frontmatter (name, description, type). The
description is what the index line summarises; the type drives where
the assistant looks for it.

- **`feedback_*`** — Guidance the operator has given about how to
  approach work. Both corrections ("don't mock the database in these
  tests") and validations ("yes, that bundled PR was the right
  call"). Saved when the operator explicitly approves or pushes back,
  with a `**Why:**` line and a `**How to apply:**` line so the
  assistant can judge edge cases. The broadest publishable category
  here — about 100–120 of the ~140 entries are public-safe
  engineering / authorship discipline. The rest touch litigation
  workflow, redaction-blocklist mechanics, or operator-personal
  posture and stay private.
- **`project_*`** — Ongoing context: who is doing what, why, by
  when. Decisions, milestones, scope notes. About 30 of the ~38
  entries publish (the remainder are litigation-specific). Each
  carries the same `**Why:**` / `**How to apply:**` shape as feedback
  entries so future sessions can judge whether the memory is still
  load-bearing.
- **`reference_*`** — Pointers to external systems and third-party
  resources. URLs, public docs, API gotchas, vendor quirks. About
  80–100 of the ~122 entries publish (the remainder cite private
  dockets, IAM specifics, per-host paths).

The published set is curated, not exhaustive. An entry that names
private participants, private paths, or private infrastructure is
either redacted to remove those references or dropped from the public
mirror entirely.

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

The published set after redaction is roughly 200–250 files out of
~300 in the private tree.

## Refresh cadence

Weekly. The private auto-memory tree is the source of truth; this
subtree mirrors. The sync script runs the redaction sweep + diff
before each publish; promotion to GitHub happens through a separate
push wrapper.

The index changes more often than the topic files — adding a new
entry typically means writing one new file and adding one line to
the index. Trimming superseded entries means removing the file and
the line in the same edit.

## How to read

Start with `MEMORY.md`. Scan the namespace prefixes — `feedback_*`
lines describe how the assistant should approach work in this
project; `project_*` lines describe what the project actually *is*;
`reference_*` lines point at external resources. Click through to a
topic file when its one-line description names something relevant.

The collection is heterogeneous on purpose. It mirrors how the
assistant actually uses it: load the index, pull relevant entries
on demand, leave the rest unloaded until needed.

## License

MIT — see `../LICENSE-MIT` at the umbrella root. Prose and
AI-agentic workflow files fall under the MIT side of the two-license
pair.
