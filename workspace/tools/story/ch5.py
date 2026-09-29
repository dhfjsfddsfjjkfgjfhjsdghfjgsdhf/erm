"""Chapter 5: Weißenfels. The Grauklamm, the royal camp, the lower city in the snow, the old aqueduct, the forge
of empty armors (Falin's first memory; Mariko and Aya) and the dragon hall: the Iron Prince, Rin's brother.

The maps are generated (tools/mapgen.py, story/terrain.py): the MZ sample maps are not part of the workspace."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story import foes
from story.ids import *
from story.ch1 import chest
from story.ch2 import camp_fire
from story.cast import *
from story.act2 import S_FALIN
from story.ch4 import Q_WF, S_MARCH, S_C4_END
from story import terrain as T
from story.terrain import Gen, OUT, DUN, INS, auto

KI = foes.KEY
FI = foes.ITEMS
FA = foes.ARMORS
FW = foes.WEAPONS
RIN_ID = 5

SAKI_CAMP = npc_speaker("Yukimura Saki", "People2", 3)
MARIKO = npc_speaker("Nishiki Mariko", "People4", 1)
AYA = npc_speaker("Nishiki Aya", "People1", 1)
FOREMAN = npc_speaker("Vorarbeiter Kuroda", "People2", 4)
QM5 = npc_speaker("Quartiermeister", "People3", 6)
RIDER = npc_speaker("Melder", "People3", 7)
SHIRANUI_S = npc_speaker("Shiranui", "", 0)
PRINZ = npc_speaker("Der Eiserne Prinz", "", 0)

# ----------------------------------------------------------------------- quests
Q_MA = Quest(21, "Mariko und Aya", "Yukimura Saki", "Weißenfels",
             "Nishiki Eiji sold the Wall to buy back his wife and daughter. They are alive, working in the forge "
             "the Host built under Weißenfels. Saki asks you to bring them home: it's the least the Wall owes him.",
             "Find the forge under the citadel.")
Q_CHAIN = Quest(22, "Die Kettenkolonne", "Asahina Rin", "Weißenfels, Unterstadt",
                "Workers in chains haul coal from the lower city to the forge. Rin wants every one of her brother's "
                "people back. Optional.",
                "The coal road in the lower city.")

# ----------------------------------------------------------------------- switches / variables
S_C5 = SW('C5: In the Grauklamm')
S_WYVERNS = SW('C5: Wyverns Beaten')
S_THRALLS = SW('C5: Thralls Unmasked')
S_CAMP = SW('C5: At the Camp')
S_COUNCIL = SW('C5: Council Held')
S_FIRE = SW('C5: Fire Talk')
S_ASSAULT = SW('C5: The Assault')
S_IN_CITY = SW('C5: In the Lower City')
S_CHAIN = SW('C5: Chain Gang Freed')
S_SLUICE1 = SW('C5: West Sluice')
S_SLUICE2 = SW('C5: East Sluice')
S_WATERGATE = SW('C5: Water Gate Open')
S_FORGE = SW('C5: In the Forge')
S_MEMORY = SW('C5: Falin Remembers')
S_SMITH = SW('C5: Ash Smith Down')
S_FREED = SW('C5: Workers Freed')
S_GATE = SW('C5: Citadel Gate Open')
S_PRINZ = SW('C5: Iron Prince Down')
S_C5_END = SW('C5: Chapter Done')

CITY_ENC = lambda: [(TR["Ghule & Knecht"], 6, ()), (TR["Leere Hüllen x2"], 5, ()), (TR["Vampirknechte x2"], 5, ()),
                    (TR["Hülle & Koloss"], 2, ())]
KLAMM_ENC = lambda: [(TR["Wyvern"], 6, ()), (TR["Gargyl & Wyvern"], 4, ()), (TR["Vampirknechte x2"], 3, ()),
                     (TR["Wyverns x2"], 2, ())]

INFO = {}          # map id -> named spots, for the other chapters (entries, exits)


def build():
    return [grauklamm(), heerlager(), unterstadt(), aquaedukt(), huellenschmiede(), drachenhalle()]


def edge_exit(mb, cells, to_map, tx, ty, d, name='Exit', cond=None):
    for (x, y) in cells:
        el = Ev().se('Move1', 60).transfer(to_map, tx, ty, d, 0)
        p = pg(el, trigger=1, priority=0)
        if cond:
            p['conditions'].update(cond)
        mb.add(name, x, y, [p])


# ---------------------------------------------------------------------------
# 75  Grauklamm: the snow canyon between the Wall and Weißenfels
# ---------------------------------------------------------------------------
def gen_grauklamm():
    g = Gen(36, 46, 2, seed=75)
    pts = [(30, 45), (29, 39), (23, 34), (15, 29), (10, 23), (14, 16), (22, 11), (20, 5), (17, 1), (17, 0)]
    pockets = g.blob(6, 25, 2.8, seed=3) | g.blob(27, 11, 2.6, seed=4)     # side pockets: camp, chests
    floor, road = T.canyon(g, pts, 8, T.SNOW, wall_h=3, rim=4, extra=pockets)
    g.keep_clear |= {(6, 24), (27, 10), (5, 23), (7, 25)}
    T.dress(g, floor, T.SNOW, trees=0.08, rocks=0.03, bushes=0.06, tufts=0.04)
    g.finish()
    return g, floor


def grauklamm():
    g, floor = gen_grauklamm()
    entry = GRAUKLAMM_ENTRY
    R = T.reach_check(g, entry, [(17, 0)], 'Grauklamm')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    top = [(x, 0) for x in range(g.w) if (x, 0) in R and (x, 0) in floor and (x, 1) in R]
    INFO[GRAUKLAMM] = {'entry': entry, 'top': (17, 1)}
    mb = MapBuild(GRAUKLAMM, NAMES[GRAUKLAMM], g.m, display=NAMES[GRAUKLAMM])
    mb.props(note="<Rank: D>\n<Area Name: Grauklamm>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field2', 60), bgs=('Wind3', 45), battleback=('Snowfield', 'Cliff'), encounters=KLAMM_ENC(),
             steps=30, weather='snow 5')
    # --- arrival (the march from the Wallfeste)
    el = Ev()
    el.card("Kapitel 5", "Weißenfels", 220)
    el.wait(10)
    el.narrate(["Two thousand of the Crown's soldiers wind into the",
                "Grauklamm: a gorge of grey rock and old snow that runs",
                "west from the Wall to the valley of Weißenfels."])
    el.narrate(["Rin rides at the head of the column with her knight",
                "captain. The three of you walk with the rearguard, where",
                "nobody minds a ghost."])
    el.say(SOMA, ["Takamura Sōma, captain of Her Highness's knights. You're",
                  "the Guild strays the Marshal lent us."])
    el.say(KANTA, ["Kanta. Hanma. Falin."], 'calm')
    el.say(SOMA, ["Hm. Her Highness trusts you. I trust Her Highness. Keep",
                  "up, keep your eyes on the ridges, and if something comes",
                  "down on the column, kill it."])
    el.say(HANMA, ["A pleasant man. I had forty like him once."], 'smile')
    el.say(FALIN, ["…Weißenfels is at the end of this. I walked out of it,",
                   "once. I never walked back."], 'calm')
    el.quest_desc(Q_WF, "The army marches west through the Grauklamm. The royal camp is at its far end, in sight "
                        "of Weißenfels.")
    el.switch(S_C5)
    el.rest_point(GRAUKLAMM, entry[0], entry[1], 8)
    mb.autorun("March", el)
    # --- back to the Wallfeste (bottom edge)
    for x in range(g.w):
        if (x, g.h - 1) in R and (x, g.h - 1) in floor:
            mb.add("To the Wall", x, g.h - 1, [pg(Ev().text(["The Grauklamm runs back east to the Wallfeste. The army",
                                                             "went the other way."]), trigger=1, priority=0)])
    # --- north end: the camp
    edge_exit(mb, top, HEERLAGER, 20, 28, 8, 'To the Camp')
    # --- soldiers along the road
    s1 = npc_speaker("Soldat", "People3", 6)
    s2 = npc_speaker("Soldatin", "People4", 5)
    for (who, near, lines) in [(s1, (26, 36), ["My boots are full of the Grauklamm. My brother's are",
                                               "full of Weißenfels. Six years. I'll bring them home."]),
                               (s2, (13, 19), ["They say the forge in the city never goes out. You can",
                                               "see its glow on the clouds at night. Like a wound."])]:
        c = sp(near)
        mb.npc("Soldier", c[0], c[1], who, Ev().say(who, lines), direction=2)
    # --- the wyverns dive on the column
    wy_row = 31
    wy_cells = [(x, wy_row) for x in range(g.w) if (x, wy_row) in R and (x, wy_row) in floor]
    victim = sp((18, 29))
    fallen = mb.add("Fallen Soldier", victim[0], victim[1],
                    [pg(None, priority=0),
                     pg(Ev().say(npc_speaker("Verwundeter", "People3", 7),
                                 ["It took Hayashi. Picked him up like a lamb. Gods…"]),
                        sw=S_WYVERNS, char='Damage2', index=1, direction=2, priority=1)])
    def dive(e):
        e.se('Monster4', 90, 110)
        e.shake(4, 6, 20)
        e.text(["Shrieks from the ridge. Two shapes fold their wings and",
                "drop onto the column like stones: long necks, barbed",
                "tails, and the stink of a carrion nest."])
        e.say(FALIN, ["Wyverns! Get the wounded behind me!"], 'fierce')
        e.say(HANMA, ["Rank D, my Lord, the same as us now. Mind the tails:",
                      "they carry poison."], 'command')
        e.battle(TR["Wyverns x2"])
        e.switch(S_WYVERNS)
        e.wait(20)
        e.say(SOMA, ["…That was quick work. Hayashi's gone. Two more hurt."])
        e.say(HANMA, ["Wyverns don't hunt this far south in pairs. Something",
                      "on the other end of this gorge is sending its dogs."], 'stern')
        e.say(SOMA, ["Then we'll go and meet it. Column, march!"])
        e.item(FI["Elixier"], 1)
        e.notice(["A grateful sergeant presses an Elixier on you."])
    for c in wy_cells:
        mb.add("Wyvern Dive", c[0], c[1], [pg(None, priority=0),
                                          pg(Ev().if_switch(S_WYVERNS, False, dive), sw=S_C5, trigger=1, priority=0)])
    # --- the "refugees" in the snow (vampire thralls)
    rc = sp((12, 21))
    thr = []
    for (dx, sheet, idx) in [(-1, 'People1', 4), (0, 'People2', 3), (1, 'People1', 5)]:
        c = sp((rc[0] + dx, rc[1]), avoid=[(e['x'], e['y']) for e in mb.m['events'] if e])
        thr.append(mb.add("Refugee", c[0], c[1], [pg(None, priority=0),
                                                  pg(None, sw=S_C5, char=sheet, index=idx, direction=2, priority=1,
                                                     step_anime=False),
                                                  pg(None, sw=S_THRALLS, priority=0)]))
    def thralls(e):
        e.text(["Three people huddle in the snow at the side of the road,",
                "in the blue coats of Weißenfels. They don't look up."])
        e.say(npc_speaker("Flüchtling", "People2", 3), ["…Help us. We got out. We got out of the city."])
        e.say(HANMA, ["My Lord. Look at the snow around them."], 'stern')
        e.say(KANTA, ["It isn't melting."], 'calm')
        e.say(HANMA, ["And there's no breath in the cold air. Whatever they",
                      "were, they're thralls now. Blood-servants."], 'stern')
        e.se('Monster2', 90, 120)
        e.flash((200, 40, 40, 120), 20)
        e.text(["The three stand up together, too smoothly. Their eyes",
                "have gone the colour of old blood."])
        e.say(FALIN, ["They're wearing Weißenfels blue. Their own blue."], 'hurt')
        e.battle(TR["Vampirknechte x2"])
        e.switch(S_THRALLS)
        e.wait(20)
        e.say(FALIN, ["…Someone in that city is making thralls out of the",
                      "people who stayed."], 'fierce')
        e.say(HANMA, ["And sends them out along the road to meet the ones",
                      "who come looking. We should tell the princess."], 'stern')
    for eid in thr:
        mb.m['events'][eid]['pages'][1]['list'] = Ev().if_switch(S_THRALLS, False, thralls).done()
    # --- rest and loot
    fire = sp((6, 24))
    rest = sp((fire[0], fire[1] + 1), avoid=[fire])
    camp_fire(mb, fire[0], fire[1], GRAUKLAMM, rest[0], rest[1], 8,
              ["A soldiers' fire pit, scraped out of the snow in the lee", "of a rock."])
    c1 = sp((27, 10))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Elixier"], 1), e.gold(900)), "Found an Elixier and \\MONEY[900].")
    c2 = sp((5, 22), avoid=[fire, rest])
    chest(mb, "Chest", c2[0], c2[1], lambda e: e.armor(FA["Fellkapuze"], 1), "Found a Fellkapuze.")
    mb.follow_light('beam', entry[0], entry[1])
    return mb


# ---------------------------------------------------------------------------
# 76  Heerlager: the royal camp in sight of Weißenfels
# ---------------------------------------------------------------------------
def gen_heerlager():
    g = Gen(40, 32, 2, seed=76)
    g.paint(g.all(), OUT.SNOW)
    walk = g.blob(20, 16, 12.5, rough=0.18, seed=6) | g.rect(18, 26, 22, 31) | g.rect(18, 0, 22, 6)
    walk &= g.rect(1, 0, 38, 31)
    ground = T.frame(g, walk, T.SNOW, thick=3, trunk_h=2)
    # trampled paths: a cross through the camp
    path = g.line([(20, 31), (20, 18), (20, 3)], 2) | g.line([(8, 17), (32, 17)], 2)
    path &= ground
    g.paint(path, OUT.SNOW_DIRT)
    g.keep_clear |= g.grow(path, 1)
    # tents: two rows either side of the north road, the command tent (red) at the top of the road
    info = {'tents': []}
    for (x, y, red) in [(23, 10, True), (9, 13, False), (13, 13, False), (27, 14, False), (31, 14, False),
                        (9, 23, False), (13, 23, False), (25, 23, False), (29, 23, False)]:
        if T.tent(g, x, y, red=red):
            info['tents'].append((x + 1, y))
    # supply crates by the quartermaster, a banner line
    for (x, y) in [(31, 18), (32, 18), (31, 19), (33, 19), (8, 18), (8, 19)]:
        g.stamp(x, y, [(0, 0, OUT.CRATES[(x + y) % 4])])
    for (x, y) in [(22, 15), (26, 11), (17, 21), (24, 21)]:
        g.stamp(x, y, [(0, 0, OUT.BARREL)])
    # a banner pole line along the north road
    for y in (5, 8):
        for x in (17, 23):
            g.stamp(x, y, OUT.LAMP)
    T.dress(g, ground - g.grow(path, 2) - g.rect(8, 9, 32, 25), T.SNOW, trees=0.08, rocks=0.02, bushes=0.04, tufts=0.03)
    g.finish()
    return g, info


def heerlager():
    g, info = gen_heerlager()
    R = T.reach_check(g, (20, 28), [(20, 1)], 'Heerlager')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    INFO[HEERLAGER] = {'entry': (20, 28), 'north': (20, 2)}
    mb = MapBuild(HEERLAGER, NAMES[HEERLAGER], g.m, display=NAMES[HEERLAGER])
    mb.props(note="<Area Name: Heerlager>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Castle2', 55), bgs=('Wind1', 30), weather='snow 3')
    # south: back into the Grauklamm
    for x in range(18, 23):
        el = Ev().se('Move1', 60).transfer(GRAUKLAMM, 17, 1, 2, 0)
        mb.add("To the Grauklamm", x, 31, [pg(el, trigger=1, priority=0)])
    # north road: shut until the assault
    def north(e):
        e.if_switch(S_GATE, True,
                    lambda b: (b.se('Move1', 60), b.transfer(WF_UNTERSTADT, 23, 37, 8, 0)),
                    lambda b: b.say(ROYAL_GUARD, ["Nobody goes up the valley before the assault. Her",
                                                  "Highness's orders."]))
    for x in range(18, 23):
        mb.add("North Road", x, 0, [pg(Ev().if_switch(S_IN_CITY, True, lambda b: (b.se('Move1', 60),
                                                                                  b.transfer(WF_UNTERSTADT, 23, 37, 8, 0)),
                                                      north), trigger=1, priority=0)])
    # --- arrival
    el = Ev()
    el.wait(10)
    el.narrate(["The royal camp fills a white valley at the mouth of the",
                "Grauklamm. North, over the treeline: the walls of",
                "Weißenfels, black against the snow, and above them a"])
    el.narrate(["red smudge on the clouds where the forge burns.", "It never goes out, the soldiers say."])
    el.say(ROYAL_GUARD, ["Her Highness is at the red tent, up the road on the",
                         "right. She wants you there before the council starts."])
    el.quest_desc(Q_WF, "The royal camp. Rin holds a council at the red command tent, up the north road on the right.")
    el.switch(S_CAMP)
    el.rest_point(HEERLAGER, 20, 27, 8)
    mb.autorun("Camp", el, cond_switch=S_C5)
    # --- the council in front of the command tent (17..19, 11)
    rin = mb.add("Asahina Rin", 24, 11, [pg(None, char=RIN.char[0], index=RIN.char[1], direction=2, priority=1)])
    soma = mb.add("Takamura Sōma", 23, 12, [pg(None, char=SOMA.char[0], index=SOMA.char[1], direction=6, priority=1)])
    hik = mb.add("Mizushima Hikari", 25, 12, [pg(None, char=HIKARI.char[0], index=HIKARI.char[1], direction=4, priority=1)])
    def council(e):
        e.say(RIN, ["Good, you're here. Sōma, Hikari: the three I told you",
                    "about."])
        e.say(HIKARI, ["Mizushima Hikari, court battle-mage. So you're the",
                       "vessel. Hm. You look like a person."])
        e.say(KANTA, ["I get that a lot."], 'wry')
        e.say(RIN, ["Weißenfels. The lower city is the Host's now, full of",
                    "ghouls and thralls and empty armors. The citadel stands",
                    "on the rock above it behind one gate, and that gate is a",
                    "portcullis on a winch."])
        e.say(HIKARI, ["I found the old waterworks plans in the Wallfeste's",
                       "archive. An aqueduct runs from the north-west tower",
                       "down under the citadel. It fed the cisterns, before."])
        e.say(HIKARI, ["The forge is down there now. Its heat comes up the",
                       "old channels: you can see the steam from here. And the",
                       "winch house for the citadel gate sits right above it."])
        e.say(SOMA, ["Two thousand men can take the lower city and hold the",
                     "square. Two thousand men can't climb a citadel."])
        e.say(RIN, ["So the army goes in through the south breach and draws",
                    "the Host onto itself. You three slip away to the tower,",
                    "down the aqueduct, through the forge, and open my gate."])
        e.say(FALIN, ["And the people in the forge?"], 'calm')
        e.say(RIN, ["Are my brother's people. Every one of them comes out."])
        e.say(HANMA, ["And whatever holds the citadel, Highness?"], 'stern')
        e.say(RIN, ["…The scouts call it the Iron Prince. It sits in the",
                    "great hall where my brother died, in armor I would know",
                    "anywhere."])
        e.say(RIN, ["I'll be at the gate when it opens. Whatever is in that",
                    "hall, I'm going to look it in the face."])
        e.say(SOMA, ["The assault starts at the second bell, before dawn.",
                     "Eat. Sleep, if you can. The quartermaster has Wall stock",
                     "and some of the Crown's."])
        e.say(RIN, ["And the thralls on the road… yes, I heard. Sōma's",
                    "men will burn them. Everyone we can save, we save."])
        e.quest_desc(Q_WF, "The plan: the army storms the south breach at the second bell. The party slips away to "
                           "the north-west tower, follows the old aqueduct to the forge under the citadel, and opens "
                           "the citadel gate from the winch house. Sleep in the party's tent until the bell.")
        e.quest_new(Q_CHAIN)
        e.switch(S_COUNCIL)
    el = Ev().if_switch(S_COUNCIL, True,
                        lambda b: b.say(RIN, ["The second bell. Sleep if you can; I won't."]),
                        council)
    for eid in (rin, soma, hik):
        mb.m['events'][eid]['pages'][0]['list'] = el.done()
        mb.m['events'][eid]['pages'].append(pg(None, sw=S_ASSAULT, priority=0))
    # --- Saki (the Wall's healer came with the army): heal + the quest
    def saki(e):
        e.if_switch(S_COUNCIL, True, lambda b: b.if_script("!$gameSystem._ma_given", saki_quest,
                                                            lambda c: c.say(SAKI_CAMP, ["Mariko and Aya. The forge. Please."])),
                    lambda b: b.say(SAKI_CAMP, ["The Marshal sent me with the army. Somebody has to",
                                                "stitch them back together. Go see the princess."]))
        e.se('Heal3')
        e.recover_all()
    def saki_quest(e):
        e.say(SAKI_CAMP, ["Before you go in. Nishiki's wife and girl, Mariko and",
                          "Aya. If they're alive in that forge…"])
        e.say(SAKI_CAMP, ["He sold the Wall for them, and it turned him to brass.",
                          "Bring them out. It's the least the Wall owes him."])
        e.say(FALIN, ["We'll find them."], 'calm')
        e.quest_new(Q_MA)
        e.script("$gameSystem._ma_given = true;")
    c = sp((11, 18))
    saki_ev = Ev()
    saki(saki_ev)
    mb.npc("Yukimura Saki", c[0], c[1], SAKI_CAMP, saki_ev, direction=2)
    # --- quartermaster
    A, W, I = FA, FW, FI
    goods = [('item', IT["Großer Heiltrank"]), ('item', I["Elixier"]), ('item', I["Großes Elixier"]),
             ('item', I["Hoher Manatrank"]), ('item', I["Starkes Riechsalz"]), ('item', I["Allheilmittel"]),
             ('item', I["Große Lichtphiole"]), ('item', IT["Wärmetee"]),
             ('armor', A["Wallhelm"]), ('armor', A["Fellkapuze"]), ('armor', A["Wallschild"]),
             ('armor', A["Kriegeramulett"]), ('armor', A["Heilerstola"]), ('armor', A["Glutamulett"]),
             ('armor', A["Wachstiefel"]), ('armor', A["Brandschutzmantel"]),
             ('armor', A["Messingbrecherhelm"]), ('armor', A["Magierhut"]),
             ('weapon', W["Wallfäuste"]), ('weapon', W["Kriegsflegel"])]
    el = Ev().say(QM5, ["Crown stock and Wall stock. The Crown's is dearer and",
                        "prettier. Neither stops a vampire."])
    el.shop(goods)
    c = sp((30, 19))
    mb.npc("Quartermaster", c[0], c[1], QM5, el, direction=4)
    # --- soldiers
    for (sheet, idx, near, lines) in [('People3', 7, (24, 20), ["Second bell. I've been awake since the first."]),
                                      ('People4', 6, (14, 20), ["The breach is south. They'll be waiting. So will we."]),
                                      ('Actor3', 6, (23, 9), ["Royal guard. I was at Weißenfels six years ago. I ran.",
                                                              "Tonight I don't."])]:
        who = npc_speaker("Soldat", sheet, idx)
        c = sp(near)
        mb.npc("Soldier", c[0], c[1], who, Ev().say(who, lines), direction=2)
    # --- the fire: Falin and Hanma, Kanta and Falin
    fire = sp((27, 20))
    def talk(e):
        e.narrate(["The camp's fires burn low. Most of the soldiers are",
                   "asleep, or pretending."])
        e.say(HANMA, ["May I ask you something, Falin?"], 'calm')
        e.say(FALIN, ["You will anyway."], 'calm')
        e.say(HANMA, ["When you woke inside the armor. Was it warm, or cold?"], 'calm')
        e.say(FALIN, ["…Cold. And then warm, all at once, like a door opening.",
                      "Why?"], 'calm')
        e.say(HANMA, ["Because that is what my Lord's waking felt like, from",
                      "the other end of the thread. And because I have seen one",
                      "soul in a borrowed body before, in my war."], 'stern')
        e.say(FALIN, ["And?"], 'calm')
        e.say(HANMA, ["It frightened me then. I was a frightened woman, most of",
                      "my life, and I called it anger."], 'calm')
        e.say(FALIN, ["Do I frighten you?"], 'calm')
        e.say(HANMA, ["You? No. Whoever made the armor you woke in does."], 'stern')
        e.wait(30)
        e.say(FALIN, ["Kanta. You woke in a cave with nothing. I woke in the",
                      "snow with nothing. No mother, no village, no name but",
                      "the one we found."], 'calm')
        e.say(KANTA, ["Two people with no past."], 'calm')
        e.say(FALIN, ["Tomorrow I walk into the city I woke outside of. What if",
                      "somebody in there knows me?"], 'hurt')
        e.say(KANTA, ["Then you'll have a name with a story attached."], 'calm')
        e.say(FALIN, ["And if I don't like the story?"], 'calm')
        e.say(KANTA, ["Then you'll still have the name. You earned it on your",
                      "own. Six years in a gap in a wall."], 'wry')
        e.say(FALIN, ["…Hm."], 'smile')
        e.switch(S_FIRE)
    el = Ev()
    el.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_COUNCIL, S_FIRE), talk,
                 lambda b: b.text(["A camp fire. The soldiers make room for you."]))
    mb.add("Campfire", fire[0], fire[1], [pg(el, char='!Other2', index=3, direction=2, trigger=0, priority=1,
                                            step_anime=True)])
    # --- the party's tent: sleep until the second bell
    tent_door = info['tents'][1]
    def sleep(e):
        e.if_switch(S_COUNCIL, True,
                    lambda b: b.if_switch(S_FIRE, True, assault,
                                          lambda c: c.say(HANMA, ["Not yet, my Lord. Falin is at the fire. Go and sit",
                                                                  "with her a while; it's a long night."], 'calm')),
                    lambda b: (b.fadeout(), b.recover_all(), b.wait(40), b.fadein(),
                               b.text(["You rest a while. (HP and MP restored.)"])))
    def assault(e):
        e.fadeout()
        e.recover_all()
        e.set_time(4, 0)
        e.wait(60)
        e.se('Bell1', 90, 70)
        e.wait(40)
        e.se('Bell1', 90, 70)
        e.fadein()
        e.say(SOMA, ["Second bell! On your feet! Column, form up!"])
        e.narrate(["In the dark the army goes up the valley without torches.",
                   "Snow squeaks under two thousand boots. Then a horn, and",
                   "the Crown's soldiers pour into the south breach."])
        e.say(RIN, ["Kanta! The north-west tower! I'll see you at my gate."])
        e.quest_desc(Q_WF, "The assault has begun. Slip away from the fighting to the north-west tower of the lower "
                           "city and follow the aqueduct to the forge.")
        e.switch(S_ASSAULT)
        e.switch(S_IN_CITY)
        e.rest_point(WF_UNTERSTADT, 23, 36, 8)
        e.fadeout()
        e.transfer(WF_UNTERSTADT, 23, 37, 8, 0)
        e.fadein()
    el = Ev().text(["The party's tent. Three bedrolls, one of them for show."])
    el.choices(["Sleep", "Not yet"], [sleep, None], cancel=1)
    mb.add("Party Tent", tent_door[0], tent_door[1], [pg(el, trigger=0, priority=1)])
    for (x, y) in [(22, 10), (26, 10)]:
        mb.light('brazier', x, y)
    mb.light('brazier', fire[0], fire[1])
    return mb


# ---------------------------------------------------------------------------
# 77  Weißenfels, the lower city
# ---------------------------------------------------------------------------
def gen_unterstadt():
    g = Gen(46, 40, 2, seed=77)
    g.paint(g.all(), OUT.SNOW)
    # the city wall around, the citadel rock and wall across the top
    city = g.rect(2, 8, 43, 37)
    wall_ring = g.border(g.rect(1, 7, 44, 38))
    g.cliff(wall_ring - g.rect(21, 37, 25, 38), *OUT.BRICK_WALL, height=1)   # city wall: tops, one row of face
    for (x, y) in g.all() - g.rect(1, 7, 44, 39):
        g.set(x, y, 0, 0)
    # the citadel: a raised rock (top rows) behind a great wall with the gate at 22..23
    cit = g.rect(1, 0, 44, 4)
    g.paint(cit, OUT.SNOW_CLIFF[0])
    for c in cit:
        g.blocked.add(c)
    for x in range(1, 45):
        for y in (5, 6):
            g.set(x, y, 0, auto(OUT.BRICK_WALL[1]))
            g.blocked.add((x, y))
    for y in (5, 6):
        for x in (22, 23):
            g.set(x, y, 0, auto(OUT.SNOW_STONES))
            g.blocked.discard((x, y))
    # streets: cobbles on snow
    streets = (g.line([(23, 38), (23, 7)], 3) | g.line([(4, 22), (42, 22)], 2) | g.line([(8, 12), (38, 12)], 2) |
               g.line([(8, 12), (8, 32)], 2) | g.line([(38, 12), (38, 32)], 2) | g.line([(8, 31), (38, 31)], 2))
    streets &= g.rect(2, 7, 43, 38)
    g.paint(streets, OUT.SNOW_STONES)
    g.keep_clear |= g.grow(streets, 1)
    # the square with a dead fountain (well)
    sq = g.rect(19, 19, 27, 25)
    g.paint(sq, OUT.SNOW_STONES)
    g.stamp(23, 22, [(0, 0, OUT.WELL)], force=True)
    # ruined houses in the blocks
    rng = g.rng
    for (x0, y0, x1, y1) in [(11, 8, 21, 11), (25, 8, 36, 11), (39, 8, 43, 11),
                             (3, 13, 7, 21), (10, 14, 20, 20), (26, 14, 37, 20), (39, 13, 43, 21),
                             (3, 24, 7, 30), (10, 24, 20, 30), (26, 24, 37, 30), (39, 24, 43, 30),
                             (3, 33, 7, 36), (10, 33, 20, 36), (26, 33, 37, 36), (39, 33, 43, 36)]:
        x = x0
        while x + 3 <= x1:
            w = min(rng.randint(4, 6), x1 - x + 1)
            h = min(rng.randint(3, 5), y1 - y0 + 1)
            if w >= 3 and h >= 3 and rng.random() < 0.8:
                T.ruin(g, x, y0, w, h, wall=rng.choice(['grey', 'snowbrick', 'darkbrick']))
            x += w + 1
    # miasma: dark sparkles and cracks, dead trees
    free = [c for c in city if c not in g.blocked and c not in g.keep_clear]
    for c in rng.sample(free, len(free) // 10):
        g.set(c[0], c[1], 1, auto(rng.choice([OUT.DARKSPARK, OUT.CRACKS])))
    g.scatter_in(set(free), [OUT.DEADTREE, OUT.DEADTREE2, OUT.SNOWPINE], 14, spacing=1)
    # the north-west tower: a stone house with a dark door in the corner
    tower_door = T.house(g, 3, 8, 5, roof='snow', wall='grey', door='dark', windows=False, roof_h=3, wall_h=2)
    g.finish()
    return g, {'tower_door': tower_door}


def unterstadt():
    g, info = gen_unterstadt()
    R = T.reach_check(g, (23, 37), [(22, 7), (info['tower_door'][0], info['tower_door'][1])], 'Weißenfels')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    INFO[WF_UNTERSTADT] = info
    mb = MapBuild(WF_UNTERSTADT, NAMES[WF_UNTERSTADT], g.m, display="Weißenfels · Unterstadt")
    mb.props(note="<Rank: D>\n<Area Name: Weißenfels>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Dungeon6', 55), bgs=('Fire2', 35), battleback=('Snowfield', 'Ruins2'), encounters=CITY_ENC(),
             steps=26, weather='snow 4')
    # --- the south breach: back to the camp
    for x in range(21, 26):
        el = Ev().se('Move1', 60).transfer(HEERLAGER, 20, 2, 2, 0)
        mb.add("South Breach", x, 38, [pg(el, trigger=1, priority=0)])
    # --- arrival during the assault
    el = Ev()
    el.wait(10)
    el.se('Battle1', 60)
    el.shake(3, 5, 30)
    el.narrate(["Weißenfels: streets of burnt-out houses under the snow,",
                "and in every doorway something that used to live here.",
                "Behind you the Crown's soldiers hold the breach."])
    el.say(SOMA, ["We have the breach! You three: the north-west tower,",
                  "left along the wall! Go!"])
    el.say(FALIN, ["I know these streets. I don't know how I know them."], 'hurt')
    el.say(HANMA, ["Follow the feeling, then. Carefully."], 'calm')
    mb.autorun("The Breach", el, cond_switch=S_ASSAULT)
    soma = mb.add("Takamura Sōma", 23, 34, [pg(None, priority=0),
                                           pg(Ev().say(SOMA, ["We hold here. The tower, go!"]), sw=S_IN_CITY,
                                              char=SOMA.char[0], index=SOMA.char[1], direction=8, priority=1),
                                           pg(Ev().say(SOMA, ["The gate's open! Her Highness went up to the citadel.",
                                                              "Don't let her face it alone."]), sw=S_GATE,
                                              char=SOMA.char[0], index=SOMA.char[1], direction=8, priority=1)])
    for (x, y) in [(21, 35), (25, 35), (22, 36)]:
        mb.add("Crown Soldier", x, y, [pg(None, priority=0),
                                       pg(Ev().say(WALL_SOLDIER, ["Hold the line!"]), sw=S_IN_CITY, char='Actor3',
                                          index=6, direction=8, priority=1)])
    # --- the north-west tower door: down to the aqueduct
    td = info['tower_door']
    el = Ev()
    el.text(["The north-west tower. The door has been forced; stairs",
             "go down into the dark, and warm, wet air comes up them."])
    el.choices(["Go down", "Not yet"], [lambda b: (b.se('Open3'), b.se('Move1', 60),
                                                   b.transfer(AQUAEDUKT, 4, 26, 8, 0)), None], cancel=1)
    mb.add("Tower Door", td[0], td[1], [pg(el, char='!Door1', index=4, direction=2, pattern=1, trigger=0, priority=1,
                                          walk_anime=False)])
    # --- the citadel gate
    gate_closed = Ev().text(["The citadel gate: a portcullis of black iron, and above",
                             "it a wall of the rock itself. The winch that lifts it",
                             "is somewhere inside."])
    def into_hall(e):
        e.say(RIN, ["Kanta. Falin. Hanma."])
        e.say(RIN, ["The Iron Prince is in the great hall. I'm going in. I'd",
                    "rather not go in alone."])
        e.say(KANTA, ["You won't."], 'calm')
        e.se('Equip3')
        e.party(RIN_ID, True)
        e.plugin('Story_Core', 'SyncLevel', {'actorId': RIN_ID, 'sourceId': 1}, 'Sync Level')
        e.plugin('Story_Core', 'AutoBuild', {'actorId': RIN_ID}, 'Auto Build')
        e.notice(["\\C[6]Rin\\C[0] joins the party for now. (A battle-mage at rank C:",
                  "fire, ice, and a shield for everyone.)"])
        e.se('Move1', 60)
        e.transfer(DRACHENHALLE, 15, 24, 8, 0)
    gate_open = Ev()
    gate_open.if_actor_in_party(RIN_ID, lambda b: (b.se('Move1', 60), b.transfer(DRACHENHALLE, 15, 24, 8, 0)), into_hall)
    for x in (22, 23):
        mb.add("Citadel Gate", x, 6, [pg(gate_closed, char='!$Gate2', index=0, direction=2, pattern=1, trigger=0,
                                         priority=1, walk_anime=False, direction_fix=True),
                                      pg(gate_open, sw=S_GATE, char='!$Gate2', index=0, direction=8, pattern=1,
                                         trigger=0, priority=1, walk_anime=False, direction_fix=True, through=True)])
    rin_gate = mb.add("Asahina Rin", 21, 8, [pg(None, priority=0),
                                            pg(Ev().say(RIN, ["The hall is straight up the stairs. Are you ready?"]),
                                               sw=S_GATE, char=RIN.char[0], index=RIN.char[1], direction=2, priority=1),
                                            pg(None, sw=S_PRINZ, priority=0)])
    # --- the chain gang on the coal road (optional)
    cg = sp((9, 26))
    workers = []
    for dy, (sheet, idx) in enumerate([('People1', 6), ('People2', 2), ('People1', 7)]):
        c = sp((cg[0], cg[1] + dy), avoid=[(e['x'], e['y']) for e in mb.m['events'] if e])
        workers.append(mb.add("Worker", c[0], c[1],
                              [pg(None, char=sheet, index=idx, direction=8, priority=1),
                               pg(Ev().say(npc_speaker("Arbeiter", sheet, idx), ["Free. Gods. Free. Which way is the army?"]),
                                  sw=S_CHAIN, priority=0)]))
    guard = sp((cg[0] + 1, cg[1] - 2), avoid=[(e['x'], e['y']) for e in mb.m['events'] if e])
    def chain(e):
        e.text(["A line of people in rags and chains, bent under sacks",
                "of coal, driven toward the citadel by a thing in armor",
                "with nobody inside it, and a thrall with a whip."])
        e.say(FOREMAN, ["Don't. Don't look at them, they'll only… oh. You're",
                        "not theirs."])
        e.say(FALIN, ["Get down."], 'fierce')
        e.battle(TR["Kettenkolonne"])
        e.switch(S_CHAIN)
        e.wait(10)
        e.say(FOREMAN, ["Kuroda. I was a smith here, before. Now I carry coal",
                        "for the thing that eats smiths."])
        e.say(FOREMAN, ["The forge is under the citadel. Hundreds down there.",
                        "The Aschenschmied works them until they drop, and then",
                        "the shells get what's left."])
        e.say(KANTA, ["Mariko and Aya Nishiki. Do you know them?"], 'calm')
        e.say(FOREMAN, ["Mariko? The scratcher. She writes the names inside the",
                        "shells so someone remembers who went into them. The",
                        "girl carries water. They're alive. Last I saw."])
        e.say(FOREMAN, ["Take this. It was my master's. Better on you than on",
                        "a thrall."])
        e.armor(FA["Kriegeramulett"], 1)
        e.notice(["Received a Kriegeramulett. The workers run for the breach."])
        e.quest_done(Q_CHAIN)
        e.quest_desc(Q_MA, "Kuroda, a freed smith: Mariko writes the names of the dead inside the empty shells; Aya "
                           "carries water. Both were alive in the forge under the citadel.")
    gd = mb.add("Chain Gang", guard[0], guard[1],
                [pg(Ev().if_switch(S_CHAIN, False, chain), char='Monster', index=3, direction=2, priority=1,
                    step_anime=True, trigger=0),
                 pg(None, sw=S_CHAIN, priority=0)])
    # --- a chest in the ruins, the dead fountain
    c1 = sp((40, 26))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Großes Elixier"], 1), e.gold(1500)),
          "Found a Großes Elixier and \\MONEY[1500].")
    c2 = sp((40, 10))
    chest(mb, "Chest", c2[0], c2[1], lambda e: e.armor(FA["Magierhut"], 1), "Found a Magierhut.")
    mb.add("Fountain", 23, 22, [pg(Ev().text(["A fountain, dry and cracked. Someone has scratched a",
                                              "blue banner on its rim, over and over."]), priority=1)])
    for (x, y) in [(12, 23), (34, 23), (20, 32), (26, 32)]:
        mb.light('gate_fire', x, y)
    mb.follow_light('beam', 23, 37)
    return mb


# ---------------------------------------------------------------------------
# 78  Alter Aquädukt: channels under the lower city (two sluices, one water gate)
# ---------------------------------------------------------------------------
def gen_aquaedukt():
    g = Gen(32, 30, 4, seed=78)
    rooms = [(2, 22, 8, 28),          # entry (stairs from the tower)
             (2, 12, 10, 19),         # west sluice chamber
             (21, 12, 29, 19),        # east sluice chamber
             (11, 3, 20, 9),          # the water gate hall
             (11, 11, 20, 27)]        # the great channel hall
    halls = [([(5, 22), (5, 19)], 3), ([(8, 25), (12, 25)], 3), ([(10, 15), (12, 15)], 3), ([(19, 15), (22, 15)], 3),
             ([(15, 9), (15, 11)], 4)]
    open_ = T.rooms_and_halls(g, rooms, halls, *DUN.MOSS_BRICK, DUN.ROCK, wall_h=2)
    # the channel: water down the middle of the great hall with walkways either side and two bridges
    chan = g.rect(14, 13, 17, 27)
    g.paint(chan, DUN.WATER)
    for y in (16, 23):
        for x in range(14, 18):
            g.set(x, y, 0, auto(DUN.ROCK))
    # a little water in the gate hall, sluice mechanisms
    g.paint(g.rect(12, 6, 13, 8) | g.rect(18, 6, 19, 8), DUN.WATER)
    free = {c for c in open_ if g.kind_at(*c) == DUN.ROCK}
    g.scatter_in(free - g.rect(13, 12, 18, 28), DUN.PEBBLES + [[(0, 0, DUN.JAR)], [(0, 0, DUN.BARREL)]], 18, spacing=1)
    g.finish()
    return g


def aquaedukt():
    g = gen_aquaedukt()
    mb = MapBuild(AQUAEDUKT, NAMES[AQUAEDUKT], g.m, display=NAMES[AQUAEDUKT])
    mb.props(note="<Rank: D>\n<Area Name: Alter Aquädukt>", bgm=('Dungeon3', 55), bgs=('Drips', 50),
             battleback=('Stone3', 'Stone3'),
             encounters=[(TR["Ghule x3"], 5, ()), (TR["Hülle & Koloss"], 4, ()), (TR["Leere Hüllen x2"], 4, ())],
             steps=24)
    mb.add("Stairs Up", 4, 27, [pg(Ev().se('Move1', 60).transfer(WF_UNTERSTADT, INFO[WF_UNTERSTADT]['tower_door'][0],
                                                                INFO[WF_UNTERSTADT]['tower_door'][1] + 1, 2, 0),
                                   trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The old aqueduct: vaulted brick, black water, and warm",
                "air breathing up from somewhere deeper. Far off, a",
                "hammer rings on metal, slow as a heartbeat."])
    el.say(HANMA, ["Two sluices, if the princess's mage read her plans",
                   "right, one on each side. Open both and the water gate",
                   "at the top should lift."], 'calm')
    mb.autorun("Aqueduct", el)
    # sluices
    def sluice(sw, troop, side):
        def f(e):
            e.text(["A sluice wheel as tall as a man, rusted fast. Something",
                    "stirs in the dark water behind it."])
            e.battle(TR[troop])
            e.se('Switch2')
            e.se('Water2', 80, 80)
            e.text(["You throw your weight on the spokes until the wheel",
                    "groans round. Somewhere water begins to drain."])
            e.switch(sw)
            e.if_script("$gameSwitches.value(%d) && $gameSwitches.value(%d)" % (S_SLUICE1, S_SLUICE2),
                        lambda b: (b.se('Gate1'), b.shake(3, 5, 30), b.text(["A deep boom from the top of the channel: the water",
                                                                             "gate is lifting."]),
                                   b.switch(S_WATERGATE)),
                        lambda b: b.say(HANMA, ["One. The other is on the %s side." % side], 'calm'))
        return f
    for (sw, troop, pos, side) in [(S_SLUICE1, "Hülle & Koloss", (5, 13), "east"),
                                   (S_SLUICE2, "Ghule & Knecht", (26, 13), "west")]:
        mb.add("Sluice", pos[0], pos[1], [pg(Ev().if_switch(sw, False, sluice(sw, troop, side),
                                                          lambda b: b.text(["The sluice wheel, turned."])),
                                            char='!Switch1', index=2, direction=2, trigger=0, priority=1,
                                            walk_anime=False),
                                         pg(Ev().text(["The sluice wheel, turned."]), sw=sw, char='!Switch1', index=2,
                                            direction=8, trigger=0, priority=1, walk_anime=False)])
    # the water gate
    closed = Ev().text(["A gate of iron bars, its lower half under dark water.",
                        "Warm air and the ring of hammers come through it."])
    open_ = Ev().se('Move1', 60).transfer(HUELLENSCHMIEDE, 16, 27, 8, 0)
    for x in (15, 16):
        mb.add("Water Gate", x, 4, [pg(closed, char='!$Gate2', index=0, direction=2, pattern=0, trigger=0, priority=1,
                                       walk_anime=False, direction_fix=True),
                                    pg(open_, sw=S_WATERGATE, char='!$Gate2', index=0, direction=8, pattern=0,
                                       trigger=0, priority=1, walk_anime=False, direction_fix=True)])
    chest(mb, "Chest", 27, 17, lambda e: (e.item(FI["Hoher Manatrank"], 2), e.item(FI["Allheilmittel"], 2)),
          "Found 2 Hoher Manatrank and 2 Allheilmittel.")
    chest(mb, "Chest", 3, 17, lambda e: e.weapon(FW["Kriegsflegel"], 1), "Found a Kriegsflegel.")
    mb.light('cave_dark', 0, 0, tile=False)
    for (x, y) in [(6, 12), (25, 12), (13, 3), (18, 3), (4, 22)]:
        mb.light('torch', x, y)
    mb.follow_light('beam', 4, 26)
    return mb


# ---------------------------------------------------------------------------
# 79  Hüllenschmiede: the forge of empty armors under the citadel
# ---------------------------------------------------------------------------
def gen_forge():
    g = Gen(34, 30, 4, seed=79)
    rooms = [(12, 22, 20, 28),        # the water gate landing
             (3, 10, 30, 21),         # the forge floor
             (11, 3, 22, 9),          # the great furnace
             (25, 2, 31, 7)]          # the winch stair
    halls = [([(16, 21), (16, 23)], 3), ([(22, 6), (26, 6)], 2), ([(28, 7), (28, 10)], 2)]
    open_ = T.rooms_and_halls(g, rooms, halls, *DUN.LAVA_ROCK, DUN.LAVAROCK, wall_h=2)
    # lava: pools on the forge floor and the furnace channel
    lava = g.rect(5, 17, 9, 19) | g.rect(23, 17, 27, 19) | g.rect(13, 5, 14, 7) | g.rect(19, 5, 20, 7)
    g.paint(lava, DUN.LAVA)
    g.paint(g.rect(15, 12, 17, 20), 34)          # a darker work floor down the middle
    # the racks of empty armors (knight statues) along the forge floor
    for x in list(range(4, 12, 2)) + list(range(22, 30, 2)):
        g.stamp(x, 12, [(0, 0, 80)])
    for x in range(4, 12, 2):
        g.stamp(x, 15, [(0, 0, 81)])
    free = {c for c in open_ if g.kind_at(*c) in (DUN.LAVAROCK, 34)}
    g.scatter_in(free - g.rect(12, 10, 20, 28), [DUN.LAVASPIRE, [(0, 0, 216)], [(0, 0, 217)], [(0, 0, 208)],
                                                 [(0, 0, 222)]], 10, spacing=1)
    g.finish()
    return g


def huellenschmiede():
    g = gen_forge()
    mb = MapBuild(HUELLENSCHMIEDE, NAMES[HUELLENSCHMIEDE], g.m, display=NAMES[HUELLENSCHMIEDE])
    mb.props(note="<Rank: C>\n<Area Name: Hüllenschmiede>", bgm=('Dungeon5', 60), bgs=('Fire3', 45),
             battleback=('LavaCave', 'LavaCave'),
             encounters=[(TR["Leere Hüllen x2"], 5, ()), (TR["Hülle & Koloss"], 4, ())], steps=30)
    el = Ev().if_switch(S_SMITH, True, lambda b: (b.se('Move1', 60), b.transfer(AQUAEDUKT, 15, 5, 2, 0)),
                        lambda b: b.text(["Back through the water gate? Not with the forge still", "burning."]))
    mb.add("Water Gate", 16, 28, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.se('Hammer', 70)
    el.wait(20)
    el.se('Hammer', 70)
    el.narrate(["Heat like a hand pushing you back. A cavern of red rock",
                "and rivers of fire, and along every wall, on racks, row on",
                "row of empty armors waiting for someone to fill them."])
    el.narrate(["Hundreds of people in chains work the bellows and the",
                "anvils. Nobody looks up."])
    el.say(FALIN, ["…"], 'hurt')
    el.say(HANMA, ["Falin?"], 'calm')
    el.say(FALIN, ["I've been here. I know I've been here."], 'hurt')
    el.switch(S_FORGE)
    el.quest_desc(Q_WF, "The forge under the citadel. The winch house is above it: up the stair on the far side.")
    mb.autorun("The Forge", el)
    # workers at the anvils (mute until freed)
    for (x, y, sheet, idx) in [(6, 14, 'People1', 6), (10, 14, 'People2', 2), (23, 14, 'People4', 4),
                               (27, 14, 'People3', 5), (13, 11, 'People1', 7), (19, 11, 'People2', 0)]:
        who = npc_speaker("Arbeiter", sheet, idx)
        mb.add("Worker", x, y, [pg(Ev().text(["They keep working. They don't dare look at you."]), char=sheet, index=idx,
                                   direction=8, priority=1),
                                pg(Ev().say(who, ["Out. The army's in the city? Out, out, out…"]), sw=S_FREED,
                                   char=sheet, index=idx, direction=2, priority=1)])
    # the racks: Falin's memory
    def memory(e):
        e.text(["An empty armor on a rack, taller than a man. Inside the",
                "breastplate, over the heart, a name has been scratched",
                "with a nail: HARUTO."])
        e.say(FALIN, ["Same hand."], 'hurt')
        e.say(KANTA, ["Falin?"], 'calm')
        e.say(FALIN, ["My name. Inside my plate. It's the same hand, the same",
                      "nail, the same crooked F…"], 'hurt')
        e.flash((255, 140, 60, 200), 40)
        e.se('Fire1', 70, 60)
        e.text(["Heat. Darkness. A hammer, very close. A woman's voice,",
                "cracked and desperate, right against the metal:"], background=1, position=1)
        e.text(["\"Wake up, Falin. Please. Please, wake up.\""], background=1, position=1)
        e.flash((255, 255, 255, 170), 30)
        e.say(FALIN, ["…I heard that. The first thing I ever heard."], 'hurt')
        e.say(HANMA, ["Then the one who scratched these names woke you. Find",
                      "her, and you'll have the story you were afraid of."], 'calm')
        e.switch(S_MEMORY)
    for x in range(4, 12, 2):
        mb.add("Armor Rack", x, 12, [pg(Ev().if_switch(S_MEMORY, False, memory,
                                                        lambda b: b.text(["Names, scratched inside every breastplate."])),
                                        trigger=0, priority=1)])
    # Mariko and Aya (by the furnace), the Aschenschmied at the great anvil
    mariko = mb.add("Mariko", 12, 8, [pg(None, char=MARIKO.char[0], index=MARIKO.char[1], direction=2, priority=1)])
    aya = mb.add("Aya", 13, 8, [pg(None, char=AYA.char[0], index=AYA.char[1], direction=2, priority=1)])
    smith = mb.add("Aschenschmied", 16, 6, [pg(None, char='Monster', index=7, direction=2, priority=1, step_anime=True),
                                           pg(None, sw=S_SMITH, priority=0)])
    def boss(e):
        e.se('Hammer', 90, 60)
        e.text(["At the great anvil, in the light of the furnace, a smith",
                "three heads taller than any man lowers a hammer the",
                "size of a door. Its skin is cracked like a cooling crust."])
        e.say(npc_speaker("Aschenschmied", "", 0), ["More metal. Good. Lie down on the anvil. Hold still.",
                                                     "You will make a fine shell."])
        e.say(FALIN, ["No."], 'fierce')
        e.say(HANMA, ["Rank C, my Lord: one above us. It's the forge's heart.",
                      "Put it out."], 'command')
        e.battle(TR["Aschenschmied"])
        e.switch(S_SMITH)
        e.wait(20)
        e.se('Fire2', 80, 60)
        e.text(["The Aschenschmied falls across its own anvil and cracks",
                "apart like a clinker. All over the cavern, hammers stop."])
        e.say(FALIN, ["Everyone! It's dead! The army is in the city: out,",
                      "through the water gate, go!"], 'fierce')
        e.switch(S_FREED)
        e.wait(20)
        e.route(mariko, [(16, [])], wait=True)
        e.say(MARIKO, ["…You. The plate. I know that plate."])
        e.say(FALIN, ["You scratched my name."], 'calm')
        e.say(MARIKO, ["Nishiki Mariko. I scratched every name. When they",
                       "brought the dead in to fill the shells, I asked each one",
                       "his name, if he could still talk, and I wrote it inside,",
                       "so somebody would remember who went in."])
        e.say(MARIKO, ["The first night, they brought a girl. Your name was the",
                       "only thing she could say. Falin. Falin. She was so cold."])
        e.say(MARIKO, ["The Vogt put her into that shell with his book, and",
                       "the shell didn't move. None of them move on their own."])
        e.say(MARIKO, ["I sat by it all night with my hand on the metal and",
                       "begged it to wake up. And it did. It stood up and walked",
                       "through the fire, and nobody could stop it."])
        e.say(FALIN, ["…Who was she? The girl?"], 'hurt')
        e.say(MARIKO, ["I don't know. The book of names burned the night the",
                       "city fell. She had a soldier's hands. She was young."])
        e.say(FALIN, ["Then I don't have a story. Just a name, and you."], 'hurt')
        e.say(MARIKO, ["That's more than any of the others got."])
        e.say(AYA, ["Mama. Is Papa here? You said Papa would come."])
        e.say(MARIKO, ["…Eiji? Did my Eiji send you? The Vogt said he signed.",
                       "He said Eiji signed for us, and we'd go home."])
        e.say(KANTA, ["He tried to buy you back. It cost him everything."], 'calm')
        e.say(HANMA, ["He's at the Wallfeste, madam. The contract took him.",
                      "He was thinking of you both when it did."], 'calm')
        e.say(MARIKO, ["…"])
        e.say(AYA, ["Mama?"])
        e.say(MARIKO, ["It's all right, Aya. It's all right. We're going home.",
                       "Papa got us out. Papa got us out."])
        e.say(FALIN, ["The army's at the south breach. Yukimura Saki is in the",
                      "camp, the Wall's healer. Go to her. She's waiting."], 'calm')
        e.fadeout()
        e.set_image(mariko, '', 0)
        e.set_image(aya, '', 0)
        e.quest_done(Q_MA)
        e.fadein()
        e.say(HANMA, ["The winch house, my Lord. Up the stair at the far end.",
                      "Rin is waiting at her gate."], 'command')
        e.quest_desc(Q_WF, "The forge is out and the workers are free. Up the stair behind the furnace to the winch "
                           "house: open the citadel gate for Rin.")
    for x in (15, 16, 17):
        mb.add("Furnace", x, 8, [pg(Ev().if_switch(S_SMITH, False, boss), trigger=1, priority=0)])
    # the winch
    def winch(e):
        e.text(["The winch house: a great drum of chain, a lever as long",
                "as a spear. Through a slit in the rock you can see the",
                "citadel gate far below, and a figure waiting in front of it."])
        e.choices(["Throw the lever", "Not yet"], [lambda b: (b.se('Switch1'), b.se('Gate2', 90, 70),
                                                              b.shake(4, 4, 60),
                                                              b.text(["Chains shriek. Far below, the portcullis grinds up",
                                                                      "into the rock."]),
                                                              b.switch(S_GATE),
                                                              b.quest_desc(Q_WF, "The citadel gate is open. Rin waits in front "
                                                                                 "of it in the lower city."),
                                                              b.fadeout(),
                                                              b.transfer(WF_UNTERSTADT, 22, 9, 8, 0), b.fadein()),
                                                   None], cancel=1)
    el = Ev().if_switch(S_SMITH, True, winch, lambda b: b.text(["The stair up to the winch house. The Aschenschmied's",
                                                                 "hammer rings behind you. Not yet."]))
    mb.add("Winch", 28, 3, [pg(el, char='!Switch1', index=0, direction=2, trigger=0, priority=1, walk_anime=False)])
    chest(mb, "Chest", 30, 6, lambda e: (e.item(FI["Großes Elixier"], 1), e.item(foes.ITEMS["Manastein (C)"], 1)),
          "Found a Großes Elixier and a Manastein (C).")
    mb.light('ash_night', 0, 0, tile=False)
    for (x, y) in [(7, 18), (25, 18), (16, 4), (13, 6), (20, 6)]:
        mb.light('brazier', x, y)
    return mb


# ---------------------------------------------------------------------------
# 80  Drachenhalle: the great hall of the citadel
# ---------------------------------------------------------------------------
def gen_hall():
    g = Gen(30, 27, 4, seed=80)
    rooms = [(4, 3, 25, 24)]
    open_ = T.rooms_and_halls(g, rooms, [([(15, 24), (15, 26)], 3)], *DUN.BLOCK, DUN.ROCK, wall_h=2)
    g.paint(g.rect(13, 5, 17, 26), DUN.CARPET)
    g.paint(g.rect(9, 5, 21, 8), DUN.CARPET)
    # pillars down both sides
    for y in range(9, 23, 4):
        for x in (7, 23):
            g.stamp(x, y, T.PILLAR, force=True)
    g.finish()
    return g


def drachenhalle():
    g = gen_hall()
    mb = MapBuild(DRACHENHALLE, NAMES[DRACHENHALLE], g.m, display=NAMES[DRACHENHALLE])
    mb.props(note="<Rank: C>\n<Area Name: Drachenhalle>", bgm=('Castle3', 55), bgs=('Fire1', 30),
             battleback=('DemonCastle2', 'DemonCastle2'))
    el = Ev().if_switch(S_PRINZ, True, lambda b: (b.se('Move1', 60), b.transfer(WF_UNTERSTADT, 22, 8, 2, 0)),
                        lambda b: b.text(["Rin doesn't move from your side. Not now."]))
    for x in (14, 15, 16):
        mb.add("Gate", x, 26, [pg(el, trigger=1, priority=0)])
    # the dragon (big sprite), the prince and his two empty armors
    dragon = mb.add("Shiranui", 15, 6, [pg(None, char='$BigMonster2', index=0, direction=2, priority=1,
                                           direction_fix=True, step_anime=True),
                                        pg(None, sw=S_C5_END, priority=0)])
    prinz = mb.add("Iron Prince", 15, 11, [pg(None, char='Evil', index=6, direction=2, priority=1),
                                          pg(None, sw=S_PRINZ, priority=0)])
    hulls = [mb.add("Empty Armor", x, 11, [pg(None, char='Monster', index=3, direction=2, priority=1),
                                           pg(None, sw=S_PRINZ, priority=0)]) for x in (13, 17)]
    el = Ev()
    el.wait(20)
    el.narrate(["The great hall of Weißenfels. Blue banners rotted to",
                "threads. At the far end, chained to the floor in black",
                "iron, a dragon the colour of embers breathes slowly."])
    el.picture(1, 'Shiranui', 408, 250, opacity=0)
    el.move_picture(1, 408, 250, opacity=210, frames=40)
    el.say(SHIRANUI_S, ["…More of them. Come to see the stove."])
    el.say(HANMA, ["A dragon. They've chained a dragon under the forge and",
                   "they burn her for their fire."], 'stern')
    el.move_picture(1, 408, 250, opacity=0, frames=30)
    el.erase_picture(1)
    el.narrate(["In front of the dragon, on the steps, stands a knight in",
                "black iron with a crown worked into his helm. There is no",
                "breath behind the visor. There is no one behind it at all."])
    el.say(RIN, ["…Hayato."])
    el.say(PRINZ, ["Clause one. The Prince of Weißenfels shall guard the",
                   "fire. Clause two. In exchange, the people of Weißenfels",
                   "shall live."])
    el.say(RIN, ["That's his voice. That's my brother's voice in that",
                 "thing."])
    el.say(HANMA, ["Gōen's bargain, my Lord. The prince signed his soul away",
                   "to save his city, and the Tyrant kept the letter of it:",
                   "they live. In chains, in the forge, but they live."], 'stern')
    el.say(PRINZ, ["Clause three. Whoever frees the fire is an enemy of the",
                   "contract. Rin. Go home."])
    el.say(RIN, ["I am home, Hayato."])
    el.say(FALIN, ["Behind me, Highness. We'll get him out of that iron."], 'fierce')
    el.battle(TR["Der Eiserne Prinz"])
    el.switch(S_PRINZ)
    el.wait(20)
    el.se('Break')
    el.flash((200, 220, 255, 200), 40)
    el.text(["The black armor comes apart at every seam and clatters",
             "down the steps, empty. For a moment the air above it is",
             "full of snow that isn't falling."])
    el.say(HAYATO, ["…Rin. You got tall."])
    el.say(RIN, ["Hayato—"])
    el.say(HAYATO, ["The contract's broken. They're free. That's all I ever",
                    "wanted it for."])
    el.say(HAYATO, ["Don't follow me. Not into the dark, not for me. Promise.",
                    "Go and be a queen. Be a better one than Father."])
    el.say(RIN, ["…I promise."])
    el.fadeout()
    el.wait(30)
    el.fadein()
    el.say(RIN, ["…"])
    # the chains
    el.say(SHIRANUI_S, ["The iron. Little light, the iron. It's null-iron: it",
                        "drinks everything. Magic, fire, light."])
    el.say(KANTA, ["Then I'll cut it."], 'fierce')
    el.se('Magic3', 80, 60)
    el.flash((150, 200, 255, 120), 20)
    el.text(["Kanta reaches for the light. It flickers in her hand and",
             "goes out, like a candle in a draught. Near the chains it",
             "won't form at all."])
    el.say(HANMA, ["Null-iron eats the sigils, my Lord. Nothing we have that",
                   "is made of power can touch it."], 'stern')
    el.say(FALIN, ["Good thing I'm made of metal, then."], 'fierce')
    el.se('Blow3', 100, 70)
    el.shake(5, 5, 20)
    el.se('Blow3', 100, 60)
    el.shake(6, 6, 20)
    el.se('Break', 100, 60)
    el.flash((255, 160, 80, 200), 30)
    el.text(["Falin takes the chain in both gauntlets and pulls. The",
             "null-iron screams. Her plate screams. The chain breaks."])
    el.say(SHIRANUI_S, ["…Ahh."])
    el.picture(1, 'Shiranui', 408, 250, opacity=0)
    el.move_picture(1, 408, 250, opacity=230, frames=30)
    el.say(SHIRANUI_S, ["Six years in the dark, feeding their forge. A living",
                        "armor, a dead general and a little light. What a strange",
                        "company to be freed by."])
    el.say(SHIRANUI_S, ["I will remember you, little light. When you call, if",
                        "you ever call, I will hear it."])
    el.se('Fire3', 90, 60)
    el.shake(8, 8, 40)
    el.move_picture(1, 408, 0, opacity=0, frames=40)
    el.erase_picture(1)
    el.set_image(dragon, '', 0)
    el.text(["The dragon goes up through the roof of the hall in a",
             "storm of sparks, and the citadel of Weißenfels is lit",
             "gold from within for the first time in six years."])
    el.text(["Where the dragon lay, a single scale as big as a shield,",
             "still warm."])
    el.armor(FA["Drachenschuppe"], 1)
    el.notice(["Received the \\C[6]Drachenschuppe\\C[0] (a rank A accessory:",
               "it will fit when you have grown into it)."])
    el.say(RIN, ["…Kanta. Falin. Hanma. This is the Asahina crest: my",
                 "brother's. He'd want it on somebody who fights."])
    el.armor(FA["Königliches Wappen"], 1)
    el.notice(["Received the \\C[6]Königliches Wappen\\C[0]."])
    # the rider: Gōen on the Wall
    el.se('Horse', 90)
    el.wait(20)
    el.say(RIDER, ["Your Highness! Your Highness, a rider from the Marshal!"])
    el.say(RIDER, ["Gōen is moving on the Wall. The whole Host, out of the",
                   "Aschenfeld at once. Frontposten 3 is under siege and the",
                   "Wallfeste will be by nightfall."])
    el.say(RIN, ["…He waited until we were here. Until the Wall had lent",
                 "me two thousand men."])
    el.say(HANMA, ["Of course he did. He's a merchant. He waits for the price",
                   "to drop."], 'stern')
    el.say(RIN, ["Sōma holds Weißenfels with half. The rest march back",
                 "tonight. Kanta. Will you come?"])
    el.say(KANTA, ["Wherever the fighting is."], 'calm')
    el.party(RIN_ID, False)
    el.quest_done(Q_WF)
    el.switch(S_C5_END)
    el.gold(4000)
    el.notice(["The Crown pays for Weißenfels: \\MONEY[4000]."])
    el.plugin('Story_Core', 'ChapterCard', {'title': "Weißenfels", 'subtitle': "ist frei", 'duration': 180},
              'Chapter Card')
    el.fadeout()
    el.transfer(WALLFESTE_SIEGE, 21, 32, 8, 0)
    el.fadein()
    mb.autorun("The Hall", el)
    for (x, y) in [(10, 6), (20, 6), (8, 18), (22, 18)]:
        mb.light('brazier', x, y)
    return mb

