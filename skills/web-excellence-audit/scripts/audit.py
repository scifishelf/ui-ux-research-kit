#!/usr/bin/env python3
"""Portable inventory, evidence reconciliation and roadmap. Does not run the app."""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
from pathlib import Path

KIT = Path(__file__).resolve().parents[3]
PROFILES = {'website', 'webapp', 'pwa'}
STATUSES = {'pass', 'fail', 'unknown', 'not_applicable'}
FEATURES = {'public_content', 'media', 'async_states', 'forms', 'editable_data',
            'destructive_actions', 'gestures', 'motion', 'pwa', 'service_worker', 'offline'}
SKIP = {'.git', 'node_modules', 'vendor', '.next', '.nuxt', '.svelte-kit', 'dist',
        'build', 'coverage', '__pycache__', '.venv', 'venv', 'storage', 'data',
        '.aws', '.ssh', '.cache', 'worktrees', '.idea'}
EXTENSIONS = {'.html', '.htm', '.css', '.scss', '.sass', '.less', '.js', '.jsx',
              '.ts', '.tsx', '.vue', '.svelte', '.astro', '.php', '.py', '.rb',
              '.md', '.mdx', '.json', '.yaml', '.yml', '.toml', '.webmanifest',
              '.lock', '.txt', '.xml', '.cs', '.cshtml', '.csproj', '.go', '.java',
              '.erb', '.twig', '.hbs', '.jinja', '.jinja2'}
EVIDENCE_KINDS = {'source', 'screenshot', 'video', 'trace', 'test-log', 'accessibility-report', 'user-test', 'field-data'}
FINDING_KEYS = {'status', 'scope', 'reason', 'observed_at', 'evidence', 'runtime', 'coverage', 'remediation', 'field_metrics'}
REMEDIATION_KEYS = {'title', 'steps', 'acceptance', 'affected_files', 'dependencies', 'effort', 'owner_role'}
JOURNEY_KEYS = {'id', 'route', 'task', 'success', 'states', 'features'}
CAPTURE_KINDS = {'desktop-browser', 'mobile-simulator', 'installed-pwa-simulator', 'real-device'}
PROJECT_KEYS = {'schema_version', 'profile', 'frontend', 'audience', 'features', 'viewports',
                'journeys', 'available_capabilities', 'report_language'}
PHASES = {
    'P0': 'Resolve required evidence; protect usability and data integrity',
    'P1': 'Enable core tasks, accessibility and responsive behavior',
    'P2': 'Improve content, structure and speed',
    'P3': 'Refine visual distinction and interaction quality',
    'P4': 'Maintain quality through regression and usability tests',
}


def digest(path):
    result = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            result.update(chunk)
    return result.hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def private_path(path):
    # Secret stores, not source named after them: src/cookies.ts and cookie-banner.png stay citable.
    return any(part.startswith('.env') or part.lower() in {'.aws', '.ssh', 'secrets', 'credentials'}
               or re.fullmatch(r'(credentials|secrets?|cookies?)\.(json|txt|ya?ml|toml|xml|ini|sqlite|db)|.*\.(pem|key|p12)', part, re.I)
               for part in Path(path).parts)


def safe_file(root, rel):
    rel = Path(rel)
    if rel.is_absolute() or '..' in rel.parts or private_path(rel):
        raise ValueError('Unsafe evidence path: ' + str(rel))
    path = root / rel
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Evidence outside root: ' + str(rel))
    if any((root / Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)):
        raise ValueError('Symlink evidence: ' + str(rel))
    if not path.is_file():
        raise ValueError('Missing evidence: ' + str(rel))
    return path


def inventory(root, excluded=None, limit=1200):
    found, capped, omitted = {}, False, set()
    excluded = Path(excluded).resolve() if excluded else None
    for base, dirs, files in os.walk(root, followlinks=False):
        base = Path(base)
        omitted.update((base / d).relative_to(root).as_posix() for d in dirs
                       if d != '.git' and (d in SKIP or private_path(d)))
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not private_path(d)
                         and not (base / d).is_symlink()
                         and not (excluded and (base / d).resolve().is_relative_to(excluded))
                         and len((base / d).relative_to(root).parts) <= 8)
        for name in sorted(files):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if (private_path(rel) or path.is_symlink() or (path.suffix not in EXTENSIONS and name not in {'Gemfile', 'Dockerfile'})
                    or (excluded and path.resolve().is_relative_to(excluded))):
                continue
            if len(found) >= limit:
                capped = True
                break
            found[rel] = {'sha256': digest(path), 'bytes': path.stat().st_size}
        if capped:
            break
    return found, {'max_files': limit, 'max_depth': 8, 'truncated': capped,
                   'skipped_directories': sorted(omitted)[:200],
                   'note': 'Selected text/configuration files; not a complete build or working-tree hash.'}


