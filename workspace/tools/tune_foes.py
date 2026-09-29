"""Finds enemy HP for the Act II-III fights with tools/battle_sim.py, against the difficulty the story wants:
regular encounters fairly difficult, mid-bosses hard, bosses very difficult (auto-battle win rates in the sim,
which runs about 20 points harsher than the engine on boss fights: the Messingvogt is 66% here, 88% there).
Prints the HP each enemy should get; tools/story/foes.py and foes3.py take the numbers by hand.
usage: python3 tools/tune_foes.py [chapter filter]"""
import sys, math, os
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
import battle_sim as B

TARGET = {                     # rounds, and then: regular -> party HP left after a win; others -> win rate
    'regular': dict(turns=(4.5, 6.5), key='hp', band=(0.42, 0.60)),
    'mid': dict(turns=(7, 10), key='win', band=(0.55, 0.75)),
    'boss': dict(turns=(10, 15), key='win', band=(0.35, 0.50)),
}
# ranks the tuning assumes (enemies a rank above the party with no regalia to pierce them: ×0.5 dealt, ×1.5
# taken, and one more action as bosses; they sit at the party's rank instead)
RANKS = {'Aschenschmied': 'D', 'Der Eiserne Prinz': 'D', 'Messingsoldat': 'D', 'Oni-Söldner': 'D',
         'Oni-Hauptmann': 'D', 'Seelenkessel': 'D', 'Arenabestie': 'C', 'Klingenmeisterin': 'C',
         'Kampfmagier': 'C', 'Schattenklinge': 'C', 'Kanemoto Gōki': 'C', 'Fomorer-Häuptling': 'B'}

