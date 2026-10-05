# RPGMXP: RPG Maker MZ foundation

Project folder: `C:\Users\Admin\Documents\RMMZ\RPGMZ` (RPG Maker MZ 1.10, JavaScript plugins).
Successor of the RMXP foundation (`claude/rank-foundation.md`): same Erdenkreis rank rules.
**The story build now lives on top of this foundation: see `claude/story-build.md`** (the whole story from the Prologue to the end of Act III, Story_Core, third-party plugins, credits). The generic test content described at the end of this file was replaced by the story build (backup: `RPGMZ\_backup_testbuild\`).

## Plugins (js/plugins, in this load order)
- **Rank_Core**: 7 stats, ranks, stat points, EXP curve, per-skill mastery, notetags, rank badges (`\RK[n]`, `\RKA[actorId]`). Commands: Gain / Refund Stat Points, Set / Gain Mastery, Complete Breakthrough.
- **Rank_Battle**: d20 vs AC, damage, GAP, saves, roles, escape, EXP by rank gap, mastery gain, victory report, breakthroughs, target preview (hit %, save %, damage range).
- **Rank_Menus**: rank badges, skill list mastery bars and info line, status / equip / shop windows, Stat Points screen (menu command; Right/OK +1, Left −1, Shift ×10, Confirm to spend).
- **Rank_Maps**: area and region ranks, encounter grace + ramp, weak-troop filter, HUD (area name, rank, danger gauge), `\RKM`. Commands: Show/Hide HUD, Reset Danger, Set Encounter Rate.
- Story build adds: McKathlin_DayNight, TausiLighting, WD_Core (stand-in), WD_Quest, **Story_Core** (after Rank_Maps).
Every number is a plugin parameter.

## Core rules
- Ranks F E D C B A S SS SSS V (Common … Divine); stats graded by 100s. Rank = grade of the average of the three best base stats.
- Stats STR DEX CON INT WIS CHA MAG, all 1 at level 1; 20 starting points, +20 per level, plus small natural growth from class aptitude (S 1.5 / A 1 / B 0.75 / C 0.5 / D 0.25 / E 0 per level). Assigned points cap at the top of the band above your rank (F 199, E 299 …). In the story build, gated actors are capped at the breakthrough gate instead (F 99 until the first story breakthrough).
- Native params mirror the stats (Attack = STR, Defense = CON, M.Attack = MAG, M.Defense = WIS, Agility = DEX, Luck = CHA; INT has no slot), so buffs, debuffs and Grow items work on stats.
- Hit: d20 + MOD + 8 vs AC (nat 1 miss, nat 20 hit; crit on 20, widened by crit traits and `<Crit Range>`). Damage: die + POW + 10 × rank, × GAP (×2, ×1.5, ×1, ×½, ×¼, WALL); weakness counts the gap one better; crit ×1.5.
- Area skills (all foes or several random): ×½ each, no attack roll. Saves: `<Save: STAT>` (half / negates / states), DC 13 + MOD (enemy vs actor 10 + MOD), trained +3, advantage/disadvantage at a gap of 2.
- Roles: minion ½ damage, elite +1 attack, boss +1 action, apex both; bosses shrug off every second disabling state, and those states last them one turn.
- HP = 10 + 2×CON + 5×level. MP = MAG × (0.8 + 0.5×rank) + 2×level + 8. EXP per actor by rank gap (two ranks below: nothing).

## Skill mastery
- Skills with an MP cost rank F → V on their own: 10 per use × foe factor × (1 + INT/400), plus kill bonuses by role. Plain attacks, guard and items never gain mastery.
- Bars 180 / 360 / 560 / 800 / 1100 / 1450 / 1900 / 2500 / 3300. A full bar needs a breakthrough: finish a next-rank foe with the skill (support skills: be used in a won fight against one). Each rank adds +5 to the skill's stat.
- A skill works at the lower of its mastery and its stat's grade (badge dims, help line says so). MP cost = base × (rank + 1)², INT cuts up to half.
- Skill notes: `<Stat: DEX>`, `<Body>` (half MP), `<At Rank C> die / hits / damage / bonus / hit / crit / state </At Rank C>`, `<Evolve C: id>`, `<Unlock D: id>`, `<Save: CON states>`, `<DC: +1>`, `<Area Rate: 75%>`, `<Support>`.

## Database conventions (MZ)
- Skill **Formula** box = die (`d8`, `2d6+3`); **MP Cost** = base cost.
- Weapon **Attack** box = damage die; armor **Defense** box = armor value (body armor competes with DEX MOD for AC; shield, head and accessory add). Notes: `<Stat>`, `<Rank>` (weapon grade bonus; heavy armor above your STR grade costs 2 AC and 5 initiative), `<STR: +5>` style bonuses.
- Class notes: `<Aptitude: STR A, …>`, `<Saves: STR, CON>`.
- Enemy stats come from the parameter boxes (same mapping as above); notes add `<Rank>`, `<Role>`, `<Attack Die>`, `<Attack Stat>`, `<Armor>` / `<AC>`, `<Saves>`. Suggested HP for a party of four: CON × (minion 0.5, standard 1, elite 2.5, boss 6, apex 12) — the story build scales F/E foes for a party of two.
- Map notes: `<Rank: E>`, `<Region 2 Rank: E>`, `<Safe Regions: 1>`, `<Region 3 Encounter: 150%>`, `<Encounter Grace: 30%>`, `<Area Name: …>`, `<No Rank HUD>`; story build: `<Weather: snow 5 unless 26>`, `<lighting: Outside>`, `<DayNight: step=1>`.

## Encounters
Map Encounter Steps stays the average distance. After a fight or map change: 40% of it with no fights, then the chance rises each step (measured: average 30 on a 30-step map, never before step 13; MZ default can fire after 1 step). Bushes count double. Troops two ranks below the party's best member stop attacking.

## Database ranges added in increment 3
| Table | Ids | What |
|---|---|---|
| Skills | 228–261 | Act III enemy skills |
| Skills | 321–337 | guest kits: Rin 321–323 (Battle Magic), Yukino 331–337 (Frost Arts) |
| Classes | 4, 5 | Battle-Mage (Rin), Frost Saint (Yukino) |
| Actors | 5, 6 | Rin (`<Rank: C>`, `<Guest>`, Auto Build), Yukino (`<Gated>`, Rank Weapon C/B/A, Breakthrough B/A) |
| States | 87–89 | Frost Body, Morgenwacht, Veil of Ash |
| Weapons | 38–41 | Kronenstab (Rin), Frostklinge, Mondeisklinge, Weißklinge (Yukino) |
| Armors | 100–101 | Rin's and Yukino's coats (the A-rank gear 96–99 existed; now sold in Salzhafen or given) |
| Enemies | 79–125 | chapters 7–9 (Calamities are `<Demon>`; Kagerō has `<Veil of Ash>`); 123–125 are chapter 5–6 variants (Heereshund, Heeresgargyl, Grabghul); battlers Riffketos and Tiefenkraken |
| Troops | 92–137 | 92 Gōen (ch. 6 pages), chapters 7–9 with the story pages of Tsumugi, Shirogane, Gōen and the three Kagerō phases; 74 and 82–91 changed (Rin's face, ch. 5–6 pages) |
| Items | 66–69, 72–76 | Dawn Regalia (key items 66–69); key items Turniermarke, Spinnensiegel, Gildenabschrift, Seekarte, Ruis Pfand |
| Common events | 4 | "Reisen": travel between the Act III hubs (options appear with their switches) |
| Variables | 12, 14–16 | 12 "Regalia" (Story_Core's Rank Pierce Variable), 14 "Voyage", 15–16 "Travel: Here" / "Travel: Choice" |
| Switches | `C3: Breakthrough E`, `C4: Breakthrough D` | added on 5 Oct: the in-battle breakthroughs of the Nordstraße and the Messingvogt run once |

## Story_Core additions (increment 3)
- **Message fit:** `Window_Message.startMessage` measures each line with `textSizeEx`; if the widest line is wider than the text area (with a face: about 616 px, 47 half-width characters of mplus-1m at 26 px), the message is drawn at `floor(26 × available / widest)` px, never below 18. Message-only codes (`\.` `\|` `\!` `\>` `\<` `\^` `\$`) are stripped before measuring so nothing waits or opens while measuring. Checked in the engine: the widest messages (60 characters) draw at 20 px inside the window.
- **Guests, regalia, Veil of Ash, travel:** see `claude/story-build.md` (Systems).

## Build pipeline (workspace)
- `tools/reconstruct_bases.py` → `story/base/MapNNN.json`: the base of each sample-based map, recovered from the last build (the sample maps are no longer needed; `load_sample` falls back to these).
- `story/base/registry.json`: switch and variable ids, loaded before any chapter module (`seed_registries`), so new content appends ids and old ones never move. Updated on 5 Oct to pin every id of the installed build (saves made now stay valid).
- `orig/data`: the builder reads States, Skills, Classes, System, Tilesets and Animations from it. Tilesets and Animations are the MZ template's (identical to the project's); States, Skills, Classes and System can be the last build's own files, because the builder only keeps the template entries it overwrites anyway (a rebuild from them is byte-identical).
- Generated maps: `tools/mapgen.py` (Gen: shapes, autotile painting, objects, cliffs, carving, shadows, prefab tile ids for Outside/Inside/Dungeon), `tools/story/terrain.py` (framed fields, canyons, plateaus, towns and houses, tents, ruins, dungeons, interiors, reachability checks), `tools/autotile.py` (autotile shapes), `tools/maprender.py` (PNG previews with events and passability; `TILEDIR=` the RTP tilesets), `tools/tilesheet.py` (tile id contact sheets).
- Tiles worth knowing (Outside tileset 2): A1 kind 0 sea has grassy shores, kind 1 sandy; kind 4 pond has snowy shores, kind 8 sandy, kind 12 earthy. A5 1539 deck planks (1538/1546 rail rows), 1541/1542/1543 pier planks.
- `tools/check_story.py`: reference checks, a static reachability playthrough (maps, switches, key items, story battles from New Game), and a node syntax check of every script command (`--rtp <img folder>` checks images against the RTP too).
- `tools/check_routes.py`: walks every scripted movement route that waits and isn't skippable from where its character stands; a blocked step (wall, another event: in MZ any event stops a moving event) would hang the scene for good. `--strict` checks all routes.
- `tools/battle_sim.py`: Python port of the combat rules for quick balance reads; `tools/tune_foes.py`: the HP / offence tuner (targets in its header); `tools/balance_scenarios.json`: the party settings per chapter. **The engine is the reference**: the simulator doesn't model states and buffs applied by skills (poison = 10% of max HP every turn until the fight ends, sleep songs, fear, webs, agility debuffs, Heerruf) or the party's support skills, so it runs far kinder on foes that poison, put to sleep or drain. `tools/scen_tune.js` finds an enemy's offence factor (STR, DEX, MAG; an optional fixed HP factor) in the engine by bisection; the corrections live in `tools/story/engine_tune.py` (18 foes, applied after the database is built). `tools/scen_story_bal2.js` confirms a chapter in the engine (`fresh`/`reset` re-arm the once-only breakthrough pages, `abortWin` counts a story abort as a win, `log` prints a battle log). The engine results per troop are at the top of `handoff/balance.txt`.
- Engine scenarios (`tools/run_game.js`, headless Chromium): see the list in `claude/story-build.md`.

## Former test content (replaced by the story build, kept in `_backup_testbuild`)
Party Reid / Michelle / Eliot / Kasey; generic F/E enemies up to the Wolfman; Hub, Field and Deep Woods maps.

## Verified
Real MZ engine in headless Chromium plus the editor's playtest: menus, stat screen, battles, breakthrough / evolve / unlock, support breakthrough, save/load, NPC events, encounter spacing, weak-troop filter, boss shrug. Story build: playthrough tests from New Game to the end of chapter 4, every map and NPC event of chapters 5–9, and the finale to the title screen (see `claude/story-build.md`).

## Not done yet
Aura clashes, CHA shop discounts, armor ranks beyond the heavy-armor penalty, custom art/UI skin. Resolution left at MZ's default 816×624.
