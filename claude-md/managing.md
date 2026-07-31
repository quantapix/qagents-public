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
below** — 2–5 are functionality; 6–14 correctness EXCEPT #10 (consistency),
the seat-capability + flip-stale legs of #9 (functionality), and #6's arms
(cron-lane / S5-divergence / trading-chain hits rank functionality as
stated). Commitment 1 (firm 6/1/2026 deliverables) is retired post-deadline;
surviving slots keep their numbers because `probes.md` cites #4, `README.md`
cites #6, and `dco-manual` cites the checker's #7.

2. **Weekly summaries on the public `quantapix` GitHub org.** Any public repo
   under `quantapix/` with `pushedAt` older than 7 days is a finding. The
   org-level profile README is included.
3. **Rapid progress in `studying/` and `explaining/`.** Either subproject
   with zero commits in the trailing 3 days is a finding. Each daily plan
   names the next concrete artifact to land.
4. **`quantapix.com/status` refresh every 3 days.** Any `data/status/<sub>.json`
   slot older than 3 days is a finding; a live `Last-Modified` on
   `https://quantapix.com/status/` older than 3 days is a separate finding
   (deploy stale, not just emit stale). **Live-deploy-age is the
   load-bearing signal** (`data/charters/qagents/specs/status-emit-cron-fleet-2026-06-22/SPEC.md`
   § 7 — the daily emit cron keeps slot-age nearly always green). Surface
   the live deploy-age line in **every** daily report. Report-only —
   managing stays observe-only; no autonomous deploy.
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
   source of truth (six sections: SPECS phase tally / TESTS conformance /
   LAYOUT lint / CHARTERS lint / TMP proposal status / LEDGER reminders);
   thresholds mirror `data/specs/CLAUDE.md` + `data/tmp/CLAUDE.md` +
   `data/charters/qagents/spec-lifecycle/CHARTER.md` and move in lockstep
   (script + `checker.md` commitment 6 + this roster land in ONE change —
   data-charters-2026-07-16 § 3.4 AUDIT-C1; charter-scopes-2026-07-16 § 6.1
   for the multi-root + DEBATES/TODOS arms). Every non-tally finding is a
   **correctness** finding — surface the note column verbatim; the
   finding-class roster lives in `checker.md` commitment 6 and the script,
   not here. Walk scope (both spec roots), the data-not-prose layout
   exemptions, and the append-only `SPEC_LEDGER` TSV + `--owner <sub>`
   column: memory `project_managing_subproject` commitment 6. The
   daily tally rides in `checks/<date>.md`; the same linter fires
   pre-landing via `/close` → `specs-audit.sh --lint-paths` (close.sh exit 45).
   Three labeled ARMS ride this commitment, same number (folded from the
   retired standalone cron-lane slot, 2026-07-25) — cron-lane health (live
   launchd lane; incl. the exit-75 collapse rule + the trading-chain
   artifact-existence check), S5-scan (verifier FINDING lines), and memsearch
   Stop-hook health. Arm findings rank as stated in `checker.md` #6 —
   cron-lane hits, S5 divergence, and trading-chain holes rank
   **functionality**, not spec-hygiene correctness.
7. **Claude permission-settings drift.** `scripts/settings-drift.sh` is the
   source of truth; `drift=YES` or `lint=ERRORS` is a **correctness** finding
   (regenerate via `scripts/claude-settings/build.py`). Hand-edit drift only;
   new allow patterns are the weekly `dco-settings` lane's job.
