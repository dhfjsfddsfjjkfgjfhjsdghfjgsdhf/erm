//=============================================================================
// Rank_Maps.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [v1.0] Rank maps: area ranks, encounter grace + ramp, weak troops back off, area HUD.
 * @author Ten & Claude
 * @base Rank_Core
 * @orderAfter Rank_Menus
 *
 * @help Rank_Maps.js
 *
 * ENCOUNTERS
 *   A map's "Encounter Steps" stays the average distance between fights, but
 *   the spacing is fairer than MZ's pure dice:
 *   - after a fight or a map change you get a grace distance with no fights
 *     (Encounter Grace, 40% of the steps by default);
 *   - after that the chance rises with every step until a fight starts,
 *     tuned so the average stays at the map's Encounter Steps.
 *   Bushes count double and "Encounter Half" halves, as in MZ.
 *   Troops whose best enemy is two ranks below your best party member stop
 *   attacking (they'd teach nothing). If nothing on the list can attack
 *   you, the danger gauge doesn't move.
 *
 * MAP NOTETAGS (Map Properties > Note)
 *   <Rank: E>                   area rank (HUD badge, \RKM)
 *   <Region 5 Rank: D>          region 5 of this map is rank D
 *   <Safe Regions: 1, 2>        no encounter progress on these regions
 *   <Region 3 Encounter: 150%>  encounter progress x1.5 on region 3
 *   <Encounter Grace: 30%>      grace for this map
 *   <Area Name: Old Road>       HUD name (default: the map's Display Name)
 *   <No Rank HUD>               no HUD on this map
 *
 * HUD (top right): area name, area rank badge, danger gauge. The name turns
 *   yellow when the area is a rank above your best member, red at two.
 *
 * Text code:  \RKM   badge of the current area rank
 * Script:     Rank.areaRank()  Rank.partyRank()  $gamePlayer.rkDanger()
 *
 * @param Encounter Grace
 * @desc Share of the map's Encounter Steps walked without any fight (0-0.9).
 * @type number
 * @decimals 2
 * @min 0
 * @max 0.9
 * @default 0.40
 *
 * @param Skip Weak Troops
 * @desc Troops this many ranks below the party's best member don't attack.
 * @type boolean
 * @default true
 *
 * @param Weak Troop Gap
 * @type number
 * @min 1
 * @default 2
 *
 * @param Show HUD
 * @type boolean
 * @default true
 *
 * @param HUD Width
 * @type number
 * @min 160
 * @default 280
 *
 * @param Danger SE
 * @desc Sound when a fight becomes due (empty = none).
 * @type file
 * @dir audio/se/
 * @default
 *
 * @param Danger SE Volume
 * @type number
 * @default 60
 *
 * @command SetHud
 * @text Show / Hide HUD
 * @arg visible
 * @type boolean
 * @default true
 *
 * @command ResetDanger
 * @text Reset Danger
 * @desc Starts a fresh grace distance (e.g. after a rest).
 *
 * @command SetEncounterRate
 * @text Set Encounter Rate
 * @desc Multiplies all encounter progress (100 = normal, 0 = none).
 * @arg rate
 * @type number
 * @min 0
 * @default 100
 */

(() => {
    "use strict";
    const PLUGIN = "Rank_Maps";
    const P = PluginManager.parameters(PLUGIN) || {};
    const Rank = window.Rank;
    if (!Rank) throw new Error("Rank_Maps needs Rank_Core above it in the plugin list.");
    const has = v => v !== undefined && v !== null && String(v).trim() !== "";
    const num = (v, d) => (has(v) && !isNaN(Number(v)) ? Number(v) : d);
    const bool = (v, d) => (has(v) ? String(v).trim() === "true" : d);

    const MAPP = (Rank.MapP = {
        grace: Rank.clamp(num(P["Encounter Grace"], 0.4), 0, 0.9),
        skipWeak: bool(P["Skip Weak Troops"], true),
        weakGap: Math.max(1, num(P["Weak Troop Gap"], 2)),
        hud: bool(P["Show HUD"], true),
        hudWidth: Math.max(160, num(P["HUD Width"], 280)),
        dangerSe: has(P["Danger SE"]) ? String(P["Danger SE"]) : "",
        dangerSeVolume: num(P["Danger SE Volume"], 60)
    });

    //-------------------------------------------------------------------------
    // Map notes
    //-------------------------------------------------------------------------
    const pctOrRate = (value, percent) => (percent ? Number(value) / 100 : Number(value));

    Rank.parseMapNote = function(map) {
        const note = String((map && map.note) || "");
        const out = { rank: null, regionRanks: {}, safe: [], regionRates: {}, grace: null, name: null, noHud: false };
        let m = note.match(/<\s*Rank\s*:\s*([^>]+)>/i);
        if (m) out.rank = Rank.parseRank(m[1]);
        let re = /<\s*Region\s+(\d+)\s+Rank\s*:\s*([^>]+)>/gi;
        while ((m = re.exec(note))) {
            const r = Rank.parseRank(m[2]);
            if (r !== null) out.regionRanks[Number(m[1])] = r;
        }
        m = note.match(/<\s*Safe\s+Regions?\s*:\s*([^>]+)>/i);
        if (m) out.safe = m[1].split(/[\s,]+/).map(Number).filter(n => n > 0);
        re = /<\s*Region\s+(\d+)\s+Encounters?\s*:\s*(\d+(?:\.\d+)?)\s*(%?)\s*>/gi;
        while ((m = re.exec(note))) out.regionRates[Number(m[1])] = pctOrRate(m[2], m[3]);
        m = note.match(/<\s*Encounter\s+Grace\s*:\s*(\d+(?:\.\d+)?)\s*(%?)\s*>/i);
        if (m) out.grace = Rank.clamp(pctOrRate(m[1], m[2]), 0, 0.9);
        m = note.match(/<\s*Area\s+Name\s*:\s*([^>]+)>/i);
        if (m) out.name = m[1].trim();
        out.noHud = /<\s*No\s+Rank\s+HUD\s*>/i.test(note);
        return out;
    };

    Rank.mapData = function() {
        if (!$dataMap) return null;
        if (!$dataMap.rkMap) $dataMap.rkMap = Rank.parseMapNote($dataMap);
        return $dataMap.rkMap;
    };

    Rank.areaRank = function() {
        const d = Rank.mapData();
        if (!d) return null;
        const region = $gamePlayer ? $gamePlayer.regionId() : 0;
        if (region > 0 && d.regionRanks[region] !== undefined) return d.regionRanks[region];
        return d.rank;
    };

    Rank.partyRank = function() {
        const members = $gameParty.battleMembers();
        return members.length ? Math.max(...members.map(a => a.rkRank())) : 0;
    };

    Rank.troopRank = function(troopId) {
        const troop = $dataTroops[troopId];
        if (!troop) return 0;
        if (troop.rkRank === undefined) {
            let r = 0;
            for (const member of troop.members) {
                const e = $dataEnemies[member.enemyId];
                if (!e) continue;
                if (!e.rk) Rank.parseEnemy(e);
                r = Math.max(r, e.rk.rank);
            }
            troop.rkRank = r;
        }
        return troop.rkRank;
    };

    //-------------------------------------------------------------------------
    // Encounter ramp: grace g, then per-step chance min(1, a * steps past g),
    // with a solved so the average distance is the map's Encounter Steps.
    //-------------------------------------------------------------------------
    Rank._rampCache = {};
    Rank.encounterRamp = function(steps, grace) {
        const n = Math.max(1, steps);
        const key = n + ":" + grace.toFixed(3);
        if (Rank._rampCache[key]) return Rank._rampCache[key];
        const g = Math.floor(n * grace);
        const target = Math.max(1, n - g);
        const meanFor = a => {
            let e = 0;
            let s = 1;
            for (let k = 1; k < 100000; k++) {
                e += s;
                s *= 1 - Math.min(1, a * k);
                if (s < 1e-9) break;
            }
            return e;
        };
        let lo = 1e-7;
        let hi = 2;
        for (let i = 0; i < 60; i++) {
            const mid = Math.sqrt(lo * hi);
            if (meanFor(mid) > target) lo = mid;
            else hi = mid;
        }
        return (Rank._rampCache[key] = { n, g, a: Math.sqrt(lo * hi) });
    };

    Game_System.prototype.rkEncounterRate = function() {
        return this._rkEncounterRate === undefined ? 1 : this._rkEncounterRate;
    };

    Game_System.prototype.rkHudHidden = function() {
        return this._rkHudHidden === true;
    };

    Game_Player.prototype.rkGrace = function() {
        const d = Rank.mapData();
        return d && d.grace !== null ? d.grace : MAPP.grace;
    };

    Game_Player.prototype.rkRegionRate = function() {
        const d = Rank.mapData();
        const region = this.regionId();
        if (d && d.safe.includes(region)) return 0;
        const r = d && d.regionRates[region] !== undefined ? d.regionRates[region] : 1;
        return r * $gameSystem.rkEncounterRate();
    };

    Game_Player.prototype.rkHasEncounterHere = function() {
        return $gameMap.encounterList().some(e => $dataTroops[e.troopId] && this.meetsEncounterConditions(e));
    };

    // true when walking here moves the danger gauge
    Game_Player.prototype.rkEncounterActive = function() {
        return $gameMap.encounterStep() > 0 && this.canEncounter() && this.rkRegionRate() > 0 && this.rkHasEncounterHere();
    };

    Game_Player.prototype.rkDanger = function() {
        const n = $gameMap.encounterStep();
        return n > 0 ? (this._rkEncSteps || 0) / n : 0;
    };

    Game_Player.prototype.rkDangerStage = function() {
        const n = $gameMap.encounterStep();
        if (!(n > 0)) return 0;
        const ramp = Rank.encounterRamp(n, this.rkGrace());
        const s = this._rkEncSteps || 0;
        return s >= n ? 2 : s > ramp.g ? 1 : 0;
    };

    Game_Player.prototype.makeEncounterCount = function() {
        this._rkEncSteps = 0;
        this._rkDueSignaled = false;
        this._encounterCount = 1; // rolls set it to 0; MZ's executeEncounter does the rest
    };

    Game_Player.prototype.updateEncounterCount = function() {
        if (!this.canEncounter()) return;
        const n = $gameMap.encounterStep();
        if (!(n > 0) || !this.rkHasEncounterHere()) return;
        const v = this.encounterProgressValue() * this.rkRegionRate();
        if (v <= 0) return;
        const ramp = Rank.encounterRamp(n, this.rkGrace());
        this._rkEncSteps = (this._rkEncSteps || 0) + v;
        const over = this._rkEncSteps - ramp.g;
        if (over > 0) {
            const h = Math.min(1, ramp.a * over);
            const p = 1 - Math.pow(1 - h, v);
            if (Math.random() < p) this._encounterCount = 0;
        }
        if (!this._rkDueSignaled && this._rkEncSteps >= n) {
            this._rkDueSignaled = true;
            if (MAPP.dangerSe && this._encounterCount > 0) {
                AudioManager.playSe({ name: MAPP.dangerSe, volume: MAPP.dangerSeVolume, pitch: 100, pan: 0 });
            }
        }
    };

    const _Game_Player_meetsEncounterConditions = Game_Player.prototype.meetsEncounterConditions;
    Game_Player.prototype.meetsEncounterConditions = function(encounter) {
        if (!_Game_Player_meetsEncounterConditions.call(this, encounter)) return false;
        if (MAPP.skipWeak && Rank.troopRank(encounter.troopId) <= Rank.partyRank() - MAPP.weakGap) return false;
        return true;
    };

    //-------------------------------------------------------------------------
    // HUD
    //-------------------------------------------------------------------------
    function Window_RankHud() {
        this.initialize(...arguments);
    }

    Window_RankHud.prototype = Object.create(Window_Base.prototype);
    Window_RankHud.prototype.constructor = Window_RankHud;

    Window_RankHud.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.opacity = 0;
        this.contentsOpacity = 0;
        this._key = "";
        this.refresh();
    };

    Window_RankHud.prototype.updatePadding = function() {
        this.padding = 6;
    };

    Window_RankHud.prototype.isWanted = function() {
        if (!MAPP.hud || $gameSystem.rkHudHidden()) return false;
        const d = Rank.mapData();
        if (!d || d.noHud) return false;
        return Rank.areaRank() !== null || ($gameMap.encounterList().length > 0 && $gameMap.encounterStep() > 0);
    };

    Window_RankHud.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        const show = this.isWanted() && !$gameMessage.isBusy();
        if (show && this.contentsOpacity < 255) this.contentsOpacity += 16;
        if (!show && this.contentsOpacity > 0) this.contentsOpacity -= 32;
        if (show || this.contentsOpacity > 0) {
            const key = this.makeKey();
            if (key !== this._key) {
                this._key = key;
                this.refresh();
            }
        }
    };

    Window_RankHud.prototype.makeKey = function() {
        const d = Rank.mapData();
        return [
            $gameMap.mapId(),
            Rank.areaRank(),
            Rank.partyRank(),
            Math.floor($gamePlayer.rkDanger() * 60),
            $gamePlayer.rkEncounterActive() ? 1 : 0,
            d && d.name ? d.name : $gameMap.displayName()
        ].join("|");
    };

    Window_RankHud.prototype.refresh = function() {
        const c = this.contents;
        c.clear();
        const d = Rank.mapData();
        if (!d || !$gamePlayer) return;
        const w = this.innerWidth;
        const h = this.innerHeight;
        const fade = Math.floor(w * 0.35);
        c.gradientFillRect(0, 0, fade, h, ColorManager.dimColor2(), ColorManager.dimColor1());
        c.fillRect(fade, 0, w - fade, h, ColorManager.dimColor1());
        const rank = Rank.areaRank();
        const name = d.name || $gameMap.displayName() || "";
        let right = w - 8;
        if (rank !== null) {
            const bh = 20;
            const bw = this.rkBadgeWidth(rank, bh);
            right -= bw;
            this.rkDrawRankBadge(rank, right, 3, bh);
            right -= 8;
        }
        const pr = Rank.partyRank();
        let color = ColorManager.normalColor();
        if (rank !== null && rank >= pr + 2) color = ColorManager.deathColor();
        else if (rank !== null && rank === pr + 1) color = ColorManager.crisisColor();
        c.fontSize = 20;
        c.textColor = color;
        if (rank !== null && rank <= pr - 2) c.paintOpacity = 160;
        c.drawText(name, 8, 0, Math.max(0, right - 8), 26, "right");
        c.paintOpacity = 255;
        this.resetFontSettings();
        if ($gameMap.encounterList().length > 0 && $gameMap.encounterStep() > 0) this.drawDanger(8, 30, w - 16, 5);
    };

    Window_RankHud.prototype.drawDanger = function(x, y, width, height) {
        const c = this.contents;
        const n = $gameMap.encounterStep();
        const ramp = Rank.encounterRamp(n, $gamePlayer.rkGrace());
        const span = 1.5; // the bar covers 1.5x the average distance
        c.fillRect(x, y, width, height, ColorManager.gaugeBackColor());
        const rate = Math.min(1, $gamePlayer.rkDanger() / span);
        const stage = $gamePlayer.rkDangerStage();
        let color = stage >= 2 ? ColorManager.deathColor() : stage >= 1 ? ColorManager.crisisColor() : ColorManager.powerUpColor();
        if (!$gamePlayer.rkEncounterActive()) color = "rgba(160,160,160,0.8)";
        const fw = Math.floor(width * rate);
        if (fw > 0) c.fillRect(x, y, fw, height, color);
        const mark = x + Math.floor(width * Math.min(1, ramp.g / n / span));
        c.fillRect(mark, y - 1, 1, height + 2, "rgba(255,255,255,0.55)");
    };

    window.Window_RankHud = Window_RankHud;

    const _Scene_Map_createMapNameWindow = Scene_Map.prototype.createMapNameWindow;
    Scene_Map.prototype.createMapNameWindow = function() {
        _Scene_Map_createMapNameWindow.call(this);
        this._rkHud = new Window_RankHud(this.rkHudRect());
        this.addWindow(this._rkHud); // added before the message windows: stays under them
    };

    Scene_Map.prototype.rkHudRect = function() {
        const ww = MAPP.hudWidth;
        const wh = 50;
        const wx = Graphics.boxWidth - ww - (ConfigManager.touchUI ? 56 : 0);
        return new Rectangle(wx, 0, ww, wh);
    };

    const _Scene_Map_launchBattle = Scene_Map.prototype.launchBattle;
    Scene_Map.prototype.launchBattle = function() {
        _Scene_Map_launchBattle.call(this);
        if (this._rkHud) this._rkHud.hide();
    };

    const _Scene_Map_terminate = Scene_Map.prototype.terminate;
    Scene_Map.prototype.terminate = function() {
        if (this._rkHud) this._rkHud.hide(); // keep it out of the menu background snapshot
        _Scene_Map_terminate.call(this);
    };

    //-------------------------------------------------------------------------
    // \RKM text code -> \RK[current area rank]
    //-------------------------------------------------------------------------
    const _Window_Base_convertEscapeCharacters = Window_Base.prototype.convertEscapeCharacters;
    Window_Base.prototype.convertEscapeCharacters = function(textValue) {
        let t = _Window_Base_convertEscapeCharacters.call(this, textValue);
        t = t.replace(/\x1bRKM(\[\d*\])?/gi, () => {
            const r = $gameMap && $dataMap ? Rank.areaRank() : null;
            return r === null ? "" : "\x1bRK[" + r + "]";
        });
        return t;
    };

    //-------------------------------------------------------------------------
    // Plugin commands
    //-------------------------------------------------------------------------
    PluginManager.registerCommand(PLUGIN, "SetHud", args => {
        $gameSystem._rkHudHidden = String(args.visible) !== "true";
    });

    PluginManager.registerCommand(PLUGIN, "ResetDanger", () => {
        $gamePlayer.makeEncounterCount();
    });

    PluginManager.registerCommand(PLUGIN, "SetEncounterRate", args => {
        $gameSystem._rkEncounterRate = Math.max(0, Number(args.rate) || 0) / 100;
    });
})();
