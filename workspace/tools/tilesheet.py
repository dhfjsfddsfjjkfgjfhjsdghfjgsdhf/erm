"""Contact sheets of a tileset with tile ids (for choosing tiles by eye). usage: tilesheet.py <tilesetId> <outdir>"""
import sys, json
from PIL import Image, ImageDraw, ImageFont
from maprender import tilesets, draw_tile, A1, A2, A3, A4, A5
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 11)
def grid(ids, cols, path, ts):
    rows = (len(ids) + cols - 1) // cols
    img = Image.new('RGBA', (cols * 52, rows * 62), (40, 40, 60, 255))
    d = ImageDraw.Draw(img)
    for i, t in enumerate(ids):
        x, y = (i % cols) * 52, (i // cols) * 62
        tile = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
        draw_tile(tile, ts, t, 0, 0)
        img.alpha_composite(tile, (x + 2, y + 2))
        d.text((x + 2, y + 50), str(t if t < A1 else (t - A1) // 48), fill=(255, 255, 0, 255), font=font)
    img.convert('RGB').save(path)
tsid = int(sys.argv[1]); out = sys.argv[2]
ts = tilesets()[tsid]
names = ts['tilesetNames']
# autotiles: kind k -> shape 46 would be an isolated island; show shape 0 (interior) and an isolated version
if names[0]: grid([A1 + k * 48 + 0 for k in range(16)], 8, f'{out}/ts{tsid}_A1.png', ts)
if names[1]: grid([A1 + k * 48 + 46 for k in range(16, 48)], 8, f'{out}/ts{tsid}_A2.png', ts)
if names[2]: grid([A1 + k * 48 + 15 for k in range(48, 80)], 8, f'{out}/ts{tsid}_A3.png', ts)
if names[3]: grid([A1 + k * 48 + (46 if (k // 8) % 2 == 0 else 15) for k in range(80, 128)], 8, f'{out}/ts{tsid}_A4.png', ts)
if names[4]: grid(list(range(A5, A5 + 128)), 8, f'{out}/ts{tsid}_A5.png', ts)
for n, base in [(5, 0), (6, 256), (7, 512), (8, 768)]:
    if names[n]:
        grid(list(range(base, base + 256)), 16, f'{out}/ts{tsid}_{"BCDE"[n - 5]}.png', ts)
print('ok')
