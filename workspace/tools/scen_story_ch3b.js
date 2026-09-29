// Chapter 3 details: menu with three members, save/load across the breakthrough, the Wolfsgrube at L15,
// the frozen ferry crossing from a thawed Eisfurt, revival at Frontposten.
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches;
module.exports = async h => {
    const idle = async () => h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
        !$gameMap.isEventRunning() && !$gamePlayer.isTransferring() && !$gameMessage.isBusy() && !SceneManager.isSceneChanging(), 60000);
    await h.eval(lib);
    // a party at the start of Act II, after the breakthrough
    await h.eval(sws => {
        DataManager.setupNewGame();
        for (const n of Object.keys(sws)) if (/^(P|C1|C2|C3|A2): /.test(n) || n === "Vessel Active") $gameSwitches.setValue(sws[n], true);
        $gameVariables.setValue(1, 0);
        const k = $gameActors.actor(1);
        k.changeLevel(12, false);
        spendAll();
        Story.breakthrough(true);
        k.changeLevel(15, false);
        $gameParty.addActor(3);
        PluginManager.callCommand($gameMap._interpreter, "Story_Core", "SyncLevel", { actorId: "3", sourceId: "1" });
        PluginManager.callCommand($gameMap._interpreter, "Story_Core", "AutoBuild", { actorId: "3" });
        spendAll();
        $gameParty.members().forEach(a => a.recoverAll());
        $gameParty.gainGold(1234);
        $gameActors.actor(1).setNickname("Wolfsbann");
        $gamePlayer.reserveTransfer(61, 16, 31, 2, 0);
        SceneManager.goto(Scene_Map);
    }, SW);
    await idle();
    const before = await h.eval(() => party());
    console.log("party:", JSON.stringify(before));
    await h.eval(() => SceneManager.push(Scene_Menu));
    await h.runUntil(() => SceneManager._scene instanceof Scene_Menu && SceneManager._scene.isStarted(), 20000);
    await h.frames(20);
    await h.shot("m3_menu");
    await h.eval(() => { $gameParty.setMenuActor($gameActors.actor(3)); SceneManager.push(Scene_Status); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Status && SceneManager._scene.isStarted(), 20000);
    await h.frames(20);
    await h.shot("m3_status_falin");
    await h.eval(() => { $gameParty.setMenuActor($gameActors.actor(3)); SceneManager.goto(Scene_Equip); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Equip && SceneManager._scene.isStarted(), 20000);
    await h.frames(20);
    await h.shot("m3_equip_falin");
    await h.eval(() => SceneManager.goto(Scene_Map));
    await idle();
    // save and load
    const saved = await h.eval(async () => {
        $gameSystem.onBeforeSave();
        await DataManager.saveGame(1);
        return true;
    });
    await h.eval(() => { $gameParty.members().forEach(a => a.changeLevel(1, false)); $gameVariables.setValue(1, 0); });
    await h.eval(async () => {
        await DataManager.loadGame(1);
        SceneManager.goto(Scene_Map);
    });
    await idle();
    const after = await h.eval(() => ({ party: party(), gate: $gameVariables.value(1), weapon: $gameActors.actor(1).weapons()[0].name,
        plate: $gameActors.actor(3).equips()[3] && $gameActors.actor(3).equips()[3].name, nick: $gameActors.actor(1).nickname() }));
    console.log("after load:", JSON.stringify(after));
    if (JSON.stringify(after.party) !== JSON.stringify(before)) throw new Error("party changed across save/load");
    if (after.gate !== 1 || after.weapon !== "Lichtdolch" || after.plate !== "Verschmolzene Platte E") throw new Error("gear/gate lost");
    console.log("  ok: save/load keeps levels, gate, rank gear");
    // revival at Frontposten (rest point from the barracks)
    await h.eval(() => {
        PluginManager.callCommand($gameMap._interpreter, "Story_Core", "SetRestPoint", { mapId: "61", x: "16", y: "31", direction: "2" });
        $gamePlayer.reserveTransfer(60, 12, 20, 8, 0);
    });
    await idle();
    await h.eval(() => {
        window.__autoBattle = true;
        $gameParty.members().forEach(a => a.setHp(1));
        const id = $dataTroops.findIndex(t => t && t.name === "Aschenschwinge");
        BattleManager.setup(id, false, false);
        SceneManager.push(Scene_Battle);
    });
    await idle();
    const rev = await h.eval(() => ({ map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y], deaths: $gameVariables.value(2),
        hp: $gameParty.members().map(a => a.hp + "/" + a.mhp) }));
    console.log("revival:", JSON.stringify(rev));
    if (rev.map !== 61) throw new Error("revival did not return to Frontposten");
    console.log("  ok: revival at Frontposten 3");
    await h.shot("m3_revived");
};
