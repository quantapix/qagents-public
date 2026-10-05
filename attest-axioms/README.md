# attest-axioms — an axiom-closure gate for Lean 4 packages

A Lean 4 theorem can type-check while resting on something you did not intend:
a `sorry`, a `native_decide`, or an `axiom` nobody declared on purpose. Lean
will tell you, one theorem at a time, if you ask with `#print axioms`. This
tool asks for every theorem in a module or a directory, compares each answer
with an allowed set, and exits non-zero when any theorem escapes it.

It is one Python file with no dependencies beyond the standard library. It
needs `lake` on PATH and a package that already builds.

## Use

```
python3 attest_axioms.py --root path/to/package --scan-dir path/to/package/Pkg --allow-declared
python3 attest_axioms.py --root path/to/package --module Pkg.Some.Module
python3 attest_axioms.py --root path/to/package --module Pkg.Some.Module \
    --theorem Pkg.Some.Module.some_theorem --allow-axioms Pkg.my_axiom
```

The allowed set is the three standard axioms (`Classical.choice`, `propext`,
`Quot.sound`), plus any names passed with `--allow-axioms`, plus, with
`--allow-declared`, every `axiom` declared in a `.lean` file under `--root`.

| Exit | Meaning |
|---|---|
| 0 | Every attested theorem's closure is inside the allowed set. |
| 2 | Finding: some closure holds `sorryAx`, a `native_decide` axiom, or an axiom outside the allowed set. |
| 3 | Could not look: the module did not elaborate, a name did not resolve, or no target was found. |

Keep 2 and 3 apart at the call site. Exit 3 says nothing about soundness
either way.

`sorryAx`, `ofReduceBool`, `ofReduceNat`, `trustCompiler` and anything shaped
like a `native_decide` axiom are refused even if you allow-list them.

## What a clean exit does not mean

- **It attests the closure, not the statement.** A theorem that proves the
  wrong thing from declared axioms passes.
- **`--allow-declared` trusts every declared axiom.** An inconsistent or
  over-strong `axiom` in your tree is allowed by construction. The flag only
  separates axioms someone wrote down from ones nobody did.
- **Allow-list matching is by full name or by last name segment.** An axiom
  `A.foo` in a closure passes if `B.foo` is allowed. Pass narrow allow-lists.
- **Targets are found by a line-oriented source scan, not by Lean.** It
  tracks `namespace` / `section` / `end` and strips comments, and it sees
  `theorem`, `lemma` and `axiom` lines. A theorem produced by a macro, a
  `def` of proposition type, or an `instance` is not a target. With
  `--theorem` you name targets yourself.
- **`private` theorems are skipped as targets.** They cannot be named from
  another module. Their axioms still surface in the closure of any public
  theorem that uses them; a private theorem used by nothing is not attested.
- **Any elaboration output containing `error:` or `unknown` is treated as
  could-not-look (exit 3),** including when that text comes from a name.

## Tests

```
python3 -B -m unittest discover -s tests
```

`tests/test_attest_axioms.py` exercises the parser, the classifier and the
source scanner on synthetic input and needs no Lean. `tests/test_lake_kb.py`
is the one test that runs Lean: it builds a two-theorem package in a temp
directory and checks that the `sorry` theorem exits 2 and the proved one
exits 0. Without `lake` on PATH that test is reported as skipped, and the
Lean behaviour is then not exercised by this copy.

## Provenance

This is a staged copy of a file maintained in a private repository, where it
gates three Lean 4 packages. The comments keep their dated notes about the
defects that shaped each rule; module names in examples and tests were
replaced with neutral ones. The licence is the one at the root of this
repository.
