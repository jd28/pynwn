from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

from pynwn.obj.item import RepositoryItem

class Placeable(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utp':
                resref = resref+'.utp'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utp = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utp':
            if not self._utp: self._utp = self.gff.structure
            return self._utp

    def __getitem__(self, name):
        return self.utp[name].val

    @property
    def tag(self):
        """Tag"""
        return self['Tag']

    @property
    def name(self):
        """Localized name"""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocName'])

        return self._locstr['name']

    @property
    def description(self):
        """Localized description."""
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self.are['Description'])

        return self._locstr['description']

    @property
    def resref(self):
        """Resref"""
        return self['TemplateResRef']

    @property
    def key_auto_remove(self):
        """Auto-remove key."""
        return self['AutoRemoveKey']

    @property
    def lock_close_dc(self):
        """Lock close DC"""
        return self['CloseLockDC']

    @property
    def conversation(self):
        """Dialog resref"""
        return self['Conversation']

    @property
    def interruptable(self):
        """Conversation interruptable flag."""
        return self['Interruptable']

    @property
    def faction(self):
        """Faction ID"""
        return self['Faction']

    @property
    def plot(self):
        """Plot flag."""
        return self['Plot']

    @property
    def key_required(self):
        """Key required flag."""
        return self['KeyRequired']

    @property
    def lockable(self):
        """Lockable flag."""
        return self['Lockable']

    @property
    def locked(self):
        """Locked flag."""
        return self['Locked']

    @property
    def lock_open_dc(self):
        """Lock open DC"""
        return self['OpenLockDC']

    @property
    def portrait_id(self):
        """Portrait ID"""
        return self['PortraitId']

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
        """Trap disarmable flag"""
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
        """Trap one-shot flag."""
        return self['TrapOneShot']

    @property
    def trap_type(self):
        """Trap type."""
        return self['TrapType']

    @property
    def key_name(self):
        """Key tag."""
        return self['KeyName']

    @property
    def animation_state(self):
        """Animation state."""
        return self['AnimationState']

    @property
    def appearance(self):
        """Appearance ID."""
        return self['Appearance']

    @property
    def hp(self):
        """Hitpoints"""
        return self['HP']

    @property
    def hp_current(self):
        """Current hitpoints"""
        return self['CurrentHP']

    @property
    def hardness(self):
        """Hardness"""
        return self['Hardness']

    @property
    def save_fortitude(self):
        """Fortitude saving throw."""
        return self['Fort']

    @property
    def save_reflex(self):
        """Reflex saving throw."""
        return self['Ref']

    @property
    def save_will(self):
        """Will saving throw."""
        return self['Will']

    @property
    def script(self):
        """Scripts.  Responds to script events:

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
        #. Event.DISTURBED
        #. Event.USED
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
        lbls[Event.DISTURBED] = 'OnInvDisturbed'
        lbls[Event.USED] = 'OnUsed'

        self._scripts = NWObjectScripts(self.utd, lbls)

        return self._scripts

    @property
    def has_inventory(self):
        """Has inventory flag."""
        return self['HasInventory']

    @property
    def body_bag(self):
        return self['BodyBag']

    @property
    def static(self):
        """Static flag."""
        return self['Static']

    @property
    def type(self):
        return self['Type']

    @property
    def useable(self):
        """Useable flag."""
        return self['Useable']

    @property
    def items(self):
        """Invenory items.

        :returns: List of RepositoryItem objects or [] if
                  the object does not have an inventory.
        """
        if self.has_inventory:
            return [RepositoryItem(i) for i in self['ItemList']]
        else:
            return []

    @property
    def paletted_id(self):
        """Palette ID."""
        return self['PaletteID']

    @property
    def comment(self):
        """Comment."""
        return self['Comment']

class PlaceableInstance(Placeable):
    """A placeable instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Placeable.__init__(self, gff, None, True)
        self.is_instance = True
