// Page-side helpers shared by test scenarios (evaluated in the game page).
module.exports = () => {
    window.__autoMsg = true;
    Window_BattleLog.prototype.messageSpeed = function() { return 1; };
    const POLICY = {
        1: { STR: 0.5, CON: 0.4, DEX: 0.1 },
        2: { DEX: 0.55, CON: 0.3, STR: 0.15 },
        3: { WIS: 0.55, CON: 0.3, MAG: 0.15 },
        4: { MAG: 0.6, CON: 0.25, INT: 0.15 }
    };
    window.buildActor = function(a, level) {
        a.changeLevel(level, false);
        const pol = POLICY[a.actorId()];
        const want = {};
        const pts = a.rkPoints();
        for (const s of Object.keys(pol)) want[s] = Math.floor(pts * pol[s]);
        for (let pass = 0; pass < 4; pass++) {
            for (const s of Object.keys(pol)) want[s] -= a.rkAllocate(Rank.statIndex(s), want[s]);
        }
        for (const s of ["CON", "DEX", "STR", "WIS", "MAG", "INT", "CHA"]) a.rkAllocate(Rank.statIndex(s), a.rkPoints());
        a.recoverAll();
    };
    // force actions: plan[actorId] = {skill, target} or "guard"
    window.__plan = null;
    if (!window.__planHooked) {
        window.__planHooked = true;
        const _mk = Game_Actor.prototype.makeAutoBattleActions;
        Game_Actor.prototype.makeAutoBattleActions = function() {
            const p = window.__plan && window.__plan[this.actorId()];
            if (!p) return _mk.call(this);
            for (let i = 0; i < this.numActions(); i++) {
                const act = new Game_Action(this);
                if (p === "guard") act.setGuard();
                else {
                    const id = this.isLearnedSkill(p.skill) && this.canUse($dataSkills[p.skill]) ? p.skill : this.attackSkillId();
                    act.setSkill(id);
                    const alive = act.isForOpponent() ? $gameTroop.aliveMembers() : $gameParty.aliveMembers();
                    act.setTarget(alive.length ? (act.isForOpponent() ? $gameTroop.members().indexOf(alive[0]) : $gameParty.members().indexOf(alive[0])) : 0);
                }
                this.setAction(i, act);
            }
            this.setActionState("waiting");
        };
    }
    Game_Actor.prototype.isAutoBattle = function() { return window.__autoBattle !== false; };
};
