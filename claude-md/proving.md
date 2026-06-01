# proving — Lean4 axiomatic theorem-proving with LLM-backed predicates

Sibling of `analyzing/`, `trading/`, `designing/`, `documenting/`,
`monitoring/`. Cross-project rules: root `CLAUDE.md`. Backs the **Qnarre**
product — public slice at `qnarre-public`.

## The split

The whole point of this subproject is **strict jurisdictional separation**
between three layers. Do not blur them.

| Layer | Where | Reads | Writes | Tools |
|---|---|---|---|---|
| **Formal kernel** | `Proving/<Framework>/*.lean` | only Lean | only Lean | Lean elaborator. No I/O, no LLM calls, no memsearch. |
| **Predicate functions** | `predicates/<framework>/*.md` | one complaint text + entity refs | a single `Bool` (plus evidence + uncertainty) | LLM sub-agent (`context: fork`); MAY use the `memory-recall` skill. |
| **Driver** | `scripts/extract_facts.py` | manifest + complaint | the framework's generated `Facts.lean` (axioms) + audit JSON | LLM invocations (Haiku by default). |

The Lean kernel never reads natural language. The predicate sub-agents
never write Lean. The driver is a thin coordinator with no legal reasoning
of its own. The verifiable proof IS the Lean elaboration trace produced by
`lake build`.

## Why this works

1. The semantic memory store sees only natural-language artefacts — it
   never tries to embed Lean dependent types.
2. Predicate functions have a very narrow output domain (one Bool per
   call) — they fit comfortably inside a forked sub-agent.
3. Lean's kernel verifies composition. Once each predicate fact is
   recorded as an axiom, the validity theorem is a pure
   structure-introduction proof — if it type-checks, the result is
   mathematically guaranteed *given the predicate truths*.
4. The audit trail is the JSON in `examples/<id>/facts.json` — every
   predicate output, with evidence quotes and uncertainty.

## Frameworks

Each framework lives under `Proving/<Framework>/` (kernel) +
`predicates/<framework>/` (specs).

| Framework | Kernel | Specs | Statutory basis |
|---|---|---|---|
| **Civil RICO** | `Proving/Rico/` | `predicates/rico/` | 18 U.S.C. §§ 1961–1968; § 1962(a)(b)(c)(d) + § 1964(c) standing |
| **Title VI** | `Proving/TitleVI/` | `predicates/titlevi/` | 42 U.S.C. §§ 2000d et seq.; intentional / disparate-impact / retaliation |
| **CivilRights** | `Proving/CivilRights/` | `predicates/civilrights/` | 42 U.S.C. §§ 1981, 1983, 1985(3) |

The operative statutory text lives under a pinned, vendored U.S. Code
mirror, not pasted into specs. Predicate sub-agents resolve a `usc_cite`
via a path/text/list lookup against an index file. These three hand-built
frameworks are the **golden reference** for the program below.

Spec roster: RICO 28 specs (14 common + 4 c + 3 a + 3 b + 4 d); Title VI
17 specs (7 coverage + 2 intentional + 5 disparate-impact + 3
retaliation); CivilRights 14 specs (4 § 1981 + 5 § 1983 + 5 § 1985(3)).

## Axiomatizing the full U.S. Code (program)

Extends the three hand-built frameworks to a phased, title-by-title
program over all 54 titles, produced redundantly by Opus subagent teams
along ≥ 5 orthogonal strategies (Elements / Deontic / Ontology / Procedure
/ Structure / Remedy), then reconciled. Cross-strategy agreement, proved in
the kernel via `Bridge.lean` lemmas, is the correctness signal for the
LLM→Lean mapping — no other oracle exists.

- **Ground truth in place:** a full U.S. Code markdown mirror (on the
  order of tens of thousands of sections, all 54 titles) bound to a pinned
  release point, with a durable off-site archive so a proof stays
  reproducible after the source rotates. Conventions, per-axis strategy
  briefings, and a shared cross-strategy predicate library are frozen.
- **Naming / Lean-shapes / predicate-shapes** are frozen in the spec;
  per-(title, axis) Lean namespaces; shared cross-title predicates collapse
  to a `Common` namespace, each collapse guarded by an equivalence Bridge.
- **Calibration anchor (hand-built, kernel-green):** the canonical
  racketeering operating-or-managing provision encoded under all six axes
  with its cross-strategy Bridges discharged at full tier (no `sorry`).
  This is the template every cell mirrors and the reference the fan-out is
  scored against.
- **Bridge-based calibration:** agreement-vs-golden is measured by
  kernel-checked golden-bridges — the blind cell's composite implies the
  golden composite under declared correspondence axioms, discharged
  sorry-free. Exact predicate-name matching is retained only as a
  regression check for hand-built cells; for blind agents, naming is a free
  variable, so a name-match score is unwinnable.
