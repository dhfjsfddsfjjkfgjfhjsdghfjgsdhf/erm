"""Static checks of the built project (story/out) without the engine: every reference an event command, page or
database entry makes (maps, events, troops, common events, items, actors, switches, plugins and their commands,
images, animations, states) must resolve, and every switch a condition reads must be set somewhere.
usage: python3 tools/check_story.py [--rtp /path/to/RTP/img]"""
import json, os, re, sys, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get('STORY_OUT', ROOT + '/story/out')
RTP = '/opt/rmmz/img'
if '--rtp' in sys.argv:
    RTP = sys.argv[sys.argv.index('--rtp') + 1]
sys.path.insert(0, ROOT + '/tools')
from story import audio

D = {}
for n in ['Actors', 'Classes', 'Skills', 'Items', 'Weapons', 'Armors', 'Enemies', 'Troops', 'States', 'Animations',
          'Tilesets', 'CommonEvents', 'System', 'MapInfos']:
    D[n] = json.load(open(f'{OUT}/data/{n}.json', encoding='utf-8'))
MAPS = {}
for info in D['MapInfos']:
    if info:
        MAPS[info['id']] = json.load(open(f"{OUT}/data/Map{info['id']:03d}.json", encoding='utf-8'))

problems = []
notes = []
def bad(where, msg):
    problems.append(f'{where}: {msg}')

def exists(kind, name):
    if not name:
        return True
    for base in (OUT + '/img', RTP):
        if os.path.exists(f'{base}/{kind}/{name}.png'):
            return True
    return False

def valid(table, i):
    return isinstance(i, int) and 0 < i < len(D[table]) and D[table][i] is not None and D[table][i].get('name', '') != ''

# ---------------------------------------------------------------- plugins and their commands
plugins_js = open(OUT + '/js/plugins.js', encoding='utf-8').read()
ON = {m.group(1) for m in re.finditer(r'"name":"([^"]+)","status":true', plugins_js)}
COMMANDS = collections.defaultdict(set)
for f in glob.glob(OUT + '/js/plugins/*.js'):
    name = os.path.basename(f)[:-3]
    src = open(f, encoding='utf-8').read()
    for m in re.finditer(r'@command\s+(\S+)', src):
        COMMANDS[name].add(m.group(1))
    for m in re.finditer(r'registerCommand\(\s*[^,]+,\s*"([^"]+)"', src):
        COMMANDS[name].add(m.group(1))

# ---------------------------------------------------------------- switches: who sets, who reads
sets = collections.defaultdict(list)
reads = collections.defaultdict(list)
self_sets = set()        # (map, event, letter)
self_reads = []
created_quests = set()
quest_refs = []
text_lines = 0

