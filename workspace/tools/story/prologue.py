"""Prologue: Erwachen. The waking cave, the ridge, the road or the trees."""
from story.common import *
from story.db import TR, IT, AR, SK, CE, ST_FEAR
from story.ids import *

NIGHT_RAIN = ('rain', 3)
CAT = ('Nature', 1)

def build():
    maps = []
    maps.append(cave())
    maps.append(ridge())
    maps.append(road())
    maps.append(trees())
    return maps

# ---------------------------------------------------------------------------
# 1  Erwachenshöhle  (sample 208)
# ---------------------------------------------------------------------------
def cave():
    mb = MapBuild(CAVE, NAMES[CAVE], 208, display=NAMES[CAVE])
    mb.props(note="<Rank: F>\n<Area Name: Erwachenshöhle>\n<Safe Regions: 0>", bgs=('Drips', 45),
             battleback=('DirtCave', 'DirtCave'), encounters=[], steps=999)

    intro = SW('P: Intro Done')
    # --- opening -----------------------------------------------------------
    el = Ev()
    el.switch(SW('Vessel Active'))
    el.followers(False)
    el.fadeout()
    el.weather('none', 0, 0)
    el.map_name(False)
    el.card("Prolog · Erwachen", "01. Blütenmond 1047", 220)
    el.narrate(["…"])
    el.narrate(["Cold. Stone under your back.", "The smell of wet rock."])
    el.narrate(["Somewhere, water drips: slow and patient, as if it had",
                "been counting for a very long time."])
    el.fadein()
    el.wait(30)
    el.balloon(-1, 8)
    el.say(KANTA, ["…Where…"], 'hurt')
    el.say(HANMA, ["You're awake, my Lord. Good. I was beginning to think",
                   "this body wouldn't take you at all."], 'calm')
    el.route(-1, [(18, [])], wait=True)  # turn right, toward Hanma
    el.say(KANTA, ["Who are you?"], 'calm')
    el.say(HANMA, ["Hanma. Once a general. Of what hardly matters; it's",
                   "all dust now. What I am now is yours: bound to your",
                   "soul, it seems, whether either of us likes it."], 'calm')
    el.say(KANTA, ["…My soul."], 'calm')
    el.say(HANMA, ["You woke in an empty body. No name on it, no purse,",
                   "no blade. Only that silver armor and the red cape.",
                   "I was already here when you opened your eyes."], 'calm')
    el.route(-1, [(16, [])], wait=True)
    el.se('Starlight', 80, 110)
    el.flash((170, 210, 255, 170), 40, True)
    el.narrate(["Light spills from her open hand: a thin blade of pale",
                "blue, no longer than a finger. It hums, faintly, and",
                "throws the cave into sharp blue shadow."])
    el.say(HANMA, ["That's yours too. A weapon of pure mana. Small now.",
                   "It'll grow as you do."], 'smile')
    el.say(KANTA, ["Where are we?"], 'calm')
    el.say(HANMA, ["North, going by the cold. Past that, I can't say.",
                   "My last good map is older than anyone alive."], 'stern')
    el.say(HANMA, ["There's daylight up the passage. Look around first if",
                   "you like, but carefully. I heard something breathing",
                   "down by the water."], 'stern')
    el.notice(["\\C[6]Stat points\\C[0]: open the menu and choose \\C[6]Stat Points\\C[0].",
               "Kanta and Hanma each have 20 to spend. Kanta's light",
               "runs on DEX; Hanma heals with WIS and rots with MAG."])
    el.notice(["Your three best stats set your \\C[6]rank\\C[0] (F to V). A rank",
               "above you hits half again as hard; two above,",
               "twice as hard. Don't pick fights with those."])
    el.switch(intro)
    el.self_switch('A')
    el.followers(True)
    el.gather()
    el.map_name(True)
    hanma_stand = pg(el, trigger=3, priority=1, char=HANMA.char[0], index=HANMA.char[1], direction=4)
    mb.add("Opening (Hanma)", 13, 8, [hanma_stand, pg(None, self_sw='A', trigger=0, priority=0)])
    # --- exit north --------------------------------------------------------
    mb.exit([(12, 3)], RIDGE, 12, 9, 2, name="To Kiefernkamm")

    # --- blocked crack (south) --------------------------------------------
    el = Ev().text(["The passage narrows to a crack. Cold air breathes",
                    "through it, and the smell of earth, but not even",
                    "your light fits through."]).route(-1, [(4, [])], skippable=True)
    mb.add("Crack", 17, 23, [pg(el, trigger=1, priority=0)])

    # --- the drip pool ----------------------------------------------------
    drank = SW('P: Drank')
    el = Ev()
    el.text(["Water drips from the rock into a shallow pool,", "clear and very cold."])
    def drink(e):
        e.se('Water1')
        e.recover_all()
        e.text(["You drink. The cold clears your head.", "(HP and MP restored.)"])
        e.if_switch(drank, False, lambda b: (b.say(HANMA, ["Good. Bodies need water, even new ones."], 'calm'),
                                             b.switch(drank)))
    el.choices(["Drink", "Leave it"], [drink, None], cancel=1)
    mb.add("Drip Pool", 7, 16, [pg(el, trigger=0, priority=1)])

    # --- the two-tail -----------------------------------------------------
    bowed, fought = SW('P: Two-Tail Bowed'), SW('P: Two-Tail Fought')
    trust = VAR('Two-Tail Trust')
    def hoard_fight(e):
        e.say(HANMA, ["My Lord, don't—"], 'command')
        e.se('Cat', 90, 70)
        e.balloon(0, 5)
        e.text(["The two-tail's fur rises. Both tails lash once,", "like a whip being tested."])
        e.switch(fought)
        e.var(trust, 1, '-')
        e.battle(TR["Two-Tail"], can_escape=False, can_lose=False,
                 win=lambda w: (w.text(["The two-tail hisses and is gone into the rocks,",
                                        "faster than your eyes can follow."]),
                                w.switch(SW('P: Two-Tail Gone'))))
    def bow(e):
        e.route(-1, [(15, [10])], wait=True)
        e.text(["You lower your head: half a bow, eyes on the cat."])
        e.wait(30)
        e.balloon(0, 8)
        e.text(["The two-tail blinks, slowly. Then one tail flicks,",
                "once, toward the daylight up the passage."])
        e.say(HANMA, ["Good. It'll remember that. They remember, my Lord:",
                      "a kindness or a kick, for a very long time."], 'smile')
        e.switch(bowed)
        e.var(trust, 1, '+')
    def back_away(e):
        e.route(-1, [(13, [])], wait=True, skippable=True)
        e.text(["You step back, slowly. The two-tail's eyes follow",
                "you until you're out of reach."])
    first = Ev()
    first.text(["On a shelf of fallen stone above the pool, something",
                "watches you: a cat, black as the cave, with two tails",
                "curling behind it like smoke."])
    first.say(HANMA, ["(A two-tail. Don't.)"], 'stern')
    first.say(HANMA, ["(A cat's tail only splits once it has lived longer than",
                      "any cat should. That one would open you up before",
                      "your light grew a hand long.)"], 'stern')
    first.text(["Behind the cat, in a hollow of the rubble, metal glints:", "coins, a buckle, something bright."])
    first.choices(["Bow to it", "Back away", "Reach past it for the glint"], [bow, back_away, hoard_fight], cancel=1)
    p1 = pg(first, char=CAT[0], index=CAT[1], direction=6, trigger=0, priority=1, step_anime=True)
    content = Ev().text(["The two-tail watches you with half-closed eyes.", "It seems content to let you be."])
    content.choices(["Bow again", "Leave it be"], [lambda e: (e.balloon(0, 4), e.text(["One tail curls, lazily."])), None],
                    cancel=1)
    p2 = pg(content, sw=bowed, char=CAT[0], index=CAT[1], direction=6, trigger=0, priority=1, step_anime=True)
    angry = Ev()
    angry.text(["The two-tail is back on its shelf, licking one paw.", "It doesn't look at you. It doesn't need to."])
    angry.choices(["Leave it be", "Reach for the glint again"],
                  [None, lambda e: (e.say(HANMA, ["My Lord. Once was a lesson."], 'stern'), hoard_fight(e))], cancel=0)
    p3 = pg(angry, sw=fought, char=CAT[0], index=CAT[1], direction=6, trigger=0, priority=1, step_anime=True)
    p4 = pg(None, sw=SW('P: Two-Tail Gone'), priority=0)
    mb.add("Two-Tail", 4, 13, [p1, p2, p3, p4])

    # --- the hoard (a strongbox in the rubble) ------------------------------
    el = Ev()
    el.text(["A battered strongbox, half buried in the rubble.",
             "Coins glint through a split in its lid."])
    el.if_switch(SW('P: Two-Tail Gone'), True,
                 lambda b: (b.se('Chest1'), b.gold(120), b.item(IT["Manastein (E)"], 1), b.item(IT["Heiltrank"], 2),
                            b.text(["The strongbox holds \\MONEY[120], a bright mana stone", "and two healing draughts."]),
                            b.self_switch('A')),
                 lambda b: b.text(["The two-tail is watching. Its hoard, its rules."]))
    mb.add("Hoard", 4, 12, [pg(el, char='!Chest', index=0, direction=2, pattern=0, trigger=0, priority=1,
                               walk_anime=False, direction_fix=True),
                            pg(Ev().text(["An empty strongbox."]), self_sw='A', char='!Chest', index=0, direction=8,
                               pattern=0, priority=1, walk_anime=False, direction_fix=True)])

    # --- moss grotto (wound herbs) ----------------------------------------
    el = Ev()
    el.text(["Grey light falls through a crack in the ceiling.", "Moss and wound-herbs grow thick here."])
    el.se('Item3').item(IT["Kräuterbündel"], 3)
    el.text(["You gather 3 Kräuterbündel."])
    el.self_switch('A')
    mb.add("Herbs", 20, 4, [pg(el, char='!Crystal', index=6, direction=2, pattern=1, trigger=0, priority=1,
                               step_anime=True), pg(None, self_sw='A', priority=0)])

    # --- lights -----------------------------------------------------------
    mb.light('cave_dark', 0, 0, tile=False)
    mb.follow_light('beam', 12, 8)
    mb.light('daylight', 12, 3)
    mb.light('crack', 20, 3)
    mb.light('pool', 7, 17)
    return mb

