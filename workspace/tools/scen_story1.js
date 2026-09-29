// Story smoke test: new game, the opening, the cave (lights), stat points, walk to the exit.
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./pagelib.js");
module.exports = async h => {
    await h.eval(lib);
    await h.eval(() => { window.__autoMsg = true; DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await h.until(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 30000);
    await h.shot("s1_start");
    const intro = ids.switches["P: Intro Done"];
    await h.runUntil(id => $gameSwitches.value(id) && !$gameMap.isEventRunning(), 6000, intro);
    await h.frames(10);
    await h.shot("s1_after_intro");
    const info = await h.eval(() => ({
        lighting: !!(window.$dataLighting && $dataLighting.maps),
        lightObjs: $dataLighting && $dataLighting.getCurrentMap ? $dataLighting.getCurrentMap().objects.length : -1,
        time: McKathlin.DayNightCycle.getHours() + ":" + McKathlin.DayNightCycle.getMinutes(),
        date: Story.dateText(),
        party: $gameParty.members().map(a => a.name() + " L" + a.level + " " + a.rkRank() + " pts" + a.rkPoints()),
        weapon: $gameActors.actor(1).weapons().map(w => w.name),
        quest: typeof window.WD_Interplugin_Core,
        msgs: window.__messages.slice(0, 40)
    }));
    console.log(JSON.stringify(info, null, 1));
};
