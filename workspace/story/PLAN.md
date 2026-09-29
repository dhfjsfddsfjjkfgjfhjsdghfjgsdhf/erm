# Erdenkreis (MZ) — story build plan  (working file; source of truth for the build)

User asks (2026-09-28): use TausiLighting + WD_Quest, flesh out systems, implement the story from Kanta + Hanma,
Falin joins roughly 1/3 in. ALL PLAYER CHARACTERS: masculine appearance, female characters (she/her).

## Structure (planned whole game: 3 acts x 3 chapters; Falin joins at the start of Act II = 1/3)
- Act I "Erwachen" (Hohenwacht, rank F -> E): Prologue, Ch1 Rabenau, Ch2 Eisfurt, Ch3 Wachtburg.
- Act II "Die Wacht" (Nordwall / Weissenfels, E -> C): opens with Falin joining at Frontposten 3.
- Act III "Morgenroete" (beyond Hohenwacht, C -> A+).
Build now: Prologue .. Ch3 + Act II opening (Falin joins). Deliver in increments.

## Levels (MZ rank curve: E ~LV13, D ~LV27)
Prologue LV1-3 | Ch1 LV3-6 | Ch2 LV6-10 | Ch3 LV10-14 (breakthrough F->E) | Act II start ~LV14-15 (Falin joins at Kanta's LV)

## Systems (Story_Core.js)
- Hanma <Bound To: 1>: level/EXP mirror Kanta, rank = Kanta's rank, gains no EXP herself.
- Breakthrough gate (party var): story actors' base stats capped at (gate+1)*100-1; natural growth above is held back
  and released at breakthrough; breakthrough raises top-3 stats to the new band floor, +1 LV, full HP/MP.
- Divine Weaponry: Kanta's weapon slot sealed; weapon = DW form for her rank (F beam d4 DEX, E dagger d6 DEX,
  D sword d8 STR ...); <DW Unlock E: id> learns techniques on DW rank-up.
- Vessel revival instead of game over: respawn at last rest point (inn, camp, waking cave), revive + recover,
  lose 10% money, common event shows Hanma's line (first time: explanation).
- Follow-player light: events with <Follow Player> glued to the player; TausiLighting lights reference them.
- Money = Kupferling (kl); shown as gk/sl/kl (1 gk = 10 sl = 100 kl).
- Passive skills <Passive State: n>; party aura <Party Aura: n>; barrier (temp HP) states.
- Date/time window in menu (McKathlin DayNight + base date 01.Bluetenmond.1047).
- WD_Core stand-in (minimal API for WD_Quest).

## Cast (Japanese names family-first; places German)
Kanta (actor 1, DW: DEX/STR/MAG S), Hanma (actor 2, WIS/MAG/CHA S, bound), Falin (actor 3, CON/STR S, joins Act II).
Rabenau: elder Okuda Noboru, innkeeper Hanamura Izumi ("Zum Schwarzen Raben"), watch captain Todo Keiji (lame leg,
ex-Nordwall), shepherd girl Natsu, smith Matsuda Daichi, herbalist Saeki Chiaki. Merchant Sagara Takumi (escort to Eisfurt).
Eisfurt: ferryman Ueda Ryo, Vogt Shirakawa Kaname, tavern "Zur Furt" Nagase Emi, shrine maiden Wakaba Aika.
Frost spirit Fubuki (yuki-onna, E boss, yields). Wachtburg: branch master Kurogane Isao (B), receptionist Hoshino Miyu.
Nordwall: wall captain Mori Daisuke (C), Falin "die Eiserne".

## Beats
P  Erwachenshoehle: wake in the dark (beam lights 10 ft), Hanma "my Lord", empty chamber (no bones/bedding/fire),
   drip pool (heal), the two-tail on the stone shelf: Bow (trust+1, tail flick to exit) / back away / touch the hoard
   (fight, unwinnable E -> vessel revival tutorial). Exit to Kiefernkamm: dawn drizzle, smoke 3 miles east,
   Hanma: road (fast, open) or trees (slow, unseen) -> both reach Rabenau.
1  Rabenau: gate (Todo), inn meal-for-work, night raiders (goblins driven south), Rabenholz -> old watchtower,
   boss Goblin chieftain "Krummzahn" + wolf; miasma-blackened raven feather (demons stirring). Reward, sheep side quest.
   Merchant Sagara needs guards to Eisfurt.
2  Oststrasse escort (deserters/kamaitachi), Eisfurt frozen ford in spring, Frostpfad, Eisfallhoehle,
   mid-boss Eiswurm (glacialserpent art), boss Fubuki (Shiva art) -> yields, cold lifts; pay 1 gk.
