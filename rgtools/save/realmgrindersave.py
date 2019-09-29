import json


class RealmGrinderSave:

    # The save is mainly just a dictionary
    # However, we add methods to evaluate expressions like
    # '_base/saveVersion' or 'directory/subdirectory/item'
    # Furthermore, there is logic to handle array elements
    # For example, we can even handle multidimensional lists with
    # an expression like 'arrayname/0/1'

    def __getitem__(self, arg):
        '''
        Simple indexing for RG saves. Simply treat the save as a dictionary
        :param arg: The key from the save. For example: 'rubies'
        :returns: The value from the save. For example: 50
        '''
        return self.save[arg]

    def __init__(self, save={}):
        '''
        Initialize a RG save object. Optionally with a pre-filled dictionary.
        '''
        self.save = save

    def get(self, key):
        '''
        Accessing the dictionary with a custom string format
        This format looks like '_base/key/subkey'
        Also supports arrays: 'arrayname/2' for the 3rd element in the array
        :param arg: key the string describing the required key
        :returns: value from the save
        '''
        # Get the subdict, then the key, and just index. Will raise KeyError if key doesn't exist
        keys = key.split('/')
        subdict = self._get_subdict(keys[:-1])

        if isinstance(subdict, list):
            # If subdict is a list, then the final key must be an integer
            return subdict[int(keys[-1])]
        else:
            # Subdict is a dictionary, we can index it normally
            return subdict[keys[-1]]

    def _get_subdict(self, dirkeys, create=False):
        '''
        Helper function that gets self.save and gets (by reference)
        The subdict that corresponds to that (partial) key
        Can also optionally create the subdir if it doesn't exist
        '''
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
            else:
                # This means save_acc is a dictionary, parse it normally
                if key == '_base' or key == '':
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

    def create_or_append(self, key, value):
        '''
        Method for changing the content of the save, with the same key format as 'get'
        If the key already exists, instead try appending the value to the existing value
        This will fail if the value already exists but is not a list
        :param key: Key to create or append to. For example: '_base/group/valuename'
        :param value: The value to fill in the save
        '''
        # Also, if the key already exists, we try to append to the existing value.
        keys = key.split('/')
        subdict = self._get_subdict(keys[:-1], True)

        if isinstance(subdict, list):
            # The final subdict is an array, so key[-1] must be an integer
            # We only append if key[-1] refers to the next element that doesn't exist yet
            if int(key[-1]) == len(subdict):
                subdict.append(value)
            else:
                subdict[int(key[-1])].append(value)
        else:
            # subdict is a regular dictionary, we can do a normal key check
            # If the value already exists, we blindly append without checking the type of the value
            if keys[-1] not in subdict:
                subdict[keys[-1]] = value
            else:
                subdict[keys[-1]].append(value)

    def write(self, fname, pretty=True):
        '''
        Writes the save to a JSON file
        :param fname: filename to write to
        :param pretty: Wether or not to pretty-print
        '''
        with open(fname, 'w') as file:
            if pretty:
                file.write(json.dumps(self.save, sort_keys=True, indent=4, separators=(',', ': ')))
            else:
                file.write(json.dumps(self.save))
