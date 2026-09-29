# Erdenkreis: inventions to review, and credits

## What I invented or changed (Chapters 5–9, this session)

The canon (the Erdenkreis browser game) gave the cast, the four Dawn Regalia, the Four Calamities and the big
beats (Gōen's rank wall and Hanma's refused contract, Tsumugi and the Morgenklinge, Shigure on the Sturmsee,
Kagerō / Kurenai Tōma and Yukino saying his name, the ending lines). The RPG Maker version compresses the canon's
ten acts into three chapters of Act III, so a lot had to be placed, joined or invented. Please review these.

**The player-character rule.** Every player character looks masculine and is a woman (she/her): Rin (guest, actor
5) uses sprite and face Actor2 #2 (it was #1 in your Act II maps; changed there too), Yukino (actor 6) Actor3 #2.

**People and roles**
- Asahina Rin: a rank C Battle-Mage guest in chapter 5 only (Flammenlanze, Eissturm, Königsschild). Rank fixed at C.
- Tsukishiro Yukino: gated at the party's rank like Kanta and Falin, a Frost Saint kit (Frostschnitt, Eiswand,
  Frostkörper; Schneesturm, Kalte Gnade at B; Weiße Stille, Morgenwacht at A), weapon line Frostklinge →
  Mondeisklinge → Weißklinge.
- Asahina Hayato, Rin's brother, is the Iron Prince (Der Eiserne Prinz) of Weißenfels.
- Nishiki Eiji sold the Wall to buy back his wife Mariko and daughter Aya, slaves in the hull forge (quest
  "Mariko und Aya"); Mariko is the one who woke Falin ("Wake up, Falin. Please." in the forge memory).
- Shiranui, a dragon chained as the fire of the hull forge; Falin breaks the null-iron chain; her scale is the
  Drachenschuppe.
- Hanma's backstory (told at the inn in Hirschheim after the second regalia): Sōryū Akira's youngest general,
  the purges with the Death arts, Akira taking her command at Frostheim, Gōen's contract for her anger, and Akira
  refusing it for her. "The General who was refused."
- Shigure was the Morgenwacht's lance, Yukino's comrade; his last words ("the sea is warm") come back at the end.
- Kaiserin Kujō Sayaka (name from canon) receives the party and sends the legions north.
- Kirishima Daigo, Guild archivist and branch master in Lichtenhall, holds the Guild record of 313 that says where
  the regalia went.
- New named NPCs: Ōkami Sōta (wolf clan), Gräfin Kagura Yui, Kitsunezaki Nanami, Shirogane (the fox who hid the
  Sternlaterne), Förster Kusaki, Iwakura Gōtetsu, Vorarbeiter Tsurugi, Minato Hisa (Küstenbund), Kaizaki Rui
  (canon name, Schwarze Flagge), Namiji Sayo (canon name, tide priestess), Bootsmann Kaji, Wirt Unagi,
  Schiffsausrüsterin Ise, Wirtin Hoshi, Arenameister Ishikawa, Kanemoto Gōki (canon name, arena champion).

**Places and plot**
- Where the regalia were: the Morgenklinge as the Sonnwende tournament prize (canon) stolen by Tsumugi; the
  Sternlaterne with Shirogane at the fox shrine; the Heldenhorn in the Troll King's hoard under Eisenberg; the
  Aschenkrone on the Fomorian chief of the Knochenriff (canon).
- The Hirschthron in the Urwald is one of the five seals, and the final battle is there (the canon's Nachtfeste in
  the Aschenfeld is not built).
- Gōen is fought twice: in the Heerlager der Asche (the unwinnable rank wall, the chain on Hanma, the breakthrough
  to C) and in the burning Urwald (the chain again, the breakthrough to A); his old unsigned contract for Hanma
  burns at the end.
- Kagerō in three battles: Maō Kagerō, then Hōkai's shadow pouring out of him, then Kurenai Tōma, which ends when
  Yukino says "Tōma." (the canon used a veil and a special battle command). The party is healed between phases.
- Breakthroughs: to C at Gōen (ch. 6), to B against Tsumugi under the dawn seal (ch. 7), to A against Gōen (ch. 9).
- The epilogue on copies of four earlier maps: Wallfeste (Kōsaka, Yukino leaves for Frostheim), Weißenfels (Rin
  buries Hayato's sword), Rabenau (Hayate, the boy from chapter 1, and Tōdō), Kiefernkamm (where it began).
- A travel menu between the Act III hubs (common event "Reisen"), the ship Seeschwalbe for the sea.

**Rules and systems**
- Story_Core: message text that is too wide is drawn smaller instead of being cut off.
- Rank changes and the difficulty retune (see HANDOFF.md section 4 and handoff/balance.txt).
- Tsumugi's and Gōen's scripted breakthroughs can't repeat after a defeat.

**Art and maps**
- 33 of the 39 new maps are generated (no MZ sample maps were available): towns, forests, canyons, the reef,
  the ship, dungeons, interiors. The other 6 reuse earlier maps' tiles: the Wallfeste and Frontposten 3 under
  siege, and the four epilogue maps.
- 44 new enemy battlers are recoloured/resized variants of RPG Maker MZ RTP battlers (tools/story/foes3.py IMAGES);
  Shiranui's picture is a recoloured RTP dragon. New NPCs use RTP faces and sprites.

## Credits

| What | Author | Where it's used |
|---|---|---|
| RPG Maker MZ runtime package (tilesets, characters, faces, battlers, battlebacks, audio) | Gotcha Gotcha Games / KADOKAWA | everywhere |
| TausiLighting | MelekTaus (github.com/themelektaus/rpgmz-lighting-plugin) | lights, `data/Lighting.json` |
| WD_Quest | Winthorp Darkrites | the quest log (a minimal WD_Core stand-in was written for this project) |
| McKathlin_DayNight | McKathlin (MIT licence) | time of day, lighting presets |
| Eiswurm, Fubuki, Aschenschwinge and other Act I–II battlers | Nemo (@theartofnemo, RPGMakerWarehouse); DLC monster art by Yutaro Tsuyuki (the `pack`, `dragonspack1_sd`, `kamedran`, `rt5monster` and `dlc` uploads of increment 2) | Act I–II foes |
| Portraits of Kanta, Hanma, Falin | the user | faces and pictures |
| Rank_Core, Rank_Battle, Rank_Menus, Rank_Maps, Story_Core, WD_Core stand-in | Ten & Claude | the rules |

Tools that aren't shipped with the game: Playwright (headless tests), Pillow and fontTools (image work, text
measurement).
