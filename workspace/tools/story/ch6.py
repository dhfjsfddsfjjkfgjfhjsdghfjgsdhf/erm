"""Chapter 6: Der Messingtyrann. The Host at the Wall: the Wallfeste under siege, the gate tower, Frontposten 3,
the Host's camp on the Aschenfeld and its soul cauldron, Gōen's offer, the unwinnable fight and Kanta's
breakthrough to C; Tsukishiro Yukino walks out of the ash. End of Act II."""
import copy, json
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story import foes
from story.ids import *
from story.ch1 import chest
from story.ch2 import camp_fire
from story.cast import *
from story.ch5 import S_C5_END, RIN_ID
from story import terrain as T
from story.terrain import Gen, OUT, DUN, auto

KI = foes.KEY
FI = foes.ITEMS
FA = foes.ARMORS
FW = foes.WEAPONS
YUKINO_ID = 6
V_REGALIA_NAME = 'Regalia'

WF_COOK = npc_speaker("Feldkoch Hanamura", "People2", 7)
CLERK = npc_speaker("Schreiber", "People1", 4)
SGT_KONO = npc_speaker("Sergeant Kōno", "People3", 4)

# ----------------------------------------------------------------------- quests
Q_SIEGE = Quest(23, "Der Messingtyrann", "Kōsaka Tetsuji", "Nordwall",
                "The whole Host came out of the Aschenfeld at once. Gōen himself leads it. The Wallfeste and "
                "Frontposten 3 are under siege.",
                "The Wallfeste: find the Marshal.")
Q_TOWER = Quest(24, "Der Torturm", "Kōsaka Tetsuji", "Wallfeste, Torturm",
                "The Host is inside the gate tower over the north gate. If it takes the winch, the gate opens. Clear "
                "the tower from the bottom up and drop the portcullis.",
                "The north gate of the Wallfeste, the tower door.")
Q_KESSEL = Quest(25, "Der Seelenkessel", "Mori Daisuke", "Aschenfeld",
                 "Every soldier who falls on the Wall gets up again for the Host. In its camp on the Aschenfeld a "
                 "cauldron boils the souls of the dead back into their bodies. Mori will open the sally port in the "
                 "new stone of the breach.",
                 "Frontposten 3: through the inner gate and the sally port.")

# ----------------------------------------------------------------------- switches
S_C6 = SW('C6: The Siege')
S_TOWER1 = SW('C6: Tower Floor 1')
S_TOWER2 = SW('C6: Tower Floor 2')
S_TOWER_DONE = SW('C6: Portcullis Down')
S_TO_FP3 = SW('C6: Sortie Ordered')
S_FP3_HOUNDS = SW('C6: FP3 Courtyard Clear')
S_SORTIE = SW('C6: Through the Breach')
S_KESSEL = SW('C6: Cauldron Broken')
S_BREAK_C = SW('C6: Breakthrough C')
S_YUKINO = SW('C6: Yukino Came')
S_FIRE6 = SW('C6: The Fire at FP3')
S_C6_END = SW('C6: Act II Done')
V_REGALIA = VAR(V_REGALIA_NAME)

SIEGE_ENC = lambda: [(TR["Messingsoldaten x3"], 5, ()), (TR["Soldaten & Oni"], 4, ()), (TR["Höllenhunde x2"], 3, ())]


def build():
    return [wallfeste_siege(), torturm(), fp3_siege(), aschenlager()]


def base_map(map_id):
    return json.load(open(f'{BASE}/Map{map_id:03d}.json', encoding='utf-8'))


