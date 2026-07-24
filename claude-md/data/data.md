# data/

**Role:** qagents monorepo's cross-subproject data hub. Holds artifacts
that serve more than one subproject OR are explicitly recognized
cross-cutting machinery (schedules, specs, hints, summaries, renders,
status). Every top-level entry must be exactly one closed-set **kind**;
every entry must have a documented **producer-of-record**; every entry
must carry a `data/<X>/CLAUDE.md` declaring producer + consumers +
schema + refresh cadence + write-lock posture.

Design rationale: `data/specs/data-charter-2026-05-17/SPEC.md` (this file
owns the live rules — the closed-set kinds, three-question gate,
single-owner rule, audit table, and stub template below).

## 1. Closed-set kinds

Every top-level `data/<X>/` is exactly one of:

| Kind | Purpose | Examples |
|---|---|---|
| **data-hub** | Producer-emitted dataset consumed by ≥ 2 subprojects | `data/donating/`, `data/publishing/`, `data/visualizing/`, `data/agent-sdk-ledger/` |
| **convention-anchor** | Cross-cutting machinery shared by every subproject | `data/schedules/`, `data/specs/`, `data/claude-updates/`, `data/summaries/`, `data/tmp/` |
| **render-cache** | Wholesale-regenerated handoff bundles or staging mirrors of an external destination | `data/renders/` |
| **status-emit** | Per-subproject status snapshots aggregated by `designing/web` | `data/status/` |
| **letter-binding** | Per-date letter / correspondence bundles produced by a single legal-side subproject | (reserved — none today) |

The kind labels are the contract; the closed set is intentionally
small. If a candidate entry doesn't cleanly fit one of these, it
probably doesn't belong under `data/` — the three-question gate fires
(§ 2).

## 2. Three-question gate

Before creating `data/<NEW>/`, the author must answer **YES** to at
least one of:

1. **Multi-consumer?** Will ≥ 2 subprojects read this?
2. **Recognized cross-cutting?** Is it a convention-anchor or
   render-cache in the closed set (§ 1)?
3. **Producer-of-record committed?** Is the producer-of-record
   script added in the same PR, with a `data/<NEW>/CLAUDE.md` stub?

If all three are NO → the artifact belongs in the originating
subproject's own directory tree, not under `data/`.

Ledger-shaped candidates (one shared file, many appenders) never pass
this gate as files — they start as a shared-ledger-store table + rendered
git projection (`data/specs/shared-ledger-store-2026-07-09/SPEC.md` § 2/§ 5).

## 3. Single-owner rule — what every `data/<X>/CLAUDE.md` carries

Every top-level entry's `CLAUDE.md` states:

1. **Kind** — one of the closed-set labels (§ 1).
2. **Producer-of-record** — absolute path of the script (or "manual")
   that authors the contents.
3. **Consumers** — subprojects that read the contents, with read-path
   modules / `file:line` references.
4. **Schema** — pinned shape (column list for parquet, top-level JSON
   keys for JSON, file-layout convention for markdown bundles).
5. **Refresh cadence** — manual / cron / per-session / per-commit.
6. **Write-lock posture** — `.data-write-lock` acquired (manual
   writers, per `data/specs/data-conventions-2026-05-06/SPEC.md` § 5.3) vs
   `pending/`-mirrored (cron lane, per § 4) vs neither (read-only
   mirrors).

When ownership is ambiguous, the entry doesn't ship.

## 4. Audit table

Authoritative status of every top-level entry. Update whenever a new
entry lands or an existing one's verdict flips.

