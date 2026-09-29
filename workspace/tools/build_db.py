"""Builds the RPGMZ test project data (database, maps, plugins.js) into mz/out/."""
import json, os, shutil, copy, sys
sys.path.insert(0, os.path.dirname(__file__))
from dbkit import *
from mapinfo import region as reach_region

ROOT = '/home/claude/mz'
ORIG = ROOT + '/orig'
SAMPLE = '/mnt/user-data/uploads/samplemaps'
OUT = ROOT + '/out'

def load(name):
    return json.load(open(f'{ORIG}/data/{name}.json', encoding='utf-8'))

os.makedirs(OUT + '/data', exist_ok=True)
os.makedirs(OUT + '/js/plugins', exist_ok=True)

# =====================================================================
# SKILLS
# =====================================================================
def skill(sid, name, stype=0, mp=0, scope=1, dtype=0, element=0, formula="0", hit=0, anim=0, icon=0,
          desc="", note="", effects=None, msg="%1 uses %2!", speed=0, occasion=1, crit=False, success=100):
    return {"id": sid, "animationId": anim,
            "damage": {"critical": crit, "elementId": element, "formula": formula, "type": dtype, "variance": 0},
            "description": desc, "effects": effects or [], "hitType": hit, "iconIndex": icon,
            "message1": msg, "message2": "", "mpCost": mp, "name": name, "note": note, "occasion": occasion,
            "repeats": 1, "requiredWtypeId1": 0, "requiredWtypeId2": 0, "scope": scope, "speed": speed,
            "stypeId": stype, "successRate": success, "tpCost": 0, "tpGain": 0, "messageType": 1}

def sep(sid, name):
    return skill(sid, name, occasion=3, scope=0, msg="")

def blank_skill(sid):
    return skill(sid, "", occasion=3, scope=0, msg="")

MAGIC, TECH = 1, 2
ADD_STATE, REMOVE_STATE, BUFF, DEBUFF = 21, 22, 31, 32
def eff(code, data, v1=1, v2=0):
    return {"code": code, "dataId": data, "value1": v1, "value2": v2}

orig_skills = load('Skills')
attack = copy.deepcopy(orig_skills[1])
attack["note"] = ("Skill #1 is the Attack command.\n"
                  "Plain attack: weapon die + POW(weapon stat) + 10 x weapon rank.\n"
                  "It never gains mastery.")
guard = copy.deepcopy(orig_skills[2])

S = [None, attack, guard]
S.append(sep(3, "-----Fighter"))
S.append(skill(4, "Power Strike", TECH, mp=2, scope=1, dtype=1, element=-1, formula="2d6", hit=1, anim=-1, icon=77,
               crit=True, desc="A heavy 2d6 blow. Scales with STR.\nMastery: 2d8 at E, +25% at C, two strikes at A.",
               note="<Stat: STR>\n<Body>\n<At Rank E>\ndie: 2d8\n</At Rank E>\n<At Rank C>\ndamage: 125%\n</At Rank C>\n<At Rank A>\nhits: 2\n</At Rank A>"))
S.append(skill(5, "War Cry", TECH, mp=3, scope=8, anim=51, icon=34, msg="%1 lets out a war cry!",
               effects=[eff(BUFF, 2, 3)],
               desc="Rallies the party: STR up for 3 turns.\nFrom rank C it also Blesses them.",
               note="<Stat: CHA>\n<Support>\n<At Rank C>\nstate: 31\n</At Rank C>"))
S.append(skill(6, "Cleave", TECH, mp=3, scope=2, dtype=1, element=-1, formula="d8", hit=1, anim=6, icon=76,
               crit=True, msg="%1 cleaves through the enemy!",
               desc="Hits every foe for half damage each. Scales with STR.\nd10 from rank D.",
               note="<Stat: STR>\n<Body>\n<At Rank D>\ndie: d10\n</At Rank D>"))
S.append(skill(7, "Shield Bash", TECH, mp=3, scope=1, dtype=1, element=-1, formula="d6", hit=1, anim=39, icon=78,
               crit=True, effects=[eff(ADD_STATE, 13, 1)],
               desc="Slams a foe: CON save or stunned for a turn.\nScales with STR.",
               note="<Stat: STR>\n<Body>\n<Save: CON states>"))
S.append(sep(8, "-----Lancer"))
S.append(skill(9, "Quick Thrust", TECH, mp=2, scope=1, dtype=1, element=-1, formula="d10", hit=1, anim=11, icon=76,
               speed=5, crit=True,
               desc="A fast thrust: +5 initiative, crits on 19-20. Scales with DEX.\nTwo strikes from rank E; becomes Flash Thrust at C.",
               note="<Stat: DEX>\n<Body>\n<Crit Range: +1>\n<At Rank E>\nhits: 2\n</At Rank E>\n<Evolve C: 12>"))
S.append(skill(10, "Pinning Strike", TECH, mp=3, scope=1, dtype=1, element=-1, formula="d8", hit=1, anim=12, icon=54,
               crit=True, effects=[eff(DEBUFF, 6, 3)],
               desc="Pins a foe: STR save or DEX down for 3 turns.\nLower DEX means lower AC and later turns.",
               note="<Stat: DEX>\n<Body>\n<Save: STR states>"))
S.append(skill(11, "Whirlwind", TECH, mp=4, scope=2, dtype=1, element=-1, formula="d8", hit=1, anim=38, icon=69,
               crit=True, msg="%1 spins through the enemy!",
               desc="Hits every foe for half damage each. Scales with DEX.",
               note="<Stat: DEX>\n<Body>"))
S.append(skill(12, "Flash Thrust", TECH, mp=3, scope=1, dtype=1, element=-1, formula="d12", hit=1, anim=26, icon=76,
               speed=8, crit=True,
               desc="Quick Thrust perfected: two strikes, crits on 18-20.\nThree strikes from rank A.",
               note="<Stat: DEX>\n<Body>\n<Crit Range: +2>\n<At Rank C>\nhits: 2\n</At Rank C>\n<At Rank A>\nhits: 3\n</At Rank A>"))
