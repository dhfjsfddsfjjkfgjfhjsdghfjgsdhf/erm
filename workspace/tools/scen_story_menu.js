// Menu, quest log and battle screenshots.
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
module.exports = async h => {
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() && !$gameMap.isEventRunning(), 20000);
    // create two quests via the plugin commands and spend points
    await h.eval(() => {
        spendAll();
        $gameParty.gainGold(1234);
        const run = (cmd, args) => PluginManager.callCommand($gameMap._interpreter, "WD_Quest", cmd, args);
        run("newCreateQuest", {id: "1", icon: "87", cat: "0", short: "A Roof and a Meal", long: "A Roof and a Meal", index: "1",
            giver: "Tōdō Keiji", area: "Rabenau", desc: "The watch captain at the gate says the inn \"Zum Schwarzen Raben\" lies past the bridge, east of the square. Tell Hanamura Izumi that Tōdō sent you.",
            questTrans: "[]", status: "ongoing", logs: "[]", track: JSON.stringify({isTrackable: "true", text: "Find the inn in Rabenau.", textTrans: "[]"})});
        run("newCreateQuest", {id: "2", icon: "87", cat: "0", short: "Night Watch", long: "Night Watch", index: "2",
            giver: "Hanamura Izumi", area: "Rabenau", desc: "Stand the south fence with Tōdō until midnight.",
            questTrans: "[]", status: "completed", logs: "[]", track: JSON.stringify({isTrackable: "true", text: "", textTrans: "[]"})});
        SceneManager.push(Scene_Menu);
    });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Menu && SceneManager._scene.isStarted(), 20000);
    await h.frames(20);
    await h.shot("m_menu");
    await h.eval(() => { SceneManager.push(SceneManager.Scene_Quest); });
    await h.runUntil(() => SceneManager._scene && SceneManager._scene.constructor.name !== "Scene_Menu" && SceneManager._scene.isStarted(), 20000);
    await h.frames(20);
    await h.shot("m_quests");
    await h.eval(() => { const w = SceneManager._scene._windowLayer.children.find(c => c instanceof Window_Selectable && c.active); if (w) { w.select(0); w.callOkHandler && w.callOkHandler(); } });
    await h.frames(20);
    await h.shot("m_quest_detail");
    await h.eval(() => SceneManager.goto(Scene_Map));
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 20000);
    await h.eval(() => { SceneManager.push(Scene_Skill); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Skill && SceneManager._scene.isStarted(), 20000);
    await h.eval(() => { const s = SceneManager._scene; s._skillTypeWindow.select(0); s.commandSkill(); s._itemWindow.select(0); });
    await h.frames(20);
    await h.shot("m_skills");
    await h.eval(() => SceneManager.goto(Scene_Map));
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 20000);
    await h.eval(() => { window.__autoBattle = false; BattleManager.setup($dataTroops.findIndex(t => t && t.name === "Goblins & Thrower"), true, true); SceneManager.push(Scene_Battle); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Battle && SceneManager._scene.isStarted() && BattleManager._phase === "input", 20000);
    await h.frames(30);
    await h.shot("m_battle");
};