8. **Brand / kit-version drift.** `scripts/brand-drift.sh` is the source of
   truth; `drift=YES` is a **correctness** finding. Two classes fold into that
   one signal. (a) *Kit-version* — a `KIT_VERSION` producer pin or the loader
   off the kit `package.json` version (the silent same-major class).
   (b) *Overlay byte-mirror parity* (arm 2a, landed 2026-07-23) — byte-compare
   of the rendering overlay SoT → consumer mirror pairs
   (`rendering/brand/tokens/quantapix/overlay/*.css` → the three visualizing
   kits + designing's `thesis-steps/`), an `UNREGISTERED` sweep so a net-new
   overlay cannot ride uncovered, and the two headless resolved-literal maps
   (`DEFAULT_TOKENS` / `DEFAULT_TOKENS_3D`) vs their DARK slices, key-set +
   value equality. Same severity, **bigger blast radius** — an overlay
   divergence ships two palettes to a live surface, silently (mechanism +
   the `--q3d-projected` white-cell case: memory
   `feedback_two_token_mirrors_ship_two_palettes`).
9. **Cron-seat capability + roster + posture + flip.** `scripts/seat-drift.sh`
   is the source of truth (wraps `data/schedules/launchd/seat_preflight.sh`;
   bit-field exit 1=capability, 2=roster). Four facts, ranked differently:
   - `capability=GAPS` **on the seat holder** → **functionality**, highest
     severity: that host's fires refuse at fire time with `exit=72`. Gaps **off**
     the holder are a readiness report about a future flip: echo, never promote.
   - `roster=DRIFT` → **correctness**. A declared-but-unplisted routine never
     fires and writes no log, so commitment 6's cron-lane arm cannot see it —
     **the checker only sees what FIRES; this is the one check that looks at
     what didn't.** Fix is `install.sh --enable` on the holder.
   - `posture=OFF-POSTURE-STALE` (≥ 7d off Posture A) → **correctness**; bare
     `OFF-POSTURE` is tally-only.
   - `flip=STALE-UNACCEPTED` (a committed SEAT flip with ≥ 1 full 21:00–21:59
     local window elapsed and no holder-side landing line — `qagents-seat OK
     host=<new> seat=<new>` / `CHANGEOVER-ACCEPTED` / `changeover=bootstrap`)
     → **functionality**. `flip=PENDING` and `flip=UNKNOWN` (non-holder) are
     tally-only; `flip=landed` is green. Detail: `checker.md` #9.
   Rationale (exclusivity ≠ capability; the `monitoring:archive-scan` instance):
   `checker.md` commitment #9 + memory `project_mobile_cron_seat`. Spec:
   `data/specs/node-return-lane-2026-07-14/SPEC.md` § 2, § 6.1, § 10 Q2.
10. **Node-PR staleness.** `scripts/node-pr-staleness.sh` is the source of
   truth (observe-only; roster-scoped remote-tracking refs, never fetches).
   An unmerged node PR older than 7 days (`stale=YES`) → **consistency**
   finding — a waiting contributor, not a broken system; everything else is
   tally-only. Answered via `/pull <subproj>` or a rejection note back to the
   node. Same lane, no new number (S4, 2026-07-23): `scripts/node-pr-gate.sh`
   evaluates every OPEN node PR against its topic's declared-surface
   allow-list + deletion refusal (closed set; no auto-widening). Any
   `verdict=BLOCK` row → **correctness** finding surfaced verbatim — that PR
   must not merge until amended or explicitly ruled. Specs:
   `data/specs/data-charters-2026-07-16/SPEC.md` § 6.2 step 7 (AUDIT-C4) +
   `data/specs/node-return-lane-2026-07-14/SPEC.md` § 5 + § 8 Phase S4.

11. **Flow-clause hygiene (tree-wide safety net).** `scripts/flow-lint.sh` is
   the source of truth (wraps `python -m qagents.flow_graph lint` at canonical
   — the SAME engine `close.sh --flow-lint` shells to; grammar owner
   `data/specs/flow-graph-2026-07-16/SPEC.md` § 3/§ 7 Arm 2). Any HARD line →
   **correctness**; the load-bearing shape is a dangling `ns:` target — slot X
   resolved a blocker while untouched slot Y still cites it, which the
   close-time gate cannot see. Advisories + the summary are tally-only.
   Observe-only: route fixes to the citing slot's owner session.
12. **Shorting review-lane hand-offs + D-4 escalation — LANE LEGS RETIRED
   2026-07-28.** `/do-retire` P2 lane 1 purged `shorting/{shorten,share,spread}/`
   under R-3 and R-4; the reports are in `archive.blob`. `spread-runway.sh` now
   prints `lane=<l> RETIRED` and `handback RETIRED` instead of reading them.
   **Still live:** the `p0_runway_slots` leg, which reads
   `data/next-steps/*.md` and is untouched — keep it in the read set. Treat a
   `RETIRED` line as expected output, never a finding. If a future `/do-spread`
   run re-creates the directories (it is deferred, not abolished) the legs
   light up again with no edit here, and the triage rules revert to
   `shorting/CLAUDE.md` § 5 + optimization charter § 2.7 D-4 SLA.
13. **Spec-family test-battery health.** `scripts/spec-battery.sh` is the
   source of truth — the loud aggregating runner over every spec-family /
   charter / subproject-harness `run.sh` tree-wide (per-suite timeout,
   always exit 0). Any
   `FAIL`/`TIMEOUT` row → **correctness** (silent-red shape-gate: an artifact
   landed without its expected-set update — the studying `t_02_quartet`
   class). Discipline: the expected-set update lands in the SAME change.
   **One row is honest red, not noise:** `store-durability-2026-07-26`'s suite
   (in the `:49` glob since its 2026-07-28 promotion out of `data/tmp/`)
   exercises the LIVE store daily — a 91 MB dump copy, a scratch DB on qblk's
   `18/verify`, a full `pg_restore` (~6 s, inside `TIMEOUT=120`) — and **exits 3
   when the verify cluster is unreachable**. That is the gate saying it could
   not verify (`feedback_could_not_look_is_not_a_verdict`), so on LAN-down
   nights the battery gains a failing row; `spec-battery.sh:96` ends in an
   unconditional `exit 0`, so nothing breaks, but anything that ever starts
   COUNTING battery reds must not filter it. Do **not** "fix" it by making the
   live arm opt-in — that converts every ordinary run into a NOT-RUN that still
   exits 0, which the suite's exit-1-on-NOT-RUN rule exists to prevent. If the
   daily cost stops being worth it, change the schedule (operator ruling
   2026-07-28; rationale in that suite's README).
14. **Blind-metric provenance on published figures.**
   `scripts/blind-metric-drift.sh` is the source of truth (day-over-day
   changed statCards on `data/status/{proving,accounting}.json`; recency
   values filtered). A changed coverage/tier figure whose minting wave +
   closed-oracle status cannot be named from the owning sub's newest close
   summary / conformance matrix → **correctness**
   (`feedback_blind_fanout_oracle_channels`). `withheld` is the correct
   posture, never a finding.

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
| `verifier` | `haiku` | `checks/<date>.pending.json` (coordinator-appended per above) | All files under `pending/`; rules table embedded in agent prompt | Closed-set allow-list classifier (default-skip); emits `passes[]` + `internal[]` + `unclassified[]`. Only `passes[]` drives the lock-protected rsync in `data/schedules/launchd/verify-pending.sh` (Layer 2 guards exit 8/9/10). Spec: `data/specs/pending-promotion-scope-2026-05-28/SPEC.md`. |

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
SDK-related finding**: `data/agent-sdk-ledger/` failure-stage findings,
SDK-lane fire failures, `agent-sdk-adoption-2026-05-17` spec-phase stalls /
OVER-CAP, SDK-credit references, and `pending/data/agent-sdk-ledger/**`
unclassified surfacing (classified DORMANT in the verifier internal-set +
`verify-pending.sh`). Reversible, dated directive — drop the suppression
when access returns. Memory: `reference_agent_sdk_credit_200_mo`.

## 4. Functionality probes — random, weighted

Each run picks 2–3 probes from a weighted pool. **Random selection is
load-bearing** — it prevents the watcher from drifting into a fixed pattern
and missing intermittent failures elsewhere. Families + weights + pass/fail
predicates live in `managing/probes.md` (P1..P7 + weight-summary table);
checker reads from there. `managing/scripts/probe-pick.sh --k 2` is the picker
(pure-awk seeded weighted draw — bounded rejection, deterministic order
fallback; no GNU shuf dep), seeded `date +%j` — deterministic per day, varied
across days.

## 5. Boundaries

Two lanes with different posture. The "observe-only" framing applies
to the cron lane; the interactive lane behaves like any other
qagents subproject session.

### 5.1 Cron lane (the daily watcher)

Observe-only with one tightly-scoped exception — the `pending/`
verification flow (§ 5.3). The 06:00 coordinator and its four
subagents never `git push`, never deploy, never mutate code or copy
in any subproject; the lane commits only its own dated outputs +
the verifier pass-list, under the audit prefixes `[managing] daily
<DATE>:` / `[managing] verify <DATE>:` (§ 5.3). The three dated `.md`
outputs (`checks/`, `tasks/`, `reports/`) ARE the surface: the operator
(or a follow-on session) reads them, decides which to act on, and the
resulting work happens inside the relevant subproject — never in the
cron output.

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
promoted via `verify-pending.sh`'s `promote_cron_ec2` lane (spec
`data/specs/cron-ec2-migration-2026-05-19/infra-2026-05-19/SPEC.md` § 3.6 + § 3.9 step 10),
(c) the ns-drain render commit — the re-rendered `data/next-steps/`
projections under the shared message `render: next-steps projections`
(load-bearing string, keep byte-identical: the substrate close lifecycle
emits the same message, and a compile-time assertion +
`data/next-steps/CLAUDE.md:238` + the reporter's window filter all key on
it; audit discriminator: the drain commits direct-to-main during a fire,
the close-lane render arrives via a session-branch merge),
plus its own dated outputs
(`managing/{checks,reports,tasks}/<DATE>.md`, including the
`.pending.json` sidecar), ONLY with the message prefix
`[managing] verify <DATE>:` (or `[managing] daily <DATE>:` for the
own-outputs lane), AND ONLY while holding the canonical
`.data-write-lock` for the promotion lanes.

The exception lives entirely inside `data/schedules/launchd/verify-pending.sh`
— that script is the single audit surface. The four-subagent fan-out
itself never commits; the coordinator invokes the script after subagents
return. Audit signal: `git log --grep "^\[managing\] verify"` lists every
output of this flow.

Script mechanics — manual `--force` invocation, `prune_stale_fails`, the
S5 state write-back + the `push_to_authority` silent-SPOF rule:
`data/schedules/CLAUDE.md` § "`verify-pending.sh` — script mechanics".

## 6. Layout

`README.md` (quickstart + cron command) · `probes.md` (weighted random-probe
pool, § 4) · `scripts/` (mechanical bash-3.2-portable fact-emitters +
`status_emit.mjs`; `scripts/tests/` is the bash harness — run.sh + cases/,
owner of the specs-audit `owner` column + `--owner`) · `.claude/` (the
standard subproject shape per root CLAUDE.md § "Subproject `.claude/` shape";
`agents/` holds `checker.md` / `planner.md` / `reporter.md` / `verifier.md`) ·
`checks/` + `tasks/` + `reports/` (the three dated outputs, § 1).

`checks/`, `tasks/`, `reports/` are committed (markdown is the source of
truth and lets future sessions reconstruct multi-day trajectories) — but
**bounded at 7 days on disk since 2026-07-29**, when `/do-retire` P2 lane 4
first reaped them (271 files). Older days are byte-exact in `archive.blob`:
`bash scripts/retire.sh --restore 'managing/checks/*' --dest <dir>`. A
trajectory longer than a week is a store query now, not a `ls`.

**That TTL is bounded by these agents' own declared lookbacks, so the two
move in lockstep** (§ 1.1's discipline, one level out).
`data/specs/do-retire-2026-07-26/lanes.tsv` records `consumer_window` =
**1** for `reports/` + `checks/` (reporter reads yesterday's checks+tasks;
planner reads yesterday's tasks+report; `verify-pending.sh` reads TODAY's
`checks/<DATE>.pending.json`) and **3** for `tasks/` (`planner.md:45` calls
a task stale after rolling over "3 days in a row" — the deepest read in the
trio). Widening any agent's lookback past its column is a two-file change;
a lookback the registry does not record is how a reap silently narrows the
watcher's own evidence. `reporter.md:22` forbids assuming continuity from
earlier reports, which is what keeps these windows this short.

## 7. Schedule

Cron-fired daily at 06:00 local via the qagents launchd scheduler at
`data/schedules/`. Registered as `com.qagents.managing-daily`; pointer row in
`data/schedules/cron_triggers.md` (the ROUTINES array is the schedule's
source of truth); ROUTINES entry
`managing:daily:06:00:0,1,2,3,4,5,6` in `data/schedules/launchd/install.sh`.
(The routine's `:sdk` token was removed 2026-06-30 — root CLAUDE.md
§ Agent SDK lane; § 3.1 owns the suppressed-finding class.) The fired
routine is the coordinator prompt at
`managing/.claude/coordinator-prompt.txt`, piped to `claude --print` by
`data/schedules/launchd/run_routine.sh`. The coordinator runs the four
subagents (three top-tier + one haiku verifier) in parallel and exits;
runtime budget ≤ 10 min (subagents wrap independently).
Per-run cost caps come from `run_routine.sh`'s `routine_policy_budget()`,
paired with `routine_policy_model` so a routine's tier and its funding cannot
drift apart; `daily` (managing's own) is $9 USD. Never `RemoteTrigger` /
`CronCreate` / cloud `/schedule` (root CLAUDE.md § `data/schedules/` owns
the rule; rationale `data/schedules/Notes.md`).

### 7.1 The cron lane is SEAT-GATED and MOBILE (2026-07-14)

Spec: `data/specs/node-return-lane-2026-07-14/SPEC.md`; memory
`project_mobile_cron_seat`. The lane runs on **exactly one laptop at a time** —
`qyel` or `qpur`, the only two hosts with a "head" (headless boxes cannot hold a
Claude subscription seat). `data/schedules/SEAT` names the holder;
`run_routine.sh :: assert_seat_holder` **freshly reads it from the `github`
authority before every fire** and refuses otherwise.

Three consequences that bind `managing/`:

- **A non-holder logs `exit=0 skipped=not-seat-holder`.** That is a no-op, **not a
  failure** — the checker's non-zero-exit scan must never score it as one.
- **A holder-side `exit=75` (CHANGEOVER-DEFERRED) span collapses to ONE finding
  per day** — carrying `refused=N of expected=M` with slot labels;
  **functionality** when the dark span overlaps 08:30–16:45 ET on a weekday; a
  BLOCKED fire never collapses into it. The action text names the real landing
  step — manual `launchctl kickstart` on the incoming host during 21:00–21:59
  local, or `rm .seat-observed` (next fire logs `changeover=bootstrap`) —
  never "resumes 21:00": the roster schedules zero fires inside that window.
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
read `data/specs/cron-ec2-migration-2026-05-19/SPEC.md` § Status.

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
