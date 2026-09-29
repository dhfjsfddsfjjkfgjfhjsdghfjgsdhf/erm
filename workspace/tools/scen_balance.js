// Balance run: builds the party at a level with a simple point policy, then auto-battles troops.
const PAGE_LIB = () => {
    window.__autoMsg = true;
    Game_Actor.prototype.isAutoBattle = function() { return true; };
    Window_BattleLog.prototype.messageSpeed = function() { return 1; };
    const POLICY = {
        1: { STR: 0.5, CON: 0.4, DEX: 0.1 },
        2: { DEX: 0.55, CON: 0.3, STR: 0.15 },
        3: { WIS: 0.55, CON: 0.3, MAG: 0.15 },
        4: { MAG: 0.6, CON: 0.25, INT: 0.15 }
    };
    window.simSetup = function(level, gear) {
        DataManager.setupNewGame();
        for (const a of $gameParty.members()) {
            a.changeLevel(level, false);
            a.recoverAll();
            const pol = POLICY[a.actorId()];
            let pts = a.rkPoints();
            const want = {};
            for (const s of Object.keys(pol)) want[s] = Math.floor(pts * pol[s]);
            for (let pass = 0; pass < 4; pass++) {
                for (const s of Object.keys(pol)) {
                    const i = Rank.statIndex(s);
                    const n = a.rkAllocate(i, want[s]);
                    want[s] -= n;
                }
            }
            // leftovers go to CON, then anything
            for (const s of ["CON", "DEX", "STR", "WIS", "MAG", "INT", "CHA"]) a.rkAllocate(Rank.statIndex(s), a.rkPoints());
            if (gear && gear[a.actorId()]) {
                gear[a.actorId()].forEach((id, slot) => {
                    if (id === null) return;
                    const item = slot === 0 ? $dataWeapons[id] : $dataArmors[id];
                    if (item) a.forceChangeEquip(slot, item);
                });
            }
            a.recoverAll();
        }
        $gamePlayer.reserveTransfer(2, 7, 37, 8, 0);
    };
    window.simSnapshot = function() {
        return $gameParty.members().map(a => ({
            id: a.actorId(), lv: a.level, rank: Rank.letter(a.rkRank()), hp: a.hp, mhp: a.mhp, mp: a.mp, mmp: a.mmp,
            stats: a.rkStats().join("/"), ac: a.rkAC(), exp: a.currentExp(),
            m: a.rkMasterySkills().map(s => s.name + ":" + Rank.letter(a.rkMasteryRank(s.id)) + a.rkMasteryExp(s.id)).join(",")
        }));
    };
    window.simStartBattle = function(troopId) {
        for (const a of $gameParty.members()) a.recoverAll();
        window.__battleLog = [];
        BattleManager.setup(troopId, true, true);
        window.__turns = 0;
        SceneManager.push(Scene_Battle);
    };
    // count damage events
    if (!window.__hooked) {
        window.__hooked = true;
        const _ex = Game_Action.prototype.executeHpDamage;
        Game_Action.prototype.executeHpDamage = function(target, value) {
            _ex.call(this, target, value);
            (window.__battleLog = window.__battleLog || []).push([this.subject().name(), this.item().name, target.name(), value]);
        };
    }
};

module.exports = async h => {
    const sceneIs = async name => {
        await h.runUntil(n => SceneManager._scene && SceneManager._scene.constructor.name === n && SceneManager._scene._started &&
            !SceneManager.isSceneChanging(), 20000, name);
    };
    await h.eval(PAGE_LIB);
    await h.eval(() => { DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await sceneIs("Scene_Map");

    const results = [];
    async function fight(level, troopId, runs, gear) {
        let wins = 0, turns = 0, deaths = 0, hpLeft = 0;
        let snap = null;
        let sample = null;
        for (let r = 0; r < runs; r++) {
            await h.eval(([l, g]) => simSetup(l, g), [level, gear || null]);
            await h.run(5);
            await h.runUntil(() => !$gamePlayer.isTransferring() && $gameMap.mapId() === 2 && SceneManager._scene.constructor.name === "Scene_Map" &&
                SceneManager._scene._started && !SceneManager.isSceneChanging() && !$gameMap.isEventRunning(), 5000);
            if (r === 0) snap = await h.eval(() => simSnapshot());
            await h.eval(t => simStartBattle(t), troopId);
            await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle", 2000);
            await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Map" && !SceneManager.isSceneChanging(), 60000);
            const res = await h.eval(() => ({
                dead: $gameParty.members().filter(a => a.isDead()).length,
                allDead: $gameParty.isAllDead(),
                turns: $gameTroop.turnCount(),
                hp: $gameParty.members().reduce((s, a) => s + a.hp / a.mhp, 0) / $gameParty.size(),
                log: window.__battleLog.slice(0, 16),
                after: simSnapshot()
            }));
            if (!res.allDead) wins++;
            turns += res.turns;
            deaths += res.dead;
            hpLeft += res.hp;
            if (r === 0) sample = res;
        }
        const row = { level, troop: troopId, wins: wins + "/" + runs, avgTurns: (turns / runs).toFixed(1),
            avgDeaths: (deaths / runs).toFixed(1), avgHpLeft: Math.round(hpLeft / runs * 100) + "%" };
        results.push(row);
        console.log("FIGHT", JSON.stringify(row));
        console.log("  party", JSON.stringify(snap.map(a => `${a.id} L${a.lv} ${a.rank} HP${a.mhp} MP${a.mmp} AC${a.ac} [${a.stats}]`)));
        console.log("  log", JSON.stringify(sample.log.map(l => l.join(" ")).slice(0, 12)));
        console.log("  after", JSON.stringify(sample.after.map(a => `${a.id} exp${a.exp} ${a.m}`)));
    }
    const lvl1 = null;
    const E_GEAR = { 1: [3, null, 9, 4, 10], 2: [7, null, 9, 2, 11], 3: [9, 7, null, 3, 10], 4: [10, null, null, 5, 12] };
    await fight(1, 2, 4, lvl1);   // goblins
    await fight(1, 1, 4, lvl1);   // crows
    await fight(1, 4, 4, lvl1);   // mushrooms
    await fight(3, 5, 4, lvl1);   // wolf elite
    await fight(5, 6, 4, lvl1);   // goblin chief
    await fight(8, 6, 3, lvl1);
    await fight(8, 8, 3, lvl1);   // lizard (E) at level 8
    await fight(14, 8, 3, E_GEAR);  // lizard at level 14 with E gear
    await fight(14, 9, 3, E_GEAR);
    await fight(14, 10, 3, E_GEAR); // treant elite
    await fight(14, 11, 3, E_GEAR); // wolfman boss
    await fight(18, 11, 3, E_GEAR);
    await fight(14, 2, 2, E_GEAR);  // goblins at 14: exp gap
    console.log("SUMMARY");
    for (const r of results) console.log(JSON.stringify(r));
};
