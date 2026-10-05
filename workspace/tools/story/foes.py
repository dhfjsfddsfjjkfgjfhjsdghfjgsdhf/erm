"""Acts II and III: the Host, the Calamities and everything else the party meets after the Wall.

Skills 201-320, enemies 61-160, troops 61-200, items 41-90, weapons 31-60, armors 71-140.
Rank bands the party stands at: ch.4 E (LV 15-21), ch.5 D (21-27), ch.6 D->C (27-31), ch.7 C->B (31-41),
ch.8 B (41-47), ch.9 B->A (47-55).  Numbers are tuned with tools/scen_story_balance.js."""
from story import db
from story.common import Ev, KANTA, HANMA, FALIN, npc_speaker, SW
from story.cast import RIN
from story.db import (eff, trait, skill, passive, enemy, act, drop, stats, weak, weapon, armor, item, state,
                      BATTLEMAGIC_ST, FROST_ST, STAFF_W, ST_FROSTBODY, ST_MORGENWACHT,
                      ADD_STATE, REMOVE_STATE, BUFF, DEBUFF, REC_HP, REC_MP,
                      FIRE, ICE, THUNDER, WATER, EARTH, WIND, LIGHT, DARK,
                      GLOVE_W, SWORD_W, FLAIL_W, AXE_W, SPEAR_W,
                      GEN, LIGHT_A, HEAVY_A, SSHIELD, LSHIELD, E_SHIELD, E_HEAD, E_BODY, E_ACC,
                      ST_DAZZLED, ST_FEAR, ST_PRONE, ST_CHILL, ST_PINNED, ST_BRACED, ST_BURN, ST_SEALED, ST_WEBBED,
                      ST_DROWNING, ST_ASHBURN, ST_FROZEN, ST_MIASMA)

# battler images made from the RTP / packs by build_story.py (name -> spec)
#   src: RTP enemy name or a path; h: target height; f: scale factor; hue (deg); sat; tint (r, g, b, amount); dark
IMAGES = {
    "Hoellenhund": dict(src="SF_Zombiedog", f=1.35, hue=12, sat=1.3, dark=0.95),
    "Gargyl": dict(src="Birdman", f=1.0, sat=0.0, tint=(140, 138, 132, 0.3), dark=0.85),
    "Messinggolem": dict(src="Stoneknight", f=1.15, sat=0.0, tint=(196, 150, 62, 0.55)),
    "Ghul": dict(src="SF_Cyborg", f=1.0, sat=0.3, tint=(120, 150, 110, 0.35), dark=0.85),
    "Messingschreiber": dict(src="Evilbook", f=1.9, sat=0.0, tint=(200, 150, 60, 0.6)),
    "Messingvogt": dict(src="Highking", f=1.35, sat=0.6, tint=(190, 140, 55, 0.35)),
    "Wyvern": dict(src="/mnt/user-data/uploads/rt5monster/rtdragon3.png", h=330),
    "Vampirknecht": dict(src="Darkelf", f=1.0, sat=0.5, tint=(170, 60, 70, 0.3), dark=0.85),
    "Leere_Huelle": dict(src="Stoneknight", f=1.1, hue=240, sat=0.4, dark=0.7),
    "Aschenschmied": dict(src="SF_Redogre", f=1.35, sat=0.7, tint=(90, 60, 50, 0.3), dark=0.8),
    "Eiserner_Prinz": dict(src="Blackknight", f=1.4),
    "Messingsoldat": dict(src="Gatekeeper", f=1.1, sat=0.0, tint=(196, 150, 62, 0.5)),
    "Oni": dict(src="SF_Blueogre", f=1.2),
    "Oni_Hauptmann": dict(src="SF_Blueogre", f=1.35, hue=150, sat=1.1),
    "Seelenkessel": dict(src="Demonpot", f=3.2, sat=0.5, tint=(170, 120, 50, 0.4)),
    "Goen": dict(src="SF_Enmadaio", f=1.1),
}


# =====================================================================================================================
# SKILLS  (201-320)
# =====================================================================================================================
SKILLS = {}


