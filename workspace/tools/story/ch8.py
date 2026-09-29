"""Chapter 8: Wald und Tiefe. The Waldweg into the Tiefenwald, Hirschheim, the fox shrine and Shirogane's game
(the Sternlaterne), Eisenberg and the Tiefgrube (the Troll King and the Heldenhorn), the Urwald and the
Hirschthron (Mukuro, the Hollow Magus). Hanma tells her story."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story import foes, foes3
from story.ids import *
from story.ch1 import chest
from story.ch2 import camp_fire
from story.cast import *
from story.ch6 import V_REGALIA
from story.ch7 import regalia_gain, S_C7_END
from story import terrain as T
from story.terrain import Gen, OUT, DUN, INS, auto

KI = foes.KEY
K3 = foes3.KEY
FI = foes.ITEMS
FA = foes.ARMORS
FW = foes.WEAPONS
T3 = foes3.TR

# ----------------------------------------------------------------------- quests
Q_WALD = Quest(29, "Die Sternlaterne", "Kirishima Daigo", "Tiefenwald, Fuchsschrein",
               "The Guild record of 313: the Sternlaterne went to the fox shrine in the Tiefenwald. Hirschheim is the "
               "town; the shrine is a day's walk east of it.",
               "The Waldweg to Hirschheim, then the shrine.")
Q_HORN = Quest(30, "Das Heldenhorn", "Kirishima Daigo", "Eisenberg, Tiefgrube",
               "The Heldenhorn went to Eisenberg with a dwarf king who liked shiny things. Eisenberg is over the "
               "mountain north of Hirschheim.",
               "Hirschheim's north road to Eisenberg.")
Q_PACK = Quest(31, "Der Rudelherr", "Ōkami Sōta", "Waldweg",
               "A packlord drunk on miasma is killing Sōta's clan on the Waldweg. Optional.",
               "The clearing north of the Waldweg.")
Q_THRONE = Quest(32, "Der Hirschthron", "Kagura Yui", "Urwald, Hirschthron",
                 "Hollow men walk out of the Urwald toward the Hirschthron, the old seal at the heart of the forest. "
                 "The leshy of the Urwald lets no one through who doesn't carry the old horn and the old light.",
                 "Hirschheim's south road into the Urwald.")

# ----------------------------------------------------------------------- switches
S_C8 = SW('C8: Waldweg')
S_HH = SW('C8: Hirschheim')
S_PACK = SW('C8: Packlord Down')
S_NANAMI = SW('C8: Shrine')
S_RIDDLE = SW('C8: Riddle')
S_LATERNE = SW('C8: Sternlaterne')
S_HANMA_TALE = SW('C8: Hanma Told')
S_EB = SW('C8: Eisenberg')
S_LAMP = SW('C8: Grubenlampe')
S_MINERS = SW('C8: Miners Found')
S_HORN = SW('C8: Heldenhorn')
S_GIFT = SW('C8: Kusakis Gabe')
S_LESHY = SW('C8: Leshy')
S_MUKURO = SW('C8: Mukuro Down')
S_C8_END = SW('C8: Chapter Done')

FOREST_ENC = lambda: [(T3["Werwölfe x2"], 5, ()), (T3["Werwolf & Irrlichter"], 4, ()), (T3["Kitsune & Irrlicht"], 2, ())]
MINE_ENC = lambda: [(T3["Grubenwichte x3"], 5, ()), (T3["Höhlentrolle x2"], 3, ()), (T3["Troll & Schamane"], 3, ())]
URWALD_ENC = lambda: [(T3["Urwaldhüter x2"], 4, ()), (T3["Hüter & Geister"], 4, ()), (T3["Hohle Diener x3"], 4, ()),
                      (T3["Magier & Diener"], 3, ())]




def build():
    return [waldweg(), hirschheim(), fuchsschrein(), urwald(), hirschthron(), eisenberg(), tiefgrube(),
            tiefgrube_unten(), trollhalle()]


def telling(e):
    """Hanma's story (after the second regalia)."""
    e.narrate(["That night Hanma doesn't stand behind the fire. She sits",
               "down at it, which she never does, and looks at the",
               "lantern for a long time."])
    e.say(HANMA, ["I promised. When we had the second one."], 'calm')
    e.say(HANMA, ["Seven hundred and thirty-five years ago I was a general",
                  "of the Dawn Host. Sōryū Akira's general. One of five.",
                  "The youngest, and the angriest."], 'calm')
    e.say(HANMA, ["The Demon Lord had burned my city when I was nine. I",
                  "wanted every demon in the world dead, and everything that",
                  "had touched one, and everything that might, later."], 'stern')
    e.say(HANMA, ["So I purged. Villages the miasma had brushed. Wells. Once",
                  "a whole valley, because two of the dead there had been",
                  "seen to twitch. The Death arts, you've seen them. I was"], 'stern')
    e.say(HANMA, ["very good at them."], 'stern')
    e.say(FALIN, ["…And Akira?"], 'calm')
    e.say(HANMA, ["Akira took my command away at Frostheim, the last winter",
                  "of the war. In front of the Host. I was dying by then,",
                  "a spear through me, and I was so angry I couldn't see."], 'hurt')
    e.say(HANMA, ["Something came to me, lying there in the snow. A merchant",
                  "in brass, with a contract for anger. Keep fighting, he",
                  "said. Forever. Purge everything. Only sign."], 'hurt')
    e.say(KANTA, ["Gōen."], 'calm')
    e.say(HANMA, ["Akira tore the contract out of my hands. She refused it",
                  "for me. So I died, angry, unbought, and I stayed angry",
                  "for seven hundred years, in the dark, until a thread"], 'calm')
    e.say(HANMA, ["pulled tight and there was a girl with a light in her",
                  "hand, waking up in a cave."], 'smile')
    e.say(HANMA, ["\"The General who was refused.\" That's what he calls me.",
                  "He's right. It's the best thing anyone ever did for me."], 'calm')
    e.say(YUKINO, ["…"])
    e.say(KANTA, ["Are you still angry?"], 'calm')
    e.say(HANMA, ["…Less, my Lord. Less every day. Don't tell anyone."], 'smile')
    e.switch(S_HANMA_TALE)


# ---------------------------------------------------------------------------
# 110  Waldweg: into the Tiefenwald
# ---------------------------------------------------------------------------
def gen_waldweg():
    g = Gen(46, 32, 2, seed=110)
    g.paint(g.all(), OUT.GRASS)
    pts = [(0, 20), (8, 19), (15, 22), (23, 18), (31, 20), (38, 16), (45, 16)]
    walk = g.line(pts, 9, wobble=1.0) | g.blob(22, 7, 5.5, seed=5) | g.line([(22, 17), (22, 10)], 4)
    walk &= g.rect(0, 1, 45, 30)
    ground = T.frame(g, walk, T.FOREST, thick=3, trunk_h=2)
    road = g.line(pts, 2, wobble=1.0) & ground
    g.paint(road, OUT.GRASS_DIRT)
    g.keep_clear |= g.grow(road, 1)
    T.dress(g, ground - g.grow(road, 2), T.FOREST, trees=0.12, rocks=0.02, bushes=0.07, tufts=0.07)
    g.finish()
    return g


