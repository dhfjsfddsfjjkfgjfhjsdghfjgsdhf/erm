// Engine smoke run through chapters 5-9: every new map is entered with an Act III party, whatever runs on
// arrival plays out (messages auto-advance, choices take the first option, battles are auto-fought), and then the
// finale is played from Gōen's clearing through the Hirschthron and the epilogue to the title screen.
// Fails on any engine error, and on a scene that never ends.
//   bash tools/make_story_web.sh && WEBROOT=/home/claude/mz/sweb node tools/run_game.js tools/scen_story_act3.js
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches;
// in story order (the siege maps 92, 90, 93, 91 come in that order in chapter 6)
const MAPS = [75, 76, 77, 78, 79, 80, 92, 90, 93, 91, 100, 101, 102, 103, 104, 105, 106, 107, 108,
              110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 130, 121, 122, 123, 124, 125];

module.exports = async h => {
    const idle = async (tag, extra) => {
        try {
            await h.run(20);        // let a switch just set start its autorun before checking for idle
            await h.runUntil(x => (SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                !$gameMap.isEventRunning() && !$gamePlayer.isTransferring() && !$gameMessage.isBusy() &&
                !SceneManager.isSceneChanging()) || (x && SceneManager._scene instanceof Scene_Title), 60000, extra);
        } catch (e) {
            const d = await h.eval(() => ({ scene: SceneManager._scene && SceneManager._scene.constructor.name,
                map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y], msg: $gameMessage._texts,
                interp: $gameMap._interpreter._list ? [$gameMap._interpreter._eventId, $gameMap._interpreter._index,
                    $gameMap._interpreter._waitMode, JSON.stringify($gameMap._interpreter.currentCommand())] : null,
                msgs: window.__messages.slice(-8) }));
            console.log("IDLE TIMEOUT", tag || "", JSON.stringify(d, null, 1));
            await h.shot("act3_timeout_" + String(tag).replace(/\W+/g, "_"));
            throw e;
        }
    };

    await h.eval(lib);
    await h.eval(sws => {
        // choices: the scripted answer if there is one, else the first option
        const _up = Window_ChoiceList.prototype.update;
        Window_ChoiceList.prototype.update = function() {
            _up.call(this);
            if (window.__autoMsg && this.active && this.isOpen() && !window.__choices.length) {
                this.select(0);
                this.processOk();
            }
        };
        DataManager.setupNewGame();
        for (const n of Object.keys(sws)) {
            if (/^(P|C1|C2|C3|A2|C4): /.test(n) || n === "Vessel Active") $gameSwitches.setValue(sws[n], true);
        }
        const k = $gameActors.actor(1), f = $gameActors.actor(3), y = $gameActors.actor(6);
        $gameParty.addActor(3);
        for (const [L, bt] of [[12, true], [20, true], [30, true], [37, true], [46, false]]) {
            k.changeLevel(L, false);
            f.changeLevel(L, false);
            spendAll();
            Story.autoBuild(f);
            if (bt) {
                Story.breakthrough(true);
                spendAll();
                Story.autoBuild(f);
            }
        }
        $gameParty.addActor(6);
        y.changeLevel(46, false);
        Story.autoBuild(y);
        $gameVariables.setValue(Story.P.pierceVar, 3);
        $gameParty.gainGold(5000000);
        window.__autoMsg = true;
        $gameMessage.clear();
        $gameParty.members().forEach(a => a.recoverAll());
        $gamePlayer.reserveTransfer(75, 30, 44, 8, 0);
        SceneManager.goto(Scene_Map);
    }, SW);
    await idle("start");
    console.log("party:", JSON.stringify(await h.eval(() => party().map(a => a.name + " L" + a.lv + " " + a.rank))));

    // ---------------------------------------------------------------- every map of chapters 5-9
    for (const m of MAPS) {
        const [x, yy] = ids.starts[String(m)];
        await h.eval(([m, x, y]) => {
            window.__choices = [];
            $gameParty.members().forEach(a => a.recoverAll());
            $gamePlayer.reserveTransfer(m, x, y, 2, 0);
        }, [m, x, yy]);
        await idle("map " + m);
        const now = await h.eval(() => [$gameMap.mapId(), $gamePlayer.x, $gamePlayer.y, $gameMap.events().length]);
        console.log(`  ok: map ${m} ${ids.maps[m]} (now on map ${now[0]} at ${now[1]},${now[2]}, ${now[3]} events)`);
        if (m % 5 === 0) await h.shot("act3_map_" + m);
    }
    console.log("battles so far:", JSON.stringify(await h.eval(() => __battles.map(b => b.troop + ":" + b.result))));

    // ---------------------------------------------------------------- the finale, fast
    // (bosses get 60 HP here: this run checks the scenes, the breakthrough, the three phases and the epilogue;
    //  scen_story_bal2.js with the ch.9 settings checks how hard the fights are)
    await h.eval(sw => {
        for (const e of $dataEnemies) if (e && /Gōen|Kagerō|Hōkai|Tōma/.test(e.name)) e.params[0] = 60;
        $gameVariables.setValue(Story.P.pierceVar, 4);
        $gameSwitches.setValue(sw["C9: Shigure Down"], true);
        $gameSwitches.setValue(sw["C9: Urwald Burns"], true);
        $gameParty.members().forEach(a => a.recoverAll());
        window.__choices = [];
        $gamePlayer.reserveTransfer(124, 20, 1, 2, 0);
    }, SW);
    await idle("burning Urwald");
    await h.eval(sw => $gameSwitches.setValue(sw["C9: Clearing (go)"], true), SW);
    await idle("Gōen");
    const gate = await h.eval(sw => [$gameSwitches.value(sw["C9: Goen Down"]), $gameVariables.value(1),
                                     $gameSwitches.value(sw["C9: Breakthrough A"])], SW);
    console.log("  Gōen down / gate / breakthrough A:", JSON.stringify(gate));
    if (!gate[0] || gate[1] < 5 || !gate[2]) throw new Error("Gōen's fight did not end with the breakthrough to A");
    await h.eval(() => $gamePlayer.reserveTransfer(125, 16, 1, 2, 0));
    await idle("Hirschthron");
    await h.eval(sw => $gameSwitches.setValue(sw["C9: The Throne (go)"], true), SW);
    await idle("the end", true);
    const end = await h.eval(sw => [SceneManager._scene.constructor.name, $gameSwitches.value(sw["Game Cleared"]),
                                    $gameParty.members().map(a => a.name())], SW);
    console.log("  finale:", JSON.stringify(end));
    if (end[0] !== "Scene_Title" || !end[1]) throw new Error("the finale did not reach the title screen");
    console.log("messages at the end:", JSON.stringify(await h.eval(() => __messages.slice(-6))));
    console.log("ACT III SMOKE RUN PASSED");
};
