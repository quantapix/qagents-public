#!/usr/bin/env python3
"""Toolchain-free unit tests for attest_axioms.py — the G7 axiom-closure gate.

The unit under test is the PARSER + CLASSIFIER (synthetic `#print axioms` output
→ allowed/unexpected) and the namespace-aware source scanners. No built Lean
kernel required — `lake` is exercised only by `test_lake_kb.py`.

Run: python3 -B -m unittest discover -s tests   (stdlib-only)
"""

import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
LEAN_TOOLS = TESTS_DIR.parent
sys.path.insert(0, str(LEAN_TOOLS))

import attest_axioms as A  # noqa: E402

# A realistic `#print axioms` transcript: one clean theorem (standard axioms +
# one declared correspondence axiom), one sorry theorem, one leaning on an
# undeclared axiom, and one that depends on nothing.
SYNTHETIC = """\
'Demo.Lib.T18.CalibBridge.A.cand_a_implies_golden_a' depends on axioms: [propext, Classical.choice, Quot.sound, Demo.Lib.T18.CalibBridge.A.corr_pattern]
'Pkg.Foo.unfinished' depends on axioms: [propext, sorryAx]
'Pkg.Foo.leaky' depends on axioms: [propext, Some.Undeclared.axiom]
'Pkg.Foo.trivial' does not depend on any axioms
"""


class TestParseClosure(unittest.TestCase):
    def test_parses_each_theorem_block(self):
        c = A.parse_axiom_closure(SYNTHETIC)
        self.assertEqual(set(c), {
            "Demo.Lib.T18.CalibBridge.A.cand_a_implies_golden_a",
            "Pkg.Foo.unfinished", "Pkg.Foo.leaky", "Pkg.Foo.trivial",
        })

    def test_no_dependency_is_empty_set(self):
        c = A.parse_axiom_closure(SYNTHETIC)
        self.assertEqual(c["Pkg.Foo.trivial"], set())

    def test_axiom_list_split(self):
        c = A.parse_axiom_closure(SYNTHETIC)
        self.assertIn("sorryAx", c["Pkg.Foo.unfinished"])
        self.assertEqual(
            c["Demo.Lib.T18.CalibBridge.A.cand_a_implies_golden_a"],
            {"propext", "Classical.choice", "Quot.sound",
             "Demo.Lib.T18.CalibBridge.A.corr_pattern"},
        )

    def test_empty_output(self):
        self.assertEqual(A.parse_axiom_closure(""), {})


class TestClassify(unittest.TestCase):
    def _closure(self):
        return A.parse_axiom_closure(SYNTHETIC)

    def test_standard_only_is_clean(self):
        allowed = set(A.STANDARD_AXIOMS)
        bad = A.unexpected_axioms({"t": {"propext", "Classical.choice"}}, allowed)
        self.assertEqual(bad, {})

    def test_sorry_is_always_unexpected(self):
        # even if a caller foolishly allow-lists it, sorryAx never passes
        allowed = set(A.STANDARD_AXIOMS) | {"sorryAx"}
        bad = A.unexpected_axioms({"t": {"sorryAx"}}, allowed)
        self.assertIn("t", bad)
        self.assertIn("sorryAx", bad["t"])

    def test_undeclared_axiom_flagged(self):
        allowed = set(A.STANDARD_AXIOMS)
        bad = A.unexpected_axioms(self._closure(), allowed)
        # the declared corr axiom is NOT in standard-only allowed → flagged too
        self.assertIn("Pkg.Foo.leaky", bad)
        self.assertIn("Pkg.Foo.unfinished", bad)
        self.assertIn(
            "Demo.Lib.T18.CalibBridge.A.cand_a_implies_golden_a", bad)
        self.assertNotIn("Pkg.Foo.trivial", bad)

    def test_declared_axiom_allowed_makes_clean(self):
        allowed = set(A.STANDARD_AXIOMS) | {
            "Demo.Lib.T18.CalibBridge.A.corr_pattern"}
        bad = A.unexpected_axioms(self._closure(), allowed)
        self.assertNotIn(
            "Demo.Lib.T18.CalibBridge.A.cand_a_implies_golden_a", bad)
        # sorry + undeclared still flagged
        self.assertIn("Pkg.Foo.unfinished", bad)
        self.assertIn("Pkg.Foo.leaky", bad)

    def test_leaf_match(self):
        # allow-list carries the leaf only; a fully-qualified closure axiom with
        # the same leaf is accepted (print may qualify differently)
        allowed = set(A.STANDARD_AXIOMS) | {"corr_pattern"}
        bad = A.unexpected_axioms(
            {"t": {"A.B.corr_pattern"}}, allowed)
        self.assertEqual(bad, {})


