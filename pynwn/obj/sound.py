from pynwn.gff import Gff, make_gff_property
from pynwn.obj.locstring import *

TRANSLATION_TABLE = {
    'tag'                : ('Tag', "Tag."),
    'resref'             : ('TemplateResRef', "Resref."),
    'active'             : ('Active', "Active flag."),
    'continous'          : ('Continous', "Continuous flag."),
    'looping'            : ('Looping', "Looping flag."),
    'positional'         : ('Positional', "Positional."),
    'random_position'    : ('RandomPosition', "Random position."),
    'random'             : ('Random', "Random."),
    'elevation'          : ('Elevation', "Elevation."),
    'distance_max'       : ('MaxDistance', "Maximum distance."),
    'distance_min'       : ('MinDistance', "Minimum distance."),
    'interval'           : ('Interval', "Interval."),
    'interval_variation' : ('IntervalVrtn', "Interval variation."),
    'pitch_variation'    : ('PitchVariation', "Pitch variation."),
    'priority'           : ('Priority', "Priority."),
    'hours'              : ('Hours', "Hours."),
    'times'              : ('Times', "Times."),
    'volume'             : ('Volume', "Volume."),
    'volume_variation'   : ('VolumeVrtn', "Volume variation."),
    'palette_id'         : ('PaletteID', "Palette ID."),
    'comment'            : ('Comment', "Comment."),
}

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
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self['LocName'])

        return self._locstr['name']

    @property
    def random_range(self):
        return (self['RandomRangeX'], self['RandomRangeY'])

    @property
    def sounds(self):
        return [s['Sound'] for s in self['Sounds']]

class SoundInstance(Sound):
    """A sound instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Sound.__init__(self, gff, None, True)
        self.is_instance = True

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Sound, key, make_gff_property('uts', val))