def waldweg():
    g = gen_waldweg()
    R = T.reach_check(g, (1, 20), [(44, 16), (22, 7)], 'Waldweg')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(WALDWEG, NAMES[WALDWEG], g.m, display=NAMES[WALDWEG])
    mb.props(note="<Rank: B>\n<Area Name: Waldweg>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field3', 60), bgs=('Wind1', 25), battleback=('Grassland', 'Forest'), encounters=FOREST_ENC(), steps=28)
    el = Ev()
    el.card("Kapitel 8", "Wald und Tiefe", 200)
    el.narrate(["West of Lichtenhall the fields end at a wall of trees",
                "older than the Empire. The Waldweg goes in under them",
                "like a road into a cave."])
    el.say(YUKINO, ["…The Tiefenwald. I was here once. With them."])
    el.say(FALIN, ["With the Morgenwacht?"], 'calm')
    el.say(YUKINO, ["Tōma liked the foxes."])
    el.quest_new(Q_WALD)
    el.switch(S_C8)
    el.rest_point(WALDWEG, 2, 20, 6)
    mb.autorun("Waldweg", el)
    for y in range(g.h):
        if (0, y) in R and (1, y) in R:
            mb.add("West", 0, y, [pg(Ev().se('Move1', 60).transfer(LICHTENHALL, 22, 3, 2, 0), trigger=1, priority=0)])
        if (g.w - 1, y) in R and (g.w - 2, y) in R:
            mb.add("East", g.w - 1, y, [pg(Ev().se('Move1', 60).transfer(HIRSCHHEIM, 1, 30, 6, 0), trigger=1,
                                           priority=0)])
    # the packlord's clearing (optional)
    lord = sp((22, 6))
    def packlord(e):
        e.text(["A clearing of flattened bracken, bones, and a stink of wet",
                "dog gone rotten. On a heap of clan totems something stands",
                "up on two legs. Its eyes are the grey of ash."])
        e.say(HANMA, ["Drunk on miasma. Whatever it was, it's mostly hunger now."], 'stern')
        e.battle(T3["Rudelherr"])
        e.switch(S_PACK)
        e.text(["The packlord falls, the grey goes out of its eyes, and it",
                "is only a big old wolf lying in the bracken."])
        e.quest_desc(Q_PACK, "The packlord is dead. Tell Ōkami Sōta in Hirschheim.")
    mb.add("Packlord", lord[0], lord[1], [pg(Ev().if_switch(S_PACK, False, packlord), char='Monster', index=2,
                                             direction=2, priority=1, step_anime=True),
                                          pg(None, sw=S_PACK, priority=0)])
    fire = sp((33, 20))
    rest = sp((fire[0], fire[1] + 1), avoid=[fire])
    camp_fire(mb, fire[0], fire[1], WALDWEG, rest[0], rest[1], 8, ["A charcoal burners' fire ring under an oak."])
    c1 = sp((12, 24))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Großes Elixier"], 2), e.gold(12000)),
          "Found 2 Großes Elixier and \\MONEY[12000].")
    c2 = sp((26, 5))
    chest(mb, "Chest", c2[0], c2[1], lambda e: e.armor(FA["Heiligenring B"], 1), "Found a Heiligenring B.")
    return mb


# ---------------------------------------------------------------------------
# 111  Hirschheim: the town of the Tiefenwald
# ---------------------------------------------------------------------------
def gen_hirschheim():
    g = Gen(44, 40, 2, seed=111)
    g.paint(g.all(), OUT.GRASS)
    walk = g.rect(1, 2, 42, 37) | g.rect(0, 28, 1, 32) | g.rect(20, 0, 23, 2) | g.rect(20, 37, 23, 39) | \
        g.rect(42, 18, 43, 21)
    ground = T.frame(g, walk, T.FOREST, thick=2, trunk_h=2)
    paths = g.line([(0, 30), (21, 30), (21, 0)], 3) | g.line([(21, 30), (21, 39)], 3) | g.line([(21, 19), (43, 19)], 3)
    paths &= ground
    g.paint(paths, OUT.GRASS_DIRT)
    g.keep_clear |= g.grow(paths, 1)
    info = {}
    info['hall'] = T.house(g, 25, 4, 11, roof='green', wall='logs', door='double', roof_h=4, wall_h=2)
    info['inn'] = T.house(g, 6, 22, 7, roof='wood', wall='wood', door='arch')
    g.set(info['inn'][0] + 1, info['inn'][1] - 1, 3, 70)
    info['shop'] = T.house(g, 26, 22, 6, roof='green', wall='wood', door='arch')
    g.set(info['shop'][0] + 1, info['shop'][1] - 1, 3, 68)
    for (x, y, w) in [(4, 8, 6), (12, 8, 6), (4, 32, 6), (27, 31, 6), (34, 31, 6), (34, 22, 6)]:
        T.house(g, x, y, w, roof='green' if (x + y) % 2 else 'wood', wall='logs' if x % 2 else 'wood', door='arch')
    free = {c for c in ground if c not in g.blocked and c not in g.keep_clear}
    g.scatter_in(free, [OUT.TREE, OUT.TREE, OUT.PINE], 40, spacing=1)
    g.scatter_in(free, [[(0, 0, 160)], [(0, 0, 161)], [(0, 0, 162)], [(0, 0, 153)]], 30, spacing=0)
    for y in (12, 25):
        g.stamp(19, y, OUT.LAMP)
        g.stamp(24, y, OUT.LAMP)
    g.finish()
    return g, info


