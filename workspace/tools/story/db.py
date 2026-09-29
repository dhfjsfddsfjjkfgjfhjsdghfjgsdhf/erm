"""The story database: skills, items, gear, states, classes, actors, enemies, troops, common events, system."""
import copy
from story.common import *

MAGIC_ST, SPIRIT_ST, BODY_ST, PASSIVE_ST, BATTLEMAGIC_ST, FROST_ST = 1, 2, 3, 4, 5, 6          # skill types
ADD_STATE, REMOVE_STATE, BUFF, DEBUFF, REC_HP, REC_MP = 21, 22, 31, 32, 11, 12
FIRE, ICE, THUNDER, WATER, EARTH, WIND, LIGHT, DARK = 2, 3, 4, 5, 6, 7, 8, 9
DIVINE_W, GLOVE_W, SWORD_W, FLAIL_W, AXE_W, SPEAR_W, DAGGER_W, STAFF_W = 13, 11, 2, 3, 4, 12, 1, 6
GEN, MAGA, LIGHT_A, HEAVY_A, SSHIELD, LSHIELD, UNIFORM_A, FUSED_A = 1, 2, 3, 4, 5, 6, 7, 8
E_WEAPON, E_SHIELD, E_HEAD, E_BODY, E_ACC = 1, 2, 3, 4, 5
RANKS = ["F", "E", "D", "C", "B", "A", "S", "SS", "SSS", "V"]

def eff(code, data, v1=1.0, v2=0):
    return {"code": code, "dataId": data, "value1": v1, "value2": v2}

def trait(code, data, value):
    return {"code": code, "dataId": data, "value": value}

# =====================================================================
# STATES
# =====================================================================
ST_BARRIER, ST_DAZZLED, ST_DEFLECT, ST_MASTERY, ST_STEADY, ST_FEAR, ST_CHALLENGE, ST_INTERPOSE, ST_BRACED, \
    ST_PRONE, ST_FUSED, ST_CHILL, ST_MIASMA, ST_CLEANSED = range(31, 45)
# the party's full kits (Kanta 45-62, Hanma 63-68, Falin 69-78, shared 79-)
ST_RADIANT, ST_FLOAT, ST_GUARDIAN, ST_LENT, ST_BLADEWALL, ST_RIPOSTE, ST_PINNED, ST_AIRBORNE, ST_TWINFLOAT, \
    ST_ARMORBREAK, ST_MIMIC, ST_RING, ST_BLINK, ST_UNSEEN, ST_ANYFORM, ST_ENDLESS, ST_SPENT, ST_OPENARMORY = range(45, 63)
ST_EYE, ST_FORWARD, ST_SWIFT, ST_BANNER, ST_COMMANDED, ST_EXHAUSTED = range(63, 69)
ST_WARDED, ST_STEEL, ST_ROARED, ST_BASTION, ST_BURDEN, ST_MOUNTAIN, ST_STEELHIDE, ST_BLOOM, ST_FORTRESS, \
    ST_LASTBASTION = range(69, 79)
ST_PURGED, ST_DAWN = range(79, 81)
# the foes of Acts II and III
ST_BURN, ST_SEALED, ST_WEBBED, ST_DROWNING, ST_ASHBURN, ST_FROZEN = range(81, 87)
# the guests of Acts II-III (Yukino) and the last act
ST_FROSTBODY, ST_MORGENWACHT, ST_VEILED = range(87, 90)
# conditions a full cleanse ends (default Poison, Blind, Silence, Confusion, Charm, Sleep, Paralysis, Stun + ours)
NEGATIVE = [4, 5, 6, 8, 9, 10, 12, 13, ST_DAZZLED, ST_FEAR, ST_PRONE, ST_CHILL, ST_PINNED]

def state(sid, name, icon, note="", traits=None, timing=2, turns=(1, 1), restriction=0, msgs=("", "", "", ""),
          battle_end=True, priority=50, motion=0, overlay=0):
    return {"id": sid, "autoRemovalTiming": timing, "chanceByDamage": 100, "iconIndex": icon, "maxTurns": turns[1],
            "message1": msgs[0], "message2": msgs[1], "message3": msgs[2], "message4": msgs[3], "minTurns": turns[0],
            "motion": motion, "name": name, "note": note, "overlay": overlay, "priority": priority,
            "releaseByDamage": False, "removeAtBattleEnd": battle_end, "removeByDamage": False,
            "removeByRestriction": False, "removeByWalking": False, "restriction": restriction, "stepsToRemove": 100,
            "traits": traits or [], "messageType": 1}

def build_states():
    S = load_orig('States')
    S[5]["note"] = "<Hit: -4>"
    S[4]["removeAtBattleEnd"] = False           # poison lingers
    new = [
        state(ST_BARRIER, "Barrier", 128, timing=0, priority=10, msgs=("", "", "", "")),
        state(ST_DAZZLED, "Dazzled", 3, "<Hit: -5>", turns=(1, 1),
              msgs=("%1 is dazzled!", "%1 is dazzled!", "", "%1 can see again.")),
        state(ST_DEFLECT, "Deflecting", 81, "<AC: +4>", turns=(1, 1),
              msgs=("%1 raises a guard of light.", "", "", "")),
        state(ST_MASTERY, "Combat Mastery", 0, "<Crit Range: +1>", [trait(23, 9, 1.2)], timing=0, battle_end=False),
        state(ST_STEADY, "Steady, Soldier", 0, "", [trait(13, ST_FEAR, 0.5)], timing=0, battle_end=False),
        state(ST_FEAR, "Frightened", 11, "<Hit: -3>", turns=(2, 3),
              msgs=("%1 is frightened!", "%1 is frightened!", "", "%1 steadies.")),
        state(ST_CHALLENGE, "Challenging", 5, "", [trait(23, 0, 6.0)], turns=(2, 2),
              msgs=("%1 dares them to try!", "", "", "")),
        state(ST_INTERPOSE, "Interposing", 128, "<Interpose>", turns=(1, 1),
              msgs=("%1 stands in front of the others.", "", "", "")),
        state(ST_BRACED, "Braced", 81, "", [trait(23, 6, 0.5), trait(23, 7, 0.5)], turns=(1, 1),
              msgs=("%1 braces.", "", "", "")),
        state(ST_PRONE, "Prone", 10, "<AC: -3>\n<Hit: -2>", turns=(1, 1),
              msgs=("%1 is knocked down!", "%1 is knocked down!", "", "%1 gets up.")),
        state(ST_FUSED, "Fused Plate", 0, "", [trait(14, ST_PRONE, 1)], timing=0, battle_end=False),
        state(ST_CHILL, "Chilled", 65, "<DEX: -20>", turns=(2, 3),
              msgs=("%1 is chilled to the bone!", "%1 is chilled!", "", "%1 warms up.")),
        state(ST_MIASMA, "Miasma-Touched", 71, "<All Stats: +50>\n<Miasma>", [trait(11, LIGHT, 2.0), trait(11, DARK, 0.5)],
              timing=0, battle_end=False),
        state(ST_CLEANSED, "Burned Clean", 72, "<All Stats: -50>", timing=0,
              msgs=("The miasma smokes off %1!", "The miasma smokes off %1!", "", "")),
    ]
    P = dict(timing=0, battle_end=False)            # passive: no icon, never runs out
    new += [
        # ---- Kanta: Divine Weaponry
        state(ST_RADIANT, "Radiant Edge", 0, "", [trait(31, LIGHT, 0)], **P),
        state(ST_FLOAT, "Float", 0, "<Float Strikes: 1>", **P),
        state(ST_GUARDIAN, "Guardian Blade", 81, "<Guardian Blade>", turns=(3, 3),
              msgs=("Blades of light circle %1's allies.", "", "", "The guardian blades fade.")),
        state(ST_LENT, "Lent Blade", 97, "<Lent Blade: d8>", [trait(31, LIGHT, 0)], turns=(5, 5),
              msgs=("A blade of light settles into %1's hand.", "", "", "The lent blade fades.")),
        state(ST_BLADEWALL, "Blade Wall", 129, "<AC: +2>\n<DEX Save: +2>\n<Concentration>", turns=(5, 5),
              msgs=("A ring of blades spins around %1.", "", "", "The blade wall stops.")),
        state(ST_RIPOSTE, "Halo Riposte", 0, "<Riposte>", **P),
        state(ST_PINNED, "Pinned", 10, "<AC: -4>\n<Hit: -4>", turns=(2, 3),
              msgs=("%1 is pinned by a spike of light!", "%1 is pinned!", "", "%1 tears free.")),
        state(ST_AIRBORNE, "Blade Ride", 36, "<AC: +3>\n<Hit: +2>\n<Concentration>", [trait(14, ST_PRONE, 1)],
              turns=(5, 5), msgs=("%1 rides a blade into the air!", "", "", "%1 comes down.")),
        state(ST_TWINFLOAT, "Floating Pair", 0, "<Float Strikes: 1>", **P),
        state(ST_ARMORBREAK, "Armor-Breaker", 0, "<Hit: +5>", **P),
        state(ST_MIMIC, "Mimic Arms", 0, "<Crit Range: +1>\n<Hit: +1>", **P),
        state(ST_RING, "Sanctuary Ring", 97, "<Ring Strike>\n<Concentration>", turns=(5, 5),
              msgs=("A ring of blades closes around the field.", "", "", "The sanctuary ring falls.")),
        state(ST_BLINK, "Blink Blade", 0, "<Blink>", **P),
        state(ST_UNSEEN, "Unseen Armory", 0, "<Hit: +3>", **P),
        state(ST_ANYFORM, "Any Form", 0, "<Crit Range: +1>", [trait(34, 0, 1)], **P),
        state(ST_ENDLESS, "Endless Guard", 0, "<Guardian Blade: all>", **P),
        state(ST_SPENT, "Armory Spent", 4, "", [trait(42, MAGIC_ST, 0)], timing=0,
              msgs=("Every blade is spent.", "", "", "")),
        state(ST_OPENARMORY, "Open Armory", 0, "<Hit: +2>", [trait(31, LIGHT, 0)], **P),
        # ---- Hanma
        state(ST_EYE, "Old General's Eye", 0, "<Init: +2>", **P),
        state(ST_FORWARD, "Forward!", 32, "<Hit: +4>\n<Init: +5>", turns=(1, 1),
              msgs=("%1 surges forward!", "", "", "")),
        state(ST_SWIFT, "Swift Mercy", 0, "", [trait(61, 0, 1.0)], **P),
        state(ST_BANNER, "Banner of the Dead", 0, "", [trait(14, ST_FEAR, 1), trait(11, DARK, 0.75)], **P),
        state(ST_COMMANDED, "Commanded", 36, "", [trait(61, 0, 1.0)], turns=(2, 2),
              msgs=("%1 hears the last command.", "", "", "")),
        state(ST_EXHAUSTED, "Spent", 8, "", restriction=4, turns=(2, 2),
              msgs=("%1 gives everything she has.", "", "", "%1 stands again.")),
        # ---- Falin
        state(ST_WARDED, "Vanguard", 81, "<Warded>", turns=(1, 1),
              msgs=("Falin plants herself beside %1.", "", "", "")),
        state(ST_STEEL, "Living Steel", 0, "<Rank Regen: 2%>", **P),
        state(ST_ROARED, "Roared", 5, "<Taunted>", timing=1, turns=(1, 1),
              msgs=("%1 can't look away from Falin!", "%1 can't look away from Falin!", "", "%1 shakes off the roar.")),
        state(ST_BASTION, "Bastion", 0, "<AC: +2>\n<DEX Save: +2>", **P),
        state(ST_BURDEN, "Shared Burden", 128, "<Burden Share>\n<Concentration>", turns=(5, 5),
              msgs=("Falin takes a share of %1's wounds.", "", "", "")),
        state(ST_MOUNTAIN, "Mountain Stance", 33, "<Taunt Aura>\n<Concentration>", [trait(14, ST_PRONE, 1)],
              turns=(5, 5), msgs=("%1 becomes a mountain.", "", "", "%1 moves again.")),
        state(ST_STEELHIDE, "Steel Hide", 0, "", [trait(23, 6, 0.5)], **P),
        state(ST_BLOOM, "Plate Bloom", 129, "<AC: +5>\n<DEX Save: +5>\n<Concentration>", turns=(5, 5),
              msgs=("Steel unfolds over %1.", "", "", "The steel folds back.")),
        state(ST_FORTRESS, "Living Fortress", 0, "<AC: +5>\n<Interpose Magic>", **P),
        state(ST_LASTBASTION, "Last Bastion", 128, "<Interpose All>\n<Unkillable>", turns=(1, 1),
              msgs=("%1 stands in front of everyone.", "", "", "")),
        # ---- shared
        state(ST_PURGED, "Purged", 72, "<All Stats: -50>", turns=(3, 3),
              msgs=("The miasma burns out of %1!", "The miasma burns out of %1!", "", "The miasma creeps back.")),
        state(ST_DAWN, "Dawn's Favor", 70, "<All Stats: +30>", timing=0, battle_end=True,
              msgs=("The dawn light falls on %1.", "", "", "")),
        # ---- foes' conditions (Acts II-III)
        state(ST_BURN, "Burning", 64, "", [trait(22, 7, -0.06)], turns=(3, 3),
              msgs=("%1 catches fire!", "%1 catches fire!", "", "%1's flames go out.")),
        state(ST_SEALED, "Sealed", 4, "", [trait(42, 1, 0), trait(42, 2, 0), trait(42, 3, 0)], turns=(2, 2),
              msgs=("A brass clause binds %1's power!", "A brass clause binds %1's power!", "", "%1's power returns.")),
        state(ST_WEBBED, "Webbed", 10, "<DEX: -30%>\n<Hit: -3>", turns=(2, 3),
              msgs=("Threads wrap around %1!", "Threads wrap around %1!", "", "%1 tears free of the web.")),
        state(ST_DROWNING, "Drowning", 67, "", [trait(22, 7, -0.05), trait(22, 8, -0.1)], turns=(3, 3),
              msgs=("Black water fills %1's lungs!", "Black water fills %1's lungs!", "", "%1 coughs up the sea.")),
        state(ST_ASHBURN, "Ash-Burned", 71, "<All Stats: -20>", [trait(22, 7, -0.08)], turns=(3, 3),
              msgs=("Ash eats into %1!", "Ash eats into %1!", "", "The ash burns out.")),
        state(ST_FROZEN, "Frozen", 65, "", restriction=4, turns=(1, 2),
              msgs=("%1 freezes solid!", "%1 freezes solid!", "", "%1 thaws.")),
        # ---- Yukino
        state(ST_FROSTBODY, "Frost Body", 0, "", [trait(11, ICE, 0.5), trait(14, ST_CHILL, 1), trait(14, ST_FROZEN, 1)], **P),
        state(ST_MORGENWACHT, "Morgenwacht", 0, "<Hit: +2>\n<Save Bonus: +2>", **P),
        # ---- the Demon Lord's veil (Act III finale; the scripted phases add and remove it)
        state(ST_VEILED, "Veil of Ash", 71, "<AC: +10>", [trait(11, 1, 0.1)], timing=0,
              msgs=("Ash closes around %1 like a cloak.", "", "", "The veil of ash tears open!")),
    ]
    while len(S) < 31:
        S.append(None)
    S = S[:31] + new
    return S

