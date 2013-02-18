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
        """Tag"""
        return self['Tag']

    @property
    def resref(self):
        """Resref"""
        return self['TemplateResRef']

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def key_auto_remove(self):
        """Auto-remove key flag."""
        return self['AutoRemoveKey']

    @property
    def faction(self):
        """Faction ID"""
        return self['Faction']

    @property
    def cursor(self):
        return self['Cursor']

    @property
    def key_auto_remove(self):
        """Auto-remove key flag."""
        return self['TemplateResRef']

    @property
    def highlight_height(self):
        """Highlight height."""
        return self['HighlightHeight']

    @property
    def key_name(self):
        """Key tag."""
        return self['KeyName']

    @property
    def linked_to(self):
        """Linked to object tag."""
        return self['LinkedTo']

    @property
    def linked_to_flags(self):
        """Linked to flags."""
        return self['LinkedToFlags']

    @property
    def load_screen(self):
        """Load screen ID"""
        return self['LoadScreenID']

    @property
    def portrait_id(self):
        """Portrait ID"""
        return self['PortraitId']

    @property
    def type(self):
        return self['Type']

    @property
    def trap_detectable(self):
        """Trap detectable flag."""
        return self['TrapDetectable']

    @property
    def trap_detect_dc(self):
        """Trap detect DC"""
        return self['TrapDetectDC']

    @property
    def trap_disarmable(self):
        """Trap disarmable flag."""
        return self['TrapDisarmable']

    @property
    def trap_disarm_dc(self):
        """Trap disarm DC"""
        return self['DisarmDC']

    @property
    def trap_flag(self):
        return self['TrapFlag']

    @property
    def trap_one_shot(self):
        return self['TrapOneShot']

    @property
    def trap_type(self):
        """Trap type."""
        return self['TrapType']

    @property
    def scripts(self):
        """Scripts.  Responds to script events:

        #. Event.TRAP_DISARMED
        #. Event.TRAP_TRIGGERED
        #. Event.CLICK
        #. Event.HEARTBEAT
        #. Event.ENTER
        #. Event.EXIT
        #. Event.USER_DEFINED
        """
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
        """Palette ID"""
        return self['PaletteID']

    @property
    def comment(self):
        """Comment"""
        return self['Comment']

class TriggerInstance(Trigger):
    """A trigger instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Trigger.__init__(self, gff, None, True)
        self.is_instance = True
