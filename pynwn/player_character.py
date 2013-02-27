from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property

from pynwn.item import RepositoryItem
from pynwn.scripts import *
from pynwn.vars import *

__all__ = ['PlayerCharacter']

# I've decided not to inherit creature or creature instance,
# since neither of them align exactly.  In the former, BIC
# is more like an instance, in the latter tho like an instance
# it is a substructure of another GFF.

TRANSLATION_TABLE = {
    'desc_override'      : ('DescriptionOverr', "Description Override"),
    'is_pc'              : ('IsPC', "Player character flag."),
    'is_dm'              : ('IsDM', "Dungeon Master flag."),
    'tag'                : ('Tag', "Tag"),
    'conversation'       : ('Conversation', "Dialog resref."),
    'gender'             : ('Gender', "Gender."),
    'race'               : ('Race', "Racial Type"),
    'subrace'            : ('Subrace', "Subrace."),
    'starting_package'   : ('StartingPackage', "Starting package ID."),
    'diety'              : ('Deity', "Deity"),
    'save_fortitude'     : ('fortbonus', "Fortitude saving throw."),
    'save_reflex'        : ('refbonus', "Reflex saving throw."),
    'save_will'          : ('willbonus', "Will saving throw."),

    # Left some out.

    'strength'           : ('Str', "Creature's strength."),
    'dexterity'          : ('Dex', "Creature's dexterity."),
    'constitution'       : ('Con', "Creature's constitution."),
    'intelligence'       : ('Int', "Creature's intelligence."),
    'wisdom'             : ('Wis', "Creature's wisdom."),
    'natural_ac'         : ('NaturalAC', "Natural AC."),
    'plot'               : ('Plot', "Plot flag."),
    'no_perm_death'      : ('NoPermDeath', "No permenant death flag."),
    'disarmable'         : ('Disarmable', "Disarmable flag."),
    'bodybag'            : ('BodyBag', "Body bag."),
    'hp'                 : ('HitPoints', "HP."),
    'hp_current'         : ('CurrentHitPoints', "Current hitpoints."),
    'hp_max'             : ('MaxHitPoints', "Maximum hitpoints."),
    'hp_pregame_current' : ('PregameCurrent', "Pregame current hitpoints."),
    'experience'         : ('Experience', "Experience."),
    'movement_rate'      : ('MovementRate', "Movement rate."),
    'portrait'           : ('Portrait', "Portrait resref."),
    'portrait_id'        : ('PortraitId', "Portrait ID."),
    'goodevil'           : ('GoodEvil', "Good - Evil"),
    'lawchaos'           : ('LawfulChaotic', "Lawful - Chaotic"),
    #Skin colors
    'phenotype'          : ('Phenotype', "Phenotype ID."),
    'appearance'         : ('Appearance_Type', "Appearance ID."),
    'appearance_head'    : ('Appearance_Head', "Head appearance ID."),
    'tail'               : ('Tail_New', "Tail ID."),
    'wings'              : ('Wings_New', "Wings ID."),
    'faction'            : ('FactionID', "Faction ID."),
    'cr'                 : ('ChallengeRating', "Challenge Rating"),
    # Body parts, Class list, level stat list
    'skillpoints'        : ('SkillPoints', "Skill points."),
    # skill, feat list, combat info
    'detect_mode'        : ('DetectMode', "Detect mode."),
    'stealth_mode'       : ('StealthMode', "Stealth mode."),
    'master'             : ('MasterID', "Master object ID."),
    'size'               : ('CreatureSize', "Size."),
    'is_immortal'        : ('IsImmortal', "Immortal flag."),
    'is_destroyable'     : ('IsDestroyable', "Destroyable flag."),
    'is_raisable'        : ('IsRaiseable', "Raisable flag."),
    'dead_selectable'    : ('DeadSelectable', "Selectable when dead flag."),
    'is_commandable'     : ('IsCommandable', "Commandable flag."),
    'is_immortal'        : ('IsImmortal', "Immortal flag."),
    'lootable'           : ('Lootable', "Lootable."),
    'corpse_decay'       : ('DecayTime', "Corpse decay time."),
}

LOCSTRING_TABLE = {
    'name_first'  : ('FirstName', "Localized first name"),
    'name_last'   : ('LastName', "Localized last name"),
    'description' : ('Description', "Localized description")
}

class PlayerCharacter( object ):
    def __init__(self, resref, container):
        self._scripts = None

        if resref[-4:] != '.bic':
            resref = resref+'.bic'

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

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(PlayerCharacter, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(PlayerCharacter, 'get_'+key, getter)
    setattr(PlayerCharacter, 'set_'+key, setter)