def skills(put, start):
    assert start == 200, start

    def en(sid, name, **kw):
        kw.setdefault("stype", 0)
        kw.setdefault("occasion", 1)
        kw.setdefault("crit", True)
        s = skill(sid, name, **kw)
        put(s)
        SKILLS[name] = sid
    put(db.sep(200, "----- Foes (Acts II-III)"))
    # ---- chapter 4: the Wall
    en(201, "Höllenfeuer", scope=2, dtype=1, element=FIRE, formula="d6", hit=0, anim=66, icon=64, crit=False,
       msg="%1 breathes hellfire!", effects=[eff(ADD_STATE, ST_BURN, 0.3)], note="<Stat: MAG>\n<Save: DEX>")
    en(202, "Glutbiss", scope=1, dtype=1, element=FIRE, formula="d8", hit=1, anim=16, icon=64,
       msg="%1 bites with burning jaws!", effects=[eff(ADD_STATE, ST_BURN, 0.3)], note="<Stat: STR>")
    en(203, "Steinhaut", scope=11, anim=52, icon=33, crit=False, msg="%1's skin turns to stone.",
       effects=[eff(BUFF, 3, 3)], note="<Stat: CON>")
    en(204, "Sturzflug", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=11, icon=76,
       msg="%1 dives out of the sky!", note="<Stat: DEX>\n<Damage: 125%>")
    en(205, "Messingfaust", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=39, icon=77,
       msg="%1 swings a fist of brass!", effects=[eff(ADD_STATE, ST_PRONE, 0.4)], note="<Stat: STR>\n<Save: STR states>")
    en(206, "Vertragsklausel", scope=1, anim=58, icon=4, crit=False, msg="%1 reads out a clause!",
       effects=[eff(ADD_STATE, ST_SEALED, 1.0)], note="<Stat: MAG>\n<Save: WIS>")
    en(207, "Tintenstrahl", scope=2, anim=33, icon=3, crit=False, msg="%1 sprays black ink!",
       effects=[eff(ADD_STATE, ST_DAZZLED, 1.0)], note="<Stat: DEX>\n<Save: CON>")
    en(208, "Federkiel", scope=1, dtype=1, element=1, formula="d8", hit=1, anim=11, icon=76,
       msg="%1 stabs with a brass quill!", note="<Stat: DEX>")
    en(209, "Schuldspruch", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=39, icon=77,
       msg="%1 pronounces the debt!", note="<Stat: STR>\n<Damage: 150%>")
    en(210, "Eintreiben", scope=1, dtype=5, element=DARK, formula="d10", hit=2, anim=59, icon=71,
       msg="%1 collects what is owed!", note="<Stat: MAG>\n<Save: CON>")
    en(211, "Messingkette", scope=1, anim=12, icon=10, crit=False, msg="%1 casts a brass chain!",
       effects=[eff(ADD_STATE, ST_PINNED, 1.0)], note="<Stat: STR>\n<Save: STR>")
    # ---- chapter 5: Weißenfels
    en(212, "Giftstachel", scope=1, dtype=1, element=1, formula="d8", hit=1, anim=11, icon=76,
       msg="%1 lashes with its stinger!", effects=[eff(ADD_STATE, 4, 0.5)], note="<Stat: DEX>")
    en(213, "Blutsaugen", scope=1, dtype=5, element=1, formula="d8", hit=1, anim=16, icon=76,
       msg="%1 drinks!", note="<Stat: STR>")
    en(214, "Bannblick", scope=1, anim=58, icon=11, crit=False, msg="%1's eyes hold you!",
       effects=[eff(ADD_STATE, ST_FEAR, 1.0)], note="<Stat: CHA>\n<Save: WIS>")
    en(215, "Schmiedehammer", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=39, icon=77,
       msg="%1 brings the forge hammer down!", note="<Stat: STR>\n<Damage: 150%>")
    en(216, "Glutfunken", scope=2, dtype=1, element=FIRE, formula="d8", hit=0, anim=66, icon=64, crit=False,
       msg="%1 shakes a storm of sparks from the forge!", effects=[eff(ADD_STATE, ST_BURN, 0.3)],
       note="<Stat: MAG>\n<Save: DEX>")
    en(217, "Härten", scope=11, anim=52, icon=33, crit=False, msg="%1 quenches itself in the forge.",
       effects=[eff(BUFF, 3, 3), eff(BUFF, 2, 3)], note="<Stat: CON>")
    en(218, "Königsklinge", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=6, icon=97,
       msg="%1 strikes with a king's sword!", note="<Stat: STR>\n<Crit Range: +1>")
    en(219, "Schildwall", scope=11, anim=52, icon=128, crit=False, msg="%1 raises a wall of shields.",
       effects=[eff(ADD_STATE, ST_BRACED, 1.0)], note="<Stat: CON>", speed=2000)
    en(220, "Heerruf", scope=8, anim=37, icon=32, crit=False, msg="%1 calls the dead to order!",
       effects=[eff(BUFF, 2, 3)], note="<Stat: CHA>")
    # ---- chapter 6: the siege
    en(221, "Hellebarde", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=11, icon=99,
       msg="%1 thrusts with a brass halberd!", note="<Stat: STR>\n<Hit: +1>")
    en(222, "Keulenschlag", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=39, icon=77,
       msg="%1 swings an iron club!", effects=[eff(ADD_STATE, ST_PRONE, 0.4)], note="<Stat: STR>\n<Save: STR states>")
    en(223, "Seelenstrom", scope=2, dtype=5, element=DARK, formula="d6", hit=0, anim=59, icon=71, crit=False,
       msg="%1 drinks at every soul in reach!", note="<Stat: MAG>\n<Save: CON>")
    en(224, "Messingurteil", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=39, icon=77,
       msg="%1 passes judgment in brass!", note="<Stat: STR>\n<Damage: 150%>")
    en(225, "Seelenvertrag", scope=2, dtype=1, element=DARK, formula="d10", hit=0, anim=58, icon=71, crit=False,
       msg="%1 unrolls a contract with every name on it!", effects=[eff(ADD_STATE, ST_SEALED, 0.5)],
       note="<Stat: CHA>\n<Save: WIS>")
    en(226, "Goldene Kette", scope=1, dtype=1, element=1, formula="d8", hit=1, anim=12, icon=10,
       msg="%1 lashes out with a golden chain!", effects=[eff(ADD_STATE, ST_PINNED, 1.0)],
       note="<Stat: STR>\n<Save: STR states>")
    en(227, "Brass Toll", scope=2, dtype=1, element=1, formula="d8", hit=0, anim=39, icon=77, crit=False,
       msg="%1 calls in every debt at once!", note="<Stat: CHA>\n<Save: CON>")
    from story import foes3
    foes3.skills(put, 228)


# =====================================================================================================================
# GUESTS (321-360): Asahina Rin (actor 5, fixed rank C) and Tsukishiro Yukino (actor 6, Act III)
# =====================================================================================================================
GUEST = {}


