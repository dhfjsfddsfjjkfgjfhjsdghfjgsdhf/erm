"""Chapter 3: Die Königsstraße. Wachtburg, the Adventurers' Guild, the granary vaults, the Nordstraße emergency
and Kanta's first breakthrough (rank F -> E). Optional: the Wolfsgrube trial."""
from story.common import *
from story.db import TR, IT, AR, WP, SK, CE
from story.ids import *
from story.ch1 import OKUDA, chest
from story.ch2 import UEDA, camp_fire

MIYU = npc_speaker("Hoshino Miyu", "People2", 3)
KUROGANE = npc_speaker("Kurogane Isao", "People3", 4)
KAJI_T = npc_speaker("Kaji Tōbei", "People4", 4)
CHIBA = npc_speaker("Chiba Masato", "People4", 6)
AOYAGI = npc_speaker("Aoyagi Kanon", "People2", 2)
ENOMOTO = npc_speaker("Enomoto Kōji", "People3", 7)
SHIORI = npc_speaker("Enomoto Shiori", "People4", 5)
REN = npc_speaker("Ren", "SF_People1", 0)
HAYAMI = npc_speaker("Hayami Kyōsuke", "Actor1", 6)
KURODA = npc_speaker("Kuroda Raiden", "Actor2", 4)
GUARD = npc_speaker("Torwache", "People3", 6)
RUNNER = npc_speaker("Bote", "People1", 2)
SISTER = npc_speaker("Schwester Yuzuki", "People2", 5)
HOUND_CHAR = ("Nature", 0)
WOLF_CHAR = ("Nature", 3)
HERB_TILE = 151            # Outside_B: a leafy herb

# ----------------------------------------------------------------------- quests
Q_ROAD = Quest(7, "Die Königsstraße", "Shirakawa Kaname", "Königsstraße, Wachtburg",
               "Ueda's ferry runs again. The Königsstraße leads east from the landing to Wachtburg, the royal seat. "
               "The Vogt said people like you should register with the Adventurers' Guild there.",
               "Reach Wachtburg and find the Guild.")
Q_LETTER = Quest(8, "Ein Brief für die Gilde", "Okuda Noboru", "Wachtburg",
                 "Elder Okuda's letter about the goblins, and the black raven feather from Krummzahn's tower, "
                 "belong with the Guild in Wachtburg.",
                 "Bring the letter to the Guild.")
Q_GRAIN = Quest(9, "Ratten im Kornspeicher", "Hoshino Miyu", "Wachtburg, Kornspeicher",
                "Rank F posting: the royal granary's vaults have rats, says the quartermaster, Enomoto Kōji. "
                "The rats have been opening sacks with their hands. He waits at the granary in the upper town, "
                "west of the castle stairs. Pay: 1 gk 2 sl.",
                "Clear the granary vaults.")
Q_WOLVES = Quest(10, "Wölfe an der Nordstraße", "Hoshino Miyu", "Nordstraße",
                 "Rank F posting: a wolf pack is taking goats outside the city. It dens where the Nordstraße's "
                 "dirt track runs south. Bring down the pack leader. Pay: 1 gk.",
                 "Find the pack on the Nordstraße's south track.")
Q_HERBS = Quest(11, "Heilwurz für das Lazarett", "Hoshino Miyu", "Königsstraße, Nordstraße",
                "Rank F posting: the field hospital needs five bunches of Heilwurz, a broad-leafed herb that grows "
                "along the roads. Pay: 8 sl.",
                "Heilwurz: \\V[%d] of 5")
Q_EMERG = Quest(12, "Notruf: Die Nordstraße", "Kurogane Isao", "Nordstraße",
                "EMERGENCY. A refugee column on the Nordstraße is under attack by ash hounds. Every registered "
                "blade answers the call.",
                "Hurry to the Nordstraße!")
Q_TRIAL = Quest(13, "Die Wolfsgrube", "Kurogane Isao", "Wachtburg, Wolfsgrube",
                "The Sondertafel's rank E trial: three Dire Wolves in the Wolfsgrube behind the Guild, under the "
                "branch master's eye. Recommended level 15. Optional; the first clear earns the title Wolfsbann and "
                "the Wachtfeuer-Amulett.",
                "Ask Kurogane at the Guild when you're ready.")
Q_WALL = Quest(14, "Die Wacht", "Kurogane Isao", "Nordstraße, Wallstraße, Nordwall",
               "Frontposten 3 on the Nordwall lost half its squad in a week. The Guild sends every E rank it has. "
               "Report to the wall captain, Mori Daisuke. The Nordstraße leads north to the Wallstraße and the Wall.",
               "Go north: Nordstraße, then the Wallstraße.")

# ----------------------------------------------------------------------- switches / variables
S_C3 = SW('C3: Across the River')
S_WB = SW('C3: In Wachtburg')
S_REG = SW('C3: Registered')
S_LETTER = SW('C3: Letter Delivered')
S_GRAIN = SW('C3: Granary Job')
S_GRAIN_DONE = SW('C3: Granary Cleared')
S_GRAIN_PAID = SW('C3: Granary Paid')
S_WOLVES = SW('C3: Wolf Job')
S_WOLVES_DONE = SW('C3: Pack Down')
S_WOLVES_PAID = SW('C3: Wolves Paid')
S_HERBS = SW('C3: Herb Job')
S_HERBS_PAID = SW('C3: Herbs Paid')
S_EMERG = SW('C3: Emergency')
S_EMERG_DONE = SW('C3: Emergency Done')
S_CALL = SW('C3: Called to the Wall')
S_TRIAL_DONE = SW('C3: Wolfsgrube Cleared')
S_REFIT = SW('C3: Armor Refitted')
V_JOBS = VAR('Guild Jobs Done')
V_HERBS = VAR('Heilwurz')
Q_HERBS.track = Q_HERBS.track % V_HERBS


def build():
    return [koenigsstrasse(), wachtburg(), gilde(), wachtfeuer(), kaji(), ausruester(), kornspeicher(),
            nordstrasse(), wolfsgrube()]


def herb(mb, x, y):
    """A bunch of Heilwurz by the road (counts for the herb job)."""
    el = Ev()
    el.se('Item1')
    el.item(IT["Heilwurz"], 1)
    el.var(V_HERBS, 1, '+')
    el.if_switch(S_HERBS, True,
                 lambda b: b.notice(["Picked Heilwurz. (\\V[%d] of 5)" % V_HERBS]),
                 lambda b: b.notice(["Picked a bunch of Heilwurz, a broad-leafed wound herb.",
                                     "Someone in Wachtburg will want it."]))
    el.self_switch('A')
    p1 = pg(el, trigger=0, priority=1)
    p1['image']['tileId'] = HERB_TILE
    p2 = pg(None, self_sw='A', priority=0)
    return mb.add("Heilwurz", x, y, [p1, p2])


def guard_line(e, lines):
    e.say(GUARD, lines)


# ---------------------------------------------------------------------------
# 40  Königsstraße  (sample 283)
# ---------------------------------------------------------------------------
ROAD_ENC = lambda: [(TR["Harpyien x2"], 7, ()), (TR["Kragenechse"], 6, ()), (TR["Wegelagerer x2"], 5, ()),
                    (TR["Harpyie & Kragenechse"], 5, ()), (TR["Wegelagerer & Harpyie"], 4, ())]


