"""Act II opening: Die Wacht. The Wallstraße, Frontposten 3 on the Nordwall, the night assault on the breach,
and Falin, the living armor, joining the party."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story.ids import *
from story.ch1 import chest
from story.ch2 import camp_fire
from story.ch3 import Q_WALL, S_CALL, GUARD, HOUND_CHAR

MORI = npc_speaker("Mori Daisuke", "Evil", 1)
SOLDIER = npc_speaker("Wall Soldier", "People3", 7)
QM = npc_speaker("Quartiermeisterin", "People4", 2)

Q_BREACH = Quest(15, "Die Bresche", "Mori Daisuke", "Frontposten 3",
                 "Frontposten 3 guards the old north gate, broken the night Weißenfels fell. Something tries the "
                 "breach every night, and every night the living armor the soldiers call die Eiserne holds it. "
                 "Captain Mori wants you on the wall when the bell rings.",
                 "Rest in the barracks; wait for the bell.")
Q_WALLFESTE = Quest(16, "Die Wallfeste", "Mori Daisuke", "Nordwall",
                    "Marshal Kōsaka Tetsuji commands the Nordwall from the Wallfeste. Mori is sending word that a "
                    "vessel and a living armor held the breach against an Aschenschwinge. The marshal will want to "
                    "see them. The Wallweg runs east from Frontposten 3's south gate.",
                    "Take the Wallweg east to the Wallfeste.")

S_A2 = SW('A2: On the Wall')
S_FP = SW('A2: At Frontposten')
S_BRIEF = SW('A2: Briefed')
S_ASSAULT = SW('A2: Night Assault')
S_VANGUARD = SW('A2: Vanguard Down')
S_FALIN = SW('A2: Falin Joined')

FALIN_ID = 3


def build():
    return [wallstrasse(), frontposten(), bresche()]


# ---------------------------------------------------------------------------
# 60  Wallstraße  (sample 217): the road to the Wall
# ---------------------------------------------------------------------------
def wallstrasse():
    mb = MapBuild(WALLSTRASSE, NAMES[WALLSTRASSE], 217, display=NAMES[WALLSTRASSE])
    mb.props(note="<Rank: E>\n<Area Name: Wallstraße>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field4', 60), bgs=('Wind2', 40), battleback=('Snowfield', 'Snowfield'),
             encounters=[(TR["Aschenhunde x2"], 6, ()), (TR["Aschenleichen x2"], 5, ()),
                         (TR["Aschenleiche & Hund"], 5, ()), (TR["Frost Wolves x2"], 2, ())],
             steps=28, weather='snow 3')
    el = Ev()
    el.card("Akt II", "Die Wacht", 240)
    el.wait(10)
    el.narrate(["Two days north of Wachtburg the farms stop. Then the",
                "trees. Then the snow, in Blütenmond, and on the",
                "horizon a grey line that is not a mountain."])
    el.say(HANMA, ["The Nordwall. Forty miles of stone, and it still",
                   "leaks. When I was alive there was no wall at all."], 'calm')
    el.say(KANTA, ["What was there?"], 'calm')
    el.say(HANMA, ["Us."], 'stern')
    el.quest_desc(Q_WALL, "The Wallstraße climbs to the Nordwall. Frontposten 3 is at the top of the road. Report "
                          "to Captain Mori Daisuke.")
    el.switch(S_A2)
    mb.autorun("Arrival", el)
    for x in (11, 12, 13):
        el = Ev().se('Move1', 60).transfer(NORDSTRASSE, 27, 1, 2, 0)
        mb.add("South", x, 26, [pg(el, trigger=1, priority=0)])
    for x in (10, 11, 12):
        el = Ev().se('Move1', 60).transfer(FRONTPOSTEN, 16, 32, 8, 0)
        mb.add("North", x, 0, [pg(el, trigger=1, priority=0)])
    # an overturned supply cart
    el = Ev()
    el.text(["A supply cart for the Wall, on its side in the snow.",
             "The mule is gone. The drivers aren't. Nobody came",
             "back to bury them."])
    el.say(HANMA, ["Hounds. Days ago. The cold kept them."], 'stern')
    el.if_self('A', False, lambda b: (b.se('Item3'), b.item(IT["Heiltrank"], 3), b.item(IT["Lichtphiole"], 2),
                                      b.notice(["Found 3 Heiltrank and 2 Lichtphiole in the cart."]),
                                      b.self_switch('A')))
    mb.add("Supply Cart", 9, 10, [pg(el, char='Damage1', index=6, direction=2, priority=1),
                                  pg(el, self_sw='A', char='Damage1', index=6, direction=2, priority=1)])
    camp_fire(mb, 9, 7, WALLSTRASSE, 10, 7, 8, ["A soldiers' fire ring, half buried. Dry wood under a", "tarp."])
    chest(mb, "Chest", 16, 21, lambda e: (e.item(IT["Großer Heiltrank"], 1), e.gold(80)),
          "Found a Großer Heiltrank and \\MONEY[80].")
    return mb


# ---------------------------------------------------------------------------
# 61  Frontposten 3  (sample 19)
# ---------------------------------------------------------------------------
def frontposten():
    mb = MapBuild(FRONTPOSTEN, NAMES[FRONTPOSTEN], 19, display=NAMES[FRONTPOSTEN])
    mb.props(note="<Area Name: Frontposten 3>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Castle3', 60), bgs=('Wind1', 35), weather='snow 2')
    el = Ev().text(["The south gate, and the Wallstraße beyond it."])
    el.choices(["Leave Frontposten 3", "Stay"],
               [lambda e: (e.se('Move1', 60), e.transfer(WALLSTRASSE, 11, 1, 2, 0)), None], cancel=1)
    el2 = Ev().text(["The south gate: the Wallstraße runs south to Wachtburg,",
                     "the Wallweg east along the Wall to the Wallfeste."])
    el2.choices(["Wallweg (east, to the Wallfeste)", "Wallstraße (south, to Wachtburg)", "Stay"],
                [lambda e: (e.se('Move1', 60), e.transfer(WALLWEG, 12, 33, 8, 0)),
                 lambda e: (e.se('Move1', 60), e.transfer(WALLSTRASSE, 11, 1, 2, 0)), None], cancel=2)
    mb.add("South Gate", 16, 34, [pg(el, trigger=0, priority=1), pg(el2, sw=S_FALIN, trigger=0, priority=1)])
    # arrival: Mori
    el = Ev()
    el.set_time(17, 0)
    el.wait(10)
    el.narrate(["Frontposten 3: a fortress of pale stone grown into the",
                "Wall like a knot in a rope. Soldiers on every rampart,",
                "and all of them are watching north."])
    el.say(MORI, ["Guild? Rank E?"])
    el.say(KANTA, ["Kanta. This is Hanma."], 'calm')
    el.say(MORI, ["Mori Daisuke, captain. They send me two."])
    el.say(HANMA, ["Two and a ghost."], 'stern')
    el.say(MORI, ["Two and a ghost. The Guild's generosity knows no",
                  "bounds. …Fine. I've had worse. I've had nothing."])
    el.say(MORI, ["Here's the Wall: forty miles, thirty thousand men, and",
                  "we hold three miles of it. The old north gate is ours.",
                  "It broke the night Weißenfels fell. The Crown's been",
                  "promising stone for six years."])
    el.say(MORI, ["Every night something tries the breach. Every night",
                  "Falin holds it."])
    el.say(KANTA, ["Die Eiserne."], 'calm')
    el.say(MORI, ["The soldiers' name. She doesn't use it. She doesn't",
                  "use much of anything. Doesn't eat with us, doesn't sleep",
                  "much. Walked out of the snow the night Weißenfels fell",
                  "and took the breach, and nobody's asked her to leave."])
    el.say(MORI, ["Eat. Sergeant Kōno has bunks for you. When the bell",
                  "rings, go through the inner gate to the keep, and the",
                  "breach is beyond it. Stay out of Falin's way and hit",
                  "whatever gets past her."])
    el.quest_done(Q_WALL)
    el.quest_new(Q_BREACH)
    el.switch(S_FP)
    el.switch(S_BRIEF)
    mb.autorun("Arrival", el)
    # Mori
    p = []
    el = Ev().say(MORI, ["Sergeant Kōno has your bunks. Sleep while you can.",
                         "The bell will wake you."])
    p.append(pg(el, char=MORI.char[0], index=MORI.char[1], direction=2, priority=1))
    el = Ev().say(MORI, ["The breach! Through the inner gate, go!"])
    p.append(pg(el, sw=S_ASSAULT, char=MORI.char[0], index=MORI.char[1], direction=2, priority=1))
    el = Ev()
    el.say(MORI, ["You held the breach with her. Against that thing."])
    el.say(MORI, ["Twenty years on this wall. I've buried a lot of better",
                  "soldiers than you, Neuling. I don't intend to bury you."])
    el.say(MORI, ["The Marshal's at the Wallfeste, a day east. Out the",
                  "south gate and take the Wallweg."])
    p.append(pg(el, sw=S_FALIN, char=MORI.char[0], index=MORI.char[1], direction=2, priority=1))
    mb.add("Mori Daisuke", 16, 29, p)
    # the sergeant: bunks, and the night assault
    sgt = npc_speaker("Sergeant Kōno", "People3", 4)
    def sleep(e):
        e.fadeout()
        e.recover_all()
        e.rest_point(FRONTPOSTEN, 16, 31, 2)
        e.wait(60)
        e.if_switch(S_ASSAULT, False, night_alarm, lambda b: (b.set_time(7, 0), b.fadein()))
    def night_alarm(e):
        e.set_time(23, 40)
        e.wait(30)
        e.se('Bell3', 100)
        e.wait(20)
        e.se('Bell3', 100)
        e.fadein()
        e.shake(3, 6, 30)
        e.text(["The bell. Boots on stone, shouting on the walls."])
        e.say(MORI, ["Up! Up! They're at the breach, more than usual, and",
                     "they've brought something big! Inner gate, then the",
                     "keep, now! Falin's out there alone!"])
        e.quest_desc(Q_BREACH, "The night assault. The inner gate (north side of the courtyard) leads through the "
                               "keep to the breach.")
        e.switch(S_ASSAULT)
    el = Ev()
    el.say(sgt, ["Kōno. Bunks are in the west tower, half of them empty,",
                 "and the empty ones still have boots under them."])
    el.choices(["Sleep", "Not yet"], [sleep, None], cancel=1)
    mb.npc("Sergeant Kōno", 19, 31, sgt, el, direction=4)
    # the quartermaster
    el = Ev()
    el.say(QM, ["Quartermaster. Wall rates, which is to say robbery,",
                "but at least it's honest robbery."])
    el.shop([('item', IT["Heiltrank"]), ('item', IT["Großer Heiltrank"]), ('item', IT["Manatrank"]),
             ('item', IT["Riechsalz"]), ('item', IT["Lichtphiole"]), ('item', IT["Wärmetee"]),
             ('armor', AR["Wachmantel"]), ('armor', AR["Stahlhaube"]), ('armor', AR["Turmschild"]),
             ('weapon', WP["Panzerhandschuhe"])])
    mb.npc("Quartermaster", 13, 31, QM, el, direction=6)
    # the inner gate: the keep, and the breach beyond it (the sample's decor gate is replaced)
    mb.remove_at(16, 27)
    closed = Ev().text(["The inner gate. Beyond it the keep, and beyond the",
                        "keep, the breach. Mori's orders: shut until the bell."])
    go = Ev().text(["The inner gate stands open. Beyond the keep, the",
                    "breach, and the sound of fighting."])
    go.choices(["To the breach", "Wait"],
               [lambda e: (e.se('Open2'), e.se('Move1', 60), e.transfer(BRESCHE, 12, 15, 2, 0)), None], cancel=1)
    mb.add("Inner Gate", 16, 27, [pg(closed, char='!$Gate1', index=0, direction=2, trigger=0, priority=1,
                                     walk_anime=False),
                                  pg(go, sw=S_ASSAULT, char='!$Gate1', index=0, direction=2, pattern=2, trigger=0,
                                     priority=1, walk_anime=False)])
    # soldiers
    el = Ev().if_switch(S_FALIN, True,
                        lambda b: b.say(SOLDIER, ["She's going with you? Die Eiserne, leaving the",
                                                  "breach? …Gods keep you. Gods keep us, too."]),
                        lambda b: b.say(SOLDIER, ["Falin? Never seen her face. Nobody has. She holds",
                                                  "that gap every night and walks back in at dawn",
                                                  "covered in ash. Doesn't say a word."]))
    mb.npc("Wall Soldier", 9, 33, SOLDIER, el, direction=2)
    s2 = npc_speaker("Wall Soldier", "People3", 6)
    el = Ev().say(s2, ["Hounds, dead men and things in armor with nobody",
                       "inside. That's what comes. The dead men used to be",
                       "Weißenfels. We burn ours, you know. That's why."])
    mb.npc("Wall Soldier", 23, 33, s2, el, direction=2)
    s3 = npc_speaker("Archer", "People3", 5)
    el = Ev().say(s3, ["The big one has wings. We call it the Aschenschwinge.",
                       "It took four of ours this month. Arrows don't stick."])
    mb.npc("Archer", 14, 29, s3, el, direction=6)
    for x, y in [(13, 28), (19, 28), (14, 19), (18, 19)]:
        mb.light('brazier', x, y)
    return mb


# ---------------------------------------------------------------------------
# 62  Die Bresche  (sample 286): the breach, the ash plain beyond
# ---------------------------------------------------------------------------
def bresche():
    mb = MapBuild(BRESCHE, NAMES[BRESCHE], 286, display=NAMES[BRESCHE])
    mb.props(note="<Rank: E>\n<Area Name: Die Bresche>", bgm=('Dungeon7', 55), bgs=('Wind3', 45),
             battleback=('Ground1', 'Ruins1'), weather='snow 4')
    el = Ev().se('Move1', 60).transfer(FRONTPOSTEN, 16, 28, 2, 0)
    mb.add("Gate", 12, 14, [pg(el, trigger=1, priority=0)])
    # the edges of the ash plain
    def edge(step):
        e = Ev().text(["The Aschenfeld: ash to the horizon under a red-black",
                       "sky. Nothing that lives out there wants to meet you."])
        e.route(-1, [(step, [])], skippable=True)
        return e
    for x in range(1, 24):
        mb.add("Ash Plain", x, 24, [pg(edge(4), trigger=1, priority=0)])
    for y in range(11, 25):
        mb.add("Ash Plain", 0, y, [pg(edge(3), trigger=1, priority=0)])
        mb.add("Ash Plain", 24, y, [pg(edge(2), trigger=1, priority=0)])
    # Falin
    p = [pg(None, priority=0)]
    fal = Ev()
    fal.say(FALIN, ["…"], 'calm')
    p.append(pg(fal, sw=S_ASSAULT, char=FALIN.char[0], index=FALIN.char[1], direction=2, priority=1))
    p.append(pg(None, sw=S_FALIN, priority=0))
    falin_ev = mb.add("Falin", 12, 18, p)
    # the vanguard
    def foe(name, x, y, sheet, index):
        return mb.add(name, x, y, [pg(None, priority=0),
                                   pg(None, sw=S_ASSAULT, char=sheet, index=index, direction=8, priority=1,
                                      step_anime=True),
                                   pg(None, sw=S_VANGUARD, priority=0)])
    foe("Aschenleiche", 10, 21, 'Monster', 1)
    foe("Leere Rüstung", 12, 22, 'Monster', 3)
    foe("Aschenleiche", 14, 21, 'Monster', 1)
    wing = mb.add("Aschenschwinge", 12, 21, [pg(None, priority=0)])

    el = Ev()
    el.wait(20)
    el.narrate(["Beyond the gate the land is grey: ash, not snow,",
                "drifting down out of a red-black sky."])
    el.narrate(["And in the gap where the old gate stood, one figure in",
                "dark, battered plate holds the line alone."])
    el.say(FALIN, ["Get back inside."], 'fierce')
    el.say(KANTA, ["The Guild sent us. Mori sent us."], 'calm')
    el.balloon(falin_ev, 1)
    el.route(falin_ev, [(19, [])], wait=True)     # she turns
    el.say(FALIN, ["…"], 'calm')
    el.say(FALIN, ["You. You smell like nothing."], 'calm')
    el.say(HANMA, ["She's a vessel. Empty, like you, my Lord. I'd stake",
                   "my second death on it."], 'stern')
    el.say(FALIN, ["Later. Stand behind me and hit what I hit."], 'fierce')
    el.route(falin_ev, [(16, [])], wait=True)
    el.se('Equip3')
    el.party(FALIN_ID, True)
    el.plugin('Story_Core', 'SyncLevel', {'actorId': FALIN_ID, 'sourceId': 1}, 'Sync Level')
    el.plugin('Story_Core', 'AutoBuild', {'actorId': FALIN_ID}, 'Auto Build')
    el.notice(["\\C[6]Falin\\C[0] joins the fight! (She levels on her own from now on;",
               "her stat points were spent for her this once.)"])
    el.battle(TR["Bresche: Vorhut"], can_escape=False, can_lose=False)
    el.switch(S_VANGUARD)
    el.wait(20)
    el.se('Monster4', 100, 70)
    el.shake(6, 7, 40)
    el.flash((255, 90, 60, 150), 30)
    el.text(["A shriek from the red sky. Wings the width of the",
             "gate, and the ash storms up around them as something",
             "lands in the breach."])
    el.route(wing, [(41, ['$BigMonster2', 0]), (35, []), (33, [])], wait=False)
    el.script("const e = $gameMap.event(%d); e.setDirectionFix(false); e.setDirection(8); e.setDirectionFix(true);" % wing)
    el.say(FALIN, ["Aschenschwinge. It took four of Mori's men this month."], 'fierce')
    el.say(HANMA, ["Miasma-touched, and rank E like you, now. No more",
                   "half-hits, my Lord. Show it what the light does."], 'command')
    el.battle(TR["Aschenschwinge"], can_escape=False, can_lose=False)
    el.route(wing, [(41, ['', 0])], wait=False)
    el.fadeout()
    el.set_time(6, 0)
    el.wait(40)
    el.fadein()
    el.narrate(["Dawn comes grey over the Aschenfeld. The breach is",
                "full of ash that used to be something."])
    el.route(falin_ev, [(19, [])], wait=True)
    el.say(FALIN, ["Six years I've held this gap. First time I've watched",
                   "the sun come up with someone else in it."], 'calm')
    el.say(KANTA, ["You said I smell like nothing."], 'calm')
    el.say(FALIN, ["Everyone smells of something. Blood, smoke, bread,",
                   "fear. You don't. Neither do I."], 'calm')
    el.say(FALIN, ["I woke in the snow outside Weißenfels, the night it",
                   "fell. The city was burning behind me. I was inside",
                   "this armor. I don't remember putting it on."], 'hurt')
    el.say(FALIN, ["I don't remember anything before the snow. There's a",
                   "name scratched inside the breastplate, over the heart:",
                   "FALIN. So that's what I answer to."], 'calm')
    el.say(HANMA, ["And the plate?"], 'calm')
    el.say(FALIN, ["The first year I could still find the straps. Then I",
                   "couldn't. It grew into me. It mends when I heal. It",
                   "bleeds when I bleed."], 'calm')
    el.say(KANTA, ["I woke in a cave. Sixteen, no, twenty days ago. With a",
                   "light in my hand and a dead general for company."], 'wry')
    el.say(HANMA, ["Charming company."], 'smile')
    el.say(FALIN, ["Then you're the first thing in six years that makes",
                   "any sense of me."], 'smile')
    el.say(MORI, ["Falin! …Gods. You're alive. All three of you. Four."])
    el.say(MORI, ["The Wallfeste has finally sent a company to wall up",
                  "the breach. They arrive in three days. Six years I've",
                  "been asking, and what gets them moving is a report that",
                  "a rank E girl killed the Aschenschwinge."])
    el.say(FALIN, ["If I go, who holds the breach?"], 'calm')
    el.say(MORI, ["Stone. Finally. Go with them, Falin. You've given this",
                  "gap six years. Go find out what you are."])
    el.say(FALIN, ["…"], 'calm')
    el.say(FALIN, ["Where are you going, vessel?"], 'calm')
    el.say(KANTA, ["Wherever the fighting is. I think."], 'calm')
    el.say(FALIN, ["Then I'll walk in front."], 'smile')
    el.me('Fanfare2')
    el.notice(["\\C[6]Falin\\C[0], the living armor, joins the party."])
    el.say(MORI, ["Marshal Kōsaka at the Wallfeste will want to see this:",
                  "a vessel, a living armor and a ghost. I'll send word.",
                  "Rest first. Gods know you've earned it."])
    el.quest_done(Q_BREACH)
    el.quest_new(Q_WALLFESTE)
    el.switch(S_FALIN)
    el.rest_point(FRONTPOSTEN, 16, 31, 2)
    mb.autorun("The Breach", el, cond_switch=S_ASSAULT)
    mb.light('ash_night', 0, 0, tile=False)
    mb.light('gate_fire', 10, 14)
    mb.light('gate_fire', 14, 14)
    mb.follow_light('beam', 12, 15)
    return mb
