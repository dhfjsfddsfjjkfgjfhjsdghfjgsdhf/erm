// Playthrough: Chapter 4 (Die Wallfeste), from a prepared end-of-Act-II-opening state.
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches, VAR = ids.variables;
const M = { FRONT: 61, WALLWEG: 63, WALLFESTE: 64, HALL: 65, KASERNE: 66, LAZARETT: 67, ZEUGHAUS: 68, FP5: 69, ZISTERNE: 70 };

module.exports = async h => {
    const idle = async (tag) => {
        try {
            await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                !$gameMap.isEventRunning() && !$gamePlayer.isTransferring() && !$gameMessage.isBusy() &&
                !SceneManager.isSceneChanging(), 120000);
        } catch (e) {
            const d = await h.eval(() => ({ scene: SceneManager._scene && SceneManager._scene.constructor.name,
                map: $gameMap.mapId(), msg: $gameMessage._texts, choices: $gameMessage._choices,
                interp: $gameMap._interpreter._list ? [$gameMap._interpreter._eventId, $gameMap._interpreter._index,
                    $gameMap._interpreter._waitMode, JSON.stringify($gameMap._interpreter.currentCommand())] : null,
                troop: $gameTroop.members().map(e => e.name() + ":" + e.hp), msgs: window.__messages.slice(-8) }));
            console.log("IDLE TIMEOUT", tag || "", JSON.stringify(d, null, 1));
            await h.shot("idle_timeout4");
            throw e;
        }
    };
    const sw = name => h.eval(id => $gameSwitches.value(id), SW[name]);
    const expect = async (cond, msg) => {
        if (!cond) {
            console.log("STATE", JSON.stringify(await h.eval(() => ({ map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y],
                msgs: __messages.slice(-12), battles: __battles.slice(-3), deaths: $gameVariables.value(2) }))));
            await h.shot("fail4_" + msg.replace(/\W+/g, "_"));
            throw new Error("expectation failed: " + msg);
        }
        console.log("  ok:", msg);
    };
    const talk = async (name, choices) => {
        await h.eval(([n, c]) => { window.__choices = c || []; startEvent(n); }, [name, choices]);
        await idle(name);
    };
    const go = async (mapId, x, y, d, choices) => {
        await h.eval(([m, x, y, d, c]) => { window.__choices = c || []; $gamePlayer.reserveTransfer(m, x, y, d || 2, 0); },
                     [mapId, x, y, d, choices]);
        await idle("go " + mapId);
    };
    const heal = () => h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); });
    const state = async label => {
        const p = await h.eval(() => ({ map: $gameMap.mapId(), gold: $gameParty.gold(), time: Story.timeText(),
            gate: $gameVariables.value(1),
            party: party().map(a => a.name + " L" + a.lv + " " + a.rank + " " + a.hp + " " + a.stats + " pts" + a.pts),
            battles: __battles.slice(-4).map(b => b.troop + ":" + b.result + ":" + b.turns + "t " + JSON.stringify(b.hpEnd)) }));
        console.log("==", label, JSON.stringify(p));
    };

    await h.eval(lib);
    await h.eval(sws => {
        DataManager.setupNewGame();
        for (const n of Object.keys(sws)) if (/^(P|C1|C2|C3|A2): /.test(n) || n === "Vessel Active") $gameSwitches.setValue(sws[n], true);
        const k = $gameActors.actor(1), hn = $gameActors.actor(2), f = $gameActors.actor(3);
        k.changeLevel(12, false); spendAll(); Story.breakthrough(true);
        k.changeLevel(16, false); spendAll();
        $gameParty.addActor(3); f.changeLevel(16, false); Story.autoBuild(f);
        $gameMessage.clear();
        $gameParty.gainGold(2500);
        const item = n => $dataItems.find(i => i && i.name === n);
        $gameParty.gainItem(item("Heiltrank"), 6);
        $gameParty.gainItem(item("Großer Heiltrank"), 4);
        $gameParty.gainItem(item("Gildenkarte"), 1);
        $gameParty.members().forEach(a => a.recoverAll());
        $gamePlayer.reserveTransfer(61, 16, 32, 8, 0);
        SceneManager.goto(Scene_Map);
    }, SW);
    await idle("start");
    await state("start (Act II opening done)");

    // ---------------------------------------------------------------- the Wallweg
    await talk("South Gate", [0]);
    await expect(await h.eval(() => $gameMap.mapId()) === M.WALLWEG && await sw("C4: On the Wallweg"), "on the Wallweg");
    await h.shot("c4_wallweg");
    await talk("Bridge North");
    await expect(await sw("C4: Courier Saved"), "hellhound beaten, courier saved");
    await heal();
    await talk("Gate Tunnel");
    await expect(await h.eval(() => $gameMap.mapId()) === M.WALLFESTE && await sw("C4: At the Wallfeste"), "arrived at the Wallfeste");
    await h.shot("c4_wallfeste");

    // ---------------------------------------------------------------- the audience
    await talk("Keep Gate");
    await expect(await sw("C4: Audience Done"), "audience with Kōsaka and Rin");
    await h.shot("c4_hall");
    await state("after the audience");

    // ---------------------------------------------------------------- clues
    await go(M.LAZARETT, 3, 9, 6);
    await talk("Yukimura Saki");
    await expect(await sw("C4: Clue Coin"), "clue: the brass coin");
    await go(M.ZEUGHAUS, 11, 12, 8);
    await talk("Nishiki Eiji", [1]);
    await expect(await sw("C4: Nishiki Gone"), "Nishiki ran");
    await talk("Ledger");
    await expect(await sw("C4: Clue Ledger"), "clue: the ledger and the key");
    await go(M.WALLFESTE, 33, 10, 8);
    await talk("Sentry Kazama");
    await expect(await sw("C4: Clue Lights"), "clue: lights under the ice");
    await expect(await h.eval(v => $gameVariables.value(v), VAR["C4: Clues"]) === 3, "3 clues");

    // ---------------------------------------------------------------- Frontposten 5 (optional)
    await go(M.WALLFESTE, 33, 6, 8);
    await talk("North Gate", [0]);
    await expect(await h.eval(() => $gameMap.mapId()) === M.FP5, "at Frontposten 5");
    await heal();
    await talk("Gargoyle");
    await heal();
    await talk("Hellhound");
    await heal();
    await talk("Top");
    await expect(await sw("C4: FP5 Relieved"), "Frontposten 5 relieved");
    await state("after Frontposten 5");
    await go(M.HALL, 12, 7, 8);
    await talk("Kōsaka (talk)");
    await expect(await sw("C4: FP5 Paid"), "Kōsaka pays for Frontposten 5");

    // ---------------------------------------------------------------- the cistern and the night raid
    await heal();
    await go(M.WALLFESTE, 28, 15, 8);
    await talk("Cistern Shaft", [0]);
    await expect(await h.eval(() => $gameMap.mapId()) === M.ZISTERNE, "down in the cistern");
    await h.shot("c4_cistern");
    await heal();
    await talk("Circle");
    await expect(await sw("C4: Scribe Down"), "Messingschreiber beaten");
    await idle("raid");
    await expect(await sw("C4: Raid Over"), "night raid survived");
    await expect(await h.eval(() => $gameVariables.value(1)) === 2, "breakthrough to D");
    await expect(await sw("C4: Chapter Done"), "chapter 4 done (writ, quest Weißenfels)");
    const k = await h.eval(() => {
        const a = $gameActors.actor(1);
        return { weapon: a.weapons()[0].name, armor: a.armors().find(x => x.etypeId === 4).name,
                 skills: a.skills().map(s => s.name), falin: $gameActors.actor(3).armors()[0].name,
                 hanma: $gameActors.actor(2).armors()[0].name, items: $gameParty.items().map(i => i.name) };
    });
    console.log(JSON.stringify(k));
    await expect(k.skills.includes("Radiant Edge") && k.skills.includes("Lance Charge"), "Kanta learned Radiant Edge and Lance Charge");
    await expect(k.falin.endsWith(" D") && k.hanma.endsWith(" D"), "rank D gear for Falin and Hanma");
    await h.shot("c4_morning");
    await state("end of chapter 4");
    console.log("battles:", JSON.stringify(await h.eval(() => __battles.map(b => b.troop + ":" + b.result + ":" + b.turns + "t"))));
};