def scan_list(where, lst, map_id=None, event_id=None):
    global text_lines
    for c in lst:
        code, p = c['code'], c['parameters']
        if code == 201 and p[0] == 0:
            if p[1] not in MAPS:
                bad(where, f'transfer to missing map {p[1]}')
            else:
                m = MAPS[p[1]]
                if not (0 <= p[2] < m['width'] and 0 <= p[3] < m['height']):
                    bad(where, f'transfer to {p[1]} ({p[2]},{p[3]}) outside the map')
        elif code == 301 and p[0] == 0:
            if not valid('Troops', p[1]) or not D['Troops'][p[1]]['members']:
                bad(where, f'battle with missing/empty troop {p[1]}')
        elif code == 117:
            if not valid('CommonEvents', p[0]):
                bad(where, f'common event {p[0]} missing')
        elif code == 121:
            if p[2] == 0:
                for s in range(p[0], p[1] + 1):
                    sets[s].append(where)
        elif code == 123 and map_id:
            self_sets.add((map_id, event_id, p[0]))
        elif code == 111:
            if p[0] == 0:
                reads[p[1]].append(where)
            elif p[0] == 2 and map_id:
                self_reads.append((where, map_id, event_id, p[1]))
            elif p[0] == 8 and not valid('Items', p[1]):
                bad(where, f'condition on missing item {p[1]}')
            elif p[0] == 9 and not valid('Weapons', p[1]):
                bad(where, f'condition on missing weapon {p[1]}')
            elif p[0] == 10 and not valid('Armors', p[1]):
                bad(where, f'condition on missing armor {p[1]}')
            elif p[0] == 4 and not valid('Actors', p[1]):
                bad(where, f'condition on missing actor {p[1]}')
        elif code == 126 and p[2] == 0 and not valid('Items', p[0]):
            bad(where, f'missing item {p[0]}')
        elif code == 127 and p[2] == 0 and not valid('Weapons', p[0]):
            bad(where, f'missing weapon {p[0]}')
        elif code == 128 and p[2] == 0 and not valid('Armors', p[0]):
            bad(where, f'missing armor {p[0]}')
        elif code == 129 and not valid('Actors', p[0]):
            bad(where, f'missing actor {p[0]}')
        elif code in (302, 605):
            table = ['Items', 'Weapons', 'Armors'][p[0]]
            if not valid(table, p[1]):
                bad(where, f'shop sells missing {table[:-1].lower()} {p[1]}')
            elif p[2] == 0 and D[table][p[1]]['price'] == 0:
                bad(where, f'shop sells {D[table][p[1]]["name"]} at its database price 0 (free)')
        elif code == 101:
            if not exists('faces', p[0]):
                bad(where, f'face "{p[0]}" missing')
        elif code == 401:
            text_lines += 1
        elif code == 231:
            if not exists('pictures', p[1]):
                bad(where, f'picture "{p[1]}" missing')
        elif code == 205:
            for mc in p[1]['list']:
                if mc['code'] == 41 and not exists('characters', mc['parameters'][0]):
                    bad(where, f'route image "{mc["parameters"][0]}" missing')
                if mc['code'] == 44 and mc['parameters'][0]['name'] not in audio.SE:
                    bad(where, f'route SE "{mc["parameters"][0]["name"]}" unknown')
        elif code in (241, 245, 249, 250):
            kind = {241: 'bgm', 245: 'bgs', 249: 'me', 250: 'se'}[code]
            name = p[0]['name']
            if name and name not in audio.KINDS[kind]:
                bad(where, f'{kind} "{name}" unknown')
        elif code == 283:
            for i, sub in ((0, 'battlebacks1'), (1, 'battlebacks2')):
                if not exists(sub, p[i]):
                    bad(where, f'battleback "{p[i]}" missing')
        elif code == 212 or code == 337:
            anim = p[1]
            if not (0 < anim < len(D['Animations']) and D['Animations'][anim]):
                bad(where, f'animation {anim} missing')
        elif code == 357:
            plugin, cmd = p[0], p[1]
            if plugin not in ON:
                bad(where, f'plugin command for disabled/missing plugin {plugin}')
            elif cmd not in COMMANDS[plugin]:
                bad(where, f'{plugin} has no command "{cmd}"')
            args = p[3] if len(p) > 3 else {}
            if plugin == 'WD_Quest' and cmd == 'newCreateQuest':
                created_quests.add(int(args['id']))
            elif plugin == 'WD_Quest':
                quest_refs.append((where, int(args.get('questID', 0))))
            if plugin == 'Story_Core' and cmd == 'SetRestPoint':
                mid, x, y = int(args['mapId']), int(args['x']), int(args['y'])
                if mid and mid not in MAPS:
                    bad(where, f'rest point on missing map {mid}')

def scan_page_conditions(where, c, map_id=None, event_id=None):
    for k in ('switch1', 'switch2'):
        if c.get(k + 'Valid'):
            reads[c[k + 'Id']].append(where)
    if c.get('itemValid') and not valid('Items', c['itemId']):
        bad(where, f'page condition on missing item {c["itemId"]}')
    if c.get('actorValid') and not valid('Actors', c['actorId']):
        bad(where, f'page condition on missing actor {c["actorId"]}')
    if c.get('selfSwitchValid') and map_id:
        self_reads.append((where, map_id, event_id, c['selfSwitchCh']))

for mid, m in MAPS.items():
    name = D['MapInfos'][mid]['name']
    if not valid('Tilesets', m['tilesetId']):
        bad(f'map {mid}', f'tileset {m["tilesetId"]} missing')
    for enc in m.get('encounterList', []):
        if not valid('Troops', enc['troopId']):
            bad(f'map {mid} {name}', f'encounter troop {enc["troopId"]} missing')
    for bb, sub in (('battleback1Name', 'battlebacks1'), ('battleback2Name', 'battlebacks2')):
        if m.get('specifyBattleback') and not exists(sub, m[bb]):
            bad(f'map {mid} {name}', f'battleback "{m[bb]}" missing')
    for e in m['events'][1:]:
        if not e:
            continue
        for pi, pg in enumerate(e['pages']):
            where = f'map {mid} {name} / {e["name"]} ({e["x"]},{e["y"]}) p{pi + 1}'
            if not exists('characters', pg['image']['characterName']):
                bad(where, f'sprite "{pg["image"]["characterName"]}" missing')
            scan_page_conditions(where, pg['conditions'], mid, e['id'])
            scan_list(where, pg['list'], mid, e['id'])
