from pynwn.file.gff import Gff, GffInstance, make_gff_locstring_property
from pynwn.file.gff import make_gff_property

from pynwn.item import RepositoryItem, ItemInstance
from pynwn.scripts import *
from pynwn.vars import *

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

LOCSTRING_TABLE = {
    'name'        : ('LocName', "Localized name."),
    'description' : ('Description', "Localized description."),
}

class Placeable(NWObjectVarable):
    def __init__(self, resref, container, instance=False, instance_gff=None):
        self._scripts = None
        self._vars = None

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utp':
                resref = resref+'.utp'

            if container.has_file(resref):
                self.container = container
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.instance_gff = instance_gff
            self.gff = resref

        NWObjectVarable.__init__(self, self.gff)

    def stage(self):
        """ Stage changes to the placeable's GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

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

        self._scripts = NWObjectScripts(self.gff, lbls)

        return self._scripts

    @property
    def items(self):
        """Invenory items.

        :returns: List of RepositoryItem objects or [] if
                  the object does not have an inventory.
        """
        if self.has_inventory:
            result = []
            i = 0
            for p in self.gff['ItemList']:
                gff_inst = GffInstance(self.gff, 'ItemList', i)
                st_inst  = RepositoryItem(gff_inst)
                result.append(st_inst)
                i += 1

            return result
        else:
            return []

class PlaceableInstance(Placeable):
    """A placeable instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff, orignal):
        Placeable.__init__(self, gff, None, True, orignal)
        self.is_instance = True
        self.parent_obj = orignal

    def stage(self):
        """ Stage changes to the placeable instance's parent GFF structure.
        """
        self.parent_obj.stage()
        
    @property
    def items(self):
        """Inventory items.

        :returns: List of Tupels contiain repository position
                  and the ItemInstance.
        """

        result = []
        i = 0
        # If the creature doesn't have inventory items they won't
        # have an 'ItemList' field in their gff structure.
        try:
            for p in self.gff['ItemList']:
                gff_inst = GffInstance(self.parent_obj, self.gff, 'ItemList', i)
                st_inst  = ItemInstance(gff_inst)
                repo_pos = (p['Repos_PosX'], p['Repos_Posy'])
                result.append((repo_pos, st_inst))
                i += 1
        except KeyError:
            pass

        return result

    @property
    def position(self):
        return (self.gff['X'], self.gff['Y'], self.gff['Z'])

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Placeable, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Placeable, 'get_'+key, getter)
    setattr(Placeable, 'set_'+key, setter)