# ---------------------------------------------------------------------------
# 2  Kiefernkamm  (sample 224)
# ---------------------------------------------------------------------------
def ridge():
    mb = MapBuild(RIDGE, NAMES[RIDGE], 224, display=NAMES[RIDGE])
    mb.props(note="<Rank: F>\n<Area Name: Kiefernkamm>\n<lighting: Outside>\n<DayNight: step=1>",
             bgs=('Rain1', 35), battleback=('Grassland', 'Forest'), encounters=[], steps=999, weather='rain 3')
    left, road_sw, trees_sw = SW('P: Left Cave'), SW('P: Road'), SW('P: Trees')
    el = Ev()
    el.weather('rain', 3, 0)
    el.wait(20)
    el.narrate(["Grey dawn. A cold drizzle sifts down through the trees."])
    el.say(HANMA, ["There."], 'command')
    el.balloon(-1, 1)
    el.say(HANMA, ["Smoke. East, three miles or so. Not a burning:",
                   "the steady smoke of hearths. People."], 'calm')
    el.say(KANTA, ["A village."], 'calm')
    el.say(HANMA, ["Likely. We have nothing, my Lord. No coin, no food,",
                   "no blade but yours. A village is where we find all three."], 'stern')
    el.say(HANMA, ["Two ways down. The road below the tree line: open",
                   "ground, but we'd be there within the hour. Or through",
                   "the trees: slower, and nobody sees us coming."], 'calm')
    def take_road(e):
        e.say(KANTA, ["The road. I'd rather see what's coming."], 'calm')
        e.say(HANMA, ["Fair. Keep your light low."], 'smile')
        e.switch(road_sw)
    def take_trees(e):
        e.say(KANTA, ["The trees. Nobody knows we're here. Let's keep it", "that way a while."], 'wry')
        e.say(HANMA, ["Spoken like a scout. Stay close."], 'smile')
        e.switch(trees_sw)
    el.choices(["The road", "The trees"], [take_road, take_trees], cancel=-1)
    el.switch(left)
    mb.autorun("Arrival", el, cond_switch=None)

    back = Ev().weather('none', 0, 0).se('Move1', 60).transfer(CAVE, 12, 4, 2, 0)
    mb.add("To the cave", 12, 8, [pg(back, trigger=1, priority=0)])
    for x in (11, 12, 13):
        el = Ev().se('Move1', 60).transfer(ROAD, 1, 9, 6, 0)
        el2 = Ev().se('Move1', 60).transfer(TREES, 2, 32, 6, 0)
        mb.add("Down", x, 26, [pg(el, trigger=1, priority=0, sw=road_sw), pg(el2, trigger=1, priority=0, sw=trees_sw)])
    return mb

