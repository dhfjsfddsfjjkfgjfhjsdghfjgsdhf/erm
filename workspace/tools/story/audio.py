"""Audio file names available in the MZ project (RTP, checked on the user's PC)."""
def _r(prefix, a, b):
    return {f'{prefix}{i}' for i in range(a, b + 1)}

BGM = set().union(_r('Battle', 1, 8), _r('Castle', 1, 3), _r('Dungeon', 1, 7), _r('Field', 1, 4), _r('Scene', 1, 9),
                  _r('Ship', 1, 3), _r('Theme', 1, 6), _r('Town', 1, 8))
BGS = {'City', 'Clock', 'Darkness', 'Drips', 'Night', 'River', 'Sea'} | _r('Fire', 1, 3) | _r('People', 1, 2) | \
      _r('Quake', 1, 2) | _r('Rain', 1, 4) | _r('Storm', 1, 2) | _r('Waterfall', 1, 2) | _r('Wave', 1, 2) | _r('Wind', 1, 5)
ME = {'Gag', 'Horror', 'Item', 'Like', 'Mystery', 'Organ', 'Refresh'} | _r('Curse', 1, 2) | _r('Defeat', 1, 2) | \
     _r('Fanfare', 1, 3) | _r('Gameover', 1, 2) | _r('Inn', 1, 2) | _r('Musical', 1, 3) | _r('Shock', 1, 3) | \
     _r('Victory', 1, 3)
SE = {'Autodoor', 'Barrier', 'Bite', 'Blind', 'Break', 'Breath', 'Cat', 'Chain', 'Chicken', 'Coin', 'Computer', 'Confuse',
      'Cow', 'Crash', 'Crossbow', 'Crow', 'Disappointment', 'Dive', 'Dog', 'Electrocardiogram', 'Fall', 'Frog', 'Growl',
      'Hammer', 'Horn', 'Horse', 'Key', 'Knock', 'Laugh', 'Launch', 'Leakage', 'Liquid', 'Machine', 'Miss', 'Neon', 'Noise',
      'Parry', 'Phone', 'Poison', 'Pollen', 'Powerup', 'Push', 'Recovery', 'Reflection', 'Resonance', 'Run', 'Sand',
      'Scream', 'Sheep', 'Silence', 'Siren', 'Sleep', 'Splash', 'Stare', 'Starlight', 'Summon', 'Teleport', 'Transceiver',
      'Twine', 'Wolf'} | _r('Absorb', 1, 2) | _r('Applause', 1, 2) | _r('Attack', 1, 3) | _r('Battle', 1, 6) | \
     _r('Bell', 1, 3) | _r('Blow', 1, 10) | _r('Book', 1, 2) | _r('Bow', 1, 5) | _r('Buzzer', 1, 3) | _r('Cancel', 1, 3) | \
     _r('Chest', 1, 2) | _r('Chime', 1, 2) | _r('Close', 1, 3) | _r('Collapse', 1, 4) | _r('Cry', 1, 2) | \
     _r('Cursor', 1, 4) | _r('Damage', 1, 5) | _r('Darkness', 1, 8) | _r('Decision', 1, 5) | _r('Devil', 1, 3) | \
     _r('Door', 1, 8) | _r('Down', 1, 7) | _r('Earth', 1, 5) | _r('Equip', 1, 3) | _r('Evasion', 1, 2) | \
     _r('Explosion', 1, 4) | _r('Fire', 1, 9) | _r('Flash', 1, 3) | _r('Float', 1, 2) | _r('Fog', 1, 2) | \
     _r('Gate', 1, 2) | _r('Gun', 1, 3) | _r('Heal', 1, 7) | _r('Ice', 1, 11) | _r('Item', 1, 3) | _r('Jump', 1, 2) | \
     _r('Laser', 1, 2) | _r('Load', 1, 2) | _r('Magic', 1, 12) | _r('Monster', 1, 10) | _r('Move', 1, 10) | \
     _r('Open', 1, 9) | _r('Paralyze', 1, 3) | _r('Particles', 1, 4) | _r('Raise', 1, 3) | _r('Saint', 1, 9) | \
     _r('Save', 1, 2) | _r('Shop', 1, 2) | _r('Shot', 1, 3) | _r('Skill', 1, 3) | _r('Slash', 1, 10) | \
     _r('Sound', 1, 3) | _r('Switch', 1, 3) | _r('Sword', 1, 7) | _r('Thunder', 1, 14) | _r('Up', 1, 8) | \
     _r('Water', 1, 5) | _r('Wind', 1, 11)

KINDS = {'bgm': BGM, 'bgs': BGS, 'me': ME, 'se': SE}

def check(kind, name):
    if name and name not in KINDS[kind]:
        raise ValueError(f'unknown {kind} "{name}"')
    return name