# ---------------------------------------------------------------------------
# 92  Wallfeste (Belagerung): the command fort at night, the Host on the north wall
# ---------------------------------------------------------------------------
def wallfeste_siege():
    mb = MapBuild(WALLFESTE_SIEGE, NAMES[WALLFESTE_SIEGE], base_map(WALLFESTE), display="Wallfeste")
    # no cannons in Mittland (as in chapter 4)
    for i, v in enumerate(mb.m['data']):
        if v in (372, 373, 380, 381, 128, 136):
            mb.m['data'][i] = 0
    mb.props(note="<Area Name: Wallfeste>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Battle4', 55),
             bgs=('Fire2', 40), battleback=('Snowfield', 'Fort1'), weather='snow 3')
    # south gate: shut (the Wallweg is the Host's tonight)
    for x in (20, 21, 22):
        mb.add("South Gate", x, 35, [pg(Ev().text(["The south gate is barred. Out there the Wallweg is full",
                                                   "of the Host's torches."]), trigger=1, priority=0)])
    # arrival from Weißenfels
    el = Ev()
    el.card("Kapitel 6", "Der Messingtyrann", 220)
    el.set_time(21, 0)
    el.wait(10)
    el.se('Explosion2', 70, 80)
    el.shake(4, 5, 40)
    el.narrate(["A day and a night back through the Grauklamm, half of",
                "Rin's army at your heels. The Wallfeste is burning when",
                "you reach it: fire on the north wall, bells everywhere."])
    el.say(KOSAKA, ["Princess. Vessel. You're late, and I have never been so",
                    "glad to see anyone."])
    el.say(RIN, ["Marshal. Where?"])
    el.say(KOSAKA, ["Everywhere. They came out of the Aschenfeld at dusk,",
                    "the whole Host: brass soldiers, oni, hounds, and him.",
                    "Gōen. On a throne of siege engines, like a merchant"])
    el.say(KOSAKA, ["come to count his stock."])
    el.say(KOSAKA, ["They're in the Torturm, the gate tower over the north",
                    "gate. If they reach the winch, the gate opens, and then",
                    "it's the courtyard, and then it's over."])
    el.say(RIN, ["My people take the walls. Kanta: the tower?"])
    el.say(KANTA, ["The tower."], 'calm')
    el.say(HANMA, ["From the bottom up, my Lord, and drop the portcullis",
                   "before anything else. A gate is a promise; keep it shut."], 'command')
    el.quest_new(Q_SIEGE)
    el.quest_new(Q_TOWER)
    el.switch(S_C6)
    el.rest_point(WALLFESTE_SIEGE, 21, 32, 8)
    mb.autorun("Siege", el)
    # the Marshal and the princess in the courtyard
    def kos(e):
        e.if_switch(S_TOWER_DONE, True, sortie,
                    lambda b: b.say(KOSAKA, ["The Torturm. North gate, then up. Every minute counts."]))
    def sortie(e):
        e.if_switch(S_TO_FP3, True,
                    lambda b: b.choices(["March to Frontposten 3", "Not yet"],
                                        [go_fp3, None], cancel=1),
                    order)
    def order(e):
        e.say(KOSAKA, ["The portcullis is down. That's the first good thing",
                       "that's happened since dusk."])
        e.say(KOSAKA, ["But it doesn't matter how many we kill. Every soldier",
                       "who falls on this wall gets up an hour later wearing",
                       "brass and walks back at us."])
        e.say(HANMA, ["A soul cauldron. Gōen boils the dead back into their",
                      "bodies and sends them in again. I've seen it. We burned",
                      "one on the Shimo plain, three hundred years before you."], 'stern')
        e.say(KOSAKA, ["Then it's in their camp. On the Aschenfeld, beyond the",
                       "old breach at Frontposten 3. Mori's still holding, just.",
                       "The new stone has a sally port."])
        e.say(RIN, ["I can't go with you. If I leave the walls, they break."])
        e.say(KOSAKA, ["Along the Wallweg, in the dark. Mori will let you out",
                       "onto the ash. Break that pot."])
        e.quest_done(Q_TOWER)
        e.quest_new(Q_KESSEL)
        e.switch(S_TO_FP3)
        e.choices(["March to Frontposten 3", "Not yet"], [go_fp3, None], cancel=1)
    def go_fp3(e):
        e.fadeout()
        e.narrate(["West along the Wallweg in the dark, under a sky that",
                   "flickers with the Host's fires. Twice you hide in the",
                   "snow while something big goes past."])
        e.transfer(FP3_SIEGE, 16, 33, 8, 0)
        e.fadein()
    mb.add("Kōsaka Tetsuji", 22, 27, [pg(Ev().say(KOSAKA, ["Go!"]), priority=0),
                                      pg((lambda e: (kos(e), e)[1])(Ev()), sw=S_C6, char=KOSAKA.char[0],
                                         index=KOSAKA.char[1], direction=2, priority=1)])
    mb.add("Asahina Rin", 24, 27, [pg(None, priority=0),
                                   pg(Ev().if_switch(S_TOWER_DONE, True,
                                                     lambda b: b.say(RIN, ["Break the pot, Kanta. I'll hold the wall."]),
                                                     lambda b: b.say(RIN, ["The tower. I'll keep them off the walls."])),
                                      sw=S_C6, char=RIN.char[0], index=RIN.char[1], direction=2, priority=1)])
    # the field cook: rest; the Zeughaus clerk: a stall in the courtyard
    def rest(e):
        e.fadeout()
        e.recover_all()
        e.rest_point(WALLFESTE_SIEGE, 21, 32, 8)
        e.wait(40)
        e.fadein()
        e.say(WF_COOK, ["There. Soup. Now go and hit something."])
    el = Ev().say(WF_COOK, ["Hanamura. The Kaserne's full of wounded; I cook out",
                            "here now. Sit a moment."])
    el.choices(["Rest (free)", "Not now"], [rest, None], cancel=1)
    mb.npc("Cook", 9, 28, WF_COOK, el, direction=2)
    goods = [('item', IT["Großer Heiltrank"]), ('item', FI["Elixier"]), ('item', FI["Großes Elixier"]),
             ('item', FI["Hoher Manatrank"]), ('item', FI["Äther"]), ('item', FI["Starkes Riechsalz"]),
             ('item', FI["Allheilmittel"]), ('item', FI["Große Lichtphiole"]),
             ('armor', FA["Messingbrecherhelm"]), ('armor', FA["Magierhut"]), ('armor', FA["Turmschild der Wacht"]),
             ('armor', FA["Kriegerring"]), ('armor', FA["Heiligenring"]), ('armor', FA["Magierring"]),
             ('armor', FA["Falkenring"]), ('weapon', FW["Morgenfaust"])]
    el = Ev().say(CLERK, ["The quartermaster's stall, what's left of it. Prices are",
                          "what they are. So is the night."])
    el.shop(goods)
    mb.npc("Clerk", 13, 27, CLERK, el, direction=6)
    # the north gate: the Torturm
    def north(e):
        e.if_switch(S_TOWER_DONE, True,
                    lambda b: b.text(["The portcullis is down. Nothing is coming through here",
                                      "tonight."]),
                    lambda b: b.choices(["Into the Torturm", "Not yet"],
                                        [lambda c: (c.se('Door1'), c.transfer(TORTURM, 5, 25, 8, 0)), None], cancel=1))
    for x in (32, 33, 34, 35):
        mb.add("Torturm", x, 5, [pg(Ev().if_switch(S_C6, True, north), trigger=0, priority=1)])
    # siege dressing: fires and the wounded
    for (x, y) in [(16, 17), (30, 18), (40, 17), (6, 21)]:
        mb.add("Fire", x, y, [pg(None, char='!Flame', index=3, direction=2, priority=1, step_anime=True)])
    for (x, y, idx) in [(18, 30, 0), (26, 31, 6), (11, 25, 2)]:
        mb.add("Wounded", x, y, [pg(Ev().say(npc_speaker("Verwundeter", "People3", 7),
                                             ["…Hold the wall. Hold the wall."]), char='Damage1', index=idx % 8,
                                    direction=2, priority=1)])
    for (x, y) in [(20, 30), (27, 25), (28, 29)]:
        mb.add("Soldier", x, y, [pg(Ev().say(WALL_SOLDIER, ["Brass men! Brass men on the north wall! …Not that",
                                                           "way, you're the tower lot. Go!"]),
                                    char=WALL_SOLDIER.char[0], index=WALL_SOLDIER.char[1], direction=8, priority=1)])
    for (x, y) in [(17, 15), (21, 15), (20, 25), (24, 25), (32, 8), (35, 8)]:
        mb.light('brazier', x, y)
    return mb


