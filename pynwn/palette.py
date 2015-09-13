from pynwn.file.gff import Gff

class PaletteNode(object):
    """Palette Node
    """
    def __init__(self, gff, parent_obj):
        self.gff = gff
        self.parent_obj = parent_obj
        self.is_instance = True

        self.gff = gff

        self._is_leaf = False
        self._id = None
        self._strref = None
        self._resref = None
        self._cr = None
        self._faction = None
        self._name = None
        self._nodes = None

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

    @property
    def is_leaf(self):
        return self._is_leaf

    @property
    def id(self):
        return self._id

    @property
    def strref(self):

        return self._strref

    @property
    def resref(self):
        return self._resref

    @property
    def cr(self):
        return self._cr

    @property
    def faction(self):
        return self._faction

    @property
    def name(self):
        return self._name

    @property
    def nodes(self):
        return self._nodes

    def stage(self):
        self.parent_obj.stage()

class Palette(object):
    """ This is a very rough absraction over ITPs.
    """
    def __init__(self, resource):
        self.is_file = False
        self.container = None

        if isinstance(resource, str):
            from resource import ContentObject
            co = ContentObject.from_file(resource)
            self.gff = Gff(co)
            self.is_file = True
        else:
            self.container = resource[1]
            self.gff = Gff(resource[0])

    @property
    def nodes(self):
        """ Gets all nodes in the palette.

        :returns: a list of :class:`PaletteNode` objects.
        """
        return [PaletteNode(p) for p in self.gff['MAIN']]

    def stage():
        if self.gff.is_loaded() and self.container:
            self.container.add_to_saves(self.gff)