def hirschheim():
    g, info = gen_hirschheim()
    R = T.reach_check(g, (1, 30), [info['hall'], info['inn'], info['shop'], (21, 1), (21, 38), (42, 19)], 'Hirschheim')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(HIRSCHHEIM, NAMES[HIRSCHHEIM], g.m, display=NAMES[HIRSCHHEIM])
    mb.props(note="<Area Name: Hirschheim>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town7', 60), bgs=('Wind1', 20))
    # exits: west (Waldweg), north (Eisenberg road), east (shrine road), south (Urwald)
    for y in range(28, 33):
        mb.add("West", 0, y, [pg(Ev().se('Move1', 60).transfer(WALDWEG, 44, 16, 4, 0), trigger=1, priority=0)])
    def north(e):
        e.if_switch(S_HH, True, lambda b: (b.fadeout(), b.narrate(["Two days over the mountain on the old dwarf road,",
                                                                   "snow on the passes, and then iron doors in a",
                                                                   "cliff."]),
                                           b.switch(S_EB), b.transfer(EISENBERG, 20, 30, 8, 0), b.fadein()),
                    lambda b: b.text(["The road north climbs into the mountains."]))
    for x in range(20, 24):
        mb.add("North Road", x, 0, [pg((lambda e: (north(e), e)[1])(Ev()), trigger=1, priority=0)])
    for y in range(18, 22):
        mb.add("East Road", 43, y, [pg(Ev().se('Move1', 60).transfer(FUCHSSCHREIN, 12, 38, 8, 0), trigger=1, priority=0)])
    def south(e):
        e.if_switch(SW('C9: Urwald Burns'), True,
                    lambda b: (b.se('Move1', 60), b.transfer(URWALD_BRAND, 20, 1, 2, 0)),
                    lambda b: south_before_fire(b))
    def south_before_fire(e):
        e.if_switch(S_MUKURO, True, lambda b: (b.se('Move1', 60), b.transfer(URWALD, 20, 1, 2, 0)),
                    lambda b: b.if_script("$gameSwitches.value(%d) && $gameSwitches.value(%d)" % (S_LATERNE, S_HORN),
                                          lambda c: (c.se('Move1', 60), c.transfer(URWALD, 20, 1, 2, 0)),
                                          lambda c: c.text(["The south road goes into the Urwald. The trees there are",
                                                            "so old they have opinions, the town says, and they",
                                                            "don't open for everyone."])))
    for x in range(20, 24):
        mb.add("South Road", x, 39, [pg((lambda e: (south(e), e)[1])(Ev()), trigger=1, priority=0)])
    # arrival
    el = Ev()
    el.wait(10)
    el.narrate(["Hirschheim: a town of timber halls under trees older than",
                "any kingdom, lanterns in the branches, and beastkin with",
                "wolf ears and deer ears watching you from every door."])
    el.say(npc_speaker("Wache", "Actor2", 4), ["Strangers. The countess will want to see you. Everyone",
                                               "strange goes to the countess. The hall up the road."])
    el.quest_desc(Q_WALD, "Hirschheim. The countess Kagura Yui is in the great hall up the north road.")
    el.switch(S_HH)
    el.rest_point(HIRSCHHEIM, 2, 30, 6)
    mb.autorun("Arrival", el)
    # the hall: the countess and Sōta (on the map, in front of the hall)
    hall = info['hall']
    yui = sp((hall[0], hall[1] + 2))
    sota = sp((hall[0] + 3, hall[1] + 2))
    def countess(e):
        e.if_switch(S_MUKURO, True, lambda b: b.say(KAGURA, ["The forest is quiet. It hasn't been quiet in a year.",
                                                             "Hirschheim remembers its friends."]),
                    lambda b: b.if_script("$gameSystem._c8_met", later, first))
    def first(e):
        e.say(KAGURA, ["Kagura Yui, countess of Hirschheim. A letter from",
                       "Lichtenhall's archivist, a guild card, a dead general and",
                       "the Frost Saint. Hohenwacht remembers us when it needs"])
        e.say(KAGURA, ["something. What do you need?"])
        e.say(KANTA, ["The fox shrine. A horn in Eisenberg. And whatever you",
                      "need first, apparently."], 'wry')
        e.say(KAGURA, ["…Honest, at least."])
        e.say(KAGURA, ["The shrine is east, a day's walk. Its guardian took the",
                       "lantern you want a hundred years ago and calls it keeping.",
                       "Be polite to her. Never give her your real name."])
        e.say(KAGURA, ["Eisenberg is over the mountain, north. The dwarves have",
                       "trolls in their deep mine, and they've been shouting",
                       "about it for a month."])
        e.say(KAGURA, ["And what I need: the Urwald is sick. Things that used to",
                       "be people walk out of the north, through my forest, to",
                       "the Hirschthron. It's an old seal. They're digging at it."])
        e.say(HANMA, ["The Hollow Magus. Mukuro. He goes where seals are thin."], 'stern')
        e.say(KAGURA, ["The leshy won't let anyone into the Urwald who doesn't",
                       "carry the old light and the old horn. Bring both, and",
                       "I'll send you in with Kusaki's gift."])
        e.quest_new(Q_HORN)
        e.quest_new(Q_THRONE)
        e.script("$gameSystem._c8_met = true;")
    def later(e):
        e.if_script("$gameSwitches.value(%d) && $gameSwitches.value(%d)" % (S_LATERNE, S_HORN), gift,
                    lambda b: b.say(KAGURA, ["The lantern at the shrine, east. The horn in Eisenberg,",
                                             "north. Then the Urwald."]))
    def gift(e):
        e.if_switch(S_GIFT, True, lambda b: b.say(KAGURA, ["The Urwald, south. Kusaki's gift for the leshy. Go."]),
                    lambda b: (
                        b.say(KAGURA, ["The lantern and the horn. Gods. The things you carry."]),
                        b.say(KUSAKI, ["Kusaki, forester. Bread and salt for the leshy, from my",
                                       "own table. Put it on the stone at the edge of the wood.",
                                       "It'll know who sent it."]),
                        b.item(KI["Kusakis Gabe"], 1), b.notice(["Received \\C[6]Kusakis Gabe\\C[0]."]),
                        b.switch(S_GIFT),
                        b.quest_desc(Q_THRONE, "Take Kusaki's gift into the Urwald (Hirschheim's south road) and leave "
                                               "it on the stone for the leshy. Then the Hirschthron.")))
    el = Ev()
    countess(el)
    mb.npc("Kagura Yui", yui[0], yui[1], KAGURA, el, direction=2)
    mb.npc("Kusaki", *sp((hall[0] - 3, hall[1] + 2)), KUSAKI,
           Ev().say(KUSAKI, ["The Urwald was friendly, once. Rude, but friendly."]), direction=2)
    def sota_talk(e):
        e.if_switch(S_PACK, True,
                    lambda b: b.if_script("!$gameSystem._c8_pack_paid",
                                          lambda c: (c.say(SOTA, ["It is done. The clan owes you a debt, and we pay our",
                                                                  "debts."]),
                                                     c.armor(FA["Fuchsspiegel"], 1), c.gold(15000),
                                                     c.notice(["Received a Fuchsspiegel and \\MONEY[15000]."]),
                                                     c.quest_done(Q_PACK), c.script("$gameSystem._c8_pack_paid = true;")),
                                          lambda c: c.say(SOTA, ["The clan remembers."])),
                    lambda b: b.if_script("!$gameSystem._c8_pack",
                                          lambda c: (c.say(SOTA, ["Ōkami Sōta. A packlord is killing my clan on the",
                                                                  "Waldweg: north of the road, in the old clearing. It",
                                                                  "came from the north with ash on its fur."]),
                                                     c.say(HANMA, ["Steel does half to a werewolf, my Lord. The light is",
                                                                   "not steel."], 'calm'),
                                                     c.quest_new(Q_PACK), c.script("$gameSystem._c8_pack = true;")),
                                          lambda c: c.say(SOTA, ["The clearing north of the Waldweg."])))
    el = Ev()
    sota_talk(el)
    mb.npc("Ōkami Sōta", sota[0], sota[1], SOTA, el, direction=2)
    # inn and shop
    inn = info['inn']
    def sleep(e):
        e.if_gold(2000, '>=', lambda b: (b.gold(-2000), b.common(CE['Inn Sleep']), b.rest_point(HIRSCHHEIM, inn[0], inn[1] + 1, 2),
                                         b.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_LATERNE, S_HANMA_TALE), telling)),
                  lambda b: b.text(["Twenty silver. You don't have it."]))
    el = Ev().text(["The inn. Beds in the branches, 2 gk the night."])
    el.choices(["Stay the night (2 gk)", "No"], [sleep, None], cancel=1)
    mb.add("Inn", inn[0], inn[1], [pg(el, char='!Door1', index=0, direction=2, pattern=1, trigger=0, priority=1,
                                      walk_anime=False)])
    shop = info['shop']
    goods = [('item', FI["Großes Elixier"]), ('item', FI["Äther"]), ('item', FI["Starkes Riechsalz"]),
             ('item', FI["Allheilmittel"]), ('item', FI["Große Lichtphiole"]),
             ('armor', FA["Waldkrone"]), ('armor', FA["Arenahelm"]), ('armor', FA["Runenschild"]),
             ('armor', FA["Kriegerring B"]), ('armor', FA["Heiligenring B"]), ('armor', FA["Magierring B"]),
             ('weapon', FW["Sternenfäuste"])]
    trader = npc_speaker("Händlerin", "Nature", 7)
    el = Ev().say(trader, ["Forest-made and dwarf-made. The dwarf-made costs more",
                           "and lasts less, don't tell them I said so."])
    el.shop(goods)
    mb.add("Shop", shop[0], shop[1], [pg(el, char='!Door1', index=0, direction=2, pattern=1, trigger=0, priority=1,
                                        walk_anime=False)])
    for near, who, lines in [((15, 16), npc_speaker("Hirschling", "Nature", 5), ["Your dead general is scary. I like her."]),
                             ((30, 27), npc_speaker("Jägerin", "Nature", 4), ["The foxes at the shrine steal hats. And names."]),
                             ((10, 18), npc_speaker("Holzfäller", "People2", 6), ["Hollow men in the Urwald. Like walking bags of",
                                                                                   "nothing. The trees hate them."])]:
        c = sp(near)
        mb.npc("Townsfolk", c[0], c[1], who, Ev().say(who, lines), direction=2, move_type=1)
    return mb


