# Task 3 — CFG and PDA Case Studies

**Course:** 21CSC301T — Formal Language and Automata  
**Student:** G Tarun Varma  
**Register No.:** RA2411026050037

This Task 3 extension contains three case studies: balanced delimiters, arithmetic-expression syntax, and palindrome recognition. Each section defines a language, gives a CFG/PDA model, explains stack behaviour, and provides accepted/rejected examples. The material follows the assignment's required case-study-report format.

## Run

From the repository root:

```bash
python -m task3.pda_cfg.cli all
python -m task3.pda_cfg.cli brackets
python -m task3.pda_cfg.cli expression
python -m task3.pda_cfg.cli palindrome
python -m pytest task3/tests -q
```

Python 3.9+; no runtime dependencies. Install pytest to run tests.

## Contents
- `pda_cfg/models.py`: bracket-stack recognizer, expression predictive parser, palindrome recognizer.
- `pda_cfg/cli.py`: command-line demonstrations.
- `tests/test_models.py`: positive and negative validation tests.
- `REPORT.md`: formal language definitions, CFG productions, PDA descriptions, derivations, traces, ambiguity and limitations.

The palindrome CFG recognises all palindromes over {a,b}; the executable recognizer uses direct reversal comparison as a reference oracle. A PDA strategy is described formally in the report. Do not confuse the CFG's full palindrome language with the special even-palindrome NPDA variant.

**Prepared for:** G Tarun Varma (RA2411026050037).