# =====================================================================
# SKILLS
# =====================================================================
def skill(sid, name, stype=0, mp=0, scope=1, dtype=0, element=0, formula="0", hit=0, anim=0, icon=0,
          desc="", note="", effects=None, msg="%1 uses %2!", speed=0, occasion=1, crit=False, success=100, repeats=1):
    return {"id": sid, "animationId": anim,
            "damage": {"critical": crit, "elementId": element, "formula": formula, "type": dtype, "variance": 0},
            "description": desc, "effects": effects or [], "hitType": hit, "iconIndex": icon,
            "message1": msg, "message2": "", "mpCost": mp, "name": name, "note": note, "occasion": occasion,
            "repeats": repeats, "requiredWtypeId1": 0, "requiredWtypeId2": 0, "scope": scope, "speed": speed,
            "stypeId": stype, "successRate": success, "tpCost": 0, "tpGain": 0, "messageType": 1}

def sep(sid, name):
    return skill(sid, name, occasion=3, scope=0, msg="")

def passive(sid, name, icon, desc, note, stype=PASSIVE_ST):
    return skill(sid, name, stype, scope=0, occasion=3, icon=icon, desc=desc, note=note + "\n<No Mastery>", msg="")

SK = {}   # name -> id

def build_skills():
    orig = load_orig('Skills')
    attack = copy.deepcopy(orig[1])
    attack["note"] = "Attack command: weapon die + POW(weapon stat) + 10 x weapon rank. Never gains mastery."
    guard = copy.deepcopy(orig[2])
    L = [None, attack, guard]

    def put(s):
        assert s["id"] == len(L), (s["id"], len(L), s["name"])
        L.append(s)
        SK[s["name"]] = s["id"]

    # ---------------------------------------------------------- Kanta (3-15)
    put(sep(3, "----- Kanta"))
    put(skill(4, "Piercing Ray", MAGIC_ST, mp=5, scope=1, dtype=1, element=-1, formula="d8", hit=1, anim=115, icon=70,
              crit=True, msg="%1's light lances out!",
              desc="The beam lances out for one strike: d8 + DEX, +2 to hit.\nd10 at mastery E, two strikes at C.",
              note="<Stat: DEX>\n<Hit: +2>\n<At Rank E>\ndie: d10\n</At Rank E>\n<At Rank C>\nhits: 2\n</At Rank C>"))
    put(skill(5, "Glare", MAGIC_ST, mp=4, scope=1, anim=40, icon=88, speed=10, msg="%1's weapon flares!",
              effects=[eff(ADD_STATE, ST_DAZZLED, 1.0)],
              desc="The light flares in a foe's eyes: CON save or Dazzled\n(-5 to hit) for a turn. Acts early.",
              note="<Stat: MAG>\n<Save: CON>\n<Support>"))
    put(skill(6, "Deflect", MAGIC_ST, mp=2, scope=11, anim=51, icon=81, speed=2000, msg="%1 turns the light into a guard.",
              effects=[eff(ADD_STATE, ST_DEFLECT, 1.0)],
              desc="Acts first: +4 AC until the round ends.\nA Body technique (half cost).",
              note="<Stat: DEX>\n<Body>\n<Support>"))
    put(passive(7, "Combat Mastery", 78,
                "Passive. Kanta learns and fights faster than others:\n+20% EXP, Divine Weaponry crits on 19-20.",
                "<Passive State: %d>" % ST_MASTERY))
    put(skill(8, "Returning Fang", MAGIC_ST, mp=5, scope=4, dtype=1, element=-1, formula="d6", hit=1, anim=26, icon=96,
              crit=True, msg="%1 throws the light-dagger!",
              desc="The thrown dagger strikes, returns and strikes again:\ntwo random foes, full d6 + DEX each.",
              note="<Stat: DEX>\n<Start Rank: E>\n<Area Rate: 100%>\n<Attack Roll>"))
    put(skill(9, "Shadow Stitch", MAGIC_ST, mp=5, scope=1, dtype=1, element=-1, formula="d6", hit=1, anim=12, icon=96,
              crit=True, effects=[eff(DEBUFF, 6, 2)], msg="%1 pins a shadow with light!",
              desc="A dagger through the foe's shadow: d6 + DEX, STR save\nor its DEX drops (slower, easier to hit).",
              note="<Stat: DEX>\n<Start Rank: E>\n<Save: STR states>"))
    while len(L) < 16:
        put(sep(len(L), ""))
    # ---------------------------------------------------------- Hanma (16-27)
    put(sep(16, "----- Hanma"))
    put(skill(17, "Heal", SPIRIT_ST, mp=5, scope=7, dtype=3, formula="d8", anim=41, icon=72, occasion=0,
              msg="%1 mends the wound.", desc="Life: heals one ally for d8 + WIS.\nd10 at mastery E.",
              note="<Stat: WIS>\n<At Rank E>\ndie: d10\n</At Rank E>"))
    put(skill(18, "Reverse Heal", SPIRIT_ST, mp=5, scope=1, dtype=1, element=DARK, formula="d8", hit=0, anim=101,
              icon=71, msg="%1 turns healing inside out!",
              desc="Death: d8 + MAG necrotic, CON save for half.\nOnly living things rot; the dead shrug it off.",
              note="<Stat: MAG>\n<Save: CON>"))
    put(passive(19, "Steady, Soldier", 73,
                "Passive aura. Allies who can hear her resist fear\n(half the chance to be Frightened).",
                "<Party Aura: %d>" % ST_STEADY))
    put(skill(20, "Rally", SPIRIT_ST, mp=5, scope=8, anim=53, icon=87, speed=10, msg="%1 rallies the line!",
              effects=[eff(REMOVE_STATE, ST_FEAR, 1.0)],
              desc="Every ally gains a barrier of (d6 + CHA) x 1/2 that\nabsorbs damage first, and shakes off fear.",
              note="<Stat: CHA>\n<Barrier: d6 50%>\n<Support>"))
    put(skill(21, "Triage", SPIRIT_ST, mp=5, scope=8, dtype=3, formula="d8", anim=43, icon=72, occasion=0,
              msg="%1 moves from wound to wound.", desc="Heals every ally for half a Heal (d8 + WIS) x 1/2.",
              note="<Stat: WIS>\n<Start Rank: E>"))
    while len(L) < 28:
        put(sep(len(L), ""))
    # ---------------------------------------------------------- Falin (28-39)
    put(sep(28, "----- Falin"))
    put(passive(29, "Fused Plate", 136,
                "Passive. Her armor is her body: heavy natural armor that\ngrows with her rank. She can't be knocked prone.",
                "<Passive State: %d>" % ST_FUSED))
    put(skill(30, "Challenge", BODY_ST, mp=2, scope=11, anim=37, icon=5, speed=20, msg="%1 bellows a challenge!",
              effects=[eff(ADD_STATE, ST_CHALLENGE, 1.0)],
              desc="Draws every foe's eye: enemies aim at Falin for\ntwo turns. Acts early.",
              note="<Stat: STR>\n<Body>\n<Support>"))
    put(skill(31, "Interpose", BODY_ST, mp=2, scope=11, anim=51, icon=81, speed=2000, msg="%1 steps in front.",
              effects=[eff(ADD_STATE, ST_INTERPOSE, 1.0)],
              desc="Acts first: until the round ends, physical attacks\naimed at her allies hit Falin instead.",
              note="<Stat: CON>\n<Body>\n<Support>"))
    put(skill(32, "Crushing Blow", BODY_ST, mp=2, scope=1, dtype=1, element=-1, formula="d10", hit=1, anim=39, icon=77,
              crit=True, effects=[eff(ADD_STATE, ST_PRONE, 1.0)], msg="%1 brings a plated fist down!",
              desc="d10 + STR with a plated fist. On a hit: STR save or\nthe foe is knocked prone (-3 AC, -2 to hit).",
              note="<Stat: STR>\n<Body>\n<Save: STR states>"))
    put(skill(33, "Brace", BODY_ST, mp=5, scope=11, anim=52, icon=128, speed=2000, msg="%1 braces for the blow.",
              effects=[eff(ADD_STATE, ST_BRACED, 1.0)],
              desc="Acts first: halves the damage of every hit Falin\ntakes this round.",
              note="<Stat: CON>\n<Body>\n<Start Rank: E>\n<Support>"))
    while len(L) < 40:
        put(sep(len(L), ""))
    # ---------------------------------------------------------- enemies (40-)
    put(sep(40, "----- Enemies"))
    def en(sid, name, **kw):
        kw.setdefault("stype", 0)
        kw.setdefault("occasion", 1)
        kw.setdefault("crit", True)
        put(skill(sid, name, **kw))
    en(41, "Bite", scope=1, dtype=1, element=1, formula="d6", hit=1, anim=16, icon=76, msg="%1 bites!", note="<Stat: STR>")
    en(42, "Peck", scope=1, dtype=1, element=1, formula="d4", hit=1, anim=11, icon=76, msg="%1 pecks!", note="<Stat: DEX>")
    en(43, "Claw", scope=1, dtype=1, element=1, formula="d6", hit=1, anim=16, icon=76, msg="%1 rakes with its claws!",
       note="<Stat: DEX>")
    en(44, "Howl", scope=8, anim=37, icon=34, crit=False, msg="%1 howls!", effects=[eff(BUFF, 2, 3)],
       note="<Stat: CHA>")
    en(45, "Rusty Stab", scope=1, dtype=1, element=1, formula="d6", hit=1, anim=11, icon=76, msg="%1 stabs with a rusty blade!",
       note="<Stat: STR>")
    en(46, "Spear Throw", scope=1, dtype=1, element=1, formula="d6", hit=1, anim=111, icon=107, msg="%1 hurls a spear!",
       note="<Stat: DEX>\n<Hit: +1>")
    en(47, "Terrible Roar", scope=2, anim=37, icon=11, crit=False, msg="%1 roars!", effects=[eff(ADD_STATE, ST_FEAR, 1.0)],
       note="<Stat: CHA>\n<Save: WIS>")
    en(48, "Crushing Swing", scope=1, dtype=1, element=1, formula="d10", hit=1, anim=39, icon=77,
       msg="%1 swings with all its weight!", note="<Stat: STR>\n<Damage: 125%>")
    en(49, "Ghostfire", scope=1, dtype=1, element=FIRE, formula="d8", hit=2, anim=66, icon=64,
       msg="%1 breathes pale ghostfire!", note="<Stat: MAG>")
    en(50, "Spore Puff", scope=2, anim=33, icon=2, crit=False, msg="%1 puffs out a cloud of spores!",
       effects=[eff(ADD_STATE, 4, 1.0)], note="<Stat: MAG>\n<Save: CON>")
    en(51, "Twin Claws", scope=1, dtype=1, element=1, formula="d6", hit=1, anim=28, icon=76, msg="%1 strikes twice!",
       note="<Stat: DEX>\n<At Rank F>\nhits: 2\n</At Rank F>")
    en(52, "Wing Buffet", scope=2, dtype=1, element=WIND, formula="d4", hit=0, anim=93, icon=69,
       msg="%1 beats its wings!", note="<Stat: DEX>\n<Save: DEX>")
    en(53, "Frost Breath", scope=2, dtype=1, element=ICE, formula="d8", hit=0, anim=73, icon=65,
       msg="%1 exhales killing frost!", effects=[eff(ADD_STATE, ST_CHILL, 0.5)], note="<Stat: MAG>\n<Save: CON>")
    en(54, "Ice Lance", scope=1, dtype=1, element=ICE, formula="d10", hit=2, anim=72, icon=65, msg="%1 casts an ice lance!",
       note="<Stat: MAG>")
    en(55, "Whiteout", scope=2, anim=74, icon=65, crit=False, msg="%1 calls down a whiteout!",
       effects=[eff(ADD_STATE, ST_CHILL, 1.0)], note="<Stat: MAG>\n<Save: CON>")
    en(56, "Sickle Wind", scope=1, dtype=1, element=WIND, formula="d6", hit=1, anim=92, icon=69, msg="%1 slashes on the wind!",
       note="<Stat: DEX>\n<Crit Range: +1>")
    en(57, "Shield Bash", scope=1, dtype=1, element=1, formula="d4", hit=1, anim=39, icon=128, msg="%1 bashes with a shield!",
       effects=[eff(ADD_STATE, ST_PRONE, 1.0)], note="<Stat: STR>\n<Save: STR states>")
    en(58, "Miasma Bite", scope=1, dtype=1, element=DARK, formula="d8", hit=1, anim=16, icon=71, msg="%1 bites, dripping ash!",
       effects=[eff(ADD_STATE, 4, 0.5)], note="<Stat: STR>")
    en(59, "Stand Still", scope=0, anim=0, icon=81, crit=False, msg="%1 watches you, unmoving.", note="<No Mastery>")
    en(60, "Flee", scope=0, anim=0, icon=82, crit=False, msg="%1 bolts!", effects=[eff(41, 0, 1.0)], note="<No Mastery>")
    en(61, "Frost Needles", scope=2, dtype=1, element=ICE, formula="d4", hit=0, anim=73, icon=65,
       msg="%1 flings a storm of frost needles!", note="<Stat: MAG>\n<Save: CON>")
    # chapter 3 / act II
    en(62, "Kornstaub", scope=1, anim=33, icon=3, crit=False, msg="%1 flings a fistful of grain dust!",
       effects=[eff(ADD_STATE, ST_DAZZLED, 1.0)], note="<Stat: DEX>\n<Save: CON>")
    en(63, "Schimmelschwall", scope=2, dtype=1, element=EARTH, formula="d6", hit=0, anim=33, icon=2,
       msg="%1 bursts, spraying rot everywhere!", effects=[eff(ADD_STATE, 4, 0.5)], note="<Stat: MAG>\n<Save: CON>")
    en(64, "Aschenatem", scope=2, dtype=1, element=DARK, formula="d8", hit=0, anim=101, icon=71,
       msg="%1 breathes a cloud of burning ash!", effects=[eff(ADD_STATE, ST_DAZZLED, 0.3)],
       note="<Stat: MAG>\n<Save: CON>")
    en(65, "Schwanzhieb", scope=2, dtype=1, element=1, formula="d6", hit=0, anim=39, icon=77,
       msg="%1 sweeps its tail through the line!", effects=[eff(ADD_STATE, ST_PRONE, 0.5)],
       note="<Stat: STR>\n<Save: DEX>")
    en(66, "Grabesgriff", scope=1, dtype=1, element=1, formula="d8", hit=1, anim=16, icon=76,
       msg="%1 grabs with cold dead hands!", effects=[eff(DEBUFF, 6, 2)], note="<Stat: STR>")
    en(67, "Kragenschreck", scope=2, anim=37, icon=11, crit=False, msg="%1 flares its frill and hisses!",
       effects=[eff(ADD_STATE, ST_FEAR, 1.0)], note="<Stat: CHA>\n<Save: WIS>")
    en(68, "Rudelruf", scope=8, anim=37, icon=34, crit=False, msg="%1 calls the pack!", effects=[eff(BUFF, 2, 3)],
       note="<Stat: CHA>")
    while len(L) <= 100:
        put(sep(len(L), ""))
    kanta_kit(put)
    while len(L) < 141:
        put(sep(len(L), ""))
    hanma_kit(put)
    while len(L) < 171:
        put(sep(len(L), ""))
    falin_kit(put)
    while len(L) < 200:
        put(sep(len(L), ""))
    from story import foes
    foes.skills(put, len(L))
    while len(L) <= 320:
        put(sep(len(L), ""))
    foes.guest_skills(put, len(L))
    while len(L) <= 360:
        put(sep(len(L), ""))
    return L