def guest_skills(put, start):
    assert start == 321, start
    def g(s):
        put(s)
        GUEST[s["name"]] = s["id"]
    BM, FA = BATTLEMAGIC_ST, FROST_ST
    g(skill(321, "Flammenlanze", BM, mp=5, scope=1, dtype=1, element=FIRE, formula="d10", hit=2, anim=66, icon=64,
            crit=True, msg="%1 hurls a lance of flame!",
            desc="Rin's fire: a lance of flame at one foe, d10 + MAG.", note="<Stat: MAG>\n<Start Rank: C>"))
    g(skill(322, "Eissturm", BM, mp=5, scope=2, dtype=1, element=ICE, formula="d8", hit=0, anim=73, icon=65,
            msg="%1 calls down an ice storm!",
            desc="Every foe: d8 + MAG ice, DEX save for half.", note="<Stat: MAG>\n<Save: DEX>\n<Start Rank: C>"))
    g(skill(323, "Königsschild", BM, mp=5, scope=8, anim=53, icon=128, speed=10,
            effects=[eff(REMOVE_STATE, ST_FEAR, 1.0)], msg="%1 raises the royal shield!",
            desc="Every ally gains a barrier of (d8 + CHA) x1/2 and shakes\noff fear.",
            note="<Stat: CHA>\n<Barrier: d8 50%>\n<Support>\n<Start Rank: C>"))
    for i in range(324, 331):
        put(db.sep(i, ""))
    g(skill(331, "Frostschnitt", FA, mp=5, scope=1, dtype=1, element=ICE, formula="d8", hit=1, anim=72, icon=65,
            crit=True, effects=[eff(ADD_STATE, ST_CHILL, 0.5)], msg="%1 cuts with a blade of frost!",
            desc="A cut of frost: d8 + DEX ice. CON save or the foe is\nChilled.",
            note="<Stat: DEX>\n<Save: CON states>\n<Start Rank: C>"))
    g(skill(332, "Eiswand", FA, mp=5, scope=8, anim=74, icon=65, speed=10, msg="%1 raises a wall of ice!",
            desc="Every ally gains a barrier of ice: (d8 + WIS) x1/2.",
            note="<Stat: WIS>\n<Barrier: d8 50%>\n<Support>\n<Start Rank: C>"))
    g(passive(333, "Frostkörper", 65,
              "Passive. The cold of the rift is in her: ice damage x1/2,\nshe can't be Chilled or frozen.",
              "<Passive State: %d>" % ST_FROSTBODY))
    g(skill(334, "Schneesturm", FA, mp=5, scope=2, dtype=1, element=ICE, formula="d10", hit=0, anim=74, icon=65,
            effects=[eff(ADD_STATE, ST_CHILL, 0.3)], msg="%1 brings the storm of Frostheim!",
            desc="B. Every foe: d10 + MAG ice, CON save for half. It may\nleave them Chilled.",
            note="<Stat: MAG>\n<Save: CON>\n<Start Rank: B>\n<Needs Rank: B>"))
    g(skill(335, "Kalte Gnade", FA, mp=5, scope=7, dtype=3, formula="d10", anim=45, icon=72, occasion=0,
            effects=[eff(REMOVE_STATE, ST_BURN, 1.0), eff(REMOVE_STATE, ST_ASHBURN, 1.0)], msg="%1 lays cold hands on the wound.",
            desc="B. Heals one ally for d10 + WIS and puts out fire and ash.",
            note="<Stat: WIS>\n<Start Rank: B>\n<Needs Rank: B>"))
    g(skill(336, "Weiße Stille", FA, mp=5, scope=1, dtype=1, element=ICE, formula="d12", hit=1, anim=72, icon=65,
            crit=True, effects=[eff(ADD_STATE, ST_FROZEN, 0.3)], msg="Everything goes white and silent around %1's blade.",
            desc="A. One cut in total silence: (d12 + DEX) x1.5 ice. CON save\nor the foe freezes solid for a turn.",
            note="<Stat: DEX>\n<Damage: 150%>\n<Save: CON states>\n<Start Rank: A>\n<Needs Rank: A>"))
    g(passive(337, "Morgenwacht", 87,
              "Passive (A). The last of the Morgenwacht: +2 to hit and +2\nto every save.",
              "<Passive State: %d>\n<Needs Rank: A>" % ST_MORGENWACHT))



# =====================================================================================================================
# ITEMS (41-90), WEAPONS (31-60), ARMORS (71-140)
# =====================================================================================================================
ITEMS = {}