def discover(root, files, frontend='auto'):
    stacks, candidates, scripts, hints = set(), set(), {}, []
    for rel in files:
        path = root / rel
        name = path.name
        parent = path.parent.relative_to(root).as_posix()
        if name == 'package.json':
            try:
                package = json.loads(path.read_text())
                deps = {**package.get('dependencies', {}), **package.get('devDependencies', {})}
                if not isinstance(deps, dict):
                    continue
            except (ValueError, TypeError, AttributeError):
                continue
            frameworks = {'react': 'react', 'next': 'next', 'vue': 'vue', 'nuxt': 'nuxt',
                          'svelte': 'svelte', '@sveltejs/kit': 'sveltekit', 'astro': 'astro',
                          '@angular/core': 'angular', 'vite': 'vite', 'gatsby': 'gatsby'}
            matches = {v for k, v in frameworks.items() if k in deps}
            stacks.update(matches)
            if matches:
                candidates.add(parent)
            # Names only: commands may contain credentials and must be reviewed before execution.
            if isinstance(package.get('scripts'), dict):
                scripts[rel] = sorted(package['scripts'])
            for dep in deps:
                if 'pwa' in dep.lower() or 'workbox' in dep.lower():
                    hints.append({'feature': 'pwa', 'path': rel, 'reason': 'PWA-related dependency'})
        if name in {'index.html', 'index.htm'} and not any(p in {'tests', 'fixtures', 'examples'} for p in path.relative_to(root).parts):
            candidates.add(parent)
            stacks.add('html')
        if name == 'composer.json':
            stacks.add('php')
            candidates.add(parent)
        if name in {'manage.py', 'pyproject.toml', 'requirements.txt'}:
            stacks.add('python')
        if name == 'Gemfile':
            stacks.add('ruby')
        if path.suffix == '.webmanifest' or name in {'sw.js', 'service-worker.js', 'sw.ts'}:
            hints.append({'feature': 'pwa', 'path': rel, 'reason': 'Manifest/worker file'})
    # index.html beneath an already identified app is a route, not another frontend.
    ordered = sorted(candidates, key=lambda p: (len(Path(p).parts), p))
    roots = []
    for candidate in ordered:
        if not any(Path(candidate).is_relative_to(Path(existing)) for existing in roots):
            roots.append(candidate)
    if frontend == 'auto':
        frontend = roots[0] if len(roots) == 1 else ('.' if not roots else None)
    if frontend is not None:
        if not (root / frontend).resolve().is_relative_to(root) or not (root / frontend).is_dir():
            raise ValueError('Frontend must be a directory inside target')
        # Stack conditions refer to the selected app, not unrelated monorepo packages.
        if frontend != '.':
            selected = {k: v for k, v in files.items() if Path(k).is_relative_to(Path(frontend))}
            scoped = discover(root, selected, '.')
            stacks, scripts, hints = set(scoped['stack_hints']), scoped['script_names'], scoped['feature_hints']
    guess = 'webapp' if stacks.intersection({'react', 'next', 'vue', 'nuxt', 'svelte', 'sveltekit', 'angular'}) else 'website'
    return {'frontend': frontend, 'frontend_candidates': roots, 'stack_hints': sorted(stacks),
            'profile_suggestion': guess, 'script_names': scripts, 'feature_hints': hints,
            'classification': 'Heuristic hints; the agent must verify purpose, features and startup path.'}


