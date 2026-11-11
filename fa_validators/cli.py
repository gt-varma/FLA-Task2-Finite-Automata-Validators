from .validators import *
def main():
 for key,dfa in [("pin",PIN_DFA),("weak_pin",WEAK_PIN_DFA),("password",PASSWORD_DFA),("email",EMAIL_DFA)]:
  print("\\n"+dfa.name)
  for s in TESTS[key]["accept"]:print(" ACCEPT",repr(s),dfa.accepts(s))
  for s in TESTS[key]["reject"]:print(" REJECT",repr(s),dfa.accepts(s))
 print("\\nState counts")
 for a in [PIN_DFA,WEAK_PIN_DFA,STRONG_PIN_DFA,SESSION_DFA,PASSWORD_PRODUCT,PASSWORD_DFA,EMAIL_SUBSET,EMAIL_DFA]:print(a.name,a.live_states(),"live",len(a.reachable()),"reachable")
 print("Email NFA",9,"states")
if __name__=="__main__":main()
