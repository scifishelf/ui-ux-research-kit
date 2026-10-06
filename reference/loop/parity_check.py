#!/usr/bin/env python3
"""Gate a real capture pair. Exit 1 for absent, stale, mismatched evidence."""
import argparse, datetime, hashlib, json
from pathlib import Path

def check(dp,pp,expected,now=None,max_age_hours=24):
    now=now or datetime.datetime.now(datetime.timezone.utc)
    errors=[];captures=[]
    if not isinstance(expected,str) or not expected.strip():errors.append('expected build must be a nonempty string')
    for path,surface in [(Path(dp),'desktop'),(Path(pp),'pwa')]:
        try:c=json.loads(path.read_text())
        except (OSError,json.JSONDecodeError) as e:errors.append(surface+': unreadable manifest '+str(e));continue
        if not isinstance(c,dict):errors.append(surface+': manifest must be an object');continue
        required=['schemaVersion','surface','buildId','runId','fixtureId','state','theme','reducedMotion','tokenVersion','capturedAt','screenshot','runtime','semantics','tokens']
        for key in required:
            if key not in c:errors.append(surface+': missing '+key)
        if c.get('schemaVersion')!='1':errors.append(surface+': schemaVersion')
        if c.get('surface')!=surface:errors.append(surface+': wrong surface')
        if c.get('buildId')!=expected:errors.append(surface+': wrong expected build')
        for key in ['buildId','runId','fixtureId','state','tokenVersion','capturedAt']:
            if not isinstance(c.get(key),str) or not c[key].strip():errors.append(surface+': invalid '+key)
        if c.get('theme') not in ['light','dark']:errors.append(surface+': invalid theme')
        if not isinstance(c.get('reducedMotion'),bool):errors.append(surface+': reducedMotion must be boolean')
        try:
            t=datetime.datetime.fromisoformat(c['capturedAt'].replace('Z','+00:00'))
            age=(now-t).total_seconds()
            if age< -300 or age>max_age_hours*3600:errors.append(surface+': stale or future capture')
        except (ValueError,TypeError,KeyError,AttributeError):errors.append(surface+': invalid time')
        image=c.get('screenshot',{})
        if not isinstance(image,dict):image={};errors.append(surface+': screenshot must be an object')
        rel=image.get('path','')
        if not isinstance(rel,str):rel=''
        im=(path.parent/rel).resolve()
        if not rel or not im.is_relative_to(path.parent.resolve()) or not im.is_file():errors.append(surface+': missing/unsafe screenshot')
        else:
            b=im.read_bytes()
            if not b.startswith(b'\x89PNG\r\n\x1a\n'):errors.append(surface+': screenshot not PNG')
            if hashlib.sha256(b).hexdigest()!=image.get('sha256'):errors.append(surface+': screenshot hash mismatch')
        runtime=c.get('runtime',{})
        if not isinstance(runtime,dict):runtime={}
        if any(not isinstance(runtime.get(k),str) or not runtime[k].strip() for k in ['name','version']):errors.append(surface+': runtime missing')
        if not isinstance(c.get('semantics'),dict) or not c.get('semantics'):errors.append(surface+': empty semantics')
        if not isinstance(c.get('tokens'),dict) or not c.get('tokens'):errors.append(surface+': empty tokens')
        if surface=='pwa':
            if c.get('displayMode')!='standalone':errors.append('pwa: not standalone')
            if c.get('swBuildId')!=expected:errors.append('pwa: controller SW build mismatch')
            if any(not isinstance(runtime.get(k),str) or not runtime[k].strip() for k in ['osVersion','device']):errors.append('pwa: device or OS missing')
            if c.get('captureKind') not in ['ios-simulator','ios-real-device']:errors.append('pwa: not an iOS capture')
        elif c.get('captureKind')!='desktop-browser':errors.append('desktop: invalid capture kind')
        captures.append(c)
    if len(captures)==2:
        d,p=captures
        for key in ['buildId','runId','fixtureId','state','theme','reducedMotion','tokenVersion','semantics','tokens']:
            if d.get(key)!=p.get(key):errors.append('parity: '+key+' differs')
    return {'status':'fail' if errors else 'pass','errors':errors,'expectedBuild':expected,'scope':'One capture pair only; not visual aesthetics, full state coverage, or usability validation.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('desktop');ap.add_argument('pwa');ap.add_argument('--expected-build',required=True);ap.add_argument('--max-age-hours',type=float,default=24);ap.add_argument('--out');a=ap.parse_args()
    if a.max_age_hours<=0:ap.error('max-age-hours must be positive')
    r=check(a.desktop,a.pwa,a.expected_build,max_age_hours=a.max_age_hours);s=json.dumps(r,indent=2)
    if a.out:Path(a.out).write_text(s+'\n')
    print(s);raise SystemExit(0 if r['status']=='pass' else 1)
if __name__=='__main__':main()
