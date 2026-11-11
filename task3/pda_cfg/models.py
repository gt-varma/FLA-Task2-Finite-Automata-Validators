"""Executable validators accompanying the Task 3 CFG/PDA report."""

from dataclasses import dataclass

OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}


def balanced_brackets(text: str) -> bool:
    """Recognise non-empty properly nested (), [] and {} strings by a stack."""
    if not text:
        return False
    stack = []
    for char in text:
        if char in OPEN_TO_CLOSE:
            stack.append(char)
        elif char in OPEN_TO_CLOSE.values():
            if not stack or OPEN_TO_CLOSE[stack.pop()] != char:
                return False
        else:
            return False
    return not stack


@dataclass(frozen=True)
class ParseResult:
    accepted: bool
    trace: tuple[str, ...]
    message: str


class ExpressionParser:
    """Predictive parser for id (+ id) and * with parentheses and precedence."""
    def __init__(self, tokens):
        self.tokens = list(tokens) + ["$"]
        self.pos = 0
        self.trace = []

    def look(self):
        return self.tokens[self.pos]

    def consume(self, token):
        if self.look() != token:
            raise ValueError(f"expected {token!r}, found {self.look()!r}")
        self.trace.append(f"match {token}")
        self.pos += 1

    def factor(self):
        if self.look() == "id":
            self.consume("id")
        elif self.look() == "(":
            self.consume("(")
            self.expr()
            self.consume(")")
        else:
            raise ValueError(f"expected id or '(', found {self.look()!r}")

    def term(self):
        self.factor()
        while self.look() == "*":
            self.consume("*")
            self.factor()

    def expr(self):
        self.term()
        while self.look() == "+":
            self.consume("+")
            self.term()

    def parse(self):
        try:
            self.expr()
            if self.look() != "$":
                raise ValueError(f"unexpected token {self.look()!r}")
            self.trace.append("accept")
            return ParseResult(True, tuple(self.trace), "well-formed expression")
        except (ValueError, IndexError) as exc:
            self.trace.append(f"reject: {exc}")
            return ParseResult(False, tuple(self.trace), str(exc))


def tokenize_expression(source: str):
    """Tokenise identifiers and the grammar punctuation; reject unknown text."""
    tokens = []
    i = 0
    while i < len(source):
        if source[i].isspace():
            i += 1
        elif source.startswith("id", i) and (i + 2 == len(source) or not source[i + 2].isalnum()):
            tokens.append("id")
            i += 2
        elif source[i] in "+*()":
            tokens.append(source[i])
            i += 1
        else:
            raise ValueError(f"invalid character/token at position {i}: {source[i]!r}")
    return tokens


def validate_expression(source: str) -> ParseResult:
    try:
        return ExpressionParser(tokenize_expression(source)).parse()
    except ValueError as exc:
        return ParseResult(False, (f"reject: {exc}",), str(exc))


def is_palindrome(text: str) -> bool:
    """Recognise palindromes over {a,b}, including epsilon."""
    return all(ch in "ab" for ch in text) and text == text[::-1]


def palindrome_derivation(text: str):
    """Return a derivation using S -> aSa | bSb | a | b | epsilon, or None."""
    if not is_palindrome(text):
        return None
    current = text
    steps = ["S"]
    while len(current) >= 2:
        if current[0] == "a":
            steps.append(f"a S a  (S -> aSa)")
        else:
            steps.append(f"b S b  (S -> bSb)")
        current = current[1:-1]
    if current == "a":
        steps.append("a  (S -> a)")
    elif current == "b":
        steps.append("b  (S -> b)")
    else:
        steps.append("epsilon  (S -> epsilon)")
    return tuple(steps)
