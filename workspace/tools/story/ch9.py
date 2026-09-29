"""Chapter 9: Morgenröte. Salzhafen and Kaizaki Rui, the Knochenriff and the Fomorian chief (the Aschenkrone, the
fourth regalia), Shigure on the Sturmsee, the burning Urwald (Gōen's end, the breakthrough to A), the Hirschthron
at night: Maō Kagerō in three phases, until Yukino says his name. The epilogue on old maps, and the end."""
import copy
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story import foes, foes3
from story.ids import *
from story.ch1 import chest, TODO, OKUDA
from story.ch2 import camp_fire
from story.cast import *
from story.ch6 import V_REGALIA, YUKINO_ID
from story.ch7 import regalia_gain, S_C7_END
from story.ch8 import gen_urwald, gen_throne
from story import terrain as T
from story.terrain import Gen, OUT, DUN, INS, auto
import mapinfo

KI = foes.KEY
K3 = foes3.KEY
FI = foes.ITEMS
FA = foes.ARMORS
FW = foes.WEAPONS
T3 = foes3.TR

SAYO = npc_speaker("Namiji Sayo", "People4", 7)
BOSUN = npc_speaker("Bootsmann Kaji", "People4", 2)
HOKAI = Speaker("Hōkai", "", 0, ("$BigMonster2", 0))
HAYATE = npc_speaker("Hayate", "People1", 2)
BARKEEP = npc_speaker("Wirt Unagi", "People4", 3)

# ----------------------------------------------------------------------- quests
Q_KRONE = Quest(33, "Die Aschenkrone", "Minato Hisa", "Salzhafen, Knochenriff",
                "The last of the Dawn Regalia went to sea in 313. A Fomorian chief on the Knochenriff wears a crown "
                "of grey iron that burns him. Nobody sails to the Knochenriff: Shigure drowns every ship on the "
                "Sturmsee.",
                "Find a ship in Salzhafen.")
Q_RUI = Quest(34, "Ruis Preis", "Kaizaki Rui", "Sturmsee",
              "Kaizaki Rui of the Schwarze Flagge sails you to the reef. Her price: when you have your crown, you "
              "fight Shigure with her.",
              "The Seeschwalbe, at the middle pier of Salzhafen.")
Q_END = Quest(35, "Morgenröte", "Hanma", "Urwald, Hirschthron",
              "Kagerō is marching on the Hirschthron, the seal under the Tiefenwald. The Host of Ash burns the "
              "Urwald ahead of him, and Gōen leads it.",
              "Hirschheim's south road, into the burning Urwald.")

# ----------------------------------------------------------------------- switches
S_OPEN = SW('C9: Salzhafen')           # set at the end of chapter 8 (travel)
S_ARRIVE = SW('C9: Salzhafen Arrived')
S_HISA = SW('C9: Hisa')
S_RUI = SW('C9: Rui')
S_REEF = SW('C9: Reef Reached')
S_KRONE = SW('C9: Aschenkrone')
S_SHIGURE = SW('C9: Shigure Down')
S_FIRE = SW('C9: Urwald Burns')
S_BREAK_A = SW('C9: Breakthrough A')
S_GOEN = SW('C9: Goen Down')
S_PH1 = SW('C9: Kagero Phase 1')
S_PH2 = SW('C9: Kagero Phase 2')
S_END = SW('C9: The End')
V_VOYAGE = VAR('Voyage')

SEA_ENC = lambda: [(T3["Ertrunkene x3"], 5, ()), (T3["Sirenen x2"], 4, ()), (T3["Krabben x2"], 5, ()),
                   (T3["Fomorer & Sirene"], 3, ())]
HALL_ENC = lambda: [(T3["Fomorer x2"], 5, ()), (T3["Fomorer & Sirene"], 4, ()), (T3["Krabben x2"], 3, ()),
                    (T3["Ketos"], 1, ())]
FIRE_ENC = lambda: [(T3["Salamander x2"], 5, ()), (T3["Phönix & Salamander"], 4, ()), (T3["Gardisten x2"], 4, ()),
                    (T3["Gardist & Phönix"], 4, ())]

SEA = 1                     # Outside_A1 kind 1: sea with sandy shores (kind 0 has grass shores)
PIER_X = 21                 # the middle pier (x 21-23); the Seeschwalbe lies at its end
PIER_END = 33


def build():
    return [salzhafen(), taverne(), schiff(), knochenriff(), versunkene_halle(), urwald_brand(), hirschthron_nacht(),
            epilog_wall(), epilog_weissenfels(), epilog_rabenau(), epilog_kamm()]


# ---------------------------------------------------------------------------
# troop pages (called from foes3.troops)
# ---------------------------------------------------------------------------
def goen_final_pages():
    """Gōen in the burning Urwald: no rank wall this time; at half HP the chain for Hanma again, and the breakthrough
    to A (once: the switch keeps a second attempt after a defeat from repeating it)."""
    t0 = Ev()
    t0.say(GOEN, ["Four regalia, a ghost, a living armor and a saint. My",
                  "wall is gone, little vessel. Let us see what you are",
                  "without it."])
    t0.say(HANMA, ["His rank can't hide him now, my Lord. Hit him!"], 'command')
    def chain(b):
        b.say(GOEN, ["Clause one. The General who was refused is forfeit.",
                     "I'll collect her myself this time."])
        b.se('Chain', 90, 60)
        b.text(["The golden chain again, thicker than an arm, around",
                "Hanma's throat. This time it doesn't pull: it drags,",
                "down, toward the brass throne and the dark under it."], background=1, position=1)
        b.say(HANMA, ["…Not… again…"], 'hurt')
        b.say(YUKINO, ["Kanta!"])
        b.say(KANTA, ["She said no. Seven hundred years ago. Somebody said it",
                      "for her. I'm saying it again."], 'fierce')
        b.se('Magic3', 90, 60)
        b.flash((255, 250, 220, 255), 60)
        b.text(["The four regalia answer together. The ring of light around",
                "Kanta closes into a crown of blades, and every one of",
                "them goes through the chain at once."], background=1, position=1)
        b.breakthrough()
        b.switch(S_BREAK_A)
        b.say(GOEN, ["…Twice. Nobody breaks my chains twice."])
    t1 = Ev().if_switch(S_BREAK_A, False, chain)
    return [(db_page(t0, turn=(0, 0))), (db_page(t1, enemy_hp=(0, 50)))]


def kagero_pages(n):
    """The three phases of the last fight: 1 Maō Kagerō, 2 Hōkai's shadow, 3 Kurenai Tōma (ends when Yukino says
    his name: the battle is aborted and the ending plays on the map)."""
    if n == 1:
        t0 = Ev()
        t0.say(KAGERO, ["Four. You really found all four. Akira's toys."])
        t0.say(HANMA, ["His veil is down, my Lord! The regalia pierce him: he",
                       "bleeds like anyone!"], 'command')
        t1 = Ev()
        t1.say(KAGERO, ["…Hōkai. Hōkai, wake up. I need you."])
        return [db_page(t0, turn=(0, 0)), db_page(t1, enemy_hp=(0, 50))]
    if n == 2:
        t0 = Ev()
        t0.say(HOKAI, ["LITTLE LIGHTS. WE HAVE EATEN BRIGHTER."])
        t2 = Ev()
        t2.say(HANMA, ["It's feeding on him, my Lord! Cut it off him!"], 'command')
        return [db_page(t0, turn=(0, 0)), db_page(t2, turn=(2, 0))]
    t0 = Ev()
    t0.say(TOMA, ["I'm sorry. I'm sorry. It won't let me stop. Don't make",
                  "me—"])
    t2 = Ev()
    t2.if_script("$gameActors.actor(%d).isDead() && $gameParty.members().includes($gameActors.actor(%d))"
                 % (YUKINO_ID, YUKINO_ID),
                 lambda b: (b.script("$gameActors.actor(%d).revive(); $gameActors.actor(%d).setHp(1);"
                                     % (YUKINO_ID, YUKINO_ID)),
                            b.text(["Yukino gets up. She has one thing left to do."], background=1, position=1)))
    t2.say(YUKINO, ["Tōma."])
    t2.wait(30)
    t2.text(["The Demon Lord stops, halfway through a swing. For one",
             "breath his face is a man's face."], background=1, position=1)
    t2.say(TOMA, ["…Yuki?"])
    t2.abort_battle()
    return [db_page(t0, turn=(0, 0)), db_page(t2, turn=(2, 0))]


