"""Inserts the player characters' portraits into the story build.

usage: python3 insert_portraits.py KANTA.png HANMA.png FALIN.png [project_img_dir]

- The exact source PNGs are copied unchanged to img/pictures/Portrait_<Name>.png.
- MZ draws faces from 144x144 cells, so each portrait is also scaled (Lanczos) into
  slot 0 of a 576x288 face sheet img/faces/<Name>.png (the other seven slots stay empty).
  Every message, menu and battle face of that character uses slot 0.
"""
import os, shutil, sys
from PIL import Image

NAMES = ["Kanta", "Hanma", "Falin"]
CELL = 144

def main():
    srcs = sys.argv[1:4]
    if len(srcs) != 3:
        sys.exit(__doc__)
    out = sys.argv[4] if len(sys.argv) > 4 else "/home/claude/mz/story/img"
    os.makedirs(f"{out}/faces", exist_ok=True)
    os.makedirs(f"{out}/pictures", exist_ok=True)
    for name, src in zip(NAMES, srcs):
        shutil.copyfile(src, f"{out}/pictures/Portrait_{name}.png")
        im = Image.open(src).convert("RGBA")
        side = min(im.size)                         # centre-crop to a square if needed
        left, top = (im.width - side) // 2, (im.height - side) // 2
        im = im.crop((left, top, left + side, top + side)).resize((CELL, CELL), Image.LANCZOS)
        sheet = Image.new("RGBA", (CELL * 4, CELL * 2), (0, 0, 0, 0))
        sheet.paste(im, (0, 0))
        sheet.save(f"{out}/faces/{name}.png")
        print(f"{name}: {src} -> faces/{name}.png (slot 0), pictures/Portrait_{name}.png")

if __name__ == "__main__":
    main()
