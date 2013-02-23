from pynwn.file.gff import Gff, GffInstance, make_gff_locstring_property
from pynwn.file.gff import make_gff_property
from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['RepositoryItem', 'ItemProperty', 'Item', 'ItemInstance']


REPO_TRANSLATION_TABLE = {
    'resref'   : ('InventoryRes', 'Resref.'),
    'dropable' : ('Dropable', 'Dropable flag.'),
    'infinite' : ('Infinite', 'Infinite flag.'),
}

class RepositoryItem(object):
    def __init__(self, gff):
        self.gff = gff

    @property
    def position(self):
        """Position in inventory

        :returns: Tuple of x and y coordinates.
        """
        return (self.gff['Repos_PosX'], self.gff['Repos_Posy'])

for key, val in REPO_TRANSLATION_TABLE.iteritems():
    setattr(RepositoryItem, key, make_gff_property('gff', val))

IP_TRANSLATION_TABLE = {
    'type'        : ('PropertyName', 'Type.'),
    'subtype'     : ('Subtype', 'Subtype.'),
    'cost_table'  : ('CostTable', 'Cost table.'),
    'cost_value'  : ('CostValue', 'Cost value.'),
    'param_table' : ('Param1', 'Parameter table.'),
    'param_value' : ('Param1Value', 'Parameter value.'),
    'chance'      : ('ChanceAppear', 'Appearance chance.'),
}

class ItemProperty(object):
    def __init__(self, gff):
        self.gff = gff

for key, val in IP_TRANSLATION_TABLE.iteritems():
    setattr(ItemProperty, key, make_gff_property('gff', val))

TRANSLATION_TABLE = {
    'resref'           : ('TemplateResRef', "Resref."),
    'base_type'        : ('BaseItem', "Base item ID."),
    'tag'              : ('Tag', "Tag."),
    'charges'          : ('Charges', "Charges."),
    'cost'             : ('cost', "Cost."),
    'stolen'           : ('stolen', "Stolen flag."),
    'stack_size'       : ('StackSize', "Stack size."),
    'plot'             : ('Plot', "Plot flag."),
    'cost_additional'  : ('AddCost', "Additional Cost."),
    'identified'       : ('Identified', "Identified flag."),
    'cursed'           : ('Cursed', "Cursed flag."),
    'palette_id'       : ('PaletteID', "Palette ID."),
    'comment'           : ('Comment', "Comment."),
}

LOCSTRING_TABLE = {
    'name'           : ('LocalizedName', "Localized name."),
    'description'    : ('Description', "Localized unidentified description."),
    'description_id' : ('DescIdentified', "Localized identified description."),
}

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
                self.container = container
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref

        NWObjectVarable.__init__(self, self.gff)

    def save(self):
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def model(self):
        # It will probably be best to encapsulate this...
        pass

    @property
    def properties(self):
        """Item properties

        :returns: List of ItemProperty objects.
        """
        result = []
        i = 0
        for p in self.gff['PropertiesList']:
            gff_inst = GffInstance(self.gff, 'PropertiesList', i)
            st_inst  = ItemProperty(gff_inst)
            result.append(st_inst)
            i += 1

        return result

class ItemInstance(Item):
    """A item instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Item.__init__(self, gff, None, True)
        self.is_instance = True

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Item, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Item, 'get_'+key, getter)
    setattr(Item, 'set_'+key, setter)