W5 = dict(walls=[12, 20])
W7 = dict(walls=[12, 20, 30], guests=[6])
W8 = dict(walls=[12, 20, 30, 37], guests=[6])
WA = dict(walls=[12, 20, 30, 37, 48], guests=[6])
PLAN = [
    # ch.5  Grauklamm, Weißenfels (party D)
    ('ch5', ['Wyvern'], 'Wyverns x2', 'regular', dict(level=22, **W5)),
    ('ch5', ['Vampirknecht'], 'Vampirknechte x2', 'regular', dict(level=24, **W5)),
    ('ch5', ['Leere Hülle'], 'Leere Hüllen x2', 'regular', dict(level=24, **W5)),
    ('ch5', ['Messingkoloss'], 'Hülle & Koloss', 'regular', dict(level=24, **W5)),
    ('ch5', ['Aschenschmied'], 'Aschenschmied', 'boss', dict(level=25, **W5)),
    ('ch5', ['Der Eiserne Prinz'], 'Der Eiserne Prinz', 'boss', dict(level=26, walls=[12, 20], guests=[5])),
    # ch.6  the siege (party D)
    ('ch6', ['Messingsoldat'], 'Messingsoldaten x3', 'regular', dict(level=28, **W5)),
    ('ch6', ['Oni-Söldner'], 'Oni x2', 'regular', dict(level=28, **W5)),
    ('ch6', ['Oni-Hauptmann'], 'Oni-Hauptmann', 'mid', dict(level=28, **W5)),
    ('ch6', ['Seelenkessel'], 'Seelenkessel', 'boss', dict(level=30, **W5)),
    # ch.7  Lichtenhall (party C, Yukino)
    ('ch7', ['Straßenräuber'], 'Straßenräuber x3', 'regular', dict(level=33, **W7)),
    ('ch7', ['Spinnenkreis-Agent'], 'Agenten x2', 'regular', dict(level=33, **W7)),
    ('ch7', ['Sturmharpyie'], 'Sturmharpyien x2', 'regular', dict(level=33, **W7)),
    ('ch7', ['Eiserner Bruder', 'Arena-Söldner'], 'Runde 1: Eiserne Brüder', 'regular', dict(level=34, **W7)),
    ('ch7', ['Arenabestie'], 'Runde 2: Arenabestie', 'mid', dict(level=34, **W7)),
    ('ch7', ['Klingenmeisterin', 'Kampfmagier', 'Schattenklinge'], 'Runde 3: Klingen von Ostmark', 'mid',
     dict(level=34, **W7)),
    ('ch7', ['Kanemoto Gōki'], 'Finale: Kanemoto Gōki', 'boss', dict(level=35, **W7)),
    ('ch7', ['Höhlenspinne'], 'Höhlenspinnen x3', 'regular', dict(level=36, **W7)),
    ('ch7', ['Spinnenkreis-Klinge'], 'Spinnenkreis-Klingen x2', 'regular', dict(level=36, **W7)),
    ('ch7', ['Tsumugi'], 'Tsumugi', 'boss', dict(level=37, bt_turn=2, **W7)),
    # ch.8  Tiefenwald, Eisenberg (party B)
    ('ch8', ['Werwolf'], 'Werwölfe x2', 'regular', dict(level=40, regalia=1, **W8)),
    ('ch8', ['Irrlicht'], 'Werwolf & Irrlichter', 'regular', dict(level=40, regalia=1, **W8)),
    ('ch8', ['Junger Kitsune'], 'Kitsune x2', 'regular', dict(level=40, regalia=1, **W8)),
    ('ch8', ['Rudelherr'], 'Rudelherr', 'mid', dict(level=41, regalia=1, **W8)),
    ('ch8', ['Shirogane'], 'Shirogane', 'mid', dict(level=41, regalia=1, yield_hp=0.4, **W8)),
    ('ch8', ['Grubenwicht'], 'Grubenwichte x3', 'regular', dict(level=42, regalia=2, **W8)),
    ('ch8', ['Höhlentroll'], 'Höhlentrolle x2', 'regular', dict(level=42, regalia=2, **W8)),
    ('ch8', ['Trollschamane'], 'Troll & Schamane', 'regular', dict(level=42, regalia=2, **W8)),
    ('ch8', ['Trollkönig'], 'Trollkönig', 'boss', dict(level=43, regalia=2, **W8)),
    ('ch8', ['Urwaldhüter'], 'Urwaldhüter x2', 'regular', dict(level=44, regalia=3, **W8)),
    ('ch8', ['Waldgeist'], 'Hüter & Geister', 'regular', dict(level=44, regalia=3, **W8)),
    ('ch8', ['Hohler Diener'], 'Hohle Diener x3', 'regular', dict(level=44, regalia=3, **W8)),
    ('ch8', ['Leerer Magier'], 'Magier & Diener', 'regular', dict(level=44, regalia=3, **W8)),
    ('ch8', ['Grimoire'], 'Grimoires & Magier', 'regular', dict(level=44, regalia=3, **W8)),
    ('ch8', ['Mukuro'], 'Mukuro', 'boss', dict(level=45, regalia=3, **W8)),
    # ch.9  the sea, the fire, the end (party B, A after Gōen)
    ('ch9', ['Ertrunkener'], 'Ertrunkene x3', 'regular', dict(level=46, regalia=3, **W8)),
    ('ch9', ['Sirene'], 'Sirenen x2', 'regular', dict(level=46, regalia=3, **W8)),
    ('ch9', ['Riffkrabbe'], 'Krabben x2', 'regular', dict(level=46, regalia=3, **W8)),
    ('ch9', ['Fomorer'], 'Fomorer x2', 'regular', dict(level=46, regalia=3, **W8)),
    ('ch9', ['Ketos'], 'Ketos', 'mid', dict(level=46, regalia=3, **W8)),
    ('ch9', ['Fomorer-Häuptling'], 'Fomorer-Häuptling', 'boss', dict(level=47, regalia=3, **W8)),
    ('ch9', ['Shigure', 'Kraken'], 'Shigure', 'boss', dict(level=47, regalia=4, **W8)),
    ('ch9', ['Glutsalamander'], 'Salamander x2', 'regular', dict(level=48, regalia=4, **W8)),
    ('ch9', ['Aschenphönix'], 'Phönix & Salamander', 'regular', dict(level=48, regalia=4, **W8)),
    ('ch9', ['Messinggardist'], 'Gardisten x2', 'regular', dict(level=48, regalia=4, **W8)),
    ('ch9', ['Gōen, der Messingtyrann'], 'Gōen (Urwald)', 'boss', dict(level=48, regalia=4, bt_hp=0.5, **W8)),
    ('ch9', ['Maō Kagerō'], 'Kagerō', 'boss', dict(level=49, regalia=4, **WA)),
    ('ch9', ['Hōkais Schatten'], 'Hōkais Schatten', 'boss', dict(level=49, regalia=4, **WA)),
]


