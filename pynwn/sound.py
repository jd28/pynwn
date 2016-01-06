from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property

TRANSLATION_TABLE = {
    'tag': ('Tag', "Tag."),
    'resref': ('TemplateResRef', "Resref."),
    'active': ('Active', "Active flag."),
    'continous': ('Continous', "Continuous flag."),
    'looping': ('Looping', "Looping flag."),
    'positional': ('Positional', "Positional."),
    'random_position': ('RandomPosition', "Random position."),
    'random': ('Random', "Random."),
    'elevation': ('Elevation', "Elevation."),
    'distance_max': ('MaxDistance', "Maximum distance."),
    'distance_min': ('MinDistance', "Minimum distance."),
    'interval': ('Interval', "Interval."),
    'interval_variation': ('IntervalVrtn', "Interval variation."),
    'pitch_variation': ('PitchVariation', "Pitch variation."),
    'priority': ('Priority', "Priority."),
    'hours': ('Hours', "Hours."),
    'times': ('Times', "Times."),
    'volume': ('Volume', "Volume."),
    'volume_variation': ('VolumeVrtn', "Volume variation."),
    'palette_id': ('PaletteID', "Palette ID."),
    'comment': ('Comment', "Comment."),
}

LOCSTRING_TABLE = {
    'name': ('LocName', "Localized name."),
}


class Sound(object):
    def __init__(self, resource, instance=False):
        self.is_file = False

        self.is_instance = instance
        if not instance:
            if isinstance(resource, str):
                from pynwn import ContentObject
                co = ContentObject.from_file(resource)
                self.gff = Gff(co)
                self.is_file = True
            else:
                self.container = resource[1]
                self.gff = Gff(resource[0])
        else:
            self.gff = resource

    def stage(self):
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def random_range(self):
        return self.gff['RandomRangeX'], self.gff['RandomRangeY']

    @property
    def sounds(self):
        return [s['Sound'] for s in self.gff['Sounds']]


class SoundInstance(Sound):
    """A sound instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """

    def __init__(self, gff, parent_obj):
        Sound.__init__(self, gff, False)
        self.is_instance = True
        self.parent_obj = parent_obj

    def stage(self):
        """Stages changes to parent GFF structure.
        """
        self.parent_obj.stage()


for key, val in TRANSLATION_TABLE.items():
    setattr(Sound, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Sound, 'get_' + key, getter)
    setattr(Sound, 'set_' + key, setter)
