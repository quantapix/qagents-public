"""stdout_channel — the Lean-stdout RECORD channel `attest_axioms.py` parses.

THE DEFECT. An imported module's `initialize` (or an `@[command_elab]`) runs at
IMPORT time in ANY process that elaborates a file importing it — `lake env lean
<tmp>.lean` included — and prints to the same stdout the reader parses. A
scratch module whose `initialize` printed one forged `'X' depends on axioms:
[…]` line made a reader report "1 theorem(s)" on a zero-theorem run; a forged
"does not depend on any axioms" line could OVERWRITE a theorem's real deps when
a NO_DEPENDS loop ran after the DEPENDS loop. Before this module the readers
were protected by ORDER (import-time prints precede the file's own commands,
and the later real line won the dict write) — which is a coincidence of
evaluation order, not a check.

THE FOUR CHANNELS a Lean-stdout reader is graded on, and this module's share:

  members vs oleans   not here — `build_precondition.require_built()` owns it
                      (a `#print axioms` probe reads the LAST-BUILT olean, so
                      each seat forces `lake build +<module>` first).
  records off stdout  HERE — the reader mints a per-run NONCE, writes it into
                      the Lean snippet it generates as a `QCHANNEL <nonce>
                      BEGIN <n>` / `END <n>` pair around its own commands, and
                      parses ONLY the window; a record outside it is convicted,
                      not skipped; a missing window is convicted (an
                      `initialize` that prints a clean record and calls
                      `IO.Process.exit 0` leaves rc 0, no error text and no
                      window); two windows convict (a forger that READ the temp
                      file can echo the nonce but cannot remove the reader's
                      own markers).
  field escaping      HERE — `PRINT_AXIOMS_RECORD_RE` takes the theorem name
                      non-greedily up to the fixed verb, so a primed name
                      (`'foo'' depends …`) is a record; the old `'([^']+)'`
                      yielded nothing for it and the seat skipped it silently.
  recomputed summary  HERE — `check_records`: exactly one record per requested
                      theorem (a duplicate convicts in EITHER order, which is
                      what retires the overwrite), no record for an unrequested
                      name, and the END count equals both the requested count
                      and the parsed count.

THREAT BOUNDARY. The window defeats import-time prints, which is the measured
attack. It does NOT defeat an imported module that overrides the elaborator of
`#eval` or `#print` itself — such a module controls every byte the reader sees,
nonce included, and no in-band check can reach it; that is a tree-review
problem, not a stdout reader's.
Likewise an EMPTY axiom closure is not a kernel check (`debug.skipKernelTC` +
`addDecl` lands `False` with no axiom): a reader of `#print axioms` output
cannot see it, and a replay that checks only target modules trusts their
imports. Recorded here so the next reader does not mistake a clean window for
a kernel attestation.

Stdlib-only; `attest_axioms.py` puts its own dir on `sys.path`, so a caller
that loads it by FILE PATH resolves this too.
"""
from __future__ import annotations

import re
import secrets
from dataclasses import dataclass

TAG = "QCHANNEL"

# One marker per line, nothing else on it. `lean` prints `#eval` info messages
# bare (no `file:line:col:` prefix) — the same shape `score_bridge`'s QFIELDS
# probe has parsed in production since CF-R8 — but the regex tolerates leading
# whitespace and never anchors on a prefix.
_MARK_RE = re.compile(
    rf"^[^\S\n]*{TAG} ([0-9a-f]{{16}}) (BEGIN|END) (\d+)[^\S\n]*(?:\n|$)", re.M)

# `'Thm' depends on axioms: [a, b.c, sorryAx]` / `'Thm' does not depend on any axioms`.
# Group 1 = name (non-greedy to the verb, so `'foo''` parses), group 2 = the
# axiom list or None.
PRINT_AXIOMS_RECORD_RE = re.compile(
    r"'(.+?)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")


class ForgedChannel(RuntimeError):
    """The stdout channel failed a check: a record this reader cannot attribute
    to its own commands. A FINDING about the tree (an import writes into the
    reader's channel), never a could-not-look — callers map it to their
    conviction exit, not their precondition exit."""


def mint_nonce() -> str:
    return secrets.token_hex(8)


