"""Act III: the foes of chapters 7-9 (skills 228-300, enemies 79-130, troops after chapter 6's), key items 72-.

Rank bands: ch.7 C (LV 31-40, breakthrough to B at the Web-Weaver), ch.8 B (41-47), ch.9 B->A (47-55,
breakthrough to A against Gōen). EXP follows the story's curve (about a quarter of the rank table's suggestion).
The Calamities are <Demon>: each Dawn Regalia the party holds cancels one rank of difference against them."""
from story import db
from story.common import Ev, KANTA, HANMA, FALIN, npc_speaker, SW
from story.cast import YUKINO
from story.db import (eff, trait, skill, enemy, act, drop, stats, weak, item,
                      ADD_STATE, REMOVE_STATE, BUFF, DEBUFF, REC_HP,
                      FIRE, ICE, THUNDER, WATER, EARTH, WIND, LIGHT, DARK,
                      ST_DAZZLED, ST_FEAR, ST_PRONE, ST_CHILL, ST_PINNED, ST_BURN, ST_SEALED, ST_WEBBED,
                      ST_DROWNING, ST_ASHBURN, ST_FROZEN, ST_VEILED)

IMAGES = {
    "Strassenraeuber": dict(src="Mercenary", f=1.0, hue=200, sat=0.8),
    "Spinnenagent": dict(src="SF_Agent", f=1.0, sat=0.4, tint=(90, 60, 110, 0.25)),
    "Sturmharpyie": dict(src="Harpy", f=1.0, hue=160),
    "Arenasoeldner": dict(src="Mercenary", f=1.05),
    "Eiserner_Bruder": dict(src="Berserker", f=1.1),
    "Arenabestie": dict(src="Hydra", f=1.25, hue=300),
    "Klingenmeisterin": dict(src="Captain", f=1.05),
    "Kampfmagier": dict(src="Sorcerer", f=1.05),
    "Schattenklinge": dict(src="Darkelf", f=1.05, hue=180, sat=0.7),
    "Arenachampion": dict(src="Actor1_3", f=1.2),
    "Hoehlenspinne": dict(src="Mechascorpion", f=1.1, sat=0.3, tint=(80, 50, 90, 0.5), dark=0.85),
    "Seidenkokon": dict(src="Oddegg", f=1.0, sat=0.0, tint=(220, 220, 200, 0.4)),
    "Spinnenklinge": dict(src="SF_Hannyamask", f=1.05),
    "Tsumugi": dict(src="Medusa", f=1.3, hue=40, sat=0.9),
    "Werwolf": dict(src="Wolfman", f=1.15),
    "Rudelherr": dict(src="SF_Whitewolf", f=1.4, hue=250, sat=0.6, dark=0.8),
    "Irrlicht": dict(src="SF_Will_o_the_wisp", f=0.9, hue=60),
    "Junger_Kitsune": dict(src="Foxman", f=0.8, hue=20),
    "Shirogane": dict(src="Foxman", f=1.35),
    "Urwaldhueter": dict(src="Treant", f=1.2),
    "Waldgeist": dict(src="Sylph", f=1.0),
    "Grubenwicht": dict(src="Gnome", f=1.0, hue=120, sat=0.6),
    "Hoehlentroll": dict(src="SF_Armygorilla", f=1.25, hue=90, sat=0.7),
    "Trollschamane": dict(src="SF_Armymonkey", f=1.2, hue=90, sat=0.7),
    "Trollkoenig": dict(src="SF_Armygorilla", f=1.6, hue=60, sat=0.8, dark=0.9),
    "Hohler_Diener": dict(src="Zombie", f=1.0, sat=0.2, tint=(120, 140, 120, 0.3)),
    "Leerer_Magier": dict(src="Wraith", f=1.05),
    "Grimoire": dict(src="Evilbook", f=1.3, hue=100),
    "Mukuro": dict(src="Lich", f=1.5),
    "Ertrunkener": dict(src="Sailor", f=1.0, sat=0.3, tint=(80, 140, 130, 0.45), dark=0.85),
    "Sirene": dict(src="Siren", f=1.1),
    "Riffkrabbe": dict(src="Crab", f=1.0, hue=160),
    "Ketos": dict(src="Ketos", f=1.2),
    "Fomorer": dict(src="SF_Kappa", f=1.1, hue=200, sat=0.8),
    "Fomorer_Haeuptling": dict(src="SF_Kappa", f=1.6, hue=160, sat=0.9, dark=0.85),
    "Kraken": dict(src="Kraken", f=1.3),
    "Shigure": dict(src="Actor2_1", f=1.4, hue=-20, sat=0.8, tint=(60, 110, 140, 0.25)),
    "Glutsalamander": dict(src="Salamander", f=1.1),
    "Aschenphoenix": dict(src="SF_Phoenix", f=1.1, sat=0.5, dark=0.75),
    "Messinggardist": dict(src="Gatekeeper", f=1.15, sat=0.0, tint=(196, 150, 62, 0.55)),
    "Goen_Final": dict(src="SF_Enmadaio", f=1.35, hue=15),
    "Kagero": dict(src="Demoncount", f=1.4),
    "Hokai": dict(src="Evilgod", f=1.3),
    "Toma": dict(src="Actor3_1", f=1.35, sat=0.6, dark=0.85),
}

SKILLS = {}