def validate_project(project):
    if not isinstance(project, dict):
        raise ValueError('Project config must be an object')
    unknown = set(project) - PROJECT_KEYS
    if unknown:
        raise ValueError('Unknown project keys: ' + ', '.join(sorted(unknown)))
    language = project.get('report_language', 'English')
    if not isinstance(language, str) or not language.strip():
        raise ValueError('report_language must be nonempty text')
    if project.get('schema_version', 1) != 1:
        raise ValueError('Project schema_version must be 1')
    if 'audience' in project and (not isinstance(project['audience'], str) or not project['audience'].strip()):
        raise ValueError('audience must be nonempty text')
    if not isinstance(project.get('features', {}), dict):
        raise ValueError('features must be an object')
    unknown = set(project.get('features', {})) - FEATURES
    if unknown:
        raise ValueError('Unknown features: ' + ', '.join(sorted(unknown)))
    if any(v is not None and type(v) is not bool for v in project.get('features', {}).values()):
        raise ValueError('Features must be true, false or null')
    if not isinstance(project.get('journeys', []), list):
        raise ValueError('journeys must be a list')
    journey_ids = set()
    for journey in project.get('journeys', []):
        if not isinstance(journey, dict) or any(not isinstance(journey.get(k), str) or not journey[k].strip()
                                                for k in ['id', 'route', 'task', 'success']):
            raise ValueError('Journey requires id, route, task, success')
        if set(journey) - JOURNEY_KEYS:
            raise ValueError('Unknown journey keys: ' + ', '.join(sorted(set(journey) - JOURNEY_KEYS)))
        if journey['id'] in journey_ids:
            raise ValueError('Duplicate journey ID: ' + journey['id'])
        journey_ids.add(journey['id'])
        states = journey.get('states', ['default'])
        if not isinstance(states, list) or not states or any(not isinstance(s, str) or not s for s in states):
            raise ValueError('Journey states must contain nonempty text')
        if not set(journey.get('features', [])) <= FEATURES:
            raise ValueError('Unknown journey feature')
    for viewport in project.get('viewports', []):
        if not isinstance(viewport, dict) or any(type(viewport.get(k)) is not int or viewport[k] <= 0 for k in ['width', 'height']):
            raise ValueError('Project viewport requires positive width/height')
    capabilities = project.get('available_capabilities', [])
    if not isinstance(capabilities, list) or any(not isinstance(c, str) for c in capabilities):
        raise ValueError('available_capabilities must be a list of capability IDs')


def timestamp(value):
    try:
        result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        raise ValueError('Invalid timezone-aware timestamp') from None
    if result.tzinfo is None:
        raise ValueError('Timestamp must include timezone')
    return result


