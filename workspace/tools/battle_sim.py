"""Auto-battle simulator: a Python port of the combat rules of Rank_Core, Rank_Battle and Story_Core, run on the
built database (story/out/data). It builds the party the way tools/scen_story_bal2.js does (levels, breakthroughs,
the same stat-spending policies, Falin's Auto Build) and fights troops with MZ's auto-battle choice (expected
damage over the target's HP), for a quick balance read without the engine.

Modelled: d20 attack rolls vs AC, crits, saves (half/negates, advantage by rank gap), dice + POW + 10 x rank,
the rank-gap multiplier, weakness (+1 gap), resistances and immunities, multi-target rate, minion rate, role extra
actions/attacks, enemy action ratings, MP costs by skill rank, skill forms, passive states' hit/crit/AC/stat
bonuses, Kanta's floating strikes and Halo Riposte, Falin's Rank Regen and Unbroken, Hanma's Hold the Line,
the Dawn Regalia against <Demon>s and the Veil of Ash.
Not modelled (the engine run is the reference): support skills (the auto-battle AI never picks them either),
states and buffs applied by skills (enemy buffs like Heerruf, fear, burns), barriers, items, turn-order effects,
troop-page scripts (scripted breakthroughs are applied from the start when fresh=True is not enough).
Added 5 Oct 2026: HP drain heals the user; enemy skills with 2-4 random targets hit that many.
The engine runs harsher than this simulator on foes that poison, put to sleep, buff themselves or drain (see
tools/story/engine_tune.py and the engine table at the top of handoff/balance.txt):
always confirm bosses with tools/scen_story_bal2.js.

usage: python3 tools/battle_sim.py [scenario name ...]      (see SCENARIOS at the bottom)"""
import json, os, re, random, sys, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.environ.get('STORY_OUT', ROOT + '/story/out') + '/data'
D = {n: json.load(open(f'{DATA}/{n}.json', encoding='utf-8'))
     for n in ['Actors', 'Classes', 'Skills', 'Weapons', 'Armors', 'Enemies', 'Troops', 'States', 'System']}

STATS = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'MAG']
LETTERS = ['F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS', 'V']
APT = {'S': 1.5, 'A': 1, 'B': 0.75, 'C': 0.5, 'D': 0.25, 'E': 0}
ROLE_ACTIONS = {'elite': 0, 'boss': 1, 'apex': 1}
ROLE_ATTACKS = {'elite': 1, 'boss': 0, 'apex': 1}
LIGHT = 8

def clamp(v, a, b):
    return max(a, min(b, v))
def mod(v):
    return int(v) // 20
def pw(v):
    return int(v) // 4
