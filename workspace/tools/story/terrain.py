"""Terrain presets for the generated maps (Acts II-III): canyons, framed fields, towns, camps, ruins, dungeons,
interiors. Everything is built on tools/mapgen.py; each builder returns a Gen whose .m is an MZ map."""
import math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from mapgen import Gen, OUT, DUN, INS, auto, objwide, Z_GROUND, Z_OVER, Z_LOW, Z_HIGH
import mapinfo

# ------------------------------------------------------------------------------------------------ small helpers
def walkable(g):
    ok, _ = mapinfo.walk_grid(g.m)
    return {(x, y) for y in range(g.h) for x in range(g.w) if ok[y][x]}


def spot(g, near, avoid=(), radius=10, need_free=True, region=None):
    """Nearest walkable cell to `near` that no object or event claims (inside `region` if given, e.g. the cells
    reachable from the map's entrance)."""
    ok = walkable(g) if region is None else set(region)
    x0, y0 = near
    best = None
    for r in range(radius + 1):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                c = (x0 + dx, y0 + dy)
                if c in ok and c not in avoid and (not need_free or c not in g.blocked):
                    d = abs(dx) + abs(dy)
                    if best is None or d < best[0]:
                        best = (d, c)
        if best:
            return best[1]
    raise ValueError(f'no free walkable cell near {near}')


