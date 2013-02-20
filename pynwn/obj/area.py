from pynwn.gff import Gff, make_gff_property

from pynwn.obj.encounter import EncounterInstance
from pynwn.obj.placeable import PlaceableInstance
from pynwn.obj.sound import SoundInstance
from pynwn.obj.trigger import TriggerInstance
from pynwn.obj.waypoint import WaypointInstance

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

ARE_TRANSLATION_TABLE = {
    'fog_clip_distance' : ('FogClipDist', "Fog clip distance."),
    'height'            : ('Height', "Area height."),
    'resref'            : ('ResRef', "Resref."),
    'tag'               : ('Tag', "Tag."),
    'tileset'           : ('Tileset', "Tileset."),
    'width'             : ('Width', "Area width.")
}

class Area(NWObjectVarable):
    def __init__(self, resref, container):
        are = resref+'.are'
        if container.has_file(are):
            self.are = container[are]
            self.are = Gff(self.are)
        else:
            raise ValueError("Container does not contain %s" % are)

        git = resref+'.git'
        if container.has_file(git):
            self.git = container[git]
            self.git = Gff(self.git)
            NWObjectVarable.__init__(self, self.git)
        else:
            raise ValueError("Container does not contain %s.git" % resref)

        gic = resref+'.gic'
        if container.has_file(gic):
            self.gic = container[gic]
            self.gic = Gff(self.gic)
        else:
            raise ValueError("Container does not contain %s.gic" % resref)

        self._scripts = None
        self._locstr = {}

    def save(self):
        if self.are.is_loaded():
            self.are.save()

        if self.git.is_loaded():
            self.git.save()

        if self.gic.is_loaded():
            self.gic.save()

    @property
    def encounters(self):
        """Encounters

        :returns: List of EncounterInstance objects.
        """
        return [EncounterInstance(p) for p in self.git['Encounter List']]

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['Name'])

        return self._locstr['name']

    @property
    def placeables(self):
        """Placeables

        :returns: List of PlaceableInstance objects.
        """
        return [PlaceableInstance(p, self.git) for p in self.git['Placeable List']]

    @property
    def script(self):
        """Scripts.  Responds to script events:

        #. Event.ENTER
        #. Event.EXIT
        #. Event.HEARTBEAT
        #. Event.USER_DEFINED
        """
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.ENTER] = 'OnEnter'
        lbls[Event.EXIT] = 'OnExit'
        lbls[Event.HEARTBEAT] = 'OnHeartbeat'
        lbls[Event.USER_DEFINED] = 'OnUserDefined'

        self._scripts = NWObjectScripts(self.are, lbls)

        return self._scripts

    @property
    def sounds(self):
        """Sounds

        :returns: List of SoundInstance objects.
        """
        return [SoundInstance(p) for p in self.git['SoundList']]

    @property
    def triggers(self):
        """Triggers

        :returns: List of TriggerInstance objects.
        """
        return [TriggerInstance(p) for p in self.git['TriggerList']]

    @property
    def waypoints(self):
        """Waypoints

        :returns: List of WaypointInstance objects.
        """
        return [WaypointInstance(p) for p in self.git['WaypointList']]

def make_are_property(gff_name):
    def getter(self):
        return self.are[gff_name[0]].val

    def setter(self, val):
        self.are[gff_name[0]].val = val

    return property(getter, setter, None, gff_name[1])

for key, val in ARE_TRANSLATION_TABLE.iteritems():
    setattr(Area, key, make_gff_property('are', val))
