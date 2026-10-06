#!/usr/bin/env python3
"""Ordinal Krippendorff alpha, one dimension/surface; missing ratings omitted."""
import argparse,csv,json,collections,math

def ordinal_alpha(units):
 usable=[u for u in units if len(u)>=2]
 if not usable:return None
 counts=collections.Counter(v for u in usable for v in u);cats=sorted(counts);n=sum(counts.values())
 def distance(a,b):
  if a==b:return 0.0
  lo,hi=sorted([a,b]);return (sum(counts[c] for c in cats if lo<=c<=hi)-(counts[lo]+counts[hi])/2)**2
 observed=sum(sum(distance(a,b) for i,a in enumerate(u) for j,b in enumerate(u) if i!=j)/(len(u)-1) for u in usable)/n
 expected=sum(counts[a]*counts[b]*distance(a,b) for a in cats for b in cats if a!=b)/(n*(n-1))
 return 1-observed/expected if expected else None

def main():
 p=argparse.ArgumentParser();p.add_argument('csv');a=p.parse_args();rows=list(csv.DictReader(open(a.csv)));units={};seen=set()
 if len({(r.get('dimension',''),r.get('surface','')) for r in rows})>1:p.error('Use one dimension and one surface')
 for r in rows:
  if r['score']=='':continue
  key=(r['sample_id'],r['rater'])
  if key in seen:p.error('Duplicate rater for sample')
  seen.add(key);score=float(r['score'])
  if not math.isfinite(score) or score not in range(5):p.error('Integer 0–4 rating required')
  units.setdefault(r['sample_id'],[]).append(score)
 print(json.dumps({'ordinal_alpha':ordinal_alpha(list(units.values())),'n_units_with_two_or_more_raters':sum(len(u)>=2 for u in units.values()),'confidence_interval':None,'status':'Point estimate only; task-cluster bootstrap required for study reporting.'},indent=2))
if __name__=='__main__':main()
