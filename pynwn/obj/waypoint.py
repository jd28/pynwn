from pynwn.gff import Gff
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

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
        if not self._utw:
            self._utw = self.gff.structure

        return self.utw[name].val

    @property
    def appearance(self):
        """Appearance ID."""
        return self['Appearance']

    @property
    def comment(self):
        """Comment."""
        return self['Comment']

    @property
    def description(self):
        """Localized description."""
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self['Description'])

        return self._locstr['description']

    @property
    def has_map_note(self):
        """Has map note flag."""
        return self['HasMapNote']

    @property
    def linked_to(self):
        """Trap disarmable flag."""
        return self['LinkedTo']

    @property
    def map_note(self):
        """Localized map note."""
        if not self._locstr.has_key('map_note'):
            self._locstr['map_note'] = LocString(self['MapNote'])

        return self._locstr['map_note']

    @property
    def map_note_enabled(self):
        """Map note enabled flag."""
        return self['MapNoteEnabled']

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self['LocalizedName'])

        return self._locstr['name']

    @property
    def palette_id(self):
        """Palette ID."""
        return self['PaletteID']

    @property
    def resref(self):
        """Resref."""
        return self['TemplateResRef']

    @property
    def tag(self):
        """Tag."""
        return self['Tag']

class WaypointInstance(Waypoint):
    def __init__(self, gff):
        Waypoint.__init__(self, gff, None, True)
