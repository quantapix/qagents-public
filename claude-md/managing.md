# CLAUDE.md — managing/

Project-specific rules for the qagents-constellation daily watcher. Assumes
Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`. Don't
re-litigate those.

## 1. Purpose

`managing/` is a meta-observer over the entire qagents constellation. It runs
once a day (06:00 local, top-tier model, cron-fired) and produces three dated artifacts:

- `checks/YYYY-MM-DD.md` — top **5** issues across consistency / correctness /
  functionality. **Functionality is always highest priority.** A failed live
  probe outranks any consistency or correctness finding regardless of source
  count.
- `tasks/YYYY-MM-DD.md` — **10** most pressing items for the team to tackle
  that day, ranked. Drawn from today's checks, untackled items from yesterday,
  and visible backlog (PLAN.md + Memory.md across subprojects).
- `reports/YYYY-MM-DD.md` — % completion of **yesterday's** checks + tasks,
  with evidence (commit hashes, file changes, closed issues, deploy log lines).

Objective: **keep an eye on the ball.** managing/ does not fix anything. It
surfaces what needs fixing and tracks whether the rest of the constellation is
making progress.

### 1.1 Pinned commitments — what "the ball" actually is

These are the load-bearing objectives the three top-tier-model subagents weight above
generic drift detection (the verifier subagent runs structural checks only,
not pinned-commitment scoring). A miss against any of them is a **functionality**
finding (highest priority).

1. **Firm 6/1/2026 deliverables.** Subagents discover them dynamically via
   `grep -rn -E "2026-06-01|6/1/2026|June 1, 2026" --include="*.md" .` from
   repo root; every match is a deadline anchor. Slip-risk = owning subproject
   has zero commits in the trailing 3 days with `days_remaining ≤ 30`.
2. **Weekly summaries on the public `quantapix` GitHub org.** Any public repo
   under `quantapix/` with `pushedAt` older than 7 days is a finding. The
   org-level profile README is included.
3. **Rapid progress in `studying/` and `explaining/`.** Either subproject
   with zero commits in the trailing 3 days is a finding. Each daily plan
   names the next concrete artifact to land.
4. **`quantapix.com/status` refresh every 3 days.** Any `data/status/<sub>.json`
   slot older than 3 days is a finding. A live `Last-Modified` on
   `https://quantapix.com/status/` older than 3 days is a separate finding
   (deploy stale, not just emit stale).
