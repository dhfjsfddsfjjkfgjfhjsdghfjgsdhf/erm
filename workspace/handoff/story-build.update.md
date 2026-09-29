# story-build.md — new sections (increment 3, Chapters 5–9)

Merge these into `claude/story-build.md` in the MZ project, after the Chapter 4 section.

## Increment 3: the rest of the story (built 29 Sept 2026 in a cloud session)

Maps 75–80, 90–93, 100–108, 110–118, 120–130. Quests 21–35. 83 maps in all. Switch names start with the
chapter (`C5:` … `C9:`); Act I–II switch and variable ids are pinned (`story/base/registry.json`).

### Chapter 5 · Weißenfels (party rank D, LV ~21–27)
- 75 Grauklamm: Rin's march; canyon, wyvern dives, chained thralls, a camp fire.
- 76 Heerlager: Rin's red command tent, the council (Rin, Sōma, Hikari), Saki's quest "Mariko und Aya",
  quartermaster, the fire talk; sleep in the party tent → the assault at 4:00.
- 77 Weißenfels Unterstadt: the breach, the chain gang (quest "Die Kettenkolonne", optional), Sōma; the NW
  tower door → 78 Alter Aquädukt (two sluices open the water gate) → 79 Hüllenschmiede (racks of empty armors,
  Falin's memory "Wake up, Falin. Please.", Mariko and Aya, the Aschenschmied boss at the furnace, the winch
  that opens the citadel gate).
- Rin joins as a guest at the citadel gate → 80 Drachenhalle: Shiranui chained as the forge fire, the Iron Prince
  (Hayato, Rin's brother), Falin breaks the null-iron, Shiranui's scale (Drachenschuppe), the Königliches Wappen,
  Rin leaves the party; card "Weißenfels ist frei" → the Wallfeste under siege.

### Chapter 6 · Der Messingtyrann (rank D → C)
- 92 Wallfeste (siege; tiles of map 64): Kōsaka, Rin, the cook's rest, the clerk's shop; the north gate → 90 Torturm
  (three floors side by side, visible foes, the Oni-Hauptmann at the winch).
- 93 Frontposten 3 (siege; tiles of 61): the hound yard, Mori's sally port → 91 Heerlager der Asche: ash camp,
  patrols, the Seelenkessel (boss), Gōen's offer and the unwinnable fight: turn 2 the chain on Hanma →
  **breakthrough to C**; Yukino's ice wall.
- Back at Frontposten 3: the fire talk (Kagerō is Kurenai Tōma; the Morgenwacht; Hanma on the regalia; Rin's
  letter), **Yukino joins** (actor 6), "Ende des zweiten Akts" → Act III.

### Chapter 7 · Die Kaiserstadt (rank C → B)
- 100 Kaiserstraße (card "Akt III · Morgenröte", ambush, the Spinnensiegel) → 101 Lichtenhall (palace, Morgendom,
  guild, inn, arena, Akira's statue, plaza shops).
- 104 Morgendom: Amane Kiyoko and the tournament; 107 Gilde: Kirishima registers the team (Turniermarke).
- 103 Kaiserarena: four rounds (Eiserne Brüder, Arenabestie, Klingen von Ostmark, Kanemoto Gōki) with a healer
  between; the ceremony: Tsumugi seizes the Empress's box and flees below.
- 105 Unterhallen (cocoons) → 106 Spinnenhalle: Tsumugi (rank B under the dawn seal), turn 2 **breakthrough to
  B**, the **Morgenklinge (regalia 1/4)**; Kiyoko; 102 Kaiserpalast: the Empress's audience (20,000 kl, legions
  north); the Guild record of 313 (Gildenabschrift) → **travel menu** opens.

### Chapter 8 · Wald und Tiefe (rank B)
- 110 Waldweg (the packlord, optional quest from Ōkami Sōta) → 111 Hirschheim (Countess Kagura, Sōta, Kusaki's gift).
- 112 Fuchsschrein: Nanami, the stone fox riddle, Shirogane's game at the silver pool → **Sternlaterne (2/4)**.
- 115 Eisenberg (Iwakura, Tsurugi, the Grubenlampe) → 116 Tiefgrube (the miners) → 117 Untere Tiefgrube →
  118 Trollhalle: the Troll King → **Heldenhorn (3/4)**.
- Hanma tells her story at the inn in Hirschheim (after the second regalia).
- 113 Urwald: the leshy wants Kusaki's bread and salt → 114 Hirschthron: Mukuro (boss); the Waldkrone; the
  messenger from Salzhafen.

### Chapter 9 · Morgenröte (rank B → A)
- 120 Salzhafen (Hisa, Sayo's shrine, the chandler, three piers) and 130 Der Ertrunkene Mann (inn, Kaizaki Rui:
  Seekarte, Ruis Pfand).
- 121 Die Seeschwalbe: voyage 1 (drowned men board) → 122 Knochenriff (reef, camp fire, chests) → 123 Versunkene
  Halle (Fomori, the chief on the throne of anchors → **Aschenkrone (4/4)**).
- Voyage 2: the Sturmsee, Shigure on the Kraken; Rui's gift (Drachenknöchel); back in port Sayo's five seals, the
  League's reward, the messenger: the Urwald burns.
- 124 Brennender Urwald (from Hirschheim's south road): Kagura's rangers, the burned leshy (heals), Gōen in the
  clearing, at half HP the chain again → **breakthrough to A**; the contract burns.
- 125 Hirschthron (Nacht): the Sternlaterne rest; Kagerō → Hōkai's shadow → Kurenai Tōma (ends when Yukino says
  his name); dawn; "Wochen später".
- Epilogue 126 Wallfeste (Yukino leaves), 127 Weißenfels (Rin buries the sword), 128 Rabenau (Hayate, Tōdō),
  129 Kiefernkamm (Hanma: "Always."), card "Erdenkreis · Ende", credits, title screen.

### Tests of increment 3
- Static (cloud): `tools/check_story.py` passes (0 problems, 83/83 maps, 163 switches and 117 story battles
  reachable, 67 script commands parse). Act I maps byte-identical to the Chapter 4 build.
- Balance: `tools/battle_sim.py` + `tools/tune_foes.py` (see `handoff/balance.txt`).
- Engine (to do locally): `tools/scen_story_act3.js`, `scen_story_ch4.js`, the Act I scenarios.
