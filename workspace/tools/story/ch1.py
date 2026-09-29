"""Chapter 1: Rabenau. The village, the night raid, the Rabenholz and Krummzahn's tower."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story.ids import *

TODO = npc_speaker("Tōdō Keiji", "Actor3", 0)
IZUMI = npc_speaker("Hanamura Izumi", "People1", 5)
OKUDA = npc_speaker("Okuda Noboru", "People2", 0)
NATSU = npc_speaker("Natsu", "People1", 0)
MATSUDA = npc_speaker("Matsuda Daichi", "People2", 6)
SAEKI = npc_speaker("Saeki Chiaki", "People4", 7)
SAGARA = npc_speaker("Sagara Takumi", "People2", 4)
MOTHER = npc_speaker("Kazama Hana", "People1", 1)
KRUMM = Speaker("Krummzahn", "", 0, ("Monster", 1))
GOBLIN_CHAR = ("Monster", 1)
PIG = ("Nature", 2)

Q_ROOF = Quest(1, "A Roof and a Meal", "Tōdō Keiji", "Rabenau",
               "The watch captain at the gate says the inn \"Zum Schwarzen Raben\" lies past the bridge, east of "
               "the square. Tell Hanamura Izumi that Tōdō sent you.",
               "Find the inn in Rabenau.")
Q_WATCH = Quest(2, "Night Watch", "Hanamura Izumi", "Rabenau",
                "Stand the south fence with Tōdō until midnight: stew, bread and beds in return. Goblins have been "
                "sniffing round the village for three nights. Talk to Tōdō at the south gate when you're ready.",
                "Talk to Tōdō at the south gate.")
Q_GOBLINS = Quest(3, "Goblins in the Rabenholz", "Okuda Noboru", "Rabenholz",
                  "Elder Okuda wants to see you. His house is the big one at the north end of the village.",
                  "See Elder Okuda (north).")
Q_PIGLETS = Quest(4, "Natsu's Piglets", "Natsu", "Rabenau, Rabenholz",
                  "Three of Natsu's piglets bolted after the goblins in the night. One may still be in the village; "
                  "the others ran south into the Rabenholz.",
                  "Find 3 piglets.")
Q_EAST = Quest(5, "East to Eisfurt", "Sagara Takumi", "Oststraße",
               "The merchant Sagara Takumi needs guards for the Oststraße to Eisfurt: two days on the road. "
               "He pays 1 gk. Meet him at the south gate when you're ready to leave.",
               "Meet Sagara at the south gate.")

S_ARRIVED = SW('C1: Arrived')
S_DEAL = SW('C1: Inn Deal')
S_RAID = SW('C1: Raid')
S_RAID_DONE = SW('C1: Raid Done')
S_SUMMONED = SW('C1: Summoned')
S_QUEST = SW('C1: Tower Quest')
S_BOSS = SW('C1: Krummzahn Down')
S_REWARD = SW('C1: Rewarded')
S_EAST = SW('C1: Sagara Hired')
S_PIGQ = SW('C1: Piglet Quest')
S_PIGDONE = SW('C1: Piglets Home')
V_PIGS = VAR('Piglets Found')

def build():
    return [rabenau(), inn(), elder(), herbs(), smithy(), farm(), rabenholz(), deepwood(), ruin(), towertop()]

def piglet(mb, name, x, y, flag):
    el = Ev()
    el.se('Cry1', 70, 150)
    el.balloon(0, 1)
    el.text(["A piglet, muddy and trembling, squeals at the sight", "of your light."])
    el.if_switch(S_PIGQ, True,
                 lambda b: (b.text(["You scoop it up. It squirms, then settles against", "the cold silver of your armor."]),
                            b.var(V_PIGS, 1, '+'), b.switch(flag),
                            b.if_var(V_PIGS, '>=', 3,
                                     lambda c: c.quest_desc(Q_PIGLETS, "All three piglets found. Take them back to "
                                                                       "Natsu at the farm by the field in Rabenau."),
                                     lambda c: c.notice(["Piglets found: \\V[%d] / 3" % V_PIGS]))),
                 lambda b: b.say(HANMA, ["Someone's pig. Someone will want it back.",
                                         "We're not thieves, my Lord."], 'calm'))
    mb.add(name, x, y, [pg(el, char=PIG[0], index=PIG[1], direction=2, trigger=0, priority=1, move_type=1,
                           step_anime=False), pg(None, sw=flag, priority=0)])

def chest(mb, name, x, y, give, label, index=0):
    el = Ev().se('Chest1')
    el.route(0, [36, 17, (15, [3]), 18, (15, [3]), 19, 35])
    give(el)
    el.text([label])
    el.self_switch('A')
    return mb.add(name, x, y, [pg(el, char='!Chest', index=index, direction=2, pattern=0, trigger=0, priority=1,
                                  walk_anime=False, direction_fix=True),
                               pg(None, self_sw='A', char='!Chest', index=index, direction=8, pattern=0, priority=1,
                                  walk_anime=False, direction_fix=True)])

# ---------------------------------------------------------------------------
# 5  Rabenau  (sample 106)
# ---------------------------------------------------------------------------
def rabenau():
    mb = MapBuild(RABENAU, NAMES[RABENAU], 106, display=NAMES[RABENAU])
    mb.props(note="<Rank: F>\n<Area Name: Rabenau>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town1', 70), battleback=('Grassland', 'Town1'), encounters=[], steps=999)

    # --- raid goblins (visible only during the raid) -------------------------
    gob = []
    for x, y in [(12, 28), (13, 29), (14, 28)]:
        gob.append(mb.add("Raider", x, y, [pg(None, priority=0),
                                           pg(None, sw=S_RAID, char=GOBLIN_CHAR[0], index=GOBLIN_CHAR[1], direction=8,
                                              priority=1)]))

    # --- arrival and Tōdō at the gate ----------------------------------------
    el = Ev()
    el.weather('none', 0, 0)
    el.card("Kapitel 1", "Rabenau", 200)
    el.wait(20)
    el.say(TODO, ["That's far enough. Hands where I can see them."])
    el.if_switch(SW('P: Trees'), True,
                 lambda b: b.say(TODO, ["Out of the trees, at dawn, in the rain. Either you're",
                                        "lost or you're trouble."]),
                 lambda b: b.say(TODO, ["Nobody walks that road at dawn unless they're lost",
                                        "or trouble."]))
    el.say(TODO, ["Silver plate and a red cape: you're no pilgrim. And your",
                  "friend's dressed for a funeral a hundred years ago."])
    el.say(HANMA, ["Two hundred, at least."], 'smile')
    el.say(KANTA, ["We saw the smoke. We need food and a place to sleep."], 'calm')
    el.say(TODO, ["No packs, no horse, no coin, I'd wager."])
    el.balloon(-1, 8)
    el.say(TODO, ["…Tōdō Keiji. I keep the watch here, what's left of it.",
                  "This is Rabenau: farmers, mostly. We've had trouble",
                  "enough this spring without strangers bringing more."])
    el.say(KANTA, ["We're not bringing trouble."], 'calm')
    el.say(TODO, ["Everybody says that."])
    el.say(TODO, ["The inn's past the bridge, east of the square: Hanamura's",
                  "place, \"Zum Schwarzen Raben\". Tell her Tōdō sent you,",
                  "and she won't throw you out before you've eaten."])
    el.quest_new(Q_ROOF)
    el.notice(["\\C[6]Quests\\C[0]: the menu's Quests page keeps track of what",
               "you've promised, and to whom."])
    el.switch(S_ARRIVED)
    mb.autorun("Arrival", el)

    # Tōdō: depending on the story
    def todo_pages():
        pages = []
        # default (before the deal)
        el = Ev().say(TODO, ["The inn's east of the square, past the bridge.", "Go on. I'm watching the road."])
        pages.append(pg(el, char=TODO.char[0], index=TODO.char[1], direction=2, priority=1))
        # after the inn deal: the night watch
        el = Ev()
        el.say(TODO, ["Izumi sent you? Good. Two more pairs of eyes. You'll",
                      "stand the fence with me until midnight."])
        def start_raid(e):
            e.fadeout()
            e.recover_all()
            e.set_time(21, 0)
            e.bgs('Night', 60)
            e.locate(-1, 13, 26, 2)
            e.locate(0, 14, 26, 2)
            e.wait(30)
            e.fadein()
            e.say(TODO, ["Quiet so far. They come from the south, from the",
                         "Rabenholz. Always the pens, always the pigs."])
            e.say(KANTA, ["Goblins."], 'calm')
            e.say(TODO, ["Goblins. Filthy, cowardly, and never this close before.",
                         "Something's pushing them out of that forest."])
            e.say(HANMA, ["Something with teeth, usually."], 'stern')
            e.wait(40)
            e.se('Crash')
            e.shake(4, 6, 20)
            e.se('Cry2', 80, 140)
            e.switch(S_RAID)
            e.say(TODO, ["There! By the gate!"])
            for gid in gob:
                e.route(gid, [4], wait=False)
            e.wait(20)
            e.say(HANMA, ["Three. Take the one with the spear first."], 'command')
            e.switch(S_RAID, False)
            e.battle(TR["Raid: Goblins"], can_escape=False, can_lose=False)
            e.se('Run')
            e.text(["The raiders scatter back into the dark, squealing.",
                    "Somewhere a pig is squealing too, running the same way."])
            e.say(TODO, ["Hah. Not bad, for travelers."])
            e.route(0, [(19, [])])
            e.balloon(0, 1)
            e.say(TODO, ["…That light of yours. I saw a knight make something",
                         "like it once, up on the Nordwall. It didn't end well",
                         "for him."])
            e.say(KANTA, ["It hasn't ended yet for me."], 'wry')
            e.say(TODO, ["See that it doesn't."])
            e.se('Run')
            e.say(NATSU, ["My piglets! Three of them ran off, after the goblins!",
                          "Into the woods, in the dark!"])
            e.say(TODO, ["Natsu, go home. Nobody goes into the Rabenholz at night."])
            e.say(NATSU, ["But they'll get eaten!"])
            e.say(KANTA, ["…We'll look for them. In daylight."], 'calm')
            e.quest_new(Q_PIGLETS)
            e.switch(S_PIGQ)
            e.quest_done(Q_WATCH)
            e.switch(S_RAID_DONE)
            e.say(TODO, ["Go and get your supper. The elder will want to see you",
                         "in the morning, if you're still here."])
            e.fadeout()
            e.fade_bgs(1)
            e.transfer(INN, 13, 7, 2, 2)
        el.choices(["We're ready", "Not yet"], [start_raid, lambda e: e.say(TODO, ["Don't take too long."])], cancel=1)
        pages.append(pg(el, sw=S_DEAL, char=TODO.char[0], index=TODO.char[1], direction=2, priority=1))
        # after the raid
        el = Ev()
        el.if_switch(S_QUEST, True,
                     lambda b: b.say(TODO, ["The Rabenholz path starts right here, south. Wolves",
                                            "in the thickets, goblins further in. Mind the old",
                                            "watchtower; they'll be thickest there."]),
                     lambda b: b.say(TODO, ["The elder's house is the big one at the north end.",
                                            "He'll want a word."]))
        pages.append(pg(el, sw=S_RAID_DONE, char=TODO.char[0], index=TODO.char[1], direction=2, priority=1))
        el = Ev()
        el.say(TODO, ["So it was Krummzahn. I know the name; he's raided the",
                      "Oststraße for years. Something scared that old goblin",
                      "out of his hole. That's what worries me."])
        el.say(TODO, ["You fight like you've done it before, both of you.",
                      "If you're going on, register with the Guild in",
                      "Wachtburg. They pay properly. We can't."])
        pages.append(pg(el, sw=S_BOSS, char=TODO.char[0], index=TODO.char[1], direction=2, priority=1))
        return pages
    mb.add("Tōdō", 14, 26, todo_pages())

    # --- the south gate: where to? ---------------------------------------
    def gate_menu(e):
        def to_road(b):
            b.se('Move1', 60)
            b.transfer(ROAD, 27, 10, 4, 0)
        def to_wood(b):
            b.se('Move1', 60)
            b.transfer(RABENHOLZ, 15, 26, 8, 0)
        def stay(b):
            b.route(-1, [(4, [])], wait=True, skippable=True)
        def east(b):
            b.say(SAGARA, ["There you are. Mule's loaded, the roads are dry.",
                           "Let's go before I think better of it."])
            b.se('Move1', 60)
            b.transfer(OSTSTRASSE, 5, 21, 8, 0)
        e.if_switch(S_EAST, True,
                    lambda b: b.choices(["Oststraße (east, with Sagara)", "Rabenholz (south)", "Karrenweg (west)", "Stay"],
                                        [east, to_wood, to_road, stay], cancel=3),
                    lambda b: b.if_switch(S_QUEST, True,
                                          lambda c: c.choices(["Rabenholz (south)", "Karrenweg (west)", "Stay"],
                                                              [to_wood, to_road, stay], cancel=2),
                                          lambda c: c.choices(["Karrenweg (west)", "Stay"], [to_road, stay], cancel=1)))
    for x in (12, 13, 14):
        el = Ev()
        gate_menu(el)
        mb.add("South Gate", x, 29, [pg(el, trigger=1, priority=0)])

    # --- doors -----------------------------------------------------------
    mb.door(23, 22, INN, 9, 13, 8, name="Door: Inn")
    mb.door(20, 14, SMITHY, 8, 9, 8, name="Door: Smithy")
    mb.door(23, 4, ELDER, 5, 11, 8, name="Door: Elder")
    mb.door(10, 8, HERBS, 8, 9, 8, name="Door: Herbalist")
    mb.door(7, 8, FARM, 8, 10, 8, name="Door: Farm")
    mb.door(2, 22, 0, 0, 0, locked_text=["Barred from the inside. Since the raids began,",
                                         "nobody opens after dark, or before noon."], name="Door: House")
    mb.door(6, 22, 0, 0, 0, locked_text=["\"Gone to Eisfurt for seed. Back by Grünmond.\"",
                                         "A note, nailed to the door."], name="Door: House")

    # --- townsfolk ---------------------------------------------------------
    el = Ev()
    el.if_switch(S_BOSS, True,
                 lambda b: b.say(npc_speaker("Old Hisako", "People1", 7),
                                 ["My hens came back on their own this morning.",
                                  "Smarter than goblins, hens."]),
                 lambda b: b.say(npc_speaker("Old Hisako", "People1", 7),
                                 ["The raiders took my hens. Hens! What does a goblin",
                                  "want with hens? …Don't answer that."]))
    mb.npc("Old Hisako", 8, 24, ("People1", 7), el, direction=6, move_type=0)

    el = Ev().say(npc_speaker("Farmer Ren", "People1", 6),
                  ["The frost came late this year, and the goblins early.",
                   "Akatsuki's dawn, but we're tired."])
    el.say(npc_speaker("Farmer Ren", "People1", 6),
           ["They say the north's worse. My cousin's boy went to",
            "the Wall two winters ago. No letters since the snow."])
    mb.npc("Farmer Ren", 9, 13, ("People1", 6), el, direction=4, move_type=0)

    kid = npc_speaker("Hayate", "People1", 2)
    el = Ev().say(kid, ["Is that light real? Can I touch it?"])
    el.say(KANTA, ["No."], 'calm')
    el.say(kid, ["…Can I look at it?"])
    el.say(KANTA, ["…Yes."], 'wry')
    el.balloon(0, 4)
    mb.npc("Hayate", 17, 24, ("People1", 2), el, direction=2, move_type=1)

    watch = npc_speaker("Watchman Jin", "People3", 6)
    el = Ev().if_switch(S_RAID_DONE, True,
                        lambda b: b.say(watch, ["Tōdō says you're alright. From him that's a medal."]),
                        lambda b: b.say(watch, ["Strangers. And one of you looks like a ghost.",
                                                "No offence to the ghost."]))
    el.if_switch(S_RAID_DONE, False, lambda b: b.say(HANMA, ["None taken. I've been called worse by better."], 'smile'))
    mb.npc("Watchman Jin", 14, 18, ("People3", 6), el, direction=2)

    el = Ev().say(NATSU, ["Hi! I'm Natsu. I look after the pigs. Well, I help."])
    natsu_q = Ev()
    natsu_q.if_var(V_PIGS, '>=', 3,
                   lambda b: (b.say(NATSU, ["You found them! All three! Oh, you smell like mud,",
                                            "you little idiots…"]),
                              b.say(NATSU, ["Mama! Mama, they're back!"]),
                              b.say(MOTHER, ["You brought them back from the Rabenholz? Here.",
                                             "It isn't much, but take it, please."]),
                              b.se('Coin'), b.gold(30), b.item(IT["Kräuterbündel"], 3),
                              b.notice(["Received \\MONEY[30] and 3 Kräuterbündel."]),
                              b.quest_done(Q_PIGLETS), b.switch(S_PIGDONE)),
                   lambda b: b.say(NATSU, ["Did you find them? There were three…", "Found so far: \\V[%d]." % V_PIGS]))
    el2 = Ev().say(NATSU, ["Mama says you're heroes. I said you're just",
                           "strangers who're good with pigs."])
    el2.say(KANTA, ["That's closer."], 'wry')
    mb.npc("Natsu", 9, 11, NATSU, el, direction=2,
           pages_extra=[pg(natsu_q, sw=S_PIGQ, char=NATSU.char[0], index=NATSU.char[1], direction=2, priority=1),
                        pg(el2, sw=S_PIGDONE, char=NATSU.char[0], index=NATSU.char[1], direction=2, priority=1)])

    piglet(mb, "Piglet (village)", 21, 7, SW('C1: Piglet 1'))

    # the well: a free drink
    el = Ev().text(["The village well. The water is cold and tastes of stone."])
    mb.add("Well", 10, 22, [pg(el, trigger=0, priority=1)])
    return mb

# ---------------------------------------------------------------------------
# 6  Zum Schwarzen Raben  (sample 113)
# ---------------------------------------------------------------------------
def inn():
    mb = MapBuild(INN, NAMES[INN], 113, display=NAMES[INN])
    mb.props(note="<Area Name: Zum Schwarzen Raben>\n<No Rank HUD>", bgm=('Town2', 60), bgs=('Fire1', 30))
    for x, y in [(9, 14)]:
        el = Ev().se('Move1', 60).transfer(RABENAU, 23, 23, 2, 0)
        mb.add("Exit", x, y, [pg(el, trigger=1, priority=0)])

    # Izumi
    p = []
    el = Ev()
    el.say(IZUMI, ["Welcome to the Black Raven. You look like you've come",
                   "a long way on an empty stomach."])
    el.say(IZUMI, ["If you've no coin, I've no bed. Sorry, love.",
                   "Times are what they are."])
    p.append(pg(el, char=IZUMI.char[0], index=IZUMI.char[1], direction=2, priority=1))
    el = Ev()
    el.say(IZUMI, ["Tōdō sent you? Then you're either useful or pitiful.", "Which is it?"])
    el.say(KANTA, ["We need food and a place to sleep. We can't pay."], 'calm')
    el.balloon(0, 8)
    el.say(IZUMI, ["…No coin. But arms on you, and a back that can lift."])
    el.say(IZUMI, ["Tōdō's short on the fence tonight. The goblins have",
                   "been sniffing round the pens three nights running."])
    el.say(IZUMI, ["Stand the fence with him till midnight, and there's",
                   "stew, bread and a bed for the both of you. Deal?"])
    def deal(e):
        e.say(KANTA, ["Deal."], 'calm')
        e.say(IZUMI, ["Good. Eat something first; you look like death."])
        e.say(HANMA, ["(If only she knew.)"], 'smile')
        e.se('Item3')
        e.item(IT["Heiltrank"], 2)
        e.notice(["Received 2 Heiltrank. \"For the fence,\" Izumi says."])
        e.quest_done(Q_ROOF)
        e.quest_new(Q_WATCH)
        e.switch(S_DEAL)
        e.rest_point(INN, 13, 7, 2)
    el.choices(["Deal", "Not yet"], [deal, lambda e: e.say(IZUMI, ["Suit yourself. Offer stands till dark."])],
               cancel=1)
    p.append(pg(el, sw=S_ARRIVED, char=IZUMI.char[0], index=IZUMI.char[1], direction=2, priority=1))
    # after the deal: free beds
    el = Ev()
    el.say(IZUMI, ["Beds are upstairs, stew's on the fire. Rest when you like."])
    def sleep(e):
        e.say(IZUMI, ["Sleep well, the both of you."])
        e.common(CE["Inn Sleep"])
    el.choices(["Rest until morning", "Not now"], [sleep, None], cancel=1)
    p.append(pg(el, sw=S_DEAL, char=IZUMI.char[0], index=IZUMI.char[1], direction=2, priority=1))
    mb.add("Hanamura Izumi", 14, 9, p)

    # the night after the raid: supper, sleep, and Tōdō in the morning
    el = Ev()
    el.bgs('Fire1', 30)
    el.wait(30)
    el.fadein()
    el.say(IZUMI, ["There they are. Sit, sit. Stew, bread, and don't",
                   "argue about the size of the bowls."])
    el.narrate(["The stew is thin and hot and better than anything you",
                "can remember. Which, you realize, is nothing at all."])
    el.say(HANMA, ["Eat slowly, my Lord. This body has never eaten."], 'calm')
    el.common(CE["Inn Sleep"])
    el.wait(30)
    el.say(TODO, ["Up, you two. Elder Okuda wants you. Big house at the",
                  "north end of the village."])
    el.say(TODO, ["And Natsu's been at my door since dawn about her pigs."])
    el.quest_new(Q_GOBLINS)
    el.switch(S_SUMMONED)
    mb.autorun("Morning", el, cond_switch=S_RAID_DONE)

    # Sagara the merchant (after the tower)
    el = Ev()
    el.say(SAGARA, ["You're the two who cleared the watchtower? Sagara",
                    "Takumi, trader. Salt, needles, nails, news."])
    el.say(SAGARA, ["I'm bound for Eisfurt, two days east on the Oststraße.",
                    "Deserters on that road now, and worse. I need guards."])
    el.say(SAGARA, ["One Goldkrone for the trip. Half now, half at the ford."])
    def hire(e):
        e.say(KANTA, ["We'll take it."], 'calm')
        e.say(HANMA, ["Eisfurt is east. Wachtburg is east of Eisfurt, if my",
                      "memory's any good. The Guild, the feather: it fits."], 'calm')
        e.se('Coin')
        e.gold(50)
        e.notice(["Received \\MONEY[50] (half the fee)."])
        e.quest_new(Q_EAST)
        e.switch(S_EAST)
    el.choices(["Take the job", "Not yet"], [hire, lambda e: e.say(SAGARA, ["I leave when I find guards. Don't take long."])],
               cancel=1)
    el2 = Ev().say(SAGARA, ["When you're ready, meet me at the south gate.", "I'll be the one with the mule."])
    mb.add("Sagara Takumi", 7, 7, [pg(None, priority=0),
                                   pg(el, sw=S_REWARD, char=SAGARA.char[0], index=SAGARA.char[1], direction=2,
                                      priority=1),
                                   pg(el2, sw=S_EAST, char=SAGARA.char[0], index=SAGARA.char[1], direction=2,
                                      priority=1)])
    # patrons
    el = Ev().say(npc_speaker("Carter Shūji", "People3", 4),
                  ["Road east's bad. Deserters from the Wall, they say.",
                   "Men who ran from the north, robbing whoever's left."])
    mb.npc("Carter Shūji", 11, 7, ("People3", 4), el, direction=4)
    for x, y in [(3, 8), (4, 8), (5, 8)]:
        el = Ev().text(["The stairs up to the rooms."])
        mb.add("Stairs", x, y, [pg(el, trigger=0, priority=0)])
    mb.light('hearth', 9, 2)
    return mb

# ---------------------------------------------------------------------------
# 7  Haus Okuda  (sample 109)
# ---------------------------------------------------------------------------
def elder():
    mb = MapBuild(ELDER, NAMES[ELDER], 109, display=NAMES[ELDER])
    mb.props(note="<Area Name: Haus Okuda>\n<No Rank HUD>", bgm=('Town3', 55))
    el = Ev().se('Move1', 60).transfer(RABENAU, 23, 5, 2, 0)
    mb.add("Exit", 5, 12, [pg(el, trigger=1, priority=0)])
    p = []
    el = Ev().say(OKUDA, ["Travelers? Welcome to Rabenau. We have little,",
                          "but you're welcome to what there is."])
    p.append(pg(el, char=OKUDA.char[0], index=OKUDA.char[1], direction=2, priority=1))
    el = Ev()
    el.say(OKUDA, ["Sit, sit. Tōdō tells me you stood the fence for us last",
                   "night. Rabenau thanks you. And Rabenau is poor, so",
                   "thanks is most of what it has."])
    el.say(OKUDA, ["The goblins come from the south, from the Rabenholz.",
                   "There's an old watchtower in that forest, from the days",
                   "when the king's riders still patrolled this road."])
    el.say(OKUDA, ["We think they've made a nest of it. We sent to the",
                   "Guild in Wachtburg twice. Nobody came. Every sword in",
                   "Hohenwacht is going north to the Wall."])
    el.say(OKUDA, ["If you would clear that tower, we can pay five silver.",
                   "And your board, for as long as you stay."])
    el.say(KANTA, ["We'll look."], 'calm')
    el.say(HANMA, ["My Lord—"], 'stern')
    el.say(HANMA, ["…Goblins. Fine. But if there's something worse in that",
                   "tower than goblins, we leave. We don't die for five",
                   "silver."], 'stern')
    el.say(KANTA, ["Agreed."], 'calm')
    el.say(OKUDA, ["Sensible. Take this: Rabenau's old raven charm.",
                   "It's kept worse things than goblins off this roof."])
    el.se('Item3')
    el.armor(AR["Rabenamulett"], 1)
    el.notice(["Received the Rabenamulett (WIS +5, MAG +5).", "Equip it on Hanma: Menu, Equip."])
    el.quest_desc(Q_GOBLINS, "Clear the old watchtower in the Rabenholz, south of Rabenau. Elder Okuda pays "
                             "5 sl and board. Hanma's condition: if it's worse than goblins, you leave.")
    el.switch(S_QUEST)
    p.append(pg(el, sw=S_SUMMONED, char=OKUDA.char[0], index=OKUDA.char[1], direction=2, priority=1))
    el = Ev().say(OKUDA, ["The Rabenholz path starts at the south gate.", "Come back safe, both of you."])
    p.append(pg(el, sw=S_QUEST, char=OKUDA.char[0], index=OKUDA.char[1], direction=2, priority=1))
    el = Ev()
    el.say(OKUDA, ["You're back! And the tower…? Krummzahn! That old",
                   "devil. Tōdō will sleep tonight, for once."])
    el.say(KANTA, ["He said the north forest had gone bad. Burning trees,",
                   "black birds. Things that walk wrong."], 'calm')
    el.text(["Kanta sets the black feather on the table."])
    el.balloon(0, 1)
    el.say(OKUDA, ["…Akatsuki keep us."])
    el.say(HANMA, ["Miasma, elder. Demon-taint. That feather came from",
                   "somewhere demons walk."], 'stern')
    el.say(OKUDA, ["Then it's worse than we feared, and the Guild must hear",
                   "of it. I'll write to them. Will you carry the letter?",
                   "Wachtburg is east, past Eisfurt on the Oststraße."])
    el.say(OKUDA, ["And your pay, as promised. Five silver."])
    el.se('Coin')
    el.gold(50)
    el.item(IT["Brief an die Gilde"], 1)
    el.notice(["Received \\MONEY[50] and the Brief an die Gilde."])
    el.quest_done(Q_GOBLINS)
    el.switch(S_REWARD)
    el.say(OKUDA, ["Hanamura says a merchant's been asking for guards to",
                   "Eisfurt. Sagara. He's at the Black Raven."])
    p.append(pg(el, sw=S_BOSS, char=OKUDA.char[0], index=OKUDA.char[1], direction=2, priority=1))
    el = Ev().say(OKUDA, ["Safe roads, Kanta. And you, Hanma-dono."])
    el.say(HANMA, ["…Dono. Nobody's called me that in a while."], 'smile')
    p.append(pg(el, sw=S_REWARD, char=OKUDA.char[0], index=OKUDA.char[1], direction=2, priority=1))
    mb.add("Okuda Noboru", 10, 9, p)
    return mb

# ---------------------------------------------------------------------------
# 8  Kräuterstube  (sample 110)
# ---------------------------------------------------------------------------
def herbs():
    mb = MapBuild(HERBS, NAMES[HERBS], 110, display=NAMES[HERBS])
    mb.props(note="<Area Name: Kräuterstube>\n<No Rank HUD>", bgm=('Town3', 55))
    el = Ev().se('Move1', 60).transfer(RABENAU, 10, 9, 2, 0)
    mb.add("Exit", 8, 10, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(SAEKI, ["Herbs, draughts, salts. If it grows between here and",
                   "the Wall, I can brew something from it."])
    el.say(SAEKI, ["I buy mushrooms, too. The Rabenholz ones. Just don't",
                   "eat any on the way here, please."])
    el.shop([('item', IT["Heiltrank"]), ('item', IT["Kräuterbündel"]), ('item', IT["Gegengift"]),
             ('item', IT["Manatrank"]), ('item', IT["Riechsalz"])])
    mb.add("Saeki Chiaki", 8, 4, [pg(el, char=SAEKI.char[0], index=SAEKI.char[1], direction=2, priority=1)])
    return mb

# ---------------------------------------------------------------------------
# 9  Schmiede Matsuda  (sample 121)
# ---------------------------------------------------------------------------
def smithy():
    mb = MapBuild(SMITHY, NAMES[SMITHY], 121, display=NAMES[SMITHY])
    mb.props(note="<Area Name: Schmiede Matsuda>\n<No Rank HUD>", bgm=('Town3', 55), bgs=('Fire2', 25))
    el = Ev().se('Move1', 60).transfer(RABENAU, 20, 15, 2, 0)
    mb.add("Exit", 8, 10, [pg(el, trigger=1, priority=0)])
    seen = SW('C1: Smith Saw Armor')
    el = Ev()
    el.say(MATSUDA, ["Matsuda's forge. Nails, hinges, plough-shares, and a bit",
                     "of armor for anyone fool enough to need it."])
    el.if_switch(seen, False,
                 lambda b: (b.balloon(0, 1),
                            b.say(MATSUDA, ["…Hold on. That plate of yours. Let me look."]),
                            b.say(MATSUDA, ["That's no smith's work I know. The silver's too clean,",
                                            "no hammer-marks at all. Like it was grown, not beaten."]),
                            b.say(MATSUDA, ["If it's what I think it is, it's worth more than this",
                                            "village. Have it appraised at the Guild in Wachtburg.",
                                            "They've a crystal for it."]),
                            b.switch(seen)))
    el.shop([('armor', AR["Lederkappe"]), ('armor', AR["Lederarmschienen"]), ('armor', AR["Wolfsfellweste"]),
             ('armor', AR["Filzmantel"])])
    mb.add("Matsuda Daichi", 9, 4, [pg(el, char=MATSUDA.char[0], index=MATSUDA.char[1], direction=2, priority=1)])
    return mb

# ---------------------------------------------------------------------------
# 10  Hof am Feldrain  (sample 116): Natsu's family
# ---------------------------------------------------------------------------
def farm():
    mb = MapBuild(FARM, NAMES[FARM], 116, display=NAMES[FARM])
    mb.props(note="<Area Name: Hof am Feldrain>\n<No Rank HUD>", bgm=('Town3', 55))
    el = Ev().se('Move1', 60).transfer(RABENAU, 7, 9, 2, 0)
    mb.add("Exit", 8, 10, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.if_switch(S_PIGDONE, True,
                 lambda b: b.say(MOTHER, ["Natsu hasn't stopped talking about you. Thank you,",
                                          "truly. Those pigs are half our winter."]),
                 lambda b: b.say(MOTHER, ["Natsu's pigs are half our winter. If the goblins",
                                          "took them… well. We'd manage. We always do."]))
    mb.npc("Kazama Hana", 7, 6, MOTHER, el, direction=2)
    return mb

# ---------------------------------------------------------------------------
# 11  Rabenholz  (sample 225)
# ---------------------------------------------------------------------------
def WOOD_ENC():
    return [(TR["Goblins x2"], 8, ()), (TR["Wolf"], 6, ()), (TR["Crows x3"], 4, ()), (TR["Rotcaps x2"], 5, ()),
            (TR["Wolf & Goblin"], 5, ())]

def DEEP_ENC():
    return [(TR["Goblins x3"], 6, ()), (TR["Goblins & Thrower"], 6, ()), (TR["Wolves x2"], 5, ()),
            (TR["Rotcap & Goblin"], 5, ()), (TR["Goblin & Thrower"], 6, ())]

def rabenholz():
    mb = MapBuild(RABENHOLZ, NAMES[RABENHOLZ], 225, display=NAMES[RABENHOLZ])
    mb.props(note="<Rank: F>\n<Area Name: Rabenholz>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Dungeon1', 60), battleback=('Grassland', 'Forest'), encounters=WOOD_ENC(), steps=26)
    el = Ev().se('Move1', 60).transfer(RABENAU, 13, 27, 8, 0)
    mb.add("To Rabenau", 15, 27, [pg(el, trigger=1, priority=0)])
    for y in (6, 7, 8):
        el = Ev().se('Move1', 60).transfer(DEEPWOOD, 3, 5, 6, 0)
        mb.add("Deeper", 28, y, [pg(el, trigger=1, priority=0)])
    first = SW('C1: Entered Wood')
    el = Ev()
    el.say(HANMA, ["Goblin sign everywhere. Tracks, bones, a broken spear.",
                   "They've been here a while."], 'stern')
    el.say(HANMA, ["The tower should be deeper in, east. Watch the ferns,",
                   "my Lord. Goblins love an ambush."], 'command')
    el.switch(first)
    mb.autorun("Enter", el)
    piglet(mb, "Piglet (Rabenholz)", 22, 13, SW('C1: Piglet 2'))
    chest(mb, "Chest", 5, 18, lambda e: e.item(IT["Heiltrank"], 2), "Found 2 Heiltrank.")
    chest(mb, "Chest", 10, 10, lambda e: (e.gold(25)), "Found \\MONEY[25] in a goblin's stash.")
    return mb

# ---------------------------------------------------------------------------
# 12  Tiefes Rabenholz  (sample 226)
# ---------------------------------------------------------------------------
def deepwood():
    mb = MapBuild(DEEPWOOD, NAMES[DEEPWOOD], 226, display=NAMES[DEEPWOOD])
    mb.props(note="<Rank: F>\n<Area Name: Tiefes Rabenholz>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Dungeon1', 60), battleback=('Grassland', 'Forest'), encounters=DEEP_ENC(), steps=24)
    for y in (4, 5, 6):
        el = Ev().se('Move1', 60).transfer(RABENHOLZ, 27, 7, 4, 0)
        mb.add("Back", 2, y, [pg(el, trigger=1, priority=0)])
    el = Ev().se('Move1', 60).transfer(RUIN, 12, 21, 8, 0)
    mb.add("To the Watchtower", 15, 7, [pg(el, trigger=1, priority=0)])
    # sentries at the gap
    done = SW('C1: Sentries')
    el = Ev()
    el.balloon(0, 1)
    el.say(Speaker("Goblin Sentry", "", 0), ["Soft-skins! Soft-skins at the gap!"])
    el.battle(TR["Goblin & Thrower"], can_escape=False, can_lose=False)
    el.switch(done)
    mb.add("Sentry", 15, 6, [pg(el, char=GOBLIN_CHAR[0], index=GOBLIN_CHAR[1], direction=2, trigger=2, priority=1),
                             pg(None, sw=done, priority=0)])
    piglet(mb, "Piglet (deep wood)", 3, 18, SW('C1: Piglet 3'))
    chest(mb, "Chest", 24, 10, lambda e: e.item(IT["Manatrank"], 1), "Found a Manatrank.")
    chest(mb, "Chest", 8, 27, lambda e: e.armor(AR["Lederkappe"], 1), "Found a Lederkappe.")
    return mb

# ---------------------------------------------------------------------------
# 13  Alter Wachturm  (sample 203)
# ---------------------------------------------------------------------------
def ruin():
    mb = MapBuild(RUIN, NAMES[RUIN], 203, display=NAMES[RUIN])
    mb.props(note="<Rank: F>\n<Area Name: Alter Wachturm>\n<lighting: Outside>",
             bgm=('Dungeon3', 60), battleback=('Stone1', 'Ruins1'),
             encounters=[(TR["Goblins x2"], 5, ()), (TR["Goblin & Thrower"], 5, ())], steps=30)
    el = Ev().se('Move1', 60).transfer(DEEPWOOD, 15, 6, 8, 0)
    mb.add("Back to the wood", 12, 22, [pg(el, trigger=1, priority=0)])
    # campfire: rest point
    el = Ev()
    el.text(["A goblin campfire, still warm. The raiders cooked",
             "something here that you'd rather not identify."])
    def rest(e):
        e.fadeout()
        e.recover_all()
        e.rest_point(RUIN, 15, 20, 8)
        e.wait(40)
        e.fadein()
        e.text(["You rest by the embers. (HP and MP restored. If you fall,", "you'll wake here.)"])
    el.choices(["Rest here", "Move on"], [rest, None], cancel=1)
    mb.add("Campfire", 16, 20, [pg(el, char='!Other2', index=3, direction=2, trigger=0, priority=1, step_anime=True)])
    # guards on the stairs
    done = SW('C1: Stair Guards')
    el = Ev()
    el.say(Speaker("Goblin", "", 0), ["The chief said nobody comes up! NOBODY!"])
    el.battle(TR["Goblins & Thrower"], can_escape=False, can_lose=False)
    el.switch(done)
    for x in (11, 12, 13):
        mid = x == 12
        mb.add("Stair Guard", x, 14, [pg(el, char=GOBLIN_CHAR[0] if mid else '', index=GOBLIN_CHAR[1], direction=2,
                                         trigger=2 if mid else 1, priority=1 if mid else 0),
                                      pg(None, sw=done, priority=0)])
    mb.door(12, 5, TOWERTOP, 3, 7, 6, sheet='', name="Tower Door")
    chest(mb, "Chest", 5, 4, lambda e: e.item(IT["Heiltrank"], 3), "Found 3 Heiltrank.")
    chest(mb, "Chest", 19, 5, lambda e: (e.gold(40), e.item(IT["Manastein (F)"], 2)),
          "Found \\MONEY[40] and 2 Manastein (F).")
    return mb

# ---------------------------------------------------------------------------
# 14  Turmkrone  (sample 206): Krummzahn
# ---------------------------------------------------------------------------
def towertop():
    mb = MapBuild(TOWERTOP, NAMES[TOWERTOP], 206, display=NAMES[TOWERTOP])
    mb.props(note="<Rank: F>\n<Area Name: Turmkrone>", bgm=('Dungeon3', 60), battleback=('Stone1', 'Ruins1'))
    el = Ev().se('Move1', 60).transfer(RUIN, 12, 6, 2, 0)
    mb.add("Down", 2, 7, [pg(el, trigger=1, priority=0)])
    wolf = mb.add("Grauzahn", 10, 7, [pg(None, char='Nature', index=0, direction=4, priority=1, step_anime=True),
                                      pg(None, sw=S_BOSS, priority=0)])
    el = Ev()
    el.balloon(0, 5)
    el.say(KRUMM, ["Soft-skins! In Krummzahn's tower!"])
    el.say(HANMA, ["It talks. Badly."], 'smile')
    el.say(KANTA, ["Why are you raiding Rabenau?"], 'calm')
    el.say(KRUMM, ["Rabenau has pigs! Krummzahn's clan was hungry!"])
    el.say(KRUMM, ["North forest is bad now. Burning trees. Black birds.",
                   "Things that walk wrong. Krummzahn not stay there!",
                   "Krummzahn takes THIS forest!"])
    el.say(HANMA, ["…Things that walk wrong."], 'stern')
    el.say(KANTA, ["Leave Rabenau alone. Take your clan and go."], 'fierce')
    el.say(KRUMM, ["Krummzahn goes NOWHERE! Grauzahn! EAT!"])
    el.se('Wolf')
    el.battle(TR["Krummzahn"], can_escape=False, can_lose=False)
    el.text(["The chieftain crumples against the brazier. Grauzahn",
             "whimpers, and bolts down the stairs into the dark."])
    el.switch(S_BOSS)
    el.text(["Among the chief's things, wrapped in a rag like a charm:",
             "a raven feather, black and brittle, stinking of ash."])
    el.se('Darkness1', 70)
    el.say(HANMA, ["Don't touch it bare-handed. That's miasma, my Lord.",
                   "Demon-taint."], 'stern')
    el.say(HANMA, ["This came from somewhere demons walk. The goblins",
                   "weren't raiding for sport. They were running."], 'stern')
    el.say(KANTA, ["From what?"], 'calm')
    el.say(HANMA, ["From the north. From what's coming out of it."], 'stern')
    el.item(IT["Schwarze Rabenfeder"], 1)
    el.notice(["Received the Schwarze Rabenfeder."])
    el.quest_desc(Q_GOBLINS, "Krummzahn is dead, his clan scattered. He carried a raven feather black with miasma, "
                             "and said the north forest had gone bad. Report to Elder Okuda in Rabenau.")
    mb.add("Krummzahn", 9, 6, [pg(el, char=KRUMM.char[0], index=KRUMM.char[1], direction=4, trigger=2, priority=1),
                               pg(None, sw=S_BOSS, priority=0)])
    chest(mb, "Krummzahn's Hoard", 12, 5, lambda e: (e.gold(60), e.item(IT["Heiltrank"], 2)),
          "Krummzahn's hoard: \\MONEY[60] and 2 Heiltrank.")
    mb.light('brazier', 9, 5)
    return mb