5. **Donation-drive credibility (active 2026-06-01 → 2026-12-01).** Two
   probes anchored to `donating/drive.md`'s public promises. (a) **Promise-3
   liveness** — once `qnarre.quantapix.com` and `qresev.quantapix.com` are
   live (PLAN Phase 3, ≈ 2026-08), a failed HTTPS sweep on either endpoint
   outranks any non-functionality finding for the day. (b) **Ledger
   cadence** — `donating/ledger/YYYY-MM.md` must land within 5 calendar
   days of each month-end; missing/late ledger past day 5 is a functionality
   finding (drive's whole pitch is *trivially verifiable*). Probe wiring
   goes in `probes.md` once endpoints + the first dated ledger exist; the
   ledger-existence check can land sooner.
6. **Spec hygiene + phase tally.** Every spec document — family-form
   `data/specs/<slug>-<date>/SPEC.md` (+ subspec `<fam>/<sub>/SPEC.md`;
   the only layout since the `specs-family-layout-2026-06-10` Phase 4
   retirement) — is tracked for **uncompleted phases**; every
   `data/tmp/<slug>-<date>{.md,/}` for proposal age + adopted-orphan
   cleanup. The audit script `scripts/specs-audit.sh` is the single
   source of truth (sections: SPECS phase tally / TESTS conformance /
   LAYOUT lint / TMP proposal status / LEDGER manual-check reminders).
   Findings:
   - A `[in-flight]` phase touched > 14 days ago is a **correctness**
     finding (stall risk).
   - A SPEC.md over 1,000 lines (`OVER-CAP` flag in the SPECS section)
     is a **correctness** finding.
   - Any LAYOUT-section finding (root entry that is neither `CLAUDE.md`
     nor a family dir; family subdir that is neither `tests/` nor a
     `SPEC.md`-bearing subspec; subspec missing `**Parent:** ../SPEC.md`
     or root carrying one; nesting deeper than 2) is a **correctness**
     finding.
   - A `tmp/` entry with slug-date > 7d AND no successor in `data/specs/`
     is a **correctness** finding (stale proposal — adopt or delete).
   - A `tmp/` entry whose slug matches an adopted spec in `data/specs/`
     (family dir name or subspec basename) is a **correctness** finding
     (adopted-orphan — promotion cleanup missed).
   - A tests dir (`<fam>[/<sub>]/tests/`) missing `README.md` / `run.sh`
     / `cases/` is a **correctness** finding, but ONLY for slug-date
     ≥ 2026-05-19 (the day the uniform shape landed). Earlier dirs are
     grandfathered per the forward-looking rule in `data/specs/CLAUDE.md`.
   - A LEDGER row with `due_in_days=PAST(Nd)` or `DUE` is a **correctness**
     finding — manual-check reminder derived from spec text (no live AWS
     calls). The note column carries the exact check; surface verbatim.
     Future `Nd` rows are tally-only. New rows are append-only entries in
     the script's `SPEC_LEDGER` TSV.
   The daily tally rides in `checks/<date>.md` as a `## Uncompleted spec
   phases` section + a `## tmp/ proposal status` section + a `## Spec
   ledger reminders` section (see § 8).

These thresholds tighten the generic "14d status hub freshness" guideline in
§ 4. Subagent prompts under `.claude/agents/` encode them verbatim — keep
those in sync if the thresholds change.

The **uniform shape** for specs + tests + tmp/ proposals is pinned in
`data/specs/CLAUDE.md` (spec file shape, tests dir shape, phase markers
protocol) and `data/tmp/CLAUDE.md` (proposal lifecycle + 7-day stale
threshold + adopted-orphan detection). When those rules change, the
thresholds in `scripts/specs-audit.sh` and the bullets above move in
lockstep.

## 2. Three top-tier-model subagents, clean contexts each

The 06:00 cron fires a single coordinator that spawns three top-tier-model subagents +
one Haiku subagent in parallel, each with a clean context. Each subagent owns
exactly one output file (verifier owns two — see below) and writes them
directly to disk. The coordinator only sees their one-line completion
confirmations — **no accumulated context bleed from their work**. This is the
same fork-isolation lever memsearch uses for recall, applied to the watcher's
four concerns.

| Subagent | Model | Output | Inputs | Notes |
|---|---|---|---|---|
| `checker` | fable (top tier) | `checks/<date>.md` | All subprojects (read-only), live websites (WebFetch), public GitHub repos (`gh`) | Three categories: consistency, correctness, functionality. Top 5 total, ranked, functionality first. |
| `planner` | fable (top tier) | `tasks/<date>.md` | Today's `checks/<date>.md`, yesterday's `tasks/`, recent git log, PLAN.md / Memory.md across subprojects | 10 ranked items. May draw from today's checks, yesterday's untackled, or backlog. |
| `reporter` | fable (top tier) | `reports/<date>.md` | Yesterday's `checks/` + `tasks/`, `git log --since=yesterday` across all subprojects, deploy logs | % completion mapped from commits / new files / closed issues. Distinguishes done / in progress / not touched. |
| `verifier` | Haiku 4.5 | `checks/<date>.pending.json` + appended `## Pending verification` section in `checks/<date>.md` | All files under `pending/`; rules table embedded in agent prompt | Closed-set allow-list classifier (default-skip); emits `passes[]` + `internal[]` + `unclassified[]`. Only `passes[]` drives the lock-protected rsync in `data/schedules/launchd/verify-pending.sh` (Layer 2 guards exit 8/9/10 as defense-in-depth). Spec: `data/specs/pending-promotion-scope-2026-05-28/SPEC.md`. Cheap & fast — runs in parallel. |

Subagent definitions live under `.claude/agents/` (created in the new
session). Each one's prompt lists exact inputs to read and the exact output
path to write — they do not negotiate scope with the coordinator at runtime.

## 3. Three categories — what counts

**Consistency** (textual + semantic drift across the constellation):
- Voice mismatches against `feedback_engineer_not_activist_voice.md` (femfas /
  quantapix / Janet copy).
- Naming drift: forbidden-brand-name appearances, product-name typos (Qnarre / Qresev),
  outdated company name.
- CLAUDE.md ↔ memory ↔ visible copy divergence (e.g. CLAUDE.md says deploy
  via `qagents` profile but `.env` pins `quantapix-deploy`).
- Schema drift: a producer emits a field the consumer's Zod schema doesn't
  expect (or vice versa).

**Correctness** (verifiable wrong-ness, not opinion):
- Broken file references in CLAUDE.mds / memory / draft .md (the private filing hub after rename).
- Dead anchor links (`/dockets#tier-X` instead of `/dockets/#tier-X` —
  trailing-slash rule).
- Statutory citations whose the canonical USC text mirror lookup fails.
- Status hub: `data/status/<sub>.json` failing the kit's Zod parse, or
  `kitVersion` drift.
- TS / Lean / Python typecheck regressions visible from `pnpm verify` /
  `lake build` / `pyright` exit codes (don't run them; just check whether
  they were green in the most recent CI / commit log).
- Spec hygiene (per § 1.1 commitment 6 + `data/specs/CLAUDE.md`):
  `[in-flight]` phase > 14d, SPEC.md over 1,000 lines (OVER-CAP), any
  LAYOUT-section lint finding, `tmp/` proposal > 7d without successor,
  adopted-orphan `tmp/` entry, post-2026-05-19 tests dir missing
  required `README.md` / `run.sh` / `cases/`.

**Functionality** (live system state, *highest priority*):
- Live HTTP 200 + non-empty body on a random route from femfas.net or
  quantapix.com.
- `last-modified` not stale by > 30 days vs. the relevant subproject's most
  recent deploy commit.
- Random Playwright spec replay against a live site (single `--grep`).
- Public GitHub repos under `quantapix` org: any failed Actions run within
  the last 24 h.
- Status hub freshness: `data/status/<sub>.json` not stale by > 14 days
  for active subprojects.

A functionality failure is the day's top issue, full stop. Consistency and
correctness fill the remaining 4 slots, ranked by blast radius (legal-record
files > shipped websites > internal docs > backlog).

## 4. Functionality probes — random, weighted

Each run picks 2–3 probes from a weighted pool. **Random selection is
load-bearing** — it prevents the watcher from drifting into a fixed pattern
and missing intermittent failures elsewhere. Pool documented in
`managing/probes.md`.

Probe families + weights + pass/fail predicates live in `managing/probes.md`
(P1..P6 + weight-summary table); checker reads from there. Random seed:
`date +%j` (day-of-year) — deterministic per day, varied across days.
`managing/scripts/probe-pick.sh --k 2` is the picker (pure-awk Fisher-Yates,
no GNU shuf dep).

## 5. Boundaries

Two lanes with different posture. The "observe-only" framing applies
to the cron lane; the interactive lane behaves like any other
qagents subproject session.

### 5.1 Cron lane (the daily watcher)

Observe-only with one tightly-scoped exception — the `pending/`
verification flow (§ 5.3). The 06:00 coordinator and its four
subagents never `git push`, never deploy, never mutate code or copy
in any subproject. Findings flow through the three dated `.md`
outputs (`checks/`, `tasks/`, `reports/`) into the operator's queue,
not into git. The cron lane commits only its own dated outputs +
the verifier pass-list, with the audit prefixes `[managing] daily
<DATE>:` and `[managing] verify <DATE>:` (§ 5.3). The output files
themselves are the surface; the operator (or a follow-on session)
reads them, decides which to act on, and the resulting work happens
inside the relevant subproject — not in the cron output.

### 5.2 Interactive lane (operator `/open managing` session)

A `/open managing` session is a normal qagents session. It reads
any file under the tree, edits managing/'s own surface, and may
contribute to shared-data conventions — `data/tmp/<slug>-<date>{,.md}`
spec drafts, `data/specs/<slug>-<date>.md` promotions,
`data/claude-updates/<branch>.md` cross-subproject hints. Commits
land through `/close`'s audit gate (close.sh), not via ad-hoc
Claude-issued `git commit` calls — the deny on `Bash(git commit:*)`
in `.claude/settings.json` enforces that. close.sh's commit message
shape is the audit signal for interactive-lane work; `git log
--grep "^\[managing\] (daily|verify)"` continues to isolate the
cron lane.

Common to both lanes: live probes via `curl`, `gh`, `pnpm -C
<sub>/web test:e2e` are available. Neither lane may `git push
--force`, mutate external state via Alpaca / AWS write APIs /
AGO/DOJ mailers without explicit operator approval, or run `rm`
outside `pending/`.

### 5.3 Pending verification — the lock-protected `git commit` exception

managing MAY commit ONLY (a) paths listed in
`managing/checks/<DATE>.pending.json` (the verifier's machine-readable
pass-list), (b) clean-exit RUN_DIR contents under
`pending/cron-ec2/<basename>/<sub>/<routine>/<run_id>/pending/<canonical>`
promoted via `verify-pending.sh`'s `promote_cron_ec2` lane (spec
`data/specs/cron-ec2-migration-2026-05-19/infra-2026-05-19/SPEC.md` § 3.6 + § 3.9 step 10),
plus its own dated outputs
(`managing/{checks,reports,tasks}/<DATE>.md`, including the
`.pending.json` sidecar), ONLY with the message prefix
`[managing] verify <DATE>:` (or `[managing] daily <DATE>:` for the
own-outputs lane), AND ONLY while holding the canonical
`.data-write-lock` (root-anchored, gitignored — same shape as
`.dot-claude-write-lock`) for the promotion lanes.

