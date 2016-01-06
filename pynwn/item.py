from pynwn.file.gff import Gff, GffInstance, make_gff_locstring_property
from pynwn.file.gff import make_gff_property
from pynwn.vars import *

__all__ = ['RepositoryItem', 'ItemProperty', 'Item', 'ItemInstance']

REPO_TRANSLATION_TABLE = {
    'resref': ('InventoryRes', 'Resref.'),
    'dropable': ('Dropable', 'Dropable flag.'),
    'infinite': ('Infinite', 'Infinite flag.'),
}


class RepositoryItem(object):
    def __init__(self, gff, parent_obj):
        self.gff = gff
        self.parent_obj = parent_obj

    def stage(self):
        self.parent_obj.stage()

    @property
    def position(self):
        """Position in inventory

        :returns: Tuple of x and y coordinates.
        """
        return self.gff['Repos_PosX'], self.gff['Repos_Posy']


for key, val in REPO_TRANSLATION_TABLE.items():
    setattr(RepositoryItem, key, make_gff_property('gff', val))

IP_TRANSLATION_TABLE = {
    'type': ('PropertyName', 'Type.'),
    'subtype': ('Subtype', 'Subtype.'),
    'cost_table': ('CostTable', 'Cost table.'),
    'cost_value': ('CostValue', 'Cost value.'),
    'param_table': ('Param1', 'Parameter table.'),
    'param_value': ('Param1Value', 'Parameter value.'),
    'chance': ('ChanceAppear', 'Appearance chance.'),
}


class ItemProperty(object):
    def __init__(self, gff, parent_obj):
        self.gff = gff
        self.parent_obj = parent_obj


for key, val in IP_TRANSLATION_TABLE.items():
    setattr(ItemProperty, key, make_gff_property('gff', val))

TRANSLATION_TABLE = {
    'resref': ('TemplateResRef', "Resref."),
    'base_type': ('BaseItem', "Base item ID."),
    'tag': ('Tag', "Tag."),
    'charges': ('Charges', "Charges."),
    'cost': ('cost', "Cost."),
    'stolen': ('stolen', "Stolen flag."),
    'stack_size': ('StackSize', "Stack size."),
    'plot': ('Plot', "Plot flag."),
    'cost_additional': ('AddCost', "Additional Cost."),
    'identified': ('Identified', "Identified flag."),
    'cursed': ('Cursed', "Cursed flag."),
    'palette_id': ('PaletteID', "Palette ID."),
    'comment': ('Comment', "Comment."),
    'display_name': ('DisplayName', 'Display Name.'),
}

LOCSTRING_TABLE = {
    'name': ('LocalizedName', "Localized name."),
    'description': ('Description', "Localized unidentified description."),
    'description_id': ('DescIdentified', "Localized identified description."),
}


class Item(object):
    def __init__(self, resource, instance=False):
        self._scripts = None
        self._vars = None
        self.container = None

        self.is_instance = instance
        if not instance:
            if isinstance(resource, str):
                from pynwn import ContentObject
                co = ContentObject.from_file(resource)
                self.gff = Gff(co)
            else:
                self.container = resource[1]
                self.gff = Gff(resource[0])
        else:
            self.gff = resource

    def stage(self):
        if self.gff.is_loaded() and self.container:
            self.container.add_to_saves(self.gff)

    @property
    def vars(self):
        """ Variable table """
        if self._vars:
            return self._vars
        self._vars = NWObjectVarable(self, self.gff)
        return self._vars

    @property
    def model(self):
        # It will probably be best to encapsulate this...
        pass

    @property
    def properties(self):
        """Item properties

        :returns: List of :class:`ItemProperty` objects.
        """
        result = []
        i = 0
        for p in self.gff['PropertiesList']:
            gff_inst = GffInstance(self.gff, 'PropertiesList', i)
            st_inst = ItemProperty(gff_inst, self)
            result.append(st_inst)
            i += 1

        return result


class ItemInstance(Item):
    """A item instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    It never needs to be instantiated directly.
    """

    def __init__(self, gff, parent_obj):
        Item.__init__(self, gff, True)
        self.is_instance = True
        self.parent_obj = parent_obj

    def stage(self):
        self.parent_obj.stage()


for key, val in TRANSLATION_TABLE.items():
    setattr(Item, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Item, 'get_' + key, getter)
    setattr(Item, 'set_' + key, setter)
