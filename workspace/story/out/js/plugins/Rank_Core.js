//=============================================================================
// Rank_Core.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [v1.0] Rank system core: 7 stats from 1, ranks F–V, stat points, per-skill mastery. Load first.
 * @author Ten & Claude
 *
 * @help Rank_Core.js  (load order: Rank_Core, Rank_Battle, Rank_Menus, Rank_Maps)
 *
 * The Erdenkreis rank system for RPG Maker MZ. This plugin holds the rules and
 * the data; Rank_Battle, Rank_Menus and Rank_Maps build on it.
 *
 * ============================================================================
 * RANKS
 * ============================================================================
 *   F E D C B A S SS SSS V  (index 0-9)
 *   Common Awakened Adept Veteran Elite Heroic Calamity Cataclysm Mythic Divine
 *   Every stat is graded by hundreds: 0-99 F, 100-199 E, ... 900-999 V.
 *   MOD = stat / 20 (to-hit, saves)   POW = stat / 4 (damage, healing)
 *   A battler's rank is the grade of the average of its three best stats
 *   (actors: base stats without gear; enemies: <Rank: X> or their stats).
 *
 * ============================================================================
 * STATS
 * ============================================================================
 *   STR DEX CON INT WIS CHA MAG, 0-999, every actor starts at 1.
 *   Level up: + Points per Level free points (Status > Stat Points), plus a
 *   little natural growth from the class aptitude. Assigned points stop at
 *   the top of the band above your rank (F: 199, E: 299 ...).
 *   HP and MP come from the formulas in the parameters.
 *
 *   The native params now mirror the stats, so buffs, traits and "Change
 *   Parameter" still work:  Attack = STR, Defense = CON, M.Attack = MAG,
 *   M.Defense = WIS, Agility = DEX, Luck = CHA  (INT has no native slot).
 *   Script: a.str a.dex a.con a.int a.wis a.cha a.mag, a.rkRank()
 *
 * ============================================================================
 * NOTETAGS
 * ============================================================================
 * Classes / Actors
 *   <Aptitude: STR A, DEX B, CON A, INT D, WIS D, CHA D, MAG E>
 *       natural growth per level: S 1.5  A 1  B 0.75  C 0.5  D 0.25  E 0
 *   <Saves: STR, CON>          trained saves (+3)
 *   <Start Points: 20>         (actor) overrides the parameter
 *   <Rank: E>                  (actor) fixed rank, e.g. a guest
 *
 * Skills
 *   Formula box: write the damage die, e.g.  d8   2d6+3   (a bare 8 = d8)
 *   MP Cost box: the base cost. Real cost = base x (rank+1)^2, INT cuts it.
 *   <Stat: DEX>                the stat it scales with
 *                              (default: physical STR, recovery WIS, else MAG)
 *   <Body>                     martial technique: half MP cost
 *   <Fixed Cost>               cost ignores rank
 *   <Start Rank: E>            mastery starts here when learned
 *   <Max Rank: B>              mastery can't go higher
 *   <No Mastery> / <Mastery>   force off / on (default: on if it costs MP)
 *   <Hit: +2>  <Crit Range: +1>  <Damage: 150%>  <Bonus: +10>
 *   <Save: DEX>                targets roll a DEX save: half damage and no
 *                              states on a success.
 *   <Save: DEX negates>        ... no damage at all on a success
 *   <Save: STR states>         ... the save only stops the states
 *   <DC: +2>                   harder save (DC = 13 + MOD(stat) + this)
 *   <Area Rate: 100%>          override the multi-target damage rate
 *   <Attack Roll> / <No Attack Roll>
 *   <Native Formula>           use the MZ formula box as JavaScript instead
 *   <At Rank C>                forms: from working rank C on
 *   die: d10                   ... new die
 *   hits: 2                    ... strikes twice
 *   damage: 125%               ... damage rate
 *   bonus: 10  hit: 1  crit: 1
 *   state: 13 50%              ... also adds state 13 (50%)
 *   </At Rank C>
 *   <Evolve C: 12>             at mastery C the skill becomes skill 12
 *                              (mastery carries over)
 *   <Unlock C: 18>             at mastery C the actor also learns skill 18
 *
 * Weapons   (Attack box = damage die: 8 means d8)
 *   <Stat: DEX>  <Rank: E>  <Die: 2d6>  <Hit: +1>  <Crit Range: +1>
 * Armors    (Defense box = ARMOR value; body armor competes with DEX MOD,
 *            shield / head / accessory add theirs on top)
 *   <Rank: E>  <Heavy>  <Armor: 6>
 * Weapons / Armors / States / Classes / Actors
 *   <STR: +10>  <DEX: -5>  <MAG: +10%>  <All Stats: +5>  <AC: +2>  <Hit: +1>
 *
 * Enemies   (HP, MP, EXP, Gold, drops, actions, traits: database)
 *   Stats come from the database boxes: Attack = STR, Defense = CON,
 *   M.Attack = MAG, M.Defense = WIS, Agility = DEX, Luck = CHA
 *   (INT = average of M.Attack and M.Defense). Tags override them:
 *   <Stats: STR 90, DEX 160, CON 100, INT 100, WIS 120, CHA 120, MAG 145>
 *   <INT: 40>   (one stat)     <STR: +10>   (bonus on top)
 *   <Rank: E>   (default: grade of the average of the 3 best stats)
 *   <Role: minion|standard|elite|boss|apex>
 *   <Attack Die: d8>  <Attack Stat: DEX>
 *   <Armor: 6>  or  <AC: 18>
 *   <Saves: DEX, MAG>   (default: elite, boss and apex are trained in all)
 *   Suggested for a party of four: HP = CON x role (minion 0.5, standard 1,
 *   elite 2.5, boss 6, apex 12); EXP = rank base (F 8, E 30, D 110, C 400,
 *   B 1400, A 5000, S 17000, SS 60000, SSS 200000, V 700000) x role
 *   (minion 0.5, standard 1, elite 2.5, boss 12, apex 40).
 *
 * ============================================================================
 * SKILL MASTERY
 * ============================================================================
 *   Every skill ranks F -> V on its own. Only skills that cost MP gain mastery
 *   (plain attacks, guard and items never do):
 *     10 per use x foe factor x (1 + INT/400), plus a kill bonus by role.
 *     Foe factor (strongest foe - skill mastery): +1 or more x1.5, 0 x1,
 *     -1 x0.5, -2 or less x0.
 *   Bars: 180 360 560 800 1100 1450 1900 2500 3300.
 *   Breakthrough: a full bar needs the skill to finish a foe of the next rank
 *   (support skills: be used in a won fight against one). Turn Breakthrough
 *   off and skills rank up as soon as the bar fills.
 *   A skill works at the lower of its mastery and its stat's grade.
 *   Each rank gained adds +5 (parameter) to the skill's stat.
 *   Working rank: damage die + POW(stat) + 10 x rank, MP x (rank+1)^2.
 *
 * ============================================================================
 * PLUGIN COMMANDS
 * ============================================================================
 *   Gain Stat Points, Refund Stat Points, Set Mastery, Gain Mastery,
 *   Complete Breakthrough.
 *
 * Text codes (any window):  \RK[n]  rank badge n (0 F ... 9 V)
 *                           \RKA[n] actor n's rank badge
 *
 * @param Rank Titles
 * @desc Title per rank, F to V.
 * @default Common,Awakened,Adept,Veteran,Elite,Heroic,Calamity,Cataclysm,Mythic,Divine
 *
 * @param Rank Colors
 * @desc Badge color per rank, F to V (hex).
 * @default #a8a8a8,#8fd06a,#6ab0e8,#b58aff,#f3d34a,#ff9a4c,#ff5a52,#ff7ad0,#ffffff,#fff2b0
 *
 * @param Level 1 Stat
 * @text Starting stat value
 * @type number
 * @min 0
 * @default 1
 *
 * @param Starting Points
 * @text Starting stat points
 * @type number
 * @min 0
 * @default 20
 *
 * @param Points per Level
 * @text Stat points per level
 * @type number
 * @min 0
 * @default 20
 *
 * @param Aptitude Values
 * @text Aptitude growth per level
 * @desc Natural growth per level for each aptitude grade.
 * @default S:1.5, A:1, B:0.75, C:0.5, D:0.25, E:0
 *
 * @param Default Aptitude
 * @desc Used when a class has no <Aptitude> tag.
 * @default STR C, DEX C, CON C, INT C, WIS C, CHA C, MAG C
 *
 * @param Actor Rank Mode
 * @type select
 * @option Power Level (avg of 3 best base stats)
 * @value pl
 * @option Level band (F 1-10, E 11-20 ...)
 * @value level
 * @default pl
 *
 * @param Max HP Formula
 * @text Actor Max HP
 * @desc JavaScript. a, level, rank, str, dex, con, int, wis, cha, mag
 * @default 10 + 2 * con + 5 * level
 *
 * @param Max MP Formula
 * @text Actor Max MP
 * @desc JavaScript. a, level, rank, str, dex, con, int, wis, cha, mag
 * @default mag * (0.8 + 0.5 * rank) + 2 * level + 8
 *
 * @param Body Slot
 * @text Body armor equip type
 * @desc Equip type ID whose armor competes with DEX MOD for AC.
 * @type number
 * @default 4
 *
 * @param EXP Curve
 * @type select
 * @option Rank curve (Erdenkreis)
 * @value rank
 * @option Database (class EXP curve)
 * @value database
 * @default rank
 *
 * @param EXP Anchors
 * @text Rank curve anchors
 * @desc level:expected rank. Where the party usually reaches each rank.
 * @default 1:0, 13:1, 27:2, 40:3, 53:4, 67:5, 80:6, 93:7, 99:7.5
 *
 * @param EXP Gap Rates
 * @desc EXP rate by (enemy rank - actor rank): -2 or less, -1, 0, +1, +2 or more.
 * @default 0, 0.5, 1, 1.5, 2
 *
 * @param Mastery Bars
 * @desc Mastery needed F>E, E>D ... SSS>V.
 * @default 180, 360, 560, 800, 1100, 1450, 1900, 2500, 3300
 *
 * @param Mastery Per Use
 * @type number
 * @decimals 1
 * @default 10
 *
 * @param Mastery INT Divisor
 * @desc Mastery gain x (1 + INT / this).
 * @type number
 * @default 400
 *
 * @param Mastery Kill Bonus
 * @desc Extra mastery when a skill finishes a foe, by role.
 * @default minion:5, standard:10, elite:25, boss:75, apex:200
 *
 * @param Breakthrough
 * @text Mastery breakthrough
 * @desc A full bar needs a next-rank foe finished with the skill.
 * @type boolean
 * @default true
 *
 * @param Mastery Stat Bonus
 * @desc Permanent bonus to a skill's stat for every mastery rank it gains.
 * @type number
 * @default 5
 *
 * @param Menu Use Mastery
 * @text Mastery from menu use
 * @desc Mastery gained per use outside battle (foe factor 1).
 * @type number
 * @default 0
 *
 * @param Body Cost Rate
 * @type number
 * @decimals 2
 * @default 0.5
 *
 * @param INT Cost Divisor
 * @desc MP cost x (1 - INT / this), cut capped by Max INT Cut.
 * @type number
 * @default 2000
 *
 * @param Max INT Cut
 * @type number
 * @decimals 2
 * @default 0.5
 *
 * @param Level Up Text
 * @desc %1 = actor, %2 = points
 * @default %1 gained %2 stat points!
 *
 * @param Mastery Rank Up Text
 * @desc %1 = actor, %2 = skill, %3 = rank letter, %4 = rank title
 * @default %1's %2 reached rank %3!
 *
 * @command GainStatPoints
 * @text Gain Stat Points
 * @arg actorId
 * @text Actor (0 = whole party)
 * @type actor
 * @default 0
 * @arg amount
 * @type number
 * @min -9999
 * @default 20
 *
 * @command RefundStatPoints
 * @text Refund Stat Points
 * @desc Returns every assigned point (respec).
 * @arg actorId
 * @text Actor (0 = whole party)
 * @type actor
 * @default 0
 *
 * @command SetMastery
 * @text Set Mastery
 * @arg actorId
 * @type actor
 * @default 1
 * @arg skillId
 * @type skill
 * @default 1
 * @arg rank
 * @type select
 * @option F
 * @option E
 * @option D
 * @option C
 * @option B
 * @option A
 * @option S
 * @option SS
 * @option SSS
 * @option V
 * @default F
 * @arg exp
 * @type number
 * @default 0
 *
 * @command GainMastery
 * @text Gain Mastery
 * @arg actorId
 * @text Actor (0 = whole party)
 * @type actor
 * @default 0
 * @arg skillId
 * @text Skill (0 = every mastery skill)
 * @type skill
 * @default 0
 * @arg amount
 * @type number
 * @default 100
 *
 * @command CompleteBreakthrough
 * @text Complete Breakthrough
 * @desc Ranks up skills whose bar is full (a trial, a teacher, a story beat).
 * @arg actorId
 * @text Actor (0 = whole party)
 * @type actor
 * @default 0
 * @arg skillId
 * @text Skill (0 = every full bar)
 * @type skill
 * @default 0
 */

