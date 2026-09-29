// Save / load round trip with story state.
const lib = require("./storylib.js");
module.exports = async h => {
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() && !$gameMap.isEventRunning(), 20000);
    const before = await h.eval(async () => {
        spendAll();
        $gameActors.actor(1).changeLevel(4, false);
        $gameParty.gainGold(345);
        Story.setRestPoint(5, 13, 20, 2);
        PluginManager.callCommand($gameMap._interpreter, "WD_Quest", "newCreateQuest", {id: "9", icon: "87", cat: "0", short: "Test", long: "Test", index: "9",
            giver: "x", area: "y", desc: "z", questTrans: "[]", status: "ongoing", logs: "[]", track: JSON.stringify({isTrackable: "true", text: "", textTrans: "[]"})});
        $gameSystem.onBeforeSave();
        await DataManager.saveGame(1);
        return { lv: $gameActors.actor(2).level, gold: $gameParty.gold(), rest: Story.restPoint(), time: Story.timeText(),
                 quests: $gameSystem._questContainer.questsArray.length, weapon: $gameActors.actor(1).weapons()[0].name };
    });
    await h.eval(() => { DataManager.setupNewGame(); });
    const after = await h.eval(async () => {
        await DataManager.loadGame(1);
        return { lv: $gameActors.actor(2).level, gold: $gameParty.gold(), rest: Story.restPoint(), time: Story.timeText(),
                 quests: $gameSystem._questContainer.questsArray.length, weapon: $gameActors.actor(1).weapons()[0].name };
    });
    console.log("before", JSON.stringify(before));
    console.log("after ", JSON.stringify(after));
};
