#!/usr/bin/env python3
"""Check portable package consistency; --schemas requires jsonschema."""
import argparse,csv,json,re
from pathlib import Path
from urllib.parse import unquote
KIT=Path(__file__).resolve().parents[2]
def validate(kit=KIT,schemas=False):
 kit=Path(kit);errors=[];files=list(kit.rglob('*.yaml'))+list(kit.rglob('*.json'));parsed={}
 for p in files:
  if '.git' in p.parts or 'node_modules' in p.parts:continue
  try:parsed[p.relative_to(kit).as_posix()]=json.loads(p.read_text())
  except (ValueError,OSError) as e:errors.append(str(p)+': '+str(e))
 catalog=parsed['criteria/catalog.yaml']['criteria'];ids={c['id'] for c in catalog}
 product=parsed.get('criteria/product/catalog.yaml',{}).get('criteria',[])
 product_ids={c['id'] for c in product}
 if len(product_ids)!=len(product) or ids.intersection(product_ids):errors.append('Duplicate product criterion IDs')
 all_ids=ids|product_ids
 sources={s['id'] for s in parsed['report/sources.yaml']['sources']}
 def walk(v,name):
  if isinstance(v,dict):
   for k,x in v.items():
    if k in ['sources','criteria'] and isinstance(x,list) and all(isinstance(a,str) for a in x):
     allowed=sources if k=='sources' else all_ids
     for a in x:
      if a not in allowed:errors.append(name+': unresolved '+k+' '+a)
    walk(x,name)
  elif isinstance(v,list):
   for x in v:walk(x,name)
 for name,v in parsed.items():walk(v,name)
 links=0
 for p in kit.rglob('*.md'):
  body=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
  for raw in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',body):
   rel=unquote(raw.strip().strip('<>')).split('#',1)[0]
   if not rel or re.match(r'^[a-zA-Z]+:',rel):continue
   links+=1
   if not (p.parent/rel).exists():errors.append(str(p.relative_to(kit))+': broken link '+rel)
 for item in parsed['motion-patterns/catalog.yaml']['patterns']:
  for rel in [item['code'],item['video_evidence']['desktop']]:
   if not (kit/'motion-patterns'/rel).is_file():errors.append(item['id']+': missing artifact '+rel)
 for repo in parsed['report/evidence/repository-pins.json']:
  if not re.fullmatch('[a-f0-9]{40}',repo['commit']):errors.append('Invalid commit '+repo['repository'])
 rows=list(csv.DictReader((kit/'benchmark/run-plan-primary.csv').open()))
 if len(rows)!=90 or len({(r['task'],r['configuration'],r['replicate']) for r in rows})!=90 or any(r['status']!='planned' for r in rows):errors.append('Invalid planned benchmark')
 if schemas:
  from jsonschema import Draft202012Validator
  for name,v in parsed.items():
   if name.endswith('.schema.json'):
    try:Draft202012Validator.check_schema(v)
    except Exception as e:errors.append(name+': '+str(e))
  critic=Draft202012Validator(parsed['rubrics/critic-output.schema.json'])
  dims=[d['id'] for d in parsed['rubrics/ui-ux-motion.yaml']['dimensions']]
  empty=dict(build='fixture',surface='both',scores={d:None for d in dims},findings=[],unknown=['Runtime not observed'],release_recommendation='human_review_required')
  critic.validate(empty)
  bad={**empty,'scores':{**empty['scores'],'invented':4}}
  if critic.is_valid(bad):errors.append('Critic schema accepts unknown dimension')
  observation_schema='skills/web-excellence-audit/references/observations.schema.json'
  if observation_schema in parsed:
   observation=Draft202012Validator(parsed[observation_schema])
   try:observation.validate(parsed['skills/web-excellence-audit/references/observations.example.json'])
   except Exception as e:errors.append('Product observation example: '+str(e))
 return {'status':'fail' if errors else 'pass','errors':errors,'json_yaml_files':len(parsed),'relative_links':links,'criteria':len(ids),'product_criteria':len(product_ids),'public_sources':len(parsed['report/sources.yaml']['sources']),'radar_entries':len(parsed['skill-radar.yaml']['tools']),'patterns':len(parsed['motion-patterns/catalog.yaml']['patterns']),'planned_runs':len(rows),'schema_definition_check':schemas}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--schemas',action='store_true');a=p.parse_args();r=validate(schemas=a.schemas);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['status']=='pass' else 1)
