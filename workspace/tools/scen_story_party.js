// Prints the party's numbers along the story's level/rank path (for calibrating enemies).
const lib = require("./storylib.js");
module.exports = async h => {
    await h.eval(lib);
    await h.eval(() => { DataManager.setupNewGame(); $gameSwitches.setValue(1, true); SceneManager.goto(Scene_Map); });
    await h.runUntil(() => SceneManager._scene instanceof Scene_Map && SceneManager._scene.isStarted(), 20000);
    const rows = await h.eval(() => {
        $gameMap._interpreter.clear();
        $gameParty._actors = [1, 2];
        const k = $gameActors.actor(1), hn = $gameActors.actor(2), f = $gameActors.actor(3);
        const out = [];
        const snap = tag => {
            for (const a of $gameParty.members()) {
                a.recoverAll();
                const w = a.weapons()[0];
                const atk = a.rkAttackStat();
                out.push(tag + " " + a.name().padEnd(6) + " L" + a.level + " " + Rank.letter(a.rkRank()) + " HP " + a.mhp +
                    " MP " + a.mmp + " AC " + a.rkAC() + " " + Rank.STATS.map((s, i) => s + a.rkStat(i)).join(" ") +
                    " atk " + (w ? w.name : "-") + " " + atk);
            }
        };
        const path = [[12, 1], [15, 0], [21, 2], [27, 0], [31, 3], [36, 0], [41, 4], [47, 0], [51, 5], [55, 0]];
        for (const [L, bt] of path) {
            if (L >= 15 && !$gameParty._actors.includes(3)) { $gameParty.addActor(3); f.changeLevel(L, false); Story.autoBuild(f); }
            k.changeLevel(L, false); if (f.level < L && $gameParty._actors.includes(3)) f.changeLevel(L, false);
            spend(k); spend(hn); if ($gameParty._actors.includes(3)) Story.autoBuild(f);
            if (bt) { Story.breakthrough(true); spend(k); spend(hn); if ($gameParty._actors.includes(3)) Story.autoBuild(f); }
            snap("L" + L);
        }
        $gameMessage.clear();
        return out;
    });
    console.log(rows.join("\n"));
};