def of_value(v):
    return clamp(int(v) // 100, 0, 9)
def gap_mult(g):
    return 2 if g >= 2 else 1.5 if g == 1 else 1 if g == 0 else 0.5 if g == -1 else 0.25 if g == -2 else 0
def power_level(v):
    s = sorted(v, reverse=True)
    return (s[0] + s[1] + s[2]) // 3
def parse_rank(s):
    if s is None:
        return None
    t = str(s).strip().upper()
    if t.isdigit():
        return clamp(int(t), 0, 9)
    return LETTERS.index(t) if t in LETTERS else None
def tag(note, name):
    m = re.search(r'<\s*' + name + r'\s*:\s*([^>]*)>', note, re.I)
    return m.group(1).strip() if m else None
def flag(note, name):
    return re.search(r'<\s*' + name + r'\s*>', note, re.I) is not None
def signed(s):
    m = re.match(r'^\s*([+\-]?\d+(?:\.\d+)?)', str(s))
    return float(m.group(1)) if m else None
def pct(s):
    m = re.match(r'^\s*([+\-]?\d+(?:\.\d+)?)\s*(%?)', str(s))
    if not m:
        return None
    return float(m.group(1)) / 100 if m.group(2) else float(m.group(1))
def parse_dice(s):
    if s is None:
        return None
    t = str(s).strip()
    m = re.match(r'^(\d*)\s*d\s*(\d+)\s*(?:([+-])\s*(\d+))?$', t, re.I)
    if m:
        bonus = (-1 if m.group(3) == '-' else 1) * int(m.group(4)) if m.group(3) else 0
        return (int(m.group(1) or 1), int(m.group(2)), bonus)
    m = re.match(r'^(\d+)$', t)
    return (1, int(m.group(1)), 0) if m else None
def roll(d):
    return d[2] + sum(random.randint(1, d[1]) for _ in range(d[0]))
def avg(d):
    return d[0] * (d[1] + 1) / 2 + d[2]


# ------------------------------------------------------------------------------------------------ database
def common(note):
    rk = {'hit': signed(tag(note, 'Hit')) or 0, 'crit': signed(tag(note, r'Crit\s*Range')) or 0,
          'ac': signed(tag(note, 'AC')) or 0, 'rank': parse_rank(tag(note, 'Rank')),
          'stat': (tag(note, 'Stat') or '').upper() or None}
    sv = tag(note, 'Saves')
    rk['saves'] = [s.upper() for s in re.split(r'[\s,]+', sv) if s.upper() in STATS] if sv else None
    plus = [0] * 7
    rate = [1.0] * 7
    for m in re.finditer(r'<\s*(STR|DEX|CON|INT|WIS|CHA|MAG|ALL\s*STATS)\s*:\s*([+\-]?\d+(?:\.\d+)?)\s*(%?)\s*>', note, re.I):
        idx = range(7) if m.group(1).upper().startswith('ALL') else [STATS.index(m.group(1).upper())]
        for i in idx:
            if m.group(3):
                rate[i] *= 1 + float(m.group(2)) / 100
            else:
                plus[i] += float(m.group(2))
    rk['plus'], rk['rate'] = plus, rate
    return rk

def parse_skill(s):
    note = s['note']
    rk = common(note)
    rk['dice'] = parse_dice(tag(note, 'Die') or tag(note, 'Dice') or s['damage']['formula'])
    rk['body'] = flag(note, 'Body')
    rk['start'] = parse_rank(tag(note, r'Start\s*Rank')) or 0
    mr = parse_rank(tag(note, r'Max\s*Rank'))
    rk['max'] = 9 if mr is None else mr
    rk['needs'] = parse_rank(tag(note, r'Needs\s*Rank'))
    sv = tag(note, 'Save')
    rk['save'] = None
    if sv:
        m = re.match(r'(STR|DEX|CON|INT|WIS|CHA|MAG)(?:\s+(negates|states|effects|half))?', sv, re.I)
        if m:
            mode = (m.group(2) or 'half').lower()
            rk['save'] = (m.group(1).upper(), 'states' if mode == 'effects' else mode)
    rk['dc'] = signed(tag(note, 'DC')) or 0
    r = tag(note, 'Damage')
    rk['rate'] = pct(r) if r is not None else 1
    rk['bonus'] = signed(tag(note, 'Bonus')) or 0
    a = tag(note, r'Area\s*Rate')
    rk['area'] = pct(a) if a is not None else None
    rk['roll'] = 'none' if flag(note, r'No\s*Attack\s*Roll') else 'roll' if flag(note, r'Attack\s*Roll') else 'auto'
    rk['forms'] = {}
    for m in re.finditer(r'<\s*At\s+Rank\s+(SSS|SS|S|F|E|D|C|B|A|V)\s*>([\s\S]*?)<\/\s*At\s+Rank\s+\1\s*>', note, re.I):
        f = {}
        for line in re.split(r'[\n;]+', m.group(2)):
            kv = re.match(r'^\s*([a-z ]+?)\s*:\s*(.+?)\s*$', line, re.I)
            if not kv:
                continue
            k, v = kv.group(1).lower().replace(' ', ''), kv.group(2)
            if k in ('die', 'dice'):
                f['dice'] = parse_dice(v)
            elif k in ('hits', 'repeats'):
                f['hits'] = max(1, int(float(v)))
            elif k in ('damage', 'rate'):
                f['rate'] = pct(v)
            elif k == 'bonus':
                f['bonus'] = signed(v) or 0
            elif k == 'hit':
                f['hit'] = signed(v) or 0
            elif k in ('crit', 'critrange'):
                f['crit'] = signed(v) or 0
        rk['forms'][parse_rank(m.group(1))] = f
    rk['mastery'] = 'off' if flag(note, r'No\s*Mastery') else 'on' if flag(note, 'Mastery') else 'auto'
    rk['passive'] = [int(x) for x in re.findall(r'<\s*Passive\s*State\s*:\s*(\d+)\s*>', note, re.I)]
    rk['aura'] = [int(x) for x in re.findall(r'<\s*Party\s*Aura\s*:\s*(\d+)\s*>', note, re.I)]
    rk['only_demons'] = flag(note, r'Only\s*Demons')
    return rk

SK = {s['id']: dict(s, rk=parse_skill(s)) for s in D['Skills'] if s}
def state_rk(i):
    s = D['States'][i]
    rk = common(s['note'])
    rk['float'] = int(signed(tag(s['note'], r'Float\s*Strikes')) or 0)
    rk['riposte'] = flag(s['note'], 'Riposte')
    rg = tag(s['note'], r'Rank\s*Regen')
    rk['regen'] = pct(rg) if rg else 0
    rk['traits'] = s['traits']
    return rk
ST = {s['id']: state_rk(s['id']) for s in D['States'] if s}
FLOAT_SKILL = next(i for i, s in SK.items() if flag(s['note'], r'Floating\s*Strike'))


def enemy_rk(e):
    note = e['note']
    rk = common(note)
    role = (tag(note, 'Role') or '').lower()
    rk['role'] = role if role in ('minion', 'standard', 'elite', 'boss', 'apex') else 'standard'
    p = e['params']
    native = [p[2], p[6], p[3], round((p[4] + p[5]) / 2), p[5], p[7], p[4]]
    rk['stats'] = [clamp(native[i], 0, 999) for i in range(7)]
    if rk['rank'] is None:
        rk['rank'] = of_value(power_level(rk['stats']))
    rk['atk_dice'] = parse_dice(tag(note, r'Attack\s*Die') or tag(note, r'Attack\s*Dice')) or (1, 6, 0)
    a = tag(note, r'Attack\s*Stat')
    rk['atk_stat'] = a.upper() if a and a.upper() in STATS else 'STR'
    arm = tag(note, 'Armor')
    rk['armor'] = signed(arm) if arm is not None else None
    act = tag(note, 'AC')
    rk['ac_fixed'] = None
    rk['ac_bonus'] = 0
    if act is not None:
        if re.match(r'^\s*[+\-]', act):
            rk['ac_bonus'] = signed(act) or 0
        else:
            rk['ac_fixed'] = signed(act)
    rk['demon'] = flag(note, 'Demon')
    rk['veil'] = flag(note, r'Veil\s*of\s*Ash')
    return rk


def element_rates(traits):
    r = {}
    for t in traits:
        if t['code'] == 11:
            r[t['dataId']] = r.get(t['dataId'], 1) * t['value']
    return r


# ------------------------------------------------------------------------------------------------ battlers
class Battler:
    def __init__(self):
        self.hp = self.mhp = self.mp = self.mmp = 0
        self.alive = True
        self.side = None
        self.name = ''

    def dead(self):
        return self.hp <= 0


class Actor(Battler):
    """A party member built like scen_story_bal2.js builds it."""
    POLICY = {1: {'DEX': 0.5, 'CON': 0.25, 'STR': 0.1, 'MAG': 0.15},
              2: {'WIS': 0.4, 'MAG': 0.3, 'CON': 0.2, 'CHA': 0.1},
              3: {'CON': 0.45, 'STR': 0.4, 'WIS': 0.15}}

    def __init__(self, aid):
        super().__init__()
        self.id = aid
        self.data = D['Actors'][aid]
        self.cls = D['Classes'][self.data['classId']]
        self.name = self.data['name']
        note = self.data['note']
        self.gated = flag(note, 'Gated')
        self.bound = tag(note, r'Bound\s*To') is not None
        self.fixed_rank = parse_rank(tag(note, 'Rank'))
        apt = tag(self.cls['note'], 'Aptitude') or ''
        g = {m.group(1).upper(): m.group(2).upper() for m in re.finditer(r'(STR|DEX|CON|INT|WIS|CHA|MAG)\s*[:=]?\s*([SABCDE])\b', apt, re.I)}
        self.apt = [APT.get(g.get(s, 'C'), 0.5) for s in STATS]
        sv = tag(self.cls['note'], 'Saves')
        self.saves = [s.upper() for s in re.split(r'[\s,]+', sv)] if sv else []
        self.level = 1
        self.alloc = [0] * 7
        self.bonus = [0] * 7
        self.points = 20
        self.auto = None
        ab = tag(note, r'Auto\s*Build')
        if ab:
            self.auto = {STATS.index(m.group(1).upper()): float(m.group(2))
                         for m in re.finditer(r'(STR|DEX|CON|INT|WIS|CHA|MAG)\s*[:=]?\s*(\d+(?:\.\d+)?)', ab, re.I)}
        self.skills = set()
        self.mastery = {}
        self.equip_weapon = self.data['equips'][0]
        self.equip_armors = [a for a in self.data['equips'][1:] if a]

    # --- stats
    def gate_cap(self, gate):
        return min(999, (gate + 1) * 100 - 1)

    def base(self, i, gate):
        v = 1 + math.floor(self.apt[i] * max(0, self.level - 1)) + self.alloc[i] + self.bonus[i]
        v = clamp(v, 0, 999)
        return min(v, self.gate_cap(gate)) if self.gated else v

    def rank(self, gate):
        if self.fixed_rank is not None:
            return self.fixed_rank
        return of_value(power_level([self.base(i, gate) for i in range(7)]))

    def cap(self, i, gate):
        c = min(999, (clamp(self.rank(gate), 0, 9) + 2) * 100 - 1)
        return min(c, self.gate_cap(gate)) if self.gated else c

    def allocate(self, i, n, gate):
        n = int(math.floor(n))
        n = max(0, min(n, self.points, self.cap(i, gate) - self.base(i, gate)))
        self.alloc[i] += n
        self.points -= n
        return n

    def change_level(self, L):
        if L > self.level:
            self.points += 20 * (L - self.level)
        self.level = L

    def spend(self, gate):
        if self.auto:
            total = sum(self.auto.values())
            for _ in range(6):
                pts = self.points
                spent = 0
                for k, w in self.auto.items():
                    spent += self.allocate(k, max(1, math.floor(pts * w / total)), gate)
                if spent == 0 or self.points <= 0:
                    break
            self.catch_up(gate)
            return
        pol = self.POLICY.get(self.id)
        if not pol:
            return
        pts = self.points
        want = {s: math.floor(pts * f) for s, f in pol.items()}
        for _ in range(4):
            for s in pol:
                want[s] -= self.allocate(STATS.index(s), want[s], gate)
        for s in ['CON', 'DEX', 'WIS', 'STR', 'MAG', 'CHA', 'INT']:
            self.allocate(STATS.index(s), self.points, gate)

    def top3(self, gate):
        return sorted(range(7), key=lambda i: (-self.base(i, gate), -self.apt[i]))[:3]

    def catch_up(self, gate):
        if not self.gated or gate <= 0:
            return
        for i in self.top3(gate):
            v = self.base(i, gate)
            if v < gate * 100:
                self.bonus[i] += gate * 100 - v

    # --- gear and skills for the current gate
    def gear(self, gate):
        note = self.data['note']
        def rank_map(t):
            out = {}
            for part in (tag(note, t) or '').split(','):
                m = re.match(r'^\s*(SSS|SS|S|F|E|D|C|B|A|V)\s+(\d+)\s*$', part, re.I)
                if m:
                    out[parse_rank(m.group(1))] = int(m.group(2))
            return out
        wmap, amap = rank_map(r'Rank\s*Weapon'), rank_map(r'Rank\s*Armor')
        weapon = self.equip_weapon
        for r in sorted(wmap):
            if r <= gate:
                weapon = wmap[r]
        armors = list(self.equip_armors)
        if amap:
            body = None
            for r in sorted(amap):
                if r <= gate:
                    body = amap[r]
            armors = [a for a in armors if D['Armors'][a]['etypeId'] != 4] + ([body] if body else [])
        return weapon, armors

    def learn(self, gate):
        for l in self.cls['learnings']:
            if l['level'] <= self.level:
                rk = SK[l['skillId']]['rk']
                if rk['needs'] is None or rk['needs'] <= gate:
                    self.skills.add(l['skillId'])
        note = self.data['note']
        for r in range(gate + 1):
            t = tag(note, 'Breakthrough ' + LETTERS[r])
            if t:
                for x in t.split(','):
                    if x.strip():
                        self.skills.add(int(x))

    def is_mastery(self, sid):
        s = SK[sid]
        if s['rk']['mastery'] == 'off':
            return False
        if s['rk']['mastery'] == 'on':
            return True
        return sid not in (1, 2) and s['mpCost'] > 0

    def prepare(self, gate, party_auras):
        """Freezes everything a battle needs at this gate."""
        self.gate = gate
        self.learn(gate)
        w, arms = self.gear(gate)
        self.weapon = D['Weapons'][w] if w else None
        self.armors = [D['Armors'][a] for a in arms]
        self.objs = []           # (rk-like dict) for hit/crit/ac/stat bonuses and traits
        for eq in ([self.weapon] if self.weapon else []) + self.armors:
            rk = common(eq['note'])
            rk['traits'] = eq['traits']
            self.objs.append(rk)
        passives = set()
        for sid in self.skills:
            passives.update(SK[sid]['rk']['passive'])
        for sid in passives | set(party_auras):
            if sid in ST:
                self.objs.append(ST[sid])
        stats = []
        for i in range(7):
            v = self.base(i, gate) + sum(o['plus'][i] for o in self.objs)
            for o in self.objs:
                v *= o['rate'][i]
            stats.append(clamp(round(v), 0, 999))
        self.stats = stats
        self.rnk = self.rank(gate)
        traits = [t for o in self.objs for t in o.get('traits', [])]
        self.erates = element_rates(traits)
        self.atk_elements = [t['dataId'] for t in traits if t['code'] == 31]
        self.hit_bonus = sum(o['hit'] for o in self.objs)
        self.crit_bonus = sum(o['crit'] for o in self.objs)
        self.floats = sum(o.get('float', 0) for o in self.objs)
        self.riposte = any(o.get('riposte') for o in self.objs)
        self.regen = max([o.get('regen', 0) for o in self.objs] + [0])
        self.unbroken = any(flag(SK[s]['note'], 'Unbroken') for s in self.skills)
        self.hold_line = any(flag(SK[s]['note'], r'Hold\s*The\s*Line') for s in self.skills)
        con, mag = stats[2], stats[6]
        self.mhp = max(1, math.floor(10 + 2 * con + 5 * self.level))
        self.mmp = max(0, math.floor(mag * (0.8 + 0.5 * self.rnk) + 2 * self.level + 8))
        # AC
        body = extra = pen = 0
        str_rank = of_value(stats[0])
        for a in self.armors:
            rk = common(a['note'])
            t = tag(a['note'], 'Armor')
            val = signed(t) if t is not None else a['params'][3]
            if a['etypeId'] == 4:
                body = max(body, val)
            else:
                extra += val
            heavy = flag(a['note'], 'Heavy') or 'heavy' in D['System']['armorTypes'][a['atypeId']].lower()
            if heavy and (rk['rank'] or 0) > str_rank:
                pen = 2
        self.ac = 10 + max(mod(stats[1]), body) + extra + sum(o['ac'] for o in self.objs) - pen
        wrk = common(self.weapon['note']) if self.weapon else {'stat': None, 'rank': 0}
        self.atk_stat = wrk['stat'] or 'STR'
        self.atk_rank = wrk['rank'] or 0
        wd = parse_dice(tag(self.weapon['note'], 'Die') or tag(self.weapon['note'], 'Dice')) if self.weapon else None
        self.atk_dice = wd or ((1, max(1, self.weapon['params'][2] or 4), 0) if self.weapon else
                               parse_dice(tag(self.data['note'], r'Unarmed\s*Die')) or (1, 4, 0))
        for sid in self.skills:
            if self.is_mastery(sid):
                rk = SK[sid]['rk']
                self.mastery[sid] = min(rk['max'], max(rk['start'], gate - 1, self.mastery.get(sid, 0)))

    def stat(self, s):
        return self.stats[STATS.index(s)]

    def skill_rank(self, sid):
        if sid == 1:
            return self.atk_rank
        rk = SK[sid]['rk']
        stat_rank = of_value(self.stat(skill_stat(sid, self)))
        if not self.is_mastery(sid):
            return min(self.rnk, stat_rank, rk['max'])
        return min(self.mastery.get(sid, rk['start']), stat_rank, rk['max'])

    def mp_cost(self, sid):
        s = SK[sid]
        if s['mpCost'] <= 0:
            return 0
        r = self.skill_rank(sid)
        c = s['mpCost'] * (r + 1) ** 2
        if s['rk']['body']:
            c = math.floor(c * 0.5)
        cut = min(0.5, self.stat('INT') / 2000)
        return max(1, round(c * (1 - cut)))

    def save_bonus(self, stat):
        return mod(self.stat(stat)) + (3 if stat in self.saves else 0)


OVERRIDE = {}        # enemy name -> {'hp': n, 'rank': 'C'} (tuning experiments)


class Enemy(Battler):
    def __init__(self, eid):
        super().__init__()
        self.data = D['Enemies'][eid]
        self.name = self.data['name']
        self.rk = enemy_rk(self.data)
        self.stats = self.rk['stats']
        self.mhp = self.hp = self.data['params'][0]
        ov = OVERRIDE.get(self.name, {})
        if 'hp' in ov:
            self.mhp = self.hp = int(ov['hp'])
        if 'rank' in ov:
            self.rk['rank'] = parse_rank(ov['rank'])
        if 'role' in ov:
            self.rk['role'] = ov['role']
        if 'ac' in ov:
            self.rk['ac_fixed'] = ov['ac']
        if 'atk' in ov:                  # offence factor: STR, DEX, INT and MAG
            self.stats = [clamp(round(v * ov['atk']), 0, 999) if i in (0, 1, 3, 6) else v
                          for i, v in enumerate(self.stats)]
        self.mp = self.mmp = self.data['params'][1]
        self.erates = element_rates(self.data['traits'])
        self.atk_elements = []
        self.saves = self.rk['saves'] or (['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'MAG']
                                          if self.rk['role'] in ('elite', 'boss', 'apex') else [])

    def stat(self, s):
        return self.stats[STATS.index(s)]

    def rank(self, pierce):
        if self.rk['veil'] and pierce < 4:
            return 9
        return self.rk['rank']

    @property
    def ac(self):
        rk = self.rk
        if rk['ac_fixed'] is not None:
            a = rk['ac_fixed']
        else:
            arm = rk['armor'] if rk['armor'] is not None else 5 * rk['rank'] + 2
            a = 10 + max(mod(self.stat('DEX')), arm)
        return a + rk['ac_bonus']

    def save_bonus(self, stat):
        return mod(self.stat(stat)) + (3 if stat in self.saves else 0)


def skill_stat(sid, b):
    s = SK[sid]
    if s['rk']['stat']:
        return s['rk']['stat']
    if sid == 1:
        return b.atk_stat if isinstance(b, Actor) else b.rk['atk_stat']
    if s['damage']['type'] in (3, 4):
        return 'WIS'
    if s['hitType'] == 1:
        return 'STR'
    return 'MAG'


# ------------------------------------------------------------------------------------------------ one action
class Battle:
    def __init__(self, party, troop_id, pierce=0, log=False, bt_turn=None, bt_hp=None, rebuild=None, yield_hp=None,
                 end_turn=None):
        self.bt_turn, self.bt_hp, self.rebuild, self.yield_hp = bt_turn, bt_hp, rebuild, yield_hp
        self.end_turn = end_turn          # a troop page that ends the battle at the start of that turn
        self.broke = False
        self.party = party
        self.pierce = pierce
        self.enemies = []
        for m in D['Troops'][troop_id]['members']:
            e = Enemy(m['enemyId'])
            self.enemies.append(e)
        self.log = log
        self.turn = 0
        for a in party:
            a.hp, a.mp = a.mhp, a.mmp
            a.used_unbroken = False
            a.held = False
            a.riposted = False

    def alive(self, side):
        return [b for b in (self.party if side == 'party' else self.enemies) if not b.dead()]

    def rank_of(self, b):
        return b.rnk if isinstance(b, Actor) else b.rank(self.pierce)

    def info(self, user, sid):
        s = SK[sid]
        rk = s['rk']
        if sid == 1:
            stat = user.atk_stat if isinstance(user, Actor) else user.rk['atk_stat']
            dice = user.atk_dice if isinstance(user, Actor) else user.rk['atk_dice']
            gb = user.atk_rank if isinstance(user, Actor) else self.rank_of(user)
            form = {}
        else:
            stat = skill_stat(sid, user)
            gb = user.skill_rank(sid) if isinstance(user, Actor) else min(self.rank_of(user), rk['max'])
            form = {}
            for r in range(gb + 1):
                form.update(rk['forms'].get(r, {}))
            dice = form.get('dice') or rk['dice'] or (1, 6, 0)
        subj = self.rank_of(user)
        atk_rank = min(subj + 2, max(subj, gb))
        return dict(stat=stat, sv=user.stat(stat), gb=gb, atk_rank=atk_rank, dice=dice, form=form, rk=rk, s=s)

    def element_rate(self, user, s, target):
        el = s['damage']['elementId']
        els = user.atk_elements if el == -1 else ([el] if el > 0 else [])
        if not els:
            return 1
        return max(target.erates.get(e, 1) for e in els)

    def gap(self, user, target, inf):
        g = inf['atk_rank'] - self.rank_of(target)
        if self.pierce:
            if isinstance(user, Actor) and isinstance(target, Enemy) and target.rk['demon'] and g < 0:
                g = min(0, g + self.pierce)
            elif isinstance(user, Enemy) and user.rk['demon'] and isinstance(target, Actor) and g > 0:
                g = max(0, g - self.pierce)
        return g

    def multi(self, s):
        return s['scope'] in (2, 8, 10, 14) or (s['scope'] in (3, 4, 5, 6) and s['scope'] - 1 > 1)

    def expected(self, user, sid, target):
        """What MZ's auto battle sees: average damage/healing, no hit chance, no saves."""
        s = SK[sid]
        inf = self.info(user, sid)
        base = avg(inf['dice']) + pw(inf['sv']) + 10 * inf['gb'] + inf['rk']['bonus'] + inf['form'].get('bonus', 0)
        rate = (inf['rk']['rate'] if inf['rk']['rate'] is not None else 1) * (inf['form'].get('rate') or 1)
        multi = (inf['rk']['area'] if inf['rk']['area'] is not None else 0.5) if self.multi(s) else 1
        if s['damage']['type'] in (3, 4):
            return base * rate * multi
        if s['damage']['type'] not in (1, 2, 5, 6):
            return 0
        g = self.gap(user, target, inf)
        er = self.element_rate(user, s, target)
        if er > 1:
            g += 1
        if er <= 0:
            return 0
        m = gap_mult(g) * (er if er < 1 else 1) * rate * multi
        return base * m

    def act(self, user, sid, target):
        """Resolves one use of a skill on one target; returns damage dealt (or healing)."""
        s = SK[sid]
        inf = self.info(user, sid)
        rk, form = inf['rk'], inf['form']
        dmg_type = s['damage']['type']
        if dmg_type in (3, 4):
            base = roll(inf['dice']) + pw(inf['sv']) + 10 * inf['gb'] + rk['bonus'] + form.get('bonus', 0)
            rate = (rk['rate'] if rk['rate'] is not None else 1) * (form.get('rate') or 1)
            multi = (rk['area'] if rk['area'] is not None else 0.5) if self.multi(s) else 1
            v = max(0, round(base * rate * multi))
            target.hp = min(target.mhp, target.hp + v)
            return -v
        if dmg_type not in (1, 2, 5, 6):
            return 0
        g = self.gap(user, target, inf)
        er = self.element_rate(user, s, target)
        if er > 1:
            g += 1
        gm = gap_mult(g)
        if gm == 0 or er <= 0:
            return 0
        # attack roll
        mode = rk['roll']
        if mode == 'auto':
            mode = 'none' if (s['scope'] in (2, 8, 10, 14) or s['hitType'] == 0 and s['scope'] in (7, 8, 11)) else 'roll'
            if s['hitType'] == 0 and rk['roll'] != 'roll':
                mode = 'none'            # certain-hit skills
        crit = False
        if mode == 'roll':
            nat = random.randint(1, 20)
            bonus = mod(inf['sv']) + 8 + user_hit(user) + rk['hit'] + form.get('hit', 0)
            if nat == 1 or (nat != 20 and nat + bonus < target.ac):
                if isinstance(target, Actor) and target.riposte and not target.riposted and not user.dead():
                    target.riposted = True
                    self.act(target, FLOAT_SKILL, user)
                return None
            thr = clamp(20 - user_crit(user) - rk['crit'] - form.get('crit', 0), 2, 20)
            crit = s['damage']['critical'] and nat >= thr
        mult = gm * (er if er < 1 else 1) * (rk['rate'] if rk['rate'] is not None else 1) * (form.get('rate') or 1)
        if self.multi(s):
            mult *= rk['area'] if rk['area'] is not None else 0.5
        if rk['save']:
            st, smode = rk['save']
            dc = (10 if isinstance(user, Enemy) and isinstance(target, Actor) else 13) + mod(inf['sv']) + rk['dc']
            r = random.randint(1, 20)
            if g <= -2:
                r = max(r, random.randint(1, 20))
            elif g >= 2:
                r = min(r, random.randint(1, 20))
            if r + target.save_bonus(st) >= dc:
                if smode == 'negates':
                    return 0
                if smode == 'half':
                    mult *= 0.5
        if crit:
            mult *= 1.5
        if isinstance(user, Enemy) and user.rk['role'] == 'minion':
            mult *= 0.5
        base = roll(inf['dice']) + pw(inf['sv']) + 10 * inf['gb'] + rk['bonus'] + form.get('bonus', 0)
        v = max(1, round(base * mult))
        if dmg_type == 5:                               # HP drain: MZ caps it at the target's HP and heals the user
            v = min(v, max(0, target.hp))
            if not user.dead():
                user.hp = min(user.mhp, user.hp + v)
        self.hurt(target, v)
        return v

    def hurt(self, t, v):
        t.hp -= v
        if t.hp <= 0 and isinstance(t, Actor):
            if t.unbroken and not t.used_unbroken:
                t.used_unbroken = True
                t.hp = 1
                return
            hanma = next((a for a in self.party if a.hold_line and not a.dead()), None)
            if hanma and not t.held and hanma.mp >= 5:
                t.held = True
                hanma.mp -= 5
                t.hp = 1

    # --- turns
    def actor_turn(self, a):
        foes = self.alive('enemy')
        if not foes:
            return
        best, bv, btarget = 1, -1, None
        choices = [1] + [s for s in a.skills if SK[s]['occasion'] in (0, 1) and SK[s]['damage']['type'] in (1, 2, 3, 4, 5, 6)]
        for sid in choices:
            s = SK[sid]
            if a.mp < a.mp_cost(sid):
                continue
            if s['rk']['only_demons'] and not any(e.rk['demon'] for e in foes):
                continue
            if s['damage']['type'] in (3, 4):
                cands = [m for m in self.alive('party')]
                vals = [min(self.expected(a, sid, m), m.mhp - m.hp) / m.mhp for m in cands]
                if self.multi(s):
                    val, tgt = sum(vals), None
                else:
                    i = max(range(len(vals)), key=lambda k: vals[k])
                    val, tgt = vals[i], cands[i]
            else:
                vals = [min(self.expected(a, sid, e), 1e9) / max(e.hp, 1) for e in foes]
                if self.multi(s):
                    val, tgt = sum(vals), None
                else:
                    i = max(range(len(vals)), key=lambda k: vals[k])
                    val, tgt = vals[i], foes[i]
            hits = max(1, self.info(a, sid)['form'].get('hits', 1)) if sid != 1 else 1
            val *= hits
            if val > 0:
                val += random.random()
            if val > bv:
                best, bv, btarget = sid, val, tgt
        s = SK[best]
        a.mp -= a.mp_cost(best)
        hits = max(1, self.info(a, best)['form'].get('hits', 1)) if best != 1 else 1
        for _ in range(hits):
            if s['damage']['type'] in (3, 4):
                targets = self.alive('party') if self.multi(s) else [btarget]
            else:
                targets = self.alive('enemy') if self.multi(s) else [btarget if btarget and not btarget.dead() else
                                                                        random.choice(self.alive('enemy') or [None])]
            for t in targets:
                if t is not None and not t.dead():
                    self.act(a, best, t)
        for _ in range(a.floats):
            foes = self.alive('enemy')
            if foes:
                self.act(a, FLOAT_SKILL, random.choice(foes))

    def enemy_turn(self, e):
        acts = e.data['actions']
        if not acts:
            return
        rmax = max(x['rating'] for x in acts)
        zero = rmax - 3
        acts = [x for x in acts if x['rating'] > zero]
        n = 1 + ROLE_ACTIONS.get(e.rk['role'], 0)
        for _ in range(n):
            if e.dead() or not self.alive('party'):
                return
            tot = sum(x['rating'] - zero for x in acts)
            r = random.uniform(0, tot)
            for x in acts:
                r -= x['rating'] - zero
                if r <= 0:
                    break
            sid = x['skillId']
            s = SK[sid]
            reps = 1 + (ROLE_ATTACKS.get(e.rk['role'], 0) if sid == 1 else 0) + max(0, s['repeats'] - 1)
            for _ in range(reps):
                if s['scope'] in (2, 8, 10, 14):
                    targets = self.alive('party') if s['scope'] == 2 else []
                elif s['scope'] in (7, 11, 0):
                    targets = []
                elif s['scope'] in (3, 4, 5, 6):           # 1-4 random targets (MZ draws each one anew)
                    alive = self.alive('party')
                    targets = [random.choice(alive) for _ in range(s['scope'] - 2)] if alive else []
                else:
                    targets = [random.choice(self.alive('party'))] if self.alive('party') else []
                for t in targets:
                    if not t.dead():
                        self.act(e, sid, t)

    def breakthrough(self):
        """A scripted breakthrough (troop page): the party rises a rank, one level, and is healed."""
        self.broke = True
        new = self.rebuild()
        self.party[:] = new
        for a in self.party:
            a.hp, a.mp = a.mhp, a.mmp
            a.used_unbroken = a.held = a.riposted = False

    def check(self):
        if not self.enemies:
            return None
        boss = self.enemies[0] if len(self.enemies) == 1 else max(self.enemies, key=lambda e: e.mhp)
        if self.bt_hp is not None and not self.broke and boss.hp <= boss.mhp * self.bt_hp:
            self.breakthrough()
        if self.yield_hp is not None and boss.hp <= boss.mhp * self.yield_hp:
            return 'win'
        return None

    def run(self, max_turns=40):
        while self.turn < max_turns:
            self.turn += 1
            if self.bt_turn is not None and self.turn == self.bt_turn and not self.broke:
                self.breakthrough()
            if self.end_turn is not None and self.turn >= self.end_turn:
                return 'win'
            for a in self.party:
                a.riposted = False
            order = [(random.randint(1, 20) + mod(b.stat('DEX')) + random.random(), b)
                     for b in self.party + self.enemies if not b.dead()]
            order.sort(key=lambda x: -x[0])
            for _, b in order:
                if b.dead():
                    continue
                if isinstance(b, Actor):
                    if b not in self.party:
                        continue          # replaced by a breakthrough this round
                    self.actor_turn(b)
                else:
                    self.enemy_turn(b)
                if self.check() == 'win':
                    return 'win'
                if not self.alive('enemy'):
                    return 'win'
                if not self.alive('party'):
                    return 'lose'
            for a in self.alive('party'):
                if a.regen:
                    a.hp = min(a.mhp, a.hp + round(a.mhp * (a.rnk + 1) * a.regen))
        return 'timeout'


def user_hit(b):
    return b.hit_bonus if isinstance(b, Actor) else b.rk['hit']
def user_crit(b):
    return b.crit_bonus if isinstance(b, Actor) else b.rk['crit']


# ------------------------------------------------------------------------------------------------ party building
def build_party(level, walls, members=(1, 2, 3), guests=(), falin=15):
    """As scen_story_bal2.js: breakthroughs at the wall levels, points spent after every step."""
    gate = 0
    k, h, f = Actor(1), Actor(2), Actor(3)
    party = [k, h]
    steps = sorted([(w, True) for w in walls] + [(level, False)])
    for L, bt in steps:
        if L >= falin and f not in party and 3 in members:
            party.append(f)
            f.change_level(L)
            f.spend(gate)
        if k.level < L:
            k.change_level(L)
        h.change_level(k.level)
        if f in party and f.level < L:
            f.change_level(L)
        k.spend(gate)
        h.spend(gate)
        if f in party:
            f.spend(gate)
        if bt:
            gate += 1
            for a in party:
                for i in a.top3(gate):
                    v = a.base(i, gate)
                    if v < gate * 100:
                        a.bonus[i] += gate * 100 - v
            k.change_level(k.level + 1)
            h.change_level(k.level)
            if f in party:
                f.change_level(f.level + 1)
            k.spend(gate)
            h.spend(gate)
            if f in party:
                f.spend(gate)
    for g in guests:
        a = Actor(g)
        a.change_level(level)
        a.spend(gate)
        party.append(a)
    party = [a for a in party if a.id in members or a.id in guests]
    auras = set()
    for a in party:
        a.learn(gate)
        for sid in a.skills:
            auras.update(SK[sid]['rk']['aura'])
    for a in party:
        a.prepare(gate, auras)
    return party, gate


def troop_id(name):
    for t in D['Troops']:
        if t and t['name'] == name:
            return t['id']
    raise KeyError(name)


def simulate(level, walls, troops, n=200, regalia=0, guests=(), members=(1, 2, 3), seed=1, show=False,
             bt_turn=None, bt_hp=None, yield_hp=None, end_turn=None, **_):
    random.seed(seed)
    out = []
    rebuild = lambda: build_party(level, list(walls) + [level], members, guests)[0]
    party, gate = build_party(level, walls, members, guests)
    if show:
        for a in party:
            print(f'    {a.name:7} L{a.level} {LETTERS[a.rnk]} HP{a.mhp} MP{a.mmp} AC{a.ac} ' +
                  ' '.join(f'{s}{v}' for s, v in zip(STATS, a.stats)))
    for t in troops:
        wins = turns = 0
        hp = 0.0
        for _ in range(n):
            party, gate = build_party(level, walls, members, guests)
            b = Battle(party, troop_id(t), regalia, bt_turn=bt_turn, bt_hp=bt_hp, rebuild=rebuild, yield_hp=yield_hp,
                       end_turn=end_turn)
            r = b.run()
            turns += b.turn
            if r == 'win':
                wins += 1
                hp += sum(max(0, a.hp) / a.mhp for a in party) / len(party)
        out.append((t, wins / n, turns / n, hp / wins if wins else 0))
    return out, party, gate


# ------------------------------------------------------------------------------------------------ scenarios
# walls: the levels the story breaks through at: E 12, D ~21 (the Messingvogt, end of ch.4), C ~30 (Gōen at the
# Aschenlager), B ~38 (Tsumugi), A ~50 (Gōen in the Urwald).
SCENARIOS = {
    'ch4 (reference: the engine runs in the build journal)': [
        dict(level=16, walls=[12], kind='reference', troops=['Höllenhund', 'Raid: Aschenhunde', 'Ghule x3', 'Messinggolems x2', 'Messingschreiber']),
        dict(level=19, walls=[12], troops=['Gargyl', 'Gargyl & Aschenhund', 'Gargylen x2', 'Gargyl & Aschenhunde']),
    ],
}


def load_scenarios():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'balance_scenarios.json')
    if os.path.exists(p):
        for k, v in json.load(open(p, encoding='utf-8')).items():
            SCENARIOS[k] = v


if __name__ == '__main__':
    load_scenarios()
    names = [a for a in sys.argv[1:] if not a.startswith('-')]
    show = '--show' in sys.argv
    n = 200
    for arg in sys.argv[1:]:
        if arg.startswith('-n'):
            n = int(arg[2:])
    for name, runs in SCENARIOS.items():
        if names and not any(x in name for x in names):
            continue
        print('==', name)
        for c in runs:
            kw = {k: v for k, v in c.items() if k not in ('level', 'walls', 'troops', 'n')}
            res, party, gate = simulate(c['level'], c.get('walls', []), c['troops'], n=c.get('n', n), show=show, **kw)
            for t, w, tu, hp in res:
                print(f'  L{c["level"]:<3}{LETTERS[gate]:>2}  {c.get("kind", ""):16} {t:30} win {w * 100:5.1f}%  '
                      f'turns {tu:4.1f}  hp left {hp * 100:4.0f}%', flush=True)
