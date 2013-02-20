from pynwn.consts import *

class LocString:
    def __init__(self, gff_struct):
        print gff_struct
        self.gff = gff_struct

    def __getitem__(self, lang):
        if not LANGUAGES.has_key(lang):
            raise ValueError("Unknown language type: %d" % lang)

        if len(self.gff) == 0: return ''
        if len(self.gff) == 1: return self.gff[0]

        temp = self.gff[1:]
        for s in temp:
            if s[0] == lang:
                return s[1]

        return ''

    def __setitem__(self, lang, value):
        if not LANGUAGES.has_key(lang):
            raise ValueError("Unknown language type: %d" % lang)

        if len(self.gff) == 0: return ''
        if len(self.gff) == 1: return self.gff[0]

        temp = self.gff[1:]
        for s in temp:
            if s[0] == lang:
                s[1] = value