def base_hp(name):
    return next(e for e in B.D['Enemies'] if e and e['name'] == name)['params'][0]


def measure(troop, cfg, n):
    kw = {k: v for k, v in cfg.items() if k not in ('level', 'walls')}
    res, _, _ = B.simulate(cfg['level'], cfg['walls'], [troop], n=n, **kw)
    return res[0]


def nice(v):
    step = 10 if v < 1000 else 50 if v < 5000 else 100
    return int(round(v / step) * step)


def logit(p):
    p = min(0.98, max(0.02, p))
    return math.log(p / (1 - p))


def tune(names, troop, kind, cfg, n=int(os.environ.get('N', 60)), steps=int(os.environ.get('STEPS', 14))):
    """Two levers: HP sets how long the fight lasts, the offence factor (STR, DEX, INT, MAG) how much it hurts."""
    T = TARGET[kind]
    t_lo, t_hi = T['turns']
    b_lo, b_hi = T['band']
    t_mid, b_mid = (t_lo + t_hi) / 2, (b_lo + b_hi) / 2
    base = {nm: B.OVERRIDE.get(nm, {}).get('hp', base_hp(nm)) for nm in names}
    hp_m, atk = 1.0, B.OVERRIDE.get(names[0], {}).get('atk', 1.0)
    def run(hp_m, atk, n):
        for nm in names:
            o = B.OVERRIDE.setdefault(nm, {})
            o['hp'] = max(10, nice(base[nm] * hp_m))
            o['atk'] = round(atk, 3)
        t, win, turns, hp = measure(troop, cfg, n)
        return win, turns, hp
    best = None
    for _ in range(steps):
        win, turns, hp = run(hp_m, atk, n)
        val = hp if T['key'] == 'hp' else win
        miss = (abs(turns - t_mid) / (t_hi - t_lo) + abs(val - b_mid) / (b_hi - b_lo) +
                (5 * (0.97 - win) / 0.1 if T['key'] == 'hp' and win < 0.97 else 0))
        if best is None or miss < best[0]:
            best = (miss, hp_m, atk)
        ok_turns = t_lo <= turns <= t_hi
        ok_val = b_lo <= val <= b_hi and (T['key'] != 'hp' or win >= 0.97)
        if ok_turns and ok_val:
            break
        if not ok_turns:
            hp_m *= clamp_f((t_mid / max(turns, 0.5)) ** 0.7, 0.6, 1.7)
        if not ok_val:
            if T['key'] == 'hp':
                taken, want = (1 - hp) if win >= 0.97 else 1.0, 1 - b_mid
                atk *= clamp_f((want / max(taken, 0.05)) ** 0.5, 0.8, 1.25)
            else:
                atk *= clamp_f(math.exp(0.2 * (logit(win) - logit(b_mid))), 0.85, 1.18)
        atk = clamp_f(atk, 0.4, 2.5)
        hp_m = clamp_f(hp_m, 0.1, 8.0)
    _, hp_m, atk = best
    win, turns, hp = run(hp_m, atk, 150)
    return {nm: B.OVERRIDE[nm]['hp'] for nm in names}, hp_m, atk, (win, turns, hp)