def koenigsstrasse():
    mb = MapBuild(KOENIGSSTRASSE, NAMES[KOENIGSSTRASSE], 283, display=NAMES[KOENIGSSTRASSE])
    mb.props(note="<Rank: F>\n<Area Name: Königsstraße>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field1', 65), battleback=('Grassland', 'Forest'), encounters=ROAD_ENC(), steps=30)
    # arrival from the ferry
    el = Ev()
    el.wait(10)
    el.say(HANMA, ["The Königsstraße. The king's road, and the king's",
                   "tolls, no doubt. Four days to Wachtburg, Ueda said."], 'calm')
    el.say(KANTA, ["And the Guild."], 'calm')
    el.say(HANMA, ["And the Guild. Register, take their coin, don't tell",
                   "them more than they ask. People notice a soul that",
                   "comes back from the dead, my Lord. Kings especially."], 'stern')
    el.say(KANTA, ["…I'll keep my head down."], 'wry')
    el.say(HANMA, ["You'll try."], 'smile')
    el.quest_new(Q_ROAD)
    el.if_item(IT["Brief an die Gilde"], lambda b: b.quest_new(Q_LETTER))
    el.switch(S_C3)
    mb.autorun("Arrival", el)
    # the ferry landing (south)
    el = Ev()
    el.text(["Ueda's ferry bobs at the landing. He waves from the",
             "stern: back across to Eisfurt?"])
    def back(e):
        e.se('Water3')
        e.fadeout()
        e.transfer(EISFURT, 21, 23, 4, 2)
        e.fadein()
    el.choices(["Cross back to Eisfurt", "Stay"], [back, lambda e: e.route(-1, [(4, [])], skippable=True)], cancel=1)
    mb.add("Ferry Landing", 21, 28, [pg(el, trigger=1, priority=0)])
    # north: the road climbs to Wachtburg
    for x in (6, 7, 8):
        el = Ev().se('Move1', 60).transfer(WACHTBURG, 24, 47, 8, 0)
        mb.add("To Wachtburg", x, 3, [pg(el, trigger=1, priority=0)])
    # the refugee camp by the road
    camp_fire(mb, 17, 19, KOENIGSSTRASSE, 17, 20, 8,
              ["A roadside fire pit, still warm. Refugees have been", "sleeping here, a family at a time."])
    el = Ev()
    el.say(SHIORI, ["You're going to Wachtburg? So are we. Everybody is."])
    el.say(SHIORI, ["We're from Kaltenbrunn, under the Wall. We left when",
                    "the hounds came: grey dogs with ash in their coats,",
                    "eyes like coals. The soldiers said the Wall would hold."])
    el.say(SHIORI, ["It held. The hounds came round it."])
    el.say(HANMA, ["Round it. Then the Wall has holes."], 'stern')
    p = [pg(el, char=SHIORI.char[0], index=SHIORI.char[1], direction=2, priority=1),
         pg(Ev().say(SHIORI, ["Thank the Guild for us, if you're with them. They", "brought the last column in."]),
            sw=S_EMERG_DONE, char=SHIORI.char[0], index=SHIORI.char[1], direction=2, priority=1)]
    mb.add("Enomoto Shiori", 16, 18, p)
    el = Ev()
    el.say(REN, ["Mama says the Guild in Wachtburg pays for Heilwurz.",
                 "It's the big leaf, like a hand. I found some by the",
                 "water! You can have it. I can't carry it anyway."])
    mb.npc("Ren", 18, 18, REN, el, direction=2, move_type=1)
    # herbs, chests
    herb(mb, 11, 19)
    herb(mb, 23, 12)
    herb(mb, 10, 7)
    chest(mb, "Chest", 9, 20, lambda e: (e.item(IT["Heiltrank"], 3), e.gold(40)),
          "Found 3 Heiltrank and \\MONEY[40].")
    chest(mb, "Chest", 19, 11, lambda e: e.item(IT["Manatrank"], 2), "Found 2 Manatrank.")
    return mb


# ---------------------------------------------------------------------------
# 41  Wachtburg  (sample 143)
# ---------------------------------------------------------------------------
def wachtburg():
    mb = MapBuild(WACHTBURG, NAMES[WACHTBURG], 143, display=NAMES[WACHTBURG])
    mb.props(note="<Area Name: Wachtburg>\n<No Rank HUD>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Town5', 65), bgs=('People1', 25))
    # arrival
    el = Ev()
    el.add_time(hours=80)
    el.set_time(16, 0)
    el.wait(20)
    el.narrate(["Four days on the road. Then walls: red stone, higher",
                "than the Rabenau church tower, and behind them the",
                "castle of the kings of Hohenwacht."])
    el.narrate(["Wachtburg, the royal seat. The gate is choked with carts",
                "and people carrying everything they own."])
    el.say(GUARD, ["Next! Name, business. Refugees to the camp by the east",
                   "wall, the Crown feeds you twice a day. Merchants pay",
                   "the toll. Soldiers report to the castle."])
    el.say(KANTA, ["We're looking for the Adventurers' Guild."], 'calm')
    el.say(GUARD, ["Guild's on the market square, east side, the big house",
                   "with the blue shield over the door. Can't miss it."])
    el.say(GUARD, ["…Unregistered? Then you're refugees, as far as the",
                   "Crown's concerned. Register before you start trouble."])
    el.say(HANMA, ["The whole north is walking south, my Lord. Look at",
                   "them."], 'calm')
    el.quest_desc(Q_ROAD, "Wachtburg. The Adventurers' Guild is on the market square, east side: the big house "
                          "with the blue shield over the door.")
    el.switch(S_WB)
    mb.autorun("Arrival", el)

    # ------------------------------------------------ gates and doors
    def gate(e):
        def south(b):
            b.se('Move1', 60)
            b.transfer(KOENIGSSTRASSE, 7, 4, 2, 0)
        def north(b):
            b.se('Move1', 60)
            b.transfer(NORDSTRASSE, 3, 13, 6, 0)
        def stay(b):
            b.route(-1, [(4, [])], wait=True, skippable=True)
        e.if_switch(S_REG, True,
                    lambda b: b.choices(["Nordstraße (north)", "Königsstraße (to Eisfurt)", "Stay"],
                                        [north, south, stay], cancel=2),
                    lambda b: b.choices(["Königsstraße (to Eisfurt)", "Stay"], [south, stay], cancel=1))
    for x in (23, 24, 25):
        el = Ev()
        gate(el)
        mb.add("South Gate", x, 49, [pg(el, trigger=1, priority=0)])
    mb.door(17, 39, WACHTFEUER, 15, 11, 4, index=4, name="Door: Zum Wachtfeuer")
    mb.door(30, 39, GILDE, 12, 15, 8, name="Door: Gildenhaus")
    mb.door(37, 37, KAJI, 14, 12, 8, name="Door: Schmiede")
    mb.door(9, 40, AUSRUESTER, 8, 14, 8, name="Door: Ausrüster")
    # the granary (upper town, west): opens with the job
    el = Ev().text(["The royal granary. Locked, and guarded by a",
                    "quartermaster who looks like he hasn't slept."])
    mb.add("Door: Kornspeicher", 11, 23,
           [pg(el, char='!Door1', index=0, direction=2, trigger=0, priority=1, walk_anime=False),
            pg(Ev().se('Open1').route(0, DOOR_ROUTE).route(-1, [12], skippable=True).se('Move1', 60)
               .transfer(KORNSPEICHER, 8, 5, 2, 0), sw=S_GRAIN, char='!Door1', index=0, direction=2, trigger=1,
               priority=1, walk_anime=False)])
    mb.door(14, 23, 0, 0, 0, locked_text=["The royal armory. Soldiers only."], name="Door: Zeughaus")
    mb.door(35, 23, 0, 0, 0, index=4, locked_text=["A barracks. Snoring, and a sergeant shouting at the",
                                                   "snoring."], name="Door: Kaserne")
    mb.door(21, 24, 0, 0, 0, index=4, locked_text=["A townhouse. The door has a red cloth nailed to it,",
                                                   "to keep out bad luck."], name="Door: Haus")
    mb.door(38, 12, 0, 0, 0, locked_text=["The court mage's tower annex. A brass plate:",
                                          "\"Yoshino. By appointment. No exceptions.\""], name="Door: Yoshino")
    mb.door(4, 12, 0, 0, 0, locked_text=["A storehouse. Locked."], name="Door: Lager")
    # the castle
    el = Ev().text(["The great doors of the royal castle, shut. Iron bands,",
                    "and the red lion of Hohenwacht."])
    for x in (23, 24, 25):
        mb.add("Castle Doors", x, 12, [pg(el, trigger=0, priority=1)])
    castle_guard = Ev().say(GUARD, ["The king receives no one without a summons. The",
                                    "princess neither, before you ask. Everyone asks."])
    mb.npc("Castle Guard", 23, 14, GUARD, castle_guard, direction=2)
    mb.npc("Castle Guard", 25, 14, GUARD, castle_guard, direction=2)

    # ------------------------------------------------ people
    el = Ev().if_switch(S_REG, True,
                        lambda b: b.say(GUARD, ["Registered now? Then welcome to Wachtburg properly.",
                                                "Mind the refugees. They've had enough trouble."]),
                        lambda b: b.say(GUARD, ["Guild's on the market square, east side. The big",
                                                "house with the blue shield."]))
    mb.npc("Gate Guard", 22, 42, GUARD, el, direction=2)
    mb.npc("Gate Guard", 26, 42, GUARD, el, direction=2)
    el = Ev()
    el.if_switch(S_GRAIN, True,
                 lambda b: b.if_switch(S_GRAIN_DONE, True,
                                       lambda c: c.say(ENOMOTO, ["Quiet down there. Quiet! I could kiss you. I won't.",
                                                                 "The Guild will pay you. I just count sacks."]),
                                       lambda c: c.say(ENOMOTO, ["The door's open. Go down, and please, whatever's down",
                                                                 "there, make it stop eating the Crown's grain."])),
                 lambda b: b.say(ENOMOTO, ["Enomoto, royal quartermaster. Something in the vaults",
                                           "is eating the grain faster than the refugees can.",
                                           "I've posted it at the Guild. Nobody's come."]))
    mb.npc("Enomoto Kōji", 12, 24, ENOMOTO, el, direction=2)
    el = Ev()
    el.say(SISTER, ["The Dawn be with you. I serve the Kirche der Morgenröte.",
                    "The Archpriestess says the Hero of Dawn walks among us",
                    "already, and doesn't know it yet."])
    el.say(SISTER, ["Light is rare this far north. If you meet someone who",
                    "carries it, send them to the Church, would you?"])
    el.say(HANMA, ["…"], 'stern')
    mb.npc("Schwester Yuzuki", 20, 33, SISTER, el, direction=2)
    old = npc_speaker("Old Refugee", "People1", 6)
    el = Ev().say(old, ["Forty years I farmed under the Wall. Forty years, and",
                        "I never once saw the other side of it. Now I'll die",
                        "on this side. There's a joke in that somewhere."])
    mb.npc("Old Refugee", 40, 41, old, el, direction=4)
    kid = npc_speaker("Refugee Child", "SF_People1", 1)
    el = Ev().say(kid, ["The soldiers give us bread twice a day! Twice!"])
    mb.npc("Refugee Child", 29, 34, kid, el, direction=2, move_type=1)
    soldier = npc_speaker("Soldier on Leave", "People3", 6)
    el = Ev()
    el.say(soldier, ["Frontposten 3, back from the Wall for a week. I'm going",
                     "to sleep for six days and drink for one."])
    el.say(soldier, ["There's a woman up there made of iron, you know. Holds",
                     "the breach every night, alone. They call her die",
                     "Eiserne. Never seen her face. Nobody has."])
    mb.npc("Soldier on Leave", 33, 41, soldier, el, direction=4)
    noble = npc_speaker("Noblewoman", "People3", 3)
    el = Ev().say(noble, ["The Crown is feeding every mouth that walks through",
                          "the gate, and the Empire sends us speeches instead of",
                          "soldiers. Sonnenthal can choke on its speeches."])
    mb.npc("Noblewoman", 15, 31, noble, el, direction=2)
    # lamps
    for x, y in [(16, 38), (18, 38), (21, 23), (35, 22), (36, 36), (38, 36), (19, 11), (29, 11), (39, 11), (10, 12)]:
        mb.light('torch', x, y)
    return mb


# ---------------------------------------------------------------------------
# 42  Gildenhaus Wachtburg  (sample 169)
# ---------------------------------------------------------------------------
def gilde():
    mb = MapBuild(GILDE, NAMES[GILDE], 169, display=NAMES[GILDE])
    mb.props(note="<Area Name: Gildenhaus Wachtburg>\n<No Rank HUD>", bgm=('Town7', 60), bgs=('People2', 20))
    el = Ev().se('Move1', 60).transfer(WACHTBURG, 30, 40, 2, 0)
    mb.add("Exit", 12, 16, [pg(el, trigger=1, priority=0)])
    stairs = Ev().text(["Stairs to the offices. A clerk looks up from her",
                        "ledger: \"Branch business only, please.\""])
    mb.add("Stairs", 8, 5, [pg(stairs, trigger=0, priority=1)])
    mb.add("Stairs", 16, 5, [pg(stairs, trigger=0, priority=1)])

    # ------------------------------------------------ registration (Miyu, first talk)
    def do_register(e):
        e.say(MIYU, ["Registration is one Goldkrone. It buys your card, the",
                     "board, and the Guild's name behind you. Also the",
                     "Guild's name in front of you, when things go wrong."])
        def pay(b):
            b.gold(-100)
            b.se('Coin')
            b.say(MIYU, ["Thank you! Name?"])
            b.say(KANTA, ["Kanta."], 'calm')
            b.say(MIYU, ["Family name?"])
            b.say(KANTA, ["…Just Kanta."], 'calm')
            b.say(MIYU, ["Origin?"])
            b.choices(["\"Rabenau.\"", "\"A cave in the Kiefernkamm.\""],
                      [lambda c: c.say(MIYU, ["Rabenau. Lovely! Goats, isn't it? Or pigs."]),
                       lambda c: (c.say(MIYU, ["A…cave. Right. I'll put \"Hohenwacht\"."]),
                                  c.say(HANMA, ["Honesty. How refreshing."], 'smile'))], cancel=-1)
            b.say(MIYU, ["And your affinity? The kind of mana you lean toward."])
            b.say(KANTA, ["Light."], 'calm')
            b.say(MIYU, ["Light? That's rare up here. The Church will want to",
                         "meet you. Don't let them talk you into a robe."])
            b.say(MIYU, ["Now the oath. Hand on the scales, please."])
            b.se('Chime2')
            b.narrate(["A little brass balance sits on the counter: Sabaki's",
                       "scales, the god who weighs oaths. Kanta lays her",
                       "palm on the empty pan."])
            b.say(MIYU, ["Repeat after me: I will honor every contract. I will",
                         "raise no blade in the wars of crowns. I will answer",
                         "the call against demons."])
            b.say(KANTA, ["I will honor every contract. I will raise no blade in",
                          "the wars of crowns. I will answer the call against",
                          "demons."], 'calm')
            b.narrate(["The scales don't move. Somewhere, very far away,",
                       "something takes note."])
            b.say(MIYU, ["And last, the appraisal. Hand on the Wahrheitskristall,",
                         "please. It reads your rank from your mana. It doesn't",
                         "hurt. Mostly."])
            b.se('Magic4')
            b.flash((170, 210, 255, 150), 30)
            b.narrate(["The crystal on its stand glows pale blue under Kanta's",
                       "hand, and letters of light crawl across its face."])
            b.say(MIYU, ["Rank F. Magic rank F. Welcome to the bottom of the",
                         "ladder, everyone starts there. …Huh."])
            b.balloon(0, 2)
            b.say(MIYU, ["That's odd. The imprint's empty."])
            b.say(KANTA, ["Empty?"], 'wry')
            b.say(MIYU, ["Everyone's crystal-read has history in it. The years",
                         "you've lived, the mana you've spent, every kill. Yours",
                         "says you're… sixteen days old?"])
            b.say(MIYU, ["Sixteen days, a goblin chief, a lot of wolves and a",
                         "very large ice serpent. Nothing before that. At all."])
            b.say(HANMA, ["My turn, then."], 'calm')
            b.se('Magic4', 70, 60)
            b.narrate(["Hanma lays a gloved hand on the crystal.", "Nothing happens. The crystal doesn't even flicker."])
            b.say(MIYU, ["It… doesn't see you. That's not possible. It sees",
                         "everything that has mana. Even goats."])
            b.say(KUROGANE, ["It's possible, Hoshino. A dead hand leaves no",
                             "imprint."])
            b.switch(SW('C3: Kurogane Down'))
            b.say(KUROGANE, ["Kurogane Isao. I run this branch."])
            b.say(KUROGANE, ["A bound spirit. I've seen one before. Once, on the",
                             "Wall. It didn't end well for the man who carried it."])
            b.say(KUROGANE, ["Is she yours?"])
            b.say(KANTA, ["…She's with me."], 'calm')
            b.say(HANMA, ["Her officer. Hanma."], 'stern')
            b.say(KUROGANE, ["Then she fights under your card. Contracted spirits",
                             "do. Register the pair, Hoshino. And a sixteen-day-old",
                             "imprint is nobody's business but the Guild's."])
            b.say(MIYU, ["Yes, Branch Master. …Last thing! Parties register under",
                         "a name. German, by custom. The Silbernen Falken, the",
                         "Blutmond, that kind of thing. What's yours?"])
            b.add(303, [4, 12])
            b.say(MIYU, ["\"\\N[4]\". Lovely. And here's your card!"])
            b.se('Item3')
            b.item(IT["Gildenkarte"], 1)
            b.add(324, [1, "Neuling"])
            b.notice(["Received the \\C[6]Gildenkarte\\C[0]. Kanta: guild rank F, title",
                      "\\C[6]Neuling\\C[0] (newcomer). Postings are at the counter."])
            b.quest_done(Q_ROAD)
            b.switch(S_REG)
            # the letter and the feather
            def deliver(c):
                c.say(KANTA, ["We carry a letter for the Guild. From Rabenau."], 'calm')
                c.say(KUROGANE, ["Rabenau."])
                c.text(["Kurogane reads Elder Okuda's letter twice. Then Kanta",
                        "holds out the black raven feather."])
                c.say(KUROGANE, ["Goblins driven south out of the Rabenholz. And this."])
                c.say(KUROGANE, ["Miasma. Demon mana, in a raven's feather, a hundred",
                                 "miles south of the Wall. Goblins don't run from a",
                                 "little ash. They ran from something."])
                c.say(KUROGANE, ["Your card shows a goblin chief. Krummzahn. There's a",
                                 "bounty on him: one Goldkrone five. The kill-log can't",
                                 "be forged, so it's yours."])
                c.se('Coin')
                c.gold(150)
                c.item(IT["Brief an die Gilde"], -1)
                c.item(IT["Schwarze Rabenfeder"], -1)
                c.notice(["Received \\MONEY[150] (bounty: Krummzahn)."])
                c.quest_done(Q_LETTER)
                c.switch(S_LETTER)
            b.if_item(IT["Brief an die Gilde"], deliver)
            b.say(KUROGANE, ["Take work from the board, Neuling. Rank F work. Come",
                             "back alive, and we'll talk about rank E."])
        def later(b):
            b.say(MIYU, ["Come back with a Goldkrone, then! The board will still",
                         "be here. Sadly."])
        e.if_gold(100, '>=',
                  lambda b: b.choices(["Pay 1 gk", "Not now"], [pay, later], cancel=1),
                  lambda b: (b.say(MIYU, ["…Ah. That's short of a Goldkrone. The monsters on the",
                                          "Königsstraße carry coin sometimes. Grim, but true."])))

    # ------------------------------------------------ postings and reports (Miyu, registered)
    def report(e):
        def grain(b):
            b.say(MIYU, ["The granary's quiet? Enomoto sent a boy running to",
                         "say so. He was crying. The boy, not Enomoto. Well."])
            b.gold(120)
            b.se('Coin')
            b.notice(["Received \\MONEY[120]."])
            b.quest_done(Q_GRAIN)
            b.switch(S_GRAIN_PAID)
            b.var(V_JOBS, 1, '+')
        e.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_GRAIN_DONE, S_GRAIN_PAID), grain)
        def wolves(b):
            b.say(MIYU, ["The pack leader's in your kill-log, so that's that.",
                         "The goatherds will sleep tonight."])
            b.gold(100)
            b.se('Coin')
            b.notice(["Received \\MONEY[100]."])
            b.quest_done(Q_WOLVES)
            b.switch(S_WOLVES_PAID)
            b.var(V_JOBS, 1, '+')
        e.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d)" % (S_WOLVES_DONE, S_WOLVES_PAID), wolves)
        def herbs(b):
            b.say(MIYU, ["Five bunches of Heilwurz! The Lazarett will be so",
                         "happy. Well. As happy as a field hospital gets."])
            b.script("$gameParty.loseItem($dataItems[%d], 99);" % IT["Heilwurz"])
            b.gold(80)
            b.se('Coin')
            b.notice(["Received \\MONEY[80]."])
            b.quest_done(Q_HERBS)
            b.switch(S_HERBS_PAID)
            b.var(V_JOBS, 1, '+')
        e.if_script("$gameSwitches.value(%d) && !$gameSwitches.value(%d) && $gameVariables.value(%d) >= 5"
                    % (S_HERBS, S_HERBS_PAID, V_HERBS), herbs)

    def board(e):
        def take_grain(b):
            b.if_switch(S_GRAIN, True,
                        lambda c: c.say(MIYU, ["You've got that one. The granary is in the upper town,",
                                               "west of the castle stairs. Enomoto's waiting."]),
                        lambda c: (c.say(MIYU, ["\"Rats in the royal granary.\" Enomoto, the quartermaster,",
                                                "says they're rats. He also says they open the sacks",
                                                "with their hands, so. One Goldkrone two."]),
                                   c.quest_new(Q_GRAIN), c.switch(S_GRAIN)))
        def take_wolves(b):
            b.if_switch(S_WOLVES, True,
                        lambda c: c.say(MIYU, ["The pack dens where the Nordstraße's dirt track runs",
                                               "south. Out the south gate, then north around the wall."]),
                        lambda c: (c.say(MIYU, ["\"Wolves on the Nordstraße.\" A pack is taking goats.",
                                                "Bring down the leader and the rest will scatter. One",
                                                "Goldkrone."]),
                                   c.quest_new(Q_WOLVES), c.switch(S_WOLVES)))
        def take_herbs(b):
            b.if_switch(S_HERBS, True,
                        lambda c: c.say(MIYU, ["Five bunches of Heilwurz for the Lazarett. You have",
                                               "\\V[%d]. It grows along the roads." % V_HERBS]),
                        lambda c: (c.say(MIYU, ["\"Heilwurz for the Lazarett.\" Five bunches. It grows",
                                                "by the roads: a broad leaf, like a hand. Eight Silber."]),
                                   c.quest_new(Q_HERBS), c.switch(S_HERBS)))
        e.say(MIYU, ["Rank F postings. Take as many as you like: we have more",
                     "work than hands."])
        e.choices(["Ratten im Kornspeicher", "Wölfe an der Nordstraße", "Heilwurz für das Lazarett", "Back"],
                  [take_grain, take_wolves, take_herbs, None], cancel=3)

    def guild_talk(e):
        e.say(MIYU, ["Guild ranks go F to S. Postings go up to your rank plus",
                     "one. The kill-log on your card records every kill by",
                     "mana imprint, so no claiming other people's wolves."])
        e.say(MIYU, ["And the Sondertafel over there is for trials and special",
                     "commissions. Rank E and up. Someday!"])

    talk = Ev()
    report(talk)
    talk.if_switch(S_EMERG, True,
                   lambda b: b.if_switch(S_EMERG_DONE, False,
                                         lambda c: (c.say(MIYU, ["The Nordstraße! Go, go, go!"]), c.exit_event())))
    talk.say(MIYU, ["What can the Guild do for you?"])
    talk.choices(["Postings", "About the Guild", "Nothing"], [board, guild_talk, None], cancel=2)

    p = [pg(Ev().say(MIYU, ["Welcome to the Adventurers' Guild!"]).choices(
        ["Register", "Just looking"], [do_register, lambda b: b.say(MIYU, ["Take your time! The board's not going anywhere."])],
        cancel=1), char=MIYU.char[0], index=MIYU.char[1], direction=2, priority=1),
         pg(talk, sw=S_REG, char=MIYU.char[0], index=MIYU.char[1], direction=2, priority=1)]
    mb.add("Hoshino Miyu", 12, 7, p)

    # ------------------------------------------------ Kurogane (after he comes down)
    s_down = SW('C3: Kurogane Down')
    k = []
    k.append(pg(None, priority=0))
    el = Ev()
    el.say(KUROGANE, ["Rank F work first, Neuling. The board's at the",
                      "counter. Come back alive."])
    k.append(pg(el, sw=s_down, char=KUROGANE.char[0], index=KUROGANE.char[1], direction=2, priority=1))
    el = Ev()
    def trial(e):
        e.say(KUROGANE, ["The Wolfsgrube. Three Dire Wolves we raise for the",
                         "Wall, loose in the pit, and you in it. Recommended for",
                         "rank E at level fifteen."])
        def go(b):
            b.say(KUROGANE, ["Follow me."])
            b.fadeout()
            b.transfer(WOLFSGRUBE, 12, 15, 8, 2)
            b.fadein()
        b_later = lambda b: b.say(KUROGANE, ["Wise. The wolves will wait. They're good at it."])
        e.choices(["Enter the Wolfsgrube", "Not yet"], [go, b_later], cancel=1)
    def wall(e):
        e.say(KUROGANE, ["Frontposten 3. Captain Mori Daisuke. North on the",
                         "Nordstraße, two days on the Wallstraße. Go when",
                         "you're ready, but don't dawdle."])
    el.say(KUROGANE, ["Rank E. You're a strange one, Kanta."])
    el.if_switch(S_TRIAL_DONE, True,
                 lambda b: b.choices(["The Wall", "Nothing"], [wall, None], cancel=1),
                 lambda b: b.choices(["The Wall", "The Wolfsgrube (trial)", "Nothing"], [wall, trial, None], cancel=2))
    k.append(pg(el, sw=S_CALL, char=KUROGANE.char[0], index=KUROGANE.char[1], direction=2, priority=1))
    mb.add("Kurogane Isao", 15, 9, k)

    # ------------------------------------------------ boards
    el = Ev()
    el.text(["The Anschlagtafel. Postings three deep: escorts to",
             "Kreuzweg, a bounty on a troll near Eisenberg, and a",
             "dozen for the Wall. Most of them are rank D or better."])
    el.if_switch(S_REG, True, lambda b: b.text(["Rank F postings are handled at the counter."]),
                 lambda b: b.text(["Unregistered adventurers can't take postings."]))
    board_p = pg(el, trigger=0, priority=1)
    board_p['image']['tileId'] = 91            # Inside_B: a posted notice
    mb.add("Anschlagtafel", 5, 4, [board_p])
    el = Ev()
    el.text(["The Sondertafel: trials and special commissions,",
             "rank E and up."])
    el.if_switch(S_CALL, True,
                 lambda b: b.if_switch(S_TRIAL_DONE, True,
                                       lambda c: c.text(["\"WOLFSGRUBE (rank E): cleared by \\N[4].\"",
                                                         "Someone has drawn a little wolf next to it."]),
                                       lambda c: c.text(["\"WOLFSGRUBE (rank E). Three Dire Wolves. Ask the",
                                                         "branch master.\""])),
                 lambda b: b.text(["Your card's rank F. The Sondertafel isn't for you yet."]))
    board_p = pg(el, trigger=0, priority=1)
    board_p['image']['tileId'] = 91
    mb.add("Sondertafel", 19, 4, [board_p])

    # ------------------------------------------------ adventurers, the buyback counter
    el = Ev()
    el.say(HAYAMI, ["Hayami Kyōsuke, the Silbernen Falken. We're rank B,",
                    "on our way north from Kreuzweg. The Wall's paying",
                    "triple and asking for anyone who can hold a sword."])
    el.say(HAYAMI, ["Neuling, hm? Everyone was. Don't die for the first",
                    "posting you take. That's all the advice there is."])
    mb.npc("Hayami Kyōsuke", 5, 9, HAYAMI, el, direction=6)
    el = Ev()
    el.say(KURODA, ["Kuroda Raiden. Blutmond. You'll have heard of us."])
    el.say(KANTA, ["No."], 'calm')
    el.say(KURODA, ["You will. Word of advice, Neuling: the kill-log",
                    "records who struck the last blow, not who did the",
                    "work. Remember that when your wolf's half dead."])
    el.say(HANMA, ["A kill-thief. Charming."], 'stern')
    mb.npc("Kuroda Raiden", 19, 9, KURODA, el, direction=4)
    clerk = npc_speaker("Materialankauf", "People1", 4)
    el = Ev()
    el.say(clerk, ["Material buyback. The Guild buys Manasteine, pelts and",
                   "such at fair prices. Fair to the Guild, anyway."])
    el.shop([('item', IT["Heiltrank"]), ('item', IT["Manatrank"]), ('item', IT["Riechsalz"])])
    mb.npc("Materialankauf", 18, 13, clerk, el, direction=2)

    # ------------------------------------------------ the emergency call (2 jobs done)
    el = Ev()
    el.wait(20)
    el.se('Bell1', 90)
    el.wait(20)
    el.se('Bell1', 90)
    el.shake(2, 6, 20)
    el.text(["The Guild's bell. Heads come up all over the hall."])
    el.say(RUNNER, ["Notruf! Emergency! A refugee column on the Nordstraße,",
                    "an hour out! Hounds, ash hounds, a whole pack of them,",
                    "and the escort's down!"])
    el.switch(s_down)
    el.say(KUROGANE, ["Every registered blade to the Nordstraße. Now. Rank",
                      "doesn't matter. Hoshino, the bell. Keep ringing."])
    el.say(KUROGANE, ["You too, Neuling. This is the oath you swore:",
                      "the call against demons."])
    el.say(KANTA, ["We're going."], 'fierce')
    el.quest_new(Q_EMERG)
    el.switch(S_EMERG)
    el.self_switch('A')
    el.fadeout()
    el.transfer(NORDSTRASSE, 3, 13, 6, 2)
    el.fadein()
    p1 = pg(el, trigger=3, priority=0, var=(V_JOBS, 2))
    mb.add("Emergency", 0, 0, [p1, pg(None, self_sw='A', priority=0)])

    # ------------------------------------------------ after the emergency: rank E
    el = Ev()
    el.wait(20)
    el.say(KUROGANE, ["Hand on the crystal, Kanta."])
    el.se('Magic4')
    el.flash((170, 210, 255, 200), 40)
    el.narrate(["The Wahrheitskristall flares so bright the whole hall", "turns to look."])
    el.say(MIYU, ["Rank… E. Magic rank E. Branch Master, it was F four",
                  "days ago! People don't jump a rank in four days!"])
    el.say(KUROGANE, ["People do, Hoshino. In a fight they shouldn't have",
                      "survived, for somebody else. I've seen it twice in",
                      "thirty years."])
    el.say(KUROGANE, ["Emergency pay, doubled: three Goldkronen. And the",
                      "Guild's thanks, which are worth less."])
    el.se('Coin')
    el.gold(300)
    el.notice(["Received \\MONEY[300]. Guild rank E: the Sondertafel is open."])
    el.say(KUROGANE, ["Now the part you won't like. Frontposten 3 on the",
                      "Nordwall lost half its squad in a week. The Wall asks",
                      "for every E rank I have. I have you."])
    el.say(HANMA, ["The Wall. Where the hounds came from."], 'stern')
    el.say(KUROGANE, ["Where everything comes from. Captain Mori Daisuke.",
                      "Nordstraße north, then the Wallstraße. Two days."])
    el.say(KUROGANE, ["And if you want to prove that crystal right first, the",
                      "Wolfsgrube is behind this hall. Ask me."])
    el.quest_new(Q_WALL)
    el.quest_new(Q_TRIAL)
    el.switch(S_CALL)
    mb.autorun("Rank E", el, cond_switch=S_EMERG_DONE, x=1, y=0)

    for x, y in [(11, 8), (7, 3), (17, 3)]:
        mb.light('torch', x, y)
    return mb


