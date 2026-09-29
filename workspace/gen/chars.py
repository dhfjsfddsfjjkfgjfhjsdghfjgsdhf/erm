import json, copy
from PIL import Image, ImageDraw
import gen
SCR='/tmp/claude-0/-home-claude/e205e0a3-bd62-5461-b21e-25640739d4b9/scratchpad'
SLOT = {k: gen.KEYS[i] for i, k in enumerate(['skin','eyes','hair','hair2','mark','beast','cloth1','cloth2','cloth3','cloth4',
        'cloak','cloak2','acca','acca2','acca3','accb','accb2','accb3','s19','glass','glass2','s22','s23','s24'])}
def mk(gender, pats, cols):
    p={"body":"p01","face":"p01","fronthair":"","rearhair":"","beard":"","ears":"p01","eyes":"p01","eyebrows":"p01","nose":"p01","mouth":"p01","facialmark":"","beastears":"","tail":"","wing":"","clothing":"","cloak":"","acca":"","accb":"","glasses":""}
    p.update(pats)
    return {"gender":gender,"patterns":p,"colors":{SLOT[k]:v for k,v in cols.items()},"offsets":{}}
CHARS = {
 'Kanta': mk('male', dict(face='p05', fronthair='p13', rearhair='p02', eyes='p04', eyebrows='p05', mouth='p03', nose='p02', clothing='p17', cloak='p01'),
             dict(skin=1, eyes=10, hair=23, hair2=23, cloth1=15, cloth2=16, cloth3=17, cloth4=16, cloak=1, cloak2=1)),
 'Hanma': mk('male', dict(face='p06', fronthair='p16', rearhair='p02', eyes='p13', eyebrows='p06', mouth='p02', nose='p02', clothing='p14'),
             dict(skin=0, eyes=4, hair=19, hair2=19, cloth1=17, cloth2=3, cloth3=17, cloth4=3)),
 'Falin': mk('male', dict(face='p04', fronthair='p12', rearhair='p02', eyes='p21', eyebrows='p04', mouth='p05', nose='p03', clothing='p21', acca='p01'),
             dict(skin=3, eyes=0, hair=23, hair2=23, cloth1=16, cloth2=17, cloth3=16, cloth4=15, acca=16, acca2=17, acca3=16)),
}
def render(chars, out):
    n=len(chars)
    sheet=Image.new('RGBA',(n*(144+150)+10,200),(80,80,90,255)); d=ImageDraw.Draw(sheet)
    for i,(name,s) in enumerate(chars.items()):
        f=gen.compose_face(s); tv=gen.compose_tv(s)
        x=i*(144+150)
        sheet.alpha_composite(f,(x,20)); sheet.alpha_composite(tv,(x+146,4)); d.text((x+2,2),name,fill=(255,255,0))
    sheet=sheet.resize((sheet.width*2,sheet.height*2),Image.NEAREST); sheet.save(out)
if __name__=='__main__':
    render(CHARS, f'{SCR}/chars_v1.png')
