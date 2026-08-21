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
- `tasks/YYYY-MM-DD.md` — the **10** most pressing items for that day, ranked
  (inputs: § 2 table).
- `reports/YYYY-MM-DD.md` — % completion of **yesterday's** checks + tasks,
  with evidence (commit hashes, file changes, closed issues, deploy log lines).

Objective: **keep an eye on the ball.** managing/ does not fix anything. It
surfaces what needs fixing and tracks whether the rest of the constellation is
making progress.

### 1.1 Pinned commitments — what "the ball" actually is

These are the load-bearing objectives the three top-tier-model subagents weight
above generic drift detection (the verifier runs structural checks only, not
pinned-commitment scoring). **Each commitment names its own finding class
below** — read the row, never a summary here. Commitment 1 (firm 6/1/2026
deliverables) is retired post-deadline;
surviving slots keep their numbers because `probes.md` cites #4, `README.md`
cites #6, and `dco-manual` cites the checker's #7.

2. **Weekly summaries on the public `quantapix` GitHub org.** Any public repo
   under `quantapix/` with `pushedAt` older than 7 days is a finding. The
   org-level profile README is included. Detail: `checker.md` #2.
3. **Rapid progress in `studying/` and `explaining/`.** Either subproject
   with zero commits in the trailing 3 days is a finding. Each daily plan
   names the next concrete artifact to land. Detail: `checker.md` #3.
4. **`quantapix.com/status` refresh every 3 days.** Any `data/status/<sub>.json`
   slot older than 3 days is a finding; a live `Last-Modified` older than 3
   days is a SEPARATE finding (deploy stale, not just emit stale), and it is
   the **load-bearing** one — the daily emit cron keeps slot-age nearly always
   green. Report-only; managing never deploys. Full row text — the
   every-report obligation and the spec cite — lives ONLY in `checker.md` #4
   (ns:managing/49).
5. **Donation-drive credibility (active 2026-06-01 → 2026-12-01).** Two
   probes anchored to `donating/drive.md`'s public promises: **ledger
   cadence** (missing past day 5 of the following month → **functionality**)
   and **Promise-3 endpoint liveness** (a PLACEHOLDER until
   `qnarre|qresev.quantapix.com` are live — never a check to fake). Full row
   text lives ONLY in `checker.md` #5, the normative carrier (ns:managing/49).
