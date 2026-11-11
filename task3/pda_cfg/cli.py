"""Command-line demonstrations for Task 3."""
import argparse
from .models import balanced_brackets, validate_expression, is_palindrome, palindrome_derivation

CASES = {
    "brackets": (["()", "[]{}", "([]{})", "{[()()]}", "(((())))"], ["(", ")( ", "([)]", "(()", "{]}"]),
    "expression": (["id", "id+id*id", "(id+id)*id", "id*(id+id)", "((id))"], ["", "id+", "+id", "id id", "(id+id", "id+*id"]),
    "palindrome": (["", "a", "aba", "abba", "babab", "aabaa"], ["ab", "aab", "abab", "abbab", "ba"]),
}

def run(name):
    accepted, rejected = CASES[name]
    check = {"brackets": balanced_brackets, "expression": lambda s: validate_expression(s).accepted, "palindrome": is_palindrome}[name]
    print(f"\n{name.upper()}")
    for label, samples, expected in (("accepted", accepted, True), ("rejected", rejected, False)):
        print(f"{label.title()} examples:")
        for sample in samples:
            actual = check(sample)
            print(f"  {sample!r:16} -> {'ACCEPT' if actual else 'REJECT'}" + ("" if actual == expected else "  [UNEXPECTED]"))
    if name == "expression":
        print("\nTrace for id+id*id:")
        for line in validate_expression("id+id*id").trace:
            print(" ", line)
    if name == "palindrome":
        print("\nCFG derivation for 'abba':")
        for line in palindrome_derivation("abba"):
            print(" ", line)

def main():
    parser = argparse.ArgumentParser(description="Task 3 CFG/PDA case-study demonstrations")
    parser.add_argument("case", choices=["all", *CASES])
    args = parser.parse_args()
    for name in CASES if args.case == "all" else [args.case]:
        run(name)

if __name__ == "__main__":
    main()
