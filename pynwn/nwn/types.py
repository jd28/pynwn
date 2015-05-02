import struct, sys
from pynwn.util.helper import get_encoding

class NWByte(object):
    type_id   = 0
    type      = 'byte'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWByte(struct.unpack('B3x', source.read(4))[0])

    def pack(self):
        return struct.pack('B3x', self.val)

class NWChar(object):
    type_id   = 1
    type      = 'char'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWChar(struct.unpack('c3x', source.read(4))[0])

    def pack(self):
        return struct.pack('c3x', self.val)

class NWWord(object):
    type_id   = 2
    type      = 'word'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWWord(struct.unpack('H2x', source.read(4))[0])

    def pack(self):
        return struct.pack('H2x', self.val)

class NWShort(object):
    type_id   = 3
    type      = 'short'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWShort(struct.unpack('h2x', source.read(4))[0])

    def pack(self):
        return struct.pack('h2x', self.val)

class NWDword(object):
    type_id   = 4
    type      = 'dword'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWDword(struct.unpack('I', source.read(4))[0])

    def pack(self):
        return struct.pack('I', self.val)

class NWInt(object):
    type_id   = 5
    type      = 'int'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWInt(struct.unpack('i', source.read(4))[0])

    def pack(self):
        return struct.pack('i', self.val)

class NWDword64(object):
    type_id   = 6
    type      = 'dword64'
    at_offset = True

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source, offset):
        source.seek(offset)
        return NWDword64(struct.unpack('Q', source.read(8))[0])

    def pack(self):
        return struct.pack('Q', self.val)

class NWInt64(object):
    type_id = 7
    type    = 'int64'
    at_offset = True

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source, offset):
        source.seek(offset)
        return NWInt64(struct.unpack('q', source.read(8))[0])

    def pack(self):
        return struct.pack('q', self.val)

class NWFloat(object):
    type_id   = 8
    type      = 'float'
    at_offset = False

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source):
        return NWFloat(struct.unpack('f', source.read(4))[0])

    def pack(self):
        return struct.pack('f', self.val)

class NWDouble(object):
    type_id   = 9
    type      = 'double'
    at_offset = True

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.val)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    @staticmethod
    def unpack(source, offset):
        source.seek(offset)
        return NWDouble(struct.unpack('d', source.read(8))[0])

    def pack(self):
        return struct.pack('d', self.val)

class NWString(object):
    type_id   = 10
    type      = 'cexostr'
    at_offset = 'data'

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.val

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        if not isinstance(val, str):
            raise ValueError("NWString Incorrect Type: %s" % type(val))

        self.val = val

    @staticmethod
    def unpack(source, offset):
        """Parses a gff cexostring."""

        source.seek(offset)
        length = struct.unpack('I', source.read(4))[0]
        pattern = "%ds" % length
        data = struct.unpack(pattern, source.read(length))[0].decode(get_encoding())

        return NWString(data)

    def pack(self):
        """Writes the specified data as a cexostring and returns it."""

        length = len( self.val )
        pattern = "I%ds" % length
        return struct.pack(pattern, length, self.val.encode('utf-8'))

class NWResref(object):
    type_id   = 11
    type      = 'resref'
    at_offset = 'data'

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.val

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        if not isinstance(val, str):
            raise ValueError("NWResref Incorrect Type: %s" % type(val))
        elif len(val) > 16:
            raise ValueError("NWResref strings must be no more than 16 characers.")
        self.val = val

    @staticmethod
    def unpack(source, offset):
        """Parses a gff resref."""

        # identify the current position, read and parse the resref, and return to the current position
        source.seek(offset)
        length = struct.unpack('B', source.read(1))[0]
        if length == 0:
            val = ''
        else:
            pattern = "%ds" % length
            val = struct.unpack(pattern, source.read(length))[0].decode(get_encoding())

        return NWResref(val)

    def pack(self):
        """Writes the specified data as a resref and returns it."""

        length = len(self.val)
        pattern = "B%ds" % length
        return struct.pack(str.encode(pattern), length, str.encode(self.val))

class NWLocalizedString(object):
    type_id   = 12
    type      = 'cexolocstr'
    at_offset = 'data'

    def __init__(self, strref, entry_list):
        self._strref = strref
        self.strings = entry_list

    def __getitem__(self, lang):
        for string in self.strings:
            if string[0] == lang:
                return string[1]

    def __setitem__(self, lang, new_string):
        if not isinstance(new_string, str):
            raise ValueError("NWResref Incorrect Type: %s" % type(new_string))

        for string in self.strings:
            if string[0] == lang:
                string[1] = new_string
                return

        self.strings.append([lang, new_string])

    @property
    def strref(self):
        return self._strref

    @strref.setter
    def strref(self, val):
        self._strref = val

    @staticmethod
    def unpack(source, offset):
        """Parses a gff cexolocstring."""

        # identify the current position, read and parse the cexolocstring, and return to the current position
        position = source.tell()
        source.seek(offset)
        length, stringref, count = struct.unpack('IiI', source.read(12))
        result = []
        if count > 0:
            for substring in range(0, count):
                id, length = struct.unpack('2I', source.read(8))
                pattern = "%ds" % length
                data = struct.unpack(pattern, source.read(struct.calcsize(pattern)))[0].decode(get_encoding())
                result.append([id, data])

        source.seek(position)

        return NWLocalizedString(stringref, result)

    def pack(self):
        """Writes the specified data as a cexolocstring and returns it."""

        if len(self.strings) == 0:
            return struct.pack('IiI', 8, self.strref, 0)

        content = struct.pack('iI', self.strref, len(self.strings))
        for substring in self.strings:
            length = len(substring[1])
            pattern = "2I%ds" % length
            content += struct.pack(pattern, substring[0], length, substring[1].encode('utf-8'))

        return struct.pack('I', len(content)) + content

class NWVoid(object):
    """ Does not abstract a type, it exists only for
    parsing"""

    type_id   = 13
    type      = 'void'
    at_offset = 'data'

    def __init__(self, val):
        self.val = val

    @staticmethod
    def unpack(source, offset):
        """Parses a gff void."""

        source.seek(offset)
        length = struct.unpack('I', source.read(4))[0]
        data = source.read(length)
        return NWVoid(data)

    def pack(self):
        """Writes the specified data as a void and returns it."""
        length = len(self.val)
        pattern = "I%dB" % length
        return struct.pack(pattern, length, self.val)

class NWStruct(object):
    """ Does not abstract a type, it exists only for
    parsing"""

    type_id   = 14
    type      = 'struct'
    at_offset = True

    def __init__(self):
        pass

    @staticmethod
    def unpack(source, offset):
        return offset

class NWList(object):
    """ Does not abstract a type, it exists only for
    parsing"""

    type_id   = 15
    type      = 'list'
    at_offset = 'list'

    def __init__(self):
        pass

    @staticmethod
    def unpack(source, offset):
        source.seek(offset)
        count = struct.unpack("I", source.read(4))[0]
        pattern = "%dI" % count
        data = struct.unpack(pattern, source.read(struct.calcsize(pattern)))
        return data