# ---------------------------------------------------------------------------
# 90  Torturm: three floors of the gate tower (side by side on one map)
# ---------------------------------------------------------------------------
def gen_tower():
    g = Gen(44, 30, 4, seed=90)
    rooms = [(2, 13, 13, 27),      # floor 1: the gate hall (door south)
             (16, 10, 28, 27),     # floor 2: the rampart gallery
             (31, 4, 42, 22)]      # floor 3: the winch room at the top
    open_ = T.rooms_and_halls(g, rooms, [], *DUN.GREY_BRICK, DUN.ROCK2, wall_h=2)
    g.paint(g.rect(19, 15, 25, 23), DUN.CARPET)
    for (x, y) in [(4, 17), (11, 17), (4, 23), (11, 23)]:
        g.stamp(x, y, T.PILLAR_SQ, force=True)
    for (x, y) in [(18, 16), (26, 16), (18, 24), (26, 24)]:
        g.stamp(x, y, T.PILLAR_SQ, force=True)
    free = {c for c in open_ if g.kind_at(*c) in (DUN.ROCK2,)}
    g.scatter_in(free, [[(0, 0, DUN.BARREL)], [(0, 0, DUN.JAR)], [(0, 0, 220)], [(0, 0, 221)]], 14, spacing=1)
    g.finish()
    return g