# ---------------------------------------------------------------------------
# 43  Zum Wachtfeuer  (sample 157)
# ---------------------------------------------------------------------------
def wachtfeuer():
    mb = MapBuild(WACHTFEUER, NAMES[WACHTFEUER], 157, display=NAMES[WACHTFEUER])
    mb.props(note="<Area Name: Zum Wachtfeuer>\n<No Rank HUD>", bgm=('Town2', 60), bgs=('Fire1', 30))
    for y in (11, 12):
        el = Ev().se('Move1', 60).transfer(WACHTBURG, 17, 40, 2, 0)
        mb.add("Exit", 16, y, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(CHIBA, ["Zum Wachtfeuer. Beds for thirty kupferling, soup for",
                   "free if you don't complain about it."])
    def rest(e):
        e.if_gold(30, '>=',
                  lambda b: (b.gold(-30), b.say(CHIBA, ["Room's up the back. Sleep well."]), b.common(CE["Inn Sleep"])),
                  lambda b: b.say(CHIBA, ["Thirty kupferling. I'm not the Crown, I can't feed",
                                          "the whole north for free."]))
    el.choices(["Rest (\\MONEY[30])", "Not now"], [rest, None], cancel=1)
    mb.add("Chiba Masato", 7, 12, [pg(el, char=CHIBA.char[0], index=CHIBA.char[1], direction=2, priority=1)])
    bard = npc_speaker("Bard", "Actor1", 5)
    el = Ev()
    el.say(bard, ["♪ Oh the Morgenwacht rode north in the snow, and none",
                  "of them ever came home… ♪"])
    el.say(bard, ["Old song. Twelve years old. They were the best party",
                  "the Guild ever had, and the Demon Lord ate them for",
                  "breakfast. Sad songs pay better."])
    mb.npc("Bard", 10, 13, bard, el, direction=2)
    soldier = npc_speaker("Wall Soldier", "People3", 7)
    el = Ev()
    el.say(soldier, ["Weißenfels fell six years ago. Our fortress, the",
                     "biggest on the Wall. Now it's a hole, and the hole",
                     "is where everything comes through."])
    el.say(soldier, ["Frontposten 3 sits right on top of the worst of it.",
                     "Poor bastards."])
    mb.npc("Wall Soldier", 4, 15, soldier, el, direction=6)
    cook = npc_speaker("Cook", "People2", 7)
    el = Ev().say(cook, ["Out of my kitchen unless you're peeling something."])
    mb.npc("Cook", 11, 5, cook, el, direction=2)
    mb.light('hearth', 12, 3)
    mb.light('torch', 6, 9)
    return mb


# ---------------------------------------------------------------------------
# 44  Königliche Schmiede  (sample 138): Kaji Tōbei
# ---------------------------------------------------------------------------
def kaji():
    mb = MapBuild(KAJI, NAMES[KAJI], 138, display=NAMES[KAJI])
    mb.props(note="<Area Name: Königliche Schmiede>\n<No Rank HUD>", bgm=('Town3', 55), bgs=('Fire2', 35))
    el = Ev().se('Move1', 60).transfer(WACHTBURG, 37, 38, 2, 0)
    mb.add("Exit", 14, 13, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(KAJI_T, ["Kaji. Royal smith. Rune-steel for the Wall, horseshoes",
                    "for the king, and whatever you can afford."])
    def refit(e):
        e.say(KAJI_T, ["That armor. Let me see it. …Hold still."])
        e.se('Hammer')
        e.say(KAJI_T, ["Silver. True silver, not plate with a shine on it.",
                       "Old work, older than the Wall. There's no maker's",
                       "mark. There's no wear, either. None."])
        e.say(KAJI_T, ["It wasn't made for you, and it fits like it was.",
                       "I don't like that. I'd like to fit it properly anyway.",
                       "One Goldkrone fifty, and it'll stop a spear."])
        def pay(b):
            b.gold(-150)
            b.se('Hammer')
            b.fadeout()
            b.wait(30)
            b.se('Hammer')
            b.wait(30)
            b.se('Equip2')
            b.script("const a = $gameActors.actor(1);\n"
                     "const silver = $dataArmors[%d], best = $dataArmors[%d];\n"
                     "$gameParty.gainItem(best, 1);\n"
                     "if (a.isEquipped(silver)) a.changeEquip(3, best);\n"
                     "$gameParty.loseItem(silver, 1, false);" % (AR["Silberrüstung"], AR["Echtsilberrüstung"]))
            b.fadein()
            b.say(KAJI_T, ["There. Echtsilber, the old smiths called it. The arm",
                           "stays bare, like you had it. Figured you'd want that."])
            b.notice(["The Silberrüstung became the \\C[6]Echtsilberrüstung\\C[0]",
                      "(Armor 5, rank E)."])
            b.switch(S_REFIT)
        e.if_gold(150, '>=',
                  lambda b: b.choices(["Pay 1 gk 5 sl", "Not now"], [pay, None], cancel=1),
                  lambda b: b.say(KAJI_T, ["Come back with a Goldkrone fifty."]))
    def shop(e):
        e.shop([('armor', AR["Wolfslederkappe"]), ('armor', AR["Stahlarmschienen"]), ('armor', AR["Stahlhaube"]),
                ('armor', AR["Turmschild"]), ('armor', AR["Eisenhaube"]), ('armor', AR["Lederrock"]),
                ('weapon', WP["Panzerhandschuhe"]), ('weapon', WP["Morgenstern"])])
    el.if_script("!$gameSwitches.value(%d) && $gameParty.hasItem($dataArmors[%d], true)" % (S_REFIT, AR["Silberrüstung"]),
                 lambda b: b.choices(["Buy", "The silver armor", "Nothing"], [shop, refit, None], cancel=2),
                 lambda b: b.choices(["Buy", "Nothing"], [shop, None], cancel=1))
    mb.add("Kaji Tōbei", 14, 5, [pg(el, char=KAJI_T.char[0], index=KAJI_T.char[1], direction=2, priority=1)])
    appr = npc_speaker("Apprentice", "People1", 2)
    el = Ev().say(appr, ["Master Kaji made the Wallfeste's gate. Forty tons of",
                         "rune-steel! He says the gate's fine. It's the wall",
                         "next to it that's the problem."])
    mb.npc("Apprentice", 7, 8, appr, el, direction=4)
    mb.light('hearth', 4, 5)
    return mb


# ---------------------------------------------------------------------------
# 45  Ausrüster Aoyagi  (sample 130)
# ---------------------------------------------------------------------------
def ausruester():
    mb = MapBuild(AUSRUESTER, NAMES[AUSRUESTER], 130, display=NAMES[AUSRUESTER])
    mb.props(note="<Area Name: Ausrüster Aoyagi>\n<No Rank HUD>", bgm=('Town3', 55))
    el = Ev().se('Move1', 60).transfer(WACHTBURG, 9, 41, 2, 0)
    mb.add("Exit", 8, 15, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.say(AOYAGI, ["Aoyagi's! Potions, charms, and Church dawn-light, the",
                    "genuine article. Throw it at anything that smells of",
                    "ash and watch it scream."])
    el.shop([('item', IT["Heiltrank"]), ('item', IT["Großer Heiltrank"]), ('item', IT["Manatrank"]),
             ('item', IT["Gegengift"]), ('item', IT["Riechsalz"]), ('item', IT["Lichtphiole"]),
             ('armor', AR["Heilerbrosche"]), ('armor', AR["Runenamulett"]), ('armor', AR["Wachmantel"])])
    mb.add("Aoyagi Kanon", 10, 6, [pg(el, char=AOYAGI.char[0], index=AOYAGI.char[1], direction=2, priority=1)])
    return mb


# ---------------------------------------------------------------------------
# 46  Kornspeicher-Gewölbe  (sample 44): the granary vaults
# ---------------------------------------------------------------------------
def kornspeicher():
    mb = MapBuild(KORNSPEICHER, NAMES[KORNSPEICHER], 44, display=NAMES[KORNSPEICHER])
    mb.props(note="<Rank: F>\n<Area Name: Kornspeicher-Gewölbe>", bgm=('Dungeon2', 55), bgs=('Drips', 40),
             battleback=('Stone1', 'Stone1'),
             encounters=[(TR["Kornkobolde x3"], 6, ()), (TR["Schimmelinge x2"], 5, ()),
                         (TR["Kobolde & Schimmeling"], 6, ())], steps=22)
    for x in (7, 8, 9):
        el = Ev().se('Move1', 60).transfer(WACHTBURG, 11, 24, 2, 0)
        mb.add("Up", x, 3, [pg(el, trigger=1, priority=0)])
    el = Ev()
    el.wait(10)
    el.se('Cry2', 60, 150)
    el.text(["Scrabbling in the dark. Something small giggles."])
    el.say(HANMA, ["\"Rats\", the man said."], 'calm')
    el.say(KANTA, ["Rats don't giggle."], 'wry')
    el.say(HANMA, ["Kobolds, then. Grain imps: they breed in stores and",
                   "spoil what they can't eat. And that smell is mold,",
                   "a great deal of it. Mind your breathing."], 'stern')
    mb.autorun("Enter", el)
    # the mold mother by the water
    p = []
    el = Ev()
    el.se('Monster3', 80, 70)
    el.shake(2, 5, 20)
    el.text(["The far wall is furred with grey-green mold, and the",
             "mold is breathing. A shape heaves itself up out of it,",
             "trailing spores like smoke."])
    el.say(HANMA, ["There's the grain gone. It's been feeding the whole",
                   "time. Burn it if you can, cut it if you can't!"], 'command')
    el.battle(TR["Schimmelmutter"], can_escape=False, can_lose=False)
    el.text(["The mold collapses into a heap of grey dust. The",
             "giggling in the dark stops all at once."])
    el.quest_desc(Q_GRAIN, "The vaults are clear: a mold mother and her grain imps. Report to Hoshino Miyu at the "
                           "Guild for the pay.")
    el.switch(S_GRAIN_DONE)
    p.append(pg(el, char='$BigMonster1', index=0, direction=6, trigger=0, priority=1, direction_fix=True,
                step_anime=True))
    p.append(pg(None, sw=S_GRAIN_DONE, priority=0))
    mb.add("Schimmelmutter", 12, 19, p)
    chest(mb, "Old Crate", 2, 12, lambda e: (e.item(IT["Gegengift"], 3), e.gold(30)),
          "Found 3 Gegengift and \\MONEY[30].")
    chest(mb, "Old Crate", 2, 19, lambda e: e.item(IT["Lichtphiole"], 1), "Found a Lichtphiole.")
    mb.light('cave_dark', 0, 0, tile=False)
    mb.follow_light('beam', 8, 5)
    for x, y in [(6, 7), (10, 7), (15, 7), (6, 17), (10, 17), (15, 17)]:
        mb.light('torch', x, y)
    return mb


# ---------------------------------------------------------------------------
# 47  Nordstraße  (sample 293): wolves, herbs, and the emergency
# ---------------------------------------------------------------------------
def nordstrasse():
    mb = MapBuild(NORDSTRASSE, NAMES[NORDSTRASSE], 293, display=NAMES[NORDSTRASSE])
    mb.props(note="<Rank: F>\n<Area Name: Nordstraße>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Field2', 65), battleback=('Grassland', 'Forest'),
             encounters=[(TR["Nordwölfe x2"], 7, ()), (TR["Harpyien x2"], 4, ()), (TR["Wegelagerer x2"], 3, ()),
                         (TR["Nordwölfe x3"], 3, ())], steps=30)
    # exits
    for y in (12, 13, 14):
        el = Ev().se('Move1', 60).transfer(WACHTBURG, 24, 47, 8, 0)
        mb.add("To Wachtburg", 2, y, [pg(el, trigger=1, priority=0)])
        el = Ev().se('Move1', 60).transfer(KOENIGSSTRASSE, 7, 4, 2, 0)
        mb.add("Königsstraße", 39, y, [pg(el, trigger=1, priority=0)])
    for x in (25, 26, 27, 28, 29):
        blocked = Ev().text(["The Nordstraße climbs north to the Wall, two days away.",
                             "A patrol turns back anyone without orders."])
        blocked.route(-1, [(1, [])], skippable=True)
        go = Ev().se('Move1', 60).transfer(WALLSTRASSE, 12, 25, 8, 0)
        mb.add("North", x, 0, [pg(blocked, trigger=1, priority=0), pg(go, sw=S_CALL, trigger=1, priority=0)])
    guard = Ev().if_switch(S_CALL, True,
                           lambda b: b.say(GUARD, ["Orders for the Wall? Then go with the gods. And come",
                                                   "back, if they let you."]),
                           lambda b: b.say(GUARD, ["The Nordstraße. North to the Wall, east back round to",
                                                   "the Königsstraße. Wolves on the south track, mind."]))
    mb.npc("Road Guard", 5, 11, GUARD, guard, direction=2)
    # herbs
    herb(mb, 6, 6)
    herb(mb, 19, 11)
    herb(mb, 9, 19)
    # the wolf pack (job)
    p = [pg(None, priority=0)]
    el = Ev()
    el.se('Wolf', 90)
    el.balloon(0, 1)
    el.text(["Wolves, lean and grey, around a big scarred male. The",
             "leader lifts its head and does not run."])
    el.battle(TR["Rudel"], can_escape=False, can_lose=False)
    el.text(["The pack leader falls. The rest scatter into the scrub", "and don't come back."])
    el.quest_desc(Q_WOLVES, "The pack leader is dead. Report to Hoshino Miyu at the Guild for the pay.")
    el.switch(S_WOLVES_DONE)
    p.append(pg(el, sw=S_WOLVES, char=WOLF_CHAR[0], index=WOLF_CHAR[1], direction=8, trigger=1, priority=1,
                step_anime=True))
    p.append(pg(None, sw=S_WOLVES_DONE, priority=0))
    mb.add("Wolf Pack", 27, 21, p)

    # ------------------------------------------------ the emergency
    # refugees and hounds on the north road (visible during the emergency only)
    def only_emerg(name, x, y, sheet, index, d=2, anime=False):
        mb.add(name, x, y, [pg(None, priority=0),
                            pg(None, sw=S_EMERG, char=sheet, index=index, direction=d, priority=1, step_anime=anime),
                            pg(None, sw=S_EMERG_DONE, priority=0)])
    only_emerg("Hound", 26, 4, HOUND_CHAR[0], HOUND_CHAR[1], 2, True)
    only_emerg("Hound", 28, 5, HOUND_CHAR[0], HOUND_CHAR[1], 2, True)
    only_emerg("Leitrüde", 27, 6, 'Monster', 5, 2, True)
    only_emerg("Wounded Escort", 25, 8, 'Damage1', 4)
    only_emerg("Wounded Refugee", 29, 7, 'Damage2', 1)
    only_emerg("Refugee", 26, 9, 'People1', 1, 8)
    only_emerg("Refugee Child", 27, 9, 'SF_People1', 0, 8)
    only_emerg("Refugee", 28, 9, 'People2', 3, 8)
    el = Ev()
    el.wait(10)
    el.se('Scream', 80)
    el.wait(20)
    el.se('Dog', 90, 70)
    el.text(["Screams up the north road. Dogs, snarling, too deep for", "dogs."])
    el.route(-1, [(29, [5])] + [(3, [])] * 24 + [(4, []), (4, []), (19, []), (29, [4])], wait=True, skippable=True)
    el.narrate(["The column is scattered across the road: carts on their",
                "sides, bundles everywhere, people pressed against the",
                "wheels. Grey hounds weave between them, trailing ash."])
    el.narrate(["And over the last cart stands something bigger. It",
                "isn't eating. It's waiting for the children under the",
                "cart to run."])
    el.say(HANMA, ["Demon hounds. Miasma in their blood, my Lord. The big",
                   "one is rank E, a whole rank above you. It will hit",
                   "you half again as hard as you hit it."], 'stern')
    el.say(HANMA, ["The Guild is coming. We could wait for—"], 'stern')
    el.say(KANTA, ["There are children under that cart."], 'fierce')
    el.say(HANMA, ["…Yes, my Lord. Then we don't wait."], 'command')
    el.battle(TR["Aschenhunde"], can_escape=False, can_lose=False)
    el.fadeout()
    el.switch(S_EMERG_DONE)
    el.wait(30)
    el.fadein()
    el.narrate(["The last hound dissolves into ash on the wind. The",
                "Guild's blades arrive at a run, far too late to help,",
                "and stop."])
    el.say(REN, ["Mama! Mama, the lady has a knife made of light!"])
    el.text(["Kanta looks at her hand. The beam is gone. In its place:", "a dagger of pale blue light, still humming."])
    el.say(HANMA, ["Your first breakthrough, my Lord. You shielded them",
                   "with your own arm, and the weapon answered."], 'smile')
    el.say(HANMA, ["…I have waited a long time to see that."], 'calm')
    el.say(KANTA, ["It doesn't feel like much."], 'wry')
    el.say(HANMA, ["It never does, from inside."], 'smile')
    el.quest_done(Q_EMERG)
    el.say(KUROGANE, ["Neuling. Guild hall. Now. I want that crystal to look",
                      "at you again."])
    el.self_switch('A')
    el.fadeout()
    el.transfer(GILDE, 12, 9, 8, 2)
    el.fadein()
    mb.autorun("Emergency", el, cond_switch=S_EMERG)
    return mb


# ---------------------------------------------------------------------------
# 48  Wolfsgrube  (sample 31): the rank E trial
# ---------------------------------------------------------------------------
def wolfsgrube():
    mb = MapBuild(WOLFSGRUBE, NAMES[WOLFSGRUBE], 31, display=NAMES[WOLFSGRUBE])
    mb.props(note="<Rank: E>\n<Area Name: Wolfsgrube>\n<lighting: Outside>\n<DayNight: step=1>",
             bgm=('Castle3', 55), battleback=('Colosseum', 'Colosseum'))
    mb.door(5, 10, GILDE, 12, 15, 8, index=3, name="Door: Gildenhaus")
    p = []
    el = Ev()
    el.say(KUROGANE, ["The Wolfsgrube. We raise Dire Wolves here for the Wall.",
                      "Trained to hold a line. Trained to break one."])
    el.say(KUROGANE, ["Three of them. Put them all down and the Guild calls",
                      "you Wolfsbann. Fall, and I call them off. Ready?"])
    def fight(e):
        e.say(KUROGANE, ["Open the pens!"])
        e.se('Gate1')
        e.se('Wolf', 90)
        def win(b):
            b.say(KUROGANE, ["Good. Very good."])
            b.say(KUROGANE, ["By the Guild's charter, the first to clear the",
                             "Wolfsgrube take the name Wolfsbann, and the gift that",
                             "goes with it."])
            b.se('Item3')
            b.armor(AR["Wachtfeuer-Amulett"], 1)
            b.add(324, [1, "Wolfsbann"])
            b.notice(["Received the \\C[6]Wachtfeuer-Amulett\\C[0]. Kanta's title:",
                      "\\C[6]Wolfsbann\\C[0]."])
            b.quest_done(Q_TRIAL)
            b.switch(S_TRIAL_DONE)
        def lose(b):
            b.recover_all()
            b.say(KUROGANE, ["Enough! Pens, back! …Up you get. Come back when",
                             "you're ready. The wolves will wait."])
        e.battle(TR["Wolfsgrube"], can_escape=False, can_lose=True, win=win, lose=lose)
    el.choices(["Ready", "Not yet"], [fight, lambda e: e.say(KUROGANE, ["Then go. The exit is behind you."])],
               cancel=1)
    p.append(pg(el, char=KUROGANE.char[0], index=KUROGANE.char[1], direction=2, priority=1))
    el = Ev().say(KUROGANE, ["Wolfsbann. Wear it lightly. The Wall doesn't care",
                             "about titles."])
    p.append(pg(el, sw=S_TRIAL_DONE, char=KUROGANE.char[0], index=KUROGANE.char[1], direction=2, priority=1))
    mb.add("Kurogane Isao", 12, 12, p)
    return mb