S.append(sep(13, "-----Cleric"))
S.append(skill(14, "Mend", MAGIC, mp=3, scope=7, dtype=3, formula="2d4", anim=41, icon=72, occasion=0,
               msg="%1 casts %2!",
               desc="Heals one ally for 2d4. Scales with WIS.\n2d8 from rank D, which also teaches Group Mend.",
               note="<Stat: WIS>\n<At Rank D>\ndie: 2d8\n</At Rank D>\n<Unlock D: 18>"))
S.append(skill(15, "Radiance", MAGIC, mp=3, scope=1, dtype=1, element=8, formula="d10", hit=0, anim=96, icon=70,
               msg="%1 casts %2!",
               desc="Searing light on one foe; a DEX save halves it.\nScales with WIS.",
               note="<Stat: WIS>\n<Save: DEX>"))
S.append(skill(16, "Bless", MAGIC, mp=4, scope=8, anim=52, icon=70, msg="%1 casts %2!",
               effects=[eff(ADD_STATE, 31, 1)],
               desc="Blesses the party for 3 turns: +2 to hit, +1 AC.",
               note="<Stat: WIS>\n<Support>"))
S.append(skill(17, "Purify", MAGIC, mp=2, scope=7, anim=45, icon=72, occasion=0, msg="%1 casts %2!",
               effects=[eff(REMOVE_STATE, 4), eff(REMOVE_STATE, 5), eff(REMOVE_STATE, 6), eff(REMOVE_STATE, 10),
                        eff(REMOVE_STATE, 12), eff(REMOVE_STATE, 13)],
               desc="Cures poison, blindness, silence, sleep, paralysis and stun.",
               note="<Stat: WIS>\n<Support>"))
S.append(skill(18, "Group Mend", MAGIC, mp=5, scope=8, dtype=3, formula="2d6", anim=43, icon=72, occasion=0,
               msg="%1 casts %2!",
               desc="Heals the whole party at 75% power each. Scales with WIS.",
               note="<Stat: WIS>\n<Area Rate: 75%>"))
S.append(sep(19, "-----Mage"))
S.append(skill(20, "Firebolt", MAGIC, mp=3, scope=1, dtype=1, element=2, formula="d10", hit=2, anim=66, icon=64,
               crit=True, msg="%1 casts %2!",
               desc="A d10 bolt of fire at one foe. Scales with MAG.\nd12 from rank E; rank D teaches Fireball.",
               note="<Stat: MAG>\n<At Rank E>\ndie: d12\n</At Rank E>\n<Unlock D: 24>"))
S.append(skill(21, "Frost Shard", MAGIC, mp=3, scope=1, dtype=1, element=3, formula="d8", hit=2, anim=71, icon=65,
               crit=True, msg="%1 casts %2!", effects=[eff(DEBUFF, 6, 3)],
               desc="An ice shard at one foe. On a hit: CON save or DEX down.\nScales with MAG.",
               note="<Stat: MAG>\n<Save: CON states>"))
S.append(skill(22, "Spark Storm", MAGIC, mp=5, scope=2, dtype=1, element=4, formula="d8", hit=2, anim=78, icon=66,
               msg="%1 casts %2!",
               desc="Lightning on every foe, half damage each. Scales with MAG.",
               note="<Stat: MAG>"))
S.append(skill(23, "Sleep", MAGIC, mp=3, scope=1, anim=62, icon=8, msg="%1 casts %2!",
               effects=[eff(ADD_STATE, 10, 1)],
               desc="Puts one foe to sleep unless it makes a WIS save.\nBosses shrug off every second attempt.",
               note="<Stat: MAG>\n<Save: WIS>"))
S.append(skill(24, "Fireball", MAGIC, mp=6, scope=2, dtype=1, element=2, formula="3d6", hit=0, anim=68, icon=64,
               msg="%1 casts %2!",
               desc="Fire bursts over every foe (half each); a DEX save halves it again.",
               note="<Stat: MAG>\n<Save: DEX>\n<DC: +1>"))
S.append(sep(25, "-----Enemy"))
S.append(skill(26, "Bite", TECH, scope=1, dtype=1, element=1, formula="d6", hit=1, anim=16, icon=76,
               crit=True, msg="%1 bites!", note="<Stat: STR>"))
S.append(skill(27, "Spore Cloud", TECH, scope=2, anim=33, icon=8, msg="%1 releases a cloud of spores!",
               effects=[eff(ADD_STATE, 10, 1)], note="<Stat: MAG>\n<Save: CON>"))
S.append(skill(28, "Crushing Blow", TECH, scope=1, dtype=1, element=1, formula="d10", hit=1, anim=39, icon=78,
               crit=True, msg="%1 swings a crushing blow!", note="<Stat: STR>\n<Damage: 125%>"))
S.append(skill(29, "Howl", TECH, scope=8, anim=37, icon=34, msg="%1 howls!",
               effects=[eff(BUFF, 2, 3)], note="<Stat: CHA>"))
S.append(skill(30, "Root Snare", TECH, scope=1, dtype=1, element=6, formula="d4", hit=1, anim=57, icon=54,
               crit=True, msg="%1 lashes out with its roots!", effects=[eff(DEBUFF, 6, 3)],
               note="<Stat: STR>\n<Save: STR states>"))
S.append(skill(31, "Gust", TECH, scope=2, dtype=1, element=7, formula="d6", hit=0, anim=93, icon=69,
               msg="%1 whips up a gust!", note="<Stat: DEX>\n<Save: DEX>"))
S.append(skill(32, "Ember", MAGIC, scope=1, dtype=1, element=2, formula="d6", hit=2, anim=66, icon=64,
               crit=True, msg="%1 spits embers!", note="<Stat: MAG>"))
S.append(skill(33, "Stand Still", TECH, scope=0, anim=0, icon=81, msg="%1 stands perfectly still.",
               note="<No Mastery>"))
