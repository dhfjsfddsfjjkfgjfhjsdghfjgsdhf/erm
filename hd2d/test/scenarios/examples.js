// Renders the README example scenes (forest, town, dungeon, night) on
// Erdenkreis maps. The map and event notes are injected while each map loads,
// exactly as they would be typed in the editor, and a screenshot is saved.
// QUERY="map=5&x=15&y=20&noevents=1"
const LAMP = "<HD2DLight: 170, #ffb060, 1.2, flicker 0.15>\n<HD2DEmissive: 1.2>";
const TORCH = "<HD2DLight: 180, #ff9a40, 1.4, flicker 0.35>\n<HD2DEmissive: 1.3>";
const CRYSTAL = "<HD2DLight: 120, #7fc8ff, 1.0>\n<HD2DEmissive: 1.6>";
const SCENES = {
    forest: { map: 3, x: 14, y: 9, note: "<HD2DPreset: Forest>", byImage: {} },
    town: { map: 5, x: 15, y: 19, note: "<HD2DPreset: Town>", byImage: { "!Flame": LAMP } },
    dungeon: {
        map: 70, x: 11, y: 9, note: "<HD2DPreset: Dungeon>\n<HD2DSet: shadows.occlusion=0.9>",
        byImage: { "!Flame": TORCH, "!Crystal": CRYSTAL }, walls: true, quality: "high"
    },
    night: { map: 41, x: 22, y: 37, note: "<HD2DPreset: Night>", byImage: { "!Flame": LAMP }, actor: "<HD2DLight: 120, #ffd9a0, 0.7, offsetY -6>" }
};

module.exports = async h => {
    await h.mapReady();
    await h.eval(() => {
        const onLoad = DataManager.onLoad;
        DataManager.onLoad = function(object) {
            onLoad.call(this, object);
            const scene = window.__scene;
            if (object === window.$dataMap && scene && $gamePlayer._newMapId === scene.map) {
                object.note = scene.note;
                for (const ev of object.events) {
                    const image = ev && ev.pages[0] && ev.pages[0].image.characterName;
                    if (image && scene.byImage[image]) ev.note = scene.byImage[image];
                }
            }
        };
    });
    const problems = [];
    for (const [name, scene] of Object.entries(SCENES)) {
        await h.eval(sc => {
            window.__scene = sc;
            HD2D.Params.wallsBlockLight = !!sc.walls;
            HD2D.setQuality(sc.quality || "medium");
            const actor = $dataActors[$gameParty.leader().actorId()];
            actor.note = sc.actor || "";
            actor._hd2dTags = null;
            $gamePlayer.reserveTransfer(sc.map, sc.x, sc.y, 2, 0);
        }, scene);
        await h.until(id => $gameMap.mapId() === id && SceneManager._scene.constructor === Scene_Map && SceneManager._scene.isStarted() && !$gamePlayer.isTransferring(), 60000, scene.map);
        await h.frames(80);
        const info = await h.eval(() => {
            const p = SceneManager._scene._spriteset._hd2dPipeline;
            return { preset: HD2D.State.data().preset, lights: HD2D.Lights.list.length, ok: !!p && !p.failed, err: HD2D.lastError && String(HD2D.lastError) };
        });
        console.log(name, JSON.stringify(info));
        if (!info.ok || info.err) problems.push(name + " " + JSON.stringify(info));
        await h.shot("example_" + name);
    }
    if (problems.length) throw new Error(problems.join("\n"));
};