def observation(c, item, root, evidence_root, stale_reason, now, max_age_days, project):
    if not isinstance(item, dict):
        raise ValueError('Observation must be an object: ' + c['id'])
    status = item.get('status')
    if status == 'not_applicable':
        raise ValueError('Applicability comes from profile/features in the project config, not observations: ' + c['id'])
    if set(item) - FINDING_KEYS:
        raise ValueError('Unknown observation keys in ' + c['id'] + ': ' + ', '.join(sorted(set(item) - FINDING_KEYS)))
    if not isinstance(status, str) or status not in STATUSES or any(
            not isinstance(item.get(k), str) or not item[k].strip() for k in ['reason', 'scope']):
        raise ValueError('Observation requires status, reason, scope: ' + c['id'])
    evidence = []
    if status in {'pass', 'fail'} and not item.get('evidence'):
        raise ValueError('Evidence required: ' + c['id'])
    for entry in item.get('evidence', []):
        if not isinstance(entry, dict) or not re.fullmatch('[a-f0-9]{64}', str(entry.get('sha256', ''))):
            raise ValueError('Evidence requires SHA-256: ' + c['id'])
        base = entry.get('root', 'target')
        if base not in {'target', 'evidence'} or (base == 'evidence' and evidence_root is None):
            raise ValueError('Invalid/missing evidence root: ' + c['id'])
        if not isinstance(entry.get('path'), str) or not entry['path'] or entry.get('kind') not in EVIDENCE_KINDS:
            raise ValueError('Evidence requires path and a known kind: ' + c['id'])
        path = safe_file(root if base == 'target' else evidence_root, entry['path'])
        if not path.stat().st_size:
            raise ValueError('Empty evidence file: ' + entry['path'])
        actual = digest(path)
        if actual != entry.get('sha256'):
            stale_reason.append('Evidence file changed: ' + entry['path'])
        evidence.append({**entry, 'sha256': actual})
    if status in {'pass', 'fail'}:
        checked = timestamp(item.get('observed_at'))
        age = now - checked
        if age.total_seconds() < -300 or age > dt.timedelta(days=max_age_days):
            stale_reason.append('Observation outside the allowed time window')
        if c['evidence_required'] == 'runtime':
            if not any(e.get('root') == 'evidence' and e['kind'] != 'source' for e in evidence):
                raise ValueError('Runtime artifact under --evidence-root required (source code is insufficient): ' + c['id'])
            runtime = item.get('runtime')
            if c['id'] == 'SPEED-01':
                pass  # aggregated field data has no single browser, viewport or journey cell
            elif not isinstance(runtime, dict) or any(not isinstance(runtime.get(k), str) or not runtime[k].strip() for k in
                    ['url', 'route', 'state', 'browser', 'browser_version', 'build_id', 'capture_kind']):
                raise ValueError('Runtime provenance required: ' + c['id'])
            elif runtime['capture_kind'] not in CAPTURE_KINDS:
                raise ValueError('capture_kind must be one of ' + ', '.join(sorted(CAPTURE_KINDS)) + ': ' + c['id'])
            elif not isinstance(runtime.get('viewport'), dict) or any(
                    type(runtime['viewport'].get(k)) is not int or runtime['viewport'][k] <= 0 for k in ['width', 'height']):
                raise ValueError('Viewport width/height required: ' + c['id'])
            elif status == 'pass' and c['category'] == 'pwa' and (runtime.get('display_mode') not in {'standalone', 'fullscreen'}
                    or runtime['capture_kind'] not in {'real-device', 'installed-pwa-simulator'}):
                raise ValueError('Installed PWA evidence required: ' + c['id'])
            elif status == 'pass' and c['id'] == 'RESP-03' and runtime['capture_kind'] not in {'real-device', 'mobile-simulator', 'installed-pwa-simulator'}:
                raise ValueError('Actual mobile keyboard runtime required: ' + c['id'])
            if c['id'] == 'SPEED-01':
                field = item.get('field_metrics') if isinstance(item.get('field_metrics'), dict) else {}
                if field.get('percentile') != 75 or not field.get('source') or not field.get('window'):
                    stale_reason.append('Field measurements with source, time window and p75 are missing')
                field_complete, field_good = True, True
                for segment in ['mobile', 'desktop']:
                    values = field.get(segment) if isinstance(field.get(segment), dict) else {}
                    for key, maximum in [('lcp_ms', 2500), ('inp_ms', 200), ('cls', 0.1)]:
                        value = values.get(key)
                        if type(value) not in {int, float} or not math.isfinite(value) or value < 0:
                            field_complete = False
                            stale_reason.append('Field value missing: ' + segment + '/' + key)
                        elif value > maximum:
                            field_good = False
                if status == 'pass' and not field_good:
                    stale_reason.append('At least one field target is not met')
                if status == 'fail' and field_complete and field_good:
                    raise ValueError('Field metrics contradict fail: ' + c['id'])
            if status == 'pass' and c['id'] != 'SPEED-01':
                # Device-bound checks cover each journey/state once; their viewport is the device's.
                device = c['id'] == 'RESP-03' or c['category'] == 'pwa'
                expected, known = set(), set()
                viewports = project.get('viewports') or [{'width': 1440, 'height': 900}, {'width': 390, 'height': 844}]
                for journey in project.get('journeys', []):
                    for state in journey.get('states', ['default']):
                        for viewport in viewports:
                            cell = (journey['id'], state) if device else (journey['id'], state, viewport['width'], viewport['height'])
                            known.add(cell)
                            if not (c.get('feature') and 'features' in journey and c['feature'] not in journey['features']):
                                expected.add(cell)
                coverage = item.get('coverage', [])
                if not isinstance(coverage, list) or any(not isinstance(e, dict) or not isinstance(e.get('viewport'), dict) for e in coverage):
                    raise ValueError('coverage must list journey_id/state/viewport objects: ' + c['id'])
                actual_coverage = {(e.get('journey_id'), e.get('state')) if device else
                                   (e.get('journey_id'), e.get('state'), e['viewport'].get('width'), e['viewport'].get('height'))
                                   for e in coverage}
                if actual_coverage - known:
                    raise ValueError('Coverage outside the configured journeys/states/viewports: ' + c['id'])
                if not expected:
                    stale_reason.append('No configured journey covers this criterion')
                if expected - actual_coverage:
                    stale_reason.append('Required journey/state/viewport matrix has not been fully checked')
        if status == 'fail':
            fix = item.get('remediation', {})
            if isinstance(fix, dict) and set(fix) - REMEDIATION_KEYS:
                raise ValueError('Unknown remediation keys in ' + c['id'] + ': ' + ', '.join(sorted(set(fix) - REMEDIATION_KEYS)))
            if not isinstance(fix, dict) or not isinstance(fix.get('title'), str) or not fix['title'].strip() or not fix.get('steps') or not fix.get('acceptance'):
                raise ValueError('Concrete remediation title, steps, acceptance required: ' + c['id'])
            for key in ['steps', 'acceptance', 'affected_files', 'dependencies']:
                values = fix.get(key, [])
                if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                    raise ValueError('Remediation lists must contain text: ' + c['id'])
            for rel in fix.get('affected_files', []):
                safe_file(root, rel)  # invented source locations are rejected
            if fix.get('effort', c['effort']) not in {'S', 'M', 'L'}:
                raise ValueError('Remediation effort must be S/M/L: ' + c['id'])
    return ('unknown' if stale_reason else status), evidence, '; '.join(dict.fromkeys(stale_reason))


