from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property
from pynwn.file.gff import GffInstance

from pynwn.item import RepositoryItem, ItemInstance
from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['Creature', 'CreatureInstance']

TRANSLATION_TABLE = {
    'resref'           : ('TemplateResRef', "Resref."),
    'race'             : ('Race', "Racial Type"),
    'appearance'       : ('Appearance_Type', "Appearance ID."),
    'gender'           : ('Gender', "Gender."),
    'phenotype'        : ('Phenotype', "Phenotype ID."),
    'portrait_id'      : ('PortraitId', "Portrait ID."),
    'tag'              : ('Tag', "Tag"),
    'conversation'     : ('Conversation', "Dialog resref."),
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
    'bodybag'          : ('BodyBag', "Body bag."),
    'starting_package' : ('StartingPackage', "Starting package ID."),
    'corpse_decay'     : ('DecayTime', "Corpse decay time."),
    'strength'         : ('Str', "Creature's strength."),
    'dexterity'        : ('Dex', "Creature's dexterity."),
    'constitution'     : ('Con', "Creature's constitution."),
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
    'cr'               : ('ChallengeRating', "Challenge Rating"),
    'perception_range' : ('PerceptionRange', "Perception Range."),
    'palette_id'       : ('PaletteID', "Palette ID."),
    'comment'          : ('Comment', "Comment.")
}

LOCSTRING_TABLE = {
    'name_first'  : ('FirstName', "Localized first name"),
    'name_last'   : ('LastName', "Localized last name"),
    'description' : ('Description', "Localized description")
}

class Creature(NWObjectVarable):
    """This abstracts over UTCs only... It doesn't handle all the additional
    fields one finds in BICs, see object PlayerCharacter for that.
    """
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utc':
                resref = resref+'.utc'

            if container.has_file(resref):
                self.container = container
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref

        NWObjectVarable.__init__(self, self.gff)

    def stage(self):
        """Stages changes creature's GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

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

        self._scripts = NWObjectScripts(self.gff, lbls)

        return self._scripts

    @property
    def skills(self):
        """Creature's skills

        :returns: List of skill ranks in order of skill ID.
        """
        return [sk['Rank'] for sk in self['SkillList']]

    @property
    def feats(self):
        """Creature's feats.

        :returns: List of feat IDs.
        """
        return [sk['Feat'] for sk in self['FeatList']]

    @property
    def special_abilities(self):
        res = []
        for s in self['SpecAbilityList']:
            res.append( (s['Spell'],
                         s['SpellFlags'],
                         s['SpellCasterLevel']) )

        return res

    @property
    def classes(self):
        """Creature's classes.

        :returns: List of tuples containing class ID and level.
        """
        return [(cl['Class'], cl['ClassLevel']) for cl in self['ClassList']]

    @property
    def items(self):
        """Creature's inventory items.

        :returns: List of RepositoryItems.
        """
        result = []
        i = 0
        for p in self.gff['ItemList']:
            gff_inst = GffInstance(self.gff, 'ItemList', i)
            st_inst  = RepositoryItem(gff_inst, self)
            result.append(st_inst)
            i += 1

        return result

    @property
    def equips(self):
        """ Creature's equipment list.

        :returns: List of tuples containing equipment ID and resref.
        """
        return [(e['_STRUCT_TYPE_'], e['EquippedRes'])
                for e in self['Equip_ItemList']]

class CreatureInstance(Creature):
    """A creature instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff, parent_obj):
        Creature.__init__(self, gff, None, True)
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

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Creature, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Creature, 'get_'+key, getter)
    setattr(Creature, 'set_'+key, setter)