# ---------------------------------------------------------------------------
# 112  Fuchsschrein: the fox shrine and the Spiegelwald
# ---------------------------------------------------------------------------
def gen_shrine():
    g = Gen(26, 40, 2, seed=112)
    g.paint(g.all(), OUT.GRASS)
    walk = g.rect(9, 20, 16, 39) | g.rect(4, 11, 21, 21) | g.blob(13, 5, 7.5, rough=0.25, seed=7)
    ground = T.frame(g, walk, T.FOREST, thick=3, trunk_h=2)
    steps = g.rect(11, 22, 14, 39) & ground
    for c in steps:
        g.set(c[0], c[1], 0, 1561)
    g.keep_clear |= g.grow(steps, 0)
    # lanterns up the path, the shrine
    for y in range(23, 38, 3):
        g.stamp(10, y, [(0, -1, 356), (0, 0, 364)], force=True)
        g.stamp(15, y, [(0, -1, 356), (0, 0, 364)], force=True)
    info = {'shrine': T.house(g, 9, 12, 8, roof='wood', wall='moss', door='arch', roof_h=3, wall_h=2)}
    # the Spiegelwald: a silver pool
    pool = g.ellipse(13, 5, 3.5, 2)
    g.paint(pool, OUT.ICE)
    T.dress(g, ground - steps - g.grow(pool, 1) - g.rect(8, 11, 17, 18), T.FOREST, trees=0.14, rocks=0.02,
            bushes=0.06, tufts=0.08)
    g.finish()
    return g, info


def fuchsschrein():
    g, info = gen_shrine()
    R = T.reach_check(g, (12, 38), [info['shrine'], (13, 8)], 'Fuchsschrein')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(FUCHSSCHREIN, NAMES[FUCHSSCHREIN], g.m, display=NAMES[FUCHSSCHREIN])
    mb.props(note="<Rank: B>\n<Area Name: Fuchsschrein>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Scene3', 55), bgs=('Wind2', 20), battleback=('Grassland', 'Forest'),
             encounters=[(T3["Kitsune x2"], 5, ()), (T3["Kitsune & Irrlicht"], 4, ())], steps=34)
    for x in range(11, 15):
        mb.add("Down", x, 39, [pg(Ev().se('Move1', 60).transfer(HIRSCHHEIM, 42, 19, 4, 0), trigger=1, priority=0)])
    el = Ev()
    el.narrate(["Stone steps climb the hill between hundreds of red",
                "lanterns. A hundred stone foxes watch you pass. At the",
                "top, a shrine, and a fox-eared girl sweeping the steps."])
    mb.autorun("Shrine", el)
    nanami = sp((12, 19))
    def nanami_talk(e):
        e.if_switch(S_LATERNE, True, lambda b: b.say(NANAMI, ["You played with her and won. She's been singing all",
                                                              "day. It's awful."]),
                    lambda b: b.if_switch(S_NANAMI, True,
                                          lambda c: c.say(NANAMI, ["The Spiegelwald. Behind the shrine. Be very polite."]),
                                          first))
    def first(e):
        e.say(NANAMI, ["Pilgrims? Adventurers? Oh, both. I run the guild branch",
                       "too. Everyone here does two jobs."])
        e.say(KANTA, ["We're looking for your lost mirror."], 'calm')
        e.say(NANAMI, ["…Nobody has asked about the mirror in a hundred years.",
                       "It isn't lost. Shirogane-sama took it. She's the shrine's",
                       "guardian. She says she's keeping it safe."])
        e.say(NANAMI, ["She says that about everything she steals."])
        e.say(NANAMI, ["She lives in the Spiegelwald, behind the shrine. If you",
                       "go, be polite, and never tell her your real name."])
        e.say(KANTA, ["I only have the one."], 'wry')
        e.say(NANAMI, ["Then be very polite."])
        e.switch(S_NANAMI)
        e.quest_desc(Q_WALD, "The shrine's guardian, Shirogane, keeps the 'mirror' in the Spiegelwald behind the shrine.")
    el = Ev()
    nanami_talk(el)
    mb.npc("Nanami", nanami[0], nanami[1], NANAMI, el, direction=2)
    # the stone fox's riddle (on the way up)
    fox = sp((14, 30))
    def riddle(e):
        e.text(["A stone fox on a plinth, taller than the others. As you",
                "pass, it speaks with a woman's laughing voice."])
        e.say(SHIROGANE, ["A riddle, little vessel, to pass the time. I have a face",
                          "but no eyes. I show you yourself, but backwards. The fox",
                          "kept me, and I was never what they said. What am I?"])
        e.choices(["A mirror.", "A lantern.", "A lie."],
                  [lambda b: (b.say(SHIROGANE, ["Clever. Too clever. I shall have to cheat later. Take",
                                                "this, for the pleasure."]),
                              b.item(FI["Äther"], 2), b.item(FI["Großes Elixier"], 2)),
                   lambda b: (b.say(SHIROGANE, ["Ha! Also true. Everything I say is a lie, including",
                                                "that. Take a little something."]), b.item(FI["Äther"], 1)),
                   lambda b: (b.say(SHIROGANE, ["Wrong! Oh, I do love wrong. Play with my children."]),
                              b.battle(T3["Kitsune x2"]))], cancel=-1)
        e.switch(S_RIDDLE)
    mb.add("Stone Fox", fox[0], fox[1], [pg(Ev().if_switch(S_RIDDLE, False, riddle,
                                                          lambda b: b.text(["The stone fox says nothing now. It looks pleased",
                                                                            "with itself."])),
                                           char='Nature', index=3, direction=2, priority=1)])
    # Shirogane at the silver pool
    shiro = mb.add("Shirogane", 13, 8, [pg(None, char=SHIROGANE.char[0], index=SHIROGANE.char[1], direction=2,
                                           priority=1),
                                        pg(None, sw=S_LATERNE, priority=0)])
    def game(e):
        e.text(["The heart of the Spiegelwald: a pool like a sheet of",
                "silver, and a white fox the size of a horse lying beside",
                "it, nine tails spread like a fan."])
        e.say(SHIROGANE, ["A girl in a borrowed body, with a dead general for a",
                          "shadow and a saint who won't speak. How delightful. You",
                          "want the lantern."])
        e.say(KANTA, ["The mirror."], 'calm')
        e.say(SHIROGANE, ["Mm. Then you want the lantern. It was never a mirror.",
                          "Play with me, and win, and it's yours. I'll bind eight of",
                          "my tails, so it's fair."])
        e.battle(T3["Shirogane"])
        e.switch(S_LATERNE)
        e.say(SHIROGANE, ["Ahaha! Oh, that was fun. I haven't bled in two hundred",
                          "years."])
        e.say(SHIROGANE, ["The Sternlaterne. I hid it in the shrine's story so the",
                          "wrong hands would stop looking. You're the right hands, I",
                          "think. Probably. Don't make me regret it."])
        regalia_gain(e, "Sternlaterne", "2 of 4")
        e.say(SHIROGANE, ["And the general. Hanma. I knew your Akira, you know. She",
                          "cheated at cards."])
        e.say(HANMA, ["…She did. Terribly."], 'smile')
        e.quest_done(Q_WALD)
        e.say(HANMA, ["Kanta. Tonight, at the inn in Hirschheim. I promised."], 'calm')
        e.set_image(shiro, '', 0)
    mb.add("Silver Pool", 13, 9, [pg(Ev().if_switch(S_LATERNE, False, game), trigger=1, priority=0)])
    mb.add("Shrine", info['shrine'][0], info['shrine'][1],
           [pg(Ev().text(["The shrine: offerings of fried tofu, and a sign in",
                          "careful brush strokes: THE MIRROR IS NOT LOST."]), trigger=0, priority=1)])
    return mb