class TestSourceScanners(unittest.TestCase):
    SRC = (
        "namespace Demo.Lib.T18.CalibBridge\n"
        "axiom corr_pattern : True\n"
        "namespace A\n"
        "theorem cand_a_implies_golden_a : True := trivial\n"
        "lemma helper : True := trivial\n"
        "end A\n"
        "section Scoped\n"
        "theorem in_section : True := trivial\n"
        "end Scoped\n"
        "@[simp] theorem attributed_thm : True := trivial\n"
        "end Demo.Lib.T18.CalibBridge\n"
    )

    def test_discover_theorems_namespace_aware(self):
        got = A.discover_theorems(self.SRC)
        self.assertIn(
            "Demo.Lib.T18.CalibBridge.A.cand_a_implies_golden_a", got)
        self.assertIn("Demo.Lib.T18.CalibBridge.A.helper", got)
        # section adds no name but still closes with its own `end`
        self.assertIn("Demo.Lib.T18.CalibBridge.in_section", got)
        self.assertIn("Demo.Lib.T18.CalibBridge.attributed_thm", got)

    def test_declared_axiom_scan(self):
        # exercise the FQN axiom extraction (via the shared scanner)
        got = A._scan_decls(self.SRC, ("axiom",))
        self.assertEqual(got, ["Demo.Lib.T18.CalibBridge.corr_pattern"])

    def test_leaf_helper(self):
        self.assertEqual(A._leaf("A.B.c"), "c")
        self.assertEqual(A._leaf("propext"), "propext")


class TestCommentStripping(unittest.TestCase):
    """The scanner keys on `theorem`/`lemma`/`axiom`/`namespace`, all of which
    are ordinary English words that saturate this corpus's doc comments. Before
    stripping, prose minted GHOST targets (7 studying / 1 accounting / 48
    proving) — each resolving to `Unknown constant`, which downgrades a
    corpus-wide soundness gate to exit 3 "broken toolchain" — and a commented-out
    `namespace` pushed a frame no `end` popped, mis-naming 27 LIVE proving
    theorems under a corrupted double-dot prefix. Studying 2026-08-05."""

    def test_block_comment_prose_mints_nothing(self):
        src = (
            "/-- this theorem ghost_one depends on the lemma ghost_two,\n"
            "    and axiom ghost_three is named in prose only. -/\n"
            "theorem real_one : True := trivial\n"
        )
        self.assertEqual(A.discover_theorems(src), ["real_one"])

    def test_line_comment_prose_mints_nothing(self):
        src = "-- theorem ghost_one is a comment\ntheorem real_one : True := trivial\n"
        self.assertEqual(A.discover_theorems(src), ["real_one"])

    def test_commented_namespace_does_not_corrupt_fqns(self):
        """The severe form: an unpopped frame renames every LATER declaration,
        so the attestation silently targets names nothing has."""
        src = (
            "namespace Real\n"
            "/-- prose mentioning namespace Ghost here. -/\n"
            "theorem kept : True := trivial\n"
            "end Real\n"
        )
        self.assertEqual(A.discover_theorems(src), ["Real.kept"])

    def test_nested_block_comments(self):
        """`/- … /- … -/ … -/` is legal Lean; a non-greedy regex would close at
        the FIRST `-/` and resume scanning inside prose — the same defect one
        layer down, which is why depth is tracked rather than regex-matched."""
        src = (
            "/- outer /- inner theorem ghost_inner -/ still outer\n"
            "   theorem ghost_outer -/\n"
            "theorem real_one : True := trivial\n"
        )
        self.assertEqual(A.discover_theorems(src), ["real_one"])

    def test_real_declarations_are_never_dropped(self):
        """The dangerous direction. A gate that attests FEWER theorems fails
        silently, so stripping must be verified additive-free on the shapes the
        three axes actually use."""
        got = A.discover_theorems(TestSourceScanners.SRC)
        self.assertEqual(len(got), 4)
        self.assertIn("Demo.Lib.T18.CalibBridge.attributed_thm", got)

    def test_code_with_arrow_is_not_eaten(self):
        """`--` opens a comment but `-/` and `->` must not; a stripper that ate
        `→`-heavy statements would drop real targets."""
        src = "theorem arrow (h : 1 - 1 = 0) : True := trivial\n"
        self.assertEqual(A.discover_theorems(src), ["arrow"])