# ---------------------------------------------------------------------------------------------------------------------
# The party's full kits (PC_Kanta: Divine Weaponry ladder and techniques; PARTY §2 Hanma, §3 Falin).
# Every MP cost is base 5 x (rank + 1)^2 (MAGIC§5), Body techniques half.  <Needs Rank> skills learned by level wait
# for the breakthrough; <Start Rank> puts a new skill at the rank it is learned in.
# ---------------------------------------------------------------------------------------------------------------------
def kanta_kit(put):
    DW = MAGIC_ST
    put(passive(101, "Radiant Edge", 70,
                "Passive (D). Her weapons of light burn the unholy: all her\nstrikes count as Light (demons, undead, miasma x2).",
                "<Passive State: %d>" % ST_RADIANT))
    put(skill(102, "Lance Charge", DW, mp=5, scope=1, dtype=1, element=-1, formula="2d10", hit=1, anim=11, icon=107,
              crit=True, effects=[eff(ADD_STATE, ST_PRONE, 1.0)], msg="%1 charges with a lance of light!",
              desc="Body (D). The light becomes a lance for one charge:\n2d10 + STR; STR save or the foe is knocked prone.",
              note="<Stat: STR>\n<Body>\n<Save: STR states>\n<Start Rank: D>"))
    put(skill(103, "Arc Sweep", DW, mp=5, scope=2, dtype=1, element=-1, formula="d8", hit=1, anim=6, icon=97,
              msg="%1 sweeps a blade of light through them!",
              desc="Body (D). One wide cut through every foe: (d8 + STR) x1/2,\nDEX save for half again.",
              note="<Stat: STR>\n<Body>\n<Save: DEX>\n<Start Rank: D>\n<Needs Rank: D>"))
    put(passive(104, "Float", 97,
                "Passive (C). Spare weapons orbit her. After each of her\nactions one floating blade strikes (d8 + MAG).",
                "<Passive State: %d>" % ST_FLOAT))
    put(skill(105, "Blade Volley", DW, mp=5, scope=5, dtype=1, element=-1, formula="d8", hit=1, anim=12, icon=97,
              crit=True, msg="%1 sends her blades flying!",
              desc="C. Three weapons of light fly at up to three foes:\nd8 + MAG each, each rolls to hit.",
              note="<Stat: MAG>\n<Area Rate: 100%>\n<Attack Roll>\n<Start Rank: C>"))
    put(skill(106, "Guardian Blade", DW, mp=5, scope=11, anim=51, icon=81, speed=2000,
              effects=[eff(ADD_STATE, ST_GUARDIAN, 1.0)], msg="%1 sets her blades to guard.",
              desc="C. Acts first. For 3 rounds, once a round, a blow that\nwould barely hit her or an ally is turned aside.",
              note="<Stat: MAG>\n<Support>\n<Start Rank: C>"))
    put(skill(107, "Lend a Blade", DW, mp=5, scope=7, anim=46, icon=97, speed=10,
              effects=[eff(ADD_STATE, ST_LENT, 1.0)], msg="%1 lends a blade of light.",
              desc="C. One floating weapon serves an ally for 5 turns: d8,\ntheir STR or DEX, Kanta's rank, Light.",
              note="<Stat: MAG>\n<Support>\n<Start Rank: C>\n<Needs Rank: C>"))
    put(skill(108, "Blade Wall", DW, mp=5, scope=8, anim=53, icon=129,
              effects=[eff(ADD_STATE, ST_BLADEWALL, 1.0)], msg="%1 raises a spinning wall of blades!",
              desc="B. A spinning ring of blades: every ally +2 AC and +2 to\nDEX saves for 5 turns (ends if she falls).",
              note="<Stat: MAG>\n<Support>\n<Start Rank: B>"))
    put(skill(109, "Rain of Blades", DW, mp=5, scope=2, dtype=1, element=-1, formula="d10", hit=1, anim=6, icon=97,
              msg="Blades of light rain down from %1's halo!",
              desc="B. Blades rain on every foe: d10 + MAG each,\nDEX save for half.",
              note="<Stat: MAG>\n<Save: DEX>\n<Area Rate: 100%>\n<Start Rank: B>"))
    put(passive(110, "Halo Riposte", 97,
                "Passive (B). Once a round, a foe that misses her takes a\nfloating strike.",
                "<Passive State: %d>\n<Needs Rank: B>" % ST_RIPOSTE))
    put(skill(111, "Colossus Blade", DW, mp=5, scope=2, dtype=1, element=-1, formula="d12", hit=1, anim=39, icon=97,
              msg="%1's blade grows thirty feet long!",
              desc="A. One weapon grown colossal cuts a line through them:\nd12 + STR to every foe, DEX save for half.",
              note="<Stat: STR>\n<Save: DEX>\n<Area Rate: 100%>\n<Start Rank: A>"))
    put(skill(112, "Pinning Light", DW, mp=5, scope=1, dtype=1, element=-1, formula="d12", hit=1, anim=12, icon=70,
              crit=True, effects=[eff(ADD_STATE, ST_PINNED, 1.0)], msg="%1 hurls a spike of light!",
              desc="A. A thrown spike of light: d12 + DEX, STR save or the\nfoe is pinned (-4 AC, -4 to hit).",
              note="<Stat: DEX>\n<Save: STR states>\n<Start Rank: A>"))
    put(skill(113, "Blade Ride", DW, mp=5, scope=7, anim=46, icon=36,
              effects=[eff(ADD_STATE, ST_AIRBORNE, 1.0)], msg="%1 rides a blade into the air!",
              desc="A. She and one ally ride her weapons for 5 turns: +3 AC,\n+2 to hit, can't be knocked down.",
              note="<Stat: DEX>\n<Support>\n<Self State: %d>\n<Start Rank: A>\n<Needs Rank: A>" % ST_AIRBORNE))
    put(passive(114, "Floating Pair", 97,
                "Passive (S). Her floating armory strikes twice after each\nof her actions.",
                "<Passive State: %d>" % ST_TWINFLOAT))
    put(passive(115, "Armor-Breaker", 77,
                "Passive (S). Armor counts one rank lower against her\nweapons (+5 to hit).",
                "<Passive State: %d>" % ST_ARMORBREAK))
    put(skill(116, "Sky Armory", DW, mp=5, scope=2, dtype=1, element=-1, formula="d12", hit=1, anim=6, icon=97,
              msg="A sky full of weapons opens above %1!",
              desc="S. Twenty weapons fall on every foe: d12 + MAG each,\nDEX save for half.",
              note="<Stat: MAG>\n<Save: DEX>\n<Area Rate: 100%>\n<Start Rank: S>"))
    put(passive(117, "Mimic Arms", 97,
                "Passive (S). Every weapon that strikes near her is learned:\n+1 to hit, crits one face wider.",
                "<Passive State: %d>\n<Needs Rank: S>" % ST_MIMIC))
    put(skill(118, "Heaven's Lance", DW, mp=5, scope=2, dtype=1, element=-1, formula="d12", hit=1, anim=11, icon=107,
              msg="%1 hurls a lance the size of a tower!",
              desc="SS. A lance the size of a tower: d12 + STR to every foe,\nCON save for half.",
              note="<Stat: STR>\n<Save: CON>\n<Area Rate: 100%>\n<Start Rank: SS>"))
    put(skill(119, "Sanctuary Ring", DW, mp=5, scope=11, anim=53, icon=97,
              effects=[eff(ADD_STATE, ST_RING, 1.0)], msg="%1 rings the field with blades!",
              desc="SS. A ring of blades for 5 turns: every foe that acts\ntakes a floating strike (ends if she falls).",
              note="<Stat: MAG>\n<Support>\n<Start Rank: SS>"))
    put(skill(120, "Siege Breaker", DW, mp=5, scope=1, dtype=1, element=-1, formula="d12", hit=1, anim=39, icon=77,
              crit=True, msg="Every blade fuses into one colossus in %1's hands!",
              desc="SS. Every weapon fuses for one swing: (d12 + STR) x2,\narmor counts for nothing (+10 to hit).",
              note="<Stat: STR>\n<Damage: 200%>\n<Hit: +10>\n<Start Rank: SS>\n<Needs Rank: SS>"))
    put(passive(121, "Blink Blade", 82,
                "Passive (SSS). Once a round the first blow that would hit\nher finds only a blade: she's already elsewhere.",
                "<Passive State: %d>" % ST_BLINK))
    put(skill(122, "Judgment Rain", DW, mp=5, scope=2, dtype=1, element=-1, formula="d12", hit=1, anim=6, icon=97,
              repeats=2, msg="Judgment rains from a mile of sky!",
              desc="SSS. Two waves of blades on every foe: d12 + MAG each,\nDEX save for half.",
              note="<Stat: MAG>\n<Save: DEX>\n<Area Rate: 100%>\n<Start Rank: SSS>"))
    put(passive(123, "Unseen Armory", 97,
                "Passive (SSS). Her weapons form anywhere she can see:\n+3 to hit, cover means nothing.",
                "<Passive State: %d>\n<Needs Rank: SSS>" % ST_UNSEEN))
    put(passive(124, "Any Form", 97,
                "Passive (V). She summons any weapon she has ever seen:\nher attack strikes twice, crits one face wider.",
                "<Passive State: %d>" % ST_ANYFORM))
    put(passive(125, "Endless Guard", 81,
                "Passive (V). Guardian Blade never ends: once a round for\nevery ally.",
                "<Passive State: %d>" % ST_ENDLESS))
    put(skill(126, "Final Light", DW, mp=5, scope=1, dtype=1, element=-1, formula="d12", hit=1, anim=46, icon=70,
              crit=True, msg="Every weapon %1 has ever held converges!",
              desc="V. Once a battle: every weapon converges, (d12 + MAG) x3.\nNo more Divine Weaponry this battle.",
              note="<Stat: MAG>\n<Damage: 300%%>\n<Once Per Battle>\n<Self State: %d>\n<Start Rank: V>" % ST_SPENT))
    put(passive(127, "Open Armory", 97,
                "Passive (V). Every ally carries one of her weapons:\n+2 to hit, their strikes count as Light.",
                "<Party Aura: %d>\n<Needs Rank: V>" % ST_OPENARMORY))
    # the floating armory's own strike (Float, Riposte, Sanctuary Ring use it; never chosen from a menu)
    put(skill(128, "Floating Blade", 0, mp=0, scope=1, dtype=1, element=-1, formula="d8", hit=1, anim=6, icon=97,
              crit=True, occasion=3, msg="%1's floating blade strikes!",
              desc="A floating weapon of light strikes on its own.",
              note="<Stat: MAG>\n<Floating Strike>\n<No Mastery>"))


