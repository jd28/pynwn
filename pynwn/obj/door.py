from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

class Door(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utd':
                resref = resref+'.utd'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utd = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utd':
            if not self._utd: self._utd = self.gff.structure
            return self._utd

    def __getitem__(self, name):
        return self.utd[name].val

    @property
    def tag(self):
        """Tag"""
        return self['Tag']

    @property
    def name(self):
        """Localized Name"""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocName'])

        return self._locstr['name']

    @property
    def description(self):
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self.are['Description'])

        return self._locstr['description']

    @property
    def resref(self):
        """Resref"""
        return self['TemplateResRef']

    @property
    def key_auto_remove(self):
        """Auto-remove key"""
        return self['AutoRemoveKey']

    @property
    def lock_close_dc(self):
        """ """
        return self['CloseLockDC']

    @property
    def conversation(self):
        """Door conversation resref."""
        return self['Conversation']

    @property
    def interruptable(self):
        """Door conversation is interruptable."""
        return self['Interruptable']

    @property
    def faction(self):
        """Door's faction ID"""
        return self['Faction']

    @property
    def plot(self):
        """Door is plot"""
        return self['Plot']

    @property
    def key_required(self):
        """Key required to unlock door."""
        return self['KeyRequired']

    @property
    def lockable(self):
        """Door is lockable."""
        return self['Lockable']

    @property
    def locked(self):
        """Door is locked"""
        return self['Locked']

    @property
    def lock_open_dc(self):
        return self['OpenLockDC']

    @property
    def portrait_id(self):
        """Portrait ID"""
        return self['PortraitId']

    @property
    def trap_detectable(self):
        """Trap is detectable"""
        return self['TrapDetectable']

    @property
    def trap_detect_dc(self):
        """Trap detect DC"""
        return self['TrapDetectDC']

    @property
    def trap_disarmable(self):
        """Trap is disarmable"""
        return self['TrapDisarmable']

    @property
    def trap_disarm_dc(self):
        """Trap disarm DC"""
        return self['DisarmDC']

    @property
    def trap_flag(self):
        """Trap flag."""
        return self['TrapFlag']

    @property
    def trap_one_shot(self):
        """Trap is one-shot."""
        return self['TrapOneShot']

    @property
    def trap_type(self):
        """Trap type"""
        return self['TrapType']

    @property
    def key_name(self):
        """Key tag"""
        return self['KeyName']

    @property
    def animation_state(self):
        """Animation State"""
        return self['AnimationState']

    @property
    def appearance(self):
        """Appearance"""
        return self['Appearance']

    @property
    def hp(self):
        """Maximum Hitpoints"""
        return self['HP']

    @property
    def hp_current(self):
        """Current Hitpoints"""
        return self['CurrentHP']

    @property
    def hardness(self):
        """Hardness"""
        return self['Hardness']

    @property
    def save_fortitude(self):
        """Fortitude Saving Throw"""
        return self['Fort']

    @property
    def save_reflex(self):
        """Reflex Saving Throw"""
        return self['Ref']

    @property
    def save_will(self):
        """Will Saving Throw"""
        return self['Will']

    @property
    def script(self):
        """Scripts: Door responds to the following script events:

        #. Event.CLOSE
        #. Event.DAMAGED
        #. Event.DEATH
        #. Event.TRAP_DISARMED
        #. Event.HEARTBEAT
        #. Event.LOCK
        #. Event.ATTACKED
        #. Event.OPEN
        #. Event.SPELL_CAST_AT
        #. Event.TRAP_TRIGGERED
        #. Event.UNLOCK
        #. Event.USER_DEFINED
        #. Event.CLICK
        #. Event.FAIL_TO_OPEN

        """
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.CLOSE] = 'OnClosed'
        lbls[Event.DAMAGED] = 'OnDamaged'
        lbls[Event.DEATH] = 'OnDeath'
        lbls[Event.TRAP_DISARMED] = 'OnDisarm'
        lbls[Event.HEARTBEAT] = 'OnHeartbeat'
        lbls[Event.LOCK] = 'OnLock'
        lbls[Event.ATTACKED] = 'OnMeleeAttacked'
        lbls[Event.OPEN] = 'OnOpen'
        lbls[Event.SPELL_CAST_AT] = 'OnSpellCastAt'
        lbls[Event.TRAP_TRIGGERED] = 'OnTrapTriggered'
        lbls[Event.UNLOCK] = 'OnUnlock'
        lbls[Event.USER_DEFINED] = 'OnUserDefined'
        lbls[Event.CLICK] = 'OnClick'
        lbls[Event.FAIL_TO_OPEN] = 'OnFailToOpen'

        self._scripts = NWObjectScripts(self.utd, lbls)

        return self._scripts

    @property
    def linked_to(self):
        """Linked to tag."""
        return self['LinkedTo']

    @property
    def linked_to_flags(self):
        """Linked to flags."""
        return self['LinkedToFlags']

    @property
    def load_screen(self):
        """Load screen id."""
        return self['LoadScreenID']

    @load_screen.setter
    def load_screen(self, val):
        self['LoadScreenID'] = val

    @property
    def generic_type(self):
        return self['GenericType_New']

    @property
    def paletted_id(self):
        """Palette ID"""
        return self['PaletteID']

    @property
    def comment(self):
        """Comment"""
        return self['Comment']

class DoorInstance(Door):
    """A door instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Door.__init__(self, gff, None, True)
        self.is_instance = True
