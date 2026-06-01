# publishing — the open-source release subproject

Project-specific rules for the open-source release subproject — the one
that produces *this* repo (and its siblings under the public org).
Cross-project rules: root `CLAUDE.md`.

## 1. Purpose

`publishing/` is the **single owner** of open-sourcing the qagents
framework — the drive's open-sourcing promise. It renders, redacts,
compiles, and pushes the public GitHub repos. After this subproject, **no
other subproject carries any open-sourcing responsibility** — each keeps
only its own internal status emit.

## 2. What it owns / does not own

**Owns:** the public-org staging tree (the org-profile slot + every
`<repo>-public/` working tree that mirrors the live org); the `/publish`
pipeline (sweep → collect → verify/redact → compile → push); the external
push surface (the only allowed push to the public org); the drive's
open-sourcing promise; the redaction-clean gate before any push.

**Does not own:** drive content (the drive doc is the source of truth —
publishing reads it, never edits it); the hosted verification service; the
axiom authoring; the internal status hub (each subproject self-emits);
Astro-site deploys.

## 3. Boundary posture

Content-in / external-out — the same shape the donation subproject has,
plus a push surface. `publishing/` imports no sibling code and none import
from it. Inbound is **content only** — public-safe renderings of the study,
video, legal-kernel, financial-kernel, and donation subprojects, plus the
root CLAUDE.md graph and the session-lifecycle skills. Outbound is the
public GitHub org only. It is **not observe-only**: it writes its own
subtree and pushes to the external org, but it never commits/pushes the
qagents repo outside the standard interactive-lane audit gate, and never
mutates any sibling subproject's tree.

## 4. The `/publish` pipeline

Triggered by the `/publish` skill (a thin orchestrator over a mechanics
script + an Opus collector fan-out). Five phases: preflight → sweep (one
collector subagent per source subproject) → verify/redact (a HARD gate) →
compile → push (operator-confirmed). No cron lane at v0.1 — the weekly
cadence is operator-run.

## 5. Redaction is a hard gate, not advisory

A non-empty result from the document-redaction sweep over the candidate
tree **aborts** the compile/push. `publishing/` inherits the constellation's
redaction rules; it invents none and relaxes none — the same load-bearing
privacy floor the donation subproject names. The gate is wired before the
push and pinned by a companion test.

## 6. Write-lock & session model

- **Branch-as-lock.** `/open publishing` creates the branch + worktree;
  every Edit/Write path begins with the worktree root (the canonical-edit
  hook).
- The status emit is a fixed-path producer under the shared-data hub, so it
  acquires the data write-lock when writing canonical.
- **The external push** is not a qagents-repo write — no qagents lock
  involved; its scratch clones live outside the tree.
- The per-source collector digests land in a gitignored, fork-internal
  buffer that is never promoted by the watcher's verifier and is discarded
  at close by default.

## 7. Status emit

The producer participates in the status contract. Four-state pill: `OK`
(last publish clean) / `BUILDING` (run in flight) / `DEGRADED` (last run
aborted on the redaction/drift gate — privacy floor held, release stale) /
`NOT_YET_LIVE` (pre-first-publish). The summary diagram is the five-stage
pipeline; a table emit carries the repo roster.