class TestNativeDecideShapeRule(unittest.TestCase):
    """accounting ns-65 (2026-08-06). `native_decide` mints a FRESH axiom per
    declaration, named after the theorem — so no literal roster reaches it, and
    the pre-fix code caught it only by accident, via the "not in the allowed set"
    arm. That accident is defeated by any broad `--allow-axioms`, which is exactly
    when a caller most needs the gate."""

    NATIVE = "Accounting.Trend.natTrue._native.native_decide.ax_1_1"

    def test_native_axiom_convicts_even_when_explicitly_allowed(self):
        """The whole point of FORBIDDEN_*: allow-listing must not buy it back."""
        allowed = set(A.STANDARD_AXIOMS) | {self.NATIVE}
        bad = A.unexpected_axioms({"t": {self.NATIVE}}, allowed)
        self.assertEqual(bad, {"t": [self.NATIVE]})

    def test_bare_native_decide_token_convicts(self):
        allowed = set(A.STANDARD_AXIOMS) | {"Lean.native_decide"}
        self.assertIn("t", A.unexpected_axioms({"t": {"Lean.native_decide"}}, allowed))

    def test_ofreducenat_is_not_the_omitted_sibling(self):
        """`Lean.ofReduceNat` is exactly what a hand-written alternation omits."""
        for ax in ("Lean.ofReduceBool", "Lean.ofReduceNat", "Lean.trustCompiler"):
            allowed = set(A.STANDARD_AXIOMS) | {ax}
            self.assertIn("t", A.unexpected_axioms({"t": {ax}}, allowed), ax)

    def test_shape_rule_does_not_overmatch_ordinary_names(self):
        """A gate that convicts compliant declarations is the standing failure
        shape; `_native` as a plain identifier segment is not the axiom form."""
        allowed = set(A.STANDARD_AXIOMS) | {"Accounting.Trend.native_bar"}
        bad = A.unexpected_axioms({"t": {"Accounting.Trend.native_bar"}}, allowed)
        self.assertEqual(bad, {})


class TestDottedDeclaredNames(unittest.TestCase):
    """accounting ns-62 (2026-08-06). Lean's projection idiom declares dotted
    names (`axiom ClassifiedLeg.strategy`). Truncating at the first dot made the
    declared set hold a PREFIX of the real name, so `--allow-declared` convicted
    theorems for depending on an axiom the same file declares — a gate convicting
    a compliant declaration. Found only by the whole-tree `--scan-dir` arm; the
    roster-scoped G7 target never reached the module."""

    SRC = (
        "namespace Accounting.OptionsRisk\n"
        "opaque ClassifiedLeg : Type\n"
        "axiom ClassifiedLeg.strategy : ClassifiedLeg -> Strategy\n"
        "theorem Hier.leg_strategy_allowed : True := trivial\n"
        "end Accounting.OptionsRisk\n"
    )

    def test_dotted_axiom_keeps_its_full_name(self):
        got = A._scan_decls(self.SRC, ("axiom",))
        self.assertEqual(got, ["Accounting.OptionsRisk.ClassifiedLeg.strategy"])

    def test_dotted_theorem_keeps_its_full_name(self):
        self.assertIn("Accounting.OptionsRisk.Hier.leg_strategy_allowed",
                      A.discover_theorems(self.SRC))

    def test_declared_dotted_axiom_is_not_unexpected(self):
        """The end-to-end shape: the closure names the axiom in full, and
        --allow-declared must recognise it. Pre-fix this returned a finding."""
        allowed = set(A.STANDARD_AXIOMS) | set(A._scan_decls(self.SRC, ("axiom",)))
        bad = A.unexpected_axioms(
            {"Accounting.OptionsRisk.Hier.leg_strategy_allowed":
                {"Accounting.OptionsRisk.ClassifiedLeg.strategy"}},
            allowed,
        )
        self.assertEqual(bad, {})

    def test_a_genuinely_undeclared_dotted_axiom_still_convicts(self):
        """The widening must not disarm the gate: a dotted axiom NOT declared in
        the tree is still unexpected. A gate that cannot fail is worse than none."""
        allowed = set(A.STANDARD_AXIOMS) | set(A._scan_decls(self.SRC, ("axiom",)))
        bad = A.unexpected_axioms(
            {"t": {"Accounting.OptionsRisk.ClassifiedLeg.premium"}}, allowed)
        self.assertEqual(bad, {"t": ["Accounting.OptionsRisk.ClassifiedLeg.premium"]})

    def test_trailing_dot_is_not_captured(self):
        """The name group must never end on a dot — that would mint a declared
        name nothing has, which is the ghost-target class one layer down."""
        self.assertEqual(A._scan_decls("axiom foo. : True\n", ("axiom",)), ["foo"])


