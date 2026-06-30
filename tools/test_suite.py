#!/usr/bin/env python3
"""QNFO Test Suite v1.1 — redirects deprecated. --quick / --redirects / --handoff-verify / --all"""
import argparse, json, os, ssl, sys, http.client as hc, urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
API = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}'
CTX = ssl._create_unverified_context()

total_tests = total_pass = total_fail = critical_failures = 0

def cf(endpoint):
    req = urllib.request.Request(f'{API}/{endpoint}')
    req.add_header('Authorization', f'Bearer {TOKEN}')
    return json.loads(urllib.request.urlopen(req, timeout=15, context=CTX).read())

def test_result(name, passed, severity='NORMAL'):
    global total_tests, total_pass, total_fail, critical_failures
    total_tests += 1
    if passed: total_pass += 1
    else: total_fail += 1; critical_failures += 1 if severity.upper() == 'CRIT' else 0
    status = 'PASS' if passed else 'FAIL'
    marker = ' [CRIT]' if severity.upper() == 'CRIT' else ''
    print(f'  [{status}]{marker} {name}')
    return passed

def run_quick():
    print('\n## SMOKE TEST')
    if not TOKEN: test_result('CLOUDFLARE_API_TOKEN set', False, 'CRIT'); return
    try:
        resp = cf(''); test_result('API token valid', True, 'CRIT')
    except: test_result('API token valid', False, 'CRIT'); return
    for name, count, endpoint in [
        ('D1', 5, 'd1/database'), ('KV', 1, 'storage/kv/namespaces'),
        ('Pages', 8, 'pages/projects'), ('Queues', 1, 'queues'),
        ('Vectorize', 0, 'vectorize/indexes')]:
        try:
            r = cf(endpoint); actual = len(r.get('result',[]))
            test_result(f'{name}: {actual} (expected {count})', actual >= count, 'NORMAL')
        except: test_result(f'{name} accessible', False, 'NORMAL')

def run_redirects():
    print('\n## HTTP REDIRECT VERIFICATION (deprecated)')
    redirects = [
        ('deep.qwav.tech', 'papers.qnfo.org', 'qwav'),
        ('archive.qnfo.org', 'papers.qnfo.org/archive', 'qnfo-archive'),
        ('adelic.qnfo.org', 'papers.qnfo.org', 'adelic-qft'),
        ('primer.qwav.tech', 'papers.qnfo.org', 'qlof-primer'),
    ]
    for host, expected, name in redirects:
        try:
            conn = hc.HTTPSConnection(host, context=CTX, timeout=15)
            conn.request('GET', '/', headers={'User-Agent': 'QNFO-TestSuite/1.1'})
            resp = conn.getresponse()
            is_redirect = resp.status in (301,302,307,308)
            loc = resp.getheader('Location', 'NONE')
            status_icon = 'PASS' if is_redirect else 'INFO'
            print(f'  [{status_icon}] {name}: {resp.status} -> {loc[:80]}' if is_redirect else f'  [{status_icon}] {name}: HTTP {resp.status} (no redirect — deprecated)')
            test_result(f'{name} redirect', is_redirect and expected in str(loc), 'NORMAL')
        except Exception as e:
            print(f'  [INFO] {name}: {str(e)[:80]}'); test_result(f'{name} redirect', False, 'NORMAL')

def main():
    p = argparse.ArgumentParser(description='QNFO Test Suite v1.1')
    p.add_argument('--quick', action='store_true'); p.add_argument('--redirects', action='store_true')
    p.add_argument('--all', action='store_true')
    args = p.parse_args()
    run_q = args.quick or args.all; run_r = args.redirects or args.all
    if not (run_q or run_r): p.print_help(); return 0
    print('=' * 60); print(f'QNFO TEST SUITE v1.1 — {datetime.now(timezone.utc).isoformat()}')
    print('(redirects deprecated 2026-06-29)'); print('=' * 60)
    if run_q: run_quick()
    if run_r: run_redirects()
    print('\n' + '=' * 60)
    print(f'RESULTS: {total_pass}/{total_tests} passed, {total_fail} failed')
    if critical_failures: print(f'CRITICAL FAILURES: {critical_failures}')
    print('=' * 60)
    if critical_failures > 0: print('\n[BLOCKED]'); return 1
    elif total_fail > 0: print('\n[WARN]'); return 0
    else: print('\n[ALL TESTS PASSED]'); return 0

if __name__ == '__main__': sys.exit(main())
