// Mastery flows, NPC events through the interpreter, encounter statistics, shop window.
const pagelib = require("./pagelib.js");

module.exports = async h => {
    const check = (cond, msg) => {
        console.log((cond ? "PASS " : "FAIL ") + msg);
        if (!cond) h.failures = (h.failures || 0) + 1;
    };
    const onMap = () => SceneManager._scene.constructor.name === "Scene_Map" && SceneManager._scene._started &&
        !SceneManager.isSceneChanging() && !$gamePlayer.isTransferring();
    const idle = () => SceneManager._scene.constructor.name === "Scene_Map" && SceneManager._scene._started &&
        !SceneManager.isSceneChanging() && !$gamePlayer.isTransferring() && !$gameMap.isEventRunning() && !$gameMessage.isBusy();

    await h.eval(pagelib);
    await h.eval(() => { DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await h.runUntil(idle, 20000);
    await h.eval(() => { for (const a of $gameParty.members()) buildActor(a, 14); });

    // ---------------------------------------------------------------- A1 breakthrough by kill
    await h.eval(() => {
        const k = $gameActors.actor(4);
        k.rkSetMastery(20, 0, 179);
        window.__plan = { 1: "guard", 2: "guard", 3: "guard", 4: { skill: 20 } };
        window.__messages = [];
        BattleManager.setup(7, true, true);
        SceneManager.push(Scene_Battle);
    });
    await h.eval(() => { window.__holdMsg = /Breakthrough/; });
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle", 3000);
    await h.runUntil(() => {
        const w = SceneManager._scene._messageWindow;
        return w && w.pause && /Breakthrough/.test(w.shownText());
    }, 40000);
    await h.run(10);
    await h.shot("30_victory_mastery");
    await h.eval(() => { window.__holdMsg = null; });
    await h.runUntil(onMap, 20000);
    const a1 = await h.eval(() => {
        const k = $gameActors.actor(4);
        return { r: k.rkMasteryRank(20), x: k.rkMasteryExp(20), bonus: k._rkBonus.slice(), msgs: window.__messages.slice(-8) };
    });
    console.log("A1", JSON.stringify(a1));
    check(a1.r === 1, "Firebolt broke through to E after finishing a rank E foe");
    check(a1.bonus[6] === 5, "mastery rank-up gave MAG +5");
    check(a1.msgs.some(m => /Breakthrough/.test(m)) && a1.msgs.some(m => /reached rank E/.test(m)), "victory shows breakthrough + rank-up lines");

    // ---------------------------------------------------------------- A1b no breakthrough when the kill is same-rank
    await h.eval(() => {
        const k = $gameActors.actor(4);
        k.rkSetMastery(21, 1, 359); // Frost Shard at E, bar nearly full
        window.__plan = { 1: "guard", 2: "guard", 3: "guard", 4: { skill: 21 } };
        for (const a of $gameParty.members()) a.recoverAll();
        BattleManager.setup(7, true, true);
        SceneManager.push(Scene_Battle);
    });
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle", 3000);
    await h.runUntil(onMap, 40000);
    const a1b = await h.eval(() => ({ r: $gameActors.actor(4).rkMasteryRank(21), full: $gameActors.actor(4).rkIsBarFull(21),
        msgs: window.__messages.slice(-4) }));
    console.log("A1b", JSON.stringify(a1b));
    check(a1b.r === 1 && a1b.full, "E skill with a full bar stays E after killing E foes (needs a D foe)");
    check(a1b.msgs.some(m => /ready to break through/.test(m)), "victory hints that the bar is full");

    // ---------------------------------------------------------------- A2 unlock via Complete Breakthrough
    await h.eval(() => {
        const k = $gameActors.actor(4);
        k.rkSetMastery(20, 1, 360);
        window.__messages = [];
        PluginManager.callCommand(null, "Rank_Core", "CompleteBreakthrough", { actorId: "4", skillId: "20" });
    });
    await h.runUntil(() => !$gameMessage.isBusy(), 5000);
    const a2 = await h.eval(() => ({ r: $gameActors.actor(4).rkMasteryRank(20), fireball: $gameActors.actor(4).isLearnedSkill(24),
        msgs: window.__messages.slice() }));
    console.log("A2", JSON.stringify(a2));
    check(a2.r === 2 && a2.fireball, "Firebolt reached D and taught Fireball");

    // ---------------------------------------------------------------- A3 evolve
    await h.eval(() => {
        const m = $gameActors.actor(2);
        m.rkSetMastery(9, 2, 560);
        window.__messages = [];
        PluginManager.callCommand(null, "Rank_Core", "CompleteBreakthrough", { actorId: "2", skillId: "0" });
    });
    await h.runUntil(() => !$gameMessage.isBusy(), 5000);
    const a3 = await h.eval(() => {
        const m = $gameActors.actor(2);
        return { old: m.isLearnedSkill(9), neu: m.isLearnedSkill(12), r: m.rkMasteryRank(12), msgs: window.__messages.slice() };
    });
    console.log("A3", JSON.stringify(a3));
    check(!a3.old && a3.neu && a3.r === 3, "Quick Thrust evolved into Flash Thrust at C, mastery kept");

    // ---------------------------------------------------------------- A4 support breakthrough
    await h.eval(() => {
        const e = $gameActors.actor(3);
        e.rkSetMastery(16, 0, 179);
        window.__plan = { 1: { skill: 1 }, 2: "guard", 3: { skill: 16 }, 4: "guard" };
        for (const a of $gameParty.members()) a.recoverAll();
        window.__messages = [];
        BattleManager.setup(8, true, true);
        SceneManager.push(Scene_Battle);
    });
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle", 3000);
    await h.runUntil(onMap, 40000);
    const a4 = await h.eval(() => ({ r: $gameActors.actor(3).rkMasteryRank(16), msgs: window.__messages.slice(-6) }));
    console.log("A4", JSON.stringify(a4));
    check(a4.r === 1, "support skill (Bless) broke through after a won fight against a higher-rank foe");
    await h.eval(() => { window.__plan = null; });

    // ---------------------------------------------------------------- A5 working rank capped by stat grade
    const a5 = await h.eval(() => {
        const k = $gameActors.actor(4);
        const before = k.rkSkillRank($dataSkills[20]);
        k.rkSetMastery(22, 4, 0); // Spark Storm mastery B, MAG grade D
        return { firebolt: before, spark: k.rkSkillRank($dataSkills[22]), magGrade: k.rkStatRank("MAG"),
            costF: Rank.mpCostFor(k, $dataSkills[22], 0), cost: k.skillMpCost($dataSkills[22]) };
    });
    console.log("A5", JSON.stringify(a5));
    check(a5.spark === a5.magGrade && a5.spark < 4, "working rank is capped by the stat's grade");
    check(a5.cost > a5.costF, "MP cost rises with the working rank");

    // ---------------------------------------------------------------- B NPC events (interpreter)
    const runEvent = async (name, choices) => {
        await h.eval(([n, c]) => {
            window.__choices = c.slice();
            window.__messages = [];
            const ev = $gameMap.events().find(e => e.event().name === n);
            ev.start();
        }, [name, choices]);
        await h.run(5);
    };
    const lv0 = await h.eval(() => ({ lv: $gameActors.actor(1).level, pts: $gameActors.actor(1).rkPoints() }));
    await runEvent("Trainer", [0]);
    await h.runUntil(idle, 10000);
    const b1 = await h.eval(() => ({ lv: $gameActors.actor(1).level, pts: $gameActors.actor(1).rkPoints(), msgs: window.__messages.slice() }));
    console.log("B1", JSON.stringify(b1));
    check(b1.lv === lv0.lv + 1 && b1.pts === lv0.pts + 20, "Trainer +1 level gives 20 points");
    check(b1.msgs.some(m => /gained 20 stat points/.test(m)), "level-up message mentions the points");

    await runEvent("Trainer", [2]);
    await h.runUntil(idle, 10000);
    const b1b = await h.eval(() => ({ pts: $gameActors.actor(1).rkPoints(), alloc: $gameActors.actor(1)._rkAlloc.reduce((s, v) => s + v, 0) }));
    console.log("B1b", JSON.stringify(b1b));
    check(b1b.alloc === 0 && b1b.pts === 20 * 15, "Refund returns every assigned point");
    await h.eval(() => { for (const a of $gameParty.members()) { a.rkRefundPoints(); } buildActor($gameActors.actor(1), 15); });

    await runEvent("Mentor", [0]);
    await h.runUntil(idle, 10000);
    const b2 = await h.eval(() => ({ x: $gameActors.actor(1).rkMasteryExp(4) }));
    check(b2.x >= 100, "Mentor study adds mastery (Power Strike " + b2.x + ")");

    await runEvent("Battle Master", [0, 0]);
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle", 5000);
    await h.runUntil(idle, 40000);
    const b3 = await h.eval(() => ({ msgs: window.__messages.slice(-3), running: $gameMap.isEventRunning() }));
    console.log("B3", JSON.stringify(b3));
    check(b3.msgs.some(m => /Well fought/.test(m)), "Battle Master sparring returns to the event after a win");

    await runEvent("Healer", []);
    await h.runUntil(idle, 10000);
    check(await h.eval(() => $gameParty.members().every(a => a.hp === a.mhp)), "Healer restores the party");

    await runEvent("Merchant", []);
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Shop" && SceneManager._scene._started, 10000);
    check(await h.eval(() => $gameParty.gold() >= 5000), "Merchant gives test funds");
    await h.eval(() => {
        const s = SceneManager._scene;
        s._commandWindow.deactivate();
        s.commandBuy();
        const w = s._buyWindow;
        const i = w._data.indexOf($dataWeapons[3]);
        w.select(Math.max(0, i));
    });
    await h.run(10);
    await h.shot("31_shop_weapon");
    await h.eval(() => {
        const w = SceneManager._scene._buyWindow;
        w.select(w._data.indexOf($dataArmors[4]));
    });
    await h.run(10);
    await h.shot("32_shop_armor");
    await h.eval(() => SceneManager.pop());
    await h.runUntil(idle, 10000);

    // ---------------------------------------------------------------- C encounter statistics (field)
    await h.eval(() => {
        for (const a of $gameParty.members()) { a.rkRefundPoints(); a.changeLevel(1, false); }
        $gamePlayer.reserveTransfer(2, 7, 34, 8, 0);
    });
    await h.runUntil(idle, 10000);
    const c = await h.eval(() => {
        const p = $gamePlayer;
        const find = (region, bush) => {
            for (let y = 0; y < $gameMap.height(); y++) for (let x = 0; x < $gameMap.width(); x++) {
                if ($gameMap.regionId(x, y) === region && $gameMap.isBush(x, y) === bush && $gameMap.isPassable(x, y, 2)) return [x, y];
            }
            return null;
        };
        const plain = find(3, false);
        p.locate(plain[0], plain[1]);
        const trial = () => {
            p.makeEncounterCount();
            let n = 0;
            while (p._encounterCount > 0 && n < 1000) { p.updateEncounterCount(); n++; }
            return n;
        };
        const res = [];
        for (let i = 0; i < 3000; i++) res.push(trial());
        res.sort((a, b) => a - b);
        const mean = res.reduce((s, v) => s + v, 0) / res.length;
        const out = { region: p.regionId(), bush: $gameMap.isBush(p.x, p.y), steps: $gameMap.encounterStep(), mean: +mean.toFixed(1),
            min: res[0], p10: res[300], p50: res[1500], p90: res[2700], max: res[res.length - 1] };
        // MZ's original spacing for comparison
        const orig = [];
        for (let i = 0; i < 3000; i++) { const n = $gameMap.encounterStep(); orig.push(Math.randomInt(n) + Math.randomInt(n) + 1); }
        orig.sort((a, b) => a - b);
        out.mzMin = orig[0]; out.mzP10 = orig[300]; out.mzP90 = orig[2700];
        // troop picks at rank F
        const picks = {};
        for (let i = 0; i < 2000; i++) { const t = p.makeEncounterTroopId(); picks[t] = (picks[t] || 0) + 1; }
        out.picks = picks;
        // bushes count double
        const bushTile = find(3, true);
        p.locate(bushTile[0], bushTile[1]);
        let bushSum = 0;
        for (let i = 0; i < 1000; i++) bushSum += trial();
        out.bushMean = +(bushSum / 1000).toFixed(1);
        // safe region
        const safe = find(1, false);
        p.locate(safe[0], safe[1]);
        out.safeRegion = p.regionId();
        out.safeActive = p.rkEncounterActive();
        p.locate(15, 3);
        out.northRegion = p.regionId();
        out.northArea = Rank.areaRank();
        const picksN = {};
        for (let i = 0; i < 500; i++) { const t = p.makeEncounterTroopId(); picksN[t] = (picksN[t] || 0) + 1; }
        out.picksNorth = picksN;
        // weak troops back off: pretend the party is rank C
        const pr = Rank.partyRank;
        Rank.partyRank = () => 2;
        p.locate(plain[0], plain[1]);
        out.weakActiveAtD = p.rkEncounterActive();
        Rank.partyRank = pr;
        out.activeAtF = p.rkEncounterActive();
        p.makeEncounterCount();
        return out;
    });
    console.log("C", JSON.stringify(c));
    check(Math.abs(c.mean - c.steps) <= c.steps * 0.08, "average steps between fights ~ Encounter Steps (" + c.mean + " vs " + c.steps + ")");
    check(c.min > Math.floor(c.steps * 0.4), "no fight inside the grace distance (min " + c.min + ")");
    check(c.safeRegion === 1 && !c.safeActive, "safe region stops encounter progress");
    check(c.northRegion === 2 && c.northArea === 1, "north stretch is region 2, rank E");
    check(Object.keys(c.picksNorth).every(t => [7, 8, 9].includes(Number(t))), "north stretch only spawns rank E troops");
    check(Object.keys(c.picks).every(t => [1, 2, 3, 4, 5].includes(Number(t))), "lower field only spawns rank F troops");
    check(c.weakActiveAtD === false && c.activeAtF === true, "rank F troops stop attacking a rank D party");
    check(Math.abs(c.bushMean - c.steps / 2) <= c.steps * 0.08, "bushes halve the distance (" + c.bushMean + ")");
};
