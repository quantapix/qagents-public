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

Commitment 1 (firm 6/1/2026 deliverables) is retired post-deadline; slots 2–8
keep their numbers because `probes.md` cites commitment 4, `README.md` cites
commitment 6, and `dco-manual` cites the checker's #7.

2. **Weekly summaries on the public `quantapix` GitHub org.** Any public repo
   under `quantapix/` with `pushedAt` older than 7 days is a finding. The
   org-level profile README is included.
3. **Rapid progress in `studying/` and `explaining/`.** Either subproject
   with zero commits in the trailing 3 days is a finding. Each daily plan
   names the next concrete artifact to land.
4. **`quantapix.com/status` refresh every 3 days.** Any `data/status/<sub>.json`
   slot older than 3 days is a finding. A live `Last-Modified` on
   `https://quantapix.com/status/` older than 3 days is a separate finding
   (deploy stale, not just emit stale). **Live-deploy-age is now the
   load-bearing signal** (`data/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`
   § 7): the `qagents:status-emit-all` cron keeps every canonical slot fresh
   daily, so the slot-age finding will essentially never fire — a live site
   that stops being deployed would otherwise go unnoticed. Surface the live
   `Last-Modified` deploy-age line in **every** daily report, not only when
   it crosses 3 days. Report-only — managing stays observe-only; no
   autonomous deploy.
