from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

class Trigger(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utt':
                resref = resref+'.utt'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utt = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utt':
            if not self._utt: self._utt = self.gff.structure
            return self._utt

    def __getitem__(self, name):
        return self.utt[name].val

    @property
    def tag(self):
        return self['Tag']

    @property
    def resref(self):
        return self['TemplateResRef']

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def key_auto_remove(self):
        return self['AutoRemoveKey']

    @property
    def faction(self):
        return self['Faction']

    @property
    def cursor(self):
        return self['Cursor']

    @property
    def key_auto_remove(self):
        return self['TemplateResRef']

    @property
    def highlight_height(self):
        return self['HighlightHeight']

    @property
    def key_name(self):
        return self['KeyName']

    @property
    def linked_to(self):
        return self['LinkedTo']

    @property
    def linked_to_flags(self):
        return self['LinkedToFlags']

    @property
    def load_screen(self):
        return self['LoadScreenID']

    @property
    def portrait_id(self):
        return self['PortraitId']

    @property
    def type(self):
        return self['Type']

    @property
    def trap_detectable(self):
        return self['TrapDetectable']

    @property
    def trap_detect_dc(self):
        return self['TrapDetectDC']

    @property
    def trap_disarmable(self):
        return self['TrapDisarmable']

    @property
    def trap_disarm_dc(self):
        return self['DisarmDC']

    @property
    def trap_flag(self):
        return self['TrapFlag']

    @property
    def trap_one_shot(self):
        return self['TrapOneShot']

    @property
    def trap_type(self):
        return self['TrapType']

    @property
    def scripts(self):
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.TRAP_DISARMED] = 'OnDisarm'
        lbls[Event.TRAP_TRIGGERED] = 'OnTrapTriggered'
        lbls[Event.CLICK] = 'OnClick'
        lbls[Event.HEARTBEAT] = 'ScriptHeartbeat'
        lbls[Event.ENTER] = 'ScriptOnEnter'
        lbls[Event.EXIT] = 'ScriptOnExit'
        lbls[Event.USER_DEFINED] = 'ScriptUserDefine'

        self._scripts = NWObjectScripts(self.utt, lbls)

        return self._scripts
    
    @property
    def paletted_id(self):
        return self['PaletteID']

    @property
    def comment(self):
        return self['Comment']

class TriggerInstance(Trigger):
    """A trigger instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Trigger.__init__(self, gff, None, True)
        self.is_instance = True
