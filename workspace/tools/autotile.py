"""Autotile shapes the way the RPG Maker editor picks them (checked against the story maps: tools/autotile.py --check).

Floor autotiles (A1 water, A2 ground, A4 wall tops) pick one of 48 shapes from their 8 neighbours; walls (A3,
A4 wall faces) one of 16 from their 4 neighbours; waterfalls (odd A1 kinds from 5 on) one of 4 from left/right.
A neighbour "joins" when it holds an autotile of the same kind on the same layer, or lies off the map.
"""
from maprender import FLOOR, WALL, WATERFALL, A1, A2, A3, A4, is_a1, is_a3, is_a4, kind

# quarter a corner uses for: (both sides join & diagonal joins, diagonal missing, only vertical side joins,
# only horizontal side joins, neither)
_Q = {0: {'in': (2, 4), 'corner': (2, 0), 'v': (0, 4), 'h': (2, 2), 'out': (0, 2)},
      1: {'in': (1, 4), 'corner': (3, 0), 'v': (3, 4), 'h': (1, 2), 'out': (3, 2)},
      2: {'in': (2, 3), 'corner': (2, 1), 'v': (0, 3), 'h': (2, 5), 'out': (0, 5)},
      3: {'in': (1, 3), 'corner': (3, 1), 'v': (3, 3), 'h': (1, 5), 'out': (3, 5)}}
_FLOOR_INDEX = {tuple(tuple(q) for q in qs): i for i, qs in enumerate(FLOOR)}


def kind_role(k):
    """'floor', 'wall' or 'waterfall' for an autotile kind."""
    if k < 16:
        return 'waterfall' if k >= 5 and k % 2 == 1 else 'floor'
    if k < 48:
        return 'floor'
    if k < 80:
        return 'wall'
    ty = k // 8
    return 'wall' if ty % 2 == 1 else 'floor'


def floor_shape(j):
    """j(dx, dy) -> True when that neighbour joins."""
    n, s, w, e = j(0, -1), j(0, 1), j(-1, 0), j(1, 0)
    quarters = []
    for i, (dx, dy, vert, horz) in enumerate([(-1, -1, w, n), (1, -1, e, n), (-1, 1, w, s), (1, 1, e, s)]):
        # vert: the side neighbour (left/right); horz: the up/down neighbour
        if vert and horz:
            q = _Q[i]['in'] if j(dx, dy) else _Q[i]['corner']
        elif horz:
            q = _Q[i]['v']          # up/down joins, the side doesn't: a side edge
        elif vert:
            q = _Q[i]['h']          # the side joins, up/down doesn't: a top/bottom edge
        else:
            q = _Q[i]['out']
        quarters.append(q)
    return _FLOOR_INDEX.get(tuple(quarters), 0)


def wall_shape(j):
    return (0 if j(-1, 0) else 1) | (0 if j(0, -1) else 2) | (0 if j(1, 0) else 4) | (0 if j(0, 1) else 8)


def waterfall_shape(j):
    return (0 if j(-1, 0) else 1) | (0 if j(1, 0) else 2)


def shape_for(k, j):
    role = kind_role(k)
    if role == 'wall':
        return wall_shape(j)
    if role == 'waterfall':
        return waterfall_shape(j)
    return floor_shape(j)


def base_id(k):
    return A1 + k * 48


def refresh(m, z, cells=None):
    """Recomputes the shapes of the autotiles on layer z (all cells, or just `cells` and their neighbours)."""
    w, h = m['width'], m['height']
    d = m['data']
    idx = lambda x, y: (z * h + y) * w + x
    def k_at(x, y):
        if not (0 <= x < w and 0 <= y < h):
            return None
        t = d[idx(x, y)]
        return kind(t) if t >= A1 else -1
    todo = set()
    if cells is None:
        todo = {(x, y) for y in range(h) for x in range(w)}
    else:
        for (x, y) in cells:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        todo.add((x + dx, y + dy))
    new = {}
    for (x, y) in todo:
        t = d[idx(x, y)]
        if t < A1:
            continue
        k = kind(t)
        def j(dx, dy, x=x, y=y, k=k):
            kk = k_at(x + dx, y + dy)
            return kk is None or kk == k
        new[(x, y)] = base_id(k) + shape_for(k, j)
    for (x, y), t in new.items():
        d[idx(x, y)] = t


def check(paths):
    import json
    from collections import Counter
    total, bad = 0, Counter()
    for p in paths:
        m = json.load(open(p, encoding='utf-8'))
        w, h = m['width'], m['height']
        orig = list(m['data'])
        for z in range(4):
            refresh(m, z)
        for z in range(4):
            for i in range(w * h):
                t0 = orig[z * w * h + i]
                if t0 >= A1:
                    total += 1
                    if m['data'][z * w * h + i] != t0:
                        bad[(kind_role(kind(t0)), 'A1' if t0 < A2 else 'A2' if t0 < A3 else 'A3' if t0 < A4 else 'A4')] += 1
    print('autotile cells', total, 'mismatches', sum(bad.values()), dict(bad))


if __name__ == '__main__':
    import sys, glob
    check(sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else '../story/out/data/Map0*.json')))
