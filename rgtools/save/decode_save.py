import base64
import re
import zlib
import json

from rgtools.raw.save_formats import get_formats
from .realmgrindersave import RealmGrinderSave
from .realmgrinderstruct import RealmGrinderByteArray


def evaluate_cond(val1, comp, val2):
    # Function to evaluate inputs like: '27', '>=', '25'
    # val1 and val2 must be integers
    # comp must be one of ['==', '>=', '>', '<=', '<']
    # This function returns a boolean
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


def viginere(save, key):
    key_num = [ord(c) for c in key]
    for i in range(len(save)):
        save[i] = save[i] ^ key_num[i % len(key)]
    return save


def decode_save(save):
    # Undoes the encoding on the save file, to turn it into an actual struct
    # This is neccecary before a bytearray can be created.
    struct_regex = r'^\$([0-9]{2})s(.*)\$e$'
    viginere_key = 'therealmisalie'

    # Remove first 3 and last 2 characters
    save = re.compile(struct_regex).match(save).group(2)
    save = base64.b64decode(save)
    save = zlib.decompress(save)
    save = viginere(list(save), viginere_key)
    return save


def _apply_rule(rule, rgsave, rgarray):

    if 'stash' in rule:
        # These rules are not neccecary for reading, only writing
        # We still read them, but only to affect the rgarray position
        _ = rgarray.get(rule['format'])
        return

    if 'cond' in rule:
        val1, comp, val2 = rule['cond'].split(' ')
        # Cond always has the form: 'key > val2'
        # where key needs a lookup in the save
        val1 = rgsave.get(val1)
        if not evaluate_cond(val1, comp, val2):
            # Condition is not met, rule is void
            return

    if rule['format'] == 'Jump':
        # This rule only affects position, not the save
        # We shift position by rule.amount
        if 'relative' in rule and rule['relative'] is False:
            rgarray.jump(rule['amount'], False)
        else:
            rgarray.jump(rule['amount'], True)
        return

    elif rule['format'] not in ['Array', 'Object']:
        # These are the base cases where we can extract the value from rgarray
        # rule.format is something like 'Uint32'
        # rule.key is the key in the save dictionary where to save the value
        value = rgarray.get(rule['format'])
        rgsave.create_or_append(rule['key'], value)
        return

    elif rule['format'] == 'Object':
        # These are essentially structs, with a fixed number of fields in rule.members
        # The key is the 'directory', each member gets created in that directory
        for member_rule in rule['members']:
            # Editing a key is not safe if the rule is evaluated multiple times.
            # This can happen in an array of objects.
            # Therefore, after evaluating the rule, recover the original key
            backup = member_rule['key']
            member_rule['key'] = rule['key'] + '/' + member_rule['key']
            _apply_rule(member_rule, rgsave, rgarray)
            member_rule['key'] = backup
        return

    elif rule['format'] == 'Array':
        # First we get the length of the array, without putting it in the save
        # Then we get all the elements of the array and place them in the save in the correct spot
        length = rgarray.get(rule['length']['format'])

        # Create empty array for rgsave.create_or_append to work correctly
        rgsave.create_or_append(rule['key'], [])

        # Now append all the sub-elements to the same key
        for i in range(length):
            rule['member']['key'] = rule['key'] + '/' + str(i)
            _apply_rule(rule['member'], rgsave, rgarray)
        return

    raise ValueError("Rule format {} is not known!".format(rule['format']))


def read_save(fname):
    # Input is a filename, output is a 'RealmGrinderSave' object
    with open(fname, 'r') as f:
        save = f.read()

    rgdata = RealmGrinderByteArray(decode_save(save))
    rgsave = RealmGrinderSave()

    for rule in get_formats():
        _apply_rule(rule, rgsave, rgdata)

    return rgsave


def read_json(fname):
    with open(fname, 'r') as f:
        save = f.read()
    return RealmGrinderSave(json.loads(save))
