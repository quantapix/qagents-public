# claude-md/

The redacted mirror of the `CLAUDE.md` graph that governs every
AI-assistant session inside the qagents working tree. One file per
published `CLAUDE.md`, refreshed weekly from the private source.

See the [umbrella README](../README.md) for the broader thesis.
Sibling subtrees: [`skills/`](../skills/) (the session-lifecycle + optimization
skill bodies + their adopted specs), [`memory/`](../memory/),
[`memsearch/`](../memsearch/), [`specs/`](../specs/).

## What a `CLAUDE.md` is

A `CLAUDE.md` is the file the AI assistant reads at session start. It
pins the project-specific rules, invariants, and caveats the assistant
needs to act safely inside that scope. Each subproject has one. The
root has one (cross-boundary conventions only — language split,
canonical bar shape, GICS mapping, status hub, session lifecycle).
The shared-hub directories (`data/`, `data/specs/`, `data/tmp/`)
each have one too.

Together, the graph defines the *operating envelope* the assistant
moves inside. Edit one file, you change one session's behaviour next
load. Edit the root, you change every session's.

## Layout

```
claude-md/
  root.md                 redacted root CLAUDE.md (cross-subproject conventions only)
  <sub>.md                one per published subproject
  data/                   shared-hub conventions (infrastructure, not subprojects)
    README.md             this sub-grouping's own note
    data.md               redacted data/CLAUDE.md         (kind: data-hub charter)
    specs.md              redacted data/specs/CLAUDE.md   (kind: convention-anchor)
    tmp.md                redacted data/tmp/CLAUDE.md     (kind: convention-anchor)
```

`<sub>.md` files are named after the private subproject they mirror.

## Which subprojects publish

This first cut is **product-focused** — the subprojects behind the two
shipping products plus the core infrastructure they ride on. The rest of
the publishable graph lands in later weekly refreshes.

Published this round:

- `root.md` — cross-subproject conventions
- `proving`, `accounting` — the two Lean kernels (Qnarre / Qresev)
- `analyzing`, `trading` — the market-inspection + portfolio-management
  surfaces that feed the Qresev financial slice
- `verifying`, `evaluating` — the app shells (Qnarre / Qresev)
- `serving` — infrastructure surface
- `managing` — the constellation watcher
- `publishing` — the open-source release subproject (the one that
  produces these repos)
- `visualizing` — the graphing surface for the three formal kernels (the
  public window onto the kernel-lattice renderer)
- `data/` — the shared-hub conventions (`data.md` / `specs.md` / `tmp.md`)

Added 2026-07-20 (the "publishable but deferred" set, now rendered):
`monitoring`, `studying`, `designing`, `explaining`, `resolving`,
`blending`, `shorting`. `designing` + `explaining` carry surgical
`REWRITES` rules that genericize brand-guard / example-id
meta-references (the same shape `proving` / `verifying` / `evaluating`
already use).

Still deferred (each needs a litigation/editorial call, not a
mechanical rewrite):

- `documenting` — its `CLAUDE.md` carries a section naming
  federal-collateral docket structure (the family barred from every
  public surface by the 2026-07-05 remediation; caught by the
  `publish.sh` gate (1b) content bar). Waits on a `pleading/` redaction
  review.
- `donating` — its `CLAUDE.md` cross-references the litigation-docket
  structure (a state-court matter id alongside the federal wrapper).
  Same gate: waits on a `pleading/` review rather than a generic rewrite.
- `rendering` — not yet on the publishable roster; whether the brand /
  render-engine `CLAUDE.md` belongs on a public surface is an open
  editorial call (a public-surface expansion beyond the settled set).
- The desktop-extension, native-client, and simulation surfaces joined
  the constellation after this subtree's roster was last drawn. None has
  been assessed for publication yet; they are unlisted rather than
  deferred.

Excluded (never published):

- `appealing/`, `pleading/` — pro se litigation surface. Their
  `CLAUDE.md`s name docket structure and filing conventions that aren't
  safe to mirror even redacted. Public-facing legal material routes
  through `documenting/` instead.
- the filing-hub layout (per-court archives, letters-vs-hub split). Same
  reasoning.

## Infrastructure files (`claude-md/data/`)

The shared-hub `CLAUDE.md`s document cross-cutting conventions that
no single subproject owns. They are not subprojects themselves — they
describe the *contracts* between subprojects. The closed-set kind
labels carried in their frontmatter map to the qagents data-hub
charter:

| Kind | Examples in this subtree |
|---|---|
| `data-hub` | `data/data.md` |
| `convention-anchor` | `data/specs.md`, `data/tmp.md` |
| `render-cache` | (none here — render-cache hubs not mirrored) |
| `status-emit` | (none here — per-subproject status emitters) |
| `letter-binding` | (none here — reserved kind) |

Per-subproject `data/<name>/CLAUDE.md` files (e.g. donating's data
slot, the status-emit slot) are *not* mirrored here — they're too
specific; the parent subproject's `CLAUDE.md` already covers them.

## Redaction

Each file in this subtree is a copy of a private `CLAUDE.md` with
private content stripped. The redaction rules:

- **No qagents-rooted paths past a subproject name.** "`proving/`"
  is fine as an engineering-surface reference; "`proving/Proving/<F>/<file>.lean`"
  is not. "The filing hub" survives; "`legal/hub/<docket>/12.pdf`"
  does not.
- **No opposing-party names, no children's names, no private
  addresses, no docket numbers.** The private blocklist that
  enforces this lives outside this repo so this repo itself stays
  safe to mirror.
- **No internal hostnames, no IAM identifiers, no per-host paths.**
- **Engineer-debugging voice throughout.** No activism, no
  exhortations, no rhetorical questions, no marketing exclamations.

A `CLAUDE.md` that cannot be safely redacted is not published.
Litigation-domain files fall in that bucket.

## Refresh cadence

Weekly. The private working tree is the source of truth; this subtree
mirrors. A sync script runs the redaction sweep + diff before each
publish; promotion to GitHub happens through a separate push wrapper.

Re-rankings, new subprojects, and new cross-subproject conventions
land as ordinary diffs — the commit log is the change record.

## How to read

The root file pins what crosses subproject boundaries. Each `<sub>.md`
pins what is local to that subproject. To understand a single
subproject's operating envelope, read both — the root for the
conventions it has to honour, the subproject file for its own rules.
The data subdirectory pins the seams: where shared state lives, who
produces it, who consumes it.

This is the *rule set*, not the implementation. Implementation lives
in the per-subproject public repos.

## License

MIT — see `../LICENSE-MIT` at the umbrella root. Prose and
AI-agentic workflow files fall under the MIT side of the two-license
pair.
