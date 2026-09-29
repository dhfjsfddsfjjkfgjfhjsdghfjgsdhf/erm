"""Adds a coordinate grid and event labels to a rendered map (from scen_render.js).
usage: python3 render_grid.py <map.json> <raw.png> <out.png> [px_per_tile=32] [--pass]
--pass also tints impassable tiles red (MZ passage rules, tileset flags)."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/mz/tools')
import mapinfo

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    mpath, raw, out = args[:3]
    px = int(args[3]) if len(args) > 3 else 32
    d = json.load(open(mpath))
    w, h = d['width'], d['height']
    im = Image.open(raw).convert('RGBA').resize((w * px, h * px), Image.LANCZOS)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    reach = None
    for f in flags:
        if f.startswith('--reach='):
            sx, sy = map(int, f.split('=')[1].split(','))
            reach = mapinfo.region(d, sx, sy)
    if reach:
        for (x, y) in reach:
            cx, cy = x * px + px // 2, y * px + px // 2
            dr.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(0, 255, 0, 200))
    if '--pass' in flags:
        ok, _ = mapinfo.walk_grid(d)
        for y in range(h):
            for x in range(w):
                if not ok[y][x]:
                    dr.rectangle([x * px, y * px, x * px + px - 1, y * px + px - 1], fill=(255, 0, 0, 70))
    for x in range(w + 1):
        c = (255, 255, 0, 150) if x % 5 == 0 else (255, 255, 255, 45)
        dr.line([(x * px, 0), (x * px, h * px)], fill=c, width=1)
    for y in range(h + 1):
        c = (255, 255, 0, 150) if y % 5 == 0 else (255, 255, 255, 45)
        dr.line([(0, y * px), (w * px, y * px)], fill=c, width=1)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', max(9, px // 3))
    except Exception:
        font = ImageFont.load_default()
    for x in range(0, w, 5):
        for y in range(0, h, 5):
            dr.text((x * px + 2, y * px + 1), f'{x},{y}', fill=(255, 255, 0, 230), font=font,
                    stroke_width=2, stroke_fill=(0, 0, 0, 230))
    for e in d['events']:
        if not e:
            continue
        x, y = e['x'], e['y']
        dr.rectangle([x * px + 1, y * px + 1, x * px + px - 2, y * px + px - 2], outline=(0, 255, 255, 220), width=2)
        dr.text((x * px + 3, y * px + px // 2), str(e['id']), fill=(0, 255, 255, 255), font=font,
                stroke_width=2, stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(im, ov).convert('RGB').save(out)
    print(out, im.size)

if __name__ == '__main__':
    main()
