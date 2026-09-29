// Balance runs for the story database: BAL='[{"level":1,"troops":["Goblins x2"],"n":20}]'
const lib = require("./storylib.js");
module.exports = async h => {
    const cfg = JSON.parse(process.env.BAL || '[{"level":1,"troops":["Crows x2","Goblins x2","Wolf"],"n":20}]');
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); $gameSwitches.setValue(1, true); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 20000);
    await h.eval(() => {
        $gameMap._interpreter.clear();
        $gameMap.events().forEach(e => e.erase());
        window.__noRevive = true;
        BattleManager.gainExp = function() {};
        BattleManager.gainGold = function() {};
        BattleManager.gainDropItems = function() {};
    });
    const results = [];
    for (const c of cfg) {
        const members = c.members || [1, 2];
        const setupParty = () => h.eval(([L, members, gate, bt]) => {
            $gameParty._actors = members.slice();
            $gameVariables.setValue(1, gate || 0);
            $gameActors._data = [];
            const actors = members.map(id => $gameActors.actor(id));
            if (bt) {
                // the real progression: level to bt under gate F, break through, then level on
                // (Falin is not there yet: she joins afterwards and catches up)
                $gameVariables.setValue(1, 0);
                $gameParty._actors = members.filter(id => id !== 3);
                for (const a of actors) if (a.actorId() !== 3) a.changeLevel(bt, false);
                for (const a of actors) spend(a);
                Story.breakthrough(true);
                for (const a of actors) if (a.actorId() !== 3) spend(a);
                $gameMessage.clear();
                $gameParty._actors = members.slice();
            }
            for (const a of actors) if (a.level < L) a.changeLevel(L, false);
            for (const a of actors) {
                if (a.actorId() === 3 && window.Story) Story.autoBuild(a);   // Falin joins with Auto Build
                else spend(a);
                a.recoverAll();
            }
            $gamePlayer.refresh();
        }, [c.level, members, c.gate, c.bt]);
        await setupParty();
        const party = await h.eval(() => party());
        for (const tname of c.troops) {
            let wins = 0, turns = 0, hpLeft = 0, n = c.n || 20;
            for (let i = 0; i < n; i++) {
                if (c.resetEach) await setupParty();
                await h.eval(t => {
                    $gameParty.members().forEach(a => a.recoverAll());
                    const id = $dataTroops.findIndex(x => x && x.name === t);
                    BattleManager.setup(id, false, true);
                    SceneManager.push(Scene_Battle);
                }, tname);
                await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                    !SceneManager.isSceneChanging(), 60000);
                const r = await h.eval(() => {
                    const b = __battles[__battles.length - 1];
                    const hp = $gameParty.members().reduce((s, a) => s + a.hp / a.mhp, 0) / $gameParty.size();
                    return { result: b.result, turns: b.turns, hp };
                });
                if (r.result === 0 || (r.result === 1 && c.abortWins)) { wins++; hpLeft += r.hp; }
                turns += r.turns;
            }
            const line = `L${c.level} ${tname.padEnd(20)} win ${Math.round(100 * wins / n)}%  turns ${(turns / n).toFixed(1)}  hp left ${wins ? Math.round(100 * hpLeft / wins) : 0}%`;
            results.push(line);
            console.log(line);
        }
        console.log("   party:", JSON.stringify(party.map(p => p.name + " " + p.stats + " HP" + p.hp + " MP" + p.mp)));
    }
};
