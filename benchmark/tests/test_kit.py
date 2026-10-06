"""Synthetic fixtures test script behavior; never product/benchmark evidence."""
import datetime,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
KIT=Path(__file__).resolve().parents[2]
def module(rel):
 spec=importlib.util.spec_from_file_location(Path(rel).stem,KIT/rel);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
parity=module('reference/loop/parity_check.py')
audit=module('skills/pipeline-audit/scripts/audit.py')
analysis=module('benchmark/scripts/analyze.py')
reliability=module('benchmark/scripts/reliability.py')
class Parity(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.addCleanup(self.tmp.cleanup)
  # Signature fixture tests provenance only, not image decoding or aesthetics.
  b=b'\x89PNG\r\n\x1a\nfixture';(self.root/'screen.png').write_bytes(b)
  self.now=datetime.datetime(2026,10,4,12,tzinfo=datetime.timezone.utc)
  self.base=dict(schemaVersion='1',buildId='build-a',runId='run-a',fixtureId='B01',state='empty',theme='light',reducedMotion=False,tokenVersion='1',capturedAt=self.now.isoformat(),screenshot=dict(path='screen.png',sha256=hashlib.sha256(b).hexdigest()),runtime=dict(name='Safari',version='27',osVersion='27',device='iPhone'),semantics={'result':'empty'},tokens={'primary':'blue'})
  self.d={**self.base,'surface':'desktop','captureKind':'desktop-browser'}
  self.p={**self.base,'surface':'pwa','captureKind':'ios-simulator','displayMode':'standalone','swBuildId':'build-a'}
 def check(self,d=None,p=None):
  (self.root/'d.json').write_text(json.dumps(self.d if d is None else d));(self.root/'p.json').write_text(json.dumps(self.p if p is None else p));return parity.check(self.root/'d.json',self.root/'p.json','build-a',now=self.now)
 def test_complete_pair(self):self.assertEqual(self.check()['status'],'pass')
 def test_browser_emulation_is_not_pwa(self):self.assertEqual(self.check(p={**self.p,'captureKind':'desktop-browser','displayMode':'browser'})['status'],'fail')
 def test_wrong_build_and_worker(self):
  for key in ['buildId','swBuildId']:self.assertEqual(self.check(p={**self.p,key:'old'})['status'],'fail')
 def test_wrong_hash_and_unsafe_path(self):
  for s in [{'path':'screen.png','sha256':'wrong'},{'path':'../screen.png','sha256':'wrong'}]:self.assertEqual(self.check(p={**self.p,'screenshot':s})['status'],'fail')
 def test_stale_or_mismatched_state(self):
  for patch in [{'capturedAt':'2026-10-01T12:00:00Z'},{'state':'error'},{'tokens':{'primary':'red'}},{'semantics':{}}]:self.assertEqual(self.check(p={**self.p,**patch})['status'],'fail')
 def test_malformed_metadata_fails_without_crash(self):
  for patch in [{'runtime':'Safari'},{'screenshot':None},{'capturedAt':None},{'reducedMotion':'false'},{'theme':[]},{'runId':None},{'captureKind':[]}]:self.assertEqual(self.check(p={**self.p,**patch})['status'],'fail')
  self.assertEqual(self.check(p=[])['status'],'fail')
class Audit(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.addCleanup(self.tmp.cleanup);(self.root/'CLAUDE.md').write_text('Screenshots required')
 def test_inventory_is_not_pass(self):
  r=audit.run(self.root,'.',KIT,kind='fixture');self.assertEqual(r['counts']['unknown'],45);self.assertEqual(r['counts']['pass'],0);self.assertEqual(r['release_gate'],'blocked')
 def test_source_change_invalidates_observation(self):
  obs={'LOOP-01':{'status':'pass','reason':'Fixture assertion','scope':'fixture','evidence':[{'path':'CLAUDE.md','sha256':audit.digest(self.root/'CLAUDE.md')}]}}
  self.assertEqual(audit.run(self.root,'.',KIT,obs,'fixture')['findings'][0]['status'],'pass')
  (self.root/'CLAUDE.md').write_text('Changed');self.assertEqual(audit.run(self.root,'.',KIT,obs,'fixture')['findings'][0]['status'],'unknown')
 def test_unsupported_and_unsafe_assertions(self):
  for obs in [{'FAKE':{}},{'LOOP-01':{'status':'pass','reason':'a','scope':'fixture'}},{'LOOP-01':{'status':'pass','reason':'a','scope':'fixture','evidence':[{'path':'../escape','sha256':'x'}]}}]:
   with self.assertRaises(ValueError):audit.run(self.root,'.',KIT,obs,'fixture')
class Statistics(unittest.TestCase):
 def rows(self):
  return [dict(task=task,replicate='1',surface=s,configuration=k,score=score) for task in ['B01','B02'] for s in ['desktop','pwa'] for k,score in [('K2',1),('K4',2)]]
 def test_surfaces_do_not_double_sample_size(self):
  r=analysis.analyze(self.rows(),'K2','K4');self.assertEqual(r['n_generations'],2);self.assertEqual(r['mean_delta'],1);self.assertEqual(r['cluster_bootstrap_ci95'],[1,1]);self.assertIsNone(r['dz'])
 def test_incomplete_or_duplicate_pairs_rejected(self):
  for rows in [self.rows()[:-1],self.rows()+[self.rows()[0]],[r for r in self.rows() if r['surface']=='desktop']]:
   with self.assertRaises(ValueError):analysis.analyze(rows,'K2','K4')
 def test_rank_ties_and_inverse_correlation(self):
  self.assertEqual(analysis.ranks([1,1,3]),[1.5,1.5,3]);self.assertAlmostEqual(analysis.correlation([1,2,3],[3,2,1]),-1)
 def test_ordinal_alpha_known_cases(self):
  self.assertEqual(reliability.ordinal_alpha([[0,0],[4,4]]),1)
  self.assertAlmostEqual(reliability.ordinal_alpha([[0,4],[0,4]]),-0.5)
  self.assertIsNone(reliability.ordinal_alpha([[2,2],[2]]))
class Catalog(unittest.TestCase):
 def test_category_copies_match_catalog(self):
  canonical=json.loads((KIT/'criteria/catalog.yaml').read_text())['criteria'];copies=[]
  for p in (KIT/'criteria').glob('*.yaml'):
   if p.name!='catalog.yaml':copies+=json.loads(p.read_text())['criteria']
  self.assertEqual(sorted(canonical,key=lambda c:c['id']),sorted(copies,key=lambda c:c['id']))
  self.assertEqual(len({c['id'] for c in canonical}),45)
if __name__=='__main__':unittest.main()
