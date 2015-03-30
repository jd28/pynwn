from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property
from pynwn.file.gff import GffInstance

from pynwn.item import RepositoryItem, ItemInstance
from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['Creature', 'CreatureInstance']

TRANSLATION_TABLE = {
    # Shared with Player Character
    'appearance'       : ('Appearance_Type', "Appearance ID."),
    'bodybag'          : ('BodyBag', "Body bag."),
    'charisma'         : ('Cha', "Creature's charisma."),
    'cr'               : ('ChallengeRating', "Challenge Rating"),
    # Class List
    'constitution'     : ('Con', "Creature's constitution."),
    'conversation'     : ('Conversation', "Dialog resref."),

    'race'             : ('Race', "Racial Type"),
    'gender'           : ('Gender', "Gender."),
    'phenotype'        : ('Phenotype', "Phenotype ID."),
    'portrait_id'      : ('PortraitId', "Portrait ID."),
    'tag'              : ('Tag', "Tag"),
    'is_pc'            : ('IsPC', "Player character flag."),
    'faction'          : ('FactionID', "Faction ID."),
    'disarmable'       : ('Disarmable', "Disarmable flag."),
    'subrace'          : ('Subrace', "Subrace."),
    'diety'            : ('Deity', "Deity"),
    'wings'            : ('Wings_New', "Wings ID."),
    'tail'             : ('Tail_New', "Tail ID."),
    'is_immortal'      : ('IsImmortal', "Immortal flag."),
    'interruptable'    : ('Interruptable', "Conversation interruptable flag."),
    'lootable'         : ('Lootable', "Lootable."),
    'no_perm_death'    : ('NoPermDeath', "No permenant death flag."),
    'starting_package' : ('StartingPackage', "Starting package ID."),
    'corpse_decay'     : ('DecayTime', "Corpse decay time."),
    'strength'         : ('Str', "Creature's strength."),
    'dexterity'        : ('Dex', "Creature's dexterity."),

    'intelligence'     : ('Int', "Creature's intelligence."),
    'wisdom'           : ('Wis', "Creature's wisdom."),

    'walkrate'         : ('WalkRate', "Walkrate."),
    'natural_ac'       : ('NaturalAC', "Natural AC."),
    'hp'               : ('HitPoints', "HP."),
    'hp_current'       : ('CurrentHitPoints', "Current hitpoints."),
    'hp_max'           : ('MaxHitPoints', "Maximum hitpoints."),
    'save_fortitude'   : ('fortbonus', "Fortitude saving throw."),
    'save_reflex'      : ('refbonus', "Reflex saving throw."),
    'save_will'        : ('willbonus', "Will saving throw."),
    'goodevil'         : ('GoodEvil', "Good - Evil"),
    'lawchaos'         : ('LawfulChaotic', "Lawful - Chaotic"),
    'perception_range' : ('PerceptionRange', "Perception Range."),
    'palette_id'       : ('PaletteID', "Palette ID."),

    # Unique to Creature

    'resref'           : ('TemplateResRef', "Resref."),
    'comment'          : ('Comment', "Comment.")

}

LOCSTRING_TABLE = {
    'name_first'  : ('FirstName', "Localized first name"),
    'name_last'   : ('LastName', "Localized last name"),
    'description' : ('Description', "Localized description")
}