def hanma_kit(put):
    SP = SPIRIT_ST
    put(skill(141, "Blight", SP, mp=5, scope=2, dtype=1, element=DARK, formula="d10", hit=0, anim=101, icon=71,
              msg="%1 lets the rot loose!",
              desc="Death (D). Rot spreads through the foes: (d10 + MAG) x1/2\nnecrotic, CON save for half. The dead shrug it off.",
              note="<Stat: MAG>\n<Save: CON>\n<Start Rank: D>\n<Needs Rank: D>"))
    put(passive(142, "Old General's Eye", 75,
                "Passive (D). At the start of every battle she reads the foes'\nweaknesses; every ally +2 initiative.",
                "<Party Aura: %d>\n<General's Eye>\n<Needs Rank: D>" % ST_EYE))
    put(skill(143, "Hold the Line", SP, mp=5, scope=0, anim=41, icon=72, occasion=3, msg="",
              desc="Reaction (C, automatic). Once per ally a battle, an ally who\nwould fall stays at 1 HP with a barrier (d10 + WIS).",
              note="<Stat: WIS>\n<Hold The Line>\n<Start Rank: C>\n<Needs Rank: C>"))
    put(skill(144, "Reap and Sow", SP, mp=5, scope=2, dtype=1, element=DARK, formula="d10", hit=0, anim=101, icon=71,
              msg="%1 reaps the living and sows it back!",
              desc="Death (B). (d10 + MAG) x1/2 necrotic to every foe, CON save\nfor half; half the damage heals the party.",
              note="<Stat: MAG>\n<Save: CON>\n<Share Drain: 50%>\n<Start Rank: B>\n<Needs Rank: B>"))
    put(passive(145, "Deathwatch", 71,
                "Passive (B). She feels every dying and miasma-touched thing\nnearby: the target window shows a foe's exact HP.",
                "<Deathwatch>\n<Needs Rank: B>"))
    put(skill(146, "Forward, March!", SP, mp=5, scope=8, anim=53, icon=32, speed=20,
              effects=[eff(ADD_STATE, ST_FORWARD, 1.0)], msg="%1: \"Forward, march!\"",
              desc="Command (A). Acts early: every ally +4 to hit and +5\ninitiative this round.",
              note="<Stat: CHA>\n<Support>\n<Start Rank: A>\n<Needs Rank: A>"))
    put(skill(147, "Unmaking", SP, mp=5, scope=1, dtype=1, element=DARK, formula="d12", hit=0, anim=101, icon=71,
              msg="%1 unmakes %2!",
              desc="Death (S). d12 + MAG necrotic, CON save for half. What it\nkills crumbles to dust.",
              note="<Stat: MAG>\n<Save: CON>\n<Start Rank: S>\n<Needs Rank: S>"))
    put(passive(148, "Swift Mercy", 72,
                "Passive (S). Heal and Triage are quick: she acts twice a turn,\nbut one of the two must be Heal, Triage or Guard.",
                "<Passive State: %d>\n<Swift: 17, 21>\n<Needs Rank: S>" % ST_SWIFT))
    put(skill(149, "Restoration", SP, mp=5, scope=8, dtype=3, formula="d12", anim=43, icon=72, occasion=0,
              effects=[eff(REMOVE_STATE, s, 1.0) for s in NEGATIVE], msg="%1 restores the line.",
              desc="Life (SS). Heals every ally (d12 + WIS) x1/2 and ends their\nconditions.",
              note="<Stat: WIS>\n<Start Rank: SS>\n<Needs Rank: SS>"))
    put(skill(150, "Purge", SP, mp=5, scope=2, dtype=1, element=LIGHT, formula="d12", hit=0, anim=46, icon=70,
              effects=[eff(REMOVE_STATE, ST_MIASMA, 1.0), eff(ADD_STATE, ST_PURGED, 1.0)],
              msg="%1 finishes the purge!",
              desc="Life (SSS). Once a battle: demons and the miasma-touched take\n(d12 + CHA) x1/2, CON save half, and lose the miasma.",
              note="<Stat: CHA>\n<Save: CON>\n<Only Demons>\n<Once Per Battle>\n<Start Rank: SSS>\n<Needs Rank: SSS>"))
    put(passive(151, "Banner of the Dead", 87,
                "Passive (SSS). Under her banner no ally can be frightened,\nand death magic hurts them less (x3/4).",
                "<Party Aura: %d>\n<Needs Rank: SSS>" % ST_BANNER))
    put(skill(152, "Last Command", SP, mp=5, scope=8, anim=43, icon=87, occasion=1,
              effects=[eff(REC_HP, 0, 1.0, 0)] + [eff(REMOVE_STATE, s, 1.0) for s in NEGATIVE] +
                      [eff(ADD_STATE, ST_COMMANDED, 1.0)],
              msg="%1 gives her last command!",
              desc="Command (V). Once a battle: every ally heals fully, sheds every\ncondition and acts twice next turn. Then she rests.",
              note="<Stat: CHA>\n<Support>\n<Once Per Battle>\n<Self State: %d>\n<Start Rank: V>\n<Needs Rank: V>"
                   % ST_EXHAUSTED))


def falin_kit(put):
    BO = BODY_ST
    put(skill(171, "Vanguard Rush", BO, mp=5, scope=7, anim=51, icon=81, speed=2000,
              effects=[eff(ADD_STATE, ST_WARDED, 1.0)], msg="%1 rushes to cover an ally!",
              desc="Body (D). Acts first: until the round ends every attack and\nspell aimed at that ally hits Falin instead.",
              note="<Stat: STR>\n<Body>\n<Support>\n<Start Rank: D>\n<Needs Rank: D>"))
    put(passive(172, "Living Steel", 136,
                "Passive (D). Her plate mends her: she regenerates (rank + 1) x2%\nof her max HP every turn. Storms stop it a round.",
                "<Passive State: %d>\n<Needs Rank: D>" % ST_STEEL))
    put(skill(173, "Iron Roar", BO, mp=5, scope=2, anim=37, icon=5, speed=10,
              effects=[eff(ADD_STATE, ST_ROARED, 1.0)], msg="%1 roars!",
              desc="Body (C). Every foe makes a WIS save or attacks only Falin\nuntil its next turn ends.",
              note="<Stat: STR>\n<Body>\n<Save: WIS states>\n<Support>\n<Start Rank: C>\n<Needs Rank: C>"))
    put(skill(174, "Unbroken", BO, mp=5, scope=0, anim=52, icon=128, occasion=3, msg="",
              desc="Reaction (B, automatic). Once a battle, when she would fall\nshe stays at 1 HP with a barrier (d10 + CON).",
              note="<Stat: CON>\n<Body>\n<Unbroken>\n<Start Rank: B>\n<Needs Rank: B>"))
    put(passive(175, "Bastion", 128,
                "Passive (B). Allies beside her have half cover: +2 AC and\n+2 to DEX saves.",
                "<Party Aura: %d>\n<Needs Rank: B>" % ST_BASTION))
    put(skill(176, "Share the Burden", BO, mp=5, scope=8, anim=52, icon=128,
              effects=[eff(ADD_STATE, ST_BURDEN, 1.0)], msg="%1 takes their wounds on herself.",
              desc="Body (A). For 5 turns half of every hit on an ally goes to\nFalin instead (her Brace applies; ends if she falls).",
              note="<Stat: CON>\n<Body>\n<Support>\n<Start Rank: A>\n<Needs Rank: A>"))
    put(skill(177, "Mountain Stance", BO, mp=5, scope=11, anim=52, icon=33, speed=10,
              effects=[eff(ADD_STATE, ST_MOUNTAIN, 1.0)], msg="%1 takes the mountain stance.",
              desc="Body (S). For 5 turns she can't be moved or knocked down,\nand every foe's attacks come to her.",
              note="<Stat: STR>\n<Body>\n<Support>\n<Start Rank: S>\n<Needs Rank: S>"))
    put(passive(178, "Steel Hide", 136,
                "Passive (S). Weapons barely bite: physical damage to her x1/2.",
                "<Passive State: %d>\n<Needs Rank: S>" % ST_STEELHIDE))
    put(skill(179, "Plate Bloom", BO, mp=5, scope=8, anim=52, icon=129,
              effects=[eff(ADD_STATE, ST_BLOOM, 1.0)], msg="Steel unfolds from %1's plate over everyone!",
              desc="Body (SS). Steel sheets cover the allies: +5 AC and +5 to DEX\nsaves for 5 turns (ends if she falls).",
              note="<Stat: CON>\n<Body>\n<Support>\n<Start Rank: SS>\n<Needs Rank: SS>"))
    put(skill(180, "Earthsunder", BO, mp=5, scope=2, dtype=1, element=EARTH, formula="d12", hit=1, anim=39, icon=68,
              effects=[eff(ADD_STATE, ST_PRONE, 1.0)], msg="%1 drives a fist into the ground!",
              desc="Body (SSS). The ground splits under every foe: (d12 + STR)\nx1/2 and knocked down, DEX save for half.",
              note="<Stat: STR>\n<Body>\n<Save: DEX>\n<Start Rank: SSS>\n<Needs Rank: SSS>"))
    put(passive(181, "Living Fortress", 136,
                "Passive (SSS). Her plate counts a rank higher (+5 AC) and\nInterpose covers spells too.",
                "<Passive State: %d>\n<Needs Rank: SSS>" % ST_FORTRESS))
    put(skill(182, "Last Bastion", BO, mp=5, scope=11, anim=52, icon=128, speed=2000,
              effects=[eff(ADD_STATE, ST_LASTBASTION, 1.0)], msg="%1 stands in front of everyone!",
              desc="Body (V). Once a battle, acts first: this round every attack\non an ally hits her, and she can't fall below 1 HP.",
              note="<Stat: CON>\n<Body>\n<Support>\n<Once Per Battle>\n<Start Rank: V>\n<Needs Rank: V>"))

# =====================================================================
# ITEMS
# =====================================================================
IT = {}
def item(iid, name, icon, price, desc, effects, scope=7, occasion=0, anim=41, note="", itype=1, consumable=True):
    return {"id": iid, "animationId": anim, "consumable": consumable,
            "damage": {"critical": False, "elementId": 0, "formula": "0", "type": 0, "variance": 20},
            "description": desc, "effects": effects, "hitType": 0, "iconIndex": icon, "itypeId": itype,
            "name": name, "note": note, "occasion": occasion, "price": price, "repeats": 1, "scope": scope,
            "speed": 0, "successRate": 100, "tpGain": 0}

def build_items():
    L = [None]
    def put(i):
        assert i["id"] == len(L)
        L.append(i)
        IT[i["name"]] = i["id"]
    put(item(1, "Heiltrank", 176, 30, "Healing draught. Restores 40 HP.", [eff(REC_HP, 0, 0, 40)]))
    put(item(2, "Kräuterbündel", 181, 12, "A bundle of wound herbs. Restores 20 HP.", [eff(REC_HP, 0, 0, 20)]))
    put(item(3, "Manatrank", 177, 60, "Mana tonic. Restores 15 MP.", [eff(REC_MP, 0, 0, 15)]))
    put(item(4, "Gegengift", 179, 20, "Antidote. Cures poison.", [eff(REMOVE_STATE, 4, 1.0)], anim=45))
    put(item(5, "Riechsalz", 183, 80, "Smelling salts. Wakes a knocked-out ally with 25% HP.",
             [eff(REMOVE_STATE, 1, 1.0), eff(REC_HP, 0, 0.25, 0)], scope=9, anim=49))
    put(item(6, "Wärmetee", 226, 25, "Hot pine tea. Cures Chilled and restores 10 HP.",
             [eff(REMOVE_STATE, ST_CHILL, 1.0), eff(REC_HP, 0, 0, 10)], anim=45))
    put(item(7, "Großer Heiltrank", 176, 150, "Strong healing draught. Restores 120 HP.", [eff(REC_HP, 0, 0, 120)]))
    lp = item(8, "Lichtphiole", 162, 90, "A phial of the Church's dawn light. Throw it: 60 Light\ndamage to one foe (demons and the dead hate it).",
              [], scope=1, occasion=1, anim=46)
    lp["damage"] = {"critical": False, "elementId": LIGHT, "formula": "60", "type": 1, "variance": 10}
    put(lp)
    while len(L) < 10:
        put(item(len(L), "", 0, 0, "", [], occasion=3, anim=0))
    put(item(10, "Manastein (F)", 300, 20, "A dull mana stone from a rank F creature.\nWorth about 1 sl to a trader.",
             [], scope=0, occasion=3, anim=0, consumable=False))
    put(item(11, "Manastein (E)", 300, 200, "A bright mana stone from a rank E creature.\nWorth about 1 gk to a trader.",
             [], scope=0, occasion=3, anim=0, consumable=False))
    put(item(12, "Wolfsfell", 150, 16, "A wolf pelt. Traders pay a little for it.", [], scope=0, occasion=3, anim=0,
             consumable=False))
    put(item(13, "Rabenholz-Pilz", 261, 6, "Edible, if you know which ones. Saeki knows.", [], scope=0, occasion=3,
             anim=0, consumable=False))
    while len(L) < 20:
        put(item(len(L), "", 0, 0, "", [], occasion=3, anim=0))
    # key items (20-)
    key = lambda iid, name, icon, desc: item(iid, name, icon, 0, desc, [], scope=0, occasion=3, anim=0, itype=2,
                                            consumable=False)
    put(key(20, "Schwarze Rabenfeder", 225, "A raven feather gone black and brittle, reeking of\nsomething burnt. Hanma called it miasma."))
    put(key(21, "Glocke eines Schafs", 205, "A little bronze bell from one of Natsu's sheep."))
    put(key(22, "Brief an die Gilde", 192, "Elder Okuda's letter to the Adventurers' Guild in\nWachtburg, about the goblins."))
    put(key(23, "Gildenkarte", 188, "Your guild card: name, rank, kill-log."))
    put(key(24, "Silberne Opferschale", 226, "A silver offering bowl, dented. Deserters carried it;\nit belongs to a shrine."))
    put(key(25, "Heilwurz", 181, "Wound-wort, picked by the roadside. The Wachtburg\nfield hospital pays for it."))
    while len(L) <= 40:
        put(key(len(L), "", 0, ""))
    from story import foes
    foes.items(put, len(L))
    while len(L) <= 60:
        put(item(len(L), "", 0, 0, "", [], occasion=3, anim=0))
    foes.key_items(put, len(L))
    while len(L) <= 100:
        put(key(len(L), "", 0, ""))
    return L

