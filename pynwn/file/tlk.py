import struct

from pynwn.util import get_encoding


class Tlk:
    """Loads a TLK file from a file handle.
    """

    HEADER_SIZE = 20
    DATA_ELEMENT_SIZE = 4 + 16 + 4 + 4 + 4 + 4 + 4

    def __init__(self, io=None):
        self.entries = {}
        if io:
            self.io = io
            buf = self.io.read(self.HEADER_SIZE)

            temp = struct.unpack("4s 4s I I I", buf)
            self.ftype, self.fvers, self.lang, self.str_count, self.str_offset = temp
        else:
            self.io = None
            self.ftype = 'TLK '
            self.fvers = 'V3.0'
            self.lang = 0
            self.str_count = 0
            self.str_offset = -1

    def __getitem__(self, i):
        """Get a TLK element.  Tlk supports integer indices and
        Python slices.  Please note that taking a huge slice say a
        reverse (tlk[::-1] can be a very costly.
        """

        if isinstance(i, slice):
            indices = i.indices(len(self))

            n = Tlk(None)
            n.ftype = self.ftype
            n.fvers = self.fvers
            n.lang = self.lang
            n.cache = {}

            for i in range(*indices):
                n.add(**self[i])

            return n

        if i == 0xffffffff or i >= len(self) or i < 0:
            return ""
        elif i in self.entries:
            return self.entries[i]
        elif self.io is not None:
            seek_to = self.HEADER_SIZE + i * self.DATA_ELEMENT_SIZE
            self.io.seek(seek_to)

            data = self.io.read(self.DATA_ELEMENT_SIZE)

            temp = struct.unpack("I 16s I I I I f", data)
            flags, sound_resref, v_variance, p_variance, offset, size, sound_length = temp
            sound_resref = sound_resref

            self.io.seek(self.str_offset + offset)
            text = self.io.read(size)
            try:
                text = text.decode(get_encoding()) if flags & 0x1 > 0 else ""
            except UnicodeDecodeError:
                print("Encoding Error: Unable to read entry %d" % i)
                text = ''

            return text
        return ""

    def __len__(self):
        """Determines the highest TLK entry.
        """
        keys = self.entries.keys()
        size = len(keys)
        if size == 0 and self.str_count == 0:
            return 0

        h = max(keys) + 1 if size > 0 else 0
        c = self.str_count

        return max(h, c)

    def __setitem__(self, i, val):
        self.entries[i] = val

    def add(self, text):
        """Adds TLK entry to the end of entry list.
        """
        next_i = len(self)

        self.entries[next_i] = text
        return next_i

    def inject(self, other):
        """Injects lines from one TLK into another.
        """
        for i in range(len(other) + 1):
            n = other[i]
            if len(n):
                self[i] = n

    def write_tls(self, io):
        io.write("#TLS V1.0 Uncompiled TLK source#\n")
        for i in range(len(self) + 1):
            n = self[i]
            if len(n):
                try:
                    io.write("<%d><%d>:%s\n" % (i, i + 0x01000000, n))
                except UnicodeError as e:
                    print("Unicode error:", i, n)

    def write(self, io):
        header = struct.pack("4s 4s I I I",
                             self.ftype.encode('ascii'),
                             self.fvers.encode('ascii'),
                             self.lang,
                             len(self),
                             self.HEADER_SIZE + len(self) * self.DATA_ELEMENT_SIZE)
        io.write(header)

        offset = 0
        strings = []
        for i in range(len(self)):
            n = self[i]
            entries = struct.pack("I 16s I I I I f",
                                  0x1 if len(n) else 0,
                                  b"",
                                  0,
                                  0,
                                  offset if len(n) else 0,
                                  len(n),
                                  0)
            io.write(entries)
            offset += len(n)
            strings.append(n)
        io.write(bytearray(''.join(strings), get_encoding()))


class TlkTable(object):
    def __init__(self, dialog, custom=None, dialogf=None, customf=None):
        self.dm = Tlk(dialog)
        self.df = Tlk(dialogf) if dialogf else self.dm
        self.cm = Tlk(custom) if custom else None
        self.cf = Tlk(customf) if customf else self.cm

    def get(self, strref, gender='male'):
        t = None
        if strref < 0x01000000:
            if gender == 'male':
                t = self.dm
            else:
                t = self.df
        else:
            strref -= 0x01000000
            if gender == 'male':
                t = self.cm
            else:
                t = self.cf

        if t is None:
            raise ValueError("No such TLK")

        return t[strref]