def reach_check(g, start, targets, label=''):
    """Raises if any target (x, y) can't be reached from start (or stood next to, for blocking events)."""
    reg = mapinfo.region(g.m, *start)
    bad = []
    for t in targets:
        x, y = t
        if t in reg or any((x + dx, y + dy) in reg for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            continue
        bad.append(t)
    if bad:
        raise ValueError(f'{label}: unreachable from {start}: {bad}')
    return reg


# ------------------------------------------------------------------------------------------------ outdoor styles
SNOW = dict(ground=OUT.SNOW, road=OUT.SNOW_DIRT, bush=OUT.SBUSH, plateau=(119, 127), frame=OUT.SNOWFOREST,
            trees=[OUT.SNOWTREE, OUT.SNOWPINE, OUT.SNOWPINE], rocks=OUT.SNOWROCKS,
            tufts=[[(0, 0, 217)], [(0, 0, 218)], [(0, 0, 219)], [(0, 0, 220)], [(0, 0, 227)]])
GRASS = dict(ground=OUT.GRASS, road=OUT.GRASS_DIRT, bush=OUT.BUSH, plateau=(116, 124), frame=OUT.FOREST,
             trees=[OUT.TREE, OUT.PINE, OUT.PINE], rocks=OUT.ROCKS,
             tufts=[[(0, 0, 153)], [(0, 0, 155)], [(0, 0, 160)], [(0, 0, 161)], [(0, 0, 152)]])
ASH = dict(ground=OUT.DIRT, road=OUT.DIRT_STONES, bush=OUT.ABUSH, plateau=(118, 126), frame=(118, 126),
           trees=[OUT.DEADTREE, OUT.DEADTREE2], rocks=OUT.ROCKS,
           tufts=[[(0, 0, 252)], [(0, 0, 227)], [(0, 0, 224)]])
FOREST = dict(ground=OUT.GRASS, road=OUT.GRASS_DIRT, bush=OUT.BUSH, plateau=(116, 124), frame=OUT.DARKFOREST,
              trees=[OUT.TREE, OUT.TREE, OUT.PINE], rocks=OUT.ROCKS,
              tufts=[[(0, 0, 153)], [(0, 0, 155)], [(0, 0, 154)], [(0, 0, 162)], [(0, 0, 163)], [(0, 0, 246)]])


def frame(g, walk, style, thick=3, trunk_h=2, void=True):
    """Encloses `walk` in a band of forest/rock (top kind on layer 0) with trunk/wall faces hanging under its
    south edges; everything beyond the band is empty (black). Returns the cells that stay walkable ground."""
    top, wall = style['frame']
    band = g.grow(walk, thick, diag=True) - walk
    outside = g.all() - walk - band
    if void:
        for (x, y) in outside:
            for z in range(4):
                g.set(x, y, z, 0)
    g.paint(band | (outside if not void else set()), top, 0)
    ground = set(walk)
    for (x, y) in walk:
        if (x, y - 1) in band or (x, y - 1) in outside:
            for d in range(trunk_h):
                c = (x, y + d)
                if c in walk:
                    g.set(c[0], c[1], 0, auto(wall))
                    g.blocked.add(c)
                    ground.discard(c)
    return ground


def plateau(g, cells, style, height=2, must_floor=()):
    """A raised area: top kind on layer 1 over the ground, `height` rows of rock face under its south edge.
    Cells within `height` rows above a must_floor cell are dropped so no face lands on them."""
    cells = set(cells)
    for (x, y) in must_floor:
        for k in range(1, height + 1):
            cells.discard((x, y - k))
    top, wall = style['plateau']
    for (x, y) in cells:
        g.set(x, y, 1, auto(top))
        g.blocked.add((x, y))
    for (x, y) in cells:
        if (x, y + 1) not in cells:
            for d in range(1, height + 1):
                c = (x, y + d)
                if g.inside(*c) and c not in cells:
                    g.set(c[0], c[1], 0, auto(wall))
                    g.set(c[0], c[1], 1, 0)
                    g.blocked.add(c)
    return cells


def canyon(g, pts, width, style, wall_h=3, rim=4, wobble=1.5, road_w=2, seed=0, extra=()):
    """A canyon along the polyline pts (plus `extra` floor cells, e.g. side pockets): snow/grass floor between
    raised rock rims, void beyond the rims."""
    g.paint(g.all(), style['ground'], 0)
    floor = g.line(pts, width, wobble) | set(extra)
    road = g.line(pts, road_w, wobble) & floor
    rimcells = g.grow(floor, rim, diag=True) - floor
    for (x, y) in g.all() - floor - rimcells:
        for z in range(4):
            g.set(x, y, z, 0)
    plateau(g, rimcells, style, wall_h, must_floor=g.grow(road, 1))
    g.paint(road, style['road'], 0)
    g.keep_clear |= road
    return floor, road


def dress(g, cells, style, trees=0.06, rocks=0.02, bushes=0.04, tufts=0.05, seed=None):
    """Scatter the style's trees, rocks, bushes (layer 1 autotile) and tufts over `cells`."""
    rng = random.Random(seed if seed is not None else g.rng.random())
    cells = {c for c in cells if c not in g.blocked and c not in g.keep_clear}
    n = len(cells)
    g.scatter_in(cells, style['trees'], int(n * trees), spacing=1)
    g.scatter_in(cells, style['rocks'], int(n * rocks), spacing=1)
    free = [c for c in cells if c not in g.blocked]
    rng.shuffle(free)
    for c in free[:int(n * bushes)]:
        g.set(c[0], c[1], 1, auto(style['bush']))
    g.scatter_in([c for c in cells if c not in g.blocked and g.get(c[0], c[1], 1) == 0], style['tufts'],
                 int(n * tufts), spacing=0)


# ------------------------------------------------------------------------------------------------ buildings
ROOFS = {'wood': [[413, 414, 415], [421, 422, 423], [429, 430, 431]],
         'green': [[384, 385, 386], [392, 393, 394], [400, 401, 402]],
         'snow': [[389, 390, 391], [397, 398, 399], [405, 406, 407]],
         'gold': [[408, 409, 410], [416, 417, 418], [424, 425, 426]]}
WALLS = {'wood': 60, 'plaster': 56, 'stone': 57, 'brick': 58, 'marble': 72, 'grey': 73, 'darkbrick': 74,
         'moss': 75, 'logs': 62, 'snowbrick': 77, 'snowwood': 78}
DOORS = {'arch': 114, 'dark': 116, 'double': 122, 'gate': 107}
WINDOWS = [96, 112, 120, 98]


def house(g, x, y, w, roof='wood', wall='wood', door='arch', door_dx=None, windows=True, roof_h=3, wall_h=2):
    """A house: 9-slice roof (upper layer) over A3 walls; the door sits on the bottom wall row.
    Returns the door cell (put the door event there; the player touches it from below)."""
    R = ROOFS[roof]
    for dy in range(roof_h):
        row = R[0] if dy == 0 else (R[2] if dy == roof_h - 1 else R[1])
        for dx in range(w):
            g.set(x + dx, y + dy, 3, row[0] if dx == 0 else (row[2] if dx == w - 1 else row[1]))
    body = g.rect(x, y, x + w - 1, y + roof_h + wall_h - 1)
    g.paint(body, WALLS[wall], 0)
    for c in body:
        g.blocked.add(c)
    dx = door_dx if door_dx is not None else w // 2
    dc = (x + dx, y + roof_h + wall_h - 1)
    if door:
        g.set(dc[0], dc[1], 3, DOORS[door])
    if windows:
        wy = y + roof_h
        for wx in range(x + 1, x + w - 1):
            if abs(wx - dc[0]) >= 2 and (wx - x) % 2 == 1:
                g.set(wx, wy if wall_h > 1 else dc[1], 3, 120 if wall != 'wood' else 96)
    g.keep_clear.add((dc[0], dc[1] + 1))
    return dc


def ruin(g, x, y, w, h, wall='grey', seed=None, rubble=True):
    """A burnt-out house: a broken ring of wall stubs (A3 wall, one row), no roof, rubble inside."""
    rng = random.Random(seed if seed is not None else g.rng.random())
    cells = set()
    for dx in range(w):
        for dy in (0, h - 1):
            cells.add((x + dx, y + dy))
    for dy in range(h):
        cells.add((x, y + dy))
        cells.add((x + w - 1, y + dy))
    gap = (x + rng.randint(1, w - 2), y + h - 1)
    for c in cells:
        if c == gap or rng.random() < 0.25:
            continue
        g.set(c[0], c[1], 0, auto(WALLS[wall]))
        g.blocked.add(c)
    if rubble:
        inner = g.rect(x + 1, y + 1, x + w - 2, y + h - 2)
        for c in inner:
            if rng.random() < 0.3:
                g.set(c[0], c[1], 1, auto(OUT.CRACKS))
        g.scatter_in(inner, [[(0, 0, 250)], [(0, 0, 251)], [(0, 0, 159)], [(0, 0, 226)]], max(1, len(inner) // 5), 0)
    return gap


PILLAR = [(0, -2, 256), (0, -1, 264), (0, 0, 272)]            # Dungeon tileset: white column
PILLAR_SQ = [(0, -2, 257), (0, -1, 265), (0, 0, 273)]         # carved square pillar
PILLAR_CRYSTAL = [(0, -2, 261), (0, -1, 269), (0, 0, 277)]
TENT_WHITE = [(dx, dy - 2, 5 + dx + dy * 8) for dy in range(3) for dx in range(3)]
TENT_RED = [(dx, dy - 2, 29 + dx + dy * 8) for dy in range(3) for dx in range(3)]


def tent(g, x, y, red=False):
    """3x3 tent standing on (x..x+2, y); its door is (x+1, y)."""
    return g.stamp(x, y, TENT_RED if red else TENT_WHITE, z=3)


def campfire_spot(g, x, y):
    g.set(x, y, 1, 0)
    g.keep_clear.add((x, y))


# ------------------------------------------------------------------------------------------------ dungeons
def void_beyond(g, open_cells, ring=1):
    """Black beyond `ring` cells of ceiling around the open area (the RPG Maker dungeon look)."""
    keep = g.grow(open_cells, ring, diag=True)
    for c in g.all() - keep:
        for z in range(4):
            g.set(c[0], c[1], z, 0)


def rooms_and_halls(g, rooms, halls, top, wall, floor, wall_h=2, ring=1):
    """rooms: list of (x0, y0, x1, y1) floor rectangles (walls take their top wall_h rows); halls: polylines
    (list of points, width). Returns the open cells (walls included). Beyond `ring` cells of ceiling: black."""
    open_ = set()
    for (x0, y0, x1, y1) in rooms:
        open_ |= g.rect(x0, y0, x1, y1)
    for pts, w in halls:
        open_ |= g.line(pts, w)
    g.carve(open_, top, wall, floor, wall_h)
    if ring is not None:
        void_beyond(g, open_, ring)
    return open_


def cave(g, cells, top, wall, floor, wall_h=2, smooth=2, seed=None):
    """Organic cave: the given cells smoothed by a cellular pass, then carved."""
    rng = random.Random(seed if seed is not None else g.rng.random())
    cur = set(cells)
    for _ in range(smooth):
        nxt = set()
        for (x, y) in g.all():
            n = sum((x + dx, y + dy) in cur for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
            if ((x, y) in cur and n >= 3) or n >= 5:
                nxt.add((x, y))
        cur = nxt & g.rect(1, 1, g.w - 2, g.h - 2)
    g.carve(cur, top, wall, floor, wall_h)
    return cur


def interior(g, rooms, top, wall, floor, wall_h=2):
    """Inside tileset rooms: like rooms_and_halls, the outside of the rooms stays empty (black)."""
    open_ = set()
    for r in rooms:
        open_ |= g.rect(*r)
    g.carve(open_, top, wall, floor, wall_h)
    # black beyond one ring of ceiling
    ring = g.grow(open_, 1, diag=True)
    for c in g.all() - ring:
        g.set(c[0], c[1], 0, 0)
    return open_
