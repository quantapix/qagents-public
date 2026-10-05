#!/usr/bin/env python3
"""attest_axioms.py — axiom-closure attestation gate for Lean 4 packages.

EXIT-CODE SEMANTICS AT CALL SITES: exit 3 is could-not-look (the build is
absent, a module did not elaborate, a name did not resolve) and exit 2 is
the real finding. A caller must keep them apart. Flattening exit 3 into a
finding, or mapping every failure to a "precondition unmet" code, is the
same defect in opposite directions.

WHAT IT ATTESTS. For each target theorem it elaborates `#print axioms <thm>`
(the theorem's module must already `lake build`) and checks the reported axiom
closure is a SUBSET of the allowed set:

    allowed = {Classical.choice, propext, Quot.sound}          (the standard
              ∪ every `axiom` DECLARED under --root  (--allow-declared)  Lean
              ∪ any names passed via --allow-axioms                      axioms)

Any axiom in a closure that is NOT allowed fails the attestation — in
particular `sorryAx` (an unfinished proof) or any UNDECLARED axiom (one that no
`.lean` in the tree introduces with `axiom`). This is the pre-build / pre-freeze
/ pre-judge witness that "no theorem secretly leans on an undeclared axiom or a
`sorry`" — the closure-level backstop G2 (oracle guard: no search automation in
a Bridge body) and G5 (≥2-witness Common mint) do not cover.

Stdlib-only, importable AND runnable. It was written as one shared gate
for three separate Lean 4 packages (called "axes" in the comments below);
the dated notes in those comments record defects found on real trees.

CLI (faithful to the sibling tools):
  --root DIR         Lean package root the module path resolves under (default cwd).
  --module M         module to import (repeatable). Without --theorem, every
                     theorem/lemma DISCOVERED in M's source file (namespace-aware)
                     is attested.
  --theorem T        fully-qualified theorem name to attest (repeatable). Requires
                     at least one --module for the import.
  --scan-dir D       discover every *.lean under D → (module = path relative to
                     --root, dotted) + its theorems, and attest all of them.
  --allow-axioms L   comma-separated EXTRA allowed axiom names — the axis's
                     declared correspondence/domain axioms (repeatable).
  --allow-declared   union in every `axiom NAME` declared under --root's tree; a
                     declared axiom is by definition not a "secret" one.

Exit-code contract (aligned with score_bridge.py's convention):
  0  every target theorem's closure ⊆ allowed set (CLEAN attestation).
  2  ATTESTATION FAILURE: some closure carries sorryAx or an unexpected /
     undeclared axiom (the G7-fail code, per the apply-share spec).
  3  build / elaboration / resolution / usage error (module did not build, a
     requested theorem is unknown, no targets found, or --scan-dir not a dir).

Examples:
  python3 attest_axioms.py --root path/to/package \
      --module Pkg.Some.Module --allow-declared
  python3 attest_axioms.py --root path/to/package \
      --module Pkg.Some.Module \
      --theorem Pkg.Some.Module.some_theorem --allow-declared
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

# The three standard Lean axioms — always allowed (soundness-preserving).
STANDARD_AXIOMS = ("Classical.choice", "propext", "Quot.sound")

# Leaf names that are NEVER allowed, even if a caller foolishly allow-lists them:
# `sorryAx` is an unfinished proof; the *ReduceBool / native-decide escape hatches
# and the compiler-trust axiom are soundness holes (mirrors dao.sh's judge audit).
FORBIDDEN_LEAVES = frozenset(
    {"sorryAx", "ofReduceBool", "ofReduceNat", "trustCompiler"}
)
# …and a SHAPE rule beside the roster, because `native_decide` cannot be rostered
# (accounting ns-65, 2026-08-06). It mints a FRESH PER-DECLARATION axiom named
# after the theorem it closes — `myThm._native.native_decide.ax_1_1` — so the leaf
# is `ax_1_1` and no literal enumeration can ever reach it. The roster caught such
# axioms only ACCIDENTALLY, via the "not in the allowed set" arm; that arm is
# defeated the moment a caller passes a broad `--allow-axioms`, and an accidental
# catch is not a gate. Same conclusion the roster-vs-tree scoping finding forced
# one level up: match the SHAPE, not the enumeration. `score_bridge.py` already
# carries this rule for the bridge scorer — this is the attester's half.
FORBIDDEN_SHAPE = re.compile(r"\._native\.|\bnative_decide\b")

# ---------------------------------------------------------------------------
# Lean-source scanning (namespace-aware) — stdlib regex, no lake needed.

_NS_OPEN = re.compile(r"^\s*namespace\s+([A-Za-z0-9_.']+)")
_SEC_OPEN = re.compile(r"^\s*section\b\s*([A-Za-z0-9_.']*)")
_END = re.compile(r"^\s*end\b\s*([A-Za-z0-9_.']*)")
# A declaration line: optional leading @[…] attribute + modifiers, then the
# keyword + the declared name. `example` (anonymous) is intentionally excluded.
#
# The declared NAME may itself be DOTTED (accounting ns-62, 2026-08-06). Lean's
# ordinary projection idiom declares `axiom ClassifiedLeg.strategy : …`, and a
# name group of `[A-Za-z0-9_']+` truncated that to `ClassifiedLeg` — so the
# declared set held `<ns>.ClassifiedLeg` while `#print axioms` reported
# `<ns>.ClassifiedLeg.strategy`, and `--allow-declared` convicted three theorems
# for depending on an axiom the tree DECLARES three lines away. That is the
# standing shape — a gate convicting a compliant declaration — and it was
# invisible because the roster-scoped G7 target never reached OptionsRisk; the
# whole-tree `--scan-dir` arm is what surfaced it. The change can only move a
# verdict toward LESS conviction, so it never manufactures a finding.
# A trailing dot cannot be captured: each `.` must be followed by ≥1 name char.
#
# The modifier run is CAPTURED rather than discarded, because `private` has to be
# filtered out (proving note 115, 2026-08-06). A private declaration is not
# addressable by its fully-qualified name from an importing module — Lean mangles
# it to `_private.<module>.<hash>.<name>` — so `#print axioms <ns>.<name>` reports
# `Unknown constant` and the run exits 3: exactly the ghost-target signature
# `strip_comments` documents below, reached from a different cause. proving's tree
# holds 5 such declarations in 2 files, and those 5 WERE the whole of the
# whole-tree sweep's failure — 8,695 closures parsed cleanly, 5 unknowns aborted
# the lot. So the `--scan-dir` arm could never pass on a tree containing one,
# which is why it had never been wired as a default anywhere but studying, whose
# 174-theorem tree happens to have none.
#
# Skipping them costs no soundness, and that is the load-bearing half of the
# argument rather than a convenience: a private lemma is reachable only from its
# own module, so any axiom it depends on — `sorryAx` included — appears in the
# closure of whatever PUBLIC theorem uses it, and `#print axioms` walks that
# closure transitively. A private lemma used by nothing is dead code contributing
# no axiom to anything. The set of attested AXIOMS is therefore unchanged; only
# the set of unaddressable NAMES shrinks. Like the dotted-name fix above, this can
# only move a verdict away from a false abort, never manufacture a finding.
_DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*"
    r"((?:private\s+|protected\s+|noncomputable\s+|scoped\s+|local\s+)*)"
    r"(theorem|lemma|axiom)\s+([A-Za-z0-9_']+(?:\.[A-Za-z0-9_']+)*)"
)
_PRIVATE = re.compile(r"\bprivate\b")


# Comment syntax. `/- … -/` nests in Lean, so a regex cannot strip it correctly;
# the scanner below tracks depth. `--` runs to end of line.
_BLOCK_OPEN, _BLOCK_CLOSE, _LINE_COMMENT = "/-", "-/", "--"


def strip_comments(src: str) -> str:
    """Blank out every Lean comment, preserving line structure (so line-oriented
    scanning downstream keeps its indices).

    WHY THIS IS NOT COSMETIC (studying, ctx_degrade r06 follow-up 2026-08-05).
    `_scan_decls` matches `theorem`/`lemma`/`axiom`/`namespace` on any line, and
    every one of those words is ordinary English that appears constantly in this
    corpus's doc comments ("the theorem depends on …", "this lemma is over …").
    Unstripped, the scanner minted GHOST targets out of prose — measured across
    the three axes: 7 ghosts on studying, 1 on accounting, 48 on proving.

    The ghosts are not merely noise, and that is the part worth keeping:

    · A ghost target resolves to `Unknown constant` at elaboration, which makes
      the whole attestation exit 3 (BUILD/RESOLUTION error) rather than exit 2
      (attestation failure). A caller that distinguishes them — all three axis
      drivers do — reads a corpus-wide soundness gate as a broken toolchain.
    · Worse, a `namespace` INSIDE a comment pushes a frame the matching `end`
      never pops, so every REAL declaration after it is named under a corrupted
      prefix. On proving that mis-named 27 live theorems
      (`Demo.Lib.T05.Rulemaking..Demo.Lib.Common.…` — note the double dot),
      i.e. the attestation was not attesting them; it was attesting nothing
      under a name nothing has. Stripping recovers all 27 and loses no real
      target on any axis (verified before the change, all three trees).

    Nesting is tracked rather than regex-matched because `/- … /- … -/ … -/` is
    legal Lean and a non-greedy regex closes at the FIRST `-/`, resuming the
    scan inside prose — which is the same defect one layer down.
    """
    out: list[str] = []
    depth = 0
    for line in src.splitlines():
        buf: list[str] = []
        i = 0
        while i < len(line):
            two = line[i:i + 2]
            if depth == 0 and two == _LINE_COMMENT:
                break                            # rest of the line is comment
            if two == _BLOCK_OPEN:
                depth += 1
                i += 2
                continue
            if two == _BLOCK_CLOSE and depth > 0:
                depth -= 1
                i += 2
                continue
            if depth == 0:
                buf.append(line[i])
            i += 1
        out.append("".join(buf))
    return "\n".join(out)


def _scan_decls(
    src: str, keywords: tuple[str, ...], *, skip_private: bool = False
) -> list[str]:
    """Return the fully-qualified names of every `<kw> NAME` declaration whose
    keyword is in `keywords`, tracking `namespace`/`section`/`end` nesting so the
    FQN is namespace-correct. Sections contribute an `end` scope but no name.

    Comments are stripped first — see `strip_comments` for why that is a
    correctness requirement and not a tidiness one.

    `skip_private` is set by the TARGET side only, and the asymmetry is
    deliberate. An attest target must be addressable by FQN, which a private
    declaration is not (see `_DECL`). A DECLARED AXIOM need not be: the allow-set
    is matched by full name OR by leaf, and Lean's mangled `_private.<mod>.<n>.f`
    has leaf `f` — the same leaf the source scan yields — so a private axiom is
    already covered there. Skipping it on that side would newly convict a theorem
    for depending on an axiom the tree declares, which is the exact defect the
    dotted-name fix cured. Filtering both sides symmetrically would have looked
    tidier and been wrong in the one direction that manufactures findings."""
    src = strip_comments(src)
    stack: list[str] = []            # only namespace segments (name-bearing)
    scopes: list[bool] = []          # True = namespace frame (pop from stack)
    out: list[str] = []
    for line in src.splitlines():
        m = _NS_OPEN.match(line)
        if m:
            stack.append(m.group(1))
            scopes.append(True)
            continue
        if _SEC_OPEN.match(line):
            scopes.append(False)     # a section: consumes an `end`, no name
            continue
        if _END.match(line):
            if scopes:
                was_ns = scopes.pop()
                if was_ns and stack:
                    stack.pop()
            continue
        d = _DECL.match(line)
        if d and d.group(2) in keywords:
            if skip_private and _PRIVATE.search(d.group(1)):
                continue         # unaddressable by FQN — see `_DECL` above
            prefix = ".".join(stack)
            out.append(f"{prefix}.{d.group(3)}" if prefix else d.group(3))
    return out


def discover_theorems(src: str) -> list[str]:
    """FQNs of every `theorem`/`lemma` in a Lean source (namespace-aware)."""
    return _scan_decls(src, ("theorem", "lemma"), skip_private=True)


def discover_declared_axioms(root: pathlib.Path) -> set[str]:
    """FQNs of every `axiom NAME` declared anywhere under `root`'s `.lean` tree —
    the "declared, therefore not secret" set the attestation allows."""
    declared: set[str] = set()
    for path in root.rglob("*.lean"):
        try:
            declared.update(_scan_decls(path.read_text(), ("axiom",)))
        except (OSError, UnicodeDecodeError):
            continue
    return declared


# ---------------------------------------------------------------------------
# `#print axioms` output parsing + closure classification.

# `'Thm' depends on axioms: [a, b.c, sorryAx]`  /  `'Thm' does not depend on any axioms`
_DEPENDS = re.compile(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]")
_NO_DEPENDS = re.compile(r"'([^']+)' does not depend on any axioms")


def parse_axiom_closure(output: str) -> dict[str, set[str]]:
    """Parse `#print axioms` stdout into {theorem_name: {axiom, …}}. A theorem
    that "does not depend on any axioms" maps to an empty set. Toolchain-free —
    this is the unit the pure-python test exercises against synthetic output."""
    closure: dict[str, set[str]] = {}
    for m in _NO_DEPENDS.finditer(output):
        closure.setdefault(m.group(1), set())
    for m in _DEPENDS.finditer(output):
        axioms = {tok.strip() for tok in m.group(2).split(",") if tok.strip()}
        closure[m.group(1)] = axioms
    return closure


def _leaf(name: str) -> str:
    return name.rsplit(".", 1)[-1]


def unexpected_axioms(
    closure: dict[str, set[str]], allowed: set[str]
) -> dict[str, list[str]]:
    """Return {theorem: [unexpected axiom, …]} for every theorem whose closure
    escapes the allowed set. A `FORBIDDEN_LEAVES` axiom (sorryAx, ofReduce*,
    trustCompiler) or a `FORBIDDEN_SHAPE` match (the per-declaration
    native_decide axioms, which no roster can enumerate) is unexpected regardless
    of the allow-list. Matching is otherwise by full name OR leaf (last dotted
    segment), so a declared axiom passes whether `#print axioms` prints it
    fully-qualified or not."""
    allowed_leaves = {_leaf(a) for a in allowed}
    bad: dict[str, list[str]] = {}
    for thm, axioms in closure.items():
        offenders = []
        for a in sorted(axioms):
            if _leaf(a) in FORBIDDEN_LEAVES or FORBIDDEN_SHAPE.search(a):
                offenders.append(a)
            elif a not in allowed and _leaf(a) not in allowed_leaves:
                offenders.append(a)
        if offenders:
            bad[thm] = offenders
    return bad


# ---------------------------------------------------------------------------
# Lake invocation (reuses score_bridge.py's temp-file shape).

def print_axioms(
    modules: list[str], theorems: list[str], root: pathlib.Path
) -> tuple[str, int]:
    """Elaborate `import <module>…` + a `#print axioms` per theorem; return
    (stdout+stderr, returncode). The modules must already `lake build`."""
    body = [f"import {m}" for m in modules] + [""]
    body += [f"#print axioms {t}" for t in theorems]
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=root, delete=False
    ) as fh:
        fh.write("\n".join(body) + "\n")
        tmp = pathlib.Path(fh.name)
    try:
        proc = subprocess.run(
            ["lake", "env", "lean", str(tmp.relative_to(root))],
            cwd=root, capture_output=True, text=True,
        )
    finally:
        tmp.unlink(missing_ok=True)
    return proc.stdout + proc.stderr, proc.returncode


# ---------------------------------------------------------------------------

def _resolve_targets(
    args, root: pathlib.Path
) -> tuple[list[str], list[str]]:
    """Build (modules_to_import, theorems_to_attest) from the CLI. Raises
    ValueError (→ exit 3) on a usage / discovery problem."""
    modules: list[str] = list(args.modules or [])
    theorems: list[str] = list(args.theorems or [])

    if args.scan_dir is not None:
        d = args.scan_dir
        if not d.is_dir():
            raise ValueError(f"--scan-dir not a directory: {d}")
        # RESOLVE BOTH SIDES BEFORE COMPARING (studying 2026-08-05). `root` and
        # `--scan-dir` arrive as the user typed them, so `--root . --scan-dir
        # Operating` gave `Path('Operating/…').relative_to(Path('.'))` → ValueError
        # on EVERY file. The old `continue` swallowed each one, and the sweep
        # reported "no attest targets" over a tree of 174 live theorems. A skip
        # that silently shrinks the attested set is the exact failure mode a
        # soundness gate cannot have, so a genuinely out-of-root file is now a
        # LOUD error instead of a skip.
        d, rroot = d.resolve(), root.resolve()
        for path in sorted(d.rglob("*.lean")):
            try:
                rel = path.resolve().relative_to(rroot).with_suffix("")
            except ValueError:
                raise ValueError(
                    f"--scan-dir file outside --root: {path} is not under {rroot}. "
                    "A module path cannot be derived, so this file could only be "
                    "SKIPPED — and a silently smaller attested set is worse than "
                    "a refusal. Pass a --root that contains --scan-dir."
                ) from None
            mod = ".".join(rel.parts)
            found = discover_theorems(path.read_text())
            if found:
                modules.append(mod)
                theorems.extend(found)

    # Explicit theorems win; otherwise discover from each --module's source.
    if modules and not theorems and args.scan_dir is None:
        for mod in modules:
            src = root / (mod.replace(".", "/") + ".lean")
            if not src.exists():
                raise ValueError(f"cannot locate module source: {src}")
            theorems.extend(discover_theorems(src.read_text()))

    # de-dupe, preserve order
    modules = list(dict.fromkeys(modules))
    theorems = list(dict.fromkeys(theorems))
    if not modules or not theorems:
        raise ValueError(
            "no attest targets — pass --module (+/- --theorem) or --scan-dir"
        )
    return modules, theorems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--root", default=".", type=pathlib.Path,
                    help="Lean package root the module path resolves under (cwd)")
    ap.add_argument("--module", action="append", dest="modules",
                    help="module to import (repeatable); discover its theorems "
                         "when no --theorem is given")
    ap.add_argument("--theorem", action="append", dest="theorems",
                    help="fully-qualified theorem name to attest (repeatable)")
    ap.add_argument("--scan-dir", type=pathlib.Path, default=None,
                    help="discover every *.lean under this dir + its theorems")
    ap.add_argument("--allow-axioms", action="append", default=[],
                    help="comma-separated EXTRA allowed axiom names (repeatable)")
    ap.add_argument("--allow-declared", action="store_true",
                    help="allow every `axiom` declared under --root's tree")
    args = ap.parse_args(argv)
    root = args.root.resolve()

    try:
        modules, theorems = _resolve_targets(args, root)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3

    allowed: set[str] = set(STANDARD_AXIOMS)
    for chunk in args.allow_axioms:
        allowed.update(tok.strip() for tok in chunk.split(",") if tok.strip())
    if args.allow_declared:
        allowed.update(discover_declared_axioms(root))

    out, rc = print_axioms(modules, theorems, root)
    low = out.lower()
    if rc != 0 or "error:" in low or "unknown" in low:
        print(f"error: elaboration/resolution failed (rc {rc}) for "
              f"modules {modules}\n{out}", file=sys.stderr)
        return 3

    closure = parse_axiom_closure(out)
    if not closure:
        print(f"error: no `#print axioms` closure parsed from output:\n{out}",
              file=sys.stderr)
        return 3

    bad = unexpected_axioms(closure, allowed)
    print(f"G7 axiom-closure attestation — {len(closure)} theorem(s), "
          f"{len(allowed)} allowed axiom(s)")
    for thm in theorems:
        if thm not in closure:
            continue
        label = ".".join(thm.split(".")[-2:])
        if thm in bad:
            print(f"  {label:52s} UNEXPECTED {bad[thm]}")
        else:
            print(f"  {label:52s} CLEAN (closure ⊆ allowed)")

    if bad:
        n = sum(len(v) for v in bad.values())
        print(f"FAIL: {len(bad)}/{len(closure)} theorem(s) carry {n} "
              f"unexpected/undeclared axiom(s) or sorryAx (G7)", file=sys.stderr)
        return 2
    print(f"PASS: all {len(closure)} theorem(s) attest clean — no undeclared "
          f"axiom, no sorryAx (G7)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