# =====================================================================
# WEAPONS  (Attack box = damage die)
# =====================================================================
WP = {}
def weapon(wid, name, wtype, die, icon, anim, price, desc, note=""):
    return {"id": wid, "animationId": anim, "description": desc, "etypeId": 1,
            "traits": [trait(31, 1, 0), trait(22, 0, 0)],
            "iconIndex": icon, "name": name, "note": note, "params": [0, 0, die, 0, 0, 0, 0, 0],
            "price": price, "wtypeId": wtype}

def build_weapons():
    L = [None]
    def put(w):
        assert w["id"] == len(L)
        L.append(w)
        WP[w["name"]] = w["id"]
    # Divine Weaponry: the held forms. Every unlocked form can be summoned from the equip screen; each counts as
    # gear of Kanta's rank and can't be put away. (The floating armory from C on is in her passives.)
    put(weapon(1, "Lichtstrahl", DIVINE_W, 4, 70, 12, 0,
               "[Divine Weaponry F] A hand-long beam of pale blue light.\nd4 · DEX · +2 to hit · lights 10 ft",
               "<Stat: DEX>\n<Hit: +2>\n<DW Form>"))
    put(weapon(2, "Lichtdolch", DIVINE_W, 6, 96, 12, 0,
               "[Divine Weaponry E] A dagger of light; throw it and it\ncomes back. d6 · DEX · crits on 19-20",
               "<Stat: DEX>\n<Rank: E>\n<Crit Range: +1>\n<DW Form>"))
    put(weapon(3, "Lichtklinge", DIVINE_W, 8, 97, 6, 0,
               "[Divine Weaponry D] A sword of light that burns the\nunholy. d8 · STR · +1 to hit · crits on 19-20",
               "<Stat: STR>\n<Rank: D>\n<Hit: +1>\n<Crit Range: +1>\n<DW Form>"))
    put(weapon(4, "Lichtlanze", DIVINE_W, 10, 107, 11, 0,
               "[Divine Weaponry D] A lance of light with a long reach.\nd10 · STR",
               "<Stat: STR>\n<Rank: D>\n<DW Form>"))
    put(weapon(5, "Lichtkoloss", DIVINE_W, 12, 97, 39, 0,
               "[Divine Weaponry A] One weapon of light grown thirty\nfeet long. d12 · STR",
               "<Stat: STR>\n<Rank: A>\n<DW Form>"))
    while len(L) < 10:
        put(weapon(len(L), "", 0, 0, 0, 0, 0, ""))
    put(weapon(10, "Eisenknüppel", FLAIL_W, 6, 98, 1, 60, "[Flail] d6 · STR"))
    put(weapon(11, "Kurzschwert", SWORD_W, 6, 97, 6, 80, "[Sword] d6 · STR"))
    put(weapon(12, "Speer", SPEAR_W, 8, 107, 11, 140, "[Spear] d8 · DEX", "<Stat: DEX>"))
    put(weapon(13, "Panzerhandschuhe", GLOVE_W, 10, 102, 1, 620, "[Gauntlets · E] Steel-plated fists. d10 · STR",
               "<Rank: E>"))
    put(weapon(14, "Morgenstern", FLAIL_W, 10, 98, 1, 700, "[Flail · E] A spiked iron ball on a haft. d10 · STR",
               "<Rank: E>"))
    while len(L) <= 30:
        put(weapon(len(L), "", 0, 0, 0, 0, 0, ""))
    from story import foes
    foes.weapons(put, len(L))
    while len(L) <= 60:
        put(weapon(len(L), "", 0, 0, 0, 0, 0, ""))
    return L

# =====================================================================
# ARMORS  (Defense box = armor value)
# =====================================================================
AR = {}
def armor(aid, name, atype, etype, value, icon, price, desc, note="", traits=None):
    return {"id": aid, "atypeId": atype, "description": desc, "etypeId": etype,
            "traits": traits if traits is not None else [trait(22, 1, 0)], "iconIndex": icon, "name": name,
            "note": note, "params": [0, 0, 0, value, 0, 0, 0, 0], "price": price}

def build_armors():
    L = [None]
    def put(a):
        assert a["id"] == len(L)
        L.append(a)
        AR[a["name"]] = a["id"]
    put(armor(1, "Silberrüstung", LIGHT_A, E_BODY, 2, 136, 0,
              "[Body · Light] Armor 2. Silver-bright plate that leaves the\nsigil arm bare. Maker and worth unknown."))
    put(armor(2, "Roter Kapuzenmantel", GEN, E_ACC, 0, 138, 0, "[Accessory] A red cape and hood, hood always down.\nCHA +3",
              "<CHA: +3>"))
    put(armor(3, "Offiziersuniform", UNIFORM_A, E_BODY, 1, 152, 0,
              "[Body] Hanma's black uniform, gold at the cuffs.\nArmor 1. Part of her; it can't be taken off.", "<Rank Gear>"))
    put(armor(4, "Lederkappe", LIGHT_A, E_HEAD, 0, 130, 40, "[Head] A boiled-leather cap. CON +3", "<CON: +3>"))
    put(armor(5, "Lederarmschienen", GEN, E_ACC, 0, 142, 60, "[Accessory] Leather bracers. +1 AC", "<AC: +1>"))
    put(armor(6, "Rabenamulett", GEN, E_ACC, 0, 147, 0,
              "[Accessory] Rabenau's old raven charm. WIS +5, MAG +5", "<WIS: +5>\n<MAG: +5>"))
    put(armor(7, "Filzmantel", GEN, E_ACC, 0, 138, 70, "[Accessory] A thick felt cloak. Halves the chance of\nbeing Chilled.",
              "", [trait(13, ST_CHILL, 0.5)]))
    put(armor(8, "Wolfsfellweste", LIGHT_A, E_BODY, 3, 136, 180, "[Body · Light] Armor 3. Wolf fur over leather."))
    put(armor(9, "Echtsilberrüstung", LIGHT_A, E_BODY, 5, 136, 0,
              "[Body · Light] Armor 5 · rank E. True silver, appraised at\nthe Wachtburg guild. Light as cloth.", "<Rank: E>"))
    put(armor(10, "Pelzmütze", LIGHT_A, E_HEAD, 0, 130, 120, "[Head] A fur cap. CON +5, halves the chance of\nbeing Chilled.",
              "<CON: +5>", [trait(13, ST_CHILL, 0.5)]))
    while len(L) < 11:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    put(armor(11, "Verschmolzene Platte F", FUSED_A, E_BODY, 6, 137, 0,
              "[Body · Fused] Armor 6. Falin's plate, grown into her.\nIt can't be removed.", "<Rank Gear>"))
    put(armor(12, "Verschmolzene Platte E", FUSED_A, E_BODY, 11, 137, 0,
              "[Body · Fused] Armor 11 · rank E. Falin's plate.", "<Rank: E>\n<Rank Gear>"))
    put(armor(13, "Verschmolzene Platte D", FUSED_A, E_BODY, 16, 137, 0,
              "[Body · Fused] Armor 16 · rank D. Falin's plate.", "<Rank: D>\n<Rank Gear>"))
    while len(L) < 14:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    put(armor(14, "Frostträne", GEN, E_ACC, 0, 165, 0,
              "[Accessory] A tear of ice that never melts: Fubuki's\nthanks. Ice damage x1/2, MAG +8",
              "<MAG: +8>", [trait(11, ICE, 0.5)]))
    put(armor(15, "Lederrock", LIGHT_A, E_BODY, 2, 136, 70, "[Body · Light] Armor 2. A long leather coat."))
    put(armor(16, "Eisenhaube", HEAVY_A, E_HEAD, 1, 132, 220, "[Head · Heavy] +1 AC. Iron coif."))
    put(armor(17, "Wachtfeuer-Amulett", GEN, E_ACC, 0, 145, 0,
              "[Accessory · E] The guild's gift for the Wolfsgrube. WIS +10.\nThe party is never surprised and strikes first more often.",
              "<Rank: E>\n<WIS: +10>", [trait(64, 2, 0), trait(64, 3, 0)]))
    put(armor(18, "Wolfslederkappe", LIGHT_A, E_HEAD, 0, 130, 380, "[Head · Light · E] Thick wolf-leather cap. CON +10",
              "<Rank: E>\n<CON: +10>"))
    put(armor(19, "Stahlarmschienen", GEN, E_ACC, 0, 142, 520, "[Accessory · E] Steel bracers. +2 AC", "<Rank: E>\n<AC: +2>"))
    put(armor(20, "Heilerbrosche", GEN, E_ACC, 0, 147, 450, "[Accessory · E] A field surgeon's brooch. WIS +10",
              "<Rank: E>\n<WIS: +10>"))
    put(armor(21, "Stahlhaube", HEAVY_A, E_HEAD, 2, 132, 450, "[Head · Heavy · E] +2 AC. A steel helm with a nasal.",
              "<Rank: E>"))
    put(armor(22, "Turmschild", LSHIELD, E_SHIELD, 3, 129, 600, "[Large Shield · E] +3 AC. Taller than most recruits.",
              "<Rank: E>"))
    put(armor(23, "Wachmantel", GEN, E_ACC, 0, 138, 400, "[Accessory · E] A Nordwall watch cloak. CON +10, halves\nthe chance of being Chilled.",
              "<Rank: E>\n<CON: +10>", [trait(13, ST_CHILL, 0.5)]))
    put(armor(24, "Runenamulett", GEN, E_ACC, 0, 147, 480, "[Accessory · E] A rune-carved amulet. MAG +10",
              "<Rank: E>\n<MAG: +10>"))
    while len(L) < 40:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    # ---- rank gear lines: each breakthrough changes them (Story_Core <Rank Armor>)
    # Kanta's silver armor grows with the vessel from D (locks the body slot while worn)
    names = {2: "Morgensilber", 3: "Klingensilber", 4: "Halosilber", 5: "Kolosssilber", 6: "Himmelssilber",
             7: "Legionssilber", 8: "Allsichtsilber", 9: "Götterlicht"}
    for r in range(2, 10):
        value = 5 * r + 2
        L_ = RANKS[r]
        put(armor(38 + r, "%s-Rüstung" % names[r], LIGHT_A, E_BODY, value, 136, 0,
                  "[Body · Light · %s] Armor %d. The vessel's silver, grown with\nher: the sigil arm still bare. CON +%d" %
                  (L_, value, 5 * r), "<Rank: %s>\n<CON: +%d>\n<Rank Gear>" % (L_, 5 * r),
                  [trait(22, 1, 0), trait(53, E_BODY, 1)]))
    while len(L) < 50:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    # Hanma's uniform: armor 2 x rank + 1 (a spirit's coat, not plate)
    for r in range(1, 10):
        value = 2 * r + 1
        L_ = RANKS[r]
        put(armor(49 + r, "Offiziersuniform %s" % L_, UNIFORM_A, E_BODY, value, 152, 0,
                  "[Body · %s] Hanma's black uniform, gold at the cuffs.\nArmor %d. Part of her. CHA +%d" % (L_, value, 5 * r),
                  "<Rank: %s>\n<CHA: +%d>\n<Rank Gear>" % (L_, 5 * r)))
    while len(L) < 60:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    # Falin's fused plate C..V: armor 5 x rank + 6 (PARTY §3)
    for r in range(3, 10):
        value = 5 * r + 6
        L_ = RANKS[r]
        put(armor(57 + r, "Verschmolzene Platte %s" % L_, FUSED_A, E_BODY, value, 137, 0,
                  "[Body · Fused] Armor %d · rank %s. Falin's plate." % (value, L_), "<Rank: %s>\n<Rank Gear>" % L_))
    while len(L) <= 70:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    from story import foes
    foes.armors(put, len(L))
    while len(L) <= 140:
        put(armor(len(L), "", 0, E_BODY, 0, 0, 0, ""))
    return L

