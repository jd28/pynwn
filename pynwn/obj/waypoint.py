from pynwn.gff import Gff, make_gff_property
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

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

class Waypoint(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self.is_instance = instance
        self._locstr = {}

        if not instance:
            if resref[-4:] != '.utw':
                resref = resref+'.utw'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
                self._utw = None
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self.utw = resref.val

        NWObjectVarable.__init__(self, self.utw)

    def __getattr__(self, name):
        if name == 'utw':
            if not self._utw: self._utw = self.gff.structure
            return self._utw

    def __getitem__(self, name):
        return self.utw[name].val

    def __getitem__(self, name, val):
        self.utw[name].val = val

    @property
    def description(self):
        """Localized description."""
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self['Description'])

        return self._locstr['description']

    @property
    def map_note(self):
        """Localized map note."""
        if not self._locstr.has_key('map_note'):
            self._locstr['map_note'] = LocString(self['MapNote'])

        return self._locstr['map_note']

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self['LocalizedName'])

        return self._locstr['name']

class WaypointInstance(Waypoint):
    def __init__(self, gff):
        Waypoint.__init__(self, gff, None, True)

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Waypoint, key, make_gff_property('utw', val))
