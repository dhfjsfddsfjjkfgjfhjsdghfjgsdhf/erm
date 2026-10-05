// Visual check of Story_Core's message fit: shows a few of the widest face messages (Act I and Act III) and
// screenshots each once it is fully drawn. Look at the shots: no line may run past the window's right edge.
//   PORT=8124 WEBROOT=/home/claude/mz/sweb node tools/run_game.js tools/scen_msgfit.js <outdir>
const lib = require("./storylib.js");
const SAMPLES = [
    ["People1", 5, "Hanamura Izumi", ["Beds are upstairs, stew's on the fire. Rest when you like."]],
    ["Hanma", 0, "Hanma", ["Likely. We have nothing, my Lord. No coin, no food,",
                           "no blade but yours. A village is where we find all three."]],
    ["Actor3", 0, "Tōdō Keiji", ["The inn's past the bridge, east of the square: Hanamura's",
                                 "place, \"Zum Schwarzen Raben\". Tell her Tōdō sent you,",
                                 "and she won't throw you out before you've eaten."]],
    ["People4", 7, "Namiji Sayo", ["Five seals chain the Father of Monsters under the world.",
                                   "One in each god's holy place: the Abgrund, the Morgendom,",
                                   "the Hirschthron, two more. The Four were sent to break them."]],
    ["People3", 3, "Kaiserin Kujō Sayaka", ["Asahina Rin's letter asks me for a sword and for my",
                                             "legions. The sword, it seems, you have already taken back.",
                                             "Keep it. It was never mine; it was only in my vault."]],
    ["Actor1", 0, "Short", ["A short line stays at the normal size."]]
];

module.exports = async h => {
    await h.eval(lib);
    await h.eval(() => {
        window.__autoMsg = false;
        Game_Map.prototype.setupStartingEvent = function() { return false; };   // no map scenes in the way
        DataManager.setupNewGame();
        $gamePlayer.reserveTransfer(5, 13, 27, 2, 0);
        SceneManager.goto(Scene_Map);
    });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
        !$gamePlayer.isTransferring(), 20000);
    await h.run(120);
    const report = [];
    for (let i = 0; i < SAMPLES.length; i++) {
        await h.eval(([face, idx, name, lines]) => {
            $gameMessage.clear();
            $gameMessage.setFaceImage(face, idx);
            $gameMessage.setSpeakerName(name);
            for (const l of lines) $gameMessage.add(l);
        }, SAMPLES[i]);
        await h.until(() => {
            const w = SceneManager._scene._messageWindow;
            return w && w.isOpen() && w.pause;
        }, 30000);
        await h.frames(10);
        const r = await h.eval(() => {
            const w = SceneManager._scene._messageWindow;
            return { size: w.contents.fontSize, fit: w._storyFitSize, inner: w.innerWidth };
        });
        report.push(r);
        console.log("sample", i, JSON.stringify(SAMPLES[i][3][0].slice(0, 30)), JSON.stringify(r));
        await h.shot("msgfit_" + i);
        await h.eval(() => { window.__autoMsg = true; });
        await h.runUntil(() => !$gameMessage.isBusy() && SceneManager._scene._messageWindow.isClosed(), 2000);
        await h.eval(() => { window.__autoMsg = false; });
    }
    console.log("MSGFIT DONE");
};
