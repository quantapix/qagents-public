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
(+ optional `background/` research notes)
**Refresh cadence:** per-session; entries are short-lived (relocate
to `data/specs/` once adopted)
**Write-lock posture:** `.data-write-lock` (manual lane) — single
session writes during draft; promotion is a separate `git mv` inside
`/close`

**Single normative owner: `data/charters/qagents/spec-lifecycle/CHARTER.md`
§ 2.7** — this stub keeps only what is needed at the moment of touching the
dir; on any divergence the charter wins. `data/tmp/` itself is unrestricted
(both draft forms valid, no tmp-side shape rule); conformance is enforced
**at promotion**. The promotion target is always `data/specs/<slug>-<date>/`
— new specs never land scope-side under `data/charters/<scope>/specs/`
(that root only receives closed families via the § 2.4 location transition;
charter-scopes-2026-07-16).

## Proposal states (charter § 2.7; audit classifies daily)

| state | criterion | watcher action |
|---|---|---|
| **in-flight** | age ≤ **7 days** (slug-date preferred over mtime) | listed; no finding |
| **stale** | age > **7 days** AND no successor in `data/specs/` | orphan candidate |
| **adopted-orphan** | slug matches a family dir or subspec basename under `data/specs/` | MUST be deleted — promotion was incomplete |

The audit identifies a dir-form proposal by `<slug>-<date>/SPEC.md`;
`.log` files and `-attempt-N` scratch never trigger orphan flags.

## Promotion checklist (charter § 2.7)

1. Dir-form: `git mv data/tmp/<slug>-<date> data/specs/<slug>-<date>`
   (tests + TODO travel). Flat-form: `mkdir` the family dir + `git mv`
   the file to `SPEC.md` inside. Amendment/subspec: `git mv` **into**
   the family dir under the de-prefixed name + add `**Parent:** ../SPEC.md`.
2. Fix non-conforming pieces in the same commit — including the
   `background/` scratch dir (relocate/delete, or register a cited
   carve-out row; a promoted `background/` subdir is otherwise a layout
   finding).
3. `**Status:**` → `adopted`; `**Tests:**` set (`tests/` or
   `none — design-only`); SPEC.md ≤ 1,000 lines.
4. Consumers re-pointed to the new `data/specs/<slug>-<date>/SPEC.md`
   relpath (stragglers: `/do-claude-updates`).
5. `data/tmp/<slug>-<date>{.md,/}` gone in the same commit — else the
   audit flags an adopted-orphan.
