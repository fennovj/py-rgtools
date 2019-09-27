import base64
import re
import zlib


def viginere(save, key):
    key_num = [ord(c) for c in key]
    for i in range(len(save)):
        save[i] = save[i] ^ key_num[i % len(key)]
    return save


def decode_save(save):
    struct_regex = r'^\$([0-9]{2})s(.*)\$e$'
    viginere_key = 'therealmisalie'

    # Remove first 3 and last 2 characters
    save = re.compile(struct_regex).match(save).group(2)
    save = base64.b64decode(save)
    save = zlib.decompress(save)
    save = viginere(list(save), viginere_key)
    return save


# Helper function to evaluate stuff like [26, '>=', '25']
# only works on integers
def evaluate_cond(val1, comp, val2):
    val1, val2 = int(val1), int(val2)
    if comp == '==':
        return val1 == val2
    elif comp == '>=':
        return val1 >= val2
    elif comp == '>':
        return val1 > val2
    elif comp == '<=':
        return val1 <= val2
    elif comp == '<':
        return val1 < val2
    raise ValueError('Comparator {} not supported!'.format(comp))


# This array essentially describes all the steps required in decoding a save
# The order of this array matters, since many steps require the values from previous steps
def get_formats():
    return [
           {'format': 'Uint16', 'key': 'saveVersion'},
           {'format': 'Uint16', 'key': 'newField32'},
           {'format': 'Uint16', 'key': 'playfabSeason'},
           {'format': 'Uint16', 'key': 'seasonN', 'cond': '_base/saveVersion >= 27'},
           {'format': 'Jump', 'amount': 2, 'cond': '_base/saveVersion < 27'},
           {'format': 'Uint16', 'key': 'halloweenMonsters', 'cond': '_base/saveVersion >= 24'},
           {'format': 'Jump', 'amount': 2, 'cond': '_base/saveVersion < 24'},
           {'format': 'Uint16', 'key': 'breathEffects', 'cond': '_base/saveVersion >= 24'},
           {'format': 'Jump', 'amount': 2, 'cond': '_base/saveVersion < 24'},
           {'format': 'Uint32', 'key': 'eggRngState', 'cond': '_base/saveVersion >= 15'},
           {'format': 'Jump', 'amount': 4, 'cond': '_base/saveVersion < 15'},
           {'format': 'Uint16', 'key': 'eggStackSize', 'cond': '_base/saveVersion >= 15'},
           {'format': 'Jump', 'amount': 2, 'cond': '_base/saveVersion < 15'},
           {'format': 'Uint16', 'key': 'ctaFactionCasts'},
           {'format': 'Uint32', 'key': 'alignment', 'stash': '_index'},
           {'format': 'Uint32', 'key': 'options', 'stash': '_index'},
           {'format': 'Array', 'key': 'buildings',
            'length': {'format': 'Uint16', 'key': 'buildings', 'stash': '_len'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Uint32', 'key': 'id'},
                {'format': 'Uint32', 'key': 'q'},
                {'format': 'Float64', 'key': 't'},
                {'format': 'Float64', 'key': 'm'},
                {'format': 'Float64', 'key': 'r'},
                {'format': 'Float64', 'key': 'e'},
            ]},
            },
           {'format': 'Array', 'key': 'upgrades',
            'length': {'format': 'Uint16', 'key': 'upgrades', 'stash': '_len'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Uint32', 'key': 'id'},
                {'format': 'Bool', 'key': 'u1'},
                {'format': 'Bool', 'key': 'u2', 'cond': '_base/saveVersion >= 1'},
                {'format': 'Bool', 'key': 'u3', 'cond': '_base/saveVersion >= 18'},
                {'format': 'Uint32', 'key': 's'},
            ]},
            },
           {'format': 'Array', 'key': 'trophies',
            'length': {'format': 'Uint16', 'key': 'trophies', 'stash': '_len'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Uint32', 'key': 'id'},
                {'format': 'Bool', 'key': 'u1', 'cond': '_base/saveVersion >= 18'},
                {'format': 'Uint8', 'key': 'u2', 'cond': '_base/saveVersion >= 27'},
            ]},
            },
           {'format': 'Uint32', 'key': 'artifactRngState', 'cond': '_base/saveVersion >= 4'},
           {'format': 'Array', 'key': 'spells',
            'length': {'format': 'Uint16', 'key': 'spells', 'stash': '_len'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Uint32', 'key': 'id'},
                {'format': 'Int32', 'key': 't'},
                {'format': 'Bool', 'key': 'a'},
                {'format': 'Int32', 'key': 'n'},
                {'format': 'Int32', 'key': 'n2'},
                {'format': 'Int32', 'key': 'n3', 'cond': '_base/saveVersion >= 5'},
                {'format': 'Int32', 'key': 'tierstat1', 'cond': '_base/saveVersion >= 22'},
                {'format': 'Int8', 'key': 'activeTiers', 'cond': '_base/saveVersion >= 23'},
                {'format': 'Float64', 'key': 'c'},
                {'format': 'Float64', 'key': 'r'},
                {'format': 'Float64', 'key': 'e'},
                {'format': 'Float64', 'key': 'active0'},
                {'format': 'Float64', 'key': 'active1'},
                {'format': 'Float64', 'key': 'active2'},
                {'format': 'Uint32', 'key': 's'},
            ]},
            },
           {'format': 'Int8', 'key': 'alignment'},
           {'format': 'Int8', 'key': 'faction'},
           {'format': 'Int8', 'key': 'prestigeFaction'},
           {'format': 'Int8', 'key': 'elitePrestigeFaction', 'cond': '_base/saveVersion >= 40'},
           {'format': 'Float64', 'key': 'gems'},
           {'format': 'Uint16', 'key': 'reincarnation'},
           {'format': 'Uint16', 'key': 'ascension', 'cond': '_base/saveVersion >= 14'},
           {'format': 'Int8', 'key': 'secondaryAlignment', 'cond': '_base/saveVersion >= 32'},
           {'format': 'Uint32', 'key': 'lastsave'},
           {'format': 'Float64', 'key': 'mana'},
           {'format': 'Float64', 'key': 'coins'},
           {'format': 'Float64', 'key': 'rubies', 'cond': '_base/saveVersion >= 4'},
           {'format': 'Float64', 'key': 'excavations', 'cond': '_base/saveVersion >= 4'},
           {'format': 'Array', 'key': 'factionCoins',
            'length': {'format': 'Uint16', 'key': 'factionCoins'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Float64', 'key': 'factionCoins'},
                {'format': 'Uint32', 'key': 'royalExchanges'},
            ]},
            },
           {'format': 'Array', 'key': 'eventResources', 'cond': 'saveVersion >= 7',
            'length': {'format': 'Uint16', 'key': '_len/eventResources'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Float64', 'key': 'res'},
            ]},
            },
           {'format': 'Array', 'key': 'stats',
            'length': {'format': 'Uint16', 'key': '_len/stats'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Float64', 'key': 'stats'},
                {'format': 'Float64', 'key': 'statsReset'},
                {'format': 'Float64', 'key': 'statsRei'},
            ]},
            },
           {'format': 'Array', 'key': 'lineageLevels', 'cond': 'saveVersion >= 29',
            'length': {'format': 'Uint16', 'key': '_len/lineageLevels'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Float64', 'key': 'lev'},
            ]},
            },
           {'format': 'Bool', 'key': 'contingency'},
           {'format': 'Float64', 'key': 'contingencyValue'},
           {'format': 'Int8', 'key': 'strikeTier'},
           {'format': 'Int32', 'key': 'miracleTier', 'cond': '_base/saveVersion >= 3'},
           {'format': 'Int32', 'key': 'miracleTimer', 'cond': '_base/saveVersion >= 3'},
           {'format': 'Array', 'key': 'catalystTargets', 'cond': '_base/saveVersion >= 43',
            'length': {'format': 'Int8', 'key': '_len/catalystTargets'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Uint32', 'key': 'targetspell'},
            ]},
            },
           {'format': 'Array', 'key': 'maelstromTargets', 'cond': '_base/saveVersion >= 43',
            'length': {'format': 'Int32', 'key': '_len/maelstromTargets'},
            'member': {'format': 'Object', 'members': [
                {'format': 'Int8', 'key': 'targeteffect'},
            ]},
            },
           {'format': 'Uint32', 'key': 'LimitedWishTarget', 'cond': '_base/saveVersion >= 48'},
           {'format': 'Float64', 'key': 'LimitedWishStrength', 'cond': '_base/saveVersion >= 48'},
           {'format': 'Int8', 'key': 'snowballScryUses', 'cond': '_base/saveVersion >= 9'},
           {'format': 'Uint16', 'key': 'snowballSize', 'cond': '_base/saveVersion >= 9'},
           {'format': 'Uint32', 'key': 'lastGiftDate', 'cond': '_base/saveVersion >= 9'},
           {'format': 'Int32', 'key': 'chargedTimer'},
           {'format': 'Int32', 'key': 'comboStrike', 'cond': '_base/saveVersion <= 15'},
           {'format': 'Float64', 'key': 'comboStrikeCont', 'cond': '_base/saveVersion >= 39'},
           {'format': 'Int32', 'key': 'comboStrikeCont', 'cond': '_base/saveVersion < 39'},
           {'format': 'Int32', 'key': 'goblinTimer'},
           {'format': 'Int32', 'key': 'wealthStormTimer', 'cond': '_base/saveVersion >= 11'},
           {'format': 'Int32', 'key': 'hourGlassTimer', 'cond': '_base/saveVersion >= 36'},
           {'format': 'Uint32', 'key': 'dreamcatcher1', 'cond': '_base/saveVersion >= 35'},
           {'format': 'Float64', 'key': 'dreamcatcher2', 'cond': '_base/saveVersion >= 35'},
           {'format': 'Uint32', 'key': 'faceunion1', 'cond': '_base/saveVersion >= 38'},
           {'format': 'Int32', 'key': 'faceunion2', 'cond': '_base/saveVersion >= 38'},
           {'format': 'Uint32', 'key': 'djinnchallenge4_1', 'cond': '_base/saveVersion >= 45'},
           {'format': 'Int32', 'key': 'djinnchallenge4_2', 'cond': '_base/saveVersion >= 45'},
           {'format': 'Uint32', 'key': 'mercSpell1'},
           {'format': 'Uint32', 'key': 'mercSpell2'},
           {'format': 'Uint32', 'key': 'mercExtraUpgrade', 'cond': '_base/saveVersion >= 47'},
           {'format': 'Uint32', 'key': 'mercUnion', 'cond': '_base/saveVersion >= 42'},
           {'format': 'Int32', 'key': 'cTimer'},
           {'format': 'Int32', 'key': 'kcTimer'},
           {'format': 'Int32', 'key': 'mTimer'},
           {'format': 'Float64', 'key': 'sTimer'},
           {'format': 'Float64', 'key': 'oTimer'},
           {'format': 'Float64', 'key': 'oTimer2'},
           {'format': 'Float64', 'key': 'oTimer3', 'cond': '_base/saveVersion >= 13'},
           {'format': 'Int8', 'key': 'season', 'cond': '_base/saveVersion >= 2'},
           {'format': 'Int8', 'key': 'bFaction'},
           {'format': 'Int8', 'key': 'combinationBL', 'cond': '_base/saveVersion >= 31'},
           {'format': 'Int8', 'key': 'lineageFaction', 'cond': '_base/saveVersion >= 29'},
           {'format': 'Int8', 'key': 'artifactSet', 'cond': '_base/saveVersion >= 35'},
           {'format': 'Int8', 'key': 'stoneheartSet', 'cond': '_base/saveVersion >= 44'},
           {'format': 'Int8', 'key': 'buyMode'},
           {'format': 'Int8', 'key': 'excavBuyMode', 'cond': '_base/saveVersion >= 10'},
           {'format': 'Int8', 'key': 'reBuyMode', 'cond': '_base/saveVersion >= 20'},
           {'format': 'Uint32', 'key': 'consecutiveDays', 'cond': '_base/saveVersion >= 41'},
           {'format': 'Uint32', 'key': 'currentDay', 'cond': '_base/saveVersion >= 41'},
           {'format': 'Uint32', 'key': 'other21'},
           {'format': 'Int8', 'key': 'saveRevision'},
           {'format': 'Object', 'key': 'options', 'members': [
                {'format': 'Int8', 'key': 'len'},
                {'format': 'Int8', 'key': 'notation'},
                {'format': 'Int8', 'key': 'thousands_sep'},
                {'format': 'Int8', 'key': 'block_bg_clicks'},
                {'format': 'Int8', 'key': 'disable_upgrade_groups'},
                {'format': 'Int8', 'key': 'disable_trophy_groups'},
                {'format': 'Int8', 'key': 'sort_purchased_upgrades'},
                {'format': 'Int8', 'key': 'sort_unpurchased_upgrades'},
                {'format': 'Int8', 'key': 'hide_purchased_upgrades'},
                {'format': 'Int8', 'key': 'disable_tutorials'},
                {'format': 'Int8', 'key': 'hide_unavail_research'},
                {'format': 'Int8', 'key': 'disable_buymax_button'},
                {'format': 'Int8', 'key': 'disable_click_particles'},
                {'format': 'Int8', 'key': 'disable_click_text'},
                {'format': 'Int8', 'key': 'disable_gift_of_heroes'},
                {'format': 'Int8', 'key': 'disable_gift_of_kings'},
                {'format': 'Int8', 'key': 'disable_gift_of_gods'},
                {'format': 'Int8', 'key': 'disable_ruby_warning'},
                {'format': 'Int8', 'key': 'disable_exchange_warning'},
                {'format': 'Int8', 'key': 'enable_extended_lists'},
                {'format': 'Int8', 'key': 'disable_cloud_check'},
                {'format': 'Int8', 'key': 'disable_sliding_menu'},
                {'format': 'Int8', 'key': 'buy_all_exchanges'},
                {'format': 'Int8', 'key': 'disable_multibuy_series'},
                {'format': 'Int8', 'key': 'disable_upgrade_stacks'},
                {'format': 'Int8', 'key': 'disable_trophy_stacks'},
                {'format': 'Int8', 'key': 'disable_autoclicks'},
                {'format': 'Int8', 'key': 'spell_tooltips_persist'},
                {'format': 'Int8', 'key': 'buy_all_upgrades'},
            ]},
           {'format': 'Object', 'key': 'tutorials', 'members': [
                {'format': 'Int8', 'key': 'len'},
                {'format': 'Int8', 'key': 'click_on_bg'},
                {'format': 'Int8', 'key': 'buy_a_farm'},
                {'format': 'Int8', 'key': 'find_FCs'},
                {'format': 'Int8', 'key': 'upgrades_spells'},
                {'format': 'Int8', 'key': 'choose_alignment'},
                {'format': 'Int8', 'key': 'choose_faction'},
                {'format': 'Int8', 'key': 'exchanges'},
                {'format': 'Int8', 'key': 'trophies_tutorial'},
                {'format': 'Int8', 'key': 'abdication_gems'},
                {'format': 'Int8', 'key': 'buyall_shop'},
                {'format': 'Int8', 'key': 'archeology'},
                {'format': 'Int8', 'key': 'excavation_system'},
                {'format': 'Int8', 'key': 'ruby_upgrades'},
                {'format': 'Int8', 'key': 'reincarnations'},
                {'format': 'Int8', 'key': 'reinc_power'},
                {'format': 'Int8', 'key': 'challenges'},
                {'format': 'Int8', 'key': 'mercs'},
                {'format': 'Int8', 'key': 'bloodline_upgrade'},
                {'format': 'Int8', 'key': 'spiritual_surge'},
                {'format': 'Int8', 'key': 'faction_quests'},
                {'format': 'Int8', 'key': 'unique_buildings'},
                {'format': 'Int8', 'key': 'research_system'},
                {'format': 'Int8', 'key': 'ascension_system'},
                {'format': 'Int8', 'key': 'ascension_diamond_coins'},
                {'format': 'Int8', 'key': 'ascension_emerald_coins'},
                {'format': 'Int8', 'key': 'ascension_amethyst_coins'},
                {'format': 'Int8', 'key': 'artifact_set_tutorial'},
                {'format': 'Int8', 'key': 'new1'},
                {'format': 'Int8', 'key': 'new2'},
                {'format': 'Int8', 'key': 'new3'},
                {'format': 'Int8', 'key': 'new4'},
                {'format': 'Int8', 'key': 'new5'},
                {'format': 'Int8', 'key': 'new6'}
            ]}
    ]
