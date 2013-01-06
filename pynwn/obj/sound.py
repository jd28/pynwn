from pynwn.gff import Gff
from pynwn.obj.locstring import *

class Sound(object):
    def __init__(self, resref, container, instance=False):
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.uts':
                resref = resref+'.uts'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._uts = resref.val

    def __getattr__(self, name):
        if name == 'uts':
            if not self._uts: self._uts = self.gff.structure
            return self._uts
            
    def __getitem__(self, name):
        return self.uts[name].val
            
    @property
    def tag(self):
        return self['Tag']

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self['LocName'])

        return self._locstr['name']

    @property
    def resref(self):
        return self['TemplateResRef']

    @property
    def active(self):
        return self['Active']

    @property
    def continous(self):
        return self['Continous']

    @property
    def looping(self):
        return self['Looping']

    @property
    def positional(self):
        return self['Positional']

    @property
    def random_position(self):
        return self['RandomPosition']

    @property
    def random(self):
        return self['Random']

    @property
    def elevation(self):
        return self['Elevation']

    @property
    def distance_max(self):
        return self['MaxDistance']

    @property
    def distance_min(self):
        return self['MinDistance']

    @property
    def random_range(self):
        return (self['RandomRangeX'], self['RandomRangeY'])

    @property
    def interval(self):
        return self['Interval']

    @property
    def interval_variation(self):
        return self['IntervalVrtn']

    @property
    def pitch_variation(self):
        return self['PitchVariation']

    @property
    def priority(self):
        return self['Priority']

    @property
    def hours(self):
        return self['Hours']

    @property
    def times(self):
        return self['Times']

    @property
    def volume(self):
        return self['Volume']

    @property
    def volume_variation(self):
        return self['VolumeVrtn']

    @property
    def sounds(self):
        return [s['Sound'] for s in self['Sounds']]

    @property
    def palette_id(self):
        return self['PaletteID']

    @property
    def comment(self):
        return self['Comment']

class SoundInstance(Sound):
    """A sound instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Sound.__init__(self, gff, None, True)
        self.is_instance = True
