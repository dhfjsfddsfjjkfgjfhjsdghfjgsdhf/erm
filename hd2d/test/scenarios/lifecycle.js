// Scene lifecycle: battle and back, save/load persistence, map transfer with a
// preset cross-fade, and an Effekseer animation drawn unlit.
// Erdenkreis: QUERY="map=5&x=15&y=20&noevents=1" (uses troop 1, animation 41, map 1).
module.exports = async h => {
    const problems = [];
    const expect = (label, cond, info) => {
        if (!cond) problems.push(label + " " + JSON.stringify(info));
    };
    const health = () => h.eval(() => {
        const s = SceneManager._scene;
        const p = s._spriteset && s._spriteset._hd2dPipeline;
        return { scene: s.constructor.name, map: $gameMap.mapId(), ok: !!p && !p.failed, err: HD2D.lastError ? String(HD2D.lastError) : null };
    });
    await h.mapReady();

    // Battle and back.
    await h.eval(() => {
        BattleManager.setup(1, true, true);
        SceneManager.push(Scene_Battle);
    });
    await h.until(() => SceneManager._scene.constructor === Scene_Battle && SceneManager._scene.isStarted(), 60000);
    await h.frames(30);
    expect("battle post filter", await h.eval(() => {
        const ss = SceneManager._scene._spriteset;
        return !!ss._hd2dPost && (ss._hd2dPost.filters || []).length > 0;
    }), null);
    await h.shot("lifecycle_battle");
    await h.eval(() => {
        $gameMessage.clear();
        BattleManager.processAbort();
    });
    await h.until(() => SceneManager._scene.constructor === Scene_Map && SceneManager._scene.isStarted(), 60000);
    await h.frames(20);
    let s = await health();
    expect("map after battle", s.ok && !s.err, s);

    // Save, change everything, load.
    await h.eval(() => {
        HD2D.setPreset("Night");
        HD2D.set("bloom.intensity", 0.9);
        HD2D.Camera.setZoom(1.3);
        HD2D.addLight({ id: "keep", attach: "player", radius: 200 });
    });
    await h.frames(10);
    const saved = await h.eval(async () => {
        $gameSystem.onBeforeSave();
        return DataManager.saveGame(1).then(() => true, e => String(e));
    });
    expect("save", saved === true, saved);
    await h.eval(() => {
        HD2D.setPreset("HD2D");
        HD2D.Camera.setZoom(1);
        HD2D.removeLight("keep");
    });
    await h.frames(5);
    await h.eval(async () => {
        await DataManager.loadGame(1);
        $gamePlayer.reserveTransfer($gameMap.mapId(), $gamePlayer.x, $gamePlayer.y);
        SceneManager.goto(Scene_Map);
    });
    await h.until(() => SceneManager._scene.constructor === Scene_Map && SceneManager._scene.isStarted() && !$gamePlayer.isTransferring(), 60000);
    await h.frames(30);
    const loaded = await h.eval(() => ({ preset: HD2D.State.data().preset, bloom: HD2D.get("bloom.intensity"), zoom: HD2D.Camera.zoom(), lights: Object.keys(HD2D.State.data().lights) }));
    expect("state restored by load", loaded.preset === "Night" && Math.abs(loaded.bloom - 0.9) < 1e-6 && Math.abs(loaded.zoom - 1.3) < 1e-6 && loaded.lights.includes("keep"), loaded);
    await h.shot("lifecycle_loaded");

    // Transfer: the look cross-fades to the next map's preset.
    await h.eval(() => {
        HD2D.Camera.setZoom(1);
        $gamePlayer.reserveTransfer(1, 12, 12, 2, 2);
    });
    await h.until(() => $gameMap.mapId() === 1 && SceneManager._scene.constructor === Scene_Map && SceneManager._scene._spriteset, 60000);
    const trans = await h.eval(() => HD2D.State.data().trans);
    expect("preset cross-fade on transfer", trans && trans.dur > 0, trans);
    await h.until(() => SceneManager._scene.isStarted() && !HD2D.State.data().trans, 60000);
    await h.frames(20);
    s = await health();
    expect("map after transfer", s.ok && !s.err, s);

    // Animation: drawn in the unlit overlay, removed when finished.
    await h.eval(() => $gameTemp.requestAnimation([$gamePlayer], 41));
    await h.frames(25);
    const playing = await h.eval(() => SceneManager._scene._spriteset._hd2dUnlit.children.filter(c => c instanceof Sprite_Animation).length);
    expect("animation drawn unlit", playing === 1, playing);
    await h.shot("lifecycle_animation");
    await h.frames(150);
    const left = await h.eval(() => SceneManager._scene._spriteset._hd2dUnlit.children.filter(c => c instanceof Sprite_Animation).length);
    expect("animation cleaned up", left === 0, left);
    s = await health();
    expect("map after animation", s.ok && !s.err, s);

    if (problems.length) throw new Error(problems.length + " problem(s):\n" + problems.join("\n"));
    console.log("lifecycle ok");
};