def db_page(ev, **kw):
    from story import db
    return db.troop_page(ev, **kw)


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def trigger_line(mb, cells, name, body, done_switch):
    """Stepping on any of `cells` (while done_switch is OFF) runs `body` once, from a single autorun event: the
    scene isn't copied onto every trigger tile. After a defeat, stepping on the line again runs it again."""
    go = SW('C9: %s (go)' % name)
    for (x, y) in cells:
        mb.add(name, x, y, [pg(Ev().if_switch(done_switch, False, lambda b: b.switch(go)), trigger=1, priority=0)])
    el = Ev().switch(go, False)
    body(el)
    mb.add(name + " (scene)", 0, 0, [pg(el, sw=go, trigger=3, priority=0)])


def voyage_to(e, voyage, tx, ty, d=6):
    e.var(V_VOYAGE, voyage)
    e.fadeout()
    e.transfer(SCHIFF, tx, ty, d, 0)
    e.fadein()


def back_to_port(e):
    e.fadeout()
    e.transfer(SALZHAFEN, PIER_X + 1, PIER_END - 1, 8, 0)
    e.fadein()


def to_reef(e):
    e.fadeout()
    e.transfer(KNOCHENRIFF, *REEF_LANDING, 6, 0)
    e.fadein()


# ---------------------------------------------------------------------------
# 120  Salzhafen
# ---------------------------------------------------------------------------
def gen_salzhafen():
    g = Gen(48, 36, 2, seed=120)
    g.paint(g.all(), OUT.SAND)
    top, wall = OUT.SNOW_CLIFF
    g.cliff(g.rect(0, 0, 47, 2), top, wall, height=2)          # white cliffs, faces on rows 3-4
    west = g.rect(0, 5, 1, 24) - g.rect(0, 10, 1, 12)          # the gate gap on the land road
    g.paint(west, top)
    g.blocked |= west
    sea = g.rect(0, 25, 47, 35) | g.rect(44, 5, 47, 24)
    g.paint(sea, SEA)
    info = {}
    # streets: the land road, the avenue down to the harbour, the quay
    main = g.rect(0, 10, 43, 12)
    avenue = g.rect(21, 5, 22, 21)
    quay = g.rect(2, 22, 43, 24)
    g.paint(main | avenue, OUT.SAND_STONES)
    g.tile(quay, 1561, z=0)
    g.keep_clear |= g.grow(main | avenue, 1) | quay
    # three piers into the harbour (A5 bridge planks with rails)
    for px, y1 in ((9, 31), (PIER_X, PIER_END), (33, 31)):
        for y in range(25, y1 + 1):
            g.set(px, y, 0, 1541)
            g.set(px + 1, y, 0, 1542)
            g.set(px + 2, y, 0, 1543)
            g.keep_clear |= {(px, y), (px + 1, y), (px + 2, y)}
    # salt pans (north-west)
    for px in (3, 7, 11, 15):
        g.paint(g.rect(px, 5, px + 2, 7), OUT.WATER2)
        g.blocked |= g.rect(px, 5, px + 2, 7)
        g.stamp(px + 3, 6, [(0, 0, 212)], force=True)        # heaps of salt on the dikes
    # buildings
    info['office'] = T.house(g, 26, 5, 9, roof='gold', wall='marble', door='double')
    info['shrine'] = T.house(g, 36, 5, 7, roof='green', wall='marble', door='arch')
    info['tavern'] = T.house(g, 3, 15, 8, roof='wood', wall='wood', door='arch')
    g.set(info['tavern'][0] + 1, info['tavern'][1] - 1, 3, 71)
    info['shop'] = T.house(g, 12, 15, 7, roof='green', wall='plaster', door='arch')
    g.set(info['shop'][0] + 1, info['shop'][1] - 1, 3, 66)
    for (x, y, w, roof, wall) in [(25, 15, 6, 'wood', 'brick'), (33, 15, 7, 'green', 'plaster')]:
        T.house(g, x, y, w, roof=roof, wall=wall, door='arch')
    # lamps on the quay, cargo, flowers
    for x in (6, 17, 28, 39):
        g.stamp(x, 22, OUT.LAMP, force=True)
    cargo = {c for c in quay if c[1] == 22 and c not in g.blocked} - g.rect(8, 22, 12, 24) - \
        g.rect(PIER_X - 1, 22, PIER_X + 3, 24) - g.rect(32, 22, 36, 24)
    g.keep_clear -= cargo
    g.scatter_in(cargo, [[(0, 0, OUT.BARREL)], [(0, 0, 180)], [(0, 0, 181)], [(0, 0, 183)]], 10, spacing=0)
    free = {c for c in g.all() if g.kind_at(*c) == OUT.SAND and c not in g.blocked and c not in g.keep_clear
            and c[1] < 22}
    g.scatter_in(free, [[(0, 0, 160)], [(0, 0, 161)], [(0, 0, 236)], [(0, 0, 237)], [(0, 0, 246)]], 20, spacing=1)
    g.finish()
    return g, info


