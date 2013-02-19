from pynwn.gff import Gff

from pynwn.obj.encounter import EncounterInstance
from pynwn.obj.placeable import PlaceableInstance
from pynwn.obj.sound import SoundInstance
from pynwn.obj.trigger import TriggerInstance
from pynwn.obj.waypoint import WaypointInstance

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

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

    @property
    def encounters(self):
        """Encounters

        :returns: List of EncounterInstance objects.
        """
        return [EncounterInstance(p) for p in self.git['Encounter List']]

    @property
    def fog_clip_distance(self):
        """Fog clip distance."""
        return self.are['FogClipDist']

    @property
    def height(self):
        """Area height."""
        return self.are['Height']

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
        return [PlaceableInstance(p) for p in self.git['Placeable List']]

    @property
    def resref(self):
        """Resref."""
        return self.are['ResRef']

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
    def tag(self):
        """Tag"""
        return self.are['Tag']

    @property
    def tileset(self):
        """Tileset"""
        return self.are['Tileset']

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

    @property
    def width(self):
        """Area width."""
        return self.are['Width']
