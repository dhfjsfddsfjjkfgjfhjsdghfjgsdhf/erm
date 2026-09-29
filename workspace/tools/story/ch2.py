"""Chapter 2: Die Oststraße and Eisfurt. The escort, the deserters, the frozen ford, the Eisfall and Fubuki."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story.ids import *
from story.ch1 import SAGARA, Q_EAST, S_EAST, chest

UEDA = npc_speaker("Ueda Ryō", "People1", 4)
VOGT = npc_speaker("Shirakawa Kaname", "People3", 5)
EMI = npc_speaker("Nagase Emi", "People4", 1)
AIKA = npc_speaker("Wakaba Aika", "People2", 1)
KUZE = npc_speaker("Kuze Riko", "People4", 3)
FUBUKI = Speaker("Fubuki", "", 0, ("Nature", 6))
DESERTER = Speaker("Deserter", "", 0, ("Evil", 0))
SERGEANT = Speaker("Deserter Sergeant", "", 0, ("Evil", 1))

Q_WINTER = Quest(6, "Winter in Blütenmond", "Shirakawa Kaname", "Eisfurt, Frostpfad",
                 "The river Eis froze at the new moon, a month into spring. No ferry, no trade. The Vogt of Eisfurt "
                 "pays 1 gk to whoever brings the spring back. The shrine maiden Wakaba Aika knows the old stories.",
                 "Ask around Eisfurt.")

S_C2 = SW('C2: On the Road')
S_KAMA = SW('C2: Kamaitachi')
S_DESERT = SW('C2: Deserters')
S_CAMP = SW('C2: Camp Night')
S_EISFURT = SW('C2: In Eisfurt')
S_VOGT = SW('C2: Vogt Asked')
S_AIKA = SW('C2: Aika Told')
S_SHRINE = SW('C2: Shrine Seen')
S_WURM = SW('C2: Eiswurm Down')
S_FUBUKI = SW('C2: Fubuki Calmed')
S_THAW = SW('C2: Thaw')
S_PAID = SW('C2: Vogt Paid')

SNOW = ('snow', 4)

def build():
    return [oststrasse(), shrine_camp(), eisfurt(), furt_inn(), vogtei(), kuze_shop(), frostpfad(), hochweg(),
            eisfall(), eisfall_heart()]

def camp_fire(mb, x, y, rest_map, rx, ry, d=8, text=None):
    el = Ev()
    el.text(text or ["A sheltered fire pit. Someone has left dry wood."])
    def rest(e):
        e.fadeout()
        e.recover_all()
        e.rest_point(rest_map, rx, ry, d)
        e.wait(40)
        e.fadein()
        e.text(["You rest by the fire. (HP and MP restored. If you fall,", "you'll wake here.)"])
    el.choices(["Rest here", "Move on"], [rest, None], cancel=1)
    mb.add("Campfire", x, y, [pg(el, char='!Other2', index=3, direction=2, trigger=0, priority=1, step_anime=True)])

# ---------------------------------------------------------------------------
# 20  Oststraße  (sample 258)
# ---------------------------------------------------------------------------
def oststrasse():
    mb = MapBuild(OSTSTRASSE, NAMES[OSTSTRASSE], 258, display=NAMES[OSTSTRASSE])
    mb.props(note="<Rank: F>\n<Area Name: Oststraße>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field3', 65), battleback=('Road1', 'Forest'),
             encounters=[(TR["Grey Wolves x2"], 8, ()), (TR["Kamaitachi x2"], 7, ()),
                         (TR["Grey Wolf & Kamaitachi"], 6, ()), (TR["Crows x3"], 3, ())], steps=30)
    # arrival from Rabenau
    el = Ev()
    el.card("Kapitel 2", "Die Oststraße", 200)
    el.say(SAGARA, ["Two days to Eisfurt if the weather holds. We camp at",
                    "the old wayside shrine tonight."])
    el.say(SAGARA, ["I'll keep to the mule. You keep to the trouble.", "That's the arrangement."])
    el.say(HANMA, ["A sensible arrangement."], 'smile')
    el.switch(S_C2)
    mb.autorun("Arrival", el)
    for x in (4, 5, 6):
        el = Ev().text(["Rabenau lies behind you. Sagara won't turn back now."])
        el.route(-1, [(4, [])], skippable=True)
        mb.add("Back", x, 22, [pg(el, trigger=1, priority=0)])
    # kamaitachi ambush
    el = Ev()
    el.se('Wind4')
    el.balloon(-1, 1)
    el.text(["The grass hisses, though there is no wind. Something", "moves through it, fast and low."])
    el.say(SAGARA, ["Kamaitachi! Mind your legs, they go for the legs!"])
    el.battle(TR["Kamaitachi x3"], can_escape=False, can_lose=False)
    el.say(SAGARA, ["…Still got both legs? Good. The mule too. Good."])
    el.switch(S_KAMA)
    for x in (5, 6, 7, 8):
        mb.add("Kamaitachi", x, 16, [pg(el, trigger=1, priority=0), pg(None, sw=S_KAMA, priority=0)])
    # deserters
    ids = []
    for x, y, who in [(32, 5, DESERTER), (33, 4, SERGEANT), (34, 5, DESERTER)]:
        ids.append(mb.add(who.name, x, y, [pg(None, priority=0),
                                           pg(None, sw=S_C2, char=who.char[0], index=who.char[1], direction=2,
                                              priority=1),
                                           pg(None, sw=S_DESERT, priority=0)]))
    el = Ev()
    el.balloon(ids[1], 1)
    el.say(SERGEANT, ["Hold it. Road toll."])
    el.say(SERGEANT, ["Everything you're carrying, and the mule. We're not",
                      "greedy. We'll leave you the boots."])
    el.say(HANMA, ["Those are Nordwall coats. Deserters."], 'stern')
    el.say(SERGEANT, ["Nordwall's dead, old woman. We saw what's coming over",
                      "it. Now pay, or join it."])
    def pay(e):
        e.say(KANTA, ["…Take the coin. Leave the mule."], 'calm')
        e.gold(-60)
        e.say(SERGEANT, ["Pathetic. Now the mule."])
        e.say(SAGARA, ["Not the mule!"])
        e.say(KANTA, ["No. Not the mule."], 'fierce')
    def refuse(e):
        e.say(KANTA, ["No."], 'fierce')
        e.say(SERGEANT, ["Wrong answer."])
    el.choices(["Pay what you have", "Refuse"], [pay, refuse], cancel=-1)
    el.se('Sword4')
    el.battle(TR["Deserters"], can_escape=False, can_lose=False)
    el.switch(S_DESERT)
    el.text(["The sergeant goes down hard. From his pack spills a",
             "clutter of stolen things: rings, a church candlestick,",
             "and a silver bowl, dented, still frosted with old ice."])
    el.se('Item3')
    el.item(IT["Silberne Opferschale"], 1)
    el.gold(40)
    el.notice(["Received the Silberne Opferschale and \\MONEY[40]."])
    el.say(HANMA, ["Shrine silver. They've robbed a shrine on their way",
                   "south."], 'stern')
    el.say(SAGARA, ["That's… an offering bowl. There's a shrine up the",
                    "Frostpfad, above Eisfurt. They keep a bowl like that."])
    el.say(SAGARA, ["Heh. I'll tell you the story at the fire."])
    for x in (31, 32, 33, 34):
        mb.add("Toll", x, 7, [pg(el, trigger=1, priority=0, sw=S_C2), pg(None, sw=S_DESERT, priority=0)])
    for x in (32, 33, 34):
        el2 = Ev().se('Move1', 60).transfer(SHRINE_CAMP, 10, 14, 8, 0)
        mb.add("On to the shrine", x, 2, [pg(el2, trigger=1, priority=0)])
    chest(mb, "Chest", 31, 17, lambda e: e.item(IT["Manatrank"], 2), "Found 2 Manatrank.")
    chest(mb, "Chest", 3, 9, lambda e: e.armor(AR["Lederrock"], 1), "Found a Lederrock.")
    return mb

# ---------------------------------------------------------------------------
# 21  Wegschrein  (sample 259): the night camp
# ---------------------------------------------------------------------------
def shrine_camp():
    mb = MapBuild(SHRINE_CAMP, NAMES[SHRINE_CAMP], 259, display=NAMES[SHRINE_CAMP])
    mb.props(note="<Area Name: Wegschrein>\n<lighting: Outside>\n<No Rank HUD>", bgm=None, bgs=('Night', 45))
    camp_fire(mb, 10, 12, SHRINE_CAMP, 10, 13, 8, ["The camp fire at the wayside shrine."])
    sag = mb.add("Sagara", 12, 12, [pg(Ev().say(SAGARA, ["Sleep while you can. Eisfurt's a cold bed."]),
                                       char=SAGARA.char[0], index=SAGARA.char[1], direction=4, priority=1)])
    el = Ev()
    el.set_time(21, 0)
    el.wait(20)
    el.narrate(["Night at the wayside shrine. The statue's face has been",
                "worn smooth by a thousand years of rain and hands."])
    el.say(SAGARA, ["So. Eisfurt. The river there, the Eis, froze at the new",
                    "moon. In Blütenmond! Ice thick enough to walk on, and",
                    "nobody dares."])
    el.say(SAGARA, ["No ferry, no trade. My salt's worth nothing if it sits",
                    "on the wrong bank."])
    el.say(KANTA, ["A late winter."], 'calm')
    el.say(SAGARA, ["Winter doesn't come back after it's left. Folk in Eisfurt",
                    "say Fubuki is angry: the snow-woman of the Eisfall."])
    el.say(SAGARA, ["Every year they put the first silver in a bowl at her",
                    "shrine, and every spring she lets the river go.",
                    "…A bowl. Like the one the deserters had."])
    el.say(HANMA, ["So someone robbed a spirit, and a town is paying for it.",
                   "That's how it usually goes."], 'stern')
    el.say(SAGARA, ["I'll sleep on that. Night."])
    el.fadeout()
    el.wait(30)
    el.fadein()
    el.narrate(["Later. Sagara snores. The fire is low."])
    el.say(HANMA, ["You haven't asked me much, my Lord."], 'calm')
    el.say(KANTA, ["Would you answer?"], 'calm')
    el.say(HANMA, ["Some of it."], 'smile')
    el.say(KANTA, ["What were you a general of?"], 'calm')
    el.say(HANMA, ["An army that marched north to end every demon in the",
                   "world. We burned a great deal of the north doing it.",
                   "We didn't finish."], 'stern')
    el.say(KANTA, ["And now?"], 'calm')
    el.say(HANMA, ["Now I mend strangers and watch you sleep in cold",
                   "places. A promotion, of sorts."], 'smile')
    el.say(KANTA, ["…Why me?"], 'hurt')
    el.say(HANMA, ["I don't know. I woke beside you; the thread chose, not I.",
                   "But I've watched you three days. You help people who",
                   "can't pay you, and you know when to walk away."], 'calm')
    el.say(HANMA, ["That's rarer than courage."], 'calm')
    el.say(KANTA, ["I don't feel brave."], 'calm')
    el.say(HANMA, ["Good. The brave ones died first, in my war."], 'stern')
    el.common(CE["Inn Sleep"])
    el.rest_point(SHRINE_CAMP, 10, 13, 8)
    el.switch(S_CAMP)
    mb.autorun("Night", el)
    for x in (9, 10, 11):
        el2 = Ev().se('Move1', 60).transfer(EISFURT, 15, 27, 8, 0)
        mb.add("To Eisfurt", x, 15, [pg(el2, trigger=1, priority=0)])
    return mb

# ---------------------------------------------------------------------------
# 22  Eisfurt  (sample 127)
# ---------------------------------------------------------------------------
def eisfurt():
    mb = MapBuild(EISFURT, NAMES[EISFURT], 127, display=NAMES[EISFURT])
    mb.props(note="<Rank: F>\n<Area Name: Eisfurt>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town4', 65), bgs=('Wind1', 30), battleback=('Snowfield', 'Snowfield'),
             weather='snow 5 unless %d' % S_THAW)
    # the frozen river (a TausiLighting layer), hidden after the thaw
    mb.light('eisfurt_ice', 0, 0, tile=False)
    el = Ev().script("const m = $dataLighting && $dataLighting.getCurrentMap();\n"
                     "if (m) m.objects.filter(o => o.getObject() instanceof Data_Lighting_Layer)"
                     ".forEach(o => o.enabled = !$gameSwitches.value(%d));" % S_THAW)
    mb.add("Ice Layer", 1, 0, [pg(el, trigger=4, priority=0)])
    # arrival
    el = Ev()
    el.wait(10)
    el.say(SAGARA, ["Eisfurt. …Colder than I left it."])
    el.narrate(["Snow on the roofs, snow in the streets, and past the",
                "houses the river Eis lies white and still, frozen from",
                "bank to bank."])
    el.say(SAGARA, ["The other half, as promised. Fifty. You earned it."])
    el.se('Coin')
    el.gold(50)
    el.notice(["Received \\MONEY[50]."])
    el.quest_done(Q_EAST)
    el.say(SAGARA, ["I'll be at Zur Furt with something hot. If you mean to",
                    "fix this, the Vogt will want to hear it. Big hall,",
                    "north side."])
    el.quest_new(Q_WINTER)
    el.switch(S_EISFURT)
    mb.autorun("Arrival", el)

    # doors
    mb.door(9, 19, FURT_INN, 5, 11, 8, name="Door: Zur Furt")
    mb.door(15, 8, VOGTEI, 8, 10, 8, name="Door: Vogtei")
    mb.door(20, 19, KUZE_SHOP, 12, 8, 8, name="Door: Handelshaus")
    mb.door(23, 19, 0, 0, 0, locked_text=["A cooper's shop. \"Closed till the ice goes.\""], name="Door: Cooper")
    mb.door(3, 20, 0, 0, 0, locked_text=["Snowed shut. Smoke from the chimney, though:",
                                         "someone's home and staying there."], name="Door: House")
    mb.door(25, 9, 0, 0, 0, locked_text=["The shrine maiden's house. Nobody answers; she's",
                                         "probably at the statue in the square."], name="Door: Aika")
    # the south gate: where to?
    def gate(e):
        def west(b):
            b.se('Move1', 60)
            b.transfer(OSTSTRASSE, 33, 3, 2, 0)
        def north(b):
            b.se('Move1', 60)
            b.transfer(FROSTPFAD, 8, 21, 8, 0)
        def stay(b):
            b.route(-1, [(4, [])], wait=True, skippable=True)
        e.if_switch(S_AIKA, True,
                    lambda b: b.choices(["Frostpfad (north)", "Oststraße (west)", "Stay"], [north, west, stay], cancel=2),
                    lambda b: b.choices(["Oststraße (west)", "Stay"], [west, stay], cancel=1))
    el = Ev()
    gate(el)
    mb.add("South Gate", 15, 28, [pg(el, trigger=1, priority=0)])

    # Ueda the ferryman and the boat
    p = []
    el = Ev()
    el.say(UEDA, ["No crossing. The Eis has been ice for a month, and it",
                  "creaks like a ship's timbers. Walk on it and it'll open",
                  "under you like a mouth."])
    el.say(UEDA, ["Twenty years I've poled that ferry. Never seen the river",
                  "freeze in Blütenmond. Never."])
    p.append(pg(el, char=UEDA.char[0], index=UEDA.char[1], direction=6, priority=1))
    el = Ev()
    el.say(UEDA, ["She's running! Listen to her: water under the hull",
                  "again. Where to?"])
    def cross(e):
        e.say(UEDA, ["East bank, the Königsstraße. Wachtburg's four days on,",
                     "if you're bound there. Hold on to something."])
        e.se('Water3')
        e.fadeout()
        e.wait(30)
        e.transfer(KOENIGSSTRASSE, 21, 27, 8, 2)
        e.card("Kapitel 3", "Die Königsstraße", 220)
        e.fadein()
    el.choices(["Cross the river", "Not yet"], [cross, None], cancel=1)
    p.append(pg(el, sw=S_THAW, char=UEDA.char[0], index=UEDA.char[1], direction=6, priority=1))
    mb.add("Ueda Ryō", 22, 23, p)
    mb.add("Ferry", 23, 24, [pg(Ev().text(["Ueda's ferry, frozen into the ice at the landing."]),
                                char='Vehicle', index=0, direction=4, priority=1),
                             pg(Ev().text(["Ueda's ferry, rocking on open water."]), sw=S_THAW, char='Vehicle', index=0,
                                direction=4, priority=1, step_anime=True)])

    # Aika at the statue
    p = []
    el = Ev()
    el.say(AIKA, ["Wakaba Aika. I keep Fubuki-sama's shrine, up the",
                  "Frostpfad. …Kept it."])
    el.say(AIKA, ["Every winter we set the first silver of the year in the",
                  "offering bowl there, and every spring she lets the river",
                  "go. At the new moon the bowl was stolen."])
    el.say(AIKA, ["The same night, the Eis froze."])
    el.say(KANTA, ["A silver bowl. Dented."], 'calm')
    el.text(["Kanta holds out the bowl from the deserter's pack."])
    el.balloon(0, 1)
    el.say(AIKA, ["That's it! That's hers! Where did you—deserters?",
                  "Of course. Men running south with their pockets full."])
    el.say(AIKA, ["Please, take it back to her. Not to the shrine: she",
                  "won't come down while she's angry. Into the Eisfall",
                  "itself, past the shrine at the top of the Frostpfad."])
    el.say(AIKA, ["She has a guardian. An ice serpent. Be careful: it's",
                  "old, and it doesn't talk."])
    el.say(HANMA, ["A serpent, a spirit and a frozen river, for one bowl.",
                   "Very well."], 'calm')
    el.item(IT["Wärmetee"], 3)
    el.notice(["Received 3 Wärmetee. Chilled slows you down; hot tea", "fixes it."])
    el.quest_desc(Q_WINTER, "The silver offering bowl the deserters carried belongs to Fubuki, the frost spirit of "
                            "the Eisfall. Aika asks you to return it to her in the Eisfall itself, north up the "
                            "Frostpfad (take the south gate). An ice serpent guards the way.")
    el.switch(S_AIKA)
    p.append(pg(el, char=AIKA.char[0], index=AIKA.char[1], direction=2, priority=1))
    el = Ev().say(AIKA, ["The Frostpfad starts at the south gate and climbs north.",
                         "Fubuki-sama's shrine is at the top. Please hurry."])
    p.append(pg(el, sw=S_AIKA, char=AIKA.char[0], index=AIKA.char[1], direction=2, priority=1))
    el = Ev().say(AIKA, ["You spoke with her. You actually spoke with her.",
                         "…Thank you. I'll set the first silver in her bowl",
                         "myself, every spring I live."])
    p.append(pg(el, sw=S_FUBUKI, char=AIKA.char[0], index=AIKA.char[1], direction=2, priority=1))
    mb.add("Wakaba Aika", 15, 17, p)

    # townsfolk
    kid = npc_speaker("Kanon", "People1", 3)
    el = Ev().if_switch(S_THAW, True,
                        lambda b: b.say(kid, ["The river's making noises like a giant eating",
                                              "gravel! Mama says it's the spring."]),
                        lambda b: b.say(kid, ["I made a snow-woman. She's Fubuki. Mama says",
                                              "don't make fun of Fubuki, so I made her pretty."]))
    mb.npc("Kanon", 12, 22, ("People1", 3), el, direction=2, move_type=1)
    old = npc_speaker("Old Masato", "People1", 6)
    el = Ev().say(old, ["Fubuki? She was old when my grandmother was a girl.",
                        "She's not wicked. She's cold, and she keeps her",
                        "promises. Folk forget that's not the same thing."])
    mb.npc("Old Masato", 6, 14, ("People1", 6), el, direction=6)
    guard = npc_speaker("Guard Hayato", "People3", 6)
    el = Ev().say(guard, ["Deserters came through at the new moon. Six of them,",
                          "Nordwall coats. The Vogt had the gate shut, but they",
                          "went round by the shrine path."])
    mb.npc("Guard Hayato", 16, 26, guard, el, direction=2)
    # after the thaw: celebration scene on arrival back
    el = Ev()
    el.weather('none', 0, 60)
    el.se('Crash', 80, 60)
    el.shake(3, 4, 40)
    el.narrate(["At dawn the ice breaks with a sound like a thousand",
                "doors slamming. By noon the Eis runs black and fast,",
                "carrying floes the size of houses."])
    el.say(SAGARA, ["Hah! Listen to that! My salt's worth something again."])
    el.say(SAGARA, ["If you're going on to Wachtburg, tell the guild Sagara",
                    "Takumi vouches for you. Won't help. It's free, though."])
    el.switch(S_THAW)
    mb.autorun("Thaw", el, cond_switch=S_FUBUKI)
    return mb

# ---------------------------------------------------------------------------
# 23  Zur Furt  (sample 162)
# ---------------------------------------------------------------------------
def furt_inn():
    mb = MapBuild(FURT_INN, NAMES[FURT_INN], 162, display=NAMES[FURT_INN])
    mb.props(note="<Area Name: Zur Furt>\n<No Rank HUD>", bgm=('Town2', 60), bgs=('Fire1', 30))
    el = Ev().se('Move1', 60).transfer(EISFURT, 9, 20, 2, 0)
    mb.add("Exit", 5, 12, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(EMI, ["Welcome to Zur Furt. Warm beds, hot stew, and I'll",
                 "only charge you double because of the ice."])
    def rest(e):
        e.if_gold(20, '>=',
                  lambda b: (b.gold(-20), b.say(EMI, ["Sleep well."]), b.common(CE["Inn Sleep"])),
                  lambda b: b.say(EMI, ["Twenty kupferling. I've got a family to feed, love."]))
    el.choices(["Rest (\\MONEY[20])", "Not now"], [rest, None], cancel=1)
    mb.add("Nagase Emi", 5, 6, [pg(el, char=EMI.char[0], index=EMI.char[1], direction=2, priority=1)])
    el = Ev().if_switch(S_THAW, True,
                        lambda b: b.say(SAGARA, ["To the river! And to the two of you!",
                                                 "…Mostly to the river."]),
                        lambda b: b.say(SAGARA, ["Hot wine. The only thing in Eisfurt that isn't frozen."]))
    mb.add("Sagara", 9, 7, [pg(el, char=SAGARA.char[0], index=SAGARA.char[1], direction=6, priority=1)])
    trader = npc_speaker("Stuck Trader", "People3", 7)
    el = Ev().say(trader, ["Three weeks I've been stuck here with a cart of wool.",
                           "Wool! In a town that's frozen solid! You'd think",
                           "I'd sell it. Nobody has coin."])
    mb.npc("Stuck Trader", 12, 8, trader, el, direction=4)
    mb.light('hearth', 8, 3)
    return mb

# ---------------------------------------------------------------------------
# 24  Vogtei  (sample 164)
# ---------------------------------------------------------------------------
def vogtei():
    mb = MapBuild(VOGTEI, NAMES[VOGTEI], 164, display=NAMES[VOGTEI])
    mb.props(note="<Area Name: Vogtei>\n<No Rank HUD>", bgm=('Castle1', 55))
    el = Ev().se('Move1', 60).transfer(EISFURT, 15, 9, 2, 0)
    mb.add("Exit", 8, 11, [pg(el, trigger=1, priority=0)])
    p = []
    el = Ev()
    el.say(VOGT, ["Shirakawa Kaname, Vogt of Eisfurt for the Crown.",
                  "Adventurers? Guild? …No? Pity."])
    el.say(VOGT, ["You've seen the river. A month of ice, in spring. The",
                  "Crown wants its tolls, the farms want their seed, and",
                  "I want to stop hearing about it."])
    el.say(VOGT, ["One Goldkrone to whoever brings the spring back. I don't",
                  "care if it's prayer, silver or a sword."])
    el.say(VOGT, ["The shrine maiden, Wakaba, has theories. She's usually",
                  "at the statue in the square."])
    el.switch(S_VOGT)
    p.append(pg(el, char=VOGT.char[0], index=VOGT.char[1], direction=2, priority=1))
    el = Ev().say(VOGT, ["The offer stands: one Goldkrone for the spring."])
    p.append(pg(el, sw=S_VOGT, char=VOGT.char[0], index=VOGT.char[1], direction=2, priority=1))
    el = Ev()
    el.say(VOGT, ["The river's open. The ferry's running. I have three",
                  "letters from the Crown on my desk and none of them",
                  "matter anymore. Here: one Goldkrone, as promised."])
    el.se('Coin')
    el.gold(100)
    el.notice(["Received \\MONEY[100]."])
    el.say(VOGT, ["If you're going to Wachtburg, register with the Guild.",
                  "People like you shouldn't be working for Vögte."])
    el.quest_done(Q_WINTER)
    el.switch(S_PAID)
    p.append(pg(el, sw=S_THAW, char=VOGT.char[0], index=VOGT.char[1], direction=2, priority=1))
    el = Ev().say(VOGT, ["Safe roads. And my thanks, which cost me nothing."])
    p.append(pg(el, sw=S_PAID, char=VOGT.char[0], index=VOGT.char[1], direction=2, priority=1))
    mb.add("Shirakawa Kaname", 10, 4, p)
    return mb

# ---------------------------------------------------------------------------
# 25  Handelshaus Kuze  (sample 165)
# ---------------------------------------------------------------------------
def kuze_shop():
    mb = MapBuild(KUZE_SHOP, NAMES[KUZE_SHOP], 165, display=NAMES[KUZE_SHOP])
    mb.props(note="<Area Name: Handelshaus Kuze>\n<No Rank HUD>", bgm=('Town4', 55))
    el = Ev().se('Move1', 60).transfer(EISFURT, 20, 20, 2, 0)
    mb.add("Exit", 12, 9, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(KUZE, ["Kuze's. Everything a frozen town needs, at prices a",
                  "frozen town can almost afford."])
    el.shop([('item', IT["Heiltrank"]), ('item', IT["Großer Heiltrank"]), ('item', IT["Wärmetee"]),
             ('item', IT["Manatrank"]), ('item', IT["Gegengift"]), ('item', IT["Riechsalz"]),
             ('armor', AR["Pelzmütze"]), ('armor', AR["Filzmantel"]), ('armor', AR["Wolfsfellweste"]),
             ('armor', AR["Eisenhaube"])])
    mb.add("Kuze Riko", 8, 5, [pg(el, char=KUZE.char[0], index=KUZE.char[1], direction=2, priority=1)])
    return mb

# ---------------------------------------------------------------------------
# 26  Frostpfad  (sample 260)
# ---------------------------------------------------------------------------
FROST_ENC = lambda: [(TR["Frost Wolves x2"], 8, ()), (TR["Ice Wisps x2"], 6, ()), (TR["Frost Wolf & Wisp"], 6, ()),
                     (TR["Kamaitachi x2"], 3, ())]

def frostpfad():
    mb = MapBuild(FROSTPFAD, NAMES[FROSTPFAD], 260, display=NAMES[FROSTPFAD])
    mb.props(note="<Rank: F>\n<Area Name: Frostpfad>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field4', 60), bgs=('Wind2', 40), battleback=('Snowfield', 'Snowfield'), encounters=FROST_ENC(),
             steps=26, weather='snow 6')
    for x in (7, 8, 9):
        el = Ev().se('Move1', 60).transfer(EISFURT, 15, 27, 8, 0)
        mb.add("To Eisfurt", x, 22, [pg(el, trigger=1, priority=0)])
        el = Ev().se('Move1', 60).transfer(HOCHWEG, 5, 25, 8, 0)
        mb.add("Up", x, 3, [pg(el, trigger=1, priority=0)])
    first = SW('C2: Frostpfad')
    el = Ev()
    el.say(HANMA, ["Mind the cold, my Lord. This body isn't used to it, and",
                   "it'll slow your hands before you notice."], 'stern')
    el.notice(["\\C[6]Chilled\\C[0] (-20 DEX: slower, easier to hit). Wärmetee",
               "cures it; a Filzmantel or Pelzmütze halves the chance."])
    el.switch(first)
    mb.autorun("Enter", el)
    chest(mb, "Chest", 12, 11, lambda e: e.item(IT["Wärmetee"], 2), "Found 2 Wärmetee.")
    return mb

# ---------------------------------------------------------------------------
# 27  Hochweg  (sample 261): the shrine
# ---------------------------------------------------------------------------
def hochweg():
    mb = MapBuild(HOCHWEG, NAMES[HOCHWEG], 261, display=NAMES[HOCHWEG])
    mb.props(note="<Rank: F>\n<Area Name: Hochweg>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field4', 60), bgs=('Wind2', 45), battleback=('Snowfield', 'Snowfield'), encounters=FROST_ENC(),
             steps=24, weather='snow 7')
    for x in (4, 5, 6):
        el = Ev().se('Move1', 60).transfer(FROSTPFAD, 8, 4, 2, 0)
        mb.add("Down", x, 26, [pg(el, trigger=1, priority=0)])
    for x in (17, 18, 19):
        el = Ev().weather('none', 0, 0).se('Move1', 60).transfer(EISFALL, 19, 36, 8, 0)
        mb.add("Into the Eisfall", x, 2, [pg(el, trigger=1, priority=0)])
    # the shrine
    el = Ev()
    el.text(["A little stone shrine, half buried in snow. The offering",
             "niche is empty; the frost on its lip is scored where",
             "something was pried loose."])
    el.if_switch(S_SHRINE, False,
                 lambda b: (b.say(HANMA, ["The bowl belongs here. But the girl was right: nobody",
                                          "is listening at this shrine now."], 'calm'),
                            b.say(KANTA, ["Then we take it to her."], 'calm'),
                            b.switch(S_SHRINE)))
    mb.add("Frost Shrine", 11, 8, [pg(el, char='!Other2', index=4, direction=2, priority=1)])
    camp_fire(mb, 21, 7, HOCHWEG, 20, 7, 4, ["A herders' fire pit under an overhang, out of the wind."])
    chest(mb, "Chest", 25, 13, lambda e: e.item(IT["Großer Heiltrank"], 1), "Found a Großer Heiltrank.")
    return mb

# ---------------------------------------------------------------------------
# 28  Eisfallhöhle  (sample 219)
# ---------------------------------------------------------------------------
def eisfall():
    mb = MapBuild(EISFALL, NAMES[EISFALL], 219, display=NAMES[EISFALL])
    mb.props(note="<Rank: F>\n<Area Name: Eisfallhöhle>", bgm=('Dungeon4', 60), bgs=('Wind3', 30),
             battleback=('IceCave', 'IceCave'),
             encounters=[(TR["Ice Wisps x2"], 7, ()), (TR["Frost Wolves x2"], 5, ()), (TR["Ice Wisps x3"], 4, ()),
                         (TR["Frost Wolf & Wisp"], 6, ())], steps=24)
    el = Ev().se('Move1', 60).transfer(HOCHWEG, 18, 3, 2, 0)
    mb.add("Out", 19, 37, [pg(el, trigger=1, priority=0)])
    # the west passage: a dead end with a frozen cache
    chest(mb, "Frozen Cache", 2, 16, lambda e: (e.item(IT["Manatrank"], 2), e.gold(60)),
          "A cache frozen into the wall: 2 Manatrank and \\MONEY[60].")
    chest(mb, "Chest", 35, 32, lambda e: e.item(IT["Riechsalz"], 2), "Found 2 Riechsalz.")
    chest(mb, "Chest", 11, 10, lambda e: e.armor(AR["Pelzmütze"], 1), "Found a Pelzmütze.")
    # Eiswurm guards the way in
    el = Ev()
    el.se('Ice9')
    el.shake(5, 6, 30)
    el.text(["The wall ahead shifts. Ice cracks, and a head the size", "of a cart uncoils from it: a serpent of living ice."])
    el.say(HANMA, ["The guardian. It won't talk and it won't stop.", "Don't let its breath settle on you!"], 'command')
    el.battle(TR["Eiswurm"], can_escape=False, can_lose=False)
    el.text(["The serpent shatters into a thousand shards… and the",
             "shards begin, slowly, to crawl back together."])
    el.say(HANMA, ["It'll reform. Guardians always do. Move, my Lord."], 'command')
    el.switch(S_WURM)
    go_in = Ev().se('Move1', 60).transfer(EISFALL_HEART, 5, 33, 8, 0)
    mb.add("Heart Passage", 15, 5, [pg(el, trigger=1, priority=0), pg(go_in, sw=S_WURM, trigger=1, priority=0)])
    first = SW('C2: Eisfall')
    el = Ev()
    el.say(HANMA, ["Dark as the first cave. Keep your light up."], 'calm')
    el.switch(first)
    mb.autorun("Enter", el)
    mb.light('ice_dark', 0, 0, tile=False)
    mb.follow_light('beam', 19, 36)
    for x, y in [(15, 6), (7, 23), (27, 29), (33, 20), (20, 5)]:
        mb.light('ice_glow', x, y)
    return mb

# ---------------------------------------------------------------------------
# 29  Herz des Eisfalls  (sample 222): Fubuki
# ---------------------------------------------------------------------------
def eisfall_heart():
    mb = MapBuild(EISFALL_HEART, NAMES[EISFALL_HEART], 222, display=NAMES[EISFALL_HEART])
    mb.props(note="<Rank: E>\n<Area Name: Herz des Eisfalls>", bgm=('Dungeon5', 55), bgs=('Wind3', 30),
             battleback=('IceCave', 'IceCave'))
    el = Ev().se('Move1', 60).transfer(EISFALL, 15, 6, 2, 0)
    mb.add("Out", 5, 34, [pg(el, trigger=1, priority=0)])
    p = []
    el = Ev()
    el.se('Ice6')
    el.balloon(0, 1)
    el.say(FUBUKI, ["Thieves. You came back."])
    el.say(KANTA, ["We brought it back."], 'calm')
    el.say(FUBUKI, ["Thieves always bring something back. Usually their",
                    "friends. I can smell my silver on you."])
    el.say(HANMA, ["She won't listen until she's cooled her temper on us.",
                   "Hold, my Lord. Don't try to win. Try to last."], 'command')
    el.battle(TR["Fubuki"], can_escape=False, can_lose=False)
    el.say(FUBUKI, ["…Enough. You fight like people protecting something,",
                    "not stealing it."])
    el.route(0, [(19, [])])
    el.say(FUBUKI, ["And you. You have no scent at all. Like fresh snow.",
                    "An empty vessel, walking and talking. How odd."])
    el.text(["Kanta holds out the silver bowl."])
    el.say(FUBUKI, ["My silver. Stolen by men running from the north with",
                    "ash in their hair."])
    el.say(FUBUKI, ["Do you know why I froze the river? Not for a bowl.",
                    "The north wind tastes of ash this spring. Something is",
                    "burning up there that should never burn."])
    el.say(FUBUKI, ["I wanted this valley shut. Nothing in, nothing out."])
    el.say(HANMA, ["The Wall is cracking, spirit. Everyone runs south.",
                   "Shutting one valley won't stop that."], 'stern')
    el.say(FUBUKI, ["No. It won't."])
    el.say(FUBUKI, ["Tell Eisfurt the Eis will break by morning. And you,",
                    "little vessel: go south and live, or go north and",
                    "die well. Take this, for the bowl."])
    el.se('Item3')
    el.armor(AR["Frostträne"], 1)
    el.item(IT["Silberne Opferschale"], -1)
    el.gain_exp(1, 200, True)
    el.notice(["Received the Frostträne (ice damage x1/2, MAG +8)."])
    el.quest_desc(Q_WINTER, "Fubuki has her bowl back and will let the river go. Return to Eisfurt; the Vogt owes "
                            "you a Goldkrone.")
    el.switch(S_FUBUKI)
    el.fadeout()
    el.transfer(EISFURT, 15, 21, 8, 2)
    el.fadein()
    p.append(pg(el, char=FUBUKI.char[0], index=FUBUKI.char[1], direction=2, trigger=2, priority=1))
    p.append(pg(None, sw=S_FUBUKI, priority=0))
    mb.add("Fubuki", 12, 8, p)
    mb.light('ice_dark', 0, 0, tile=False)
    mb.follow_light('beam', 5, 33)
    mb.light('ice_glow', 12, 8)
    mb.light('ice_glow', 12, 11)
    return mb
