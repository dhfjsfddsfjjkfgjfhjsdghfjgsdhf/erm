"""Shared helpers for the story build: ids, speakers, event lists, maps, quests, lights."""
import json, copy, os, sys
sys.path.insert(0, '/home/claude/mz/tools')
from dbkit import dumps, write_list, write_map, write_obj, page, event, conditions
from story import audio

ROOT = '/home/claude/mz'
ORIG = ROOT + '/orig'
SAMPLE = '/mnt/user-data/uploads/samplemaps'
OUT = ROOT + '/story/out'

def load_orig(name):
    return json.load(open(f'{ORIG}/data/{name}.json', encoding='utf-8'))

BASE = ROOT + '/story/base'

def load_sample(n, map_id=None):
    """An MZ sample map. Without the sample folder, the verified base of story map map_id (story/base, made by
    tools/reconstruct_bases.py from the last build) stands in for it."""
    path = f'{SAMPLE}/Map{n:03d}.json'
    if not os.path.exists(path) and map_id is not None and os.path.exists(f'{BASE}/Map{map_id:03d}.json'):
        path = f'{BASE}/Map{map_id:03d}.json'
    return json.load(open(path, encoding='utf-8'))

# =====================================================================
# Switch / variable registries (names show up in the editor)
# =====================================================================
class Registry:
    def __init__(self, kind, size, fixed):
        self.kind = kind
        self.size = size
        self.names = {}
        self.ids = {}
        for i, n in fixed.items():
            self.ids[n] = i
            self.names[i] = n

    def __call__(self, name):
        if name not in self.ids:
            i = 1
            while i in self.names:
                i += 1
            self.ids[name] = i
            self.names[i] = name
        return self.ids[name]

    def array(self):
        n = max(self.size, max(self.names) if self.names else 0)
        return [''] + [self.names.get(i, '') for i in range(1, n + 1)]

def seed_registries(path):
    """Pins switch and variable ids of an earlier build (names -> ids), so new chapters only append."""
    if not os.path.exists(path):
        return
    reg = json.load(open(path, encoding='utf-8'))
    for R, key in ((SW, 'switches'), (VAR, 'variables')):
        for i, n in reg[key].items():
            i = int(i)
            if n in R.ids and R.ids[n] != i:
                raise ValueError(f'{key}: {n} already has id {R.ids[n]}, frozen id {i}')
            R.ids[n] = i
            R.names[i] = n

SW = Registry('switch', 100, {1: 'Vessel Active', 2: 'Daytime', 3: 'Night', 4: 'Night Raid (quiet)'})
VAR = Registry('variable', 100, {1: 'Breakthrough Gate', 2: 'Deaths', 3: 'Money Lost', 4: 'Days Passed', 5: 'Hour',
                                 6: 'Minute'})

# =====================================================================
# Speakers (face sets)
# =====================================================================
class Speaker:
    def __init__(self, name, face, index, char=None, expr=None):
        self.name = name
        self.face = face
        self.index = index
        self.char = char or (face, index)
        self.expr = expr or {}

    def f(self, mood=None):
        """(face file, index) for a mood."""
        if mood is None:
            return self.face, self.index
        return self.expr.get(mood, (self.face, self.index))

# The player characters' portraits (img/faces/<Name>.png, slot 0; see tools/insert_portraits.py).
# Moods are kept in the script so extra expressions can be added later: add a slot and point the mood at it.
KANTA = Speaker('Kanta', 'Kanta', 0, ('Cast', 0),
                {'calm': ('Kanta', 0), 'fierce': ('Kanta', 0), 'wry': ('Kanta', 0), 'hurt': ('Kanta', 0)})
HANMA = Speaker('Hanma', 'Hanma', 0, ('Cast', 1),
                {'calm': ('Hanma', 0), 'smile': ('Hanma', 0), 'stern': ('Hanma', 0), 'command': ('Hanma', 0)})
FALIN = Speaker('Falin', 'Falin', 0, ('Cast', 2),
                {'calm': ('Falin', 0), 'fierce': ('Falin', 0), 'smile': ('Falin', 0), 'hurt': ('Falin', 0)})

def npc_speaker(name, sheet, index):
    return Speaker(name, sheet, index, (sheet, index))

