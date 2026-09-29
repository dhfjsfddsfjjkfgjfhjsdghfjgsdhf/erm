//=============================================================================
// Rank_Battle.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [v1.0] Rank combat: d20 vs AC, die + POW + grade bonus, rank GAP, saves, mastery gain.
 * @author Ten & Claude
 * @base Rank_Core
 * @orderAfter Rank_Core
 *
 * @help Rank_Battle.js
 *
 * Classic turn-based battle on the Erdenkreis rank rules. Set the battle
 * system to "Turn-based" in the database (System 2).
 *
 * HIT     d20 + MOD(stat) + Attack Bonus + hit bonuses  vs  AC
 *         natural 1 misses, natural 20 hits. Crits on a natural 20 (every
 *         5% Critical Rate trait and every <Crit Range: +1> widens it by one
 *         face) and deal x1.5.
 *         Heals, buffs, Certain Hit skills and area skills don't roll.
 * DAMAGE  die + POW(stat) + 10 x rank  x GAP x modifiers
 *         GAP = attack rank - target rank:
 *           +2 or more x2, +1 x1.5, 0 x1, -1 x1/2, -2 x1/4, -3 or less WALL
 *         (a WALL deals nothing and lands no states).
 *         Attack rank = the higher of the user's rank and the weapon/skill
 *         rank, never more than 2 above the user.
 *         Weakness (element rate above 100%) counts the gap one better.
 *         Element rate below 100% scales the damage down; 0% = immune.
 *         Multi-target skills deal the Multi-Target Rate (x1/2).
 * SAVES   <Save: STAT>: d20 + MOD(stat) (+3 trained) vs 13 + MOD(skill stat)
 *         (enemy DCs against actors use the Enemy DC Base, 10).
 *         Two ranks above the source: advantage. Two below: disadvantage.
 * ROLES   minion: half damage. elite: attacks twice. boss: one extra action.
 *         apex: both. Boss/apex shrug off every second disabling state and
 *         disabling states last them 1 turn.
 * TURNS   initiative d20 + MOD(DEX) every round.
 * ESCAPE  45% + (party DEX - foe DEX) / 300, +15% per failed try.
 * EXP     each actor gets enemy EXP x rank-gap rate (foes two ranks below
 *         teach nothing).
 * MASTERY gained after every use of an MP skill, shown after the battle,
 *         breakthroughs happen on victory.
 *
 * The target window shows the hit chance, save chance, damage range and GAP
 * for the action being chosen.
 *
 * @param Attack Bonus
 * @desc Flat bonus on every attack roll.
 * @type number
 * @min -99
 * @default 8
 *
 * @param Unarmed Die
 * @type number
 * @min 1
 * @default 4
 *
 * @param Enemy Attack Die
 * @desc Die for enemies without <Attack Die>.
 * @type number
 * @min 1
 * @default 6
 *
 * @param Default Skill Die
 * @desc Die for skills whose Formula box isn't a die.
 * @type number
 * @min 1
 * @default 6
 *
 * @param Crit Multiplier
 * @type number
 * @decimals 2
 * @default 1.5
 *
 * @param Multi-Target Rate
 * @desc Damage/healing rate for skills that hit all targets or several random ones.
 * @type number
 * @decimals 2
 * @default 0.5
 *
 * @param Area Attack Roll
 * @text Area skills roll to hit
 * @type boolean
 * @default false
 *
 * @param Save DC Base
 * @type number
 * @default 13
 *
 * @param Enemy DC Base
 * @desc DC base when an enemy forces an actor to save.
 * @type number
 * @default 10
 *
 * @param Trained Save Bonus
 * @type number
 * @default 3
 *
 * @param Minion Damage Rate
 * @type number
 * @decimals 2
 * @default 0.5
 *
 * @param Role Extra Actions
 * @desc Extra actions per turn by role.
 * @default elite:0, boss:1, apex:1
 *
 * @param Role Extra Attacks
 * @desc Extra hits on a plain attack by role.
 * @default elite:1, boss:0, apex:1
 *
 * @param Boss State Shrug
 * @type boolean
 * @default true
 *
 * @param Escape Base
 * @type number
 * @decimals 2
 * @default 0.45
 *
 * @param Escape DEX Divisor
 * @type number
 * @default 300
 *
 * @param Escape Step
 * @desc Added after every failed escape.
 * @type number
 * @decimals 2
 * @default 0.15
 *
 * @param Target Preview
 * @type boolean
 * @default true
 *
 * @param Log Notes
 * @text Log weakness / wall / saves
 * @type boolean
 * @default true
 *
 * @param Show Rolls
 * @text Show dice in the log
 * @type boolean
 * @default false
 *
 * @param Mastery Report
 * @type boolean
 * @default true
 */

