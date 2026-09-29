import json, sys
from collections import deque
TS = json.load(open('/home/claude/mz/orig/data/Tilesets.json'))
def load(path):
    return json.load(open(path))
def tile(d, x, y, z):
    w, h = d['width'], d['height']
    return d['data'][(z * h + y) * w + x] or 0
def check_passage(d, flags, x, y, bit):
    for z in (3, 2, 1, 0):
        t = tile(d, x, y, z)
        f = flags[t] if t < len(flags) else 0
        if f & 0x10:  # star
            continue
        if (f & bit) == 0:
            return True
        if (f & bit) == bit:
            return False
    return False
def passable(d, flags, x, y, dirn):
    return check_passage(d, flags, x, y, (1 << (dirn // 2 - 1)) & 0x0f)
def walk_grid(d):
    flags = TS[d['tilesetId']]['flags']
    w, h = d['width'], d['height']
    ok = [[any(passable(d, flags, x, y, dd) for dd in (2,4,6,8)) for x in range(w)] for y in range(h)]
    return ok, flags
def can_move(d, flags, x, y, dirn):
    w, h = d['width'], d['height']
    dx = {4:-1, 6:1}.get(dirn, 0); dy = {2:1, 8:-1}.get(dirn, 0)
    x2, y2 = x + dx, y + dy
    if not (0 <= x2 < w and 0 <= y2 < h): return False
    rev = {2:8, 8:2, 4:6, 6:4}[dirn]
    return passable(d, flags, x, y, dirn) and passable(d, flags, x2, y2, rev)
def region(d, sx, sy, blocked=None):
    ok, flags = walk_grid(d)
    blocked = blocked or set()
    seen = {(sx, sy)}; q = deque([(sx, sy)])
    while q:
        x, y = q.popleft()
        for dd in (2,4,6,8):
            if can_move(d, flags, x, y, dd):
                dx = {4:-1, 6:1}.get(dd, 0); dy = {2:1, 8:-1}.get(dd, 0)
                n = (x+dx, y+dy)
                if n not in seen and n not in blocked:
                    seen.add(n); q.append(n)
    return seen
def ascii(d, marks=None, reg=None):
    ok, flags = walk_grid(d)
    w, h = d['width'], d['height']
    out = []
    for y in range(h):
        row = ''
        for x in range(w):
            c = '.' if ok[y][x] else '#'
            if reg is not None and (x, y) in reg: c = 'o'
            if marks and (x, y) in marks: c = marks[(x, y)]
            row += c
        out.append('%3d %s' % (y, row))
    head = '    ' + ''.join(str(x % 10) for x in range(w))
    return head + '\n' + '\n'.join(out)
if __name__ == '__main__':
    d = load(sys.argv[1])
    ev = {(e['x'], e['y']): 'E' for e in d['events'] if e}
    print(ascii(d, ev))

def exit_tiles(d):
    """Tiles holding touch events that transfer (the player never walks past them)."""
    out = set()
    for e in d['events']:
        if not e:
            continue
        for p in e['pages']:
            if p['trigger'] in (1, 2) and any(c['code'] == 201 for c in p['list']):
                out.add((e['x'], e['y']))
    return out