- **Lane:** a programmatic batch lane (gated on a 2026-06-15 credit
  activation) + a manual-interactive bridge via the `/dau-manual` skill.
  Mechanical phases in `scripts/dau.sh`; LLM fan-out over per-role agent
  definitions. Zero-prompt fan-out is enforced (the fan-out must draw no
  manual approvals). Cells write to a gitignored sandbox, promoted only
  after a reconcile gate + human review.
- **Status:** foundation + conventions done; calibration anchor + several
  waves promoted (a no-golden-reference title under all five strategies; a
  golden-adjacent wave with a full-tier sorry-free property↔contract
  bridge; an employment-discrimination wave scored on cross-axis agreement
  alone; cross-title shared-predicate collapses). Remaining Phase 2 work is
  scale: fan out more sections, title by title. The authoritative build
  target is `lake build ProvingUSC`.

## Layout (essentials)

```
proving/
├── Proving.lean                    root module — imports both frameworks
├── lakefile.toml
├── lean-toolchain                  pinned Lean version
├── Proving/<Framework>/{Types,Predicates,Statute,Theorems}.lean
│                                   Facts.lean is GENERATED + gitignored
├── predicates/<framework>/         markdown specs (one per opaque predicate)
├── scripts/
│   ├── extract_facts.py            driver — reads the `framework` block from the manifest
│   ├── lake_trace.py               lake-build stderr → typed error records
│   ├── lean_parse.py               regex-based proof-file structural parser
│   └── uscode.py                   path/text/list lookup against the vendored U.S. Code mirror
├── graphs/                         design prompts for the proof-graph rendering kit
└── examples/<id>/                  per-run artefacts
```

## Hard rules — DO NOT violate

1. **Lean files MUST NOT do I/O.** No `IO`, no FFI. Kernel is pure.
2. **Predicate specs MUST NOT cite or read `Proving/<Framework>/*.lean`.**
   Their world is the complaint text + spec rubric.
3. **The driver MUST NOT make legal judgments.** Add fields to the JSON
   schema or a new `framework` block field rather than logic to the driver.
4. **`Facts.lean` is generated. Never hand-edit.** Both are gitignored.
5. **The semantic memory store never indexes Lean files** — excluded by
   design (it only scans markdown).
6. **Predicates live under `predicates/<framework>/`.**

## Per-run artefacts (`examples/<id>/`)

When invoked with `--build`, the driver emits a per-predicate audit JSON
(`facts.json`), the generated axiom block (`Facts.lean`), a full run record
(`report.json` — predicates + kernel verdict + per-error locus), a proof
DAG (`graph.json`, byte-compatible with the proof-graph rendering kit), and
a status-hub diagram (`loci.json`). The schema is locked at the consumer
boundary — any change to `graph.json` field names is a two-sided edit
against the kit loader.

`accounting/` mirrors this pipeline for the financial domain;
`lake_trace.py` is a verbatim copy across the two trees and must be patched
in lockstep. Deliberate accounting-side divergences (lowercase axiom names,
multi-judgment loci roster) are not drift.

## What we encode (one paragraph each)

**RICO** encodes § 1961 definitions (enterprise, pattern, unlawful debt,
culpable person), § 1962(c) operation-or-management, § 1962(a) investment,
§ 1962(b) acquisition, § 1962(d) conspiracy, and § 1964(c) standing
(proximate cause + 4-year limitations). The top-level validity proposition
is an inductive over the four substantive subsections.

**Title VI** encodes common coverage, intentional discrimination (direct +
the burden-shifting framework), disparate impact (admin-only), and
retaliation. The judicially- vs administratively-enforceable split is
encoded formally; the judicial validity inductive omits disparate impact.

**CivilRights** encodes § 1981 (racial-class plaintiff, intent,
contract-identification, but-for race causation), § 1983 (under-color,
federal-statutory rights, the § 1983 "person", moving-force, absence of
absolute immunity — qualified immunity is not decided by the predicate
layer), and § 1985(3) (meeting-of-minds + class-based animus).

## Redaction (separate channel)

Predicate sub-agents quote complaint text verbatim into evidence strings,
which flow through the per-run JSON + the status page. A deterministic
redaction pass scrubs those artefacts before they reach any public surface
— a **separate channel** from the document-redaction gate that sweeps the
public-filing staging tree. For a fresh `--build` run, the source complaint
must itself be redacted first, or the sub-agents will re-leak.

## Toolchain notes

Lean pinned via `lean-toolchain`; no Mathlib dependency in the initial
scaffold (keeps `lake build` fast). Python ≥ 3.10 for the driver (system
`python3`, no venv). Predicate sub-agents are text-reasoning-only by
default; when they need external tools they adopt a real-call flag set + a
driver-injected preamble, without which a Haiku sub-agent falls back to
stub-mode hallucinations even when the data hub is populated.