3  Koenigsstrasse, Wachtburg: guild registration (1 gk, oath on Sabaki's scales, Wahrheitskristall: F, "empty imprint"),
   Neuling title (nickname), board quests (rats in the granary, wolves on the Nordstrasse, herbs), refugee column attacked
   by Aschenhund (miasma-touched) -> Kanta shields refugees -> BREAKTHROUGH mid-fight (beam -> dagger, Returning Fang).
   Optional: Wolfsgrube trial (E: Dire Wolves) -> Wolfsbann title + Wachtfeuer-Amulett. Emergency call north.
II Nordstrasse -> Frontposten 3 (Mori Daisuke). Night assault on the breach; Falin holds it; guest fight; Falin joins.
   Falin backstory (my invention, flag to user): woke inside the armor the night Weissenfels fell (1041), remembers only
   the name engraved in the breastplate; the plate grew into her flesh; guards the breach; senses Kanta is also a vessel.

## Maps (sample map ids)
P1 cave 208/211 | P2 ridge 202 | road 256 | trees 257 | Rabenau 106 | inn 113 | elder 109 | store 110/121 | farm 116 |
Rabenholz 225/226 | watchtower ruin 203/206 | Oststrasse 258 | Eisfurt 127 | Eisfurt interiors 162-165 |
Frostpfad 260/261 | Eisfall cave 219 + 222 | Koenigsstrasse 264/265 | Wachtburg 143 | guild hall 157 | inn 169 |
shops 130/138 | granary cellar 044 | Wolfsgrube 031 | Nordstrasse 262 | Frontposten 3 247 + wall 195.

## BUILD STATE (2026-09-29)
- Tools: tools/build_story.py (+ tools/story/{common,db,ids,prologue,ch1,lighting,audio}.py) -> story/out;
  tools/make_story_web.sh -> sweb (headless root); run with PORT=8124 WEBROOT=/home/claude/mz/sweb node tools/run_game.js <scen>.
  Scenarios: scen_story1 (opening), scen_story_ch1 (full prologue+ch1 playthrough, passes), scen_story_balance (BAL env),
  scen_story_menu (menu/quest/battle shots), scen_story_save (save/load ok). Map render: tools/render_maps.sh ids px --pass;
  render_grid.py --reach=x,y.
- Plugins: plugins/Story_Core.js (bound actors, gate, rank gear, breakthrough cmd, vessel revival, passives/auras, barrier,
  interpose, follow-player events, money gk/sl/kl, calendar menu window, chapter card), plugins/WD_Core.js (stand-in).
  Third-party copies in thirdparty/ (TausiLighting.js, WD_Quest.js); tausi classes in /home/claude/tausi/tausi-lighting.
- Increment 1 DONE (maps 1-14): Prologue (cave 1, ridge 2, road 3, trees 4) + Ch1 (Rabenau 5, inn 6, elder 7, herbs 8,
  smithy 9, farm 10, Rabenholz 11, deep wood 12, ruin 13, tower top 14). Quests 1-5 (WD_Quest). Balance: Krummzahn L5 83%, L6 100%.
- Piglets instead of sheep (no sheep sprite in MZ RTP). Money loss on revival = gameplay concession (canon: new vessel has
  nothing) -> tell user.
- NEXT: Ch2 (Oststrasse escort, Eisfurt, Frostpfad, Eisfallhoehle, Eiswurm, Fubuki), Ch3 (Wachtburg, guild, breakthrough),
  Act II opening (Falin). Map ids: Ch2 20-39, Ch3 40-59, Act II 60+.


## BUILD STATE (2026-09-29, increment 2) — installed on the PC
- Increment 2 DONE: Ch2 (maps 20-29), Ch3 (40-48), Act II opening (60-62). 36 maps total. Quests 1-16.
- Ch3: Königsstraße 40 (283), Wachtburg 41 (143), Gildenhaus 42 (169), Zum Wachtfeuer 43 (157), Königliche Schmiede 44 (138),
  Ausrüster Aoyagi 45 (130), Kornspeicher-Gewölbe 46 (044, Schimmelmutter boss), Nordstraße 47 (293, Rudel + emergency),
  Wolfsgrube 48 (031, optional E trial). Registration: 1 gk, oath on Sabaki's scales, crystal F + "empty imprint", Hanma
  invisible to the crystal, party name via name input on actor 4 ("Rabenfeder" default, \N[4]), nickname Neuling.
  Jobs: granary / wolves / Heilwurz (6 herb spots, var Heilwurz). Two paid jobs -> emergency autorun in the guild ->
  Nordstraße: Aschenhunde troop, turn 2 page = BREAKTHROUGH (Kanta shields the children; Leitrüde gets "Burned Clean" -50,
  small hounds die to the flare). Afterwards crystal reads E, 3 gk, quests "Die Wacht" + "Die Wolfsgrube".
  Kaji refits Silberrüstung -> Echtsilberrüstung (1 gk 5 sl). Ueda's ferry now crosses to the Königsstraße.
- Act II: Wallstraße 60 (217, card "Akt II · Die Wacht"), Frontposten 3 61 (019, Mori, Sgt. Kōno bunks -> night bell),
  Die Bresche 62 (286): Falin joins (party add, SyncLevel, AutoBuild -> Catch Up), Vorhut fight, Aschenschwinge boss
  (kamedran art), dawn talk (Falin backstory), quest "Die Wallfeste" = cliffhanger / end of build.
- Story_Core additions: <Weather: snow 5 unless 26> map notes (weather per map on entry), Ground_ Tausi layers drawn under
  characters, Catch Up (late gated joiners get top-3 raised to the current band).
- Balance (auto-battle sims): Ch3 F fights L12 ~80-95% HP left; Schimmelmutter L12 100% (45% HP); Rudel L12 100% (26%);
  emergency L12 100% (44%); Wolfsgrube L15 two-person 100% (34%); Vorhut L15 trio 100% (71%); Aschenschwinge L15 100% (40%).
- Tests: scen_story_ch3.js (full Ch3 + Act II playthrough), scen_story_ch3b.js (menu, save/load, revival), scen_story_eisfurt.js.
- NEXT (Act II proper): Wallfeste (Marshal Kōsaka), Falin's skills past E (Brace at E already), Weißenfels. Map ids 63+.
