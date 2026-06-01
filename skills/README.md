# skills/

The session-lifecycle + context-optimization skills that govern every
AI-assistant session inside the qagents working tree, plus the adopted
specs they implement. Redacted public mirror, refreshed weekly from the
private source.

See the [umbrella README](../README.md) for the broader thesis; the
session-lifecycle discipline is theme 4 (parallel sessions via worktrees)
and the optimization discipline is theme 5 (context-window optimization).
Sibling subtree: [`claude-md/`](../claude-md/).

## What a skill is

A Claude Code **skill** is a named, invocable procedure (`/open`, `/close`,
…). In qagents the lifecycle skills are deliberately **thin orchestrators**:
the mechanical, deterministic steps live in a shell script, and the SKILL.md
interleaves only the *judgment* steps that need an LLM in session context
(writing a session summary, deciding which CLAUDE.md edits a hint implies,
curating the memory index). The script is the source of truth; the skill
narrates the judgment.

## The four skills

| Skill | Role |
|---|---|
| [`open`](./open/SKILL.md) | Provision a write-locked session — a git branch + worktree for one project. The branch IS the write-lock. |
| [`close`](./close/SKILL.md) | End a session — summary, memory update, immediate CLAUDE.md edits, queued cross-subproject hints, status emit, next-steps gate, merge up the stack. |
| [`do-claude-updates`](./do-claude-updates/SKILL.md) | Flush queued cross-subproject CLAUDE.md hints in full-tree context, periodically, after several close cycles. |
| [`do-claude-optimizations`](./do-claude-optimizations/SKILL.md) | The "shrinking" half — a fan-out trim pass that keeps the memory index and every CLAUDE.md under the harness's load-truncation caps. |

`open` / `close` / `do-claude-updates` *add* content over time; `do-claude-
optimizations` is the continuous trim that keeps the whole graph under the
caps that would otherwise silently truncate at session load. Together they
are the lifecycle: open → work → close (× N) → periodic flush + trim.

## The adopted specs ([`specs/`](./specs/))

- [`open-close-dcu-<date>.md`](./specs/) — the consolidated open / close /
  do-claude-updates triad: the lock model, the stack, the per-hop cascade,
  the canonical-edit hook, the close-time status + next-steps gates.
- [`dco-<date>.md`](./specs/) — the do-claude-optimizations fan-out: the
  digester-per-CLAUDE.md + memory-index parallel pass, the sequential
  cross-cutting digester, the apply-plan, and the dry-run-first safety gate.

Both are redacted public renderings — faithful on design, phase ledger, and
contracts; operator-specific absolute paths are genericized to `<repo>` /
`<worktree>`.

## Redaction

Operator home paths (`<repo>`, `<worktree>`) and host-specific identifiers
are genericized; the engineering content — exit-code contracts, phase
sequences, hook behavior — is preserved, because that *is* the methodology
this repo exists to publish.

## License

MIT — see `../LICENSE-MIT`. Prose + AI-agentic workflow files fall under the
MIT side of the two-license pair.