| Entry | Kind | Producer | CLAUDE.md |
|---|---|---|---|
| `agent-sdk-ledger/` | data-hub | `code/agent_sdk/qagents/agent_sdk/ledger.py` (append-only, per SDK call) | `data/agent-sdk-ledger/CLAUDE.md` |
| `charters/` | convention-anchor | sessions — charters by ratifying debate + spec-lane amendment (`data/specs/data-charters-2026-07-16/SPEC.md` § 3.3/§ 4.4); migrated spec families/debate records by the owner-scope's `/open` session; `todos/` fix-requests by session/operator (charter-scopes-2026-07-16 § 4) | `data/charters/CLAUDE.md` |
| `claude-settings/` | convention-anchor | manual `sources/*` → `scripts/claude-settings/build.py` | `data/claude-settings/CLAUDE.md` |
| `claude-updates/` | convention-anchor | `scripts/close.sh` | `data/claude-updates/CLAUDE.md` |
| `debates/` | convention-anchor | sessions (debate convener at `/close`) | `data/debates/CLAUDE.md` |
| `donating/` | data-hub | `donating/scripts/emit.mjs` | `data/donating/CLAUDE.md` |
| `messaging-rulings/` | convention-anchor | `pleading/` gate pass — CLEARED subset of `data/debates/messaging-hardening-<date>.md`, promoted at `/close` | `data/messaging-rulings/CLAUDE.md` |
| `next-steps/` | convention-anchor | `python -m qagents.ledger render-next-steps` — GENERATED renders of `ledger.ns_item_event`; writes via the `ns-*` verbs, gated by `scripts/close.sh --next-steps` (session-lifecycle charter § 2.8; `templates/` + `terminals/` stay hand-edited) | `data/next-steps/CLAUDE.md` |
| `publishing/` | data-hub | `publishing/scripts/videos_emit.mjs` (videos roster → `/videos`) | `data/publishing/CLAUDE.md` |
| `renders/` | render-cache (render-cache → render-output transition; see `data/renders/CLAUDE.md`) | `rendering/` engines (migrated consumers) / designer handoff wholesale-regen (legacy bundles) | `data/renders/CLAUDE.md` |
| `schedules/` | convention-anchor | manual (`launchd/install.sh` ROUTINES) | `data/schedules/CLAUDE.md` |
| `signoffs/` | convention-anchor (**slot hub** — single-owner per `<gate-id>/` slot, the `status/` pattern) | sessions via `/do-signoff` — each gate's sole grantor writes its own slot | `data/signoffs/CLAUDE.md` |
| `specs/` | convention-anchor | manual (session-promoted from `data/tmp/`) | `data/specs/CLAUDE.md` |
| `status/` | status-emit | per-sub `scripts/status_emit.*` | `data/status/CLAUDE.md` |
| `summaries/` | convention-anchor | `scripts/{close,dcu,dco}.sh` + axiomatization-lane drivers (full roster in the stub) | `data/summaries/CLAUDE.md` |
| `tmp/` | convention-anchor | sessions (in-flight specs) | `data/tmp/CLAUDE.md` |
| `visualizing/` | data-hub | `visualizing/extractor/*.py` (Phase 1) → `dau`/`dat` driver-emit (Phase ≥3) | `data/visualizing/CLAUDE.md` |

**Promoted out:** market/trading datasets (parquet/portfolios/reports/gics)
moved to the top-level `financial/` hub — see root `CLAUDE.md` § "Shared-data
hubs".

## 5. Stub template

```markdown
# data/<X>/

**Kind:** <data-hub | convention-anchor | render-cache | status-emit | letter-binding>
**Producer-of-record:** <abspath/to/script.py | manual | sessions>
**Consumers:** <sub> (<file:line>), <sub> (<file:line>), …
**Schema:** <column list | JSON keys | file-layout convention>
**Refresh cadence:** <manual | cron <name> @ HH:MM | per-session | per-commit>
**Write-lock posture:** <.data-write-lock acquired | pending/ mirrored | none (read-only)>

<one-paragraph prose: what this directory holds, who reads it, when it
changes. Cross-references to the producer script + consumer modules
+ load-bearing prior spec(s).>
```

## 6. Not a session anchor

No session ever opens `/open data` — `data/` is not a subproject; this
file is a reference doc, not a session anchor. Editing it during any
`/open <sub>` session is allowed when the audit table needs an entry
flip or a new top-level kind is being added.