# =====================================================================
# Event command lists
# =====================================================================
class Ev:
    """Event command list with correct indents (RPG Maker MZ codes)."""
    def __init__(self):
        self.cmds = []
        self.indent = 0

    # ---- core
    def add(self, code, params=None):
        self.cmds.append({"code": code, "indent": self.indent, "parameters": params if params is not None else []})
        return self

    def done(self):
        return self.cmds + [{"code": 0, "indent": 0, "parameters": []}]

    def block(self, body):
        """Runs body(self) one indent deeper and closes it with code 0."""
        self.indent += 1
        if body:
            body(self)
        self.add(0, [])
        self.indent -= 1

    # ---- messages
    def text(self, lines, face="", index=0, name="", background=0, position=2):
        if isinstance(lines, str):
            lines = lines.split('\n')
        for i in range(0, len(lines), 4):
            self.add(101, [face, index, background, position, name])
            for line in lines[i:i + 4]:
                self.add(401, [line])
        return self

    def say(self, who, lines, mood=None):
        face, index = who.f(mood)
        return self.text(lines, face, index, who.name)

    def narrate(self, lines, background=1, position=1):
        """Dim window in the middle: narration."""
        return self.text(lines, background=background, position=position)

    def choices(self, options, branches, cancel=-2, default=0, position=2):
        self.add(102, [options, cancel, default, position, 0])
        for i, label in enumerate(options):
            self.add(402, [i, label])
            self.block(branches[i] if i < len(branches) else None)
        if cancel == -2:
            self.add(403, [6, None])
            self.block(None)
        self.add(404, [])
        return self

    # ---- flow
    def cond(self, params, then=None, other=None):
        self.add(111, params)
        self.block(then)
        if other is not None:
            self.add(411, [])
            self.block(other)
        self.add(412, [])
        return self

    def if_switch(self, sid, on=True, then=None, other=None):
        return self.cond([0, sid, 0 if on else 1], then, other)

    def if_self(self, ch, on=True, then=None, other=None):
        return self.cond([2, ch, 0 if on else 1], then, other)

    def if_var(self, vid, op, value, then=None, other=None):
        """op: '==', '>=', '<=', '>', '<', '!='"""
        ops = {'==': 0, '>=': 1, '<=': 2, '>': 3, '<': 4, '!=': 5}
        return self.cond([1, vid, 0, value, ops[op]], then, other)

    def if_script(self, js, then=None, other=None):
        return self.cond([12, js], then, other)

    def if_gold(self, amount, op='>=', then=None, other=None):
        ops = {'>=': 0, '<=': 1, '<': 2}
        return self.cond([7, amount, ops[op]], then, other)

    def if_item(self, item_id, then=None, other=None):
        return self.cond([8, item_id], then, other)

    def if_actor_in_party(self, actor_id, then=None, other=None):
        return self.cond([4, actor_id, 0], then, other)

    def label(self, name):
        return self.add(118, [name])

    def jump(self, name):
        return self.add(119, [name])

    def exit_event(self):
        return self.add(115, [])

    def common(self, ce_id):
        return self.add(117, [ce_id])

    def comment(self, text):
        return self.add(108, [text])

    # ---- state
    def switch(self, sid, on=True):
        return self.add(121, [sid, sid, 0 if on else 1])

    def var(self, vid, value, op='='):
        ops = {'=': 0, '+': 1, '-': 2, '*': 3, '/': 4, '%': 5}
        return self.add(122, [vid, vid, ops[op], 0, value])

    def var_script(self, vid, js):
        return self.add(122, [vid, vid, 0, 4, js])

    def self_switch(self, ch="A", on=True):
        return self.add(123, [ch, 0 if on else 1])

    def gold(self, amount):
        return self.add(125, [0 if amount >= 0 else 1, 0, abs(amount)])

    def item(self, item_id, n=1):
        return self.add(126, [item_id, 0 if n >= 0 else 1, 0, abs(n)])

    def weapon(self, wid, n=1):
        return self.add(127, [wid, 0 if n >= 0 else 1, 0, abs(n), False])

    def armor(self, aid, n=1):
        return self.add(128, [aid, 0 if n >= 0 else 1, 0, abs(n), False])

    def party(self, actor_id, add=True, init=False):
        return self.add(129, [actor_id, 0 if add else 1, init])

    def menu_access(self, on):
        return self.add(135, [1 if on else 0])

    def save_access(self, on):
        return self.add(134, [1 if on else 0])

    def encounters(self, on):
        return self.add(136, [1 if on else 0])

    # ---- movement / map
    def transfer(self, map_id, x, y, direction=0, fade=0):
        return self.add(201, [0, map_id, x, y, direction, fade])

    def locate(self, char, x, y, direction=0):
        return self.add(203, [char, 0, x, y, direction])

    def scroll(self, direction, distance, speed=4, wait=True):
        return self.add(204, [direction, distance, speed, wait])

    def route(self, char, moves, wait=True, repeat=False, skippable=False):
        """moves: list of (code, params) or bare codes."""
        mv = [(m, []) if isinstance(m, int) else m for m in moves]
        r = {"list": [{"code": c, "parameters": p} for c, p in mv] + [{"code": 0, "parameters": []}],
             "repeat": repeat, "skippable": skippable, "wait": wait}
        self.add(205, [char, r])
        for c, p in mv:
            self.add(505, [{"code": c, "parameters": p}])
        return self

    def transparent(self, on=True):
        return self.add(211, [0 if on else 1])

    def anim(self, char, anim_id, wait=False):
        return self.add(212, [char, anim_id, wait])

    def balloon(self, char, balloon, wait=True):
        """balloon: 1 ! 2 ? 3 note 4 heart 5 anger 6 sweat 7 frustration 8 silence 9 idea 10 zzz"""
        return self.add(213, [char, balloon, wait])

    def erase(self):
        return self.add(214, [])

    def followers(self, show):
        return self.add(216, [0 if show else 1])

    def gather(self):
        return self.add(217, [])

    # ---- screen
    def fadeout(self):
        return self.add(221, [])

    def fadein(self):
        return self.add(222, [])

    def tint(self, tone, frames=60, wait=True):
        return self.add(223, [list(tone), frames, wait])

    def flash(self, color=(255, 255, 255, 170), frames=30, wait=True):
        return self.add(224, [list(color), frames, wait])

    def shake(self, power=5, speed=5, frames=30, wait=True):
        return self.add(225, [power, speed, frames, wait])

    def wait(self, frames):
        return self.add(230, [frames])

    def weather(self, kind='none', power=0, frames=0, wait=False):
        return self.add(236, [kind, power, frames, wait])

    # ---- audio
    def _au(self, kind, name, volume, pitch):
        return {"name": audio.check(kind, name), "volume": volume, "pitch": pitch, "pan": 0}

    def bgm(self, name, volume=80, pitch=100):
        return self.add(241, [self._au('bgm', name, volume, pitch)])

    def fade_bgm(self, sec=2):
        return self.add(242, [sec])

    def save_bgm(self):
        return self.add(243, [])

    def resume_bgm(self):
        return self.add(244, [])

    def bgs(self, name, volume=70, pitch=100):
        return self.add(245, [self._au('bgs', name, volume, pitch)])

    def fade_bgs(self, sec=2):
        return self.add(246, [sec])

    def me(self, name, volume=90, pitch=100):
        return self.add(249, [self._au('me', name, volume, pitch)])

    def se(self, name, volume=90, pitch=100):
        return self.add(250, [self._au('se', name, volume, pitch)])

    # ---- scene / party
    def battle(self, troop_id, can_escape=False, can_lose=False, win=None, escape=None, lose=None):
        self.add(301, [0, troop_id, can_escape, can_lose])
        if can_escape or can_lose:
            self.add(601, [])
            self.block(win)
            if can_escape:
                self.add(602, [])
                self.block(escape)
            if can_lose:
                self.add(603, [])
                self.block(lose)
            self.add(604, [])
        elif win:
            win(self)
        return self

    def shop(self, goods, purchase_only=False):
        """goods: list of ('item'|'weapon'|'armor', id)"""
        kind = {'item': 0, 'weapon': 1, 'armor': 2}
        first = goods[0]
        self.add(302, [kind[first[0]], first[1], 0, 0, purchase_only])
        for g in goods[1:]:
            self.add(605, [kind[g[0]], g[1], 0, 0])
        return self

    def recover_all(self, actor=0):
        return self.add(314, [0, actor])

    def add_state(self, actor, state_id):
        return self.add(313, [0, actor, 0, state_id])

    def change_level(self, actor, n, show=True):
        return self.add(316, [0, actor, 0 if n >= 0 else 1, 0, abs(n), show])

    def gain_exp(self, actor, n, show=True):
        return self.add(315, [0, actor, 0, 0, n, show])

    def learn(self, actor, skill_id):
        return self.add(318, [0, actor, 0, skill_id])

    def change_equip(self, actor, etype, item_id):
        return self.add(319, [actor, etype, item_id])

    def script(self, js):
        lines = js.split('\n')
        self.add(355, [lines[0]])
        for line in lines[1:]:
            self.add(655, [line])
        return self

    def plugin(self, plugin, command, args, label=None):
        self.add(357, [plugin, command, label or command, {k: str(v) for k, v in args.items()}])
        for k, v in args.items():
            self.add(657, [f"{k} = {v}"])
        return self

    def map_name(self, show):
        return self.add(281, [0 if show else 1])

    def picture(self, pid, name, x=408, y=312, origin=1, scale=100, opacity=255, blend=0):
        """Show Picture (centre origin by default)."""
        return self.add(231, [pid, name, origin, 0, x, y, scale, scale, opacity, blend])

    def move_picture(self, pid, x=408, y=312, origin=1, scale=100, opacity=255, frames=60, wait=True):
        return self.add(232, [pid, 0, origin, 0, x, y, scale, scale, opacity, 0, frames, wait, 0])

    def erase_picture(self, pid):
        return self.add(235, [pid])

    def to_title(self):
        return self.add(354, [])

    def abort_battle(self):
        return self.add(340, [])

    def change_name(self, actor, name):
        return self.add(320, [actor, name])

    def set_image(self, eid, sheet, index):
        return self.script("$gameMap.event(%d).setImage('%s', %d);" % (eid, sheet, index))

    def face_dir(self, eid, d):
        """Turns an event (direction fix aside) to 2/4/6/8."""
        return self.script("(e => { const f = e.isDirectionFixed(); e.setDirectionFix(false); e.setDirection(%d); "
                           "e.setDirectionFix(f); })($gameMap.event(%d));" % (d, eid))

    def battleback(self, b1, b2):
        return self.add(283, [b1, b2])

    # ---- story plugin shortcuts
    def rest_point(self, map_id=0, x=0, y=0, d=2):
        return self.plugin('Story_Core', 'SetRestPoint', {'mapId': map_id, 'x': x, 'y': y, 'direction': d})

    def breakthrough(self):
        return self.plugin('Story_Core', 'Breakthrough', {'silent': 'false'})

    def card(self, title, subtitle='', duration=200):
        return self.plugin('Story_Core', 'ChapterCard', {'title': title, 'subtitle': subtitle, 'duration': duration})

    def set_time(self, hour, minute=0):
        h12 = hour % 12
        if h12 == 0:
            h12 = 12
        ampm = 'AM' if hour < 12 else 'PM'
        return self.plugin('McKathlin_DayNight', 'setTime',
                           {'time_of_day': json.dumps({"hour": str(h12), "minutes": str(minute), "ampm": ampm})})

    def add_time(self, hours=0, minutes=0):
        return self.plugin('McKathlin_DayNight', 'addTime',
                           {'time_span': json.dumps({"hours": str(hours), "minutes": str(minutes)})})

    def lighting_preset(self, keyword, duration=60):
        return self.plugin('McKathlin_DayNight', 'useLightingPreset', {'lightingKeyword': keyword, 'duration': duration})

    def reset_lighting(self, duration=60):
        return self.plugin('McKathlin_DayNight', 'resetLighting', {'duration': duration})

    # ---- quests (WD_Quest)
    def quest_new(self, q):
        track = json.dumps({"isTrackable": "true", "text": q.track, "textTrans": "[]"})
        args = {'id': q.id, 'icon': q.icon, 'cat': 0, 'short': q.title, 'long': q.long or q.title, 'index': q.id,
                'giver': q.giver, 'area': q.area, 'desc': q.desc, 'questTrans': '[]', 'status': 'ongoing',
                'logs': '[]', 'track': track}
        self.plugin('WD_Quest', 'newCreateQuest', args, 'Create Quest')
        return self

    def quest_desc(self, q, desc):
        args = {'questID': q.id, 'questName': '', 'icon': 0, 'cat': -1, 'short': '', 'long': '', 'giver': '',
                'area': '', 'desc': desc, 'questTrans': '[]'}
        return self.plugin('WD_Quest', 'editQuestDescriptors', args, 'Edit Quest Descriptors')

    def quest_done(self, q, status='completed'):
        return self.plugin('WD_Quest', 'SetCompletion', {'questID': q.id, 'questName': '', 'status': status},
                           'Set Quest Completion Parameter')

    def notice(self, lines):
        """Short system notice (dim window, centre)."""
        return self.text(lines, background=1, position=1)

