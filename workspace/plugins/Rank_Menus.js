//=============================================================================
// Rank_Menus.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [v1.0] Rank menus: rank badges, skill mastery bars, stat point screen, rank-aware status/equip/shop.
 * @author Ten & Claude
 * @base Rank_Core
 * @orderAfter Rank_Battle
 *
 * @help Rank_Menus.js
 *
 * The menu side of the rank system.
 *
 *  - A rank badge after every level (menu, skill and status screens) and in
 *    the corner of every battle face.
 *  - Skill lists: mastery rank badge, a thin mastery bar under the name and
 *    the rank-scaled MP cost. The help box gets an extra line: mastery,
 *    stat, power (dimmed badge = the stat's grade holds the skill back).
 *  - Status: rank and title, stat points, AC / hit / crit, the 7 stats with
 *    grade, MOD, POW and aptitude, attack die and trained saves.
 *  - Equip: the 7 stats, Max HP/MP, AC and attack die, before -> after.
 *  - Shop: average damage change for weapons, AC change for armor.
 *  - "Stat Points" menu command, the point-assignment screen:
 *        Right or OK  +1        Left  -1        hold Shift  x10
 *        Q / W        other party member
 *        Cancel       undo the unconfirmed points, then leave
 *    Nothing is spent until you pick Confirm.
 *
 * Plugin command: Open Stat Points.   Script: SceneManager.push(Scene_RankStats)
 *
 * @param Stat Command
 * @text Stat menu command
 * @desc Main menu command for the stat point screen. Empty = no command.
 * @default Stat Points
 *
 * @param Points Label
 * @default Stat Points
 *
 * @param Confirm Text
 * @default Confirm
 *
 * @param Reset Text
 * @default Reset
 *
 * @param Battle Badges
 * @text Rank badges on battle faces
 * @type boolean
 * @default true
 *
 * @param Menu Help Lines
 * @text Skill screen help lines
 * @desc Lines in the skill screen help box (description + mastery line).
 * @type number
 * @min 2
 * @max 4
 * @default 3
 *
 * @command OpenStatPoints
 * @text Open Stat Points
 * @desc Opens the stat point screen.
 * @arg actorId
 * @text Actor (0 = party leader)
 * @type actor
 * @default 0
 */

(() => {
    "use strict";
    const PLUGIN = "Rank_Menus";
    const P = PluginManager.parameters(PLUGIN) || {};
    const Rank = window.Rank;
    if (!Rank) throw new Error("Rank_Menus needs Rank_Core above it in the plugin list.");
    const has = v => v !== undefined && v !== null && String(v).trim() !== "";
    const text = (v, d) => (has(v) ? String(v) : d);
    const num = (v, d) => (has(v) && !isNaN(Number(v)) ? Number(v) : d);
    const bool = (v, d) => (has(v) ? String(v).trim() === "true" : d);
    const signed = n => (n >= 0 ? "+" + n : String(n));

    const MP = (Rank.MP = {
        statCommand: P["Stat Command"] !== undefined ? String(P["Stat Command"]) : "Stat Points",
        pointsLabel: text(P["Points Label"], "Stat Points"),
        confirmText: text(P["Confirm Text"], "Confirm"),
        resetText: text(P["Reset Text"], "Reset"),
        battleBadges: bool(P["Battle Badges"], true),
        helpLines: Rank.clamp(num(P["Menu Help Lines"], 3), 2, 4)
    });

    const isDamaging = item => [1, 2, 5, 6].includes(item.damage.type);
    const isRecovering = item => [3, 4].includes(item.damage.type);

    //-------------------------------------------------------------------------
    // Shared numbers
    //-------------------------------------------------------------------------
    Rank.aptitudeLetter = function(value) {
        let best = null;
        let bestDiff = Infinity;
        for (const key of Object.keys(Rank.P.aptitudeValues)) {
            const d = Math.abs(Rank.P.aptitudeValues[key] - value);
            if (d < bestDiff) {
                best = key.toUpperCase();
                bestDiff = d;
            }
        }
        return best || String(value);
    };

    // plain attack: die, stat, flat part, hit bonus, crit threshold, AC
    Rank.combatInfo = function(actor) {
        const out = {
            ac: actor.rkAC(),
            dice: actor.rkAttackDice(),
            stat: actor.rkAttackStat(),
            hit: 0,
            crit: 20
        };
        out.flat = Rank.pow(actor.rkStat(out.stat)) + 10 * (actor.rkWeaponRank ? actor.rkWeaponRank() : 0);
        if (Rank.BP && Game_Action.prototype.rkInfo && $gameActors.actor(actor.actorId()) === actor) {
            const action = new Game_Action(actor);
            action.setAttack();
            const info = action.rkInfo();
            out.hit = action.rkHitBonus(info);
            out.crit = action.rkCritThreshold(info);
        } else {
            out.hit = Rank.mod(actor.rkStat(out.stat)) + (Rank.BP ? Rank.BP.attackBonus : 0) + actor.rkHitBonus();
        }
        out.critText = out.crit >= 20 ? "20" : out.crit + "-20";
        return out;
    };

    // average plain-attack damage before the target (for comparisons)
    Rank.attackAverage = function(actor) {
        const flat = Rank.pow(actor.rkStat(actor.rkAttackStat())) + 10 * (actor.rkWeaponRank ? actor.rkWeaponRank() : 0);
        return Rank.diceAvg(actor.rkAttackDice()) + flat;
    };

    // damage / healing range of a skill before the target
    Rank.skillPowerRange = function(actor, skill) {
        if (!actor || !skill || !DataManager.isSkill(skill)) return null;
        const rk = Rank.skillRk(skill);
        if (!rk || rk.native) return null;
        if (!isDamaging(skill) && !isRecovering(skill)) return null;
        const form = actor.rkSkillForm(skill);
        const defDie = Rank.BP ? Rank.BP.skillDie : 6;
        const dice = form.dice || rk.dice || Rank.dice(1, defDie, 0);
        const stat = Rank.skillStat(skill, actor);
        const wr = actor.rkSkillRank(skill);
        const flat = Rank.pow(actor.rkStat(stat)) + 10 * wr + (rk.bonus || 0) + (form.bonus || 0);
        let rate = (rk.rate === null || rk.rate === undefined ? 1 : rk.rate) * (form.rate || 1);
        // all enemies/allies, or several random targets (same rule as Rank_Battle)
        const multi = [2, 4, 5, 6, 8, 10, 13, 14].includes(skill.scope);
        let each = false;
        if (multi) {
            const areaRate = rk.areaRate !== null && rk.areaRate !== undefined ? rk.areaRate : Rank.BP ? Rank.BP.multiRate : 0.5;
            rate *= areaRate;
            each = true;
        }
        const lo = Math.max(0, Math.round((Rank.diceMin(dice) + flat) * rate));
        const hi = Math.max(0, Math.round((Rank.diceMax(dice) + flat) * rate));
        return { lo, hi, hits: form.hits || 1, heal: isRecovering(skill), each };
    };

    // "Mastery \RK[2] 120/360 · DEX · Power 14-21" (text codes for drawTextEx)
    Rank.skillInfoLine = function(actor, skill) {
        if (!actor || !actor.isActor || !actor.isActor() || !skill || !DataManager.isSkill(skill)) return "";
        const rk = Rank.skillRk(skill);
        if (!rk) return "";
        const parts = [];
        const stat = Rank.skillStat(skill, actor);
        const wr = actor.rkSkillRank(skill);
        const mastery = Rank.isMasterySkill(skill);
        const mr = mastery ? actor.rkMasteryRank(skill.id) : wr;
        if (mastery) {
            const need = actor.rkMasteryNeed(skill.id);
            let m = "Mastery \\RK[" + mr + "]";
            if (need === Infinity) m += "max";
            else if (Rank.P.breakthrough && actor.rkIsBarFull(skill.id)) {
                m += "\\C[17]full: finish a rank " + Rank.letter(mr + 1) + " foe\\C[0]";
            } else m += actor.rkMasteryExp(skill.id) + "/" + need;
            parts.push(m);
        } else {
            parts.push("Rank \\RK[" + wr + "]");
        }
        // a skill never works above the grade of its stat
        if (mastery && wr < mr) parts.push("\\C[2]works at\\C[0] \\RK[" + wr + "]" + "(" + stat + " grade)");
        else parts.push(stat);
        const pw = Rank.skillPowerRange(actor, skill);
        if (pw) {
            let s = (pw.heal ? "Heal " : "Power ") + (pw.lo === pw.hi ? pw.lo : pw.lo + "-" + pw.hi);
            if (pw.hits > 1) s += " x" + pw.hits;
            if (pw.each) s += " each";
            parts.push(s);
        }
        return "\\FS[21]" + parts.join("  ·  ");
    };

    Rank.skillHelpText = function(actor, skill, lines) {
        const desc = String(skill.description || "");
        const info = Rank.skillInfoLine(actor, skill);
        if (!info) return desc;
        const keep = desc.split("\n").slice(0, Math.max(1, lines - 1));
        while (keep.length > 0 && keep[keep.length - 1].trim() === "") keep.pop();
        return (keep.length ? keep.join("\n") + "\n" : "") + info;
    };

    //-------------------------------------------------------------------------
    // Drawing helpers
    //-------------------------------------------------------------------------
    Window_Base.prototype.rkDrawBar = function(x, y, width, height, rate, color1, color2) {
        if (width <= 0) return;
        const r = Rank.clamp(rate, 0, 1);
        this.contents.fillRect(x, y, width, height, ColorManager.gaugeBackColor());
        const fw = Math.floor(width * r);
        if (fw > 0) this.contents.gradientFillRect(x, y, fw, height, color1, color2 || color1);
    };

    Window_Base.prototype.rkLabelValue = function(label, value, x, y, width, valueColor) {
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(label, x, y, width);
        this.changeTextColor(valueColor || ColorManager.normalColor());
        this.drawText(value, x, y, width, "right");
        this.resetTextColor();
    };

    Window_Base.prototype.rkBadgeY = function(y, rowHeight, h) {
        return y + Math.floor(((rowHeight || this.lineHeight()) - h) / 2);
    };

    //-------------------------------------------------------------------------
    // Level lines get a rank badge
    //-------------------------------------------------------------------------
    const _Window_StatusBase_drawActorLevel = Window_StatusBase.prototype.drawActorLevel;
    Window_StatusBase.prototype.drawActorLevel = function(actor, x, y) {
        _Window_StatusBase_drawActorLevel.call(this, actor, x, y);
        const h = this.rkBadgeHeight();
        this.rkDrawRankBadge(actor.rkRank(), x + 128, this.rkBadgeY(y, null, h), h);
    };

    //-------------------------------------------------------------------------
    // Battle faces get a rank badge
    //-------------------------------------------------------------------------
    const _Window_BattleStatus_drawItemStatus = Window_BattleStatus.prototype.drawItemStatus;
    Window_BattleStatus.prototype.drawItemStatus = function(index) {
        _Window_BattleStatus_drawItemStatus.call(this, index);
        const actor = this.actor(index);
        if (!MP.battleBadges || !actor) return;
        const rect = this.itemRectWithPadding(index);
        this.rkDrawRankBadge(actor.rkRank(), rect.x, rect.y + 4, 20);
    };

    //-------------------------------------------------------------------------
    // Status screen
    //-------------------------------------------------------------------------
    Scene_Status.prototype.statusParamsWidth = function() {
        return Math.min(456, Math.floor(Graphics.boxWidth * 0.56));
    };

    Scene_Status.prototype.statusParamsHeight = function() {
        return this.calcWindowHeight(7, false);
    };

    Window_Status.prototype.drawBlock1 = function() {
        const a = this._actor;
        const y = this.block1Y();
        this.drawActorName(a, 6, y, 168);
        this.drawActorClass(a, 192, y, 168);
        const r = a.rkRank();
        const h = this.rkBadgeHeight();
        const bw = this.rkDrawRankBadge(r, 378, this.rkBadgeY(y, null, h), h);
        this.changeTextColor(Rank.color(r));
        this.drawText(Rank.title(r), 378 + bw + 8, y, 170);
        this.resetTextColor();
        const nx = 570;
        if (a.nickname()) this.drawText(a.nickname(), nx, y, this.innerWidth - nx - 6, "right");
    };

    // block 2 starts right under the name line; the face is trimmed to fit
    Window_Status.prototype.block2Y = function() {
        return this.lineHeight();
    };

    Window_Status.prototype.drawBlock2 = function() {
        const y = this.block2Y();
        const faceH = Math.min(ImageManager.standardFaceHeight, this.innerHeight - y);
        this.drawActorFace(this._actor, 12, y, ImageManager.standardFaceWidth, faceH);
        this.drawBasicInfo(204, y);
        this.drawExpInfo(456, y);
    };

    Window_Status.prototype.drawExpInfo = function(x, y) {
        const a = this._actor;
        const lh = this.lineHeight();
        const w = Math.min(336, this.innerWidth - x - 6);
        this.rkLabelValue(TextManager.expTotal.format(TextManager.exp), this.expTotalValue(), x, y, w);
        this.rkLabelValue(TextManager.expNext.format(TextManager.level), this.expNextValue(), x, y + lh, w);
        const pts = a.rkPoints();
        this.rkLabelValue(MP.pointsLabel, pts, x, y + lh * 2, w, pts > 0 ? ColorManager.powerUpColor() : null);
        const c = Rank.combatInfo(a);
        const colW = Math.floor(w / 3);
        this.contents.fontSize = 22;
        this.rkLabelValue("AC", c.ac, x, y + lh * 3, colW - 14);
        this.rkLabelValue("Hit", signed(c.hit), x + colW, y + lh * 3, colW - 14);
        this.rkLabelValue("Crit", c.critText, x + colW * 2, y + lh * 3, w - colW * 2);
        this.resetFontSettings();
    };

    Window_StatusParams.prototype.maxItems = function() {
        return 7;
    };

    Window_StatusParams.prototype.drawItem = function(index) {
        const a = this._actor;
        if (!a) return;
        const rect = this.itemLineRect(index);
        const x = rect.x;
        const y = rect.y;
        const v = a.rkStat(index);
        const base = a.rkBaseStat(index);
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(Rank.STATS[index], x, y, 48);
        this.changeTextColor(ColorManager.paramchangeTextColor(v - base));
        this.drawText(v, x + 48, y, 52, "right");
        const h = this.rkBadgeHeight();
        this.rkDrawRankBadge(Rank.ofValue(v), x + 110, this.rkBadgeY(y, rect.height, h), h);
        this.contents.fontSize = 20;
        this.changeTextColor(ColorManager.systemColor());
        this.drawText("MOD", x + 160, y, 50);
        this.drawText("POW", x + 256, y, 50);
        this.drawText("Apt", x + 356, y, 50);
        this.resetTextColor();
        this.drawText(signed(Rank.mod(v)), x + 196, y, 50, "right");
        this.drawText(Rank.pow(v), x + 290, y, 54, "right");
        this.drawText(Rank.aptitudeLetter(a.rkAptitude()[index]), x + 356, y, Math.max(20, rect.width - 356), "right");
        this.resetFontSettings();
    };

    Window_StatusEquip.prototype.drawItem = function(index) {
        const rect = this.itemLineRect(index);
        const equips = this._actor.equips();
        const item = equips[index];
        const slotName = this.actorSlotName(this._actor, index);
        const sw = Math.min(138, Math.floor(rect.width * 0.34));
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(slotName, rect.x, rect.y, sw, rect.height);
        this.drawItemName(item, rect.x + sw, rect.y, rect.width - sw);
    };

    Window_StatusEquip.prototype.refresh = function() {
        Window_StatusBase.prototype.refresh.call(this);
        if (this._actor) this.rkDrawCombatSummary();
    };

    Window_StatusEquip.prototype.rkDrawCombatSummary = function() {
        const lh = this.lineHeight();
        const rows = Math.floor(this.innerHeight / lh);
        if (this.maxItems() > rows - 2) return;
        const a = this._actor;
        const x = this.itemPadding() + 4;
        const w = this.innerWidth - x * 2;
        const y = (rows - 2) * lh;
        this.contents.paintOpacity = 64;
        this.contents.fillRect(x, y, w, 2, ColorManager.normalColor());
        this.contents.paintOpacity = 255;
        const c = Rank.combatInfo(a);
        this.rkLabelValue("Attack", Rank.diceText(c.dice) + " + " + c.flat + "  (" + c.stat + ")", x, y + 2, w);
        const trained = Rank.STATS.filter(s => a.rkIsTrainedSave(s));
        const bonus = Rank.BP ? Rank.BP.trainedSave : 3;
        this.rkLabelValue("Saves", trained.length ? trained.join(" ") + "  (+" + bonus + ")" : "-", x, y + lh, w);
    };

    //-------------------------------------------------------------------------
    // Skill lists: mastery badge + bar, scaled cost, info line in the help
    //-------------------------------------------------------------------------
    Window_SkillList.prototype.costWidth = function() {
        return this.textWidth("0000");
    };

    const _Window_SkillList_drawItem = Window_SkillList.prototype.drawItem;
    Window_SkillList.prototype.drawItem = function(index) {
        const skill = this.itemAt(index);
        const actor = this._actor;
        if (!skill || !actor || !actor.isActor() || !Rank.isMasterySkill(skill)) {
            _Window_SkillList_drawItem.call(this, index);
            return;
        }
        const rect = this.itemLineRect(index);
        const costWidth = this.costWidth();
        const mr = actor.rkMasteryRank(skill.id);
        const wr = actor.rkSkillRank(skill);
        const bh = 20;
        const bw = this.rkBadgeWidth(mr, bh);
        const nameW = rect.width - costWidth - bw - 12;
        this.changePaintOpacity(this.isEnabled(skill));
        this.drawItemName(skill, rect.x, rect.y, nameW);
        this.rkDrawRankBadge(mr, rect.x + rect.width - costWidth - bw - 6, this.rkBadgeY(rect.y, rect.height, bh), bh, wr < mr);
        this.drawSkillCost(skill, rect.x, rect.y, rect.width);
        // mastery bar under the name
        const need = actor.rkMasteryNeed(skill.id);
        const full = need !== Infinity && actor.rkMasteryExp(skill.id) >= need;
        const rate = need === Infinity ? 1 : actor.rkMasteryExp(skill.id) / need;
        const bx = rect.x + ImageManager.standardIconWidth + 4;
        const barW = nameW - (bx - rect.x) - 4;
        const col = need === Infinity ? Rank.color(mr) : full ? ColorManager.crisisColor() : Rank.color(mr);
        this.rkDrawBar(bx, rect.y + rect.height - 5, barW, 3, rate, col, col);
        this.changePaintOpacity(true);
    };

    Window_SkillList.prototype.updateHelp = function() {
        const skill = this.item();
        const hw = this._helpWindow;
        if (hw && skill && this._actor && this._actor.isActor()) {
            const lines = Math.max(1, Math.floor(hw.innerHeight / hw.lineHeight()));
            hw.setText(lines >= 2 ? Rank.skillHelpText(this._actor, skill, lines) : skill.description);
        } else {
            this.setHelpWindowItem(skill);
        }
    };

    Scene_Skill.prototype.helpAreaHeight = function() {
        return this.calcWindowHeight(MP.helpLines, false);
    };

    //-------------------------------------------------------------------------
    // Equip screen: stats, pools, AC, attack die before -> after
    //-------------------------------------------------------------------------
    Window_EquipStatus.prototype.paramWidth = function() {
        return 60;
    };

    Window_EquipStatus.prototype.rkRows = function() {
        const rows = [];
        for (let i = 0; i < 7; i++) rows.push({ label: Rank.STATS[i], get: a => a.rkStat(i) });
        rows.push({ label: TextManager.param(0), get: a => a.mhp });
        rows.push({ label: TextManager.param(1), get: a => a.mmp });
        rows.push({ label: "AC", get: a => a.rkAC() });
        rows.push({ label: "Attack", get: a => Rank.attackAverage(a), show: a => Rank.diceText(a.rkAttackDice()) });
        return rows;
    };

    Window_EquipStatus.prototype.refresh = function() {
        this.contents.clear();
        const a = this._actor;
        if (!a) return;
        const lh = this.lineHeight();
        const x = this.itemPadding();
        const w = this.innerWidth - x * 2;
        const r = a.rkRank();
        const h = this.rkBadgeHeight();
        const bw = this.rkBadgeWidth(r, h);
        this.drawActorName(a, x, 0, w - bw - 8);
        this.rkDrawRankBadge(r, x + w - bw, this.rkBadgeY(0, lh, h), h);
        const rows = this.rkRows();
        const avail = Math.floor(this.innerHeight / lh) - 1;
        rows.slice(0, avail).forEach((row, i) => this.rkDrawCompareRow(row, x, lh * (i + 1)));
    };

    Window_EquipStatus.prototype.rkDrawCompareRow = function(row, x, y) {
        const a = this._actor;
        const t = this._tempActor;
        const paramX = this.paramX();
        const pw = this.paramWidth();
        const aw = this.rightArrowWidth();
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(row.label, x, y, paramX - x - 4);
        const cur = row.get(a);
        this.resetTextColor();
        this.drawText(row.show ? row.show(a) : cur, paramX, y, pw, "right");
        this.drawRightArrow(paramX + pw, y);
        if (t) {
            const nv = row.get(t);
            this.changeTextColor(ColorManager.paramchangeTextColor(nv - cur));
            this.drawText(row.show ? row.show(t) : nv, paramX + pw + aw, y, pw, "right");
        }
    };

    //-------------------------------------------------------------------------
    // Shop: damage / AC change
    //-------------------------------------------------------------------------
    Window_ShopStatus.prototype.drawActorParamChange = function(x, y, actor, item1) {
        const width = this.innerWidth - this.itemPadding() - x;
        const slots = actor.equipSlots();
        const equips = actor.equips();
        let slotIndex = -1;
        for (let i = 0; i < slots.length; i++) {
            if (slots[i] === this._item.etypeId && equips[i] === item1) {
                slotIndex = i;
                break;
            }
        }
        if (slotIndex < 0) slotIndex = slots.indexOf(this._item.etypeId);
        if (slotIndex < 0) return;
        const temp = JsonEx.makeDeepCopy(actor);
        temp.forceChangeEquip(slotIndex, this._item);
        let diff;
        let label;
        if (DataManager.isWeapon(this._item)) {
            diff = Math.round((Rank.attackAverage(temp) - Rank.attackAverage(actor)) * 10) / 10;
            label = Rank.diceText(temp.rkAttackDice()) + "  " + signed(diff);
        } else {
            diff = temp.rkAC() - actor.rkAC();
            label = "AC " + signed(diff);
        }
        this.changeTextColor(ColorManager.paramchangeTextColor(diff));
        this.drawText(label, x, y, width, "right");
    };

    //-------------------------------------------------------------------------
    // Main menu command
    //-------------------------------------------------------------------------
    const _Window_MenuCommand_addOriginalCommands = Window_MenuCommand.prototype.addOriginalCommands;
    Window_MenuCommand.prototype.addOriginalCommands = function() {
        _Window_MenuCommand_addOriginalCommands.call(this);
        if (MP.statCommand) this.addCommand(MP.statCommand, "rkStats", this.areMainCommandsEnabled());
    };

    const _Window_MenuCommand_drawItem = Window_MenuCommand.prototype.drawItem;
    Window_MenuCommand.prototype.drawItem = function(index) {
        _Window_MenuCommand_drawItem.call(this, index);
        if (this.commandSymbol(index) !== "rkStats") return;
        const total = $gameParty.members().reduce((s, a) => s + a.rkPoints(), 0);
        if (total <= 0) return;
        const rect = this.itemLineRect(index);
        this.contents.fontSize = 18;
        this.changeTextColor(ColorManager.powerUpColor());
        this.drawText(total, rect.x, rect.y, rect.width, "right");
        this.resetFontSettings();
    };

    const _Scene_Menu_createCommandWindow = Scene_Menu.prototype.createCommandWindow;
    Scene_Menu.prototype.createCommandWindow = function() {
        _Scene_Menu_createCommandWindow.call(this);
        this._commandWindow.setHandler("rkStats", this.commandPersonal.bind(this));
    };

    const _Scene_Menu_onPersonalOk = Scene_Menu.prototype.onPersonalOk;
    Scene_Menu.prototype.onPersonalOk = function() {
        if (this._commandWindow.currentSymbol() === "rkStats") SceneManager.push(Scene_RankStats);
        else _Scene_Menu_onPersonalOk.call(this);
    };

    //-------------------------------------------------------------------------
    // Stat point screen
    //-------------------------------------------------------------------------
    function Window_RankStatList() {
        this.initialize(...arguments);
    }

    Window_RankStatList.prototype = Object.create(Window_Selectable.prototype);
    Window_RankStatList.prototype.constructor = Window_RankStatList;

    Window_RankStatList.prototype.initialize = function(rect) {
        Window_Selectable.prototype.initialize.call(this, rect);
        this._actor = null;
        this._preview = null;
        this._pending = [0, 0, 0, 0, 0, 0, 0];
        this._statusWindow = null;
        this._canRepeat = true;
    };

    Window_RankStatList.prototype.maxItems = function() {
        return 9; // 7 stats, Confirm, Reset
    };

    Window_RankStatList.prototype.setStatusWindow = function(w) {
        this._statusWindow = w;
    };

    Window_RankStatList.prototype.setActor = function(actor) {
        this._actor = actor;
        this.clearPending();
    };

    Window_RankStatList.prototype.preview = function() {
        return this._preview;
    };

    Window_RankStatList.prototype.pendingTotal = function() {
        return this._pending.reduce((s, v) => s + v, 0);
    };

    Window_RankStatList.prototype.clearPending = function() {
        this._pending = [0, 0, 0, 0, 0, 0, 0];
        this._preview = this._actor ? JsonEx.makeDeepCopy(this._actor) : null;
        this.refreshAll();
    };

    Window_RankStatList.prototype.refreshAll = function() {
        this.refresh();
        if (this._statusWindow) this._statusWindow.setData(this._actor, this._preview, this.pendingTotal());
        this.callUpdateHelp();
    };

    Window_RankStatList.prototype.canIncrease = function(i) {
        const p = this._preview;
        return !!p && p.rkPoints() > 0 && p.rkRoomFor(i) > 0;
    };

    Window_RankStatList.prototype.bump = function(i, n) {
        const p = this._preview;
        p.rkArr("_rkAlloc")[i] += n;
        p._rkPoints = (p._rkPoints || 0) - n;
        this._pending[i] += n;
    };

    Window_RankStatList.prototype.changeStat = function(i, n) {
        if (!this._preview) return 0;
        let done = 0;
        if (n > 0) {
            while (done < n && this.canIncrease(i)) {
                this.bump(i, 1);
                done++;
            }
        } else {
            while (done < -n && this._pending[i] > 0) {
                this.bump(i, -1);
                done++;
            }
            if (done > 0) this.enforceCaps();
        }
        if (done > 0) this.refreshAll();
        return done;
    };

    // taking points back can lower the rank (and the cap) under other stats
    Window_RankStatList.prototype.enforceCaps = function() {
        const p = this._preview;
        let changed = true;
        while (changed) {
            changed = false;
            for (let j = 0; j < 7; j++) {
                while (this._pending[j] > 0 && p.rkBaseStat(j) > p.rkStatCap(j)) {
                    this.bump(j, -1);
                    changed = true;
                }
            }
        }
    };

    Window_RankStatList.prototype.confirm = function() {
        const a = this._actor;
        if (!a) return;
        const rest = this._pending.slice();
        let progress = true;
        // several passes: a rank gained from one stat can lift another's cap
        while (progress) {
            progress = false;
            for (let i = 0; i < 7; i++) {
                if (rest[i] > 0) {
                    const n = a.rkAllocate(i, rest[i]);
                    if (n > 0) {
                        rest[i] -= n;
                        progress = true;
                    }
                }
            }
        }
        this.clearPending();
    };

    Window_RankStatList.prototype.step = function() {
        return Input.isPressed("shift") ? 10 : 1;
    };

    Window_RankStatList.prototype.isCurrentItemEnabled = function() {
        const i = this.index();
        if (i >= 0 && i < 7) return this.canIncrease(i);
        return this.pendingTotal() > 0;
    };

    Window_RankStatList.prototype.playChange = function(ok) {
        if (ok) this.playCursorSound();
        else this.playBuzzerSound();
    };

    Window_RankStatList.prototype.processCursorMove = function() {
        const i = this.index();
        if (this.isCursorMovable() && i >= 0 && i < 7) {
            if (Input.isRepeated("right")) {
                this.playChange(this.changeStat(i, this.step()) > 0);
                return;
            }
            if (Input.isRepeated("left")) {
                this.playChange(this.changeStat(i, -this.step()) > 0);
                return;
            }
        }
        Window_Selectable.prototype.processCursorMove.call(this);
    };

    Window_RankStatList.prototype.processOk = function() {
        const i = this.index();
        if (i >= 0 && i < 7) {
            this.playChange(this.changeStat(i, this.step()) > 0);
            return;
        }
        Window_Selectable.prototype.processOk.call(this);
    };

    Window_RankStatList.prototype.drawItem = function(index) {
        const rect = this.itemLineRect(index);
        if (index >= 7) {
            this.resetTextColor();
            this.changePaintOpacity(this.pendingTotal() > 0);
            this.drawText(index === 7 ? MP.confirmText : MP.resetText, rect.x, rect.y, rect.width, "center");
            this.changePaintOpacity(true);
            return;
        }
        const a = this._actor;
        const p = this._preview;
        if (!a || !p) return;
        const x = rect.x;
        const y = rect.y;
        const cur = a.rkBaseStat(index);
        const nv = p.rkBaseStat(index);
        const pend = this._pending[index];
        const full = p.rkRoomFor(index) <= 0;
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(Rank.STATS[index], x, y, 52);
        this.resetTextColor();
        this.drawText(cur, x + 50, y, 50, "right");
        if (pend > 0) {
            this.contents.fontSize = 20;
            this.changeTextColor(ColorManager.powerUpColor());
            this.drawText("+" + pend, x + 106, y, 50);
            this.resetFontSettings();
        }
        this.changeTextColor(ColorManager.systemColor());
        this.drawText("→", x + 158, y, 26, "center");
        this.changeTextColor(pend > 0 ? ColorManager.powerUpColor() : full ? ColorManager.crisisColor() : ColorManager.normalColor());
        this.drawText(nv, x + 184, y, 50, "right");
        const h = this.rkBadgeHeight();
        this.rkDrawRankBadge(Rank.ofValue(nv), x + 242, this.rkBadgeY(y, rect.height, h), h);
        this.contents.fontSize = 20;
        this.changeTextColor(ColorManager.systemColor());
        this.drawText("MOD", x + 290, y, 44);
        this.drawText("POW", x + 374, y, 44);
        this.resetTextColor();
        this.drawText(signed(Rank.mod(nv)), x + 326, y, 36, "right");
        this.drawText(Rank.pow(nv), x + 412, y, Math.max(30, rect.width - 412), "right");
        this.resetFontSettings();
    };

    Window_RankStatList.prototype.updateHelp = function() {
        const hw = this._helpWindow;
        if (!hw) return;
        const i = this.index();
        const p = this._preview;
        if (i >= 0 && i < 7) {
            const s = Rank.STATS[i];
            let line2 = "\\FS[20]";
            if (p) {
                line2 += "Cap " + p.rkStatCap(i) + " at rank " + Rank.letter(p.rkRank());
                if (p.rkRoomFor(i) <= 0) line2 += " (reached: raise your rank)";
                line2 += "   ·   Right/OK +1   Left -1   Shift x10";
            }
            hw.setText("\\FS[22]" + Rank.STAT_NAMES[s] + ": " + (Rank.STAT_HINTS[s] || "") + "\n" + line2);
        } else if (i === 7) {
            hw.setText("Spend the assigned points.\n\\FS[21]Confirmed points stay assigned.");
        } else if (i === 8) {
            hw.setText("Take back every point assigned on this screen.");
        } else {
            hw.setText("");
        }
    };

    function Window_RankStatStatus() {
        this.initialize(...arguments);
    }

    Window_RankStatStatus.prototype = Object.create(Window_StatusBase.prototype);
    Window_RankStatStatus.prototype.constructor = Window_RankStatStatus;

    Window_RankStatStatus.prototype.initialize = function(rect) {
        Window_StatusBase.prototype.initialize.call(this, rect);
        this._actor = null;
        this._preview = null;
        this._pending = 0;
    };

    Window_RankStatStatus.prototype.setData = function(actor, preview, pending) {
        this._actor = actor;
        this._preview = preview;
        this._pending = pending;
        this.refresh();
    };

    Window_RankStatStatus.prototype.refresh = function() {
        Window_StatusBase.prototype.refresh.call(this);
        const a = this._actor;
        if (!a) return;
        const p = this._preview || a;
        const x = this.itemPadding();
        const w = this.innerWidth - x * 2;
        const lh = this.lineHeight();
        let y = 0;
        this.drawActorName(a, x, y, w);
        y += lh;
        this.drawActorClass(a, x, y, w);
        y += lh;
        this.drawActorLevel(a, x, y);
        y += lh;
        const r1 = a.rkRank();
        const r2 = p.rkRank();
        let rankText = "\\RK[" + r1 + "]" + Rank.title(r1);
        if (r2 !== r1) rankText = "\\RK[" + r1 + "]\\C[16]→\\C[0] \\RK[" + r2 + "]\\C[24]" + Rank.title(r2) + "\\C[0]";
        this.drawTextEx(rankText, x, y, w);
        y += lh + 8;
        const pts = p.rkPoints();
        this.rkLabelValue(MP.pointsLabel, pts, x, y, w, pts > 0 ? ColorManager.powerUpColor() : null);
        y += lh;
        this.rkCompare(TextManager.param(0), a.mhp, p.mhp, x, y, w);
        y += lh;
        this.rkCompare(TextManager.param(1), a.mmp, p.mmp, x, y, w);
        y += lh;
        this.rkCompare("AC", a.rkAC(), p.rkAC(), x, y, w);
        y += lh;
        this.rkCompare("Stat cap", a.rkStatCap(0), p.rkStatCap(0), x, y, w);
        y += lh + 8;
        this.contents.fontSize = 18;
        this.changeTextColor(ColorManager.systemColor());
        const hints = ["Right / OK  +1     Left  -1", "Hold Shift  x10", "Q / W  other member", "Cancel  undo, then leave"];
        for (const line of hints) {
            if (y + 24 > this.innerHeight) break;
            this.drawText(line, x, y, w);
            y += 24;
        }
        this.resetFontSettings();
    };

    Window_RankStatStatus.prototype.rkCompare = function(label, before, after, x, y, w) {
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(label, x, y, w);
        if (after !== before) {
            const aw = 56;
            this.resetTextColor();
            this.drawText(before, x, y, w - aw - 28, "right");
            this.changeTextColor(ColorManager.systemColor());
            this.drawText("→", x + w - aw - 28, y, 28, "center");
            this.changeTextColor(ColorManager.paramchangeTextColor(after - before));
            this.drawText(after, x + w - aw, y, aw, "right");
        } else {
            this.resetTextColor();
            this.drawText(before, x, y, w, "right");
        }
        this.resetTextColor();
    };

    function Scene_RankStats() {
        this.initialize(...arguments);
    }

    Scene_RankStats.prototype = Object.create(Scene_MenuBase.prototype);
    Scene_RankStats.prototype.constructor = Scene_RankStats;

    Scene_RankStats.prototype.initialize = function() {
        Scene_MenuBase.prototype.initialize.call(this);
    };

    Scene_RankStats.prototype.create = function() {
        Scene_MenuBase.prototype.create.call(this);
        this.createHelpWindow();
        this.createStatusWindow();
        this.createListWindow();
        this.refreshActor();
    };

    Scene_RankStats.prototype.statusWidth = function() {
        return 300;
    };

    Scene_RankStats.prototype.createStatusWindow = function() {
        const rect = new Rectangle(0, this.mainAreaTop(), this.statusWidth(), this.mainAreaHeight());
        this._statusWindow = new Window_RankStatStatus(rect);
        this.addWindow(this._statusWindow);
    };

    Scene_RankStats.prototype.createListWindow = function() {
        const wx = this.statusWidth();
        const rect = new Rectangle(wx, this.mainAreaTop(), Graphics.boxWidth - wx, this.mainAreaHeight());
        const w = new Window_RankStatList(rect);
        w.setHelpWindow(this._helpWindow);
        w.setStatusWindow(this._statusWindow);
        w.setHandler("ok", this.onListOk.bind(this));
        w.setHandler("cancel", this.onListCancel.bind(this));
        w.setHandler("pagedown", this.nextActor.bind(this));
        w.setHandler("pageup", this.previousActor.bind(this));
        this.addWindow(w);
        this._listWindow = w;
    };

    Scene_RankStats.prototype.needsPageButtons = function() {
        return true;
    };

    Scene_RankStats.prototype.refreshActor = function() {
        const w = this._listWindow;
        w.setActor(this.actor());
        w.activate();
        if (w.index() < 0) w.select(0);
    };

    Scene_RankStats.prototype.onActorChange = function() {
        Scene_MenuBase.prototype.onActorChange.call(this);
        this.refreshActor();
    };

    Scene_RankStats.prototype.onListOk = function() {
        const w = this._listWindow;
        if (w.index() === 7) {
            w.confirm();
            SoundManager.playEquip();
        } else if (w.index() === 8) {
            w.clearPending();
        }
        w.activate();
    };

    Scene_RankStats.prototype.onListCancel = function() {
        const w = this._listWindow;
        if (w.pendingTotal() > 0) {
            w.clearPending();
            w.activate();
        } else {
            this.popScene();
        }
    };

    window.Window_RankStatList = Window_RankStatList;
    window.Window_RankStatStatus = Window_RankStatStatus;
    window.Scene_RankStats = Scene_RankStats;

    PluginManager.registerCommand(PLUGIN, "OpenStatPoints", args => {
        const id = Number(args.actorId) || 0;
        const actor = id > 0 ? $gameActors.actor(id) : $gameParty.leader();
        if (actor) $gameParty.setMenuActor(actor);
        SceneManager.push(Scene_RankStats);
    });
})();
