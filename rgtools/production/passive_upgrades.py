# Passive upgrades are those that are always active
# They exist as a patchwork for certain upgrade-like behavior that is not an upgrade, but can be
# represented as one. For example, Hall of Legends produce 250k per trophy, which can more
# easily be represented as an upgrade than be baked in the game logic.

passive_upgrades = [
    ('s_trophies', 'b_halloflegends_production', lambda x: x*25e4, 'additive')
]
