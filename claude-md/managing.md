# managing — the constellation watcher

Project-specific rules for the qagents-constellation daily watcher.
Cross-project rules: root `CLAUDE.md`.

## 1. Purpose

`managing/` is a meta-observer over the entire constellation. It runs once a
day (cron-fired, top individual tier) and produces three dated artifacts:

- `checks/<date>.md` — the top **5** issues across consistency /
  correctness / functionality. **Functionality is always highest
  priority** — a failed live probe outranks any consistency or correctness
  finding.
- `tasks/<date>.md` — the **10** most pressing items for the day, ranked,
  drawn from today's checks, yesterday's untackled items, and visible
  backlog.
- `reports/<date>.md` — % completion of **yesterday's** checks + tasks, with
  evidence (commit hashes, file changes, deploy log lines).

Objective: **keep an eye on the ball.** managing/ does not fix anything; it
surfaces what needs fixing and tracks whether the rest of the constellation
is making progress.

### 1.1 Pinned commitments — what "the ball" is

Load-bearing objectives the subagents weight above generic drift detection;
a miss against any is a functionality finding. Discovered dynamically (e.g.
deadline anchors grepped across the tree), they include: firm deliverable
dates, weekly summaries on the public GitHub org (any public repo with
`pushedAt` older than 7 days is a finding), rapid progress in the study +
video subprojects, a `/status` refresh cadence, donation-drive credibility
(endpoint liveness once the products are live + on-time monthly ledgers),
and spec hygiene (a `[in-flight]` phase untouched > 14 days, a stale `tmp/`
proposal > 7 days, an adopted-orphan `tmp/` entry, a test dir missing its
required shape). The single source of truth for the spec tally is an audit
script; the daily tally rides in `checks/<date>.md`.

## 2. Subagents, clean contexts each

The cron fire spawns three top-tier subagents + one small-tier verifier in
parallel, each with a clean context. Each owns exactly one output file (the
verifier owns two) and writes it directly to disk; the coordinator sees only
their one-line completion confirmations — **no accumulated context bleed**.
Same fork-isolation lever the recall lane uses.

| Subagent | Output | Notes |
|---|---|---|
| `checker` | `checks/<date>.md` | consistency / correctness / functionality; top 5, ranked, functionality first |
| `planner` | `tasks/<date>.md` | 10 ranked items |
| `reporter` | `reports/<date>.md` | % completion mapped from commits / new files |
| `verifier` | a machine-readable pass-list + an appended section | closed-set allow-list classifier (default-skip); emits `passes[]` + `internal[]` + `unclassified[]` |

Subagent prompts list exact inputs to read and the exact output path to
write — they do not negotiate scope at runtime.

## 3. Three categories — what counts

**Consistency:** voice mismatches against the engineer-not-activist voice;
naming drift (a banned brand string, product-name typos, an outdated company
name); CLAUDE.md ↔ memory ↔ visible-copy divergence; producer/consumer
schema drift. **Correctness:** broken file references after a rename; dead
anchor links (the trailing-slash rule); statutory citations whose index
lookup fails; a status slot failing the kit's parse or drifting on
`kitVersion`; typecheck regressions visible from the commit log; spec
hygiene. **Functionality (highest priority):** live HTTP 200 + non-empty
body on a random route; `last-modified` not stale vs the latest deploy
commit; a random Playwright spec replay against a live site; a failed
public-org Actions run in the last 24 h; status-hub freshness. A
functionality failure is the day's top issue, full stop.

## 4. Functionality probes — random, weighted

Each run picks 2–3 probes from a weighted pool. **Random selection is
load-bearing** — it prevents the watcher from drifting into a fixed pattern
and missing intermittent failures. The seed is the day-of-year
(deterministic per day, varied across days); a pure-awk picker does the
selection (no GNU `shuf` dependency).

## 5. Boundaries — two lanes

**Cron lane (the daily watcher):** observe-only with one tightly-scoped
exception — the `pending/` verification flow. The coordinator and its
subagents never `git push`, deploy, or mutate code/copy in any subproject.
Findings flow through the three dated `.md` outputs into the operator's
queue, not into git. The cron lane commits only its own dated outputs + the
verifier pass-list, with audit-prefixed messages. **Interactive lane (an
operator session):** a normal qagents session — reads any file, edits
managing/'s own surface, may contribute shared-data conventions; commits
land through `/close`'s audit gate, not ad-hoc `git commit` (a deny in
settings enforces that). Common to both: live probes via `curl` / `gh` /
e2e; neither lane may force-push, mutate external state without operator
approval, or `rm` outside `pending/`.

**Pending verification — the lock-protected exception.** managing MAY
commit only the verifier's pass-list paths + clean-exit cron run-dir
contents, only with the audit-prefixed message, and only while holding the
root-anchored data write-lock. The exception lives entirely inside the
verify-pending script — that script is the single audit surface; the
subagent fan-out itself never commits. Manual ad-hoc invocations follow the
same path (with a force-accept escape hatch that's itself audit-prefixed).
The same script prunes stale, tiny `pending/**` stubs at the end of every
fire.

## 8. Voice + format for output files

The dated outputs use the **engineer-debugging-a-system register**. Each
finding carries: a one-line title, evidence (file:line, commit hash, URL +
HTTP status), a severity tag (functionality > correctness > consistency),
and a one-line imperative proposed action. No "we should consider…", no
rhetorical questions, no exhortations. File references are repo-relative
paths, not prose descriptions.

## 9. Scope boundary

managing/ does not import from any sibling (the language-split rule). It
reads via the filesystem only; there are no shared-code seams — the data hub
for managing/ is the qagents tree itself. A read-side specialization of the
data-hub-not-shared-code pattern.
