# Task 3 Case-Study Report — CFG and PDA Design

**Course:** 21CSC301T — Formal Language and Automata  
**Student:** G Tarun Varma  
**Register Number:** RA2411026050037  
**Assessment:** CLA-2, Task 3

## 1. Aim and method

The aim is to define context-free target languages and design CFG/PDA models, demonstrate derivations or stack processing, examine ambiguity and determinism, and validate accepted and rejected strings. The implementation is an executable companion to the formal models; the formal PDA descriptions below are the mathematical specification.

A finite automaton has only finite control and cannot retain an unbounded nesting history. A PDA adds a last-in-first-out stack, which is suitable for nested delimiters and the matching halves of palindromes. For arithmetic expressions, parentheses can nest without a fixed depth, and a stack-based parser checks that structure.

## 2. Case study 1 — Balanced bracket validation

### 2.1 Target language

Let Σ = { (, ), [, ], {, } }. L is the set of **non-empty** strings over Σ in which every closing bracket matches the most recent unmatched opening bracket and no opening bracket remains unmatched at the end.

Accepted: `()`, `[]{}`, `([]{})`, `{[()()]}`, `(((())))`.  
Rejected: `(`, `)(`, `([)]`, `(()`, `{]}`.

### 2.2 CFG and ambiguity

A compact grammar is:

```
S → SS | (S) | [S] | {S} | () | [] | {}
```

The `SS` alternative permits multiple parse-tree groupings for concatenated blocks. For example, a concatenation of three balanced blocks can be split into a first block plus the remaining two, or the first two plus the last. The grammar is therefore ambiguous with respect to concatenation structure.

An unambiguous revised grammar is:

```
S → B S | B
B → (S) | () | [S] | [] | {S} | {}
```

S is a non-empty sequence of blocks; B is exactly one bracketed block. The right-recursive sequence fixes the grouping of concatenation.

### 2.3 PDA definition

