# data/tmp/

**Kind:** convention-anchor
**Producer-of-record:** sessions (in-flight specs land here at
`data/tmp/<slug>-<date>.md` or `data/tmp/<slug>-<date>/SPEC.md`)
**Consumers:** sessions until the spec is promoted to `data/specs/`; the
daily watcher's spec audit (proposal age + orphan detection)
**Refresh cadence:** per-session; entries are short-lived (relocate to
`data/specs/` once adopted)
**Write-lock posture:** the data write-lock during draft; promotion is a
separate `git mv` inside `/close`

## Proposal lifecycle

A `data/tmp/<slug>-<date>.md` entry is in one of three states; the daily
audit classifies each and surfaces it:

| state | criterion | watcher action |
|---|---|---|
| **in-flight** | file mtime ≤ 7 days | listed; no finding |
| **stale** | mtime > 7 days AND no successor in `data/specs/` | orphan candidate — adopt or delete |
| **adopted-orphan** | the slug appears as a section header or status line in any adopted spec | MUST be deleted — promotion was incomplete |

### Adopted-orphan detection

When a spec is promoted to `data/specs/<slug>-<date>.md`, the corresponding
`data/tmp/<slug>-<date>.md` MUST be removed in the same commit. The audit
looks for the inverse: a `tmp/` entry whose basename matches an adopted spec
filename. Any match is an adopted-orphan — cleanup pending.

### Authoring scratch (subdirectory form)

When a draft needs more than one file, use the subdirectory shape: a
`SPEC.md` (the single point of truth) plus supporting artifacts and an
optional `background/`. The audit identifies the proposal by the `SPEC.md`
mtime; session-scoped scratch (`.log` files, `-attempt-N` files) doesn't
trigger orphan flags on its own.

### Promotion checklist (for the human running `/close`)

1. `git mv` the draft into `data/specs/`.
2. Edit the promoted spec's `Status` line to `adopted` + add the `Tests`
   line.
3. `git mv` (or create) the companion tests directory.
4. Update consumers (skills, sibling specs, subproject CLAUDE.mds) to cite
   the new relpath.
5. Verify the `tmp/` entry no longer exists — the audit flags it otherwise.

Step 5 is the missed-cleanup failure mode the audit catches; step 4 is the
stale-relpath failure mode `/do-claude-updates` later handles.
