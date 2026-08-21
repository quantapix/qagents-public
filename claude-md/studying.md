# CLAUDE.md — studying/

Project-specific rules for the **operational-axis Lean4 kernel + cross-axis
representation research** subproject. Assumes Claude Code's default guidance
and the repo-root `qagents/CLAUDE.md`. Don't re-litigate those.
Scope charter: `data/charters/studying/operational-axis/CHARTER.md` — the whole
`lean4-charter-2026-06-10` family (root of the three-axis architecture; root
CLAUDE.md § "Lean4 axes") is scope-resident at
`data/charters/studying/specs/lean4-charter-2026-06-10/` as an
`owner-living-program` (neutral-steward ownership; § 3 carves the uscode +
market-tape domains out to `proving/textual-axis` + `accounting/numerical-axis`).

## 1. Purpose

Axiomatizes the *operational* domain — what happens daily in qagents, git
first. Consumer: `monitoring/` (local-only); debate pairing: coding v. testing
(`/dao`, P2). Pure-mathlib paths (Topology, MeasureTheory, Analysis,
CategoryTheory) are out of scope.

## 2. Workstream A — representation research (cross-axis)

How to effectively *represent* all three Lean4 workflows — kernel shape,
facts-generation contract, debate protocol, verification gate — drawing from
the standard examples in `hub/theorem_proving_in_lean4` and
`hub/reference-manual`. Deliverables (spec § 5.1, P1):

- `studying/representation.md` — maps each standard TPiL4 / reference-manual
  idiom to its qagents kernel counterpart, three axes as parallel columns.
  The document LLM proof-drivers are pointed at; replaces folklore. Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/representation-guide-2026-06-10/SPEC.md`.
- `studying/thesis.md` — the **canonical public-distillation source** (seven-step
  cross-axis method synthesis + hero-node label contract); public-facing sibling of
  internal `representation.md`. Rendered out by `publishing/` → quantapix.com
  `/thesis` + the `qgraph-wire/1` hero; never copied out by `studying/`. The three
  public pages (`/thesis`+`/qnarre`+`/qresev`) are governed as one messaging surface
  (spec § 10; `pleading/` binding). Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/quantapix-thesis-2026-06-22/SPEC.md`.
- Code-generation templates the debate lanes consume (`mem_*_cases`-style
  helpers, axiom-list witness patterns, `Facts.lean` skeletons), extracted
  with `hub/vscode-lean4` as **template source only** — never installed as
  an interactive proof surface (spec § 4.2; no manual proof driving, ever).
- **Hierarchical-predicate object classes** — the cross-axis vocabulary all
  three axes use is `representation.md` Ch. 13, owned by
  `data/charters/proving/specs/axiomatize-uscode-2026-05-29/hierarchical-predicates-2026-06-20/SPEC.md`
  (tactic layer is kernel-side Lean, never a plugin — charter § 4 pin R2.5).
