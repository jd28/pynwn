from pynwn.gff import Gff, make_gff_property

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

TRANSLATION_TABLE = {
    'tag'              : ('Tag', "Tag."),
    'resref'           : ('TemplateResRef', "Resref."),
    'key_auto_remove'  : ('AutoRemoveKey', "Auto-remove key flag."),
    'faction'          : ('Faction', "Faction ID."),
    'highlight_height' : ('HighlightHeight', "Cursor."),
    'key_tag'          : ('KeyName', "Key tag."),
    'linked_to'        : ('LinkedTo', "Linked to object tag."),
    'linked_to_flags'  : ('LinkedToFlags', "Linked to flags."),
    'load_screen'      : ('LoadScreenID', "Load screen ID."),
    'portrait_id'      : ('PortraitId', "Portrait ID."),
    'type'             : ('Type', "Type."),
    'trap_detectable'  : ('TrapDetectable', "Trap detectable flag."),
    'trap_detect_dc'   : ('TrapDetectDC', "Trap detect DC."),
    'trap_disarmable'  : ('TrapDisarmable', "Trap disarmable flag."),
    'trap_disarm_dc'   : ('DisarmDC', "Trap disarm DC."),
    'trap_flag'        : ('TrapFlag', "Trap flag."),
    'trap_one_shot'    : ('TrapOneShot', "Trap one shot flag."),
    'trap_type'        : ('TrapType', "Trap type."),
    'paletted_id'      : ('PaletteID', "Palette ID."),
    'comment'          : ('Comment', "Comment."),
}

class Trigger(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utt':
                resref = resref+'.utt'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utt = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utt':
            if not self._utt: self._utt = self.gff.structure
            return self._utt

    @property
    def name(self):
        """Localized name."""
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.utt['LocalizedName'])

        return self._locstr['name']

    @property
    def scripts(self):
        """Scripts.  Responds to script events:

        #. Event.TRAP_DISARMED
        #. Event.TRAP_TRIGGERED
        #. Event.CLICK
        #. Event.HEARTBEAT
        #. Event.ENTER
        #. Event.EXIT
        #. Event.USER_DEFINED
        """
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.TRAP_DISARMED] = 'OnDisarm'
        lbls[Event.TRAP_TRIGGERED] = 'OnTrapTriggered'
        lbls[Event.CLICK] = 'OnClick'
        lbls[Event.HEARTBEAT] = 'ScriptHeartbeat'
        lbls[Event.ENTER] = 'ScriptOnEnter'
        lbls[Event.EXIT] = 'ScriptOnExit'
        lbls[Event.USER_DEFINED] = 'ScriptUserDefine'

        self._scripts = NWObjectScripts(self.utt, lbls)

        return self._scripts

class TriggerInstance(Trigger):
    """A trigger instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Trigger.__init__(self, gff, None, True)
        self.is_instance = True

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Trigger, key, make_gff_property('utt', val))
