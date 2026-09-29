// Playthrough: Chapter 2 (from a prepared end-of-chapter-1 state).
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches;

module.exports = async h => {
    const idle = async () => {
        try {
            await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                !$gameMap.isEventRunning() && !$gamePlayer.isTransferring() && !$gameMessage.isBusy() &&
                !SceneManager.isSceneChanging(), 60000);
        } catch (e) {
            const d = await h.eval(() => ({ scene: SceneManager._scene && SceneManager._scene.constructor.name,
                map: $gameMap.mapId(), msg: $gameMessage._texts, choices: $gameMessage._choices,
                interp: $gameMap._interpreter._list ? [$gameMap._interpreter._eventId, $gameMap._interpreter._index,
                    $gameMap._interpreter._waitMode, JSON.stringify($gameMap._interpreter.currentCommand())] : null,
                troop: $gameTroop.members().map(e => e.name() + ":" + e.hp), msgs: window.__messages.slice(-8) }));
            console.log("IDLE TIMEOUT", JSON.stringify(d, null, 1));
            await h.shot("idle_timeout2");
            throw e;
        }
    };
    const sw = id => h.eval(id => $gameSwitches.value(id), id);
    const expect = async (cond, msg) => {
        if (!cond) {
            console.log("STATE", JSON.stringify(await h.eval(() => ({ map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y],
                msgs: __messages.slice(-10), battles: __battles.slice(-2), deaths: $gameVariables.value(2) }))));
            await h.shot("fail2_" + msg.replace(/\W+/g, "_"));
            throw new Error("expectation failed: " + msg);
        }
        console.log("  ok:", msg);
    };
    const talk = async (name, choices) => {
        await h.eval(([n, c]) => { window.__choices = c || []; startEvent(n); }, [name, choices]);
        await idle();
    };
    const go = async (mapId, x, y, d, choices) => {
        await h.eval(([m, x, y, d, c]) => { window.__choices = c || []; $gamePlayer.reserveTransfer(m, x, y, d || 2, 0); },
                     [mapId, x, y, d, choices]);
        await idle();
    };
    const heal = () => h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); });
    const state = async label => {
        const p = await h.eval(() => ({ map: $gameMap.mapId(), gold: $gameParty.gold(), time: Story.timeText(), date: Story.dateText(),
            party: party().map(a => a.name + " L" + a.lv + " " + a.hp + " " + a.stats), battles: __battles.slice(-2).map(b => b.troop + ":" + b.result + ":" + b.turns + "t " + JSON.stringify(b.hpEnd)) }));
        console.log("==", label, JSON.stringify(p));
    };

    await h.eval(lib);
    await h.eval(sws => {
        DataManager.setupNewGame();
        for (const n of ["Vessel Active", "P: Intro Done", "P: Left Cave", "P: Road", "C1: Arrived", "C1: Inn Deal", "C1: Raid Done",
                         "C1: Summoned", "C1: Tower Quest", "C1: Krummzahn Down", "C1: Rewarded", "C1: Sagara Hired"]) $gameSwitches.setValue(sws[n], true);
        $gameActors.actor(1).changeLevel(7, false);
        spendAll();
        $gameParty.gainGold(250);
        $gameParty.gainItem($dataItems.find(i => i && i.name === "Heiltrank"), 5);
        $gamePlayer.reserveTransfer(5, 13, 28, 8, 0);
        SceneManager.goto(Scene_Map);
    }, SW);
    await idle();
    await h.eval(() => { window.__choices = [0]; startEvent("South Gate"); });
    await idle();
    await expect(await sw(SW["C2: On the Road"]), "on the Oststraße");
    await h.shot("c2_oststrasse");
    await heal();
    await talk("Kamaitachi");
    await expect(await sw(SW["C2: Kamaitachi"]), "kamaitachi beaten");
    await heal();
    await talk("Toll", [1]);
    await expect(await sw(SW["C2: Deserters"]), "deserters beaten");
    await state("after deserters");
    await go(21, 10, 14, 8);
    await expect(await sw(SW["C2: Camp Night"]), "camp night");
    await go(22, 15, 27, 8);
    await expect(await sw(SW["C2: In Eisfurt"]), "arrived in Eisfurt");
    await h.shot("c2_eisfurt");
    await go(24, 8, 10, 8);
    await talk("Shirakawa Kaname");
    await go(22, 15, 18, 8);
    await talk("Wakaba Aika");
    await expect(await sw(SW["C2: Aika Told"]), "Aika told the story");
    await h.eval(() => { $gameActors.actor(1).changeLevel(8, false); });
    await h.eval(() => { window.__choices = [0]; startEvent("South Gate"); });
    await idle();
    await expect(await h.eval(() => $gameMap.mapId()) === 26, "on the Frostpfad");
    await h.shot("c2_frostpfad");
    await go(27, 5, 25, 8);
    await h.eval(() => $gamePlayer.locate(11, 9));
    await talk("Frost Shrine");
    await expect(await sw(SW["C2: Shrine Seen"]), "shrine seen");
    await go(28, 19, 36, 8);
    await h.shot("c2_eisfall");
    await h.eval(() => { $gameActors.actor(1).changeLevel(9, false); });
    await heal();
    await talk("Heart Passage");
    await expect(await sw(SW["C2: Eiswurm Down"]), "Eiswurm beaten");
    await state("after Eiswurm");
    await go(29, 5, 33, 8);
    await h.eval(() => { $gameActors.actor(1).changeLevel(10, false); });
    await heal();
    await talk("Fubuki");
    await expect(await sw(SW["C2: Fubuki Calmed"]), "Fubuki calmed");
    await expect(await sw(SW["C2: Thaw"]), "thaw");
    await state("after Fubuki");
    await h.shot("c2_thaw");
    await go(24, 8, 10, 8);
    await talk("Shirakawa Kaname");
    await expect(await sw(SW["C2: Vogt Paid"]), "Vogt paid");
    await go(22, 22, 22, 2);
    await talk("Ueda Ryō", [0]);
    await state("end of chapter 2");
    console.log("quests:", JSON.stringify(await h.eval(() => $gameSystem._questContainer.questsArray.map(q => q.id + ":" + q.status))));
};
