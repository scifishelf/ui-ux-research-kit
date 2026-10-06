#!/usr/bin/env python3
"""Read-only project inventory; evidence-based observations, never regex-based pass."""
import argparse, datetime, hashlib, json, subprocess
from pathlib import Path
STATUSES={'pass','fail','unknown','not_applicable'}
SKIP={'.git','node_modules','.next','build-output','dist','worktrees','data','storage','__pycache__'}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(p,root): return p.resolve().is_relative_to(root.resolve())
def collect(root,frontend):
    fixed=['CLAUDE.md','AGENTS.md','.claude/settings.json','.mcp.json','.gitlab-ci.yml','check.sh']
    fixed += [str(Path(frontend)/x) for x in ['package.json','pnpm-lock.yaml','package-lock.json','playwright.config.ts','playwright.config.js','next.config.ts','tailwind.config.ts','biome.json','docs/design/design-system.md','src/app/sw.ts','src/styles/globals.css']]
    found={}
    def add(p):
        if p.is_file() and not p.is_symlink() and inside(p,root):
            if p.stat().st_size<=4_000_000: found[p.relative_to(root).as_posix()]={'sha256':digest(p),'bytes':p.stat().st_size}
    for rel in fixed: add(root/rel)
    for base,pattern in [('.claude/skills','*/SKILL.md'),('.agents/skills','*/SKILL.md'),('.github/workflows','*.y*ml'),('tools/simulator','*')]:
        for p in sorted((root/base).glob(pattern)):add(p)
    for base in ['docs/pwa.md','docs/HANDOFF.md','docs/BACKLOG.md','docs/TESTING.md']:
        add(root/base)
    for base in [Path(frontend)/'src/lib/pwa',Path(frontend)/'tests/e2e']:
        for p in sorted((root/base).rglob('*')):
            if not any(x in SKIP for x in p.parts) and p.suffix in {'.ts','.tsx','.md'}: add(p)
    return found

def run(target,frontend,kit,observations=None,kind='app'):
    root=Path(target).resolve()
    if not root.is_dir(): raise ValueError('Target directory missing')
    if not (root/frontend).resolve().is_relative_to(root): raise ValueError('Frontend must be inside target')
    catalog=json.loads((Path(kit)/'criteria/catalog.yaml').read_text())['criteria']
    inventory=collect(root,frontend)
    commit=None
    try:
        commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],stderr=subprocess.DEVNULL,text=True).strip()
    except (subprocess.CalledProcessError,FileNotFoundError): pass
    inventory_hash=hashlib.sha256(json.dumps(inventory,sort_keys=True).encode()).hexdigest()
    obs=observations or {}
    ids={c['id'] for c in catalog}
    if set(obs)-ids: raise ValueError('Unknown criterion: '+str(set(obs)-ids))
    findings=[]
    for c in catalog:
        o=obs.get(c['id']); status='unknown'; reason='No criterion-specific check has been evidenced.'; evidence=[]; scope='inventory_only'; stale=False
        if o:
            status=o.get('status');reason=o.get('reason','');scope=o.get('scope','')
            if status not in STATUSES or not reason or not scope: raise ValueError('Invalid observation '+c['id'])
            if status in {'pass','fail'} and not o.get('evidence'): raise ValueError('Evidence required '+c['id'])
            for e in o.get('evidence',[]):
                p=root/e['path']
                if not inside(p,root) or not p.is_file() or p.is_symlink(): raise ValueError('Unsafe/missing evidence '+e['path'])
                actual=digest(p); evidence.append({'path':e['path'],'sha256':actual,'locator':e.get('locator')})
                if actual!=e.get('sha256'):stale=True
            if stale: status='unknown';reason='Evidence file changed since observation. '+reason
        findings.append({'id':c['id'],'level':c['level'],'platforms':c['platforms'],'status':status,'scope':scope,'reason':reason,'evidence':evidence,'action':c['action'],'effort':c['effort'],'test':c['test'],'passing':c['passing']})
    counts={s:sum(x['status']==s for x in findings) for s in sorted(STATUSES)}
    blockers=[x['id'] for x in findings if x['level']=='MUST' and x['status'] in {'fail','unknown'}]
    return {'version':(Path(kit)/'VERSION').read_text().strip(),'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target':str(root),'frontend':frontend,'kind':kind,'commit':commit,'inventory_hash':inventory_hash,'scope':'Selected project files only; no global skill/MCP inventory or runtime test.','inventory':inventory,'findings':findings,'counts':counts,'unresolved_must':blockers,'release_gate':'blocked' if blockers else 'human_review_required'}

def write(report,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    lines=['# Pipeline audit — gap report','',f"Target: `{report['target']}` · Frontend: `{report['frontend']}` · Commit: `{report['commit']}`",'',report['scope'],'',f"Gate: **{report['release_gate']}** · Status: `{report['counts']}`",'', '| ID | Level | Status | Observation / scope | Action / effort |','| --- | --- | --- | --- | --- |']
    for f in report['findings']:
        reason=(f['reason']+' ['+f['scope']+']').replace('|','/').replace('\n',' ')
        lines.append(f"| {f['id']} | {f['level']} | {f['status']} | {reason} | {f['action']} ({f['effort']}) |")
    lines += ['','Evidence hashes and locations are in audit.json. Unknown means a missing check, not an observed defect. Fail applies to its stated scope. Unchanged source does not prove a current runtime.']
    (out/'gap-report.md').write_text('\n'.join(lines)+'\n')
    decisions=[{'id':f['id'],'decision':'pending','proposal':f['action'],'effort':f['effort'],'reason':f['reason'],'owner':None,'decided_at':None,'retest':f['test']} for f in report['findings'] if f['status'] in {'fail','unknown'}]
    (out/'decisions.json').write_text(json.dumps({'status':'Proposals; no user decisions assumed','items':decisions},ensure_ascii=False,indent=2)+'\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--target',required=True);p.add_argument('--frontend',default='.');p.add_argument('--out',required=True);p.add_argument('--kit',default=str(Path(__file__).resolve().parents[3]));p.add_argument('--observations');p.add_argument('--kind',choices=['app','fixture','research'],default='app')
    a=p.parse_args();obs=json.loads(Path(a.observations).read_text()) if a.observations else None
    try:r=run(a.target,a.frontend,a.kit,obs,a.kind);write(r,a.out);print(json.dumps({'counts':r['counts'],'release_gate':r['release_gate'],'criteria':len(r['findings'])},ensure_ascii=False))
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as e:p.error(str(e))
if __name__=='__main__':main()
