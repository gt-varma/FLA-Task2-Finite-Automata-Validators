import string
from .automata import DFA,NFA
# PIN format: exactly four digits; O is any non-digit.
def pin_class(c):return "D" if c in string.digits else "O"
PIN_DFA=DFA("ATM PIN format",["D","O"],{("q0","D"):"q1",("q1","D"):"q2",("q2","D"):"q3",("q3","D"):"q4"},"q0",{"q4"},pin_class)
# Separate weak-PIN recognizer for four identical digits.
def make_weak():
 ds=list(string.digits);d={}
 for x in ds:
  d[("s",x)]=x+"1"
  for i in (1,2,3):d[(x+str(i),x)]=x+str(i+1)
 return DFA("Weak PIN",ds,d,"s",{x+"4" for x in ds},lambda c:c)
WEAK_PIN_DFA=make_weak()
def make_any4():return DFA("Any four digits",list(string.digits),{("p"+str(i),x):"p"+str(i+1) for i in range(4) for x in string.digits},"p0",{"p4"},lambda c:c)
STRONG_PIN_DFA=make_any4().intersect(DFA("Not weak",WEAK_PIN_DFA.alphabet,WEAK_PIN_DFA.delta,WEAK_PIN_DFA.start,set(WEAK_PIN_DFA.states)-WEAK_PIN_DFA.accepting,lambda c:c,WEAK_PIN_DFA.states)).minimize("Strong PIN")
SESSION_DFA=DFA("ATM lockout",["C","W"],{("s0","C"):"AUTH",("s0","W"):"s1",("s1","C"):"AUTH",("s1","W"):"s2",("s2","C"):"AUTH",("s2","W"):"LOCK",("AUTH","C"):"AUTH",("AUTH","W"):"AUTH",("LOCK","C"):"LOCK",("LOCK","W"):"LOCK"},"s0",{"AUTH"},lambda c:c)
SPECIALS="!@#$%^&*()-_=+[]{};:,.?/"
PW_ALPHA=["U","L","D","S","O"]
def pw_class(c):return "U" if c in string.ascii_uppercase else "L" if c in string.ascii_lowercase else "D" if c in string.digits else "S" if c in SPECIALS else "O"
def contains(sym):
 d={}
 for a in PW_ALPHA:
  if a!="O":d[("n",a)]="y" if a==sym else "n";d[("y",a)]="y"
 return DFA("Contains "+sym,PW_ALPHA,d,"n",{"y"},pw_class)
def length_dfa():return DFA("Length 8-16",PW_ALPHA,{("l"+str(i),a):"l"+str(i+1) for i in range(16) for a in PW_ALPHA if a!="O"},"l0",{"l"+str(i) for i in range(8,17)},pw_class)
PW_PARTS=[contains(x) for x in "ULDS"]+[length_dfa()]
PASSWORD_PRODUCT=PW_PARTS[0]
for part in PW_PARTS[1:]:PASSWORD_PRODUCT=PASSWORD_PRODUCT.intersect(part)
PASSWORD_DFA=PASSWORD_PRODUCT.minimize("Password policy")
# NFA grammar: local=alnum+([._-]alnum+)*; domain=label('.'label)*'.'tld.
EM_ALPHA=["L","D","DOT","HY","US","AT","O"]
def email_class(c):return "L" if c in string.ascii_letters else "D" if c in string.digits else {".":"DOT","-":"HY","_":"US","@":"AT"}.get(c,"O")
ed={}
def add(p,syms,q):
 for a in syms:ed.setdefault((p,a),set()).add(q)
A=["L","D"];add("n0",A,"n1");add("n1",A,"n1");add("n1",["DOT","HY","US"],"n2");add("n2",A,"n1");add("n1",["AT"],"n3");add("n3",A,"n4");add("n4",A,"n4");add("n4",["HY"],"n5");add("n5",["HY"],"n5");add("n5",A,"n4");add("n4",["DOT"],"n3");add("n4",["DOT"],"n6");add("n6",["L"],"n7");add("n7",["L"],"n8");add("n8",["L"],"n8")
EMAIL_NFA=NFA("Email NFA",EM_ALPHA,ed,"n0",{"n8"},email_class)
EMAIL_SUBSET=EMAIL_NFA.to_dfa("Email subset DFA");EMAIL_DFA=EMAIL_SUBSET.minimize("Email minimal DFA")
TESTS={"pin":{"accept":["4821","0000","9375","1234","0042"],"reject":["123","12345","12a4","12 4",""]},"weak_pin":{"accept":["0000","1111","2222","9999"],"reject":["1234","1000","0001","12a4",""]},"password":{"accept":["Srm@2026","Trichy#Aiml5","aB3$efgh","P@ssw0rdX","Q1w2e3r4!T"],"reject":["srm@2026","SRM@2026","Srm@Trichy","Srm20266","Srm @2026"]},"email":{"accept":["tarun.varma@srmist.edu.in","ra2411026050037@srmist.edu.in","student_one@gmail.com","alex-raj@my-site.co","user123@college.org"],"reject":["student@college",".tarun@gmail.com","student..one@gmail.com","student@-college.in","student@gmail.c"]}}