# =====================================================================
# CLASSES
# =====================================================================
def build_classes():
    C0 = load_orig('Classes')
    params_template = C0[1]["params"]
    def klass(cid, name, stypes, wtypes, atypes, learnings, note, extra=None):
        traits = [trait(23, 0, 1), trait(22, 0, 0.95), trait(22, 1, 0.05)]
        traits += [trait(41, s, 0) for s in stypes]
        traits += [trait(51, w, 0) for w in wtypes]
        traits += [trait(52, a, 0) for a in atypes]
        traits += extra or []
        return {"id": cid, "expParams": [30, 20, 30, 30], "traits": traits,
                "learnings": [{"level": l, "note": "", "skillId": s} for l, s in learnings],
                "name": name, "note": note, "params": copy.deepcopy(params_template)}
    C = [None,
         klass(1, "Weapon-Bearer", [MAGIC_ST, PASSIVE_ST], [DIVINE_W], [GEN, LIGHT_A],
               [(1, SK["Piercing Ray"]), (1, SK["Combat Mastery"]), (4, SK["Glare"]), (7, SK["Deflect"]),
                (15, SK["Shadow Stitch"]), (25, SK["Arc Sweep"]), (35, SK["Lend a Blade"]), (45, SK["Halo Riposte"]),
                (55, SK["Blade Ride"]), (65, SK["Mimic Arms"]), (75, SK["Siege Breaker"]), (85, SK["Unseen Armory"]),
                (95, SK["Open Armory"])],
               "<Aptitude: DEX S, STR S, MAG S, CON A, WIS C, CHA C, INT D>\n<Saves: STR, CON>"),
         klass(2, "Spirit General", [SPIRIT_ST, PASSIVE_ST], [], [UNIFORM_A, GEN],
               [(1, SK["Heal"]), (1, SK["Reverse Heal"]), (1, SK["Steady, Soldier"]), (5, SK["Rally"]),
                (11, SK["Triage"]), (21, SK["Blight"]), (25, SK["Old General's Eye"]), (31, SK["Hold the Line"]),
                (41, SK["Reap and Sow"]), (45, SK["Deathwatch"]), (51, SK["Forward, March!"]), (61, SK["Unmaking"]),
                (65, SK["Swift Mercy"]), (71, SK["Restoration"]), (81, SK["Purge"]), (85, SK["Banner of the Dead"]),
                (91, SK["Last Command"])],
               "<Aptitude: WIS S, MAG S, CHA S, CON A, INT C, DEX C, STR D>\n<Saves: WIS, MAG>"),
         klass(3, "Living Armor", [BODY_ST, PASSIVE_ST], [GLOVE_W, SWORD_W, FLAIL_W, AXE_W, SPEAR_W],
               [FUSED_A, GEN, SSHIELD, LSHIELD, HEAVY_A],
               [(1, SK["Fused Plate"]), (1, SK["Challenge"]), (4, SK["Interpose"]), (7, SK["Crushing Blow"]),
                (11, SK["Brace"]), (21, SK["Vanguard Rush"]), (25, SK["Living Steel"]), (31, SK["Iron Roar"]),
                (41, SK["Unbroken"]), (45, SK["Bastion"]), (51, SK["Share the Burden"]), (61, SK["Mountain Stance"]),
                (65, SK["Steel Hide"]), (71, SK["Plate Bloom"]), (81, SK["Earthsunder"]), (85, SK["Living Fortress"]),
                (91, SK["Last Bastion"])],
               "<Aptitude: CON S, STR S, WIS A, CHA A, MAG B, DEX C, INT C>\n<Saves: CON, STR>")]
    from story import foes
    G = foes.GUEST
    C.append(klass(4, "Battle-Mage", [BATTLEMAGIC_ST, PASSIVE_ST], [STAFF_W], [GEN, LIGHT_A],
                   [(1, G["Flammenlanze"]), (1, G["Eissturm"]), (1, G["Königsschild"])],
                   "<Aptitude: MAG S, WIS A, CHA A, DEX B, CON B, INT B, STR D>\n<Saves: WIS, MAG>"))
    C.append(klass(5, "Frost Saint", [FROST_ST, PASSIVE_ST], [SWORD_W], [GEN, LIGHT_A],
                   [(1, G["Frostschnitt"]), (1, G["Eiswand"]), (1, G["Frostkörper"]), (41, G["Schneesturm"]),
                    (41, G["Kalte Gnade"]), (51, G["Weiße Stille"]), (51, G["Morgenwacht"])],
                   "<Aptitude: DEX S, MAG S, WIS A, CON A, STR B, CHA C, INT C>\n<Saves: DEX, WIS>"))
    return C

# =====================================================================
# ACTORS
# =====================================================================
def build_actors():
    def actor(aid, name, cid, equips, char, face, nickname, profile, note, traits):
        return {"id": aid, "battlerName": "", "characterIndex": char[1], "characterName": char[0], "classId": cid,
                "equips": equips, "faceIndex": face[1], "faceName": face[0], "traits": traits, "initialLevel": 1,
                "maxLevel": 99, "name": name, "nickname": nickname, "note": note, "profile": profile}
    A = [None,
         actor(1, "Kanta", 1, [WP["Lichtstrahl"], 0, 0, AR["Silberrüstung"], AR["Roter Kapuzenmantel"]],
               ("Cast", 0), ("Kanta", 0), "",
               "Woke in an empty vessel with a weapon of light in her hand.\nDies, and wakes again. Not a hero; not yet.",
               "<Gated>\n<Rank Weapon: F %d, E %d, D %d, A %d>\n<DW Extra: D %d>\n"
               "<Rank Armor: D 40, C 41, B 42, A 43, S 44, SS 45, SSS 46, V 47>\n"
               "<Breakthrough E: %d>\n<Breakthrough D: %d, %d>\n<Breakthrough C: %d, %d, %d>\n"
               "<Breakthrough B: %d, %d>\n<Breakthrough A: %d, %d>\n<Breakthrough S: %d, %d, %d>\n"
               "<Breakthrough SS: %d, %d>\n<Breakthrough SSS: %d, %d>\n<Breakthrough V: %d, %d, %d>" %
               (WP["Lichtstrahl"], WP["Lichtdolch"], WP["Lichtklinge"], WP["Lichtkoloss"], WP["Lichtlanze"],
                SK["Returning Fang"], SK["Radiant Edge"], SK["Lance Charge"],
                SK["Float"], SK["Blade Volley"], SK["Guardian Blade"], SK["Blade Wall"], SK["Rain of Blades"],
                SK["Colossus Blade"], SK["Pinning Light"], SK["Floating Pair"], SK["Armor-Breaker"], SK["Sky Armory"],
                SK["Heaven's Lance"], SK["Sanctuary Ring"], SK["Blink Blade"], SK["Judgment Rain"],
                SK["Any Form"], SK["Endless Guard"], SK["Final Light"]),
               [trait(54, E_SHIELD, 1)]),
         actor(2, "Hanma", 2, [0, 0, 0, AR["Offiziersuniform"], 0], ("Cast", 1), ("Hanma", 0), "",
               "A war general, dead for centuries, bound to Kanta's soul.\nCalls her \"my Lord\". Heals, and rots.",
               "<Bound To: 1>\n<Gated>\n<Rank Armor: F 3, E 50, D 51, C 52, B 53, A 54, S 55, SS 56, SSS 57, V 58>",
               [trait(54, E_WEAPON, 1), trait(54, E_SHIELD, 1), trait(54, E_HEAD, 1), trait(53, E_BODY, 1)]),
         actor(3, "Falin", 3, [0, 0, 0, AR["Verschmolzene Platte F"], 0], ("Cast", 2), ("Falin", 0), "die Eiserne",
               "A living armor. She woke inside the plate the night\nWeißenfels fell; it has grown into her since.",
               "<Gated>\n<Rank Armor: F %d, E %d, D %d, C 60, B 61, A 62, S 63, SS 64, SSS 65, V 66>\n<Unarmed Die: d8>\n"
               "<Auto Build: CON 34, STR 30, WIS 12, CHA 12, MAG 7, DEX 3, INT 2>" %
               (AR["Verschmolzene Platte F"], AR["Verschmolzene Platte E"], AR["Verschmolzene Platte D"]),
               [trait(53, E_BODY, 1)]),
         actor(4, "Rabenfeder", 1, [0, 0, 0, 0, 0], ("", 0), ("", 0), "",
               "Not a character: holds the party's guild name (\\N[4]).", "<Party Name>", [])]
    from story import foes
    W, R = foes.WEAPONS, foes.ARMORS
    A.append(actor(5, "Rin", 4, [W["Kronenstab"], 0, 0, R["Kronprinzenmantel"], 0], ("Actor2", 2), ("Actor2", 2),
                   "Kronprinzessin",
                   "Asahina Rin, Crown Princess of Hohenwacht. A battle-mage who\nwatched her brother fall at Weißenfels.",
                   "<Rank: C>\n<Auto Build: MAG 40, WIS 20, DEX 15, CON 15, CHA 10>\n<Guest>", []))
    A.append(actor(6, "Yukino", 5, [W["Frostklinge"], 0, 0, R["Morgenwacht-Mantel"], 0], ("Actor3", 2), ("Actor3", 2),
                   "die Frostheilige",
                   "Tsukishiro Yukino, the Frost Saint: the last of the Morgenwacht.\nTwelve years silent. The rift took most of her power.",
                   "<Gated>\n<Rank Weapon: C %d, B %d, A %d>\n<Auto Build: DEX 35, MAG 25, WIS 20, CON 15, STR 5>\n"
                   "<Breakthrough B: %d, %d>\n<Breakthrough A: %d>" %
                   (W["Frostklinge"], W["Mondeisklinge"], W["Weißklinge"], foes.GUEST["Schneesturm"],
                    foes.GUEST["Kalte Gnade"], foes.GUEST["Weiße Stille"]),
                   [trait(53, E_WEAPON, 1)]))
    return A

# =====================================================================
# ENEMIES
# =====================================================================
EN = {}
def act(skill_id, rating, ctype=0, p1=0, p2=0):
    return {"conditionParam1": p1, "conditionParam2": p2, "conditionType": ctype, "rating": rating, "skillId": skill_id}

def drop(kind=0, data=1, denom=1):
    return {"dataId": data, "denominator": denom, "kind": kind}

def stats(STR, DEX, CON, WIS, CHA, MAG):
    return dict(STR=STR, DEX=DEX, CON=CON, WIS=WIS, CHA=CHA, MAG=MAG)

def enemy(eid, name, battler, mhp, st, exp, gold, actions, note, hue=0, drops=None, extra=None):
    params = [mhp, 0, st['STR'], st['CON'], st['MAG'], st['WIS'], st['DEX'], st['CHA']]
    traits = [trait(22, 0, 0.95), trait(22, 1, 0.05), trait(31, 1, 0)] + (extra or [])
    d = (drops or []) + [drop(0, 1, 1)] * 3
    return {"id": eid, "actions": actions, "battlerHue": hue, "battlerName": battler, "dropItems": d[:3],
            "exp": exp, "traits": traits, "gold": gold, "name": name, "note": note, "params": params}

def weak(element, rate=2.0):
    return trait(11, element, rate)