class TestPrivateDeclarations(unittest.TestCase):
    """proving note 115 (2026-08-06). A `private theorem` is not
    addressable by its FQN from an importing module — Lean mangles it to
    `_private.<mod>.<hash>.<name>` — so emitting it as an attest TARGET yields
    `Unknown constant` and exits 3 (build/resolution error), not 2 (attestation
    failure). Every caller distinguishes those, so a corpus-wide soundness gate
    read as a broken toolchain. proving's tree holds exactly 5 such declarations
    in 2 files, and those 5 were the entire failure of its first whole-tree
    sweep: 8,695 closures parsed clean, 5 unknowns aborted all of them."""

    SRC = (
        "namespace Demo.Lib.T18.SpecBridge\n"
        "private theorem elements_implies_golden_violation : True := trivial\n"
        "theorem public_one : True := trivial\n"
        "end Demo.Lib.T18.SpecBridge\n"
    )

    def test_private_theorem_is_not_an_attest_target(self):
        self.assertEqual(A.discover_theorems(self.SRC),
                         ["Demo.Lib.T18.SpecBridge.public_one"])

    def test_public_siblings_are_never_dropped(self):
        """The known-bad the filter must NOT swallow. A skip that silently
        shrinks the attested set is the failure mode a soundness gate cannot
        have — the same rule `--scan-dir` learned when a path mismatch was
        `continue`ing over a whole tree."""
        self.assertIn("Demo.Lib.T18.SpecBridge.public_one",
                      A.discover_theorems(self.SRC))

    def test_private_modifier_among_others_still_filtered(self):
        """Lean permits the modifiers in any order; matching must not depend on
        `private` coming first."""
        src = ("namespace N\n"
               "private noncomputable theorem a : True := trivial\n"
               "noncomputable private theorem b : True := trivial\n"
               "protected theorem c : True := trivial\n"
               "end N\n")
        self.assertEqual(A.discover_theorems(src), ["N.c"])

    def test_a_name_merely_containing_private_is_not_filtered(self):
        r"""`\bprivate\b` must not overmatch: `privateEnforcement` is an ordinary
        public theorem name in this corpus's civil-rights modules."""
        src = "theorem privateEnforcement : True := trivial\n"
        self.assertEqual(A.discover_theorems(src), ["privateEnforcement"])

    def test_private_AXIOM_stays_in_the_declared_set(self):
        """The asymmetry, pinned. The allow-set matches by full name OR leaf, and
        a mangled `_private.M.0.h` has leaf `h`, so a private axiom is already
        covered there. Filtering it symmetrically would newly convict a theorem
        for depending on an axiom the tree DECLARES — the exact defect the
        dotted-name fix cured, reintroduced in the name of tidiness."""
        src = ("namespace N\n"
               "private axiom h : True\n"
               "end N\n")
        self.assertEqual(A._scan_decls(src, ("axiom",)), ["N.h"])
        allowed = set(A.STANDARD_AXIOMS) | set(A._scan_decls(src, ("axiom",)))
        self.assertEqual(A.unexpected_axioms({"t": {"_private.M.0.h"}}, allowed), {})


if __name__ == "__main__":
    unittest.main()