while len(S) <= 50:
    S.append(blank_skill(len(S)))
assert all(S[i]["id"] == i for i in range(1, len(S)))
write_list(OUT + '/data/Skills.json', S)

# =====================================================================
# ITEMS
# =====================================================================
def item(iid, name, icon, price, desc, effects, scope=7, occasion=0, anim=41, note=""):
    return {"id": iid, "animationId": anim, "consumable": True,
            "damage": {"critical": False, "elementId": 0, "formula": "0", "type": 0, "variance": 20},
            "description": desc, "effects": effects, "hitType": 0, "iconIndex": icon, "itypeId": 1,
            "name": name, "note": note, "occasion": occasion, "price": price, "repeats": 1, "scope": scope,
            "speed": 0, "successRate": 100, "tpGain": 0}

I = [None,
     item(1, "Potion", 176, 30, "Restores 40 HP.", [eff(11, 0, 0, 40)]),
     item(2, "Hi-Potion", 176, 150, "Restores 150 HP.", [eff(11, 0, 0, 150)]),
     item(3, "Ether", 176, 120, "Restores 20 MP.", [eff(12, 0, 0, 20)]),
     item(4, "Antidote", 176, 20, "Cures poison.", [eff(REMOVE_STATE, 4)], anim=45),
     item(5, "Remedy", 176, 100, "Cures poison, blindness, silence, sleep, paralysis and stun.",
          [eff(REMOVE_STATE, s) for s in (4, 5, 6, 10, 12, 13)], anim=46),
     item(6, "Elixir", 176, 1000, "Fully restores HP and MP.", [eff(11, 0, 1, 0), eff(12, 0, 1, 0)]),
     item(7, "Ward Incense", 176, 60, "Halves random encounters for a while.", [eff(ADD_STATE, 29, 1)],
          scope=11, occasion=2, anim=51),
     item(8, "Seed of Might", 34, 500, "STR +5 permanently.", [eff(42, 2, 5)], occasion=2, anim=51),
     item(9, "Seed of Vigor", 35, 500, "CON +5 permanently.", [eff(42, 3, 5)], occasion=2, anim=51),
     item(10, "Seed of Mana", 36, 500, "MAG +5 permanently.", [eff(42, 4, 5)], occasion=2, anim=51)]
while len(I) <= 20:
    I.append(item(len(I), "", 0, 0, "", [], occasion=3, anim=0))
write_list(OUT + '/data/Items.json', I)

# =====================================================================
# WEAPONS  (Attack box = die size)
# =====================================================================
def weapon(wid, name, wtype, die, icon, anim, price, desc, note=""):
    return {"id": wid, "animationId": anim, "description": desc, "etypeId": 1,
            "traits": [{"code": 31, "dataId": 1, "value": 0}, {"code": 22, "dataId": 0, "value": 0}],
            "iconIndex": icon, "name": name, "note": note, "params": [0, 0, die, 0, 0, 0, 0, 0],
            "price": price, "wtypeId": wtype}

SWORD, FLAIL, AXE, STAFF, DAGGER, SPEAR = 2, 3, 4, 6, 1, 12
W = [None,
     weapon(1, "Short Sword", SWORD, 6, 97, 6, 50, "[Sword] d6 · STR"),
     weapon(2, "Longsword", SWORD, 8, 97, 6, 150, "[Sword] d8 · STR"),
     weapon(3, "Steel Longsword", SWORD, 8, 97, 6, 1200, "[Sword] d8 · STR · rank E: +10 damage", "<Rank: E>"),
     weapon(4, "Battle Axe", AXE, 10, 99, 6, 240, "[Axe] d10 · STR · -1 to hit", "<Hit: -1>"),
     weapon(5, "Dagger", DAGGER, 4, 96, 6, 40, "[Dagger] d4 · DEX · crits on 19-20", "<Stat: DEX>\n<Crit Range: +1>"),
     weapon(6, "Spear", SPEAR, 8, 107, 11, 140, "[Spear] d8 · DEX", "<Stat: DEX>"),
     weapon(7, "Steel Spear", SPEAR, 8, 107, 11, 1200, "[Spear] d8 · DEX · rank E: +10 damage", "<Stat: DEX>\n<Rank: E>"),
     weapon(8, "Oak Staff", STAFF, 6, 101, 1, 60, "[Staff] d6 · STR · MAG +5", "<MAG: +5>"),
     weapon(9, "Mace", FLAIL, 6, 98, 1, 90, "[Flail] d6 · STR · WIS +3", "<WIS: +3>"),
     weapon(10, "Ash Wand", STAFF, 4, 101, 1, 1100, "[Staff] d4 · rank E · MAG +15", "<Rank: E>\n<MAG: +15>")]
while len(W) <= 20:
    W.append(weapon(len(W), "", 0, 0, 0, 0, 0, ""))
write_list(OUT + '/data/Weapons.json', W)

# =====================================================================
# ARMORS  (Defense box = ARMOR value)
# =====================================================================
def armor(aid, name, atype, etype, value, icon, price, desc, note=""):
    return {"id": aid, "atypeId": atype, "description": desc, "etypeId": etype,
            "traits": [{"code": 22, "dataId": 1, "value": 0}], "iconIndex": icon, "name": name, "note": note,
            "params": [0, 0, 0, value, 0, 0, 0, 0], "price": price}

