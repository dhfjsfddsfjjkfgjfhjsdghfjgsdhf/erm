Erdenkreis (RPG Maker MZ) - Claude's build workspace, backup of 2026-09-29 21:10 (Europe/Berlin)

What this is
  The source that builds the game in C:\Users\Admin\Documents\RMMZ\RPGMZ: Python builders for the database,
  maps and events, the plugins, the headless test scenarios, and the latest built output (story/out).
  Everything after "increment 2" (portraits, the Act II-III skill kits, Chapter 4) exists only here and in
  story/out; it has NOT been copied into the RPG Maker project yet.

Layout
  tools/build_story.py        builds everything into story/out (python3 tools/build_story.py)
  tools/story/*.py            db.py (database), foes.py (Acts II-III foes, items, gear), common.py (event/map
                              helpers), prologue.py, ch1-ch4.py, act2.py, cast.py, ids.py, lighting.py, overlays.py
  tools/make_story_web.sh     build + copy into a browser-runnable test copy (needs the MZ engine files)
  tools/run_game.js + scen_*  headless Playwright tests (scen_story_ch4.js = chapter 4 playthrough,
                              scen_story_bal2.js = balance sims, scen_story_kits.js = skill kit tests)
  plugins/                    Rank_Core, Rank_Battle, Rank_Menus, Rank_Maps, Story_Core (1900 lines), WD_Core stand-in
  thirdparty/                 TausiLighting, WD_Quest (third-party, credits in the build notes)
  story/PLAN.md               the original build plan
  story/img/                  portraits (Kanta, Hanma, Falin), cast sprites
  story/out/                  the latest build: data/*.json, img/, js/ (copy into the MZ project to install)
  gen/                        character-generator scripts used for the cast art

Inputs the builder expects (from the uploads, not included here)
  /mnt/user-data/uploads/samplemaps   RPG Maker MZ sample maps (MapNNN.json)
  /mnt/user-data/uploads/RPGMZ        the RTP project (img, audio, data)
  /mnt/user-data/uploads/{pack,dragonspack1_sd,kamedran,rt5monster,dlc,generator}  battler and generator art
