"""Map generator for the story maps of Acts II-III (no sample maps needed).

A Gen holds an MZ map (6 layers: 0-1 autotiles, 2-3 upper tiles, 4 shadows, 5 regions). Paint autotile kinds
into cell sets, stamp multi-tile objects, raise cliffs, carve dungeons; finish() recomputes every autotile's
shape (tools/autotile.py) and adds the wall shadows. The result is an ordinary map dict for MapBuild.
"""
import math, random
from autotile import refresh, kind_role
from maprender import A1, A5, kind

Z_GROUND, Z_OVER, Z_LOW, Z_HIGH, Z_SHADOW, Z_REGION = 0, 1, 2, 3, 4, 5


def auto(k):
    return A1 + k * 48


class Gen:
    def __init__(self, w, h, tileset, seed=1):
        self.w, self.h, self.tileset = w, h, tileset
        self.rng = random.Random(seed)
        self.m = {"autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "",
                  "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
                  "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
                  "disableDashing": False, "displayName": "", "encounterList": [], "encounterStep": 30,
                  "height": h, "note": "", "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": "",
                  "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0,
                  "specifyBattleback": False, "tilesetId": tileset, "width": w,
                  "data": [0] * (w * h * 6), "events": [None]}
        self.blocked = set()          # cells an object or wall already claims (for scatter)
        self.keep_clear = set()       # cells scatter must leave alone (paths, doors, event spots)

    # ------------------------------------------------------------------ raw access
    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def i(self, x, y, z):
        return (z * self.h + y) * self.w + x

    def get(self, x, y, z):
        return self.m['data'][self.i(x, y, z)] if self.inside(x, y) else 0

    def set(self, x, y, z, t):
        if self.inside(x, y):
            self.m['data'][self.i(x, y, z)] = t

    def kind_at(self, x, y, z=0):
        t = self.get(x, y, z)
        return kind(t) if t >= A1 else None

    # ------------------------------------------------------------------ cell sets
    def rect(self, x0, y0, x1, y1):
        """Inclusive rectangle."""
        return {(x, y) for y in range(max(0, y0), min(self.h - 1, y1) + 1)
                for x in range(max(0, x0), min(self.w - 1, x1) + 1)}

    def all(self):
        return self.rect(0, 0, self.w - 1, self.h - 1)

    def ellipse(self, cx, cy, rx, ry):
        return {(x, y) for (x, y) in self.rect(int(cx - rx) - 1, int(cy - ry) - 1, int(cx + rx) + 1, int(cy + ry) + 1)
                if ((x - cx) / max(rx, 0.5)) ** 2 + ((y - cy) / max(ry, 0.5)) ** 2 <= 1.0}

    def blob(self, cx, cy, r, rough=0.35, seed=None):
        """An irregular round patch."""
        rng = random.Random(seed if seed is not None else self.rng.random())
        phase = [rng.random() * 6.28 for _ in range(3)]
        out = set()
        for (x, y) in self.rect(int(cx - r * 1.6) - 1, int(cy - r * 1.6) - 1, int(cx + r * 1.6) + 1, int(cy + r * 1.6) + 1):
            a = math.atan2(y - cy, x - cx)
            rr = r * (1 + rough * (0.5 * math.sin(3 * a + phase[0]) + 0.3 * math.sin(5 * a + phase[1]) +
                                   0.2 * math.sin(7 * a + phase[2])))
            if math.hypot(x - cx, y - cy) <= rr:
                out.add((x, y))
        return out

    def line(self, pts, width=1, wobble=0.0):
        """A path through points (polyline), `width` cells wide; wobble bends it a little."""
        out = set()
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0), 1) * 2
            ph = self.rng.random() * 6.28
            for s in range(n + 1):
                t = s / n
                x = x0 + (x1 - x0) * t
                y = y0 + (y1 - y0) * t
                if wobble:
                    off = wobble * math.sin(t * 6.28 * 1.5 + ph)
                    if abs(x1 - x0) > abs(y1 - y0):
                        y += off
                    else:
                        x += off
                for dy in range(-(width // 2), width - width // 2):
                    for dx in range(-(width // 2), width - width // 2):
                        cx, cy = int(round(x)) + dx, int(round(y)) + dy
                        if self.inside(cx, cy):
                            out.add((cx, cy))
        return out

    def border(self, cells):
        """Cells of `cells` with a 4-neighbour outside it."""
        return {(x, y) for (x, y) in cells if any((x + dx, y + dy) not in cells
                                                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}

    def grow(self, cells, n=1, diag=False):
        out = set(cells)
        for _ in range(n):
            add = set()
            for (x, y) in out:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) + (((1, 1), (1, -1), (-1, 1), (-1, -1)) if diag else ()):
                    if self.inside(x + dx, y + dy):
                        add.add((x + dx, y + dy))
            out |= add
        return out

    def noise_cells(self, density, cells=None, seed=None):
        rng = random.Random(seed if seed is not None else self.rng.random())
        return {c for c in (cells if cells is not None else self.all()) if rng.random() < density}

    # ------------------------------------------------------------------ painting
    def paint(self, cells, k, z=0):
        """Autotile kind k (or a plain tile id when k >= 256 is not an autotile kind: pass tile=...) on layer z."""
        for (x, y) in cells:
            self.set(x, y, z, auto(k))

    def tile(self, cells, t, z=2):
        for (x, y) in cells:
            self.set(x, y, z, t)

    def clear(self, cells, z):
        for (x, y) in cells:
            self.set(x, y, z, 0)

    def region(self, cells, rid):
        for (x, y) in cells:
            self.set(x, y, Z_REGION, rid)

    # ------------------------------------------------------------------ objects
    def fits(self, cells):
        return all(self.inside(x, y) and (x, y) not in self.blocked and (x, y) not in self.keep_clear for (x, y) in cells)

    def stamp(self, x, y, obj, z=None, force=False, claim=True):
        """obj: list of (dx, dy, tile) or (dx, dy, tile, z). Blocks the footprint's lowest row (objects stand
        there) unless the tile is a star tile."""
        cells = [(x + o[0], y + o[1]) for o in obj]
        if not force and not self.fits(cells):
            return False
        for o in obj:
            zz = o[3] if len(o) > 3 else (z if z is not None else Z_HIGH)
            self.set(x + o[0], y + o[1], zz, o[2])
        if claim:
            for c in cells:
                self.blocked.add(c)
        return True

    def scatter(self, cells, objs, count, spacing=1, tries=40, z=None):
        """Places up to `count` objects (chosen from objs) at random in `cells` with `spacing` free cells around."""
        cells = list(cells)
        self.rng.shuffle(cells)
        placed = 0
        for (x, y) in cells:
            if placed >= count:
                break
            obj = self.rng.choice(objs)
            foot = [(x + o[0], y + o[1]) for o in obj]
            ring = self.grow(set(foot), spacing, diag=True) if spacing else set(foot)
            if all(c in self._scatter_ok for c in foot) and self.fits(ring & self.all()) and self.fits(foot):
                self.stamp(x, y, obj, z=z)
                placed += 1
        return placed

    def scatter_in(self, cells, objs, count, spacing=1, z=None):
        self._scatter_ok = set(cells)
        return self.scatter(cells, objs, count, spacing, z=z)

    # ------------------------------------------------------------------ terrain
    def cliff(self, cells, top, wall, height=2, z=0):
        """Raises `cells` into a plateau: top kind on the plateau, `height` rows of wall kind under its south edge."""
        self.paint(cells, top, z)
        for (x, y) in cells:
            if (x, y + 1) not in cells:
                for d in range(1, height + 1):
                    if self.inside(x, y + d) and (x, y + d) not in cells:
                        self.set(x, y + d, z, auto(wall))
                        self.blocked.add((x, y + d))
        return self

    def carve(self, open_cells, top, wall, floor, wall_h=2, z=0):
        """Dungeon: everything is ceiling (top kind) except open_cells; open cells under the ceiling become
        `wall_h` rows of wall face, the rest floor."""
        for (x, y) in self.all():
            self.set(x, y, z, auto(top))
        for (x, y) in open_cells:
            self.set(x, y, z, auto(floor))
        for (x, y) in open_cells:
            if (x, y - 1) not in open_cells and self.inside(x, y - 1):
                for d in range(wall_h):
                    if (x, y + d) in open_cells:
                        self.set(x, y + d, z, auto(wall))
                        self.blocked.add((x, y + d))
        return self

    # ------------------------------------------------------------------ finish
    def shadows(self):
        """Editor-style shadows: the west half of a floor cell east of a wall face."""
        for y in range(self.h):
            for x in range(1, self.w):
                k0 = self.kind_at(x, y)
                k1 = self.kind_at(x - 1, y)
                if k1 is None or k0 is None:
                    continue
                if kind_role(k1) == 'wall' and kind_role(k0) != 'wall' and k1 >= 48:
                    above = self.kind_at(x - 1, y - 1)
                    bits = 5 if above is not None and kind_role(above) == 'wall' else 4
                    self.set(x, y, Z_SHADOW, bits)

    def finish(self, shadows=True):
        for z in (0, 1):
            refresh(self.m, z)
        if shadows:
            self.shadows()
        return self.m

    # ------------------------------------------------------------------ checks
    def reach(self, start):
        import mapinfo
        return mapinfo.region(self.m, *start)


# ============================================================================================================ prefabs
def obj2(top, bottom):
    """A 1x2 object: star top over a blocking base."""
    return [(0, -1, top), (0, 0, bottom)]


def objwide(ids, w, h):
    """A w x h block of consecutive sheet tiles: ids = top-left id; rows are 8 ids apart; anchored at bottom-left."""
    return [(dx, dy - (h - 1), ids + dx + dy * 8) for dy in range(h) for dx in range(w)]


class OUT:
    """Outside tileset (2)."""
    GRASS, GRASS_DIRT, GRASS_COBBLE, STONE_FLOOR, BUSH = 16, 17, 18, 19, 20
    SAND, SAND_GRASS, SAND_STONES, SAND_TILES, YBUSH = 24, 25, 26, 27, 28
    DIRT, DIRT_GRASS, DIRT_STONES, CARPET, ABUSH, HOLE, DGRASS = 32, 33, 34, 35, 36, 37, 39
    SNOW, SNOW_DIRT, SNOW_STONES, SBUSH, PIT = 40, 41, 42, 44, 45
    CRACKS, DARKSPARK = 23, 31
    SEA, WATER, WATER2, ICE, POISON = 0, 4, 8, 12, 14
    # A4: (top, wall)
    STONE_WALL = (80, 88)
    BRICK_WALL = (81, 89)
    SAND_WALL = (82, 90)
    CASTLE_WALL = (83, 91)
    SNOW_CLIFF = (84, 92)
    SNOWSTONE = (85, 93)
    RED_WALL = (96, 104)
    MARBLE = (101, 109)
    FOREST = (113, 121)
    DARKFOREST = (114, 122)
    SNOWFOREST = (115, 123)
    ROCK = (116, 124)
    ROCK2 = (117, 125)
    ROCK3 = (118, 126)
    SNOWROCK = (119, 127)
    MOSSWALL = (112, 120)
    # objects
    TREE = objwide(176, 2, 2)
    SNOWTREE = objwide(192, 2, 2)
    PINE = [(0, -1, 157), (0, 0, 165)]
    SNOWPINE = [(0, -1, 221), (0, 0, 229)]
    DEADTREE = [(0, -1, 232), (0, 0, 240)]
    DEADTREE2 = [(0, -1, 233), (0, 0, 241)]
    LAMP = [(0, -2, 8), (0, -1, 16), (0, 0, 24)]
    ROCKS = [[(0, 0, 159)], [(0, 0, 167)]]
    SNOWROCKS = [[(0, 0, 223)], [(0, 0, 231)]]
    BARREL, POT, BUCKET, WELL = 141, 144, 145, 139
    GRAVE, SNOWGRAVE = 142, 214
    SIGN = 137
    CRATES = [180, 181, 182, 183]
    SNOWMAN = 216


class DUN:
    """Dungeon tileset (4)."""
    DIRT, GRASS, DIRT2, ROCK, CRYSTAL, ROCK2, LAVAROCK, FLESH, CARPET, ICE, PURPLE, ICE2 = \
        16, 17, 18, 24, 25, 26, 32, 33, 35, 40, 41, 42
    HOLE, PIT, CRACKS, MOSS = 20, 30, 23, 39
    WATER, DEEP, LAVA, DARKWATER, CANAL = 0, 1, 4, 6, 14
    BROWN_ROCK = (80, 88)
    GREY_ROCK = (81, 89)
    DARK_ROCK = (82, 90)
    ICE_ROCK = (83, 91)
    VINE_ROCK = (84, 92)
    GREY_BRICK = (96, 104)
    RED_BRICK = (97, 105)
    SAND_BRICK = (98, 106)
    COBBLE = (99, 107)
    MOSS_BRICK = (100, 108)
    BLOCK = (101, 109)
    DARK_BRICK = (113, 121)
    ICE_BRICK = (114, 122)
    ORE_ROCK = (115, 123)
    LAVA_ROCK = (118, 126)
    STALAG = [(0, -1, 40), (0, 0, 48)]
    BOULDER = [(0, -1, 41), (0, 0, 49)]
    LAVASPIRE = [(0, -1, 42), (0, 0, 50)]
    ICESPIRE = [(0, -1, 43), (0, 0, 51)]
    CRYSTALS = [(0, -1, 45), (0, 0, 53)]
    PEBBLES = [[(0, 0, 32)], [(0, 0, 33)], [(0, 0, 34)]]
    BONES = [[(0, 0, 240)], [(0, 0, 241)], [(0, 0, 242)], [(0, 0, 248)], [(0, 0, 249)], [(0, 0, 250)]]
    COBWEB = 176
    JAR, SACK, BARREL, BUCKET = 230, 231, 238, 239
    CRATES = [220, 221, 222]


class INS:
    """Inside tileset (3)."""
    WOOD, COBBLE, TERRACOTTA, TATAMI, WOOD2, STONE, RUG_RED, RUG_GREEN = 16, 17, 18, 19, 24, 25, 26, 27
    PARQUET, BRICK, RUG_BLUE, RUG_RED2, MARBLE, CHECKER, RUG_ORNATE, RUG_PURPLE = 32, 33, 34, 35, 40, 41, 42, 43
    GREY_STONE = (80, 88)
    ORNATE_STONE = (81, 89)
    PLAIN_STONE = (83, 91)
    MARBLE_PILLARS = (84, 92)
    RED_BRICK = (85, 93)
    SANDSTONE = (86, 94)
    WOOD_WALL = (96, 104)
    LOG_WALL = (97, 105)
    PANEL = (98, 106)
    PLASTER = (103, 111)
    CREAM = (112, 120)
    GOLD = (118, 126)
