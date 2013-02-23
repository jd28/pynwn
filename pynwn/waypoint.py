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

class Waypoint(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self.is_instance = instance
        self._locstr = {}

        if not instance:
            if resref[-4:] != '.utw':
                resref = resref+'.utw'

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

class WaypointInstance(Waypoint):
    def __init__(self, gff):
        Waypoint.__init__(self, gff, None, True)

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Waypoint, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Waypoint, 'get_'+key, getter)
    setattr(Waypoint, 'set_'+key, setter)
