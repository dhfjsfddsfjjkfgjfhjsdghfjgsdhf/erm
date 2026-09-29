// Playthrough: Prologue and Chapter 1 (fast-forwarded), with checks.
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches, V = ids.variables;

module.exports = async h => {
    const idle = async () => {
        try {
            await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                !$gameMap.isEventRunning() && !$gamePlayer.isTransferring() && !$gameMessage.isBusy() &&
                !SceneManager.isSceneChanging(), 40000);
        } catch (e) {
            const d = await h.eval(() => ({ scene: SceneManager._scene && SceneManager._scene.constructor.name,
                phase: BattleManager._phase, msg: $gameMessage.isBusy(), texts: $gameMessage._texts,
                choices: $gameMessage._choices, running: $gameMap.isEventRunning(),
                interp: $gameMap._interpreter._list ? [$gameMap._interpreter._eventId, $gameMap._interpreter._index,
                    $gameMap._interpreter._waitMode, JSON.stringify($gameMap._interpreter.currentCommand())] : null,
                troop: $gameTroop.members().map(e => e.name() + ":" + e.hp), party: $gameParty.members().map(a => a.name() + ":" + a.hp),
                log: SceneManager._scene._logWindow ? SceneManager._scene._logWindow._lines.slice(-6) : null,
                msgs: window.__messages.slice(-6) }));
            console.log("IDLE TIMEOUT", JSON.stringify(d, null, 1));
            await h.shot("idle_timeout");
            throw e;
        }
    };
    const sw = id => h.eval(id => $gameSwitches.value(id), id);
    const expect = async (cond, msg) => {
        if (!cond) {
            console.log("STATE", JSON.stringify(await h.eval(() => ({ map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y],
                msgs: __messages.slice(-12), battles: __battles.slice(-2), deaths: $gameVariables.value(2) }))));
            await h.shot("fail_" + msg.replace(/\W+/g, "_"));
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
    const state = async label => {
        const p = await h.eval(() => ({ map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y], gold: $gameParty.gold(),
            time: Story.timeText(), party: party(), battles: __battles.slice(-3) }));
        console.log("==", label, JSON.stringify(p));
        return p;
    };

    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await idle();
    await expect(await sw(SW["P: Intro Done"]), "opening ran");
    await h.eval(() => spendAll());
    await state("after intro");

    // the two-tail: bow
    await h.eval(() => $gamePlayer.locate(5, 13));
    await talk("Two-Tail", [0]);
    await expect(await sw(SW["P: Two-Tail Bowed"]), "bowed to the two-tail");
    await talk("Drip Pool", [0]);
    await talk("Herbs");
    await h.shot("c1_cave");
    // out to the ridge
    await go(2, 12, 9, 2, [0]);
    await expect(await sw(SW["P: Road"]), "chose the road");
    await h.shot("c1_ridge");
    // the road: crows
    await go(3, 1, 9, 6);
    await talk("Crows");
    await expect(await sw(SW["P: Crows"]), "crow fight done");
    await state("after crows");
    await h.eval(() => spendAll());
    // Rabenau
    await go(5, 13, 28, 8);
    await expect(await sw(SW["C1: Arrived"]), "arrived in Rabenau");
    await h.shot("c1_rabenau");
    await go(6, 9, 13, 8);
    await talk("Hanamura Izumi", [0]);
    await expect(await sw(SW["C1: Inn Deal"]), "inn deal");
    await go(5, 13, 25, 2);
    await h.eval(() => { $gameActors.actor(1).changeLevel(2, false); spendAll(); });
    await talk("Tōdō", [0]);
    await expect(await sw(SW["C1: Raid Done"]), "raid done");
    await expect(await sw(SW["C1: Summoned"]), "summoned by the elder");
    await state("morning after the raid");
    await h.shot("c1_morning");
    // the elder
    await go(7, 5, 11, 8);
    await h.eval(() => $gamePlayer.locate(10, 10));
    await talk("Okuda Noboru");
    await expect(await sw(SW["C1: Tower Quest"]), "tower quest");
    // piglet in the village
    await go(5, 21, 8, 8);
    await h.eval(() => { const e = evByName("Piglet (village)"); if (e) e.start(); });
    await idle();
    // the Rabenholz, with some fights on the way
    await h.eval(() => { $gameActors.actor(1).changeLevel(3, false); spendAll(); });
    await go(11, 15, 26, 8);
    for (let i = 0; i < 3; i++) {
        await h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); BattleManager.setup($dataTroops.findIndex(t => t && t.name === "Goblins x2"), true, true); SceneManager.push(Scene_Battle); });
        await idle();
    }
    await state("after 3 wood fights");
    await h.eval(() => { const e = evByName("Piglet (Rabenholz)"); if (e) e.start(); });
    await idle();
    await go(12, 3, 5, 6);
    for (let i = 0; i < 3; i++) {
        await h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); BattleManager.setup($dataTroops.findIndex(t => t && t.name === "Goblins & Thrower"), true, true); SceneManager.push(Scene_Battle); });
        await idle();
    }
    await h.eval(() => { const e = evByName("Piglet (deep wood)"); if (e) e.start(); });
    await idle();
    await h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); });
    await talk("Sentry");
    await expect(await sw(SW["C1: Sentries"]), "sentries beaten");
    await go(13, 12, 21, 8);
    await h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); });
    await talk("Stair Guard");
    await expect(await sw(SW["C1: Stair Guards"]), "stair guards beaten");
    await state("before the boss");
    await go(14, 3, 7, 6);
    await h.eval(() => { if ($gameActors.actor(1).level < 5) $gameActors.actor(1).changeLevel(5, false); spendAll(); $gameParty.members().forEach(a => a.recoverAll()); });
    await talk("Krummzahn");
    await h.shot("c1_boss_after");
    const boss = await state("after the boss");
    await expect(await sw(SW["C1: Krummzahn Down"]), "Krummzahn beaten");
    // back to the elder, reward, Sagara
    await go(7, 10, 10, 8);
    await talk("Okuda Noboru");
    await expect(await sw(SW["C1: Rewarded"]), "rewarded");
    await go(5, 9, 12, 8);
    await talk("Natsu");
    await expect(await sw(SW["C1: Piglets Home"]), "piglets home");
    await go(6, 7, 8, 8);
    await talk("Sagara Takumi", [0]);
    await expect(await sw(SW["C1: Sagara Hired"]), "Sagara hired");
    await state("end of chapter 1");
    const quests = await h.eval(() => $gameSystem._questContainer.questsArray.map(q => q.id + ":" + q.shortTitle + ":" + q.status));
    console.log("quests:", JSON.stringify(quests));
    console.log("battles:", JSON.stringify(await h.eval(() => __battles.map(b => b.troop + ":" + b.result + ":" + b.turns + "t"))));
};
