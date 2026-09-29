#!/bin/bash
# Render sample maps with coordinates: render_maps.sh 208,211,202 [px] [--pass]
# Output: $SCR/render/map<id>_grid.png
set -e
IDS=$1; PX=${2:-32}; PASS=$3
SCR=/tmp/claude-0/-home-claude/e205e0a3-bd62-5461-b21e-25640739d4b9/scratchpad
W=${WEBROOT:-/home/claude/mz/web}
SRC=${MAPSRC:-/mnt/user-data/uploads/samplemaps}
cp -rn /mnt/user-data/uploads/RPGMZ/img/* $W/img/ 2>/dev/null || true
for id in ${IDS//,/ }; do
  f=$(printf "Map%03d.json" $id)
  if [ "$SRC" != "$W/data" ]; then cp $SRC/$f $W/data/$f; fi
done
mkdir -p $SCR/render
cd /home/claude/mz && MAPS=$IDS node tools/run_game.js tools/scen_render.js $SCR/render 2>&1 | grep -v "^shot" | tail -20
for id in ${IDS//,/ }; do
  f=$(printf "Map%03d.json" $id)
  python3 tools/render_grid.py $W/data/$f $SCR/render/map$id.png $SCR/render/map${id}_grid.png $PX $PASS
done
