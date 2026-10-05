# Erdenkreis (RPG Maker MZ): the story build

Installed in `C:\Users\Admin\Documents\RMMZ\RPGMZ` (increment 3, 2026-10-05; increment 2 was 2026-09-29). Built on the rank foundation (`claude/mz-foundation.md`).
**The whole story is playable from New Game:** Prologue → Act I (chapters 1–3) → Act II (opening, chapters 4–6) → Act III (chapters 7–9) → epilogue → title screen. 83 maps, 35 quests.
Every player character is a woman with a masculine look (she/her): Kanta, Hanma, Falin and the guests Rin and Yukino. Cast art was assembled from the generator's male parts; Rin and Yukino use RTP sprites and faces.

## Structure
| Part | Maps (id) | Level / rank | Content |
|---|---|---|---|
| Prologue "Erwachen" | Erwachenshöhle 1, Kiefernkamm 2, Karrenweg 3, Kiefernwald 4 | 1–3, F | Kanta wakes in the dark with Hanma; the two-tail's den (bow / back away / touch the hoard → unwinnable fight → vessel revival tutorial); road or trees to Rabenau |
| Ch1 "Rabenau" | 5–14 | 3–7, F | Tōdō at the gate, inn deal, night goblin raid, Elder Okuda, Rabenholz, the old watchtower, boss Krummzahn + Grauzahn, the black raven feather, Natsu's piglets, Sagara hires the pair |
| Ch2 "Die Oststraße" | 20–29 | 7–12, F | Escort east (kamaitachi, deserters' toll, silver bowl), wayside shrine camp, frozen Eisfurt, Vogt Shirakawa, shrine maiden Aika, Frostpfad, Eisfallhöhle, Eiswurm, Fubuki yields, the thaw |
| Ch3 "Die Königsstraße" | 40–48 | 12–15, F → E | Ueda's ferry, the road to Wachtburg, Guild registration, three rank F jobs, the Nordstraße emergency and Kanta's first breakthrough (F → E), optional Wolfsgrube trial |
| Act II "Die Wacht" (opening) | 60–62 | 15+, E | Wallstraße north, Frontposten 3 and Captain Mori, the night assault on the breach, Falin joins, the Aschenschwinge, dawn |
| Ch4 "Die Wallfeste" | 63–70 | 15–21, E → D | Wallweg, the Marshal's audience, the brass coins, Frontposten 5 (optional), the old cistern, the night raid: breakthrough to D |
| Ch5 "Weißenfels" | 75–80 | 21–27, D | Rin's march, the dawn assault, the sluices, the hull forge, the dragon Shiranui, the Iron Prince |
| Ch6 "Der Messingtyrann" | 90–93 | 27–31, D → C | The siege of the Wallfeste, the gate tower, the Seelenkessel, Gōen's rank wall: breakthrough to C; Yukino joins; end of Act II |
| Ch7 "Die Kaiserstadt" | 100–108 | 31–41, C → B | Lichtenhall, the Sonnwende tournament, Tsumugi: breakthrough to B, the Morgenklinge (regalia 1/4); the travel menu opens |
| Ch8 "Wald und Tiefe" | 110–118 | 41–47, B | Hirschheim, the fox shrine (Sternlaterne 2/4), the Tiefgrube (Heldenhorn 3/4), Hanma's story, Mukuro |
| Ch9 "Morgenröte" + epilogue | 120–130 | 47–55, B → A | Salzhafen, Rui's ship, the Knochenriff (Aschenkrone 4/4), Shigure, the burning Urwald: breakthrough to A, Kagerō in three phases, four epilogue scenes, back to the title |

## Chapter 3 in detail
- **Königsstraße (40)**: refugees from Kaltenbrunn (ash hounds came round the Wall), 3 Heilwurz, 2 chests, campfire rest.
- **Wachtburg (41)**: gate guards, castle closed, Church sister looking for "light", soldier on leave (first mention of *die Eiserne*), refugees. Doors: Guild, inn *Zum Wachtfeuer*, royal smith, Aoyagi's outfitter, granary (opens with the job).
- **Guild (42)**: Hoshino Miyu registers the party: 1 gk, oath on Sabaki's scales, Wahrheitskristall reads F with an "empty imprint" (16 days of history); the crystal doesn't see Hanma at all; branch master Kurogane Isao: "a dead hand leaves no imprint", registers her as Kanta's contracted spirit. The player names the party (default *Rabenfeder*, `\N[4]`). Kanta's title: *Neuling*. Okuda's letter + feather → 1 gk 5 sl bounty for Krummzahn. Rivals: Hayami Kyōsuke (Silberne Falken), Kuroda Raiden (Blutmond).
- **Jobs** (counter): *Ratten im Kornspeicher* (granary vaults, boss Schimmelmutter), *Wölfe an der Nordstraße* (pack leader), *Heilwurz für das Lazarett* (5 of 6 herbs). Two paid jobs trigger the **emergency**: refugee column on the Nordstraße vs ash hounds. Turn 2 of that battle: the Leitrüde goes for the children, Kanta takes the bite on her sigil arm → **Breakthrough to E** (beam → Lichtdolch, Returning Fang, Hanma rises with her); the flare burns the small hounds to ash and strips 50 from the Leitrüde. The crystal then reads E; 3 gk; Kurogane sends them to the Wall.
- **Kaji Tōbei** refits the Silberrüstung into the **Echtsilberrüstung** (armor 5, rank E) for 1 gk 5 sl; sells rank E gear.
- **Wolfsgrube (48, optional)**: three Dire Wolves (Schreckenswolf, E); first clear → title *Wolfsbann* + Wachtfeuer-Amulett (WIS +10, preemptive/no surprise).

## Act II opening
Wallstraße (snow, ash hounds, ash corpses, a wrecked supply cart) → Frontposten 3: Mori Daisuke briefs them; sleep via Sergeant Kōno → midnight bell → through the inner gate to **Die Bresche**. Falin holds the gap alone; she says Kanta "smells like nothing", Hanma names her a vessel; Falin joins mid-scene (Sync Level to Kanta, Auto Build, Catch Up to rank E) → Vorhut fight → **Aschenschwinge** boss → dawn talk → Falin leaves the breach with them. Quest *Die Wallfeste* leads into chapter 4.

## Chapter 4 · Die Wallfeste (rank E → D, LV ~16–23)
Quests 17 *Messingmünzen*, 18 *Frontposten 5* (optional), 19 *Die Zisterne*, 20 *Weißenfels*.
- **63 Wallweg** (card "Kapitel 4 · Die Wallfeste"): a lone hellhound (rank D) over the courier Ichijō; the Marshal's orders, word of sentries dead with brass coins on their eyes.
- **64 Wallfeste** (the command fort; camp fire, barracks 66, Lazarett 67, Zeughaus 68) → **65 Marschallhalle**: Marshal Kōsaka Tetsuji doubts a rank E killed the Aschenschwinge until Falin walks in; Crown Princess **Asahina Rin** arrives with her father's refusal and asks for the Crown's two thousand for Weißenfels; Hanma reads the coins as Gōen's soul fee. Kōsaka: find the seller first.
- **Clues** (3): healer Yukimura Saki's brass coins (Lazarett), quartermaster **Nishiki Eiji** runs and leaves his ledger and the cistern key (Zeughaus), Sentry Kazama saw lights under the ice.
- **69 Frontposten 5** (optional, recommended LV 19): gargoyles and hellhounds on every floor; Sergeant Tōdō Ren and her three walk home.
- **70 Alte Zisterne**: Nishiki confesses (his wife Mariko and daughter Aya are slaves in Weißenfels' forge); the **Messingschreiber** (brass scribe) fights while he runs for the gate.
- **The night raid**: hounds through the sally port, then the **Messingvogt**; on turn 2 its chain goes for Rin and Kanta takes it → **breakthrough to D** (Lichtklinge and Lichtlanze, Radiant Edge, Lance Charge; Hanma's and Falin's rank D gear). Nishiki's contract comes due: he turns to brass. Morning: Kōsaka's writ (Siegelbrief) and 3,000 kl; Rin marches on Weißenfels.

## Increment 3: the rest of the story (built 29 Sept 2026 in a cloud session, tested and installed 5 Oct 2026)
Maps 75–80, 90–93, 100–108, 110–118, 120–130. Quests 21–35. Switch names start with the chapter (`C5:` … `C9:`); all switch and variable ids are pinned in `story/base/registry.json`.

### Chapter 5 · Weißenfels (party rank D, LV ~21–27)
- 75 Grauklamm: Rin's march; canyon, wyvern dives, chained thralls, a camp fire.
- 76 Heerlager: Rin's red command tent, the council (Rin, Sōma, Hikari), Saki's quest "Mariko und Aya", quartermaster, the fire talk; sleep in the party tent → the assault at 4:00.
- 77 Weißenfels Unterstadt: the breach, the chain gang (quest "Die Kettenkolonne", optional), Sōma; the NW tower door → 78 Alter Aquädukt (two sluices open the water gate) → 79 Hüllenschmiede (racks of empty armors, Falin's memory "Wake up, Falin. Please.", Mariko and Aya, the Aschenschmied boss at the furnace, the winch that opens the citadel gate).
- Rin joins as a guest at the citadel gate → 80 Drachenhalle: Shiranui chained as the forge fire, the Iron Prince (Hayato, Rin's brother), Falin breaks the null-iron, Shiranui's scale (Drachenschuppe), the Königliches Wappen, Rin leaves the party; card "Weißenfels ist frei" → the Wallfeste under siege.

### Chapter 6 · Der Messingtyrann (rank D → C)
- 92 Wallfeste (siege; tiles of map 64): Kōsaka, Rin, the cook's rest, the clerk's shop; the north gate → 90 Torturm (three floors side by side, visible foes, the Oni-Hauptmann at the winch).
- 93 Frontposten 3 (siege; tiles of 61): the hound yard, Mori's sally port → 91 Heerlager der Asche: ash camp, patrols, the Seelenkessel (boss), Gōen's offer and the unwinnable fight: turn 2 the chain on Hanma → **breakthrough to C**; Yukino's ice wall.
- Back at Frontposten 3: the fire talk (Kagerō is Kurenai Tōma; the Morgenwacht; Hanma on the regalia; Rin's letter), **Yukino joins** (actor 6), "Ende des zweiten Akts" → Act III.

### Chapter 7 · Die Kaiserstadt (rank C → B)
- 100 Kaiserstraße (card "Akt III · Morgenröte", ambush, the Spinnensiegel) → 101 Lichtenhall (palace, Morgendom, guild, inn, arena, Akira's statue, plaza shops).
- 104 Morgendom: Amane Kiyoko and the tournament; 107 Gilde: Kirishima registers the team (Turniermarke).
- 103 Kaiserarena: four rounds (Eiserne Brüder, Arenabestie, Klingen von Ostmark, Kanemoto Gōki) with a healer between; the ceremony: Tsumugi seizes the Empress's box and flees below.
- 105 Unterhallen (cocoons) → 106 Spinnenhalle: Tsumugi (rank B under the dawn seal), turn 2 **breakthrough to B**, the **Morgenklinge (regalia 1/4)**; Kiyoko; 102 Kaiserpalast: the Empress's audience (20,000 kl, legions north); the Guild record of 313 (Gildenabschrift) → **travel menu** opens.

### Chapter 8 · Wald und Tiefe (rank B)
- 110 Waldweg (the packlord, optional quest from Ōkami Sōta) → 111 Hirschheim (Countess Kagura, Sōta, Kusaki's gift).
- 112 Fuchsschrein: Nanami, the stone fox riddle, Shirogane's game at the silver pool → **Sternlaterne (2/4)**.
- 115 Eisenberg (Iwakura, Tsurugi, the Grubenlampe) → 116 Tiefgrube (the miners) → 117 Untere Tiefgrube → 118 Trollhalle: the Troll King → **Heldenhorn (3/4)**.
- Hanma tells her story at the inn in Hirschheim (after the second regalia).
- 113 Urwald: the leshy wants Kusaki's bread and salt → 114 Hirschthron: Mukuro (boss); the Waldkrone; the messenger from Salzhafen.

### Chapter 9 · Morgenröte (rank B → A)
- 120 Salzhafen (Hisa, Sayo's shrine, the chandler, three piers) and 130 Der Ertrunkene Mann (inn, Kaizaki Rui: Seekarte, Ruis Pfand).
- 121 Die Seeschwalbe: voyage 1 (drowned men board) → 122 Knochenriff (reef, camp fire, chests) → 123 Versunkene Halle (Fomori, the chief on the throne of anchors → **Aschenkrone (4/4)**).
- Voyage 2: the Sturmsee, Shigure on the Kraken; Rui's gift (Drachenknöchel); back in port Sayo's five seals, the League's reward, the messenger: the Urwald burns.
- 124 Brennender Urwald (from Hirschheim's south road): Kagura's rangers, the burned leshy (heals), Gōen in the clearing, at half HP the chain again → **breakthrough to A**; the contract burns.
- 125 Hirschthron (Nacht): the Sternlaterne rest; Kagerō → Hōkai's shadow → Kurenai Tōma (ends when Yukino says his name); dawn; "Wochen später".
- Epilogue 126 Wallfeste (Yukino leaves), 127 Weißenfels (Rin buries the sword), 128 Rabenau (Hayate, Tōdō), 129 Kiefernkamm (Hanma: "Always."), card "Erdenkreis · Ende", credits, title screen.

## Inventions and deviations (flag to the user; change freely)
**Acts I–II (increments 1–2)**
- **Falin's backstory** (the docs only say "living armor, fused plate, joins ≈⅓"): she woke in the snow outside Weißenfels the night it fell (1041), inside the armor, remembering nothing; FALIN is scratched inside the breastplate; the plate grew into her and bleeds when she bleeds; she held the Frontposten 3 breach for six years. She is also an empty vessel (not stated in canon).
- Hanma is invisible to the Wahrheitskristall ("a dead hand leaves no imprint").
- Piglets instead of Natsu's sheep (no sheep sprite in MZ's RTP).
- Vessel revival costs 10% of the money (a game concession; canon only says the new vessel has nothing).
- Emergency pay 3 gk and job pay (1 gk 2 sl, 1 gk, 8 sl) are scaled down from WORLD§9 so early money stays meaningful.
- The Aschenschwinge, Leitrüde, Schimmelmutter, Harpyie, Kragenechse, Aschenleiche, Leere Rüstung are my monsters for the Wall/road (miasma-touched ones have the +50 baked into their stats).
- Chapter 4: Nishiki Eiji sold the Wall to buy back his wife Mariko and daughter Aya; the Messingschreiber and the Messingvogt are Gōen's clerks; Nishiki turns to brass when his contract comes due.

**Act II–III (increment 3, the cloud session's list)**
- People: Asahina Hayato (Rin's brother) is the Iron Prince of Weißenfels; Mariko is the woman who woke Falin in the hull forge and scratched every name; Shiranui is a dragon chained as the forge fire (her scale: the Drachenschuppe); Shigure was the Morgenwacht's lance; Kirishima Daigo keeps the Guild record of 313; new NPCs Ōkami Sōta, Gräfin Kagura Yui, Kitsunezaki Nanami, Shirogane, Förster Kusaki, Iwakura Gōtetsu, Tsurugi, Minato Hisa, Bootsmann Kaji, Wirt Unagi, Ise, Wirtin Hoshi, Arenameister Ishikawa (canon names: Kujō Sayaka, Kaizaki Rui, Namiji Sayo, Kanemoto Gōki).
- Hanma's backstory (told in Hirschheim after the second regalia): Sōryū Akira's youngest general, the purges with the Death arts, Akira taking her command at Frostheim, Gōen's contract for her anger, Akira refusing it for her: "the General who was refused".
- Guests: Rin (actor 5, Battle-Mage, fixed rank C) in chapter 5 only; Yukino (actor 6, Frost Saint, gated like the party) from the end of chapter 6.
- Places: the Morgenklinge is the tournament prize stolen by Tsumugi; the Sternlaterne is Shirogane's at the fox shrine; the Heldenhorn is in the Troll King's hoard; the Aschenkrone sits on the Fomorian chief of the Knochenriff. The Hirschthron is the fifth seal and the final battle is there (the Nachtfeste isn't built). Gōen is fought twice (Heerlager: rank wall, breakthrough to C; burning Urwald: breakthrough to A). Kagerō in three battles (Maō Kagerō → Hōkai's shadow → Kurenai Tōma, ended by Yukino saying "Tōma."); the party is healed between phases.
- 33 of the 39 new maps are generated (no MZ sample maps were available); the other six reuse earlier maps' tiles (the two siege maps, the four epilogue maps). 44 new battlers are recoloured/resized RTP battlers.

**Where increment 3 departs from `claude/story-outline.md`** (decide which version you want)
- Falin: the outline makes her the Morgenwacht's shield-bearer whose soul Tōma kept and forged into a vessel ("Wake up, Falin" in his voice), and Yukino speaks again when she sees her. The build keeps Falin's origin unknown: Mariko woke an unnamed young soldier's soul in the forge, and Yukino has no tie to her.
- The finale: the outline has the Veil (phase 1), the Demon Lord (phase 2), Yukino's "Tōma.", then Hōkai's whisper ended by Hanma's Purge and Kanta's light, Kaede renewing the seal and Tōma dying in Yukino's arms. The build runs Kagerō → Hōkai's shadow → Tōma, ends on Yukino's word, and Tōma turns to ash after his last lines; Kaede doesn't appear.
- Hanma's truth comes in Hirschheim (chapter 8), not at the Morgendom (chapter 7); her story is Akira's refusal of Gōen's contract rather than the failed Purge and the dying oath.
- Shiranui doesn't carry the party north in chapter 9; the Urwald is reached by the south road from Hirschheim.

## Systems added for the story (Story_Core.js)
Bound actor (Hanma mirrors Kanta's level/rank, earns no EXP), breakthrough gate (stats capped at the band until a story breakthrough), rank gear (Kanta's DW weapon, Falin's fused plate change form with the gate), vessel revival at the last rest point, passives and party auras, barrier (temp HP), Interpose, follow-player lights, money in gk/sl/kl, calendar + clock in the menu, chapter cards, **per-map weather** (`<Weather: snow 5 unless 26>`; untagged maps are clear), **Ground_ TausiLighting layers** (drawn under characters: Eisfurt's frozen river), **Catch Up** for gated actors who join after a breakthrough.
Increment 3: **guest fighters** (`<Guest>`, fixed `<Rank: C>`, Auto Build); **Dawn Regalia** (key items 66–69; variable 12 "Regalia" is the Rank Pierce Variable: against `<Demon>` foes each regalia cancels one rank of difference, never past even; `<Veil of Ash>` holds until four); **travel menu** (common event 4 "Reisen" from any Act III city gate); **message fit** (a message whose widest line doesn't fit is drawn smaller, down to 18 px, instead of being cut off; about 850 face messages use it, Act I included, mostly at 20–22 px). Every scripted in-battle breakthrough (Nordstraße, Messingvogt, Tsumugi, both Gōen fights) now happens once only, even after a defeat and a rematch.

## Third-party plugins and art in use (credits)
- TausiLighting 0.1.8 by MelekTaus (Tausi): lighting, the `tausi-lighting/` folder at the project root (installed; the plugin also unpacks it itself).
- WD_Quest by Winthorp Darkrites: quest log (menu command "Quests"). **WD_Core is a stand-in** written for this project (minimal API); replace it with the official WD_Core if you get it.
- McKathlin_DayNight 2.1.1 (MIT): time of day, tints, calendar source.
- Battlers from RPGMakerWarehouse / @theartofnemo: Eiswurm (glacial serpent), Fubuki (Shiva), Aschenschwinge (kamedran); Act I–II DLC monster art by Yutaro Tsuyuki.
- RPG Maker MZ RTP (Gotcha Gotcha Games / KADOKAWA): tilesets, characters, faces, battlebacks, audio, and the source of the 44 recoloured Act II–III battlers (Ketos and Kraken are saved as `Riffketos` and `Tiefenkraken` so the RTP's own files stay untouched).
- Not used: AuraMZ (a complete game template, would replace much of the engine), Pixel Crawler (16 px pixel art, doesn't match MZ's 48 px RTP).

## Balance
- Acts I–II (auto-battle, engine): Ch3 road/vault/wolf fights at L12: 80–95% HP left. Schimmelmutter L12: 100% wins, 45% HP left. Rudel L12: 100%, 26%. Emergency L12: 100%, 44%. Wolfsgrube L15 (two): 100%, 34%. Breach Vorhut L15 (three): 100%, 71%. Aschenschwinge L15: 100%, 40%.
- Acts II–III (your direction: regular encounters fairly difficult, bosses very difficult). The cloud session tuned them with the Python simulator (`tools/battle_sim.py`), which doesn't model poison (10% of max HP every turn until the fight ends), sleep songs, fear, webs, debuffs, enemy buffs or the Seelenkessel's drain healing it. In the engine ten bosses and mid-bosses came out as walls (0–25% auto-battle wins) and six regular fights at 25–75%.
- **Engine-tuned (5 Oct 2026, the reference):** `tools/story/engine_tune.py` scales the offence (STR, DEX, MAG; DEX is also their AC) of 18 foes and the HP of three (Grabghul, Seelenkessel, Trollkönig) after the database is built; every factor was found by bisection in the engine. Auto-battle results on the installed data: regular fights 92–100% with 33–74% HP left (3–9 rounds); mid-bosses Oni-Hauptmann 70–85%, Arenabestie 80%, Klingen von Ostmark 60%, Ketos 75%, Rudelherr (optional) 50%; bosses Aschenschmied 45%, Iron Prince 60%, Seelenkessel 60% (a long fight, 13–17 rounds: it heals from what it drains), Kanemoto Gōki 60%, Tsumugi 45%, Trollkönig 50%, Mukuro 50%, Fomorer-Häuptling 55%, Shigure 65%, Gōen in the Urwald 45%, the final battle Kagerō 70% then Hōkai's shadow 35% (healed in between). Chapter 4's Messingvogt stays at 90% (Kanta's breakthrough to D happens mid-fight). A player who uses antidotes, guards and support skills does better than auto-battle. Full table: `handoff/balance.txt`.

## Build pipeline (Claude's workspace)
Python builders `tools/story/{db,common,ids,cast,prologue,ch1,ch2,ch3,act2,ch4,ch5,ch6,ch7,ch8,ch9,foes,foes3,terrain,lighting,overlays,audio}.py` → `tools/build_story.py` → `story/out`. Generated maps: `tools/mapgen.py` + `tools/story/terrain.py`; sample-map bases recovered in `story/base/`.
Checks: `tools/check_story.py` (references, reachability playthrough, script syntax), `tools/check_routes.py` (scripted movement routes that would block and hang a scene).
Engine tests (Playwright, `tools/run_game.js`): `scen_story1`, `_ch1`, `_ch2`, `_ch3`, `_ch3b`, `_save`, `_eisfurt`, `_menu`, `_kits`, `_party`, `_ch4` (chapter 4 playthrough), `_act3` (every map of chapters 5–9 plus the finale to the title), `_sweep` (every NPC/door/chest event of chapters 5–9), `_rematch` (in-battle breakthroughs happen once), `_msgfit` (message fit screenshots), `_bal2` (balance runs).
Last run 5 Oct 2026, all passing: `_act3` and `_rematch` on the final installed data; `_sweep` (419 events, 0 hangs or errors), `_ch4`, `_ch1`, `_ch2`, `_ch3`, `_ch3b`, `_save`, `_eisfurt`, `_menu`, `_kits`, `_party`, `scen_story1`, `_msgfit` on the installed build before the balance pass (it only changed enemy numbers); `check_story.py --rtp` 0 problems (83/83 maps, 165 switches, 117 battles reachable from New Game), `check_routes.py` 0 blocked routes.