def skills(put, start):
    assert start == 228, start
    def en(sid, name, **kw):
        kw.setdefault("stype", 0)
        kw.setdefault("occasion", 1)
        kw.setdefault("crit", True)
        put(skill(sid, name, **kw))
        SKILLS[name] = sid
    put(db.sep(228, "----- Foes (Act III)"))
    # ---- chapter 7: the road, the arena, the spiders
    en(229, "Giftdolch", scope=1, dtype=1, element=1, formula="d8", hit=1, anim=11, icon=76,
       effects=[eff(ADD_STATE, 4, 0.5)], msg="%1 strikes with a poisoned dagger!", note="<Stat: DEX>")
    en(230, "Netzwurf", scope=1, anim=12, icon=10, crit=False, effects=[eff(ADD_STATE, ST_WEBBED, 1.0)],
       msg="%1 throws a weighted net!", note="<Stat: DEX>\n<Save: DEX>")
    en(231, "Arenahieb", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=6, icon=97,
       msg="%1 swings for the crowd!", note="<Stat: STR>")
    en(232, "Hydrabiss", scope=4, dtype=1, element=1, formula="d8", hit=1, anim=16, icon=76, repeats=3,
       msg="%1 strikes with every head!", note="<Stat: STR>\n<Area Rate: 100%>")
    en(233, "Feuerball", scope=2, dtype=1, element=FIRE, formula="d10", hit=0, anim=66, icon=64, crit=False,
       effects=[eff(ADD_STATE, ST_BURN, 0.3)], msg="%1 hurls a ball of fire!", note="<Stat: MAG>\n<Save: DEX>")
    en(234, "Schattenschnitt", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=6, icon=97,
       msg="%1 cuts from the shadows!", note="<Stat: DEX>\n<Crit Range: +2>")
    en(235, "Kriegsschrei", scope=8, anim=37, icon=32, crit=False, effects=[eff(BUFF, 2, 3)],
       msg="%1 roars a war cry!", note="<Stat: CHA>")
    en(236, "Seidenfaden", scope=2, dtype=1, element=1, formula="d8", hit=0, anim=12, icon=10, crit=False,
       effects=[eff(ADD_STATE, ST_WEBBED, 0.6)], msg="%1 spins threads through the air!",
       note="<Stat: DEX>\n<Save: DEX>")
    en(237, "Giftbiss", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=16, icon=76,
       effects=[eff(ADD_STATE, 4, 0.6)], msg="%1 bites with dripping fangs!", note="<Stat: STR>")
    en(238, "Kokonfessel", scope=1, anim=12, icon=10, crit=False, effects=[eff(ADD_STATE, ST_WEBBED, 1.0)],
       msg="%1 wraps a victim in silk!", note="<Stat: DEX>\n<Save: STR>")
    en(239, "Schuldschein", scope=1, dtype=1, element=DARK, formula="d12", hit=2, anim=58, icon=71,
       effects=[eff(ADD_STATE, ST_SEALED, 0.5)], msg="%1 calls in a debt!", note="<Stat: MAG>\n<Save: WIS states>")
    # ---- chapter 8: the forest, the mines, the hollow magus
    en(240, "Mondheulen", scope=8, anim=37, icon=34, crit=False, effects=[eff(BUFF, 2, 3), eff(BUFF, 6, 3)],
       msg="%1 howls at a moon that isn't there!", note="<Stat: CHA>")
    en(241, "Fuchsfeuer", scope=1, dtype=1, element=FIRE, formula="d10", hit=2, anim=66, icon=64,
       msg="%1 conjures foxfire!", note="<Stat: MAG>")
    en(242, "Blendwerk", scope=2, anim=40, icon=3, crit=False, effects=[eff(ADD_STATE, ST_DAZZLED, 1.0)],
       msg="%1 weaves an illusion!", note="<Stat: CHA>\n<Save: WIS>")
    en(243, "Wurzelgriff", scope=1, dtype=1, element=EARTH, formula="d10", hit=1, anim=39, icon=68,
       effects=[eff(ADD_STATE, ST_PINNED, 0.6)], msg="%1 grabs with roots!", note="<Stat: STR>\n<Save: STR states>")
    en(244, "Trollkeule", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=39, icon=77,
       effects=[eff(ADD_STATE, ST_PRONE, 0.5)], msg="%1 swings a tree trunk!", note="<Stat: STR>\n<Save: STR states>")
    en(245, "Nachwachsen", scope=11, dtype=3, formula="d12", anim=41, icon=72, crit=False,
       msg="%1's wounds close over!", note="<Stat: CON>\n<Damage: 200%>")
    en(246, "Horngesang", scope=2, anim=37, icon=11, crit=False, effects=[eff(ADD_STATE, ST_FEAR, 1.0)],
       msg="The horn on %1's belt sings in the draught!", note="<Stat: CHA>\n<Save: WIS>")
    en(247, "Todeshauch", scope=2, dtype=1, element=DARK, formula="d12", hit=0, anim=101, icon=71, crit=False,
       msg="%1 breathes the air of the grave!", note="<Stat: MAG>\n<Save: CON>")
    en(248, "Seelenriss", scope=1, dtype=1, element=DARK, formula="d12", hit=2, anim=59, icon=71,
       effects=[eff(ADD_STATE, ST_SEALED, 0.5)], msg="%1 tears at a soul!", note="<Stat: MAG>\n<Save: WIS states>")
    en(249, "Toter Wille", scope=8, anim=58, icon=71, crit=False, effects=[eff(BUFF, 2, 3), eff(BUFF, 3, 3)],
       msg="%1 lends the dead his will!", note="<Stat: MAG>")
    # ---- chapter 9: the sea, the fire, the end
    en(250, "Flutspeer", scope=1, dtype=1, element=WATER, formula="d12", hit=1, anim=11, icon=67,
       effects=[eff(ADD_STATE, ST_DROWNING, 0.4)], msg="%1 drives a lance of black water!",
       note="<Stat: STR>\n<Crit Range: +1>")
    en(251, "Sturmflut", scope=2, dtype=1, element=WATER, formula="d10", hit=0, anim=91, icon=67, crit=False,
       effects=[eff(ADD_STATE, ST_DROWNING, 0.3)], msg="%1 calls the sea over the deck!",
       note="<Stat: MAG>\n<Save: STR>")
    en(252, "Sirenengesang", scope=2, anim=58, icon=6, crit=False, effects=[eff(ADD_STATE, 10, 0.5)],
       msg="%1 sings, and the world goes soft!", note="<Stat: CHA>\n<Save: WIS>")
    en(253, "Scherenzange", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=16, icon=76,
       effects=[eff(ADD_STATE, ST_PINNED, 0.5)], msg="%1 pinches!", note="<Stat: STR>\n<Save: STR states>")
    en(254, "Tentakelschlag", scope=4, dtype=1, element=1, formula="d10", hit=1, anim=39, icon=77, repeats=2,
       msg="%1 lashes with its tentacles!", note="<Stat: STR>\n<Area Rate: 100%>")
    en(255, "Glutodem", scope=2, dtype=1, element=FIRE, formula="d10", hit=0, anim=66, icon=64, crit=False,
       effects=[eff(ADD_STATE, ST_BURN, 0.4)], msg="%1 breathes embers!", note="<Stat: MAG>\n<Save: DEX>")
    en(256, "Aschenflügel", scope=2, dtype=1, element=FIRE, formula="d8", hit=0, anim=66, icon=64, crit=False,
       effects=[eff(ADD_STATE, ST_ASHBURN, 0.4)], msg="%1 beats wings of burning ash!", note="<Stat: MAG>\n<Save: CON>")
    en(257, "Schwarzes Feuer", scope=2, dtype=1, element=DARK, formula="d12", hit=0, anim=101, icon=71, crit=False,
       effects=[eff(ADD_STATE, ST_ASHBURN, 0.3)], msg="%1 burns the world with black fire!",
       note="<Stat: MAG>\n<Save: CON>")
    en(258, "Heldenklinge", scope=1, dtype=1, element=1, formula="d12", hit=1, anim=6, icon=97,
       msg="%1 cuts like the hero he was!", note="<Stat: STR>\n<Damage: 150%>\n<Crit Range: +1>")
    en(259, "Hōkais Ruf", scope=2, anim=58, icon=11, crit=False,
       effects=[eff(ADD_STATE, ST_FEAR, 0.8), eff(ADD_STATE, ST_ASHBURN, 0.5)],
       msg="Something speaks through %1, and it is very old!", note="<Stat: CHA>\n<Save: WIS>")
    en(260, "Leere", scope=2, dtype=1, element=DARK, formula="2d10", hit=0, anim=101, icon=71, crit=False,
       msg="%1 opens a hole in the world!", note="<Stat: MAG>\n<Save: CON>")
    en(261, "Aschenschritt", scope=1, dtype=1, element=DARK, formula="d12", hit=1, anim=6, icon=97,
       msg="%1 steps through the ash and strikes!", note="<Stat: DEX>\n<Crit Range: +1>")


