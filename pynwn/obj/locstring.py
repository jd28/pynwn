from pynwn.consts import *

class LocString:
    def __init__(self, gff_struct):
        self.gff = gff_struct[1:]
        print gff_struct
        print self.gff

    def __getitem__(self, lang):
        if not LANGUAGES.has_key(lang):
            raise ValueError("Unknown language type: %d" % lang)

        for s in self.gff:
            if s[0] == lang: return s[1]

        return ''
