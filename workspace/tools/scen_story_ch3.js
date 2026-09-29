// Playthrough: Chapter 3 and the Act II opening (from a prepared end-of-chapter-2 state).
const ids = require("/home/claude/mz/story/out/ids.json");
const lib = require("./storylib.js");
const SW = ids.switches, VAR = ids.variables;
const M = { EISFURT: 22, KOENIG: 40, WACHTBURG: 41, GILDE: 42, KAJI: 44, KORN: 46, NORD: 47, WOLF: 48,
            WALL: 60, FRONT: 61, BRESCHE: 62 };

module.exports = async h => {
    const idle = async () => {
        try {
            await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                !$gameMap.isEventRunning() && !$gamePlayer.isTransferring() && !$gameMessage.isBusy() &&
                !SceneManager.isSceneChanging(), 90000);
        } catch (e) {
            const d = await h.eval(() => ({ scene: SceneManager._scene && SceneManager._scene.constructor.name,
                map: $gameMap.mapId(), msg: $gameMessage._texts, choices: $gameMessage._choices,
                interp: $gameMap._interpreter._list ? [$gameMap._interpreter._eventId, $gameMap._interpreter._index,
                    $gameMap._interpreter._waitMode, JSON.stringify($gameMap._interpreter.currentCommand())] : null,
                troop: $gameTroop.members().map(e => e.name() + ":" + e.hp), msgs: window.__messages.slice(-8) }));
            console.log("IDLE TIMEOUT", JSON.stringify(d, null, 1));
            await h.shot("idle_timeout3");
            throw e;
        }
    };
    const sw = name => h.eval(id => $gameSwitches.value(id), SW[name]);
    const expect = async (cond, msg) => {
        if (!cond) {
            console.log("STATE", JSON.stringify(await h.eval(() => ({ map: $gameMap.mapId(), pos: [$gamePlayer.x, $gamePlayer.y],
                msgs: __messages.slice(-12), battles: __battles.slice(-2), deaths: $gameVariables.value(2) }))));
            await h.shot("fail3_" + msg.replace(/\W+/g, "_"));
            throw new Error("expectation failed: " + msg);
        }
        console.log("  ok:", msg);
    };
    const talk = async (name, choices) => {
        await h.eval(([n, c]) => { window.__choices = c || []; startEvent(n); }, [name, choices]);
        await idle();
    };
    const startAll = async name => {
        const n = await h.eval(name => {
            const evs = $gameMap.events().filter(e => e.event().name === name && e.page() && e.list().length > 1);
            return evs.map(e => e.eventId());
        }, name);
        for (const id of n) {
            await h.eval(id => { window.__choices = []; startEvent(id); }, id);
            await idle();
        }
        return n.length;
    };
    const go = async (mapId, x, y, d, choices) => {
        await h.eval(([m, x, y, d, c]) => { window.__choices = c || []; $gamePlayer.reserveTransfer(m, x, y, d || 2, 0); },
                     [mapId, x, y, d, choices]);
        await idle();
    };
    const fight = async troop => {
        await h.eval(t => {
            const id = $dataTroops.findIndex(x => x && x.name === t);
            BattleManager.setup(id, true, false);
            BattleManager.setEventCallback(() => {});
            SceneManager.push(Scene_Battle);
        }, troop);
        await idle();
        const b = await h.eval(() => __battles[__battles.length - 1]);
        return b.result;
    };
    const heal = () => h.eval(() => { spendAll(); $gameParty.members().forEach(a => a.recoverAll()); });
    const state = async label => {
        const p = await h.eval(() => ({ map: $gameMap.mapId(), gold: $gameParty.gold(), time: Story.timeText(), date: Story.dateText(),
            gate: $gameVariables.value(1),
            party: party().map(a => a.name + " L" + a.lv + " " + a.rank + " " + a.hp + " " + a.stats + " pts" + a.pts),
            battles: __battles.slice(-3).map(b => b.troop + ":" + b.result + ":" + b.turns + "t " + JSON.stringify(b.hpEnd)) }));
        console.log("==", label, JSON.stringify(p));
    };

    await h.eval(lib);
    await h.eval(sws => {
        DataManager.setupNewGame();
        for (const n of Object.keys(sws)) if (/^(P|C1|C2): /.test(n) || n === "Vessel Active") $gameSwitches.setValue(sws[n], true);
        $gameActors.actor(1).changeLevel(12, false);
        spendAll();
        $gameParty.gainGold(490);
        const item = n => $dataItems.find(i => i && i.name === n);
        $gameParty.gainItem(item("Heiltrank"), 5);
        $gameParty.gainItem(item("Brief an die Gilde"), 1);
        $gameParty.gainItem(item("Schwarze Rabenfeder"), 1);
        $gamePlayer.reserveTransfer(22, 21, 23, 6, 0);
        SceneManager.goto(Scene_Map);
    }, SW);
    await idle();
    await state("start (end of chapter 2)");

    // ---------------------------------------------------------------- across the river
    await talk("Ueda Ryō", [0]);
    await expect(await sw("C3: Across the River"), "crossed to the Königsstraße");
    await h.shot("c3_koenigsstrasse");
    const herbs1 = await startAll("Heilwurz");
    await expect(herbs1 === 3, "3 Heilwurz on the Königsstraße");
    for (const t of ["Harpyien x2", "Wegelagerer x2", "Harpyie & Kragenechse"]) { await fight(t); await heal(); }
    await state("after the road");

    // ---------------------------------------------------------------- Wachtburg, the Guild
    await go(M.WACHTBURG, 24, 47, 8);
    await expect(await sw("C3: In Wachtburg"), "arrived in Wachtburg");
    await h.shot("c3_wachtburg");
    await go(M.GILDE, 12, 9, 8);
    await h.shot("c3_guild");
    await talk("Hoshino Miyu", [0, 0, 0]);
    await expect(await sw("C3: Registered"), "registered at the Guild");
    await expect(await sw("C3: Letter Delivered"), "letter delivered, bounty paid");
    const nick = await h.eval(() => $gameActors.actor(1).nickname() + " / party " + $gameActors.actor(4).name());
    await expect(nick.startsWith("Neuling"), "title Neuling (" + nick + ")");
    await talk("Hoshino Miyu", [0, 0]);
    await talk("Hoshino Miyu", [0, 1]);
    await talk("Hoshino Miyu", [0, 2]);
    await expect(await sw("C3: Granary Job") && await sw("C3: Wolf Job") && await sw("C3: Herb Job"), "three jobs taken");
    await state("registered");

    // ---------------------------------------------------------------- Kaji
    await go(M.KAJI, 14, 7, 8);
    await talk("Kaji Tōbei", [1, 0]);
    const armor = await h.eval(() => $gameActors.actor(1).equips()[3] && $gameActors.actor(1).equips()[3].name);
    await expect(armor === "Echtsilberrüstung", "armor refitted (" + armor + ")");

    // ---------------------------------------------------------------- the granary vaults
    await go(M.WACHTBURG, 11, 24, 8);
    await talk("Door: Kornspeicher");
    await expect(await h.eval(() => $gameMap.mapId()) === M.KORN, "into the granary vaults");
    await h.shot("c3_vaults");
    for (const t of ["Kornkobolde x3", "Kobolde & Schimmeling"]) { await fight(t); await heal(); }
    await talk("Schimmelmutter");
    await expect(await sw("C3: Granary Cleared"), "Schimmelmutter beaten");
    await state("after the granary");

    // ---------------------------------------------------------------- the Nordstraße
    await heal();
    await go(M.NORD, 3, 13, 6);
    const herbs2 = await startAll("Heilwurz");
    await expect(herbs2 === 3, "3 Heilwurz on the Nordstraße");
    await fight("Nordwölfe x2"); await heal();
    await talk("Wolf Pack");
    await expect(await sw("C3: Pack Down"), "pack leader beaten");
    await h.shot("c3_nordstrasse");
    await state("after the wolves");

    // ---------------------------------------------------------------- report -> emergency -> breakthrough
    await heal();
    await go(M.GILDE, 12, 9, 8);
    await talk("Hoshino Miyu", [2]);
    await idle();
    await expect(await sw("C3: Emergency Done"), "emergency answered");
    await expect(await sw("C3: Called to the Wall"), "called to the Wall");
    const bt = await h.eval(() => ({ gate: $gameVariables.value(1), weapon: $gameActors.actor(1).weapons()[0].name,
        fang: $gameActors.actor(1).isLearnedSkill($dataSkills.findIndex(s => s && s.name === "Returning Fang")),
        rank: Rank.letter($gameActors.actor(1).rkRank()), hanma: Rank.letter($gameActors.actor(2).rkRank()) }));
    await expect(bt.gate === 1 && bt.weapon === "Lichtdolch" && bt.fang && bt.rank === "E", "breakthrough to E: " + JSON.stringify(bt));
    await state("after the emergency");
    await h.shot("c3_rank_e");

    // ---------------------------------------------------------------- the Wolfsgrube (optional)
    await heal();
    await talk("Kurogane Isao", [1, 0]);
    await expect(await h.eval(() => $gameMap.mapId()) === M.WOLF, "in the Wolfsgrube");
    await h.shot("c3_wolfsgrube");
    await talk("Kurogane Isao", [0]);
    console.log("  Wolfsgrube cleared:", await sw("C3: Wolfsgrube Cleared"));
    await state("after the Wolfsgrube");

    // ---------------------------------------------------------------- Act II: the Wall
    await heal();
    await go(M.NORD, 27, 1, 8);
    await talk("North");
    await expect(await sw("A2: On the Wall"), "Act II: on the Wallstraße");
    await h.shot("a2_wallstrasse");
    for (const t of ["Aschenhunde x2", "Aschenleichen x2", "Aschenleiche & Hund"]) { await fight(t); await heal(); }
    await talk("Supply Cart");
    await go(M.FRONT, 16, 32, 8);
    await expect(await sw("A2: At Frontposten"), "arrived at Frontposten 3");
    await h.shot("a2_frontposten");
    await talk("Sergeant Kōno", [0]);
    await expect(await sw("A2: Night Assault"), "night assault");
    await h.shot("a2_night");
    await talk("Inner Gate", [0]);
    await idle();
    await expect(await sw("A2: Falin Joined"), "Falin joined");
    const pt = await h.eval(() => party());
    await expect(pt.length === 3 && pt[2].name === "Falin", "party of three");
    await expect(pt[2].rank === "E", "Falin at rank E (" + pt[2].stats + ")");
    await state("end of the build");
    await h.shot("a2_end");
    const q = await h.eval(() => $gameSystem._questContainer.questsArray.map(q => q.id + ":" + q.shortTitle + ":" + q.status));
    console.log("quests:", JSON.stringify(q));
    console.log("battles:", JSON.stringify(await h.eval(() => __battles.map(b => b.troop + ":" + b.result + ":" + b.turns + "t"))));
};
