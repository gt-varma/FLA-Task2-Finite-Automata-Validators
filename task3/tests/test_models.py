import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from task3.pda_cfg.models import balanced_brackets, validate_expression, is_palindrome, palindrome_derivation


def test_balanced_brackets_examples():
    for value in ["()", "[]{}", "([]{})", "{[()()]}", "(((())))"]:
        assert balanced_brackets(value), value
    for value in ["", "(", ")( ", "([)]", "(()", "{]}"]:
        assert not balanced_brackets(value), value


def test_expression_examples():
    for value in ["id", "id+id*id", "(id+id)*id", "id*(id+id)", "((id))"]:
        assert validate_expression(value).accepted, value
    for value in ["", "id+", "+id", "id id", "(id+id", "id+*id", "id&"]:
        assert not validate_expression(value).accepted, value


def test_expression_precedence_parser_accepts_chain():
    result = validate_expression("id+id*id+id")
    assert result.accepted
    assert result.trace[-1] == "accept"


def test_palindrome_examples():
    for value in ["", "a", "aba", "abba", "babab", "aabaa"]:
        assert is_palindrome(value), value
    for value in ["ab", "aab", "abab", "abbab", "ba", "abc"]:
        assert not is_palindrome(value), value


def test_palindrome_derivation():
    derivation = palindrome_derivation("abba")
    assert derivation is not None
    assert "S -> bSb" in derivation[1]
    assert palindrome_derivation("ab") is None