# ---------------------------------------------------------------------------
# 115  Eisenberg: the dwarf city in the mountain
# ---------------------------------------------------------------------------
def gen_eisenberg():
    g = Gen(40, 34, 2, seed=115)
    g.paint(g.all(), OUT.DIRT)
    walk = g.rect(2, 4, 37, 31) | g.rect(18, 31, 22, 33)
    ground = T.frame(g, walk, dict(frame=OUT.SNOW_CLIFF), thick=3, trunk_h=3)
    streets = g.line([(20, 33), (20, 12)], 3) | g.line([(4, 20), (36, 20)], 2)
    streets &= ground
    g.paint(streets, OUT.DIRT_STONES)
    g.keep_clear |= g.grow(streets, 1)
    info = {}
    info['forge'] = T.house(g, 23, 12, 9, roof='wood', wall='darkbrick', door='double', roof_h=3, wall_h=2)
    info['inn'] = T.house(g, 5, 22, 7, roof='wood', wall='stone', door='arch')
    g.set(info['inn'][0] + 1, info['inn'][1] - 1, 3, 70)
    info['shop'] = T.house(g, 26, 23, 7, roof='wood', wall='darkbrick', door='arch')
    g.set(info['shop'][0] + 1, info['shop'][1] - 1, 3, 65)
    for (x, y, w) in [(5, 12, 7), (13, 25, 5)]:
        T.house(g, x, y, w, roof='wood', wall='stone', door='arch')
    # the mine gate in the cliff (top centre)
    info['mine'] = (20, 6)
    free = {c for c in ground if c not in g.blocked and c not in g.keep_clear}
    g.scatter_in(free, OUT.ROCKS + [[(0, 0, OUT.BARREL)], [(0, 0, 181)], [(0, 0, 180)]], 30, spacing=1)
    for y in (10, 16, 26):
        g.stamp(18, y, OUT.LAMP)
        g.stamp(22, y, OUT.LAMP)
    g.finish()
    return g, info


def eisenberg():
    g, info = gen_eisenberg()
    R = T.reach_check(g, (20, 32), [info['forge'], info['inn'], info['shop'], info['mine']], 'Eisenberg')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(EISENBERG, NAMES[EISENBERG], g.m, display=NAMES[EISENBERG])
    mb.props(note="<Area Name: Eisenberg>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town8', 60), bgs=('Fire1', 25), weather='snow 1')
    for x in range(18, 23):
        mb.add("Pass", x, 33, [pg(Ev().if_switch(S_C7_END, True, lambda b: b.common(CE['Reisen'])), trigger=1,
                                  priority=0)])
    el = Ev()
    el.wait(10)
    el.narrate(["Eisenberg is carved into its mountain like a honeycomb.",
                "Rune-forges glow day and night; dwarfs, orcs and horn-",
                "blooded walk the streets with their axes on their backs."])
    el.quest_desc(Q_HORN, "Eisenberg. The forge master, Iwakura Gōtetsu, runs the city from the great forge.")
    el.switch(S_EB)
    el.rest_point(EISENBERG, 20, 31, 8)
    mb.autorun("Arrival", el)
    iw = sp((info['forge'][0], info['forge'][1] + 2))
    def iwakura(e):
        e.if_switch(S_HORN, True, lambda b: b.say(IWAKURA, ["The deep crew is home. Rune-steel for the Wall, at last."]),
                    lambda b: b.if_switch(S_LAMP, True,
                                          lambda c: c.say(IWAKURA, ["The mine gate, top of the street. Bring my people home."]),
                                          first))
    def first(e):
        e.say(IWAKURA, ["Iwakura Gōtetsu. Rune-steel for the Wall, that's what I",
                        "need, and I can't make it. Trolls took the lower",
                        "Tiefgrube. The whole deep crew is trapped down there."])
        e.say(TSURUGI, ["Tsurugi Kenta, foreman. It's my crew. Twenty-six, when",
                        "I last counted. The big troll wears the old dwarf king's",
                        "helm. The miners call it the Troll King."])
        e.say(TSURUGI, ["It sits on the hoard down there, and it has a horn on",
                        "its belt that sings when the wind goes through it. Like",
                        "a hundred men far away."])
        e.say(HANMA, ["…The Heldenhorn. It was sounded at the breach of",
                      "Yamiji's fortress. I was standing next to it."], 'calm')
        e.say(TSURUGI, ["Take my lamp. The deep levels are dark in a way that",
                        "isn't just dark. Trolls regrow anything but burns; bring",
                        "fire."])
        e.item(KI["Grubenlampe"], 1)
        e.notice(["Received the \\C[6]Grubenlampe\\C[0]."])
        e.switch(S_LAMP)
        e.quest_desc(Q_HORN, "The Troll King has the Heldenhorn, at the bottom of the Tiefgrube. The mine gate is at the "
                             "top of Eisenberg's street. Trolls regrow anything but burns.")
    el = Ev()
    iwakura(el)
    mb.npc("Iwakura", iw[0], iw[1], IWAKURA, el, direction=2)
    ts = sp((iw[0] + 2, iw[1]))
    mb.npc("Tsurugi", ts[0], ts[1], TSURUGI, Ev().say(TSURUGI, ["Twenty-six. Bring them home."]), direction=2)
    # the mine gate
    mg = info['mine']
    def mine(e):
        e.if_switch(S_LAMP, True, lambda b: (b.se('Open2'), b.transfer(TIEFGRUBE, 20, 30, 8, 0)),
                    lambda b: b.text(["The mine gate. Iron doors, chained. The forge master",
                                      "holds the key."]))
    mb.add("Mine Gate", mg[0], mg[1], [pg((lambda e: (mine(e), e)[1])(Ev()), char='!$Gate2', index=0, direction=2,
                                          pattern=2, trigger=0, priority=1, walk_anime=False, direction_fix=True)])
    inn = info['inn']
    def sleep(e):
        e.if_gold(2000, '>=', lambda b: (b.gold(-2000), b.common(CE['Inn Sleep']), b.rest_point(EISENBERG, inn[0], inn[1] + 1, 2),
                                         b.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_LATERNE, S_HANMA_TALE), telling)),
                  lambda b: b.text(["Twenty silver. You don't have it."]))
    el = Ev().text(["The inn: stone beds, fur blankets, 2 gk the night."])
    el.choices(["Stay the night (2 gk)", "No"], [sleep, None], cancel=1)
    mb.add("Inn", inn[0], inn[1], [pg(el, char='!Door1', index=0, direction=2, pattern=1, trigger=0, priority=1,
                                      walk_anime=False)])
    shop = info['shop']
    goods = [('weapon', FW["Sternenfäuste"]), ('weapon', FW["Trollmorgenstern"]), ('armor', FA["Runenschild"]),
             ('armor', FA["Arenahelm"]), ('armor', FA["Kriegerring B"]), ('armor', FA["Magierring B"]),
             ('armor', FA["Heiligenring B"]), ('item', FI["Großes Elixier"]), ('item', FI["Äther"]),
             ('item', FI["Allheilmittel"]), ('item', FI["Große Lichtphiole"])]
    dw = npc_speaker("Runenschmiedin", "People2", 7)
    el = Ev().say(dw, ["Rune-steel. The best there is, and the dearest."])
    el.shop(goods)
    mb.add("Shop", shop[0], shop[1], [pg(el, char='!Door1', index=0, direction=2, pattern=1, trigger=0, priority=1,
                                        walk_anime=False)])
    for near, who, lines in [((10, 28), npc_speaker("Orkin", "People4", 4), ["Axes on the back is the law here. Makes",
                                                                             "conversation very polite."]),
                             ((30, 29), npc_speaker("Zwerg", "People2", 0), ["My brother's in the deep crew. Twenty-six,",
                                                                             "Tsurugi says. Twenty-six."])]:
        c = sp(near)
        mb.npc("Townsfolk", c[0], c[1], who, Ev().say(who, lines), direction=2, move_type=1)
    for (x, y) in [(18, 8), (22, 8)]:
        mb.light('brazier', x, y)
    return mb