def run(target, kit=KIT, frontend='auto', profile='auto', project=None, observations=None,
        evidence_root=None, excluded=None, now=None, max_age_days=7, max_files=1200):
    root, kit = Path(target).resolve(), Path(kit).resolve()
    if not root.is_dir():
        raise ValueError('Target directory missing')
    if max_age_days <= 0:
        raise ValueError('max_age_days must be positive')
    project = project or {}
    validate_project(project)
    files, limits = inventory(root, excluded, max_files)
    discovery = discover(root, files, frontend if frontend != 'auto' else project.get('frontend', 'auto'))
    if discovery['frontend'] is None:
        raise ValueError('Multiple frontends; select --frontend: ' + ', '.join(discovery['frontend_candidates']))
    requested_profile = profile if profile != 'auto' else project.get('profile', 'auto')
    selected = requested_profile
    if selected == 'auto':
        selected = discovery['profile_suggestion']
    if selected not in PROFILES:
        raise ValueError('Unknown profile: ' + str(selected))
    explicit_profile = requested_profile != 'auto'
    features = {k: project.get('features', {}).get(k) for k in FEATURES}
    if features['pwa'] is not None and features['pwa'] != (selected == 'pwa'):
        raise ValueError('features.pwa must agree with selected profile')
    features['pwa'] = selected == 'pwa'
    now = now or dt.datetime.now(dt.timezone.utc)
    identity = {'commit': None, 'git_status_hash': None}
    for key, args in [('commit', ['rev-parse', 'HEAD']), ('git_status_hash', ['status', '--porcelain=v1', '--untracked-files=all'])]:
        try:
            if key == 'git_status_hash':
                args = [*args, '--', '.']
                if excluded and Path(excluded).resolve().is_relative_to(root):
                    args.append(':(exclude)' + Path(excluded).resolve().relative_to(root).as_posix())
            raw = subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL)
            identity[key] = raw.decode().strip() if key == 'commit' else hashlib.sha256(raw).hexdigest()
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
    source_hash = fingerprint({'inventory': files, 'identity': identity})
    scope_hash = fingerprint({'frontend': discovery['frontend'], 'profile': selected, 'project': {k: v for k, v in project.items() if k not in {'report_language', 'available_capabilities', 'schema_version'}}})
    obs, binding_errors = {}, []
    if observations is not None:
        if not isinstance(observations, dict) or observations.get('schema_version') != 1:
            raise ValueError('Use observations.schema.json envelope with schema_version=1')
        if observations.get('target') != str(root):
            raise ValueError('Observation target does not match project')
        if observations.get('source_inventory_hash') != source_hash:
            binding_errors.append('Project inventory or Git working tree changed since observation')
        if observations.get('scope_hash') != scope_hash:
            binding_errors.append('Audit scope changed since observation')
        obs = observations.get('findings', {})
        if not isinstance(obs, dict):
            raise ValueError('findings must be an object keyed by criterion ID')
    if not (kit / 'criteria/product/catalog.yaml').is_file():
        raise ValueError(f'Kit not found at {kit}; pass --kit <kit-root>')
    catalog = json.loads((kit / 'criteria/product/catalog.yaml').read_text())['criteria']
    if set(obs) - {c['id'] for c in catalog}:
        raise ValueError('Unknown criterion: ' + ', '.join(sorted(set(obs) - {c['id'] for c in catalog})))
    evidence_root = Path(evidence_root).resolve() if evidence_root else None
    if evidence_root and (root.is_relative_to(evidence_root) or (evidence_root.is_relative_to(root) and not (
            excluded and evidence_root.is_relative_to(Path(excluded).resolve())))):
        raise ValueError('Evidence root must lie outside the target or inside --out')
    findings = []
    for c in catalog:
        f = {**c, 'status': 'unknown', 'scope': 'not_observed', 'evidence': [],
             'reason': 'No criterion-specific check has been evidenced.', 'observation': None}
        feature = c.get('feature')
        if selected not in c['profiles'] or (feature and features[feature] is False):
            f.update(status='not_applicable', scope='profile', reason=(
                'Criterion belongs to the PWA profile.' if selected not in c['profiles'] else
                'Feature explicitly excluded from the verified project scope: ' + feature))
            if c['id'] in obs:
                raise ValueError('Observation conflicts with applicability: ' + c['id'])
        elif feature and features[feature] is None:
            f['reason'] = 'Check applicability first; feature not confirmed: ' + feature
            if c['id'] in obs:
                raise ValueError('Confirm feature in project config before observing: ' + feature)
        elif c['id'] in obs:
            item = obs[c['id']]
            status, evidence, stale = observation(c, item, root, evidence_root, list(binding_errors), now, max_age_days, project)
            f.update(status=status, scope=item['scope'], evidence=evidence,
                     reason=(stale + '. ' if stale else '') + item['reason'],
                     observation=item if not stale else None)
        findings.append(f)
    counts = {s: sum(f['status'] == s for f in findings) for s in sorted(STATUSES)}
    unresolved = [f['id'] for f in findings if f['level'] == 'MUST' and f['status'] in {'unknown', 'fail'}]
    limitations = ['Inventory does not run the app; UI judgments come only from added observations.',
                   'Evidence applies to its stated scope; partial checks do not establish full WCAG conformance.',
                   'File/metadata validation proves neither screenshot content nor actual task success.']
    if not explicit_profile:
        limitations.append('Profile automatically suggested; the agent must confirm it against product purpose.')
    if not project.get('journeys'):
        limitations.append('No concrete journeys configured; define scope and routes first.')
    if not project.get('audience'):
        limitations.append('No audience configured; judgments lack their reference.')
    if limits['truncated']:
        limitations.append('Inventory is truncated; raise --max-files.')
    if max_age_days != 7:
        limitations.append(f'Observation age limit changed to {max_age_days} days.')
    for hint in discovery['feature_hints']:
        if features[hint['feature']] is False:
            limitations.append(f"Inventory hints at excluded feature {hint['feature']} ({hint['path']}); verify the exclusion.")
    incomplete_scope = not explicit_profile or not project.get('journeys') or not project.get('audience') or limits['truncated']
    report = {'version': (kit / 'VERSION').read_text().strip(), 'generated_utc': now.isoformat(),
              'target': str(root), 'frontend': discovery['frontend'], 'profile': selected,
              'profile_confirmed': explicit_profile, 'report_language': project.get('report_language', 'English'),
              'template_language': 'English', 'project': project, 'features': features,
              **identity, 'source_inventory_hash': source_hash, 'scope_hash': scope_hash,
              'inventory': files, 'inventory_limits': limits, 'discovery': discovery,
              'evidence_root': str(evidence_root) if evidence_root else None, 'max_age_days': max_age_days,
              'findings': findings, 'counts': counts, 'unresolved_must': unresolved,
              'release_gate': 'blocked' if unresolved or incomplete_scope else 'human_review_required',
              'limitations': limitations}
    report['roadmap'] = roadmap(report)
    report['tool_recommendations'] = recommendations(report, kit)
    return report


