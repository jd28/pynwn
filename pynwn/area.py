from pynwn.file.gff import Gff, GffInstance, make_gff_locstring_property
from pynwn.file.gff import make_gff_property

from pynwn.creature import CreatureInstance
from pynwn.door import DoorInstance
from pynwn.encounter import EncounterInstance
from pynwn.placeable import PlaceableInstance
from pynwn.sound import SoundInstance
from pynwn.store import StoreInstance
from pynwn.trigger import TriggerInstance
from pynwn.waypoint import WaypointInstance
from pynwn.tile import TileInstance

from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['Area']

ARE_TRANSLATION_TABLE = {
    'fog_clip_distance' : ('FogClipDist', "Fog clip distance."),
    'height'            : ('Height', "Area height."),
    'resref'            : ('ResRef', "Resref."),
    'tag'               : ('Tag', "Tag."),
    'tileset'           : ('Tileset', "Tileset."),
    'width'             : ('Width', "Area width.")
}

LOCSTRING_TABLE = {
    'name'        : ('Name', "Localized name."),
}

class Area(NWObjectVarable):
    def __init__(self, resref, container):
        are = resref+'.are'

        self.container = container
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

    def stage(self):
        """Stages changes to the Area's GFF structures.
        """
        if self.are.is_loaded():
            self.container.add_to_saves(self.are)

        if self.git.is_loaded():
            self.container.add_to_saves(self.git)

        if self.gic.is_loaded():
            self.container.add_to_saves(self.gic)

    def get_instances(self, list_name, instance_class):
        result = []
        i = 0
        for p in self.git[list_name]:
            gff_inst = GffInstance(self.git, list_name, i)
            st_inst  = instance_class(gff_inst, self)
            result.append(st_inst)
            i += 1

        return result

    @property
    def doors(self):
        """Door instances.

        :returns: List of DoorInstance objects.
        """
        return self.get_instances('Door List', DoorInstance)


    @property
    def creatures(self):
        """Creature instances.

        :returns: List of CreatureInstance objects.
        """
        return self.get_instances('Creature List',  CreatureInstance)

    @property
    def encounters(self):
        """Encounters

        :returns: List of EncounterInstance objects.
        """
        return self.get_instances('Encounter List', EncounterInstance)

    @property
    def placeables(self):
        """Placeables

        :returns: List of PlaceableInstance objects.
        """
        return self.get_instances('Placeable List', PlaceableInstance)

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
        return self.get_instances('SoundList', SoundInstance)

    @property
    def tiles(self):
        """Tiles
        :returns: List of TileInstance objects.
        """
        result = []
        i = 0
        for p in self.are['Tile_List']:
            gff_inst = GffInstance(self.are, 'Tile_List', i)
            st_inst  = TileInstance(gff_inst, self)
            result.append(st_inst)
            i += 1

        return result

    @property
    def stores(self):
        """Stores

        :returns: List of StoreInstance objects.
        """
        return self.get_instances('StoreList', StoreInstance)

    @property
    def triggers(self):
        """Triggers

        :returns: List of TriggerInstance objects.
        """
        return self.get_instances('TriggerList', TriggerInstance)

    @property
    def waypoints(self):
        """Waypoints

        :returns: List of WaypointInstance objects.
        """
        return self.get_instances('WaypointList', WaypointInstance)

for key, val in ARE_TRANSLATION_TABLE.iteritems():
    setattr(Area, key, make_gff_property('are', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('are', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Area, 'get_'+key, getter)
    setattr(Area, 'set_'+key, setter)