for ce in D['CommonEvents'][1:]:
    if ce and ce['list']:
        where = f'common event {ce["id"]} {ce["name"]}'
        if ce['trigger'] in (1, 2):
            reads[ce['switchId']].append(where)
        scan_list(where, ce['list'])
for tr in D['Troops'][1:]:
    if not tr:
        continue
    for m in tr['members']:
        if not valid('Enemies', m['enemyId']):
            bad(f'troop {tr["id"]} {tr["name"]}', f'member enemy {m["enemyId"]} missing')
    for pi, pg in enumerate(tr['pages']):
        where = f'troop {tr["id"]} {tr["name"]} p{pi + 1}'
        if pg['conditions'].get('switchValid'):
            reads[pg['conditions']['switchId']].append(where)
        scan_list(where, pg['list'])

# ---------------------------------------------------------------- database cross references
for a in D['Actors'][1:]:
    if not a or not a['name']:
        continue
    if not valid('Classes', a['classId']):
        bad(f'actor {a["name"]}', f'class {a["classId"]} missing')
    for kind, name in (('faces', a['faceName']), ('characters', a['characterName'])):
        if not exists(kind, name):
            bad(f'actor {a["name"]}', f'{kind} "{name}" missing')
    for slot, i in enumerate(a['equips']):
        if i:
            table = 'Weapons' if slot == 0 else 'Armors'
            if not valid(table, i):
                bad(f'actor {a["name"]}', f'starting equipment {table[:-1].lower()} {i} missing')
for c in D['Classes'][1:]:
    if not c or not c['name']:
        continue
    for l in c['learnings']:
        if not valid('Skills', l['skillId']):
            bad(f'class {c["name"]}', f'learns missing skill {l["skillId"]}')
for en in D['Enemies'][1:]:
    if not en or not en['name']:
        continue
    if not exists('enemies', en['battlerName']):
        bad(f'enemy {en["id"]} {en["name"]}', f'battler "{en["battlerName"]}" missing')
    for act in en['actions']:
        if not valid('Skills', act['skillId']):
            bad(f'enemy {en["name"]}', f'action skill {act["skillId"]} missing')
    for d in en['dropItems']:
        if d['kind']:
            table = ['', 'Items', 'Weapons', 'Armors'][d['kind']]
            if not valid(table, d['dataId']):
                bad(f'enemy {en["name"]}', f'drop {table} {d["dataId"]} missing')
for table in ('Skills', 'Items'):
    for s in D[table][1:]:
        if not s or not s['name']:
            continue
        if s['animationId'] > 0 and not (s['animationId'] < len(D['Animations']) and D['Animations'][s['animationId']]):
            bad(f'{table[:-1].lower()} {s["id"]} {s["name"]}', f'animation {s["animationId"]} missing')
        for ef in s['effects']:
            if ef['code'] in (21, 22) and ef['dataId'] and not valid('States', ef['dataId']):
                bad(f'{table[:-1].lower()} {s["name"]}', f'state {ef["dataId"]} missing')
            if ef['code'] == 44 and not valid('CommonEvents', ef['dataId']):
                bad(f'{table[:-1].lower()} {s["name"]}', f'common event {ef["dataId"]} missing')
            if ef['code'] == 43 and not valid('Skills', ef['dataId']):
                bad(f'{table[:-1].lower()} {s["name"]}', f'learns missing skill {ef["dataId"]}')
for ts in D['Tilesets'][1:]:
    if ts and ts['name']:
        for n in ts['tilesetNames']:
            if n and not exists('tilesets', n):
                bad(f'tileset {ts["name"]}', f'image {n} missing')

# ---------------------------------------------------------------- switches
names = D['System']['switches']
ENGINE_SET = {i for i, n in enumerate(names) if n in ('Daytime', 'Night', 'Vessel Active')}
never_set = sorted(s for s in reads if s not in sets and s not in ENGINE_SET)
for s in never_set:
    bad(f'switch {s} "{names[s] if s < len(names) else "?"}"', f'read by {reads[s][0]} (+{len(reads[s]) - 1} more), '
                                                             f'never turned ON')