def salzhafen():
    g, info = gen_salzhafen()
    pier_end = (PIER_X + 1, PIER_END)
    R = T.reach_check(g, (1, 11), [info['office'], info['shrine'], info['tavern'], info['shop'], pier_end],
                      'Salzhafen')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(SALZHAFEN, NAMES[SALZHAFEN], g.m, display=NAMES[SALZHAFEN])
    mb.props(note="<Area Name: Salzhafen>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town3', 60), bgs=('Wave1', 35))
    for y in range(10, 13):
        mb.add("Land Road", 0, y, [pg(Ev().if_switch(S_C7_END, True, lambda b: b.common(CE['Reisen'])), trigger=1,
                                      priority=0)])
    # arrival
    el = Ev()
    el.card("Kapitel 9", "Morgenröte", 200)
    el.narrate(["Salzhafen: white cliffs, glittering salt pans, a harbour",
                "full of masts that do not move. No ship has sailed in a",
                "month."])
    el.say(HANMA, ["The Aschenkrone went to sea in 313, the record says.",
                   "Somebody here knows where it came ashore."], 'calm')
    el.quest_new(Q_KRONE)
    el.switch(S_ARRIVE)
    mb.autorun("Salzhafen", el)
    # Minato Hisa on the steps of the League office
    hisa_at = sp((info['office'][0] + 2, info['office'][1] + 1))
    def hisa(e):
        def first(b):
            b.say(HISA, ["Minato Hisa, for the Küstenbund. If you're here to buy",
                         "salt, you're the first in a month."])
            b.say(HISA, ["Shigure. One of the Four. He rides a kraken out of the",
                         "Sturmsee and drowns anything with a sail. The League is",
                         "strangling."])
            b.say(KANTA, ["I'm looking for a crown. Ash-grey iron. It went to sea a",
                          "long time ago."], 'calm')
            b.say(HISA, ["The Fomorian chief on the Knochenriff wears one. It burns",
                         "him, and he won't take it off. Nobody sails to the",
                         "Knochenriff, either. Try the tavern. Try Rui."])
            b.switch(S_HISA)
            b.quest_desc(Q_KRONE, "The Fomorian chief on the Knochenriff wears the Aschenkrone. Nobody sails "
                                  "there: ask for Rui at Der Ertrunkene Mann.")
        e.if_switch(S_SHIGURE, True,
                    lambda b: b.say(HISA, ["Ships are going out. Ships are coming back. I'd forgotten",
                                           "what that sounds like."]),
                    lambda b: b.if_switch(S_HISA, True,
                                          lambda c: c.say(HISA, ["Rui. Der Ertrunkene Mann, at the back. Don't sit in",
                                                                 "her chair."]),
                                          first))
    mb.npc("Minato Hisa", hisa_at[0], hisa_at[1], HISA, (lambda e: (hisa(e), e)[1])(Ev()), direction=2)
    mb.door(info['office'][0], info['office'][1], SALZHAFEN, 0, 0, name='League Office',
            locked_text=["The League office. The clerks inside wave you back out", "to Hisa on the steps."])
    # the tide shrine: Namiji Sayo
    sayo_at = sp((info['shrine'][0] + 2, info['shrine'][1] + 1))
    el = Ev().if_switch(S_SHIGURE, True,
                        lambda b: b.say(SAYO, ["Five seals. Four still whole tonight. Go and keep the",
                                               "fifth whole, vessel."]),
                        lambda b: b.say(SAYO, ["Namiji Sayo, of Meguri's tide shrine. The goddess is",
                                               "restless. Something hunts in the deep, and she turns",
                                               "over in her sleep."]))
    mb.npc("Namiji Sayo", sayo_at[0], sayo_at[1], SAYO, el, direction=2)
    mb.door(info['shrine'][0], info['shrine'][1], SALZHAFEN, 0, 0, name='Tide Shrine',
            locked_text=["The shrine of Meguri. Inside, the sound of the sea,", "though the sea is outside."])
    # the tavern (inn)
    mb.door(info['tavern'][0], info['tavern'][1], TAVERNE_SH, 9, 11, 8, name='Der Ertrunkene Mann')
    # the chandler: A-rank gear
    shop_at = sp((info['shop'][0] + 2, info['shop'][1] + 1))
    goods = [('armor', FA["Seefahrerhelm"]), ('armor', FA["Sturmschild"]), ('armor', FA["Perlenamulett"]),
             ('armor', FA["Kriegerring B"]), ('armor', FA["Heiligenring B"]), ('armor', FA["Magierring B"]),
             ('item', FI["Großes Elixier"]), ('item', FI["Äther"]), ('item', FI["Starkes Riechsalz"]),
             ('item', FI["Allheilmittel"]), ('item', FI["Große Lichtphiole"])]
    chandler = npc_speaker("Schiffsausrüsterin Ise", "People3", 7)
    mb.npc("Chandler", shop_at[0], shop_at[1], chandler,
           Ev().say(chandler, ["Storm gear, sea gear, and the League buys mana stones",
                               "at the going rate. Everything's cheap. Nobody's sailing."]).shop(goods), direction=2)
    mb.door(info['shop'][0], info['shop'][1], SALZHAFEN, 0, 0, name='Chandlery',
            locked_text=["The chandlery's stock is out on the street, with Ise."])
    # salt workers, fish wife
    worker = npc_speaker("Salzsieder", "People1", 4)
    w_at = sp((10, 9))
    mb.npc("Salt Worker", w_at[0], w_at[1], worker,
           Ev().say(worker, ["Salt keeps. That's the whole trick of it. Fish don't,",
                             "men don't, but salt keeps."]), direction=8, move_type=1)
    fish = npc_speaker("Fischerin", "People2", 7)
    f_at = sp((30, 23))
    mb.npc("Fisher", f_at[0], f_at[1], fish,
           Ev().if_switch(S_SHIGURE, True,
                          lambda b: b.say(fish, ["The boats are out! Look at them! …Don't look at me,",
                                                 "I'm not crying, it's the salt."]),
                          lambda b: b.say(fish, ["Don't whistle on the harbour wall. You'll wake him."])),
           direction=2)
    # the middle pier: Bootsmann Kaji and the Seeschwalbe
    mb.add("Seeschwalbe", PIER_X + 1, PIER_END + 1, [pg(None, char='Vehicle', index=1, direction=4, priority=1,
                                                        step_anime=True, direction_fix=True)])
    for bx in (10, 34):
        mb.add("Boat", bx, 32, [pg(None, char='Vehicle', index=0, direction=2, priority=1, step_anime=True)])
    def boat(e):
        def reef_menu(b):
            b.say(BOSUN, ["The Knochenriff, then. Rui's aboard."])
            b.choices(["Sail to the Knochenriff", "Not yet"], [lambda c: voyage_to(c, 1, 11, 9), None], cancel=1)
        def after_crown(b):
            b.if_switch(S_SHIGURE, True,
                        lambda c: c.choices(["Sail to the Knochenriff", "Not yet"], [to_reef, None], cancel=1),
                        lambda c: (c.say(BOSUN, ["Rui says it's time. Into the Sturmsee. Gods keep you."]),
                                   c.choices(["Into the Sturmsee (Shigure)", "Back to the Knochenriff", "Not yet"],
                                             [lambda d: voyage_to(d, 2, 11, 9), to_reef, None], cancel=2)))
        e.if_switch(S_RUI, False,
                    lambda b: b.say(BOSUN, ["The Seeschwalbe's Rui's. Nobody sails her without Rui.",
                                            "Nobody sails at all, these days."]),
                    lambda b: b.if_switch(S_KRONE, False, reef_menu, after_crown))
    mb.npc("Bootsmann Kaji", PIER_X + 1, PIER_END, BOSUN, (lambda e: (boat(e), e)[1])(Ev()), direction=2)
    # back from the Sturmsee: the seals, and the fire in the south
    el = Ev()
    el.wait(20)
    el.narrate(["Back in Salzhafen the whole harbour is on the quay, and",
                "the tide-priestess Namiji Sayo is waiting at the harbour",
                "wall."])
    el.say(SAYO, ["The goddess turned over in her sleep last night and",
                  "settled. Shigure was hunting the Abgrund. The seal there",
                  "is safe."])
    el.say(KANTA, ["Seal?"], 'calm')
    el.say(SAYO, ["Five seals chain the Father of Monsters under the world.",
                  "One in each god's holy place: the Abgrund, the Morgendom,",
                  "the Hirschthron, two more. The Four were sent to break them."])
    el.say(HANMA, ["So that is what he wants. Not the world. What is under",
                   "it."], 'stern')
    el.say(HISA, ["For the Guild vessel: the Küstenbund's thanks, and the",
                  "League's money, which is the same thing but heavier."])
    el.gold(1000000)
    el.notice(["Received \\MONEY[1000000]."])
    el.se('Horse', 90)
    el.say(npc_speaker("Bote", "People3", 7), ["From Hirschheim! The countess begs the Guild vessel:",
                                               "the Urwald is burning. An army of brass and ash is",
                                               "cutting its way to the Hirschthron."])
    el.say(npc_speaker("Bote", "People3", 7), ["The golden one leads it. And behind it, walking, one man",
                                               "in grey armour. The trees die where he passes."])
    el.say(YUKINO, ["…Tōma."])
    el.say(HANMA, ["The last seal of the forest. And the last of the Four in",
                   "front of it. My Lord, this is the end of it, one way or",
                   "the other."], 'stern')
    el.say(KANTA, ["Then let's go and end it."], 'fierce')
    el.switch(S_FIRE)
    el.quest_new(Q_END)
    el.notice(["Travel to \\C[6]Hirschheim\\C[0], and take the south road into the Urwald."])
    mb.autorun("The Harbour Wall", el, cond_switch=S_SHIGURE)
    return mb


# ---------------------------------------------------------------------------
# 130  Der Ertrunkene Mann (the tavern: inn, Rui)
# ---------------------------------------------------------------------------
def gen_taverne():
    g = Gen(20, 14, 3, seed=130)
    T.interior(g, [(2, 2, 17, 12)], *INS.WOOD_WALL, INS.WOOD)
    g.paint(g.rect(7, 6, 12, 9), INS.RUG_RED)
    for (x, y, tiles) in [(4, 5, [(0, 0, 136), (1, 0, 137), (2, 0, 138)]),
                          (12, 6, [(0, 0, 112), (1, 0, 113)]), (11, 6, [(0, 0, 120)]), (14, 6, [(0, 0, 120)]),
                          (12, 9, [(0, 0, 112), (1, 0, 113)]), (11, 9, [(0, 0, 120)]), (14, 9, [(0, 0, 120)]),
                          (8, 3, [(0, 0, 128), (1, 0, 129)]), (15, 3, [(0, 0, 196)]), (16, 3, [(0, 0, 212)]),
                          (3, 11, [(0, 0, 240)]), (4, 11, [(0, 0, 242)]), (16, 11, [(0, 0, 196)])]:
        g.stamp(x, y, tiles, force=True)
    g.finish()
    return g


def taverne():
    g = gen_taverne()
    mb = MapBuild(TAVERNE_SH, NAMES[TAVERNE_SH], g.m, display=NAMES[TAVERNE_SH])
    mb.props(note="<Area Name: Der Ertrunkene Mann>\n<No Rank HUD>", bgm=('Town2', 50), bgs=('Wave1', 15))
    mb.add("Exit", 9, 12, [pg(Ev().se('Move1', 60).transfer(SALZHAFEN, 7, 20, 2, 0), trigger=1, priority=0)])
    def sleep(e):
        e.if_gold(3000, '>=', lambda b: (b.gold(-3000), b.common(CE['Inn Sleep']),
                                         b.rest_point(TAVERNE_SH, 9, 10, 8)),
                  lambda b: b.say(BARKEEP, ["Thirty silver. Even drowned men pay here."]))
    el = Ev().say(BARKEEP, ["Unagi. Beds upstairs, 3 gk the night. The view's the",
                            "harbour, which is to say, the graveyard."])
    el.choices(["Stay the night (3 gk)", "No thanks"], [sleep, None], cancel=1)
    mb.npc("Barkeep", 5, 4, BARKEEP, el, direction=2)
    # Kaizaki Rui at the back table
    def rui(e):
        e.text(["In the back of Der Ertrunkene Mann, a woman with a sea-",
                "green braid and a coat covered in someone else's medals",
                "has her boots on the table."])
        e.say(RUI, ["You're the one asking about the Knochenriff. I've got a",
                    "ship. I had a crew. Shigure drowned them, all sixty, one",
                    "at a time, while I watched from a rope."])
        e.say(RUI, ["I'll take you to the reef. And when you have your crown,",
                    "I'll take you to Shigure. That's the price. You fight",
                    "him with me."])
        e.say(HANMA, ["A fair price, my Lord. We were going to have to fight him",
                      "anyway."], 'calm')
        e.say(YUKINO, ["…He was ours, once. Shigure. The Morgenwacht's lance."])
        e.say(RUI, ["Then you'll know where to put the knife."])
        e.say(KANTA, ["Deal."], 'calm')
        e.item(K3["Seekarte"], 1)
        e.item(K3["Ruis Pfand"], 1)
        e.notice(["Received the \\C[6]Seekarte\\C[0] and \\C[6]Ruis Pfand\\C[0]."])
        e.say(RUI, ["The Seeschwalbe. Middle pier. Tell Kaji I said so."])
        e.switch(S_RUI)
        e.quest_new(Q_RUI)
        e.quest_desc(Q_KRONE, "Rui sails you to the Knochenriff: the Seeschwalbe waits at the middle pier.")
    mb.add("Kaizaki Rui", 15, 7, [pg(Ev().if_switch(S_RUI, False, rui), char=RUI.char[0], index=RUI.char[1],
                                     direction=4, priority=1),
                                  pg(None, sw=S_RUI, priority=0)])
    sailor = npc_speaker("Seemann", "Evil", 0)
    mb.npc("Sailor", 12, 8, sailor,
           Ev().say(sailor, ["Rui? Rui held the rope for three days. Then she cut it",
                             "and swam home. Nobody sits in her chair."]), direction=8)
    old = npc_speaker("Alter Kapitän", "People4", 0)
    mb.npc("Old Captain", 12, 11, old,
           Ev().say(old, ["The Knochenriff's a whale's graveyard. The Fomori live",
                          "in the biggest one. You walk in through its ribs."]), direction=8)
    return mb


# ---------------------------------------------------------------------------
# 121  Die Seeschwalbe (the deck, at sea)
# ---------------------------------------------------------------------------
def gen_schiff():
    g = Gen(30, 18, 2, seed=121)
    g.paint(g.all(), SEA)
    deck = g.rect(6, 6, 20, 11) | g.rect(21, 7, 22, 10) | g.rect(23, 8, 24, 9)
    g.tile(deck, 1539, z=0)
    for (x, y) in deck:
        if (x, y - 1) not in deck:
            g.set(x, y, 0, 1538)
        elif (x, y + 1) not in deck:
            g.set(x, y, 0, 1546)
    hull = {(x, y + 1) for (x, y) in deck if (x, y + 1) not in deck} | \
           {(x, y + 2) for (x, y) in deck if (x, y + 1) not in deck}
    g.paint(hull, 60)
    g.blocked |= hull
    for (x, y) in [(13, 6), (13, 7), (13, 8)]:
        g.set(x, y, 3, 19)
    g.blocked.add((13, 8))
    for (x, y, t) in [(7, 7, OUT.BARREL), (7, 10, OUT.BARREL), (8, 10, 181), (18, 7, 180), (18, 10, 183),
                      (19, 10, 181)]:
        g.stamp(x, y, [(0, 0, t)], force=True)
    g.finish()
    return g


def schiff():
    g = gen_schiff()
    T.reach_check(g, (11, 9), [(20, 8)], 'Seeschwalbe')
    mb = MapBuild(SCHIFF, NAMES[SCHIFF], g.m, display=NAMES[SCHIFF])
    mb.props(note="<Rank: A>\n<Area Name: Die Seeschwalbe>\n<lighting: Outside>", bgm=('Ship1', 60), bgs=('Sea', 50),
             battleback=('Ship', 'Ship'))
    rui = mb.npc("Kaizaki Rui", 8, 8, RUI, Ev().say(RUI, ["Mind the rail. The sea's hungry today."]), direction=6)
    kraken = mb.add("Kraken", 26, 11, [pg(None, direction=6, direction_fix=True, priority=1, step_anime=True,
                                          through=True)])
    shig = mb.add("Shigure", 26, 8, [pg(None, direction=4, direction_fix=True, priority=2, through=True)])
    # voyage 1: to the Knochenriff (drowned men board)
    v1 = Ev()
    v1.wait(20)
    v1.narrate(["The Seeschwalbe goes out past the harbour wall with",
                "nobody on her but Rui, three of Rui's cousins, and you.",
                "The sea is grey and very flat."])
    v1.say(RUI, ["Sixty men used to work this deck. Now it's four of us",
                 "and a dead general. No offence."])
    v1.say(HANMA, ["None taken. I've been a crew of one for seven hundred",
                   "years. Four is luxury."], 'smile')
    v1.wait(30)
    v1.se('Water1', 90, 70)
    v1.shake(3, 5, 20)
    v1.narrate(["Hands come up over the rail: grey, swollen, still",
                "wearing the rings of the men they were."])
    v1.say(RUI, ["Shigure's leftovers. Clear my deck!"])
    v1.battle(T3["Ertrunkene x3"])
    v1.say(RUI, ["…That one was Kōji. He owed me money."])
    v1.wait(20)
    v1.narrate(["By evening the Knochenriff comes up out of the sea: white",
                "reefs like the ribs of something enormous, and the smell",
                "of old salt and older bones."])
    v1.say(RUI, ["I'll wait with the ship. Bring me a crown."])
    v1.var(V_VOYAGE, 0)
    v1.switch(S_REEF)
    to_reef(v1)
    # voyage 2: the Sturmsee, Shigure
    v2 = Ev()
    v2.weather('storm', 6, 60)
    v2.bgs('Storm1', 60)
    v2.tint((-68, -68, -34, 68), 60)
    v2.narrate(["A day out the sky goes the colour of slate and the wind",
                "never stops. Then the drowned fleet: hulls standing up",
                "out of the water like tombstones."])
    v2.say(RUI, ["He's close. He can smell the crown on you."])
    v2.se('Water5', 100, 60)
    v2.shake(7, 6, 60)
    v2.set_image(kraken, '$BigMonster2', 0)
    v2.narrate(["Something vast rises beside the Seeschwalbe, tentacles",
                "and a beak, and on its back a knight in armour of black",
                "water."])
    v2.set_image(shig, SHIGURE.char[0], SHIGURE.char[1])
    v2.say(SHIGURE, ["The girl with the regalia. Kagerō said you would come",
                     "this way. He asked me to drown you gently."])
    v2.say(RUI, ["Sixty men, Shigure. You drowned them one at a time."])
    v2.say(SHIGURE, ["Did I? I don't remember them. I am sorry. That is the",
                     "truth."])
    v2.say(HANMA, ["A Calamity, my Lord. But four regalia: his rank will not",
                   "wall us out. Fight."], 'command')
    v2.battle(T3["Shigure"])
    v2.se('Water4', 90, 60)
    v2.narrate(["The Drowned Lance sinks to one knee on the kraken's back,",
                "and the kraken sinks under him, and the sea goes flat."])
    v2.set_image(kraken, '', 0)
    v2.say(SHIGURE, ["Tell… tell him the sea is warm. He'll understand. Tōma",
                     "always—"])
    v2.set_image(shig, '', 0)
    v2.narrate(["He goes under before he finishes."])
    v2.weather('none', 0, 90)
    v2.tint((0, 0, 0, 0), 90)
    v2.bgs('Sea', 50)
    v2.say(YUKINO, ["…Tōma always said he'd go somewhere the sea was warm,",
                    "after. Shigure promised to come and fish with him."])
    v2.say(HANMA, ["Then we carry the message, Yukino."], 'calm')
    v2.say(RUI, ["That's sixty. Thank you. The Schwarze Flagge owes you,",
                 "which is a thing I have never said to anyone."])
    v2.say(RUI, ["Here. Off a wyrm-hunter who doesn't need them any more.",
                 "They'll fit the big one."])
    v2.weapon(FW["Drachenknöchel"], 1)
    v2.notice(["Received the \\C[6]Drachenknöchel\\C[0]."])
    v2.quest_done(Q_RUI)
    v2.switch(S_SHIGURE)
    v2.var(V_VOYAGE, 0)
    back_to_port(v2)
    mb.add("Voyage", 0, 0, [pg(v1, var=(V_VOYAGE, 1), trigger=3, priority=0),
                            pg(v2, var=(V_VOYAGE, 2), trigger=3, priority=0)])
    return mb


# ---------------------------------------------------------------------------
# 122  Knochenriff
# ---------------------------------------------------------------------------
REEF_LANDING = (4, 17)
REEF_DOOR = (39, 7)


def gen_reef():
    g = Gen(46, 34, 2, seed=122)
    g.paint(g.all(), SEA)
    islands = [g.blob(7, 17, 4.2, seed=1), g.blob(17, 9, 4.5, seed=2), g.blob(18, 25, 4.3, seed=3),
               g.blob(29, 17, 5.0, seed=4), g.blob(39, 9, 5.2, seed=5), g.blob(38, 26, 3.6, seed=6)]
    land = set().union(*islands) | g.rect(3, 15, 7, 19)
    bars = g.line([(9, 15), (16, 11)], 3) | g.line([(9, 19), (17, 24)], 3) | g.line([(19, 11), (28, 15)], 3) | \
        g.line([(20, 24), (28, 19)], 3) | g.line([(32, 15), (38, 11)], 3) | g.line([(31, 20), (37, 25)], 3)
    land = (land | bars) & g.rect(2, 2, 44, 31)
    g.paint(land, OUT.SAND)
    g.paint(bars & land, OUT.SAND_STONES)
    # the whale-rib hall: a rock outcrop on the east island with a mouth
    rock = g.rect(36, 3, 42, 5)
    g.paint(g.grow(rock, 1) - rock, OUT.SAND)
    g.cliff(rock, *OUT.ROCK2, height=2)
    g.set(REEF_DOOR[0], REEF_DOOR[1], 3, 134)
    g.keep_clear |= {REEF_DOOR, (REEF_DOOR[0], REEF_DOOR[1] + 1), REEF_LANDING}
    g.keep_clear |= g.grow(bars, 0)
    # bones and wrecks
    free = {c for c in land if c not in g.blocked and c not in g.keep_clear}
    g.scatter_in(free, [[(0, 0, 280)], [(0, 0, 281)], [(0, 0, 206)], [(0, 0, 228)], [(0, 0, 244)],
                        [(0, 0, 159)], [(0, 0, 167)], OUT.DEADTREE, OUT.DEADTREE2], 34, spacing=1)
    g.finish()
    return g, land


def knochenriff():
    g, land = gen_reef()
    R = T.reach_check(g, REEF_LANDING, [(REEF_DOOR[0], REEF_DOOR[1] + 1), (38, 26), (18, 25)], 'Knochenriff')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(KNOCHENRIFF, NAMES[KNOCHENRIFF], g.m, display=NAMES[KNOCHENRIFF])
    mb.props(note="<Rank: A>\n<Area Name: Knochenriff>\n<lighting: Outside>", bgm=('Dungeon5', 55),
             bgs=('Wave2', 40), battleback=('Sand', 'Cliff'), encounters=SEA_ENC(), steps=26)
    el = Ev()
    el.narrate(["The Knochenriff: reefs of white bone and white coral, and",
                "the bones are whales, mostly. Some are not."])
    el.say(FALIN, ["Something's watching from the water."], 'calm')
    el.say(HANMA, ["Everything here is watching from the water. Keep to the",
                   "sand, my Lord."], 'stern')
    el.rest_point(KNOCHENRIFF, REEF_LANDING[0], REEF_LANDING[1], 6)
    mb.autorun("Knochenriff", el)
    # the Seeschwalbe at anchor, and Rui
    mb.add("Seeschwalbe", REEF_LANDING[0] - 2, REEF_LANDING[1], [pg(None, char='Vehicle', index=1, direction=6,
                                                                    priority=1, step_anime=True, direction_fix=True)])
    rui_at = sp((REEF_LANDING[0], REEF_LANDING[1] - 1), avoid=[REEF_LANDING])
    ship = Ev().say(RUI, ["Back to Salzhafen?"])
    ship.choices(["Sail back to Salzhafen", "Stay"], [back_to_port, None], cancel=1)
    mb.npc("Kaizaki Rui", rui_at[0], rui_at[1], RUI, ship, direction=2)
    # the mouth of the hall
    mb.add("The Whale Mouth", REEF_DOOR[0], REEF_DOOR[1],
           [pg(Ev().se('Move1', 60).transfer(VERSUNKENE_HALLE, 16, 28, 8, 0), trigger=1, priority=1)])
    # rest, chests
    fire = sp((29, 17))
    rest = sp((fire[0], fire[1] + 1), avoid=[fire])
    camp_fire(mb, fire[0], fire[1], KNOCHENRIFF, rest[0], rest[1], 8, ["Driftwood, and a ring of whale vertebrae",
                                                                       "someone once sat on."])
    c1 = sp((18, 26))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Großes Elixier"], 3), e.item(FI["Äther"], 2)),
          "Found 3 Großes Elixier and 2 Äther.")
    c2 = sp((38, 27))
    chest(mb, "Chest", c2[0], c2[1], lambda e: e.armor(FA["Seefahrerhelm"], 1), "Found a Seefahrerhelm.")
    c3 = sp((17, 7))
    chest(mb, "Chest", c3[0], c3[1], lambda e: e.gold(250000), "Found \\MONEY[250000] in a drowned purse.")
    return mb


