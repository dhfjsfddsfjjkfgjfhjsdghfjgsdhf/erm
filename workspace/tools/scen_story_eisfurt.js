// Eisfurt: the frozen-river layer before and after the thaw.
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
module.exports = async h => {
    const S = ids.switches;
    await h.eval(lib);
    await h.eval(S => {
        DataManager.setupNewGame();
        $gameSwitches.setValue(S["Vessel Active"], true);
        $gameSwitches.setValue(S["C2: In Eisfurt"], true);
        $gamePlayer.reserveTransfer(22, 20, 22, 2, 0);
        SceneManager.goto(Scene_Map);
    }, S);
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
        $gameMap.mapId() === 22 && !$gameMap.isEventRunning(), 20000);
    await h.eval(() => McKathlin.DayNightCycle && PluginManager.callCommand($gameMap._interpreter, "McKathlin_DayNight", "setTime", {time_of_day: JSON.stringify({hour: "12", minutes: "0", ampm: "PM"})}));
    await h.run(120);
    await h.frames(30);
    const before = await h.eval(() => {
        const s = SceneManager._scene._spriteset;
        return (s._tausiLighting_layerSprites || []).map(sp => ({ visible: sp.visible, w: sp.bitmap && sp.bitmap.width,
            ready: sp.bitmap && sp.bitmap.isReady(), x: sp.x, y: sp.y, parent: sp.parent === s._baseSprite }));
    });
    console.log("layers before:", JSON.stringify(before));
    await h.shot("eisfurt_frozen");
    await h.eval(S => $gameSwitches.setValue(S["C2: Thaw"], true), S);
    await h.run(30);
    await h.frames(30);
    const after = await h.eval(() => SceneManager._scene._spriteset._tausiLighting_layerSprites.map(sp => sp.visible));
    console.log("layers after:", JSON.stringify(after));
    await h.shot("eisfurt_thawed");
    // weather follows the map: snow on the Frostpfad, clear in the Eisfall, clear in thawed Eisfurt
    const weatherAt = async (id, x, y) => {
        await h.eval(([id, x, y]) => $gamePlayer.reserveTransfer(id, x, y, 2, 0), [id, x, y]);
        await h.runUntil(id => $gameMap.mapId() === id && !$gamePlayer.isTransferring(), 5000, id);
        return h.eval(() => $gameScreen.weatherType() + " " + $gameScreen.weatherPower());
    };
    const w1 = await weatherAt(26, 8, 21), w2 = await weatherAt(28, 19, 36), w3 = await weatherAt(22, 15, 27);
    await h.eval(S => $gameSwitches.setValue(S["C2: Thaw"], false), S);
    const w4 = await weatherAt(26, 8, 21), w5 = await weatherAt(22, 15, 27);
    console.log("weather frostpfad:", w1, "| eisfall:", w2, "| eisfurt thawed:", w3, "| eisfurt frozen:", w5);
    if (w1 !== "snow 6" || w2 !== "none 0" || w3 !== "none 0" || w5 !== "snow 5") throw new Error("weather wrong");
};
