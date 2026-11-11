from collections import deque
DEAD="qD"
class DFA:
 def __init__(self,name,alphabet,delta,start,accepting,classify,states=None):
  self.name=name; self.alphabet=list(alphabet); self.delta=dict(delta); self.start=start; self.accepting=set(accepting); self.classify=classify
  found={start}|self.accepting
  for (p,_),q in self.delta.items(): found.update((p,q))
  self.states=list(states) if states is not None else sorted(found)
  for p in list(self.states):
   for a in self.alphabet:self.delta.setdefault((p,a),DEAD)
  if DEAD in self.states or any(q==DEAD for q in self.delta.values()):
   if DEAD not in self.states:self.states.append(DEAD)
   for a in self.alphabet:self.delta[(DEAD,a)]=DEAD
 def step(self,p,a):return self.delta.get((p,a),DEAD)
 def run_symbols(self,seq):
  p=self.start; trace=[]
  for a in seq:q=self.step(p,a);trace.append((p,a,q));p=q
  return p in self.accepting,trace
 def run(self,text):return self.run_symbols([self.classify(c) for c in text])
 def accepts(self,text):return self.run(text)[0]
 def reachable(self):
  seen={self.start};todo=deque([self.start])
  while todo:
   p=todo.popleft()
   for a in self.alphabet:
    q=self.step(p,a)
    if q not in seen:seen.add(q);todo.append(q)
  return seen
 def live_states(self):return len(self.reachable()-{DEAD})
 def minimize(self,name=None):
  ss=sorted(self.reachable());n=len(ss);idx={s:i for i,s in enumerate(ss)};mark=[[False]*n for _ in range(n)]
  for i in range(n):
   for j in range(i):mark[i][j]=(ss[i] in self.accepting)!=(ss[j] in self.accepting)
  change=True
  while change:
   change=False
   for i in range(n):
    for j in range(i):
     if mark[i][j]:continue
     for a in self.alphabet:
      x,y=idx[self.step(ss[i],a)],idx[self.step(ss[j],a)]
      if x!=y and mark[max(x,y)][min(x,y)]:mark[i][j]=True;change=True;break
  par=list(range(n))
  def root(x):
   while par[x]!=x:par[x]=par[par[x]];x=par[x]
   return x
  for i in range(n):
   for j in range(i):
    if not mark[i][j]:par[root(i)]=root(j)
  groups={}
  for i,s in enumerate(ss):groups.setdefault(root(i),[]).append(s)
  block={s:b for b,g in groups.items() for s in g};order=[];seen={block[self.start]};todo=deque([block[self.start]])
  while todo:
   b=todo.popleft();order.append(b);rep=groups[b][0]
   for a in self.alphabet:
    nb=block[self.step(rep,a)]
    if nb not in seen:seen.add(nb);todo.append(nb)
  dead=next((b for b in order if groups[b][0] not in self.accepting and all(block[self.step(groups[b][0],a)]==b for a in self.alphabet)),None)
  names={};k=0
  for b in order:
   if b==dead:names[b]=DEAD
   else:names[b]=f"m{k}";k+=1
  delta={(names[b],a):names[block[self.step(groups[b][0],a)]] for b in order for a in self.alphabet}
  acc={names[b] for b in order if groups[b][0] in self.accepting}
  return DFA(name or self.name+" minimal",self.alphabet,delta,names[block[self.start]],acc,self.classify,[names[b] for b in order])
 def intersect(self,o,name=None):
  assert self.alphabet==o.alphabet
  start=(self.start,o.start);seen={start};todo=deque([start]);d={}
  while todo:
   p,q=todo.popleft()
   for a in self.alphabet:
    z=(self.step(p,a),o.step(q,a));d[((p,q),a)]=z
    if z not in seen:seen.add(z);todo.append(z)
  labels={s:f"{s[0]}|{s[1]}" for s in seen};delta={(labels[p],a):labels[q] for (p,a),q in d.items()}
  acc={labels[s] for s in seen if s[0] in self.accepting and s[1] in o.accepting}
  return DFA(name or self.name+" AND "+o.name,self.alphabet,delta,labels[start],acc,self.classify,list(labels.values()))
class NFA:
 def __init__(self,name,alphabet,delta,start,accepting,classify):self.name=name;self.alphabet=list(alphabet);self.delta={k:set(v) for k,v in delta.items()};self.start=start;self.accepting=set(accepting);self.classify=classify
 def accepts(self,text):
  cur={self.start}
  for c in text:
   a=self.classify(c);cur=set().union(*(self.delta.get((q,a),set()) for q in cur)) if cur else set()
  return bool(cur&self.accepting)
 def to_dfa(self,name=None):
  start=frozenset([self.start]);seen={start};todo=deque([start]);names={start:"{"+self.start+"}"};d={}
  while todo:
   sub=todo.popleft()
   for a in self.alphabet:
    nxt=frozenset().union(*(self.delta.get((q,a),set()) for q in sub))
    if nxt and nxt not in seen:seen.add(nxt);todo.append(nxt);names[nxt]="{"+",".join(sorted(nxt))+"}"
    d[(names[sub],a)]=names.get(nxt,DEAD)
  acc={names[s] for s in seen if s&self.accepting}
  return DFA(name or self.name+" subset DFA",self.alphabet,d,names[start],acc,self.classify)
