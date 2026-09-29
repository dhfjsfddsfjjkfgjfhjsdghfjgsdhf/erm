"""Minimal re-implementation of the RPG Maker MZ character generator (faces first).

Parts live in /mnt/user-data/uploads/generator/<Kind>/<Gender>/.
Face parts: FG_<Part>_p<NN>_c<layer>[_m<slot>].png  (144x144, some 160x160 centred)
A layer with _m<slot> is recoloured through the gradient chosen for that slot.
"""
import os, re, glob, json
import numpy as np
from PIL import Image

ROOT = '/mnt/user-data/uploads/generator'

def _rows(name):
    im = np.array(Image.open(f'{ROOT}/{name}').convert('RGB')).astype(np.float32)
    h = 4
    return [im[r * h + 1] for r in range(im.shape[0] // h)]

GRAD = {'skin': _rows('grad_skin.png'), 'eyes': _rows('grad_eyes.png'),
        'hair': _rows('grad_hair.png'), 'common': _rows('grad_common.png')}

# slot number -> gradient file
def slot_grad(slot):
    if slot == 1:
        return 'skin'
    if slot == 2:
        return 'eyes'
    if slot in (3, 4):
        return 'hair'
    return 'common'

# key colours in the order the generator JSON lists them (slot 1..24)
KEYS = ["#F9C19D", "#2C80CB", "#FCCB0A", "#B892C5", "#009296", "#D3CEC7", "#AE8682", "#FE9D1E", "#1C76D0",
        "#D9A404", "#D8AC00", "#A30708", "#D3CEC2", "#DA346E", "#A4C911", "#C78407", "#C0D3D2", "#4155B6",
        "#BA3B45", "#999999", "#CCBAD2", "#607E4B", "#E6D6BD", "#A7D6D6"]

_default_row_cache = {}

def default_row(slot, arr):
    """Finds which gradient row the part art was painted with (best fit)."""
    g = GRAD[slot_grad(slot)]
    m = arr[:, :, 3] > 128
    px = arr[m][:, :3].astype(np.float32)
    if len(px) > 4000:
        px = px[:: len(px) // 4000 + 1]
    best = None
    for ri, row in enumerate(g):
        d = ((px[:, None, :] - row[None, :, :]) ** 2).sum(-1).min(1).mean()
        if best is None or d < best[0]:
            best = (d, ri)
    return best[1]

def recolor(arr, slot, row_index, mode='lum'):
    """arr: HxWx4 uint8. Returns recoloured copy using gradient row row_index."""
    out = arr.copy()
    g = GRAD[slot_grad(slot)]
    row = g[min(row_index, len(g) - 1)]
    rgb = arr[:, :, :3].astype(np.float32)
    if mode == 'lum':
        lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
        idx = np.clip(255 - lum, 0, 255).astype(int)
    elif mode == 'fit':
        src = g[default_row(slot, arr)]
        flat = rgb.reshape(-1, 3)
        idx = np.empty(len(flat), int)
        for i in range(0, len(flat), 8192):
            d = ((flat[i:i + 8192, None, :] - src[None, :, :]) ** 2).sum(-1)
            idx[i:i + 8192] = d.argmin(1)
        idx = idx.reshape(rgb.shape[:2])
    new = row[idx]
    out[:, :, :3] = np.clip(new, 0, 255).astype(np.uint8)
    return out

PAT = re.compile(r'FG_([A-Za-z]+?)(\d?)_p(\d+)(?:_c(\d+))?(?:_m(\d+))?\.png$')

def face_layers(gender, part, pid):
    """All layer files of a face part pattern (Part may have a 1/2 split)."""
    files = glob.glob(f'{ROOT}/Face/{gender}/FG_{part}*_p{pid:02d}_*.png') + \
            glob.glob(f'{ROOT}/Face/{gender}/FG_{part}*_p{pid:02d}.png')
    out = []
    for f in files:
        m = PAT.search(os.path.basename(f))
        if not m or m.group(1) != part:
            continue
        sub = m.group(2) or ''
        layer = int(m.group(4) or 1)
        slot = int(m.group(5)) if m.group(5) else None
        out.append((sub, layer, slot, f))
    return out

# drawing order (back to front) for face parts: (part, sub-layer)
FACE_ORDER = [('RearHair', '2'), ('Cloak', '1'), ('Clothing', '1'), ('Body', ''), ('Clothing', '2'),
              ('Face', ''), ('Ears', ''), ('Mouth', ''), ('Nose', ''), ('Eyes', ''), ('Eyebrows', ''),
              ('FacialMark', ''), ('Beard', ''), ('RearHair', '1'), ('BeastEars', ''), ('FrontHair', ''),
              ('Cloak', '2'), ('Glasses', ''), ('AccB', ''), ('AccA', '')]

OFFX = 1
OFFY = 1

PART_KEY = {'Cloak': 'cloak', 'RearHair': 'rearhair', 'Clothing': 'clothing', 'Body': 'body', 'Ears': 'ears',
            'Face': 'face', 'Mouth': 'mouth', 'Nose': 'nose', 'Eyes': 'eyes', 'Eyebrows': 'eyebrows',
            'FacialMark': 'facialmark', 'Beard': 'beard', 'BeastEars': 'beastears', 'FrontHair': 'fronthair',
            'Glasses': 'glasses', 'AccB': 'accb', 'AccA': 'acca'}

def compose_face(settings, mode='lum', order=None, size=144):
    gender = {'female': 'Female', 'male': 'Male', 'kid': 'Kid'}[settings['gender']]
    pats = settings['patterns']
    colors = settings.get('colors', {})
    offs = settings.get('offsets', {})
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    for part, sub in (order or FACE_ORDER):
        key = PART_KEY[part]
        p = pats.get(key, '')
        if not p:
            continue
        pid = int(p[1:])
        layers = [l for l in face_layers(gender, part, pid) if l[0] == sub]
        layers.sort(key=lambda l: -l[1])
        o = offs.get(key, {"x": 0, "y": 0})
        for s, layer, slot, f in layers:
            im = Image.open(f).convert('RGBA')
            arr = np.array(im)
            if slot:
                row = colors.get(KEYS[slot - 1], 0) if slot <= len(KEYS) else 0
                if isinstance(row, (list, tuple)):
                    row = row[0]
                arr = recolor(arr, slot, int(row), mode)
            im = Image.fromarray(arr)
            # parts may be larger than the face (e.g. 160x160): centre them
            dx = (size - im.width) // 2 * OFFX + int(o.get('x', 0))
            dy = (size - im.height) // 2 * OFFY + int(o.get('y', 0))
            layer_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            layer_img.paste(im, (dx, dy))
            canvas = Image.alpha_composite(canvas, layer_img)
    return canvas


# ---------------------------------------------------------------------------
# TV (walking sprite) parts: TV_<Part>_p<NN>.png + TV_<Part>_p<NN>_c.png (key-colour slot map)
# ---------------------------------------------------------------------------
KEY_RGB = [tuple(int(k[i:i + 2], 16) for i in (1, 3, 5)) for k in KEYS]

TV_ORDER = [('Cloak', '1'), ('Body', ''), ('Ears', ''), ('RearHair', '2'), ('Clothing', '2'),
            ('FacialMark', ''), ('RearHair', '1'), ('FrontHair', '1'), ('FrontHair', '2'), ('Cloak', '2'),
            ('AccB', ''), ('AccA', '')]

def tv_files(gender, part, sub, pid):
    base = f'{ROOT}/TV/{gender}/TV_{part}{sub}_p{pid:02d}'
    main, key = base + '.png', base + '_c.png'
    if os.path.exists(main):
        return main, (key if os.path.exists(key) else None)
    return None, None

def recolor_keyed(arr, keyarr, colors):
    out = arr.copy()
    rgb = arr[:, :, :3].astype(np.float32)
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    idx = np.clip(255 - lum, 0, 255).astype(int)
    kr = keyarr[:, :, :3].astype(int)
    ka = keyarr[:, :, 3] > 0
    for slot, krgb in enumerate(KEY_RGB, start=1):
        m = ka & (kr[:, :, 0] == krgb[0]) & (kr[:, :, 1] == krgb[1]) & (kr[:, :, 2] == krgb[2])
        if not m.any():
            continue
        row = colors.get(KEYS[slot - 1], 0)
        g = GRAD[slot_grad(slot)]
        row = g[min(int(row), len(g) - 1)]
        out[:, :, :3][m] = np.clip(row[idx[m]], 0, 255).astype(np.uint8)
    return out

TV_KEY = {'RearHair': 'rearhair', 'Cloak': 'cloak', 'Body': 'body', 'Ears': 'ears', 'Clothing': 'clothing',
          'FacialMark': 'facialmark', 'FrontHair': 'fronthair', 'AccB': 'accb', 'AccA': 'acca'}

def fix_unkeyed(arr, keyarr, hue_lo, hue_hi, grad_name, row_index, min_sat=0.25):
    """Recolour unkeyed pixels whose hue is in [hue_lo, hue_hi] (0-360) through a gradient row."""
    import colorsys
    out = arr.copy()
    kr = keyarr[:, :, :3].astype(int)
    unkeyed = (keyarr[:, :, 3] == 0) | ((kr[:, :, 0] == 255) & (kr[:, :, 1] == 255) & (kr[:, :, 2] == 255))
    rgb = arr[:, :, :3].astype(np.float32) / 255.0
    mx = rgb.max(2); mn = rgb.min(2); d = mx - mn + 1e-6
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = d / (mx + 1e-6)
    m = unkeyed & (arr[:, :, 3] > 0) & (h >= hue_lo) & (h <= hue_hi) & (s >= min_sat)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    idx = np.clip(255 - lum, 0, 255).astype(int)
    row = GRAD[grad_name][row_index]
    out[:, :, :3][m] = np.clip(row[idx[m]], 0, 255).astype(np.uint8)
    return out

def compose_tv(settings, order=None):
    gender = {'female': 'Female', 'male': 'Male', 'kid': 'Kid'}[settings['gender']]
    pats = settings['patterns']
    colors = settings.get('colors', {})
    canvas = None
    for part, sub in (order or TV_ORDER):
        p = pats.get(TV_KEY[part], '')
        if not p:
            continue
        main, key = tv_files(gender, part, sub, int(p[1:]))
        if not main:
            continue
        arr = np.array(Image.open(main).convert('RGBA'))
        if key:
            karr = np.array(Image.open(key).convert('RGBA'))
            arr = recolor_keyed(arr, karr, colors)
            for fx in settings.get('tvfix', {}).get(TV_KEY[part], []):
                arr = fix_unkeyed(arr, karr, *fx)
        im = Image.fromarray(arr)
        if canvas is None:
            canvas = Image.new('RGBA', im.size, (0, 0, 0, 0))
        layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        layer.paste(im, (0, 0))
        canvas = Image.alpha_composite(canvas, layer)
    return canvas