6. **Spec hygiene + phase tally.** `scripts/specs-audit.sh` is the single
   source of truth (eight sections; COHERENCY is commitment 15's surface, not
   this one's). Every non-tally row is a **correctness** finding; `*-tally`
   rows are tally-only. **Four labeled ARMS ride this commitment, same
   number** (folded from the retired standalone cron-lane slot, 2026-07-25):
   cron-lane health, **watcher-liveness** (the only arm that can report the
   daily fire ITSELF stopped — `scripts/watcher-liveness.sh`), S5-scan
   (verifier FINDING lines + per-axis `coverage-diff`, REPORT-only), and
   memsearch Stop-hook health; their hits rank **functionality**, not
   spec-hygiene correctness. Full row text — section semantics, the
   exit-75/76 collapse rules, the trading-chain and artifact-existence
   arms, the carve-out registry, the S8 `retire` relays, the `dco-verify`
   marker rule, and the walk scope — lives ONLY in `checker.md` #6
   (ns:managing/49) + memory `project_managing_subproject` commitment 6.
   Thresholds mirror `data/specs/CLAUDE.md` + `data/tmp/CLAUDE.md` +
   `data/charters/qagents/spec-lifecycle/CHARTER.md` and move in lockstep
   (script + `checker.md` #6 + this roster land in ONE change —
   data-charters-2026-07-16 § 3.4 AUDIT-C1; charter-scopes-2026-07-16 § 6.1
   for the multi-root + DEBATES/TODOS arms).
7. **Claude permission-settings drift.** `scripts/settings-drift.sh` is the
   source of truth; `drift=YES` or `lint=ERRORS` is a **correctness** finding
   (regenerate via `scripts/claude-settings/build.py`). Hand-edit drift only;
   new allow patterns are the weekly `dco-settings` lane's job. Detail:
   `checker.md` #7.
8. **Brand / kit-version drift.** `scripts/brand-drift.sh` is the source of
   truth; `drift=YES` → **correctness**. Three classes fold in: kit-version
   pins, overlay byte-mirror parity, and the sanctioned-deviation premise
   (**a premise is not a mirror** — `cmp` cannot decide it, so it expires
   with the other two green). `premise UNKNOWN` is always a finding, never
   clean. Full row text — the three arms, the mirror pairs, the
   `UNREGISTERED` sweep, the headless literal maps — lives ONLY in
   `checker.md` #8 (ns:managing/49) + memory
   `feedback_two_token_mirrors_ship_two_palettes`.
9. **Cron-seat capability + roster + posture + flip + peer-dark + unloaded +
   pending-enable.** `scripts/seat-drift.sh` is the source of truth (wraps
   `data/schedules/launchd/seat_preflight.sh`; bit-field exit 1=capability,
   2=roster). SEVEN facts, classes only here: `capability=GAPS` **on the seat
   holder**, `unloaded=UNLOADED` (peer's `declared − loaded` non-empty) and
   `flip=STALE-UNACCEPTED` → **functionality**; `roster=DRIFT` (**the checker
   only sees what FIRES; this is the one check that looks at what didn't**),
   `posture=OFF-POSTURE-STALE` (≥ 7d), `peerdark=DARK` (one per NAMED entry),
   `pending-enable=<n>-AGED` (≥ 7d) → **correctness**; every `UNKNOWN` /
   `no-peer` is tally-only but **never** reads clean, and `PEER-AGE` is graded
   every compare. managing REPORTS these rows, never edits them. Full row text
   — thresholds, rationale, landing-line forms, the exclusivity ≠ capability
   argument, the `monitoring:archive-scan` and 2026-08-11 qpur `loaded=0`
   instances — lives ONLY in `checker.md` #9, the copy the daily fleet reads
   (roster-ization, ns:managing/49). Memory `project_mobile_cron_seat`; spec
   family `data/specs/node-return-lane-2026-07-14/`. Three-file lockstep:
   script + `checker.md` #9 + this row move in ONE change.
10. **Node-PR staleness.** `scripts/node-pr-staleness.sh` is the source of
   truth (observe-only; never fetches). `stale=YES` (unmerged node PR > 7d) →
   **consistency** — a waiting contributor, not a broken system; everything
   else tally-only. Same lane, no new number: `scripts/node-pr-gate.sh`
   `verdict=BLOCK` → **correctness**, surfaced verbatim; that PR must not
   merge until amended or ruled. Full row text — the declared-surface
   allow-list (closed set, no auto-widening), the answer path, and the spec
   families — lives ONLY in `checker.md` #10 (ns:managing/49).

11. **Flow-clause hygiene (tree-wide safety net).** `scripts/flow-lint.sh` is
   the source of truth. Any HARD line → **correctness**; the load-bearing
   shape is a dangling `ns:` target, which the close-time gate structurally
   cannot see. Advisories + the summary are tally-only. Observe-only: route
   fixes to the citing slot's owner session. Detail: `checker.md` #11
   (ns:managing/49).
12. **Spread review-lane hand-offs + D-4 escalation — LIVE (dco SPREAD-OP,
   spread-merge-2026-08-09).** `scripts/spread-runway.sh` is the source of
   truth; the lane is absorbed into `/dco-manual` as the SPREAD-OP
   (optimization charter § 2.12). `sla=ESCALATE`, the § 5.6 `ESCALATE
   dco-spread apply item …` rows, the R6 `STALE no shrink pass …` row, and
   `fail_headroom min < 2500` B (distance-to-fail, graded instead of the
   breach count — I-7) are **correctness** findings; UNKNOWN rows are
   findings, never clean.
   Triage routes to `data/next-steps/qagents.md`. Full row text — thresholds,
   the two run-dir homes, the purge-vs-disuse `no-runs` reading, and the
   2026-08-16 SLA-lineage + p0 re-key (ns:managing/48) — lives ONLY in
   `checker.md` #12 (ns:managing/49).
13. **Spec-family test-battery health.** `scripts/spec-battery.sh` is the
   source of truth — the tree-wide aggregating runner over every spec-family /
   charter / subproject-harness `run.sh`. `FAIL` / `TIMEOUT` /
   `SKIPPED-OVERSIZE` rows → **correctness**; a sweep with no trailing
   `suites=…` summary is UNKNOWN, never a clean count. Full row text — the
   background-invocation + `--out` discipline, the 600 s ceiling and the
   OVERSIZE carve, the post-sweep `git status` spillage check (an aggregating
   READER must never need a write lock —
   `feedback_test_suite_shared_hub_spillage`), the run-length rule for
   standing reds, and the `store-durability` honest-red carve — lives ONLY in
   `checker.md` #13 (ns:managing/49).
14. **Blind-metric provenance on published figures.**
   `scripts/blind-metric-drift.sh` is the source of truth. A changed
   coverage/tier figure on a public status slot whose minting wave +
   closed-oracle status cannot be named → **correctness**
   (`feedback_blind_fanout_oracle_channels`). `withheld` is the correct
   posture, never a finding. Detail: `checker.md` #14 (ns:managing/49).
15. **Coherency arms — the deterministic half of the § 3 daily mandate.**
   `scripts/specs-audit.sh --section coherency` is the source of truth
   (operator ruling 2026-08-05 = do-retire R-18 + reap-boundary R1: an
   EXECUTION gap closed, not new ownership; § 3 already charters the
   mandate). Four arms: exit-46 citation existence; declared-pair value
   checks; the absorbed-body freeze detector (drift REPORT-ONLY per
   ns:managing/30, but exit 2 is a **correctness** finding — a dead matcher
   must never read as clean); and the warn-cap fleet byte-sweep cross-checked
   against filed `spread-review owed` items in `data/next-steps/qagents.md`.
   Any `coherency` row → **correctness**; `coherency-report` rows are
   report-only echo; UNKNOWN is always a finding, never clean. Full row text
   lives ONLY in `checker.md` #15 (ns:managing/49). Three-file lockstep: the
   script section + `checker.md` #15 + this row move in ONE change.

16. **Node-backup per-arm verdict diff.** `scripts/backup-arm-drift.sh` is the
   source of truth; `serving:node-backup`'s aggregate exit code is a saturated
   channel and this is the fire-to-fire DIFF that replaces it. Classes:
   `NEW-RED` → **functionality**; `COVERAGE-REGRESSION` → **correctness**;
   `UNKNOWN` → tally-only but **never green**. Observe-only; route fixes to
   serving. Full row text — the three state definitions, the 2026-07-26
   three-day instance, the `PG_HEALTH_ARM_VERDICTS=1` + seat-holder
   host-scoping caveats, and the reciprocal cites (ns:serving/80 →
   ns:managing/44) — lives ONLY in `checker.md` #16, which is the copy the
   daily fleet reads (roster-ization, ns:managing/49). Three-file lockstep:
   the script + `checker.md` #16 + this row move in ONE change.

Subagent prompts under `.claude/agents/` encode these commitments verbatim —
keep them in sync when a threshold changes.

## 2. Four subagents (three top-tier + one haiku), clean contexts each

The 06:00 cron fires a single coordinator that spawns three top-tier-model subagents +
one Haiku subagent in parallel, each with a clean context. Each subagent owns
exactly one output file and writes it directly to disk. The coordinator only
sees their one-line completion confirmations — **no accumulated context bleed
from their work** (its one write is the verifier-sidecar-derived
`## Pending verification` append, sequenced after checker returns).

| Subagent | Model | Output | Inputs | Notes |
|---|---|---|---|---|
| `checker` | opus (top tier) | `checks/<date>.md` | All subprojects (read-only), live websites (WebFetch), public GitHub repos (`gh`), `shorting/positions/` (adversarial findings — promote / dismiss-with-reason / ignore, per `shorting/CLAUDE.md` § 5) | Three categories: consistency, correctness, functionality. Top 5 total, ranked, functionality first. |
| `planner` | opus (top tier) | `tasks/<date>.md` | Today's `checks/<date>.md`, yesterday's `tasks/`, recent git log, PLAN.md / Memory.md across subprojects | 10 ranked items. May draw from today's checks, yesterday's untackled, or backlog. |
| `reporter` | opus (top tier) | `reports/<date>.md` | Yesterday's `checks/` + `tasks/`, `git log --since=yesterday` across all subprojects, deploy logs | % completion mapped from commits / new files / closed issues. Distinguishes done / in progress / not touched. |
| `verifier` | `haiku` | `checks/<date>.pending.json` (coordinator-appended per above) | All files under `pending/`; rules table embedded in agent prompt | Closed-set allow-list classifier (default-skip); emits `passes[]` + `internal[]` + `unclassified[]`. Only `passes[]` drives the § 5.3 lock-protected rsync. Spec family: `data/specs/pending-promotion-scope-2026-05-28/`. |

Each subagent's prompt (`.claude/agents/`) lists exact inputs to read and the
exact output path to write — they never negotiate scope at runtime.

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
- TS / Lean / Python typecheck regressions from `pnpm verify` / `lake build` /
  `pyright` exit codes — read the most recent CI / commit log; never run them.
- Spec hygiene — § 1.1 commitment 6 (`scripts/specs-audit.sh` finding set).

**Functionality** (live system state, *highest priority*) — the weighted probe
pool: live route fetch (femfas.net / quantapix.com), single-spec Playwright
replay, status-hub freshness, public-org Actions runs, legal-corpus cite
integrity, shipped-ruling regression. Families, weights, and pass/fail
predicates are owned by `managing/probes.md` (P1..P7, § 4) — never restated
here; the pinned commitments (§ 1.1) carry the rest.

A functionality failure is the day's top issue, full stop. Consistency and
correctness fill the remaining 4 slots, ranked by blast radius (legal-record
files > shipped websites > internal docs > backlog).

### 3.1 Suppressed-finding class — Agent SDK (operator directive 2026-06-30)

The SDK lane is parked — root CLAUDE.md § Agent SDK lane owns status +
restore path. Until it returns, **all four subagents must NOT surface any
SDK-related finding** (ledger failure stages, SDK-lane fires, SDK spec-phase
stalls / OVER-CAP, credit references, and `pending/data/agent-sdk-ledger/**`
unclassified surfacing — DORMANT in the verifier internal-set +
`verify-pending.sh`). Reversible, dated directive — drop the suppression
when access returns. Memory: `feedback_managing_suppress_sdk_findings`.

## 4. Functionality probes — random, weighted

Each run picks 2–3 probes from a weighted pool. **Random selection is
load-bearing** — it prevents the watcher from drifting into a fixed pattern
and missing intermittent failures elsewhere. Families + weights + pass/fail
predicates live in `managing/probes.md` (P1..P7 + weight-summary table);
checker reads from there. `managing/scripts/probe-pick.sh --k 2` is the picker
(pure-awk seeded weighted draw — bounded rejection, deterministic order
fallback; no GNU shuf dep), seeded `date +%j` — deterministic per day, varied
across days.

**A gate cross-checking a human-authored free-text field must match on the
FACT, never on the FORMATTING** — if the shape of the prose is load-bearing to
a gate, the gate is reading the wrong surface. Worked instance (the coherency
warn-cap arm reporting a genuinely filed breach as unfiled, daily, until
2026-08-07) + the relax-and-re-pin rule: memory
`feedback_data_structure_over_brittle_code` § Corollary.

## 5. Boundaries

Two lanes with different posture. The "observe-only" framing applies
to the cron lane; the interactive lane behaves like any other
qagents subproject session.

### 5.1 Cron lane (the daily watcher)

Observe-only with one tightly-scoped exception — the `pending/`
verification flow (§ 5.3). The 06:00 coordinator and its four
subagents never `git push`, never deploy, never mutate code or copy
in any subproject; the lane commits only its own dated outputs +
the verifier pass-list, under the § 5.3 audit prefixes. The three
dated `.md` outputs ARE the surface: the operator (or a follow-on
session) reads them and the resulting work happens inside the
relevant subproject — never in the cron output.

### 5.2 Interactive lane (operator `/open managing` session)

A `/open managing` session is a normal qagents session. It reads
any file under the tree, edits managing/'s own surface, and may
contribute to shared-data conventions — `data/tmp/<slug>-<date>{,.md}`
spec drafts, `data/specs/<slug>-<date>/SPEC.md` promotions,
`data/claude-updates/<branch>.md` cross-subproject hints. Commits
land through `/close`'s audit gate (close.sh), never via ad-hoc
Claude-issued `git commit` calls — close.sh IS the enforcement; the
`Bash(git commit:*)` deny only backstops it, and is inert in sessions
launched at the worktree root (cwd-only settings loading; see
`ns:qagents/61`). The cron lane needs no caveat — `run_routine.sh`
pins CWD to canonical `<repo>/managing` with
`--setting-sources project,user`. `git log --grep "^\[managing\]
(daily|verify)"` isolates the cron lane from interactive-lane work.

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
promoted via `verify-pending.sh`'s `promote_cron_ec2` lane (owner
`data/charters/serving/cloud-base/cron-ec2-lane.md`),
(c) the ns-drain render commit — the re-rendered `data/next-steps/`
projections under the shared message `render: next-steps projections`
(load-bearing string, keep byte-identical — the substrate close lifecycle
emits it too and a compile-time assertion keys on it; audit discriminator:
the drain commits direct-to-main during a fire, the close-lane render
arrives via a session-branch merge), plus its own dated outputs
(`managing/{checks,reports,tasks}/<DATE>.md`, including the
`.pending.json` sidecar), ONLY with the message prefix
`[managing] verify <DATE>:` (or `[managing] daily <DATE>:` for the
own-outputs lane), AND ONLY while holding the canonical
`.data-write-lock` for the promotion lanes.

The exception lives entirely inside `data/schedules/launchd/verify-pending.sh`
— that script is the single audit surface; the fan-out itself never commits.
The coordinator invokes it **twice**: once the moment the VERIFIER returns, and
again after all four return (ns:managing/56 — the fan-out's 600 s ceiling
TERMINATES the fire, so a commit gated on the slowest subagent inherits that
subagent's failure rate; the script's lanes filter to new/modified files, so the
second run is additive). Audit signal: `git log --grep "^\[managing\] verify"`.

Script mechanics — manual `--force`, `prune_stale_fails`, the S5 write-back
+ the `push_to_authority` silent-SPOF rule: `data/schedules/CLAUDE.md`
§ "`verify-pending.sh` — script mechanics".

## 6. Layout

`README.md` (quickstart + cron command) · `probes.md` (weighted random-probe
pool, § 4) · `scripts/` (mechanical bash-3.2-portable fact-emitters +
`status_emit.mjs`; `scripts/tests/` is the bash harness — run.sh + cases/,
owner of the specs-audit `owner` column + `--owner`) · `.claude/` (the
standard subproject shape per root CLAUDE.md § "Subproject `.claude/` shape";
`agents/` holds `checker.md` / `planner.md` / `reporter.md` / `verifier.md`) ·
`checks/` + `tasks/` + `reports/` (the three dated outputs, § 1).

`checks/`, `tasks/`, `reports/` are committed (markdown is the source of
truth and lets future sessions reconstruct multi-day trajectories).
`/do-retire` P2 lane 4 reaps them on a registry TTL — **operator-fired, so
nothing enforces the bound**; reaped days are byte-exact in `archive.blob`
(`bash scripts/retire.sh --restore 'managing/checks/*' --dest <dir>`).

**That TTL is bounded by these agents' own declared lookbacks, so the two
move in lockstep** (§ 1.1's discipline, one level out):
`data/specs/do-retire-2026-07-26/lanes.tsv` records each dir's `ttl` +
`consumer_window` — read them there, never from a figure restated here.
Widening any agent's lookback past its column is a two-file change; a
lookback the registry does not record is how a reap silently narrows the
watcher's own evidence.

## 7. Schedule

Cron-fired daily at 06:00 local via the qagents launchd scheduler at
`data/schedules/`. Registered as `com.qagents.managing-daily`; the ROUTINES
entry `managing:daily:06:00:0,1,2,3,4,5,6` in
`data/schedules/launchd/install.sh` is the schedule's source of truth
(§ 3.1 owns the suppressed-finding class). The fired routine is the
coordinator prompt at `managing/.claude/coordinator-prompt.txt`, piped to
`claude --print` by `data/schedules/launchd/run_routine.sh`; it runs the
four subagents in parallel and exits, runtime budget **≤ 25 min (ruled
2026-08-18, `data/debates/operator-sittings-2026-08-18.md` § A** — raised from
10 min because the checker's measured wall clock is 14–21 min against the
`claude --print` 600 s background-wait default, which killed the fan-out on
08-16 and 08-18). The raise is delivered by a `managing:daily`-scoped
`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` export in `run_routine.sh`
(`ns:serving/99`); **until that lands, the fan-out still terminates at 600 s**
with "Background tasks still running" and the checker's work is lost. The
budget stays a hard CEILING, not a target: any arm added here is spending a
fixed pot — cost the wall clock before adding one. **The seat host must not
SLEEP inside that window** — the host-config half is cured (qpur `pmset` reads
`sleep=0` on AC since ≥ 08-17); the repo-level sleep assertion stays open as
the battery arm (`ns:serving/97`). A fire that stops with NO exit line is one
of those two classes, never a budget kill (a budget kill is *distinguishable*:
exit 4 + `Error: Exceeded USD budget` verbatim); do not diagnose it from one
day's log — `ns:managing/52` decomposed into four mechanisms across nine days,
detail in memory `project_managing_subproject`.
Per-run cost caps come from `run_routine.sh`'s `routine_policy_budget()`,
paired with `routine_policy_model` so a routine's tier and its funding cannot
drift apart — read `daily`'s figure from that function, never from a copy
here (this line carried a stale one for five days). Never `RemoteTrigger` /
`CronCreate` / cloud `/schedule` (root CLAUDE.md § `data/schedules/` owns
the rule; rationale `data/schedules/Notes.md`).

### 7.1 The cron lane is SEAT-GATED and MOBILE (2026-07-14)

Spec family: `data/specs/node-return-lane-2026-07-14/`; memory
`project_mobile_cron_seat`. The lane runs on **exactly one laptop at a time** —
`qyel` or `qpur`, the only two hosts with a "head" (headless boxes cannot hold a
Claude subscription seat). `data/schedules/SEAT` names the holder;
`run_routine.sh :: assert_seat_holder` **freshly reads it from the `github`
authority before every fire** and refuses otherwise.

Three consequences that bind `managing/`:

- **A non-holder logs `exit=0 skipped=not-seat-holder`.** That is a no-op, **not a
  failure** — the checker's non-zero-exit scan must never score it as one.
- **A holder-side `exit=75` (CHANGEOVER-DEFERRED) span collapses to ONE finding
  per day** carrying `refused=N of expected=M`; **functionality** when the dark
  span overlaps 08:30–16:45 ET on a weekday; a BLOCKED fire never collapses into
  it. Landing steps + the full rule: `checker.md` #6's cron-lane arm.
- **`.data-write-lock` does not provide the exclusion** — a filesystem sentinel
  cannot span machines. The SEAT value is the exclusion; the lock only serializes
  writers *within* the seat holder.
- **`managing:daily` rides the seat** (it needs the lock + the canonical repo, and
  those travel) — a watcher on the machine that is not firing watches nothing. A
  declared amendment to herdr's M7.

**Bootstrap trap:** the gate reads `SEAT` from `github/main`, never the local file.
A merge that is not **pushed** leaves the authority without `SEAT` → every routine
on every host refuses. Order is merge → push → verify
`git ls-tree github/main data/schedules/SEAT` is non-empty. `/close` does not push.

**Cron-EC2 lane** is dead — before triaging `pending/cron-ec2/` or any AWS drift,
read `data/charters/serving/cloud-base/cron-ec2-lane.md`.

## 8. Voice + format for output .md files

The dated outputs use the **engineer-debugging-a-system register** — same as
`documenting/`, `designing/`, and the femfas/quantapix copy; see
`memory/feedback_engineer_not_activist_voice.md` (factual, present-tense,
third-person system-state; no "we should consider…", no rhetorical
questions). Two format contracts:

- Each finding carries: **title** (one line), **evidence** (file:line, commit
  hash, URL + HTTP status), **severity** (functionality > correctness >
  consistency, with one-word tag), **proposed action** (one line, imperative).
- File references are absolute repo-relative paths ((private appellate-drafting artifact),
  not "the appeals memory file").

## 9. Scope boundary

managing/ does not import from any sibling subproject (root CLAUDE.md
language-split rule) — it reads via the filesystem only. No shared-code
seams; the data hub for managing/ is the qagents tree itself.