(() => {
    "use strict";
    const PLUGIN = "Rank_Battle";
    const P = PluginManager.parameters(PLUGIN) || {};
    const has = v => v !== undefined && v !== null && String(v).trim() !== "";
    const num = (v, d) => (has(v) && !isNaN(Number(v)) ? Number(v) : d);
    const bool = (v, d) => (has(v) ? String(v).trim() === "true" : d);
    const Rank = window.Rank;
    if (!Rank) throw new Error("Rank_Battle needs Rank_Core above it in the plugin list.");
    const roleMap = s => {
        const out = {};
        for (const part of String(s || "").split(",")) {
            const m = part.match(/^\s*(\w+)\s*:\s*(-?\d+)\s*$/);
            if (m) out[m[1].toLowerCase()] = Number(m[2]);
        }
        return out;
    };

    const BP = (Rank.BP = {
        attackBonus: num(P["Attack Bonus"], 8),
        unarmedDie: num(P["Unarmed Die"], 4),
        enemyAttackDie: num(P["Enemy Attack Die"], 6),
        skillDie: num(P["Default Skill Die"], 6),
        critMult: num(P["Crit Multiplier"], 1.5),
        multiRate: num(P["Multi-Target Rate"], 0.5),
        areaRoll: bool(P["Area Attack Roll"], false),
        dcBase: num(P["Save DC Base"], 13),
        enemyDcBase: num(P["Enemy DC Base"], 10),
        trainedSave: num(P["Trained Save Bonus"], 3),
        minionRate: num(P["Minion Damage Rate"], 0.5),
        roleActions: roleMap(has(P["Role Extra Actions"]) ? P["Role Extra Actions"] : "elite:0, boss:1, apex:1"),
        roleAttacks: roleMap(has(P["Role Extra Attacks"]) ? P["Role Extra Attacks"] : "elite:1, boss:0, apex:1"),
        bossShrug: bool(P["Boss State Shrug"], true),
        escBase: num(P["Escape Base"], 0.45),
        escDiv: num(P["Escape DEX Divisor"], 300),
        escStep: num(P["Escape Step"], 0.15),
        preview: bool(P["Target Preview"], true),
        logNotes: bool(P["Log Notes"], true),
        showRolls: bool(P["Show Rolls"], false),
        masteryReport: bool(P["Mastery Report"], true)
    });
    Rank.unarmedDie = () => BP.unarmedDie;
    Rank.enemyAttackDie = () => BP.enemyAttackDie;

    //-------------------------------------------------------------------------
    // Action info (everything that depends on the user, not the target)
    //-------------------------------------------------------------------------
    Game_Action.prototype.rkUsesRules = function() {
        const item = this.item();
        if (!item || !DataManager.isSkill(item)) return false;
        const rk = Rank.skillRk(item);
        return !!rk && !rk.native;
    };

    Game_Action.prototype.rkIsMultiTarget = function() {
        return this.isForAll() || (this.isForRandom() && this.numTargets() > 1);
    };

    Game_Action.prototype.rkInfo = function() {
        const subject = this.subject();
        const item = this.item();
        const rk = Rank.skillRk(item);
        const isAttack = this.isAttack();
        const statName = isAttack ? subject.rkAttackStat() : Rank.skillStat(item, subject);
        const statValue = subject.rkStat(statName);
        const subjRank = subject.rkRank();
        let gbRank;
        let dice;
        let form;
        if (isAttack) {
            gbRank = subject.isActor() ? subject.rkWeaponRank() : subjRank;
            dice = subject.rkAttackDice();
            form = { hits: 1, rate: 1, bonus: 0, hit: 0, crit: 0, states: [] };
        } else {
            gbRank = subject.rkSkillRank(item);
            form = subject.rkSkillForm(item);
            dice = form.dice || rk.dice || Rank.dice(1, BP.skillDie, 0);
        }
        const atkRank = Math.min(subjRank + 2, Math.max(subjRank, gbRank));
        return { subject, item, rk, isAttack, statName, statValue, subjRank, gbRank, atkRank, dice, form };
    };

    // Hook for other plugins: adjust the rank gap of one action against one target
    // (before weakness is counted). Story plugins use it for rank-piercing relics.
    Game_Action.prototype.rkAdjustGap = function(gap, info, target) {
        return gap;
    };

    // "roll" = attack roll vs AC, "none" = lands automatically
    Game_Action.prototype.rkRollMode = function(info) {
        if (info.rk.rollMode === "roll") return "roll";
        if (info.rk.rollMode === "none") return "none";
        if (this.isCertainHit()) return "none";
        if (this.isForFriend() && !this.isForOpponent()) return "none";
        if (this.isForAll() && !BP.areaRoll) return "none";
        return "roll";
    };

    Game_Action.prototype.rkHitBonus = function(info) {
        return Rank.mod(info.statValue) + BP.attackBonus + info.subject.rkHitBonus() + (info.rk.hit || 0) + (info.form.hit || 0);
    };

    Game_Action.prototype.rkCritThreshold = function(info) {
        const subject = info.subject;
        const fromTrait = Math.floor((subject.cri || 0) * 20 + 1e-6);
        const t = 20 - fromTrait - subject.rkCritBonus() - (info.rk.crit || 0) - (info.form.crit || 0);
        return Rank.clamp(t, 2, 20);
    };

    Game_Action.prototype.rkSaveDC = function(info, target) {
        const base = info.subject.isEnemy() && target.isActor() ? BP.enemyDcBase : BP.dcBase;
        return base + Rank.mod(info.statValue) + (info.rk.dcBonus || 0);
    };

    Game_Action.prototype.rkSaveBonus = function(target, stat) {
        return Rank.mod(target.rkStat(stat)) + (target.rkIsTrainedSave(stat) ? BP.trainedSave : 0);
    };

    Rank.hitChance = function(need) {
        // P(d20 >= need) with natural 1 always missing and natural 20 always hitting
        const faces = Rank.clamp(21 - need, 1, 19);
        return faces / 20;
    };

    Rank.saveChance = function(need, adv, dis) {
        const p = Rank.clamp((21 - need) / 20, 0, 1);
        if (adv && !dis) return 1 - (1 - p) * (1 - p);
        if (dis && !adv) return p * p;
        return p;
    };

    Rank.isDamaging = item => [1, 2, 5, 6].includes(item.damage.type);
    Rank.isRecovering = item => [3, 4].includes(item.damage.type);

    //-------------------------------------------------------------------------
    // Resolution: rolls (or estimates) hit, crit, save, gap for one target
    //-------------------------------------------------------------------------
    Game_Action.prototype.rkResolve = function(target, estimate) {
        const info = this.rkInfo();
        const item = info.item;
        const res = { info, hit: true, crit: false, roll: 0, total: 0, ac: 0, mode: "none", gap: 0, gapMult: 1,
            weak: false, resist: 1, immune: false, wall: false, saved: false, save: null, saveMode: null,
            hitChance: 1, saveChance: 0 };
        const hostile = Rank.isDamaging(item) || (this.isForOpponent() && target.isActor() !== info.subject.isActor());
        // --- rank gap (only for harm) ---
        if (hostile) {
            res.gap = this.rkAdjustGap(info.atkRank - target.rkRank(), info, target);
            const rate = this.calcElementRate(target);
            if (rate > 1) {
                res.weak = true;
                res.gap += 1;
            } else if (rate <= 0) {
                res.immune = true;
            } else if (rate < 1) {
                res.resist = rate;
            }
            res.gapMult = Rank.gapMult(res.gap);
            res.wall = res.gapMult === 0;
        }
        // --- attack roll ---
        res.mode = this.rkRollMode(info);
        if (res.mode === "roll") {
            res.ac = target.rkAC();
            const bonus = this.rkHitBonus(info);
            res.bonus = bonus;
            res.hitChance = Rank.hitChance(res.ac - bonus);
            if (!estimate) {
                const nat = Rank.d20();
                res.roll = nat;
                res.total = nat + bonus;
                res.hit = nat === 20 || (nat !== 1 && res.total >= res.ac);
                res.crit = res.hit && !!item.damage.critical && Rank.isDamaging(item) && nat >= this.rkCritThreshold(info);
            }
        }
        // --- save ---
        if (info.rk.save && hostile) {
            const stat = info.rk.save.stat;
            const dc = this.rkSaveDC(info, target);
            const bonus = this.rkSaveBonus(target, stat);
            const adv = res.gap <= -2;
            const dis = res.gap >= 2;
            res.save = { stat, dc, bonus, adv, dis };
            res.saveMode = info.rk.save.mode;
            res.saveChance = res.wall ? 1 : Rank.saveChance(dc - bonus, adv, dis);
            if (!estimate && res.hit) {
                if (res.wall) res.saved = true;
                else {
                    let r = Rank.d20();
                    if (adv && !dis) r = Math.max(r, Rank.d20());
                    if (dis && !adv) r = Math.min(r, Rank.d20());
                    res.save.roll = r;
                    res.save.total = r + bonus;
                    res.saved = res.save.total >= dc;
                }
            }
        }
        return res;
    };

    // Damage (positive) or healing (negative). mode: roll | min | max | avg
    Game_Action.prototype.rkComputeValue = function(target, res, mode, critical) {
        const info = res.info;
        const item = info.item;
        const d = info.dice;
        const roll = mode === "min" ? Rank.diceMin(d) : mode === "max" ? Rank.diceMax(d) : mode === "avg" ? Rank.diceAvg(d) : Rank.rollDice(d);
        const base = roll + Rank.pow(info.statValue) + 10 * info.gbRank + (info.rk.bonus || 0) + (info.form.bonus || 0);
        const rate = (info.rk.rate === null || info.rk.rate === undefined ? 1 : info.rk.rate) * (info.form.rate || 1);
        const multi = this.rkIsMultiTarget() ? (info.rk.areaRate !== null && info.rk.areaRate !== undefined ? info.rk.areaRate : BP.multiRate) : 1;
        if (Rank.isRecovering(item)) {
            let v = base * rate * multi * target.rec;
            if (this.isItem()) v *= info.subject.pha;
            return -Math.max(0, Math.round(v));
        }
        if (!Rank.isDamaging(item)) return 0;
        if (res.wall || res.immune) return 0;
        let mult = res.gapMult * res.resist * rate * multi;
        if (res.saved) {
            if (res.saveMode === "negates") return 0;
            if (res.saveMode === "half") mult *= 0.5;
        }
        if (critical) mult *= BP.critMult;
        if (info.subject.isEnemy() && info.subject.rkRole() === "minion") mult *= BP.minionRate;
        if (this.isPhysical()) mult *= target.pdr;
        if (this.isMagical()) mult *= target.mdr;
        if (mult <= 0) return 0;
        let value = this.applyGuard(base * mult, target);
        return Math.max(1, Math.round(value));
    };

    const _Game_Action_makeDamageValue = Game_Action.prototype.makeDamageValue;
    Game_Action.prototype.makeDamageValue = function(target, critical) {
        if (!this.rkUsesRules()) return _Game_Action_makeDamageValue.call(this, target, critical);
        if (this._rkRes) return this.rkComputeValue(target, this._rkRes, "roll", critical);
        // AI evaluation: expected value, no dice
        const res = this.rkResolve(target, true);
        return this.rkComputeValue(target, res, "avg", false);
    };

    const _Game_Action_apply = Game_Action.prototype.apply;
    Game_Action.prototype.apply = function(target) {
        if (!this.rkUsesRules()) {
            _Game_Action_apply.call(this, target);
            this.rkRecordApply(target, null, false);
            return;
        }
        const wasAlive = target.isAlive();
        const result = target.result();
        this.subject().clearResult();
        result.clear();
        result.used = this.testApply(target);
        const res = this.rkResolve(target, false);
        this._rkRes = res;
        result.rk = res;
        result.missed = result.used && !res.hit;
        result.evaded = false;
        result.physical = this.isPhysical();
        result.drain = this.isDrain();
        if (result.isHit()) {
            if (this.item().damage.type > 0) {
                result.critical = res.crit;
                const value = this.makeDamageValue(target, result.critical);
                this.executeDamage(target, value);
            }
            if (!res.wall) {
                for (const effect of this.item().effects) {
                    this.applyItemEffect(target, effect);
                }
                this.rkApplyFormStates(target, res);
            }
            this.applyItemUserEffect(target);
        }
        this.updateLastTarget(target);
        this._rkRes = null;
        this.rkRecordApply(target, res, wasAlive && target.isDead());
    };

    Game_Action.prototype.rkBlocksStates = function() {
        const res = this._rkRes;
        return !!res && (res.wall || res.immune || (res.saved && res.saveMode !== null));
    };

    const _Game_Action_itemEffectAddState = Game_Action.prototype.itemEffectAddState;
    Game_Action.prototype.itemEffectAddState = function(target, effect) {
        if (this.rkBlocksStates()) return;
        _Game_Action_itemEffectAddState.call(this, target, effect);
    };

    const _Game_Action_itemEffectAddDebuff = Game_Action.prototype.itemEffectAddDebuff;
    Game_Action.prototype.itemEffectAddDebuff = function(target, effect) {
        if (this.rkBlocksStates()) return;
        _Game_Action_itemEffectAddDebuff.call(this, target, effect);
    };

    Game_Action.prototype.rkApplyFormStates = function(target, res) {
        if (this.rkBlocksStates()) return;
        for (const s of res.info.form.states || []) {
            if (!$dataStates[s.id]) continue;
            const chance = s.chance * target.stateRate(s.id) * this.lukEffectRate(target);
            if (Math.random() < chance) {
                target.addState(s.id);
                this.makeSuccess(target);
            }
        }
    };

    // skill forms can strike more than once
    const _Game_Action_numRepeats = Game_Action.prototype.numRepeats;
    Game_Action.prototype.numRepeats = function() {
        let n = _Game_Action_numRepeats.call(this);
        if (this.rkUsesRules() && !this.isAttack()) {
            const form = this.subject().rkSkillForm(this.item());
            if (form.hits > n) n = form.hits;
        }
        return n;
    };

    // initiative: d20 + MOD(DEX) (heavy armor without the strength: -5)
    Game_Action.prototype.speed = function() {
        const subject = this.subject();
        let speed = Rank.d20() + subject.rkMod("DEX") + Math.random();
        if (subject.isActor() && subject.rkHeavyPenalty()) speed -= 5;
        if (this.item()) speed += this.item().speed;
        if (this.isAttack()) speed += subject.attackSpeed();
        return speed;
    };

    //-------------------------------------------------------------------------
    // Roles
    //-------------------------------------------------------------------------
    Game_Enemy.prototype.rkIsBig = function() {
        const r = this.rkRole();
        return r === "boss" || r === "apex";
    };

    const _Game_Enemy_makeActionTimes = Game_Enemy.prototype.makeActionTimes;
    Game_Enemy.prototype.makeActionTimes = function() {
        const base = _Game_Enemy_makeActionTimes.call(this);
        return base + Math.max(0, BP.roleActions[this.rkRole()] || 0);
    };

    Game_Enemy.prototype.attackTimesAdd = function() {
        return Game_BattlerBase.prototype.attackTimesAdd.call(this) + Math.max(0, BP.roleAttacks[this.rkRole()] || 0);
    };

    Game_Enemy.prototype.addState = function(stateId) {
        const st = $dataStates[stateId];
        if (BP.bossShrug && st && this.rkIsBig() && stateId !== this.deathStateId() && st.restriction > 0 &&
            this.isStateAddable(stateId) && !this.isStateAffected(stateId)) {
            this._rkShrug = this._rkShrug || {};
            if (this._rkShrug[stateId]) {
                this._rkShrug[stateId] = false;
                this._result.rkShrugged = true;
                return;
            }
            this._rkShrug[stateId] = true;
        }
        Game_Battler.prototype.addState.call(this, stateId);
    };

    Game_Enemy.prototype.resetStateCounts = function(stateId) {
        Game_Battler.prototype.resetStateCounts.call(this, stateId);
        const st = $dataStates[stateId];
        if (BP.bossShrug && st && this.rkIsBig() && st.restriction > 0) {
            this._stateTurns[stateId] = Math.min(this._stateTurns[stateId], 1);
        }
    };

    //-------------------------------------------------------------------------
    // Escape
    //-------------------------------------------------------------------------
    const avgDex = unit => {
        const m = unit.aliveMembers();
        return m.length ? m.reduce((r, b) => r + b.rkStat("DEX"), 0) / m.length : 0;
    };

    BattleManager.makeEscapeRatio = function() {
        const r = BP.escBase + (avgDex($gameParty) - avgDex($gameTroop)) / Math.max(1, BP.escDiv);
        this._escapeRatio = Rank.clamp(r, 0.1, 0.95);
    };

    const _BattleManager_onEscapeFailure = BattleManager.onEscapeFailure;
    BattleManager.onEscapeFailure = function() {
        _BattleManager_onEscapeFailure.call(this);
        this._escapeRatio = Rank.clamp(this._escapeRatio - 0.1 + BP.escStep, 0.1, 0.95);
    };

    //-------------------------------------------------------------------------
    // Mastery tracking
    //-------------------------------------------------------------------------
    const _BattleManager_initMembers = BattleManager.initMembers;
    BattleManager.initMembers = function() {
        _BattleManager_initMembers.call(this);
        this.rkResetMastery();
    };

    BattleManager.rkResetMastery = function() {
        this._rkUse = null;
        this._rkGains = {};
        this._rkBreak = {};
        this._rkSupportFull = {};
        this._rkMessages = [];
    };

    const _BattleManager_startAction = BattleManager.startAction;
    BattleManager.startAction = function() {
        const subject = this._subject;
        const action = subject ? subject.currentAction() : null;
        _BattleManager_startAction.call(this);
        this._rkUse = action ? { subject, action, item: action.item(), foeRank: -1, kills: [] } : null;
    };

    Game_Action.prototype.rkRecordApply = function(target, res, killed) {
        const use = BattleManager._rkUse;
        if (!$gameParty.inBattle() || !use || use.action !== this) return;
        const subject = use.subject;
        if (target.isActor() === subject.isActor()) return; // only foes teach
        if (res && res.hit === false && !Rank.isDamaging(this.item())) return;
        use.foeRank = Math.max(use.foeRank, target.rkRank());
        if (killed) use.kills.push({ rank: target.rkRank(), role: target.rkRole() });
    };

    const _BattleManager_endAction = BattleManager.endAction;
    BattleManager.endAction = function() {
        this.rkFinishUse();
        _BattleManager_endAction.call(this);
    };

    BattleManager.rkStrongestFoeRank = function(includeDead) {
        const members = includeDead ? $gameTroop.members() : $gameTroop.aliveMembers();
        return members.reduce((r, e) => Math.max(r, e.rkRank()), -1);
    };

    BattleManager.rkFinishUse = function() {
        const use = this._rkUse;
        this._rkUse = null;
        if (!use || !use.subject || !use.subject.isActor()) return;
        const actor = use.subject;
        const skill = use.item;
        if (!DataManager.isSkill(skill) || !Rank.isMasterySkill(skill) || !actor.hasSkill(skill.id)) return;
        const id = skill.id;
        const mr = actor.rkMasteryRank(id);
        let foeRank = use.foeRank;
        const support = !use.action.isForOpponent() || Rank.skillRk(skill).support;
        if (foeRank < 0) foeRank = this.rkStrongestFoeRank(false);
        if (foeRank < 0) return;
        const intFactor = 1 + actor.rkStat("INT") / Math.max(1, Rank.P.masteryIntDivisor);
        let gain = Rank.P.masteryPerUse * Rank.masteryFactor(foeRank - mr) * intFactor;
        for (const k of use.kills) {
            const bonus = Rank.P.masteryKill[k.role] !== undefined ? Rank.P.masteryKill[k.role] : 10;
            gain += bonus * Rank.masteryFactor(k.rank - mr) * intFactor;
        }
        gain = Math.round(gain);
        const messages = [];
        const got = actor.rkGainMastery(id, gain, messages);
        const aid = actor.actorId();
        if (got > 0) {
            this._rkGains[aid] = this._rkGains[aid] || {};
            this._rkGains[aid][id] = (this._rkGains[aid][id] || 0) + got;
        }
        // breakthrough: the bar is full and the skill finished a next-rank foe
        if (Rank.P.breakthrough && actor.rkIsBarFull(id)) {
            if (support) {
                (this._rkSupportFull[aid] = this._rkSupportFull[aid] || {})[id] = true;
            } else if (use.kills.some(k => k.rank >= mr + 1)) {
                (this._rkBreak[aid] = this._rkBreak[aid] || {})[id] = true;
            }
        }
        for (const m of messages) {
            this._logWindow.push("addText", m);
            this._logWindow.push("wait");
        }
    };

    //-------------------------------------------------------------------------
    // Victory: EXP by rank gap, mastery report, breakthroughs
    //-------------------------------------------------------------------------
    BattleManager.rkExpFor = function(actor) {
        const ar = actor.rkRank();
        let total = 0;
        for (const enemy of $gameTroop.deadMembers()) {
            total += enemy.exp() * Rank.expGapRate(enemy.rkRank() - ar);
        }
        return Math.round(total);
    };

    const _BattleManager_makeRewards = BattleManager.makeRewards;
    BattleManager.makeRewards = function() {
        _BattleManager_makeRewards.call(this);
        const exp = {};
        for (const actor of $gameParty.allMembers()) exp[actor.actorId()] = this.rkExpFor(actor);
        this._rewards.rkExp = exp;
    };

    BattleManager.displayExp = function() {
        const exp = this._rewards.rkExp || {};
        const members = $gameParty.battleMembers();
        const values = members.map(a => exp[a.actorId()] || 0);
        if (values.length === 0) return;
        const same = values.every(v => v === values[0]);
        if (same) {
            if (values[0] > 0) {
                $gameMessage.add("\\." + TextManager.obtainExp.format(values[0], TextManager.exp));
            } else if (this._rewards.exp > 0) {
                $gameMessage.add("\\.These foes are too weak to teach you anything.");
            }
            return;
        }
        const parts = members.map(a => a.name() + " " + (exp[a.actorId()] || 0));
        $gameMessage.add("\\." + TextManager.exp + ": " + parts.join("  "));
    };

    BattleManager.gainExp = function() {
        const exp = this._rewards.rkExp || {};
        for (const actor of $gameParty.allMembers()) {
            actor.gainExp(exp[actor.actorId()] || 0);
        }
    };

    const _BattleManager_gainRewards = BattleManager.gainRewards;
    BattleManager.gainRewards = function() {
        _BattleManager_gainRewards.call(this);
        this.rkVictoryMastery();
    };

    BattleManager.rkVictoryMastery = function() {
        const lines = [];
        const rankUps = [];
        const troopTop = this.rkStrongestFoeRank(true);
        // report gains
        if (BP.masteryReport) {
            for (const actor of $gameParty.members()) {
                const g = this._rkGains[actor.actorId()];
                if (!g) continue;
                const parts = Object.keys(g).map(id => {
                    const s = $dataSkills[id];
                    return s ? s.name + " +" + g[id] : "";
                }).filter(Boolean);
                if (parts.length) lines.push(actor.name() + ": " + parts.join(", "));
            }
        }
        // breakthroughs
        if (Rank.P.breakthrough) {
            for (const actor of $gameParty.members()) {
                const aid = actor.actorId();
                const ids = new Set(Object.keys(this._rkBreak[aid] || {}).map(Number));
                for (const id of Object.keys(this._rkSupportFull[aid] || {}).map(Number)) {
                    if (troopTop >= actor.rkMasteryRank(id) + 1) ids.add(id);
                }
                for (const id of ids) {
                    if (actor.isLearnedSkill(id) && actor.rkIsBarFull(id)) {
                        rankUps.push("Breakthrough!");
                        actor.rkRankUpSkill(id, rankUps);
                    }
                }
            }
            // hint for full bars still waiting
            for (const actor of $gameParty.members()) {
                const g = this._rkGains[actor.actorId()];
                if (!g) continue;
                for (const id of Object.keys(g).map(Number)) {
                    if (actor.isLearnedSkill(id) && actor.rkIsBarFull(id)) {
                        const need = Rank.letter(actor.rkMasteryRank(id) + 1);
                        lines.push($dataSkills[id].name + " is ready to break through: defeat a rank " + need + " foe with it.");
                    }
                }
            }
        }
        if (lines.length || rankUps.length) {
            $gameMessage.newPage();
            for (const l of lines) $gameMessage.add(l);
            for (const r of rankUps) $gameMessage.add(r);
        }
        this.rkResetMastery();
    };

    //-------------------------------------------------------------------------
    // Menu use (optional mastery outside battle)
    //-------------------------------------------------------------------------
    const _Scene_Skill_useItem = Scene_Skill.prototype.useItem;
    Scene_Skill.prototype.useItem = function() {
        const skill = this.item();
        const actor = this.user();
        _Scene_Skill_useItem.call(this);
        if (Rank.P.menuMastery > 0 && actor && Rank.isMasterySkill(skill)) {
            const messages = [];
            actor.rkGainMastery(skill.id, Rank.P.menuMastery, messages);
        }
    };

    //-------------------------------------------------------------------------
    // Battle log notes
    //-------------------------------------------------------------------------
    Rank.resultNote = function(res, target) {
        if (!res) return "";
        const bits = [];
        if (BP.showRolls && res.mode === "roll" && res.roll) {
            bits.push("d20 " + res.roll + " + " + res.bonus + " vs AC " + res.ac);
        }
        if (res.wall) bits.push("Rank wall: nothing gets through.");
        else {
            if (res.immune) bits.push("Immune!");
            if (res.weak) bits.push("Weak spot! " + Rank.gapLabel(res.gap));
            else if (res.gap !== 0 && res.info && Rank.isDamaging(res.info.item)) bits.push(Rank.gapLabel(res.gap));
            if (res.resist < 1 && !res.immune) bits.push("Resisted.");
            if (res.save && res.save.roll) {
                const s = res.save;
                if (BP.showRolls) bits.push(s.stat + " save " + s.roll + " + " + s.bonus + " vs DC " + s.dc + (res.saved ? " saved" : " failed"));
                else if (res.saved) bits.push(target.name() + " saves!");
            }
        }
        return bits.join("  ");
    };

    const _Window_BattleLog_displayCritical = Window_BattleLog.prototype.displayCritical;
    Window_BattleLog.prototype.displayCritical = function(target) {
        _Window_BattleLog_displayCritical.call(this, target);
        const result = target.result();
        if (BP.logNotes && result.rk && result.isHit()) {
            const note = Rank.resultNote(result.rk, target);
            if (note) this.push("addText", note);
        }
        if (result.rkShrugged) this.push("addText", target.name() + " shrugs it off!");
    };

    const _Game_ActionResult_clear = Game_ActionResult.prototype.clear;
    Game_ActionResult.prototype.clear = function() {
        _Game_ActionResult_clear.call(this);
        this.rk = null;
        this.rkShrugged = false;
    };

    //-------------------------------------------------------------------------
    // Target preview (help window while choosing a target)
    //-------------------------------------------------------------------------
    Rank.conditionText = function(b) {
        const r = b.mhp > 0 ? b.hp / b.mhp : 0;
        if (b.isDead()) return "Down";
        if (r >= 1) return "Unhurt";
        if (r > 0.5) return "Hurt";
        if (r > 0.25) return "Bloodied";
        return "Critical";
    };

    Rank.pct = p => Math.round(p * 100) + "%";

    Rank.previewText = function(action, target) {
        if (!target) return "";
        const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
        let head = target.name() + " \\RK[" + target.rkRank() + "]";
        if (target.isEnemy()) {
            if (target.rkRole() !== "standard") head += " " + cap(target.rkRole());
            head += "  " + Rank.conditionText(target);
        } else {
            head += "  HP " + target.hp + "/" + target.mhp;
        }
        if (!action || !action.item()) return head;
        const item = action.item();
        if (!action.rkUsesRules()) return head + "\n" + item.name;
        const res = action.rkResolve(target, true);
        const bits = [];
        if (Rank.isDamaging(item) || action.isForOpponent()) {
            if (res.wall) return head + "\n\\C[2]RANK WALL\\C[0]  nothing gets through (" + Rank.letter(res.info.atkRank) + " vs " + Rank.letter(target.rkRank()) + ")";
            if (res.mode === "roll") bits.push("Hit " + Rank.pct(res.hitChance) + " (AC " + res.ac + ")");
            if (res.save) bits.push(res.save.stat + " save " + Rank.pct(res.saveChance) + (res.save.adv ? " (adv)" : res.save.dis ? " (dis)" : ""));
            if (Rank.isDamaging(item)) {
                if (res.immune) bits.push("\\C[2]IMMUNE\\C[0]");
                else {
                    const lo = action.rkComputeValue(target, res, "min", false);
                    const hi = action.rkComputeValue(target, res, "max", false);
                    let dmg = "Dmg " + (lo === hi ? lo : lo + "-" + hi) + " " + Rank.gapLabel(res.gap);
                    if (res.weak) dmg += " \\C[3]WEAK\\C[0]";
                    if (res.resist < 1) dmg += " resist";
                    if (res.save && res.saveMode === "half") dmg += " (half on save)";
                    if (res.save && res.saveMode === "negates") dmg += " (none on save)";
                    bits.push(dmg);
                }
            }
        } else if (Rank.isRecovering(item)) {
            const lo = -action.rkComputeValue(target, res, "min", false);
            const hi = -action.rkComputeValue(target, res, "max", false);
            bits.push((item.damage.type === 4 ? "Restore MP " : "Heal ") + (lo === hi ? lo : lo + "-" + hi));
        } else {
            bits.push(item.name);
        }
        return head + "\n" + bits.join("  ·  ");
    };

    const _Scene_Battle_createEnemyWindow = Scene_Battle.prototype.createEnemyWindow;
    Scene_Battle.prototype.createEnemyWindow = function() {
        _Scene_Battle_createEnemyWindow.call(this);
        if (BP.preview) this._enemyWindow.setHelpWindow(this._helpWindow);
    };

    const _Scene_Battle_createActorWindow = Scene_Battle.prototype.createActorWindow;
    Scene_Battle.prototype.createActorWindow = function() {
        _Scene_Battle_createActorWindow.call(this);
        if (BP.preview) this._actorWindow.setHelpWindow(this._helpWindow);
    };

    Window_BattleEnemy.prototype.updateHelp = function() {
        if (this._helpWindow) this._helpWindow.setText(Rank.previewText(BattleManager.inputtingAction(), this.enemy()));
    };

    Window_BattleActor.prototype.updateHelp = function() {
        if (this._helpWindow) this._helpWindow.setText(Rank.previewText(BattleManager.inputtingAction(), this.actor(this.index())));
    };

    const _Window_BattleEnemy_show = Window_BattleEnemy.prototype.show;
    Window_BattleEnemy.prototype.show = function() {
        _Window_BattleEnemy_show.call(this);
        this.showHelpWindow();
    };

    const _Window_BattleEnemy_hide = Window_BattleEnemy.prototype.hide;
    Window_BattleEnemy.prototype.hide = function() {
        _Window_BattleEnemy_hide.call(this);
        this.hideHelpWindow();
    };

    const _Window_BattleActor_show = Window_BattleActor.prototype.show;
    Window_BattleActor.prototype.show = function() {
        _Window_BattleActor_show.call(this);
        this.showHelpWindow();
    };

    const _Window_BattleActor_hide = Window_BattleActor.prototype.hide;
    Window_BattleActor.prototype.hide = function() {
        _Window_BattleActor_hide.call(this);
        this.hideHelpWindow();
    };
})();
