#!/usr/bin/env python3
"""Check the handoff without dependencies, provider access or application claims."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime as dt
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md', 'README.es.md', 'AGENTS.md', 'IMPLEMENTATION.md',
            'design.md', 'LICENSE', 'docs/ai-team/state.md', 'docs/backlog.md',
            'docs/security-model.md', 'docs/testing.md', 'contracts/events.md',
            'contracts/event.schema.json', 'contracts/config.schema.json',
            'examples/demo-events.ndjson', 'examples/workspace.example.json']
LINK = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
BAD_UNICODE = re.compile('[\u00ad\u200b-\u200f\u202a-\u202e\u2060-\u2069\ufeff]')
TRANSITIONS = {
    None: {'queued'}, 'queued': {'running', 'cancelled', 'failed'},
    'running': {'waiting_approval', 'succeeded', 'failed', 'cancel_requested'},
    'waiting_approval': {'running', 'failed', 'cancel_requested'},
    'cancel_requested': {'cancelled', 'succeeded', 'failed'},
    'succeeded': set(), 'failed': set(), 'cancelled': set(),
}

def ensure(condition, message):
    if not condition:
        raise ValueError(message)

def check_docs():
    for name in REQUIRED:
        ensure((ROOT/name).is_file(), f'Missing {name}')
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text()
        ensure(not BAD_UNICODE.search(text), f'Invisible Unicode in {path.relative_to(ROOT)}')
        # Markdown paths outside fenced snippets only.
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in LINK.findall(text):
            parsed = urlsplit(target.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = (path.parent/unquote(parsed.path)).resolve()
            ensure(dest.is_relative_to(ROOT) and dest.exists(),
                   f'Broken/local-external link in {path.relative_to(ROOT)}: {target}')
    for path in (ROOT/'contracts').glob('*.json'):
        schema = json.loads(path.read_text())
        ensure(schema.get('$schema') == 'https://json-schema.org/draft/2020-12/schema', 'Missing schema dialect')
        def refs(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == '$ref' and not item.startswith('#'):
                        ensure((path.parent/item.split('#')[0]).is_file(), f'Missing schema ref {item}')
                    refs(item)
            elif isinstance(value, list):
                for item in value:
                    refs(item)
        refs(schema)

def check_fixture():
    config = json.loads((ROOT/'examples/workspace.example.json').read_text())
    ensure(config['schemaVersion'] == '1.0' and config['workspace']['mode'] == 'demo', 'Example must be a versioned demo')
    ensure(config['workspace']['budgetUsd'] == 0, 'Demo cannot spend')
    projects = {p['id'] for p in config['projects']}
    agents = {a['id']: a for a in config['agents']}
    connections = {c['id']: c for c in config['connections']}
    runtimes = {r['id']: r for r in config['runtimes']}
    ensure(all(not c['enabled'] or c['adapter'] == 'mock' for c in connections.values()), 'Real example connections must be disabled')
    ensure(all(not r['enabled'] or r['adapter'] == 'mock' for r in runtimes.values()), 'Real example runtimes must be disabled')
    for a in agents.values():
        ensure(a['projectId'] in projects and a['runtimeRef'] in runtimes and a['connectionRef'] in connections, 'Dangling agent refs')
        ensure(a['policy'] == {'tools': [], 'network': 'deny', 'maxCostUsd': 0}, 'Demo policies must deny real tools/network/spending')
    schema = json.loads((ROOT/'contracts/event.schema.json').read_text())
    events = [json.loads(line) for line in (ROOT/'examples/demo-events.ndjson').read_text().splitlines() if line.strip()]
    seen = set()
    states = {}
    approval_ids = {}
    artifacts = set()
    for sequence, e in enumerate(events, 1):
        ensure(set(schema['required']) <= e.keys(), 'Missing envelope fields')
        ensure(e['schemaVersion'] == '1.0' and e['mode'] == 'demo', 'Non-demo/unknown event')
        ensure(e['workspaceId'] == config['workspace']['id'] and e['projectId'] in projects, 'Invalid event scope')
        ensure(e['sequence'] == sequence and e['eventId'] not in seen, 'Duplicate event or sequence gap')
        ensure(e['type'] in schema['properties']['type']['enum'], 'Unknown event type')
        seen.add(e['eventId'])
        for key in ['occurredAt', 'observedAt']:
            ensure(dt.datetime.fromisoformat(e[key].replace('Z', '+00:00')).utcoffset() == dt.timedelta(0), 'UTC timestamp required')
        if 'agentId' in e:
            ensure(e['agentId'] in agents, 'Unknown worker')
        data = e['data']
        if e['type'] == 'attempt.state.changed':
            ensure(all(k in e for k in ['taskId', 'attemptId', 'agentId']), 'Attempt refs missing')
            attempt = e['attemptId']
            ensure(data['state'] in TRANSITIONS[states.get(attempt)], f'Illegal transition {attempt}')
            ensure(data['state'] != 'failed' or data.get('reason'), 'Failed attempts need a reason')
            states[attempt] = data['state']
        elif e['type'] == 'approval.requested':
            ensure(states.get(e['attemptId']) == 'waiting_approval', 'Approval outside waiting attempt')
            ensure(re.fullmatch('[a-f0-9]{64}', data['actionHash']), 'Invalid action hash')
            ensure(data['approvalId'] not in approval_ids, 'Duplicate approval')
            approval_ids[data['approvalId']] = (e['attemptId'], None)
        elif e['type'] == 'approval.resolved':
            ensure(data['decision'] in {'approved', 'rejected', 'expired'}, 'Invalid decision')
            ensure(approval_ids.get(data['approvalId']) == (e['attemptId'], None), 'Approval must resolve exactly once for the same attempt')
            approval_ids[data['approvalId']] = (e['attemptId'], data['decision'])
        elif e['type'] == 'artifact.created':
            ensure(data['ref'].startswith('demo://') and re.fullmatch('[a-f0-9]{64}', data['sha256']), 'Synthetic artifact ref/hash required')
            artifacts.add(data['artifactId'])
        elif e['type'] == 'task.verification.changed':
            ensure(data['status'] in {'not_run', 'passed', 'failed', 'unknown'}, 'Invalid verification')
            ensure(data['status'] not in {'passed', 'failed'} or bool(data['evidenceRefs']), 'Verification needs evidence')
    ensure(set(states.values()) == {'succeeded', 'failed'} and artifacts, 'Expected completed and rejected demo outcomes missing')
    return len(events)

if __name__ == '__main__':
    try:
        check_docs()
        count = check_fixture()
        print(f'OK: documentation links, schema files, configuration and {count} synthetic events.')
        print('Specification checks only; no full JSON Schema validation, app execution or provider acceptance.')
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
