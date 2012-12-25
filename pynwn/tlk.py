import struct

LANGUAGES = {
    0: "english",
    1: "french",
    2: "german",
    3: "italian",
    4: "spanish",
    5: "polish",
    128: "korean",
    129: "chinese_traditional",
    130: "chinese_simplified",
    131: "japanese",
}

GENDER = ['male', 'female']

class Tlk:
    """Loads a TLK file from a file handle.
    """

    HEADER_SIZE = 20
    DATA_ELEMENT_SIZE = 4 + 16 + 4 + 4 + 4 + 4 + 4

    def __init__(self, io = None):
        self.cache = {}
        if io:
            self.io = io
            buf = self.io.read(self.HEADER_SIZE)

            temp = struct.unpack("4s 4s I I I", buf)
            self.ftype, self.fvers, self.lang, self.str_count, self.str_offset = temp
        else:
            self.io = None
            self.ftype = 'TLK'
            self.fvers = 'V3.0'
            self.lang = 0
            self.str_count = 0
            self.str_offset = -1


    def __getitem__(self, i):
        if i == 0xffffffff:
            return {
                'text': '',
                'sound': "",
                'sound_length': 0.0,
                'volume_variance': 0,
                'pitch_variance': 0
            }
        elif self.cache.has_key(i):
            return self.cache[i]
        elif i > self.highest() or i < 0:
            print "Invalid TLK entry: %d" % i
        else:
            seek_to = self.HEADER_SIZE + (i) * self.DATA_ELEMENT_SIZE
            self.io.seek(seek_to)

            data = self.io.read(self.DATA_ELEMENT_SIZE)

            temp = struct.unpack("I 16s I I I I f", data)
            flags, sound_resref, v_variance, p_variance, offset, size, sound_length = temp
            sound_resref = sound_resref.encode()

            self.io.seek(self.str_offset + offset)
            text = self.io.read(size)

            text = text if flags & 0x1 > 0 else ""
            sound = sound_resref if flags & 0x2 > 0 else ""
            sound_length = float(sound_length) if flags & 0x4 > 0 else 0.0

            self.cache[i] = {
                'text': text,
                'sound': sound,
                'sound_length': sound_length,
                'volume_variance': v_variance,
                'pitch_variance': p_variance
            }

            return self[i]

    def __setitem__(self, i, val):
        d = self[i]

        d['text'] = val['text']
        d['sound'] = val['sound']
        d['sound_length'] = val['sound_length']
        d['volume_variance'] = val['volume_variance']
        d['pitch_variance'] = val['pitch_variance']

    def add (self, text, sound = "", sound_length = 0.0, volume_variance = 0, pitch_variance = 0):
        """Adds TLK entry to the end of entry list.
        """
        next_i = self.highest()

        #$stderr.puts "put in cache: #{next_id}"
        self.cache[next_i] = {
            'text': text,
            'sound': sound,
            'sound_length': 0.0,
            'volume_variance': volume_variance,
            'pitch_variance': pitch_variance
        }
        return next_i

    def highest(self):
        """Determines the highest TLK entry.
        """
        keys = self.cache.keys()
        if len(keys)  == 0 and self.str_count == 0:
            return 0

        h = max(keys) + 1 if len(keys) > 0 else 0
        c = self.str_count

        return max(h, c)

    def extract(self, start=0, count=None):
        """Extracts lines from a TLK, returning a new Tlk instance.
        """
        if not count: count = self.highest()
        n = Tlk(None)

        n.ftype = self.ftype
        n.fvers = self.fvers
        n.lang = self.lang
        n.cache = {}

        for i in range(start, start+count):
            n.add(**self[i])

        return n

    def inject(self, loc, tlk, start=0, count=None):
        """Injects lines from one TLK into another.
        """        
        if not end: end = tlk.highest()

        for i in range(start, count):
            self[loc + i] = tlk[i]
