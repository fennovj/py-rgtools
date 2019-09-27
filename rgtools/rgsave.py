import struct
from rgtools.resources import evaluate_cond


class RealmGrinderByteArray:

    _struct_formats = {
        'Bool': (1, '?'),
        'Uint8': (1, 'B'),
        'Int8': (1, 'b'),
        'Uint16': (2, 'H'),
        'Int16': (2, 'h'),
        'Uint32': (4, 'I'),
        'Int32': (4, 'i'),
        'Float32': (4, 'f'),
        'Float64': (8, 'd')
    }

    def __init__(self, data, endian='>'):
        # Data is a list of 8-bit integers
        self.data = data
        self.endian = endian

    def get(self, format, position):
        # This function uses struct to convert binary data to usable numbers
        # This function also returns the length of the data that was read
        # example: array.get('Uint32', 100) gets 4 bytes from 100-103
        if format == 'Array':
            return self.get_array(self, position)
        elif format == 'Object':
            return self.get_object(self, position)
        elif format in self._struct_formats:
            length, format_string = self._struct_formats[format]
            bits = self.data[position:(position+length)]
            return struct.unpack(self.endian + format_string, bytes(bits))[0], length
        raise ValueError("Format {} is not a valid format!".format(format))


class RealmGrinderSave:

    # The save is mainly just a dictionary
    # However, we add methods to evaluate expressions like
    # '_base/saveVersion' or 'directory/subdirectory/item'
    # Furthermore, there is logic to handle array elements
    # For example, we can even handle multidimensional lists with
    # an expression like 'arrayname/0/1'

    def __init__(self, save={}):
        self.save = save

    # Helper function that gets self.save and gets (by reference)
    # The subdict that corresponds to that (partial) key
    # Can also optionally create the subdir if it doesn't exist
    def _get_subdict(self, dirkeys, create=False):
        save_acc = self.save

        for key in dirkeys:
            if isinstance(save_acc, list):
                # If the save is a list, we are inside an array value
                # This is only allowed if the key is an integer
                if len(save_acc) == int(key) and create:
                    # In this case, the value must be a dictionary that doesn't exist yet
                    # We can safely create it if allowed
                    save_acc.append({})
                save_acc = save_acc[int(key)]
            elif key == '_base' or key == '':
                # This key means go back to base
                save_acc = self.save
            elif key == '_up' or key == '..':
                raise NotImplementedError("_up or .. are not supported")
            else:
                # only create subdicts if desired
                if key not in save_acc and create:
                    save_acc[key] = {}
                save_acc = save_acc[key]
        return save_acc

    def get(self, key):
        # Get the subdict, then the key, and just index. Will raise KeyError if key doesn't exist
        keys = key.split('/')
        subdict = self._get_subdict(keys[:-1])
        if isinstance(subdict, list):
            # If subdict is a list, then the final key must be an integer
            return subdict[int(keys[-1])]
        return subdict[keys[-1]]

    def create_or_append(self, key, value):
        # Similar to above, but this time, actually allow creation
        # This makes use of the fact that _get_subdict returns a reference
        # Also, if the key already exists, we try to append to the existing value.
        # This will obviously fail if the existing value is not a list.
        keys = key.split('/')

        subdict = self._get_subdict(keys[:-1], True)
        if isinstance(subdict, list):
            # The final subdict is an array, needs to be handled separately
            # key[-1] must be an integer
            if int(key[-1]) == len(subdict):
                subdict.append(value)
            else:
                subdict[int(key[-1])].append(value)
        # subdict is a regular dictionary, we can do a normal key check
        elif keys[-1] not in subdict:
            subdict[keys[-1]] = value
        else:
            subdict[keys[-1]].append(value)


def _apply_rule(rule, rgsave, rgarray, position):

    if 'stash' in rule:
        # These rules are not neccecary for reading, only writing
        # We still read them to affect position
        _, length = rgarray.get(rule['format'], position)
        return rgsave, position + length

    if 'cond' in rule:
        val1, comp, val2 = rule['cond'].split(' ')
        # Cond always has the form: 'savekey > 0'
        # where savekey needs a lookup in the save
        val1 = rgsave.get(val1)
        if not evaluate_cond(val1, comp, val2):
            # Condition is not met, rule is void
            return rgsave, position

    if rule['format'] == 'Jump':
        # This rule only affects position, not the save
        # We shift position by rule.amount
        if 'relative' in rule and rule['relative'] is False:
            return rgsave, rule['amount']
        else:
            return rgsave, position + rule['amount']

    elif rule['format'] not in ['Array', 'Object']:
        # These are the base cases where we can extract the value from rgarray
        # We get the dictionary key to create from rule.key
        value, length = rgarray.get(rule['format'], position)
        rgsave.create_or_append(rule['key'], value)
        return rgsave, position + length

    elif rule['format'] == 'Object':
        # These are essentially structs, with a fixed number of fields in rule.members
        # The key is the 'directory', each member gets created in that directory
        for member_rule in rule['members']:
            # Editing a key is not safe if the rule is evaluated multiple times by array
            # Therefore, after evaluating the rule, recover the original key
            backup = member_rule['key']
            member_rule['key'] = rule['key'] + '/' + member_rule['key']
            rgsave, position = _apply_rule(member_rule, rgsave, rgarray, position)
            member_rule['key'] = backup
        return rgsave, position

    elif rule['format'] == 'Array':
        # These are the most complex: first we get the length of the array,
        # Then we get all the elements of the array and place them in the save in the correct spot
        length, nbits = rgarray.get(rule['length']['format'], position)
        position = position + nbits

        # Create empty array for rgsave.create_or_append to work
        rgsave.create_or_append(rule['key'], [])
        # Now append all the sub-elements to the same key
        for i in range(length):
            rule['member']['key'] = rule['key'] + '/' + str(i)
            rgsave, position = _apply_rule(rule['member'], rgsave, rgarray, position)
        return rgsave, position

    raise ValueError("Rule format {} is not known!".format(rule['format']))


if __name__ == '__main__':
    save = RealmGrinderSave()

    arr = [2, 10, 11, 12, 13, 14, 15]
    rgarr = RealmGrinderByteArray(arr, '>')



    # 2 arrays: [2, 10, 11] (representing [10, 11]) and [2, 12, 13] (representing [12, 13])
    arr2 = [2, 2, 10, 11, 2, 12, 13]
    rgarr2 = RealmGrinderByteArray(arr2, '>')

    doublearrayrule = {'format': 'Array', 'key': 'mainarr',
                       'length': {'format': 'Uint8'},
                       'member': {'format': 'Array',
                                  'length': {'format': 'Uint8'},
                                  'member': {'format': 'Uint8'}
                                  }
                       }

    rgsave, position = _apply_rule(doublearrayrule, save, rgarr2, 0)
    print("Done")
    print(rgsave.save, position)
