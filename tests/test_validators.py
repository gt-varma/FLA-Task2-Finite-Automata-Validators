import itertools,re,string
from fa_validators.validators import *
def test_examples():
 for key,dfa in [("pin",PIN_DFA),("weak_pin",WEAK_PIN_DFA),("password",PASSWORD_DFA),("email",EMAIL_DFA)]:
  for s in TESTS[key]["accept"]:assert dfa.accepts(s),(key,s)
  for s in TESTS[key]["reject"]:assert not dfa.accepts(s),(key,s)
def test_counts():
 assert (PIN_DFA.live_states(),len(PIN_DFA.reachable()))==(5,6)
 assert (WEAK_PIN_DFA.live_states(),len(WEAK_PIN_DFA.reachable()))==(41,42)
 assert (STRONG_PIN_DFA.live_states(),len(STRONG_PIN_DFA.reachable()))==(34,35)
 assert SESSION_DFA.live_states()==5
 assert len(PASSWORD_PRODUCT.reachable())==240 and PASSWORD_DFA.live_states()==196
 assert EMAIL_SUBSET.live_states()==9 and EMAIL_DFA.live_states()==8
def test_pin_lengths():
 for n in range(7):assert PIN_DFA.accepts("7"*n)==(n==4)
def test_password_boundary():
 assert PASSWORD_DFA.accepts("Abcdef1!") and PASSWORD_DFA.accepts("A"*7+"a1!")
 assert not PASSWORD_DFA.accepts("Abcde1!") and not PASSWORD_DFA.accepts("A"*14+"a1!X")
def test_email_against_regex_exhaustive_short_strings():
 p=re.compile(r"^[A-Za-z0-9]+([._-][A-Za-z0-9]+)*@[A-Za-z0-9]+(-+[A-Za-z0-9]+)*(\.[A-Za-z0-9]+(-+[A-Za-z0-9]+)*)*\.[A-Za-z]{2,}$")
 for s in TESTS["email"]["accept"]:
  assert EMAIL_NFA.accepts(s)==bool(p.fullmatch(s)),s
 for s in TESTS["email"]["reject"]:
  assert EMAIL_NFA.accepts(s)==bool(p.fullmatch(s)),s
 for n in range(6):
  for t in itertools.product("a1.@-_",repeat=n):
   s="".join(t);assert EMAIL_NFA.accepts(s)==bool(p.fullmatch(s)),s
