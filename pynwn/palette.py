from pynwn.file.gff import Gff


class PaletteNode(object):
    """Palette Node
    """

    def __init__(self, gff, parent_obj):
        """
        """
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
            self._id = self.gff['ID']
        except KeyError:
            pass

        try:
            self._strref = self.gff['STRREF']
        except KeyError:
            pass

        try:
            self._nodes = [PaletteNode(n, self) for n in self.gff['LIST']]
        except KeyError:
            pass

        try:
            self._resref = self.gff['RESREF']
        except KeyError:
            pass

        try:
            self._name = self.gff['NAME']
        except KeyError:
            pass

        try:
            self._cr = self.gff['CR']
        except KeyError:
            pass

        try:
            self._faction = self.gff['FACTION']
        except KeyError:
            pass

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
            from pynwn import ContentObject
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
        return [PaletteNode(p, self) for p in self.gff['MAIN']]

    def stage(self):
        if self.gff.is_loaded() and self.container:
            self.container.add_to_saves(self.gff)