def build_enemies():
    SF, SE_ = IT["Manastein (F)"], IT["Manastein (E)"]
    L = [None]
    def put(e):
        assert e["id"] == len(L)
        L.append(e)
        EN[e["name"]] = e["id"]
    s = SK
    # ---- rank F (prologue, chapter 1)
    put(enemy(1, "Crow", "Crow", 6, stats(6, 16, 8, 8, 4, 0), 4, 1, [act(s["Peck"], 5)],
              "<Rank: F>\n<Role: minion>\n<Attack Die: d4>\n<Attack Stat: DEX>", extra=[weak(THUNDER, 1.5)]))
    put(enemy(2, "Wolf", "SF_Wolf", 22, stats(16, 18, 16, 10, 6, 0), 8, 0, [act(1, 5), act(s["Bite"], 4), act(s["Howl"], 2)],
              "<Rank: F>\n<Attack Die: d6>\n<Attack Stat: DEX>", drops=[drop(1, IT["Wolfsfell"], 3)]))
    put(enemy(3, "Goblin", "Goblin", 16, stats(12, 12, 14, 6, 6, 3), 8, 3, [act(1, 5), act(s["Rusty Stab"], 4)],
              "<Rank: F>\n<Attack Die: d6>", drops=[drop(1, SF, 1), drop(1, IT["Heiltrank"], 8)]))
    put(enemy(4, "Goblin Thrower", "Goblin", 14, stats(10, 14, 12, 6, 6, 3), 8, 4, [act(1, 3), act(s["Spear Throw"], 5)],
              "<Rank: F>\n<Attack Die: d4>\n<Attack Stat: DEX>", hue=60, drops=[drop(1, SF, 1)]))
    put(enemy(5, "Rotcap", "Matango", 20, stats(8, 6, 20, 14, 2, 12), 8, 0, [act(1, 5), act(s["Spore Puff"], 3)],
              "<Rank: F>\n<Attack Die: d4>\n<Armor: 1>", drops=[drop(1, SF, 1), drop(1, IT["Rabenholz-Pilz"], 2)],
              extra=[weak(FIRE)]))
    put(enemy(6, "Grauzahn", "SF_Whitewolf", 40, stats(20, 24, 22, 12, 16, 4), 24, 0,
              [act(1, 5), act(s["Bite"], 5), act(s["Howl"], 2)],
              "<Rank: F>\n<Role: elite>\n<Attack Die: d6>\n<Attack Stat: DEX>", hue=200,
              drops=[drop(1, SF, 1), drop(1, IT["Wolfsfell"], 1)]))
    put(enemy(7, "Krummzahn", "Goblin", 110, stats(30, 18, 34, 14, 30, 8), 96, 60,
              [act(1, 6), act(s["Crushing Swing"], 3), act(s["Terrible Roar"], 2, 1, 2, 3)],
              "<Rank: F>\n<Role: boss>\n<Attack Die: d8>\n<Armor: 3>", hue=330,
              drops=[drop(1, SF, 1), drop(3, AR["Lederarmschienen"], 1)]))
    put(enemy(8, "Two-Tail", "Caitsith", 100, stats(90, 160, 100, 120, 120, 145), 75, 0,
              [act(s["Twin Claws"], 5), act(s["Ghostfire"], 3)],
              "<Rank: E>\n<Role: elite>\n<Attack Die: d6>\n<Attack Stat: DEX>\n<AC: 18>\n<INT: 100>\n<Saves: DEX, MAG>",
              drops=[drop(1, SE_, 1)]))
    # ---- chapter 2 (upper F, one E)
    put(enemy(9, "Kamaitachi", "SF_Kamaitachi", 34, stats(28, 50, 28, 20, 10, 18), 12, 0,
              [act(1, 4), act(s["Sickle Wind"], 5)], "<Rank: F>\n<Attack Die: d4>\n<Attack Stat: DEX>",
              drops=[drop(1, SF, 2)], extra=[weak(FIRE, 1.5)]))
    put(enemy(10, "Grey Wolf", "SF_Wolf", 40, stats(34, 42, 34, 14, 8, 0), 12, 0,
              [act(1, 5), act(s["Bite"], 4), act(s["Howl"], 2)], "<Rank: F>\n<Attack Die: d6>\n<Attack Stat: DEX>",
              hue=330, drops=[drop(1, IT["Wolfsfell"], 2)]))
    put(enemy(11, "Deserter", "Mercenary", 40, stats(38, 28, 38, 20, 16, 4), 12, 10,
              [act(1, 5), act(s["Shield Bash"], 3)], "<Rank: F>\n<Role: minion>\n<Attack Die: d8>\n<Armor: 3>",
              drops=[drop(1, SF, 1), drop(1, IT["Heiltrank"], 3)]))
    put(enemy(12, "Deserter Sergeant", "Berserker", 100, stats(46, 32, 48, 20, 30, 6), 48, 30,
              [act(1, 5), act(s["Crushing Swing"], 3), act(s["Terrible Roar"], 2, 1, 1, 3)],
              "<Rank: F>\n<Attack Die: d10>\n<Armor: 3>", drops=[drop(1, SF, 1), drop(1, IT["Heiltrank"], 1)]))
    put(enemy(13, "Frost Wolf", "SF_Whitewolf", 46, stats(38, 46, 38, 16, 10, 10), 14, 0,
              [act(1, 5), act(s["Bite"], 4), act(s["Howl"], 1)], "<Rank: F>\n<Attack Die: d6>\n<Attack Stat: DEX>",
              drops=[drop(1, IT["Wolfsfell"], 2)], extra=[weak(FIRE), trait(11, ICE, 0.5)]))
    put(enemy(14, "Ice Wisp", "SF_Will_o_the_wisp", 30, stats(10, 40, 26, 40, 10, 52), 14, 0,
              [act(s["Ice Lance"], 5), act(s["Whiteout"], 1)], "<Rank: F>\n<Attack Die: d4>",
              hue=180, drops=[drop(1, SF, 1)], extra=[weak(FIRE), trait(11, ICE, 0.0)]))
    put(enemy(15, "Eiswurm", "Eiswurm", 300, stats(60, 26, 66, 30, 20, 50), 150, 0,
              [act(s["Bite"], 5), act(s["Frost Breath"], 3), act(s["Crushing Swing"], 2)],
              "<Rank: F>\n<Role: boss>\n<Attack Die: d8>\n<Armor: 4>", drops=[drop(1, SF, 1), drop(1, SF, 1)],
              extra=[weak(FIRE), trait(11, ICE, 0.0)]))
    put(enemy(16, "Fubuki", "Fubuki", 220, stats(40, 104, 100, 120, 130, 110), 0, 0,
              [act(s["Whiteout"], 4), act(s["Frost Needles"], 4), act(s["Ice Lance"], 2), act(s["Stand Still"], 2)],
              "<Rank: E>\n<Role: elite>\n<Attack Die: d6>\n<Attack Stat: DEX>\n<Saves: WIS, MAG>",
              extra=[weak(FIRE, 1.5), trait(11, ICE, 0.0)]))
    # ---- chapter 3: the Königsstraße, Wachtburg (upper F)
    put(enemy(17, "Harpyie", "Harpy", 70, stats(50, 80, 55, 40, 45, 30), 12, 6,
              [act(s["Claw"], 5), act(s["Wing Buffet"], 3)], "<Rank: F>\n<Attack Die: d6>\n<Attack Stat: DEX>",
              drops=[drop(1, SF, 2)], extra=[weak(THUNDER, 1.5)]))
    put(enemy(18, "Kragenechse", "Frilledlizard", 90, stats(70, 55, 75, 30, 50, 10), 14, 4,
              [act(1, 4), act(s["Bite"], 4), act(s["Kragenschreck"], 2)], "<Rank: F>\n<Attack Die: d8>\n<Armor: 3>",
              drops=[drop(1, IT["Heiltrank"], 3)], extra=[weak(ICE, 1.5)]))
    put(enemy(19, "Wegelagerer", "Mercenary", 80, stats(70, 60, 70, 30, 30, 5), 12, 25,
              [act(1, 5), act(s["Shield Bash"], 2)], "<Rank: F>\n<Attack Die: d8>\n<Armor: 3>", hue=100,
              drops=[drop(1, IT["Heiltrank"], 2)]))
    put(enemy(20, "Kornkobold", "Petitdevil", 40, stats(30, 75, 40, 30, 30, 60), 7, 4,
              [act(s["Claw"], 4), act(s["Kornstaub"], 3)], "<Rank: F>\n<Role: minion>\n<Attack Die: d4>\n<Attack Stat: DEX>",
              drops=[drop(1, SF, 2)], extra=[weak(LIGHT, 1.5)]))
    put(enemy(21, "Schimmeling", "Matango", 75, stats(40, 30, 85, 50, 10, 65), 11, 0,
              [act(1, 4), act(s["Spore Puff"], 3)], "<Rank: F>\n<Attack Die: d6>", hue=90,
              drops=[drop(1, SF, 2), drop(1, IT["Gegengift"], 4)], extra=[weak(FIRE)]))
    put(enemy(22, "Schimmelmutter", "Schimmelmutter", 300, stats(60, 30, 90, 60, 40, 72), 100, 50,
              [act(1, 5), act(s["Schimmelschwall"], 2), act(s["Spore Puff"], 2)],
              "<Rank: F>\n<Role: boss>\n<Attack Die: d8>\n<Armor: 2>",
              drops=[drop(1, SF, 1), drop(1, IT["Gegengift"], 1)], extra=[weak(FIRE)]))
    put(enemy(23, "Nordwolf", "SF_Wolf", 70, stats(65, 80, 65, 30, 20, 0), 12, 0,
              [act(1, 5), act(s["Bite"], 4), act(s["Howl"], 1)], "<Rank: F>\n<Attack Die: d6>\n<Attack Stat: DEX>",
              hue=30, drops=[drop(1, IT["Wolfsfell"], 2)]))
    put(enemy(24, "Rudelführer", "SF_Whitewolf", 130, stats(75, 85, 75, 40, 50, 0), 40, 0,
              [act(1, 5), act(s["Bite"], 5), act(s["Rudelruf"], 2)],
              "<Rank: F>\n<Role: elite>\n<Attack Die: d6>\n<Attack Stat: DEX>", hue=20,
              drops=[drop(1, IT["Wolfsfell"], 1), drop(1, SF, 1)]))
    # ---- the emergency (rank E, the demon war reaches the road)
    put(enemy(25, "Aschenhund", "SF_Zombiedog", 70, stats(110, 120, 100, 40, 30, 60), 30, 0,
              [act(1, 4), act(s["Miasma Bite"], 4)],
              "<Rank: E>\n<Role: minion>\n<Attack Die: d6>\n<Attack Stat: DEX>",
              drops=[drop(1, SE_, 6)], extra=[weak(LIGHT), trait(11, DARK, 0.5)]))
    put(enemy(26, "Aschenhund-Leitrüde", "Leitruede", 280, stats(150, 150, 150, 90, 110, 100), 150, 0,
              [act(s["Miasma Bite"], 5), act(1, 3), act(s["Terrible Roar"], 2, 1, 1, 3), act(s["Howl"], 1)],
              "<Rank: E>\n<Attack Die: d8>\n<Attack Stat: DEX>\nMiasma-touched: +50 to every stat (baked in).",
              drops=[drop(1, SE_, 1)], extra=[weak(LIGHT), trait(11, DARK, 0.5)]))
    put(enemy(27, "Schreckenswolf", "SF_Whitewolf", 115, stats(115, 125, 110, 45, 50, 0), 70, 0,
              [act(1, 5), act(s["Bite"], 4), act(s["Howl"], 2)], "<Rank: E>\n<Attack Die: d8>\n<Attack Stat: DEX>",
              hue=270, drops=[drop(1, IT["Wolfsfell"], 1)]))
    # ---- act II: the Wall
    put(enemy(28, "Aschenleiche", "Zombie", 110, stats(120, 50, 130, 20, 10, 30), 36, 0,
              [act(1, 4), act(s["Grabesgriff"], 3)], "<Rank: E>\n<Role: minion>\n<Attack Die: d8>",
              drops=[drop(1, SE_, 8)], extra=[weak(LIGHT), weak(FIRE, 1.5), trait(11, DARK, 0.0)]))
    put(enemy(29, "Leere Rüstung", "Stoneknight", 170, stats(130, 60, 150, 40, 30, 40), 80, 0,
              [act(1, 5), act(s["Shield Bash"], 3), act(s["Crushing Swing"], 2)],
              "<Rank: E>\n<Attack Die: d8>\n<Armor: 8>", hue=300,
              drops=[drop(1, SE_, 4)], extra=[weak(THUNDER, 1.5), weak(LIGHT, 1.5), trait(11, DARK, 0.0)]))
    put(enemy(30, "Aschenschwinge", "Aschenschwinge", 650, stats(170, 150, 170, 110, 130, 170), 400, 0,
              [act(1, 3), act(s["Aschenatem"], 3), act(s["Schwanzhieb"], 3), act(s["Terrible Roar"], 1, 1, 1, 3)],
              "<Rank: E>\n<Role: boss>\n<Attack Die: d10>\nMiasma-touched: +50 to every stat (baked in).",
              drops=[drop(1, SE_, 1), drop(1, SE_, 1)], extra=[weak(LIGHT), trait(11, DARK, 0.5)]))
    while len(L) <= 60:
        put(enemy(len(L), "", "", 1, stats(1, 1, 1, 1, 1, 1), 0, 0, [act(1, 5)], ""))
    from story import foes
    foes.enemies(put, len(L))
    while len(L) <= 160:
        put(enemy(len(L), "", "", 1, stats(1, 1, 1, 1, 1, 1), 0, 0, [act(1, 5)], ""))
    return L

# =====================================================================
# TROOPS
# =====================================================================
TR = {}
Y = 436
def troop(tid, name, members, pages=None):
    empty_page = {"conditions": {"actorHp": 50, "actorId": 1, "actorValid": False, "enemyHp": 50, "enemyIndex": 0,
                                 "enemyValid": False, "switchId": 1, "switchValid": False, "turnA": 0, "turnB": 0,
                                 "turnEnding": False, "turnValid": False},
                  "list": [{"code": 0, "indent": 0, "parameters": []}], "span": 0}
    return {"id": tid, "members": [{"enemyId": e, "x": x, "y": y, "hidden": False} for e, x, y in members],
            "name": name, "pages": pages or [empty_page]}

def troop_page(lst, turn=None, enemy_hp=None, span=0, turn_end=False, switch=None):
    c = {"actorHp": 50, "actorId": 1, "actorValid": False, "enemyHp": 50, "enemyIndex": 0, "enemyValid": False,
         "switchId": 1, "switchValid": False, "turnA": 0, "turnB": 0, "turnEnding": turn_end, "turnValid": False}
    if turn is not None:
        c.update({"turnValid": True, "turnA": turn[0], "turnB": turn[1]})
    if enemy_hp is not None:
        c.update({"enemyValid": True, "enemyIndex": enemy_hp[0], "enemyHp": enemy_hp[1]})
    if switch:
        c.update({"switchValid": True, "switchId": switch})
    return {"conditions": c, "list": lst.done() if isinstance(lst, Ev) else lst, "span": span}

