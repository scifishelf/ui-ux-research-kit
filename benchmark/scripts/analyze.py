#!/usr/bin/env python3
"""Pilot analysis of one dimension/client. Rows are panel aggregates per generation/surface."""
import argparse,csv,json,math,random,statistics as st
from pathlib import Path

def ranks(xs):
 s=sorted(range(len(xs)),key=lambda i:xs[i]);r=[0.0]*len(xs);i=0
 while i<len(s):
  j=i+1
  while j<len(s) and xs[s[j]]==xs[s[i]]:j+=1
  for k in range(i,j):r[s[k]]=(i+1+j)/2
  i=j
 return r

def correlation(x,y):
 if len(x)<2 or st.pstdev(x)==0 or st.pstdev(y)==0:return None
 return st.correlation(x,y)

def analyze(rows,a,b,seed=20261004):
 groups={}
 for r in rows:
  if r['configuration'] not in {a,b}:continue
  key=(r['task'],r['replicate'],r['surface'])
  g=groups.setdefault(key,{})
  if r['configuration'] in g:raise ValueError('Duplicate aggregate; collapse panel raters first')
  score=float(r['score'])
  if not math.isfinite(score) or not 0<=score<=4:raise ValueError('Invalid 0–4 score')
  g[r['configuration']]=score
 if not groups or any(set(g)!={a,b} for g in groups.values()):raise ValueError('Missing paired configuration; include failure outcomes explicitly')
 # Collapse paired desktop/PWA differences per generation to avoid pseudo-replication.
 by_gen={}
 for (task,rep,surface),g in groups.items():by_gen.setdefault((task,rep),{})[surface]=g[b]-g[a]
 if any(set(s)!={'desktop','pwa'} for s in by_gen.values()):raise ValueError('Both surfaces required')
 differences=[st.mean(v.values()) for v in by_gen.values()];clusters={}
 for (task,rep),surfaces in by_gen.items():clusters.setdefault(task,[]).append(st.mean(surfaces.values()))
 delta=st.mean(differences);sd=st.stdev(differences) if len(differences)>1 else 0
 rng=random.Random(seed);keys=sorted(clusters);bs=[]
 if len(keys)>1:
  for _ in range(3000):
   sample=rng.choices(keys,k=len(keys));vals=[v for key in sample for v in clusters[key]];bs.append(st.mean(vals))
  bs.sort()
 return {'contrast':b+'-'+a,'n_generations':len(by_gen),'n_task_clusters':len(keys),'mean_delta':delta,'dz':delta/sd if sd else None,'cluster_bootstrap_ci95':[bs[int(.025*(len(bs)-1))],bs[int(.975*(len(bs)-1))]] if bs else None,'surface_deltas':{s:st.mean(g[b]-g[a] for key,g in groups.items() if key[2]==s) for s in ['desktop','pwa']},'warning':'Pilot; few task clusters, ordinal scores, no causal conclusion without protocol compliance.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--a',default='K2');p.add_argument('--b',default='K4');p.add_argument('--out');args=p.parse_args();rows=list(csv.DictReader(open(args.csv)))
 if len({r.get('client','') for r in rows})>1 or len({r.get('dimension','') for r in rows})>1:p.error('Use one client and one dimension')
 try:
  result=analyze(rows,args.a,args.b)
  paired=[r for r in rows if r.get('judge_score','')!='']
  if paired:
   experts=[float(r['score']) for r in paired];judges=[float(r['judge_score']) for r in paired]
   if any(not math.isfinite(x) or not 0<=x<=4 for x in judges):raise ValueError('Invalid judge score')
   result['judge']={'n':len(paired),'spearman':correlation(ranks(experts),ranks(judges)),'mae':st.mean(abs(a-b) for a,b in zip(experts,judges)),'note':'Exploratory; dependent rows and missing calibration/holdout require separate analysis.'}
 except (ValueError,KeyError) as e:p.error(str(e))
 s=json.dumps(result,indent=2)
 if args.out:Path(args.out).write_text(s+'\n')
 print(s)
if __name__=='__main__':main()