def roadmap(report):
    tasks = []
    # A prerequisite whose criterion is no longer open needs no action.
    resolved = {'ACT-' + f['id'] for f in report['findings'] if f['status'] not in {'unknown', 'fail'}}
    for f in report['findings']:
        if f['status'] not in {'unknown', 'fail'}:
            continue
        fix = (f.get('observation') or {}).get('remediation', {})
        investigation = f['status'] == 'unknown'
        tasks.append({'id': 'ACT-' + f['id'], 'criterion': f['id'],
                      'kind': 'investigation' if investigation else 'improvement',
                      'priority': 'P0' if investigation and f['level'] == 'MUST' else ('P4' if investigation else f['priority']),
                      'title': 'Investigate: ' + f['requirement'] if investigation else fix['title'],
                      'status_quo': f['reason'], 'scope': f['scope'], 'evidence': f['evidence'],
                      'steps': ([f['test'], 'Record findings per route/state with evidence and actual source locations.']
                                if investigation else fix['steps']),
                      'affected_files': [] if investigation else fix.get('affected_files', []),
                      'acceptance': ['Applicability and status documented with current evidence; any deficiencies planned separately.']
                                    if investigation else fix['acceptance'],
                      'product_target': f['passing'],
                      'effort': 'S (investigation; estimate implementation afterwards)' if investigation else fix.get('effort', f['effort']),
                      'owner_role': 'Audit / QA' if investigation else fix.get('owner_role', 'Design / Frontend'),
                      'dependencies': [] if investigation else [d for d in fix.get('dependencies', []) if d not in resolved],
                      'capabilities': f['capabilities'], 'retest': f['test']})
    ids = {t['id'] for t in tasks}
    for task in tasks:
        for d in task['dependencies']:
            if d not in ids or d == task['id']:
                raise ValueError(f"Unknown/self dependency {d} in {task['id']}")
    # Topological ordering preserves concrete prerequisites before cosmetic improvements.
    catalog_priority = {f['id']: f['priority'] for f in report['findings']}
    ordered, pending = [], sorted(tasks, key=lambda t: (t['priority'], t['kind'] == 'investigation',
                                                        catalog_priority[t['criterion']], t['criterion']))
    while pending:
        ready = next((t for t in pending if set(t['dependencies']) <= {o['id'] for o in ordered}), None)
        if ready is None:
            raise ValueError('Cyclic roadmap dependencies')
        ordered.append(ready)
        pending.remove(ready)
    return ordered