def torturm():
    g = gen_tower()
    mb = MapBuild(TORTURM, NAMES[TORTURM], g.m, display=NAMES[TORTURM])
    mb.props(note="<Rank: C>\n<Area Name: Torturm>", bgm=('Battle3', 55), bgs=('Fire1', 30),
             battleback=('Stone2', 'Fort2'))
    # the door back to the courtyard (floor 1, south)
    mb.add("Tower Door", 7, 27, [pg(Ev().se('Move1', 60).transfer(WALLFESTE_SIEGE, 33, 6, 2, 0), trigger=1,
                                    priority=0)])
    el = Ev()
    el.narrate(["The Torturm. The gate hall is full of smoke and the",
                "clatter of brass. Stairs go up from the far wall."])
    el.say(FALIN, ["Behind me. They'll come in threes."], 'fierce')
    mb.autorun("Tower", el)
    # stairs between the floors (up: floor 1 -> 2 -> 3)
    def stairs(x, y, to, tx, ty, need, text):
        el = Ev().if_switch(need, True, lambda b: (b.se('Move1', 60), b.transfer(TORTURM, tx, ty, 8, 0)),
                            lambda b: b.text(text)) if need else Ev().se('Move1', 60).transfer(TORTURM, tx, ty, 8, 0)
        mb.add("Stairs", x, y, [pg(el, trigger=0, priority=1)])
    stairs(7, 14, TORTURM, 22, 26, S_TOWER1, ["Brass soldiers hold the stairs. Clear the hall first."])
    stairs(22, 11, TORTURM, 36, 21, S_TOWER2, ["Oni on the gallery. Not yet."])
    mb.add("Stairs Down", 22, 27, [pg(Ev().se('Move1', 60).transfer(TORTURM, 7, 15, 2, 0), trigger=1, priority=0)])
    mb.add("Stairs Down", 36, 22, [pg(Ev().se('Move1', 60).transfer(TORTURM, 22, 12, 2, 0), trigger=1, priority=0)])
    # fights: visible foes that attack on touch
    def foe(name, x, y, sheet, idx, troop, lines, after=None, sw=None):
        e = Ev()
        e.se('Monster2', 80, 90)
        e.text(lines)
        e.battle(TR[troop])
        e.self_switch('A')
        if after:
            after(e)
        p = [pg(e, char=sheet, index=idx, direction=2, trigger=2, priority=1, step_anime=True),
             pg(None, self_sw='A', priority=0)]
        if sw:
            for q in p:
                q['conditions'].update(cond_switch(sw))
            p.insert(0, pg(None, priority=0))
        mb.add(name, x, y, p)
    foe("Brass Soldiers", 6, 20, 'Evil', 6, "Messingsoldaten x3", ["Three brass soldiers turn as one."])
    foe("Brass Soldiers", 9, 16, 'Evil', 6, "Soldaten & Oni", ["A brass line and an oni behind it."],
        after=lambda e: (e.switch(S_TOWER1), e.text(["The stairs up are clear."])))
    foe("Gargoyles", 20, 20, 'Monster', 7, "Gargylen & Soldat", ["Gargoyles on the gallery rail!"])
    foe("Oni", 24, 14, 'SF_Monster', 3, "Oni x2", ["Two oni mercenaries block the stair, clubs up."],
        after=lambda e: (e.switch(S_TOWER2), e.text(["The way to the winch room is open."])))
    # the top: the oni captain at the winch
    capt = mb.add("Oni Captain", 36, 8, [pg(None, char='SF_Monster', index=3, direction=2, priority=1, step_anime=True),
                                        pg(None, sw=S_TOWER_DONE, priority=0)])
    def top(e):
        e.se('Monster1', 90, 70)
        e.text(["The winch room. An oni in a captain's harness has both",
                "hands on the gate winch, and it's already half turned."])
        e.say(npc_speaker("Oni-Hauptmann", "", 0), ["Little soldiers. The gate opens at the next bell. Gōen",
                                                     "pays by the hour."])
        e.say(HANMA, ["An Oni captain, my Lord. Everything it hits, it hits",
                      "hard. Falin, the front!"], 'command')
        e.battle(TR["Oni-Hauptmann"])
        e.switch(S_TOWER_DONE)
        e.se('Switch1')
        e.se('Gate2', 100, 60)
        e.shake(6, 5, 40)
        e.text(["You kick the pawl free. The winch spins, the chain howls",
                "through the tower, and the portcullis comes down on the",
                "north gate like an axe."])
        e.say(FALIN, ["That's the gate. Back to the Marshal."], 'calm')
        e.quest_desc(Q_TOWER, "The portcullis is down. Report to the Marshal in the courtyard.")
        e.fadeout()
        e.transfer(WALLFESTE_SIEGE, 22, 29, 8, 0)
        e.fadein()
    for x in (35, 36, 37):
        mb.add("Winch", x, 10, [pg(Ev().if_switch(S_TOWER_DONE, False, top), trigger=1, priority=0)])
    chest(mb, "Chest", 41, 20, lambda e: (e.item(FI["Äther"], 1), e.gold(3000)), "Found an Äther and \\MONEY[3000].")
    chest(mb, "Chest", 27, 26, lambda e: e.armor(FA["Turmschild der Wacht"], 1), "Found a Turmschild der Wacht.")
    for (x, y) in [(5, 13), (10, 13), (19, 10), (25, 10), (33, 4), (40, 4)]:
        mb.light('torch', x, y)
    mb.light('cave_dark', 0, 0, tile=False)
    return mb


