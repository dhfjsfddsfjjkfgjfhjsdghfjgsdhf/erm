// Renders whole maps (sample maps or built maps) with the real MZ engine.
// usage: MAPS=208,211 node tools/run_game.js tools/scen_render.js <outdir>
// Writes <outdir>/map<id>.png at 48 px per tile (player hidden).
const fs = require("fs");
const path = require("path");
module.exports = async h => {
    const ids = (process.env.MAPS || "1").split(",").map(Number);
    await h.eval(() => {
        // missing images must not stop the render
        ImageManager.throwLoadError = function(bitmap) {
            bitmap._loadingState = "none";
        };
        // no cutscenes while rendering
        Game_Map.prototype.setupStartingEvent = function() { return false; };
        Game_Event.prototype.updateParallel = function() {};
        Game_Map.prototype.autoplay = function() {};
        DataManager.setupNewGame();
        $gamePlayer.setTransparent(true);
        $gamePlayer._followers.hide && $gamePlayer._followers.hide();
        window.__errors = [];
    });
    for (const id of ids) {
        const size = await h.eval(id => {
            window.__renderReady = false;
            return new Promise(resolve => {
                const xhr = new XMLHttpRequest();
                xhr.open("GET", "data/Map" + String(id).padStart(3, "0") + ".json");
                xhr.onload = () => {
                    const m = JSON.parse(xhr.responseText);
                    resolve([m.width, m.height]);
                };
                xhr.send();
            });
        }, id);
        const [w, hgt] = size;
        await h.eval(([id, w, hgt]) => {
            Graphics.resize(w * 48, hgt * 48);
            $gamePlayer.reserveTransfer(id, 0, 0, 2, 2);
            $gamePlayer.setTransparent(true);
            if (!(SceneManager._scene instanceof Scene_Map)) SceneManager.goto(Scene_Map);
        }, [id, w, hgt]);
        await h.until(id => {
            const s = SceneManager._scene;
            return s instanceof Scene_Map && s.isStarted() && $gameMap.mapId() === id &&
                !$gamePlayer.isTransferring() && ImageManager.isReady() && s._spriteset;
        }, 60000, id);
        await h.eval(() => {
            $gameMap.setDisplayPos(0, 0);
            $gameScreen.clearTone && $gameScreen.startTint([0, 0, 0, 0], 1);
            $gameMap._interpreter.clear && $gameMap._interpreter.clear();
        });
        await h.frames(6);
        const data = await h.eval(() => {
            const scene = SceneManager._scene;
            // hide windows (map name etc.)
            if (scene._mapNameWindow) scene._mapNameWindow.visible = false;
            if (scene._windowLayer) scene._windowLayer.visible = false;
            const b = Bitmap.snap(scene);
            if (scene._windowLayer) scene._windowLayer.visible = true;
            return b.canvas.toDataURL("image/png");
        });
        const file = path.join(h.out, "map" + id + ".png");
        fs.writeFileSync(file, Buffer.from(data.split(",")[1], "base64"));
        console.log("rendered", id, w + "x" + hgt, file);
    }
};