(() => {
    "use strict";
    const PLUGIN = "Rank_Core";
    const P = PluginManager.parameters(PLUGIN) || {};

    //-------------------------------------------------------------------------
    // Parameter helpers
    //-------------------------------------------------------------------------
    const has = v => v !== undefined && v !== null && String(v).trim() !== "";
    const num = (v, d) => (has(v) && !isNaN(Number(v)) ? Number(v) : d);
    const bool = (v, d) => (has(v) ? String(v).trim() === "true" : d);
    const text = (v, d) => (has(v) ? String(v) : d);
    const csv = (v, d) => text(v, d).split(",").map(s => s.trim()).filter(s => s.length > 0);

    const Rank = (window.Rank = window.Rank || {});
    Rank.VERSION = "1.0.0";
    Rank.LETTERS = ["F", "E", "D", "C", "B", "A", "S", "SS", "SSS", "V"];
    Rank.STATS = ["STR", "DEX", "CON", "INT", "WIS", "CHA", "MAG"];
    Rank.STAT_NAMES = {
        STR: "Strength", DEX: "Dexterity", CON: "Constitution", INT: "Intellect",
        WIS: "Wisdom", CHA: "Charisma", MAG: "Mana"
    };
    Rank.STAT_HINTS = {
        STR: "Heavy weapons and techniques; heavy armor.",
        DEX: "Light weapons, AC and turn order.",
        CON: "Hit points; saves against poison and stuns.",
        INT: "Cheaper skills and faster mastery.",
        WIS: "Healing power; saves against sleep and charm.",
        CHA: "Rallying skills; better odds with states.",
        MAG: "MP pool and spell power."
    };
    // native param id <-> stat
    Rank.PARAM_OF = { STR: 2, CON: 3, MAG: 4, WIS: 5, DEX: 6, CHA: 7 };
    Rank.STAT_OF_PARAM = { 2: "STR", 3: "CON", 4: "MAG", 5: "WIS", 6: "DEX", 7: "CHA" };
    Rank.ROLES = ["minion", "standard", "elite", "boss", "apex"];

    Rank.TITLES = csv(P["Rank Titles"], "Common,Awakened,Adept,Veteran,Elite,Heroic,Calamity,Cataclysm,Mythic,Divine");
    Rank.COLORS = csv(P["Rank Colors"], "#a8a8a8,#8fd06a,#6ab0e8,#b58aff,#f3d34a,#ff9a4c,#ff5a52,#ff7ad0,#ffffff,#fff2b0");

    const parseMap = (s, conv) => {
        const out = {};
        for (const part of String(s).split(",")) {
            const m = part.match(/^\s*([^:]+?)\s*:\s*([^:]+?)\s*$/);
            if (m) out[m[1].toLowerCase()] = conv ? conv(m[2]) : m[2];
        }
        return out;
    };

    Rank.P = {
        startStat: num(P["Level 1 Stat"], 1),
        startPoints: num(P["Starting Points"], 20),
        pointsPerLevel: num(P["Points per Level"], 20),
        aptitudeValues: parseMap(text(P["Aptitude Values"], "S:1.5, A:1, B:0.75, C:0.5, D:0.25, E:0"), Number),
        defaultAptitude: text(P["Default Aptitude"], "STR C, DEX C, CON C, INT C, WIS C, CHA C, MAG C"),
        actorRankMode: text(P["Actor Rank Mode"], "pl"),
        hpFormula: text(P["Max HP Formula"], "10 + 2 * con + 5 * level"),
        mpFormula: text(P["Max MP Formula"], "mag * (0.8 + 0.5 * rank) + 2 * level + 8"),
        bodySlot: num(P["Body Slot"], 4),
        expCurve: text(P["EXP Curve"], "rank"),
        expAnchors: text(P["EXP Anchors"], "1:0, 13:1, 27:2, 40:3, 53:4, 67:5, 80:6, 93:7, 99:7.5"),
        expGapRates: csv(P["EXP Gap Rates"], "0, 0.5, 1, 1.5, 2").map(Number),
        masteryBars: csv(P["Mastery Bars"], "180, 360, 560, 800, 1100, 1450, 1900, 2500, 3300").map(Number),
        masteryPerUse: num(P["Mastery Per Use"], 10),
        masteryIntDivisor: num(P["Mastery INT Divisor"], 400),
        masteryKill: parseMap(text(P["Mastery Kill Bonus"], "minion:5, standard:10, elite:25, boss:75, apex:200"), Number),
        breakthrough: bool(P["Breakthrough"], true),
        masteryStatBonus: num(P["Mastery Stat Bonus"], 5),
        menuMastery: num(P["Menu Use Mastery"], 0),
        bodyCostRate: num(P["Body Cost Rate"], 0.5),
        intCostDivisor: num(P["INT Cost Divisor"], 2000),
        maxIntCut: num(P["Max INT Cut"], 0.5),
        levelUpText: text(P["Level Up Text"], "%1 gained %2 stat points!"),
        masteryRankUpText: text(P["Mastery Rank Up Text"], "%1's %2 reached rank %3!")
    };

    //-------------------------------------------------------------------------
    // Rank math
    //-------------------------------------------------------------------------
    Rank.clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    Rank.ofValue = v => Rank.clamp(Math.floor((Number(v) || 0) / 100), 0, 9);
    Rank.mod = v => Math.floor((Number(v) || 0) / 20);
    Rank.pow = v => Math.floor((Number(v) || 0) / 4);
    Rank.letter = i => Rank.LETTERS[Rank.clamp(Math.floor(Number(i) || 0), 0, 9)];
    Rank.title = i => Rank.TITLES[Rank.clamp(Math.floor(Number(i) || 0), 0, 9)] || "";
    Rank.color = i => Rank.COLORS[Rank.clamp(Math.floor(Number(i) || 0), 0, 9)] || "#ffffff";
    Rank.statIndex = name => Rank.STATS.indexOf(String(name || "").trim().toUpperCase());
    Rank.statCapFor = rank => Math.min(999, (Rank.clamp(rank, 0, 9) + 2) * 100 - 1);

    Rank.parseRank = function(s) {
        if (s === undefined || s === null) return null;
        const t = String(s).trim().toUpperCase().replace(/-?RANK$/, "").trim();
        if (/^\d+$/.test(t)) return Rank.clamp(Number(t), 0, 9);
        const i = Rank.LETTERS.indexOf(t);
        return i >= 0 ? i : null;
    };

    Rank.gapMult = g => (g >= 2 ? 2 : g === 1 ? 1.5 : g === 0 ? 1 : g === -1 ? 0.5 : g === -2 ? 0.25 : 0);
    Rank.gapLabel = g => (g >= 2 ? "×2" : g === 1 ? "×1.5" : g === 0 ? "×1" : g === -1 ? "×½" : g === -2 ? "×¼" : "WALL");
    Rank.expGapRate = g => {
        const r = Rank.P.expGapRates;
        const i = Rank.clamp(g, -2, 2) + 2;
        return r[i] !== undefined ? r[i] : 1;
    };
    Rank.masteryFactor = g => (g >= 1 ? 1.5 : g === 0 ? 1 : g === -1 ? 0.5 : 0);
    Rank.masteryNeed = r => (r >= 9 ? Infinity : Rank.P.masteryBars[r] || Infinity);

    // average of the three highest values
    Rank.powerLevel = values => {
        const v = values.slice().sort((a, b) => b - a);
        return Math.floor(((v[0] || 0) + (v[1] || 0) + (v[2] || 0)) / 3);
    };

    //-------------------------------------------------------------------------
    // Dice
    //-------------------------------------------------------------------------
    Rank.parseDice = function(s) {
        if (s === undefined || s === null) return null;
        const t = String(s).trim();
        let m = t.match(/^(\d*)\s*d\s*(\d+)\s*(?:([+-])\s*(\d+))?$/i);
        if (m) {
            const count = m[1] ? Number(m[1]) : 1;
            const bonus = m[3] ? (m[3] === "-" ? -1 : 1) * Number(m[4]) : 0;
            return { count: Math.max(1, count), sides: Math.max(1, Number(m[2])), bonus };
        }
        m = t.match(/^(\d+)$/);
        if (m) return { count: 1, sides: Math.max(1, Number(m[1])), bonus: 0 };
        return null;
    };
    Rank.dice = (count, sides, bonus) => ({ count: count || 1, sides: Math.max(1, sides || 1), bonus: bonus || 0 });
    Rank.rollDie = sides => 1 + Math.floor(Math.random() * Math.max(1, sides));
    Rank.rollDice = function(d) {
        let t = d.bonus || 0;
        for (let i = 0; i < d.count; i++) t += Rank.rollDie(d.sides);
        return t;
    };
    Rank.diceMin = d => d.count + (d.bonus || 0);
    Rank.diceMax = d => d.count * d.sides + (d.bonus || 0);
    Rank.diceAvg = d => (d.count * (d.sides + 1)) / 2 + (d.bonus || 0);
    Rank.diceText = d => (d.count > 1 ? d.count : "") + "d" + d.sides + (d.bonus > 0 ? "+" + d.bonus : d.bonus < 0 ? String(d.bonus) : "");
    Rank.d20 = () => Rank.rollDie(20);

    //-------------------------------------------------------------------------
    // Formulas
    //-------------------------------------------------------------------------
    const FORMULA_ARGS = ["a", "level", "rank", "str", "dex", "con", "int", "wis", "cha", "mag"];
    Rank.makeFormula = function(src, fallback) {
        try {
            return new Function(...FORMULA_ARGS, "return (" + src + ");");
        } catch (e) {
            console.error("Rank_Core: bad formula '" + src + "'", e);
            return new Function(...FORMULA_ARGS, "return (" + fallback + ");");
        }
    };
    Rank.hpFormula = Rank.makeFormula(Rank.P.hpFormula, "10 + 2 * con + 5 * level");
    Rank.mpFormula = Rank.makeFormula(Rank.P.mpFormula, "mag * (0.8 + 0.5 * rank) + 2 * level + 8");

    //-------------------------------------------------------------------------
    // EXP curve (Erdenkreis): a level costs more as the expected rank rises
    //-------------------------------------------------------------------------
    Rank.expAnchors = String(Rank.P.expAnchors).split(",").map(s => s.split(":").map(Number))
        .filter(a => a.length === 2 && !isNaN(a[0]) && !isNaN(a[1])).sort((a, b) => a[0] - b[0]);
    if (Rank.expAnchors.length < 2) Rank.expAnchors = [[1, 0], [99, 8]];
    Rank.expectedRank = function(level) {
        const A = Rank.expAnchors;
        if (level <= A[0][0]) return A[0][1];
        for (let i = 1; i < A.length; i++) {
            const [l1, r1] = A[i - 1];
            const [l2, r2] = A[i];
            if (level <= l2) return r1 + ((r2 - r1) * (level - l1)) / Math.max(1, l2 - l1);
        }
        return A[A.length - 1][1];
    };
    Rank.expToNext = function(level) {
        const er = Rank.expectedRank(level);
        const band = Math.floor(er);
        const frac = er - band;
        return Math.round((2.6 + 0.025 * level) * 20 * Math.pow(3.6, band + 0.5 * frac));
    };
    Rank._expTotals = [0, 0];
    for (let l = 2; l <= 150; l++) Rank._expTotals[l] = Rank._expTotals[l - 1] + Rank.expToNext(l - 1);
    Rank.expTotal = level => (level <= 1 ? 0 : Rank._expTotals[Math.min(level, 150)]);

    //-------------------------------------------------------------------------
    // Notetag parsing
    //-------------------------------------------------------------------------
    const RANK_ALT = "SSS|SS|S|F|E|D|C|B|A|V";
    const tagValue = (note, name) => {
        const m = note.match(new RegExp("<\\s*" + name + "\\s*:\\s*([^>]*)>", "i"));
        return m ? m[1].trim() : null;
    };
    const tagFlag = (note, name) => new RegExp("<\\s*" + name + "\\s*>", "i").test(note);
    const signedNum = s => {
        const m = String(s).match(/^\s*([+\-]?\d+(?:\.\d+)?)/);
        return m ? Number(m[1]) : null;
    };
    const pctNum = s => {
        const m = String(s).match(/^\s*([+\-]?\d+(?:\.\d+)?)\s*(%?)/);
        if (!m) return null;
        return m[2] ? Number(m[1]) / 100 : Number(m[1]);
    };

    Rank.parseStatList = function(textValue, allowPositional) {
        // "STR 90, DEX 160" or "STR: A" style pairs -> {idx: value}
        const out = {};
        const re = /(STR|DEX|CON|INT|WIS|CHA|MAG)\s*[:=]?\s*([+\-]?\d+(?:\.\d+)?|SSS|SS|[SABCDEF])\b/gi;
        let m;
        let any = false;
        while ((m = re.exec(textValue))) {
            out[Rank.statIndex(m[1])] = m[2];
            any = true;
        }
        if (!any && allowPositional) {
            const parts = String(textValue).split(/[\s,]+/).filter(x => x.length);
            parts.slice(0, 7).forEach((p, i) => (out[i] = p));
        }
        return out;
    };

    function parseStatBonuses(note, rk) {
        rk.statPlus = [0, 0, 0, 0, 0, 0, 0];
        rk.statRate = [1, 1, 1, 1, 1, 1, 1];
        const re = /<\s*(STR|DEX|CON|INT|WIS|CHA|MAG|ALL\s*STATS)\s*:\s*([+\-]?\d+(?:\.\d+)?)\s*(%?)\s*>/gi;
        let m;
        while ((m = re.exec(note))) {
            const which = m[1].toUpperCase().replace(/\s+/g, " ");
            const idxs = which.startsWith("ALL") ? [0, 1, 2, 3, 4, 5, 6] : [Rank.statIndex(which)];
            const v = Number(m[2]);
            for (const i of idxs) {
                if (i < 0) continue;
                if (m[3]) rk.statRate[i] *= 1 + v / 100;
                else rk.statPlus[i] += v;
            }
        }
    }

    function parseCommon(note, rk) {
        const hit = tagValue(note, "Hit");
        rk.hit = hit !== null ? signedNum(hit) || 0 : 0;
        const crit = tagValue(note, "Crit\\s*Range");
        rk.crit = crit !== null ? signedNum(crit) || 0 : 0;
        const ac = tagValue(note, "AC");
        rk.acText = ac;
        rk.ac = ac !== null ? signedNum(ac) || 0 : 0;
        const rank = tagValue(note, "Rank");
        rk.rank = rank !== null ? Rank.parseRank(rank) : null;
        const stat = tagValue(note, "Stat");
        rk.stat = stat !== null && Rank.statIndex(stat) >= 0 ? stat.toUpperCase() : null;
        const saves = tagValue(note, "Saves");
        rk.saves = saves !== null ? saves.split(/[\s,]+/).map(s => s.toUpperCase()).filter(s => Rank.statIndex(s) >= 0) : null;
    }

    function parseForms(note) {
        const forms = {};
        const re = new RegExp("<\\s*At\\s+Rank\\s+(" + RANK_ALT + ")\\s*>([\\s\\S]*?)<\\/\\s*At\\s+Rank\\s+\\1\\s*>", "gi");
        let m;
        while ((m = re.exec(note))) {
            const r = Rank.parseRank(m[1]);
            const f = {};
            for (const line of m[2].split(/[\n;]+/)) {
                const kv = line.match(/^\s*([a-z ]+?)\s*:\s*(.+?)\s*$/i);
                if (!kv) continue;
                const key = kv[1].toLowerCase().replace(/\s+/g, "");
                const val = kv[2];
                if (key === "die" || key === "dice") f.dice = Rank.parseDice(val);
                else if (key === "hits" || key === "repeats") f.hits = Math.max(1, Math.floor(Number(val) || 1));
                else if (key === "damage" || key === "rate") f.rate = pctNum(val);
                else if (key === "bonus") f.bonus = signedNum(val) || 0;
                else if (key === "hit") f.hit = signedNum(val) || 0;
                else if (key === "crit" || key === "critrange") f.crit = signedNum(val) || 0;
                else if (key === "state") {
                    const sm = val.match(/(\d+)(?:\s+(\d+(?:\.\d+)?)\s*%)?/);
                    if (sm) (f.states = f.states || []).push({ id: Number(sm[1]), chance: sm[2] ? Number(sm[2]) / 100 : 1 });
                }
            }
            forms[r] = f;
        }
        return forms;
    }

    Rank.parseSkill = function(skill) {
        const note = skill.note || "";
        const rk = {};
        parseCommon(note, rk);
        rk.dice = Rank.parseDice(tagValue(note, "Die") || tagValue(note, "Dice") || skill.damage.formula);
        rk.native = tagFlag(note, "Native\\s*Formula");
        rk.body = tagFlag(note, "Body");
        rk.fixedCost = tagFlag(note, "Fixed\\s*Cost");
        rk.mastery = tagFlag(note, "No\\s*Mastery") ? "off" : tagFlag(note, "Mastery") ? "on" : "auto";
        const sr = tagValue(note, "Start\\s*Rank");
        rk.startRank = sr !== null ? Rank.parseRank(sr) || 0 : 0;
        const mr = tagValue(note, "Max\\s*Rank");
        rk.maxRank = mr !== null ? Rank.parseRank(mr) : 9;
        if (rk.maxRank === null) rk.maxRank = 9;
        const save = tagValue(note, "Save");
        if (save) {
            const sm = save.match(/(STR|DEX|CON|INT|WIS|CHA|MAG)(?:\s+(negates|states|effects|half))?/i);
            if (sm) {
                const mode = (sm[2] || "half").toLowerCase();
                rk.save = { stat: sm[1].toUpperCase(), mode: mode === "effects" ? "states" : mode };
            }
        }
        const dcb = tagValue(note, "DC");
        rk.dcBonus = dcb !== null ? signedNum(dcb) || 0 : 0;
        const dmg = tagValue(note, "Damage");
        rk.rate = dmg !== null ? pctNum(dmg) : 1;
        const bonus = tagValue(note, "Bonus");
        rk.bonus = bonus !== null ? signedNum(bonus) || 0 : 0;
        const area = tagValue(note, "Area\\s*Rate");
        rk.areaRate = area !== null ? pctNum(area) : null;
        rk.rollMode = tagFlag(note, "No\\s*Attack\\s*Roll") ? "none" : tagFlag(note, "Attack\\s*Roll") ? "roll" : "auto";
        rk.support = tagFlag(note, "Support");
        rk.forms = parseForms(note);
        rk.evolve = null;
        const ev = note.match(new RegExp("<\\s*Evolve\\s+(" + RANK_ALT + ")\\s*:\\s*(\\d+)\\s*>", "i"));
        if (ev) rk.evolve = { rank: Rank.parseRank(ev[1]), id: Number(ev[2]) };
        rk.unlocks = [];
        const ure = new RegExp("<\\s*Unlock\\s+(" + RANK_ALT + ")\\s*:\\s*(\\d+)\\s*>", "gi");
        let um;
        while ((um = ure.exec(note))) rk.unlocks.push({ rank: Rank.parseRank(um[1]), id: Number(um[2]) });
        skill.rk = rk;
    };

    Rank.parseEquip = function(item, isWeapon) {
        const note = item.note || "";
        const rk = {};
        parseCommon(note, rk);
        parseStatBonuses(note, rk);
        rk.rank = rk.rank !== null ? rk.rank : 0;
        if (isWeapon) {
            rk.dice = Rank.parseDice(tagValue(note, "Die") || tagValue(note, "Dice")) || Rank.dice(1, Math.max(1, item.params[2] || 4), 0);
            rk.stat = rk.stat || null;
        } else {
            const armor = tagValue(note, "Armor");
            rk.armor = armor !== null ? signedNum(armor) || 0 : item.params[3] || 0;
            const atype = $dataSystem && $dataSystem.armorTypes ? String($dataSystem.armorTypes[item.atypeId] || "") : "";
            rk.heavy = tagFlag(note, "Heavy") || /heavy/i.test(atype);
        }
        item.rk = rk;
    };

    Rank.parseState = function(state) {
        const rk = {};
        parseCommon(state.note || "", rk);
        parseStatBonuses(state.note || "", rk);
        state.rk = rk;
    };

    Rank.parseAptitude = function(textValue) {
        const list = Rank.parseStatList(textValue, true);
        const out = [];
        for (let i = 0; i < 7; i++) {
            const g = String(list[i] !== undefined ? list[i] : "C").toUpperCase();
            const v = Rank.P.aptitudeValues[g.toLowerCase()];
            out.push(v !== undefined ? v : isNaN(Number(g)) ? 0.5 : Number(g));
        }
        return out;
    };

    Rank.parseClassOrActor = function(obj) {
        const note = obj.note || "";
        const rk = {};
        parseCommon(note, rk);
        parseStatBonuses(note, rk);
        const apt = tagValue(note, "Aptitude");
        rk.aptitude = apt !== null ? Rank.parseAptitude(apt) : null;
        const sp = tagValue(note, "Start\\s*Points");
        rk.startPoints = sp !== null ? signedNum(sp) : null;
        obj.rk = rk;
    };

    Rank.parseEnemy = function(enemy) {
        const note = enemy.note || "";
        const rk = {};
        parseCommon(note, rk);
        const role = tagValue(note, "Role");
        rk.role = role && Rank.ROLES.includes(role.toLowerCase()) ? role.toLowerCase() : "standard";
        const base = [];
        const st = tagValue(note, "Stats");
        const list = st !== null ? Rank.parseStatList(st, true) : {};
        // individual <STR: 90> (unsigned = base, signed = bonus)
        const re = /<\s*(STR|DEX|CON|INT|WIS|CHA|MAG)\s*:\s*([+\-]?)(\d+)\s*>/gi;
        const plus = [0, 0, 0, 0, 0, 0, 0];
        let m;
        while ((m = re.exec(note))) {
            const i = Rank.statIndex(m[1]);
            if (m[2]) plus[i] += (m[2] === "-" ? -1 : 1) * Number(m[3]);
            else list[i] = m[3];
        }
        // untagged stats come from the database boxes:
        // Attack = STR, Defense = CON, M.Attack = MAG, M.Defense = WIS, Agility = DEX, Luck = CHA,
        // INT = average of M.Attack and M.Defense
        const p = enemy.params || [];
        const native = [p[2], p[6], p[3], Math.round(((p[4] || 0) + (p[5] || 0)) / 2), p[5], p[7], p[4]];
        const fallback = rk.rank !== null ? rk.rank * 100 + 50 : 10;
        for (let i = 0; i < 7; i++) {
            let v = list[i] !== undefined ? Number(list[i]) : NaN;
            if (isNaN(v)) v = typeof native[i] === "number" ? native[i] : fallback;
            base.push(Rank.clamp(Math.round(v + plus[i]), 0, 999));
        }
        rk.stats = base;
        if (rk.rank === null) rk.rank = Rank.ofValue(Rank.powerLevel(base));
        rk.attackDice = Rank.parseDice(tagValue(note, "Attack\\s*Die") || tagValue(note, "Attack\\s*Dice")) || null;
        const as = tagValue(note, "Attack\\s*Stat");
        rk.attackStat = as !== null && Rank.statIndex(as) >= 0 ? as.toUpperCase() : "STR";
        const armor = tagValue(note, "Armor");
        rk.armor = armor !== null ? signedNum(armor) : null;
        // <AC: 18> sets AC, <AC: +2> adds to it
        rk.acFixed = null;
        rk.acBonus = 0;
        if (rk.acText !== null) {
            if (/^\s*[+\-]/.test(rk.acText)) rk.acBonus = signedNum(rk.acText) || 0;
            else rk.acFixed = signedNum(rk.acText);
        }
        rk.ac = 0;
        enemy.rk = rk;
    };

    Rank.parseDatabase = function() {
        for (const s of $dataSkills) if (s) Rank.parseSkill(s);
        for (const w of $dataWeapons) if (w) Rank.parseEquip(w, true);
        for (const a of $dataArmors) if (a) Rank.parseEquip(a, false);
        for (const s of $dataStates) if (s) Rank.parseState(s);
        for (const c of $dataClasses) if (c) Rank.parseClassOrActor(c);
        for (const a of $dataActors) if (a) Rank.parseClassOrActor(a);
        for (const e of $dataEnemies) if (e) Rank.parseEnemy(e);
        for (const i of $dataItems) if (i) {
            const rk = {};
            parseCommon(i.note || "", rk);
            i.rk = rk;
        }
    };

    Rank._dbParsed = false;
    const _DataManager_isDatabaseLoaded = DataManager.isDatabaseLoaded;
    DataManager.isDatabaseLoaded = function() {
        if (!_DataManager_isDatabaseLoaded.call(this)) return false;
        if (!Rank._dbParsed) {
            Rank.parseDatabase();
            Rank._dbParsed = true;
        }
        return true;
    };
    // (re)parse after a battle test or a reload of the database
    const _DataManager_loadDatabase = DataManager.loadDatabase;
    DataManager.loadDatabase = function() {
        Rank._dbParsed = false;
        _DataManager_loadDatabase.call(this);
    };

    Rank.skillRk = skill => (skill ? skill.rk || (Rank.parseSkill(skill), skill.rk) : null);

    // Skills that grow with use: cost MP (or <Mastery>), not attack/guard, not <No Mastery>
    Rank.isMasterySkill = function(skill) {
        if (!skill || !DataManager.isSkill(skill)) return false;
        const rk = Rank.skillRk(skill);
        if (rk.mastery === "off") return false;
        if (skill.id === 1 || skill.id === 2) return rk.mastery === "on";
        if (rk.mastery === "on") return true;
        return skill.mpCost > 0;
    };

    // The stat a skill scales with
    Rank.skillStat = function(skill, battler) {
        const rk = Rank.skillRk(skill);
        if (rk && rk.stat) return rk.stat;
        if (battler && skill.id === battler.attackSkillId()) return battler.rkAttackStat();
        if ([3, 4].includes(skill.damage.type)) return "WIS";
        if (skill.hitType === 1) return "STR";
        return "MAG";
    };

    //-------------------------------------------------------------------------
    // Game_BattlerBase: stats, rank, AC
    //-------------------------------------------------------------------------
    const statProps = {};
    Rank.STATS.forEach((name, i) => {
        statProps[name.toLowerCase()] = {
            get: function() {
                return this.rkStat(i);
            },
            configurable: true
        };
    });
    Object.defineProperties(Game_BattlerBase.prototype, statProps);

    Game_BattlerBase.prototype.rkBaseStat = function(/*i*/) {
        return 0;
    };

    // objects whose notetag bonuses apply (states, and for actors: equips, class, actor)
    Game_BattlerBase.prototype.rkBonusObjects = function() {
        return this.states();
    };

    Game_BattlerBase.prototype.rkStatPlus = function(i) {
        let v = 0;
        for (const obj of this.rkBonusObjects()) {
            if (obj && obj.rk && obj.rk.statPlus) v += obj.rk.statPlus[i];
        }
        const p = Rank.PARAM_OF[Rank.STATS[i]];
        if (p !== undefined && this._paramPlus) v += this._paramPlus[p] || 0;
        return v;
    };

    Game_BattlerBase.prototype.rkStatRate = function(i) {
        let r = 1;
        for (const obj of this.rkBonusObjects()) {
            if (obj && obj.rk && obj.rk.statRate) r *= obj.rk.statRate[i];
        }
        const p = Rank.PARAM_OF[Rank.STATS[i]];
        if (p !== undefined) r *= this.paramRate(p) * this.paramBuffRate(p);
        return r;
    };

    Game_BattlerBase.prototype.rkStat = function(i) {
        if (typeof i === "string") i = Rank.statIndex(i);
        if (i < 0) return 0;
        const v = (this.rkBaseStat(i) + this.rkStatPlus(i)) * this.rkStatRate(i);
        return Rank.clamp(Math.round(v), 0, 999);
    };

    Game_BattlerBase.prototype.rkStats = function() {
        return Rank.STATS.map((s, i) => this.rkStat(i));
    };

    Game_BattlerBase.prototype.rkBaseStats = function() {
        return Rank.STATS.map((s, i) => this.rkBaseStat(i));
    };

    Game_BattlerBase.prototype.rkMod = function(stat) {
        return Rank.mod(this.rkStat(stat));
    };

    Game_BattlerBase.prototype.rkPow = function(stat) {
        return Rank.pow(this.rkStat(stat));
    };

    Game_BattlerBase.prototype.rkStatRank = function(stat) {
        return Rank.ofValue(this.rkStat(stat));
    };

    Game_BattlerBase.prototype.rkPowerLevel = function(baseOnly) {
        return Rank.powerLevel(baseOnly ? this.rkBaseStats() : this.rkStats());
    };

    Game_BattlerBase.prototype.rkRank = function() {
        return Rank.ofValue(this.rkPowerLevel(false));
    };

    Game_BattlerBase.prototype.rkRole = function() {
        return "standard";
    };

    Game_BattlerBase.prototype.rkTraitSum = function(key) {
        let v = 0;
        for (const obj of this.rkBonusObjects()) {
            if (obj && obj.rk && typeof obj.rk[key] === "number") v += obj.rk[key];
        }
        return v;
    };

    Game_BattlerBase.prototype.rkHitBonus = function() {
        return this.rkTraitSum("hit");
    };

    Game_BattlerBase.prototype.rkCritBonus = function() {
        return this.rkTraitSum("crit");
    };

    Game_BattlerBase.prototype.rkAC = function() {
        return 10 + this.rkMod("DEX") + this.rkTraitSum("ac");
    };

    Game_BattlerBase.prototype.rkIsTrainedSave = function(/*stat*/) {
        return false;
    };

    Game_BattlerBase.prototype.rkAttackStat = function() {
        return "STR";
    };

    Game_BattlerBase.prototype.rkAttackDice = function() {
        return Rank.dice(1, 4, 0);
    };

    Game_BattlerBase.prototype.rkAttackRank = function() {
        return this.rkRank();
    };

    Game_BattlerBase.prototype.rkSkillRank = function(skill) {
        const rk = Rank.skillRk(skill);
        return Math.min(this.rkRank(), rk ? rk.maxRank : 9);
    };

    // The form (per-rank overrides) a skill has at its working rank
    Game_BattlerBase.prototype.rkSkillForm = function(skill) {
        const rk = Rank.skillRk(skill);
        const r = this.rkSkillRank(skill);
        const form = { dice: rk.dice, hits: 1, rate: 1, bonus: 0, hit: 0, crit: 0, states: [] };
        for (let i = 0; i <= r; i++) {
            const f = rk.forms[i];
            if (!f) continue;
            if (f.dice) form.dice = f.dice;
            if (f.hits) form.hits = f.hits;
            if (f.rate !== undefined && f.rate !== null) form.rate = f.rate;
            if (f.bonus) form.bonus = f.bonus;
            if (f.hit) form.hit = f.hit;
            if (f.crit) form.crit = f.crit;
            if (f.states) form.states = form.states.concat(f.states);
        }
        return form;
    };

    // Native params mirror the stats; actors compute HP/MP from formulas
    const _Game_BattlerBase_param = Game_BattlerBase.prototype.param;
    Game_BattlerBase.prototype.param = function(paramId) {
        const stat = Rank.STAT_OF_PARAM[paramId];
        if (stat) return this.rkStat(stat);
        if ((paramId === 0 || paramId === 1) && this.isActor()) return this.rkActorPool(paramId);
        return _Game_BattlerBase_param.call(this, paramId);
    };

    // MP cost scales with the skill's working rank; INT cuts it
    const _Game_BattlerBase_skillMpCost = Game_BattlerBase.prototype.skillMpCost;
    Game_BattlerBase.prototype.skillMpCost = function(skill) {
        const rk = Rank.skillRk(skill);
        if (!rk || rk.fixedCost || skill.mpCost <= 0) return _Game_BattlerBase_skillMpCost.call(this, skill);
        return Rank.mpCostFor(this, skill, this.rkSkillRank(skill));
    };

    Rank.mpCostFor = function(battler, skill, rank) {
        const rk = Rank.skillRk(skill);
        let cost = skill.mpCost * (rank + 1) * (rank + 1);
        if (rk.body) cost = Math.floor(cost * Rank.P.bodyCostRate);
        const cut = Math.min(Rank.P.maxIntCut, battler.rkStat("INT") / Math.max(1, Rank.P.intCostDivisor));
        cost = Math.max(1, Math.round(cost * (1 - cut)));
        return Math.floor(cost * battler.mcr);
    };

    //-------------------------------------------------------------------------
    // Game_Actor
    //-------------------------------------------------------------------------
    Game_Actor.prototype.rkArr = function(key) {
        if (!Array.isArray(this[key]) || this[key].length !== 7) this[key] = [0, 0, 0, 0, 0, 0, 0];
        return this[key];
    };

    Game_Actor.prototype.rkInit = function() {
        this._rkAlloc = [0, 0, 0, 0, 0, 0, 0];
        this._rkBonus = [0, 0, 0, 0, 0, 0, 0];
        if (!this._rkMastery) this._rkMastery = {};
        const a = this.actor().rk || {};
        const start = a.startPoints !== null && a.startPoints !== undefined ? a.startPoints : Rank.P.startPoints;
        this._rkPoints = start + Rank.P.pointsPerLevel * Math.max(0, this._level - 1);
        for (const id of this._skills) this.rkMasteryData(id);
    };

    const _Game_Actor_setup = Game_Actor.prototype.setup;
    Game_Actor.prototype.setup = function(actorId) {
        this._rkMastery = {};
        _Game_Actor_setup.call(this, actorId);
        this.rkInit();
        this.recoverAll();
    };

    Game_Actor.prototype.rkAptitude = function() {
        const a = this.actor().rk;
        if (a && a.aptitude) return a.aptitude;
        const c = this.currentClass().rk;
        if (c && c.aptitude) return c.aptitude;
        if (!Rank._defaultAptitude) Rank._defaultAptitude = Rank.parseAptitude(Rank.P.defaultAptitude);
        return Rank._defaultAptitude;
    };

    Game_Actor.prototype.rkNatural = function(i) {
        return Math.floor(this.rkAptitude()[i] * Math.max(0, this._level - 1));
    };

    Game_Actor.prototype.rkBaseStat = function(i) {
        const v = Rank.P.startStat + this.rkNatural(i) + this.rkArr("_rkAlloc")[i] + this.rkArr("_rkBonus")[i];
        return Rank.clamp(v, 0, 999);
    };

    Game_Actor.prototype.rkBonusObjects = function() {
        return this.traitObjects();
    };

    Game_Actor.prototype.rkRank = function() {
        const a = this.actor().rk;
        if (a && a.rank !== null && a.rank !== undefined) return a.rank;
        if (Rank.P.actorRankMode === "level") return Rank.clamp(Math.floor((this._level - 1) / 10), 0, 9);
        return Rank.ofValue(this.rkPowerLevel(true));
    };

    Game_Actor.prototype.rkStatCap = function(/*i*/) {
        return Rank.statCapFor(this.rkRank());
    };

    Game_Actor.prototype.rkActorPool = function(paramId) {
        const s = this.rkStats();
        const fn = paramId === 0 ? Rank.hpFormula : Rank.mpFormula;
        let base = 0;
        try {
            base = Number(fn(this, this._level, this.rkRank(), s[0], s[1], s[2], s[3], s[4], s[5], s[6])) || 0;
        } catch (e) {
            console.error("Rank_Core: HP/MP formula error", e);
        }
        const value = (Math.floor(base) + this.paramPlus(paramId)) * this.paramRate(paramId) * this.paramBuffRate(paramId);
        const min = paramId === 0 ? 1 : 0;
        return Math.round(Rank.clamp(value, min, this.paramMax(paramId)));
    };

    // native base/plus for params 2-7 now report the stats (other code reads them)
    const _Game_Actor_paramBase = Game_Actor.prototype.paramBase;
    Game_Actor.prototype.paramBase = function(paramId) {
        const stat = Rank.STAT_OF_PARAM[paramId];
        if (stat) return this.rkBaseStat(Rank.statIndex(stat));
        return _Game_Actor_paramBase.call(this, paramId);
    };

    const _Game_Actor_paramPlus = Game_Actor.prototype.paramPlus;
    Game_Actor.prototype.paramPlus = function(paramId) {
        // equipment Attack/Defense boxes are the die and the armor value, not stats
        if (Rank.STAT_OF_PARAM[paramId]) return Game_Battler.prototype.paramPlus.call(this, paramId);
        return _Game_Actor_paramPlus.call(this, paramId);
    };

    Game_Actor.prototype.rkIsTrainedSave = function(stat) {
        const a = this.actor().rk;
        if (a && a.saves) return a.saves.includes(stat);
        const c = this.currentClass().rk;
        return !!(c && c.saves && c.saves.includes(stat));
    };

    Game_Actor.prototype.rkMainWeapon = function() {
        return this.weapons()[0] || null;
    };

    Game_Actor.prototype.rkAttackStat = function() {
        const w = this.rkMainWeapon();
        if (w && w.rk && w.rk.stat) return w.rk.stat;
        return "STR";
    };

    Game_Actor.prototype.rkAttackDice = function() {
        const w = this.rkMainWeapon();
        if (w && w.rk && w.rk.dice) return w.rk.dice;
        return Rank.dice(1, Rank.unarmedDie ? Rank.unarmedDie() : 4, 0);
    };

    Game_Actor.prototype.rkWeaponRank = function() {
        const w = this.rkMainWeapon();
        return w && w.rk ? w.rk.rank || 0 : 0;
    };

    Game_Actor.prototype.rkAC = function() {
        let body = 0;
        let extra = 0;
        let penalty = 0;
        const strRank = this.rkStatRank("STR");
        for (const item of this.armors()) {
            const rk = item.rk || {};
            const value = typeof rk.armor === "number" ? rk.armor : item.params[3] || 0;
            if (item.etypeId === Rank.P.bodySlot) body = Math.max(body, value);
            else extra += value;
            if (rk.heavy && (rk.rank || 0) > strRank) penalty = 2;
        }
        return 10 + Math.max(this.rkMod("DEX"), body) + extra + this.rkTraitSum("ac") - penalty;
    };

    Game_Actor.prototype.rkHeavyPenalty = function() {
        const strRank = this.rkStatRank("STR");
        return this.armors().some(item => item.rk && item.rk.heavy && (item.rk.rank || 0) > strRank);
    };

    // --- stat points -------------------------------------------------------
    Game_Actor.prototype.rkPoints = function() {
        return Math.max(0, this._rkPoints || 0);
    };

    Game_Actor.prototype.rkGainPoints = function(n) {
        this._rkPoints = Math.max(0, (this._rkPoints || 0) + n);
    };

    Game_Actor.prototype.rkAllocated = function(i) {
        return this.rkArr("_rkAlloc")[i];
    };

    Game_Actor.prototype.rkRoomFor = function(i) {
        return Math.max(0, this.rkStatCap(i) - this.rkBaseStat(i));
    };

    Game_Actor.prototype.rkAllocate = function(i, n) {
        n = Math.floor(n);
        if (n > 0) n = Math.min(n, this.rkPoints(), this.rkRoomFor(i));
        else n = -Math.min(-n, this.rkAllocated(i));
        if (n === 0) return 0;
        const hpRate = this.mhp > 0 ? this.hp / this.mhp : 1;
        const mpRate = this.mmp > 0 ? this.mp / this.mmp : 1;
        const wasFull = this.hp >= this.mhp;
        this.rkArr("_rkAlloc")[i] += n;
        this._rkPoints -= n;
        // gaining max HP/MP keeps the gap, losing keeps the ratio
        this.refresh();
        if (n > 0 && wasFull) this.setHp(this.mhp);
        else if (n < 0) this.setHp(Math.max(1, Math.round(this.mhp * hpRate)));
        if (n < 0) this.setMp(Math.round(this.mmp * mpRate));
        return n;
    };

    Game_Actor.prototype.rkRefundPoints = function() {
        const alloc = this.rkArr("_rkAlloc");
        let total = 0;
        for (let i = 0; i < 7; i++) {
            total += alloc[i];
            alloc[i] = 0;
        }
        this._rkPoints = (this._rkPoints || 0) + total;
        this.refresh();
        return total;
    };

    const _Game_Actor_levelUp = Game_Actor.prototype.levelUp;
    Game_Actor.prototype.levelUp = function() {
        _Game_Actor_levelUp.call(this);
        this._rkPoints = (this._rkPoints || 0) + Rank.P.pointsPerLevel;
        this._rkLevelGainPending = (this._rkLevelGainPending || 0) + Rank.P.pointsPerLevel;
    };

    const _Game_Actor_changeExp = Game_Actor.prototype.changeExp;
    Game_Actor.prototype.changeExp = function(exp, show) {
        this._rkLevelGainPending = 0;
        const hpGap = this.mhp - this.hp;
        const mpGap = this.mmp - this.mp;
        _Game_Actor_changeExp.call(this, exp, show);
        // a level up grows max HP/MP; current values grow with them
        if (this.isAlive()) {
            this.setHp(Math.max(1, this.mhp - hpGap));
            this.setMp(Math.max(0, this.mmp - mpGap));
        }
        this._rkLevelGainPending = 0;
    };

    const _Game_Actor_displayLevelUp = Game_Actor.prototype.displayLevelUp;
    Game_Actor.prototype.displayLevelUp = function(newSkills) {
        _Game_Actor_displayLevelUp.call(this, newSkills);
        if (this._rkLevelGainPending > 0) {
            $gameMessage.add(Rank.P.levelUpText.format(this.name(), this._rkLevelGainPending));
        }
    };

    Game_Actor.prototype.expForLevel = (function(orig) {
        return function(level) {
            if (Rank.P.expCurve === "database") return orig.call(this, level);
            return Rank.expTotal(level);
        };
    })(Game_Actor.prototype.expForLevel);

    // --- skill mastery ------------------------------------------------------
    Game_Actor.prototype.rkMasteryTable = function() {
        if (!this._rkMastery) this._rkMastery = {};
        return this._rkMastery;
    };

    Game_Actor.prototype.rkMasteryData = function(skillId) {
        const table = this.rkMasteryTable();
        if (!table[skillId]) {
            const skill = $dataSkills[skillId];
            const rk = Rank.skillRk(skill);
            table[skillId] = { r: rk ? Math.min(rk.startRank || 0, rk.maxRank) : 0, x: 0 };
        }
        return table[skillId];
    };

    Game_Actor.prototype.rkMasteryRank = function(skillId) {
        return this.rkMasteryData(skillId).r;
    };

    Game_Actor.prototype.rkMasteryExp = function(skillId) {
        return this.rkMasteryData(skillId).x;
    };

    Game_Actor.prototype.rkMasteryCap = function(skillId) {
        const rk = Rank.skillRk($dataSkills[skillId]);
        return rk ? rk.maxRank : 9;
    };

    Game_Actor.prototype.rkMasteryNeed = function(skillId) {
        const d = this.rkMasteryData(skillId);
        if (d.r >= this.rkMasteryCap(skillId)) return Infinity;
        return Rank.masteryNeed(d.r);
    };

    Game_Actor.prototype.rkIsBarFull = function(skillId) {
        const need = this.rkMasteryNeed(skillId);
        return need !== Infinity && this.rkMasteryExp(skillId) >= need;
    };

    Game_Actor.prototype.rkSkillRank = function(skill) {
        if (!skill) return 0;
        // the plain attack works at its weapon's rank (the grade bonus comes from the weapon)
        if (skill.id === this.attackSkillId() || skill.id === this.guardSkillId()) {
            return this.rkWeaponRank();
        }
        const rk = Rank.skillRk(skill);
        const statRank = this.rkStatRank(Rank.skillStat(skill, this));
        if (!Rank.isMasterySkill(skill)) return Math.min(this.rkRank(), statRank, rk.maxRank);
        return Math.min(this.rkMasteryRank(skill.id), statRank, rk.maxRank);
    };

    // Adds mastery; returns the amount that stuck
    Game_Actor.prototype.rkGainMastery = function(skillId, amount, messages) {
        const skill = $dataSkills[skillId];
        if (!skill || amount <= 0) return 0;
        const d = this.rkMasteryData(skillId);
        const need = this.rkMasteryNeed(skillId);
        if (need === Infinity) return 0;
        const before = d.x;
        d.x = Math.min(need, d.x + amount);
        const gained = d.x - before;
        if (!Rank.P.breakthrough) {
            while (this.rkIsBarFull(skillId)) {
                const id = this.rkRankUpSkill(skillId, messages);
                if (id !== skillId) break;
            }
        }
        return gained;
    };

    // Rank up a skill; returns the (possibly evolved) skill id
    Game_Actor.prototype.rkRankUpSkill = function(skillId, messages) {
        const skill = $dataSkills[skillId];
        const d = this.rkMasteryData(skillId);
        if (d.r >= this.rkMasteryCap(skillId)) return skillId;
        d.r += 1;
        d.x = 0;
        const statIdx = Rank.statIndex(Rank.skillStat(skill, this));
        if (statIdx >= 0 && Rank.P.masteryStatBonus) {
            this.rkArr("_rkBonus")[statIdx] += Rank.P.masteryStatBonus;
        }
        if (messages) messages.push(Rank.P.masteryRankUpText.format(this.name(), skill.name, Rank.letter(d.r), Rank.title(d.r)));
        const rk = Rank.skillRk(skill);
        for (const u of rk.unlocks) {
            if (u.rank <= d.r && $dataSkills[u.id] && !this.isLearnedSkill(u.id)) {
                this.learnSkill(u.id);
                if (messages) messages.push(TextManager.obtainSkill.format($dataSkills[u.id].name));
            }
        }
        let result = skillId;
        if (rk.evolve && rk.evolve.rank <= d.r && $dataSkills[rk.evolve.id]) {
            const newId = rk.evolve.id;
            const table = this.rkMasteryTable();
            const carried = { r: d.r, x: d.x };
            const existing = table[newId];
            table[newId] = existing && existing.r > carried.r ? existing : carried;
            if (this.isLearnedSkill(skillId)) this.forgetSkill(skillId);
            this.learnSkill(newId);
            if (messages) messages.push(Rank.evolveText(this, skill, $dataSkills[newId]));
            result = newId;
        }
        this.refresh();
        return result;
    };

    Rank.evolveText = (actor, from, to) => from.name + " became " + to.name + "!";

    const _Game_Actor_learnSkill = Game_Actor.prototype.learnSkill;
    Game_Actor.prototype.learnSkill = function(skillId) {
        _Game_Actor_learnSkill.call(this, skillId);
        if ($dataSkills[skillId]) this.rkMasteryData(skillId);
    };

    Game_Actor.prototype.rkSetMastery = function(skillId, rank, exp) {
        const d = this.rkMasteryData(skillId);
        d.r = Rank.clamp(rank, 0, this.rkMasteryCap(skillId));
        const need = this.rkMasteryNeed(skillId);
        d.x = Math.max(0, Math.min(need === Infinity ? 0 : need, exp || 0));
        this.refresh();
    };

    Game_Actor.prototype.rkMasterySkills = function() {
        return this.skills().filter(s => Rank.isMasterySkill(s));
    };

    //-------------------------------------------------------------------------
    // Game_Enemy
    //-------------------------------------------------------------------------
    Game_Enemy.prototype.rkData = function() {
        const e = this.enemy();
        if (!e.rk) Rank.parseEnemy(e);
        return e.rk;
    };

    Game_Enemy.prototype.rkBaseStat = function(i) {
        return this.rkData().stats[i];
    };

    Game_Enemy.prototype.rkRank = function() {
        return this.rkData().rank;
    };

    Game_Enemy.prototype.rkRole = function() {
        return this.rkData().role;
    };

    Game_Enemy.prototype.rkAttackStat = function() {
        return this.rkData().attackStat;
    };

    Game_Enemy.prototype.rkAttackDice = function() {
        return this.rkData().attackDice || Rank.dice(1, Rank.enemyAttackDie ? Rank.enemyAttackDie() : 6, 0);
    };

    Game_Enemy.prototype.rkAC = function() {
        const rk = this.rkData();
        let ac;
        if (rk.acFixed !== null && rk.acFixed !== undefined) ac = rk.acFixed;
        else {
            const armor = rk.armor !== null && rk.armor !== undefined ? rk.armor : 5 * rk.rank + 2;
            ac = 10 + Math.max(this.rkMod("DEX"), armor);
        }
        return ac + rk.acBonus + this.rkTraitSum("ac");
    };

    Game_Enemy.prototype.rkHitBonus = function() {
        return this.rkData().hit + Game_BattlerBase.prototype.rkHitBonus.call(this);
    };

    Game_Enemy.prototype.rkCritBonus = function() {
        return this.rkData().crit + Game_BattlerBase.prototype.rkCritBonus.call(this);
    };

    Game_Enemy.prototype.rkIsTrainedSave = function(stat) {
        const rk = this.rkData();
        if (rk.saves) return rk.saves.includes(stat);
        return ["elite", "boss", "apex"].includes(rk.role);
    };

    Game_Enemy.prototype.rkSkillRank = function(skill) {
        const rk = Rank.skillRk(skill);
        return Math.min(this.rkRank(), rk ? rk.maxRank : 9);
    };

    // enemies' native base params also mirror their stats
    const _Game_Enemy_paramBase = Game_Enemy.prototype.paramBase;
    Game_Enemy.prototype.paramBase = function(paramId) {
        const stat = Rank.STAT_OF_PARAM[paramId];
        if (stat) return this.rkBaseStat(Rank.statIndex(stat));
        return _Game_Enemy_paramBase.call(this, paramId);
    };

    //-------------------------------------------------------------------------
    // Rank badges and text codes
    //-------------------------------------------------------------------------
    Window_Base.prototype.rkBadgeWidth = function(rank, height) {
        const h = height || this.rkBadgeHeight();
        const saveSize = this.contents.fontSize;
        this.contents.fontSize = Math.max(12, Math.floor(h * 0.72));
        const w = Math.max(h, this.textWidth(Rank.letter(rank)) + 10);
        this.contents.fontSize = saveSize;
        return w;
    };

    Window_Base.prototype.rkBadgeHeight = function() {
        return Math.max(16, this.lineHeight() - 12);
    };

    Window_Base.prototype.rkDrawRankBadge = function(rank, x, y, height, dim) {
        const bmp = this.contents;
        const h = height || this.rkBadgeHeight();
        const w = this.rkBadgeWidth(rank, h);
        const col = Rank.color(rank);
        const saveSize = bmp.fontSize;
        const saveColor = bmp.textColor;
        const saveOutline = bmp.outlineWidth;
        const saveOutlineColor = bmp.outlineColor;
        bmp.paintOpacity = dim ? 120 : 255;
        bmp.fillRect(x, y, w, h, "rgba(0,0,0,0.6)");
        bmp.fillRect(x + 1, y + 1, w - 2, h - 2, col);
        bmp.fontSize = Math.max(12, Math.floor(h * 0.72));
        bmp.textColor = "#16161c";
        bmp.outlineWidth = 0;
        bmp.drawText(Rank.letter(rank), x, y, w, h, "center");
        bmp.fontSize = saveSize;
        bmp.textColor = saveColor;
        bmp.outlineWidth = saveOutline;
        bmp.outlineColor = saveOutlineColor;
        bmp.paintOpacity = 255;
        return w;
    };

    const _Window_Base_processEscapeCharacter = Window_Base.prototype.processEscapeCharacter;
    Window_Base.prototype.processEscapeCharacter = function(code, textState) {
        if (code === "RK" || code === "RKA") {
            const n = this.obtainEscapeParam(textState);
            let rank = Number(n) || 0;
            if (code === "RKA") {
                const actor = $gameActors.actor(Number(n) || 0);
                rank = actor ? actor.rkRank() : 0;
            }
            const h = Math.min(this.rkBadgeHeight(), textState.height - 8);
            const w = this.rkBadgeWidth(rank, h);
            if (textState.drawing) {
                this.rkDrawRankBadge(rank, textState.x + 2, textState.y + Math.floor((textState.height - h) / 2), h);
            }
            textState.x += w + 4;
            return;
        }
        _Window_Base_processEscapeCharacter.call(this, code, textState);
    };

    //-------------------------------------------------------------------------
    // Plugin commands
    //-------------------------------------------------------------------------
    const actorsFor = id => {
        id = Number(id) || 0;
        if (id > 0) return $gameActors.actor(id) ? [$gameActors.actor(id)] : [];
        return $gameParty.members();
    };

    PluginManager.registerCommand(PLUGIN, "GainStatPoints", args => {
        for (const a of actorsFor(args.actorId)) a.rkGainPoints(Number(args.amount) || 0);
    });

    PluginManager.registerCommand(PLUGIN, "RefundStatPoints", args => {
        for (const a of actorsFor(args.actorId)) a.rkRefundPoints();
    });

    PluginManager.registerCommand(PLUGIN, "SetMastery", args => {
        const a = $gameActors.actor(Number(args.actorId));
        const r = Rank.parseRank(args.rank);
        if (a && $dataSkills[Number(args.skillId)]) a.rkSetMastery(Number(args.skillId), r === null ? 0 : r, Number(args.exp) || 0);
    });

    PluginManager.registerCommand(PLUGIN, "GainMastery", args => {
        const messages = [];
        for (const a of actorsFor(args.actorId)) {
            const id = Number(args.skillId) || 0;
            const skills = id > 0 ? [$dataSkills[id]].filter(s => s && a.hasSkill(s.id)) : a.rkMasterySkills();
            for (const s of skills) a.rkGainMastery(s.id, Number(args.amount) || 0, messages);
        }
        Rank.showMessages(messages);
    });

    PluginManager.registerCommand(PLUGIN, "CompleteBreakthrough", args => {
        const messages = [];
        for (const a of actorsFor(args.actorId)) {
            const id = Number(args.skillId) || 0;
            const skills = id > 0 ? [$dataSkills[id]].filter(Boolean) : a.rkMasterySkills();
            for (const s of skills) if (a.rkIsBarFull(s.id)) a.rkRankUpSkill(s.id, messages);
        }
        Rank.showMessages(messages);
    });

    Rank.showMessages = function(messages) {
        if (!messages || messages.length === 0) return;
        for (const m of messages) $gameMessage.add(m);
    };
})();