def build_troops():
    e = EN
    L = [None]
    def put(name, members, pages=None):
        tid = len(L)
        L.append(troop(tid, name, members, pages))
        TR[name] = tid
        return tid
    put("Crows x2", [(e["Crow"], 300, Y - 50), (e["Crow"], 516, Y - 30)])
    put("Crows x3", [(e["Crow"], 228, Y - 60), (e["Crow"], 408, Y - 30), (e["Crow"], 588, Y - 60)])
    put("Wolf", [(e["Wolf"], 408, Y)])
    put("Wolves x2", [(e["Wolf"], 300, Y), (e["Wolf"], 530, Y)])
    put("Wolf & Crow", [(e["Wolf"], 330, Y), (e["Crow"], 560, Y - 60)])
    put("Goblins x2", [(e["Goblin"], 300, Y), (e["Goblin"], 516, Y)])
    put("Goblins x3", [(e["Goblin"], 228, Y), (e["Goblin"], 408, Y + 6), (e["Goblin"], 588, Y)])
    put("Goblin & Thrower", [(e["Goblin"], 320, Y), (e["Goblin Thrower"], 520, Y - 10)])
    put("Goblins & Thrower", [(e["Goblin"], 228, Y), (e["Goblin Thrower"], 408, Y - 10), (e["Goblin"], 588, Y)])
    put("Rotcaps x2", [(e["Rotcap"], 300, Y), (e["Rotcap"], 516, Y)])
    put("Rotcap & Goblin", [(e["Rotcap"], 300, Y), (e["Goblin"], 516, Y)])
    put("Wolf & Goblin", [(e["Wolf"], 300, Y), (e["Goblin"], 516, Y)])
    # scripted
    boss = Ev()
    boss.say(npc_speaker("Krummzahn", "", 0), ["Rrrah! Soft-skins! Grauzahn, eat!"])
    put("Krummzahn", [(e["Grauzahn"], 250, Y), (e["Krummzahn"], 500, Y + 6)],
        [troop_page(boss, turn=(0, 0))])
    put("Two-Tail", [(e["Two-Tail"], 408, Y)])
    put("Raid: Goblins", [(e["Goblin"], 228, Y), (e["Goblin Thrower"], 408, Y - 10), (e["Goblin"], 588, Y)])
    # chapter 2
    put("Kamaitachi x2", [(e["Kamaitachi"], 300, Y - 20), (e["Kamaitachi"], 516, Y - 20)])
    put("Kamaitachi x3", [(e["Kamaitachi"], 228, Y - 20), (e["Kamaitachi"], 408, Y), (e["Kamaitachi"], 588, Y - 20)])
    put("Grey Wolves x2", [(e["Grey Wolf"], 300, Y), (e["Grey Wolf"], 530, Y)])
    put("Grey Wolf & Kamaitachi", [(e["Grey Wolf"], 320, Y), (e["Kamaitachi"], 540, Y - 20)])
    put("Deserters", [(e["Deserter"], 220, Y), (e["Deserter Sergeant"], 408, Y + 6), (e["Deserter"], 596, Y)])
    put("Frost Wolves x2", [(e["Frost Wolf"], 300, Y), (e["Frost Wolf"], 530, Y)])
    put("Ice Wisps x2", [(e["Ice Wisp"], 300, Y - 40), (e["Ice Wisp"], 516, Y - 40)])
    put("Frost Wolf & Wisp", [(e["Frost Wolf"], 320, Y), (e["Ice Wisp"], 540, Y - 40)])
    put("Ice Wisps x3", [(e["Ice Wisp"], 228, Y - 40), (e["Ice Wisp"], 408, Y - 20), (e["Ice Wisp"], 588, Y - 40)])
    put("Eiswurm", [(e["Eiswurm"], 408, Y + 20)])
    yld = Ev()
    yld.se('Ice4')
    yld.say(npc_speaker("Fubuki", "", 0), ["Enough!"])
    yld.add(340, [])
    put("Fubuki", [(e["Fubuki"], 408, Y + 20)], [troop_page(yld, enemy_hp=(0, 50))])
    # chapter 3
    put("Harpyien x2", [(e["Harpyie"], 300, Y - 40), (e["Harpyie"], 520, Y - 40)])
    put("Kragenechse", [(e["Kragenechse"], 408, Y)])
    put("Wegelagerer x2", [(e["Wegelagerer"], 300, Y), (e["Wegelagerer"], 520, Y)])
    put("Harpyie & Kragenechse", [(e["Kragenechse"], 320, Y), (e["Harpyie"], 540, Y - 40)])
    put("Wegelagerer & Harpyie", [(e["Wegelagerer"], 320, Y), (e["Harpyie"], 540, Y - 40)])
    put("Kornkobolde x3", [(e["Kornkobold"], 228, Y - 30), (e["Kornkobold"], 408, Y - 10), (e["Kornkobold"], 588, Y - 30)])
    put("Schimmelinge x2", [(e["Schimmeling"], 300, Y), (e["Schimmeling"], 520, Y)])
    put("Kobolde & Schimmeling", [(e["Kornkobold"], 250, Y - 30), (e["Schimmeling"], 408, Y), (e["Kornkobold"], 566, Y - 30)])
    mold = Ev()
    mold.say(npc_speaker("Schimmelmutter", "", 0), ["…grow… grow… feed…"])
    put("Schimmelmutter", [(e["Kornkobold"], 200, Y - 30), (e["Schimmelmutter"], 430, Y + 20)],
        [troop_page(mold, turn=(0, 0))])
    put("Nordwölfe x2", [(e["Nordwolf"], 300, Y), (e["Nordwolf"], 530, Y)])
    put("Nordwölfe x3", [(e["Nordwolf"], 228, Y), (e["Nordwolf"], 408, Y + 6), (e["Nordwolf"], 588, Y)])
    put("Rudel", [(e["Nordwolf"], 200, Y), (e["Rudelführer"], 420, Y + 10), (e["Nordwolf"], 630, Y)])
    # the emergency: Kanta's breakthrough happens inside this battle (turn 2)
    bt = Ev()
    bt.text(["The Leitrüde's eyes slide past Kanta, past Hanma, to", "the cart where the children are hiding."],
            background=1, position=1)
    bt.text(["It lunges. Kanta is already there.", "Its jaws close on the sigil arm."], background=1, position=1)
    bt.se('Damage5')
    bt.flash((255, 60, 60, 170), 20)
    bt.say(HANMA, ["My Lord!"], 'command')
    bt.se('Magic3', 90, 80)
    bt.flash((200, 230, 255, 255), 60)
    bt.text(["The sigils blaze white-hot. The beam in Kanta's hand", "stretches, sharpens, and settles into a blade:",
             "a dagger of light, heavy and certain."], background=1, position=1)
    bt.breakthrough()
    bt.say(KANTA, ["…Get away from them."], 'fierce')
    bt.se('Fire3', 80, 120)
    bt.add(333, [1, 0, ST_CLEANSED])
    bt.text(["The light scorches the Leitrüde's muzzle. Ash smokes", "off its hide, and it backs away, snarling."],
            background=1, position=1)
    bt.se('Explosion1', 70, 130)
    bt.flash((200, 230, 255, 200), 30)
    bt.add(331, [0, 1, 0, 9999, True])
    bt.add(331, [2, 1, 0, 9999, True])
    bt.text(["The flare catches the smaller hounds mid-leap. They", "burst apart into drifting ash."],
            background=1, position=1)
    bt.say(HANMA, ["The light burns miasma! Press it, my Lord!"], 'command')
    put("Aschenhunde", [(e["Aschenhund"], 200, Y), (e["Aschenhund-Leitrüde"], 420, Y + 20), (e["Aschenhund"], 640, Y)],
        [troop_page(bt, turn=(2, 0))])
    # the guild's E trial
    put("Wolfsgrube", [(e["Schreckenswolf"], 200, Y), (e["Schreckenswolf"], 420, Y + 10), (e["Schreckenswolf"], 640, Y)])
    # act II
    put("Aschenhunde x2", [(e["Aschenhund"], 300, Y), (e["Aschenhund"], 530, Y)])
    put("Aschenleichen x2", [(e["Aschenleiche"], 300, Y), (e["Aschenleiche"], 530, Y)])
    put("Aschenleiche & Hund", [(e["Aschenleiche"], 320, Y), (e["Aschenhund"], 540, Y)])
    put("Bresche: Vorhut", [(e["Aschenleiche"], 170, Y), (e["Aschenhund"], 320, Y - 10), (e["Leere Rüstung"], 480, Y + 10),
                            (e["Aschenleiche"], 650, Y)])
    wing = Ev()
    wing.say(FALIN, ["Here it comes. Stay behind me, whatever it does."], 'fierce')
    put("Aschenschwinge", [(e["Aschenschwinge"], 408, Y + 30)], [troop_page(wing, turn=(0, 0))])
    while len(L) <= 60:
        put("", [])
    from story import foes
    foes.troops(put, len(L))
    while len(L) <= 200:
        put("", [])
    return L

# =====================================================================
# COMMON EVENTS
# =====================================================================
CE = {}
def build_common_events():
    L = [None]
    def put(name, lst, trigger=0, switch=1):
        cid = len(L)
        L.append({"id": cid, "list": lst.done() if isinstance(lst, Ev) else lst, "name": name, "switchId": switch,
                  "trigger": trigger})
        CE[name] = cid
        return cid

    # 1: vessel revival (reserved by Story_Core after a defeat)
    el = Ev()
    def first(e):
        e.narrate(["…", "Cold stone under your back. Darkness, again."])
        e.say(HANMA, ["My Lord."], 'stern')
        e.say(HANMA, ["You died. I watched it happen: your body went still,",
                      "and I felt the thread between us go slack…",
                      "and then you were here. Whole. As if the first body",
                      "had never been."], 'stern')
        e.say(KANTA, ["…I died."], 'hurt')
        e.say(HANMA, ["You did. And you came back. So that's what you are:",
                      "a soul that finds empty vessels. I won't pretend",
                      "to understand it."], 'calm')
        e.say(HANMA, ["But don't make a habit of it. Something is always",
                      "left behind. Your purse, for one."], 'stern')
        e.notice(["\\C[6]Vessel\\C[0]: when the party falls, Kanta wakes in a new",
                  "vessel at the last place you rested, healed, but a",
                  "tenth of your money stays with the old body."])
    def again(e):
        e.narrate(["…", "Stone, cold air. A new body, the same as the last."])
        e.if_var(VAR('Deaths'), '>=', 4,
                 lambda b: b.say(HANMA, ["Again, my Lord. Each time you come back a little",
                                         "quieter. I don't like it."], 'stern'),
                 lambda b: b.say(HANMA, ["Welcome back, my Lord. Try to keep this one",
                                         "a while longer."], 'calm'))
        e.if_var(VAR('Money Lost'), '>', 0,
                 lambda b: b.notice(["\\MONEY[\\V[3]] stayed behind with the old body."]))
    el.if_var(VAR('Deaths'), '==', 1, first, again)
    put("Vessel Revival", el)

    # 2: sleep at an inn (party healed, morning)
    el = Ev()
    el.fadeout()
    el.me('Inn1')
    el.wait(90)
    el.recover_all()
    el.set_time(7, 0)
    el.plugin('Story_Core', 'SetRestPoint', {'mapId': 0, 'x': 0, 'y': 0, 'direction': 2}, 'Set Rest Point')
    el.fadein()
    put("Inn Sleep", el)

    # 3: learn-hint shown the first time the party gains a level (called manually)
    el = Ev()
    el.notice(["\\C[6]Stat points\\C[0]: every level gives 20 points. Spend them in",
               "the menu (Stat Points). Your three best stats set",
               "your rank."])
    put("Tip: Stat Points", el)

    # 4: travel between the hubs of Act III (only the places already unlocked are offered)
    from story.ids import TRAVEL
    el = Ev()
    el.text(["Where to? (The Guild's carts and boats take you.)"])
    opts = ", ".join('["%s", %d, %d]' % (label, i + 1, SW(swname)) for i, (label, m, x, y, d, swname) in enumerate(TRAVEL))
    el.script("const all = [%s];\n"
              "const list = all.filter(o => $gameSwitches.value(o[2]) && o[1] !== $gameVariables.value(%d));\n"
              "$gameMessage.setChoices(list.map(o => o[0]).concat(['Stay']), 0, list.length);\n"
              "$gameMessage.setChoiceCallback(n => $gameVariables.setValue(%d, n < list.length ? list[n][1] : 0));\n"
              "this.setWaitMode('message');" % (opts, VAR('Travel: Here'), VAR('Travel: Choice')))
    for i, (label, m, x, y, d, swname) in enumerate(TRAVEL):
        el.if_var(VAR('Travel: Choice'), '==', i + 1,
                  lambda b, m=m, x=x, y=y, d=d, i=i: (b.fadeout(), b.var(VAR('Travel: Here'), i + 1),
                                                      b.transfer(m, x, y, d, 0), b.fadein()))
    put("Reisen", el)
    while len(L) <= 20:
        put("", Ev())
    return L

# =====================================================================
# SYSTEM
# =====================================================================
def build_system(start_map, start_x, start_y):
    Sy = load_orig('System')
    Sy["gameTitle"] = "Erdenkreis"
    Sy["currencyUnit"] = "kl"
    Sy["partyMembers"] = [1, 2]
    Sy["startMapId"], Sy["startX"], Sy["startY"] = start_map, start_x, start_y
    Sy["optDisplayTp"] = False
    Sy["optFollowers"] = True
    Sy["optSideView"] = False
    Sy["battleSystem"] = 0
    Sy["skillTypes"] = ["", "Divine Weaponry", "Spirit Arts", "Body Arts", "Passive", "Battle Magic", "Frost Arts"]
    wt = Sy["weaponTypes"]
    while len(wt) < 14:
        wt.append("")
    wt[13] = "Divine"
    at = Sy["armorTypes"]
    while len(at) < 9:
        at.append("")
    at[7], at[8] = "Uniform", "Fused Plate"
    Sy["elements"][9] = "Death"
    Sy["terms"]["params"] = ["Max HP", "Max MP", "STR", "CON", "MAG", "WIS", "DEX", "CHA", "Hit", "Evasion"]
    Sy["terms"]["messages"]["obtainGold"] = "Found \\MONEY[%1]."
    Sy["terms"]["basic"][8], Sy["terms"]["basic"][9] = "EXP", "EXP"
    Sy["switches"] = SW.array()
    Sy["variables"] = VAR.array()
    Sy["testBattlers"] = [{"actorId": 1, "level": 5, "equips": [WP["Lichtstrahl"], 0, 0, AR["Silberrüstung"],
                                                                  AR["Roter Kapuzenmantel"]]},
                          {"actorId": 2, "level": 5, "equips": [0, 0, 0, AR["Offiziersuniform"], 0]}]
    Sy["testTroopId"] = TR.get("Goblins x2", 1)
    Sy["editMapId"] = start_map
    Sy["title1Name"] = "Ruins"
    Sy["title2Name"] = ""
    Sy["titleBgm"] = {"name": "Theme4", "pan": 0, "pitch": 100, "volume": 90}
    Sy["battleBgm"] = {"name": "Battle1", "pan": 0, "pitch": 100, "volume": 90}
    Sy["battleback1Name"], Sy["battleback2Name"] = "Grassland", "Forest"
    return Sy