# ---------------------------------------------------------------------------
# 123  Versunkene Halle (inside the whale)
# ---------------------------------------------------------------------------
def gen_halle():
    g = Gen(34, 32, 4, seed=123)
    rooms = [(13, 23, 20, 29), (4, 3, 29, 16), (3, 20, 9, 27), (24, 20, 30, 27)]
    halls = [([(16, 23), (16, 16)], 3), ([(9, 25), (13, 25)], 3), ([(20, 25), (24, 25)], 3)]
    open_ = T.rooms_and_halls(g, rooms, halls, 112, 120, DUN.ROCK, wall_h=2, ring=1)
    # flooded aisles and the ribs of the whale
    for r in (g.rect(6, 8, 9, 14), g.rect(24, 8, 27, 14)):
        g.paint(r, DUN.WATER)
        g.blocked |= r
    for x in (12, 21):
        for y in (8, 11, 14):
            g.stamp(x, y, T.PILLAR, force=True)
    # the throne of anchors: bones and gold around a stone seat
    g.stamp(16, 6, [(0, 0, 72)], force=True)
    for (x, y, t) in [(14, 6, 204), (18, 6, 205), (13, 5, 240), (19, 5, 241), (15, 5, 234), (17, 5, 234)]:
        g.stamp(x, y, [(0, 0, t)], force=True)
    free = {c for c in open_ if c not in g.blocked and c not in g.keep_clear and g.kind_at(*c) == DUN.ROCK}
    g.keep_clear |= g.line([(16, 29), (16, 7)], 3)
    free -= g.keep_clear
    g.scatter_in(free, [[(0, 0, 248)], [(0, 0, 249)], [(0, 0, 250)], [(0, 0, 238)], [(0, 0, 130)], [(0, 0, 131)]],
                 18, spacing=1)
    g.finish()
    return g


