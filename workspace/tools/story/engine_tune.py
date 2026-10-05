"""Engine corrections for Act II-III foes (5 Oct 2026).

The cloud session tuned chapters 5-9 with tools/battle_sim.py, which doesn't model states and buffs applied by
skills (poison: 10% of max HP every turn until the fight ends; Sleep and Frightened; Heerruf, Terrible Roar), HP
drain (the Seelenkessel's Seelenstrom) or skills that hit two or more random targets at full rate (Hydrabiss). In
the real engine some fights came out as walls (0-25% auto-battle wins where the target was ~50% for bosses and
~65-75% for mid-bosses, and regular fights at 25-75%).

These factors scale an enemy's offence (STR, DEX and MAG: damage, to-hit and AC from DEX) and, for a few, its HP,
after the database is built. Each was found by bisection in the engine with tools/scen_tune.js, auto-battle, the
party built like tools/scen_story_bal2.js. Targets: regular fights >= 90% wins (most at 100%, 4-9 rounds, 40-60% HP
left), mid-bosses 60-75%, bosses 45-60% (auto-battle; a player who uses items and support skills does better).
Results in handoff/balance.txt.
"""

# name: factor (engine auto-battle result at that factor; before)
OFFENCE = {
    # chapter 5
    'Grabghul': 0.675,            # regular "Ghule & Knecht" (with HP x0.75): 92-94% (was 25%: poison + agility debuff)
    'Der Eiserne Prinz': 0.90,    # boss: 50-60% (was 20-50%)
    # chapter 6
    'Messingsoldat': 0.75,        # regular "Soldaten & Oni": 100% (was 50%); "Messingsoldaten x3", "Gargylen & Soldat" 100%
    'Oni-Hauptmann': 0.90,        # mid, Torturm (with an Oni-Söldner and the tuned Messingsoldat): 69-85% (was 25-33%)
    'Seelenkessel': 0.87,         # boss: 56-60% in 13-17 rounds with HP x0.45 (was 0%: Seelenstrom drains the party)
    # chapter 7
    'Arenabestie': 0.775,         # mid, tournament round 2: 67-80% (was 6-17%: Hydrabiss hits two at full rate)
    'Spinnenkreis-Agent': 0.85,   # regular "Klinge & Agenten": 100% (was 50%: DEX 560 is AC 38, poison, webs)
    'Tsumugi': 0.88,              # boss (with the breakthrough to B on turn 2): ~45-50% (was 0-8%)
    # chapter 8
    'Werwolf': 0.80,              # regular: 94-100%, 5-6 rounds, 60% HP left (was 58-75%)
    'Rudelherr': 0.825,           # mid, optional: 50% (45-67% at 0.85, 92% at 0.80; was 0%)
    'Trollkönig': 0.975,          # boss: 50% in 11 rounds with HP x0.6 (was 13-17%, 13-26 rounds)
    'Mukuro': 0.96,               # boss: ~50% (was 33-38%)
    # chapter 9
    'Sirene': 0.85,               # regular "Sirenen x2", "Fomorer & Sirene": 100% (were 75% / 67%: sleep song, AC 41)
    'Ketos': 0.95,                # mid: 75% (75-90% at 0.925, 25-42% at 1.0)
    'Kraken': 0.80,               # with Shigure, boss: 50-65% (was 0-8%)
    'Shigure': 0.80,
    'Maō Kagerō': 0.96,           # final boss phase 1: ~50% (was 8-25%)
    'Hōkais Schatten': 0.925,     # final boss phase 2: 58% (was 6-8%)
}

# name: HP factor (fights that only got long when their offence came down)
HP = {
    'Grabghul': 0.75,
    'Seelenkessel': 0.45,
    'Trollkönig': 0.60,
}


def jsround(v):
    """Math.round, as the tuner applied it in the engine."""
    return int(v + 0.5)


def apply(enemies):
    for e in enemies:
        if not e:
            continue
        f = OFFENCE.get(e['name'])
        if f is not None:
            for i in (2, 4, 6):                 # STR, MAG, DEX (MZ's Attack, M.Attack, Agility boxes)
                e['params'][i] = max(1, jsround(e['params'][i] * f))
        h = HP.get(e['name'])
        if h is not None:
            e['params'][0] = max(1, jsround(e['params'][0] * h))
    return enemies