# ---------------------------------------------------------------------------
# 116-118  Tiefgrube, Untere Tiefgrube, Trollhalle
# ---------------------------------------------------------------------------
def gen_mine(seed, rooms, halls, style, floor):
    g = Gen(40, 34, 4, seed=seed)
    open_ = T.rooms_and_halls(g, rooms, halls, *style, floor, wall_h=2)
    free = {c for c in open_ if g.kind_at(*c) == floor}
    g.scatter_in(free, [DUN.BOULDER, DUN.STALAG, [(0, 0, 208)], [(0, 0, 209)], [(0, 0, 210)], [(0, 0, 211)],
                        [(0, 0, 232)], [(0, 0, 233)], [(0, 0, 238)]], 26, spacing=1)
    g.finish()
    return g


def tiefgrube():
    g = gen_mine(116, [(16, 26, 24, 32), (14, 15, 26, 22), (3, 3, 12, 11), (28, 3, 37, 11), (4, 17, 10, 28)],
                 [([(20, 22), (20, 26)], 3), ([(14, 18), (10, 18)], 3), ([(26, 18), (32, 18), (32, 11)], 3),
                  ([(7, 17), (7, 11)], 3)], DUN.BROWN_ROCK, DUN.DIRT)
    mb = MapBuild(TIEFGRUBE, NAMES[TIEFGRUBE], g.m, display=NAMES[TIEFGRUBE])
    mb.props(note="<Rank: B>\n<Area Name: Tiefgrube>", bgm=('Dungeon1', 55), bgs=('Drips', 30),
             battleback=('DirtCave', 'DirtCave'), encounters=MINE_ENC(), steps=26)
    mb.add("Gate", 20, 32, [pg(Ev().se('Move1', 60).transfer(EISENBERG, 20, 7, 2, 0), trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The Tiefgrube: galleries cut by dwarfs who never met a",
                "straight line they liked. Ore carts lie on their sides.",
                "Somewhere far below, something big is singing."])
    mb.autorun("Mine", el)
    # the barricaded miners (west gallery)
    def miners(e):
        e.text(["A side gallery barricaded with ore carts. Behind it,",
                "lamplight, and thin faces: the deep crew, twenty-six of",
                "them. Tsurugi's lamp, they say, you've got Tsurugi's lamp."])
        e.say(npc_speaker("Bergmann", "People1", 6), ["The king troll's at the bottom, on the hoard. It's got the",
                                                      "horn. Kill it, miss. Please kill it. We'll go up now,",
                                                      "while the galleries are clear."])
        e.item(FI["Äther"], 2)
        e.notice(["The miners give you 2 Äther and head for the gate."])
        e.switch(S_MINERS)
    mb.add("Barricade", 7, 20, [pg(Ev().if_switch(S_MINERS, False, miners,
                                                   lambda b: b.text(["The barricade, empty. They made it out."])),
                                   char='!Other1', index=0, direction=2, priority=1)])
    mb.add("Shaft Down", 33, 4, [pg(Ev().text(["A ladder down into the dark."]).choices(
        ["Climb down", "Not yet"], [lambda b: (b.se('Move1', 60), b.transfer(TIEFGRUBE_UNTEN, 5, 5, 2, 0)), None], cancel=1),
        trigger=0, priority=1)])
    chest(mb, "Chest", 6, 5, lambda e: (e.item(FI["Großes Elixier"], 2), e.gold(10000)), "Found 2 Großes Elixier and \\MONEY[10000].")
    chest(mb, "Chest", 25, 16, lambda e: e.armor(FA["Runenschild"], 1), "Found a Runenschild.")
    mb.light('cave_dark', 0, 0, tile=False)
    mb.follow_light('beam', 20, 31)
    for (x, y) in [(20, 16), (7, 4), (33, 5)]:
        mb.light('torch', x, y)
    return mb


def tiefgrube_unten():
    g = gen_mine(117, [(2, 3, 10, 12), (14, 8, 26, 16), (28, 18, 37, 30), (4, 20, 14, 30)],
                 [([(10, 9), (14, 9)], 3), ([(26, 12), (32, 12), (32, 18)], 3), ([(28, 25), (14, 25)], 3)],
                 DUN.ORE_ROCK, DUN.ROCK)
    mb = MapBuild(TIEFGRUBE_UNTEN, NAMES[TIEFGRUBE_UNTEN], g.m, display=NAMES[TIEFGRUBE_UNTEN])
    mb.props(note="<Rank: B>\n<Area Name: Untere Tiefgrube>", bgm=('Dungeon1', 55), bgs=('Darkness', 30),
             battleback=('RockCave', 'RockCave'), encounters=MINE_ENC(), steps=24)
    mb.add("Ladder", 5, 4, [pg(Ev().se('Move1', 60).transfer(TIEFGRUBE, 33, 5, 2, 0), trigger=0, priority=1)])
    el = Ev()
    el.narrate(["Down here the dark is thick, like cloth over the eyes.",
                "Tsurugi's lamp makes a small warm room of it, and the",
                "singing is closer."])
    el.if_switch(S_LATERNE, True, lambda b: (b.text(["The Sternlaterne wakes on its own at Kanta's belt, and",
                                                     "the dark folds back from its light like a curtain."]),))
    mb.autorun("Deep", el)
    mb.add("Hall", 9, 29, [pg(Ev().text(["A gallery opens into a great hall. Gold glints, and the",
                                         "singing is right there."]).choices(
        ["Go in", "Not yet"], [lambda b: (b.se('Move1', 60), b.transfer(TROLLHALLE, 14, 24, 8, 0)), None], cancel=1),
        trigger=0, priority=1)])
    chest(mb, "Chest", 35, 20, lambda e: e.item(FI["Manastein (B)"], 2), "Found 2 Manastein (B).")
    chest(mb, "Chest", 24, 10, lambda e: (e.item(FI["Äther"], 2), e.gold(14000)), "Found 2 Äther and \\MONEY[14000].")
    mb.light('cave_dark', 0, 0, tile=False)
    mb.follow_light('beam', 5, 5)
    return mb


def trollhalle():
    g = Gen(28, 26, 4, seed=118)
    open_ = T.cave(g, g.ellipse(14, 12, 11, 9.5) | g.rect(12, 20, 16, 25), *DUN.BROWN_ROCK, DUN.DIRT2, wall_h=2)
    T.void_beyond(g, open_, 1)
    hoard = g.ellipse(14, 7, 5, 2.5) & open_
    for (x, y) in hoard:
        if (x + y) % 2 == 0:
            g.stamp(x, y, [(0, 0, 212 + (x % 2))], force=True)
    g.finish()
    mb = MapBuild(TROLLHALLE, NAMES[TROLLHALLE], g.m, display=NAMES[TROLLHALLE])
    mb.props(note="<Rank: B>\n<Area Name: Trollhalle>", bgm=('Battle6', 55), bgs=('Wind4', 25),
             battleback=('RockCave', 'RockCave'))
    mb.add("Gallery", 14, 25, [pg(Ev().if_switch(S_HORN, True,
                                                 lambda b: (b.se('Move1', 60), b.transfer(TIEFGRUBE_UNTEN, 9, 28, 2, 0)),
                                                 lambda b: b.text(["The singing holds you."])), trigger=1, priority=0)])
    king = mb.add("Troll King", 14, 9, [pg(None, char='Monster', index=1, direction=2, priority=1, step_anime=True),
                                        pg(None, sw=S_HORN, priority=0)])
    el = Ev()
    el.narrate(["The bottom of the Tiefgrube: a cavern of gold and bones",
                "and old dwarf-work. On the hoard, wearing a crowned helm",
                "too small for it, sits the Troll King."])
    el.say(FALIN, ["Fire, Tsurugi said. Burn it and it stays burned."], 'fierce')
    el.battle(T3["Trollkönig"])
    el.switch(S_HORN)
    el.text(["The Troll King goes down in a heap of its own gold, and",
             "this time the flesh doesn't knit. You take the horn off",
             "its belt. It is lighter than it looks, and warm."])
    el.set_image(king, '', 0)
    regalia_gain(el, "Heldenhorn", "3 of 4")
    el.say(HANMA, ["…I heard this sound go through a whole army like a",
                   "shiver. Seven hundred years. It still sounds the same."], 'calm')
    el.quest_done(Q_HORN)
    el.gold(20000)
    el.notice(["Tsurugi's crew left you their gratitude in coin: \\MONEY[20000]."])
    el.if_switch(S_LATERNE, True, lambda b: b.say(HANMA, ["The lantern and the horn. The countess will open the",
                                                          "Urwald for us now."], 'calm'))
    mb.autorun("The Hoard", el)
    mb.light('cave_dark', 0, 0, tile=False)
    mb.light('brazier', 14, 6)
    return mb


# ---------------------------------------------------------------------------
# 113  Urwald; 114 Hirschthron
# ---------------------------------------------------------------------------
def gen_urwald(seed=113, burning=False):
    g = Gen(42, 40, 2, seed=seed)
    g.paint(g.all(), OUT.GRASS if not burning else OUT.DIRT)
    pts = [(20, 0), (19, 7), (12, 13), (15, 22), (27, 25), (30, 33), (26, 39)]
    walk = g.line(pts, 8, wobble=1.3) | g.blob(8, 26, 4.5, seed=8) | g.blob(33, 12, 4.5, seed=9)
    style = T.FOREST if not burning else T.ASH
    ground = T.frame(g, walk, dict(frame=OUT.DARKFOREST) if not burning else dict(frame=(118, 126)), thick=4, trunk_h=2)
    road = g.line(pts, 2, wobble=1.3) & ground
    g.paint(road, OUT.GRASS_DIRT if not burning else OUT.DIRT_STONES)
    g.keep_clear |= g.grow(road, 1)
    T.dress(g, ground - g.grow(road, 2), style, trees=0.16 if not burning else 0.08, rocks=0.02, bushes=0.07,
            tufts=0.06)
    if burning:
        for c in g.rng.sample(sorted(ground - g.blocked), len(ground) // 8):
            g.set(c[0], c[1], 1, auto(OUT.DARKSPARK))
    g.finish()
    return g


def urwald():
    g = gen_urwald()
    R = T.reach_check(g, (20, 1), [(26, 38)], 'Urwald')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(URWALD, NAMES[URWALD], g.m, display=NAMES[URWALD])
    mb.props(note="<Rank: B>\n<Area Name: Urwald>\n<lighting: Outside>", bgm=('Dungeon4', 55), bgs=('Wind2', 30),
             battleback=('Grassland', 'Forest'), encounters=URWALD_ENC(), steps=26)
    for x in range(g.w):
        if (x, 0) in R and (x, 1) in R:
            mb.add("North", x, 0, [pg(Ev().se('Move1', 60).transfer(HIRSCHHEIM, 21, 38, 8, 0), trigger=1, priority=0)])
        if (x, g.h - 1) in R and (x, g.h - 2) in R:
            mb.add("South", x, g.h - 1, [pg(Ev().if_switch(S_LESHY, True,
                                                          lambda b: (b.se('Move1', 60), b.transfer(HIRSCHTHRON, 16, 1, 2, 0)),
                                                          lambda b: b.text(["The trees close in. The path is gone."])),
                                            trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The Urwald: trees like the pillars of a hall with no",
                "roof, moss to the knee, and a silence so deep you can",
                "hear the Sternlaterne hum at Kanta's belt."])
    mb.autorun("Urwald", el)
    # the leshy at the stone
    lc = sp((15, 22))
    leshy = mb.add("Leshy", lc[0], lc[1], [pg(None, char='$BigMonster1', index=0, direction=4, priority=1,
                                              direction_fix=True, step_anime=True),
                                           pg(None, sw=S_LESHY, priority=0)])
    def leshy_talk(e):
        e.text(["A shape as tall as the trees steps out between them:",
                "bark and moss and antlers, and eyes like two drops of",
                "sap with the sun behind them."])
        e.say(npc_speaker("Leshy", "", 0), ["…Light. Horn. Old things, carried by new things. And",
                                            "bread, and salt, from Kusaki's table."])
        e.if_item(KI["Kusakis Gabe"], lambda b: (
            b.text(["Kanta sets Kusaki's gift on the flat stone. The leshy",
                    "bends down, a long way, and breathes on it."]),
            b.item(KI["Kusakis Gabe"], -1),
            b.say(npc_speaker("Leshy", "", 0), ["The hollow ones dig at the throne. The throne is mine.",
                                                "Go. Kill the one who sends them. The path will be there."]),
            b.switch(S_LESHY),
            b.quest_desc(Q_THRONE, "The leshy opened the way south to the Hirschthron.")),
                  lambda b: b.say(npc_speaker("Leshy", "", 0), ["No bread. No salt. No path."]))
    mb.add("Stone", lc[0], lc[1] + 1, [pg(Ev().if_switch(S_LESHY, False, leshy_talk), trigger=0, priority=1)])
    fire = sp((33, 12))
    rest = sp((fire[0], fire[1] + 1), avoid=[fire])
    camp_fire(mb, fire[0], fire[1], URWALD, rest[0], rest[1], 8, ["A foresters' fire ring, cold but dry."])
    c1 = sp((8, 26))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Großes Elixier"], 3), e.item(FI["Äther"], 2)),
          "Found 3 Großes Elixier and 2 Äther.")
    return mb


def gen_throne(night=False):
    g = Gen(32, 30, 2, seed=114)
    g.paint(g.all(), OUT.GRASS if not night else OUT.DIRT)
    walk = g.ellipse(16, 16, 12, 11) | g.rect(14, 0, 18, 6)
    ground = T.frame(g, walk, dict(frame=OUT.DARKFOREST) if not night else dict(frame=(118, 126)), thick=3, trunk_h=2)
    ring = g.ellipse(16, 16, 6.5, 5.5) - g.ellipse(16, 16, 5.5, 4.5)
    for (x, y) in ring:
        if (x * 7 + y * 3) % 3 == 0:
            g.stamp(x, y, [(0, -1, 288), (0, 0, 304)], force=True)
    # the throne of antler and stone
    g.stamp(16, 16, [(0, -1, 296), (0, 0, 312)], force=True)
    g.paint(g.ellipse(16, 16, 4, 3), OUT.STONE_FLOOR)
    g.keep_clear |= g.line([(16, 0), (16, 12)], 3)
    T.dress(g, ground - g.ellipse(16, 16, 7, 6) - g.line([(16, 0), (16, 12)], 3), T.FOREST if not night else T.ASH,
            trees=0.12, rocks=0.02, bushes=0.05, tufts=0.05)
    g.finish()
    return g


def hirschthron():
    g = gen_throne()
    mb = MapBuild(HIRSCHTHRON, NAMES[HIRSCHTHRON], g.m, display=NAMES[HIRSCHTHRON])
    mb.props(note="<Rank: S>\n<Area Name: Hirschthron>\n<lighting: Outside>", bgm=('Battle8', 55), bgs=('Wind3', 30),
             battleback=('Grassland', 'Forest'))
    for x in range(14, 19):
        mb.add("North", x, 0, [pg(Ev().se('Move1', 60).transfer(URWALD, 26, 38, 8, 0), trigger=1, priority=0)])
    muk = mb.add("Mukuro", 16, 13, [pg(None, char=MUKURO.char[0], index=MUKURO.char[1], direction=2, priority=1),
                                    pg(None, sw=S_MUKURO, priority=0)])
    for x in (13, 19):
        mb.add("Hollow", x, 14, [pg(None, char='Monster', index=1, direction=8, priority=1), pg(None, sw=S_MUKURO, priority=0)])
    el = Ev()
    el.narrate(["The Hirschthron: a ring of standing stones in a clearing,",
                "and in the middle a throne of stone and antler that",
                "nobody has sat on in a thousand years."])
    el.narrate(["Hollow men dig at its roots with their hands. Over them,",
                "reading aloud from a book with no pages, stands a thin",
                "man in grey with a face like a skull wearing skin."])
    el.say(MUKURO, ["Little vessel. And the General who was refused. How",
                    "fitting, at this door of all doors."])
    el.say(MUKURO, ["I promised a widow her husband, once. I keep my",
                    "promises. After the seal breaks, there will be no more",
                    "doors. Nobody will ever have to say goodbye again."])
    el.say(HANMA, ["Because nobody will be left to say it, magus."], 'stern')
    el.say(YUKINO, ["…He was always a liar, Tōma said."])
    el.say(MUKURO, ["Tōma. He sends his regards to his saint."])
    el.battle(T3["Mukuro"])
    el.switch(S_MUKURO)
    el.se('Book2')
    el.text(["Mukuro comes apart like a book in the rain: pages, grey",
             "dust, a smell of old libraries. The hollow men stop",
             "digging and lie down, and are only dead."])
    el.set_image(muk, '', 0)
    el.say(HANMA, ["Two of the Four. Tsumugi, Mukuro. That leaves Shigure,",
                   "and Gōen. And then him."], 'stern')
    el.fadeout()
    el.transfer(HIRSCHHEIM, 21, 36, 8, 0)
    el.fadein()
    el.say(KAGURA, ["The forest is quiet. It hasn't been quiet in a year."])
    el.say(KAGURA, ["Hohenwacht remembers us when it needs something.",
                    "Hirschheim remembers its friends. Take this: the Waldkrone",
                    "my grandmother wore at the last war."])
    el.armor(FA["Waldkrone"], 1)
    el.quest_done(Q_THRONE)
    el.if_switch(S_HANMA_TALE, False, telling)
    el.wait(20)
    el.se('Horse', 90)
    el.say(npc_speaker("Bote", "People3", 7), ["For the Guild vessel! From Salzhafen, the League of the",
                                               "coast: Shigure is drowning every ship on the Sturmsee."])
    el.say(npc_speaker("Bote", "People3", 7), ["And the Guild archivist adds: the Aschenkrone went to",
                                               "sea in 313, and a Fomorian chief on the Knochenriff has",
                                               "worn a grey crown for a hundred years."])
    el.say(KANTA, ["The last one."], 'calm')
    el.switch(S_C8_END)
    el.plugin('Story_Core', 'ChapterCard', {'title': "Wald und Tiefe", 'subtitle': "3 von 4", 'duration': 160},
              'Chapter Card')
    el.switch(SW('C9: Salzhafen'))
    el.notice(["\\C[6]Salzhafen\\C[0] is open (travel from any city gate)."])
    mb.autorun("The Throne", el)
    return mb