EN = {}


def enemies(put, start):
    assert start == 79, start
    s = {**db.SK, **__import__('story.foes', fromlist=['SKILLS']).SKILLS, **SKILLS}
    F = __import__('story.foes', fromlist=['ITEMS'])
    MS = {r: F.ITEMS["Manastein (%s)" % r] for r in "DCBA"}
    I = F.ITEMS
    def e(x):
        put(x)
        EN[x["name"]] = x["id"]
    # ------------------------------------------------ ch.7 the Kaiserstraße, the arena, the Unterhallen (party C)
    e(enemy(79, "Straßenräuber", "Strassenraeuber", 380, stats(320, 300, 320, 180, 180, 60), 110, 180,
            [act(1, 5), act(s["Netzwurf"], 2), act(s["Shield Bash"], 2)], "<Rank: C>\n<Attack Die: d10>\n<Armor: 6>",
            drops=[drop(1, MS["C"], 10), drop(1, I["Elixier"], 6)]))
    e(enemy(80, "Spinnenkreis-Agent", "Spinnenagent", 340, stats(260, 360, 300, 220, 240, 200), 120, 220,
            [act(1, 4), act(s["Giftdolch"], 4), act(s["Netzwurf"], 2)],
            "<Rank: C>\n<Attack Die: d8>\n<Attack Stat: DEX>", drops=[drop(1, MS["C"], 8)]))
    e(enemy(81, "Sturmharpyie", "Sturmharpyie", 330, stats(280, 360, 280, 160, 200, 200), 100, 60,
            [act(s["Claw"], 5), act(s["Wing Buffet"], 3)], "<Rank: C>\n<Attack Die: d8>\n<Attack Stat: DEX>",
            drops=[drop(1, MS["C"], 10)], extra=[weak(THUNDER, 1.5)]))
    e(enemy(82, "Arena-Söldner", "Arenasoeldner", 420, stats(340, 300, 340, 180, 200, 80), 140, 0,
            [act(1, 4), act(s["Arenahieb"], 4)], "<Rank: C>\n<Attack Die: d10>\n<Armor: 6>"))
    e(enemy(83, "Eiserner Bruder", "Eiserner_Bruder", 520, stats(380, 280, 380, 160, 220, 60), 170, 0,
            [act(1, 4), act(s["Arenahieb"], 4), act(s["Kriegsschrei"], 1)], "<Rank: C>\n<Attack Die: d12>\n<Armor: 6>"))
    e(enemy(84, "Arenabestie", "Arenabestie", 1700, stats(440, 360, 460, 200, 260, 300), 800, 0,
            [act(1, 3), act(s["Hydrabiss"], 4), act(s["Feuerball"], 2)],
            "<Rank: B>\n<Role: elite>\n<Attack Die: d10>\n<Armor: 8>", extra=[weak(ICE, 1.5)]))
    e(enemy(85, "Klingenmeisterin", "Klingenmeisterin", 560, stats(430, 440, 420, 260, 300, 120), 380, 0,
            [act(1, 4), act(s["Arenahieb"], 3), act(s["Kriegsschrei"], 1)], "<Rank: B>\n<Attack Die: d10>\n<Armor: 8>"))
    e(enemy(86, "Kampfmagier", "Kampfmagier", 480, stats(220, 360, 380, 420, 340, 460), 380, 0,
            [act(s["Feuerball"], 4), act(s["Ice Lance"], 3), act(1, 1)], "<Rank: B>\n<Attack Die: d6>"))
    e(enemy(87, "Schattenklinge", "Schattenklinge", 500, stats(360, 460, 380, 260, 280, 200), 380, 0,
            [act(s["Schattenschnitt"], 5), act(s["Giftdolch"], 3)],
            "<Rank: B>\n<Attack Die: d10>\n<Attack Stat: DEX>"))
    e(enemy(88, "Kanemoto Gōki", "Arenachampion", 3400, stats(470, 420, 470, 260, 380, 200), 1800, 5000,
            [act(1, 3), act(s["Arenahieb"], 5), act(s["Kriegsschrei"], 1), act(s["Crushing Swing"], 2)],
            "<Rank: B>\n<Role: boss>\n<Attack Die: d12>\n<Armor: 10>"))
    e(enemy(89, "Höhlenspinne", "Hoehlenspinne", 420, stats(330, 380, 340, 180, 160, 200), 130, 0,
            [act(s["Giftbiss"], 5), act(s["Netzwurf"], 2)], "<Rank: C>\n<Attack Die: d10>\n<Miasma>",
            drops=[drop(1, MS["C"], 8)], extra=[weak(FIRE, 1.5), weak(LIGHT, 1.5)]))
    e(enemy(90, "Seidenkokon", "Seidenkokon", 300, stats(40, 40, 360, 200, 60, 200), 60, 0,
            [act(s["Stand Still"], 5)], "<Rank: C>\n<Role: minion>\n<Armor: 4>\nA cocoon. Someone is inside.",
            extra=[weak(FIRE, 2.0)]))
    e(enemy(91, "Spinnenkreis-Klinge", "Spinnenklinge", 560, stats(400, 460, 400, 260, 280, 220), 380, 300,
            [act(s["Schattenschnitt"], 4), act(s["Giftdolch"], 3), act(s["Netzwurf"], 2)],
            "<Rank: B>\n<Attack Die: d10>\n<Attack Stat: DEX>", drops=[drop(1, MS["B"], 10)]))
    e(enemy(92, "Tsumugi", "Tsumugi", 4200, stats(360, 480, 440, 480, 500, 480), 2400, 0,
            [act(s["Seidenfaden"], 4), act(s["Schuldschein"], 3), act(s["Kokonfessel"], 2), act(s["Giftbiss"], 2)],
            "<Rank: B>\n<Role: boss>\n<Attack Die: d10>\n<Attack Stat: DEX>\n<Armor: 8>\n<Demon>\n"
            "Under the Morgendom the dawn seal presses on her: here she is only rank B.",
            extra=[weak(FIRE, 1.5), weak(LIGHT, 1.5), trait(11, DARK, 0.5)]))
    # ------------------------------------------------ ch.8 the Tiefenwald, Eisenberg (party B)
    e(enemy(93, "Werwolf", "Werwolf", 560, stats(440, 440, 420, 200, 280, 100), 380, 0,
            [act(1, 4), act(s["Twin Claws"], 3), act(s["Mondheulen"], 1)],
            "<Rank: B>\n<Attack Die: d10>\n<Attack Stat: DEX>", drops=[drop(1, MS["B"], 12)],
            extra=[trait(11, 1, 0.5), weak(LIGHT, 1.5)]))
    e(enemy(94, "Rudelherr", "Rudelherr", 1500, stats(470, 480, 460, 240, 360, 120), 900, 0,
            [act(1, 3), act(s["Twin Claws"], 4), act(s["Mondheulen"], 2), act(s["Terrible Roar"], 1)],
            "<Rank: B>\n<Role: elite>\n<Attack Die: d10>\n<Attack Stat: DEX>\n<Miasma>",
            drops=[drop(1, MS["B"], 2)], extra=[trait(11, 1, 0.5), weak(LIGHT)]))
    e(enemy(95, "Irrlicht", "Irrlicht", 260, stats(100, 460, 260, 400, 200, 440), 190, 0,
            [act(s["Blendwerk"], 3), act(s["Fuchsfeuer"], 4)], "<Rank: B>\n<Role: minion>\n<Attack Die: d6>",
            extra=[weak(ICE, 1.5)]))
    e(enemy(96, "Junger Kitsune", "Junger_Kitsune", 480, stats(280, 460, 380, 400, 420, 440), 380, 0,
            [act(s["Fuchsfeuer"], 4), act(s["Blendwerk"], 2), act(s["Claw"], 2)],
            "<Rank: B>\n<Attack Die: d8>\n<Attack Stat: DEX>", extra=[weak(ICE, 1.5)]))
    e(enemy(97, "Shirogane", "Shirogane", 2600, stats(360, 520, 460, 500, 540, 520), 0, 0,
            [act(s["Fuchsfeuer"], 4), act(s["Blendwerk"], 3), act(s["Twin Claws"], 2)],
            "<Rank: B>\n<Role: elite>\n<Attack Die: d10>\n<Attack Stat: DEX>\n<Saves: DEX, WIS, CHA, MAG>\n"
            "Eight of her nine tails are bound: she plays fair.", extra=[weak(ICE, 1.5)]))
    e(enemy(98, "Urwaldhüter", "Urwaldhueter", 640, stats(450, 200, 480, 300, 260, 300), 400, 0,
            [act(1, 4), act(s["Wurzelgriff"], 4)], "<Rank: B>\n<Attack Die: d10>\n<Armor: 8>",
            drops=[drop(1, MS["B"], 12)], extra=[weak(FIRE, 2.0)]))
    e(enemy(99, "Waldgeist", "Waldgeist", 460, stats(200, 460, 360, 420, 400, 460), 360, 0,
            [act(s["Sickle Wind"], 4), act(s["Blendwerk"], 2)], "<Rank: B>\n<Attack Die: d8>\n<Attack Stat: DEX>",
            extra=[weak(FIRE, 1.5)]))
    e(enemy(100, "Grubenwicht", "Grubenwicht", 300, stats(300, 400, 320, 260, 200, 300), 190, 200,
            [act(1, 4), act(s["Kornstaub"], 2)], "<Rank: B>\n<Role: minion>\n<Attack Die: d8>",
            drops=[drop(1, MS["B"], 20)]))
    e(enemy(101, "Höhlentroll", "Hoehlentroll", 760, stats(480, 220, 500, 160, 200, 120), 420, 60,
            [act(1, 4), act(s["Trollkeule"], 4), act(s["Nachwachsen"], 1)],
            "<Rank: B>\n<Attack Die: d12>\n<Armor: 6>\nTrolls regrow anything but burns.",
            drops=[drop(1, MS["B"], 10)], extra=[weak(FIRE, 2.0), trait(22, 7, 0.04)]))
    e(enemy(102, "Trollschamane", "Trollschamane", 620, stats(380, 300, 440, 420, 380, 440), 420, 60,
            [act(s["Todeshauch"], 3), act(s["Nachwachsen"], 2), act(1, 3)], "<Rank: B>\n<Attack Die: d8>",
            extra=[weak(FIRE, 2.0), trait(22, 7, 0.03)]))
    e(enemy(103, "Trollkönig", "Trollkoenig", 5600, stats(520, 300, 540, 200, 400, 200), 3400, 8000,
            [act(s["Trollkeule"], 5), act(1, 3), act(s["Horngesang"], 2), act(s["Nachwachsen"], 1)],
            "<Rank: B>\n<Role: boss>\n<Attack Die: d12>\n<Armor: 10>\nIt wears the old dwarf-king's helm.",
            extra=[weak(FIRE, 1.5), trait(22, 7, 0.03)]))
    e(enemy(104, "Hohler Diener", "Hohler_Diener", 380, stats(420, 200, 400, 100, 60, 200), 190, 0,
            [act(1, 5), act(s["Grabesgriff"], 3)], "<Rank: B>\n<Role: minion>\n<Attack Die: d10>\n<Miasma>",
            extra=[weak(LIGHT), weak(FIRE, 1.5), trait(11, DARK, 0.0)]))
    e(enemy(105, "Leerer Magier", "Leerer_Magier", 520, stats(200, 380, 400, 460, 300, 480), 400, 0,
            [act(s["Todeshauch"], 3), act(s["Seelenriss"], 3), act(s["Ice Lance"], 2)],
            "<Rank: B>\n<Attack Die: d6>\n<Miasma>", drops=[drop(1, MS["B"], 10)],
            extra=[weak(LIGHT), trait(11, DARK, 0.0)]))
    e(enemy(106, "Grimoire", "Grimoire", 480, stats(160, 380, 420, 480, 300, 500), 380, 0,
            [act(s["Vertragsklausel"], 2), act(s["Seelenriss"], 3), act(s["Tintenstrahl"], 2)],
            "<Rank: B>\n<Attack Die: d6>", extra=[weak(FIRE, 2.0)]))
    e(enemy(107, "Mukuro", "Mukuro", 7400, stats(300, 480, 520, 680, 600, 680), 6000, 0,
            [act(s["Todeshauch"], 4), act(s["Seelenriss"], 4), act(s["Toter Wille"], 1), act(s["Ice Lance"], 2)],
            "<Rank: S>\n<Role: boss>\n<Attack Die: d8>\n<Armor: 8>\n<Demon>\n<Miasma>",
            extra=[weak(LIGHT, 1.5), trait(11, DARK, 0.0)]))
    # ------------------------------------------------ ch.9 the sea, the fire, the end (party B -> A)
    e(enemy(108, "Ertrunkener", "Ertrunkener", 700, stats(560, 400, 560, 200, 200, 300), 1200, 0,
            [act(1, 5), act(s["Grabesgriff"], 3), act(s["Sturmflut"], 1)],
            "<Rank: A>\n<Role: minion>\n<Attack Die: d10>\n<Miasma>", drops=[drop(1, MS["A"], 20)],
            extra=[weak(THUNDER, 1.5), weak(LIGHT, 1.5), trait(11, WATER, 0.0)]))
    e(enemy(109, "Sirene", "Sirene", 820, stats(300, 560, 520, 560, 600, 580), 1300, 0,
            [act(s["Sirenengesang"], 3), act(s["Sturmflut"], 3), act(s["Ice Lance"], 2)],
            "<Rank: A>\n<Attack Die: d8>", extra=[weak(THUNDER, 1.5), trait(11, WATER, 0.0)]))
    e(enemy(110, "Riffkrabbe", "Riffkrabbe", 960, stats(580, 360, 620, 200, 200, 200), 1300, 0,
            [act(1, 4), act(s["Scherenzange"], 4)], "<Rank: A>\n<Attack Die: d12>\n<Armor: 12>",
            drops=[drop(1, MS["A"], 12)], extra=[weak(THUNDER, 2.0), trait(11, WATER, 0.5)]))
    e(enemy(111, "Ketos", "Ketos", 2800, stats(600, 460, 620, 300, 400, 500), 3200, 0,
            [act(1, 3), act(s["Sturmflut"], 3), act(s["Bite"], 3)], "<Rank: A>\n<Role: elite>\n<Attack Die: d12>",
            drops=[drop(1, MS["A"], 2)], extra=[weak(THUNDER, 1.5), trait(11, WATER, 0.0)]))
    e(enemy(112, "Fomorer", "Fomorer", 900, stats(580, 420, 580, 200, 300, 260), 1300, 400,
            [act(1, 5), act(s["Trollkeule"], 3)], "<Rank: A>\n<Attack Die: d12>\n<Armor: 8>",
            drops=[drop(1, MS["A"], 12)], extra=[weak(LIGHT, 1.5)]))
    e(enemy(113, "Fomorer-Häuptling", "Fomorer_Haeuptling", 9000, stats(640, 440, 660, 300, 520, 400), 6000, 20000,
            [act(s["Trollkeule"], 4), act(1, 3), act(s["Terrible Roar"], 1), act(s["Glutodem"], 2)],
            "<Rank: A>\n<Role: boss>\n<Attack Die: d12>\n<Armor: 12>\nThe Aschenkrone burns him. He wears it anyway.",
            extra=[weak(LIGHT, 1.5), weak(ICE, 1.5)]))
    e(enemy(114, "Kraken", "Kraken", 3000, stats(620, 420, 640, 300, 360, 480), 3200, 0,
            [act(s["Tentakelschlag"], 5), act(s["Sturmflut"], 2)], "<Rank: A>\n<Role: elite>\n<Attack Die: d10>",
            extra=[weak(THUNDER, 2.0), trait(11, WATER, 0.0)]))
    e(enemy(115, "Shigure", "Shigure", 9600, stats(700, 620, 680, 400, 520, 560), 8000, 0,
            [act(s["Flutspeer"], 5), act(s["Sturmflut"], 3), act(1, 2)],
            "<Rank: S>\n<Role: boss>\n<Attack Die: d12>\n<Armor: 12>\n<Demon>",
            extra=[weak(THUNDER, 1.5), trait(11, WATER, 0.0)]))
    e(enemy(116, "Glutsalamander", "Glutsalamander", 860, stats(560, 480, 560, 300, 300, 560), 1300, 0,
            [act(1, 4), act(s["Glutodem"], 4)], "<Rank: A>\n<Attack Die: d10>",
            drops=[drop(1, MS["A"], 12)], extra=[weak(ICE, 2.0), trait(11, FIRE, 0.0)]))
    e(enemy(117, "Aschenphönix", "Aschenphoenix", 900, stats(400, 600, 520, 400, 460, 600), 1400, 0,
            [act(s["Aschenflügel"], 4), act(s["Sturzflug"], 3)], "<Rank: A>\n<Attack Die: d10>\n<Attack Stat: DEX>\n<Miasma>",
            extra=[weak(ICE, 1.5), trait(11, FIRE, 0.0)]))
    e(enemy(118, "Messinggardist", "Messinggardist", 980, stats(600, 420, 620, 300, 300, 200), 1300, 300,
            [act(1, 4), act(s["Hellebarde"], 4), act(s["Shield Bash"], 2)], "<Rank: A>\n<Attack Die: d12>\n<Armor: 12>",
            drops=[drop(1, MS["A"], 10)], extra=[weak(THUNDER, 1.5)]))
    e(enemy(119, "Gōen, der Messingtyrann", "Goen_Final", 21000, stats(760, 700, 760, 720, 790, 740), 15000, 0,
            [act(s["Messingurteil"], 5), act(s["Seelenvertrag"], 3), act(s["Goldene Kette"], 2), act(s["Brass Toll"], 2)],
            "<Rank: SS>\n<Role: apex>\n<Attack Die: d12>\n<Armor: 16>\n<Demon>\n<Saves: STR, CON, WIS, CHA, MAG>",
            extra=[trait(11, DARK, 0.0), weak(LIGHT, 1.5)]))
    e(enemy(120, "Maō Kagerō", "Kagero", 17000, stats(800, 760, 800, 740, 760, 800), 0, 0,
            [act(s["Schwarzes Feuer"], 4), act(s["Aschenschritt"], 4), act(s["Heldenklinge"], 2)],
            "<Rank: SS>\n<Role: apex>\n<Attack Die: d12>\n<Armor: 16>\n<Demon>\n<Veil of Ash>",
            extra=[trait(11, DARK, 0.0), weak(LIGHT, 1.5)]))
    e(enemy(121, "Hōkais Schatten", "Hokai", 14000, stats(600, 600, 820, 800, 820, 840), 0, 0,
            [act(s["Leere"], 4), act(s["Hōkais Ruf"], 3), act(s["Todeshauch"], 3)],
            "<Rank: SS>\n<Role: apex>\n<Armor: 14>\n<Demon>\nThe thing in the miasma that spoke to Tōma.",
            extra=[trait(11, DARK, 0.0), weak(LIGHT, 2.0)]))
    e(enemy(122, "Kurenai Tōma", "Toma", 9000, stats(700, 700, 680, 500, 600, 500), 0, 0,
            [act(s["Heldenklinge"], 5), act(1, 3), act(s["Aschenschritt"], 2)],
            "<Rank: S>\n<Role: boss>\n<Attack Die: d12>\n<Armor: 12>\n<Demon>\nThe man under the Demon Lord.",
            extra=[weak(LIGHT, 1.5)]))