# ---------------------------------------------------------------------------
# 93  Frontposten 3 (Belagerung)
# ---------------------------------------------------------------------------
def fp3_siege():
    mb = MapBuild(FP3_SIEGE, NAMES[FP3_SIEGE], base_map(FRONTPOSTEN), display="Frontposten 3")
    mb.props(note="<Area Name: Frontposten 3>\n<No Rank HUD>\n<lighting: Outside>", bgm=('Battle4', 50),
             bgs=('Wind3', 40), battleback=('Snowfield', 'Fort1'), weather='snow 4')
    mb.add("South Gate", 16, 34, [pg(Ev().text(["The Wallweg back to the Wallfeste. Not until the cauldron",
                                                "is broken."]), trigger=0, priority=1),
                                  pg(Ev().text(["The Wallweg east to the Wallfeste."]), sw=S_C6_END, trigger=0, priority=1)])
    el = Ev()
    el.wait(10)
    el.narrate(["Frontposten 3 is a ring of fires. Hounds in the courtyard,",
                "brass on the walls, and in the middle of it Mori with a",
                "pike, bellowing orders at everyone."])
    el.say(MORI, ["Neuling! Die Eiserne! Gods, it's good to see ugly faces.",
                  "Clear my yard and we'll talk!"])
    mb.autorun("FP3", el, cond_switch=S_TO_FP3)
    # hounds in the courtyard
    hounds = []
    for (x, y) in [(14, 30), (18, 30)]:
        hounds.append(mb.add("Hellhound", x, y, [pg(None, priority=0),
                                                 pg(None, sw=S_TO_FP3, char='Nature', index=0, direction=2, priority=1,
                                                    step_anime=True),
                                                 pg(None, sw=S_FP3_HOUNDS, priority=0)]))
    def yard(e):
        e.se('Dog', 90, 60)
        e.text(["Two hellhounds turn from Mori's line, embers dripping",
                "from their jaws."])
        e.battle(TR["Höllenhunde x2"])
        e.switch(S_FP3_HOUNDS)
    for x in (15, 16, 17):
        mb.add("Yard", x, 32, [pg(None, priority=0),
                               pg(Ev().if_switch(S_FP3_HOUNDS, False, yard), sw=S_TO_FP3, trigger=1, priority=0)])
    # Mori: the sally port
    def mori(e):
        e.if_switch(S_KESSEL, True, lambda b: b.say(MORI, ["The pot's broken. I'll write that on my wall, if I",
                                                           "still have one in the morning."]),
                    lambda b: b.if_switch(S_FP3_HOUNDS, True, sally,
                                          lambda c: c.say(MORI, ["Hounds first! Talk later!"])))
    def sally(e):
        e.say(MORI, ["The Marshal's bird got here. A cauldron, he says. I've",
                     "seen the glow of it out there on the ash, every night",
                     "for a week."])
        e.say(MORI, ["The breach is stone now, and the stone has a sally",
                     "port. Through the inner gate, through the keep, and I'll",
                     "have it opened for you. And shut behind you."])
        e.say(FALIN, ["Six years I held that gap from this side."], 'calm')
        e.say(MORI, ["And tonight you go through it. Don't make me wait six",
                     "more years for you."])
        e.quest_desc(Q_KESSEL, "Through the inner gate of Frontposten 3 and out of the sally port onto the "
                               "Aschenfeld. The cauldron is in the Host's camp.")
        e.switch(S_SORTIE)
    mb.add("Mori Daisuke", 16, 29, [pg(None, priority=0),
                                    pg((lambda e: (mori(e), e)[1])(Ev()), sw=S_TO_FP3, char=MORI.char[0],
                                       index=MORI.char[1], direction=2, priority=1)])
    # the inner gate: the sally port onto the Aschenfeld
    mb.remove_at(16, 27)
    closed = Ev().text(["The inner gate. Mori's people hold it shut."])
    go = Ev().text(["The inner gate, and beyond the keep the new stone of the",
                    "breach with its little iron sally port."])
    go.choices(["Out onto the Aschenfeld", "Wait"],
               [lambda e: (e.se('Open2'), e.se('Move1', 60), e.transfer(ASCHENLAGER, 22, 37, 8, 0)), None], cancel=1)
    mb.add("Inner Gate", 16, 27, [pg(closed, char='!$Gate1', index=0, direction=2, trigger=0, priority=1,
                                     walk_anime=False),
                                  pg(go, sw=S_SORTIE, char='!$Gate1', index=0, direction=2, pattern=2, trigger=0,
                                     priority=1, walk_anime=False),
                                  pg(Ev().text(["The inner gate. The ash can wait."]), sw=S_KESSEL, char='!$Gate1',
                                     index=0, direction=2, trigger=0, priority=1, walk_anime=False)])
    # soldiers on the walls
    for (x, y) in [(9, 33), (23, 33), (13, 31), (20, 31)]:
        mb.add("Soldier", x, y, [pg(Ev().say(SOLDIER_FP, ["Hold! Hold!"]), char=SOLDIER_FP.char[0],
                                    index=SOLDIER_FP.char[1], direction=8, priority=1)])
    # --- after the Aschenfeld: the fire, Yukino speaks
    yk = mb.add("Yukino", 19, 31, [pg(None, priority=0),
                                   pg(Ev().say(YUKINO, ["…"]), sw=S_YUKINO, char=YUKINO.char[0], index=YUKINO.char[1],
                                      direction=4, priority=1),
                                   pg(None, sw=S_C6_END, priority=0)])
    el = Ev()
    el.set_time(2, 0)
    el.wait(20)
    el.narrate(["Frontposten 3, after. The Host has gone back into the ash",
                "as if a tide went out. Mori's soldiers sleep where they",
                "fell down. Nobody has gotten up again wearing brass."])
    el.narrate(["The woman from the ash sits at the brazier with you and",
                "has said nothing at all."])
    el.say(MORI, ["Tsukishiro Yukino. The Frost Saint. S-rank, once. She",
                  "hasn't said a word in twelve years. Kills more of them",
                  "than a company, though, when she comes."])
    el.say(MORI, ["She walks out of the Aschenfeld every few months, sleeps",
                  "a night by a Wall fire and walks back in. Nobody asks.",
                  "…I'll leave you to it."])
    el.wait(30)
    el.say(YUKINO, ["…"])
    el.say(HANMA, ["You came for us. Out there. Why?"], 'calm')
    el.wait(40)
    el.say(YUKINO, ["…Because he smiled."])
    el.say(KANTA, ["Gōen?"], 'calm')
    el.say(YUKINO, ["Kagerō. When he watched your light cut the chain. From",
                    "the other side of the ash. I felt it."])
    el.say(YUKINO, ["His name is Kurenai Tōma."])
    el.say(FALIN, ["The Demon Lord has a name?"], 'calm')
    el.say(YUKINO, ["He had a mother, and a sword, and four friends. We were",
                    "five. The Morgenwacht. The Guild's best, twelve years",
                    "ago. We went into the rift at Frostheim to close it."])
    el.say(YUKINO, ["Something in the miasma spoke to him. Hōkai, I think.",
                    "It told him everything could stop. War. Heroes. Being",
                    "needed, being sent, being the one who dies next."])
    el.say(YUKINO, ["He listened. The others died. I came back. The rift kept",
                    "most of what I was."])
    el.say(YUKINO, ["He spares children because he still remembers being one.",
                    "He kills heroes because he still remembers being one."])
    el.say(HANMA, ["And inside the miasma nothing touches him. Swords go",
                   "through him like smoke. The Veil of Ash."], 'stern')
    el.say(YUKINO, ["You know it."])
    el.say(HANMA, ["I knew the last one. In the year 312 the first Demon Lord",
                   "wore the same veil, and Sōryū Akira cut it open with",
                   "four relics. The Dawn Regalia."], 'stern')
    el.say(KANTA, ["You knew the hero of the Dawn War."], 'calm')
    el.say(HANMA, ["I was one of her generals, my Lord. Later. Not tonight.",
                   "I don't come out of that story well."], 'hurt')
    el.say(HANMA, ["The Morgenklinge. The Sternlaterne. The Heldenhorn. The",
                   "Aschenkrone. Each one pierces one step of a demon's rank.",
                   "All four, and the veil tears."], 'stern')
    el.say(YUKINO, ["…If I say his name to him, he might remember. Once.",
                    "I will come with you. If you'll let me."])
    el.say(KANTA, ["We'd be glad of you."], 'calm')
    el.say(YUKINO, ["You won't be. I don't talk."])
    el.say(FALIN, ["Neither do I. We'll get on."], 'smile')
    el.fadeout()
    el.set_time(8, 0)
    el.wait(40)
    el.fadein()
    el.narrate(["Morning. A rider from the Wallfeste with the princess's",
                "colours, and a letter under the seal of Asahina."])
    el.say(RIN, ["(in the letter) Kanta. The Wall stands. The Marshal is",
                 "asleep on his feet and the Host is back in the ash."])
    el.say(RIN, ["(in the letter) Hanma's regalia are in the court records:",
                 "the Morgenklinge went to the Emperor in 313 and it is",
                 "still in the vault at Lichtenhall. The Empress won't"])
    el.say(RIN, ["(in the letter) give it to a vessel from the Wall because",
                 "a princess asks. So take this letter and ask her anyway.",
                 "She's holding her Sonnwende tournament. Be persuasive."])
    el.item(KI["Rins Brief"], 1)
    el.notice(["Received \\C[6]Rins Brief\\C[0]."])
    el.se('Equip3')
    el.party(YUKINO_ID, True)
    el.plugin('Story_Core', 'SyncLevel', {'actorId': YUKINO_ID, 'sourceId': 1}, 'Sync Level')
    el.plugin('Story_Core', 'AutoBuild', {'actorId': YUKINO_ID}, 'Auto Build')
    el.me('Fanfare2')
    el.notice(["\\C[6]Yukino\\C[0], the Frost Saint, joins the party."])
    el.quest_done(Q_KESSEL)
    el.quest_done(Q_SIEGE)
    el.switch(S_C6_END)
    el.wait(20)
    el.plugin('Story_Core', 'ChapterCard', {'title': "Ende des zweiten Akts", 'subtitle': "Die Wacht", 'duration': 240},
              'Chapter Card')
    el.fadeout()
    el.transfer(ACT3_START[0], ACT3_START[1], ACT3_START[2], 2, 0)
    el.fadein()
    mb.autorun("After", el, cond_switch=S_YUKINO)
    for (x, y) in [(13, 28), (19, 28), (14, 19), (18, 19)]:
        mb.light('brazier', x, y)
    return mb


