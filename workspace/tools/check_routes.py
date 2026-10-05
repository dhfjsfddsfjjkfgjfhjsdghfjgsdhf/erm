"""Static check of the scripted movement routes in the built maps (story/out): a "Set Movement Route" that waits for
completion and isn't skippable hangs the game for good if one of its steps can't be taken (a wall, another event
on the target tile, a jump without coordinates). This walks every such route from where its character stands and
reports the steps that would block.

Rules mirrored from MZ: a moving event is stopped by any other event on the target tile (Game_Event
.isCollidedWithEvents), the player only by events of normal priority; "Through ON" (code 37) lifts both;
directional passability of both tiles (tools/mapinfo.can_move).
usage: python3 tools/check_routes.py [--strict] [map ids...]"""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
import mapinfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get('STORY_OUT', ROOT + '/story/out')
STRICT = '--strict' in sys.argv      # also report skippable and non-waiting routes (they don't hang, they misplace)
DIRS = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}
MOVE = {1: 2, 2: 4, 3: 6, 4: 8}
TURN = {16: 2, 17: 4, 18: 6, 19: 8}
REV = {2: 8, 8: 2, 4: 6, 6: 4}


def check_map(path):
    m = json.load(open(path, encoding='utf-8'))
    mid = int(os.path.basename(path)[3:6])
    ok, flags = mapinfo.walk_grid(m)
    events = {e['id']: e for e in m['events'] if e}
    issues = []

    def blockers(x, y, mover):
        out = []
        for e in events.values():
            if e['id'] == mover or (e['x'], e['y']) != (x, y):
                continue
            pages = e['pages']
            if all(p['through'] for p in pages):
                continue
            if mover == -1 and not any(p['priorityType'] == 1 for p in pages):
                continue
            out.append(e['name'])
        return out

    for e in events.values():
        for pi, page in enumerate(e['pages']):
            pos = {}
            look = {}
            for i, c in enumerate(page['list']):
                if c['code'] == 203 and c['parameters'][1] == 0:       # set event location (direct)
                    ch = c['parameters'][0] or e['id']
                    pos[ch] = (c['parameters'][2], c['parameters'][3])
                    continue
                if c['code'] != 205:
                    continue
                ch, route = c['parameters']
                ch = e['id'] if ch == 0 else ch
                if ch == -1:
                    continue        # the player's position isn't known statically (and its routes are skippable)
                if ch not in events:
                    issues.append(f"map {mid} event {e['id']} '{e['name']}' p{pi + 1} #{i}: route for missing event {ch}")
                    continue
                tgt = events[ch]
                x, y = pos.get(ch, (tgt['x'], tgt['y']))
                d = look.get(ch, tgt['pages'][0]['image']['direction'] or 2)
                through = any(p['through'] for p in tgt['pages'][:1])
                dfix = tgt['pages'][0]['directionFix']
                waits = (route.get('wait') and not route.get('skippable')) or STRICT
                for step in route['list']:
                    code, prm = step['code'], step['parameters']
                    want = None
                    if code in MOVE:
                        want = MOVE[code]
                        if not dfix:
                            d = want
                    elif code == 12:
                        want = d
                    elif code == 13:
                        want = REV[d]
                    elif code in TURN:
                        if not dfix:
                            d = TURN[code]
                    elif code == 14:
                        if len(prm) < 2 or not all(isinstance(v, int) for v in prm[:2]):
                            issues.append(f"map {mid} event {e['id']} '{e['name']}' p{pi + 1} #{i}: '{tgt['name']}' "
                                          f"jumps without coordinates ({prm}): the route never ends")
                            break
                        x, y = x + prm[0], y + prm[1]
                    elif code == 35:
                        dfix = True
                    elif code == 36:
                        dfix = False
                    elif code == 37:
                        through = True
                    elif code == 38:
                        through = False
                    elif code in (5, 6, 7, 8, 9, 10, 11, 23, 24, 25, 26) and waits:
                        issues.append(f"map {mid} event {e['id']} '{e['name']}' p{pi + 1} #{i}: '{tgt['name']}' "
                                      f"route code {code} can't be checked statically")
                    if want is None:
                        continue
                    dx, dy = DIRS[want]
                    nx, ny = x + dx, y + dy
                    if not through:
                        why = None
                        if not mapinfo.can_move(m, flags, x, y, want):
                            why = 'wall'
                        else:
                            b = blockers(nx, ny, ch)
                            if b:
                                why = 'event ' + '/'.join(b)
                        if why:
                            if waits:
                                issues.append(f"map {mid} event {e['id']} '{e['name']}' p{pi + 1} #{i}: '{tgt['name']}' "
                                              f"can't step {x},{y} -> {nx},{ny} ({why}): the scene waits forever")
                            break
                    x, y = nx, ny
                pos[ch] = (x, y)
                look[ch] = d
    return issues


if __name__ == '__main__':
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()]
    files = sorted(glob.glob(OUT + '/data/Map[0-9][0-9][0-9].json'))
    issues = []
    for f in files:
        if ids and int(os.path.basename(f)[3:6]) not in ids:
            continue
        issues += check_map(f)
    for s in issues:
        print('ROUTE', s)
    print('route problems:', len(issues))
