"""Chapter 7: Die Kaiserstadt (Act III opens). The Kaiserstraße, Lichtenhall, the Sonnwende tournament, the
Web-Weaver in the imperial box, the Unterhallen under the Morgendom, the breakthrough to B, the Morgenklinge."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story import foes, foes3
from story.ids import *
from story.ch1 import chest
from story.ch2 import camp_fire
from story.cast import *
from story.ch6 import V_REGALIA, S_C6_END, YUKINO_ID
from story import terrain as T
from story.terrain import Gen, OUT, DUN, INS, auto

KI = foes.KEY
K3 = foes3.KEY
FI = foes.ITEMS
FA = foes.ARMORS
FW = foes.WEAPONS
T3 = foes3.TR

GUARD_LH = npc_speaker("Stadtwache", "Actor3", 6)
CITIZEN = [npc_speaker("Bürger", "People1", 2), npc_speaker("Bürgerin", "People1", 3), npc_speaker("Händler", "People2", 4),
           npc_speaker("Bürgerin", "People4", 3), npc_speaker("Junge", "People1", 0)]
INNKEEP = npc_speaker("Wirtin Hoshi", "People4", 1)
SMITH_LH = npc_speaker("Waffenhändler", "People2", 6)
GROCER = npc_speaker("Krämerin", "People4", 7)
HEALER = npc_speaker("Arenaheilerin", "People2", 3)

# ----------------------------------------------------------------------- quests
Q_EMPRESS = Quest(26, "Die Kaiserin", "Asahina Rin", "Lichtenhall",
                  "Rin's letter asks the Empress in Lichtenhall for the Morgenklinge, the first of the four Dawn "
                  "Regalia, and for her legions on the Wall. The Empress receives no one before the Sonnwende.",
                  "Lichtenhall, at the end of the Kaiserstraße.")
Q_TURNIER = Quest(27, "Das Sonnwende-Turnier", "Amane Kiyoko", "Lichtenhall, Kaiserarena",
                  "The Morgenklinge is the prize of this year's Sonnwende tournament: the Empress thinks it is a pretty "
                  "old sword. Guild teams may enter. Register at the Lichtenhall guild, then fight four rounds in the "
                  "Kaiserarena.",
                  "Register at the guild; the arena is in the east of the city.")
Q_WEB = Quest(28, "Die Weberin", "Amane Kiyoko", "Lichtenhall, Unterhallen",
              "The Empress's lady-in-waiting was Tsumugi, the Web-Weaver, one of the Four. She took the Morgenklinge "
              "and fled into the Unterhallen under the city.",
              "Down through the arena floor into the Unterhallen.")

# ----------------------------------------------------------------------- switches
S_C7 = SW('C7: Kaiserstraße')
S_AMBUSH = SW('C7: Ambush')
S_LH = SW('C7: In Lichtenhall')
S_KIYOKO = SW('C7: Kiyoko Met')
S_STATUE = SW('C7: Akira Statue')
S_REG = SW('C7: Registered')
S_R1 = SW('C7: Round 1')
S_R2 = SW('C7: Round 2')
S_R3 = SW('C7: Round 3')
S_R4 = SW('C7: Final Won')
S_THEFT = SW('C7: The Theft')
S_COCOONS = SW('C7: Cocoons Freed')
S_TSUMUGI = SW('C7: Web-Weaver Down')
S_AUDIENCE7 = SW('C7: Audience')
S_C7_END = SW('C7: Chapter Done')
V_COCOONS = VAR('C7: Cocoons')

ROAD_ENC = lambda: [(T3["Straßenräuber x3"], 5, ()), (T3["Räuber & Agent"], 4, ()), (T3["Sturmharpyien x2"], 4, ()),
                    (T3["Agenten x2"], 2, ())]
CATA_ENC = lambda: [(T3["Höhlenspinnen x3"], 5, ()), (T3["Spinnen & Kokon"], 4, ()), (T3["Klinge & Agenten"], 3, ()),
                    (T3["Spinnenkreis-Klingen x2"], 2, ())]

KAISER_ENTRY = (20, 1)


def build():
    return [kaiserstrasse(), lichtenhall(), palast(), arena(), morgendom(), katakomben(), spinnenhalle(), gilde(),
            gasthaus()]


def regalia_gain(e, key_name, count_text):
    e.se('Item3')
    e.me('Fanfare3')
    e.item(KI[key_name], 1)
    e.var(V_REGALIA, 1, '+')
    e.notice(["Received the \\C[6]%s\\C[0]. (%s)" % (key_name, count_text),
              "Each Dawn Regalia cancels one rank of difference against",
              "demons. With all four, the Demon Lord's veil fails."])


# ---------------------------------------------------------------------------
# 100  Kaiserstraße: south through the imperial farmland
# ---------------------------------------------------------------------------
def gen_kaiserstrasse():
    g = Gen(40, 40, 2, seed=100)
    g.paint(g.all(), OUT.GRASS)
    walk = g.line([(20, 0), (19, 8), (12, 15), (14, 24), (25, 29), (27, 35), (26, 39)], 13, wobble=1.0)
    walk |= g.blob(30, 12, 5, seed=2) | g.blob(8, 30, 4.5, seed=3)
    ground = T.frame(g, walk, T.GRASS, thick=3, trunk_h=2)
    road = g.line([(20, 0), (19, 8), (12, 15), (14, 24), (25, 29), (27, 35), (26, 39)], 2, wobble=1.0) & ground
    g.paint(road, OUT.GRASS_COBBLE)
    g.keep_clear |= g.grow(road, 1)
    # fields: a farm patch with fences and crops
    field = g.rect(27, 9, 34, 15) & ground
    g.paint(field, OUT.DIRT)
    for (x, y) in field:
        if (x + y) % 2 == 0 and g.fits([(x, y)]):
            g.stamp(x, y, [(0, 0, 172 + (x % 3))])
    T.dress(g, ground - g.grow(road, 2) - field, T.GRASS, trees=0.07, rocks=0.02, bushes=0.05, tufts=0.07)
    g.finish()
    return g


def kaiserstrasse():
    g = gen_kaiserstrasse()
    R = T.reach_check(g, KAISER_ENTRY, [(26, 38)], 'Kaiserstraße')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(KAISERSTRASSE, NAMES[KAISERSTRASSE], g.m, display=NAMES[KAISERSTRASSE])
    mb.props(note="<Rank: C>\n<Area Name: Kaiserstraße>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field1', 60), battleback=('Grassland', 'Grassland'), encounters=ROAD_ENC(), steps=30)
    # arrival: Act III
    el = Ev()
    el.card("Akt III", "Morgenröte", 240)
    el.wait(10)
    el.card("Kapitel 7", "Die Kaiserstadt", 200)
    el.narrate(["Ten days south of the Wall the snow gives up, then the",
                "hills, and the Kaiserstraße runs white and straight",
                "through farmland that has never seen a demon."])
    el.say(FALIN, ["Wheat. Sheep. Children. It's like walking into a story."], 'calm')
    el.say(HANMA, ["The Empire has had a wall between it and the Aschenfeld",
                   "for three hundred years. Walls make people forget."], 'stern')
    el.say(YUKINO, ["…"])
    el.say(KANTA, ["Lichtenhall is at the end of the road. An Empress, a",
                   "tournament and a sword."], 'wry')
    el.quest_new(Q_EMPRESS)
    el.switch(S_C7)
    el.rest_point(KAISERSTRASSE, KAISER_ENTRY[0], KAISER_ENTRY[1] + 1, 2)
    mb.autorun("Act III", el)
    # the north end: back north (not needed any more)
    for x in range(g.w):
        if (x, 0) in R and (x, 1) in R:
            mb.add("North", x, 0, [pg(Ev().text(["The Kaiserstraße runs north to the Wall. Your business",
                                                 "is south."]), trigger=1, priority=0)])
    for x in range(g.w):
        if (x, g.h - 1) in R and (x, g.h - 2) in R:
            mb.add("To Lichtenhall", x, g.h - 1, [pg(Ev().se('Move1', 60).transfer(LICHTENHALL, 22, 2, 2, 0),
                                                     trigger=1, priority=0)])
    # the ambush at the ford of the farm road
    amb = sp((13, 20))
    def ambush(e):
        e.se('Crossbow', 90)
        e.text(["A crossbow bolt hums past Kanta's ear and buries itself",
                "in the milestone. Figures in grey stand up out of the",
                "wheat on both sides of the road."])
        e.say(npc_speaker("Agent", "Evil", 7), ["The girl with the light. The Web sends its regards."])
        e.say(FALIN, ["Ambush. Behind me!"], 'fierce')
        e.battle(T3["Räuber & Agent"])
        e.switch(S_AMBUSH)
        e.item(K3["Spinnensiegel"], 1)
        e.say(HANMA, ["A spider pressed into black wax. Someone in the Empire",
                      "knew we were coming before we did."], 'stern')
        e.say(YUKINO, ["…Spinnenkreis."])
        e.say(KANTA, ["You know them?"], 'calm')
        e.say(YUKINO, ["They sell to anyone. Even to him."])
        e.notice(["Found a \\C[6]Spinnensiegel\\C[0] on the agent."])
    for dx in range(-2, 3):
        c = (amb[0] + dx, amb[1])
        if c in R:
            mb.add("Ambush", c[0], c[1], [pg(Ev().if_switch(S_AMBUSH, False, ambush), trigger=1, priority=0)])
    fire = sp((30, 12))
    rest = sp((fire[0], fire[1] + 1), avoid=[fire])
    camp_fire(mb, fire[0], fire[1], KAISERSTRASSE, rest[0], rest[1], 8,
              ["A drovers' fire pit beside a well. Imperial milestones", "count down to Lichtenhall."])
    far = npc_speaker("Bäuerin", "People4", 3)
    c = sp((31, 16))
    mb.npc("Farmer", c[0], c[1], far, Ev().say(far, ["The Wall? That's a story for children, love. Nothing's",
                                                    "come over the Wall in my grandmother's time."]), direction=2)
    c1 = sp((8, 30))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Großes Elixier"], 2), e.gold(6000)),
          "Found 2 Großes Elixier and \\MONEY[6000].")
    c2 = sp((33, 10))
    chest(mb, "Chest", c2[0], c2[1], lambda e: e.armor(FA["Falkenring"], 1), "Found a Falkenring.")
    return mb


# ---------------------------------------------------------------------------
# 101  Lichtenhall: the imperial city
# ---------------------------------------------------------------------------
def gen_lichtenhall():
    g = Gen(46, 42, 2, seed=101)
    g.paint(g.all(), OUT.GRASS)
    ring = g.border(g.rect(0, 0, 45, 41))
    g.cliff(ring - g.rect(21, 0, 24, 0), *OUT.BRICK_WALL, height=1)
    info = {}
    # streets: the avenue north-south, the cross street, the plaza
    streets = g.rect(21, 1, 24, 30) | g.rect(3, 17, 42, 19) | g.rect(8, 11, 9, 17) | g.rect(37, 15, 38, 17)
    g.paint(streets, OUT.GRASS_COBBLE)
    plaza = g.rect(16, 14, 29, 22)
    for (x, y) in plaza:
        g.set(x, y, 0, 1561)
    g.keep_clear |= g.grow(streets | plaza, 1)
    # the palace at the south end
    info['palace'] = T.house(g, 14, 29, 18, roof='gold', wall='marble', door='double', roof_h=4, wall_h=3, windows=True)
    # the Morgendom (west) and its statue of Akira
    info['dom'] = T.house(g, 3, 3, 11, roof='green', wall='marble', door='arch', roof_h=4, wall_h=3)
    g.stamp(8, 12, [(0, -1, 320), (0, 0, 336)], force=True)
    # the Kaiserarena (east): an oval of stone stands around sand
    arena = g.ellipse(37.5, 8, 6.5, 5.5)
    g.paint(arena, OUT.SAND)
    stands = arena - g.ellipse(37.5, 8, 4.5, 3.5)
    g.cliff(stands - g.rect(37, 12, 38, 14), *OUT.BRICK_WALL, height=1)
    info['arena'] = (37, 14)
    # the guild, the inn, houses
    info['gilde'] = T.house(g, 3, 20, 7, roof='wood', wall='plaster', door='arch')
    g.set(info['gilde'][0] + 1, info['gilde'][1] - 1, 3, 66)
    info['inn'] = T.house(g, 11, 20, 7, roof='wood', wall='wood', door='arch')
    g.set(info['inn'][0] + 1, info['inn'][1] - 1, 3, 70)
    for (x, y, w, roof, wall) in [(27, 23, 6, 'wood', 'brick'), (34, 23, 7, 'green', 'plaster'), (3, 28, 7, 'green', 'brick'),
                                  (35, 30, 7, 'wood', 'plaster'), (27, 1, 6, 'wood', 'plaster'), (15, 2, 5, 'green', 'brick')]:
        T.house(g, x, y, w, roof=roof, wall=wall, door='arch')
    # market stalls and the fountain on the plaza
    for x in (17, 19, 26, 28):
        g.stamp(x, 15, [(0, 0, 100)], force=True)
    g.stamp(22, 21, [(0, 0, OUT.WELL)], force=True)
    # lamps along the avenue, trees and flowers in the gaps
    for y in (4, 9, 24):
        g.stamp(20, y, OUT.LAMP)
        g.stamp(25, y, OUT.LAMP)
    free = {c for c in g.all() if g.kind_at(*c) == OUT.GRASS and c not in g.blocked and c not in g.keep_clear}
    g.scatter_in(free, [OUT.TREE, OUT.PINE], 18, spacing=1)
    g.scatter_in(free, [[(0, 0, 160)], [(0, 0, 161)], [(0, 0, 162)], [(0, 0, 163)]], 30, spacing=0)
    g.finish()
    return g, info


def lichtenhall():
    g, info = gen_lichtenhall()
    targets = [info['palace'], info['dom'], info['arena'], info['gilde'], info['inn']]
    R = T.reach_check(g, (22, 2), targets, 'Lichtenhall')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(LICHTENHALL, NAMES[LICHTENHALL], g.m, display=NAMES[LICHTENHALL])
    mb.props(note="<Area Name: Lichtenhall>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town4', 65), bgs=('People1', 30))
    # the north gate: the Kaiserstraße, later the roads of Act III
    def gate(e):
        e.if_switch(S_C7_END, True, lambda b: b.common(CE['Reisen']),
                    lambda b: (b.se('Move1', 60), b.transfer(KAISERSTRASSE, 26, 38, 8, 0)))
    for x in range(21, 25):
        mb.add("North Gate", x, 0, [pg((lambda e: (gate(e), e)[1])(Ev()), trigger=1, priority=0)])
    # arrival
    el = Ev()
    el.wait(10)
    el.narrate(["Lichtenhall: white stone and gold leaf, the green spires",
                "of the Morgendom catching the sun, and every afternoon the",
                "roar of the Kaiserarena rolling over the rooftops."])
    el.say(GUARD_LH, ["Papers. …A letter under the seal of Asahina? For Her",
                      "Imperial Majesty? Hah. Get in line."])
    el.say(GUARD_LH, ["Her Majesty receives nobody before the Sonnwende. The",
                      "tournament starts in the Kaiserarena, east of the plaza.",
                      "After that, maybe. Welcome to Lichtenhall."])
    el.say(HANMA, ["The Morgenklinge was given to the Emperor in 313. If it",
                   "is anywhere, it's in this city. The Morgendom will know."], 'calm')
    el.quest_desc(Q_EMPRESS, "The Empress receives no one before the Sonnwende tournament. The Morgendom (west) "
                             "might know where the Morgenklinge is.")
    el.switch(S_LH)
    el.rest_point(LICHTENHALL, 22, 3, 2)
    mb.autorun("Arrival", el)
    # doors
    p = info['palace']
    def palace(e):
        e.if_switch(S_TSUMUGI, True, lambda b: (b.se('Open1'), b.transfer(PALAST, 13, 17, 8, 0)),
                    lambda b: b.say(GUARD_LH, ["The palace is closed until the Sonnwende. By order."]))
    mb.add("Palace Door", p[0], p[1], [pg((lambda e: (palace(e), e)[1])(Ev()), char='!Door1', index=2, direction=2,
                                          pattern=1, trigger=0, priority=1, walk_anime=False)])
    mb.door(info['dom'][0], info['dom'][1], MORGENDOM, 11, 24, 8, sheet='!Door1', index=2, name='Morgendom')
    mb.door(info['gilde'][0], info['gilde'][1], GILDE_LH, 9, 11, 8, name='Gilde')
    mb.door(info['inn'][0], info['inn'][1], GASTHAUS_LH, 9, 11, 8, name='Gasthaus')
    a = info['arena']
    mb.add("Arena Gate", a[0], a[1], [pg(Ev().se('Move1', 60).transfer(ARENA, 18, 26, 8, 0), trigger=1, priority=0)])
    mb.add("Arena Gate", a[0] + 1, a[1], [pg(Ev().se('Move1', 60).transfer(ARENA, 18, 26, 8, 0), trigger=1, priority=0)])
    # the statue of Akira
    def statue(e):
        e.text(["A statue of a woman in old armor, a sword raised to the",
                "morning. The plinth: SŌRYŪ AKIRA · HELDIN DER MORGENRÖTE",
                "· 312. Around her feet: a crown, a horn, a lantern."])
        e.if_switch(S_STATUE, False, lambda b: (
            b.say(HANMA, ["…They gave her a kind face. She didn't have one. She",
                          "had a tired face, and she was right about me."], 'hurt'),
            b.say(FALIN, ["Right about what?"], 'calm'),
            b.say(HANMA, ["That I would burn the world to kill every demon in it,",
                          "if nobody stopped me. Later, Falin."], 'stern'),
            b.switch(S_STATUE)))
    mb.add("Statue", 8, 12, [pg((lambda e: (statue(e), e)[1])(Ev()), trigger=0, priority=1)])
    # merchants on the plaza
    goods_w = [('weapon', FW["Morgenfaust"]), ('weapon', FW["Messingbrecher"]), ('weapon', FW["Sternenfäuste"]),
               ('armor', FA["Messingbrecherhelm"]), ('armor', FA["Magierhut"]), ('armor', FA["Turmschild der Wacht"]),
               ('armor', FA["Arenahelm"]), ('armor', FA["Waldkrone"]), ('armor', FA["Runenschild"]),
               ('armor', FA["Kriegerring"]), ('armor', FA["Heiligenring"]), ('armor', FA["Magierring"]),
               ('armor', FA["Falkenring"])]
    goods_i = [('item', IT["Großer Heiltrank"]), ('item', FI["Elixier"]), ('item', FI["Großes Elixier"]),
               ('item', FI["Hoher Manatrank"]), ('item', FI["Äther"]), ('item', FI["Starkes Riechsalz"]),
               ('item', FI["Allheilmittel"]), ('item', FI["Große Lichtphiole"])]
    el = Ev().say(SMITH_LH, ["Imperial steel, Eisenberg rune-steel, and prices to",
                             "match. The tournament's good for business."])
    el.shop(goods_w)
    mb.npc("Smith", 17, 16, SMITH_LH, el, direction=2)
    el = Ev().say(GROCER, ["Elixirs, salts, ether. Everything a hero needs, and",
                           "most of what a coward needs too."])
    el.shop(goods_i)
    mb.npc("Grocer", 28, 16, GROCER, el, direction=2)
    # citizens
    lines = [["The Sonnwende! Eight years Gōki's been champion. Somebody",
              "ought to knock him down. Not me. Somebody."],
             ["Her Majesty's new lady-in-waiting, Lady Tsumugi, did you",
              "see her? Such a lovely laugh. Such long fingers."],
             ["People go missing in the lower city. The watch says they",
              "went to the Wall. Nobody goes to the Wall."],
             ["The Morgendom's bells ring the hours. They stop ringing,",
              "we're all in trouble, my grandfather said."],
             ["Are you a hero? You look like a hero. Sort of."]]
    for i, near in enumerate([(24, 12), (18, 20), (33, 20), (10, 16), (26, 25)]):
        c = sp(near)
        mb.npc("Citizen", c[0], c[1], CITIZEN[i], Ev().say(CITIZEN[i], lines[i]), direction=2, move_type=1)
    for (x, y) in [(20, 4), (25, 4), (20, 9), (25, 9), (20, 24), (25, 24)]:
        mb.light('torch', x, y - 2)
    return mb


# ---------------------------------------------------------------------------
# 102  Kaiserpalast: the throne room
# ---------------------------------------------------------------------------
def gen_palast():
    g = Gen(28, 22, 4, seed=102)
    T.rooms_and_halls(g, [(3, 3, 24, 18)], [([(13, 18), (13, 21)], 3)], *DUN.BLOCK, DUN.ROCK, wall_h=2)
    g.paint(g.rect(12, 5, 14, 21), DUN.CARPET)
    g.paint(g.rect(9, 5, 17, 7), DUN.CARPET)
    g.stamp(13, 6, [(0, -1, 499), (0, 0, 507)], force=True)
    for y in (10, 14):
        for x in (7, 19):
            g.stamp(x, y, T.PILLAR, force=True)
    g.finish()
    return g


def palast():
    g = gen_palast()
    mb = MapBuild(PALAST, NAMES[PALAST], g.m, display=NAMES[PALAST])
    mb.props(note="<Area Name: Kaiserpalast>\n<No Rank HUD>", bgm=('Castle1', 55))
    for x in (12, 13, 14):
        mb.add("Exit", x, 21, [pg(Ev().se('Move1', 60).transfer(LICHTENHALL, 23, 36, 2, 0), trigger=1, priority=0)])
    mb.add("Empress", 13, 7, [pg(None, char=EMPRESS.char[0], index=EMPRESS.char[1], direction=2, priority=1)])
    for x in (10, 16):
        mb.add("Guard", x, 9, [pg(Ev().say(GUARD_LH, ["The Imperial Guard. We were at the Sonnwende too. We",
                                                      "didn't see her either."]),
                                  char='Actor3', index=6, direction=2, priority=1)])
    el = Ev()
    el.wait(10)
    el.say(EMPRESS, ["Kanta of the Guild. Tsukishiro Yukino. The living armor.",
                     "And the dead general, I'm told, though I can't see her."])
    el.say(HANMA, ["You wouldn't want to, Majesty."], 'smile')
    el.say(EMPRESS, ["Kujō Sayaka, by the grace of the Dawn, and so on. I let",
                     "a demon hold my hand for a year. I laughed at her jokes.",
                     "She chose my wine."])
    el.say(EMPRESS, ["Asahina Rin's letter asks me for a sword and for my",
                     "legions. The sword, it seems, you have already taken back.",
                     "Keep it. It was never mine; it was only in my vault."])
    el.say(EMPRESS, ["The legions march north tomorrow. Twenty thousand. Tell",
                     "the princess the Empire remembers the Wall exists. Late,",
                     "and ashamed, but it remembers."])
    el.say(KANTA, ["Thank you, Majesty."], 'calm')
    el.say(EMPRESS, ["Don't. Go and find the other three. Kirishima at the",
                     "guild has been reading old records all night, I hear. He",
                     "reads everything. It's the only thing he does."])
    el.gold(20000)
    el.notice(["The Empress's gift: \\MONEY[20000]."])
    el.quest_done(Q_EMPRESS)
    el.switch(S_AUDIENCE7)
    mb.autorun("Audience", el)
    return mb


# ---------------------------------------------------------------------------
# 103  Kaiserarena: the Sonnwende tournament
# ---------------------------------------------------------------------------
def gen_arena():
    g = Gen(36, 30, 2, seed=103)
    g.paint(g.all(), OUT.SAND)
    floor = g.ellipse(17.5, 14, 11.5, 8.5)
    stands = g.ellipse(17.5, 14, 16.5, 13) - floor
    g.cliff(stands - g.rect(17, 22, 18, 29), 97, 105, height=2)       # sandstone tiers
    for (x, y) in g.all() - g.ellipse(17.5, 14, 16.5, 13) - g.rect(16, 22, 19, 29):
        for z in range(4):
            g.set(x, y, z, 0)
    g.paint(g.rect(16, 22, 19, 29), OUT.SAND_TILES)
    # the imperial box: a marble balcony at the top of the stands
    box = g.rect(14, 1, 21, 3)
    g.paint(box, OUT.MARBLE[0], 1)
    # banners
    for x in (8, 27):
        g.stamp(x, 4, [(0, -1, 352), (0, 0, 360)], force=True)
    g.finish()
    return g


def arena():
    g = gen_arena()
    mb = MapBuild(ARENA, NAMES[ARENA], g.m, display=NAMES[ARENA])
    mb.props(note="<Area Name: Kaiserarena>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Battle2', 55),
             bgs=('People2', 45), battleback=('Colosseum', 'Colosseum'))
    for x in (16, 17, 18, 19):
        mb.add("Gate", x, 29, [pg(Ev().if_switch(S_THEFT, True,
                                                 lambda b: b.text(["The gate is barred. Tsumugi went down, not out."]),
                                                 lambda b: (b.se('Move1', 60), b.transfer(LICHTENHALL, 37, 15, 2, 0))),
                                  trigger=1, priority=0)])
    # spectators on the stands (decoration)
    import random
    rng = random.Random(3)
    for (x, y) in [(6, 8), (9, 4), (26, 4), (30, 9), (5, 14), (31, 15), (7, 20), (29, 20), (11, 3), (24, 3)]:
        sheet, idx = rng.choice([('People1', 0), ('People1', 3), ('People2', 4), ('People4', 3), ('People3', 6)])
        mb.add("Crowd", x, y, [pg(None, char=sheet, index=idx, direction=2, priority=1, step_anime=True)])
    # the Empress and her lady in the box
    emp = mb.add("Empress", 17, 2, [pg(None, char=EMPRESS.char[0], index=EMPRESS.char[1], direction=2, priority=1)])
    tsu = mb.add("Lady Tsumugi", 18, 2, [pg(None, char=TSUMUGI.char[0], index=TSUMUGI.char[1], direction=2, priority=1),
                                         pg(None, sw=S_THEFT, priority=0)])
    # the arena master and the healer by the gate
    def rounds(e):
        e.if_switch(S_REG, False, lambda b: b.say(ARENAMASTER, ["Guild team? Registered? No? The guild's on the cross",
                                                                "street, west of the plaza. No token, no fight."]),
                    lambda b: b.if_switch(S_R1, False, round1,
                                          lambda c: c.if_switch(S_R2, False, round2,
                                                                lambda d: d.if_switch(S_R3, False, round3,
                                                                                      lambda f: f.if_switch(S_R4, False, final,
                                                                                                            done)))))
    def ready(e, name, text, then):
        e.say(ARENAMASTER, text)
        e.choices(["Fight: %s" % name, "Not yet"], [then, None], cancel=1)
    def round1(e):
        ready(e, "Round one", ["Ishikawa, arena master. First round: the Eiserne Brüder,",
                               "three mercenaries from Ostmark. Fight fair, the crowd",
                               "likes blood but the Empress doesn't."], fight1)
    def fight1(e):
        intro(e, "Round one! The Eiserne Brüder!")
        e.battle(T3["Runde 1: Eiserne Brüder"])
        e.switch(S_R1)
        win(e, ["The crowd roars. The Brothers limp off, grinning.", "They'll drink to you later."])
    def round2(e):
        ready(e, "Round two", ["Round two isn't a team. It's a beast. The Emperor's",
                               "father caught it in the Glutsand. Seven heads, give or",
                               "take. Rank B, mind."], fight2)
    def fight2(e):
        intro(e, "Round two! The Arenabestie!")
        e.battle(T3["Runde 2: Arenabestie"])
        e.switch(S_R2)
        win(e, ["The beast goes down, all seven heads of it. Somewhere in", "the stands, somebody faints."])
    def round3(e):
        ready(e, "Round three", ["Semifinal: the Klingen von Ostmark. A captain, a mage,",
                                 "and a knife from the south. Rank B, all three. They",
                                 "don't lose often."], fight3)
    def fight3(e):
        intro(e, "Round three! The Klingen von Ostmark!")
        e.battle(T3["Runde 3: Klingen von Ostmark"])
        e.switch(S_R3)
        win(e, ["The Blades salute you as they go. The captain says", "something about next year."])
    def final(e):
        ready(e, "The final", ["The final. Kanemoto Gōki, eight years champion, and his",
                               "shield-mates. He's never lost. He's never been hit by a",
                               "light-sword, either."], fight4)
    def fight4(e):
        intro(e, "The final! Kanemoto Gōki!")
        e.battle(T3["Finale: Kanemoto Gōki"])
        e.switch(S_R4)
        ceremony(e)
    def done(e):
        e.say(ARENAMASTER, ["Gods. Gods. The Unterhallen, girl. Get after her."])
    def intro(e, line):
        e.fadeout()
        e.se('Applause1', 90)
        e.fadein()
        e.text([line])
    def win(e, lines):
        e.se('Applause2', 90)
        e.text(lines)
        e.say(HEALER, ["Sit, sit. Let me look at you before the next round."])
        e.recover_all()
    def ceremony(e):
        e.se('Applause2', 100)
        e.wait(20)
        e.narrate(["Kanemoto Gōki goes down on one knee in the sand and laughs,",
                   "and the Kaiserarena comes to its feet. Eight years. Gone,",
                   "to a vessel, a ghost, a living armor and a saint."])
        e.say(GOKI, ["Well. Well well. Worth it. Go on, girl, take your sword."])
        e.text(["Gōki takes the champion's wreath off his own head and",
                "drops it on Kanta's."])
        e.armor(FA["Siegerkranz"], 1)
        e.notice(["Received the \\C[6]Siegerkranz\\C[0]."])
        e.say(EMPRESS, ["The champions of the Sonnwende! Come up, come up. The",
                        "prize: an old sword from our vault. The Morgenklinge,",
                        "the heralds tell me. Isn't it pretty?"])
        e.fadeout()
        e.transfer(ARENA, 17, 9, 8, 0)
        e.fadein()
        e.say(EMPRESS, ["Tsumugi, dear, the sword."])
        e.say(TSUMUGI, ["Of course, Majesty."])
        e.balloon(tsu, 8)
        e.say(TSUMUGI, ["…Four. You have four with you. Oh, he will be so cross",
                        "with me. I was supposed to have this sword before you",
                        "ever got near it, little vessel."])
        e.se('Twine', 100, 70)
        e.flash((230, 230, 230, 200), 20)
        e.text(["Threads shoot out of the lady's sleeves, hundreds of them,",
                "and wrap the Empress, the guards, the heralds. Her face",
                "splits along seams that were never there."])
        e.say(HANMA, ["Tsumugi, the Web-Weaver! The Spinnenkreis has had a",
                      "spider in the imperial box all along! After her, my",
                      "Lord!"], 'command')
        e.say(TSUMUGI, ["Catch me, then. Down, down, down."])
        e.se('Crash', 100, 70)
        e.shake(6, 6, 30)
        e.set_image(tsu, '', 0)
        e.text(["She leaps from the box, lands in the sand behind you",
                "and goes through the arena floor as if it were water.",
                "Where she went in, a hole into the dark."])
        e.say(ARENAMASTER, ["The Unterhallen! The old halls under the city. They",
                            "run all the way under the Morgendom."])
        e.quest_done(Q_TURNIER)
        e.quest_new(Q_WEB)
        e.switch(S_THEFT)
    el = Ev()
    rounds(el)
    mb.npc("Arena Master", 16, 24, ARENAMASTER, el, direction=8)
    el = Ev().say(HEALER, ["Arena healer. Sit, I'll patch you."])
    el.se('Heal3')
    el.recover_all()
    mb.npc("Healer", 19, 24, HEALER, el, direction=8)
    # the hole in the arena floor
    hole = mb.add("Hole", 17, 12, [pg(None, priority=0),
                                   pg(Ev().text(["A hole in the sand, lined with silk, going down into the",
                                                 "dark."]).choices(["Climb down", "Not yet"],
                                                                   [lambda b: (b.se('Move1', 60),
                                                                               b.transfer(KATAKOMBEN, 20, 31, 8, 0)),
                                                                    None], cancel=1),
                                      sw=S_THEFT, char='!Other1', index=4, direction=2, priority=1)])
    return mb


# ---------------------------------------------------------------------------
# 104  Morgendom: the cathedral of the Dawn
# ---------------------------------------------------------------------------
def gen_morgendom():
    g = Gen(24, 28, 3, seed=104)
    T.interior(g, [(3, 3, 20, 25)], *INS.MARBLE_PILLARS, INS.MARBLE)
    g.paint(g.rect(10, 6, 13, 25), INS.RUG_RED2)
    # altar, candelabra, organ, pews, statues
    g.stamp(10, 6, [(0, 0, 448), (1, 0, 449), (2, 0, 450)], force=True)
    g.stamp(9, 6, [(0, 0, 440)], force=True)
    g.stamp(13, 6, [(0, 0, 442)], force=True)
    g.stamp(4, 6, [(0, 0, 213), (1, 0, 214), (2, 0, 215), (0, 1, 229), (1, 1, 230), (2, 1, 231)], force=True)
    for y in range(10, 22, 2):
        for x in (5, 6, 7, 16, 17, 18):
            g.stamp(x, y, [(0, 0, 122)], force=True)
    for (x, y) in [(3, 13), (20, 13), (3, 19), (20, 19)]:
        g.stamp(x, y, [(0, 0, 466)], force=True)
    g.finish()
    return g


def morgendom():
    g = gen_morgendom()
    mb = MapBuild(MORGENDOM, NAMES[MORGENDOM], g.m, display=NAMES[MORGENDOM])
    mb.props(note="<Area Name: Morgendom>\n<No Rank HUD>", bgm=('Theme3', 50), bgs=('Clock', 20))
    for x in (11, 12):
        mb.add("Exit", x, 25, [pg(Ev().se('Move1', 60).transfer(LICHTENHALL, 8, 11, 2, 0), trigger=1, priority=0)])
    def kiyoko(e):
        e.if_switch(S_TSUMUGI, True, after, lambda b: b.if_switch(S_KIYOKO, True, again, first))
    def first(e):
        e.say(KIYOKO, ["Amane Kiyoko, high priestess of the Morgendom. You have",
                       "a dead general standing behind you, child, and she's",
                       "staring at my ceiling."])
        e.say(HANMA, ["I've seen it before. When it was new."], 'calm')
        e.say(KANTA, ["We're looking for the Morgenklinge."], 'calm')
        e.say(KIYOKO, ["Of course you are. Everyone is, all of a sudden."])
        e.say(KIYOKO, ["…The Morgenklinge is this year's tournament prize. The",
                       "Empress thinks it is a pretty old sword. It sat in her",
                       "vault for three hundred years and nobody remembered."])
        e.say(KIYOKO, ["Win it. Bring it to me before you do anything clever",
                       "with it. Guild teams may enter the Sonnwende: the guild",
                       "on the cross street takes the names."])
        e.say(YUKINO, ["…"])
        e.say(KIYOKO, ["And Tsukishiro. You came back after all. I prayed for",
                       "the Morgenwacht every morning for twelve years."])
        e.say(YUKINO, ["…Thank you."])
        e.quest_new(Q_TURNIER)
        e.switch(S_KIYOKO)
    def again(e):
        e.say(KIYOKO, ["The guild takes the names. The arena takes the rest."])
    def after(e):
        e.say(KIYOKO, ["The bells are ringing again. That's you. Go with the",
                       "Dawn, child. The Guild's archivist has something for you."])
    el = Ev()
    kiyoko(el)
    mb.npc("Amane Kiyoko", 11, 8, KIYOKO, el, direction=2)
    nun = npc_speaker("Novizin", "People4", 7)
    mb.npc("Novice", 15, 23, nun, Ev().say(nun, ["The Unterhallen? The door is behind the altar, but it's",
                                                "sealed. Nobody has been down since my grandmother's time."]),
           direction=2)
    return mb


# ---------------------------------------------------------------------------
# 105  Unterhallen: the old halls under the city
# ---------------------------------------------------------------------------
def gen_katakomben():
    g = Gen(40, 34, 4, seed=105)
    rooms = [(17, 26, 23, 32), (15, 16, 25, 23), (3, 3, 12, 12), (28, 3, 37, 12), (3, 16, 11, 25), (28, 16, 37, 25),
             (16, 3, 24, 11)]
    halls = [([(20, 23), (20, 26)], 3), ([(15, 21), (11, 21)], 3), ([(25, 21), (28, 21)], 3),
             ([(7, 16), (7, 12)], 2), ([(33, 16), (33, 12)], 2), ([(12, 8), (16, 8)], 3), ([(24, 8), (28, 8)], 3)]
    open_ = T.rooms_and_halls(g, rooms, halls, *DUN.DARK_BRICK, DUN.ROCK2, wall_h=2)
    free = {c for c in open_ if g.kind_at(*c) == DUN.ROCK2}
    g.scatter_in(free, DUN.BONES + [[(0, 0, DUN.COBWEB)], [(0, 0, DUN.COBWEB)]], 40, spacing=0)
    for (x, y) in [(5, 8), (10, 8), (30, 8), (35, 8)]:
        g.stamp(x, y, [(0, 0, 334), (1, 0, 335)], force=True)
    g.finish()
    return g


def katakomben():
    g = gen_katakomben()
    mb = MapBuild(KATAKOMBEN, NAMES[KATAKOMBEN], g.m, display=NAMES[KATAKOMBEN])
    mb.props(note="<Rank: B>\n<Area Name: Unterhallen>", bgm=('Dungeon2', 55), bgs=('Drips', 40),
             battleback=('DirtCave', 'RockCave'), encounters=CATA_ENC(), steps=26)
    mb.add("Rope", 20, 32, [pg(Ev().se('Move1', 60).transfer(ARENA, 17, 13, 2, 0), trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The Unterhallen: the city's first cellars, older than the",
                "Morgendom. Silk everywhere, grey and thick as fleece, and",
                "in the silk, shapes the size of people."])
    el.say(FALIN, ["Those are people."], 'hurt')
    el.say(HANMA, ["Cocoons. Some of them are still breathing. Cut them out",
                   "if you can: she'll be feeding on them."], 'stern')
    el.quest_desc(Q_WEB, "Tsumugi fled into the Unterhallen with the Morgenklinge. The cocoons hold missing citizens: "
                         "free them. Her lair is at the top of the halls, under the Morgendom.")
    mb.autorun("Unterhallen", el)
    # cocoons: each a fight (the silk fights back), the person inside freed
    for i, (x, y) in enumerate([(6, 22), (33, 21), (5, 6), (35, 9), (19, 18)]):
        e = Ev()
        e.text(["A cocoon of grey silk. Something inside twitches."])
        e.choices(["Cut it open", "Leave it"], [lambda b: (b.battle(T3["Spinnen & Kokon"]),
                                                          b.se('Slash1'),
                                                          b.text(["A man tumbles out of the silk, grey-faced, alive. He",
                                                                  "runs for the rope without a word."]),
                                                          b.var(V_COCOONS, 1, '+'),
                                                          b.self_switch('A')), None], cancel=1)
        mb.add("Cocoon", x, y, [pg(e, char='!Other1', index=2, direction=2, priority=1),
                                pg(None, self_sw='A', priority=0)])
    # the way up to her hall
    def up(e):
        e.text(["Stairs going up under the Morgendom, thick with silk. At",
                "the top, a great space full of threads, humming."])
        e.choices(["Go up", "Not yet"], [lambda b: (b.se('Move1', 60), b.transfer(SPINNENHALLE, 14, 22, 8, 0)), None],
                  cancel=1)
    mb.add("Stairs", 20, 4, [pg((lambda e: (up(e), e)[1])(Ev()), trigger=0, priority=1)])
    chest(mb, "Chest", 36, 23, lambda e: (e.item(FI["Äther"], 2), e.gold(9000)), "Found 2 Äther and \\MONEY[9000].")
    chest(mb, "Chest", 4, 24, lambda e: e.armor(FA["Arenahelm"], 1), "Found an Arenahelm.")
    chest(mb, "Chest", 23, 6, lambda e: e.item(FI["Manastein (B)"], 1), "Found a Manastein (B).")
    mb.light('cave_dark', 0, 0, tile=False)
    for (x, y) in [(20, 26), (20, 16), (7, 3), (33, 3), (7, 16), (33, 16)]:
        mb.light('torch', x, y)
    mb.follow_light('beam', 20, 31)
    return mb


# ---------------------------------------------------------------------------
# 106  Spinnenhalle: Tsumugi's web under the Morgendom
# ---------------------------------------------------------------------------
def gen_spinnenhalle():
    g = Gen(28, 26, 4, seed=106)
    open_ = T.cave(g, g.ellipse(14, 12, 11, 10) | g.rect(12, 20, 16, 24), *DUN.DARK_ROCK, DUN.PURPLE, wall_h=2)
    T.void_beyond(g, open_, 1)
    free = {c for c in open_ if g.kind_at(*c) == DUN.PURPLE}
    g.scatter_in(free - g.rect(11, 8, 17, 16), [[(0, 0, DUN.COBWEB)]], 30, spacing=0)
    g.finish()
    return g


def spinnenhalle():
    g = gen_spinnenhalle()
    mb = MapBuild(SPINNENHALLE, NAMES[SPINNENHALLE], g.m, display=NAMES[SPINNENHALLE])
    mb.props(note="<Rank: B>\n<Area Name: Spinnenhalle>", bgm=('Dungeon4', 55), bgs=('Darkness', 35),
             battleback=('DemonicWorld', 'DemonicWorld'))
    mb.add("Stairs", 14, 23, [pg(Ev().if_switch(S_TSUMUGI, True,
                                               lambda b: (b.se('Move1', 60), b.transfer(KATAKOMBEN, 20, 5, 2, 0)),
                                               lambda b: b.text(["Not now. She's right there."])),
                                 trigger=1, priority=0)])
    tsu = mb.add("Tsumugi", 14, 10, [pg(None, char=TSUMUGI.char[0], index=TSUMUGI.char[1], direction=2, priority=1),
                                     pg(None, sw=S_TSUMUGI, priority=0)])
    el = Ev()
    el.narrate(["The bottom of the Unterhallen is a web the size of a",
                "cathedral. Right above it, through the stone, the bells of",
                "the Morgendom are ringing the hour."])
    el.narrate(["In the middle of the web, Tsumugi sits with the",
                "Morgenklinge across her knees, humming along."])
    el.say(TSUMUGI, ["Every one of them signed something, you know. A contract.",
                     "A promise. A debt. I only ever collect what I'm owed."])
    el.say(KANTA, ["And what do they owe you?"], 'calm')
    el.say(TSUMUGI, ["Oh, everything. Eventually. Everyone does."])
    el.say(HANMA, ["Here, under the dawn seal, she is weaker than she ought",
                   "to be, my Lord. Rank B, no more. That sword burns her to",
                   "hold. Take it back."], 'command')
    el.battle(T3["Tsumugi"])
    el.if_switch(SW('C7: Breakthrough B'), False, late_break_b)
    el.switch(S_TSUMUGI)
    el.wait(20)
    el.se('Collapse3')
    el.text(["The Web-Weaver comes apart the way a web does, all at",
             "once, into drifting grey threads. The sword falls out of",
             "them and rings on the stone."])
    el.say(TSUMUGI, ["…He wanted the labyrinth seal. Under the dome. I was going",
                     "to give it to him for his birthday."])
    el.set_image(tsu, '', 0)
    regalia_gain(el, "Morgenklinge", "1 of 4")
    el.say(HANMA, ["…Akira's sword. The first time I saw it, it was killing",
                   "a thing like her. The last time, it was pointed at me."], 'hurt')
    el.say(FALIN, ["Hanma."], 'calm')
    el.say(HANMA, ["I'll tell you. All of you. When we have the second one.",
                   "I promise."], 'calm')
    el.quest_done(Q_WEB)
    el.fadeout()
    el.transfer(MORGENDOM, 11, 12, 8, 0)
    el.fadein()
    el.say(KIYOKO, ["The bells. Did you hear the bells? They rang all through",
                    "it, and they didn't stop. Show me."])
    el.text(["The high priestess holds the Morgenklinge up to the",
             "windows, and the morning comes in through the glass and",
             "runs along the blade like water."])
    el.say(KIYOKO, ["Yes. That's it. That's the first one. The Empress is",
                    "asking for you, and she is very, very embarrassed."])
    el.rest_point(LICHTENHALL, 22, 3, 2)
    mb.autorun("The Web", el)
    mb.light('ash_night', 0, 0, tile=False)
    return mb


# ---------------------------------------------------------------------------
# 107  Gilde Lichtenhall; 108 Zur Arenatreppe
# ---------------------------------------------------------------------------
def late_break_b(e):
    """The breakthrough to B still happens if the Web-Weaver fell before the troop page ran."""
    e.say(HANMA, ["My Lord, the seal is still ringing. Take it, now!"], 'command')
    e.se('Magic3', 90, 80)
    e.flash((255, 240, 200, 255), 60)
    e.breakthrough()
    e.switch(SW('C7: Breakthrough B'))


def gen_room(seed, rug, furniture):
    g = Gen(20, 14, 3, seed=seed)
    T.interior(g, [(2, 2, 17, 12)], *INS.WOOD_WALL, INS.WOOD)
    if rug:
        g.paint(g.rect(7, 6, 12, 9), rug)
    for (x, y, tiles) in furniture:
        g.stamp(x, y, tiles, force=True)
    g.finish()
    return g


def gilde():
    g = gen_room(107, INS.RUG_GREEN, [(4, 5, [(0, 0, 136), (1, 0, 137), (2, 0, 138)]), (12, 3, [(0, 0, 128), (1, 0, 129)]),
                                      (14, 7, [(0, 0, 112), (1, 0, 113)]), (13, 7, [(0, 0, 120)]), (16, 7, [(0, 0, 120)]),
                                      (15, 4, [(0, -1, 144), (0, 0, 152)])])
    mb = MapBuild(GILDE_LH, NAMES[GILDE_LH], g.m, display=NAMES[GILDE_LH])
    mb.props(note="<Area Name: Gilde Lichtenhall>\n<No Rank HUD>", bgm=('Town6', 50))
    mb.add("Exit", 9, 12, [pg(Ev().se('Move1', 60).transfer(LICHTENHALL, 7, 25, 2, 0), trigger=1, priority=0)])
    def kiri(e):
        e.if_switch(S_AUDIENCE7, True, record,
                    lambda b: b.if_switch(S_REG, True,
                                          lambda c: c.say(KIRISHIMA, ["You're entered. The arena is east of the plaza."]),
                                          register))
    def register(e):
        e.say(KIRISHIMA, ["Kirishima Daigo, archivist, branch master, and whatever",
                          "else nobody else wants to be. The Sonnwende? Guild",
                          "teams may enter. Rank C at least."])
        e.say(KIRISHIMA, ["\\N[4]. Four of you, though one's hard to count. Fine.",
                          "Here's your token. Don't die, the paperwork is awful."])
        e.item(K3["Turniermarke"], 1)
        e.notice(["Received the \\C[6]Turniermarke\\C[0]."])
        e.switch(S_REG)
        e.quest_desc(Q_TURNIER, "Registered. Four rounds in the Kaiserarena, east of the plaza.")
    def record(e):
        e.if_script("!$gameSystem._c7_record", give_record,
                    lambda b: b.say(KIRISHIMA, ["The lantern is with the foxes. The horn is with the",
                                                "dwarfs' trolls. The crown is at sea. Go."]))
    def give_record(e):
        e.say(KIRISHIMA, ["There you are. I read the record of 313 last night. The",
                          "Guild writes everything down; nobody ever reads it."])
        e.say(KIRISHIMA, ["After the Dawn War the regalia were scattered, so no",
                          "king could own them. The Morgenklinge to the Emperor:",
                          "you have it. The Sternlaterne to the fox shrine in the"])
        e.say(KIRISHIMA, ["Tiefenwald. The Heldenhorn to Eisenberg, to a dwarf king",
                          "who liked shiny things. The Aschenkrone went to sea,",
                          "with a captain nobody trusted. That's all."])
        e.say(HANMA, ["…I remember the day we gave them away. Akira wept. I",
                      "didn't."], 'stern')
        e.item(K3["Gildenabschrift"], 1)
        e.notice(["Received the \\C[6]Gildenabschrift\\C[0]."])
        e.say(KIRISHIMA, ["The Tiefenwald is west, three days by the Waldweg.",
                          "Hirschheim is the town. Take the west road from the",
                          "city gate; the Guild's carts will carry you."])
        e.script("$gameSystem._c7_record = true;")
        e.switch(S_C7_END)
        e.plugin('Story_Core', 'ChapterCard', {'title': "Die Morgenklinge", 'subtitle': "1 von 4", 'duration': 160},
                 'Chapter Card')
        e.notice(["\\C[6]Travel\\C[0]: the city gate now takes you anywhere you",
                  "have already been, and to the roads of the regalia."])
    el = Ev()
    kiri(el)
    mb.npc("Kirishima Daigo", 5, 4, KIRISHIMA, el, direction=2)
    adv = npc_speaker("Abenteurerin", "Actor1", 1)
    mb.npc("Adventurer", 14, 9, adv, Ev().say(adv, ["Rank C and the Sonnwende? Brave. I'll bet on you. A",
                                                   "little."]), direction=4)
    return mb


def gasthaus():
    g = gen_room(108, INS.RUG_RED, [(4, 5, [(0, 0, 136), (1, 0, 137), (2, 0, 138)]), (12, 6, [(0, 0, 112), (1, 0, 113)]),
                                    (11, 6, [(0, 0, 120)]), (14, 6, [(0, 0, 120)]), (12, 9, [(0, 0, 112), (1, 0, 113)]),
                                    (15, 3, [(0, 0, 196)]), (16, 3, [(0, 0, 196)])])
    mb = MapBuild(GASTHAUS_LH, NAMES[GASTHAUS_LH], g.m, display=NAMES[GASTHAUS_LH])
    mb.props(note="<Area Name: Zur Arenatreppe>\n<No Rank HUD>", bgm=('Town2', 50))
    mb.add("Exit", 9, 12, [pg(Ev().se('Move1', 60).transfer(LICHTENHALL, 15, 25, 2, 0), trigger=1, priority=0)])
    def sleep(e):
        e.if_gold(3000, '>=', lambda b: (b.gold(-3000), b.common(CE['Inn Sleep']),
                                         b.rest_point(GASTHAUS_LH, 9, 10, 8)),
                  lambda b: b.say(INNKEEP, ["Thirty silver, love. Come back when you've got it."]))
    el = Ev().say(INNKEEP, ["Hoshi. A bed's 3 gk, the Sonnwende week. Breakfast",
                            "thrown in, and the view of the arena steps."])
    el.choices(["Stay the night (3 gk)", "No thanks"], [sleep, None], cancel=1)
    mb.npc("Innkeeper", 5, 4, INNKEEP, el, direction=2)
    drunk = npc_speaker("Gast", "People2", 4)
    mb.npc("Guest", 13, 7, drunk, Ev().say(drunk, ["Gōki's never lost. Never. …Buy me a drink and I'll tell",
                                                   "you about the time he almost did."]), direction=2)
    return mb