5. **Donation-drive credibility (active 2026-06-01 → 2026-12-01).** Two
   probes anchored to `donating/drive.md`'s public promises. (a) **Promise-3
   liveness** — once `qnarre.quantapix.com` and `qresev.quantapix.com` are
   live (PLAN Phase 3, ≈ 2026-08), a failed HTTPS sweep on either endpoint
   outranks any non-functionality finding for the day. (b) **Ledger
   cadence** — `donating/ledger/YYYY-MM.md` must land within 5 calendar
   days of each month-end; missing/late ledger past day 5 is a functionality
   finding (drive's whole pitch is *trivially auditable*). Probe wiring
   goes in `probes.md` once endpoints + the first dated ledger exist; the
   ledger-existence check can land sooner.
6. **Spec hygiene + phase tally.** `scripts/specs-audit.sh` is the single
   source of truth (sections: SPECS phase tally / TESTS conformance /
   LAYOUT lint / TMP proposal status / LEDGER manual-check reminders); its
   thresholds and finding rules mirror `data/specs/CLAUDE.md` +
   `data/tmp/CLAUDE.md` and move in lockstep with them. Every non-tally
   finding it emits (`[in-flight]` > 14d, OVER-CAP, LAYOUT lint, stale /
   adopted-orphan `tmp/`, post-2026-05-19 tests-dir shape, LEDGER
   `PAST`/`DUE` rows — surface the note column verbatim) is a
   **correctness** finding. New LEDGER rows are append-only entries in the
   script's `SPEC_LEDGER` TSV; the `owner` column powers
   `specs-audit.sh --owner <sub>` (pinned by `scripts/tests/`). The daily
   tally rides in `checks/<date>.md` as `## Uncompleted spec phases` +
   `## tmp/ proposal status` + `## Spec ledger reminders` (see § 8).
7. **Claude permission-settings drift.** `scripts/settings-drift.sh` is the
   source of truth; `drift=YES` or `lint=ERRORS` is a **correctness** finding
   (regenerate via `scripts/claude-settings/build.py`). Hand-edit drift only;
   new allow patterns are the weekly `dco-settings` lane's job.
8. **Brand / kit-version drift.** `scripts/brand-drift.sh` is the source of
   truth; `drift=YES` (a `KIT_VERSION` producer pin or the loader off the kit
   `package.json` version — the silent same-major class) is a **correctness**
   finding.

Subagent prompts under `.claude/agents/` encode these commitments verbatim —
keep them in sync when a threshold changes.

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
| `checker` | opus (top tier) | `checks/<date>.md` | All subprojects (read-only), live websites (WebFetch), public GitHub repos (`gh`), `shorting/positions/` (adversarial findings — promote / dismiss-with-reason / ignore, per `shorting/CLAUDE.md` § 5) | Three categories: consistency, correctness, functionality. Top 5 total, ranked, functionality first. |
| `planner` | opus (top tier) | `tasks/<date>.md` | Today's `checks/<date>.md`, yesterday's `tasks/`, recent git log, PLAN.md / Memory.md across subprojects | 10 ranked items. May draw from today's checks, yesterday's untackled, or backlog. |
| `reporter` | opus (top tier) | `reports/<date>.md` | Yesterday's `checks/` + `tasks/`, `git log --since=yesterday` across all subprojects, deploy logs | % completion mapped from commits / new files / closed issues. Distinguishes done / in progress / not touched. |
| `verifier` | `haiku` | `checks/<date>.pending.json` + appended `## Pending verification` section in `checks/<date>.md` | All files under `pending/`; rules table embedded in agent prompt | Closed-set allow-list classifier (default-skip); emits `passes[]` + `internal[]` + `unclassified[]`. Only `passes[]` drives the lock-protected rsync in `data/schedules/launchd/verify-pending.sh` (Layer 2 guards exit 8/9/10 as defense-in-depth). Spec: `data/specs/pending-promotion-scope-2026-05-28/SPEC.md`. Cheap & fast — runs in parallel. |

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
- Spec hygiene — § 1.1 commitment 6 (`scripts/specs-audit.sh` finding set).

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

### 3.1 Suppressed-finding class — Agent SDK (operator directive 2026-06-30)

Anthropic dropped the SDK credits from the Max-20x subscription, so the SDK
lane is unusable for now. **All four subagents must NOT surface any
SDK-related finding** until the subscription regains SDK access. Concretely,
suppress: `data/agent-sdk-ledger/` failure-stage findings (checker.md's
`data/agent-sdk-ledger/` scan), SDK-lane fire failures, `agent-sdk-adoption-2026-05-17`
spec-phase stalls / OVER-CAP, SDK-credit references, and the
`pending/data/agent-sdk-ledger/**` unclassified surfacing (now classified
DORMANT in the verifier internal-set + `verify-pending.sh`). This is a
reversible, dated directive — drop the suppression and re-enable the scans
when a new subscription/SDK plan ships. See memory
`reference_agent_sdk_credit_200_mo`. The root-cause revert — dropping the
`:sdk` token from `managing:daily` in `install.sh` ROUTINES — was applied
2026-06-30; the routine now runs the `claude --print` lane (§ 7 owns the
current lane status + restore path).

## 4. Functionality probes — random, weighted

Each run picks 2–3 probes from a weighted pool. **Random selection is
load-bearing** — it prevents the watcher from drifting into a fixed pattern
and missing intermittent failures elsewhere.

Probe families + weights + pass/fail predicates live in `managing/probes.md`
(P1..P7 + weight-summary table); checker reads from there. Random seed:
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

Same script also owns `prune_stale_fails` — end-of-fire cleanup of stale
sub-50-byte `pending/**` stubs (thresholds + skip-list live in the script
and match the verifier's stub-reject rule). pending/ is gitignored — no
commit, no lock contention.

## 6. Layout

```
managing/
├── CLAUDE.md                 # this file
├── README.md                 # quickstart + cron command
├── probes.md                 # weighted random-probe pool (P1..P7)
├── scripts/                  # mechanical helpers (bash-3.2 portable) + status_emit.mjs
│   └── tests/                # bash harness (run.sh + cases/) — specs-audit owner column + --owner
├── .claude/
│   ├── settings.json         # observe-only allow-list
│   ├── settings.local.json   # gitignored, user-local overrides
│   ├── skills -> ../../.claude/skills
│   └── agents/
│       ├── checker.md
│       ├── planner.md
│       ├── reporter.md
│       └── verifier.md       # `haiku`; pending/ structural validation
├── checks/                   # dated .md, top 5 issues (functionality first)
├── tasks/                    # dated .md, 10 ranked items
└── reports/                  # dated .md, yesterday's % completion
```

`checks/`, `tasks/`, `reports/` are committed (markdown is the source of
truth and lets future sessions reconstruct multi-day trajectories).

## 7. Schedule

Cron-fired daily at 06:00 local via the qagents launchd scheduler at
`data/schedules/`. Registered as `com.qagents.managing-daily`; spec row in
`data/schedules/cron_triggers.md`; ROUTINES entry
`managing:daily:06:00:0,1,2,3,4,5,6` in `data/schedules/launchd/install.sh`.
**The `:sdk` token was removed 2026-06-30** (SDK lane paused indefinitely
2026-06-15; `:sdk` fleet reverted 2026-06-30; gate on SDK access returning —
root § Agent SDK lane owns status). The routine runs the `claude --print` lane
until then; restore the trailing `:sdk` (Agent SDK lane,
`data/specs/agent-sdk-adoption-2026-05-17/SPEC.md` Phase 3) via
`install.sh --enable` from canonical when access returns. See § 3.1 + memory
`feedback_managing_suppress_sdk_findings`.
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


