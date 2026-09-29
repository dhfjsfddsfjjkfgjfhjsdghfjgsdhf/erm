//=============================================================================
// Story_Core.js
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [v1.0] Story systems: bound actors, breakthrough gate, rank gear, vessel revival, passives, barrier, money, calendar.
 * @author Ten & Claude
 * @base Rank_Core
 * @orderAfter Rank_Maps
 *
 * @help Story_Core.js  (load after Rank_Core, Rank_Battle, Rank_Menus, Rank_Maps)
 *
 * The story rules of Erdenkreis on top of the rank system.
 *
 * ============================================================================
 * ACTORS (Actor Note)
 * ============================================================================
 *   <Bound To: 1>        level and EXP always equal actor 1's, rank = actor
 *                        1's rank, earns no EXP of its own (Hanma)
 *   <Gated>              base stats stop at the story's breakthrough gate:
 *                        gate F: 99, E: 199 ... Natural growth above the
 *                        gate is held back and comes back on breakthrough.
 *   <Rank Weapon: F 21, E 22, D 23>   weapon slot holds this weapon at each
 *   <Rank Armor: F 31, E 32>          gate rank (lock the slot with the
 *                                     Lock Equip trait): Divine Weaponry,
 *                                     Fused Plate
 *   <Breakthrough E: 8, 9>            skills learned when the gate reaches E
 *   <Unarmed Die: d8>                 attack die with no weapon
 *   <Auto Build: CON 40, STR 35, WIS 10, CHA 10, MAG 5>
 *                        how "Auto Build" spends free stat points (weights).
 *                        Auto Build ends with Catch Up: a gated actor who
 *                        joins after a breakthrough gets its three best
 *                        stats raised to the current band, like the party.
 *
 * ============================================================================
 * SKILLS (Skill Note)
 * ============================================================================
 *   <Passive State: 30>  while known, the actor has state 30's traits and
 *                        rank bonuses (no icon, can't be removed)
 *   <Party Aura: 31>     while the actor is alive in the party, every party
 *                        member has state 31's traits
 *   <Barrier: d6 50%>    each target gains a barrier (temporary HP) of
 *                        (die + POW(stat) + 10 x working rank) x rate.
 *                        Barriers absorb damage first, don't stack (the
 *                        higher one stays) and fade after battle.
 *   <Needs Rank: D>      a gated actor learns it only once the gate has
 *                        reached D (early level skills wait for the
 *                        breakthrough)
 *   <Once Per Battle>    <Self State: 61>   <Only Demons>
 *   <Share Drain: 50%>   that share of the damage dealt heals the allies
 *   <Unbroken>           (occasion Never) once per battle: she stays at 1 HP
 *   <Hold The Line>      (occasion Never) once per ally per battle: an ally
 *                        stays at 1 HP. Both pay the skill's MP and give a
 *                        barrier of d10 + POW + 10 x rank.
 *   <General's Eye>      foes' weaknesses shown at the start of a battle
 *   <Deathwatch>         the target window shows a foe's exact HP
 *   <Swift: 17, 21>      with two actions a turn, only one may be something
 *                        other than these skills or Guard
 *   <Floating Strike>    the skill the floating armory strikes with
 *
 * STATES / PASSIVES (any trait object: states, passive states, auras, gear)
 *   <Init: +2>  <Save Bonus: +2>  <DEX Save: +2>  <Concentration>
 *   <Float Strikes: 1>   a floating strike after each of her actions
 *   <Riposte>            a foe that misses her takes a floating strike
 *   <Ring Strike>        every foe that acts takes a floating strike
 *   <Guardian Blade>     once a round a blow that lands by less than 5 on
 *                        her or an ally misses (<Guardian Blade: all>: once
 *                        per ally)
 *   <Blink>              the first hit on her each round misses
 *   <Lent Blade: d8>     attack with that die, STR or DEX, the bearer's rank
 *   <Taunted>            (on a foe) it attacks whoever applied the state
 *   <Taunt Aura>         every foe's single-target attacks come to her
 *   <Burden Share>       half of every hit goes to whoever applied it
 *   <Warded>             whoever applied it takes the hits meant for them
 *   <Interpose All>      every hostile action aimed at an ally hits her
 *   <Interpose Magic>    Interpose covers spells too
 *   <Unkillable>         can't drop below 1 HP
 *   <Rank Regen: 2%>     (rank + 1) x 2% of max HP each turn
 *   <Miasma>             counts as miasma-touched
 * ENEMIES
 *   <Demon>              the party's relics (Rank Pierce Variable) cancel a
 *                        rank of difference each, never past even
 *   <Veil of Ash>        counts as rank V until four relics are held
 *   <Miasma>             miasma-touched (Purge and <Only Demons> skills)
 *
 * STATES (State Note)
 *   <Interpose>          whoever has this state takes physical hits aimed
 *                        at the rest of the party
 * EVENTS (Event Note)
 *   <Follow Player>      the event stays on the player (for lights that
 *                        follow the party: TausiLighting "Reference Event")
 * MAPS (Map Note)
 *   <Weather: snow 5>    weather set on entering the map (none, rain, storm,
 *                        snow; power 1-9). A map without the tag is clear.
 *   <Weather: snow 5 unless 26>   clear once switch 26 is ON
 *   <Weather: keep>      leave the weather as it is
 * TAUSILIGHTING LAYERS
 *   A "Blend" layer whose image is named Ground_... (img/pictures/Ground_
 *   Eisfurt_Ice.png) is drawn on the ground: under characters and star
 *   tiles instead of over everything.
 *
 * ============================================================================
 * BREAKTHROUGH (plugin command)
 * ============================================================================
 *   Raises the gate variable by one rank. For every gated party member:
 *   the three best base stats rise to the floor of the new band, +1 level
 *   (bound actors follow their master), rank gear changes form, the
 *   <Breakthrough X> skills are learned, HP and MP are full.
 *
 * ============================================================================
 * VESSEL REVIVAL
 * ============================================================================
 *   While the Vessel switch is ON a defeat is never a game over: the party
 *   wakes at the last rest point (Set Rest Point), fully healed, a share of
 *   the money is lost, and the Revival common event runs (the Deaths
 *   variable counts deaths, Lost Money holds the amount).
 *   Party members knocked out in a won or fled battle get up with 1 HP.
 *
 * ============================================================================
 * MONEY, CALENDAR
 * ============================================================================
 *   Gold is counted in the smallest coin: 1 gk = 10 sl = 100 kl.
 *   Windows show "1 gk 2 sl 5 kl". Text code: \MONEY[125]  (\MONEY[\V[3]])
 *   The menu shows the date (12 months x 30 days) and the time of day from
 *   McKathlin_DayNight if it is installed. Text code: \DATE
 *
 * ============================================================================
 * PLUGIN COMMANDS
 * ============================================================================
 *   Breakthrough, Set Rest Point, Sync Level, Auto Build, Catch Up,
 *   Chapter Card, Vessel Revival (test)
 *
 * @param Gate Variable
 * @desc Variable holding the breakthrough gate (0 = F, 1 = E ...).
 * @type variable
 * @default 1
 *
 * @param Vessel Switch
 * @desc While ON, defeat triggers vessel revival instead of game over.
 * @type switch
 * @default 1
 *
 * @param Revival Common Event
 * @type common_event
 * @default 1
 *
 * @param Deaths Variable
 * @type variable
 * @default 2
 *
 * @param Lost Money Variable
 * @type variable
 * @default 3
 *
 * @param Money Loss
 * @desc Share of the money lost on each revival (0-1).
 * @type number
 * @decimals 2
 * @default 0.10
 *
 * @param Default Rest Map
 * @type number
 * @default 1
 *
 * @param Default Rest X
 * @type number
 * @default 0
 *
 * @param Default Rest Y
 * @type number
 * @default 0
 *
 * @param Barrier State
 * @desc State shown while a battler has a barrier (icon only).
 * @type state
 * @default 0
 *
 * @param Revive Downed
 * @text Knocked-out members get up after battle
 * @type boolean
 * @default true
 *
 * @param Currency Names
 * @desc Big, middle, small coin (10 small = 1 middle, 10 middle = 1 big).
 * @default gk,sl,kl
 *
 * @param Start Date
 * @desc Day, month, year of day 0.
 * @default 1,4,1047
 *
 * @param Month Names
 * @default Eismond,Schneemond,Taumond,Blütenmond,Grünmond,Sonnmond,Glutmond,Erntemond,Weinmond,Nebelmond,Aschmond,Nachtmond
 *
 * @param Menu Clock
 * @text Date and time in the menu
 * @type boolean
 * @default true
 *
 * @param Rank Pierce Variable
 * @desc Variable: how many rank-piercing relics the party carries (Dawn Regalia). 0 = off.
 * @type variable
 * @default 0
 *
 * @param Storm Element
 * @desc Element whose damage stops <Rank Regen> for the round.
 * @type number
 * @default 4
 *
 * @command Breakthrough
 * @text Breakthrough
 * @desc Raise the gate by one rank (see help).
 *
 * @arg silent
 * @text No messages
 * @type boolean
 * @default false
 *
 * @command SetRestPoint
 * @text Set Rest Point
 * @desc Where the party wakes after a defeat. Map 0 = here, where the player stands.
 *
 * @arg mapId
 * @type number
 * @default 0
 *
 * @arg x
 * @type number
 * @default 0
 *
 * @arg y
 * @type number
 * @default 0
 *
 * @arg direction
 * @type select
 * @option down
 * @value 2
 * @option left
 * @value 4
 * @option right
 * @value 6
 * @option up
 * @value 8
 * @default 2
 *
 * @command SyncLevel
 * @text Sync Level
 * @desc Set an actor's level to another actor's (a companion joining late).
 *
 * @arg actorId
 * @type actor
 * @default 3
 *
 * @arg sourceId
 * @text Take the level of
 * @type actor
 * @default 1
 *
 * @command AutoBuild
 * @text Auto Build
 * @desc Spend an actor's free stat points by its <Auto Build> weights, then Catch Up.
 *
 * @arg actorId
 * @type actor
 * @default 3
 *
 * @command CatchUp
 * @text Catch Up
 * @desc A gated actor who joins after a breakthrough: raise the three best stats to the current band.
 *
 * @arg actorId
 * @type actor
 * @default 3
 *
 * @command ChapterCard
 * @text Chapter Card
 * @desc Big centred title over the map (waits until it fades).
 *
 * @arg title
 * @type string
 * @default
 *
 * @arg subtitle
 * @type string
 * @default
 *
 * @arg duration
 * @type number
 * @default 180
 *
 * @command Revive
 * @text Vessel Revival (test)
 * @desc Run the vessel revival now.
 */