The exception lives entirely inside `data/schedules/launchd/verify-pending.sh`
— that script is the single audit surface. The four-subagent fan-out
itself never commits; the coordinator invokes the script after subagents
return. Audit signal: `git log --grep "^\[managing\] verify"` lists every
output of this flow.

Manual ad-hoc invocations follow the same path: operators run
`data/schedules/launchd/verify-pending.sh` (or `--force <pending-relpath>`
to bypass verifier rules for a single file with audit-prefixed
`force-accept <path>` in the message). Both modes acquire the lock the
same way. Spec: `data/specs/data-conventions-2026-05-06/SPEC.md` § 7.4 + § 7.6.

Same script also owns `prune_stale_fails` — at the end of every fire it
`rm`s any `pending/**` file that is **(a)** >7 days old AND **(b)**
<50 bytes, skipping `pending/logs/` + `pending/tmp/` + `pending/cron-ec2/`
(the last has its own per-RUN_DIR lifetime managed by
`promote_cron_ec2`). Thresholds match the verifier's
`"too small (<50 bytes): stub memory file"` reject rule and give
memsearch a week's grace before empty-day stubs sweep. pending/
is gitignored — no commit, no lock contention.

## 6. Layout

```
managing/
├── CLAUDE.md                 # this file
├── README.md                 # quickstart + cron command
├── probes.md                 # weighted random-probe pool (P1..P6)
├── scripts/                  # mechanical helpers (bash-3.2 portable) + status_emit.mjs
├── .claude/
│   ├── settings.json         # observe-only allow-list
│   ├── settings.local.json   # gitignored, user-local overrides
│   ├── skills -> ../../.claude/skills
│   └── agents/
│       ├── checker.md
│       ├── planner.md
│       ├── reporter.md
│       └── verifier.md       # Haiku 4.5; pending/ structural validation
├── checks/                   # dated .md, top 5 issues (functionality first)
├── tasks/                    # dated .md, 10 ranked items
└── reports/                  # dated .md, yesterday's % completion
```