class Creature(object):
    """This abstracts over UTCs only... It doesn't handle all the additional
    fields one finds in BICs, see object PlayerCharacter for that.
    """
    def __init__(self, resource, instance=False):
        self._scripts = None
        self._vars = None
        self.is_file = False

        self.is_instance = instance
        if not instance:
            if isinstance(resource, str):
                from resource import ContentObject
                co = ContentObject.from_file(resource)
                self.gff = Gff(co)
                self.is_file = True
            else:
                self.container = resource[1]
                self.gff = Gff(resource[0])
        else:
            self.gff = resource

    def stage(self):
        """Stages changes creature's GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def vars(self):
        """ Variable table """
        if self._vars: return self._vars
        self._vars = NWObjectVarable(self, self.gff)
        return self._vars

    @property
    def scripts(self):
        """Creature's scripts.  Responds to script events:

        * Event.HEARTBEAT
        * Event.PERCEPTION
        * Event.SPELL_CAST_AT
        * Event.ATTACKED
        * Event.DAMAGED
        * Event.DISTURBED
        * Event.END_COMBAT_ROUND
        * Event.CONVERSATION
        * Event.SPAWN
        * Event.REST
        * Event.DEATH
        * Event.USER_DEFINED
        * Event.BLOCKED
        """

        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.HEARTBEAT] = 'ScriptHeartbeat'
        lbls[Event.PERCEPTION] = 'ScriptOnNotice'
        lbls[Event.SPELL_CAST_AT] = 'ScriptSpellAt'
        lbls[Event.ATTACKED] = 'ScriptAttacked'
        lbls[Event.DAMAGED] = 'ScriptDamaged'
        lbls[Event.DISTURBED] = 'ScriptDisturbed'
        lbls[Event.END_COMBAT_ROUND] = 'ScriptEndRound'
        lbls[Event.CONVERSATION] = 'ScriptDialogue'
        lbls[Event.SPAWN] = 'ScriptSpawn'
        lbls[Event.REST] = 'ScriptRested'
        lbls[Event.DEATH] = 'ScriptDeath'
        lbls[Event.USER_DEFINED] = 'ScriptUserDefine'
        lbls[Event.BLOCKED] = 'ScriptOnBlocked'

        self._scripts = NWObjectScripts(self, lbls)

        return self._scripts

    @property
    def skills(self):
        """Creature's skills

        :returns: List of skill ranks in order of skill ID.
        """
        return [sk['Rank'].val for sk in self.gff['SkillList']]

    def get_skill(self, skill):
        return self.gff['SkillList'][skill]['Rank']

    def set_skill(self, skill, value):
        self.gff['SkillList'][skill]['Rank'].val = value
        self.stage()

    @property
    def feats(self):
        """Creature's feats.

        :returns: List of feat IDs.
        """
        return [sk['Feat'].val for sk in self.gff['FeatList']]

    @property
    def special_abilities(self):
        res = []
        for s in self.gff['SpecAbilityList']:
            res.append( (s['Spell'].val,
                         s['SpellFlags'].val,
                         s['SpellCasterLevel'].val) )

        return res

    @property
    def classes(self):
        """Creature's classes.

        :returns: List of tuples containing class ID and level.
        """
        return [(cl['Class'].val, cl['ClassLevel'].val) for cl in self.gff['ClassList']]

    @property
    def items(self):
        """Creature's inventory items.

        :returns: List of RepositoryItems.
        """
        result = []
        i = 0
        try:
            for p in self.gff['ItemList']:
                gff_inst = GffInstance(self.gff, 'ItemList', i)
                st_inst  = RepositoryItem(gff_inst, self)
                result.append(st_inst)
                i += 1
        except KeyError:
            pass

        return result

    @property
    def equips(self):
        """ Creature's equipment list.

        :returns: List of tuples containing equipment ID and resref.
        """
        return [(e['_STRUCT_TYPE_'], e['EquippedRes'])
                for e in self.gff['Equip_ItemList']]

class CreatureInstance(Creature):
    """A creature instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff, parent_obj):
        Creature.__init__(self, gff, True)
        self.is_instance = True
        self.parent_obj = parent_obj

    def stage(self):
        """Stages changes to the creature instances parent object.
        """
        self.parent_obj.stage()

    @property
    def items(self):
        """Creature's inventory items.

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
                st_inst  = ItemInstance(gff_inst, self.parent_obj)
                repo_pos = (p['Repos_PosX'], p['Repos_Posy'])
                result.append((repo_pos, st_inst))
                i += 1
        except KeyError:
            pass

        return result

    @property
    def equips(self):
        """ Creature's equipment list.

        :returns: List of tuples containing equipment ID and ItemInstance.
        """
        result = []
        i = 0
        for p in self.gff['Equip_ItemList']:
            gff_inst = GffInstance(self.gff, 'Equip_ItemList', i)
            st_inst  = ItemInstance(gff_inst, self.parent_obj)

            equip_slot = p['_STRUCT_TYPE_']
            result.append((equip_slot, st_inst))
            i += 1

        return result

for key, val in TRANSLATION_TABLE.items():
    setattr(Creature, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Creature, 'get_'+key, getter)
    setattr(Creature, 'set_'+key, setter)
