from pynwn.file.gff import Gff

class PaletteNode(object):
    def __init__(self, gff):
        self.gff = gff

        self.is_leaf = False
        self.id = None
        self.strref = None
        self.resref = None
        self.cr = None
        self.faction = None
        self.name = None
        self.nodes = None

        try:
            self.id = self.gff['ID']
        except Exception: pass

        try:
            self.strref = self.gff['STRREF']
        except Exception: pass

        try:
            self.nodes = [PaletteNode(n) for n in self.gff['LIST']]
        except Exception: pass

        try:
            self.resref = self.gff['RESREF']
        except Exception: pass

        try:
            self.name = self.gff['NAME']
        except Exception: pass

        try:
            self.cr = self.gff['CR']
        except Exception: pass

        try:
            self.faction = self.gff['FACTION']
        except Exception: pass


class Palette(object):
    """ This is a very rough absraction over ITPs.
    """
    def __init__(self, resref, container):
        if resref[-4:] != '.itp':
            resref = resref+'.itp'

        if container.has_file(resref):
            self.gff = container[resref]
            self.gff = Gff(self.gff)
        else:
            raise ValueError("Container does not contain: %s" % resref)

    def __getattr__(self, name):
        if name == 'itp':
            if not self._itp: self._itp = self.gff.structure
            return self._itp

    def __getitem__(self, name):
        return self.itp[name].val

    @property
    def nodes(self):
        return [PaletteNode(p) for p in self['MAIN']]
