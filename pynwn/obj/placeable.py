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
        return self['Tag']

    @property
    def name(self):
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
        return self['TemplateResRef']

    @property
    def key_auto_remove(self):
        return self['AutoRemoveKey']

    @property
    def lock_close_dc(self):
        return self['CloseLockDC']

    @property
    def conversation(self):
        return self['Conversation']

    @property
    def interruptable(self):
        return self['Interruptable']

    @property
    def faction(self):
        return self['Faction']

    @property
    def plot(self):
        return self['Plot']

    @property
    def key_required(self):
        return self['KeyRequired']

    @property
    def lockable(self):
        return self['Lockable']

    @property
    def locked(self):
        return self['Locked']

    @property
    def lock_open_dc(self):
        return self['OpenLockDC']

    @property
    def portrait_id(self):
        return self['PortraitId']

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
    def key_name(self):
        return self['KeyName']

    @property
    def animation_state(self):
        return self['AnimationState']

    @property
    def appearance(self):
        return self['Appearance']

    @property
    def hp(self):
        return self['HP']

    @property
    def hp_current(self):
        return self['CurrentHP']

    @property
    def hardness(self):
        return self['Hardness']

    @property
    def save_fortitude(self):
        return self['Fort']

    @property
    def save_reflex(self):
        return self['Ref']

    @property
    def save_will(self):
        return self['Will']

    @property
    def script(self):
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
        return self['HasInventory']

    @property
    def body_bag(self):
        return self['BodyBag']

    @property
    def static(self):
        return self['Static']

    @property
    def type(self):
        return self['Type']

    @property
    def useable(self):
        return self['Useable']

    @property
    def items(self):
        if self.has_inventory:
            return [RepositoryItem(i) for i in self['ItemList']]
        else:
            return []

    @property
    def paletted_id(self):
        return self['PaletteID']

    @property
    def comment(self):
        return self['Comment']

class PlaceableInstance(Placeable):
    """A placeable instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Placeable.__init__(self, gff, None, True)
        self.is_instance = True