def versunkene_halle():
    g = gen_halle()
    R = T.reach_check(g, (16, 28), [(16, 8), (5, 22), (28, 22)], 'Versunkene Halle')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(VERSUNKENE_HALLE, NAMES[VERSUNKENE_HALLE], g.m, display=NAMES[VERSUNKENE_HALLE])
    mb.props(note="<Rank: A>\n<Area Name: Versunkene Halle>", bgm=('Dungeon6', 55), bgs=('Drips', 45),
             battleback=('Stone3', 'Ruins2'), encounters=HALL_ENC(), steps=30)
    for x in (15, 16, 17):
        mb.add("Out", x, 29, [pg(Ev().se('Move1', 60).transfer(KNOCHENRIFF, REEF_DOOR[0], REEF_DOOR[1] + 1, 2, 0),
                                 trigger=1, priority=0)])
    el = Ev()
    el.narrate(["Inside the whale: ribs as tall as a church, a floor of",
                "old stone laid by somebody long before the Fomori, and",
                "sea water in the aisles, black and perfectly still."])
    el.say(YUKINO, ["…The crown is here. I can feel it the way you feel a",
                    "fire behind a door."])
    mb.autorun("The Hall", el)
    # Fomori on guard (visible, one fight each)
    for (x, y) in [(16, 20), (8, 10), (25, 16)]:
        c = sp((x, y))
        fe = Ev()
        fe.battle(T3["Fomorer x2"])
        fe.self_switch('A')
        mb.add("Fomor", c[0], c[1], [pg(fe, char='Monster', index=1, direction=2, trigger=2, priority=1,
                                        move_type=1, step_anime=True),
                                     pg(None, self_sw='A', priority=0)])
    c1 = sp((5, 22))
    chest(mb, "Chest", c1[0], c1[1], lambda e: e.armor(FA["Sturmschild"], 1), "Found a Sturmschild.")
    c2 = sp((28, 22))
    chest(mb, "Chest", c2[0], c2[1], lambda e: (e.item(FI["Manastein (A)"], 2), e.item(FI["Äther"], 2)),
          "Found 2 Manastein (A) and 2 Äther.")
    # the chief on the throne of anchors
    chief_at = (16, 7)
    chief = mb.add("Fomorian Chief", chief_at[0], chief_at[1],
                   [pg(None, char='Evil', index=5, direction=2, priority=1), pg(None, sw=S_KRONE, priority=0)])
    def fight(e):
        e.narrate(["On a throne of anchors and whale-bone sits the chief:",
                   "one eye, a mouth full of broken teeth, and on his head a",
                   "crown of ash-grey iron that smokes where it touches him."])
        e.say(HANMA, ["The Aschenkrone. It hates him. He wears it anyway,",
                      "because it frightens the others. Take it off him, my",
                      "Lord."], 'stern')
        e.battle(T3["Fomorer-Häuptling"])
        e.switch(S_KRONE)
        e.se('Collapse4')
        e.narrate(["The chief falls, and the crown rolls off his head and",
                   "stops at Kanta's feet, quite cool now."])
        e.set_image(chief, '', 0)
        regalia_gain(e, "Aschenkrone", "4 of 4")
        e.say(HANMA, ["All four, my Lord. The morning blade, the light, the",
                      "horn and the crown. Akira carried them to the last",
                      "battle. Now you do."], 'calm')
        e.say(FALIN, ["…It's warm. The crown. Like a hearth."], 'calm')
        e.say(YUKINO, ["Shigure will smell it on us now. Good."])
        e.quest_done(Q_KRONE)
        e.quest_desc(Q_RUI, "Rui's turn: sail into the Sturmsee from Salzhafen and fight Shigure with her.")
    trigger_line(mb, [(x, 9) for x in (15, 16, 17)], "Throne Steps", fight, S_KRONE)
    mb.light('cave_dark', 0, 0, tile=False)
    mb.light('pool', 8, 11)
    mb.light('pool', 25, 11)
    mb.light('brazier', 16, 6)
    return mb


