// Event sweep through chapters 5-9: enters each map (in story order, with an Act III party like
// scen_story_act3.js), lets the arrival scene play, then starts every event on the map that the player can
// trigger (action button or touch) one after another: messages auto-advance, choices take the first option,
// battles are auto-fought, shops are left at once. Reports engine errors and scenes that never end (a hang).
//   MAPS=75,76 PORT=8124 WEBROOT=/home/claude/mz/sweb node tools/run_game.js tools/scen_story_sweep.js
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches;
const ALL = [75, 76, 77, 78, 79, 80, 92, 90, 93, 91, 100, 101, 102, 103, 104, 105, 106, 107, 108,
             110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 130, 121, 122, 123, 124, 125];
const MAPS = process.env.MAPS ? process.env.MAPS.split(",").map(Number) : ALL;

module.exports = async h => {
    const hangs = [];
    // waits until the map is idle; leaves shops/menus/name input on its own. false = the scene never ended
    const idle = async (tag, limit = 20000) => {
        await h.run(20);
        for (let done = 0; done < limit; done += 200) {
            const st = await h.eval(() => {
                const s = SceneManager._scene;
                if (s instanceof Scene_Shop || s instanceof Scene_Menu || s instanceof Scene_Save || s instanceof Scene_Load ||
                    s instanceof Scene_Item || s instanceof Scene_Equip || s instanceof Scene_Status) {
                    if (!SceneManager.isSceneChanging()) SceneManager.pop();
                    return "busy";
                }
                if (s instanceof Scene_Gameover) { SceneManager.goto(Scene_Map); return "busy"; }
                const ok = s instanceof Scene_Map && s.isStarted() && !$gameMap.isEventRunning() &&
                    !$gamePlayer.isTransferring() && !$gameMessage.isBusy() && !SceneManager.isSceneChanging();
                return ok ? "idle" : s instanceof Scene_Title ? "title" : "busy";
            });
            if (st !== "busy") return st;
            await h.run(200);
            const errs = await h.eval(() => window.__errors.length);
            if (errs) throw new Error("game error at " + tag);
        }
        const d = await h.eval(() => ({ scene: SceneManager._scene && SceneManager._scene.constructor.name,
            map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y], msg: $gameMessage._texts.slice(0, 2),
            interp: $gameMap._interpreter._list ? [$gameMap._interpreter._eventId, $gameMap._interpreter._index,
                $gameMap._interpreter._waitMode, JSON.stringify($gameMap._interpreter.currentCommand()).slice(0, 200)] : null,
            msgs: window.__messages.slice(-4) }));
        console.log("  HANG", tag, JSON.stringify(d));
        hangs.push(tag);
        await h.shot("sweep_hang_" + hangs.length);
        // unstick and carry on
        await h.eval(() => {
            $gameMap._interpreter.clear();
            $gameMessage.clear();
            for (const e of $gameMap.events()) { e._moveRouteForcing = false; e._waitCount = 0; if (e._interpreter) e._interpreter.clear(); }
            $gamePlayer._moveRouteForcing = false;
            if (SceneManager._scene instanceof Scene_Battle) BattleManager.abort();
        });
        await h.run(60);
        return "hang";
    };

    await h.eval(lib);
    await h.eval(sws => {
        const _up = Window_ChoiceList.prototype.update;
        Window_ChoiceList.prototype.update = function() {
            _up.call(this);
            if (window.__autoMsg && this.active && this.isOpen() && !window.__choices.length) { this.select(0); this.processOk(); }
        };
        const _num = Window_NumberInput.prototype.update;
        Window_NumberInput.prototype.update = function() {
            _num.call(this);
            if (window.__autoMsg && this.active && this.isOpen()) this.processOk();
        };
        const _item = Window_EventItem.prototype.update;
        Window_EventItem.prototype.update = function() {
            _item.call(this);
            if (window.__autoMsg && this.active && this.isOpen()) this.processCancel();
        };
        DataManager.setupNewGame();
        for (const n of Object.keys(sws)) {
            if (/^(P|C1|C2|C3|A2|C4): /.test(n) || n === "Vessel Active") $gameSwitches.setValue(sws[n], true);
        }
        const k = $gameActors.actor(1), f = $gameActors.actor(3), y = $gameActors.actor(6);
        $gameParty.addActor(3);
        for (const [L, bt] of [[12, true], [20, true], [30, true], [37, true], [46, false]]) {
            k.changeLevel(L, false); f.changeLevel(L, false); spendAll(); Story.autoBuild(f);
            if (bt) { Story.breakthrough(true); spendAll(); Story.autoBuild(f); }
        }
        $gameParty.addActor(6); y.changeLevel(46, false); Story.autoBuild(y);
        $gameVariables.setValue(Story.P.pierceVar, 3);
        $gameParty.gainGold(5000000);
        window.__autoMsg = true;
        $gameMessage.clear();
        $gameParty.members().forEach(a => a.recoverAll());
        $gamePlayer.reserveTransfer(75, 30, 44, 8, 0);
        SceneManager.goto(Scene_Map);
    }, SW);
    await idle("start", 60000);

    let started = 0;
    for (const m of MAPS) {
        const [sx, sy] = ids.starts[String(m)];
        const go = async () => {
            await h.eval(([m, x, y]) => {
                window.__choices = [];
                $gameParty.members().forEach(a => a.recoverAll());
                $gamePlayer.reserveTransfer(m, x, y, 2, 0);
            }, [m, sx, sy]);
            return idle("enter " + m, 60000);
        };
        await go();
        const evs = await h.eval(() => $gameMap.events().filter(e => {
            const p = e.page();
            return p && p.list.length > 1 && [0, 1, 2].includes(p.trigger);
        }).map(e => [e.eventId(), e.event().name]));
        let n = 0;
        for (const [id, name] of evs) {
            if (await h.eval(() => $gameMap.mapId()) !== m) await go();
            const can = await h.eval(id => {
                const e = $gameMap.event(id);
                const p = e && e.page();
                if (!p || p.list.length <= 1 || ![0, 1, 2].includes(p.trigger) || e._erased) return false;
                $gameParty.members().forEach(a => a.recoverAll());
                e.start();
                return true;
            }, id);
            if (!can) continue;
            n++;
            await idle(`map ${m} event ${id} '${name}'`);
        }
        started += n;
        console.log(`  map ${m} ${ids.maps[m]}: ${n} events run`);
    }
    console.log("events run:", started, "hangs:", hangs.length);
    if (hangs.length) throw new Error("scenes that never ended: " + hangs.join(" | "));
    console.log("SWEEP PASSED");
};