def marker_commands(nonce: str, n: int) -> tuple[str, str]:
    """Top-level Lean commands bracketing `n` reader-authored commands."""
    return (f'#eval IO.println "{TAG} {nonce} BEGIN {n}"',
            f'#eval IO.println "{TAG} {nonce} END {n}"')


def marker_statements(nonce: str, n: int) -> tuple[str, str]:
    """The same pair as `do`-block statements (for a single meta `#eval`)."""
    return (f'IO.println "{TAG} {nonce} BEGIN {n}"',
            f'IO.println "{TAG} {nonce} END {n}"')


@dataclass(frozen=True)
class Window:
    before: str
    body: str
    after: str
    declared: int        # the <n> both markers carry


def extract_window(output: str, nonce: str | None = None, *,
                   required: bool = True) -> Window | None:
    """Locate the reader's own BEGIN/END pair.

    With `nonce`, the pair must carry it. Without one (a legacy caller reading
    a SAVED dump) the pair may carry any nonce, and `required=False` lets an
    output with NO markers at all parse whole — the pre-355 reading, kept only
    for saved dumps; a live seat always passes its nonce."""
    marks = list(_MARK_RE.finditer(output))
    if not marks:
        if nonce is None and not required:
            return None
        raise ForgedChannel(
            f"no {TAG} window in the output — the reader's own BEGIN/END "
            "markers never printed (an import-time print followed by "
            "`IO.Process.exit 0`, or the probe never reached its commands); "
            "nothing in this output is a record")
    if len(marks) != 2:
        raise ForgedChannel(
            f"{len(marks)} {TAG} marker(s), expected exactly one BEGIN and one "
            f"END — a second window is a forged one: "
            f"{[m.group(0).strip() for m in marks]}")
    b, e = marks
    if (b.group(2), e.group(2)) != ("BEGIN", "END"):
        raise ForgedChannel(
            f"{TAG} markers out of order: {b.group(2)} then {e.group(2)}")
    if b.group(1) != e.group(1):
        raise ForgedChannel(
            f"{TAG} BEGIN/END nonce disagree ({b.group(1)} vs {e.group(1)})")
    if nonce is not None and b.group(1) != nonce:
        raise ForgedChannel(
            f"{TAG} window nonce {b.group(1)} is not this run's nonce {nonce}")
    if b.group(3) != e.group(3):
        raise ForgedChannel(
            f"{TAG} BEGIN/END count disagree ({b.group(3)} vs {e.group(3)})")
    return Window(output[:b.start()], output[b.end():e.start()],
                  output[e.end():], int(b.group(3)))


def reject_outside(win: Window, record_re: re.Pattern, what: str) -> None:
    """A record printed outside the window is an import-time print."""
    outside = [m.group(1) for m in record_re.finditer(win.before)]
    outside += [m.group(1) for m in record_re.finditer(win.after)]
    if outside:
        raise ForgedChannel(
            f"{len(outside)} {what} record(s) outside the {TAG} window "
            f"{outside} — printed by an import, not by this reader's commands")


def check_records(names: list[str], expected: list[str] | None = None,
                  declared: int | None = None, *, what: str = "theorem",
                  allow_missing: bool = False) -> None:
    """Exactly one record per requested name; the END count recomputed."""
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        raise ForgedChannel(
            f"duplicate record(s) for {what} {dup} — exactly one record per "
            f"requested {what}; the second one is a forged one, whichever "
            "order they printed in")
    if expected is not None:
        extra = sorted(set(names) - set(expected))
        if extra:
            raise ForgedChannel(
                f"record(s) for unrequested {what}(s) {extra} — this reader "
                "asked for none of them")
        missing = [t for t in expected if t not in names]
        if missing and not allow_missing:
            raise ForgedChannel(
                f"missing record(s) for requested {what}(s) {missing} — a "
                "requested name with no record is never skipped")
        if declared is not None and declared != len(expected):
            raise ForgedChannel(
                f"END count {declared} ≠ requested count {len(expected)}")
    if declared is not None and not allow_missing and declared != len(names):
        raise ForgedChannel(
            f"END count {declared} ≠ {len(names)} parsed {what} record(s)")
