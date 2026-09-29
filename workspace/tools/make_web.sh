#!/bin/bash
# Assemble a runnable web copy of the project for headless testing.
set -e
python3 /home/claude/mz/tools/build_db.py > /dev/null
W=/home/claude/mz/web
rm -rf $W && mkdir -p $W/js/plugins $W/data
cp /home/claude/mz/orig/index.html /home/claude/mz/orig/package.json $W/
cp /home/claude/mz/orig/js/main.js /home/claude/mz/orig/js/rmmz_*.js $W/js/
cp -r /mnt/user-data/uploads/RPGMZ/js/libs $W/js/libs
for d in img fonts css icon; do cp -r /mnt/user-data/uploads/RPGMZ/$d $W/$d; done
cp /home/claude/mz/out/data/*.json $W/data/
cp /home/claude/mz/out/js/plugins/*.js $W/js/plugins/
cp /home/claude/mz/tools/ZZ_TestHarness.js $W/js/plugins/
python3 - <<'PY'
import re
src=open('/home/claude/mz/out/js/plugins.js').read()
entry='{"name":"ZZ_TestHarness","status":true,"description":"test only","parameters":{}}'
src=src.replace('\n];', ',\n'+entry+'\n];')
open('/home/claude/mz/web/js/plugins.js','w').write(src)
PY
echo "web ready"
