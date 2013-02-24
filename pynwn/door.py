from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property
from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['Door', 'DoorInstance']

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

LOCSTRING_TABLE = {
    'name'        : ('LocName', "Localized name."),
    'description' : ('Description', "Localized description."),
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
                self.container = container
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref

        NWObjectVarable.__init__(self, self.gff)

    def save(self):
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

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

        self._scripts = NWObjectScripts(self.gff, lbls)

        return self._scripts

class DoorInstance(Door):
    """A door instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Door.__init__(self, gff, None, True)
        self.is_instance = True

    @property
    def position(self):
        return (self.gff['X'], self.gff['Y'], self.gff['Z'])

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Door, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Door, 'get_'+key, getter)
    setattr(Door, 'set_'+key, setter)