GEN, MAGA, LIGHT, HEAVY, SSHIELD, LSHIELD = 1, 2, 3, 4, 5, 6
E_SHIELD, E_HEAD, E_BODY, E_ACC = 2, 3, 4, 5
A = [None,
     armor(1, "Traveler's Clothes", GEN, E_BODY, 1, 135, 20, "[Body] Armor 1"),
     armor(2, "Leather Armor", LIGHT, E_BODY, 2, 136, 90, "[Body · Light] Armor 2"),
     armor(3, "Chain Mail", HEAVY, E_BODY, 4, 137, 300, "[Body · Heavy] Armor 4"),
     armor(4, "Plate Armor", HEAVY, E_BODY, 7, 137, 1800,
           "[Body · Heavy] Armor 7 · rank E: below STR E it costs\n2 AC and 5 initiative", "<Rank: E>"),
     armor(5, "Apprentice Robe", MAGA, E_BODY, 1, 139, 70, "[Body · Magic] Armor 1 · MAG +5", "<MAG: +5>"),
     armor(6, "Buckler", SSHIELD, E_SHIELD, 1, 129, 60, "[Shield] +1 AC"),
     armor(7, "Kite Shield", LSHIELD, E_SHIELD, 2, 128, 220, "[Shield · Large] +2 AC"),
     armor(8, "Leather Cap", LIGHT, E_HEAD, 0, 130, 40, "[Head] CON +2", "<CON: +2>"),
     armor(9, "Iron Helm", HEAVY, E_HEAD, 1, 132, 180, "[Head · Heavy] +1 AC"),
     armor(10, "Ring of Vigor", GEN, E_ACC, 0, 147, 300, "[Accessory] CON +5", "<CON: +5>"),
     armor(11, "Swift Anklet", GEN, E_ACC, 0, 147, 300, "[Accessory] DEX +5", "<DEX: +5>"),
     armor(12, "Sage's Pendant", GEN, E_ACC, 0, 147, 400, "[Accessory] INT +10: cheaper skills, faster mastery", "<INT: +10>")]
while len(A) <= 20:
    A.append(armor(len(A), "", 0, E_BODY, 0, 0, 0, ""))
write_list(OUT + '/data/Armors.json', A)

# =====================================================================
# STATES
# =====================================================================
St = load('States')
St[5]["note"] = "<Hit: -4>"
blessed = copy.deepcopy(St[4])
blessed.update({"id": 31, "name": "Blessed", "iconIndex": 70, "autoRemovalTiming": 2, "minTurns": 3, "maxTurns": 3,
                "message1": "%1 is blessed!", "message2": "%1 is blessed!", "message3": "",
                "message4": "%1's blessing fades.", "motion": 0, "overlay": 0, "priority": 40,
                "removeAtBattleEnd": True, "restriction": 0, "traits": [], "note": "<Hit: +2>\n<AC: +1>"})
while len(St) < 31:
    St.append(None)
St = St[:31] + [blessed]
write_list(OUT + '/data/States.json', St)

# =====================================================================
# CLASSES
# =====================================================================
C0 = load('Classes')
params_template = C0[1]["params"]

def klass(cid, name, crit, stype, wtypes, atypes, learnings, note):
    traits = [{"code": 23, "dataId": 0, "value": 1},
              {"code": 22, "dataId": 0, "value": 0.95},
              {"code": 22, "dataId": 1, "value": 0.05},
              {"code": 22, "dataId": 2, "value": crit},
              {"code": 41, "dataId": stype, "value": 0}]
    traits += [{"code": 51, "dataId": w, "value": 0} for w in wtypes]
    traits += [{"code": 52, "dataId": a, "value": 0} for a in atypes]
    return {"id": cid, "expParams": [30, 20, 30, 30], "traits": traits,
            "learnings": [{"level": l, "note": "", "skillId": s} for l, s in learnings],
            "name": name, "note": note, "params": copy.deepcopy(params_template)}

C = [None,
     klass(1, "Fighter", 0, TECH, [SWORD, AXE, FLAIL], [GEN, LIGHT, HEAVY, SSHIELD, LSHIELD],
           [(1, 4), (4, 5), (7, 6), (10, 7)],
           "<Aptitude: STR A, DEX C, CON A, INT E, WIS D, CHA B, MAG E>\n<Saves: STR, CON>"),
     klass(2, "Lancer", 0.05, TECH, [SPEAR, DAGGER, SWORD], [GEN, LIGHT, SSHIELD],
           [(1, 9), (4, 10), (7, 11)],
           "<Aptitude: STR B, DEX A, CON B, INT D, WIS D, CHA C, MAG E>\n<Saves: DEX, STR>"),
     klass(3, "Cleric", 0, MAGIC, [FLAIL, STAFF], [GEN, MAGA, LIGHT, SSHIELD],
           [(1, 14), (1, 15), (5, 16), (8, 17)],
           "<Aptitude: STR D, DEX D, CON B, INT C, WIS A, CHA B, MAG B>\n<Saves: WIS, CHA>"),
     klass(4, "Mage", 0, MAGIC, [STAFF, DAGGER], [GEN, MAGA],
           [(1, 20), (3, 21), (6, 22), (9, 23)],
           "<Aptitude: STR E, DEX C, CON D, INT A, WIS C, CHA D, MAG A>\n<Saves: INT, MAG>")]
write_list(OUT + '/data/Classes.json', C)

# =====================================================================
# ACTORS  (all stats start at 1; 20 points to assign)
# =====================================================================
def actor(aid, name, cid, equips, index, battler, profile):
    return {"id": aid, "battlerName": battler, "characterIndex": index, "characterName": "Actor1",
            "classId": cid, "equips": equips, "faceIndex": index, "faceName": "Actor1", "traits": [],
            "initialLevel": 1, "maxLevel": 99, "name": name, "nickname": "", "note": "", "profile": profile}

Ac = [None,
      actor(1, "Reid", 1, [2, 6, 8, 2, 0], 0, "Actor1_1",
            "Test fighter. Grows STR and CON fastest.\nSwords, axes, heavy armor, shields."),
      actor(2, "Michelle", 2, [6, 0, 8, 2, 0], 3, "Actor1_4",
            "Test lancer. Grows DEX fastest.\nSpears and daggers, light armor."),
      actor(3, "Eliot", 3, [9, 6, 0, 1, 0], 6, "Actor1_7",
            "Test cleric. Grows WIS fastest.\nHeals scale with WIS."),
      actor(4, "Kasey", 4, [8, 0, 0, 5, 0], 5, "Actor1_6",
            "Test mage. Grows MAG and INT fastest.\nSpells scale with MAG; INT cuts MP costs.")]
