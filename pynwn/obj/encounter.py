from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

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

    @property
    def tag(self):
        return self['Tag']

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def resref(self):
        return self['TemplateResRef']

    @property
    def active(self):
        return self['Active']

    @property
    def difficulty(self):
        return self['Difficulty']

    @property
    def difficulty_index(self):
        return self['DifficultyIndex']

    @property
    def faction(self):
        return self['Faction']

    @property
    def max_creatures(self):
        return self['MaxCreatures']

    @property
    def player_only(self):
        return self['PlayerOnly']

    @property
    def rec_creatures(self):
        return self['RecCreatures']

    @property
    def reset(self):
        return self['Reset']

    @property
    def reset_time(self):
        return self['ResetTime']

    @property
    def respawns(self):
        return self['Respawns']

    @property
    def spawn_option(self):
        return self['SpawnOption']

    @property
    def scripts(self):
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
        return [EncounterCreature(c) for c in self['CreatureList']]

    @property
    def palette_id(self):
        return self['PaletteID']

    @property
    def comment(self):
        return self['Comment']


class EncounterInstance(Encounter):
    """A encounter instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Encounter.__init__(self, gff, None, True)
        self.is_instance = True
