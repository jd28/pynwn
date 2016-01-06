from pynwn.file.gff import Gff, GffInstance, make_gff_locstring_property
from pynwn.file.gff import make_gff_property

from pynwn.item import RepositoryItem, ItemInstance
from pynwn.scripts import *
from pynwn.vars import *

TRANSLATION_TABLE = {
    'tag': ('Tag', "Tag."),
    'resref': ('TemplateResRef', "Resref."),
    'key_auto_remove': ('AutoRemoveKey', "Auto-remove key."),
    'lock_close_dc': ('CloseLockDC', "Close lock DC."),
    'conversation': ('Conversation', "Conversation resref."),
    'interruptable': ('Interruptable', "Conversation interruptable flag."),
    'faction': ('Faction', "Faction ID."),
    'plot': ('Plot', "Plot flag."),
    'key_required': ('KeyRequired', "Key required flag."),
    'lockable': ('Lockable', "Lockable flag."),
    'locked': ('Locked', "Locked flag."),
    'lock_open_dc': ('OpenLockDC', "Open lock DC."),
    'portrait_id': ('PortraitId', "Portrait ID."),
    'trap_detectable': ('TrapDetectable', "Trap detectable flag."),
    'trap_detect_dc': ('TrapDetectDC', "Trap detect DC."),
    'trap_disarmable': ('TrapDisarmable', "Trap disarmable flag."),
    'trap_disarm_dc': ('DisarmDC', "Trap disarm DC."),
    'trap_flag': ('TrapFlag', "Trap flag."),
    'trap_one_shot': ('TrapOneShot', "Trap is one-shot."),
    'trap_type': ('TrapType', "Trap type."),
    'key_tag': ('KeyName', "Key tag."),
    'animation_state': ('AnimationState', "Animation State."),
    'appearance': ('Appearance', "Appearance ID."),
    'hp': ('HP', "Maximum Hitpoints."),
    'hp_current': ('CurrentHP', "Current Hitpoints."),
    'hardness': ('Hardness', "Hardness."),
    'save_fortitude': ('Fort', "Fortitude Saving Throw."),
    'save_reflex': ('Ref', "Reflex Saving Throw."),
    'save_will': ('Will', "Will Saving Throw."),
    'has_inventory': ('HasInventory', "Has inventory flag."),
    'body_bag': ('BodyBag', "Body bag."),
    'static': ('Static', "Static flag."),
    'type': ('Type', "Type."),
    'useable': ('Useable', "Useable flag."),
    'paletted_id': ('PaletteID', "Palette ID."),
    'comment': ('Comment', "Comment.")
}

LOCSTRING_TABLE = {
    'name': ('LocName', "Localized name."),
    'description': ('Description', "Localized description."),
}


class Placeable(object):
    def __init__(self, resource, instance=False):
        self._scripts = None
        self._vars = None
        self.is_file = False

        self.is_instance = instance
        if not instance:
            if isinstance(resource, str):
                from pynwn import ContentObject
                co = ContentObject.from_file(resource)
                self.gff = Gff(co)
                self.is_file = True
            else:
                self.container = resource[1]
                self.gff = Gff(resource[0])
        else:
            self.gff = resource

    def stage(self):
        """ Stage changes to the placeable's GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def vars(self):
        """ Variable table """
        if self._vars:
            return self._vars
        self._vars = NWObjectVarable(self, self.gff)
        return self._vars

    @property
    def scripts(self):
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
        if self._scripts:
            return self._scripts

        lbls = {
            Event.CLOSE: 'OnClosed',
            Event.DAMAGED: 'OnDamaged',
            Event.DEATH: 'OnDeath',
            Event.TRAP_DISARMED: 'OnDisarm',
            Event.HEARTBEAT: 'OnHeartbeat',
            Event.LOCK: 'OnLock',
            Event.ATTACKED: 'OnMeleeAttacked',
            Event.OPEN: 'OnOpen',
            Event.SPELL_CAST_AT: 'OnSpellCastAt',
            Event.TRAP_TRIGGERED: 'OnTrapTriggered',
            Event.UNLOCK: 'OnUnlock',
            Event.USER_DEFINED: 'OnUserDefined',
            Event.CLICK: 'OnClick',
            Event.DISTURBED: 'OnInvDisturbed',
            Event.USED: 'OnUsed'
        }

        self._scripts = NWObjectScripts(self, lbls)

        return self._scripts

    @property
    def items(self):
        """Invenory items.

        :returns: List of RepositoryItem objects or [] if
                  the object does not have an inventory.
        """
        if self.has_inventory and self.gff.has_field('ItemList'):
            result = []
            i = 0
            for p in self.gff['ItemList']:
                gff_inst = GffInstance(self.gff, 'ItemList', i)
                st_inst = RepositoryItem(gff_inst, self)
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
        Placeable.__init__(self, gff, True)
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
                gff_inst = GffInstance(self.gff, 'ItemList', i)
                st_inst = ItemInstance(gff_inst, self)
                repo_pos = (p['Repos_PosX'], p['Repos_Posy'])
                result.append((repo_pos, st_inst))
                i += 1
        except KeyError:
            pass

        return result

    @property
    def position(self):
        return self.gff['X'], self.gff['Y'], self.gff['Z']


for key, val in TRANSLATION_TABLE.items():
    setattr(Placeable, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Placeable, 'get_' + key, getter)
    setattr(Placeable, 'set_' + key, setter)