def tune_grid(names, troop, kind, cfg, n=60):
    """For steep fights: a few HP levels, and for each a bisection on the offence factor for the target result;
    keeps the HP whose fight length comes closest to the middle of the target rounds."""
    T = TARGET[kind]
    t_lo, t_hi = T['turns']
    b_lo, b_hi = T['band']
    b_mid, t_mid = (b_lo + b_hi) / 2, (t_lo + t_hi) / 2
    base = {nm: B.OVERRIDE.get(nm, {}).get('hp', base_hp(nm)) for nm in names}
    atk0 = B.OVERRIDE.get(names[0], {}).get('atk', 1.0)
    def run(hp_m, atk, n):
        for nm in names:
            o = B.OVERRIDE.setdefault(nm, {})
            o['hp'] = max(10, nice(base[nm] * hp_m))
            o['atk'] = round(atk, 3)
        _, win, turns, hp = measure(troop, cfg, n)
        return win, turns, hp
    cands = []
    for hp_m in (0.7, 0.85, 1.0, 1.2, 1.45):
        lo, hi = math.log(atk0 * 0.4), math.log(atk0 * 2.5)
        best = None
        for _ in range(7):
            a = math.exp((lo + hi) / 2)
            win, turns, hp = run(hp_m, a, n)
            val = hp if T['key'] == 'hp' else win
            if T['key'] == 'hp' and win < 0.97:
                val = 0
            d = abs(val - b_mid)
            if best is None or d < best[0]:
                best = (d, a, win, turns, hp)
            if val > b_mid:
                lo = math.log(a)          # too easy: more offence
            else:
                hi = math.log(a)
        d, a, win, turns, hp = best
        cands.append((d > (b_hi - b_lo) / 2, abs(turns - t_mid), hp_m, a))
    cands.sort()
    _, _, hp_m, atk = cands[0]
    win, turns, hp = run(hp_m, atk, 150)
    return {nm: B.OVERRIDE[nm]['hp'] for nm in names}, hp_m, atk, (win, turns, hp)


def clamp_f(v, a, b):
    return max(a, min(b, v))


ROLES = {'Grubenwicht': 'standard', 'Hohler Diener': 'standard', 'Irrlicht': 'standard'}
ACS = {'Shirogane': 30}


def load_pass(paths):
    """Starts from earlier results (lines printed by this script)."""
    import re
    for p in paths:
        for line in open(p, encoding='utf-8'):
            m = re.search(r' atk x([\d.]+) .*?%   (.*)$', line)
            if not m:
                continue
            for nm, old, new in re.findall(r'(.+?) (\d+)->(\d+)(?:, |$)', m.group(2).strip()):
                o = B.OVERRIDE.setdefault(nm.strip(), {})
                o['hp'] = int(new)
                o['atk'] = float(m.group(1))


if __name__ == '__main__':
    for nm, rank in RANKS.items():
        B.OVERRIDE.setdefault(nm, {})['rank'] = rank
    for nm, role in ROLES.items():
        B.OVERRIDE.setdefault(nm, {})['role'] = role
    for nm, ac in ACS.items():
        B.OVERRIDE.setdefault(nm, {})['ac'] = ac
    import glob, os
    if os.environ.get('PASS'):
        load_pass(sorted(glob.glob(os.environ['PASS'])))
    only = [t for t in os.environ.get('ONLY', '').split('|') if t]
    flt = ARGS[0] if ARGS else ''
    for ch, names, troop, kind, cfg in PLAN:
        if flt and ch not in flt.split(','):
            continue
        if only and troop not in only:
            continue
        fn = tune_grid if os.environ.get('GRID') else tune
        hps, m, atk, (win, turns, hp) = fn(names, troop, kind, cfg)
        now = ', '.join(f'{nm} {base_hp(nm)}->{hps[nm]}' for nm in names)
        print(f'{ch} {kind:7} {troop:30} hp x{m:4.2f} atk x{atk:4.2f}  win {win * 100:3.0f}%  turns {turns:4.1f}  '
              f'hp left {hp * 100:3.0f}%   {now}', flush=True)
