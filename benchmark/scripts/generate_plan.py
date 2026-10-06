#!/usr/bin/env python3
import argparse,csv,itertools,json,random
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--seed',type=int,default=20261004);p.add_argument('--clients',nargs='+',default=['Claude Code']);p.add_argument('--repetitions',type=int,default=3);a=p.parse_args()
if a.repetitions<3:p.error('At least three repetitions')
k=Path(__file__).resolve().parents[1];tasks=json.loads((k/'tasks.yaml').read_text())['tasks'];configs=json.loads((k/'configurations.yaml').read_text())['configurations'];rng=random.Random(a.seed)
rows=[]
for task in tasks:
 block=list(itertools.product(a.clients,configs,range(1,a.repetitions+1)));rng.shuffle(block)
 for client,config,rep in block:rows.append({'run_id':f'run-{len(rows)+1:04d}','task':task['id'],'client':client,'configuration':config['id'],'replicate':rep,'fixture_seed':a.seed,'surfaces':'desktop+pwa','status':'planned'})
with Path(a.out).open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps({'planned_generations':len(rows),'surface_evaluations':len(rows)*2,'seed':a.seed}))