write_list(OUT + '/data/Actors.json', Ac)

# =====================================================================
# ENEMIES  (Attack=STR Defense=CON M.Attack=MAG M.Defense=WIS Agility=DEX Luck=CHA)
# =====================================================================
def act(skill_id, rating):
    return {"conditionParam1": 0, "conditionParam2": 0, "conditionType": 0, "rating": rating, "skillId": skill_id}

def drop(kind=0, data=1, denom=1):
    return {"dataId": data, "denominator": denom, "kind": kind}

def enemy(eid, name, battler, mhp, st, exp, gold, actions, note, hue=0, drops=None, extra=None):
    params = [mhp, 0, st['STR'], st['CON'], st['MAG'], st['WIS'], st['DEX'], st['CHA']]
    traits = [{"code": 22, "dataId": 0, "value": 0.95}, {"code": 22, "dataId": 1, "value": 0.05},
              {"code": 31, "dataId": 1, "value": 0}] + (extra or [])
    d = (drops or []) + [drop()] * 3
    return {"id": eid, "actions": actions, "battlerHue": hue, "battlerName": battler, "dropItems": d[:3],
            "exp": exp, "traits": traits, "gold": gold, "name": name, "note": note, "params": params}

def stats(STR, DEX, CON, WIS, CHA, MAG):
    return dict(STR=STR, DEX=DEX, CON=CON, WIS=WIS, CHA=CHA, MAG=MAG)

def weak(element, rate=2.0):
    return {"code": 11, "dataId": element, "value": rate}

FIRE, ICE, THUNDER, LIGHT_EL = 2, 3, 4, 8
E = [None,
     enemy(1, "Crow", "Crow", 8, stats(10, 34, 14, 10, 4, 1), 4, 2, [act(1, 5)],
           "<Rank: F>\n<Role: minion>\n<Attack Die: d4>\n<Attack Stat: DEX>", extra=[weak(THUNDER, 1.5)]),
     enemy(2, "Goblin", "Goblin", 22, stats(24, 16, 22, 8, 8, 1), 8, 6, [act(1, 5)],
           "<Rank: F>\n<Attack Die: d6>", drops=[drop(1, 1, 4)]),
     enemy(3, "Mushroom", "Matango", 26, stats(12, 6, 26, 18, 2, 20), 8, 5, [act(1, 5), act(27, 3)],
           "<Rank: F>\n<Attack Die: d4>\n<Armor: 1>", drops=[drop(1, 4, 3)], extra=[weak(FIRE)]),
     enemy(4, "Wild Wolf", "SF_Wolf", 60, stats(32, 38, 30, 12, 6, 1), 20, 14, [act(1, 5), act(29, 3)],
           "<Rank: F>\n<Role: elite>\n<Attack Die: d6>\n<Attack Stat: DEX>", drops=[drop(1, 1, 2)]),
     enemy(5, "Goblin Chief", "Goblin", 320, stats(48, 22, 52, 14, 34, 1), 96, 80,
           [act(1, 5), act(28, 5), act(29, 3)],
           "<Rank: F>\n<Role: boss>\n<Attack Die: d8>\n<Armor: 4>", hue=200, drops=[drop(2, 4, 2)]),
     enemy(6, "Imp", "Petitdevil", 55, stats(100, 150, 110, 120, 110, 150), 15, 20, [act(1, 4), act(32, 5)],
           "<Rank: E>\n<Role: minion>\n<Attack Die: d4>\n<Attack Stat: DEX>", drops=[drop(1, 3, 4)]),
     enemy(7, "Frilled Lizard", "Frilledlizard", 135, stats(145, 110, 135, 80, 30, 20), 30, 30,
           [act(1, 5), act(26, 5)], "<Rank: E>\n<Attack Die: d8>", drops=[drop(1, 2, 4)], extra=[weak(ICE, 1.5)]),
     enemy(8, "Harpy", "Harpy", 115, stats(110, 165, 115, 100, 120, 90), 30, 32, [act(1, 5), act(31, 4)],
           "<Rank: E>\n<Attack Die: d6>\n<Attack Stat: DEX>", drops=[drop(1, 3, 4)], extra=[weak(THUNDER, 1.5)]),
     enemy(9, "Treant", "Treant", 480, stats(150, 60, 190, 140, 50, 120), 75, 60, [act(1, 5), act(30, 4)],
           "<Rank: E>\n<Role: elite>\n<Attack Die: d8>\n<Armor: 12>", drops=[drop(1, 2, 2)], extra=[weak(FIRE)]),
     enemy(10, "Wolfman", "Wolfman", 1100, stats(185, 170, 180, 110, 150, 40), 360, 300,
           [act(1, 5), act(28, 5), act(29, 3)], "<Rank: E>\n<Role: boss>\n<Attack Die: d10>",
           drops=[drop(1, 6, 1)]),
     enemy(11, "Stone Sentinel", "Stoneknight", 999, stats(1, 1, 380, 300, 1, 320), 0, 0, [act(33, 5)],
           "<Rank: C>\n<AC: 12>")]
while len(E) <= 20:
    E.append(enemy(len(E), "", "", 1, stats(1, 1, 1, 1, 1, 1), 0, 0, [act(1, 5)], ""))
write_list(OUT + '/data/Enemies.json', E)

# =====================================================================
# TROOPS
# =====================================================================
def troop(tid, name, members):
    return {"id": tid, "members": [{"enemyId": e, "x": x, "y": y, "hidden": False} for e, x, y in members],
            "name": name,
            "pages": [{"conditions": {"actorHp": 50, "actorId": 1, "actorValid": False, "enemyHp": 50,
                                      "enemyIndex": 0, "enemyValid": False, "switchId": 1, "switchValid": False,
                                      "turnA": 0, "turnB": 0, "turnEnding": False, "turnValid": False},
                       "list": [{"code": 0, "indent": 0, "parameters": []}], "span": 0}]}

