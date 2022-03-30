from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property
from pynwn.file.gff import GffInstance

from pynwn.item import RepositoryItem, ItemInstance

__all__ = ['PlayerCharacter']

# I've decided not to inherit creature or creature instance,
# since neither of them align exactly.  In the former, BIC
# is more like an instance, in the latter tho like an instance
# it is a substructure of another GFF.

TRANSLATION_TABLE = {
    'desc_override': ('DescriptionOverr', "Description Override"),
    'is_pc': ('IsPC', "Player character flag."),
    'is_dm': ('IsDM', "Dungeon Master flag."),
    'tag': ('Tag', "Tag"),
    'conversation': ('Conversation', "Dialog resref."),
    'gender': ('Gender', "Gender."),
    'race': ('Race', "Racial Type"),
    'subrace': ('Subrace', "Subrace."),
    'starting_package': ('StartingPackage', "Starting package ID."),
    'diety': ('Deity', "Deity"),
    'save_fortitude': ('fortbonus', "Fortitude saving throw."),
    'save_reflex': ('refbonus', "Reflex saving throw."),
    'save_will': ('willbonus', "Will saving throw."),

    # Left some out.

    'strength': ('Str', "Creature's strength."),
    'dexterity': ('Dex', "Creature's dexterity."),
    'constitution': ('Con', "Creature's constitution."),
    'intelligence': ('Int', "Creature's intelligence."),
    'wisdom': ('Wis', "Creature's wisdom."),
    'charisma': ('Cha', "Creature's charisma."),
    'natural_ac': ('NaturalAC', "Natural AC."),
    'plot': ('Plot', "Plot flag."),
    'no_perm_death': ('NoPermDeath', "No permenant death flag."),
    'disarmable': ('Disarmable', "Disarmable flag."),
    'bodybag': ('BodyBag', "Body bag."),
    'hp': ('HitPoints', "HP."),
    'hp_current': ('CurrentHitPoints', "Current hitpoints."),
    'hp_max': ('MaxHitPoints', "Maximum hitpoints."),
    'hp_pregame_current': ('PregameCurrent', "Pregame current hitpoints."),
    'experience': ('Experience', "Experience."),
    'movement_rate': ('MovementRate', "Movement rate."),
    'portrait': ('Portrait', "Portrait resref."),
    'portrait_id': ('PortraitId', "Portrait ID."),
    'goodevil': ('GoodEvil', "Good - Evil"),
    'lawchaos': ('LawfulChaotic', "Lawful - Chaotic"),
    # Skin colors
    'phenotype': ('Phenotype', "Phenotype ID."),
    'appearance': ('Appearance_Type', "Appearance ID."),
    'appearance_head': ('Appearance_Head', "Head appearance ID."),
    'tail': ('Tail_New', "Tail ID."),
    'wings': ('Wings_New', "Wings ID."),
    'faction': ('FactionID', "Faction ID."),
    'cr': ('ChallengeRating', "Challenge Rating"),
    # Body parts, Class list, level stat list
    'skillpoints': ('SkillPoints', "Skill points."),
    # skill, feat list, combat info
    'detect_mode': ('DetectMode', "Detect mode."),
    'stealth_mode': ('StealthMode', "Stealth mode."),
    'master': ('MasterID', "Master object ID."),
    'size': ('CreatureSize', "Size."),
    'is_immortal': ('IsImmortal', "Immortal flag."),
    'is_destroyable': ('IsDestroyable', "Destroyable flag."),
    'is_raisable': ('IsRaiseable', "Raisable flag."),
    'dead_selectable': ('DeadSelectable', "Selectable when dead flag."),
    'is_commandable': ('IsCommandable', "Commandable flag."),
    'lootable': ('Lootable', "Lootable."),
    'corpse_decay': ('DecayTime', "Corpse decay time."),
}

LOCSTRING_TABLE = {
    'name_first': ('FirstName', "Localized first name"),
    'name_last': ('LastName', "Localized last name"),
    'description': ('Description', "Localized description")
}


class LevelStats(object):
    def __init__(self):
        self.hitdice = None
        self.class_type = None
        self.epic_level = None
        self.skills = []
        self.feats = []


class PlayerCharacter(object):
    def __init__(self, resref, container):
        self._scripts = None

        if resref[-4:] != '.bic':
            resref += '.bic'

        self.container = container
        if container.has_file(resref):
            self.gff = container[resref]
            self.gff = Gff(self.gff)
        else:
            raise ValueError("Container does not contain: %s" % resref)

    def stage(self):
        """ Stage changes to the placeable's GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def equips(self):
        """ Creature's equipment list.

        :returns: List of tuples containing equipment ID and ItemInstance.
        """
        result = []
        i = 0
        for p in self.gff['Equip_ItemList']:
            gff_inst = GffInstance(self.gff, 'Equip_ItemList', i)
            st_inst = ItemInstance(gff_inst, self)

            equip_slot = p['_STRUCT_TYPE_']
            result.append((equip_slot, st_inst))
            i += 1

        return result

    @property
    def items(self):
        """Creature's inventory items.

        :returns: List of tuples contiain repository position
                  and the :class:`pynwn.ItemInstance`.
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
    def level_stats(self):
        """ Player's level stat list.
        """
        result = []
        for p in self.gff['LvlStatList']:
            ls = LevelStats()
            ls.class_type = p['LvlStatClass'].value
            ls.hitdice = p['LvlStatHitDie'].value
            ls.epic_level = p['EpicLevel'].value
            ls.skillpoints = p['SkillPoints'].value

            for sk in p['SkillList']:
                ls.skills.append(sk['Rank'].value)

            for ft in p['FeatList']:
                ls.feats.append(ft['Feat'].value)

            result.append(ls)
        return result


for key, val in TRANSLATION_TABLE.items():
    setattr(PlayerCharacter, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(PlayerCharacter, 'get_' + key, getter)
    setattr(PlayerCharacter, 'set_' + key, setter)