(() => {
    "use strict";
    const PLUGIN = "Story_Core";
    const P0 = PluginManager.parameters(PLUGIN) || {};
    const num = (v, d) => (v !== undefined && v !== "" && !isNaN(Number(v)) ? Number(v) : d);
    const Story = (window.Story = window.Story || {});

    const csvNums = s => String(s || "").split(",").map(x => Number(x.trim()));
    const startDate = csvNums(P0["Start Date"] || "1,4,1047");
    Story.P = {
        gateVar: num(P0["Gate Variable"], 1),
        vesselSwitch: num(P0["Vessel Switch"], 1),
        reviveCE: num(P0["Revival Common Event"], 1),
        deathsVar: num(P0["Deaths Variable"], 2),
        lostVar: num(P0["Lost Money Variable"], 3),
        moneyLoss: num(P0["Money Loss"], 0.1),
        restMap: num(P0["Default Rest Map"], 1),
        restX: num(P0["Default Rest X"], 0),
        restY: num(P0["Default Rest Y"], 0),
        barrierState: num(P0["Barrier State"], 0),
        reviveDowned: String(P0["Revive Downed"] || "true") === "true",
        coins: String(P0["Currency Names"] || "gk,sl,kl").split(",").map(s => s.trim()),
        startDay: startDate[0] || 1,
        startMonth: startDate[1] || 4,
        startYear: startDate[2] || 1047,
        months: String(P0["Month Names"] ||
            "Eismond,Schneemond,Taumond,Blütenmond,Grünmond,Sonnmond,Glutmond,Erntemond,Weinmond,Nebelmond,Aschmond,Nachtmond")
            .split(",").map(s => s.trim()),
        menuClock: String(P0["Menu Clock"] || "true") === "true",
        pierceVar: num(P0["Rank Pierce Variable"], 0),
        stormElement: num(P0["Storm Element"], 4)
    };
    const P = Story.P;

    //-------------------------------------------------------------------------
    // Notetag helpers (MZ fills obj.meta from <Name: value>)
    //-------------------------------------------------------------------------
    const meta = (obj, name) => {
        if (!obj || !obj.meta) return undefined;
        const v = obj.meta[name];
        return typeof v === "string" ? v.trim() : v;
    };

    // "F 21, E 22" -> {0: 21, 1: 22}
    Story.parseRankMap = function(text) {
        const out = {};
        if (!text || text === true) return out;
        for (const part of String(text).split(",")) {
            const m = part.trim().match(/^(SSS|SS|S|F|E|D|C|B|A|V)\s+(\d+)$/i);
            if (m) out[Rank.parseRank(m[1])] = Number(m[2]);
        }
        return out;
    };

    Story.pickForRank = function(map, rank) {
        let best = null;
        for (const key of Object.keys(map)) {
            const r = Number(key);
            if (r <= rank && (best === null || r > best)) best = r;
        }
        return best === null ? 0 : map[best];
    };

    //-------------------------------------------------------------------------
    // Bound actors: <Bound To: 1>
    //-------------------------------------------------------------------------
    Story.boundTo = actor => {
        const v = meta(actor && actor.actor(), "Bound To");
        return v ? Number(v) || 0 : 0;
    };

    Game_Actor.prototype.storyMaster = function() {
        const id = Story.boundTo(this);
        if (!id || id === this.actorId()) return null;
        return $gameActors.actor(id);
    };

    Story._syncing = false;
    Story.syncBound = function(master, show) {
        for (const actor of $gameActors._data) {
            if (!actor || actor === master) continue;
            if (Story.boundTo(actor) !== master.actorId()) continue;
            if (actor.currentExp() === master.currentExp()) continue;
            Story._syncing = true;
            try {
                actor.changeExp(master.currentExp(), !!show && $gameParty.members().includes(actor));
            } finally {
                Story._syncing = false;
            }
        }
    };

    const _Game_Actor_changeExp = Game_Actor.prototype.changeExp;
    Game_Actor.prototype.changeExp = function(exp, show) {
        if (this.storyMaster() && !Story._syncing) return; // bound: follows the master
        _Game_Actor_changeExp.call(this, exp, show);
        if (!Story._syncing && $gameActors && $gameActors._data) Story.syncBound(this, show);
    };

    Story._rankDepth = 0;
    const _Game_Actor_rkRank = Game_Actor.prototype.rkRank;
    Game_Actor.prototype.rkRank = function() {
        const m = this.storyMaster();
        if (m && Story._rankDepth < 3) {
            Story._rankDepth++;
            try {
                return m.rkRank();
            } finally {
                Story._rankDepth--;
            }
        }
        return _Game_Actor_rkRank.call(this);
    };

    const _Game_Party_addActor = Game_Party.prototype.addActor;
    Game_Party.prototype.addActor = function(actorId) {
        _Game_Party_addActor.call(this, actorId);
        const actor = $gameActors.actor(actorId);
        const master = actor && actor.storyMaster();
        if (master) Story.syncBound(master, false);
    };

    if (window.BattleManager && BattleManager.rkExpFor) {
        const _rkExpFor = BattleManager.rkExpFor;
        BattleManager.rkExpFor = function(actor) {
            const m = actor.storyMaster();
            return m ? _rkExpFor.call(this, m) : _rkExpFor.call(this, actor);
        };
    }

    //-------------------------------------------------------------------------
    // Breakthrough gate: <Gated>
    //-------------------------------------------------------------------------
    Story.gate = () => ($gameVariables ? $gameVariables.value(P.gateVar) || 0 : 0);
    Story.gateCap = () => Math.min(999, (Rank.clamp(Story.gate(), 0, 9) + 1) * 100 - 1);
    Story.isGated = actor => !!meta(actor && actor.actor(), "Gated");

    Game_Actor.prototype.storyGateLimited = function() {
        return Story.isGated(this);
    };

    const _Game_Actor_rkStatCap = Game_Actor.prototype.rkStatCap;
    Game_Actor.prototype.rkStatCap = function(i) {
        const c = _Game_Actor_rkStatCap.call(this, i);
        return Story.isGated(this) ? Math.min(c, Story.gateCap()) : c;
    };

    const _Game_Actor_rkBaseStat = Game_Actor.prototype.rkBaseStat;
    Game_Actor.prototype.rkBaseStat = function(i) {
        const v = _Game_Actor_rkBaseStat.call(this, i);
        return Story.isGated(this) ? Math.min(v, Story.gateCap()) : v;
    };

    // the stat screen's hint: a gated cap is lifted by the story, not by points
    if (window.Window_RankStatList) {
        const _updateHelp = Window_RankStatList.prototype.updateHelp;
        Window_RankStatList.prototype.updateHelp = function() {
            _updateHelp.call(this);
            const p = this._preview;
            const hw = this._helpWindow;
            if (!p || !hw || !Story.isGated(p) || !hw._text) return;
            if (p.rkStatCap(0) === Story.gateCap() && hw._text.includes("(reached: raise your rank)")) {
                hw.setText(hw._text.replace("(reached: raise your rank)", "(held: your next breakthrough lifts it)"));
            }
        };
    }

    //-------------------------------------------------------------------------
    // Rank gear: <Rank Weapon: F 21, E 22>  <Rank Armor: F 31, E 32>
    //-------------------------------------------------------------------------
    Game_Actor.prototype.storyGearFor = function(tag) {
        const map = Story.parseRankMap(meta(this.actor(), tag));
        return Story.pickForRank(map, Story.gate());
    };

    Story.isRankGear = item => !!(item && item.meta && (item.meta["Rank Gear"] || item.meta["DW Form"]));

    // force: a breakthrough equips the new weapon form; otherwise a chosen older form is kept
    Game_Actor.prototype.storyRefreshGear = function(force) {
        const slots = this.equipSlots();
        const put = (etypeId, item) => {
            const i = slots.indexOf(etypeId);
            if (i < 0 || !item || !this._equips[i]) return;
            const old = this._equips[i].object();
            if (old !== item) {
                // gear that isn't part of the body goes back to the bag
                if (old && !Story.isRankGear(old) && $gameParty) $gameParty.gainItem(old, 1);
                this._equips[i].setObject(item);
                this.refresh();
            }
        };
        const wmap = Story.parseRankMap(meta(this.actor(), "Rank Weapon"));
        const w = Story.pickForRank(wmap, Story.gate());
        if (w) {
            const cur = this.weapons()[0];
            const forms = Story.unlockedForms(this);
            // a form the player picked stays in hand; a breakthrough hands her the new one, unless one of
            // her other forms suits her stats clearly better (a DEX-built bearer keeps the dagger at D)
            let pick = $dataWeapons[w];
            if (force) {
                let best = null;
                for (const id of forms) {
                    const f = $dataWeapons[id];
                    if (f && f !== pick && (!best || Story.formScore(this, f) > Story.formScore(this, best))) best = f;
                }
                if (best && Story.formScore(this, best) > Story.formScore(this, pick) * 1.15) pick = best;
            }
            const keep = !force && cur && forms.includes(cur.id);
            if (!keep) put(1, pick);
            Story.grantForms(this);
        }
        const a = this.storyGearFor("Rank Armor");
        if (a && $dataArmors[a]) put($dataArmors[a].etypeId, $dataArmors[a]);
    };

    // expected damage of a weapon form in this actor's hands (die + POW of its stat, a little for accuracy)
    Story.formScore = function(actor, w) {
        if (!w) return -1;
        const rk = w.rk || {};
        const d = rk.dice || Rank.dice(1, w.params[2] || 4, 0);
        return Rank.diceAvg(d) + Rank.pow(actor.rkStat(rk.stat || "STR")) + (rk.hit || 0) + (rk.crit || 0);
    };

    // "F 1, E 2, D 3" plus extra forms "<DW Extra: D 4>" (a second shape at the same rank)
    Story.unlockedForms = function(actor) {
        const out = [];
        const add = text => {
            for (const part of String(text || "").split(",")) {
                const m = part.trim().match(/^(SSS|SS|S|F|E|D|C|B|A|V)\s+(\d+)$/i);
                if (m && Rank.parseRank(m[1]) <= Story.gate()) out.push(Number(m[2]));
            }
        };
        add(meta(actor.actor(), "Rank Weapon"));
        add(meta(actor.actor(), "DW Extra"));
        return out;
    };

    // Divine Weaponry: every form unlocked so far can be summoned (the equip screen lists them)
    Story.grantForms = function(actor) {
        if (!$gameParty || !$gameParty._weapons) return;
        for (const id of Story.unlockedForms(actor)) {
            const item = $dataWeapons[id];
            if (item && item.meta && item.meta["DW Form"] && !actor.isEquipped(item) && !$gameParty.hasItem(item, false)) {
                $gameParty._weapons[item.id] = 1;
            }
        }
    };

    // a summoned form counts as gear of the bearer's rank; plated fists hit with the bearer's rank too
    const _Game_Actor_rkWeaponRank = Game_Actor.prototype.rkWeaponRank;
    Game_Actor.prototype.rkWeaponRank = function() {
        const w = this.rkMainWeapon ? this.rkMainWeapon() : this.weapons()[0];
        if (w && w.meta && w.meta["DW Form"]) return Math.max(_Game_Actor_rkWeaponRank.call(this), Story.gate());
        if (!w && meta(this.actor(), "Unarmed Die") && Story.isGated(this)) return Story.gate();
        return _Game_Actor_rkWeaponRank.call(this);
    };

    // the weapon of light can be changed but never put away
    const _Game_Actor_changeEquip = Game_Actor.prototype.changeEquip;
    Game_Actor.prototype.changeEquip = function(slotId, item) {
        const cur = this._equips[slotId] && this._equips[slotId].object();
        if (!item && cur && cur.meta && cur.meta["DW Form"]) return;
        _Game_Actor_changeEquip.call(this, slotId, item);
    };

    const _Game_Actor_discardEquip = Game_Actor.prototype.discardEquip;
    Game_Actor.prototype.discardEquip = function(item) {
        if (item && item.meta && item.meta["DW Form"]) return;
        _Game_Actor_discardEquip.call(this, item);
    };

    Story.refreshAllGear = function(force) {
        if (!$gameActors || !$gameActors._data) return;
        for (const actor of $gameActors._data) if (actor) actor.storyRefreshGear(force);
    };

    const _Game_Actor_setup = Game_Actor.prototype.setup;
    Game_Actor.prototype.setup = function(actorId) {
        _Game_Actor_setup.call(this, actorId);
        if ($gameVariables) this.storyRefreshGear();
    };

    const _Game_Variables_setValue = Game_Variables.prototype.setValue;
    Game_Variables.prototype.setValue = function(variableId, value) {
        const before = this.value(variableId);
        _Game_Variables_setValue.call(this, variableId, value);
        if (variableId === P.gateVar && before !== this.value(variableId)) Story.refreshAllGear(true);
    };

    const _DataManager_extractSaveContents = DataManager.extractSaveContents;
    DataManager.extractSaveContents = function(contents) {
        _DataManager_extractSaveContents.call(this, contents);
        Story.refreshAllGear();
    };

    // rank gear never goes to the inventory
    const _Game_Party_gainItem = Game_Party.prototype.gainItem;
    Game_Party.prototype.gainItem = function(item, amount, includeEquip) {
        if (item && item.meta && item.meta["Rank Gear"] && amount > 0) return;
        _Game_Party_gainItem.call(this, item, amount, includeEquip);
    };

    //-------------------------------------------------------------------------
    // Unarmed die per actor: <Unarmed Die: d8>
    //-------------------------------------------------------------------------
    const _Game_Actor_rkAttackDice = Game_Actor.prototype.rkAttackDice;
    Game_Actor.prototype.rkAttackDice = function() {
        if (!this.rkMainWeapon()) {
            const d = Rank.parseDice(meta(this.actor(), "Unarmed Die"));
            if (d) return d;
        }
        return _Game_Actor_rkAttackDice.call(this);
    };

    //-------------------------------------------------------------------------
    // Breakthrough
    //-------------------------------------------------------------------------
    Story.breakthrough = function(silent) {
        const from = Story.gate();
        if (from >= 9) return;
        const to = from + 1;
        $gameVariables.setValue(P.gateVar, to);
        const floor = to * 100;
        const gated = $gameParty.members().filter(a => Story.isGated(a));
        const lines = [];
        // the three best base stats cross into the new band
        for (const a of gated) {
            const apt = a.rkAptitude();
            const order = [0, 1, 2, 3, 4, 5, 6].sort((x, y) => (a.rkBaseStat(y) - a.rkBaseStat(x)) || (apt[y] - apt[x]));
            for (const i of order.slice(0, 3)) {
                const v = a.rkBaseStat(i);
                if (v < floor) a.rkArr("_rkBonus")[i] += floor - v;
            }
        }
        // one level (bound actors follow their master)
        for (const a of gated) {
            if (!a.storyMaster() && !a.isMaxLevel()) a.changeLevel(a.level + 1, false);
        }
        for (const a of gated) {
            a.storyRefreshGear(true);
            // new weapon forms (the equip screen switches between every form unlocked so far)
            for (const tag of ["Rank Weapon", "DW Extra"]) {
                const map = String(meta(a.actor(), tag) || "");
                for (const part of map.split(",")) {
                    const m = part.trim().match(/^(SSS|SS|S|F|E|D|C|B|A|V)\s+(\d+)$/i);
                    const f = m && Rank.parseRank(m[1]) === to ? $dataWeapons[Number(m[2])] : null;
                    if (f && f.meta && f.meta["DW Form"]) lines.push(a.name() + " can summon a new form: " + f.name + "!");
                }
            }
            // known skills rise with her: none stays more than one rank behind the new rank
            for (const id of a._skills.slice()) {
                const sk = $dataSkills[id];
                if (!sk || !Rank.isMasterySkill(sk)) continue;
                const floor = Math.min(to - 1, a.rkMasteryCap(id));
                if (floor > 0 && a.rkMasteryRank(id) < floor) a.rkSetMastery(id, floor, 0);
            }
            const learned = [];
            const learn = meta(a.actor(), "Breakthrough " + Rank.letter(to));
            if (learn) {
                for (const id of String(learn).split(",").map(s => Number(s.trim())).filter(Boolean)) learned.push(id);
            }
            // level skills that waited for this rank (<Needs Rank: D>)
            for (const l of a.currentClass().learnings) if (l.level <= a.level) learned.push(l.skillId);
            for (const id of learned) {
                if ($dataSkills[id] && !a.isLearnedSkill(id)) {
                    a.learnSkill(id);
                    if (a.isLearnedSkill(id)) lines.push(a.name() + " learned " + $dataSkills[id].name + "!");
                }
            }
            a.recoverAll();
        }
        if (!silent) {
            const names = gated.map(a => a.name()).join(" and ");
            const head = "\\C[6]Breakthrough!\\C[0]  " + names + ": rank \\RK[" + from + "] → \\RK[" + to + "]";
            $gameMessage.add(head);
            if (gated.length) {
                $gameMessage.add("Level " + gated[0].level + ". Stat caps rise to " + Story.gateCap() + ".");
            }
            for (const l of lines) $gameMessage.add(l);
        }
    };

    //-------------------------------------------------------------------------
    // Auto Build: <Auto Build: CON 40, STR 35 ...>
    //-------------------------------------------------------------------------
    Story.autoBuild = function(actor) {
        const text = meta(actor.actor(), "Auto Build");
        if (!text) return;
        const w = {};
        let total = 0;
        const re = /(STR|DEX|CON|INT|WIS|CHA|MAG)\s*[:=]?\s*(\d+(?:\.\d+)?)/gi;
        let m;
        while ((m = re.exec(text))) {
            w[Rank.statIndex(m[1])] = Number(m[2]);
            total += Number(m[2]);
        }
        if (total <= 0) return;
        for (let pass = 0; pass < 6 && actor.rkPoints() > 0; pass++) {
            const pts = actor.rkPoints();
            let spent = 0;
            for (const k of Object.keys(w)) {
                const want = Math.max(1, Math.floor((pts * w[k]) / total));
                spent += actor.rkAllocate(Number(k), want);
            }
            if (spent === 0) break;
        }
        Story.catchUp(actor);
        actor.recoverAll();
    };

    // A gated actor who joins after breakthroughs gets what the party got at each one: the three best base
    // stats are raised to the floor of the current band, so the newcomer stands at the party's rank.
    Story.catchUp = function(actor) {
        if (!actor || !Story.isGated(actor)) return;
        const floor = Story.gate() * 100;
        if (floor <= 0) return;
        const apt = actor.rkAptitude();
        const order = [0, 1, 2, 3, 4, 5, 6].sort((x, y) => (actor.rkBaseStat(y) - actor.rkBaseStat(x)) || (apt[y] - apt[x]));
        for (const i of order.slice(0, 3)) {
            const v = actor.rkBaseStat(i);
            if (v < floor) actor.rkArr("_rkBonus")[i] += floor - v;
        }
        actor.refresh();
    };

    //-------------------------------------------------------------------------
    // Rest points and vessel revival
    //-------------------------------------------------------------------------
    Story.vesselActive = () => !!($gameSwitches && P.vesselSwitch && $gameSwitches.value(P.vesselSwitch));

    Story.setRestPoint = function(mapId, x, y, d) {
        $gameSystem._storyRest = { mapId, x, y, d: d || 2 };
    };

    Story.restPoint = function() {
        return $gameSystem._storyRest || { mapId: P.restMap, x: P.restX, y: P.restY, d: 2 };
    };

    Story.performRevival = function() {
        const interp = $gameMap._interpreter;
        if (interp && interp.isRunning()) {
            const id = interp.eventId();
            if (id > 0) $gameMap.unlockEvent(id);
            interp.clear();
        }
        $gameMessage.clear();
        $gameScreen.clearFade();
        for (const actor of $gameParty.members()) {
            actor.recoverAll();
            actor._storyBarrier = 0;
        }
        const lost = Math.floor($gameParty.gold() * P.moneyLoss);
        $gameParty.loseGold(lost);
        if (P.lostVar) $gameVariables.setValue(P.lostVar, lost);
        if (P.deathsVar) $gameVariables.setValue(P.deathsVar, $gameVariables.value(P.deathsVar) + 1);
        const r = Story.restPoint();
        $gamePlayer.reserveTransfer(r.mapId, r.x, r.y, r.d || 2, 0);
        if (P.reviveCE) $gameTemp.reserveCommonEvent(P.reviveCE);
    };

    const _SceneManager_goto = SceneManager.goto;
    SceneManager.goto = function(sceneClass) {
        if (sceneClass === Scene_Gameover && Story.vesselActive() && !BattleManager.isBattleTest()) {
            Story.performRevival();
            if (this._scene instanceof Scene_Battle) {
                this.pop();
                return;
            }
            _SceneManager_goto.call(this, Scene_Map);
            return;
        }
        _SceneManager_goto.call(this, sceneClass);
    };

    // knocked-out members get up with 1 HP after a won or fled battle
    const _BattleManager_endBattle = BattleManager.endBattle;
    BattleManager.endBattle = function(result) {
        _BattleManager_endBattle.call(this, result);
        if (P.reviveDowned && result !== 2 && !$gameParty.isAllDead()) {
            for (const actor of $gameParty.members()) {
                if (actor.isDead()) {
                    actor.revive();
                    actor.setHp(1);
                }
            }
        }
    };

    //-------------------------------------------------------------------------
    // Passive states and party auras
    //-------------------------------------------------------------------------
    Story.skillStates = function(actor, tag) {
        const out = [];
        for (const id of actor._skills || []) {
            const s = $dataSkills[id];
            const v = s && s.meta ? s.meta[tag] : null;
            if (v) {
                for (const sid of String(v).split(",").map(x => Number(x.trim())).filter(Boolean)) {
                    if ($dataStates[sid]) out.push($dataStates[sid]);
                }
            }
        }
        return out;
    };

    // party members that already exist (never creates actors: traitObjects runs during actor setup)
    Story.existingMembers = function() {
        if (!$gameParty || !$gameActors) return [];
        return $gameParty._actors.map(id => $gameActors._data[id]).filter(Boolean);
    };

    Story._auraCache = { frame: -1, states: [] };
    Story.partyAuras = function() {
        const f = Graphics.frameCount;
        if (Story._auraCache.frame === f && !Story._auraDirty) return Story._auraCache.states;
        const states = [];
        const max = $gameParty ? $gameParty.maxBattleMembers() : 4;
        for (const member of Story.existingMembers().slice(0, max)) {
            if (member.isDeathStateAffected()) continue;
            for (const st of Story.skillStates(member, "Party Aura")) if (!states.includes(st)) states.push(st);
        }
        Story._auraCache = { frame: f, states };
        Story._auraDirty = false;
        return states;
    };

    const _Game_Actor_traitObjects = Game_Actor.prototype.traitObjects;
    Game_Actor.prototype.traitObjects = function() {
        const objects = _Game_Actor_traitObjects.call(this);
        for (const st of Story.skillStates(this, "Passive State")) objects.push(st);
        if ($gameParty && $gameParty._actors.includes(this.actorId())) {
            for (const st of Story.partyAuras()) if (!objects.includes(st)) objects.push(st);
        }
        return objects;
    };

    // <Needs Rank: D>: a gated actor learns the skill only once the story gate has reached that rank
    // (a level skill that arrives early waits for the next breakthrough)
    Story.skillNeedsRank = function(skill) {
        const v = skill && skill.meta ? skill.meta["Needs Rank"] : null;
        return v ? Rank.parseRank(String(v).trim()) || 0 : 0;
    };

    const _Game_Actor_learnSkill = Game_Actor.prototype.learnSkill;
    Game_Actor.prototype.learnSkill = function(skillId) {
        const skill = $dataSkills[skillId];
        if (Story.isGated(this) && $gameVariables && Story.skillNeedsRank(skill) > Story.gate()) return;
        _Game_Actor_learnSkill.call(this, skillId);
        Story._auraDirty = true;
    };

    // passive skills are never used
    const _Game_BattlerBase_meetsSkillConditions = Game_BattlerBase.prototype.meetsSkillConditions;
    Game_BattlerBase.prototype.meetsSkillConditions = function(skill) {
        if (skill && skill.meta && (skill.meta["Passive State"] || skill.meta["Party Aura"]) && skill.occasion === 3) {
            return false;
        }
        return _Game_BattlerBase_meetsSkillConditions.call(this, skill);
    };

    //-------------------------------------------------------------------------
    // Barrier (temporary HP): <Barrier: d6 50%>
    //-------------------------------------------------------------------------
    Story.parseBarrier = function(skill) {
        if (!skill || !skill.meta || !skill.meta.Barrier) return null;
        if (skill._storyBarrier !== undefined) return skill._storyBarrier;
        const t = String(skill.meta.Barrier).trim();
        const m = t.match(/^(\S+)(?:\s+(\d+(?:\.\d+)?)%)?/);
        const dice = m ? Rank.parseDice(m[1]) : null;
        skill._storyBarrier = dice ? { dice, rate: m[2] ? Number(m[2]) / 100 : 1 } : null;
        return skill._storyBarrier;
    };

    Game_Battler.prototype.storyBarrier = function() {
        return this._storyBarrier || 0;
    };

    Game_Battler.prototype.storySetBarrier = function(value) {
        this._storyBarrier = Math.max(0, Math.round(value));
        const st = P.barrierState;
        if (st && $dataStates[st]) {
            if (this._storyBarrier > 0 && !this.isStateAffected(st)) this.addNewState(st);
            if (this._storyBarrier <= 0 && this.isStateAffected(st)) this.eraseState(st);
        }
    };

    const _Game_Action_apply = Game_Action.prototype.apply;
    Game_Action.prototype.apply = function(target) {
        _Game_Action_apply.call(this, target);
        const subject = this.subject();
        const item = this.item();
        const result = target.result();
        const b = Story.parseBarrier(item);
        if (b && result.isHit() && target.isAlive()) {
            const amount = Story.rollAmount(subject, item, b.dice, b.rate);
            if (amount > target.storyBarrier()) {
                target.storySetBarrier(amount);
                result.storyBarrierGain = amount;
                result.success = true;
            }
        }
        if (item && result.isHit()) Story.afterApply(this, subject, target, item, result);
    };

    // die + POW(skill stat) + 10 x working rank, times a rate
    Story.rollAmount = function(subject, item, dice, rate) {
        const stat = Rank.skillStat(item, subject);
        const rank = DataManager.isSkill(item) && subject.rkSkillRank ? subject.rkSkillRank(item) : subject.rkRank();
        return Math.round((Rank.rollDice(dice) + Rank.pow(subject.rkStat(stat)) + 10 * rank) * (rate === undefined ? 1 : rate));
    };

    const _Game_Action_executeHpDamage = Game_Action.prototype.executeHpDamage;
    Game_Action.prototype.executeHpDamage = function(target, value) {
        if (value > 0 && target.storyBarrier() > 0) {
            const absorbed = Math.min(value, target.storyBarrier());
            target.storySetBarrier(target.storyBarrier() - absorbed);
            target.result().storyAbsorbed = absorbed;
            value -= absorbed;
        }
        if (value > 0) value = Story.shareBurden(this, target, value);
        if (value > 0) value = Story.lethalGuard(target, value);
        _Game_Action_executeHpDamage.call(this, target, value);
        const saved = target.result().storySaved;
        if (saved && saved.barrier > target.storyBarrier()) target.storySetBarrier(saved.barrier);
        // storm damage stops regeneration for the round (Living Steel)
        if (value > 0 && this.item() && this.item().damage.elementId === Story.P.stormElement) target._storyNoRegen = true;
    };

    const _Game_ActionResult_clear = Game_ActionResult.prototype.clear;
    Game_ActionResult.prototype.clear = function() {
        _Game_ActionResult_clear.call(this);
        this.storyAbsorbed = 0;
        this.storyBarrierGain = 0;
        this.storySaved = null;
        this.storyShared = null;
    };

    const _Window_BattleLog_displayHpDamage = Window_BattleLog.prototype.displayHpDamage;
    Window_BattleLog.prototype.displayHpDamage = function(target) {
        const r = target.result();
        if (r.storyAbsorbed > 0) {
            this.push("addText", target.name() + "'s barrier absorbs " + r.storyAbsorbed + ".");
        }
        _Window_BattleLog_displayHpDamage.call(this, target);
        if (r.storyShared) {
            this.push("addText", r.storyShared.who.name() + " takes " + r.storyShared.amount + " of it.");
        }
        if (r.storySaved) {
            this.push("addText", r.storySaved.text);
            this.push("wait");
        }
    };

    const _Window_BattleLog_displayActionResults = Window_BattleLog.prototype.displayActionResults;
    Window_BattleLog.prototype.displayActionResults = function(subject, target) {
        _Window_BattleLog_displayActionResults.call(this, subject, target);
        const r = target.result();
        if (r.storyBarrierGain > 0) {
            this.push("addText", target.name() + " is shielded (barrier " + r.storyBarrierGain + ").");
            this.push("wait");
        }
    };

    const _Game_Battler_onBattleEnd = Game_Battler.prototype.onBattleEnd;
    Game_Battler.prototype.onBattleEnd = function() {
        _Game_Battler_onBattleEnd.call(this);
        this.storySetBarrier(0);
    };

    //-------------------------------------------------------------------------
    // Interpose: a state with <Interpose> takes physical hits aimed at allies
    //-------------------------------------------------------------------------
    Game_Battler.prototype.storyIsInterposing = function() {
        return this.isAlive() && this.canMove() && this.states().some(s => s.meta && s.meta.Interpose);
    };

    const _BattleManager_applySubstitute = BattleManager.applySubstitute;
    BattleManager.applySubstitute = function(target) {
        const action = this._action;
        const subject = this._subject;
        const hostile = action && target && subject && subject.isActor() !== target.isActor() &&
            (Rank.isDamaging(action.item()) || action.isForOpponent());
        if (hostile) {
            const friends = target.friendsUnit().aliveMembers().filter(m => m !== target && m.canMove());
            // Last Bastion: every attack and effect aimed at an ally lands on her
            let guard = friends.find(m => Story.hasTag(m, "Interpose All"));
            // Vanguard Rush: the ally she ran to is hers to cover
            if (!guard && target._storyWardBy && target.states().some(s => s.meta && s.meta.Warded)) {
                guard = friends.find(m => m.isActor() && m.actorId() === target._storyWardBy) || null;
            }
            // Interpose: single-target attacks (Living Fortress: spells too)
            if (!guard && !action.isForAll()) {
                guard = friends.find(m => m.storyIsInterposing() && (action.isPhysical() || Story.hasTag(m, "Interpose Magic")));
            }
            if (guard) {
                this._logWindow.displaySubstitute(guard, target);
                return guard;
            }
        }
        return _BattleManager_applySubstitute.call(this, target);
    };

    //=========================================================================
    // COMBAT KIT: relics, reactions, stances and the floating armory
    //=========================================================================
    // Tags are read from a battler's trait objects (states, passive skills' states, auras, gear; enemies: their
    // database entry) and from the skills an actor knows.
    Story.traitObjs = b => (b && b.traitObjects ? b.traitObjects() : []);
    Story.tagSum = function(b, tag) {
        let v = 0;
        for (const o of Story.traitObjs(b)) {
            const t = o && o.meta ? o.meta[tag] : undefined;
            if (t === undefined || t === true) continue;
            const n = parseFloat(String(t));
            if (!isNaN(n)) v += n;
        }
        return v;
    };
    Story.tagValue = function(b, tag) {
        for (const o of Story.traitObjs(b)) {
            const t = o && o.meta ? o.meta[tag] : undefined;
            if (t !== undefined) return t === true ? true : String(t).trim();
        }
        return undefined;
    };
    Story.hasTag = (b, tag) => Story.tagValue(b, tag) !== undefined;
    Story.skillWith = function(actor, tag) {
        if (!actor || !actor.isActor || !actor.isActor()) return null;
        for (const s of actor.skills()) if (s && s.meta && s.meta[tag]) return s;
        return null;
    };
    Story.partyKnows = tag => $gameParty.battleMembers().some(m => m.isAlive() && Story.skillWith(m, tag));

    //-------------------------------------------------------------------------
    // Rank-piercing relics (the Dawn Regalia) and the Veil of Ash
    //-------------------------------------------------------------------------
    //   Enemy <Demon>: every relic the party holds (Rank Pierce Variable) cancels one rank of difference in
    //   either direction, never past even. Enemy <Veil of Ash>: counts as rank V until four relics are held.
    Story.pierce = () => (P.pierceVar && $gameVariables ? Math.max(0, $gameVariables.value(P.pierceVar) || 0) : 0);
    Story.isDemon = b => !!(b && b.isEnemy() && meta(b.enemy(), "Demon"));
    Story.isDemonic = b => !!(b && b.isEnemy() && (meta(b.enemy(), "Demon") || meta(b.enemy(), "Miasma") ||
        b.states().some(s => s.meta && s.meta.Miasma)));

    const _Game_Enemy_rkRank = Game_Enemy.prototype.rkRank;
    Game_Enemy.prototype.rkRank = function() {
        if (meta(this.enemy(), "Veil of Ash") && Story.pierce() < 4 && !this._storyVeilDown) return 9;
        return _Game_Enemy_rkRank.call(this);
    };

    const _Game_Action_rkAdjustGap = Game_Action.prototype.rkAdjustGap;
    Game_Action.prototype.rkAdjustGap = function(gap, info, target) {
        gap = _Game_Action_rkAdjustGap.call(this, gap, info, target);
        const n = Story.pierce();
        if (n > 0) {
            const s = info.subject;
            if (s.isActor() && Story.isDemon(target) && gap < 0) gap = Math.min(0, gap + n);
            else if (Story.isDemon(s) && target.isActor() && gap > 0) gap = Math.max(0, gap - n);
        }
        return gap;
    };

    //-------------------------------------------------------------------------
    // Once per battle, self states, concentration, initiative, save bonuses
    //-------------------------------------------------------------------------
    //   Skill <Once Per Battle>   Skill <Self State: 61>   State <Concentration> (ends when its caster falls)
    //   <Init: +2> (initiative)   <Save Bonus: +2> (all saves)   <DEX Save: +2> (one stat's saves)
    const _Game_Battler_useItem = Game_Battler.prototype.useItem;
    Game_Battler.prototype.useItem = function(item) {
        _Game_Battler_useItem.call(this, item);
        if (!DataManager.isSkill(item) || !item.meta) return;
        if (item.meta["Once Per Battle"] && $gameParty.inBattle()) (this._storyOnce = this._storyOnce || []).push(item.id);
        const ss = item.meta["Self State"];
        if (ss) {
            for (const id of String(ss).split(",").map(x => Number(x.trim())).filter(Boolean)) {
                this.addState(id);
                Story.markConc(this, id, this);
            }
        }
    };

    const _Game_BattlerBase_meetsSkillConditions2 = Game_BattlerBase.prototype.meetsSkillConditions;
    Game_BattlerBase.prototype.meetsSkillConditions = function(skill) {
        if (skill && skill.meta && skill.meta["Once Per Battle"] && $gameParty.inBattle() &&
            (this._storyOnce || []).includes(skill.id)) return false;
        if (this.isActor() && this.storySwiftBlocked && this.storySwiftBlocked(skill)) return false;
        return _Game_BattlerBase_meetsSkillConditions2.call(this, skill);
    };

    const _Game_Battler_onBattleStart = Game_Battler.prototype.onBattleStart;
    Game_Battler.prototype.onBattleStart = function(advantageous) {
        _Game_Battler_onBattleStart.call(this, advantageous);
        this._storyOnce = [];
        this._storyConc = {};
        this._storyNoRegen = false;
    };

    const _Game_Battler_onBattleEnd2 = Game_Battler.prototype.onBattleEnd;
    Game_Battler.prototype.onBattleEnd = function() {
        _Game_Battler_onBattleEnd2.call(this);
        this._storyOnce = [];
        this._storyConc = {};
        this._storyTauntBy = 0;
        this._storyBurdenBy = 0;
        this._storyWardBy = 0;
    };

    Story.concKey = b => (b.isActor() ? "a" + b.actorId() : "e" + b.index());
    Story.markConc = function(target, stateId, source) {
        const st = $dataStates[stateId];
        if (!st || !st.meta || !st.meta.Concentration || !target.isStateAffected(stateId)) return;
        (target._storyConc = target._storyConc || {})[stateId] = Story.concKey(source);
    };
    Story.dropConc = function(source) {
        if (!$gameParty.inBattle()) return;
        const key = Story.concKey(source);
        for (const b of $gameParty.battleMembers().concat($gameTroop.members())) {
            if (!b._storyConc) continue;
            for (const id of Object.keys(b._storyConc)) {
                if (b._storyConc[id] === key) {
                    delete b._storyConc[id];
                    b.removeState(Number(id));
                }
            }
        }
    };
    const _Game_BattlerBase_die = Game_BattlerBase.prototype.die;
    Game_BattlerBase.prototype.die = function() {
        _Game_BattlerBase_die.call(this);
        if (this.friendsUnit) Story.dropConc(this);
    };

    const _Game_Action_speed = Game_Action.prototype.speed;
    Game_Action.prototype.speed = function() {
        return _Game_Action_speed.call(this) + Story.tagSum(this.subject(), "Init");
    };

    if (Game_Action.prototype.rkSaveBonus) {
        const _rkSaveBonus = Game_Action.prototype.rkSaveBonus;
        Game_Action.prototype.rkSaveBonus = function(target, stat) {
            return _rkSaveBonus.call(this, target, stat) + Story.tagSum(target, "Save Bonus") + Story.tagSum(target, stat + " Save");
        };
    }

    //-------------------------------------------------------------------------
    // After a hit lands: who applied which state, reactions to misses, harvests
    //-------------------------------------------------------------------------
    //   State <Taunted> (the foe attacks whoever applied it)   <Burden Share> (half of every hit goes to whoever
    //   applied it)   <Warded> (whoever applied it covers the ally)   Skill <Share Drain: 50%> (that share of the
    //   damage dealt heals the allies, most hurt first)   State <Riposte> (a foe that misses her takes a floating strike)
    Story.afterApply = function(action, subject, target, item, result) {
        for (const e of item.effects || []) {
            if (e.code !== 21 || !target.isStateAffected(e.dataId)) continue;
            const m = ($dataStates[e.dataId] && $dataStates[e.dataId].meta) || {};
            Story.markConc(target, e.dataId, subject);
            if (subject.isActor()) {
                if (m.Taunted) target._storyTauntBy = subject.actorId();
                if (m.Warded) target._storyWardBy = subject.actorId();
                if (m["Burden Share"]) {
                    // the bearer doesn't share her own wounds with herself
                    if (target === subject) {
                        target.removeState(e.dataId);
                        result.addedStates = result.addedStates.filter(id => id !== e.dataId);
                        result.removedStates = result.removedStates.filter(id => id !== e.dataId);
                    } else target._storyBurdenBy = subject.actorId();
                }
            }
        }
        if (subject.isActor() !== target.isActor()) {
            action._storyLastFoe = target;
            if (item.meta && item.meta["Share Drain"] && result.hpDamage > 0) {
                action._storyDrained = (action._storyDrained || 0) + result.hpDamage;
            }
        }
    };

    const _Game_Action_apply_miss = Game_Action.prototype.apply;
    Game_Action.prototype.apply = function(target) {
        _Game_Action_apply_miss.call(this, target);
        const s = this.subject();
        const r = target.result();
        if (!$gameParty.inBattle() || !s.isEnemy() || !target.isActor() || !r.missed) return;
        if (target.isAlive() && target.canMove() && Story.hasTag(target, "Riposte") && Story.floatSkillId()) {
            const turn = $gameTroop.turnCount();
            if (target._storyRiposteTurn !== turn) {
                target._storyRiposteTurn = turn;
                BattleManager.storyQueue(target, Story.floatSkillId(), s);
            }
        }
    };

    Story.shareHeal = function(subject, action, log) {
        const rate = Story.pct(action.item().meta["Share Drain"], 0.5);
        let pool = Math.round((action._storyDrained || 0) * rate);
        action._storyDrained = 0;
        if (pool <= 0) return;
        const allies = subject.friendsUnit().aliveMembers().slice().sort((a, b) => (b.mhp - b.hp) - (a.mhp - a.hp));
        const parts = [];
        for (const m of allies) {
            if (pool <= 0) break;
            const need = m.mhp - m.hp;
            if (need <= 0) continue;
            const h = Math.min(need, pool);
            m.gainHp(h);
            pool -= h;
            parts.push(m.name() + " +" + h);
        }
        if (parts.length && log) {
            log.push("addText", "The harvest mends the living: " + parts.join(", ") + ".");
            log.push("wait");
        }
    };
    Story.pct = function(v, d) {
        if (v === undefined || v === true) return d;
        const m = String(v).match(/([+\-]?\d+(?:\.\d+)?)\s*(%?)/);
        if (!m) return d;
        return m[2] ? Number(m[1]) / 100 : Number(m[1]);
    };

    //-------------------------------------------------------------------------
    // Reactions that keep someone standing
    //-------------------------------------------------------------------------
    //   State <Unkillable>: can't drop below 1 HP.
    //   Skill <Unbroken> (occasion Never): once per battle, when she would drop to 0 HP she pays its MP, stays at
    //   1 and gains a barrier (d10 + POW + 10 x rank).
    //   Skill <Hold The Line> (occasion Never): once per ally per battle, when an ally would drop to 0 HP the
    //   one who knows it pays its MP; the ally stays at 1 with the same barrier.
    Story.canReact = (actor, skill) => actor.isAlive() && actor.canMove() && actor.mp >= actor.skillMpCost(skill) &&
        !actor.isSkillSealed(skill.id) && !actor.isSkillTypeSealed(skill.stypeId);
    Story.payReaction = (actor, skill) => actor.setMp(actor.mp - actor.skillMpCost(skill));

    Story.lethalGuard = function(target, value) {
        if (target.hp <= 0 || value < target.hp) return value;
        const r = target.result();
        if (Story.hasTag(target, "Unkillable")) {
            r.storySaved = { text: target.name() + " will not fall!" };
            return target.hp - 1;
        }
        if (!$gameParty.inBattle() || !target.isActor()) return value;
        BattleManager._storyOnceKeys = BattleManager._storyOnceKeys || {};
        const once = BattleManager._storyOnceKeys;
        const d10 = Rank.dice(1, 10, 0);
        const ub = Story.skillWith(target, "Unbroken");
        if (ub && !once["ub" + target.actorId()] && Story.canReact(target, ub)) {
            once["ub" + target.actorId()] = true;
            Story.payReaction(target, ub);
            r.storySaved = { text: target.name() + ": Unbroken! She stays on her feet.", barrier: Story.rollAmount(target, ub, d10) };
            return target.hp - 1;
        }
        if (!once["hl" + target.actorId()]) {
            for (const m of $gameParty.battleMembers()) {
                if (m === target) continue;
                const hl = Story.skillWith(m, "Hold The Line");
                if (!hl || !Story.canReact(m, hl)) continue;
                once["hl" + target.actorId()] = true;
                Story.payReaction(m, hl);
                r.storySaved = { text: m.name() + ": \"Hold the line!\" " + target.name() + " stays standing.",
                    barrier: Story.rollAmount(m, hl, d10) };
                return target.hp - 1;
            }
        }
        return value;
    };

    // Share the Burden: half of every hit on a sharer goes to the bearer (her Brace and resistances apply)
    Story.shareBurden = function(action, target, value) {
        if (!target.isActor() || !target._storyBurdenBy) return value;
        if (!target.states().some(s => s.meta && s.meta["Burden Share"])) return value;
        const bearer = $gameActors.actor(target._storyBurdenBy);
        if (!bearer || bearer === target || !bearer.isAlive() || !$gameParty.battleMembers().includes(bearer)) return value;
        const half = Math.floor(value / 2);
        if (half <= 0) return value;
        let hers = half;
        if (action.isPhysical()) hers *= bearer.pdr;
        else if (action.isMagical()) hers *= bearer.mdr;
        hers = Math.max(0, Math.round(hers));
        const keep = bearer.result();
        hers = Story.lethalGuard(bearer, hers);
        bearer.setHp(bearer.hp - hers);
        if (keep.storySaved && keep.storySaved.barrier > bearer.storyBarrier()) bearer.storySetBarrier(keep.storySaved.barrier);
        target.result().storyShared = { who: bearer, amount: hers };
        return value - half;
    };

    //-------------------------------------------------------------------------
    // Regeneration by rank: <Rank Regen: 2%> heals (rank + 1) x 2% of max HP each turn (storms stop it a round)
    //-------------------------------------------------------------------------
    const _Game_BattlerBase_xparam = Game_BattlerBase.prototype.xparam;
    Game_BattlerBase.prototype.xparam = function(xparamId) {
        let v = _Game_BattlerBase_xparam.call(this, xparamId);
        if (xparamId === 7 && !this._storyNoRegen) {
            const pct = Story.tagSum(this, "Rank Regen");
            if (pct > 0) v += (pct / 100) * (this.rkRank() + 1);
        }
        return v;
    };
    const _Game_Battler_regenerateAll = Game_Battler.prototype.regenerateAll;
    Game_Battler.prototype.regenerateAll = function() {
        _Game_Battler_regenerateAll.call(this);
        this._storyNoRegen = false;
    };

    //-------------------------------------------------------------------------
    // Taunts: <Taunted> on a foe, <Taunt Aura> on the one every foe must face
    //-------------------------------------------------------------------------
    Story.taunter = function(enemy) {
        const party = $gameParty.aliveMembers();
        const aura = party.find(m => m.canMove() && Story.hasTag(m, "Taunt Aura"));
        if (aura) return aura;
        if (enemy._storyTauntBy && enemy.states().some(s => s.meta && s.meta.Taunted)) {
            const a = $gameActors.actor(enemy._storyTauntBy);
            if (a && party.includes(a)) return a;
        }
        return null;
    };
    const _Game_Action_targetsForOpponents = Game_Action.prototype.targetsForOpponents;
    Game_Action.prototype.targetsForOpponents = function() {
        const s = this.subject();
        if (s && s.isEnemy() && this.isForOne() && $gameParty.inBattle()) {
            const t = Story.taunter(s);
            if (t) return [t];
        }
        return _Game_Action_targetsForOpponents.call(this);
    };

    //-------------------------------------------------------------------------
    // Lend a Blade: <Lent Blade: d8> — the ally strikes with the lent die, the better of STR/DEX and the
    // bearer's weapon rank (and Light, from the state's attack element)
    //-------------------------------------------------------------------------
    Story.lentDie = function(actor) {
        const st = actor.states().find(s => s.meta && s.meta["Lent Blade"]);
        return st ? Rank.parseDice(String(st.meta["Lent Blade"])) : null;
    };
    const _Game_Actor_rkAttackDice2 = Game_Actor.prototype.rkAttackDice;
    Game_Actor.prototype.rkAttackDice = function() {
        const own = _Game_Actor_rkAttackDice2.call(this);
        const lent = Story.lentDie(this);
        return lent && Rank.diceAvg(lent) > Rank.diceAvg(own) ? lent : own;
    };
    const _Game_Actor_rkAttackStat2 = Game_Actor.prototype.rkAttackStat;
    Game_Actor.prototype.rkAttackStat = function() {
        if (Story.lentDie(this)) return this.rkStat("DEX") > this.rkStat("STR") ? "DEX" : "STR";
        return _Game_Actor_rkAttackStat2.call(this);
    };
    const _Game_Actor_rkWeaponRank2 = Game_Actor.prototype.rkWeaponRank;
    Game_Actor.prototype.rkWeaponRank = function() {
        const r = _Game_Actor_rkWeaponRank2.call(this);
        return Story.lentDie(this) ? Math.max(r, Story.gate()) : r;
    };

    //-------------------------------------------------------------------------
    // Only against demons: skill <Only Demons> has no effect on anything that isn't a demon or miasma-touched
    //-------------------------------------------------------------------------
    const _Game_Action_testApply = Game_Action.prototype.testApply;
    Game_Action.prototype.testApply = function(target) {
        const item = this.item();
        if (item && item.meta && item.meta["Only Demons"] && !Story.isDemonic(target)) return false;
        return _Game_Action_testApply.call(this, target);
    };

    //-------------------------------------------------------------------------
    // Blows turned aside: <Guardian Blade> (once a round, a hit on her or an ally that lands by less than 5
    // misses; <Guardian Blade: all> once a round for each ally) and <Blink> (the first hit on her each round)
    //-------------------------------------------------------------------------
    if (Game_Action.prototype.rkResolve) {
        const _rkResolve = Game_Action.prototype.rkResolve;
        Game_Action.prototype.rkResolve = function(target, estimate) {
            const res = _rkResolve.call(this, target, estimate);
            if (estimate || res.mode !== "roll" || !res.hit || !$gameParty.inBattle()) return res;
            const s = this.subject();
            if (!s.isEnemy() || !target.isActor()) return res;
            const turn = $gameTroop.turnCount();
            if (Story.hasTag(target, "Blink") && target.canMove() && target._storyBlinkTurn !== turn) {
                target._storyBlinkTurn = turn;
                res.hit = false;
                res.crit = false;
                res.storyTurned = target.name() + " blinks to one of her blades!";
                return res;
            }
            if (res.roll !== 20 && res.total - res.ac < 5) {
                for (const g of $gameParty.aliveMembers()) {
                    const mode = Story.tagValue(g, "Guardian Blade");
                    if (mode === undefined || !g.canMove()) continue;
                    const key = String(mode).toLowerCase() === "all" ? "a" + target.actorId() : "one";
                    g._storyGuardTurn = g._storyGuardTurn || {};
                    if (g._storyGuardTurn[key] === turn) continue;
                    g._storyGuardTurn[key] = turn;
                    res.hit = false;
                    res.crit = false;
                    res.storyTurned = g.name() + "'s floating blade turns the blow aside!";
                    return res;
                }
            }
            return res;
        };
        const _Window_BattleLog_displayMiss = Window_BattleLog.prototype.displayMiss;
        Window_BattleLog.prototype.displayMiss = function(target) {
            const r = target.result();
            if (r.rk && r.rk.storyTurned) {
                this.push("performMiss", target);
                this.push("addText", r.rk.storyTurned);
                return;
            }
            _Window_BattleLog_displayMiss.call(this, target);
        };
    }

    //-------------------------------------------------------------------------
    // Chained strikes: the floating armory strikes after its bearer's action (<Float Strikes: 1>), answers a
    // miss (<Riposte>) and cuts any foe that acts inside its ring (<Ring Strike>). They use the skill tagged
    // <Floating Strike> and play as their own short action right after the one that caused them.
    //-------------------------------------------------------------------------
    Story.floatSkillId = function() {
        if (Story._floatId === undefined) {
            const s = $dataSkills.find(x => x && x.meta && x.meta["Floating Strike"]);
            Story._floatId = s ? s.id : 0;
        }
        return Story._floatId;
    };

    BattleManager.storyQueue = function(subject, skillId, target) {
        (this._storyChain = this._storyChain || []).push({ subject, skillId, target });
    };

    BattleManager.storyFollowUps = function() {
        const act = this._action;
        const subj = this._subject;
        // (endAction also runs for a battler whose action was invalid: this._action is then someone else's)
        if (!act || !subj || act._storyChained || act._storyFollowed || act.subject() !== subj) return;
        act._storyFollowed = true;
        if (act._storyDrained > 0) Story.shareHeal(subj, act, this._logWindow);
        const fid = Story.floatSkillId();
        if (!fid) return;
        if (subj.isActor() && subj.isAlive() && subj.canMove() && !subj.isConfused()) {
            const n = Math.floor(Story.tagSum(subj, "Float Strikes"));
            for (let i = 0; i < n; i++) {
                const last = act._storyLastFoe;
                const foes = $gameTroop.aliveMembers();
                const t = last && last.isAlive() ? last : foes[Math.floor(Math.random() * foes.length)];
                if (t) this.storyQueue(subj, fid, t);
            }
        }
        if (subj.isEnemy() && subj.isAlive()) {
            for (const m of $gameParty.aliveMembers()) {
                if (m.canMove() && Story.hasTag(m, "Ring Strike") && subj._storyRingTurn !== $gameTroop.turnCount()) {
                    subj._storyRingTurn = $gameTroop.turnCount();
                    this.storyQueue(m, fid, subj);
                }
            }
        }
    };

    BattleManager.storyNextChain = function() {
        const q = this._storyChain || [];
        while (q.length) {
            const n = q.shift();
            if ($gameTroop.isAllDead() || $gameParty.isAllDead()) continue;
            if (n.subject.isAlive() && n.subject.canMove() && n.target && n.target.isAlive()) return n;
        }
        return null;
    };

    BattleManager.storyStartChain = function(n) {
        if (this.rkFinishUse) this.rkFinishUse();
        this._logWindow.endAction(this._subject);
        if (!this._storyChainOwner) this._storyChainOwner = this._subject;
        this._subject = n.subject;
        const action = new Game_Action(n.subject, true);
        action.setSkill(n.skillId);
        action._storyChained = true;
        this._action = action;
        this._targets = [n.target];
        this._phase = "action";
        n.subject.cancelMotionRefresh();
        this._logWindow.startAction(n.subject, action, [n.target]);
    };

    BattleManager.storyEndChain = function() {
        const owner = this._storyChainOwner;
        if (!owner) return;
        this._storyChainOwner = null;
        if (this._subject !== owner) {
            this._logWindow.endAction(this._subject);
            this._subject = owner;
        }
    };

    const _BattleManager_endAction = BattleManager.endAction;
    BattleManager.endAction = function() {
        this.storyFollowUps();
        const next = this.storyNextChain();
        if (next) {
            this.storyStartChain(next);
            return;
        }
        this.storyEndChain();
        _BattleManager_endAction.call(this);
    };

    const _BattleManager_initMembers = BattleManager.initMembers;
    BattleManager.initMembers = function() {
        _BattleManager_initMembers.call(this);
        this._storyChain = [];
        this._storyChainOwner = null;
        this._storyOnceKeys = {};
    };

    //-------------------------------------------------------------------------
    // Swift Mercy: <Swift: 17, 21> — with two actions a turn, only one may be something other than these
    // skills (or Guard)
    //-------------------------------------------------------------------------
    Story.swiftList = function(actor) {
        const out = [];
        for (const s of actor.skills()) {
            if (s && s.meta && s.meta.Swift) out.push(...String(s.meta.Swift).split(",").map(x => Number(x.trim())).filter(Boolean));
        }
        return out;
    };
    Game_Actor.prototype.storySwiftBlocked = function(item) {
        if (!$gameParty.inBattle() || BattleManager._phase !== "input" || !item) return false;
        if (this.numActions() < 2) return false;
        const list = Story.swiftList(this);
        if (!list.length) return false;
        const swift = it => it && DataManager.isSkill(it) && (list.includes(it.id) || it.id === this.guardSkillId());
        if (swift(item)) return false;
        const idx = this._actionInputIndex;
        return this._actions.some((a, i) => i !== idx && a && a.item() && !swift(a.item()));
    };
    const _Game_Actor_canUse = Game_Actor.prototype.canUse;
    Game_Actor.prototype.canUse = function(item) {
        if (item && DataManager.isItem(item) && this.storySwiftBlocked(item)) return false;
        return _Game_Actor_canUse.call(this, item);
    };

    //-------------------------------------------------------------------------
    // Old General's Eye (<General's Eye> on a known skill): the foes' weaknesses at the start of a battle.
    // Deathwatch (<Deathwatch>): the target window shows a foe's exact HP.
    //-------------------------------------------------------------------------
    const _BattleManager_displayStartMessages = BattleManager.displayStartMessages;
    BattleManager.displayStartMessages = function() {
        _BattleManager_displayStartMessages.call(this);
        const eye = $gameParty.battleMembers().find(m => m.isAlive() && Story.skillWith(m, "General's Eye"));
        if (!eye) return;
        const seen = new Set();
        const lines = [];
        for (const e of $gameTroop.aliveMembers()) {
            if (seen.has(e.enemyId())) continue;
            seen.add(e.enemyId());
            const weak = [];
            const res = [];
            for (let el = 2; el < $dataSystem.elements.length; el++) {
                const r = e.elementRate(el);
                const n = $dataSystem.elements[el];
                if (r > 1) weak.push(n);
                else if (r <= 0) res.push(n + " (immune)");
                else if (r < 1) res.push(n);
            }
            if (!weak.length && !res.length) continue;
            let t = e.originalName() + ":";
            if (weak.length) t += " weak to " + weak.join(", ");
            if (res.length) t += (weak.length ? ";" : "") + " resists " + res.join(", ");
            lines.push(t);
        }
        if (lines.length) {
            $gameMessage.add("\\C[6]" + eye.name() + "'s eye\\C[0] reads the field:");
            for (const l of lines.slice(0, 5)) $gameMessage.add(l);
        }
    };

    if (Rank.conditionText) {
        const _conditionText = Rank.conditionText;
        Rank.conditionText = function(b) {
            const t = _conditionText.call(this, b);
            if (b && b.isEnemy && b.isEnemy() && $gameParty.inBattle() && Story.partyKnows("Deathwatch")) {
                return t + " (" + b.hp + "/" + b.mhp + ")";
            }
            return t;
        };
    }

    //-------------------------------------------------------------------------
    // Events that stay on the player: <Follow Player>
    //-------------------------------------------------------------------------
    const _Game_Event_initialize = Game_Event.prototype.initialize;
    Game_Event.prototype.initialize = function(mapId, eventId) {
        _Game_Event_initialize.call(this, mapId, eventId);
        this._storyFollow = !!(this.event() && this.event().meta && this.event().meta["Follow Player"]);
        if (this._storyFollow) {
            this.setThrough(true);
            this.storyStick();
        }
    };

    Game_Event.prototype.storyStick = function() {
        this._x = $gamePlayer._x;
        this._y = $gamePlayer._y;
        this._realX = $gamePlayer._realX;
        this._realY = $gamePlayer._realY;
    };

    const _Game_Event_update = Game_Event.prototype.update;
    Game_Event.prototype.update = function() {
        _Game_Event_update.call(this);
        if (this._storyFollow) this.storyStick();
    };

    // map transfer: the follower light starts where the player lands
    const _Game_Map_setupEvents = Game_Map.prototype.setupEvents;
    Game_Map.prototype.setupEvents = function() {
        _Game_Map_setupEvents.call(this);
        for (const ev of this.events()) if (ev._storyFollow) ev.storyStick();
    };

    //-------------------------------------------------------------------------
    // Money: 1 gk = 10 sl = 100 kl, gold counts kl
    //-------------------------------------------------------------------------
    Story.formatMoney = function(value) {
        value = Math.max(0, Math.floor(Number(value) || 0));
        const [g, s, k] = P.coins;
        const gk = Math.floor(value / 100);
        const sl = Math.floor((value % 100) / 10);
        const kl = value % 10;
        const parts = [];
        if (gk) parts.push(gk + " " + g);
        if (sl) parts.push(sl + " " + s);
        if (kl || !parts.length) parts.push(kl + " " + k);
        return parts.join(" ");
    };

    Window_Base.prototype.drawCurrencyValue = function(value, unit, x, y, width) {
        this.resetTextColor();
        this.drawText(Story.formatMoney(value), x, y, width, "right");
    };

    Window_ShopBuy.prototype.priceWidth = function() {
        return 150;
    };

    Window_ShopBuy.prototype.drawItem = function(index) {
        const item = this.itemAt(index);
        const price = this.price(item);
        const rect = this.itemLineRect(index);
        const priceWidth = this.priceWidth();
        const priceX = rect.x + rect.width - priceWidth;
        const nameWidth = rect.width - priceWidth;
        this.changePaintOpacity(this.isEnabled(item));
        this.drawItemName(item, rect.x, rect.y, nameWidth);
        this.drawText(Story.formatMoney(price), priceX, rect.y, priceWidth, "right");
        this.changePaintOpacity(true);
    };

    //-------------------------------------------------------------------------
    // Calendar (12 months x 30 days) and clock
    //-------------------------------------------------------------------------
    Story.cycle = () => (window.McKathlin && McKathlin.DayNightCycle && $gameSystem ? McKathlin.DayNightCycle : null);

    Story.daysPassed = function() {
        const c = Story.cycle();
        return c ? c.getDays() : 0;
    };

    Story.dateText = function(daysPassed) {
        const d = daysPassed === undefined ? Story.daysPassed() : daysPassed;
        let index = (P.startDay - 1) + (P.startMonth - 1) * 30 + d;
        const year = P.startYear + Math.floor(index / 360);
        index %= 360;
        const month = Math.floor(index / 30);
        const day = (index % 30) + 1;
        return String(day).padStart(2, "0") + "." + (P.months[month] || "?") + "." + year;
    };

    Story.timeText = function() {
        const c = Story.cycle();
        if (!c) return "";
        const h = c.getHours();
        const m = c.getMinutes();
        const part = h < 5 ? "Night" : h < 8 ? "Dawn" : h < 12 ? "Morning" : h < 17 ? "Afternoon" : h < 20 ? "Evening" : "Night";
        return String(h).padStart(2, "0") + ":" + String(m).padStart(2, "0") + "  " + part;
    };

    // text codes: \MONEY[n]  \DATE
    const _Window_Base_convertEscapeCharacters = Window_Base.prototype.convertEscapeCharacters;
    Window_Base.prototype.convertEscapeCharacters = function(text) {
        text = _Window_Base_convertEscapeCharacters.call(this, text);
        text = text.replace(/\x1bMONEY\[(\d+)\]/gi, (_, n) => Story.formatMoney(Number(n)));
        text = text.replace(/\x1bDATE/gi, () => Story.dateText());
        return text;
    };

    function Window_StoryInfo() {
        this.initialize(...arguments);
    }
    Window_StoryInfo.prototype = Object.create(Window_Gold.prototype);
    Window_StoryInfo.prototype.constructor = Window_StoryInfo;
    Window_StoryInfo.prototype.refresh = function() {
        const rect = this.itemLineRect(0);
        const lh = this.lineHeight();
        this.contents.clear();
        this.changeTextColor(ColorManager.systemColor());
        this.contents.fontSize = $gameSystem.mainFontSize() - 4;
        this.drawText(Story.dateText(), rect.x, rect.y, rect.width, "left");
        this.resetFontSettings();
        this.contents.fontSize = $gameSystem.mainFontSize() - 4;
        this.drawText(Story.timeText(), rect.x, rect.y + lh, rect.width, "left");
        this.resetFontSettings();
        this.drawCurrencyValue(this.value(), this.currencyUnit(), rect.x, rect.y + lh * 2, rect.width);
    };
    window.Window_StoryInfo = Window_StoryInfo;

    const _Scene_Menu_goldWindowRect = Scene_Menu.prototype.goldWindowRect;
    Scene_Menu.prototype.goldWindowRect = function() {
        if (!P.menuClock) return _Scene_Menu_goldWindowRect.call(this);
        const ww = this.mainCommandWidth();
        const wh = this.calcWindowHeight(3, true);
        const wx = this.isRightInputMode() ? Graphics.boxWidth - ww : 0;
        const wy = this.mainAreaBottom() - wh;
        return new Rectangle(wx, wy, ww, wh);
    };

    const _Scene_Menu_createGoldWindow = Scene_Menu.prototype.createGoldWindow;
    Scene_Menu.prototype.createGoldWindow = function() {
        if (!P.menuClock) return _Scene_Menu_createGoldWindow.call(this);
        this._goldWindow = new Window_StoryInfo(this.goldWindowRect());
        this.addWindow(this._goldWindow);
    };

    //-------------------------------------------------------------------------
    // Chapter card
    //-------------------------------------------------------------------------
    function Sprite_StoryCard() {
        this.initialize(...arguments);
    }
    Sprite_StoryCard.prototype = Object.create(Sprite.prototype);
    Sprite_StoryCard.prototype.constructor = Sprite_StoryCard;
    Sprite_StoryCard.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        this.bitmap = new Bitmap(Graphics.width, 180);
        this.y = Math.floor(Graphics.height / 2 - 110);
        this.opacity = 0;
        this._key = null;
    };
    Sprite_StoryCard.prototype.update = function() {
        Sprite.prototype.update.call(this);
        const card = $gameTemp._storyCard;
        if (!card) {
            this.opacity = 0;
            this._key = null;
            return;
        }
        if (this._key !== card.key) {
            this._key = card.key;
            const b = this.bitmap;
            b.clear();
            const w = b.width;
            b.fillRect(0, 40, w, 100, "rgba(0,0,0,0.55)");
            b.fontSize = 44;
            b.fontFace = $gameSystem.mainFontFace();
            b.textColor = "#f4e6c8";
            b.outlineWidth = 5;
            b.drawText(card.title, 0, 46, w, 56, "center");
            b.fontSize = 24;
            b.textColor = "#c9b89a";
            b.drawText(card.subtitle, 0, 98, w, 34, "center");
        }
        card.t++;
        const fade = 30;
        const d = card.duration;
        this.opacity = card.t < fade ? (255 * card.t) / fade : card.t > d - fade ? Math.max(0, (255 * (d - card.t)) / fade) : 255;
        if (card.t >= d) $gameTemp._storyCard = null;
    };

    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this._storyCardSprite = new Sprite_StoryCard();
        this.addChild(this._storyCardSprite);
    };

    Story.showCard = function(title, subtitle, duration) {
        $gameTemp._storyCard = { title: title || "", subtitle: subtitle || "", duration: Math.max(60, duration || 180), t: 0,
            key: Date.now() + Math.random() };
    };

    const _Game_Interpreter_updateWaitMode = Game_Interpreter.prototype.updateWaitMode;
    Game_Interpreter.prototype.updateWaitMode = function() {
        if (this._waitMode === "storyCard") {
            if ($gameTemp._storyCard) return true;
            this._waitMode = "";
            return false;
        }
        return _Game_Interpreter_updateWaitMode.call(this);
    };

    //-------------------------------------------------------------------------
    // Map weather:  <Weather: snow 5>  <Weather: rain 3 unless 26>  <Weather: keep>
    //-------------------------------------------------------------------------
    // Weather belongs to the place: entering a map sets its weather (a map
    // without the tag is clear), so snow never follows the party into a cave.
    Story.mapWeather = function() {
        const tag = $dataMap && $dataMap.meta ? $dataMap.meta.Weather : undefined;
        const clear = { type: "none", power: 0 };
        if (tag === undefined || tag === true) return clear;
        const s = String(tag).trim().toLowerCase();
        if (s === "keep") return null;
        const m = s.match(/^(none|rain|storm|snow)\s*(\d+)?(?:\s+unless\s+(\d+))?/);
        if (!m) return clear;
        if (m[3] && $gameSwitches.value(Number(m[3]))) return clear;
        return { type: m[1], power: m[1] === "none" ? 0 : Number(m[2] || 5) };
    };

    const _Game_Map_setup = Game_Map.prototype.setup;
    Game_Map.prototype.setup = function(mapId) {
        _Game_Map_setup.apply(this, arguments);
        const w = Story.mapWeather();
        if (w) $gameScreen.changeWeather(w.type, w.power, 0);
    };

    //-------------------------------------------------------------------------
    // Ground layers (TausiLighting)
    //-------------------------------------------------------------------------
    // TausiLighting draws "Blend" layers above the whole tilemap, characters
    // included. Layers whose image is named "Ground_..." (a frozen river, a
    // flooded field) belong on the ground: they are moved into the tilemap,
    // above the floor tiles and below characters and star tiles.
    Story.patchTausiLayers = function() {
        const proto = Spriteset_Map.prototype;
        const refresh = proto._tausiLighting_refreshLayers;
        if (!refresh || refresh._storyGround) return;
        const patched = function() {
            // hand our sprites back to the base sprite so Tausi can remove them
            for (const s of this._tausiLighting_layerSprites || []) {
                if (s.parent && s.parent !== this._baseSprite) {
                    s.parent.removeChild(s);
                    this._baseSprite.addChild(s);
                }
            }
            refresh.apply(this, arguments);
            for (const s of this._tausiLighting_layerSprites || []) {
                const obj = s.mapObject && s.mapObject.getObject && s.mapObject.getObject();
                if (obj && /(^|\/)Ground_/.test(obj.url || "") && this._tilemap) {
                    this._baseSprite.removeChild(s);
                    s.z = 0.5;
                    this._tilemap.addChild(s);
                }
            }
        };
        patched._storyGround = true;
        proto._tausiLighting_refreshLayers = patched;
    };

    const _Spriteset_Map_initialize = Spriteset_Map.prototype.initialize;
    Spriteset_Map.prototype.initialize = function() {
        Story.patchTausiLayers();
        _Spriteset_Map_initialize.apply(this, arguments);
    };

    //-------------------------------------------------------------------------
    // Plugin commands
    //-------------------------------------------------------------------------
    PluginManager.registerCommand(PLUGIN, "Breakthrough", function(args) {
        Story.breakthrough(String(args.silent) === "true");
        if (String(args.silent) !== "true") this.setWaitMode("message");
    });

    PluginManager.registerCommand(PLUGIN, "SetRestPoint", function(args) {
        let mapId = Number(args.mapId) || 0;
        let x = Number(args.x) || 0;
        let y = Number(args.y) || 0;
        const d = Number(args.direction) || 2;
        if (mapId <= 0) {
            mapId = $gameMap.mapId();
            x = $gamePlayer.x;
            y = $gamePlayer.y;
        }
        Story.setRestPoint(mapId, x, y, d);
    });

    PluginManager.registerCommand(PLUGIN, "SyncLevel", function(args) {
        const a = $gameActors.actor(Number(args.actorId));
        const s = $gameActors.actor(Number(args.sourceId));
        if (a && s && a.level !== s.level) a.changeLevel(s.level, false);
        if (a) a.recoverAll();
    });

    PluginManager.registerCommand(PLUGIN, "AutoBuild", function(args) {
        const a = $gameActors.actor(Number(args.actorId));
        if (a) Story.autoBuild(a);
    });

    PluginManager.registerCommand(PLUGIN, "CatchUp", function(args) {
        const a = $gameActors.actor(Number(args.actorId));
        if (a) {
            Story.catchUp(a);
            a.recoverAll();
        }
    });

    PluginManager.registerCommand(PLUGIN, "ChapterCard", function(args) {
        Story.showCard(args.title, args.subtitle, Number(args.duration) || 180);
        this.setWaitMode("storyCard");
    });

    PluginManager.registerCommand(PLUGIN, "Revive", function() {
        Story.performRevival();
    });
})();
