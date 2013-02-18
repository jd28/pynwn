from pynwn.gff import Gff

from pynwn.obj.item import RepositoryItem

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

class Creature(NWObjectVarable):
    """This abstracts over UTCs only... It doesn't handle all the additional
    fields one finds in BICs
    """
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utc':
                resref = resref+'.utc'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utc = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utc':
            if not self._utc: self._utc = self.gff.structure
            return self._utc

    def __getitem__(self, name):
        return self.utc[name].val

    @property
    def resref(self):
        """Resref."""
        return self['TemplateResRef']

    @property
    def race(self):
        """Race ID."""
        return self['Race']

    @property
    def name_first(self):
        """Localized first name."""
        if not self._locstr.has_key('namef'):
            self._locstr['namef'] = LocString(self['FirstName'])

        return self._locstr['namef']

    @property
    def name_last(self):
        """Localized last name."""
        if not self._locstr.has_key('namel'):
            self._locstr['namel'] = LocString(self['LastName'])

        return self._locstr['namel']

    @property
    def appearance(self):
        """Appearance ID."""
        return self['Appearance_Type']

    @property
    def gender(self):
        """Gender."""
        return self['Gender']

    @property
    def phenotype(self):
        """Phenotype ID."""
        return self['Phenotype']

    @property
    def portrait_id(self):
        """Portrait ID."""
        return self['PortraitId']

    @property
    def description(self):
        """Localized description."""
        if not self._locstr.has_key('desc'):
            self._locstr['desc'] = LocString(self['Description'])

        return self._locstr['desc']

    @property
    def tag(self):
        """Tag."""
        return self['Tag']

    @property
    def conversation(self):
        """Dialog resref."""
        return self['Conversation']

    @property
    def is_pc(self):
        """Player character flag."""
        return self['IsPC']

    @property
    def faction(self):
        """Faction ID."""
        return self['FactionID']

    @property
    def disarmable(self):
        """Disarmable flag."""
        return self['Disarmable']

    @property
    def subrace(self):
        """Subrace."""
        return self['Subrace']

    @property
    def diety(self):
        """Deity."""
        return self['Deity']

    @property
    def wings(self):
        """Wing ID"""
        return self['Wings_New']

    @property
    def tail(self):
        """Tail ID"""
        return self['Tail_New']

    @property
    def soundset(self):
        """Soundset."""
        return self['SoundSetFile']

    @property
    def plot(self):
        """Plot flag."""
        return self['Plot']

    @property
    def is_immortal(self):
        """Immortal flag."""
        return self['IsImmortal']

    @property
    def interruptable(self):
        """Conversation interruptable flag."""
        return self['Interruptable']

    @property
    def lootable(self):
        return self['Lootable']

    @property
    def no_perm_death(self):
        """No permenant death flag."""
        return self['NoPermDeath']

    @property
    def bodybag(self):
        return self['BodyBag']

    @property
    def starting_package(self):
        """Starting package ID."""
        return self['StartingPackage']

    @property
    def corpse_decay(self):
        """Corpse decay time."""
        return self['DecayTime']

    @property
    def strength(self):
        """Creature's strength."""
        return self['Str']

    @property
    def dexterity(self):
        """Creature's dexterity."""
        return self['Dex']

    @property
    def constitution(self):
        """Creature's constitution."""
        return self['Con']

    @property
    def intelligence(self):
        """Creature's intelligence."""
        return self['Int']

    @property
    def wisdom(self):
        """Creature's wisdom."""
        return self['Wis']

    @property
    def charisma(self):
        """Creature's charisma."""
        return self['Cha']

    @property
    def walkrate(self):
        return self['WalkRate']

    @property
    def natural_ac(self):
        """Creature's natural AC."""
        return self['NaturalAC']

    @property
    def hp(self):
        return self['HitPoints']

    @property
    def hp_current(self):
        """Creature's current hitpoints."""
        return self['CurrentHitPoints']

    @property
    def hp_max(self):
        """Creature's maximum hitpoints."""
        return self['MaxHitPoints']

    @property
    def save_fortitude(self):
        """Creature's fortitude saving throw."""
        return self['fortbonus']

    @property
    def save_reflex(self):
        """Creature's reflex saving throw."""
        return self['refbonus']

    @property
    def save_will(self):
        """Creature's will saving throw."""
        return self['willbonus']

    @property
    def goodevil(self):
        return self['GoodEvil']

    @property
    def lawchaos(self):
        return self['LawfulChaotic']

    @property
    def cr(self):
        """Creature's challenge rating."""
        return self['ChallengeRating']

    @property
    def cr_adjust(self):
        """Creature's challenge rating adjustment."""
        return self['CRAdjust']

    @property
    def perception_range(self):
        return self['PerceptionRange']

    @property
    def scripts(self):
        """Creature's scripts.  Responds to script events:

        #. Event.HEARTBEAT
        #. Event.PERCEPTION
        #. Event.SPELL_CAST_AT
        #. Event.ATTACKED
        #. Event.DAMAGED
        #. Event.DISTURBED
        #. Event.END_COMBAT_ROUND
        #. Event.CONVERSATION
        #. Event.SPAWN
        #. Event.REST
        #. Event.DEATH
        #. Event.USER_DEFINED
        #. Event.BLOCKED
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

        self._scripts = NWObjectScripts(self.utc, lbls)

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
            res.append( (s['Spell'], s['SpellFlags'], s['SpellCasterLevel']) )

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
        return [RepositoryItem(i) for i in self['ItemList']]

    @property
    def equips(self):
        """ Creature's equipment list.

        :returns: List of tuples containing equipment ID and resref.
        """
        return [(e.type, e['EquippedRes']) for e in self['Equip_ItemList']]

    @property
    def palette_id(self):
        """Palette ID"""
        return self['PaletteID']

    @property
    def comment(self):
        """Comment"""
        return self['Comment']

class CreatureInstance(Creature):
    """A creature instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Creature.__init__(self, gff, None, True)
        self.is_instance = True