Y = 436
T = [None,
     troop(1, "Crows x3", [(1, 228, Y - 60), (1, 408, Y - 30), (1, 588, Y - 60)]),
     troop(2, "Goblins x2", [(2, 300, Y), (2, 516, Y)]),
     troop(3, "Goblin & Mushroom", [(2, 300, Y), (3, 516, Y)]),
     troop(4, "Mushrooms x2", [(3, 300, Y), (3, 516, Y)]),
     troop(5, "Wild Wolf & Crow", [(4, 330, Y), (1, 540, Y - 40)]),
     troop(6, "Goblin Chief", [(2, 220, Y), (5, 408, Y + 10), (2, 596, Y)]),
     troop(7, "Imps x2", [(6, 300, Y - 20), (6, 516, Y - 20)]),
     troop(8, "Frilled Lizard", [(7, 408, Y)]),
     troop(9, "Harpy & Imp", [(8, 320, Y), (6, 530, Y - 20)]),
     troop(10, "Treant", [(9, 408, Y + 10)]),
     troop(11, "Wolfman", [(10, 408, Y + 10)]),
     troop(12, "Stone Sentinel", [(11, 408, Y + 10)]),
     troop(13, "Lizard & Harpy", [(7, 300, Y), (8, 520, Y)])]
while len(T) <= 20:
    T.append(troop(len(T), "", []))
write_list(OUT + '/data/Troops.json', T)

# =====================================================================
# SYSTEM
# =====================================================================
Sy = load('System')
Sy["partyMembers"] = [1, 2, 3, 4]
Sy["startMapId"], Sy["startX"], Sy["startY"] = 1, 19, 17
Sy["optDisplayTp"] = False
Sy["skillTypes"] = ["", "Magic", "Technique"]
Sy["terms"]["params"] = ["Max HP", "Max MP", "STR", "CON", "MAG", "WIS", "DEX", "CHA", "Hit", "Evasion"]
Sy["testBattlers"] = [{"actorId": 1, "level": 1, "equips": [2, 6, 8, 2, 0]},
                      {"actorId": 2, "level": 1, "equips": [6, 0, 8, 2, 0]},
                      {"actorId": 3, "level": 1, "equips": [9, 6, 0, 1, 0]},
                      {"actorId": 4, "level": 1, "equips": [8, 0, 0, 5, 0]}]
Sy["testTroopId"] = 2
Sy["editMapId"] = 1
write_obj(OUT + '/data/System.json', Sy)

# =====================================================================
# MAPS
# =====================================================================
def load_sample(n):
    return json.load(open(f'{SAMPLE}/Map{n:03d}.json', encoding='utf-8'))

def bgm(name, volume=90):
    return {"name": name, "pan": 0, "pitch": 100, "volume": volume}

def next_id(m):
    return len(m['events'])

def add_event(m, name, x, y, pages, note=""):
    eid = next_id(m)
    m['events'].append(event(eid, name, x, y, pages, note))
    return eid

def transfer_events(m, name, tiles, map_id, x, y, direction):
    for tx, ty in tiles:
        el = EventList().se("Move1", 60).transfer(map_id, x, y, direction, 0)
        add_event(m, name, tx, ty, [page(el.done(), trigger=1, priority=0)])

def chest(m, name, x, y, give, label):
    el = EventList().se("Chest1")
    el.move_route(0, [(36, []), (17, []), (15, [3]), (18, []), (15, [3]), (19, []), (35, [])])
    give(el)
    el.text([label])
    el.self_switch("A")
    p1 = page(el.done(), char="!Chest", index=0, direction=2, pattern=0, trigger=0, priority=1,
              walk_anime=False, direction_fix=True)
    p2 = page(None, char="!Chest", index=0, direction=8, pattern=0, trigger=0, priority=1,
              self_switch="A", walk_anime=False, direction_fix=True)
    return add_event(m, name, x, y, [p1, p2])

GUIDE = ("People1", 4)
HEALER = ("People2", 5)
MASTER = ("People3", 6)
TRAINER = ("People4", 4)
MENTOR = ("People2", 0)
MERCHANT = ("People1", 6)
SCOUT = ("People3", 4)

def npc_page(el, who, direction=2):
    return page(el.done(), char=who[0], index=who[1], direction=direction, trigger=0, priority=1)

def say(el, who, name, lines):
    return el.text(lines, face=who[0], face_index=who[1], name=name)

# ------------------------------------------------------------- Map 1: Hub
hub = load_sample(7)
hub.update({"displayName": "Test Town", "note": "<Area Name: Test Town>", "autoplayBgm": True,
            "bgm": bgm("Town1"), "encounterList": [], "encounterStep": 30})

el = EventList()
el.text(["Test build of the rank system.",
         "Everyone starts at level 1, every stat at 1,",
         "with 20 points to spend.",
         "Open the menu: Stat Points."])
el.text(["Talk to the townsfolk to test battles, levels",
         "and skill mastery. The south gate leads out",
         "to the field."])
el.self_switch("A")
add_event(hub, "Intro", 0, 0, [page(el.done(), trigger=3, priority=0),
                               page(None, trigger=0, priority=0, self_switch="A")])

el = EventList()
say(el, GUIDE, "Guide", ["Welcome to the test town. Everyone here",
                         "helps you try out the rank system."])
say(el, GUIDE, "Guide", ["Ranks run F to V:",
                         "\\RK[0]\\RK[1]\\RK[2]\\RK[3]\\RK[4]\\RK[5]\\RK[6]\\RK[7]\\RK[8]\\RK[9]",
                         "Each stat is graded by hundreds: 0-99 is F,",
                         "100-199 is E, and so on up to V."])
say(el, GUIDE, "Guide", ["Your rank is the average of your three best",
                         "stats. Every level gives 20 points to",
                         "assign: Menu > Stat Points."])
