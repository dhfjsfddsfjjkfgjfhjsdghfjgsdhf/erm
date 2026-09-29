"""One-off: recover each story map's base (sample tiles + the sample decor the builder kept) from a built map.

The builders start every map from an RPG Maker MZ sample map. Those samples are not part of the workspace
backup, so this script takes the last built maps (orig/frozen_out/data/MapNNN.json), strips the events the
builder added and checks that rebuilding from that base reproduces the built map exactly. The verified bases
are written to story/base/MapNNN.json (named by story map id); common.MapBuild loads them when the sample
folder is missing.
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from story import common
from story.common import MapBuild

FROZEN = common.ROOT + '/orig/frozen_out/data'
BASE = common.ROOT + '/story/base'
os.makedirs(BASE, exist_ok=True)

frozen = {}
for f in os.listdir(FROZEN):
    if f.startswith('Map') and f[3:6].isdigit():
        frozen[int(f[3:6])] = json.load(open(f'{FROZEN}/{f}', encoding='utf-8'))

K = {}                 # map id -> number of leading events that came from the sample
current = {'id': None}

def decor_prefix(m):
    n = 0
    for e in m['events'][1:]:
        if e and MapBuild._is_decor(e):
            n += 1
        else:
            break
    return n

def base_of(mid, k):
    m = copy.deepcopy(frozen[mid])
    m['events'] = m['events'][:1 + k]
    return m

_orig_init = MapBuild.__init__
def patched_init(self, map_id, name, sample, *a, **kw):
    current['id'] = map_id
    if isinstance(sample, int):
        sample = base_of(map_id, K.setdefault(map_id, decor_prefix(frozen[map_id])))
    _orig_init(self, map_id, name, sample, *a, **kw)
    self.sample = sample if not isinstance(sample, dict) else self.sample
MapBuild.__init__ = patched_init

def build_all():
    import importlib
    MapBuild.registry.clear()
    for name in ['story.common', 'story.db', 'story.prologue', 'story.ch1', 'story.ch2', 'story.ch3', 'story.act2',
                 'story.ch4']:
        pass
    from story import db, prologue, ch1, ch2, ch3, act2, ch4
    db.build_states(); db.build_skills(); db.build_items(); db.build_weapons(); db.build_armors()
    db.build_classes(); db.build_actors(); db.build_enemies(); db.build_troops(); db.build_common_events()
    return prologue.build() + ch1.build() + ch2.build() + ch3.build() + act2.build() + ch4.build()

def norm(m):
    return json.loads(common.dumps(m))

for attempt in range(12):
    maps = build_all()
    bad = []
    for mb in maps:
        if norm(mb.m) != frozen[mb.id]:
            bad.append(mb)
    print('attempt', attempt, 'mismatches:', [m.id for m in bad])
    if not bad:
        break
    for mb in bad:
        a, b = norm(mb.m), frozen[mb.id]
        if a['data'] != b['data']:
            print('  map', mb.id, 'tile data differs')
        if len(a['events']) != len(b['events']):
            print('  map', mb.id, 'events', len(a['events']), 'vs', len(b['events']), 'K', K[mb.id])
            # too many decor kept -> fewer; too few -> more
            K[mb.id] += -1 if len(a['events']) > len(b['events']) else 1
        else:
            for k in a:
                if a[k] != b[k]:
                    print('  map', mb.id, 'field', k, 'differs')
            for i, (ea, eb) in enumerate(zip(a['events'], b['events'])):
                if ea != eb:
                    print('   event', i, (ea or {}).get('name'), (eb or {}).get('name'))
                    break

for mb in maps:
    json.dump(base_of(mb.id, K[mb.id]), open(f'{BASE}/Map{mb.id:03d}.json', 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
print('bases written:', len(maps), {m: K[m] for m in sorted(K)})
