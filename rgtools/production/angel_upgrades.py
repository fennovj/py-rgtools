import math
# This file is a first attempt at modelling some of the upgrades
# This file is meant to be somewhat compact and easy to write
# An internal representation of upgrades may be more complex

# TODO ascension nerfs
# TODO the numbers don't seem to match exactly?
angel_upgrades = [
    ('cathedrals', 'mana_regen', lambda x: x**0.28, 'additive'),
    ('spells_cast_game', 'production_building', lambda x: 1.5*(x**0.85), 'percent'),
    ([], 'mana_regen', 40, 'percent'),
    ('royalcastles', 'mana_regen', lambda x: x**0.305, 'additive'),
    ([], 'spell_cost', -100, 'additive'),
    ([], 'mana_regen', 60, 'percent'),
    ('heavensgates', 'mana_regen', lambda x: x**0.33, 'additive'),
    ([], 'spell_duration', 50, 'percent'),
    ('mana_regen', 'production_building', lambda x: 3*(x**0.85), 'percent'),
    [
        ('cathedrals', 'gemgrinder_effect', lambda x: 0.65*(x**0.65), 'percent'),
        ('cathedrals', 'dragonsbreath_effect', lambda x: 0.65*(x**0.65), 'percent'),
        # Below bonus does not affect gg/db
        ('cathedrals', 'spell_tier', lambda x: 0.02 * math.log(1+x), 'additive')
    ],
    ('spells_time_game', 'factionfind', lambda x: 0.7*(x**0.7), 'percent'),
    ([], ('mana_max', 'mana_regen', 'factionfind', 'assistants'), (200, 200, 200, 200), 'percent')


]

# Miscelaneous other upgrades
other_upgrades = [
    [
        # Crop rotation
        ([], 'farm_production', 100, 'percent'),
        ([], 'assistants', 1, 'additive')
    ]
]