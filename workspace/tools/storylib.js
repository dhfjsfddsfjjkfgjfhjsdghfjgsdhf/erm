// Page-side helpers for story playthrough tests (evaluated in the game page).
module.exports = () => {
    window.__autoMsg = true;
    window.__autoBattle = true;
    Window_BattleLog.prototype.messageSpeed = function() { return 1; };
    Game_Actor.prototype.isAutoBattle = function() { return window.__autoBattle !== false; };
    // spending policies: share of free points per stat
    window.POLICY = {
        1: { DEX: 0.5, CON: 0.25, STR: 0.1, MAG: 0.15 },
        2: { WIS: 0.4, MAG: 0.3, CON: 0.2, CHA: 0.1 },
        3: { CON: 0.45, STR: 0.4, WIS: 0.15 }
    };
    window.spend = function(a) {
        const pol = POLICY[a.actorId()];
        if (!pol) return;
        const pts = a.rkPoints();
        const want = {};
        for (const s of Object.keys(pol)) want[s] = Math.floor(pts * pol[s]);
        for (let pass = 0; pass < 4; pass++) {
            for (const s of Object.keys(pol)) want[s] -= a.rkAllocate(Rank.statIndex(s), want[s]);
        }
        for (const s of ["CON", "DEX", "WIS", "STR", "MAG", "CHA", "INT"]) a.rkAllocate(Rank.statIndex(s), a.rkPoints());
    };
    window.spendAll = () => $gameParty.members().forEach(a => spend(a));
    window.evByName = name => $gameMap.events().find(e => e.event().name === name);
    window.startEvent = function(nameOrId) {
        const ev = typeof nameOrId === "number" ? $gameMap.event(nameOrId) : evByName(nameOrId);
        if (!ev) throw new Error("no event " + nameOrId);
        ev.start();
        return ev.eventId();
    };
    window.party = () => $gameParty.members().map(a => ({
        name: a.name(), lv: a.level, rank: Rank.letter(a.rkRank()), hp: a.hp + "/" + a.mhp, mp: a.mp + "/" + a.mmp,
        stats: Rank.STATS.map((s, i) => s + a.rkBaseStat(i)).join(" "), pts: a.rkPoints(),
        skills: a.skills().map(s => s.name).join(",")
    }));
    // log battles
    window.__battles = [];
    if (!window.__battleHooked) {
        window.__battleHooked = true;
        const _setup = BattleManager.setup;
        BattleManager.setup = function(troopId, canEscape, canLose) {
            _setup.call(this, troopId, canEscape, canLose);
            window.__battles.push({ troop: $dataTroops[troopId].name, turns: 0, result: null,
                                    hpStart: $gameParty.members().map(a => a.hp) });
        };
        const _end = BattleManager.endBattle;
        BattleManager.endBattle = function(result) {
            const b = window.__battles[window.__battles.length - 1];
            if (b) {
                b.result = result;
                b.turns = $gameTroop.turnCount();
                b.hpEnd = $gameParty.members().map(a => a.hp + "/" + a.mhp);
            }
            _end.call(this, result);
        };
    }
};
