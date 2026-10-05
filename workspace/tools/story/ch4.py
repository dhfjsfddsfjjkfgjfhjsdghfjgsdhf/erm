"""Chapter 4: Die Wallfeste. The Wallweg, the Nordwall's command fort, the brass coins, the old cistern,
Frontposten 5 (optional) and the night raid: Kanta's breakthrough to rank D."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story import foes
from story.ids import *
from story.ch1 import chest
from story.ch2 import camp_fire
from story.cast import *
from story.act2 import Q_WALLFESTE, S_FALIN

COURIER = npc_speaker("Kurier Ichijō", "People1", 2)
GATEGUARD = npc_speaker("Torwache", "People3", 6)
SENTRY = npc_speaker("Wache Kazama", "People3", 7)
COOK = npc_speaker("Feldkoch Hanamura", "People2", 7)
SERGEANT5 = npc_speaker("Feldwebel Tōdō Ren", "People4", 6)
KI = foes.KEY
FI = foes.ITEMS

# ----------------------------------------------------------------------- quests
Q_COINS = Quest(17, "Messingmünzen", "Kōsaka Tetsuji", "Wallfeste",
                "Supplies vanish from the Wallfeste, and three sentries died in a week with brass coins on their "
                "eyes. Marshal Kōsaka trusts none of his own officers. Find out who is selling the Wall.",
                "Ask around: the Lazarett, the Zeughaus, the sentries.")
Q_FP5 = Quest(18, "Frontposten 5", "Kōsaka Tetsuji", "Nordwall, Frontposten 5",
              "Frontposten 5, east along the Wall, hasn't signalled in two days. Gargoyles were seen over it: rank D, "
              "a rank above you. Optional, and hard: recommended level 19. Take the north gate of the Wallfeste and "
              "bring the squad home.",
              "North gate, then Frontposten 5's tower.")
Q_CISTERN = Quest(19, "Die Zisterne", "Wache Kazama", "Wallfeste, alte Zisterne",
                  "Lights under the ice, where the old cistern lies under the fort. The quartermaster keeps its key.",
                  "The shaft by the canal, east of the barracks.")
Q_WF = Quest(20, "Weißenfels", "Asahina Rin", "Wallfeste, Weißenfels",
             "The Crown Princess marches on Weißenfels with two thousand of the Crown's soldiers. She wants blades "
             "that aren't the Wall's. Falin woke there.",
             "Tell Rin in the courtyard when you're ready to march.")

# ----------------------------------------------------------------------- switches / variables
S_C4 = SW('C4: On the Wallweg')
S_COURIER = SW('C4: Courier Saved')
S_WF = SW('C4: At the Wallfeste')
S_AUDIENCE = SW('C4: Audience Done')
S_CLUE_COIN = SW('C4: Clue Coin')
S_CLUE_LEDGER = SW('C4: Clue Ledger')
S_CLUE_LIGHTS = SW('C4: Clue Lights')
S_NISHIKI_GONE = SW('C4: Nishiki Gone')
S_FP5 = SW('C4: FP5 Offered')
S_FP5_DONE = SW('C4: FP5 Relieved')
S_FP5_PAID = SW('C4: FP5 Paid')
S_SCRIBE = SW('C4: Scribe Down')
S_RAID = SW('C4: Night Raid')
S_RAID_DONE = SW('C4: Raid Over')
S_C4_END = SW('C4: Chapter Done')
S_MARCH = SW('C5: March')          # set when the party marches with Rin (chapter 5)
V_CLUES = VAR('C4: Clues')

WALL_ENC = lambda: [(TR["Aschenhunde x2"], 6, ()), (TR["Aschenleichen x2"], 5, ()), (TR["Aschenleiche & Hund"], 5, ()),
                    (TR["Raid: Aschenhunde"], 2, ())]


def build():
    return [wallweg(), wallfeste(), marschallhalle(), kaserne(), lazarett(), zeughaus(), fp5_turm(), zisterne()]


def clue_count(e):
    e.var_script(V_CLUES, "[%d, %d, %d].filter(id => $gameSwitches.value(id)).length" % (S_CLUE_COIN, S_CLUE_LEDGER, S_CLUE_LIGHTS))


# ---------------------------------------------------------------------------
# 63  Wallweg  (sample 218): along the Wall to the Wallfeste
# ---------------------------------------------------------------------------
def wallweg():
    mb = MapBuild(WALLWEG, NAMES[WALLWEG], 218, display=NAMES[WALLWEG])
    mb.props(note="<Rank: E>\n<Area Name: Wallweg>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field4', 60), bgs=('Wind2', 45), battleback=('Snowfield', 'Snowfield'),
             encounters=WALL_ENC(), steps=28, weather='snow 4')
    el = Ev()
    el.card("Kapitel 4", "Die Wallfeste", 220)
    el.wait(10)
    el.narrate(["The Wallweg runs east under the Nordwall: a soldiers'",
                "road cut into the snow, the Wall a grey cliff on the",
                "left the whole way."])
    el.say(FALIN, ["The Wallfeste is a day east. Keep the Wall on your",
                   "left and don't leave the road."], 'calm')
    el.say(KANTA, ["You know the way?"], 'calm')
    el.say(FALIN, ["I've never walked it. Six years, and I never left the",
                   "breach. I know it from the soldiers' talk."], 'calm')
    el.say(HANMA, ["The Marshal will want to look at you, Falin. A living",
                   "armor that holds a breach for six years is either a",
                   "weapon or a threat. Men like him keep lists of both."], 'stern')
    el.say(FALIN, ["Then he'll have to choose a list."], 'fierce')
    el.quest_desc(Q_WALLFESTE, "Marshal Kōsaka Tetsuji commands the Nordwall from the Wallfeste, a day east along "
                               "the Wallweg. Mori sent word ahead.")
    el.switch(S_C4)
    mb.autorun("Wallweg", el)
    for x in (11, 12, 13):
        el = Ev().se('Move1', 60).transfer(FRONTPOSTEN, 16, 32, 8, 0)
        mb.add("South", x, 34, [pg(el, trigger=1, priority=0)])
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 21, 33, 8, 0)
    mb.add("Gate Tunnel", 12, 9, [pg(el, trigger=1, priority=0)])
    # the courier and the first hellhound
    cour = mb.add("Courier", 16, 17, [pg(None, priority=0),
                                      pg(None, sw=S_C4, char='Damage2', index=1, direction=2, priority=1),
                                      pg(Ev().say(COURIER, ["Thanks again. I'll make Frontposten 3 by nightfall,",
                                                             "if the hounds let me."]), sw=S_COURIER,
                                         char='People1', index=2, direction=4, priority=1)])
    hound = mb.add("Hellhound", 15, 19, [pg(None, priority=0),
                                          pg(None, sw=S_C4, char='Nature', index=0, direction=8, priority=1, step_anime=True),
                                          pg(None, sw=S_COURIER, priority=0)])
    def ambush(e):
        e.se('Dog', 90, 70)
        e.balloon(hound, 1)
        e.text(["A shape on the snow ahead: a man face-down beside the",
                "road, and something standing over him that smokes in",
                "the cold. Its hide glows like a banked fire."])
        e.say(FALIN, ["Hellhound. Rank D, and it's alone. Don't let it",
                      "breathe on you."], 'fierce')
        e.say(HANMA, ["One rank above us, my Lord. It will hit harder than",
                      "anything you've fought, and shrug off half of what",
                      "you give it. Fight it anyway: it's eating him."], 'command')
        e.battle(TR["Höllenhund"])
        e.switch(S_COURIER)
        e.wait(20)
        e.say(COURIER, ["…Gods. I thought that was it. Ichijō, Wall courier."])
        e.say(COURIER, ["The Marshal's orders for Frontposten 3. They'll be",
                        "short, I'm afraid. Everything's short. Crates go into",
                        "the Wallfeste's stores and don't come out."])
        e.say(COURIER, ["And the sentries… they found another one dead at the",
                        "south gate. Coins on his eyes. Brass coins. Nobody's",
                        "saying it, but everybody's thinking it."])
        e.say(HANMA, ["Brass coins."], 'stern')
        e.say(COURIER, ["Here. It's not much. Thank you."])
        e.item(IT["Großer Heiltrank"], 2)
        e.item(FI["Elixier"], 1)
        e.notice(["Received 2 Großer Heiltrank and an Elixier."])
    for x in (10, 11, 12, 13):
        mb.add("Bridge North", x, 21, [pg(None, priority=0),
                                       pg(Ev().if_switch(S_COURIER, False, ambush), sw=S_C4, trigger=1, priority=0)])
    camp_fire(mb, 17, 26, WALLWEG, 17, 27, 8, ["A cairn of Wall stones around a fire pit. Soldiers", "rest here on the march."])
    chest(mb, "Chest", 20, 23, lambda e: (e.item(FI["Elixier"], 1), e.gold(300)), "Found an Elixier and \\MONEY[300].")
    chest(mb, "Chest", 3, 15, lambda e: e.armor(AR["Wachmantel"], 1), "Found a Wachmantel.")
    return mb


# ---------------------------------------------------------------------------
# 64  Wallfeste  (sample 22): the Nordwall's command fort
# ---------------------------------------------------------------------------
def wallfeste():
    mb = MapBuild(WALLFESTE, NAMES[WALLFESTE], 22, display=NAMES[WALLFESTE])
    mb.props(note="<Area Name: Wallfeste>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Castle3', 60), bgs=('Wind1', 30), battleback=('Snowfield', 'Fort1'), weather='snow 2')
    # no cannons in Mittland (WORLD§1): the sample's wall guns become bare wall tops
    for i, v in enumerate(mb.m['data']):
        if v in (372, 373, 380, 381, 128, 136):
            mb.m['data'][i] = 0
    # --- exits
    for x in (20, 21, 22):
        el = Ev().se('Move1', 60).transfer(WALLWEG, 12, 10, 2, 0)
        mb.add("South Gate", x, 35, [pg(el, trigger=1, priority=0)])
    # the keep: its gate on the courtyard side, a back door on the inner side
    el = Ev()
    el.if_switch(S_RAID, True, lambda b: b.text(["Soldiers have barred the keep's gate."]),
                 lambda b: (b.se('Open2'), b.se('Move1', 60), b.transfer(MARSCHALLHALLE, 6, 5, 2, 0)))
    mb.add("Keep Gate", 22, 23, [pg(el, char='', trigger=0, priority=1)])
    el = Ev()
    el.if_switch(S_RAID, True, lambda b: b.text(["Soldiers have barred the keep's back door."]),
                 lambda b: (b.se('Open2'), b.se('Move1', 60), b.transfer(MARSCHALLHALLE, 18, 5, 2, 0)))
    mb.add("Keep Back Door", 22, 19, [pg(el, char='!Door2', index=0, direction=2, pattern=1, trigger=0, priority=1,
                                        walk_anime=False)])
    mb.door(6, 12, LAZARETT, 3, 9, 6, name='Lazarett')
    mb.door(19, 14, KASERNE, 8, 12, 8, name='Kaserne')
    mb.door(42, 12, ZEUGHAUS, 11, 12, 8, name='Zeughaus')
    # the north gate: the Wall road east to Frontposten 5 (side mission)
    def north(e):
        e.if_switch(S_FP5_DONE, True,
                    lambda b: b.text(["The north gate. Beyond it the Wall road runs east to",
                                      "Frontposten 5, where the squad holds again."]),
                    lambda b: b.if_switch(S_FP5, True,
                                          lambda c: c.choices(["March to Frontposten 5", "Not yet"],
                                                              [lambda d: (d.fadeout(), d.narrate(
                                                                  ["Three miles east along the Wall, through the snow."]),
                                                                          d.transfer(FP5_TURM, 12, 45, 8, 0), d.fadein()),
                                                               None], cancel=1),
                                          lambda c: c.say(WALL_SOLDIER, ["North gate's for patrols. Marshal's orders."])))
    for x in (32, 33, 34, 35):
        mb.add("North Gate", x, 5, [pg(Ev().if_switch(S_RAID, False, north), trigger=0, priority=1)])
    # the cistern shaft by the canal
    def shaft(e):
        def down(b):
            b.say(HANMA, ["Miasma. Faint, but it's there, down in the dark.",
                          "Someone has been carrying it in on their boots."], 'stern')
            b.choices(["Climb down", "Not yet"], [lambda c: (c.se('Open3'), c.se('Move1', 60),
                                                             c.transfer(ZISTERNE, 11, 24, 8, 0)), None], cancel=1)
        e.if_switch(S_SCRIBE, True, lambda b: b.text(["The shaft to the old cistern. Nothing moves down there now."]),
                    lambda b: b.if_item(KI["Zisternenschlüssel"],
                                        lambda c: c.if_switch(S_CLUE_LIGHTS, True, down,
                                                              lambda d: (d.text(["An iron grate over an old shaft, locked. Warm air",
                                                                                 "rises through it, and the snow around it has melted."]),
                                                                         d.choices(["Open it with the Zeughaus key", "Leave it"],
                                                                                   [down, None], cancel=1))),
                                        lambda c: c.text(["An iron grate over an old shaft, locked. Warm air rises",
                                                          "through it, and the snow around it has melted."])))
    mb.add("Cistern Shaft", 28, 14, [pg(Ev().if_switch(S_RAID, False, shaft), char='!Other1', index=4, direction=2,
                                        trigger=0, priority=0)])
    # --- arrival
    el = Ev()
    el.wait(10)
    el.narrate(["The Wallfeste: the Nordwall's command fort, a town of",
                "stone and soldiers grown around the Wall's thickest",
                "stretch. Thirty thousand men answer to it."])
    el.say(GATEGUARD, ["Halt. …Frontposten 3? The Guild vessel, the ghost and",
                       "die Eiserne?"])
    el.say(GATEGUARD, ["Captain Mori's bird came in yesterday. The Marshal's",
                       "expecting you. The keep, straight ahead, and mind the",
                       "Crown's people. The princess got in this morning."])
    el.say(FALIN, ["The princess."], 'calm')
    el.say(GATEGUARD, ["Asahina Rin. She wants Weißenfels back. The Marshal",
                       "wants to keep the Wall standing. Guess how that's",
                       "going."])
    el.quest_desc(Q_WALLFESTE, "The Marshal waits in the keep of the Wallfeste, at the top of the courtyard.")
    el.switch(S_WF)
    el.rest_point(WALLFESTE, 21, 32, 8)
    mb.autorun("Arrival", el)
    # --- people
    gg = [pg(Ev().say(GATEGUARD, ["The keep's straight ahead. Kasernen west of the canal,",
                                  "Lazarett by the tents, Zeughaus east."]), char=GATEGUARD.char[0],
             index=GATEGUARD.char[1], direction=2, priority=1),
          pg(Ev().say(GATEGUARD, ["Gods, what a night. Go on, the Marshal's asking for you."]),
             sw=S_RAID_DONE, char=GATEGUARD.char[0], index=GATEGUARD.char[1], direction=2, priority=1)]
    mb.add("Gate Guard", 23, 31, gg)
    # Rin and her guard in the courtyard after the audience (chapter 5 starts with her)
    def march(e):
        e.say(RIN, ["Two thousand of the Crown's soldiers, and three who",
                    "aren't anybody's. It'll do. It has to."])
        e.choices(["March to Weißenfels", "Not yet"],
                  [lambda b: (b.say(RIN, ["Then we march. The Grauklamm first; the camp is at",
                                          "the far end of the pass."]),
                              b.switch(S_MARCH),
                              b.fadeout(), b.transfer(GRAUKLAMM, GRAUKLAMM_ENTRY[0], GRAUKLAMM_ENTRY[1], 8, 0), b.fadein()),
                   lambda b: b.say(RIN, ["Don't take long. Every day we wait, the forge eats",
                                         "another of my brother's people."])], cancel=1)
    el = Ev()
    march(el)
    mb.add("Asahina Rin", 25, 28, [pg(None, priority=0),
                                   pg(Ev().say(RIN, ["The Marshal needs his traitor. Find him, and then",
                                                     "come and find me."]), sw=S_AUDIENCE, char=RIN.char[0],
                                      index=RIN.char[1], direction=2, priority=1),
                                   pg(None, sw=S_RAID, priority=0),
                                   pg(el, sw=S_C4_END, char=RIN.char[0], index=RIN.char[1], direction=2, priority=1)])
    guard_pages = [pg(None, priority=0),
                   pg(Ev().say(ROYAL_GUARD, ["Her Highness is not to be disturbed. …Unless she wants",
                                             "to be, in which case she'll say so."]), sw=S_AUDIENCE,
                      char=ROYAL_GUARD.char[0], index=ROYAL_GUARD.char[1], direction=2, priority=1)]
    mb.add("Royal Guard", 27, 28, guard_pages)
    mb.add("Royal Guard", 23, 28, [pg(None, priority=0),
                                   pg(Ev().say(ROYAL_GUARD, ["The Crown's second company. We're the ones who didn't",
                                                             "make it to Weißenfels six years ago."]), sw=S_AUDIENCE,
                                      char=ROYAL_GUARD.char[0], index=ROYAL_GUARD.char[1], direction=2, priority=1)])
    # the sentry who saw the lights (inner fort, north)
    def lights(e):
        e.say(SENTRY, ["Kazama. Night watch on the inner wall."])
        e.say(SENTRY, ["You're the ones the Marshal set on it? Good. I'll tell",
                       "you what I told my sergeant, and he laughed at me."])
        e.say(SENTRY, ["Three nights ago: light, under the ice of the canal.",
                       "Like a lantern moving under the water. Down where the",
                       "old cistern is."])
        e.say(SENTRY, ["Nobody's used the cistern since the Wall was built.",
                       "The shaft's by the canal, east of the barracks, and",
                       "it's locked. The quartermaster keeps the key."])
        e.switch(S_CLUE_LIGHTS)
        e.quest_new(Q_CISTERN)
        clue_count(e)
        e.quest_desc(Q_COINS, "Clues: \\V[%d] of 3. The sentry Kazama saw lights under the canal ice, where the old "
                              "cistern lies." % V_CLUES)
    el = Ev().if_switch(S_CLUE_LIGHTS, True,
                        lambda b: b.say(SENTRY, ["The cistern. By the canal. The quartermaster has the key."]),
                        lambda b: b.if_switch(S_AUDIENCE, True, lights,
                                              lambda c: c.say(SENTRY, ["Move along. Wall business."])))
    mb.add("Sentry Kazama", 33, 9, [pg(el, char=SENTRY.char[0], index=SENTRY.char[1], direction=2, priority=1),
                                    pg(Ev().say(SENTRY, ["I saw the lights. I should have said it louder."]),
                                       sw=S_RAID_DONE, char=SENTRY.char[0], index=SENTRY.char[1], direction=2, priority=1)])
    # soldiers and the camp
    s1 = npc_speaker("Wallsoldat", "People3", 6)
    mb.npc("Soldier", 9, 22, s1, Ev().say(s1, ["The tents are for the ones who came in from the east",
                                                "posts. Frontposten 5 hasn't signalled in two days."]), direction=2)
    s2 = npc_speaker("Rekrutin", "People1", 1)
    mb.npc("Recruit", 5, 28, s2, Ev().say(s2, ["They say die Eiserne held the breach at Frontposten 3",
                                                "alone. For six years. Is that her? She's… smaller",
                                                "than I thought."]), direction=6)
    s3 = npc_speaker("Veteran", "People2", 4)
    mb.npc("Veteran", 13, 27, s3, Ev().say(s3, ["Three dead sentries this week. Brass on their eyes.",
                                                 "Old soldiers' tale says that's what the Brass Tyrant",
                                                 "pays for a soul. I don't like old soldiers' tales."]), direction=4)
    camp_fire(mb, 8, 29, WALLFESTE, 8, 28, 8, ["The camp's fire. The soldiers make room for you."])
    # --- the night raid (from the cistern; see zisterne())
    raid_hounds = []
    for x, y in [(33, 7), (34, 9), (31, 9)]:
        raid_hounds.append(mb.add("Raid Hound", x, y, [pg(None, priority=0),
                                                         pg(None, sw=S_RAID, char='Nature', index=0, direction=2,
                                                            priority=1, step_anime=True),
                                                         pg(None, sw=S_RAID_DONE, priority=0)]))
    vogt = mb.add("Messingvogt", 33, 6, [pg(None, priority=0)])
    rin_raid = mb.add("Rin (raid)", 33, 11, [pg(None, priority=0),     # on the gate road (30,12 was the canal)
                                             pg(None, sw=S_RAID, char=RIN.char[0], index=RIN.char[1], direction=8,
                                                priority=1),
                                             pg(None, sw=S_RAID_DONE, priority=0)])
    nishiki = mb.add("Nishiki (raid)", 34, 7, [pg(None, priority=0),
                                                 pg(None, sw=S_RAID, char=NISHIKI.char[0], index=NISHIKI.char[1],
                                                    direction=8, priority=1),
                                                 pg(None, sw=S_RAID_DONE, char='!Other2', index=4, direction=2, pattern=0,
                                                    priority=1, walk_anime=False, direction_fix=True)])
    el = Ev()
    el.set_time(23, 30)
    el.wait(20)
    el.se('Bell3', 100)
    el.shake(4, 6, 30)
    el.se('Bell3', 100)
    el.narrate(["Bells. The north gate stands open, the sally port",
                "beside it thrown wide, and the Host is coming through."])
    el.say(HANMA, ["He opened it. Of course he did. The contract said",
                   "midnight."], 'stern')
    el.se('Dog', 90, 60)
    el.battle(TR["Raid: Aschenhunde"])
    el.wait(10)
    el.route(rin_raid, [(13, [])], wait=True, skippable=True)          # she gives ground: one step back
    el.say(RIN, ["You three! Hold the gate with me, the Marshal's men",
                 "are cut off in the barracks!"])
    el.se('Chain', 90, 70)
    el.shake(5, 5, 30)
    el.route(vogt, [(41, ['Evil', 6])], wait=False)
    el.text(["Through the sally port, stooping under the arch: a",
             "figure in brass-plated robes, a chain of brass coins",
             "trailing from each hand."])
    el.say(npc_speaker("Messingvogt", "", 0), ["Clause nine. The Crown's debt falls due. Asahina Rin,",
                                                 "your brother's soul was collected at Weißenfels. Yours",
                                                 "is forfeit for the interest."])
    el.say(NISHIKI, ["That wasn't the contract! You said the gate, only the",
                     "gate! You said they'd come home!"])
    el.say(npc_speaker("Messingvogt", "", 0), ["Clause eleven. Signatories are not to read clauses."])
    el.say(RIN, ["Come and collect, then."])
    el.battle(TR["Messingvogt"])
    el.wait(20)
    el.se('Break')
    el.flash((255, 220, 120, 200), 30)
    el.text(["The Messingvogt folds in on itself like a burning",
             "ledger and is gone, leaving a heap of blackened coins."])
    el.script("$gameMap.event(%d).setImage('', 0);" % vogt)
    el.say(NISHIKI, ["…It's midnight."])
    el.say(NISHIKI, ["The contract. I opened the gate, so it's paid, and it's",
                     "due. That's how it works, the Vogt said. I get my",
                     "Mariko and my little Aya back, and the Brass Tyrant…"])
    el.say(NISHIKI, ["…gets…"])
    el.se('Bell1', 80, 60)
    el.flash((255, 200, 90, 220), 40)
    el.switch(S_RAID_DONE)
    el.wait(30)
    el.text(["Where the quartermaster stood there is a statue of",
             "brass, one hand still reaching for the gate."])
    el.say(HANMA, ["That's what a soul contract pays, my Lord. Gōen never",
                   "breaks a clause. He only writes them."], 'stern')
    el.say(FALIN, ["…He wanted his family back."], 'hurt')
    el.say(RIN, ["They're in the forge at Weißenfels. Everyone who",
                 "lived there is in that forge, working."])
    el.say(RIN, ["…And you. The light. You stepped in front of that chain",
                 "for me. Nobody has stepped in front of anything for",
                 "me since my brother."])
    el.say(KANTA, ["It seemed like the thing to do."], 'wry')
    el.say(RIN, ["Asahina Rin. Crown Princess of Hohenwacht, battle-mage,",
                 "and in your debt. Come to the keep in the morning. The",
                 "Marshal will want to hear it from you."])
    el.fadeout()
    el.switch(S_RAID, False)
    el.set_time(7, 0)
    el.recover_all()
    el.transfer(MARSCHALLHALLE, 12, 8, 8, 0)
    el.fadein()
    mb.autorun("Night Raid", el, cond_switch=S_RAID)
    for (x, y) in [(17, 15), (21, 15), (20, 25), (24, 25), (4, 13), (8, 13), (40, 13), (44, 13), (32, 8), (35, 8)]:
        mb.light('brazier', x, y)
    return mb


# ---------------------------------------------------------------------------
# 65  Marschallhalle  (sample 192): Kōsaka, Falin, Rin
# ---------------------------------------------------------------------------
def marschallhalle():
    mb = MapBuild(MARSCHALLHALLE, NAMES[MARSCHALLHALLE], 192, display=NAMES[MARSCHALLHALLE])
    mb.props(note="<Area Name: Marschallhalle>\n<No Rank HUD>", bgm=('Castle1', 55))
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 22, 24, 2, 0)
    mb.add("Stairs (courtyard)", 6, 4, [pg(el, trigger=1, priority=0)])
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 22, 18, 2, 0)
    mb.add("Stairs (inner fort)", 18, 4, [pg(el, trigger=1, priority=0)])
    kos = mb.add("Kōsaka Tetsuji", 12, 5, [pg(None, char=KOSAKA.char[0], index=KOSAKA.char[1], direction=2, priority=1)])
    officer = npc_speaker("Stabsoffizier", "People4", 6)
    mb.npc("Officer", 9, 6, officer, Ev().say(officer, ["The Marshal hasn't slept in two days. If you have",
                                                         "something for him, make it short."]), direction=6)
    rin = mb.add("Rin (hall)", 6, 9, [pg(None, priority=0)])
    herald = mb.add("Herald", 6, 10, [pg(None, priority=0)])
    # --- the audience
    el = Ev()
    el.wait(10)
    el.say(KOSAKA, ["So. Mori writes that a rank E girl killed the",
                    "Aschenschwinge at his breach. Mori drinks."])
    el.say(KANTA, ["Three of us did."], 'calm')
    el.say(KOSAKA, ["Three. A Guild vessel with an empty imprint, a ghost in",
                    "a general's coat, and…"])
    el.balloon(kos, 1)
    el.say(KOSAKA, ["…Falin."])
    el.say(FALIN, ["Marshal."], 'calm')
    el.say(KOSAKA, ["Six years. Six summonses. You ignored every one of",
                    "them, and I let you, because the breach held."])
    el.say(FALIN, ["You wanted me here, where I'd be useful to you. The",
                   "breach needed me there, where I was useful."], 'calm')
    el.say(KOSAKA, ["And now?"])
    el.say(FALIN, ["Now the breach has stone. Mori finally got his stone."], 'calm')
    el.say(KOSAKA, ["…So he did. On my order, the day his bird came."])
    el.say(KOSAKA, ["All right. If Falin walks behind you, Mori wasn't",
                    "drinking. I'll hear you out."])
    el.se('Door1')
    el.route(herald, [(41, ['People3', 7]), (16, [])], wait=True)
    el.say(HERALD, ["Her Royal Highness, the Crown Princess of Hohenwacht!"])
    el.route(herald, [(41, ['', 0])], wait=False)
    el.script("$gameMap.event(%d).setImage('%s', %d);" % (rin, RIN.char[0], RIN.char[1]))
    el.route(rin, [(19, []), (4, []), (4, [])], wait=True, skippable=True)     # she walks up the hall to the party
    el.say(RIN, ["Marshal. My father's answer."])
    el.say(KOSAKA, ["Is the same as mine, Highness. The Host is mustering on",
                    "the Aschenfeld. Gōen himself has been seen. If I send",
                    "the Wall's men to Weißenfels, the Wall falls behind",
                    "them."])
    el.say(RIN, ["Then give me the Crown's men. The Wall's can stay on",
                 "the Wall."])
    el.say(RIN, ["Weißenfels's people are still alive, Marshal. They're",
                 "working in the forge the Host built in the lower city.",
                 "My brother died holding that city. I will not leave",
                 "his people in a forge."])
    el.say(KOSAKA, ["…I know."])
    el.say(KOSAKA, ["Two thousand of the Crown's. When I know the Wall is",
                    "sound behind me. It isn't."])
    el.say(KOSAKA, ["Crates go into my stores and never come out. Three",
                    "sentries died this week, and every one had a brass",
                    "coin on each eye. Someone inside these walls is",
                    "selling us, and I don't know which of my officers."])
    el.say(HANMA, ["Brass coins on the eyes. I know that mark. It's the fee",
                   "for a soul: the Brass Tyrant pays it when a contract",
                   "is signed. Gōen is buying your Wall, Marshal."], 'stern')
    el.say(KOSAKA, ["The ghost knows her demons. Good."])
    el.say(KOSAKA, ["You three aren't mine. Nobody in this fort can have",
                    "bought you. Find me the seller, and the princess gets",
                    "her two thousand."])
    el.say(RIN, ["…Then find him quickly. I'll be in the courtyard."])
    el.route(rin, [(16, []), (1, []), (1, [])], wait=True, skippable=True)     # and back the way she came
    el.script("$gameMap.event(%d).setImage('', 0);" % rin)
    el.say(KOSAKA, ["The healer at the Lazarett laid out the dead. The",
                    "quartermaster runs the Zeughaus. My sentries walk the",
                    "inner wall. Start anywhere."])
    el.say(KOSAKA, ["And Frontposten 5, east along the Wall, hasn't signalled",
                    "in two days. If you've time, the north gate. If not,",
                    "I'll lose another squad."])
    el.quest_done(Q_WALLFESTE)
    el.quest_new(Q_COINS)
    el.quest_new(Q_FP5)
    el.switch(S_AUDIENCE)
    el.switch(S_FP5)
    el.gold(500)
    el.notice(["The Marshal pays the Guild's rate for Frontposten 3:", "\\MONEY[500]."])
    mb.autorun("Audience", el, cond_switch=S_WF)
    # --- talks afterwards
    def kosaka_talk(e):
        e.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_FP5_DONE, S_FP5_PAID), fp5_reward)
        e.if_switch(S_RAID_DONE, True, after_raid,
                    lambda b: b.say(KOSAKA, ["Lazarett, Zeughaus, the sentries. Find me the seller."]))
    def fp5_reward(e):
        e.say(KOSAKA, ["Sergeant Tōdō and her three came in an hour ago,",
                       "frostbitten and furious. Alive, all four. That's your",
                       "doing."])
        e.gold(1500)
        e.armor(foes.ARMORS["Wallhelm"], 1)
        e.notice(["Received \\MONEY[1500] and a Wallhelm."])
        e.switch(S_FP5_PAID)
        e.quest_done(Q_FP5)
    def after_raid(e):
        e.say(KOSAKA, ["The gate is shut, the fires are out, and my quarter-",
                       "master is a statue in my inner yard."])
        e.say(KOSAKA, ["Nishiki Eiji. Twenty years in the Zeughaus. His wife",
                       "and daughter were in Weißenfels when it fell."])
        e.say(KOSAKA, ["I should have known. I should have asked."])
        e.say(KOSAKA, ["You found him, and you held the gate. The Wall owes",
                       "you. This is my writ: wherever the Wall's word runs,",
                       "you speak for it."])
        e.item(KI["Siegelbrief"], 1)
        e.gold(3000)
        e.notice(["Received the \\C[6]Siegelbrief\\C[0] and \\MONEY[3000]."])
        e.say(KOSAKA, ["The princess has her two thousand. Go with her, if",
                       "you're going. Weißenfels is a day west through the",
                       "Grauklamm."])
        e.say(FALIN, ["That's where I woke."], 'calm')
        e.say(KOSAKA, ["Then maybe it's where you'll find out why."])
        e.quest_done(Q_COINS)
        e.quest_done(Q_CISTERN)
        e.quest_new(Q_WF)
        e.switch(S_C4_END)
        e.rest_point(WALLFESTE, 21, 32, 8)
    el = Ev()
    el.if_switch(S_C4_END, True, lambda b: b.say(KOSAKA, ["The princess is in the courtyard. Gods keep you."]),
                 kosaka_talk)
    mb.add("Kōsaka (talk)", 12, 5, [pg(None, priority=0),
                                    pg(el, sw=S_AUDIENCE, char=KOSAKA.char[0], index=KOSAKA.char[1], direction=2,
                                       priority=1)])
    # remove the audience sprite once the talk page takes over
    mb.m['events'][kos]['pages'].append(pg(None, sw=S_AUDIENCE, priority=0))
    # the morning after the raid
    el = Ev()
    el.wait(10)
    el.say(KOSAKA, ["Come here, all three of you."])
    kosaka_talk(el)
    mb.autorun("Morning After", el, cond_switch=S_RAID_DONE)
    return mb


# ---------------------------------------------------------------------------
# 66  Kaserne  (sample 153): the barracks' mess hall; rest
# ---------------------------------------------------------------------------
def kaserne():
    mb = MapBuild(KASERNE, NAMES[KASERNE], 153, display=NAMES[KASERNE])
    mb.props(note="<Area Name: Kaserne>\n<No Rank HUD>", bgm=('Town5', 50), bgs=('Fire1', 25))
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 19, 15, 2, 0)
    mb.add("Exit", 8, 13, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(COOK, ["Hanamura. I feed the Wall. You look like you haven't",
                  "eaten since Frontposten 3."])
    def sleep(e):
        e.fadeout()
        e.me('Inn1')
        e.wait(90)
        e.recover_all()
        e.set_time(7, 0)
        e.rest_point(KASERNE, 8, 11, 8)
        e.fadein()
        e.say(COOK, ["Porridge. Eat it, it's an order."])
    el.choices(["Eat and sleep (free)", "Not now"], [sleep, None], cancel=1)
    mb.npc("Cook", 8, 7, COOK, el, direction=2)
    s1 = npc_speaker("Wallsoldat", "People3", 7)
    mb.npc("Soldier", 4, 9, s1, Ev().say(s1, ["Crates came in last week: bandages, lamp oil, arrows.",
                                               "Signed for. I saw the signature. Never saw the crates."]),
           direction=6)
    s2 = npc_speaker("Bogenschützin", "People4", 5)
    mb.npc("Archer", 13, 9, s2, Ev().say(s2, ["The quartermaster's been jumpy for weeks. Nishiki's",
                                               "a decent sort. Had family in Weißenfels, poor man."]),
           direction=4)
    mb.light('hearth', 8, 2)
    return mb


# ---------------------------------------------------------------------------
# 67  Lazarett  (sample 151): the healer Yukimura Saki, the coin
# ---------------------------------------------------------------------------
def lazarett():
    mb = MapBuild(LAZARETT, NAMES[LAZARETT], 151, display=NAMES[LAZARETT])
    mb.props(note="<Area Name: Lazarett>\n<No Rank HUD>", bgm=('Scene6', 45))
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 6, 13, 2, 0)
    mb.add("Stairs", 2, 9, [pg(el, trigger=1, priority=0)])
    def clue(e):
        e.say(SAKI, ["The Marshal sent you? Good. Then look at this."])
        e.text(["On a cloth on the table: two coins of dull brass. On",
                "each, a tiny hand is stamped, holding a quill."])
        e.say(SAKI, ["From the eyes of the last sentry. Tōya, nineteen. No",
                     "wound on him. His heart simply stopped."])
        e.say(HANMA, ["A quill in a brass hand. Gōen's seal. The coins are",
                      "the price of a soul that has been signed over. Whoever",
                      "sold the Wall signed for them."], 'stern')
        e.say(SAKI, ["There's something else. I've requested bandages four",
                     "times this month. The ledger says they were delivered.",
                     "They never came. Ask the quartermaster where they went."])
        e.item(KI["Messingmünze"], 1)
        e.notice(["Received the \\C[6]Messingmünze\\C[0]."])
        e.switch(S_CLUE_COIN)
        clue_count(e)
        e.quest_desc(Q_COINS, "Clues: \\V[%d] of 3. The coins carry Gōen's seal: a soul was sold. The ledger says "
                              "the Lazarett's bandages were delivered; they never came. The quartermaster keeps "
                              "the ledger in the Zeughaus." % V_CLUES)
    def heal(e):
        e.se('Heal3')
        e.recover_all()
        e.say(SAKI, ["There. Try to stay in one piece. I'm out of bandages."])
    el = Ev()
    el.if_switch(S_AUDIENCE, True,
                 lambda b: b.if_switch(S_CLUE_COIN, False, clue,
                                       lambda c: (c.say(SAKI, ["Let me look at those wounds."]), heal(c))),
                 lambda b: (b.say(SAKI, ["Yukimura. I run the Lazarett. Sit, you're bleeding",
                                         "on my floor."]), heal(b)))
    mb.npc("Yukimura Saki", 6, 6, SAKI, el, direction=2)
    w1 = npc_speaker("Verwundeter", "People3", 7)
    mb.add("Wounded", 4, 5, [pg(Ev().say(w1, ["Hellhound got my leg. Burns like it's still in there."]),
                                char='Damage1', index=6, direction=2, priority=1)])
    w2 = npc_speaker("Verwundete", "People4", 5)
    mb.add("Wounded", 7, 8, [pg(Ev().say(w2, ["Frontposten 5 was mine. I got out. Sergeant Tōdō",
                                                "didn't. She's still up that tower with three of ours."]),
                                 char='Damage2', index=7, direction=2, priority=1)])
    return mb


# ---------------------------------------------------------------------------
# 68  Zeughaus  (sample 186): the quartermaster Nishiki Eiji, his ledger, the key
# ---------------------------------------------------------------------------
def zeughaus():
    mb = MapBuild(ZEUGHAUS, NAMES[ZEUGHAUS], 186, display=NAMES[ZEUGHAUS])
    mb.props(note="<Area Name: Zeughaus>\n<No Rank HUD>", bgm=('Town3', 50))
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 42, 13, 2, 0)
    mb.add("Exit", 11, 13, [pg(el, trigger=1, priority=0)])
    A, W, I = foes.ARMORS, foes.WEAPONS, foes.ITEMS
    goods = [('item', IT["Großer Heiltrank"]), ('item', I["Elixier"]), ('item', IT["Manatrank"]),
             ('item', I["Hoher Manatrank"]), ('item', IT["Riechsalz"]), ('item', IT["Lichtphiole"]),
             ('item', I["Allheilmittel"]),
             ('armor', A["Wallhelm"]), ('armor', A["Fellkapuze"]), ('armor', A["Wallschild"]),
             ('armor', A["Kriegeramulett"]), ('armor', A["Heilerstola"]), ('armor', A["Glutamulett"]),
             ('armor', A["Wachstiefel"]), ('armor', A["Brandschutzmantel"]),
             ('weapon', W["Wallfäuste"]), ('weapon', W["Kriegsflegel"])]
    def ask(e):
        e.say(KANTA, ["The Lazarett's bandages. Four requests, the ledger says",
                      "delivered, and they never arrived."], 'calm')
        e.say(NISHIKI, ["The… bandages. Yes. There must be a mistake in the",
                        "count. I'll see to it. I'll see to it now, in the",
                        "stores. Excuse me."])
        e.fadeout()
        e.switch(S_NISHIKI_GONE)
        e.fadein()
        e.say(FALIN, ["He's running."], 'calm')
        e.say(HANMA, ["He's afraid. The ledger's on his desk, my Lord."], 'stern')
    def shop(e):
        e.shop(goods)
    el = Ev()
    el.say(NISHIKI, ["Nishiki, quartermaster. The Wall's stores, at the Wall's",
                     "prices, which is to say nobody's happy."])
    el.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_CLUE_COIN, S_NISHIKI_GONE),
                 lambda b: b.choices(["Buy", "Ask about the bandages", "Nothing"], [shop, ask, None], cancel=2),
                 lambda b: b.choices(["Buy", "Nothing"], [shop, None], cancel=1))
    mb.add("Nishiki Eiji", 11, 5, [pg(el, char=NISHIKI.char[0], index=NISHIKI.char[1], direction=2, priority=1),
                                   pg(None, sw=S_NISHIKI_GONE, priority=0)])
    # his clerk keeps selling once he's gone
    clerk = npc_speaker("Schreiber", "People1", 4)
    el = Ev().say(clerk, ["The quartermaster stepped out. I can sell you things.",
                          "I can't explain things."])
    el.shop(goods)
    mb.add("Clerk", 13, 7, [pg(None, priority=0),
                            pg(el, sw=S_NISHIKI_GONE, char=clerk.char[0], index=clerk.char[1], direction=2, priority=1)])
    # the ledger and the key
    def ledger(e):
        e.text(["The supply ledger. Crates of bandages, lamp oil, arrows,",
                "grain: signed for, week after week, always at night,",
                "always in the same neat hand."])
        e.text(["N. Eiji."])
        e.text(["Behind the ledger, on a hook: an old iron key, marked",
                "ZISTERNE."])
        e.item(KI["Hauptbuch"], 1)
        e.item(KI["Zisternenschlüssel"], 1)
        e.notice(["Took the \\C[6]Hauptbuch\\C[0] and the \\C[6]Zisternenschlüssel\\C[0]."])
        e.say(HANMA, ["The stores go down to the cistern, and the cistern goes",
                      "to whoever is waiting in it."], 'stern')
        e.switch(S_CLUE_LEDGER)
        clue_count(e)
        e.quest_desc(Q_COINS, "Clues: \\V[%d] of 3. The missing crates were signed for at night by the "
                              "quartermaster, Nishiki Eiji. He has fled; his key opens the old cistern." % V_CLUES)
        e.self_switch('A')
    mb.add("Ledger", 10, 5, [pg(None, priority=0),
                             pg(Ev().if_self('A', False, ledger), sw=S_NISHIKI_GONE, char='', trigger=0, priority=0),
                             pg(Ev().text(["The ledger's gone. You took it."]), self_sw='A', priority=0)])
    guard = npc_speaker("Zeugwart", "People3", 6)
    mb.npc("Armorer", 8, 8, guard, Ev().say(guard, ["Rune-steel from Eisenberg, when it comes. It doesn't",
                                                      "come often."]), direction=6)
    return mb


# ---------------------------------------------------------------------------
# 69  Frontposten 5  (sample 195): the besieged tower (optional)
# ---------------------------------------------------------------------------
def fp5_turm():
    mb = MapBuild(FP5_TURM, NAMES[FP5_TURM], 195, display=NAMES[FP5_TURM])
    mb.props(note="<Rank: D>\n<Area Name: Frontposten 5>", bgm=('Dungeon5', 55), bgs=('Wind3', 40),
             battleback=('Stone2', 'Fort2'))
    el = Ev().if_switch(S_FP5_DONE, True,
                        lambda b: (b.se('Move1', 60), b.transfer(WALLFESTE, 33, 7, 2, 0)),
                        lambda b: b.choices(["Back to the Wallfeste", "Stay"],
                                            [lambda c: (c.se('Move1', 60), c.transfer(WALLFESTE, 33, 7, 2, 0)), None],
                                            cancel=1))
    mb.add("Tower Door", 12, 44, [pg(el, trigger=0, priority=1)])
    el = Ev()
    el.narrate(["Frontposten 5: a single tower where the Wall bends",
                "north. The door has been torn off. Inside, the stairs",
                "go up into the dark, and something up there shrieks."])
    el.say(FALIN, ["Gargoyles. They'll be on every floor. Rank D."], 'fierce')
    el.say(HANMA, ["Above us again, and they hit hard. We don't have to do",
                   "this, my Lord. Nobody would blame us."], 'stern')
    el.say(KANTA, ["Four people are up there."], 'calm')
    el.say(HANMA, ["…Then up we go. Carefully."], 'command')
    mb.autorun("Tower", el)
    # two floors of foes, one scripted fight each
    for (name, x, y, troop, sprite, index, lines) in [
            ("Gargoyle", 12, 32, "Gargyl", 'Monster', 7,
             ["Stone wings unfold in the dark, and a gargoyle drops", "from the rafters."]),
            ("Hellhound", 11, 19, "Gargyl & Aschenhund", 'Monster', 7,
             ["An ash hound guards the stair, and a gargoyle clings to", "the wall above it."])]:
        e = Ev()
        e.se('Monster2', 80, 90)
        e.text(lines)
        e.battle(TR[troop])
        e.self_switch('A')
        mb.add(name, x, y, [pg(e, char=sprite, index=index, direction=2, trigger=2, priority=1, step_anime=True),
                            pg(None, self_sw='A', priority=0)])
    # the squad at the top
    sgt = mb.add("Sergeant Tōdō", 6, 5, [pg(None, char=SERGEANT5.char[0], index=SERGEANT5.char[1], direction=2,
                                            priority=1),
                                         pg(None, sw=S_FP5_DONE, priority=0)])
    mb.add("Soldier", 4, 5, [pg(None, char='Damage2', index=5, direction=2, priority=1), pg(None, sw=S_FP5_DONE, priority=0)])
    mb.add("Soldier", 7, 5, [pg(None, char='People3', index=7, direction=4, priority=1), pg(None, sw=S_FP5_DONE, priority=0)])
    el = Ev()
    el.say(SERGEANT5, ["Stop right there, or— …You're not gargoyles."])
    el.say(SERGEANT5, ["Tōdō Ren, Frontposten 5. Four of us left, one who",
                       "can't walk. We've been holding this stair with pikes",
                       "and prayers for two days."])
    el.say(KANTA, ["The Marshal sent us. Can you walk out?"], 'calm')
    el.say(SERGEANT5, ["Now we can. …Listen."])
    el.se('Monster2', 90, 70)
    el.shake(4, 6, 30)
    el.say(SERGEANT5, ["They heard you come up. All of them."])
    el.say(FALIN, ["Behind me. All of you."], 'fierce')
    el.battle(TR["Gargyl & Aschenhunde"])
    el.switch(S_FP5_DONE)
    el.fadeout()
    el.narrate(["You carry the wounded down the stairs and out into the",
                "snow, and three miles back along the Wall to the",
                "Wallfeste's north gate."])
    el.quest_desc(Q_FP5, "Sergeant Tōdō and her three are home. Tell the Marshal.")
    el.transfer(WALLFESTE, 33, 7, 2, 0)
    el.fadein()
    mb.add("Top", 5, 6, [pg(el, trigger=1, priority=0), pg(None, sw=S_FP5_DONE, priority=0)])
    mb.light('torch', 6, 4)
    mb.light('torch', 11, 29)
    mb.light('torch', 11, 16)
    mb.light('torch', 11, 42)
    return mb


# ---------------------------------------------------------------------------
# 70  Alte Zisterne  (sample 49): Gōen's clerk and the quartermaster
# ---------------------------------------------------------------------------
def zisterne():
    mb = MapBuild(ZISTERNE, NAMES[ZISTERNE], 49, display=NAMES[ZISTERNE])
    mb.props(note="<Rank: E>\n<Area Name: Alte Zisterne>", bgm=('Dungeon3', 55), bgs=('Drips', 45),
             battleback=('Stone3', 'Temple'),
             encounters=[(TR["Ghule x3"], 5, ()), (TR["Messinggolems x2"], 4, ()), (TR["Ghule & Golem"], 5, ())],
             steps=26)
    el = Ev().se('Move1', 60).transfer(WALLFESTE, 28, 15, 2, 0)
    mb.add("Shaft", 11, 25, [pg(Ev().if_switch(S_SCRIBE, False, lambda b: b.text(["There's no going back up now."]),
                                               lambda b: (b.se('Move1', 60), b.transfer(WALLFESTE, 28, 15, 2, 0))),
                                trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The old cistern: a flooded hall of pillars under the",
                "fort, older than the Wall. Somebody has been down here.",
                "The walkways are swept, and there are crates."])
    el.say(HANMA, ["Bandages. Lamp oil. Arrows. All the Wall's missing",
                   "crates, stacked neatly, waiting to be collected."], 'stern')
    mb.autorun("Cistern", el)
    for (x, y) in [(6, 16), (16, 16), (5, 14)]:
        mb.add("Crates", x, y, [pg(Ev().text(["Crates stamped with the Wall's black tower. Bandages."]),
                                   char='!Other1', index=0, direction=2, priority=1)])
    chest(mb, "Chest", 16, 8, lambda e: (e.item(foes.ITEMS["Hoher Manatrank"], 2), e.gold(400)),
          "Found 2 Hoher Manatrank and \\MONEY[400].")
    chest(mb, "Chest", 6, 8, lambda e: e.armor(foes.ARMORS["Brandschutzmantel"], 1), "Found a Brandschutzmantel.")
    scribe = mb.add("Messingschreiber", 12, 7, [pg(None, char='!Other1', index=7, direction=2, priority=1,
                                                   step_anime=True),
                                                pg(None, sw=S_SCRIBE, priority=0)])
    nish = mb.add("Nishiki", 10, 8, [pg(None, char=NISHIKI.char[0], index=NISHIKI.char[1], direction=8, priority=1),
                                      pg(None, sw=S_SCRIBE, priority=0)])
    el = Ev()
    el.balloon(nish, 1)
    el.route(nish, [(16, [])], wait=True)
    el.say(NISHIKI, ["…You weren't supposed to come down here. Nobody comes",
                     "down here."])
    el.say(KANTA, ["The crates. The sentries. Why?"], 'calm')
    el.say(NISHIKI, ["Mariko. My wife. And Aya, she was six. They were in",
                     "Weißenfels when it fell. Everyone thought they were",
                     "dead. Then this thing came up out of the water with",
                     "a letter in Aya's hand."])
    el.say(NISHIKI, ["Alive. Working in the forge. And the Brass Tyrant would",
                     "send them home. For crates. For a few coins. For one",
                     "gate, one night."])
    el.say(HANMA, ["And the sentries who saw you?"], 'stern')
    el.say(NISHIKI, ["I didn't kill them! The contract said witnesses would",
                     "be… removed. I didn't know it meant…"])
    el.se('Book1')
    el.say(npc_speaker("Messingschreiber", "", 0), ["Clause seven. Witnesses are to be removed. The clause",
                                                     "does not specify how many."])
    el.say(NISHIKI, ["It's midnight soon. I have to open the gate, or they",
                     "die. I'm sorry. I'm so sorry."])
    el.route(nish, [(1, []), (1, []), (1, []), (1, [])], wait=False)
    el.say(FALIN, ["He's running for the gate. The book first."], 'fierce')
    el.battle(TR["Messingschreiber"])
    el.switch(S_SCRIBE)
    el.wait(10)
    el.say(HANMA, ["The gate, my Lord. Up the shaft, now!"], 'command')
    el.quest_desc(Q_COINS, "It was the quartermaster, Nishiki Eiji. He's running to open the north gate at midnight.")
    el.fadeout()
    el.switch(S_RAID)
    el.transfer(WALLFESTE, 28, 15, 8, 0)
    el.fadein()
    mb.add("Circle", 11, 12, [pg(el, trigger=1, priority=0), pg(None, sw=S_SCRIBE, priority=0)])
    mb.light('pool', 11, 8)
    mb.light('torch', 6, 7)
    mb.light('torch', 16, 7)
    return mb