Use a deterministic stack machine M = (Q, Σ, Γ, δ, q0, Z0, F):
- Q = {q0, q1, qf}; q0 is the start state, qf is the accepting state.
- Σ = { (, ), [, ], {, } }.
- Γ = {Z0, (, [, {} where Z0 is the bottom marker.
- F = {qf}; acceptance is by final state after all input is consumed.

For each opening bracket o and any stack top X, δ(q0,o,Z0)=(q1,oZ0), and δ(q1,o,X)=(q1,oX). For each matching pair (o,c), δ(q1,c,o)=(q1,ε). When the input is exhausted and the stack top is Z0, δ(q1,ε,Z0)=(qf,Z0). No transition is defined for a mismatched closer, an unexpected symbol, or a non-empty stack at end of input. The transition notation writes the new stack string with its leftmost symbol on top.

### 2.4 Successful stack processing

For `{[()]}`, top of stack is shown at the left:

```
(q0, {[()]}, Z0)
⊢ (q1, [()]}, { Z0)
⊢ (q1, ()]}, [ { Z0)
⊢ (q1, )]}, ( [ { Z0)
⊢ (q1, ]}, [ { Z0)
⊢ (q1, }, { Z0)
⊢ (q1, ε, Z0)
⊢ (qf, ε, Z0)  ACCEPT
```

For `([)]`, after reading `([ ` the stack top is `[`. The next input is `)`, for which no matching-pop transition exists. The machine rejects.

### 2.5 Limits

The model validates delimiter nesting only. It does not check programming-language types, statement syntax, or whether delimiters occur inside comments or string literals. A practical source-code validator would first need lexical analysis.

## 3. Case study 2 — Arithmetic expression syntax

### 3.1 Target language

The token alphabet is Σ = {id, +, *, (, )}. The language contains expressions built from the identifier token `id`, binary addition and multiplication, and parentheses. Unary operators and implicit multiplication are excluded. Multiplication has higher precedence than addition; both operators are left-associative.

### 3.2 Ambiguous grammar and corrected grammar

Naïve grammar:

```
E → E + E | E * E | (E) | id
```

For `id + id * id`, two distinct structures are possible: `id + (id * id)` and `(id + id) * id`. The grammar does not encode precedence and is ambiguous.

Precedence grammar:

```
E → E + T | T
T → T * F | F
F → (E) | id
```

E handles addition, T handles multiplication, and F handles identifiers or parenthesised expressions. Thus multiplication binds more tightly.

For predictive parsing, remove left recursion:

```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

This grammar supports a deterministic LL(1) predictive parser.

### 3.3 PDA construction

The standard CFG-to-NPDA construction uses one state q and a stack initially containing the start variable E. For each production A → α, add an ε-transition that replaces A by α. For every terminal a, add a transition that reads a and pops the matching terminal a. The machine accepts when the input is consumed and the stack is empty. This generic construction is nondeterministic because it chooses among productions using ε-moves.

The executable parser uses the left-recursion-free grammar and one look-ahead token. Its parser procedures correspond to E, E', T, T', and F. This is a deterministic predictive parser rather than the generic NPDA above.

### 3.4 Leftmost derivation

For `id + id * id`:

```
E
⇒ E + T
⇒ T + T
⇒ F + T
⇒ id + T
⇒ id + T * F
⇒ id + F * F
⇒ id + id * F
⇒ id + id * id
```

The multiplication is contained within T, showing that it binds more tightly than addition.

### 3.5 Validation

Accepted: `id`, `id+id*id`, `(id+id)*id`, `id*(id+id)`, `((id))`.  
Rejected: empty input, `id+`, `+id`, `id id`, `(id+id`, `id+*id`.

### 3.6 Limits

This is a syntax model over abstract tokens, not a complete programming language. It does not evaluate values, detect division by zero, resolve variable names, or enforce types. A real compiler also performs lexical, semantic, and type analysis.

## 4. Case study 3 — Palindrome recognition

### 4.1 Target language

Let Σ = {a,b}. Lpal = {w ∈ Σ* : w = wᴿ}, where wᴿ is the reverse of w. The empty string ε is included. This includes both odd- and even-length palindromes.

Accepted: ε, `a`, `aba`, `abba`, `babab`, `aabaa`.  
Rejected: `ab`, `aab`, `abab`, `abbab`, `ba`.

### 4.2 CFG

```
S → aSa | bSb | a | b | ε
```

The recursive rules add the same symbol at both ends; the base cases generate the empty string or a one-symbol centre. The grammar is unambiguous: the outermost symbols determine which recursive production applies, and the centre is determined when zero or one symbols remain.

Example derivation for `abba`:

```
S ⇒ aSa
  ⇒ abSba
  ⇒ abεba
  ⇒ abba
```

Example for `aba`:

```
S ⇒ aSa ⇒ aba
```

### 4.3 PDA strategy and determinism

For an even palindrome `w wᴿ` with no centre marker, a PDA must guess where the first half ends. An NPDA can push symbols while reading the first half, nondeterministically take an ε-transition to a matching phase, then pop one matching symbol for each remaining input symbol. It accepts when input is exhausted and only the bottom marker remains. This midpoint guess is the source of nondeterminism.

If the input format contains a special centre marker `c`, the language `{w c wᴿ : w ∈ {a,b}*}` can be recognised deterministically: push symbols before c, switch phase when c is read, and compare/pop after c. The marker makes the midpoint explicit. This marked-centre language is a subset-format variant, not the same input language as all unmarked palindromes.

The CFG above describes all palindromes. The Python function in this project checks the defining reversal property as a reference validator; it is not presented as a literal PDA simulator. The NPDA/DPDA stack procedures above are the formal automata design.

### 4.4 Validation

Accepted: ε, `a`, `aba`, `abba`, `babab`, `aabaa`.  
Rejected: `ab`, `aab`, `abab`, `abbab`, `ba`.

### 4.5 Limits

The palindrome checker accepts only the alphabet {a,b}. It is a formal-language demonstration, not a secure password checker or a natural-language palindrome tool.

## 5. Comparison and conclusion

| Case study | Why finite-state memory is insufficient | Stack/grammar feature |
|---|---|---|
| Balanced brackets | Arbitrarily deep nesting and matching types | Deterministic push/pop |
| Arithmetic expressions | Arbitrarily nested parentheses | CFG with precedence; predictive parser |
| Palindromes | Matching an unbounded first half with its reverse | NPDA midpoint guess; DPDA when centre marker is explicit |

The three examples show different uses of context-free modelling: nested structure, precedence-aware syntax, and mirrored strings. Ambiguity is exposed and corrected for bracket concatenation and arithmetic precedence. Determinism depends on the input structure: the bracket PDA is deterministic, the revised expression grammar supports LL(1) parsing, and unmarked even-palindrome recognition uses nondeterministic midpoint selection.

## 6. Demonstration checklist

- Run the CLI for each case study and explain the accepted/rejected examples.
- Demonstrate the bracket stack on `{[()]}` and the mismatch in `([)]`.
- Explain why `id+id*id` parses with multiplication first.
- Show the derivation of `abba` and explain the guessed midpoint for an unmarked NPDA.
- State the limitations: delimiter-only validation, token-level arithmetic syntax, and the restricted palindrome alphabet.

**Student:** G Tarun Varma  
**Register No.:** RA2411026050037