unused = sorted(s for s in sets if s not in reads)
notes.append(f'{len(unused)} switches are set but never read (harmless): ' +
             ', '.join(names[s] for s in unused[:12]) + (' …' if len(unused) > 12 else ''))
for where, mid, eid, ch in self_reads:
    if (mid, eid, ch) not in self_sets:
        # a self switch read by the event itself but set nowhere; autorun "A" pages set it themselves
        bad(where, f'self switch {ch} is read but never set by this event')
for where, qid in quest_refs:
    if qid not in created_quests:
        bad(where, f'quest {qid} is edited/completed but never created')

print(f'{len(MAPS)} maps, {len(D["CommonEvents"]) - 1} common events, {len(D["Troops"]) - 1} troops, '
      f'{text_lines} message lines, {len(created_quests)} quests')
for n in notes:
    print('note:', n)
for p in problems:
    print('PROBLEM', p)
print('problems:', len(problems))


# ================================================================ static playthrough
# Which maps, switches, key items, common events and story battles can be reached from New Game? Every command
# is a "site" guarded by the switches (ON) and items its page conditions and enclosing branches require, inside a
# container (a map, a common event, a troop) that must itself be reachable. Variables, self switches, scripts and
# OFF-conditions are taken as satisfiable, so this over-approximates the player's freedom; what it can't reach, the
# player can't either.
def sites_of(lst, container, base_sw=(), base_items=()):
    out = []
    stack = []                      # (indent, requires_sw, requires_item, else_sw, else_item)
    for c in lst:
        code, p, ind = c['code'], c['parameters'], c['indent']
        while stack and stack[-1][0] > ind:
            stack.pop()
        if code == 111:
            sw_then, it_then, sw_else = set(), set(), set()
            if p[0] == 0:
                (sw_then if p[2] == 0 else sw_else).add(p[1])
            elif p[0] == 8:
                it_then.add(('item', p[1]))
            elif p[0] == 9:
                it_then.add(('weapon', p[1]))
            elif p[0] == 10:
                it_then.add(('armor', p[1]))
            stack.append([ind + 1, sw_then, it_then, sw_else])
            continue
        if code == 411:
            for fr in stack:
                if fr[0] == ind + 1:
                    fr[1], fr[2] = fr[3], set()
            continue
        req_sw = set(base_sw).union(*[fr[1] for fr in stack]) if stack else set(base_sw)
        req_it = set(base_items).union(*[fr[2] for fr in stack]) if stack else set(base_items)
        what = None
        if code == 121 and p[2] == 0:
            what = [('switch', s) for s in range(p[0], p[1] + 1)]
        elif code == 201 and p[0] == 0:
            what = [('map', p[1])]
        elif code == 117:
            what = [('ce', p[0])]
        elif code == 301 and p[0] == 0:
            what = [('troop', p[1])]
        elif code == 126 and p[1] == 0 and p[2] == 0:
            what = [('item', p[0])]
        elif code == 127 and p[1] == 0 and p[2] == 0:
            what = [('weapon', p[0])]
        elif code == 128 and p[1] == 0 and p[2] == 0:
            what = [('armor', p[0])]
        if what:
            for w in what:
                out.append((w, container, frozenset(req_sw), frozenset(req_it)))
    return out

SITES = []
for mid, m in MAPS.items():
    for enc in m.get('encounterList', []):
        SITES.append((('troop', enc['troopId']), ('map', mid), frozenset(), frozenset()))
    for e in m['events'][1:]:
        if not e:
            continue
        for pg in e['pages']:
            c = pg['conditions']
            sw = {c[k + 'Id'] for k in ('switch1', 'switch2') if c.get(k + 'Valid')}
            it = {('item', c['itemId'])} if c.get('itemValid') else set()
            SITES += sites_of(pg['list'], ('map', mid), sw, it)
for ce in D['CommonEvents'][1:]:
    if ce and ce['list']:
        sw = {ce['switchId']} if ce['trigger'] in (1, 2) else set()
        SITES += sites_of(ce['list'], ('ce', ce['id']), sw)
for tr in D['Troops'][1:]:
    if tr:
        for pg in tr['pages']:
            sw = {pg['conditions']['switchId']} if pg['conditions'].get('switchValid') else set()
            SITES += sites_of(pg['list'], ('troop', tr['id']), sw)

