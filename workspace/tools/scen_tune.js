// Engine balance tuner: finds the offence factor (STR, DEX and MAG of the named enemies, applied at runtime) that
// brings a troop's auto-battle win rate into a target band, by bisection. The party is built like
// scen_story_bal2.js (same config keys: level, walls, guests, regalia, fresh, reset).
//   TUNE='[{"troop":"Seelenkessel","level":30,"walls":[12,20],"enemies":["Seelenkessel"],"target":[0.45,0.6],
//           "fix":{"Werwolf":0.8},"n":12,"steps":5}]' node tools/run_game.js tools/scen_tune.js
// fix: factors already decided for other enemies (applied first); abortWin: a story page that aborts the
// battle counts as a win. Prints one RESULT line per task.
const lib = require("./storylib.js");
module.exports = async h => {
    const tasks = JSON.parse(process.env.TUNE);
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); $gameSwitches.setValue(1, true); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 60000);
    await h.eval(() => {
        $gameMap._interpreter.clear();
        $gameMap.events().forEach(e => e.erase());
        window.__noRevive = true;
        BattleManager.gainExp = function() {};
        BattleManager.gainGold = function() {};
        BattleManager.gainDropItems = function() {};
        window.__orig = {};
        // offence factor on STR (params[2]), MAG (params[4]) and DEX (params[6]) of the enemies named
        window.__scale = (names, f) => {
            for (const e of $dataEnemies) {
                if (!e || !names.includes(e.name)) continue;
                if (!window.__orig[e.id]) window.__orig[e.id] = e.params.slice();
                const o = window.__orig[e.id];
                for (const i of [2, 4, 6]) e.params[i] = Math.max(1, Math.round(o[i] * f));
                Rank.parseEnemy(e);
            }
        };
        // HP factor (params[0]) of the enemies named
        window.__hp = (names, f) => {
            for (const e of $dataEnemies) {
                if (!e || !names.includes(e.name)) continue;
                if (!window.__orig[e.id]) window.__orig[e.id] = e.params.slice();
                e.params[0] = Math.max(1, Math.round(window.__orig[e.id][0] * f));
            }
        };
    });
    const setup = c => h.eval(c => {
        $gameActors._data = [];
        $gameVariables.setValue(1, 0);
        for (const s of c.reset || []) $gameSwitches.setValue(s, false);
        $gameVariables.setValue(Story.P.pierceVar, c.regalia || 0);
        const k = $gameActors.actor(1), hn = $gameActors.actor(2), f = $gameActors.actor(3);
        $gameParty._actors = [1, 2];
        const falinAt = c.falin || 15;
        const steps = (c.walls || []).map(w => [w, true]).concat([[c.level, false]]).sort((a, b) => a[0] - b[0]);
        for (const [L, bt] of steps) {
            if (L >= falinAt && !$gameParty._actors.includes(3)) {
                $gameParty.addActor(3); f.changeLevel(Math.max(falinAt, L), false); Story.autoBuild(f);
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
        $gameMessage.clear();
        $gameParty.members().forEach(a => a.recoverAll());
    }, c);
    const measure = async (c, n) => {
        let wins = 0, turns = 0, hp = 0;
        await setup(c);
        for (let i = 0; i < n; i++) {
            if (c.fresh) await setup(c);
            await h.eval(() => $gameParty.members().forEach(a => { a.recoverAll(); a.clearStates(); }));
            await h.eval(t => {
                const id = $dataTroops.findIndex(x => x && x.name === t);
                if (id < 0) throw new Error("no troop " + t);
                BattleManager.setup(id, false, true);
                SceneManager.push(Scene_Battle);
            }, c.troop);
            await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted() &&
                !SceneManager.isSceneChanging(), 150000);
            const r = await h.eval(() => {
                const b = __battles[__battles.length - 1];
                return { result: b.result, turns: b.turns,
                         hp: $gameParty.members().reduce((s, a) => s + a.hp / a.mhp, 0) / $gameParty.size() };
            });
            // abortWin: the troop's story page ends the fight ("Abort Battle"), e.g. Shirogane yields at 40% HP
            if (r.result === 0 || (c.abortWin && r.result === 1)) { wins++; hp += r.hp; }
            turns += r.turns;
        }
        return { win: wins / n, turns: turns / n, hp: wins ? hp / wins : 0 };
    };
    for (const c of tasks) {
        for (const [name, f] of Object.entries(c.fix || {})) await h.eval(([n, f]) => __scale([n], f), [name, f]);
        if (c.hp) await h.eval(([names, f]) => __hp(names, f), [c.enemies, c.hp]);     // hp: a fixed HP factor
        const [lo, hi] = c.target;
        let a = c.min || 0.4, b = c.max || 1.0, best = null;
        const n = c.n || 12;
        // start at the current numbers (factor 1) unless told otherwise
        let f = c.start || 1.0;
        for (let step = 0; step < (c.steps || 5); step++) {
            await h.eval(([names, f]) => __scale(names, f), [c.enemies, f]);
            const r = await measure(c, n);
            console.log(`  ${c.troop}: factor ${f.toFixed(3)} -> win ${(r.win * 100).toFixed(0)}% turns ${r.turns.toFixed(1)} hp ${(r.hp * 100).toFixed(0)}%`);
            const mid = (lo + hi) / 2;
            if (!best || Math.abs(r.win - mid) < Math.abs(best.win - mid)) best = { f, ...r };
            if (r.win >= lo && r.win <= hi) break;
            if (r.win < lo) b = f; else a = f;     // too hard: lower the offence
            if (b - a < 0.02) break;
            f = (a + b) / 2;
        }
        await h.eval(([names]) => { __scale(names, 1.0); __hp(names, 1.0); }, [c.enemies]);
        console.log(`RESULT ${JSON.stringify({ troop: c.troop, enemies: c.enemies, factor: Number(best.f.toFixed(3)), win: best.win, turns: Number(best.turns.toFixed(1)), hp: Number(best.hp.toFixed(2)) })}`);
    }
};