def items(put, start):
    assert start == 41, start
    def it(i):
        put(i)
        ITEMS[i["name"]] = i["id"]
    it(item(41, "Elixier", 175, 400, "A Church elixir. Restores 350 HP.", [eff(REC_HP, 0, 0, 350)]))
    it(item(42, "Großes Elixier", 175, 1800, "A court alchemist's elixir. Restores 900 HP.", [eff(REC_HP, 0, 0, 900)]))
    it(item(43, "Hoher Manatrank", 177, 500, "Strong mana tonic. Restores 100 MP.", [eff(REC_MP, 0, 0, 100)]))
    it(item(44, "Äther", 177, 2400, "Distilled mana. Restores 300 MP.", [eff(REC_MP, 0, 0, 300)]))
    it(item(45, "Starkes Riechsalz", 183, 600, "Wakes a knocked-out ally with half their HP.",
            [eff(REMOVE_STATE, 1, 1.0), eff(REC_HP, 0, 0.5, 0)], scope=9, anim=49))
    lp = item(46, "Große Lichtphiole", 162, 900, "A great phial of dawn light: 250 Light damage to one\nfoe.",
              [], scope=1, occasion=1, anim=46)
    lp["damage"] = {"critical": False, "elementId": LIGHT, "formula": "250", "type": 1, "variance": 10}
    it(lp)
    it(item(47, "Allheilmittel", 179, 300, "Cures every ailment.",
            [eff(REMOVE_STATE, s, 1.0) for s in db.NEGATIVE + [ST_BURN, ST_SEALED, ST_WEBBED, ST_DROWNING, ST_ASHBURN]],
            anim=45))
    # mana stones by rank: WORLD economy (D 10 gk, C 100 gk, B 1000 gk, A 10000 gk), traders pay half
    for i, (r, gk) in enumerate([("D", 10), ("C", 100), ("B", 1000), ("A", 10000)]):
        it(item(48 + i, "Manastein (%s)" % r, 300, gk * 100, "A mana stone from a rank %s creature.\nWorth about %d gk to a "
                "trader." % (r, gk // 2 if gk > 1 else 1), [], scope=0, occasion=3, anim=0, consumable=False))


KEY = {}


def key_items(put, start):
    assert start == 61, start
    key = lambda iid, name, icon, desc: item(iid, name, icon, 0, desc, [], scope=0, occasion=3, anim=0, itype=2,
                                            consumable=False)
    def k(i):
        put(i)
        KEY[i["name"]] = i["id"]
    k(key(61, "Messingmünze", 314, "A brass coin, warm to the touch. It was found on a\ndead sentry's eyes."))
    k(key(62, "Hauptbuch", 186, "The Wallfeste's supply ledger. The numbers don't add\nup, and one hand made the difference."))
    k(key(63, "Zisternenschlüssel", 195, "An old iron key to the Wallfeste's cistern."))
    k(key(64, "Siegelbrief", 192, "Marshal Kōsaka's writ: the bearer speaks for the Wall."))
    k(key(65, "Rins Brief", 192, "Crown Princess Rin's letter to the Empress in\nLichtenhall."))
    # the Dawn Regalia (Act III)
    k(key(66, "Morgenklinge", 97, "[Dawn Regalia] The sword of the first Hero of Dawn.\nDemons can't hide behind their rank from it."))
    k(key(67, "Sternlaterne", 162, "[Dawn Regalia] A lantern that holds a piece of the\nfirst dawn."))
    k(key(68, "Heldenhorn", 225, "[Dawn Regalia] The horn that called the hosts of 312\nto the last battle."))
    k(key(69, "Aschenkrone", 229, "[Dawn Regalia] A crown of grey iron that burns\nwhite in the dark."))
    k(key(70, "Kusakis Gabe", 182, "Bread and salt, left for the leshy of the Urwald."))
    k(key(71, "Grubenlampe", 162, "Foreman Tsurugi's lamp. His miners are down there."))
    from story import foes3
    foes3.key_items(put, 72)


WEAPONS = {}
WEAPONS_LIST = {}


def weapons(put, start):
    assert start == 31, start
    def w(x):
        put(x)
        WEAPONS[x["name"]] = x["id"]
        WEAPONS_LIST[x["id"]] = x
    # Falin: gauntlets (d10 STR) and flails (d12, -1 to hit) by rank; she can wield any weapon
    w(weapon(31, "Wallfäuste", GLOVE_W, 10, 102, 1, 6000, "[Gauntlets · D] Plates riveted by the Wall's smiths.\nd10 · STR", "<Rank: D>"))
    w(weapon(32, "Morgenfaust", GLOVE_W, 10, 102, 1, 60000, "[Gauntlets · C] Rune-steel knuckles. d10 · STR · +1 to hit",
             "<Rank: C>\n<Hit: +1>"))
    w(weapon(33, "Sternenfäuste", GLOVE_W, 10, 102, 1, 600000, "[Gauntlets · B] Star-iron from Eisenberg. d10 · STR · +2 to hit",
             "<Rank: B>\n<Hit: +2>"))
    w(weapon(34, "Drachenknöchel", GLOVE_W, 12, 102, 1, 0, "[Gauntlets · A] Wyrm-bone and rune-steel. d12 · STR",
             "<Rank: A>"))
    w(weapon(35, "Kriegsflegel", FLAIL_W, 12, 98, 1, 7000, "[Flail · D] A heavy war flail. d12 · STR · -1 to hit",
             "<Rank: D>\n<Hit: -1>"))
    w(weapon(36, "Messingbrecher", FLAIL_W, 12, 98, 1, 70000, "[Flail · C] Made to break brass. d12 · STR", "<Rank: C>"))
    w(weapon(37, "Trollmorgenstern", FLAIL_W, 12, 98, 1, 700000, "[Flail · B] A troll king's morning star, cut down to\nsize. d12 · STR · +1 to hit",
             "<Rank: B>\n<Hit: +1>"))
    # the guests' own weapons
    w(weapon(38, "Kronenstab", STAFF_W, 6, 101, 1, 0, "[Staff · C] Rin's staff, the Asahina crest on its head.\nd6 · MAG",
             "<Stat: MAG>\n<Rank: C>"))
    w(weapon(39, "Frostklinge", SWORD_W, 8, 97, 6, 0, "[Sword · C] Yukino's blade, rimed white. d8 · DEX · Ice",
             "<Stat: DEX>\n<Rank: C>", ))
    w(weapon(40, "Mondeisklinge", SWORD_W, 10, 97, 6, 0, "[Sword · B] The blade remembers the rift. d10 · DEX · Ice\n+1 to hit",
             "<Stat: DEX>\n<Rank: B>\n<Hit: +1>"))
    w(weapon(41, "Weißklinge", SWORD_W, 12, 97, 6, 0, "[Sword · A] Frostheim's white steel. d12 · DEX · Ice",
             "<Stat: DEX>\n<Rank: A>"))
    for wid in (39, 40, 41):
        WEAPONS_LIST[wid]["traits"] = [trait(31, ICE, 0), trait(22, 0, 0)]


ARMORS = {}


def armors(put, start):
    assert start == 71, start
    def a(x):
        put(x)
        ARMORS[x["name"]] = x["id"]
    # ---- D (the Wallfeste, Weißenfels camp)
    a(armor(71, "Wallhelm", HEAVY_A, E_HEAD, 3, 132, 4500, "[Head · Heavy · D] +3 AC. The Nordwall's riveted helm.", "<Rank: D>"))
    a(armor(72, "Fellkapuze", LIGHT_A, E_HEAD, 0, 130, 3800, "[Head · Light · D] CON +20, halves the chance of being\nChilled.",
            "<Rank: D>\n<CON: +20>", [trait(13, ST_CHILL, 0.5)]))
    a(armor(73, "Wallschild", LSHIELD, E_SHIELD, 5, 129, 6000, "[Large Shield · D] +5 AC. Painted with the Wall's black\ntower.", "<Rank: D>"))
    a(armor(74, "Kriegeramulett", GEN, E_ACC, 0, 147, 5000, "[Accessory · D] STR +20", "<Rank: D>\n<STR: +20>"))
    a(armor(75, "Heilerstola", GEN, E_ACC, 0, 147, 5000, "[Accessory · D] WIS +20", "<Rank: D>\n<WIS: +20>"))
    a(armor(76, "Glutamulett", GEN, E_ACC, 0, 147, 5000, "[Accessory · D] MAG +20", "<Rank: D>\n<MAG: +20>"))
    a(armor(77, "Wachstiefel", GEN, E_ACC, 0, 142, 5500, "[Accessory · D] DEX +20", "<Rank: D>\n<DEX: +20>"))
    a(armor(78, "Brandschutzmantel", GEN, E_ACC, 0, 138, 4800, "[Accessory · D] Fire damage x1/2, CON +10",
            "<Rank: D>\n<CON: +10>", [trait(11, FIRE, 0.5)]))
    a(armor(79, "Königliches Wappen", GEN, E_ACC, 0, 145, 0, "[Accessory · D] Rin's gift: the Asahina crest. CHA +25,\nevery stat +5.",
            "<Rank: D>\n<CHA: +25>\n<All Stats: +5>"))
    # ---- C (Weißenfels, the siege, Lichtenhall)
    a(armor(80, "Messingbrecherhelm", HEAVY_A, E_HEAD, 5, 132, 45000, "[Head · Heavy · C] +5 AC.", "<Rank: C>"))
    a(armor(81, "Magierhut", LIGHT_A, E_HEAD, 1, 133, 40000, "[Head · Light · C] +1 AC, MAG +25", "<Rank: C>\n<MAG: +25>"))
    a(armor(82, "Turmschild der Wacht", LSHIELD, E_SHIELD, 8, 129, 60000, "[Large Shield · C] +8 AC.", "<Rank: C>"))
    a(armor(83, "Kriegerring", GEN, E_ACC, 0, 144, 50000, "[Accessory · C] STR +35", "<Rank: C>\n<STR: +35>"))
    a(armor(84, "Heiligenring", GEN, E_ACC, 0, 144, 50000, "[Accessory · C] WIS +35", "<Rank: C>\n<WIS: +35>"))
    a(armor(85, "Magierring", GEN, E_ACC, 0, 144, 50000, "[Accessory · C] MAG +35", "<Rank: C>\n<MAG: +35>"))
    a(armor(86, "Falkenring", GEN, E_ACC, 0, 144, 55000, "[Accessory · C] DEX +35", "<Rank: C>\n<DEX: +35>"))
    a(armor(87, "Frostsiegel", GEN, E_ACC, 0, 165, 0, "[Accessory · C] Yukino's seal of ice. Ice and Death damage\nx1/2, WIS +30.",
            "<Rank: C>\n<WIS: +30>", [trait(11, ICE, 0.5), trait(11, DARK, 0.5)]))
    # ---- B (Lichtenhall arena, Hirschheim, Eisenberg)
    a(armor(88, "Arenahelm", HEAVY_A, E_HEAD, 7, 132, 450000, "[Head · Heavy · B] +7 AC.", "<Rank: B>"))
    a(armor(89, "Waldkrone", LIGHT_A, E_HEAD, 2, 133, 400000, "[Head · Light · B] +2 AC, WIS +40, MAG +20",
            "<Rank: B>\n<WIS: +40>\n<MAG: +20>"))
    a(armor(90, "Runenschild", LSHIELD, E_SHIELD, 11, 129, 600000, "[Large Shield · B] +11 AC. Eisenberg rune-steel.", "<Rank: B>"))
    a(armor(91, "Siegerkranz", GEN, E_ACC, 0, 145, 0, "[Accessory · B] The Sonnwende champion's wreath. Every\nstat +15.",
            "<Rank: B>\n<All Stats: +15>"))
    a(armor(92, "Fuchsspiegel", GEN, E_ACC, 0, 147, 0, "[Accessory · B] Shirogane's mirror shard: the wearer is\nhit less (+3 AC), DEX +30.",
            "<Rank: B>\n<AC: +3>\n<DEX: +30>"))
    a(armor(93, "Kriegerring B", GEN, E_ACC, 0, 144, 500000, "[Accessory · B] STR +50", "<Rank: B>\n<STR: +50>"))
    a(armor(94, "Heiligenring B", GEN, E_ACC, 0, 144, 500000, "[Accessory · B] WIS +50", "<Rank: B>\n<WIS: +50>"))
    a(armor(95, "Magierring B", GEN, E_ACC, 0, 144, 500000, "[Accessory · B] MAG +50", "<Rank: B>\n<MAG: +50>"))
    # ---- A (Salzhafen, the end)
    a(armor(96, "Seefahrerhelm", HEAVY_A, E_HEAD, 9, 132, 4500000, "[Head · Heavy · A] +9 AC.", "<Rank: A>"))
    a(armor(97, "Sturmschild", LSHIELD, E_SHIELD, 14, 129, 6000000, "[Large Shield · A] +14 AC.", "<Rank: A>"))
    a(armor(98, "Perlenamulett", GEN, E_ACC, 0, 147, 5000000, "[Accessory · A] Water damage x1/2, every stat +20",
            "<Rank: A>\n<All Stats: +20>", [trait(11, WATER, 0.5)]))
    a(armor(99, "Drachenschuppe", GEN, E_ACC, 0, 145, 0, "[Accessory · A] Shiranui's shed scale. Fire x0, CON +60.",
            "<Rank: A>\n<CON: +60>", [trait(11, FIRE, 0.0)]))
    # ---- the guests
    a(armor(100, "Kronprinzenmantel", LIGHT_A, E_BODY, 6, 136, 0, "[Body · Light · C] Rin's battle-mage coat. Armor 6, WIS +10",
            "<Rank: C>\n<WIS: +10>"))
    a(armor(101, "Morgenwacht-Mantel", LIGHT_A, E_BODY, 8, 136, 0, "[Body · Light · C] The white coat of the Morgenwacht.\nArmor 8, ice x1/2",
            "<Rank: C>", [trait(22, 1, 0), trait(11, ICE, 0.5)]))


# =====================================================================================================================
# ENEMIES (61-160)
# =====================================================================================================================
EN = {}


def enemies(put, start):
    assert start == 61, start
    s = {**db.SK, **SKILLS}
    MS = {r: ITEMS["Manastein (%s)" % r] for r in "DCBA"}
    SE_ = db.IT["Manastein (E)"]
    def e(x):
        put(x)
        EN[x["name"]] = x["id"]
    # ---------------------------------------------------------------- ch.4 the Wall (party E -> D)
    e(enemy(61, "Höllenhund", "Hoellenhund", 220, stats(220, 210, 210, 120, 100, 190), 60, 60,
            [act(1, 4), act(s["Glutbiss"], 4), act(s["Höllenfeuer"], 2)],
            "<Rank: D>\n<Attack Die: d8>\n<Attack Stat: DEX>\n<Miasma>",
            drops=[drop(1, MS["D"], 4)], extra=[weak(LIGHT), trait(11, FIRE, 0.25), trait(11, DARK, 0.5)]))
    e(enemy(62, "Gargyl", "Gargyl", 240, stats(230, 190, 250, 120, 90, 150), 60, 50,
            [act(1, 5), act(s["Sturzflug"], 4), act(s["Steinhaut"], 1)],
            "<Rank: D>\n<Attack Die: d8>\n<Armor: 6>\n<Miasma>",
            drops=[drop(1, MS["D"], 5)], extra=[weak(THUNDER, 1.5), weak(LIGHT, 1.5), trait(11, DARK, 0.5)]))
    e(enemy(63, "Messinggolem", "Messinggolem", 240, stats(170, 90, 185, 80, 50, 60), 34, 20,
            [act(1, 5), act(s["Messingfaust"], 4)], "<Rank: E>\n<Attack Die: d10>\n<Armor: 8>",
            drops=[drop(1, SE_, 4)], extra=[weak(THUNDER, 2.0), trait(11, DARK, 0.0), trait(11, FIRE, 0.5)]))
    e(enemy(64, "Ghul", "Ghul", 150, stats(150, 140, 140, 60, 40, 80), 30, 10,
            [act(1, 5), act(s["Grabesgriff"], 3), act(s["Miasma Bite"], 3)],
            "<Rank: E>\n<Attack Die: d8>\n<Miasma>",
            drops=[drop(1, SE_, 6)], extra=[weak(LIGHT), weak(FIRE, 1.5), trait(11, DARK, 0.0)]))
    e(enemy(65, "Messingschreiber", "Messingschreiber", 700, stats(100, 170, 170, 170, 150, 190), 160, 150,
            [act(s["Federkiel"], 5), act(s["Vertragsklausel"], 3), act(s["Tintenstrahl"], 2), act(s["Eintreiben"], 2)],
            "<Rank: E>\n<Role: elite>\n<Attack Die: d6>\n<Attack Stat: DEX>",
            drops=[drop(1, SE_, 1)], extra=[weak(THUNDER, 1.5), weak(FIRE, 1.5)]))
    e(enemy(66, "Messingvogt", "Messingvogt", 1200, stats(280, 200, 290, 200, 260, 240), 500, 500,
            [act(1, 4), act(s["Schuldspruch"], 3), act(s["Messingkette"], 2), act(s["Eintreiben"], 2)],
            "<Rank: D>\n<Role: boss>\n<Attack Die: d10>\n<Armor: 8>",
            drops=[drop(1, MS["D"], 1), drop(3, ARMORS["Wallschild"], 1)], extra=[weak(THUNDER, 1.5)]))
    # ---------------------------------------------------------------- ch.5 Weißenfels (party D)
    e(enemy(67, "Wyvern", "Wyvern", 370, stats(300, 300, 230, 110, 100, 190), 65, 40,
            [act(1, 4), act(s["Giftstachel"], 4), act(s["Wing Buffet"], 2)],
            "<Rank: D>\n<Attack Die: d10>\n<Attack Stat: DEX>",
            drops=[drop(1, MS["D"], 4)], extra=[weak(ICE, 1.5), weak(THUNDER, 1.5)]))
    e(enemy(68, "Vampirknecht", "Vampirknecht", 390, stats(345, 375, 210, 150, 240, 310), 60, 70,
            [act(1, 4), act(s["Blutsaugen"], 4), act(s["Bannblick"], 2)],
            "<Rank: D>\n<Attack Die: d8>\n<Attack Stat: DEX>\n<Miasma>",
            drops=[drop(1, MS["D"], 5), drop(1, ITEMS["Elixier"], 6)],
            extra=[weak(LIGHT), weak(FIRE, 1.5), trait(11, DARK, 0.0)]))
    e(enemy(69, "Leere Hülle", "Leere_Huelle", 460, stats(435, 270, 270, 100, 60, 215), 60, 0,
            [act(1, 5), act(s["Shield Bash"], 3), act(s["Crushing Swing"], 2)],
            "<Rank: D>\n<Attack Die: d10>\n<Armor: 10>",
            drops=[drop(1, MS["D"], 5)], extra=[weak(THUNDER, 1.5), weak(LIGHT, 1.5), trait(11, DARK, 0.0)]))
    e(enemy(70, "Aschenschmied", "Aschenschmied", 1200, stats(420, 255, 340, 200, 220, 385), 680, 400,
            [act(s["Schmiedehammer"], 5), act(s["Glutfunken"], 3), act(s["Härten"], 1)],
            "<Rank: D>\n<Role: elite>\n<Attack Die: d10>\n<Armor: 8>",
            drops=[drop(1, MS["C"], 1), drop(2, WEAPONS["Messingbrecher"], 1)],
            extra=[weak(ICE, 1.5), trait(11, FIRE, 0.0)]))
    e(enemy(71, "Der Eiserne Prinz", "Eiserner_Prinz", 2400, stats(370, 305, 350, 260, 320, 220), 1200, 0,
            [act(s["Königsklinge"], 5), act(1, 3), act(s["Schildwall"], 1), act(s["Heerruf"], 1)],
            "<Rank: D>\n<Role: boss>\n<Attack Die: d10>\n<Armor: 10>",
            drops=[drop(1, MS["C"], 1)], extra=[weak(LIGHT, 1.5), trait(11, DARK, 0.5)]))
    # ---------------------------------------------------------------- ch.6 the siege (party D -> C)
    e(enemy(72, "Messingsoldat", "Messingsoldat", 340, stats(615, 495, 320, 150, 120, 200), 80, 60,
            [act(1, 4), act(s["Hellebarde"], 4), act(s["Shield Bash"], 2)],
            "<Rank: D>\n<Role: minion>\n<Attack Die: d10>\n<Armor: 8>",
            drops=[drop(1, MS["C"], 10)], extra=[weak(THUNDER, 1.5)]))
    e(enemy(73, "Oni-Söldner", "Oni", 570, stats(495, 350, 350, 150, 200, 170), 160, 150,
            [act(1, 4), act(s["Keulenschlag"], 4), act(s["Terrible Roar"], 1)],
            "<Rank: D>\n<Attack Die: d12>", drops=[drop(1, MS["C"], 6)], extra=[weak(LIGHT, 1.5)]))
    e(enemy(74, "Oni-Hauptmann", "Oni_Hauptmann", 1000, stats(330, 235, 370, 200, 300, 155), 520, 400,
            [act(1, 4), act(s["Keulenschlag"], 4), act(s["Heerruf"], 2), act(s["Terrible Roar"], 1)],
            "<Rank: D>\n<Role: elite>\n<Attack Die: d12>\n<Armor: 6>\n<Demon>",
            drops=[drop(1, MS["C"], 1)], extra=[weak(LIGHT, 1.5)]))
    e(enemy(75, "Seelenkessel", "Seelenkessel", 1450, stats(90, 45, 380, 300, 100, 340), 1500, 0,
            [act(s["Seelenstrom"], 5), act(s["Stand Still"], 1)],
            "<Rank: D>\n<Role: boss>\n<Armor: 10>\n<Demon>",
            drops=[drop(1, MS["C"], 1), drop(1, MS["C"], 1)], extra=[weak(LIGHT), weak(ICE, 1.5)]))
    e(enemy(76, "Gōen", "Goen", 99999, stats(760, 700, 760, 720, 790, 740), 0, 0,
            [act(s["Messingurteil"], 5), act(s["Seelenvertrag"], 3), act(s["Goldene Kette"], 2), act(s["Brass Toll"], 2)],
            "<Rank: SS>\n<Role: apex>\n<Attack Die: d12>\n<Armor: 20>\n<Demon>\n<Saves: STR, DEX, CON, WIS, CHA, MAG>",
            extra=[trait(11, DARK, 0.0)]))
    e(enemy(77, "Messingkoloss", "Messinggolem", 340, stats(470, 225, 280, 100, 60, 150), 65, 40,
            [act(1, 5), act(s["Messingfaust"], 4)], "<Rank: D>\n<Attack Die: d10>\n<Armor: 8>", hue=20,
            drops=[drop(1, MS["D"], 4)], extra=[weak(THUNDER, 2.0), trait(11, DARK, 0.0), trait(11, FIRE, 0.5)]))
    e(enemy(78, "Verwundeter Höllenhund", "Hoellenhund", 130, stats(200, 190, 190, 110, 90, 170), 50, 30,
            [act(1, 5), act(s["Glutbiss"], 3)],
            "<Rank: D>\n<Attack Die: d8>\n<Attack Stat: DEX>\n<Miasma>\nThe courier's escort wounded it.",
            drops=[drop(1, MS["D"], 1)], extra=[weak(LIGHT), trait(11, FIRE, 0.25), trait(11, DARK, 0.5)]))
    from story import foes3
    foes3.enemies(put, 79)


# =====================================================================================================================
# TROOPS (61-200)
# =====================================================================================================================
TR = {}
Y = db.Y


def troops(put, start):
    assert start == 61, start
    e = {**EN, **__import__('story.foes3', fromlist=['EN']).EN}
    def t(name, members, pages=None):
        tid = put(name, members, pages)
        TR[name] = tid
        return tid
    # ---- chapter 4
    t("Höllenhund", [(e["Verwundeter Höllenhund"], 408, Y)])
    t("Raid: Aschenhunde", [(db.EN["Aschenhund"], 220, Y), (db.EN["Aschenhund"], 420, Y + 10), (db.EN["Aschenhund"], 620, Y)])
    t("Gargyl", [(e["Gargyl"], 408, Y - 40)])
    t("Gargyl & Aschenhund", [(db.EN["Aschenhund"], 320, Y), (e["Gargyl"], 540, Y - 40)])
    t("Höllenhund & Aschenhunde", [(db.EN["Aschenhund"], 220, Y), (e["Höllenhund"], 420, Y + 10), (db.EN["Aschenhund"], 620, Y)])
    t("Gargylen x2", [(e["Gargyl"], 300, Y - 40), (e["Gargyl"], 520, Y - 40)])
    t("Gargyl & Aschenhunde", [(db.EN["Aschenhund"], 220, Y), (e["Gargyl"], 420, Y - 40), (db.EN["Aschenhund"], 620, Y)])
    t("Gargylen x3", [(e["Gargyl"], 220, Y - 40), (e["Gargyl"], 420, Y - 20), (e["Gargyl"], 620, Y - 40)])
    t("Gargyl & Höllenhund", [(e["Höllenhund"], 320, Y), (e["Gargyl"], 540, Y - 40)])
    t("Messinggolems x2", [(e["Messinggolem"], 300, Y), (e["Messinggolem"], 520, Y)])
    t("Ghule x3", [(e["Ghul"], 220, Y), (e["Ghul"], 420, Y + 6), (e["Ghul"], 620, Y)])
    t("Ghule & Golem", [(e["Ghul"], 220, Y), (e["Messinggolem"], 420, Y + 6), (e["Ghul"], 620, Y)])
    t("Messingschreiber", [(e["Messinggolem"], 220, Y), (e["Messingschreiber"], 430, Y - 20)])
    # the night raid: Kanta takes the chain meant for Rin -> breakthrough to D (turn 2)
    vogt = npc_speaker("Messingvogt", "", 0)
    bt = Ev()
    bt.say(vogt, ["Clause fourteen. Collection."])
    bt.se('Chain', 90, 70)
    bt.text(["The chain of coins uncoils past the party, a whip of", "brass, straight at Rin by the gate."],
            background=1, position=1)
    bt.say(RIN, ["—!"])
    bt.se('Damage5')
    bt.flash((255, 200, 90, 170), 20)
    bt.text(["Kanta is already in its way. The chain wraps her sigil", "arm, and brass crawls up her skin like frost."],
            background=1, position=1)
    bt.say(HANMA, ["My Lord! Don't let it write on you!"], 'command')
    bt.se('Magic3', 90, 80)
    bt.flash((200, 230, 255, 255), 60)
    bt.text(["The sigils answer. White light boils the brass off her", "arm and the coins burst like hot glass. The light in",
             "her hand grows long and heavy: a blade, then a lance."], background=1, position=1)
    bt.breakthrough()
    bt.say(KANTA, ["You don't get her."], 'fierce')
    bt.se('Explosion1', 70, 130)
    bt.add(331, [1, 1, 0, 250, False])
    bt.text(["The broken chain whips back into the Messingvogt, and", "its ledger-robes smoke where the light touched them."],
            background=1, position=1)
    bt.say(FALIN, ["Good. Now it bleeds. Everyone on the bailiff!"], 'fierce')
    # once only: a rematch after a defeat must not break through a second time
    S_BT_D = SW('C4: Breakthrough D')
    bt.switch(S_BT_D)
    bt = Ev().if_switch(S_BT_D, False, lambda b, inner=bt: b.splice(inner))
    t("Messingvogt", [(db.EN["Aschenhund"], 200, Y), (e["Messingvogt"], 430, Y + 20)], [db.troop_page(bt, turn=(2, 0))])
    # ---- chapter 5
    t("Wyvern", [(e["Wyvern"], 408, Y - 20)])
    t("Wyverns x2", [(e["Wyvern"], 300, Y - 30), (e["Wyvern"], 540, Y - 30)])
    t("Gargyl & Wyvern", [(e["Heeresgargyl"], 300, Y - 40), (e["Wyvern"], 540, Y - 20)])
    t("Vampirknechte x2", [(e["Vampirknecht"], 300, Y), (e["Vampirknecht"], 520, Y)])
    t("Ghule & Knecht", [(e["Grabghul"], 220, Y), (e["Vampirknecht"], 420, Y + 6), (e["Grabghul"], 620, Y)])
    t("Leere Hüllen x2", [(e["Leere Hülle"], 300, Y), (e["Leere Hülle"], 520, Y)])
    t("Hülle & Koloss", [(e["Leere Hülle"], 300, Y), (e["Messingkoloss"], 520, Y)])
    t("Kettenkolonne", [(e["Vampirknecht"], 300, Y), (e["Leere Hülle"], 530, Y)])
    t("Aschenschmied", [(e["Leere Hülle"], 200, Y), (e["Aschenschmied"], 430, Y + 20)])
    t("Der Eiserne Prinz", [(e["Leere Hülle"], 190, Y), (e["Der Eiserne Prinz"], 420, Y + 20), (e["Leere Hülle"], 650, Y)])
    # ---- chapter 6
    t("Messingsoldaten x3", [(e["Messingsoldat"], 220, Y), (e["Messingsoldat"], 420, Y + 6), (e["Messingsoldat"], 620, Y)])
    t("Soldaten & Oni", [(e["Messingsoldat"], 220, Y), (e["Oni-Söldner"], 430, Y + 10), (e["Messingsoldat"], 630, Y)])
    t("Oni x2", [(e["Oni-Söldner"], 300, Y), (e["Oni-Söldner"], 520, Y)])
    t("Höllenhunde x2", [(e["Heereshund"], 300, Y), (e["Heereshund"], 520, Y)])
    t("Gargylen & Soldat", [(e["Heeresgargyl"], 220, Y - 40), (e["Messingsoldat"], 420, Y), (e["Heeresgargyl"], 620, Y - 40)])
    t("Oni-Hauptmann", [(e["Oni-Söldner"], 200, Y), (e["Oni-Hauptmann"], 430, Y + 10), (e["Messingsoldat"], 650, Y)])
    t("Seelenkessel", [(e["Messingkoloss"], 180, Y), (e["Seelenkessel"], 420, Y + 20), (e["Messingkoloss"], 660, Y)])
    from story import ch6
    t("Gōen", [(e["Gōen"], 408, Y + 30)], [db.troop_page(ev, turn=tn) for ev, tn in ch6.goen_troop_pages()])
    from story import foes3
    foes3.troops(put)
