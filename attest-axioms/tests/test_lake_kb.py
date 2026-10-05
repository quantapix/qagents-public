#!/usr/bin/env python3
"""Lake-gated behavioral known-bad for attest_axioms.py.

Every other test in this directory feeds the parser SYNTHETIC `#print axioms`
output. This one runs the real thing: it writes a minimal Lake package into a
temp dir, builds it, and attests it.

  known-bad   a theorem closed with `sorry`      → exit 2
  control     a theorem proved in the same file  → exit 0

Without `lake` on PATH the test is SKIPPED — counted and printed by unittest,
never reported `ok`. With `lake` on PATH a build failure is a test failure.

Run: python3 -B -m unittest discover -s tests
"""

import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR.parent))

import attest_axioms as A  # noqa: E402

LAKEFILE = 'name = "kb"\n\n[[lean_lib]]\nname = "Kb"\n'
SOURCE = (
    "namespace Kb\n"
    "theorem unfinished : (1 : Nat) = 1 := by sorry\n"
    "theorem finished : (1 : Nat) = 1 := rfl\n"
    "end Kb\n"
)


def _attest(root: Path, theorem: str) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = A.main(["--root", str(root), "--module", "Kb", "--theorem", theorem])
    return rc, buf.getvalue()


class TestLakeKnownBad(unittest.TestCase):
    @unittest.skipUnless(shutil.which("lake"), "lake not on PATH — Lean behaviour NOT exercised")
    def test_sorry_theorem_exits_2_and_proved_theorem_exits_0(self):
        with tempfile.TemporaryDirectory(prefix="attest-kb-") as td:
            root = Path(td)
            (root / "lakefile.toml").write_text(LAKEFILE)
            (root / "Kb.lean").write_text(SOURCE)
            b = subprocess.run(["lake", "build", "Kb"], cwd=root, capture_output=True, text=True)
            self.assertEqual(b.returncode, 0, b.stdout + b.stderr)
            rc_bad, out_bad = _attest(root, "Kb.unfinished")
            rc_ok, out_ok = _attest(root, "Kb.finished")
        self.assertEqual(rc_bad, 2, out_bad)
        self.assertIn("sorryAx", out_bad)
        self.assertEqual(rc_ok, 0, out_ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
