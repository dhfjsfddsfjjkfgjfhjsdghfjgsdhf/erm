"""Builds the story cast's faces and walking sprites with the generator re-implementation."""
import copy, os
from PIL import Image
import gen
from chars import mk
OUT = '/home/claude/mz/story/img'

def variant(base, **pats):
    s = copy.deepcopy(base); s['patterns'].update(pats); return s

KANTA = mk('male', dict(face='p05', fronthair='p13', rearhair='p02', eyes='p04', eyebrows='p05', mouth='p03', nose='p02',
                        clothing='p17', cloak='p03'),
           dict(skin=1, eyes=10, hair=23, hair2=23, cloth1=15, cloth2=16, cloth3=17, cloth4=16, cloak=1, cloak2=1))
HANMA = mk('male', dict(face='p06', fronthair='p16', rearhair='p02', eyes='p13', eyebrows='p06', mouth='p02', nose='p02',
                        clothing='p14'),
           dict(skin=0, eyes=4, hair=19, hair2=19, cloth1=17, cloth2=3, cloth3=3, cloth4=3))
HANMA['tvfix'] = {'clothing': [(40, 160, 'common', 17)]}
FALIN = mk('male', dict(face='p04', fronthair='p12', rearhair='p02', eyes='p21', eyebrows='p04', mouth='p16', nose='p03',
                        clothing='p21', acca='p01'),
           dict(skin=3, eyes=6, hair=23, hair2=23, cloth1=16, cloth2=17, cloth3=16, cloth4=15, acca=16, acca2=17, acca3=16))

FACES = {
    'Cast1': [KANTA,                                   # 0 Kanta calm
              variant(KANTA, mouth='p22', eyebrows='p12'),   # 1 Kanta fierce
              variant(KANTA, mouth='p10'),                # 2 Kanta wry smile
              variant(KANTA, mouth='p18', eyes='p13'),    # 3 Kanta hurt / tired
              HANMA,                                   # 4 Hanma calm
              variant(HANMA, mouth='p01'),                # 5 Hanma faint smile
              variant(HANMA, mouth='p12', eyebrows='p12'),   # 6 Hanma stern
              variant(HANMA, mouth='p13', eyebrows='p12')],  # 7 Hanma commanding (open mouth)
    'Cast2': [FALIN,                                   # 0 Falin calm
              variant(FALIN, mouth='p22', eyebrows='p12'),   # 1 Falin fierce
              variant(FALIN, mouth='p01'),                # 2 Falin faint smile
              variant(FALIN, mouth='p18', eyes='p13')],   # 3 Falin hurt
}
SPRITES = {'Cast': [KANTA, HANMA, FALIN]}

def face_sheet(faces):
    sheet = Image.new('RGBA', (576, 288), (0, 0, 0, 0))
    for i, s in enumerate(faces):
        sheet.alpha_composite(gen.compose_face(s), ((i % 4) * 144, (i // 4) * 144))
    return sheet

def char_sheet(chars):
    sheet = Image.new('RGBA', (576, 384), (0, 0, 0, 0))
    for i, s in enumerate(chars):
        sheet.alpha_composite(gen.compose_tv(s), ((i % 4) * 144, (i // 4) * 192))
    return sheet

if __name__ == '__main__':
    os.makedirs(OUT + '/faces', exist_ok=True); os.makedirs(OUT + '/characters', exist_ok=True)
    for name, faces in FACES.items():
        face_sheet(faces).save(f'{OUT}/faces/{name}.png')
    for name, chars in SPRITES.items():
        char_sheet(chars).save(f'{OUT}/characters/{name}.png')
    # preview
    prev = Image.new('RGBA', (576, 288 + 144 + 384), (80, 80, 90, 255))
    prev.alpha_composite(Image.open(f'{OUT}/faces/Cast1.png'), (0, 0))
    prev.alpha_composite(Image.open(f'{OUT}/faces/Cast2.png'), (0, 288))
    prev.alpha_composite(Image.open(f'{OUT}/characters/Cast.png'), (0, 432))
    prev.save('/tmp/claude-0/-home-claude/e205e0a3-bd62-5461-b21e-25640739d4b9/scratchpad/cast_preview.png')
    print('ok')
