// Smoke test: title, new game, map, menus, stat screen, battle preview, field HUD.
module.exports = async h => {
    const sceneIs = async name => {
        await h.until(n => SceneManager._scene && SceneManager._scene.constructor.name === n && SceneManager._scene._started &&
            !SceneManager.isSceneChanging(), 20000, name);
        await h.frames(20);
    };
    await h.frames(30);
    await h.shot("01_title");

    await h.eval(() => {
        DataManager.setupNewGame();
        SceneManager.goto(Scene_Map);
    });
    await sceneIs("Scene_Map");
    await h.frames(30);
    await h.shot("02_intro_message");
    await h.eval(() => { window.__autoMsg = true; });
    await h.until(() => !$gameMessage.isBusy() && !$gameMap.isEventRunning(), 10000);
    await h.eval(() => { window.__autoMsg = false; });
    await h.frames(10);
    await h.shot("03_hub");

    // main menu
    await h.eval(() => SceneManager.push(Scene_Menu));
    await sceneIs("Scene_Menu");
    await h.shot("04_menu");

    // status
    await h.eval(() => { $gameParty.setMenuActor($gameActors.actor(1)); SceneManager.push(Scene_Status); });
    await sceneIs("Scene_Status");
    await h.shot("05_status");
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Menu");

    // stat points: assign some points and preview
    await h.eval(() => { $gameParty.setMenuActor($gameActors.actor(1)); SceneManager.push(Scene_RankStats); });
    await sceneIs("Scene_RankStats");
    await h.shot("06_stats_empty");
    await h.eval(() => {
        const w = SceneManager._scene._listWindow;
        w.changeStat(0, 10);
        w.changeStat(2, 8);
        w.select(2);
    });
    await h.frames(5);
    await h.shot("07_stats_pending");
    await h.eval(() => {
        const w = SceneManager._scene._listWindow;
        w.select(7);
        SceneManager._scene.onListOk();
    });
    await h.frames(5);
    await h.shot("08_stats_confirmed");
    const st = await h.eval(() => { const a = $gameActors.actor(1); return { stats: a.rkBaseStats(), pts: a.rkPoints(), hp: a.hp, mhp: a.mhp }; });
    console.log("after confirm", JSON.stringify(st));
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Menu");

    // skill menu with help line
    await h.eval(() => { $gameParty.setMenuActor($gameActors.actor(4)); SceneManager.push(Scene_Skill); });
    await sceneIs("Scene_Skill");
    await h.eval(() => {
        const s = SceneManager._scene;
        s._skillTypeWindow.deactivate();
        s.commandSkill();
    });
    await h.frames(5);
    await h.shot("09_skills_mage");
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Menu");

    // equip screen comparing a weapon
    await h.eval(() => {
        $gameParty.gainItem($dataWeapons[4], 1);
        $gameParty.gainItem($dataArmors[3], 1);
        $gameParty.setMenuActor($gameActors.actor(1));
        SceneManager.push(Scene_Equip);
    });
    await sceneIs("Scene_Equip");
    await h.eval(() => {
        const s = SceneManager._scene;
        s._commandWindow.deactivate();
        s.commandEquip();
        s._slotWindow.select(0);
        s.onSlotOk();
    });
    await h.frames(5);
    await h.eval(() => {
        const w = SceneManager._scene._itemWindow;
        const i = w._data.indexOf($dataWeapons[4]);
        w.select(Math.max(0, i));
    });
    await h.frames(5);
    await h.shot("10_equip_compare");
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Menu");
    await h.eval(() => SceneManager.pop());
    await sceneIs("Scene_Map");

    // battle: goblins
    await h.eval(() => {
        window.__autoMsg = true;
        BattleManager.setup(2, true, true);
        SceneManager.push(Scene_Battle);
    });
    await h.until(() => SceneManager._scene.constructor.name === "Scene_Battle" && BattleManager._phase === "input", 30000);
    await h.eval(() => { window.__autoMsg = false; });
    await h.frames(40);
    await h.shot("11_battle_start");
    // choose fight -> attack -> enemy selection (preview)
    await h.eval(() => {
        const s = SceneManager._scene;
        if (s._partyCommandWindow.active) s.commandFight();
    });
    await h.frames(20);
    await h.eval(() => SceneManager._scene.commandAttack());
    await h.frames(20);
    await h.shot("12_battle_attack_preview");
    await h.eval(() => SceneManager._scene.onEnemyCancel());
    await h.frames(10);
    // skill window with help info (Reid: Power Strike)
    await h.eval(() => {
        const s = SceneManager._scene;
        const w = s._actorCommandWindow;
        w.selectSymbol("skill");
        s.commandSkill();
    });
    await h.frames(20);
    await h.shot("13_battle_skill_help");
    await h.eval(() => SceneManager._scene.onSkillOk());
    await h.frames(20);
    await h.shot("14_battle_skill_preview");
    // let the party fight on its own to the end
    await h.eval(() => {
        window.__autoMsg = true;
        Game_Actor.prototype.isAutoBattle = function() { return true; };
        const s = SceneManager._scene;
        s.hideSubInputWindows();
        s.endCommandSelection();
        $gameParty.makeActions();
        BattleManager.startTurn();
    });
    await h.frames(60);
    await h.shot("15_battle_running");
    await h.runUntil(() => SceneManager._scene.constructor.name === "Scene_Map" && !SceneManager.isSceneChanging(), 30000);
    const res = await h.eval(() => $gameParty.members().map(a => ({ n: a.name(), lv: a.level, exp: a.currentExp(), hp: a.hp + "/" + a.mhp,
        mastery: a.rkMasterySkills().map(s => s.name + ":" + a.rkMasteryRank(s.id) + "/" + a.rkMasteryExp(s.id)) })));
    console.log("after battle", JSON.stringify(res));
    await h.eval(() => { window.__autoMsg = false; });

    // field + HUD
    await h.eval(() => { $gamePlayer.reserveTransfer(2, 7, 37, 8, 0); });
    await h.until(() => $gameMap.mapId() === 2 && SceneManager._scene.constructor.name === "Scene_Map" && !SceneManager.isSceneChanging(), 20000);
    await h.frames(90);
    await h.shot("16_field_hud");
    // walk north a bit to raise danger and step into the E region
    await h.eval(() => { $gamePlayer._rkEncSteps = 25; });
    await h.frames(10);
    await h.shot("17_field_danger");
    await h.eval(() => { $gamePlayer.locate(15, 3); $gamePlayer._rkEncSteps = 5; });
    await h.frames(30);
    await h.shot("18_field_north_E");
};
