import os

from pynwn.erf import Erf
from pynwn.gff import Gff
import pynwn.resource as RES


class Module:
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
            self.container = Erf.from_io(open(module, 'rb'))
        else:
            msg = "File/Directory %s does not exist!" % module
            raise ValueError(msg)

        if not self.container.has_file('module.ifo'):
            raise ValueError("The %s Container has no module.ifo!" % module)

        self.ifo = Gff(self.container['module.ifo'])

        # Generate Structure.
        self.struct = self.ifo.structure

    @property
    def areas(self):
        return self.ifo.get_list_values('Mod_Area_list', 'Area_Name')

    @property
    def haks(self):
        return self.ifo.get_list_values('Mod_HakList', 'Mod_Hak')

    @property
    def tlk(self):
        return self.struct['Mod_CustomTlk'][1]