say(el, GUIDE, "Guide", ["Skills that cost MP grow when you use them",
                         "in battle. A full bar needs a breakthrough:",
                         "finish a foe one rank above the skill",
                         "with it."])
say(el, GUIDE, "Guide", ["Outside, watch the top-right corner: area",
                         "name, area rank and the danger gauge. A red",
                         "name means the area outranks you by two."])
say(el, GUIDE, "Guide", ["Your party right now:",
                         "\\N[1] \\RKA[1]   \\N[2] \\RKA[2]",
                         "\\N[3] \\RKA[3]   \\N[4] \\RKA[4]"])
add_event(hub, "Guide", 20, 14, [npc_page(el, GUIDE)])

el = EventList()
say(el, HEALER, "Healer", ["Rest a moment. I'll patch you up."])
el.add(314, [0, 0]).se("Recovery")
say(el, HEALER, "Healer", ["Your party is fully healed."])
add_event(hub, "Healer", 24, 16, [npc_page(el, HEALER)])

def win(e):
    say(e, MASTER, "Battle Master", ["Well fought."])
def fled(e):
    say(e, MASTER, "Battle Master", ["Running away is a skill too."])
def lost(e):
    e.add(314, [0, 0])
    say(e, MASTER, "Battle Master", ["Up you get. All patched up."])
def spar(tid):
    return lambda e: e.battle(tid, True, True, win, fled, lost)

def f_fights(e):
    e.choices(["Crows x3", "Goblins x2", "Wild Wolf (elite)", "Goblin Chief (boss)", "Back"],
              [spar(1), spar(2), spar(5), spar(6), None], cancel=4)
def e_fights(e):
    e.choices(["Frilled Lizard", "Harpy and Imp", "Treant (elite)", "Wolfman (boss)", "Back"],
              [spar(8), spar(9), spar(10), spar(11), None], cancel=4)
def wall(e):
    say(e, MASTER, "Battle Master", ["The Stone Sentinel is rank \\RK[3]. Two ranks",
                                     "below it you deal a quarter; three below,",
                                     "nothing gets through. It never fights back."])
    spar(12)(e)

el = EventList()
say(el, MASTER, "Battle Master", ["Want a sparring match? Losing here won't",
                                  "end your game; I'll drag you out."])
el.choices(["Rank F fights", "Rank E fights", "Rank wall demo", "Never mind"],
           [f_fights, e_fights, wall, None], cancel=3)
add_event(hub, "Battle Master", 12, 16, [npc_page(el, MASTER)])

def lvl(n):
    def body(e):
        e.add(316, [0, 0, 0, 0, n, True])
        say(e, TRAINER, "Trainer", ["Assign the new points: Menu > Stat Points."])
    return body
def refund(e):
    e.plugin("Rank_Core", "RefundStatPoints", "Refund Stat Points", {"actorId": "0"},
             ["Actor (0 = whole party) = 0"])
    say(e, TRAINER, "Trainer", ["Every assigned point is back to spend."])
el = EventList()
say(el, TRAINER, "Trainer", ["Short on time? I can train you up."])
el.choices(["+1 level", "+5 levels", "Refund stat points", "Never mind"], [lvl(1), lvl(5), refund, None], cancel=3)
add_event(hub, "Trainer", 23, 28, [npc_page(el, TRAINER)])

def study(e):
    e.plugin("Rank_Core", "GainMastery", "Gain Mastery", {"actorId": "0", "skillId": "0", "amount": "100"},
             ["Actor (0 = whole party) = 0", "Skill (0 = every mastery skill) = 0", "amount = 100"])
    say(e, MENTOR, "Mentor", ["Every mastery skill gained 100."])
def trial(e):
    e.plugin("Rank_Core", "CompleteBreakthrough", "Complete Breakthrough", {"actorId": "0", "skillId": "0"},
             ["Actor (0 = whole party) = 0", "Skill (0 = every full bar) = 0"])
    say(e, MENTOR, "Mentor", ["Every full bar broke through. Out there,",
                              "that takes a win over a stronger foe."])
def explain(e):
    say(e, MENTOR, "Mentor", ["Each use gives 10 mastery: x1.5 against a",
                              "higher rank, half one rank lower, nothing",
                              "two lower. INT speeds it up, and finishing",
                              "a foe with the skill adds a bonus."])
    say(e, MENTOR, "Mentor", ["Every rank adds +10 damage and raises the",
                              "MP cost. Some skills change at a rank,",
                              "evolve, or teach a new one. The skill",
                              "menu's help line shows where you stand."])
    say(e, MENTOR, "Mentor", ["A skill never works above its stat's grade:",
                              "a rank E Firebolt with MAG 80 still casts",
                              "at F. Its badge dims when that happens."])
el = EventList()
say(el, MENTOR, "Mentor", ["Mastery grows each time you use an MP skill",
                           "in battle. I can speed that up for tests."])
el.choices(["Study (+100 mastery)", "Breakthrough trial", "How does mastery work?", "Never mind"],
           [study, trial, explain, None], cancel=3)
add_event(hub, "Mentor", 10, 26, [npc_page(el, MENTOR)])

def shop(e):
    goods = [(0, i) for i in range(1, 11)] + [(1, i) for i in range(1, 11)] + [(2, i) for i in range(1, 13)]
    first = goods[0]
    e.add(302, [first[0], first[1], 0, 0, False])
    for g in goods[1:]:
        e.add(605, [g[0], g[1], 0, 0])
el = EventList()
say(el, MERCHANT, "Merchant", ["Test funds, on the house. Buy anything."])
el.add(125, [0, 0, 5000]).se("Coin").self_switch("A")
shop(el)
el2 = EventList()
say(el2, MERCHANT, "Merchant", ["Take a look."])
shop(el2)
add_event(hub, "Merchant", 26, 18, [npc_page(el, MERCHANT),
                                    page(el2.done(), char=MERCHANT[0], index=MERCHANT[1], self_switch="A")])

