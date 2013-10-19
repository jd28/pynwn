from pynwn.file.gff import Gff, GffInstance, make_gff_locstring_property
from pynwn.file.gff import make_gff_property

from pynwn.creature import CreatureInstance
from pynwn.door import DoorInstance
from pynwn.encounter import EncounterInstance
from pynwn.item import ItemInstance
from pynwn.placeable import PlaceableInstance
from pynwn.sound import SoundInstance
from pynwn.store import StoreInstance
from pynwn.tile import TileInstance
from pynwn.trigger import TriggerInstance
from pynwn.waypoint import WaypointInstance

from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['Area']

ARE_TRANSLATION_TABLE = {
    'lightning'           : ('ChanceLightning', 'Chance of lighting [0,100]'),
    'rain'                : ('ChanceRain', 'Chance of rain [0,100]'),
    'snow'                : ('ChanceSnow', 'Chance of snow [0,100]'),
    'day_night_cycle'     : ('DayNightCycle', "1 if day/night transitions occur, 0 otherwise."),
    'fog_clip_distance'   : ('FogClipDist', "Fog clip distance."),
    'flags'               : ('Flags', "Bit flags specifying area terrain type."),
    'is_night'            : ('IsNight', "1 if always night, 0 if always day."),
    'lighting_scheme'     : ('LightingScheme', 'Index into environment.2da'),
    'load_screen'         : ('LoadScreenID', 'Load screen ID'),
    'listen_modifier'     : ('ModListenCheck', 'Modifier to Listen skill checks made in area'),
    'spot_modifier'       : ('ModSpotCheck', 'Modifier to Spot skill checks made in area'),
    'night_ambient_color' : ('MoonAmbientColor', 'Nighttime ambient color.'),
    'night_diffuse_color' : ('MoonDiffuseColor', 'Nighttime diffuse color.'),
    'night_fog_color'     : ('MoonFogColor', 'Nighttime fog color.'),
    'night_fog_amount'    : ('MoonFogAmount', 'Nighttime fog amount (0-15)'),
    'night_shadows'       : ('MoonShadows', '1 if shadows appear at night, 0 otherwise'),
    'pvp'                 : ('PlayerVsPlayer', 'Area PvP setting.'),
    'skybox'              : ('SkyBox', 'Index into skyboxes.2da.'),
    'shadow_opacity'      : ('ShadowOpacity', 'Opacity of shadows (0-100).'),
    'day_ambient_color'   : ('SunAmbientColor', 'Day ambient color.'),
    'day_diffuse_color'   : ('SunDiffuseColor', 'Day diffuse color.'),
    'day_fog_color'       : ('SunFogColor', 'Daytime fog color (BGR format) '),
    'day_fog_amount'      : ('SunFogAmount', 'Daytime fog amount (0-15) '),
    'day_shadows'         : ('SunShadows', '1 if shadows appear during the day, 0 otherwise.'),
    'version'             : ('Version', 'Area version'),
    'no_rest'             : ('NoRest', '1 if resting is not allowed, 0 otherwise '),
    'wind_power'          : ('WindPower', 'Strength of the wind in the area. None, weak, or strong (0-2).'),
    'height'              : ('Height', "Area height."),
    'resref'              : ('ResRef', "Resref."),
    'tag'                 : ('Tag', "Tag."),
    'tileset'             : ('Tileset', "Tileset."),
    'width'               : ('Width', "Area width."),
    'comments'            : ('Comments', "Comments.")
}

LOCSTRING_TABLE = {
    'name'        : ('Name', "Localized name."),
}

class Area(object):
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
        else:
            raise ValueError("Container does not contain %s.git" % resref)

        gic = resref+'.gic'
        if container.has_file(gic):
            self.gic = container[gic]
            self.gic = Gff(self.gic)
        else:
            raise ValueError("Container does not contain %s.gic" % resref)

        self._vars = None
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
    def vars(self):
        """ Variable table """
        if self._vars: return self._vars
        self._vars = NWObjectVarable(self, self.git)
        return self._vars

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
    def items(self):
        """Item instance list.

        :returns: List of ItemInstance objects.
        """
        return self.get_instances('List', ItemInstance)

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
