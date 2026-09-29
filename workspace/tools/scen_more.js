// Save/load, woods boss + chest, rank wall note, boss shrug, stat cap raise, skill badge dimming.
const pagelib = require("./pagelib.js");

module.exports = async h => {
    const check = (cond, msg) => console.log((cond ? "PASS " : "FAIL ") + msg);
    const idle = () => SceneManager._scene.constructor.name === "Scene_Map" && SceneManager._scene._started &&
        !SceneManager.isSceneChanging() && !$gamePlayer.isTransferring() && !$gameMap.isEventRunning() && !$gameMessage.isBusy();
    const sceneIs = name => h.runUntil(n => SceneManager._scene.constructor.name === n && SceneManager._scene._started &&
        !SceneManager.isSceneChanging(), 20000, name);

    await h.eval(pagelib);
    await h.eval(() => { DataManager.setupNewGame(); SceneManager.goto(Scene_Map); });
    await h.runUntil(idle, 20000);
    await h.eval(() => { for (const a of $gameParty.members()) buildActor(a, 14); $gameActors.actor(4).rkSetMastery(20, 1, 77); });

    // ---------------------------------------------------------------- save / load
    await h.eval(() => {
        $gameSystem.onBeforeSave();
        window.__saved = null;
        DataManager.saveGame(1).then(() => { window.__saved = true; }).catch(e => { window.__saved = String(e); });
    });
    await h.until(() => window.__saved !== null, 10000);
    const before = await h.eval(() => JSON.stringify({ s: $gameActors.actor(4).rkBaseStats(), m: $gameActors.actor(4)._rkMastery, p: $gameActors.actor(4).rkPoints() }));
    await h.eval(() => {
        $gameActors.actor(4).rkSetMastery(20, 0, 0);
        window.__loaded = null;
        DataManager.loadGame(1).then(() => { window.__loaded = true; }).catch(e => { window.__loaded = String(e); });
    });
    await h.until(() => window.__loaded !== null, 10000);
    const after = await h.eval(() => JSON.stringify({ s: $gameActors.actor(4).rkBaseStats(), m: $gameActors.actor(4)._rkMastery, p: $gameActors.actor(4).rkPoints() }));
    check(await h.eval(() => window.__saved === true && window.__loaded === true), "save and load succeed");
    check(before === after, "stats, mastery and points survive save/load");
    await h.eval(() => SceneManager.goto(Scene_Map));
    await h.runUntil(idle, 20000);

    // ---------------------------------------------------------------- skill menu: dimmed badge + works-at line
    await h.eval(() => {
        const k = $gameActors.actor(4);
        k.rkSetMastery(22, 4, 300); // Spark Storm mastery B, but MAG is only grade D
        $gameParty.setMenuActor(k);
        SceneManager.push(Scene_Skill);
    });
    await sceneIs("Scene_Skill");
    await h.eval(() => {
        const s = SceneManager._scene;
        s._skillTypeWindow.deactivate();
        s.commandSkill();
        const w = s._itemWindow;
        w.select(w._data.indexOf($dataSkills[22]));
    });
    await h.run(5);
    await h.shot("40_skill_capped");
    const helpText = await h.eval(() => SceneManager._scene._helpWindow._text);
    console.log("help", JSON.stringify(helpText));
    check(/works at/.test(helpText) && /MAG grade/.test(helpText), "help line says the skill works at the stat's grade");
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Map");

    // ---------------------------------------------------------------- stat screen: cap rises when the rank rises
    await h.eval(() => {
        const a = $gameActors.actor(2);
        a.rkRefundPoints();
        a.changeLevel(20, false);
        $gameParty.setMenuActor(a);
        SceneManager.push(Scene_RankStats);
    });
    await sceneIs("Scene_RankStats");
    const cap = await h.eval(() => {
        const w = SceneManager._scene._listWindow;
        const p = w.preview();
        const out = { rank0: p.rkRank(), cap0: p.rkStatCap(1), pts: p.rkPoints() };
        w.changeStat(1, 250);  // DEX: stops at the F cap
        out.dexAfterFirst = p.rkBaseStat(1);
        w.changeStat(2, 90);   // CON
        w.changeStat(0, 60);   // STR -> PL crosses 100, rank E, cap 299
        out.rank1 = p.rkRank();
        out.cap1 = p.rkStatCap(1);
        w.changeStat(1, 50);   // DEX can go further now
        out.dexPending = p.rkBaseStat(1);
        w.select(1);
        return out;
    });
    await h.run(5);
    await h.shot("41_stats_rankup_preview");
    const conf = await h.eval(() => {
        const s = SceneManager._scene;
        const w = s._listWindow;
        const want = w.preview().rkBaseStats();
        w.select(7);
        s.onListOk();
        return { want, got: $gameActors.actor(2).rkBaseStats(), rank: $gameActors.actor(2).rkRank() };
    });
    console.log("cap", JSON.stringify(cap), JSON.stringify(conf));
    check(cap.dexAfterFirst === 199 && cap.rank1 === 1 && cap.cap1 === 299 && cap.dexPending > 199, "cap rises from 199 to 299 as the preview reaches rank E");
    check(JSON.stringify(conf.want) === JSON.stringify(conf.got), "confirm applies the previewed stats exactly (multi-pass)");
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Map");

    // ---------------------------------------------------------------- rank wall + boss shrug
    await h.eval(() => {
        for (const a of $gameParty.members()) a.recoverAll();
        window.__autoBattle = false;
        window.__autoMsg = true;
        BattleManager.setup(12, true, true);
        SceneManager.push(Scene_Battle);
    });
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle" && BattleManager._phase === "input", 20000);
    const wall = await h.eval(() => {
        const actor = $gameActors.actor(1);
        const sentinel = $gameTroop.members()[0];
        const act = new Game_Action(actor);
        act.setAttack();
        const res = act.rkResolve(sentinel, true);
        const preview = Rank.previewText(act, sentinel);
        // F-rank attacker: wall
        const low = JSON.parse(JSON.stringify(actor._rkAlloc));
        return { gapE: res.gap, multE: res.gapMult, preview };
    });
    console.log("wall", JSON.stringify(wall));
    check(wall.gapE === -2 && wall.multE === 0.25, "rank E attacker vs rank C sentinel deals a quarter");
    // show the preview in the target window
    await h.eval(() => {
        const s = SceneManager._scene;
        if (s._partyCommandWindow.active) s.commandFight();
    });
    await h.run(10);
    await h.eval(() => SceneManager._scene.commandAttack());
    await h.run(10);
    await h.shot("42_wall_preview");
    await h.eval(() => {
        const s = SceneManager._scene;
        s.onEnemyCancel();
        s.hideSubInputWindows();
        s.endCommandSelection();
        window.__autoBattle = true;
        window.__plan = { 1: "guard", 2: "guard", 3: "guard", 4: "guard" };
        $gameParty.makeActions();
        BattleManager.startTurn();
    });
    await h.run(300);
    await h.eval(() => { $gameParty.members().forEach(a => a.recoverAll()); BattleManager.processEscape = BattleManager.processEscape; });
    // test the rank F attacker (wall) with a fresh F actor copy
    const wallF = await h.eval(() => {
        const a = JsonEx.makeDeepCopy($gameActors.actor(1));
        a.rkRefundPoints();
        const sentinel = $gameTroop.members()[0];
        const act = new Game_Action($gameActors.actor(1));
        act.subject = () => a;
        act.setAttack();
        const res = act.rkResolve(sentinel, true);
        return { rank: a.rkRank(), gap: res.gap, wall: res.wall, text: Rank.previewText(act, sentinel) };
    });
    console.log("wallF", JSON.stringify(wallF));
    check(wallF.wall === true, "rank F attacker hits a wall against rank C");
    await h.eval(() => { BattleManager.abort(); });
    await h.runUntil(idle, 20000);

    // boss shrug: sleep twice on the wolfman
    const shrug = await h.eval(() => {
        BattleManager.setup(11, true, true);
        $gameTroop.setup(11);
        const boss = $gameTroop.members()[0];
        const out = [];
        for (let i = 0; i < 4; i++) {
            boss.removeState(10);
            boss.clearResult();
            boss.addState(10);
            out.push([boss.isStateAffected(10), !!boss.result().rkShrugged, boss._stateTurns[10] || 0]);
        }
        return out;
    });
    console.log("shrug", JSON.stringify(shrug));
    check(shrug[0][0] && !shrug[1][0] && shrug[2][0] && !shrug[3][0], "boss shrugs off every second disabling state");
    check(shrug[0][2] === 1, "disabling states last a boss one turn");

    // ---------------------------------------------------------------- woods: boss event and chest
    await h.eval(() => {
        $gameParty.members().forEach(a => a.recoverAll());
        $gamePlayer.reserveTransfer(3, 33, 47, 8, 0);
    });
    await h.runUntil(idle, 20000);
    await h.run(60);
    await h.shot("43_woods");
    await h.eval(() => {
        window.__plan = null;
        window.__choices = [0];
        window.__messages = [];
        $gameMap.events().find(e => e.event().name === "Wolfman").start();
    });
    await h.run(5);
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Battle", 10000);
    await h.runUntil(() => (SceneManager._scene.constructor.name === "Scene_Map" && SceneManager._scene._started && !SceneManager.isSceneChanging() &&
        !$gameMap.isEventRunning() && !$gameMessage.isBusy()) || SceneManager._scene.constructor.name === "Scene_Gameover", 80000);
    const boss = await h.eval(() => ({
        scene: SceneManager._scene.constructor.name,
        gone: $gameSelfSwitches.value([3, $gameMap.events().find(e => e.event().name === "Wolfman").eventId(), "A"]),
        msgs: window.__messages.slice(-6), turns: $gameTroop.turnCount()
    }));
    console.log("boss", JSON.stringify(boss));
    check(boss.scene === "Scene_Map" && boss.gone, "Wolfman boss beaten at level 14, event cleared (" + boss.turns + " turns)");
    await h.eval(() => {
        window.__messages = [];
        $gameMap.events().find(e => e.event().name === "Chest: Plate Armor").start();
    });
    await h.runUntil(idle, 10000);
    const chest = await h.eval(() => ({ n: $gameParty.numItems($dataArmors[4]), msgs: window.__messages.slice() }));
    check(chest.n >= 1 && chest.msgs.some(m => /Plate Armor/.test(m)), "chest gives Plate Armor");
};
