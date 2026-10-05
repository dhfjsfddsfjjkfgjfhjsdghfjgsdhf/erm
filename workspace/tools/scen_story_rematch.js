// A story breakthrough inside a battle (troop page at turn 2) must happen once: fights the Nordstraße emergency
// (E) and the Messingvogt (D) twice each, the first time aborted after turn 2 as if the party had lost, and checks
// that the breakthrough gate only moved once.
//   PORT=8124 WEBROOT=/home/claude/mz/sweb node tools/run_game.js tools/scen_story_rematch.js
const lib = require("./storylib.js");
module.exports = async h => {
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); $gameSwitches.setValue(1, true); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 20000);
    await h.eval(() => {
        $gameMap._interpreter.clear();
        $gameMap.events().forEach(e => e.erase());
        window.__noRevive = true;
        const k = $gameActors.actor(1);
        k.changeLevel(12, false); spendAll();
        $gameParty.members().forEach(a => a.recoverAll());
    });
    const fails = [];
    const fightTo = async (troop, turns) => {
        await h.eval(t => {
            const id = $dataTroops.findIndex(x => x && x.name === t);
            if (id < 0) throw new Error("no troop " + t);
            $gameParty.members().forEach(a => a.recoverAll());
            BattleManager.setup(id, false, true);
            SceneManager.push(Scene_Battle);
        }, troop);
        await h.runUntil(t => (SceneManager._scene instanceof Scene_Battle && $gameTroop.turnCount() >= t &&
            !$gameTroop.isEventRunning() && BattleManager._phase !== "turn") || SceneManager._scene instanceof Scene_Map, 120000, turns);
        await h.eval(() => { if (SceneManager._scene instanceof Scene_Battle) BattleManager.abort(); });
        await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
            !SceneManager.isSceneChanging(), 60000);
        return h.eval(() => $gameVariables.value(1));
    };
    for (const [troop, before, level] of [["Aschenhunde", 0, 12], ["Messingvogt", 1, 20]]) {
        await h.eval(([g, L]) => {
            $gameVariables.setValue(1, g);
            const k = $gameActors.actor(1); if (k.level < L) { k.changeLevel(L, false); spendAll(); }
            if (L >= 15 && !$gameParty._actors.includes(3)) { $gameParty.addActor(3); $gameActors.actor(3).changeLevel(L, false); Story.autoBuild($gameActors.actor(3)); }
        }, [before, level]);
        const g1 = await fightTo(troop, 3);
        const g2 = await fightTo(troop, 3);
        const ok = g1 === before + 1 && g2 === before + 1;
        console.log((ok ? "  ok   " : "  FAIL ") + troop + ": gate " + before + " -> " + g1 + " (first fight) -> " + g2 + " (rematch)");
        if (!ok) fails.push(troop);
    }
    if (fails.length) throw new Error("breakthrough repeated: " + fails.join(", "));
    console.log("REMATCH TEST PASSED");
};
