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

## Proposal lifecycle

A `data/tmp/<slug>-<date>.md` entry is in one of three states; the
daily `specs-audit.sh` pass classifies each entry and surfaces it in
`managing/checks/<date>.md` under `## tmp/ proposal status`.

| state               | criterion                                                                                 | watcher action                       |
|---------------------|-------------------------------------------------------------------------------------------|--------------------------------------|
| **in-flight**       | file mtime ≤ **7 days**                                                                   | listed; no finding                   |
| **stale**           | file mtime > **7 days** AND **no successor** in `data/specs/`                             | listed as **orphan candidate**       |
| **adopted-orphan**  | the slug appears as a family directory name or subspec basename under `data/specs/`       | listed as **adopted-orphan** — MUST be deleted |

### Adopted-orphan detection

When a spec is promoted to `data/specs/<slug>-<date>/SPEC.md` (family
form — `specs-family-layout-2026-06-10/SPEC.md` § 4), the corresponding
`data/tmp/<slug>-<date>.md` (or `data/tmp/<slug>-<date>/`) MUST be
removed in the same commit. The audit looks for the inverse: a `tmp/`
entry whose **basename** (stripping `.md` and any `/SPEC.md` suffix)
matches a family directory name or a subspec directory basename. Any
match is an `adopted-orphan` — the promotion was incomplete; cleanup pending.

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

Both draft forms stay valid here; conformance is enforced **at
promotion** — the promoted spec must arrive in `data/specs/` in full
family form (`specs-family-layout-2026-06-10/SPEC.md` § 4).

1. Dir-form draft: `git mv data/tmp/<slug>-<date>
   data/specs/<slug>-<date>` (tests + TODO travel with it; fix any
   non-conforming pieces in the same commit). Flat-form draft:
   `mkdir data/specs/<slug>-<date>` + `git mv` the file to `SPEC.md`
   inside. Amendment/subspec: `git mv` **into** the family directory
   under the de-prefixed name and add the `**Parent:** ../SPEC.md`
   line.
2. Edit the promoted SPEC.md's `**Status:**` line to `adopted` and
   set the `**Tests:**` line (`tests/` or `none — design-only`) per
   `data/specs/CLAUDE.md`; SPEC.md must be ≤ 1,000 lines.
3. If tests exist, land them as `data/specs/<slug>-<date>/tests/`
   (suite files under `cases/`).
4. Update consumers (skills, sibling specs, subproject CLAUDE.mds)
   to cite the new `data/specs/<slug>-<date>/SPEC.md` relpath.
5. Verify `data/tmp/<slug>-<date>{.md,/}` no longer exists — the
   audit will flag it otherwise.

Step 5 is the failure mode the audit catches: missed-cleanup. Step 4
is the failure mode `/do-claude-updates` later handles when stale
relpaths surface in cross-subproject hint files.
