from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property

from pynwn.vars import *

TRANSLATION_TABLE = {
    'tag'              : ('Tag', "Tag."),
    'resref'           : ('TemplateResRef', "Resref."),
    'appearance'       : ('Appearance', 'Appearance ID'),
    'comment'          : ('Comment', "Comment."),
    'has_map_note'     : ('HasMapNote', "Has map note flag."),
    'linked_to'        : ('LinkedTo', "Linked to."),
    'map_note_enabled' : ('MapNoteEnabled', "Map note enabled."),
    'palette_id'       : ('PaletteID', "Palette ID."),
}

LOCSTRING_TABLE = {
    'name'        : ('LocalizedName', "Localized name."),
    'map_note'    : ('MapNote', "Localized map note."),
    'description' : ('Description', "Localized description."),
}

class Waypoint(object):
    def __init__(self, resource, instance=False):
        self._vars = None
        self.is_file = False

        self.is_instance = instance
        if not instance:
            if isinstance(resource, str):
                from resource import ContentObject
                co = ContentObject.from_file(resource)
                self.gff = Gff(co)
                self.is_file = True
            else:
                self.container = resource[1]
                self.gff = Gff(resource[0])
        else:
            self.gff = resource

    def stage(self):
        """Stage changes to GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def vars(self):
        """ Variable table """
        if self._vars: return self._vars
        self._vars = NWObjectVarable(self, self.gff)
        return self._vars


class WaypointInstance(Waypoint):
    def __init__(self, gff, parent_obj):
        Waypoint.__init__(self, gff, True)
        self.parent_obj = parent_obj

    @property
    def position(self):
        return (self.gff['XPosition'], self.gff['YPosition'],
                self.gff['ZPosition'])

    def stage(self):
        """Stages changes to parent GFF structure.
        """
        self.parent_obj.stage()

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Waypoint, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Waypoint, 'get_'+key, getter)
    setattr(Waypoint, 'set_'+key, setter)