# ---------------------------------------------------------------------------
# 3  Karrenweg  (sample 256): the road
# ---------------------------------------------------------------------------
def first_fight_tips(e):
    tips = SW('Tip: First Fight')
    def show(b):
        b.say(HANMA, ["Not bad. Now listen, because I'll only say it twice."], 'command')
        b.say(HANMA, ["Every art that costs mana grows each time you use it in",
                      "a real fight. Plain strikes teach you nothing new."], 'command')
        b.notice(["\\C[6]Mastery\\C[0]: skills that cost MP rank up from F to V",
                  "with use. Each rank hits harder. A full bar breaks",
                  "through when the skill finishes a stronger foe."])
        b.notice(["The \\C[6]danger gauge\\C[0] (top right) fills as you walk. When it",
                  "is full, something finds you."])
        b.switch(tips)
    e.if_switch(tips, False, show)

def road():
    mb = MapBuild(ROAD, NAMES[ROAD], 256, display=NAMES[ROAD])
    mb.props(note="<Rank: F>\n<Area Name: Karrenweg>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field1', 70), bgs=('Rain1', 25), battleback=('Road1', 'Forest'),
             encounters=[(TR["Crows x2"], 10, ()), (TR["Crows x3"], 5, ()), (TR["Wolf"], 6, ())], steps=28)
    mb.exit([(0, 9), (0, 10)], RIDGE, 12, 25, 8, name="To Kiefernkamm")
    for x, y in [(28, 10), (28, 11)]:
        el = Ev().se('Move1', 60).transfer(RABENAU, 13, 28, 8, 0)
        mb.add("To Rabenau", x, y, [pg(el, trigger=1, priority=0)])
    # crows in the ditch: the first fight
    done = SW('P: Crows')
    el = Ev()
    el.se('Crow')
    el.balloon(-1, 1)
    el.text(["Crows lift screaming from something in the ditch,", "then wheel back down at you."])
    el.say(HANMA, ["Your first fight in this body. Strike true;", "the light does the rest."], 'command')
    el.battle(TR["Crows x2"], can_escape=False, can_lose=False)
    el.text(["In the ditch lies a goat, torn open. Not by crows."])
    el.say(HANMA, ["Wolves, or worse. The village has trouble."], 'stern')
    first_fight_tips(el)
    el.switch(done)
    for y in (9, 10):
        mb.add("Crows", 7, y, [pg(el, trigger=1, priority=0), pg(None, sw=done, priority=0)])
    # a waymark stone
    el = Ev().text(["A weathered waymark stone. Most of the letters are gone:", "\"…ENAU  3\" and an arrow east."])
    mb.add("Waymark", 20, 8, [pg(el, trigger=0, priority=1)])
    return mb

