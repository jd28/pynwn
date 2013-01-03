import os

from pynwn.erf import Erf
from pynwn.gff import Gff
import pynwn.resource as RES
from pynwn.obj.area import Area

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

class Module(NWObjectVarable):
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

        self.ifo = Gff(self.container['module.ifo'])

        NWObjectVarable.__init__(self, self.ifo)

        self._scripts = None
        self._vars = None
        self._locstr = {}

        # Generate Structure.
        self.struct = self.ifo.structure

    @property
    def areas(self):
        return [Area(a['Area_Name'], self.container) for a in self.ifo['Mod_Area_list']]

    @property
    def description(self):
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self.ifo['Mod_Description'])

        return self._locstr['description']

    @property
    def entry_area(self):
        return Area(self.ifo['Mod_Entry_Area'], self.container)

    @property
    def entry_location(self):
        return (self.ifo['Mod_Entry_X'], self.ifo['Mod_Entry_Y'], self.ifo['Mod_Entry_Z'])

    @property
    def expansion_pack(self):
        return self.ifo['Expansion_Pack']

    @property
    def haks(self):
        return [hak['Mod_Hak'] for hak in self.ifo['Mod_HakList']]

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.ifo['Mod_Name'])

        return self._locstr['name']

    @property
    def game_version(self):
        return self.ifo['Mod_MinGameVer']

    @property
    def script(self):
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

        self._scripts = NWObjectScripts(self.ifo, lbls)

        return self._scripts

    @property
    def tlk(self):
        return self.ifo['Mod_CustomTlk']

    @property
    def xp_scale(self):
        return self.ifo['Mod_XPScale']
