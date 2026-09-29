"""Map-sized overlay images (TausiLighting layers): the frozen river of Eisfurt."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def water_tiles(m):
    w, h = m['width'], m['height']
    out = set()
    for y in range(h):
        for x in range(w):
            t = m['data'][(0 * h + y) * w + x]
            if 2048 <= t < 2816:            # A1 (water)
                out.add((x, y))
    return out

def paste_decor(img, m, tileset, tiledir, cells):
    """Redraw the non-star B-E tiles of `cells` on top of an overlay: the layer lies
    over the lower tilemap layer, so trunks and tufts standing on the ice come back."""
    w, h = m['width'], m['height']
    flags = tileset['flags']
    sheets = {}
    for (x, y) in cells:
        if not (0 <= x < w and 0 <= y < h):
            continue
        for z in (2, 3):
            t = m['data'][(z * h + y) * w + x]
            if not t or t >= 1024 and not (1536 <= t < 1664):
                continue
            if flags[t] & 0x10:
                continue                    # star tiles are drawn above anyway
            n = 4 if t >= 1536 else 5 + t // 256
            name = tileset['tilesetNames'][n]
            if not name:
                continue
            if name not in sheets:
                sheets[name] = Image.open(f'{tiledir}/{name}.png').convert('RGBA')
            sx = ((t // 128) % 2 * 8 + t % 8) * 48
            sy = ((t % 256) // 8 % 16) * 48
            tile = sheets[name].crop((sx, sy, sx + 48, sy + 48))
            img.alpha_composite(tile, (x * 48, y * 48))
    return img

def ice_overlay(m, path, seed=7, tileset=None, tiledir=None):
    rng = np.random.default_rng(seed)
    w, h = m['width'] * 48, m['height'] * 48
    mask = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(mask)
    tiles = water_tiles(m)
    for (x, y) in tiles:
        d.rectangle([x * 48, y * 48, x * 48 + 47, y * 48 + 47], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(5))
    # ice: pale blue-white with soft noise
    noise = rng.normal(0, 1, (h // 8 + 1, w // 8 + 1))
    noise = np.array(Image.fromarray(((noise - noise.min()) / (np.ptp(noise) + 1e-6) * 255).astype('uint8'))
                     .resize((w, h), Image.BICUBIC)).astype(np.float32) / 255.0
    base = np.zeros((h, w, 4), np.float32)
    base[..., 0] = 205 + 30 * noise
    base[..., 1] = 225 + 22 * noise
    base[..., 2] = 238 + 15 * noise
    img = Image.fromarray(np.clip(base, 0, 255).astype('uint8'), 'RGBA')
    # cracks
    cd = ImageDraw.Draw(img)
    xs = [x for x, _ in tiles] or [0]
    ys = [y for _, y in tiles] or [0]
    for _ in range(max(6, len(tiles) // 6)):
        tx, ty = list(tiles)[rng.integers(len(tiles))] if tiles else (0, 0)
        px, py = tx * 48 + rng.integers(48), ty * 48 + rng.integers(48)
        for _ in range(rng.integers(3, 7)):
            nx, ny = px + rng.integers(-40, 41), py + rng.integers(-40, 41)
            cd.line([(px, py), (nx, ny)], fill=(150, 185, 210, 255), width=1)
            px, py = nx, ny
    alpha = np.array(mask).astype(np.float32) * 0.93
    arr = np.array(img)
    arr[..., 3] = alpha.astype('uint8')
    out = Image.fromarray(arr, 'RGBA')
    if tileset and tiledir:
        near = {(x + dx, y + dy) for (x, y) in tiles for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        out = paste_decor(out, m, tileset, tiledir, near)
    out.save(path)
    return path