# ---------------------------------------------------------------------------
# 4  Kiefernwald  (sample 257): the trees
# ---------------------------------------------------------------------------
def trees():
    mb = MapBuild(TREES, NAMES[TREES], 257, display=NAMES[TREES])
    mb.props(note="<Rank: F>\n<Area Name: Kiefernwald>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field2', 60), bgs=('Rain1', 20), battleback=('Grassland', 'Forest'),
             encounters=[(TR["Wolf"], 8, ()), (TR["Crows x2"], 8, ()), (TR["Wolf & Crow"], 4, ())], steps=26)
    mb.exit([(1, 32), (1, 33)], RIDGE, 12, 25, 8, name="To Kiefernkamm")
    for x in (17, 18, 19):
        el = Ev().se('Move1', 60).transfer(RABENAU, 13, 28, 8, 0)
        mb.add("To Rabenau", x, 3, [pg(el, trigger=1, priority=0)])
    # the hungry wolf
    done = SW('P: Wolf')
    el = Ev()
    el.se('Wolf')
    el.balloon(-1, 1)
    el.text(["A lone wolf steps onto the path, ribs showing under", "wet fur. It lowers its head."])
    el.say(HANMA, ["Hungry. It won't back down, and neither can we."], 'command')
    el.battle(TR["Wolf"], can_escape=False, can_lose=False)
    first_fight_tips(el)
    el.switch(done)
    for x in (7, 8, 9):
        mb.add("Hungry Wolf", x, 24, [pg(el, trigger=1, priority=0), pg(None, sw=done, priority=0)])
    # an old trapper's cache
    el = Ev().se('Chest1').item(IT["Heiltrank"], 2).text(["An old trapper's cache under the roots:", "2 Heiltrank."])
    el.self_switch('A')
    mb.add("Cache", 32, 6, [pg(el, char='!Chest', index=0, direction=2, pattern=0, trigger=0, priority=1,
                               walk_anime=False, direction_fix=True),
                            pg(None, self_sw='A', char='!Chest', index=0, direction=8, pattern=0, priority=1,
                               walk_anime=False, direction_fix=True)])
    el = Ev().se('Item3').item(IT["Kräuterbündel"], 2).text(["Wound-herbs, sheltered from the rain:",
                                                              "2 Kräuterbündel."]).self_switch('A')
    mb.add("Herbs", 6, 15, [pg(el, char='!Crystal', index=6, trigger=0, priority=1, step_anime=True),
                            pg(None, self_sw='A', priority=0)])
    return mb
