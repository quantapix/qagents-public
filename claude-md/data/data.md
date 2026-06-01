# data/

**Role:** the monorepo's cross-subproject data hub. Holds artifacts that
serve more than one subproject OR are explicitly recognized cross-cutting
machinery (schedules, specs, hints, summaries, renders, status). Every
top-level entry must be exactly one closed-set **kind**; every entry must
have a documented **producer-of-record**; every entry must carry a
`data/<X>/CLAUDE.md` declaring producer + consumers + schema + refresh
cadence + write-lock posture.

## 1. Closed-set kinds

Every top-level `data/<X>/` is exactly one of:

| Kind | Purpose |
|---|---|
| **data-hub** | producer-emitted dataset consumed by ≥ 2 subprojects |
| **convention-anchor** | cross-cutting machinery shared by every subproject (schedules, specs, claude-updates, summaries, tmp, next-steps) |
| **render-cache** | wholesale-regenerated handoff bundles or staging mirrors of an external destination |
| **status-emit** | per-subproject status snapshots aggregated by the site |
| **letter-binding** | per-date correspondence bundles from a single subproject (reserved) |

The kind labels are the contract; the closed set is intentionally small. If
a candidate doesn't cleanly fit one, it probably doesn't belong under
`data/`.

## 2. Three-question gate

Before creating `data/<NEW>/`, the author must answer **YES** to at least
one of: (1) multi-consumer — will ≥ 2 subprojects read this? (2) recognized
cross-cutting — is it a convention-anchor or render-cache in the closed
set? (3) producer-of-record committed — is the producer script added in the
same change, with a `CLAUDE.md` stub? If all three are NO, the artifact
belongs in the originating subproject's own tree.

## 3. Single-owner rule

Every top-level entry's `CLAUDE.md` states its **kind**,
**producer-of-record** (the script path or "manual"), **consumers** (with
read-path modules), **schema** (column list / JSON keys / file layout),
**refresh cadence** (manual / cron / per-session / per-commit), and
**write-lock posture** (acquires the data write-lock / `pending/`-mirrored /
read-only). When ownership is ambiguous, the entry doesn't ship.

## 4. Audit table

An authoritative table records every top-level entry's kind + producer +
CLAUDE.md, updated whenever an entry lands or its verdict flips. Two
notable promotions out of `data/`: the market/trading datasets (parquet /
portfolios / reports / GICS) moved to a top-level `financial/` hub — a
domain peer governed by its own CLAUDE.md graph, sharing the root data
write-lock; and the public-org staging mirror moved to the `publishing/`
subproject — it was a working tree, not a multi-consumer dataset, so it
left `data/` entirely.

## 5. Not a session anchor

No session ever opens `/open data` — `data/` is not a subproject; this file
is a reference doc. Editing it during any session is allowed when the audit
table needs a flip or a new top-level kind is being added.
