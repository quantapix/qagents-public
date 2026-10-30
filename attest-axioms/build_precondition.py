"""build_precondition — the BUILD precondition `attest_axioms.py` runs
before it elaborates anything.

`lake env lean` on a temp file that imports a module reads that module's
PREVIOUSLY BUILT `.olean`. When the current source does not compile, the import
still resolves the old olean, so a `#print axioms` probe grades the PREVIOUS
state and its void result reads exactly like a clean one. A caller's own
step order does not prevent it, so `attest_axioms.py` calls `require_built()`
immediately before it elaborates: `lake build +<module>…` must exit 0 — a
no-op on an up-to-date tree — or it refuses with its could-not-look exit 3,
never a verdict.
"""
from __future__ import annotations

import pathlib
import subprocess


def lake_build_argv(modules: list[str]) -> list[str]:
    """`lake build` with each module as an explicit `+<module>` target."""
    return ["lake", "build", *[f"+{m}" for m in modules]]


def require_built(modules: list[str], root: pathlib.Path,
                  run=subprocess.run) -> str | None:
    """None when every module builds at `root`; else the refusal message.
    `run` is the subprocess seam the witnesses replace."""
    argv = lake_build_argv(modules)
    try:
        proc = run(argv, cwd=root, capture_output=True, text=True)
    except (OSError, subprocess.SubprocessError) as exc:
        return (f"BUILD PRECONDITION UNMET — `{' '.join(argv)}` could not run "
                f"({exc}). Nothing was elaborated: without a build, an import "
                f"resolves whatever olean was built last.")
    if proc.returncode != 0:
        # Lean-stdout channel: N/A. This tail is QUOTED into
        # the refusal message for a human; no record is graded off it — the
        # verdict is `lake build`'s exit code alone, which an import-time
        # print cannot forge. Nonce/escaping/summary do not apply.
        tail = "\n".join(((proc.stdout or "") + (proc.stderr or ""))
                         .strip().splitlines()[-15:])
        return (f"BUILD PRECONDITION UNMET — `{' '.join(argv)}` exited "
                f"{proc.returncode}. Elaborating now would import the "
                f"PREVIOUSLY built olean and grade the old state, and a void "
                f"result would read clean. Fix the build, then re-run.\n{tail}")
    return None