TR = {}


def troops(put):
    Y = db.Y
    e = {**__import__('story.foes', fromlist=['EN']).EN, **EN}
    def t(name, members, pages=None):
        tid = put(name, members, pages)
        TR[name] = tid
        return tid
    # ---- chapter 7
    t("Straßenräuber x3", [(e["Straßenräuber"], 220, Y), (e["Straßenräuber"], 420, Y + 6), (e["Straßenräuber"], 620, Y)])
    t("Räuber & Agent", [(e["Straßenräuber"], 300, Y), (e["Spinnenkreis-Agent"], 530, Y)])
    t("Sturmharpyien x2", [(e["Sturmharpyie"], 300, Y - 40), (e["Sturmharpyie"], 530, Y - 40)])
    t("Agenten x2", [(e["Spinnenkreis-Agent"], 300, Y), (e["Spinnenkreis-Agent"], 530, Y)])
    t("Runde 1: Eiserne Brüder", [(e["Arena-Söldner"], 220, Y), (e["Eiserner Bruder"], 420, Y + 6),
                                  (e["Arena-Söldner"], 620, Y)])
    t("Runde 2: Arenabestie", [(e["Arenabestie"], 408, Y + 30)])
    t("Runde 3: Klingen von Ostmark", [(e["Klingenmeisterin"], 220, Y), (e["Kampfmagier"], 420, Y + 6),
                                       (e["Schattenklinge"], 620, Y)])
    gk = Ev()
    gk.say(npc_speaker("Kanemoto Gōki", "People2", 4), ["Eight years champion. Let's see if a vessel bleeds."])
    t("Finale: Kanemoto Gōki", [(e["Arena-Söldner"], 200, Y), (e["Kanemoto Gōki"], 430, Y + 20),
                                (e["Arena-Söldner"], 650, Y)], [db.troop_page(gk, turn=(0, 0))])
    t("Höhlenspinnen x3", [(e["Höhlenspinne"], 220, Y), (e["Höhlenspinne"], 420, Y + 6), (e["Höhlenspinne"], 620, Y)])
    t("Spinnen & Kokon", [(e["Höhlenspinne"], 250, Y), (e["Seidenkokon"], 430, Y + 10), (e["Höhlenspinne"], 610, Y)])
    t("Klinge & Agenten", [(e["Spinnenkreis-Agent"], 220, Y), (e["Spinnenkreis-Klinge"], 420, Y + 6),
                           (e["Spinnenkreis-Agent"], 620, Y)])
    t("Spinnenkreis-Klingen x2", [(e["Spinnenkreis-Klinge"], 300, Y), (e["Spinnenkreis-Klinge"], 530, Y)])
    S_BB = SW('C7: Breakthrough B')
    def tsumugi_break(bt):
        bt.say(npc_speaker("Tsumugi", "People2", 1), ["Clause one: the little vessel's light belongs to the",
                                                      "Web. It was written before you woke, darling."])
        bt.se('Twine', 90, 80)
        bt.text(["Silk wraps Kanta from shoulder to heel and pulls tight.", "Somewhere above, the Morgendom's bells begin to ring."],
                background=1, position=1)
        bt.say(HANMA, ["My Lord! The dawn seal is right above us: use it!"], 'command')
        bt.se('Magic3', 90, 80)
        bt.flash((255, 240, 200, 255), 60)
        bt.text(["The sigils drink the light of the seal. The silk burns",
                 "away, and the light that comes back out of Kanta is no",
                 "longer one weapon or three, but a ring of them."], background=1, position=1)
        bt.breakthrough()
        bt.say(KANTA, ["I didn't sign anything."], 'fierce')
        bt.say(npc_speaker("Tsumugi", "People2", 1), ["…That's not in the contract."])
        bt.switch(S_BB)
    bt = Ev().if_switch(S_BB, False, tsumugi_break)
    t("Tsumugi", [(e["Seidenkokon"], 190, Y), (e["Tsumugi"], 420, Y + 20), (e["Seidenkokon"], 650, Y)],
      [db.troop_page(bt, turn=(2, 0))])
    # ---- chapter 8
    t("Werwölfe x2", [(e["Werwolf"], 300, Y), (e["Werwolf"], 530, Y)])
    t("Werwolf & Irrlichter", [(e["Irrlicht"], 220, Y - 40), (e["Werwolf"], 420, Y + 6), (e["Irrlicht"], 620, Y - 40)])
    t("Rudelherr", [(e["Werwolf"], 200, Y), (e["Rudelherr"], 430, Y + 20), (e["Werwolf"], 650, Y)])
    t("Kitsune x2", [(e["Junger Kitsune"], 300, Y), (e["Junger Kitsune"], 530, Y)])
    t("Kitsune & Irrlicht", [(e["Junger Kitsune"], 300, Y), (e["Irrlicht"], 530, Y - 40)])
    yield_ = Ev()
    yield_.say(npc_speaker("Shirogane", "Monster", 4), ["Ahaha! Enough, enough! I haven't bled in two hundred", "years."])
    yield_.add(340, [])
    t("Shirogane", [(e["Shirogane"], 408, Y + 20)], [db.troop_page(yield_, enemy_hp=(0, 40))])
    t("Urwaldhüter x2", [(e["Urwaldhüter"], 300, Y), (e["Urwaldhüter"], 530, Y)])
    t("Hüter & Geister", [(e["Waldgeist"], 220, Y - 20), (e["Urwaldhüter"], 420, Y + 6), (e["Waldgeist"], 620, Y - 20)])
    t("Grubenwichte x3", [(e["Grubenwicht"], 220, Y), (e["Grubenwicht"], 420, Y + 6), (e["Grubenwicht"], 620, Y)])
    t("Höhlentrolle x2", [(e["Höhlentroll"], 300, Y), (e["Höhlentroll"], 530, Y)])
    t("Troll & Schamane", [(e["Höhlentroll"], 300, Y), (e["Trollschamane"], 530, Y)])
    tk = Ev()
    tk.se('Horn', 90, 70)
    tk.text(["The horn on the Troll King's belt sings as it moves, a", "sound like a hundred men far away."],
            background=1, position=1)
    t("Trollkönig", [(e["Höhlentroll"], 200, Y), (e["Trollkönig"], 430, Y + 30), (e["Trollschamane"], 650, Y)],
      [db.troop_page(tk, turn=(0, 0))])
    t("Hohle Diener x3", [(e["Hohler Diener"], 220, Y), (e["Hohler Diener"], 420, Y + 6), (e["Hohler Diener"], 620, Y)])
    t("Magier & Diener", [(e["Hohler Diener"], 250, Y), (e["Leerer Magier"], 430, Y + 6), (e["Hohler Diener"], 610, Y)])
    t("Grimoires & Magier", [(e["Grimoire"], 250, Y - 20), (e["Leerer Magier"], 430, Y + 6), (e["Grimoire"], 610, Y - 20)])
    mk = Ev()
    mk.say(npc_speaker("Mukuro", "Evil", 2), ["Three regalia. Three. How did a vessel get three?"])
    mk.say(HANMA, ["They pierce you, magus. Feel it."], 'stern')
    t("Mukuro", [(e["Hohler Diener"], 190, Y), (e["Mukuro"], 420, Y + 20), (e["Leerer Magier"], 650, Y)],
      [db.troop_page(mk, turn=(0, 0))])
    # ---- chapter 9
    t("Ertrunkene x3", [(e["Ertrunkener"], 220, Y), (e["Ertrunkener"], 420, Y + 6), (e["Ertrunkener"], 620, Y)])
    t("Sirenen x2", [(e["Sirene"], 300, Y - 20), (e["Sirene"], 530, Y - 20)])
    t("Krabben x2", [(e["Riffkrabbe"], 300, Y), (e["Riffkrabbe"], 530, Y)])
    t("Fomorer x2", [(e["Fomorer"], 300, Y), (e["Fomorer"], 530, Y)])
    t("Fomorer & Sirene", [(e["Fomorer"], 300, Y), (e["Sirene"], 530, Y - 20)])
    t("Ketos", [(e["Ketos"], 408, Y + 20)])
    sh = Ev()
    sh.say(YUKINO, ["…Shigure. You were our lance."])
    sh.say(npc_speaker("Shigure", "Actor2", 0), ["Was I? …The sea is so loud, Yuki. I can't hear anything",
                                                 "else any more."])
    t("Shigure", [(e["Kraken"], 250, Y), (e["Shigure"], 470, Y + 20)], [db.troop_page(sh, turn=(0, 0))])
    fc = Ev()
    fc.say(HANMA, ["The Aschenkrone. It hates him. He wears it anyway,", "because it frightens the others."], 'stern')
    t("Fomorer-Häuptling", [(e["Fomorer"], 200, Y), (e["Fomorer-Häuptling"], 430, Y + 30), (e["Fomorer"], 650, Y)],
      [db.troop_page(fc, turn=(0, 0))])
    t("Salamander x2", [(e["Glutsalamander"], 300, Y), (e["Glutsalamander"], 530, Y)])
    t("Phönix & Salamander", [(e["Aschenphönix"], 300, Y - 30), (e["Glutsalamander"], 530, Y)])
    t("Gardisten x2", [(e["Messinggardist"], 300, Y), (e["Messinggardist"], 530, Y)])
    t("Gardist & Phönix", [(e["Messinggardist"], 300, Y), (e["Aschenphönix"], 530, Y - 30)])
    from story import ch9
    t("Gōen (Urwald)", [(e["Gōen, der Messingtyrann"], 408, Y + 30)], ch9.goen_final_pages())
    t("Kagerō", [(e["Maō Kagerō"], 408, Y + 30)], ch9.kagero_pages(1))
    t("Hōkais Schatten", [(e["Hōkais Schatten"], 408, Y + 30)], ch9.kagero_pages(2))
    t("Kurenai Tōma", [(e["Kurenai Tōma"], 408, Y + 20)], ch9.kagero_pages(3))


KEY = {}


def key_items(put, start):
    assert start == 72, start
    key = lambda iid, name, icon, desc: item(iid, name, icon, 0, desc, [], scope=0, occasion=3, anim=0, itype=2,
                                            consumable=False)
    def k(i):
        put(i)
        KEY[i["name"]] = i["id"]
    k(key(72, "Turniermarke", 187, "A bronze token: a Guild team entered in the Sonnwende-\nTurnier at the Kaiserarena."))
    k(key(73, "Spinnensiegel", 314, "Black wax, a spider pressed into it. The Spinnenkreis\nseals its contracts with it."))
    k(key(74, "Gildenabschrift", 192, "Kirishima Daigo's copy of the Guild record of 313:\nwhere the Dawn Regalia were scattered."))
    k(key(75, "Seekarte", 191, "Kaizaki Rui's chart of the Sturmsee and the Knochenriff."))
    k(key(76, "Ruis Pfand", 189, "Rui's promise, in her own words: to the reef, and then\nto Shigure."))