class Quest:
    def __init__(self, qid, title, giver, area, desc, track, icon=87, long=None):
        self.id, self.title, self.giver, self.area, self.desc, self.track, self.icon = qid, title, giver, area, desc, track, icon
        self.long = long

# =====================================================================
# Maps
# =====================================================================
DOOR_ROUTE = [17, (15, [3]), 18, (15, [3]), 19, 37]

class MapBuild:
    """A sample map with our own events (sample decor can be kept)."""
    registry = {}

    def __init__(self, map_id, name, sample, display='', keep_decor=True, parent=0):
        self.id = map_id
        self.name = name
        self.parent = parent
        self.m = load_sample(sample, map_id) if isinstance(sample, int) else sample
        self.sample = sample
        self.m['displayName'] = display
        self.m['events'] = [None] + ([e for e in self.m['events'][1:] if e and keep_decor and self._is_decor(e)])
        for i, e in enumerate(self.m['events'][1:], start=1):
            e['id'] = i
        self.lights = []          # Tausi map objects
        self.notes = []
        MapBuild.registry[map_id] = self

    @staticmethod
    def _is_decor(e):
        p = e['pages'][0]
        codes = {c['code'] for c in p['list']}
        return p['image']['characterName'] and not (codes & {201, 101, 301, 302}) and p['trigger'] in (0,) \
            and not p['image']['characterName'].startswith('!Door')

    @property
    def w(self):
        return self.m['width']

    @property
    def h(self):
        return self.m['height']

    def events_at(self, x, y):
        return [e for e in self.m['events'] if e and e['x'] == x and e['y'] == y]

    def remove_at(self, x, y):
        self.m['events'] = [None] + [e for e in self.m['events'][1:] if not (e['x'] == x and e['y'] == y)]
        for i, e in enumerate(self.m['events'][1:], start=1):
            e['id'] = i

    def add(self, name, x, y, pages, note=''):
        eid = len(self.m['events'])
        self.m['events'].append(event(eid, name, x, y, pages, note))
        return eid

    def props(self, note='', bgm=None, bgs=None, battleback=None, encounters=None, steps=30, dash=True, weather=None):
        # weather: 'snow 5', 'rain 3 unless 26', 'keep' (Story_Core <Weather>); no tag = clear on entry
        if weather:
            note = (note + '\n' if note else '') + '<Weather: %s>' % weather
        self.m['note'] = note
        if bgm:
            self.m['autoplayBgm'] = True
            self.m['bgm'] = {"name": audio.check('bgm', bgm[0]), "pan": 0, "pitch": bgm[2] if len(bgm) > 2 else 100,
                             "volume": bgm[1] if len(bgm) > 1 else 80}
        else:
            self.m['autoplayBgm'] = False
            self.m['bgm'] = {"name": "", "pan": 0, "pitch": 100, "volume": 90}
        if bgs:
            self.m['autoplayBgs'] = True
            self.m['bgs'] = {"name": audio.check('bgs', bgs[0]), "pan": 0, "pitch": 100,
                             "volume": bgs[1] if len(bgs) > 1 else 60}
        else:
            self.m['autoplayBgs'] = False
            self.m['bgs'] = {"name": "", "pan": 0, "pitch": 100, "volume": 90}
        if battleback:
            self.m['specifyBattleback'] = True
            self.m['battleback1Name'], self.m['battleback2Name'] = battleback
        else:
            self.m['specifyBattleback'] = False
        self.m['encounterList'] = [{"regionSet": list(r), "troopId": t, "weight": w} for t, w, r in (encounters or [])]
        self.m['encounterStep'] = steps
        self.m['disableDashing'] = not dash
        return self

    # --- common event shapes
    def exit(self, tiles, to_map, tx, ty, d=0, fade=0, cond=None, se=True, name='Exit'):
        for x, y in tiles:
            el = Ev()
            if se:
                el.se('Move1', 60)
            el.transfer(to_map, tx, ty, d, fade)
            p = page(el.done(), trigger=1, priority=0)
            if cond:
                p['conditions'].update(cond)
            self.add(name, x, y, [p])

    def door(self, x, y, to_map, tx, ty, d=8, sheet='!Door1', index=0, name='Door', locked_text=None, cond=None):
        el = Ev()
        if locked_text:
            el.text(locked_text)
        else:
            el.se('Open1')
            el.route(0, DOOR_ROUTE)
            el.route(-1, [12], skippable=True)
            el.se('Move1', 60)
            el.transfer(to_map, tx, ty, d, 0)
        p = page(el.done(), char=sheet, index=index, direction=2, pattern=1, trigger=1, priority=1, walk_anime=False)
        if cond:
            p['conditions'].update(cond)
        return self.add(name, x, y, [p])

    def npc(self, name, x, y, who, lst, direction=2, move_type=0, pages_extra=None, trigger=0, note=''):
        sheet, idx = who.char if isinstance(who, Speaker) else who
        p = page(lst.done() if isinstance(lst, Ev) else lst, char=sheet, index=idx, direction=direction, trigger=trigger,
                 priority=1, move_type=move_type)
        return self.add(name, x, y, [p] + (pages_extra or []), note)

    def autorun(self, name, lst, switch=None, self_off=True, x=0, y=0, cond_switch=None):
        """Runs once: page 1 autorun (optionally only when cond_switch is ON); page 2 blank after self switch A."""
        if isinstance(lst, Ev):
            lst.self_switch('A')
        p1 = page(lst.done() if isinstance(lst, Ev) else lst, trigger=3, priority=0)
        if cond_switch:
            p1['conditions']['switch1Valid'] = True
            p1['conditions']['switch1Id'] = cond_switch
        p2 = page(None, trigger=0, priority=0, self_switch='A')
        return self.add(name, x, y, [p1, p2])

    def light(self, obj, x, y, ref=0, enabled=True, tile=True):
        """Tausi map object: obj = light object name; x, y in tiles (centre) unless tile=False."""
        px = x * 48 + 24 if tile else x
        py = y * 48 + 24 if tile else y
        self.lights.append({"obj": obj, "x": px, "y": py, "ref": ref, "enabled": enabled})

    def follow_light(self, obj='beam', x=0, y=0):
        """Invisible event glued to the player + a light that follows it."""
        eid = self.add('Player Light', x, y, [page(None, trigger=0, priority=0, through=True)], note='<Follow Player>')
        self.light(obj, x, y, ref=eid)
        return eid

    def info(self, order, expanded=False):
        return {"id": self.id, "expanded": expanded, "name": self.name, "order": order, "parentId": self.parent,
                "scrollX": self.w * 24, "scrollY": self.h * 24}

def cond_switch(sid):
    return {"switch1Valid": True, "switch1Id": sid}

def cond_switch2(sid):
    return {"switch2Valid": True, "switch2Id": sid}

def cond_var(vid, value):
    return {"variableValid": True, "variableId": vid, "variableValue": value}

def pg(lst=None, **kw):
    """page() with conditions: sw=, sw2=, var=(id, value), self_sw='A', item=, actor= ..."""
    cond = {}
    if 'sw' in kw:
        cond.update(cond_switch(kw.pop('sw')))
    if 'sw2' in kw:
        cond.update(cond_switch2(kw.pop('sw2')))
    if 'var' in kw:
        v = kw.pop('var')
        cond.update(cond_var(v[0], v[1]))
    if 'item' in kw:
        cond.update({"itemValid": True, "itemId": kw.pop('item')})
    if 'actor' in kw:
        cond.update({"actorValid": True, "actorId": kw.pop('actor')})
    self_sw = kw.pop('self_sw', None)
    p = page(lst.done() if isinstance(lst, Ev) else lst, self_switch=self_sw, **kw)
    p['conditions'].update(cond)
    return p
