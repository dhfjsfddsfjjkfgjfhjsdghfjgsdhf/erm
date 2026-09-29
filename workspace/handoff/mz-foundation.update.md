# mz-foundation.md — new sections (increment 3)

Merge these into `claude/mz-foundation.md` in the MZ project.

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
| Enemies | 79–122 | chapters 7–9 (Calamities are `<Demon>`; Kagerō has `<Veil of Ash>`) |
| Troops | 92–137 | 92 Gōen (ch. 6 pages), chapters 7–9 with the story pages of Tsumugi, Shirogane, Gōen and the three Kagerō phases; 74 and 82–91 changed (Rin's face, ch. 5–6 pages) |
| Items | 72–76 | key items: Turniermarke, Spinnensiegel, Gildenabschrift, Seekarte, Ruis Pfand |
| Common events | 4 | "Reisen": travel between the Act III hubs (options appear with their switches) |
| Variables | 12, 14–16 | 12 "Regalia" (Story_Core's Rank Pierce Variable), 14 "Voyage", 15–16 "Travel: Here" / "Travel: Choice" |

## Story_Core additions
- **Message fit:** `Window_Message.startMessage` measures each line with `textSizeEx`; if the widest line is wider
  than the text area (with a face: 620 px, about 47 half-width characters of mplus-1m at 26 px), the message is
  drawn at `floor(26 × available / widest)` px, never below 18. Message-only codes (`\.` `\|` `\!` `\>` `\<` `\^`
  `\$`) are stripped before measuring so nothing waits or opens while measuring.

## Build pipeline (workspace)
- `tools/reconstruct_bases.py` → `story/base/MapNNN.json`: the base of each sample-based map, recovered from the
  last build (the sample maps are no longer needed; `load_sample` falls back to these).
- `story/base/registry.json`: switch and variable ids of the Chapter 4 build, loaded before any chapter module
  (`seed_registries`), so new chapters append ids and old ones never move.
- Generated maps: `tools/mapgen.py` (Gen: shapes, autotile painting, objects, cliffs, carving, shadows, prefab tile
  ids for Outside/Inside/Dungeon), `tools/story/terrain.py` (framed fields, canyons, plateaus, towns and houses,
  tents, ruins, dungeons, interiors, reachability checks), `tools/autotile.py` (autotile shapes),
  `tools/maprender.py` (PNG previews with events and passability), `tools/tilesheet.py` (tile id contact sheets).
- Tiles worth knowing (Outside tileset 2): A1 kind 0 sea has grassy shores, kind 1 sandy; kind 4 pond has snowy
  shores, kind 8 sandy, kind 12 earthy. A5 1539 deck planks (1538/1546 rail rows), 1541/1542/1543 pier planks.
- `tools/check_story.py`: reference checks, a static reachability playthrough (maps, switches, key items, story
  battles from New Game), and a node syntax check of every script command.
- `tools/battle_sim.py`: Python port of the combat rules for balance reads; `tools/tune_foes.py`: the HP / offence
  tuner (targets in its header); `tools/balance_scenarios.json`: the party settings per chapter.
- `tools/scen_story_act3.js`: engine smoke run for chapters 5–9 and the finale (new, not yet run).