got = {('map', D['System']['startMapId'])} | {('switch', s) for s in ENGINE_SET}
got |= {('ce', ce['id']) for ce in D['CommonEvents'][1:] if ce and ce['trigger'] in (1, 2)}
for table in ('Skills', 'Items'):                   # common events run by skills and items
    for s in D[table][1:]:
        for ef in (s or {}).get('effects', []):
            if ef['code'] == 44:
                got.add(('ce', ef['dataId']))
for a in D['Actors'][1:]:                           # starting equipment
    if a:
        for slot, i in enumerate(a['equips']):
            if i:
                got.add(('weapon' if slot == 0 else 'armor', i))
changed = True
while changed:
    changed = False
    for what, container, sw, it in SITES:
        if what in got or container not in got:
            continue
        if all(('switch', s) in got for s in sw) and all(i in got for i in it):
            got.add(what)
            changed = True

unreached = []
for mid in MAPS:
    if ('map', mid) not in got:
        unreached.append(f'map {mid} {D["MapInfos"][mid]["name"]}')
for s in sorted({w[1] for w, *_ in SITES if w[0] == 'switch'}):
    if ('switch', s) not in got:
        unreached.append(f'switch {s} "{names[s]}"')
for i, itm in enumerate(D['Items']):
    if itm and itm['name'] and itm['itypeId'] == 2 and any(w == ('item', i) for w, *_ in SITES) and ('item', i) not in got:
        unreached.append(f'key item {i} {itm["name"]}')
story_troops = {w[1] for w, c, *_ in SITES if w[0] == 'troop' and c[0] != 'map' or
                (w[0] == 'troop' and c[0] == 'map' and D['Troops'][w[1]]['pages'] and
                 any(pg['list'] and len(pg['list']) > 1 for pg in D['Troops'][w[1]]['pages']))}
for t in sorted(story_troops):
    if ('troop', t) not in got:
        unreached.append(f'battle {t} {D["Troops"][t]["name"]}')
print(f'static playthrough: {sum(1 for g in got if g[0] == "map")}/{len(MAPS)} maps, '
      f'{sum(1 for g in got if g[0] == "switch")} switches, {sum(1 for g in got if g[0] == "troop")} battles reachable')
for u in unreached:
    print('UNREACHABLE', u)
if problems or unreached:
    sys.exit(1)


# ================================================================ script commands must parse
# Every Script command (355 + 655) and script condition (111 type 12) is wrapped in a function and handed to node
# for a syntax check (nothing is run).
import subprocess, tempfile, shutil as _sh
if _sh.which('node'):
    snippets = []
    def collect(where, lst):
        i = 0
        while i < len(lst):
            c = lst[i]
            if c['code'] == 355:
                body = [c['parameters'][0]]
                j = i + 1
                while j < len(lst) and lst[j]['code'] == 655:
                    body.append(lst[j]['parameters'][0])
                    j += 1
                snippets.append((where, '\n'.join(body)))
            elif c['code'] == 111 and c['parameters'][0] == 12:
                snippets.append((where, 'return (' + c['parameters'][1] + ');'))
            i += 1
    for mid, m in MAPS.items():
        for e in m['events'][1:]:
            if e:
                for pi, pg in enumerate(e['pages']):
                    collect(f'map {mid} / {e["name"]} p{pi + 1}', pg['list'])
    for ce in D['CommonEvents'][1:]:
        if ce:
            collect(f'common event {ce["name"]}', ce['list'])
    for tr in D['Troops'][1:]:
        if tr:
            for pi, pg in enumerate(tr['pages']):
                collect(f'troop {tr["name"]} p{pi + 1}', pg['list'])
    src = 'const S = [\n' + ',\n'.join('[%s, %s]' % (json.dumps(w), json.dumps(b)) for w, b in snippets) + '];\n' + \
          'let bad = 0; for (const [w, b] of S) { try { new Function(b); } catch (e) { bad++; console.log("SCRIPT", w, ":", e.message, "::", b.slice(0, 80)); } }\n' + \
          'console.log("scripts checked:", S.length, "bad:", bad); process.exit(bad ? 1 : 0);\n'
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(src)
    r = subprocess.run(['node', f.name], capture_output=True, text=True)
    print(r.stdout.strip())
    os.unlink(f.name)
    if r.returncode:
        sys.exit(1)