SOLDIER_FP = npc_speaker("Wall Soldier", "People3", 7)
ACT3_START = (KAISERSTRASSE, 20, 1)         # chapter 7 begins on the Kaiserstraße (ch7.KAISER_ENTRY)


# ---------------------------------------------------------------------------
# 91  Heerlager der Asche: the Host's camp on the Aschenfeld
# ---------------------------------------------------------------------------
def gen_aschenlager():
    g = Gen(46, 40, 2, seed=91)
    g.paint(g.all(), OUT.DIRT)
    walk = g.blob(23, 21, 17, rough=0.2, seed=9) | g.rect(20, 34, 25, 39)
    walk &= g.rect(1, 1, 44, 39)
    ground = T.frame(g, walk, T.ASH, thick=3, trunk_h=2)
    # ash everywhere, darker patches, cracks and miasma
    rng = g.rng
    for c in rng.sample(sorted(ground), len(ground) // 5):
        g.set(c[0], c[1], 1, auto(rng.choice([OUT.CRACKS, OUT.DARKSPARK, OUT.DARKSPARK])))
    road = g.line([(22, 39), (22, 26), (23, 8)], 3) & ground
    g.paint(road, OUT.DIRT_STONES)
    for c in road:
        g.set(c[0], c[1], 1, 0)
    g.keep_clear |= g.grow(road, 1)
    # the camp: red tents in rows, the cauldron clearing in the middle, the throne of engines at the top
    for (x, y) in [(8, 16), (12, 16), (31, 16), (35, 16), (8, 28), (12, 28), (31, 28), (35, 28), (15, 10), (28, 10)]:
        T.tent(g, x, y, red=True)
    clearing = g.ellipse(22.5, 20, 5, 3.5)
    g.paint(clearing, OUT.DIRT_STONES)
    for c in clearing:
        g.set(c[0], c[1], 1, 0)
    g.keep_clear |= clearing
    # the engines: timber frames and wheels around the throne
    for (x, y) in [(18, 6), (27, 6), (19, 8), (26, 8)]:
        g.stamp(x, y, [(0, -1, 148), (0, 0, 149)])
    T.dress(g, ground - clearing - g.grow(road, 2), T.ASH, trees=0.03, rocks=0.02, bushes=0.02, tufts=0.03)
    g.finish()
    return g


def aschenlager():
    g = gen_aschenlager()
    R = T.reach_check(g, (22, 37), [(22, 20), (23, 9)], 'Aschenlager')
    sp = lambda near, **kw: T.spot(g, near, region=R, **kw)
    mb = MapBuild(ASCHENLAGER, NAMES[ASCHENLAGER], g.m, display="Aschenfeld")
    mb.props(note="<Rank: C>\n<Area Name: Aschenfeld>", bgm=('Dungeon7', 60), bgs=('Wind3', 45),
             battleback=('Wasteland', 'Wasteland'), encounters=SIEGE_ENC(), steps=26, weather='snow 2')
    for x in range(20, 26):
        mb.add("Sally Port", x, 39, [pg(Ev().if_switch(S_KESSEL, True,
                                                        lambda b: (b.se('Move1', 60), b.transfer(FP3_SIEGE, 16, 28, 2, 0)),
                                                        lambda b: b.text(["The sally port. Not without breaking the pot."])),
                                        trigger=1, priority=0)])
    el = Ev()
    el.narrate(["The Aschenfeld. Grey to the horizon, under a sky the",
                "colour of an old bruise, and in the middle of it the",
                "Host's camp: tents of red hide, engines of timber and"])
    el.narrate(["brass, and in the heart of the camp a glow like a", "second, sick moon."])
    el.say(HANMA, ["There. The cauldron. Everything that fell today is in",
                   "that pot, my Lord. Let's give them back."], 'stern')
    mb.autorun("Ash", el)
    # patrols
    def patrol(name, near, sheet, idx, troop, lines):
        c = sp(near)
        e = Ev()
        e.se('Monster2', 80, 90)
        e.text(lines)
        e.battle(TR[troop])
        e.self_switch('A')
        mb.add(name, c[0], c[1], [pg(e, char=sheet, index=idx, direction=2, trigger=2, priority=1, step_anime=True,
                                     move_type=1),
                                  pg(None, self_sw='A', priority=0)])
    patrol("Brass Patrol", (22, 31), 'Evil', 6, "Messingsoldaten x3", ["A brass patrol, marching in step."])
    patrol("Oni", (14, 22), 'SF_Monster', 3, "Oni x2", ["Oni at a fire, sharpening clubs. They look up."])
    patrol("Hounds", (31, 22), 'Nature', 0, "Höllenhunde x2", ["Hellhounds, chained to a post. Not anymore."])
    patrol("Captain", (22, 26), 'SF_Monster', 3, "Oni-Hauptmann", ["The cauldron's guard: an oni captain and his",
                                                                    "brass honour guard."])
    # the cauldron
    kessel = mb.add("Seelenkessel", 22, 19, [pg(None, char='$BigMonster1', index=0, direction=6, priority=1,
                                               direction_fix=True, step_anime=True),
                                            pg(None, sw=S_KESSEL, priority=0)])
    goen = mb.add("Gōen", 23, 8, [pg(None, priority=0),
                                 pg(None, sw=S_KESSEL, char=GOEN.char[0], index=GOEN.char[1], direction=2, priority=1)])
    yuk = mb.add("Yukino (ash)", 26, 12, [pg(None, priority=0)])
    def pot(e):
        e.se('Fire2', 90, 60)
        e.text(["The cauldron: brass and bone, big as a house, boiling",
                "with something that isn't water. Faces rise to the top",
                "and sink again. It hums a hymn to itself."])
        e.say(HANMA, ["Rank D, and made of souls. Light hurts it, my Lord.",
                      "Everything else hurts it less."], 'command')
        e.battle(TR["Seelenkessel"])
        e.switch(S_KESSEL)
        e.se('Explosion3', 100, 60)
        e.flash((255, 255, 255, 220), 60)
        e.shake(8, 8, 60)
        e.text(["The cauldron cracks from rim to foot. Light pours out of",
                "it, hundreds of little lights, and rises into the grey,",
                "and is gone."])
        e.say(FALIN, ["…They're free."], 'hurt')
        e.wait(30)
        e.se('Coin', 100, 70)
        e.wait(20)
        e.se('Coin', 100, 70)
        e.text(["Coins. Somebody is dropping coins, one at a time, from",
                "the top of the engines."])
        e.route(goen, [(1, [])], wait=True)
        e.say(GOEN, ["Two hundred and eleven souls, at the market rate. Do",
                     "you know what you just cost me, little vessel?"])
        e.say(HANMA, ["Gōen."], 'stern')
        e.say(GOEN, ["And the General who was refused. How are you, Hanma?",
                     "Still angry? I have a contract for anger."])
        e.say(GOEN, ["Let us do business, vessel. Sign with me, and your",
                     "vessels never run out. Every one of them will be yours",
                     "to wake in. Die as often as you like. I only take a"])
        e.say(GOEN, ["small percentage. On each death. Of your soul."])
        e.choices(["Refuse", "\"What percentage?\""],
                  [lambda b: b.say(KANTA, ["No."], 'fierce'),
                   lambda b: (b.say(GOEN, ["Ten. Only ten. After ten deaths, of course, there is",
                                           "nothing left to take, and you are mine."]),
                              b.say(HANMA, ["My Lord. No."], 'stern'),
                              b.say(KANTA, ["…No."], 'calm'))], cancel=0)
        e.say(GOEN, ["Everyone says no at first."])
        e.say(GOEN, ["Let me show you the price of no."])
        e.battle(TR["Gōen"], can_escape=False, can_lose=True, lose=lambda b: b.switch(S_YUKINO))
        e.if_switch(S_BREAK_C, False, late_break)
        e.switch(S_YUKINO)
        e.wait(10)
        e.set_image(yuk, YUKINO.char[0], YUKINO.char[1])
        e.se('Ice4', 100, 70)
        e.flash((200, 240, 255, 255), 60)
        e.text(["Cold. A wall of ice as tall as the engines stands between",
                "you and the Brass Tyrant, and on the other side of it a",
                "figure in white walks out of the ash."])
        e.say(GOEN, ["…Tsukishiro. The last of the Morgenwacht. You're",
                     "interrupting a sale."])
        e.say(YUKINO, ["…"])
        e.say(GOEN, ["No? Never anything, from you. Very well."])
        e.say(GOEN, ["Keep your souls, vessel. For now. Everyone signs, in",
                     "the end. I am a very patient man."])
        e.se('Coin', 100, 60)
        e.fadeout()
        e.set_image(goen, '', 0)
        e.wait(20)
        e.transfer(FP3_SIEGE, 16, 30, 8, 0)
        e.fadein()
    for (x, y) in [(21, 21), (22, 21), (23, 21), (24, 21)]:
        mb.add("Cauldron Ring", x, y, [pg(Ev().if_switch(S_KESSEL, False, pot), trigger=1, priority=0)])
    chest(mb, "Chest", *sp((9, 30)), lambda e: (e.item(FI["Großes Elixier"], 2), e.gold(2500)),
          "Found 2 Großes Elixier and \\MONEY[2500].")
    chest(mb, "Chest", *sp((37, 30)), lambda e: e.armor(FA["Kriegerring"], 1), "Found a Kriegerring.")
    mb.light('ash_night', 0, 0, tile=False)
    for (x, y) in [(22, 19), (23, 8), (10, 14), (33, 14), (10, 26), (33, 26)]:
        mb.light('brazier', x, y)
    mb.follow_light('beam', 22, 37)
    return mb


def late_break(e):
    """If the party fell before the troop page ran, the breakthrough still happens (after the fight)."""
    e.text(["On the ash, the golden chain winds around Hanma's throat,",
            "and Kanta gets up. She doesn't know how."], background=1, position=1)
    e.se('Magic3', 90, 70)
    e.flash((200, 230, 255, 255), 60)
    e.breakthrough()
    e.switch(S_BREAK_C)


def goen_troop_pages():
    """Pages of the unwinnable fight (troop "Gōen"): the wall, the chain meant for Hanma, the breakthrough."""
    t0 = Ev()
    t0.say(GOEN, ["Rank SS, little vessel. Rank D. Do you know what that",
                  "means? It means nothing you own can touch me."])
    t1 = Ev()
    t1.say(HANMA, ["My Lord, it's the rank wall! Nothing reaches him! Don't",
                   "spend yourself, stay alive!"], 'command')
    t2 = Ev()
    t2.say(GOEN, ["Clause one. The General who was refused is forfeit.",
                  "Collection."])
    t2.se('Chain', 90, 60)
    t2.text(["A golden chain lashes out of the Tyrant's sleeve and",
             "coils around Hanma's throat. The thread between her and",
             "Kanta pulls tight as a bowstring."], background=1, position=1)
    t2.say(HANMA, ["…My… Lord…"], 'hurt')
    t2.say(KANTA, ["Let her go."], 'fierce')
    t2.se('Magic3', 90, 70)
    t2.flash((200, 230, 255, 255), 60)
    t2.text(["The sigils on Kanta's arm burn white. The light in her",
             "hand stops being one weapon and becomes three, and they",
             "don't wait for her hand: they cut the chain."], background=1, position=1)
    t2.breakthrough()
    t2.switch(S_BREAK_C)
    t2.say(GOEN, ["…Oh? That's new. Nobody has ever cut one of my chains."])
    t2.say(GOEN, ["Interesting. Very interesting. Let us see how long it",
                  "lasts."])
    return [(t0, (0, 0)), (t1, (1, 0)), (t2, (2, 0))]
