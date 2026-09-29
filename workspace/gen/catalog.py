import json, copy, glob, re, os, sys
from PIL import Image, ImageDraw
import gen
SCR='/tmp/claude-0/-home-claude/e205e0a3-bd62-5461-b21e-25640739d4b9/scratchpad'
def base(gender='male'):
    return {"gender":gender,"patterns":{"body":"p01","face":"p01","fronthair":"p01","rearhair":"p01","beard":"","ears":"p01","eyes":"p01","eyebrows":"p01","nose":"p01","mouth":"p01","facialmark":"","beastears":"","tail":"","wing":"","clothing":"p01","cloak":"","acca":"","accb":"","glasses":""},
      "colors":{"#F9C19D":2,"#2C80CB":0,"#FCCB0A":23,"#AE8682":15,"#FE9D1E":16,"#1C76D0":17,"#D8AC00":1,"#D3CEC2":15,"#C78407":16,"#C0D3D2":15,"#999999":16},"offsets":{}}
def ids(gender, part):
    s=set()
    for f in glob.glob(f'/mnt/user-data/uploads/generator/Face/{gender}/FG_{part}*_p*.png'):
        m=re.search(r'FG_'+part+r'\d?_p(\d+)',os.path.basename(f))
        if m: s.add(int(m.group(1)))
    return sorted(s)
def sheet(gender, key, part, name, tweak=None, cols=8, size=120):
    G={'male':'Male','female':'Female'}[gender]
    ps=ids(G, part)
    rows=(len(ps)+cols-1)//cols
    out=Image.new('RGBA',(cols*size,rows*(size+14)),(70,70,80,255)); d=ImageDraw.Draw(out)
    for i,p in enumerate(ps):
        s=base(gender); s['patterns'][key]='p%02d'%p
        if tweak: tweak(s)
        im=gen.compose_face(s).resize((size,size),Image.LANCZOS)
        x=(i%cols)*size; y=(i//cols)*(size+14)
        out.alpha_composite(im,(x,y+14)); d.text((x+3,y+1),f'{part} {p}',fill=(255,255,0))
    out.save(f'{SCR}/cat_{gender}_{name}.png'); print(name,len(ps),out.size)
if __name__=='__main__':
    g=sys.argv[1]
    sheet(g,'fronthair','FrontHair','fronthair')
    sheet(g,'rearhair','RearHair','rearhair', lambda s: s['patterns'].update(fronthair='p05'))
    sheet(g,'clothing','Clothing','clothing')
    sheet(g,'acca','AccA','acca'); sheet(g,'accb','AccB','accb'); sheet(g,'cloak','Cloak','cloak')
    sheet(g,'eyes','Eyes','eyes'); sheet(g,'mouth','Mouth','mouth'); sheet(g,'eyebrows','Eyebrows','eyebrows'); sheet(g,'face','Face','face'); sheet(g,'facialmark','FacialMark','facialmark')
