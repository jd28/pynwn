from pynwn.gff import Gff, make_gff_property

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

from pynwn.obj.item import RepositoryItem

TRANSLATION_TABLE = {
    'tag'             : ('Tag', "Tag."),
    'resref'          : ('TemplateResRef', "Resref."),
    'key_auto_remove' : ('AutoRemoveKey', "Auto-remove key."),
    'lock_close_dc'   : ('CloseLockDC', "Close lock DC."),
    'conversation'    : ('Conversation', "Conversation resref."),
    'interruptable'   : ('Interruptable', "Conversation interruptable flag."),
    'faction'         : ('Faction', "Faction ID."),
    'plot'            : ('Plot', "Plot flag."),
    'key_required'    : ('KeyRequired', "Key required flag."),
    'lockable'        : ('Lockable', "Lockable flag."),
    'locked'          : ('Locked', "Locked flag."),
    'lock_open_dc'    : ('OpenLockDC', "Open lock DC."),
    'portrait_id'     : ('PortraitId', "Portrait ID."),
    'trap_detectable' : ('TrapDetectable', "Trap detectable flag."),
    'trap_detect_dc'  : ('TrapDetectDC', "Trap detect DC."),
    'trap_disarmable' : ('TrapDisarmable', "Trap disarmable flag."),
    'trap_disarm_dc'  : ('DisarmDC', "Trap disarm DC."),
    'trap_flag'       : ('TrapFlag', "Trap flag."),
    'trap_one_shot'   : ('TrapOneShot', "Trap is one-shot."),
    'trap_type'       : ('TrapType', "Trap type."),
    'key_tag'         : ('KeyName', "Key tag."),
    'animation_state' : ('AnimationState', "Animation State."),
    'appearance'      : ('Appearance', "Appearance ID."),
    'hp'              : ('HP', "Maximum Hitpoints."),
    'hp_current'      : ('CurrentHP', "Current Hitpoints."),
    'hardness'        : ('Hardness', "Hardness."),
    'save_fortitude'  : ('Fort', "Fortitude Saving Throw."),
    'save_reflex'     : ('Ref', "Reflex Saving Throw."),
    'save_will'       : ('Will', "Will Saving Throw."),
    'has_inventory'   : ('HasInventory', "Has inventory flag."),
    'body_bag'        : ('BodyBag', "Body bag."),
    'static'          : ('Static', "Static flag."),
    'type'            : ('Type', "Type."),
    'useable'         : ('Useable', "Useable flag."),
    'paletted_id'     : ('PaletteID', "Palette ID."),
    'comment'         : ('Comment', "Comment.")
}

class Placeable(NWObjectVarable):
    def __init__(self, resref, container, instance=False, instance_gff=None):
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
            self.instance_gff = instance_gff
            self.gff = resref
            self._utp = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utp':
            if not self._utp: self._utp = self.gff.structure
            return self._utp

    def __getitem__(self, name):
        return self.utp[name].val

    def __setitem__(self, name, value):
        self.utp[name].val = value

    def save(self):
        if not self.is_instance:
            self.gff.save()

    @property
    def name(self):
        """Localized name"""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self['LocName'])

        return self._locstr['name']

    @property
    def description(self):
        """Localized description."""
        if not self._locstr.has_key('description'):
            self._locstr['description'] = LocString(self['Description'])

        return self._locstr['description']

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

        self._scripts = NWObjectScripts(self.utp, lbls)

        return self._scripts

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

class PlaceableInstance(Placeable):
    """A placeable instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff, orignal):
        Placeable.__init__(self, gff, None, True, orignal)
        self.is_instance = True

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Placeable, key, make_gff_property('utp', val))
