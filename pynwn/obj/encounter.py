from pynwn.gff import Gff, make_gff_property

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

TRANSLATION_TABLE = {
    'tag'              : ('Tag', "Tag."),
    'resref'           : ('TemplateResRef', "Resref."),
    'active'           : ('Active', "Active flag."),
    'difficulty'       : ('Difficulty', "Difficulty."),
    'difficulty_index' : ('DifficultyIndex', "Difficulty Index."),
    'faction'          : ('Faction', "Faction ID."),
    'max_creatures'    : ('MaxCreatures', "Maximum creatures."),
    'player_only'      : ('PlayerOnly', "Triggered by player only."),
    'rec_creatures'    : ('RecCreatures', "rec_creatures."),
    'reset'            : ('Reset', "Resets flag."),
    'reset_time'       : ('ResetTime', "Reset time."),
    'respawns'         : ('Respawns', "Respawns."),
    'spawn_option'     : ('SpawnOption', "Spawn option."),
    'palette_id'       : ('PaletteID', "Palette ID."),
    'comment'          : ('Comment', "Comment."),
}

class EncounterCreature(object):
    def __init__(self, gff):
        self.gff = gff

    @property
    def appearance(self):
        return self.gff['Appearance']

    @property
    def cr(self):
        return self.gff['CR']

    @property
    def resref(self):
        return self.gff['ResRef']

    @property
    def unique(self):
        return self.gff['SingleSpawn']


class Encounter(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.ute':
                resref = resref+'.ute'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._ute = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'ute':
            if not self._ute: self._ute = self.gff.structure
            return self._ute

    def __getitem__(self, name):
        return self.ute[name].val

    def __setitem__(self, name):
        return self.ute[name].val

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def scripts(self):
        """Scripts. Responts to script events:

        * Event.ENTER
        * Event.EXIT
        * Event.EXHAUSTED
        * Event.HEARTBEAT
        * Event.USER_DEFINED

        """
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.ENTER] = 'OnEntered'
        lbls[Event.EXIT] = 'OnExit'
        lbls[Event.EXHAUSTED] = 'OnExhausted'
        lbls[Event.HEARTBEAT] = 'OnHeartbeat'
        lbls[Event.USER_DEFINED] = 'OnUserDefined'

        self._scripts = NWObjectScripts(self.utt, lbls)

        return self._scripts

    @property
    def creatures(self):
        """Creatures in the encounter.

        :returns: List of EncounterCreature objects.
        """
        return [EncounterCreature(c) for c in self['CreatureList']]

class EncounterInstance(Encounter):
    """A encounter instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Encounter.__init__(self, gff, None, True)
        self.is_instance = True

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Encounter, key, make_gff_property('ute', val))
