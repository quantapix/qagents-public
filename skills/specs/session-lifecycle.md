# Session lifecycle — the charter, condensed

Condensed public-safe rendering of the private session-lifecycle charter (the
authoritative contract behind the `open` / `close` / `do-claude-updates` skill
bodies in this subtree). The dated spec files that preceded the charter are
retired; this render tracks the charter.

## Contract

Every session starts with `/open <project>` and ends with
`/close [--to-main]`. The session's git branch IS the write-lock; closing
merges work back toward `main` and tears the worktree down. Memory writes and
per-project rule-file updates ride on the close; cross-subproject implications
stage as hints that a later `/do-claude-updates` flush judges with the whole
tree in view. Everything lands on `main` with assistant-authored commit
messages and zero manual git plumbing.

Five standing guarantees:

1. **Three-layer model** — charter (contract) → mechanics (scripts, now a
   native binary behind a path-stable shim) → thin orchestrator skills.
   Mechanics is the single source of truth for executable phases.
2. **Uniform footer** — every verb ends with a `<project> <verb> complete`
   footer + a summary table, captured to an append-only summaries archive.
3. **Zero-prompt noop close** — an `/open` immediately followed by `/close`
   fires zero permission prompts and leaves the git graph untouched apart
   from the open-record and close-footer commits.
4. **Forward-only next-steps** — one forward-looking slot per project lists
   what's left; resolved items are deleted to bare numbering gaps;
   resolution detail lives only in close summaries. The slots are generated
   projections of a shared ledger store — writes go through typed verbs,
   never hand edits.
5. **Canonical-edit lock hook** — while any worktree is active, edits
   addressed to the canonical checkout are hard-blocked: a canonical edit
   would land on `main`, silently bypassing the lock.

The lock is conventional, not enforced cross-process (single-maintainer
machine); branch-presence checks guard the entry path and a hook adds
in-process enforcement.

## Why it is shaped this way

- **Branch-as-lock** makes parallel sessions cheap and conflicts structural:
  a second `/open` of the same project stacks a numbered branch off its
  predecessor rather than colliding.
- **Worktree-path discipline** is load-bearing: which working tree a write
  lands in is decided by the file path, so the tooling pins every write to
  the worktree root and blocks the canonical form.
- **Hints over live edits**: a session that learns something about another
  subproject queues a hint instead of editing foreign files; the flush verb
  later judges every hint with full context, applying, adapting, or
  dropping each on the record.

## License

MIT — see `../../LICENSE-MIT` at the umbrella root.
