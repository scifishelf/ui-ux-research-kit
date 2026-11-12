"""Synthetic projects validate audit behavior, not real product quality."""
import datetime
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('product_audit', KIT / 'skills/web-excellence-audit/scripts/audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ProductAudit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.root = self.base / 'app'
        self.root.mkdir()
        self.evidence = self.base / 'evidence'
        self.evidence.mkdir()
        (self.root / 'index.html').write_text('<h1>Task fixture</h1>')
        (self.evidence / 'run.txt').write_text('Synthetic runtime log; not a real browser result.')
        self.now = datetime.datetime(2026, 10, 5, 10, tzinfo=datetime.timezone.utc)
        self.project = {'profile': 'website', 'features': {f: False for f in audit.FEATURES},
                        'viewports': [{'width': 390, 'height': 844}],
                        'journeys': [{'id': 'J1', 'route': '/', 'task': 'Read purpose',
                                      'success': 'Purpose is understood', 'states': ['default']}],
                        'available_capabilities': []}

    def run_audit(self, obs=None, **kwargs):
        return audit.run(self.root, KIT, project=kwargs.pop('project', self.project),
                         observations=obs, evidence_root=self.evidence, now=self.now, **kwargs)

    def envelope(self, findings):
        baseline = self.run_audit()
        return {'schema_version': 1, 'target': str(self.root),
                'source_inventory_hash': baseline['source_inventory_hash'],
                'scope_hash': baseline['scope_hash'], 'findings': findings}

    def observed(self, status='pass', **patch):
        value = {'status': status, 'reason': 'Synthetic fixture observation',
                 'scope': 'J1 / default mobile', 'observed_at': self.now.isoformat(),
                 'evidence': [{'root': 'evidence', 'path': 'run.txt', 'kind': 'test-log',
                               'sha256': audit.digest(self.evidence / 'run.txt')}],
                 'runtime': {'url': 'http://localhost:3000/', 'route': '/', 'state': 'default',
                             'browser': 'Synthetic', 'browser_version': 'fixture',
                             'build_id': 'fixture', 'viewport': {'width': 390, 'height': 844},
                             'capture_kind': 'desktop-browser'},
                 'coverage': [{'journey_id': 'J1', 'state': 'default', 'viewport': {'width': 390, 'height': 844}}]}
        if status == 'fail':
            value['remediation'] = {'title': 'Repair heading hierarchy',
                                    'steps': ['Change the conflicting heading in index.html.'],
                                    'affected_files': ['index.html'],
                                    'acceptance': ['J1 has one unambiguous heading.'], 'effort': 'S'}
        return {**value, **patch}

    def field_evidence(self):
        return [{'root': 'evidence', 'path': 'run.txt', 'kind': 'field-data', 'sha256': audit.digest(self.evidence / 'run.txt')}]

    def finding(self, report, id):
        return next(f for f in report['findings'] if f['id'] == id)

    def test_static_website_has_no_pwa_or_study_blockers(self):
        report = self.run_audit()
        self.assertEqual(report['profile'], 'website')
        self.assertEqual(len(report['findings']), 31)
        self.assertFalse(any(id.startswith(('PWA-', 'EVAL-', 'LOCAL-')) for id in report['unresolved_must']))
        self.assertEqual(report['counts']['pass'], 0)
        self.assertFalse(any(t['kind'] == 'Agent skill' for t in report['tool_recommendations']))

    def test_unknown_feature_is_not_excluded(self):
        config = {**self.project, 'features': {'pwa': False}}
        report = self.run_audit(project=config)
        self.assertEqual(self.finding(report, 'FLOW-03')['status'], 'unknown')
        self.assertEqual(self.finding(self.run_audit(), 'FLOW-03')['status'], 'not_applicable')

    def test_framework_discovery_and_explicit_profile(self):
        (self.root / 'package.json').write_text(json.dumps({'dependencies': {'react': 'fixture'}, 'scripts': {'dev': 'secret-command'}}))
        report = audit.run(self.root, KIT, now=self.now)
        self.assertEqual(report['profile'], 'webapp')
        self.assertFalse(report['profile_confirmed'])
        self.assertEqual(report['discovery']['script_names']['package.json'], ['dev'])
        self.assertNotIn('secret-command', json.dumps(report))
        self.assertEqual(self.run_audit(profile='webapp', project={**self.project, 'features': {}})['profile'], 'webapp')

    def test_monorepo_requires_selection_and_scopes_stack(self):
        (self.root / 'index.html').unlink()
        for name, framework in [('react-app', 'react'), ('vue-app', 'vue')]:
            folder = self.root / 'apps' / name
            folder.mkdir(parents=True)
            (folder / 'package.json').write_text(json.dumps({'dependencies': {framework: 'fixture'}}))
        with self.assertRaisesRegex(ValueError, 'Multiple frontends'):
            self.run_audit()
        report = self.run_audit(frontend='apps/vue-app')
        self.assertEqual(report['discovery']['stack_hints'], ['vue'])

    def test_runtime_pass_requires_runtime_and_full_matrix(self):
        value = self.observed()
        value.pop('runtime')
        with self.assertRaisesRegex(ValueError, 'Runtime provenance'):
            self.run_audit(self.envelope({'WEB-01': value}))
        report = self.run_audit(self.envelope({'WEB-01': self.observed(coverage=[])}))
        self.assertEqual(self.finding(report, 'WEB-01')['status'], 'unknown')
        report = self.run_audit(self.envelope({'WEB-01': self.observed()}))
        self.assertEqual(self.finding(report, 'WEB-01')['status'], 'pass')

    def test_source_only_cannot_pass_runtime(self):
        value = self.observed(evidence=[{'root': 'target', 'path': 'index.html', 'kind': 'source',
                                         'sha256': audit.digest(self.root / 'index.html')}])
        with self.assertRaisesRegex(ValueError, 'Runtime artifact'):
            self.run_audit(self.envelope({'WEB-01': value}))

    def test_project_change_invalidates_same_runtime_artifact(self):
        obs = self.envelope({'WEB-01': self.observed()})
        (self.root / 'index.html').write_text('<h1>Changed product</h1>')
        report = self.run_audit(obs)
        self.assertEqual(self.finding(report, 'WEB-01')['status'], 'unknown')
        self.assertIn('Project inventory', self.finding(report, 'WEB-01')['reason'])

    def test_scope_and_evidence_changes_invalidate_observation(self):
        obs = self.envelope({'WEB-01': self.observed()})
        changed = {**self.project, 'audience': 'Different audience'}
        self.assertEqual(self.finding(self.run_audit(obs, project=changed), 'WEB-01')['status'], 'unknown')
        (self.evidence / 'run.txt').write_text('Changed log')
        self.assertEqual(self.finding(self.run_audit(obs), 'WEB-01')['status'], 'unknown')

    def test_report_language_does_not_invalidate_tested_product_scope(self):
        obs = self.envelope({'WEB-01': self.observed()})
        config = {**self.project, 'report_language': 'Japanese / 日本語'}
        report = self.run_audit(obs, project=config)
        self.assertEqual(self.finding(report, 'WEB-01')['status'], 'pass')
        self.assertEqual(report['report_language'], config['report_language'])
        self.assertEqual(report['template_language'], 'English')
        out = self.base / 'multilingual-audit'
        audit.write(report, out)
        plan = json.loads((out / 'action-plan.json').read_text())
        self.assertEqual(plan['report_language'], config['report_language'])
        self.assertEqual(json.loads((out / 'audit.json').read_text())['counts'], report['counts'])

    def test_report_language_requires_nonempty_text(self):
        self.assertEqual(self.run_audit()['report_language'], 'English')
        for language in ['', '   ', None, 42, []]:
            with self.assertRaisesRegex(ValueError, 'report_language'):
                self.run_audit(project={**self.project, 'report_language': language})

    def test_wrong_target_and_expired_evidence(self):
        obs = self.envelope({'WEB-01': self.observed()})
        with self.assertRaisesRegex(ValueError, 'target'):
            self.run_audit({**obs, 'target': '/tmp/other-app'})
        value = self.observed(observed_at='2026-09-01T10:00:00Z')
        self.assertEqual(self.finding(self.run_audit(self.envelope({'WEB-01': value})), 'WEB-01')['status'], 'unknown')

    def test_fail_requires_concrete_remediation_and_becomes_improvement(self):
        with self.assertRaisesRegex(ValueError, 'Concrete remediation'):
            self.run_audit(self.envelope({'WEB-01': self.observed('fail', remediation={})}))
        report = self.run_audit(self.envelope({'WEB-01': self.observed('fail')}))
        task = next(t for t in report['roadmap'] if t['criterion'] == 'WEB-01')
        self.assertEqual(task['kind'], 'improvement')
        self.assertEqual(task['affected_files'], ['index.html'])
        self.assertIn('Change the conflicting heading', task['steps'][0])

    def test_known_design_gap_recommends_skill_or_reuses_existing(self):
        report = self.run_audit(self.envelope({'VIS-01': self.observed('fail')}))
        self.assertTrue(any(t['id'] == 'TOOL-DESIGN' for t in report['tool_recommendations']))
        config = {**self.project, 'available_capabilities': ['visual-design']}
        baseline = self.run_audit(project=config)
        obs = {**self.envelope({'VIS-01': self.observed('fail')}), 'scope_hash': baseline['scope_hash']}
        report = self.run_audit(obs, project=config)
        tool = next(t for t in report['tool_recommendations'] if t['id'] == 'TOOL-DESIGN')
        self.assertEqual(tool['decision'], 'reuse_existing')
        self.assertEqual(tool['installation_status'], 'proposal_not_executed')

    def test_react_skill_only_for_observed_performance_gap_in_react(self):
        obs = self.envelope({'SPEED-02': self.observed('fail')})
        self.assertFalse(any(t['id'] == 'TOOL-REACT' for t in self.run_audit(obs)['tool_recommendations']))
        (self.root / 'package.json').write_text(json.dumps({'dependencies': {'react': 'fixture'}}))
        obs = self.envelope({'SPEED-02': self.observed('fail')})
        self.assertTrue(any(t['id'] == 'TOOL-REACT' for t in self.run_audit(obs)['tool_recommendations']))

    def test_dependency_order_and_cycle_rejection(self):
        low = self.observed('fail')
        high = self.observed('fail')
        high['remediation']['dependencies'] = ['ACT-VIS-01']
        report = self.run_audit(self.envelope({'WEB-01': high, 'VIS-01': low}))
        order = [t['id'] for t in report['roadmap']]
        self.assertLess(order.index('ACT-VIS-01'), order.index('ACT-WEB-01'))
        low['remediation']['dependencies'] = ['ACT-WEB-01']
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            self.run_audit(self.envelope({'WEB-01': high, 'VIS-01': low}))

    def test_local_trace_does_not_prove_field_vitals(self):
        obs = self.envelope({'SPEED-01': self.observed()})
        self.assertEqual(self.finding(self.run_audit(obs), 'SPEED-01')['status'], 'unknown')
        local_fail = self.envelope({'SPEED-01': self.observed('fail')})
        self.assertEqual(self.finding(self.run_audit(local_fail), 'SPEED-01')['status'], 'unknown')
        metrics = {'source': 'Synthetic RUM', 'window': 'fixture', 'percentile': 75,
                   'mobile': {'lcp_ms': 2400, 'inp_ms': 180, 'cls': 0.09},
                   'desktop': {'lcp_ms': 1500, 'inp_ms': 90, 'cls': 0.01}}
        obs = self.envelope({'SPEED-01': self.observed(field_metrics=metrics)})
        self.assertEqual(self.finding(self.run_audit(obs), 'SPEED-01')['status'], 'unknown')
        obs = self.envelope({'SPEED-01': self.observed(field_metrics=metrics, evidence=self.field_evidence())})
        self.assertEqual(self.finding(self.run_audit(obs), 'SPEED-01')['status'], 'pass')

    def test_desktop_viewport_is_not_actual_mobile_keyboard(self):
        self.project = {**self.project, 'features': {**self.project['features'], 'forms': True}}
        with self.assertRaisesRegex(ValueError, 'mobile keyboard'):
            self.run_audit(self.envelope({'RESP-03': self.observed()}))

    def test_server_rendered_php_project_needs_no_react_rules(self):
        (self.root / 'index.html').unlink()
        (self.root / 'composer.json').write_text(json.dumps({'require': {'laravel/framework': 'fixture'}}))
        report = self.run_audit()
        self.assertEqual(report['discovery']['stack_hints'], ['php'])
        self.assertEqual(report['frontend'], '.')

    def test_installed_pwa_provenance_required(self):
        self.project = {**self.project, 'profile': 'pwa', 'features': {**self.project['features'], 'pwa': True}}
        with self.assertRaisesRegex(ValueError, 'Installed PWA'):
            self.run_audit(self.envelope({'PWA-X01': self.observed()}))
        value = self.observed()
        value['runtime'].update(capture_kind='installed-pwa-simulator', display_mode='standalone')
        self.assertEqual(self.finding(self.run_audit(self.envelope({'PWA-X01': value})), 'PWA-X01')['status'], 'pass')

    def test_private_files_and_symlinks_are_excluded_and_evidence_rejected(self):
        (self.root / '.env.local').write_text('synthetic secret')
        (self.root / 'cookies.json').write_text('{}')
        (self.root / 'link.html').symlink_to(self.root / 'index.html')
        report = self.run_audit()
        self.assertFalse({'.env.local', 'cookies.json', 'link.html'} & set(report['inventory']))
        for path in ['../app/index.html', '.env.local', 'cookies.json', 'link.html']:
            value = self.observed(evidence=[{'root': 'target', 'path': path, 'kind': 'source', 'sha256': '0' * 64}])
            with self.assertRaises(ValueError):
                self.run_audit(self.envelope({'GOAL-01': value}))

    def test_truncated_inventory_is_reported(self):
        files, limits = audit.inventory(self.root, limit=0)
        self.assertFalse(files)
        self.assertTrue(limits['truncated'])

    def test_cli_writes_reviewable_plan_without_modifying_target(self):
        out = self.base / 'audit'
        before = audit.digest(self.root / 'index.html')
        script = KIT / 'skills/web-excellence-audit/scripts/audit.py'
        result = subprocess.run([sys.executable, str(script), '--target', str(self.root),
                                 '--profile', 'website', '--out', str(out), '--kit', str(KIT)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(audit.digest(self.root / 'index.html'), before)
        for name in ['summary.md', 'audit.json', 'gap-report.md', 'action-plan.md',
                     'action-plan.json', 'tool-recommendations.json', 'observations.template.json']:
            self.assertTrue((out / name).is_file(), name)
        report = json.loads((out / 'audit.json').read_text())
        self.assertEqual(report['counts']['pass'], 0)
        self.assertTrue(all(t['kind'] == 'investigation' for t in report['roadmap']))

    def test_cli_consumes_external_runtime_evidence_and_preserves_specific_plan(self):
        config = self.base / 'project.json'
        config.write_text(json.dumps(self.project))
        value = self.observed('fail')
        value['observed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        observations = self.base / 'observations.json'
        observations.write_text(json.dumps(self.envelope({'VIS-01': value})))
        out = self.base / 'complete-audit'
        result = subprocess.run([sys.executable, str(KIT / 'skills/web-excellence-audit/scripts/audit.py'),
                                 '--target', str(self.root), '--project', str(config),
                                 '--observations', str(observations), '--evidence-root', str(self.evidence),
                                 '--out', str(out), '--kit', str(KIT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((out / 'audit.json').read_text())
        self.assertEqual(self.finding(report, 'VIS-01')['status'], 'fail')
        plan = json.loads((out / 'action-plan.json').read_text())
        action = next(t for t in plan['items'] if t['criterion'] == 'VIS-01')
        self.assertEqual(action['affected_files'], ['index.html'])
        self.assertEqual(action['evidence'][0]['path'], 'run.txt')
        self.assertTrue(any(t['id'] == 'TOOL-DESIGN' for t in report['tool_recommendations']))

    def test_output_directory_does_not_change_git_bound_source(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        out = self.root / 'audit-output'
        before = self.run_audit(excluded=out)['source_inventory_hash']
        audit.write(self.run_audit(excluded=out), out)
        self.assertEqual(before, self.run_audit(excluded=out)['source_inventory_hash'])

    def test_repeated_report_does_not_erase_edited_observation_template(self):
        out = self.base / 'audit'
        report = self.run_audit()
        audit.write(report, out)
        template = out / 'observations.template.json'
        edited = self.envelope({'WEB-01': self.observed()})
        template.write_text(json.dumps(edited))
        audit.write(report, out)
        self.assertEqual(json.loads(template.read_text()), edited)
        self.assertEqual(json.loads((out / 'observations.next-template.json').read_text())['findings'], {})

    def test_report_refuses_output_symlink_into_target(self):
        out = self.base / 'audit'
        out.mkdir()
        (out / 'audit.json').symlink_to(self.root / 'index.html')
        before = audit.digest(self.root / 'index.html')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            audit.write(self.run_audit(), out)
        self.assertEqual(before, audit.digest(self.root / 'index.html'))

    def test_observation_cannot_waive_or_fake_applicable_criteria(self):
        waived = {'status': 'not_applicable', 'scope': 'n/a', 'reason': 'n/a'}
        with self.assertRaisesRegex(ValueError, 'Applicability'):
            self.run_audit(self.envelope({'WEB-01': waived}))
        source_as_log = self.observed(evidence=[{'root': 'target', 'path': 'index.html', 'kind': 'test-log',
                                                 'sha256': audit.digest(self.root / 'index.html')}])
        with self.assertRaisesRegex(ValueError, 'Runtime artifact'):
            self.run_audit(self.envelope({'WEB-01': source_as_log}))
        invented = self.observed('fail')
        invented['remediation']['affected_files'] = ['src/does/not/Exist.tsx']
        with self.assertRaisesRegex(ValueError, 'Missing evidence'):
            self.run_audit(self.envelope({'WEB-01': invented}))
        with self.assertRaisesRegex(ValueError, 'Unknown project keys: viewport'):
            self.run_audit(project={**self.project, 'viewport': []})

    def test_feature_criterion_cannot_pass_with_empty_matrix(self):
        self.project = {**self.project, 'features': {**self.project['features'], 'async_states': True},
                        'journeys': [{**self.project['journeys'][0], 'features': []}]}
        report = self.run_audit(self.envelope({'FLOW-02': self.observed(coverage=[])}))
        self.assertEqual(self.finding(report, 'FLOW-02')['status'], 'unknown')

    def test_truthful_failures_and_names_are_recordable(self):
        (self.evidence / 'cookie-banner-mobile.txt').write_text('Synthetic log')
        named = self.observed(evidence=[{'root': 'evidence', 'path': 'cookie-banner-mobile.txt', 'kind': 'test-log',
                                         'sha256': audit.digest(self.evidence / 'cookie-banner-mobile.txt')}])
        self.assertEqual(self.finding(self.run_audit(self.envelope({'WEB-01': named})), 'WEB-01')['status'], 'pass')
        dependent = self.observed('fail')
        dependent['remediation']['dependencies'] = ['ACT-VIS-01']
        report = self.run_audit(self.envelope({'WEB-01': dependent, 'VIS-01': self.observed()}))
        self.assertEqual(next(t for t in report['roadmap'] if t['id'] == 'ACT-WEB-01')['dependencies'], [])
        dependent['remediation']['dependencies'] = ['ACT-TYPO-01']
        with self.assertRaisesRegex(ValueError, 'ACT-TYPO-01'):
            self.run_audit(self.envelope({'WEB-01': dependent}))
        self.project = {**self.project, 'profile': 'pwa', 'features': {**self.project['features'], 'pwa': True}}
        not_installable = self.observed('fail')
        not_installable['runtime'].update(display_mode='browser')
        self.assertEqual(self.finding(self.run_audit(self.envelope({'PWA-X01': not_installable})), 'PWA-X01')['status'], 'fail')

    def test_skipped_directories_are_reported(self):
        (self.root / 'src' / 'data').mkdir(parents=True)
        (self.root / 'src' / 'data' / 'routes.js').write_text('export default []')
        self.assertIn('src/data', self.run_audit()['inventory_limits']['skipped_directories'])

    def test_device_bound_and_field_criteria_need_no_invented_cells(self):
        self.project = {**self.project, 'features': {**self.project['features'], 'forms': True},
                        'viewports': [{'width': 1440, 'height': 900}, {'width': 390, 'height': 844}]}
        keyboard = self.observed()
        keyboard['runtime'].update(capture_kind='mobile-simulator')
        self.assertEqual(self.finding(self.run_audit(self.envelope({'RESP-03': keyboard})), 'RESP-03')['status'], 'pass')
        ghost = self.observed(coverage=[{'journey_id': 'GHOST', 'state': 'default', 'viewport': {'width': 390, 'height': 844}}])
        with self.assertRaisesRegex(ValueError, 'Coverage outside'):
            self.run_audit(self.envelope({'WEB-01': ghost}))
        metrics = {'source': 'Synthetic RUM', 'window': 'fixture', 'percentile': 75,
                   'mobile': {'lcp_ms': 2400, 'inp_ms': 180, 'cls': 0.09},
                   'desktop': {'lcp_ms': 1500, 'inp_ms': 90, 'cls': 0.01}}
        field = self.observed(field_metrics=metrics, evidence=self.field_evidence())
        del field['runtime'], field['coverage']
        self.assertEqual(self.finding(self.run_audit(self.envelope({'SPEED-01': field})), 'SPEED-01')['status'], 'pass')

    def test_cheap_fabrications_and_typos_are_rejected(self):
        (self.evidence / 'empty.png').write_bytes(b'')
        empty = self.observed(evidence=[{'root': 'evidence', 'path': 'empty.png', 'kind': 'screenshot', 'sha256': audit.digest(self.evidence / 'empty.png')}])
        with self.assertRaisesRegex(ValueError, 'Empty evidence'):
            self.run_audit(self.envelope({'WEB-01': empty}))
        with self.assertRaisesRegex(ValueError, 'Evidence root'):
            audit.run(self.root, KIT, project=self.project, evidence_root=self.root, now=self.now)
        with self.assertRaisesRegex(ValueError, 'Unknown observation keys'):
            self.run_audit(self.envelope({'WEB-01': self.observed(bogus_key=1)}))
        with self.assertRaisesRegex(ValueError, 'Unknown journey keys'):
            self.run_audit(project={**self.project, 'journeys': [{**self.project['journeys'][0], 'feature': []}]})

    def test_scope_binding_and_source_named_after_secrets(self):
        obs = self.envelope({'WEB-01': self.observed()})
        report = self.run_audit(obs, project={**self.project, 'available_capabilities': ['browser-control']})
        self.assertEqual(self.finding(report, 'WEB-01')['status'], 'pass')
        self.assertIn('No audience configured; judgments lack their reference.', report['limitations'])
        (self.root / 'src' / 'cookies').mkdir(parents=True)
        (self.root / 'src' / 'cookies' / 'cookies.ts').write_text('export {}')
        (self.root / 'sw.js').write_text('// worker')
        report = self.run_audit()
        self.assertIn('src/cookies/cookies.ts', report['inventory'])
        self.assertTrue(any('excluded feature pwa' in x for x in report['limitations']))

    def test_uncommitted_content_and_nested_frontends_are_bound(self):
        def git(*args):
            subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=t', '-c', 'user.email=t@example.invalid', *args],
                           check=True, capture_output=True)
        (self.root / 'logo.svg').write_text('<svg/>')
        git('init', '-q')
        git('add', '-A')
        git('commit', '-q', '-m', 'fixture')
        (self.root / 'logo.svg').write_text('<svg><!-- first edit --></svg>')
        first = self.run_audit()['source_inventory_hash']
        (self.root / 'logo.svg').write_text('<svg><!-- second edit --></svg>')
        self.assertNotEqual(first, self.run_audit()['source_inventory_hash'])
        (self.root / 'package.json').write_text(json.dumps({'devDependencies': {'vite': 'fixture'}}))
        for name, framework in [('web', 'react'), ('admin', 'vue')]:
            (self.root / 'apps' / name).mkdir(parents=True)
            (self.root / 'apps' / name / 'package.json').write_text(json.dumps({'dependencies': {framework: 'fixture'}}))
        with self.assertRaisesRegex(ValueError, 'Multiple frontends'):
            self.run_audit()

    def test_runtime_writes_outside_the_binding_keep_observations(self):
        def git(*args):
            subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=t', '-c', 'user.email=t@example.invalid', *args],
                           check=True, capture_output=True)
        (self.root / 'data').mkdir()
        (self.root / 'data' / 'db.json').write_text('[]')
        (self.root / '.gitignore').write_text('test-results/\n')
        git('init', '-q')
        git('add', '-A')
        git('commit', '-q', '-m', 'fixture')
        obs = self.envelope({'WEB-01': self.observed()})
        (self.root / 'data' / 'db.json').write_text('[{"id": 1}]')
        (self.root / 'test-results').mkdir()
        (self.root / 'test-results' / 'last-run.json').write_text('{}')
        self.assertEqual(self.finding(self.run_audit(obs), 'WEB-01')['status'], 'pass')
        (self.root / 'index.html').write_text('<h1>Changed product</h1>')
        self.assertEqual(self.finding(self.run_audit(obs), 'WEB-01')['status'], 'unknown')
        nested = self.root / 'web'
        nested.mkdir()
        (nested / 'page.html').write_text('<p>first</p>')
        subprocess.run(['git', '-C', str(nested), 'init', '-q'], check=True, capture_output=True)
        first = self.run_audit()
        self.assertIn('web/page.html', first['inventory'])
        (nested / 'page.html').write_text('<p>second</p>')
        self.assertNotEqual(first['source_inventory_hash'], self.run_audit()['source_inventory_hash'])

    def test_pwa_journey_narrowing_and_reviewable_outputs(self):
        self.project = {**self.project, 'profile': 'pwa', 'features': {**self.project['features'], 'pwa': True},
                        'journeys': [{**self.project['journeys'][0], 'features': []}]}
        installed = self.observed()
        installed['runtime'].update(capture_kind='installed-pwa-simulator', display_mode='standalone')
        report = self.run_audit(self.envelope({'PWA-X01': installed, 'WEB-01': self.observed(coverage=[])}))
        self.assertEqual(self.finding(report, 'PWA-X01')['status'], 'pass')
        self.assertIn('1 of 1 cells missing, first J1/390/844', self.finding(report, 'WEB-01')['reason'])
        task = next(t for t in report['roadmap'] if t['id'] == 'ACT-WEB-01')
        self.assertEqual((task['evidence_required'], task['pass_covers']), ('runtime', 'every journey at every viewport'))
        elsewhere = self.observed()
        elsewhere['runtime']['state'] = 'bogus'
        with self.assertRaisesRegex(ValueError, 'configured journey state'):
            self.run_audit(self.envelope({'WEB-01': elsewhere}))
        with self.assertRaisesRegex(ValueError, 'list of known features'):
            self.run_audit(project={**self.project, 'journeys': [{**self.project['journeys'][0], 'features': {'forms': True}}]})

    def test_matrix_shape_and_prerequisite_order(self):
        self.project = {**self.project, 'journeys': [{**self.project['journeys'][0], 'states': ['default', 'error']}]}
        once = self.observed()
        self.assertEqual(self.finding(self.run_audit(self.envelope({'FLOW-01': once})), 'FLOW-01')['status'], 'pass')
        self.assertEqual(self.finding(self.run_audit(self.envelope({'WEB-03': once})), 'WEB-03')['status'], 'unknown')
        with self.assertRaisesRegex(ValueError, 'exactly'):
            self.run_audit(project={**self.project, 'viewports': [{'width': 1440, 'height': 900, 'label': 'desktop'}]})
        blocked = self.observed('fail')
        blocked['remediation']['dependencies'] = ['ACT-SYS-02']
        order = [t['id'] for t in self.run_audit(self.envelope({'FLOW-01': blocked}))['roadmap']]
        self.assertEqual(order.index('ACT-SYS-02') + 1, order.index('ACT-FLOW-01'))
        self.assertLess(order.index('ACT-FLOW-01'), order.index('ACT-VIS-01'))
        self.assertEqual(self.run_audit(max_age_days=30)['release_gate'], 'blocked')

    def test_evidence_type_and_states_must_fit_the_claim(self):
        (self.evidence / 'notes.json').write_text('{}')
        mislabeled = self.observed(evidence=[{'root': 'evidence', 'path': 'notes.json', 'kind': 'screenshot',
                                              'sha256': audit.digest(self.evidence / 'notes.json')}])
        with self.assertRaisesRegex(ValueError, 'contradicts kind'):
            self.run_audit(self.envelope({'WEB-01': mislabeled}))
        elsewhere = self.observed()
        elsewhere['runtime']['viewport'] = {'width': 9999, 'height': 1}
        with self.assertRaisesRegex(ValueError, 'configured viewport'):
            self.run_audit(self.envelope({'WEB-01': elsewhere}))
        typo = self.observed()
        typo['runtime']['displaymode'] = 'standalone'
        with self.assertRaisesRegex(ValueError, 'Unknown runtime keys'):
            self.run_audit(self.envelope({'WEB-01': typo}))
        (self.root / 'src' / 'app' / 'credentials').mkdir(parents=True)
        (self.root / 'src' / 'app' / 'credentials' / 'page.tsx').write_text('export {}')
        self.assertIn('src/app/credentials/page.tsx', self.run_audit()['inventory'])
        self.project = {**self.project, 'features': {**self.project['features'], 'async_states': True}}
        report = self.run_audit(self.envelope({'FLOW-02': self.observed()}))
        self.assertEqual(self.finding(report, 'FLOW-02')['status'], 'unknown')


if __name__ == '__main__':
    unittest.main()
