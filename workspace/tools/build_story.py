"""Builds the Erdenkreis story project into mz/story/out (data/, js/plugins.js, js/plugins/, img/)."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from story.common import *
from story import db, lighting, prologue, ch1, ch2, ch3, act2, ch4, ch5
from story.ids import *
import mapinfo

OUTD = OUT + '/data'
os.makedirs(OUTD, exist_ok=True)
os.makedirs(OUT + '/js/plugins', exist_ok=True)

# ------------------------------------------------------------- database
states = db.build_states()
skills = db.build_skills()
items = db.build_items()
weapons = db.build_weapons()
armors = db.build_armors()
classes = db.build_classes()
actors = db.build_actors()
enemies = db.build_enemies()
troops = db.build_troops()
common = db.build_common_events()

# ------------------------------------------------------------- maps
maps = prologue.build() + ch1.build() + ch2.build() + ch3.build() + act2.build() + ch4.build() + ch5.build()
V_REGALIA = VAR('Regalia')          # Story_Core's Rank Pierce Variable (the Dawn Regalia held)

# ------------------------------------------------------------- validation
problems = []
def check_map(mb, start):
    d = mb.m
    starts = start if isinstance(start, list) else [start]
    reach = set()
    for st in starts:
        reach |= set(mapinfo.region(d, *st, mapinfo.exit_tiles(d)))
    ok, flags = mapinfo.walk_grid(d)
    counter = lambda x, y: 0 <= x < d['width'] and 0 <= y < d['height'] and any(
        (flags[mapinfo.tile(d, x, y, z)] & 0x80) for z in range(4) if mapinfo.tile(d, x, y, z))
    for e in d['events'][1:]:
        if not e:
            continue
        x, y = e['x'], e['y']
        if (x, y) == (0, 0):
            continue
        pages = e['pages']
        if all(len(p['list']) <= 1 for p in pages):
            continue                       # decor / blank
        trig = {p['trigger'] for p in pages if len(p['list']) > 1}
        prio = {p['priorityType'] for p in pages if len(p['list']) > 1}
        if trig and trig <= {3, 4}:
            continue
        near = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))]
        across = [(x + 2 * dx, y + 2 * dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
                  if counter(x + dx, y + dy)]
        if (x, y) in reach or any(n in reach for n in near + across):
            continue
        problems.append(f"map {mb.id} {mb.name}: '{e['name']}' at {x},{y} can't be reached")

STARTS = {CAVE: (12, 8), RIDGE: (12, 10), ROAD: (1, 9), TREES: (2, 32), RABENAU: (13, 27), INN: (9, 13),
          ELDER: (5, 11), HERBS: (8, 9), SMITHY: (8, 9), FARM: (8, 10), RABENHOLZ: (15, 26), DEEPWOOD: (3, 5),
          RUIN: (12, 21), TOWERTOP: (3, 7), OSTSTRASSE: (5, 21), SHRINE_CAMP: (10, 14), EISFURT: (15, 27),
          FURT_INN: (5, 11), VOGTEI: (8, 10), KUZE_SHOP: (12, 8), FROSTPFAD: (8, 21), HOCHWEG: (5, 25),
          EISFALL: (19, 36), EISFALL_HEART: (5, 33),
          KOENIGSSTRASSE: (21, 27), WACHTBURG: (24, 47), GILDE: (12, 15), WACHTFEUER: (15, 11), KAJI: (14, 12),
          AUSRUESTER: (8, 14), KORNSPEICHER: (8, 5), NORDSTRASSE: (3, 13), WOLFSGRUBE: (12, 15),
          WALLSTRASSE: (12, 25), FRONTPOSTEN: (16, 32), BRESCHE: (12, 15),
          WALLWEG: (12, 33), MARSCHALLHALLE: (6, 5), KASERNE: (8, 12), LAZARETT: (2, 9),
          ZEUGHAUS: (11, 12), FP5_TURM: (12, 45), ZISTERNE: (11, 24), WALLFESTE: [(21, 33), (22, 18)],
          GRAUKLAMM: GRAUKLAMM_ENTRY, HEERLAGER: (20, 28), WF_UNTERSTADT: (23, 37), AQUAEDUKT: (4, 26),
          HUELLENSCHMIEDE: (16, 27), DRACHENHALLE: (15, 24)}
for mb in maps:
    if mb.id in STARTS:
        check_map(mb, STARTS[mb.id])
# transfers must land on walkable tiles
for mb in maps:
    for e in mb.m['events'][1:]:
        for p in e['pages']:
            for c in p['list']:
                if c['code'] == 201:
                    _, mid, tx, ty = c['parameters'][:4]
                    if mid == 0:
                        continue
                    if mid not in MapBuild.registry:
                        problems.append(f"map {mb.id}: '{e['name']}' transfers to unknown map {mid}")
                        continue
                    t = MapBuild.registry[mid].m
                    ok, _ = mapinfo.walk_grid(t)
                    if not (0 <= tx < t['width'] and 0 <= ty < t['height']) or not ok[ty][tx]:
                        pass
                    if not (0 <= tx < t['width'] and 0 <= ty < t['height']) or (not ok[ty][tx] and (tx, ty) not in mapinfo.exit_tiles(t)):
                        problems.append(f"map {mb.id}: '{e['name']}' lands on a blocked tile {mid}:{tx},{ty}")

# ------------------------------------------------------------- write
write_list(OUTD + '/States.json', states)
write_list(OUTD + '/Skills.json', skills)
write_list(OUTD + '/Items.json', items)
write_list(OUTD + '/Weapons.json', weapons)
write_list(OUTD + '/Armors.json', armors)
write_list(OUTD + '/Classes.json', classes)
write_list(OUTD + '/Actors.json', actors)
write_list(OUTD + '/Enemies.json', enemies)
write_list(OUTD + '/Troops.json', troops)
write_list(OUTD + '/CommonEvents.json', common)
write_obj(OUTD + '/System.json', db.build_system(CAVE, 12, 8))
for name in ['Animations', 'Tilesets']:
    shutil.copy(f'{ORIG}/data/{name}.json', f'{OUTD}/{name}.json')

infos = [None]
order = 0
for mb in sorted(maps, key=lambda m: m.id):
    order += 1
    write_map(f'{OUTD}/Map{mb.id:03d}.json', mb.m)
    while len(infos) < mb.id:
        infos.append(None)
    infos.append(mb.info(order))
write_list(OUTD + '/MapInfos.json', infos)
write_obj(OUTD + '/Lighting.json', lighting.build())

# ------------------------------------------------------------- plugins
PLUG = [
    ('Rank_Core', ROOT + '/plugins/Rank_Core.js', {}),
    ('Rank_Battle', ROOT + '/plugins/Rank_Battle.js', {}),
    ('Rank_Menus', ROOT + '/plugins/Rank_Menus.js', {}),
    ('Rank_Maps', ROOT + '/plugins/Rank_Maps.js', {}),
    ('McKathlin_DayNight', ROOT + '/thirdparty/McKathlin_DayNight.js', {
        'Daytime Switch': '2', 'Night Switch': '3', 'Days Passed Variable': '4', 'Current Hour Variable': '5',
        'Current Minute Variable': '6',
        'New Game Start Time': '{"hour":"6","minutes":"0","ampm":"AM"}',
        'Dawn Start Time': '{"hour":"5","minutes":"0","ampm":"AM"}',
        'Day Start Time': '{"hour":"7","minutes":"0","ampm":"AM"}',
        'Dusk Start Time': '{"hour":"6","minutes":"0","ampm":"PM"}',
        'Night Start Time': '{"hour":"8","minutes":"0","ampm":"PM"}',
        'Minutes Per Step': '1', 'Minutes Per Tone Phase': '30', 'Default Lighting Keyword': 'Bright',
        'Outdoor Lighting Keyword': 'Outside'}),
    ('TausiLighting', ROOT + '/thirdparty/TausiLighting.js', {'Show Overlay': 'false', 'Add to Title Menu': 'false'}),
    ('WD_Core', ROOT + '/plugins/WD_Core.js', {}),
    ('WD_Quest', ROOT + '/thirdparty/WD_Quest.js', {
        'menucommand': 'true', 'commandname': 'Quests', 'Title': 'Quests', 'giverprefix': 'From:',
        'areaprefix': 'Where:', 'statusname': 'Status:', 'trackSetting': 'player', 'trackDefText': 'Track',
        'untrackDefText': 'Stop tracking',
        'trackConfiguration': '{"maxQuest":"2","textColor":"#ffffff","maxFont":"16","hudSize":"{\\"width\\":\\"30\\",\\"height\\":\\"14\\",\\"x\\":\\"0\\",\\"y\\":\\"0\\"}"}'}),
    ('Story_Core', ROOT + '/plugins/Story_Core.js', {
        'Gate Variable': '1', 'Vessel Switch': '1', 'Revival Common Event': str(db.CE['Vessel Revival']),
        'Deaths Variable': '2', 'Lost Money Variable': '3', 'Money Loss': '0.10', 'Default Rest Map': str(CAVE),
        'Default Rest X': '12', 'Default Rest Y': '8', 'Barrier State': str(db.ST_BARRIER),
        'Rank Pierce Variable': str(V_REGALIA), 'Storm Element': str(db.THUNDER)}),
]
from dbkit import plugin_defaults
entries = []
for name, src, overrides in PLUG:
    shutil.copy(src, f'{OUT}/js/plugins/{name}.js')
    try:
        desc, params = plugin_defaults(src)
    except Exception as ex:
        print("plugin header not parsed:", name, ex)
        desc, params = '', {}
    params.update(overrides)
    entries.append({"name": name, "status": True, "description": desc, "parameters": params})
with open(OUT + '/js/plugins.js', 'w', encoding='utf-8') as f:
    f.write('// Generated by RPG Maker.\n// Do not edit this file directly.\nvar $plugins =\n[\n')
    f.write(',\n'.join(dumps(e) for e in entries))
    f.write('\n];\n')

# ------------------------------------------------------------- images
IMG = OUT + '/img'
for sub in ['faces', 'characters', 'enemies']:
    os.makedirs(f'{IMG}/{sub}', exist_ok=True)
# the player characters' portraits (faces from tools/insert_portraits.py, originals in img/pictures)
os.makedirs(f'{IMG}/pictures', exist_ok=True)
for n in ['Kanta', 'Hanma', 'Falin']:
    shutil.copy(f'{ROOT}/story/img/faces/{n}.png', f'{IMG}/faces/{n}.png')
    shutil.copy(f'{ROOT}/story/img/pictures/Portrait_{n}.png', f'{IMG}/pictures/Portrait_{n}.png')
shutil.copy(f'{ROOT}/story/img/characters/Cast.png', f'{IMG}/characters/Cast.png')
# the frozen river overlay for Eisfurt (TausiLighting layer)
from story import overlays
os.makedirs(f'{IMG}/pictures', exist_ok=True)
_ts = json.load(open(f'{ORIG}/data/Tilesets.json', encoding='utf-8'))
overlays.ice_overlay(MapBuild.registry[EISFURT].m, f'{IMG}/pictures/Ground_Eisfurt_Ice.png',
                     tileset=_ts[MapBuild.registry[EISFURT].m['tilesetId']],
                     tiledir='/mnt/user-data/uploads/RPGMZ/img/tilesets')
# Nemo battlers (@theartofnemo / RPGMakerWarehouse), scaled for the 816x624 front view
from PIL import Image
NEMO = {'Eiswurm': ('/mnt/user-data/uploads/dragonspack1_sd/SD/glacialserpent.png', 380),
        'Fubuki': ('/mnt/user-data/uploads/pack/SD/shiva_full.png', 440),
        'Aschenschwinge': ('/mnt/user-data/uploads/kamedran/kamedran1_glow.png', 470)}
for name, (src, height) in NEMO.items():
    dst = f'{IMG}/enemies/{name}.png'
    if not os.path.exists(src):
        continue          # source art pack not uploaded: keep the image from the last build
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        im = Image.open(src).convert('RGBA')
        w = round(im.width * height / im.height)
        im.resize((w, height), Image.LANCZOS).save(dst)

# RTP battlers scaled up (and tinted) for bosses
RTP_EN = '/mnt/user-data/uploads/RPGMZ/img/enemies'
def scaled(src, dst, factor, hue=0, dark=1.0):
    if os.path.exists(dst):
        return            # built once; delete the file to rebuild it
    im = Image.open(src).convert('RGBA')
    im = im.resize((round(im.width * factor), round(im.height * factor)), Image.LANCZOS)
    if hue or dark != 1.0:
        import numpy as np
        a = np.array(im).astype(np.float32)
        rgb = Image.fromarray(a[..., :3].astype('uint8'), 'RGB').convert('HSV')
        h = np.array(rgb).astype(np.int32)
        h[..., 0] = (h[..., 0] + int(hue * 255 / 360)) % 256
        h[..., 2] = np.clip(h[..., 2] * dark, 0, 255)
        back = np.array(Image.fromarray(h.astype('uint8'), 'HSV').convert('RGB')).astype(np.float32)
        a[..., :3] = back
        im = Image.fromarray(a.astype('uint8'), 'RGBA')
    im.save(dst)
scaled(f'{RTP_EN}/Matango.png', f'{IMG}/enemies/Schimmelmutter.png', 1.8, hue=90)
scaled(f'{RTP_EN}/SF_Zombiedog.png', f'{IMG}/enemies/Leitruede.png', 1.7, hue=-15, dark=0.8)

# Acts II-III battlers (story/foes.py IMAGES): scale, hue shift, saturation, colour tint, darken
from story import foes
def variant(name, spec):
    import numpy as np
    src = spec['src'] if spec['src'].startswith('/') else f"{RTP_EN}/{spec['src']}.png"
    dst = f'{IMG}/enemies/{name}.png'
    if not os.path.exists(src):
        if not os.path.exists(dst):
            problems.append(f'battler {name}: source {src} missing and no built image')
        return
    stamp = max(os.path.getmtime(src), os.path.getmtime(foes.__file__))
    if os.path.exists(dst) and os.path.getmtime(dst) >= stamp:
        return
    im = Image.open(src).convert('RGBA')
    if spec.get('h'):
        f = spec['h'] / im.height
    else:
        f = spec.get('f', 1.0)
    if f != 1.0:
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    a = np.array(im).astype(np.float32)
    rgb = a[..., :3]
    hue, sat, dark = spec.get('hue', 0), spec.get('sat', 1.0), spec.get('dark', 1.0)
    if hue or sat != 1.0 or dark != 1.0:
        hsv = np.array(Image.fromarray(rgb.astype('uint8'), 'RGB').convert('HSV')).astype(np.float32)
        hsv[..., 0] = (hsv[..., 0] + hue * 255 / 360) % 256
        hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 255)
        hsv[..., 2] = np.clip(hsv[..., 2] * dark, 0, 255)
        rgb = np.array(Image.fromarray(hsv.astype('uint8'), 'HSV').convert('RGB')).astype(np.float32)
    if spec.get('tint'):
        r, g, b, k = spec['tint']
        lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255.0
        col = np.stack([lum * r * 1.6, lum * g * 1.6, lum * b * 1.6], axis=-1)
        rgb = np.clip(rgb * (1 - k) + col * k, 0, 255)
    a[..., :3] = rgb
    Image.fromarray(a.astype('uint8'), 'RGBA').save(dst)
for _n, _spec in foes.IMAGES.items():
    variant(_n, _spec)

# story pictures made from RTP battlers (shown with Show Picture in scenes)
PICTURES = {'Shiranui': dict(src="Dragon", f=1.2, hue=-10, sat=1.1)}
for _n, _spec in PICTURES.items():
    _dst = f'{IMG}/pictures/{_n}.png'
    if not os.path.exists(_dst):
        _src = f"{RTP_EN}/{_spec['src']}.png"
        _tmp = f'{IMG}/enemies/_tmp_{_n}.png'
        variant('_tmp_' + _n, _spec)
        os.replace(_tmp, _dst)

print("built", OUT, "maps:", len(maps))
for p in problems:
    print("PROBLEM:", p)

# ids for tests
with open(OUT + '/ids.json', 'w', encoding='utf-8') as f:
    json.dump({"switches": SW.ids, "variables": VAR.ids, "troops": db.TR, "items": db.IT, "skills": db.SK,
               "enemies": db.EN, "common": db.CE, "weapons": db.WP, "armors": db.AR}, f, ensure_ascii=False, indent=1)
