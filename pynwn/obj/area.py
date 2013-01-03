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
        return [EncounterInstance(p) for p in self.git['Encounter List']]

    @property
    def fog_clip_distance(self):
        return self.are['FogClipDist']

    @property
    def height(self):
        return self.are['Height']

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['Name'])

        return self._locstr['name']

    @property
    def placeables(self):
        return [PlaceableInstance(p) for p in self.git['Placeable List']]

    @property
    def resref(self):
        return self.are['ResRef']

    @property
    def script(self):
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
        return [SoundInstance(p) for p in self.git['SoundList']]

    @property
    def tag(self):
        return self.are['Tag']

    @property
    def tileset(self):
        return self.are['Tileset']

    @property
    def triggers(self):
        return [TriggerInstance(p) for p in self.git['TriggerList']]

    @property
    def waypoints(self):
        return [WaypointInstance(p) for p in self.git['WaypointList']]

    @property
    def width(self):
        return self.are['Width']