# ---------------------------------------------------------------------------
# 124  Brennender Urwald
# ---------------------------------------------------------------------------
def urwald_brand():
    g = gen_urwald(seed=113, burning=True)
    R = T.reach_check(g, (20, 1), [(26, 38)], 'Brennender Urwald')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(URWALD_BRAND, NAMES[URWALD_BRAND], g.m, display=NAMES[URWALD_BRAND])
    mb.props(note="<Rank: A>\n<Area Name: Brennender Urwald>\n<lighting: Outside>", bgm=('Battle5', 55),
             bgs=('Fire2', 50), battleback=('Grassland', 'Forest'), encounters=FIRE_ENC(), steps=26,
             weather='snow 4')
    for x in range(g.w):
        if (x, 0) in R and (x, 1) in R:
            mb.add("North", x, 0, [pg(Ev().se('Move1', 60).transfer(HIRSCHHEIM, 21, 38, 8, 0), trigger=1, priority=0)])
        if (x, g.h - 1) in R and (x, g.h - 2) in R:
            mb.add("South", x, g.h - 1, [pg(Ev().if_switch(S_GOEN, True,
                                                          lambda b: (b.se('Move1', 60),
                                                                     b.transfer(HIRSCHTHRON_NACHT, 16, 1, 2, 0)),
                                                          lambda b: b.text(["Brass and fire. The way is shut."])),
                                            trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The Urwald is burning. Not the way forests burn: in",
                "rows, in lanes, cut and fired by people who know",
                "exactly where they are going."])
    el.narrate(["Ash comes down like snow. Somewhere south, a horn made",
                "of brass keeps blowing the same three notes."])
    el.say(KAGURA, ["Vessel! My rangers are holding the fire at the north",
                    "edge. The rest is theirs. Go. Please."])
    el.say(HANMA, ["He's cutting a road to the throne. Gōen first. Then him."], 'stern')
    el.quest_desc(Q_END, "Through the burning Urwald to the Hirschthron. Gōen leads the Host of Ash.")
    mb.autorun("Fire", el)
    ranger_at = sp((20, 4))
    mb.npc("Countess Kagura", ranger_at[0], ranger_at[1], KAGURA,
           Ev().say(KAGURA, ["Hirschheim remembers its friends. Come back to it."]), direction=2)
    # the leshy, burned
    lc = sp((15, 22))
    leshy = Ev()
    leshy.text(["The leshy leans on the flat stone, half of it charcoal,",
                "sap running like tears out of the cracks."])
    leshy.say(npc_speaker("Leshy", "", 0), ["…Light. Horn. Crown. Sword. All of them, at last.",
                                            "Too late for my trees. Not too late for my throne."])
    leshy.say(npc_speaker("Leshy", "", 0), ["The golden one sits in my clearing. The quiet one waits",
                                            "at my throne. Go through them."])
    leshy.se('Heal3')
    leshy.recover_all()
    leshy.notice(["The leshy breathes on you: HP and MP restored."])
    mb.add("Leshy", lc[0], lc[1], [pg(leshy, char='$BigMonster1', index=0, direction=4, priority=1,
                                      direction_fix=True, step_anime=True)])
    fire = sp((33, 12))
    rest = sp((fire[0], fire[1] + 1), avoid=[fire])
    camp_fire(mb, fire[0], fire[1], URWALD_BRAND, rest[0], rest[1], 8, ["Kagura's rangers left this fire burning",
                                                                        "on purpose: a fire that belongs to you."])
    c1 = sp((8, 26))
    chest(mb, "Chest", c1[0], c1[1], lambda e: (e.item(FI["Großes Elixier"], 4), e.item(FI["Äther"], 3)),
          "Found 4 Großes Elixier and 3 Äther.")
    # fires in the undergrowth (off the road, never on a tile an event or the path needs)
    rng = __import__('random').Random(124)
    busy = {(e['x'], e['y']) for e in mb.m['events'][1:] if e}
    road = g.grow(g.keep_clear, 1)
    spots = sorted(c for c in R if c not in busy and c not in road and c[1] > 3)
    for c in rng.sample(spots, 14):
        mb.add("Fire", c[0], c[1], [pg(None, char='!Flame', index=rng.choice([0, 1, 2]), direction=2, priority=0,
                                       step_anime=True, walk_anime=False)])
    # Gōen's clearing in the south
    line_y = 32
    cells = [x for x in range(g.w) if (x, line_y) in R]
    gx = sum(cells) // len(cells)
    goen_at = sp((gx, line_y + 3))
    goen = mb.add("Gōen", goen_at[0], goen_at[1], [pg(None, char=GOEN.char[0], index=GOEN.char[1], direction=8,
                                                       priority=1),
                                                    pg(None, sw=S_GOEN, priority=0)])
    guards = []
    for dx in (-2, 2):
        c = sp((goen_at[0] + dx, goen_at[1]), avoid=[goen_at])
        guards.append(mb.add("Brass Guard", c[0], c[1], [pg(None, char='Monster', index=3, direction=8, priority=1),
                                                          pg(None, sw=S_GOEN, priority=0)]))
    def clearing(e):
        e.gather()
        e.narrate(["A clearing of stumps. In the middle, on a throne of",
                   "brass hauled all the way from the Nordwall, sits Gōen,",
                   "chains wrapped around his arms, smiling."])
        e.say(GOEN, ["Little vessel! And the General. I saved you a seat.",
                     "Sign with me, and your vessels never run out. Every one",
                     "of them will be mine, of course. Details."])
        e.say(KANTA, ["No."], 'fierce')
        e.say(GOEN, ["Everyone says no at first."])
        e.say(HANMA, ["Not everyone, Gōen. I said yes, once. She said no for",
                      "me. Now she says it for herself."], 'stern')
        e.battle(T3["Gōen (Urwald)"])
        e.if_switch(S_BREAK_A, False, late_break_a)
        e.switch(S_GOEN)
        e.se('Collapse4')
        e.narrate(["The Brass Tyrant falls in his own clearing, and the Host",
                   "behind him stops, all at once, like a clock whose spring",
                   "has broken. Then it starts to run."])
        e.say(GOEN, ["…Collection is… overdue…"])
        e.text(["Out of his coat falls a contract, very old, the ink gone",
                "brown. At the bottom, a name that was never signed: the",
                "name of a general of the Dawn Host."])
        e.say(HANMA, ["…Burn it, my Lord."], 'calm')
        e.se('Fire1')
        e.text(["Kanta holds it to the light. It goes up like dry leaves."])
        e.set_image(goen, '', 0)
        for gd in guards:
            e.set_image(gd, '', 0)
        e.say(HANMA, ["Seven hundred years that thing waited for me. …Thank",
                      "you."], 'smile')
        e.say(YUKINO, ["He's at the throne. I can feel the cold of him from here."])
        e.quest_desc(Q_END, "Gōen is dead. Kagerō waits at the Hirschthron, south of the clearing.")
        e.rest_point(URWALD_BRAND, rest[0], rest[1], 8)
    trigger_line(mb, [(x, line_y) for x in cells], "Clearing", clearing, S_GOEN)
    return mb


def late_break_a(e):
    """The breakthrough to A still happens if Gōen fell before the troop page ran."""
    e.say(HANMA, ["My Lord, the regalia are still singing. Take it!"], 'command')
    e.se('Magic3', 90, 60)
    e.flash((255, 250, 220, 255), 60)
    e.breakthrough()
    e.switch(S_BREAK_A)


# ---------------------------------------------------------------------------
# 125  Hirschthron (Nacht): Kagerō
# ---------------------------------------------------------------------------
def hirschthron_nacht():
    g = gen_throne(night=True)
    R = mapinfo.region(g.m, 16, 1)
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(HIRSCHTHRON_NACHT, NAMES[HIRSCHTHRON_NACHT], g.m, display="Hirschthron")
    mb.props(note="<Rank: SS>\n<Area Name: Hirschthron>\n<lighting: Outside>", bgm=('Dungeon7', 55),
             bgs=('Darkness', 40), battleback=('Grassland', 'Forest'), weather='snow 5')
    for x in range(14, 19):
        mb.add("North", x, 0, [pg(Ev().if_switch(S_END, False,
                                                 lambda b: (b.se('Move1', 60), b.transfer(URWALD_BRAND, 26, 38, 8, 0))),
                                  trigger=1, priority=0)])
    el = Ev()
    el.set_time(1, 0)
    el.narrate(["Night. The standing stones of the Hirschthron are black",
                "against a red sky, and the sky is falling in grey flakes",
                "that are not snow."])
    el.say(HANMA, ["The last of it, my Lord. Rest by the lantern first, if",
                   "you need to. He isn't going anywhere."], 'calm')
    el.rest_point(HIRSCHTHRON_NACHT, 16, 4, 2)
    mb.autorun("Night", el)
    lamp = Ev()
    lamp.text(["Kanta sets the Sternlaterne on a stone. Its light makes a",
               "small, warm room in the dark."])
    def rest(b):
        b.fadeout()
        b.recover_all()
        b.rest_point(HIRSCHTHRON_NACHT, 16, 4, 2)
        b.wait(40)
        b.fadein()
        b.text(["You rest in the lantern's light. (HP and MP restored. If",
                "you fall, you'll wake here.)"])
    lamp.choices(["Rest", "Go on"], [rest, None], cancel=1)
    lamp_at = sp((18, 3), avoid=[(16, 4)])
    mb.add("Sternlaterne", lamp_at[0], lamp_at[1], [pg(lamp, char='!Other2', index=3, direction=2, priority=1,
                                                       step_anime=True)])
    mb.light('ash_night', 0, 0, tile=False)
    mb.light('hearth', lamp_at[0], lamp_at[1])
    mb.light('gate_fire', 16, 15)
    # Kagerō on the throne; his later shapes follow the phase switches
    kag = mb.add("Kagerō", 16, 16, [pg(None, char=KAGERO.char[0], index=KAGERO.char[1], direction=2, priority=1),
                                    pg(None, sw=S_PH1, char='$BigMonster2', index=0, direction=8, priority=1,
                                       direction_fix=True, step_anime=True),
                                    pg(None, sw=S_PH2, char=TOMA.char[0], index=TOMA.char[1], direction=8, priority=1),
                                    pg(None, sw=S_END, priority=0)])

    def phase1(b):
        b.gather()
        b.narrate(["On the throne of stone and antler sits a man in armour",
                   "of ash, with no face you can hold in your mind. He",
                   "stands up. He is not tall. He sounds tired."])
        b.say(KAGERO, ["The one with the regalia. And a dead general. And a",
                       "living armour. And— Yuki."])
        b.say(KAGERO, ["It's a good party. Mine was better. They all died,",
                       "because they believed in things."])
        b.say(KANTA, ["Why the seals?"], 'calm')
        b.say(KAGERO, ["Because under the world there is a father who makes",
                       "monsters, and above it there are gods who make heroes",
                       "to kill them, and it never, ever ends."])
        b.say(KAGERO, ["I am going to eat the father, and then I am going to be",
                       "the last thing that ever happens. It will be quiet.",
                       "You'll like it."])
        b.say(HANMA, ["My Lord. With all four, his veil will not hold."], 'command')
        b.narrate(["Yukino says nothing. Her hand is white on her sword."])
        b.bgm('Battle8', 100)
        b.battle(T3["Kagerō"])
        b.se('Crash', 90, 70)
        b.shake(8, 7, 50)
        b.narrate(["The ash armour cracks. Kagerō goes down on one knee,",
                   "and out of the cracks something pours up into the sky:",
                   "a shadow with too many arms, and no face at all."])
        b.switch(S_PH1)
        b.say(HOKAI, ["WE ARE THE QUIET AFTER. HE ASKED FOR QUIET. WE ARE",
                      "KEEPING OUR PROMISE."])
        b.say(YUKINO, ["That's the voice from the rift. That's what spoke to him."])
        b.say(HANMA, ["Then that's the thing we kill. Not him. Not yet."], 'command')

    def phase2(b):
        b.se('Saint4', 90, 80)
        b.flash((255, 240, 200, 200), 40)
        b.narrate(["The Sternlaterne flares at Kanta's belt, the four regalia",
                   "sing together, and for a moment the dark is only dark."])
        b.recover_all()
        b.notice(["HP and MP restored."])
        b.bgm('Battle8', 100, 90)
        b.battle(T3["Hōkais Schatten"])
        b.se('Darkness5', 90, 70)
        b.narrate(["The shadow screams without a mouth and falls back into",
                   "the man it came out of, the way smoke goes back into a",
                   "fire that is going out."])
        b.switch(S_PH2)
        b.say(TOMA, ["…It's gone quiet. Oh, it's so quiet."])
        b.say(TOMA, ["No. No, it's still in there. I can't stop. It doesn't",
                     "let me stop. Yuki, get out of the way."])
        b.say(YUKINO, ["No."])

    def phase3(b):
        b.say(FALIN, ["Once more. I've got you, all of you."], 'fierce')
        b.recover_all()
        b.notice(["HP and MP restored."])
        b.bgm('Battle7', 100)
        b.battle(T3["Kurenai Tōma"])
        ending(b)

    def ending(b):
        b.fade_bgm(3)
        b.wait(40)
        b.narrate(["Kurenai Tōma kneels in the ash. The last of the grey runs",
                   "out of him like water, and he is a man of about thirty",
                   "with a scar through one eyebrow, looking very surprised."])
        b.say(TOMA, ["Yuki. You got old."])
        b.say(YUKINO, ["You didn't."])
        b.say(TOMA, ["Tell Rin I'm sorry about her brother. I remember him. He",
                     "was brave, and I hated him for it."])
        b.say(TOMA, ["And you. Vessel girl. It doesn't end, you know. There'll",
                     "be another one of me."])
        b.say(KANTA, ["Then there'll be another one of me."], 'calm')
        b.say(YUKINO, ["Shigure said to tell you. The sea is warm."])
        b.say(TOMA, ["…Ha. Liar. It never was. …Thank you, Yuki."])
        b.se('Darkness3', 80, 80)
        b.narrate(["He laughs, once, and then he is ash, and then the ash",
                   "stops falling."])
        b.switch(S_END)
        b.weather('none', 0, 120)
        b.fade_bgs(4)
        b.wait(60)
        b.set_time(5, 30)
        b.bgm('Theme4', 80)
        b.narrate(["For the first time in twelve years, the dawn comes up",
                   "red and gold over the Tiefenwald, and nothing in the",
                   "north is burning."])
        b.say(HANMA, ["It is done, my Lord."], 'calm')
        b.say(KANTA, ["I'm still not a hero."], 'wry')
        b.say(HANMA, ["No. Something better. Someone who keeps coming back."], 'smile')
        b.quest_done(Q_END)
        b.fadeout()
        b.card("Morgenröte", "Wochen später", 180)
        b.transfer(EPILOG_WALL, *EPI_WALL_POS, 8, 0)

    def throne(e):
        e.if_switch(S_PH1, False, phase1)
        e.if_switch(S_PH2, False, phase2)
        phase3(e)

    trigger_line(mb, [(x, 10) for x in range(g.w) if (x, 10) in R], "The Throne", throne, S_END)

    return mb


# ---------------------------------------------------------------------------
# 126-129  the epilogue, on old maps (tiles and scenery copied, only the scene's events)
# ---------------------------------------------------------------------------
EPI_WALL_POS = (33, 10)
EPI_WF_POS = (22, 10)
EPI_RABENAU_POS = (13, 24)
EPI_KAMM_POS = (12, 10)


def epilog_map(map_id, source_id, display, start):
    src = MapBuild.registry[source_id].m
    mb = MapBuild(map_id, NAMES[map_id], copy.deepcopy(src), display=display)
    reg = mapinfo.region(mb.m, *start)
    if start not in reg:
        raise ValueError(f'epilogue {map_id}: start {start} not walkable')
    return mb, reg


def near(mb, reg, at, taken):
    best = None
    busy = {(e['x'], e['y']) for e in mb.m['events'][1:] if e}
    for c in reg:
        if c in taken or c in busy:
            continue
        d = abs(c[0] - at[0]) + abs(c[1] - at[1])
        if best is None or d < best[0]:
            best = (d, c)
    taken.add(best[1])
    return best[1]


def epilog_wall():
    mb, reg = epilog_map(EPILOG_WALL, WALLFESTE, "Wallfeste", EPI_WALL_POS)
    mb.props(note="<Area Name: Wallfeste>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Theme2', 70),
             bgs=('Wind1', 25))
    taken = {EPI_WALL_POS}
    k = near(mb, reg, (EPI_WALL_POS[0] - 2, EPI_WALL_POS[1] + 1), taken)
    kos = mb.add("Kōsaka", k[0], k[1], [pg(None, char=KOSAKA.char[0], index=KOSAKA.char[1], direction=6, priority=1)])
    y = near(mb, reg, (EPI_WALL_POS[0] + 1, EPI_WALL_POS[1] - 1), taken)
    yuk = mb.add("Yukino", y[0], y[1], [pg(None, direction=8, priority=1, through=True)])
    el = Ev()
    el.set_time(10, 0)
    el.fadein()
    el.narrate(["Weeks later, the Nordwall counts its dead and its living.",
                "Marshal Kōsaka sleeps for two days, and wakes up asking",
                "for tea."])
    el.say(KOSAKA, ["The Empress's legions are on the Aschenfeld. They say the",
                    "snow up there is falling white again."])
    el.say(KOSAKA, ["The Wall stands. Because a vessel and a ghost walked",
                    "through its gate one winter. I'll have that carved over",
                    "the gate, if the stonemasons can spell."])
    el.party(YUKINO_ID, False)
    el.set_image(yuk, YUKINO.char[0], YUKINO.char[1])
    el.face_dir(yuk, 2)
    el.say(YUKINO, ["I want to see Frostheim once more. And tell them. The",
                    "other three."])
    el.say(KANTA, ["Come back after."], 'calm')
    el.say(YUKINO, ["…I'll try. That's new, too."])
    el.route(yuk, [37, 19] + [4] * 6, wait=True)
    el.route(yuk, [39], wait=True)
    el.say(HANMA, ["She'll come back, my Lord. People do, for you."], 'smile')
    el.fadeout()
    el.transfer(EPILOG_WEISSENFELS, *EPI_WF_POS, 8, 0)
    mb.autorun("Epilogue", el)
    return mb


def epilog_weissenfels():
    mb, reg = epilog_map(EPILOG_WEISSENFELS, WF_UNTERSTADT, "Weißenfels", EPI_WF_POS)
    mb.props(note="<Area Name: Weißenfels>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Theme5', 70),
             bgs=('Wind1', 25), weather='snow 1')
    taken = {EPI_WF_POS}
    r = near(mb, reg, (EPI_WF_POS[0], EPI_WF_POS[1] - 2), taken)
    mb.add("Rin", r[0], r[1], [pg(None, char=RIN.char[0], index=RIN.char[1], direction=8, priority=1)])
    s = near(mb, reg, (EPI_WF_POS[0] - 2, EPI_WF_POS[1] - 1), taken)
    mb.add("Sōma", s[0], s[1], [pg(None, char=SOMA.char[0], index=SOMA.char[1], direction=6, priority=1)])
    h = near(mb, reg, (EPI_WF_POS[0] + 2, EPI_WF_POS[1] - 1), taken)
    mb.add("Hikari", h[0], h[1], [pg(None, char=HIKARI.char[0], index=HIKARI.char[1], direction=4, priority=1)])
    el = Ev()
    el.fadein()
    el.narrate(["In Weißenfels, Princess Rin buries her brother's sword",
                "under the gate of the citadel."])
    el.say(RIN, ["…Kanta. Is it done?"])
    el.say(KANTA, ["It's done. He asked me to tell you he was sorry about",
                   "your brother. He remembered him. He said Hayato was",
                   "brave."], 'calm')
    el.say(RIN, ["…He was. He was an idiot, and he was brave."])
    el.say(SOMA, ["Weißenfels will have a gate again by spring, Highness."])
    el.say(HIKARI, ["And a bell. I want a bell."])
    el.say(RIN, ["There's a place at the table of this house for the three",
                 "of you. Always. Even the one who doesn't eat."])
    el.say(HANMA, ["I'll sit very politely, Highness."], 'smile')
    el.fadeout()
    el.transfer(EPILOG_RABENAU, *EPI_RABENAU_POS, 8, 0)
    mb.autorun("Epilogue", el)
    return mb


def epilog_rabenau():
    mb, reg = epilog_map(EPILOG_RABENAU, RABENAU, "Rabenau", EPI_RABENAU_POS)
    mb.props(note="<Area Name: Rabenau>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Town1', 70))
    taken = {EPI_RABENAU_POS}
    k = near(mb, reg, (EPI_RABENAU_POS[0] + 2, EPI_RABENAU_POS[1] - 1), taken)
    mb.add("Hayate", k[0], k[1], [pg(None, char=HAYATE.char[0], index=HAYATE.char[1], direction=4, priority=1,
                                     step_anime=True)])
    for dx, dy, who in ((3, -2, ("People1", 0)), (4, -1, ("People1", 3)), (4, 0, ("People2", 2))):
        c = near(mb, reg, (EPI_RABENAU_POS[0] + dx, EPI_RABENAU_POS[1] + dy), taken)
        mb.add("Listener", c[0], c[1], [pg(None, char=who[0], index=who[1], direction=4, priority=1)])
    t = near(mb, reg, (EPI_RABENAU_POS[0] - 2, EPI_RABENAU_POS[1]), taken)
    mb.add("Tōdō", t[0], t[1], [pg(None, char=TODO.char[0], index=TODO.char[1], direction=6, priority=1)])
    el = Ev()
    el.fadein()
    el.narrate(["In Lichtenhall, Kirishima Daigo writes Kanta's name into",
                "the Guild's book, and under it, after a long time, a",
                "second name: Hanma."])
    el.narrate(["In Rabenau, a boy named Hayate tells everyone who will",
                "listen that he once looked at the vessel's light from",
                "this close. Nobody believes him. He does not care."])
    el.say(HAYATE, ["It was warm! Like holding a morning! And the ghost said",
                    "I could look as long as I wanted!"])
    el.say(HANMA, ["I did say that."], 'smile')
    el.say(TODO, ["…Welcome back, Kanta. Your room at the Raven's still",
                  "yours. Nobody else wanted it. It's haunted, apparently."])
    el.say(KANTA, ["It is."], 'wry')
    el.fadeout()
    el.transfer(EPILOG_KAMM, *EPI_KAMM_POS, 2, 0)
    mb.autorun("Epilogue", el)
    return mb


def epilog_kamm():
    mb, reg = epilog_map(EPILOG_KAMM, RIDGE, "Kiefernkamm", EPI_KAMM_POS)
    mb.props(note="<Area Name: Kiefernkamm>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Theme1', 75),
             bgs=('Wind1', 30))
    el = Ev()
    el.set_time(7, 0)
    el.fadein()
    el.narrate(["The Kiefernkamm, where it began: pines, and grey stone,",
                "and this time no rain."])
    el.say(HANMA, ["Where now, my Lord?"], 'calm')
    el.say(KANTA, ["Wherever there's work. You coming?"], 'calm')
    el.say(HANMA, ["Always."], 'smile')
    el.say(FALIN, ["…Me too. Obviously."], 'smile')
    el.switch(SW('Game Cleared'))
    el.wait(60)
    el.card("Erdenkreis", "Ende", 300)
    el.fadeout()
    el.narrate(["Erdenkreis. Thank you for playing.",
                "",
                "Plugins: TausiLighting (MelekTaus), WD_Quest (Winthorp",
                "Darkrites), McKathlin_DayNight (McKathlin)."])
    el.narrate(["Art: RPG Maker MZ RTP and DLC (Yutaro Tsuyuki and",
                "others), battlers after Nemo's work. Story systems: Ten",
                "and Claude."])
    el.to_title()
    mb.autorun("The End", el)
    return mb
