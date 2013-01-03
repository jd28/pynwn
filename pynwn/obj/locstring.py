from pynwn.consts import *

class LocString:
    def __init__(self, gff_struct):
        self.gff = gff_struct[1:]

    def __getitem__(self, lang):
        if not LANGUAGES.has_key(lang):
            raise ValueError("Unknown language type: %d" % lang)

        if len(self.gff) == 0: return ''
        
        for s in self.gff:
            if s[0] == lang: return s[1]

        return ''
