import struct


class RealmGrinderByteArray:

    # This is essentially a version of javascript DataView
    # Also, it has a built in memory of the 'position' that is being read

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

    def __init__(self, data, endian='>', position=0):
        # Data is a list of 8-bit integers
        self.data = data
        self.endian = endian
        self.position = position

    def get(self, format):
        if format in self._struct_formats:
            length, format_string = self._struct_formats[format]
            bits = self.data[self.position:(self.position+length)]
            self.position += length
            return struct.unpack(self.endian + format_string, bytes(bits))[0]
        raise ValueError("Format {} is not a valid format!".format(format))

    def jump(self, amount, relative=True):
        # Affect position without reading anything
        if not relative:
            self.position = amount
        else:
            self.position += amount
