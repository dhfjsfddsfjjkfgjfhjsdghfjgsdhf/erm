"""Renders an RPG Maker MZ map to PNG from the tileset images (no engine needed).

usage: python3 maprender.py <map.json> <out.png> [scale=0.5] [--grid] [--events] [--pass]

Autotiles are composed from quarter tiles with the standard RPG Maker floor / wall / waterfall layouts;
B-E and A5 tiles are copied whole. Layer 4 (shadows) is drawn as half-transparent black quarters.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

TILEDIR = os.environ.get('TILEDIR', '/opt/rmmz/img/tilesets')
CHARDIR = os.environ.get('CHARDIR', '/opt/rmmz/img/characters')
EXTRA_CHARDIRS = [os.path.join(os.path.dirname(__file__), '..', 'story', 'out', 'img', 'characters')]
TS_PATH = os.path.join(os.path.dirname(__file__), '..', 'orig', 'data', 'Tilesets.json')

A1, A2, A3, A4, A5, MAXID = 2048, 2816, 4352, 5888, 1536, 8192

# quarter (x, y) positions inside an autotile block, for the four quarters of a cell (TL, TR, BL, BR)
FLOOR = [
    [[2, 4], [1, 4], [2, 3], [1, 3]], [[2, 0], [1, 4], [2, 3], [1, 3]], [[2, 4], [3, 0], [2, 3], [1, 3]],
    [[2, 0], [3, 0], [2, 3], [1, 3]], [[2, 4], [1, 4], [2, 3], [3, 1]], [[2, 0], [1, 4], [2, 3], [3, 1]],
    [[2, 4], [3, 0], [2, 3], [3, 1]], [[2, 0], [3, 0], [2, 3], [3, 1]], [[2, 4], [1, 4], [2, 1], [1, 3]],
    [[2, 0], [1, 4], [2, 1], [1, 3]], [[2, 4], [3, 0], [2, 1], [1, 3]], [[2, 0], [3, 0], [2, 1], [1, 3]],
    [[2, 4], [1, 4], [2, 1], [3, 1]], [[2, 0], [1, 4], [2, 1], [3, 1]], [[2, 4], [3, 0], [2, 1], [3, 1]],
    [[2, 0], [3, 0], [2, 1], [3, 1]], [[0, 4], [1, 4], [0, 3], [1, 3]], [[0, 4], [3, 0], [0, 3], [1, 3]],
    [[0, 4], [1, 4], [0, 3], [3, 1]], [[0, 4], [3, 0], [0, 3], [3, 1]], [[2, 2], [1, 2], [2, 3], [1, 3]],
    [[2, 2], [1, 2], [2, 3], [3, 1]], [[2, 2], [1, 2], [2, 1], [1, 3]], [[2, 2], [1, 2], [2, 1], [3, 1]],
    [[2, 4], [3, 4], [2, 3], [3, 3]], [[2, 4], [3, 4], [2, 1], [3, 3]], [[2, 0], [3, 4], [2, 3], [3, 3]],
    [[2, 0], [3, 4], [2, 1], [3, 3]], [[2, 4], [1, 4], [2, 5], [1, 5]], [[2, 0], [1, 4], [2, 5], [1, 5]],
    [[2, 4], [3, 0], [2, 5], [1, 5]], [[2, 0], [3, 0], [2, 5], [1, 5]], [[0, 4], [3, 4], [0, 3], [3, 3]],
    [[2, 2], [1, 2], [2, 5], [1, 5]], [[0, 2], [1, 2], [0, 3], [1, 3]], [[0, 2], [1, 2], [0, 3], [3, 1]],
    [[2, 2], [3, 2], [2, 3], [3, 3]], [[2, 2], [3, 2], [2, 1], [3, 3]], [[2, 4], [3, 4], [2, 5], [3, 5]],
    [[2, 0], [3, 4], [2, 5], [3, 5]], [[0, 4], [1, 4], [0, 5], [1, 5]], [[0, 4], [3, 0], [0, 5], [1, 5]],
    [[0, 2], [3, 2], [0, 3], [3, 3]], [[0, 2], [1, 2], [0, 5], [1, 5]], [[0, 4], [3, 4], [0, 5], [3, 5]],
    [[2, 2], [3, 2], [2, 5], [3, 5]], [[0, 2], [3, 2], [0, 5], [3, 5]], [[0, 0], [1, 0], [0, 1], [1, 1]]]
WALL = [
    [[2, 2], [1, 2], [2, 1], [1, 1]], [[0, 2], [1, 2], [0, 1], [1, 1]], [[2, 0], [1, 0], [2, 1], [1, 1]],
    [[0, 0], [1, 0], [0, 1], [1, 1]], [[2, 2], [3, 2], [2, 1], [3, 1]], [[0, 2], [3, 2], [0, 1], [3, 1]],
    [[2, 0], [3, 0], [2, 1], [3, 1]], [[0, 0], [3, 0], [0, 1], [3, 1]], [[2, 2], [1, 2], [2, 3], [1, 3]],
    [[0, 2], [1, 2], [0, 3], [1, 3]], [[2, 0], [1, 0], [2, 3], [1, 3]], [[0, 0], [1, 0], [0, 3], [1, 3]],
    [[2, 2], [3, 2], [2, 3], [3, 3]], [[0, 2], [3, 2], [0, 3], [3, 3]], [[2, 0], [3, 0], [2, 3], [3, 3]],
    [[0, 0], [3, 0], [0, 3], [3, 3]]]
WATERFALL = [[[2, 0], [1, 0], [2, 1], [1, 1]], [[0, 0], [1, 0], [0, 1], [1, 1]],
             [[2, 0], [3, 0], [2, 1], [3, 1]], [[0, 0], [3, 0], [0, 1], [3, 1]]]

_TS = None
def tilesets():
    global _TS
    if _TS is None:
        _TS = json.load(open(TS_PATH, encoding='utf-8'))
    return _TS

_sheets = {}
def sheet(name):
    if name not in _sheets:
        p = f'{TILEDIR}/{name}.png'
        _sheets[name] = Image.open(p).convert('RGBA') if name and os.path.exists(p) else None
    return _sheets[name]

def is_a1(t): return A1 <= t < A2
def is_a2(t): return A2 <= t < A3
def is_a3(t): return A3 <= t < A4
def is_a4(t): return A4 <= t < MAXID
def is_auto(t): return t >= A1
def kind(t): return (t - A1) // 48
def shape(t): return (t - A1) % 48

def autotile_quarters(t, frame=0):
    """(set index, block x, block y, table) of an autotile id."""
    k, tx, ty = kind(t), kind(t) % 8, kind(t) // 8
    table = FLOOR
    if is_a1(t):
        s = 0
        wsi = [0, 1, 2, 1][frame % 4]
        if k == 0: bx, by = wsi * 2, 0
        elif k == 1: bx, by = wsi * 2, 3
        elif k == 2: bx, by = 6, 0
        elif k == 3: bx, by = 6, 3
        else:
            bx = (tx // 4) * 8
            by = ty * 6 + ((tx // 2) % 2) * 3
            if k % 2 == 0:
                bx += wsi * 2
            else:
                bx += 6
                table = WATERFALL
                by += frame % 3
    elif is_a2(t):
        s, bx, by = 1, tx * 2, (ty - 2) * 3
    elif is_a3(t):
        s, bx, by, table = 2, tx * 2, (ty - 6) * 2, WALL
    else:
        s, bx = 3, tx * 2
        by = int((ty - 10) * 2.5 + (0.5 if ty % 2 == 1 else 0))
        if ty % 2 == 1:
            table = WALL
    return s, bx, by, table

def draw_tile(img, ts, t, dx, dy, tw=48):
    if t <= 0 or t >= MAXID:
        return
    names = ts['tilesetNames']
    h = tw // 2
    if is_auto(t):
        s, bx, by, table = autotile_quarters(t)
        sh = sheet(names[s])
        if sh is None:
            return
        q = table[shape(t) % len(table)]
        for i in range(4):
            qx, qy = q[i]
            sx, sy = (bx * 2 + qx) * h, (by * 2 + qy) * h
            img.alpha_composite(sh.crop((sx, sy, sx + h, sy + h)), (dx + (i % 2) * h, dy + (i // 2) * h))
    else:
        s = 4 if A5 <= t < A1 else 5 + t // 256
        sh = sheet(names[s]) if s < len(names) else None
        if sh is None:
            return
        sx = ((t // 128) % 2 * 8 + t % 8) * tw
        sy = ((t % 256) // 8 % 16) * tw
        img.alpha_composite(sh.crop((sx, sy, sx + tw, sy + tw)), (dx, dy))

def render(m, scale=0.5, events=False, grid=False, passmap=False, chars=True):
    ts = tilesets()[m['tilesetId']]
    w, h = m['width'], m['height']
    img = Image.new('RGBA', (w * 48, h * 48), (0, 0, 0, 255))
    data = m['data']
    at = lambda x, y, z: data[(z * h + y) * w + x]
    for z in range(4):
        for y in range(h):
            for x in range(w):
                t = at(x, y, z)
                if t:
                    draw_tile(img, ts, t, x * 48, y * 48)
        if z == 1:
            # shadows (layer 4 bits) sit between the lower and upper layers
            sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(sh)
            for y in range(h):
                for x in range(w):
                    bits = at(x, y, 4) & 0x0f
                    for i in range(4):
                        if bits & (1 << i):
                            qx, qy = x * 48 + (i % 2) * 24, y * 48 + (i // 2) * 24
                            d.rectangle([qx, qy, qx + 23, qy + 23], fill=(0, 0, 0, 128))
            img.alpha_composite(sh)
    if chars:
        for e in m['events']:
            if not e or not e['pages']:
                continue
            p = e['pages'][0]
            im = p['image']
            if im.get('tileId'):
                draw_tile(img, ts, im['tileId'], e['x'] * 48, e['y'] * 48)
            elif im.get('characterName'):
                spr = char_frame(im['characterName'], im['characterIndex'], im['direction'], im['pattern'])
                if spr:
                    ox = e['x'] * 48 + 24 - spr.width // 2
                    oy = e['y'] * 48 + 48 - spr.height - (0 if im['characterName'].startswith('!') else 6)
                    img.alpha_composite(spr, (max(0, ox), max(0, oy)))
    out = img.convert('RGB').resize((int(w * 48 * scale), int(h * 48 * scale)), Image.LANCZOS)
    if grid or events or passmap:
        px = 48 * scale
        ov = Image.new('RGBA', out.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', max(8, int(px / 2.6)))
        except Exception:
            font = ImageFont.load_default()
        if passmap:
            import mapinfo
            ok, _ = mapinfo.walk_grid(m)
            for y in range(h):
                for x in range(w):
                    if not ok[y][x]:
                        d.rectangle([x * px, y * px, (x + 1) * px - 1, (y + 1) * px - 1], fill=(255, 0, 0, 70))
        if grid:
            for x in range(w + 1):
                d.line([(x * px, 0), (x * px, h * px)], fill=(255, 255, 0, 150) if x % 5 == 0 else (255, 255, 255, 40))
            for y in range(h + 1):
                d.line([(0, y * px), (w * px, y * px)], fill=(255, 255, 0, 150) if y % 5 == 0 else (255, 255, 255, 40))
            for x in range(0, w, 5):
                for y in range(0, h, 5):
                    d.text((x * px + 2, y * px + 1), f'{x},{y}', fill=(255, 255, 0, 230), font=font, stroke_width=2,
                           stroke_fill=(0, 0, 0, 230))
        if events:
            for e in m['events']:
                if not e:
                    continue
                x, y = e['x'], e['y']
                d.rectangle([x * px + 1, y * px + 1, (x + 1) * px - 2, (y + 1) * px - 2], outline=(0, 255, 255, 220), width=2)
                d.text((x * px + 2, y * px + px / 3), str(e['id']), fill=(0, 255, 255, 255), font=font, stroke_width=2,
                       stroke_fill=(0, 0, 0, 255))
        out = Image.alpha_composite(out.convert('RGBA'), ov).convert('RGB')
    return out

_chars = {}
def char_frame(name, index, direction, pattern):
    if name not in _chars:
        path = None
        for dirn in [CHARDIR] + EXTRA_CHARDIRS:
            p = f'{dirn}/{name}.png'
            if os.path.exists(p):
                path = p
                break
        _chars[name] = Image.open(path).convert('RGBA') if path else None
    sh = _chars[name]
    if sh is None:
        return None
    big = name.lstrip('!').startswith('$')
    cw, ch = (sh.width // 3, sh.height // 4) if big else (sh.width // 12, sh.height // 8)
    bx, by = (0, 0) if big else ((index % 4) * 3, (index // 4) * 4)
    di = {2: 0, 4: 1, 6: 2, 8: 3}.get(direction, 0)
    sx, sy = (bx + pattern) * cw, (by + di) * ch
    return sh.crop((sx, sy, sx + cw, sy + ch))

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    fl = [a for a in sys.argv[1:] if a.startswith('--')]
    m = json.load(open(args[0], encoding='utf-8'))
    scale = float(args[2]) if len(args) > 2 else 0.5
    render(m, scale, events='--events' in fl, grid='--grid' in fl, passmap='--pass' in fl).save(args[1])
    print(args[1])