def recommendations(report, kit):
    registry = json.loads((kit / 'reference/audit-tools.yaml').read_text())['tools']
    available = set(report['project'].get('available_capabilities', []))
    supported = {tool['capability'] for tool in registry}
    if available - supported:
        raise ValueError('Unknown available capability: ' + ', '.join(sorted(available - supported)))
    needed = {}
    for task in report['roadmap']:
        for capability in task['capabilities']:
            needed.setdefault(capability, []).append(task['id'])
    result = []
    for tool in registry:
        capability = tool['capability']
        if capability not in needed:
            continue
        if tool['kind'] == 'Agent skill':
            triggered = [task['id'] for task in report['roadmap']
                         if task['kind'] == 'improvement' and capability in task['capabilities']]
            if not triggered:
                continue
        else:
            triggered = needed[capability]
        if tool.get('stack') and not set(tool['stack']).intersection(report['discovery']['stack_hints']):
            continue
        decision = 'reuse_existing' if capability in available else (
            'use_existing_or_verify_candidate' if not tool.get('installation_example') else 'check_existing_then_trial')
        result.append({**tool, 'decision': decision, 'addresses': triggered,
                       'installation_status': 'proposal_not_executed',
                       'note': 'Capability documented; no measured quality gain or tool winner claimed.'})
    # Stack-specific React optimization is an optional support for measured performance work.
    if set(report['discovery']['stack_hints']).intersection({'react', 'next'}):
        react = next(t for t in registry if t['id'] == 'TOOL-REACT')
        triggers = [t['id'] for t in report['roadmap'] if t['criterion'].startswith('SPEED-') and t['kind'] == 'improvement']
        if triggers:
            result.append({**react, 'decision': 'reuse_existing' if react['capability'] in available else 'check_existing_then_trial',
                           'addresses': triggers, 'installation_status': 'proposal_not_executed',
                           'note': 'Use only after measurement and with a matching React/Next stack.'})
    return result


def md(value):
    return str(value).replace('|', '/').replace('\n', ' ')


