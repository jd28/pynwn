from pynwn.gff import Gff, make_gff_property

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

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
    'linked_to'       : ('LinkedTo', "Linked to tag."),
    'linked_to_flags' : ('LinkedToFlags', "Linked to flags."),
    'load_screen'     : ('LoadScreenID', "Load screen ID."),
    'generic_type'    : ('GenericType_New', "Generic type."),
    'paletted_id'     : ('PaletteID', "Palette ID."),
    'comment'         : ('Comment', "Comment."),
}

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

    def __setitem__(self, name, val):
        self.utd[name].val = val

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

class DoorInstance(Door):
    """A door instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Door.__init__(self, gff, None, True)
        self.is_instance = True

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Door, key, make_gff_property('utd', val))
