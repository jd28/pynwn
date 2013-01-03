from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

class RepositoryItem(object):
    def __init__(self, gff):
        self.gff = gff

    @property
    def resref(self):
        return self.gff['InventoryRes']

    @property
    def position(self):
        return (self.gff['Repos_PosX'], self.gff['Repos_Posy'])

    @property
    def dropable(self):
        """Field only occurs in creature item lists"""
        return self.gff['Dropable']

    @property
    def infinite(self):
        """Field only occurs in store item lists"""
        return self.gff['Infinite']


class ItemProperty(object):
    def __init__(self, gff):
        self.gff = gff

    @property
    def type(self):
        return self.gff['PropertyName']

    def subtype(self):
        return self.gff['Subtype']

    def cost_table(self):
        return self.gff['CostTable']

    def cost_value(self):
        return self.gff['CostValue']

    def param_table(self):
        return self.gff['Param1']

    def param_value(self):
        return self.gff['Param1Value']

    def chance(self):
        return self.gff['ChanceAppear']

class Item(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.uti':
                resref = resref+'.uti'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._uti = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'uti':
            if not self._uti: self._uti = self.gff.structure
            return self._uti

    def __getitem__(self, name):
        return self.uti[name].val

    @property
    def resref(self):
        return self['TemplateResRef']

    @property
    def base_type(self):
        return self['BaseItem']

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def description(self):
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self.are['Description'])

        return self._locstr['description']

    @property
    def description_id(self):
        if not self._locstr.has_key('description_id'):
            self._locstr['description_id'] = LocString(self.are['DescIdentified'])

        return self._locstr['description_id']

    @property
    def tag(self):
        return self['Tag']

    @property
    def charges(self):
        return self['Charges']

    @property
    def cost(self):
        return self['cost']

    @property
    def stolen(self):
        return self['stolen']

    @property
    def stack_size(self):
        return self['StackSize']

    @property
    def plot(self):
        return self['Plot']

    @property
    def cost_additional(self):
        return self['AddCost']

    @property
    def identified(self):
        return self['Identified']

    @property
    def cursed(self):
        return self['Cursed']

    @property
    def model(self):
        # It will probably be best to encapsulate this...
        pass

    @property
    def properties(self):
        return [ItemProperty(ip) for ip in self['PropertiesList']]

    @property
    def palette_id(self):
        return self['PaletteID']

    @property
    def comment(self):
        return self['Comment']

class ItemInstance(Item):
    """A item instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Item.__init__(self, gff, None, True)
        self.is_instance = True