def write(report, out):
    out = Path(out).resolve()
    if Path(report['target']).resolve().is_relative_to(out):
        raise ValueError('Output must not equal or contain target')
    out.mkdir(parents=True, exist_ok=True)
    for name in ['audit.json', 'action-plan.json', 'tool-recommendations.json',
                 'observations.template.json', 'observations.next-template.json',
                 'summary.md', 'gap-report.md', 'action-plan.md']:
        if (out / name).is_symlink():
            raise ValueError('Output file must not be a symlink: ' + name)
    def save(name, value):
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    save('audit.json', report)
    save('action-plan.json', {'version': report['version'], 'target': report['target'],
         'source_inventory_hash': report['source_inventory_hash'], 'scope_hash': report['scope_hash'],
         'report_language': report['report_language'], 'items': report['roadmap']})
    save('tool-recommendations.json', {'items': report['tool_recommendations']})
    template_name = 'observations.template.json'
    index = 0
    while (out / template_name).exists():
        existing = out / template_name
        preserve = True
        try:
            preserve = bool(json.loads(existing.read_text()).get('findings'))
        except (ValueError, AttributeError):
            pass
        if not preserve:
            break
        index += 1
        template_name = 'observations.next-template.json' if index == 1 else f'observations.next-{index}-template.json'
        if (out / template_name).is_symlink():
            raise ValueError('Output template must not be a symlink')
    save(template_name, {'schema_version': 1, 'target': report['target'],
         'source_inventory_hash': report['source_inventory_hash'], 'scope_hash': report['scope_hash'], 'findings': {}})
    summary = ['# Web excellence audit', '',
               f"Requested report language: {report['report_language']}. English checker templates; the agent authors/translates final prose.", '',
               f"Target: `{report['target']}` · Frontend: `{report['frontend']}` · Profile: **{report['profile']}**", '',
               f"Commit: `{report['commit']}` · Profile confirmed: `{report['profile_confirmed']}`", '',
               f"Status: `{report['counts']}` · Acceptance: **{report['release_gate']}**", '',
               '## Limitations', '', *['- ' + x for x in report['limitations']], '',
               '## Address first', '']
    for task in report['roadmap'][:5]:
        summary.append(f"- **{task['id']} ({task['priority']})**: {task['title']}")
    summary += ['', 'Order prioritizes evidence and blockers, then core flows, structure, visual quality and regression.',
                'Excellence also needs user/design review within the defined scope; an average score does not replace acceptance.']
    (out / 'summary.md').write_text('\n'.join(summary) + '\n')
    gap = ['# Product audit — current state', '', '| ID | Level | Status | Observation / scope |', '| --- | --- | --- | --- |']
    for f in report['findings']:
        gap.append(f"| {f['id']} | {f['level']} | {f['status']} | {md(f['reason'])} [{md(f['scope'])}] |")
    (out / 'gap-report.md').write_text('\n'.join(gap) + '\n')
    plan = ['# Action plan from current state to excellence', '',
            f"Target: `{report['target']}` · Profile: `{report['profile']}`", '',
            'Effort is provisional: S up to one day, M two to five days, L more than five days.',
            'Investigations resolve open criteria. Improvements address observed deficiencies.', '',
            '## Concrete audit scope', '', f"Audience: {report['project'].get('audience', 'to be determined')}", '']
    for j in report['project'].get('journeys', []):
        plan += [f"- **{j['id']}** `{j['route']}`: {j['task']} → {j['success']}"]
    plan += ['', '## Milestones', '']
    for p, title in PHASES.items():
        plan.append(f'- **{p} — {title}**')
    plan += ['', 'Dependencies determine execution order. Retest the same flow after each implementation.', '']
    for index, task in enumerate(report['roadmap'], 1):
        plan += [f"## {index}. {task['id']} — {task['title']}", '',
                 f"**Kind:** {task['kind']} · **Priority:** {task['priority']} · **Effort:** {task['effort']} · **Role:** {task['owner_role']}", '',
                 '**Status quo:** ' + task['status_quo'], '', '**Scope:** ' + task['scope'], '', '**Evidence:**', '']
        plan.extend(f"- `{e.get('root', 'target')}:{e['path']}` · SHA-256 `{e['sha256']}` · {e.get('locator', 'Location within evidence')}" for e in task['evidence'])
        if not task['evidence']:
            plan.append('- To be collected.')
        plan += ['', '**Steps:**', '']
        plan.extend(f'{i}. {step}' for i, step in enumerate(task['steps'], 1))
        plan += ['', '**Affected files:** ' + (', '.join(task['affected_files']) or 'Determine during investigation; no source location invented.'), '',
                 '**Dependencies:** ' + (', '.join(task['dependencies']) or 'none'), '', '**Acceptance:**', '']
        plan.extend('- ' + a for a in task['acceptance'])
        plan += ['', '**Quality target:** ' + task['product_target'], '', '**Re-Test:** ' + task['retest'], '']
    plan += ['## Capabilities and skill recommendations', '',
             'Reuse existing capabilities first. Installation examples are proposals for the target project and have not been executed.', '']
    for tool in report['tool_recommendations']:
        plan += [f"### {tool['name']}", '', f"**Decision:** {tool['decision']} · **Kind:** {tool['kind']}", '',
                 '**For actions:** ' + ', '.join(tool['addresses']), '', tool['reason'], '',
                 f"Source: [{tool['name']}]({tool['source']})", '', '**Before adoption:** ' + tool['verification'], '']
        if tool.get('installation_example') and tool['decision'] != 'reuse_existing':
            plan += ['```sh', tool['installation_example'], '```', '',
                     'Select a reviewed source commit and CLI/package version before execution; a main-branch example is not a reviewed pin.', '']
    (out / 'action-plan.md').write_text('\n'.join(plan) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    parser.add_argument('--frontend', default='auto')
    parser.add_argument('--profile', choices=['auto', *sorted(PROFILES)], default='auto')
    parser.add_argument('--out', required=True)
    parser.add_argument('--kit', default=str(KIT))
    parser.add_argument('--project')
    parser.add_argument('--observations')
    parser.add_argument('--evidence-root')
    parser.add_argument('--max-age-days', type=int, default=7)
    parser.add_argument('--max-files', type=int, default=1200, help='inventory cap; a truncated inventory blocks acceptance')
    args = parser.parse_args()
    try:
        project = json.loads(Path(args.project).read_text()) if args.project else None
        obs = json.loads(Path(args.observations).read_text()) if args.observations else None
        out = Path(args.out).resolve()
        target = Path(args.target).resolve()
        if target.is_relative_to(out):
            raise ValueError('Output must not equal or contain target')
        report = run(target, args.kit, args.frontend, args.profile, project, obs,
                     args.evidence_root, out, max_age_days=args.max_age_days, max_files=args.max_files)
        write(report, out)
        print(json.dumps({'profile': report['profile'], 'counts': report['counts'],
                          'release_gate': report['release_gate'], 'out': str(out)}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
