# data/tmp/

**Kind:** convention-anchor
**Producer-of-record:** sessions (in-flight specs land here at
`data/tmp/<slug>-<date>.md` or `data/tmp/<slug>-<date>/SPEC.md` per
the adopted-spec convention)
**Consumers:** sessions until the spec is promoted to `data/specs/`;
`managing/` (daily `specs-audit.sh` pass — proposal age + orphan
detection)
**Schema:** one `<slug>-<date>.md` per in-flight spec; optionally a
`<slug>-<date>/` directory with `SPEC.md` + scratch artifacts
**Refresh cadence:** per-session; entries are short-lived (relocate
to `data/specs/` once adopted)
**Write-lock posture:** `.data-write-lock` (manual lane) — single
session writes during draft; promotion is a separate `git mv` inside
`/close`

Replaced the legacy root-level `tmp/` directory when the tmp+summaries
reorg landed (`data/specs/data-conventions-2026-05-06.md` § 14).

---

## Proposal lifecycle

A `data/tmp/<slug>-<date>.md` entry is in one of three states; the
daily `specs-audit.sh` pass classifies each entry and surfaces it in
`managing/checks/<date>.md` under `## tmp/ proposal status`.

| state               | criterion                                                                                 | watcher action                       |
|---------------------|-------------------------------------------------------------------------------------------|--------------------------------------|
| **in-flight**       | file mtime ≤ **7 days**                                                                   | listed; no finding                   |
| **stale**           | file mtime > **7 days** AND **no successor** in `data/specs/`                             | listed as **orphan candidate**       |
| **adopted-orphan**  | the slug appears as a section header or status line in any `data/specs/*.md`              | listed as **adopted-orphan** — MUST be deleted |

The 7-day threshold matches the "long-running entries with no
promotion path are a code smell" rule that the prior version of this
file gestured at — quantified now so the audit can act on it.

### Adopted-orphan detection

When a spec is promoted to `data/specs/<slug>-<date>.md`, the
corresponding `data/tmp/<slug>-<date>.md` (or `data/tmp/<slug>-<date>/`)
MUST be removed in the same commit. The audit looks for the inverse:
a `tmp/` entry whose **basename** (stripping `.md` and any `/SPEC.md`
suffix) matches a `data/specs/*.md` filename. Any match is an
`adopted-orphan` — the promotion was incomplete; cleanup pending.

### Authoring scratch (subdirectory form)

When a draft needs more than one file (planning subagent outputs,
sample artifacts, diagrams), use the subdirectory shape:

```
data/tmp/<slug>-<date>/
├── SPEC.md         # the load-bearing draft (single point of truth)
├── …               # supporting artifacts (sketches, sample JSON, etc.)
└── background/     # optional — research notes, prior-session digests
```

The audit identifies the proposal by `<slug>-<date>/SPEC.md` (mtime of
that file is the age). Subdirectories `.log` files and adjacent
`-attempt-N` files do not trigger orphan flags on their own — they're
session-scoped scratch.

### Promotion checklist (for the human running `/close`)

1. `git mv data/tmp/<slug>-<date>.md data/specs/<slug>-<date>.md`
   (or the directory equivalent if subdir form).
2. Edit the promoted spec's `**Status:**` line to `adopted` and add
   the `**Tests:**` line per `data/specs/CLAUDE.md`.
3. If tests exist, `git mv` (or `mkdir -p`) the
   `<slug>-<date>-tests/` directory under `data/specs/`.
4. Update consumers (skills, sibling specs, subproject CLAUDE.mds)
   to cite the new `data/specs/<slug>-<date>.md` relpath.
5. Verify `data/tmp/<slug>-<date>{.md,/}` no longer exists — the
   audit will flag it otherwise.

Step 5 is the failure mode the audit catches: missed-cleanup. Step 4
is the failure mode `/do-claude-updates` later handles when stale
relpaths surface in cross-subproject hint files.
