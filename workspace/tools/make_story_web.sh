#!/bin/bash
# Assemble a runnable web copy of the story build for headless tests.
set -e
python3 /home/claude/mz/tools/build_story.py
W=/home/claude/mz/sweb
rm -rf $W && mkdir -p $W/js/plugins $W/data
cp /home/claude/mz/orig/index.html /home/claude/mz/orig/package.json $W/
cp /home/claude/mz/orig/js/main.js /home/claude/mz/orig/js/rmmz_*.js $W/js/
cp -r /mnt/user-data/uploads/RPGMZ/js/libs $W/js/libs
for d in img fonts css icon; do cp -r /mnt/user-data/uploads/RPGMZ/$d $W/$d; done
cp -r /home/claude/mz/story/out/img/* $W/img/
cp /home/claude/mz/story/out/data/*.json $W/data/
cp /home/claude/mz/story/out/js/plugins/*.js $W/js/plugins/
cp -r /home/claude/tausi/tausi-lighting $W/tausi-lighting
cp /home/claude/mz/tools/ZZ_TestHarness.js $W/js/plugins/
python3 - <<'PY'
src=open('/home/claude/mz/story/out/js/plugins.js').read()
entry='{"name":"ZZ_TestHarness","status":true,"description":"test only","parameters":{}}'
src=src.replace('\n];', ',\n'+entry+'\n];')
open('/home/claude/mz/sweb/js/plugins.js','w').write(src)
PY
echo "story web ready"
