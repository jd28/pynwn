import os

from pynwn.file.erf import Erf
from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property

from pynwn.area import Area
from pynwn.placeable import Placeable
import pynwn.resource as RES
from pynwn.scripts import *
from pynwn.vars import *

TRANSLATION_TABLE = {
    'game_version'   : ('Mod_MinGameVer', 'Game version'),
    'expansion_pack' : ('Expansion_Pack', 'Expansion pack.'),
    'tlk'            : ('Mod_CustomTlk', 'Custom TLK file.'),
    'xp_scale'       : ('Mod_XPScale', 'Experience point scale.'),
}

LOCSTRING_TABLE = {
    'name'  : ('Mod_Name', "Localized name."),
    'description' : ('Mod_Description', "Localized description.")
}

class Module(object):
    """Module abstracts over MOD ERF files and directories containing the contents of
    MOD files.
    """
    def __init__(self, module):
        if not isinstance(module, str):
            raise ValueError("Module must be instantiated with a file path to a MOD file or a directory")

        if os.path.isdir(module):
            self.container = RES.DirectoryContainer(module)
        elif os.path.isfile(module):
            # If it's a file, assume that it is a module ERF.
            self.container = Erf.from_file(module)
        else:
            msg = "File/Directory %s does not exist!" % module
            raise ValueError(msg)

        if not self.container.has_file('module.ifo'):
            raise ValueError("The %s Container has no module.ifo!" % module)

        self.gff = Gff(self.container['module.ifo'])

        self._scripts = None
        self._vars = None
        self._locstr = {}

    def glob(self, glob_pattern):
        """Returns a list of (ContentObject, Container) tuples for file names matching the glob pattern.
        i.e. Unix shell-style wildcards: \*.utc
        Note: all file names are converted to lowercase.
        """
        return self.container.glob(glob_pattern)

    def stage(self):
        """Stages changes to the modules IFO GFF structure."""
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def vars(self):
        """ Variable table """
        if self._vars: return self._vars
        self._vars = NWObjectVarable(self, self.gff)
        return self._vars

    @property
    def areas(self):
        """Areas.

        :returns: List of Area objects.
        """

        res = []
        for a in self.gff['Mod_Area_list']:
            res.append(Area(a['Area_Name'].val, self.container))

        return res

    @property
    def entry_area(self):
        """Entry area resref"""
        return Area(self.gff['Mod_Entry_Area'], self.container)

    @property
    def entry_location(self):
        """Entry location.

        :returns: Tuple of the X, Y, Z coordinates.
        """
        return (self.gff['Mod_Entry_X'], self.gff['Mod_Entry_Y'], self.gff['Mod_Entry_Z'])


    @property
    def haks(self):
        """List of HAK files."""
        return [hak['Mod_Hak'].value for hak in self.gff['Mod_HakList']]

    @property
    def script(self):
        """Scripts.  Responds to script events:

        #. Event.CUTSCENE_ABORT
        #. Event.ENTER
        #. Event.EXIT
        #. Event.HEARTBEAT
        #. Event.ITEM_ACQUIRED
        #. Event.ITEM_ACTIVATED
        #. Event.ITEM_EQUIPPED
        #. Event.ITEM_UNACQUIRED
        #. Event.ITEM_UNEQUIPPED
        #. Event.LEVELUP
        #. Event.LOAD
        #. Event.DEATH
        #. Event.DYING
        #. Event.RESPAWN
        #. Event.REST
        #. Event.USER_DEFINED
        """
        if self._scripts: return self._scripts

        lbls = {}

        lbls[Event.CUTSCENE_ABORT] = 'Mod_OnCutsnAbort'
        lbls[Event.ENTER] = 'Mod_OnClientEntr'
        lbls[Event.EXIT] = 'Mod_OnClientLeav'
        lbls[Event.HEARTBEAT] = 'Mod_OnHeartbeat'
        lbls[Event.ITEM_ACQUIRED] = 'Mod_OnAcquirItem'
        lbls[Event.ITEM_ACTIVATED] = 'Mod_OnActvtItem'
        lbls[Event.ITEM_EQUIPPED] = 'Mod_OnPlrEqItm'
        lbls[Event.ITEM_UNACQUIRED] = 'Mod_OnUnAqreItem'
        lbls[Event.ITEM_UNEQUIPPED] = 'Mod_OnPlrUnEqItm'
        lbls[Event.LEVELUP] = 'Mod_OnPlrLvlUp'
        lbls[Event.LOAD] = 'Mod_OnModLoad'
        lbls[Event.DEATH] = 'Mod_OnPlrDeath'
        lbls[Event.DYING] = 'Mod_OnPlrDying'
        lbls[Event.RESPAWN] = 'Mod_OnSpawnBtnDn'
        lbls[Event.REST] = 'Mod_OnPlrRest'
        lbls[Event.USER_DEFINED] = 'Mod_OnUsrDefined'

        self._scripts = NWObjectScripts(self, lbls)

        return self._scripts


for key, val in TRANSLATION_TABLE.items():
    setattr(Module, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Module, 'get_'+key, getter)
    setattr(Module, 'set_'+key, setter)
