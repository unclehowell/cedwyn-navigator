#!/usr/bin/env python3
"""Build apps.json for the Cedwyn navigator from the site's own webapp registry.

The navigator must show the SAME "N of 59" as every webapp page, so it never keeps its own numbering.
The numbers come from the same three sources unclehowell/cedwyn tools/site.py uses for /areas.json "nav" (docs/NAV.md):
  1. /areas.json "nav" from the live site (areas with their slot; source themes listed as aliases);
  2. themes.json entries with "slot": N at a cedwyn ref (since nav 1.4.0 such a theme is its own webapp, not an alias);
  3. data/coming-soon.json at that ref (placeholder unclehowell/coming-soon-NN for any slot no webapp takes).
Repositories come from split-repos.json at the same ref (row "page" = the webapp's path). Store/sync status is kept from
the previous apps.json unless --status names a JSON file {"<repo>": {"store": "...", "sync": "..."}}.

Usage: python3 tools/build_apps.py [--ref main] [--site https://bucklerfamily.estate] [--status status.json] [--out apps.json]
Exits 1 (and writes nothing) if the 59 slots are not each taken exactly once.
"""
import json, sys, time, argparse, urllib.request
def get(u):
    r = urllib.request.Request(u, headers={'User-Agent': 'cedwyn-navigator-build'})
    with urllib.request.urlopen(r, timeout=60) as f: return json.loads(f.read().decode('utf-8'))
ap = argparse.ArgumentParser()
ap.add_argument('--ref', default='main'); ap.add_argument('--site', default='https://bucklerfamily.estate')
ap.add_argument('--status'); ap.add_argument('--out', default='apps.json')
a = ap.parse_args()
RAW = 'https://raw.githubusercontent.com/unclehowell/cedwyn/' + a.ref + '/'
areas = get(a.site + '/areas.json?cb=%d' % time.time())
themes = get(RAW + 'themes.json'); themes = themes.get('themes', themes)
if isinstance(themes, dict): themes = [dict(id=k, **v) for k, v in themes.items() if isinstance(v, dict)]
soon = get(RAW + 'data/coming-soon.json')
split = get(RAW + 'split-repos.json')['apps']
of = soon.get('of', 59)
own = {t['id']: t for t in themes if isinstance(t, dict) and isinstance(t.get('slot'), int)}
reg = {}
for n in areas.get('nav', []):
    reg[n['slot']] = dict(slot=n['slot'], id=n['id'], title=n['title'], path=n['path'], href=n.get('href') or n['path'],
                          aliases=[x for x in n.get('aliases', []) if x.strip('/') not in own])
for tid, t in own.items():
    if t['slot'] in reg and reg[t['slot']]['id'] != tid: sys.exit('slot %d claimed by %s and %s' % (t['slot'], reg[t['slot']]['id'], tid))
    reg[t['slot']] = dict(slot=t['slot'], id=tid, title=t.get('title') or tid, path='/%s/' % tid, href='/%s/' % tid, aliases=[])
for s in soon.get('slots', []):
    e = reg.setdefault(s['slot'], dict(slot=s['slot'], id=s['id'], title='Coming soon', path=s['path'], href=s['path'], aliases=[],
                                       repo=s['repo'], kind='coming-soon'))
    # since the 8 Nov build (main 8d4dba1) the live /areas.json nav lists the placeholders itself; keep their repo
    if e['id'] == s['id']: e.update(repo=s['repo'], kind='coming-soon')
if sorted(reg) != list(range(1, of + 1)): sys.exit('slots not 1..%d exactly once: missing %s' % (of, [i for i in range(1, of + 1) if i not in reg]))
prev = {}
try: prev = {x.get('repo'): x for x in json.load(open(a.out)).get('apps', []) + json.load(open(a.out)).get('unregistered', [])}
except Exception: pass
status = json.load(open(a.status)) if a.status else {}
bypage = {}
for r in split: bypage.setdefault(r.get('page'), []).append(r)
def stat(repo):
    s = status.get(repo) or {k: prev.get(repo, {}).get(k) for k in ('store', 'sync')}
    return {k: v for k, v in s.items() if v}
apps, used = [], set()
for i in range(1, of + 1):
    e = reg[i]; c = bypage.get(e['path'], []) or bypage.get(e['href'], [])
    if not c: c = [r for r in split if r['repo'] == 'unclehowell/cedwyn-' + e['id']]
    repo = c[0]['repo'] if c else e.get('repo')
    if c: used.add(repo)
    row = dict(slot=i, id=e['id'], title=e['title'], url=a.site + e['href'], repo=repo,
               kind=e.get('kind') or ('own-repo' if c else 'cedwyn'))
    row.update(stat(repo) if c else {})
    apps.append(row)
unreg = [dict(id=r['repo'].split('/')[-1].replace('cedwyn-', ''), title=r.get('app'), url=a.site + (r.get('page') or '/'),
              repo=r['repo'], kind='own-repo, no slot', **stat(r['repo'])) for r in split if r['repo'] not in used]
m = dict(schema='cedwyn_navigator/v2', updated_utc=time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime()), total=of,
         split=sum(1 for x in apps if x['kind'] == 'own-repo'),
         stores=sum(1 for x in apps if str(x.get('store', '')).startswith('own store')),
         source=dict(registry=a.site + '/areas.json', themes='unclehowell/cedwyn@%s:themes.json' % a.ref,
                     coming_soon='unclehowell/cedwyn@%s:data/coming-soon.json' % a.ref, repos='unclehowell/cedwyn@%s:split-repos.json' % a.ref),
         apps=apps, unregistered=unreg)
open(a.out, 'w').write(json.dumps(m, indent=1, ensure_ascii=False) + '\n')
print('wrote %s: %d slots, %d in own repos, %d with own store, %d repos with no slot' % (a.out, of, m['split'], m['stores'], len(unreg)))
