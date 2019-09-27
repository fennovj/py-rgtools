import struct


class RealmGrinderByteArray():

    struct_formats = {
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

    def __init__(self, data, endian):
        # Data is a list of 8-bit integers
        self.data = data
        self.endian = endian

    def get_array(self, position):
        pass

    def get_object(self, position):
        pass

    def get_data(self, format, position):
        # This function also returns the length of the data that was read
        if format == 'Array':
            return self.get_array(self, position)
        elif format == 'Object':
            return self.get_object(self, position)
        elif format in self.struct_formats:
            length, format_string = self.struct_formats[format]
            bits = self.data[position:(position+length)]
            return struct.unpack(self.endian + format_string, bytes(bits))[0], length
        raise ValueError("Format {} is not a valid format!".format(format))


class RealmGrinderSave():

    # The save is mainly just a dictionary
    # However, we add methods to evaluate expressions like
    # '_base/saveVersion >= 43' or '_len/maelstromTargets'

    def __init__(self, save={}):
        self.save = save

    # Helper function that gets self.save and gets (by reference)
    # The subdict that corresponds to that (partial) key
    # Can also optionally create the subdir if it doesn't exist
    def _get_subdict(self, dirkeys, create=False):
        save_acc = self.save

        for key in dirkeys:
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

    def get_value(self, key):
        # Get the subdict, then the key, and just index
        # Will raise KeyError if key doesn't exist
        keys = key.split('/')
        subdict = self._get_subdict(keys[:-1])
        return subdict[keys[-1]]

    def create_or_update_value(self, key, value):
        # Similar to above, but this time, actually allow creation
        # This makes use of the fact that _get_subdict returns a reference
        keys = key.split('/')
        subdict = self._get_subdict(keys[:-1], True)
        subdict[keys[-1]] = value


if __name__ == '__main__':
    save_dict = {'stuff': {'sub': 3}}
    save = RealmGrinderSave(save_dict)
    x = save.get_value('_base/stuff/sub')
    print(x)
    print(save.save)
    x = save.create_or_update_value('_base/stuff/new', 2)
    print(x)
    print(save.save)

    # Test bytearray
    arr = [130, 133, 248, 102, 102, 255, 55, 243, 135, 229]
    rgarr = RealmGrinderByteArray(arr, '>')
    print(rgarr.get_data('Bool', 9))