- **Hierarchical predicates H0/H1 — applied to the operational axis** (sibling
  parity with proving/accounting). H0 = the Mathlib-free tactic substrate in the
  shared `Common/` namespace (path deliberately unnamed — C5-graded roster; find
  it by behaviour); H1 = the `Operating/Qagents/Hier/`
  cell decomposing `OpenedAs` (the axis's single LLM-judged predicate) with a
  term-only `Bridge.lean` oracle guard, shrinking the lone model call to the
  narrow `has-session-footer` leaf. Specs `predicates/operating/hier/`;
  K-graph probe `op.Qagents.opened_as_hier`.

- **Proof-carrying context injection — Phases A+B+C SHIPPED (C 2026-07-16: the
  fork-isolated `kernel-recall` pull skill, `studying/skills/kernel-recall/`).** Spec
  `data/charters/studying/specs/lean4-charter-2026-06-10/proof-context-injection-2026-07-09/SPEC.md`
  + ADOPT-AMEND debate record `proof-context-injection-2026-07-09` (data/debates/, HELD lane) (PRIVACY
  9-cond + NO-MANUAL-PROVING 4-cond). The machinery roster AND the two biting
  invariants are the SPEC's — don't mirror them here: R2 (state-key = digest of the
  extractor input snapshot, never HEAD) at SPEC § 6; R15 (machine-context seam,
  `monitoring/` sole consumer, non-precedential) at SPEC § inv-5. Mid-migration to
  a `qx` shim (`ns:studying/39`).
  Ledger privacy: § 5.1.2(c) path-blocklist carries (committed-but-never-published
  — the `studying_entailment_ledger` Stage-4 rule in
  `publishing/scripts/sync_mirror.py`).

## 3. Workstream B — operational axiomatization (git first)

Map git (`hub/git` as ground truth) into Lean4 axioms, structured like
`proving/Proving/<Framework>/` and `accounting/Accounting/<Framework>/`,
closely following the template of `hub/cslib`. Lake package:
`studying/Operating/`, module root `Operating/` — module-relative paths below,
with the `Operating/{Git,Qagents}/` quartets (executing
subspec `data/charters/studying/specs/lean4-charter-2026-06-10/axiomatize-git-2026-06-10/SPEC.md`;
content emit co-located at `Operating/emits/`). The qagents angle is the point:
first theorems target *our* operational invariants —
branch-presence-as-write-lock exclusion, `/close` cascade safety,
canonical-vs-worktree divergence — with git's semantics as the axiom layer
beneath them. Proofs are driven by the coding-v.-testing `/dao` debate lane
(manual-interactive first: `/dao-manual`), never manually.

**HARD RULE — adversarial independence is the ONLY oracle.** A parried attack is
evidence *only* if the attacker did not know the proof and the proof was not
pre-hardened against the attack list. Closing one leak channel buys nothing —
the doctrine is protect-all-or-nothing, and the channel roster is not enumerated
here (see the pointer two paragraphs down).

**THIS FILE IS A LEAK SURFACE NO INSTRUMENT CAN GRADE, and a SPLIT is the only
cure that reaches it — landed 2026-08-20 (`ns:studying/160`, off ledger L-278).**
A subproject `CLAUDE.md` is delivered to every subagent in SYSTEM CONTEXT, which
no graded channel can see (every channel grades a READ) and which the transcript
does not record, so a transcript check's silence reads exactly like absence. A
brief-side prohibition cannot reach a disclosure authored in the INSTRUCTION
layer; this axis had already recorded that lesson about a MANDATE and failed to
apply it to a NAMING one paragraph away, in the same file. **Standing authoring
rule — permanent, and not conditional on any assessment of whether cells receive
this file: nothing answer-shaped goes in here.** No example identifiers, no round
history or agendas, no per-example findings, no adjudication figures, and no path
to any orchestrator-facing document. Route all of it to the ns slot or to those
documents. Whether `/dao` cells actually receive this file remains `owed: assess`
and is not claimed either way — the split removes the payload, so the answer no
longer gates a round.

**ORCHESTRATOR-FACING DOCTRINE — paths deliberately unnamed, the same C5
discipline § 2 applies to the H0 roster; find the set by behaviour.** Every such
document at this subproject's root carries the literal marker
`ORCHESTRATOR-facing` in its header, so one `grep -l` over `studying/*.md` is the
index and nothing here re-lists it (this file matches too — it names the marker). Between them they own: the `/dao` blindness-
firewall doctrine (channel anatomy, the brief channel, the round loop, the
`mandate_conflict.py` wiring, the spec-of-record cite); the evidence-archive and
gate/instrument doctrine (including the axiom floor, the clean-verdict bound, and
every published-figure basis); and the per-family completion records with their
compact roster. Read the relevant one before authoring any `/dao` round brief,
running `--blindness-audit`, freezing or verifying a round's evidence, landing
anything under `code/lean_tools/`, or quoting any adjudication figure anywhere
public. **Neither those documents nor any path they name may appear in a blind
cell's brief** — a rule that is enforceable for the first time now that this file
no longer supplies the paths. Per-round state stays `ns:studying/60`; the round
scoping, the mechanical breach-refusal and the `--round-close` step order are
SKILL mechanics (`.claude/skills/dao-manual/SKILL.md`).

**`mandate_conflict.py` screens this file plus both cell contracts — re-run it
after editing any of the three.** It reports no conflict today. It cannot see the
system-context payload, which is why the authoring rule above is a discipline and
not a gate.

**Daily unit = the SENTINEL, seated at `studying:dao-state` 07:45 daily**
(`ns:studying/91`; six-part registration 2026-08-16). 07:45 is ORDERED — arm (e)
reads managing's 06:00 report, the opposite ordering from `proving:axiom-state`
05:10 whose output managing scans. DARK until the operator runs `install.sh
--enable` on BOTH seats (qyel + qpur — studying's archives are host-split); row
in `data/schedules/pending-enable.md`. Until then, fire it by hand at session
open. **The host-relative census arm that held this enable back is now measured
GREEN on both seats (2026-08-20, `ns:studying/154`)** — the doctrine, the
mechanism and the measurement live in the orchestrator-facing evidence-archive
document, not here.

## 4. Guide-rails — `hub/` governance

`studying/guide-rails.md` is the committed manifest over the five Lean4
guide-rail clones in root-level `hub/` (root CLAUDE.md § Shared-code hubs owns
the hub's read-only + gitignored posture). Refresh is manual from an
`/open studying` session via `studying/scripts/hub_refresh.sh` (`--check` = the
charter's P0 test; read the docs-vs-pin skew note at each refresh). Adding a
row is a manifest + script + spec amendment. lean4 source citations use
upstream GitHub URLs (side-clone convention retired, charter D3).

## 5. Toolchain — three-way lockstep

`studying/lean-toolchain` is pinned in lockstep with `proving/lean-toolchain` +
`accounting/lean-toolchain` (the pin value is the file itself + the `guide-rails.md`
skew note — not restated here). Any bump moves all three and replays each kernel's
example proofs (`feedback_lean_toolchain_bump_verify_example_proofs`). **Studying
carries TWO pins**, not one: `studying/lean-toolchain` *and*
`studying/Operating/lean-toolchain` (the Operating package is the actual kernel) —
both move together or `elan` resolves differently depending on cwd. **"One commit"
is not always achievable — record the deviation:** when each axis is held by its
own open session the bump lands one commit per branch, in lockstep in time, each
independently verified. Say so; never let the three drift across a day.

**The pin is CWD-DEPENDENT (2026-07-14).** `elan` reads `lean-toolchain` from the
*current directory*, so a bare `lean` run anywhere without a pin file (a sandbox probe
dir, `/tmp`) silently falls back to elan's **default** toolchain — it voided real
textual-axis work (anatomy: `reference_lean_isolation_probe_full_path_imports`).
Always `lake env` from the package root, or `elan run leanprover/lean4:<pin> lean`. A
file-in-the-root is not a pin for any process whose cwd is elsewhere.

## 6. Source authority

`studying/focus-areas.md` is the **single source** for the ranked focus
areas, their difficulty ratings, reading order, active threads to track, and
the skip list — each area tagged to Workstream A or B. Don't fork the
syllabus into multiple files; edit the same file — the commit log is the
change record.

**Dated narratives are ARMED ephemeral lanes (since 2026-08-06).** `AUDIT-*.md` and
`weekly/*.md` are `ephemeral` (ttl in `data/specs/do-retire-2026-07-26/lanes.tsv`,
the single source of truth — never a remembered figure). A new audit narrative lives
about a week on disk: freeze the verdict into its rounds file or a CLAUDE.md standing
section, and promote sole-copy evidence via `scripts/retire-evidence-promote.sh`,
**before** anything relies on it. Git + `archive.blob` are the retention; the file is
not. **A CITE into such a lane is UNGRADED — do not infer safety from a green
`--check-cites`** (`ns:studying/127` / `ns:qagents/170`; anatomy in memory
`project_do_retire_spec`), so an ns body citing a dated artifact carries the durable
commit SHA beside the path.

## 7. Public-facing derivation

The public `qstudying-public` README is rendered from `focus-areas.md` (§ 6) by
`publishing/` during `/publish` (redaction + voice guardrails; drive Promise 1;
spec `data/specs/publishing-2026-05-31/`) — `studying/` never renders or copies
it out. See `feedback_public_facing_source_render_split.md`.

## 8. Scope boundary

No imports from `analyzing/`, `trading/`, or any other code-bearing
subproject; no cross-kernel imports (`proving/`/`accounting/`) and no
importing the consumer (`monitoring/`) — the seam is files, never code. The
only outbound dependency is *content*: focus-area summaries via
`publishing/`, the emitted workflow JSON `monitoring/` mounts (day-one per
the round-1 ruling, debate record `representation-guide-2026-06-10` — data/debates/, HELD lane), and
the code-generation templates at `studying/templates/` the debate lanes
read at prompt-assembly time (never imported or built).

## Status emit (`data/status/studying.json`)

`studying/scripts/status_emit.mjs` participates in the qagents-wide Status page
contract. The pill computes the charter P2 gate from the tree (spec § 5.3) and
honestly degrades to `NOT_YET_LIVE` if a checkout lacks the example artifacts.
The slot carries the real toolchain pin (read from `studying/lean-toolchain`),
focus-area count, and lane metrics. Schema `@qagents/diagram-kit`; contract
`qagents/CLAUDE.md` § "Status hub". **Read every value from the tree or from a
run — never from this file.**

**PUBLISHED FIGURES — every counting basis, every stamp obligation, and every
standing ruling that governs quoting an adjudication figure on a public surface
live in the orchestrator-facing gate/instrument document** (§ 3 names the
find-by-behaviour rule). They are deliberately not restated here and **no figure
appears here**: a count a cell could recognise as a verdict is exactly the
payload the § 3 authoring rule excludes, and this section carried the largest
such payload in the file until 2026-08-20. Read that document before quoting
`theoremsProved`, any round count, or any adjudication pair — each carries stamp
obligations that make the difference between an honest figure and a withdrawn
one.