transfer_events(hub, "To Field", [(15, 35), (16, 35), (17, 35)], 2, 7, 37, 8)

# ------------------------------------------------------------- Map 2: Field
field = load_sample(23)
field.update({"displayName": "Meadow Path", "autoplayBgm": True, "bgm": bgm("Field1"), "encounterStep": 30,
              "note": "<Rank: F>\n<Region 2 Rank: E>\n<Safe Regions: 1>\n<Area Name: Meadow Path>"})
field["encounterList"] = [
    {"regionSet": [3], "troopId": 1, "weight": 10},
    {"regionSet": [3], "troopId": 2, "weight": 10},
    {"regionSet": [3], "troopId": 3, "weight": 8},
    {"regionSet": [3], "troopId": 4, "weight": 6},
    {"regionSet": [3], "troopId": 5, "weight": 3},
    {"regionSet": [2], "troopId": 7, "weight": 6},
    {"regionSet": [2], "troopId": 8, "weight": 6},
    {"regionSet": [2], "troopId": 9, "weight": 4}]
# regions: 2 = north stretch (rank E), 1 = cabin clearing (safe), 3 = the rest
w, h = field['width'], field['height']
reach = reach_region(field, 7, 38)
for (x, y) in reach:
    if y <= 8:
        r = 2
    elif 14 <= x <= 22 and 12 <= y <= 19:
        r = 1
    else:
        r = 3
    field['data'][(5 * h + y) * w + x] = r

transfer_events(field, "To Town", [(6, 39), (7, 39), (8, 39)], 1, 16, 34, 8)
transfer_events(field, "To Deep Woods", [(14, 0), (15, 0), (16, 0)], 3, 33, 47, 8)
el = EventList()
say(el, SCOUT, "Scout", ["North is the Deep Woods, rank \\RK[1] ground.",
                         "\\RK[0] fighters take x1.5 there and deal",
                         "half. Come back at \\RK[1], or at least with",
                         "good gear."])
say(el, SCOUT, "Scout", ["The last stretch of this path is already",
                         "rank \\RK[1]. See the corner of your screen."])
add_event(field, "Scout", 16, 3, [npc_page(el, SCOUT)])

# ------------------------------------------------------------- Map 3: Deep Woods
woods = load_sample(28)
woods.update({"displayName": "Deep Woods", "autoplayBgm": True, "bgm": bgm("Dungeon1"), "encounterStep": 25,
              "note": "<Rank: E>\n<Area Name: Deep Woods>"})
woods["encounterList"] = [
    {"regionSet": [], "troopId": 7, "weight": 8},
    {"regionSet": [], "troopId": 8, "weight": 8},
    {"regionSet": [], "troopId": 9, "weight": 6},
    {"regionSet": [], "troopId": 13, "weight": 4},
    {"regionSet": [], "troopId": 10, "weight": 3}]
transfer_events(woods, "To Field", [(32, 49), (33, 49), (34, 49)], 2, 15, 1, 2)

def boss_win(e):
    e.self_switch("A")
    e.text(["The Wolfman falls. The way north is open.", "(That's the end of the test area.)"])
def boss_fight(e):
    e.battle(11, can_escape=True, can_lose=False, win=boss_win, escape=None)
el = EventList()
el.text(["A Wolfman blocks the path north.", "Rank \\RK[1] boss. Fight it?"])
el.choices(["Fight", "Leave"], [boss_fight, None], cancel=1)
add_event(woods, "Wolfman", 33, 4, [page(el.done(), char="Monster", index=2, trigger=0, priority=1),
                                    page(None, self_switch="A", priority=0)])

chest(woods, "Chest: Steel Spear", 1, 31, lambda e: e.add(127, [7, 0, 0, 1, False]), "Found a Steel Spear!")
chest(woods, "Chest: Plate Armor", 48, 17, lambda e: e.add(128, [4, 0, 0, 1, False]), "Found Plate Armor!")
chest(woods, "Chest: Ash Wand", 23, 34, lambda e: e.add(127, [10, 0, 0, 1, False]), "Found an Ash Wand!")
chest(woods, "Chest: Elixirs", 9, 43, lambda e: e.add(126, [6, 0, 0, 2]), "Found 2 Elixirs!")

write_map(OUT + '/data/Map001.json', hub)
write_map(OUT + '/data/Map002.json', field)
write_map(OUT + '/data/Map003.json', woods)

mapinfos = [None,
            {"id": 1, "expanded": False, "name": "Hub", "order": 1, "parentId": 0, "scrollX": 840, "scrollY": 960},
            {"id": 2, "expanded": False, "name": "Field", "order": 2, "parentId": 0, "scrollX": 768, "scrollY": 960},
            {"id": 3, "expanded": False, "name": "Deep Woods", "order": 3, "parentId": 0, "scrollX": 1200, "scrollY": 1200}]
write_list(OUT + '/data/MapInfos.json', mapinfos)

# unchanged files
for name in ['Animations', 'CommonEvents', 'Tilesets']:
    shutil.copy(f'{ORIG}/data/{name}.json', f'{OUT}/data/{name}.json')

# =====================================================================
# PLUGINS
# =====================================================================
order = ['Rank_Core', 'Rank_Battle', 'Rank_Menus', 'Rank_Maps']
entries = []
for name in order:
    src = f'{ROOT}/plugins/{name}.js'
    shutil.copy(src, f'{OUT}/js/plugins/{name}.js')
    desc, params = plugin_defaults(src)
    entries.append({"name": name, "status": True, "description": desc, "parameters": params})
with open(OUT + '/js/plugins.js', 'w', encoding='utf-8') as f:
    f.write('// Generated by RPG Maker.\n// Do not edit this file directly.\nvar $plugins =\n[\n')
    f.write(',\n'.join(dumps(e) for e in entries))
    f.write('\n];\n')

print("built", OUT)
for fn in sorted(os.listdir(OUT + '/data')):
    print(' ', fn, os.path.getsize(OUT + '/data/' + fn))
