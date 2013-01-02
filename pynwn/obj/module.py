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
        return [Area(a, self.container) for a in self.ifo.get_list_values('Mod_Area_list', 'Area_Name')]

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
        return self.ifo.get_list_values('Mod_HakList', 'Mod_Hak')

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

        lbls[EVENT_CUTSCENE_ABORT] = 'Mod_OnCutsnAbort'
        lbls[EVENT_ENTER] = 'Mod_OnClientEntr'
        lbls[EVENT_EXIT] = 'Mod_OnClientLeav'
        lbls[EVENT_HEARTBEAT] = 'Mod_OnHeartbeat'
        lbls[EVENT_ITEM_ACQUIRED] = 'Mod_OnAcquirItem'
        lbls[EVENT_ITEM_ACTIVATED] = 'Mod_OnActvtItem'
        lbls[EVENT_ITEM_EQUIPPED] = 'Mod_OnPlrEqItm'
        lbls[EVENT_ITEM_UNACQUIRED] = 'Mod_OnUnAqreItem'
        lbls[EVENT_ITEM_UNEQUIPPED] = 'Mod_OnPlrUnEqItm'
        lbls[EVENT_LEVELUP] = 'Mod_OnPlrLvlUp'
        lbls[EVENT_LOAD] = 'Mod_OnModLoad'
        lbls[EVENT_DEATH] = 'Mod_OnPlrDeath'
        lbls[EVENT_DYING] = 'Mod_OnPlrDying'
        lbls[EVENT_RESPAWN] = 'Mod_OnSpawnBtnDn'
        lbls[EVENT_REST] = 'Mod_OnPlrRest'
        lbls[EVENT_USER_DEFINED] = 'Mod_OnUsrDefined'

        self._scripts = NWObjectScripts(self.ifo, lbls)

        return self._scripts

    @property
    def tlk(self):
        return self.ifo['Mod_CustomTlk']

    @property
    def xp_scale(self):
        return self.ifo['Mod_XPScale']