`checks/`, `tasks/`, `reports/` are committed (markdown is the source of
truth and lets future sessions reconstruct multi-day trajectories). The
three subdirs each carry a `.gitkeep` until the first dated file lands.

## 7. Schedule

Cron-fired daily at 06:00 local via the qagents launchd scheduler at
`data/schedules/`. Registered as `com.qagents.managing-daily`; spec row in
`data/schedules/cron_triggers.md`; ROUTINES entry
`managing:daily:06:00:0,1,2,3,4,5,6:sdk` in `data/schedules/launchd/install.sh`
(the trailing `:sdk` opts the route into the Agent SDK lane per
`agent-sdk-adoption-2026-05-17.md` Phase 3; migrate routine-by-routine and
don't flip the daily coordinator until the SDK lane demonstrates parity).
The fired routine is the coordinator prompt at
`managing/.claude/coordinator-prompt.txt` — `data/schedules/launchd/run_routine.sh`
reads the sidecar and either pipes it to `claude --print` (legacy lane) or
invokes `python -m qagents.agent_sdk.cron` (SDK lane, when
`QAGENTS_DISPATCH=sdk_task` is baked into the plist). The coordinator runs
the four subagents (three top-tier + one Haiku verifier) in parallel and exits.
Estimated runtime budget: ≤ 10 min total (subagents wrap independently).
Per-run cost cap is **$9 USD** (`MAX_BUDGET_USD` defaults to `9.00` for
`daily`; `3.00` for trading routines).

Do **not** use `RemoteTrigger` / `CronCreate` / the cloud `schedule` skill —
the cowork sandbox VM cannot mount the qagents tree, and that path was
abandoned 2026-04-25 (see `data/schedules/Notes.md` § "Why not RemoteTrigger
/ `/schedule`?").

**Cron-EC2 lane** (`data/specs/cron-ec2-migration-2026-05-19/SPEC.md`) is jointly
implemented: `serving/` owns the AWS-facing infrastructure (Phase 0a — CDK
deltas, `serving/scripts/ec2-cron/`, deploy script; tracked as
`data/specs/serving-2026-05-26/SPEC.md § 10 Phase 7`); `managing/` owns the laptop-side coordination
(`data/schedules/launchd/cron-pull.sh` + `enable-laptop-cron.sh`, the
`install.sh --target=ec2` switch, the `managing/.claude/agents/checker.md`
ledger scan), plus Phase 1's daily+status-emit shadow week. Don't touch AWS state from a `managing/`
session — open a `serving/` session if a drift surfaces.

## 8. Voice + format for output .md files

The dated outputs use the **engineer-debugging-a-system register** — same
as `documenting/`, `designing/`, Janet narration in `explaining/`, and the
femfas/quantapix copy. See
`memory/feedback_engineer_not_activist_voice.md`. Specifically:

- Factual, present-tense, third-person system-state.
- Each finding carries: **title** (one line), **evidence** (file:line, commit
  hash, URL + HTTP status), **severity** (functionality > correctness >
  consistency, with one-word tag), **proposed action** (one line, imperative).
- No "we should consider…", no rhetorical questions, no exhortations.
- File references are absolute repo-relative paths ((private appellate-drafting artifact),
  not "the appeals memory file").

## 9. Scope boundary

managing/ does not import from any sibling subproject (root CLAUDE.md
language-split rule). It reads via the filesystem only. There are no
shared-code seams; the data hub for managing/ is the qagents tree itself.
This is a read-side specialization of the data-hub-not-shared-code pattern.


