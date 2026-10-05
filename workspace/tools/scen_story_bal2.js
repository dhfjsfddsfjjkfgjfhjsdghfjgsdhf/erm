// Balance runs along the story's path: BAL='[{"level":17,"walls":[12],"troops":["Höllenhund"],"n":20}]'
//   fresh: rebuild the party before every fight; reset: switch ids to clear first (the once-only breakthrough
//   pages of the Messingvogt, Tsumugi and Gōen, so the scripted breakthrough happens in every fight)
//   walls: levels at which the party broke through (E at 12, D at 21, C at 31 ...); Falin joins at 15 (falin: level)
//   members: default [1, 2, 3] once Falin has joined; guests: extra actor ids (level = party level)
const lib = require("./storylib.js");
module.exports = async h => {
    const cfg = JSON.parse(process.env.BAL || '[{"level":17,"walls":[12],"troops":["Höllenhund"],"n":10}]');
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); $gameSwitches.setValue(1, true); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 20000);
    await h.eval(() => {
        $gameMap._interpreter.clear();
        $gameMap.events().forEach(e => e.erase());
        window.__noRevive = true;
        BattleManager.gainExp = function() {};
        BattleManager.gainGold = function() {};
        BattleManager.gainDropItems = function() {};
    });
    for (const c of cfg) {
        const setup = () => h.eval(c => {
            $gameActors._data = [];
            $gameVariables.setValue(1, 0);
            for (const s of c.reset || []) $gameSwitches.setValue(s, false);   // once-only story pages fire again
            $gameVariables.setValue(Story.P.pierceVar, c.regalia || 0);
            const k = $gameActors.actor(1), hn = $gameActors.actor(2), f = $gameActors.actor(3);
            $gameParty._actors = [1, 2];
            const falinAt = c.falin || 15;
            const walls = c.walls || [];
            const steps = walls.map(w => [w, true]).concat([[c.level, false]]).sort((a, b) => a[0] - b[0]);
            for (const [L, bt] of steps) {
                if (L >= falinAt && !$gameParty._actors.includes(3) && c.noFalin !== true) {
                    $gameParty.addActor(3); f.changeLevel(Math.min(L, Math.max(falinAt, L)), false); Story.autoBuild(f);
                }
                if (k.level < L) k.changeLevel(L, false);
                if ($gameParty._actors.includes(3) && f.level < L) f.changeLevel(L, false);
                spend(k); spend(hn); if ($gameParty._actors.includes(3)) Story.autoBuild(f);
                if (bt) { Story.breakthrough(true); spend(k); spend(hn); if ($gameParty._actors.includes(3)) Story.autoBuild(f); }
            }
            for (const g of c.guests || []) {
                const a = $gameActors.actor(g);
                a.changeLevel(c.level, false);
                Story.autoBuild(a);
                $gameParty.addActor(g);
            }
            if (c.items) for (const [name, n] of c.items) $gameParty.gainItem($dataItems.find(i => i && i.name === name), n);
            $gameMessage.clear();
            $gameParty.members().forEach(a => a.recoverAll());
        }, c);
        await setup();
        const party = await h.eval(() => party());
        if (c.log) await h.eval(() => {          // c.log: print the battle log of the first fight of each troop
            window.__blog = [];
            if (!window.__blogHooked) {
                window.__blogHooked = true;
                const _add = Window_BattleLog.prototype.addText;
                Window_BattleLog.prototype.addText = function(t) { if (window.__blog) window.__blog.push(t); _add.call(this, t); };
                const _st = BattleManager.startTurn;
                BattleManager.startTurn = function() {
                    if (window.__blog) window.__blog.push("== turn " + ($gameTroop.turnCount() + 1) + "  party " +
                        $gameParty.members().map(a => a.name() + " " + a.hp + "/" + a.mhp).join(", ") + "  foes " +
                        $gameTroop.members().map(e => e.name() + " " + e.hp + "/" + e.mhp).join(", "));
                    _st.call(this);
                };
            }
        });
        for (const tname of c.troops) {
            let wins = 0, turns = 0, hpLeft = 0, n = c.n || 20;
            for (let i = 0; i < n; i++) {
                if (c.fresh) await setup();   // scripted breakthroughs change the party: rebuild it for every fight
                await h.eval(() => $gameParty.members().forEach(a => { a.recoverAll(); a.clearStates(); }));
                await h.eval(t => {
                    const id = $dataTroops.findIndex(x => x && x.name === t);
                    if (id < 0) throw new Error("no troop " + t);
                    BattleManager.setup(id, false, true);
                    SceneManager.push(Scene_Battle);
                }, tname);
                await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                    !SceneManager.isSceneChanging(), 120000);
                const r = await h.eval(() => {
                    const b = __battles[__battles.length - 1];
                    const hp = $gameParty.members().reduce((s, a) => s + a.hp / a.mhp, 0) / $gameParty.size();
                    return { result: b.result, turns: b.turns, hp };
                });
                if (c.log && i === 0) {
                    console.log("---- battle log: " + tname + " (" + (r.result === 0 ? "won" : "lost") + ")");
                    console.log((await h.eval(() => window.__blog.splice(0))).map(t => "   " + t.replace(/\\C\[\d+\]/g, "")).join("\n"));
                } else if (c.log) await h.eval(() => { window.__blog.length = 0; });
                if (r.result === 0 || (c.abortWin && r.result === 1)) { wins++; hpLeft += r.hp; }   // abortWin: a story page ends it
                turns += r.turns;
            }
            const line = `L${c.level} gate ${"FEDCBA"[0]} ${tname.padEnd(24)} win ${Math.round(100 * wins / n)}%  turns ${(turns / n).toFixed(1)}  hp left ${wins ? Math.round(100 * hpLeft / wins) : 0}%`;
            console.log(line.replace("gate F", "rank " + party[0].rank));
        }
        if (c.show) console.log("   party:", JSON.stringify(party.map(p => p.name + " " + p.rank + " " + p.stats + " HP" + p.hp + " MP" + p.mp)));
    }
};
