from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property

from pynwn.scripts import *
from pynwn.vars import *

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

LOCSTRING_TABLE = {
    'name'        : ('LocalizedName', "Localized name."),
}

class Trigger(object):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utt':
                resref = resref+'.utt'

            if container.has_file(resref):
                self.container - container
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref

    def stage(self):
        """Stages changes to GFF structure.
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

        self._scripts = NWObjectScripts(self.gff, lbls)

        return self._scripts

class TriggerInstance(Trigger):
    """A trigger instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff, parent_obj):
        Trigger.__init__(self, gff, None, True)
        self.is_instance = True
        self.parent_obj = parent_obj

    def stage(self):
        """Stages changes to parent GFF structure.
        """
        self.parent_obj.stage()

    @property
    def position(self):
        return (self.gff['XPosition'], self.gff['YPosition'],
                self.gff['ZPosition'])

for key, val in TRANSLATION_TABLE.iteritems():
    setattr(Trigger, key, make_gff_property('gff', val))

for key, val in LOCSTRING_TABLE.iteritems():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(Trigger, 'get_'+key, getter)
    setattr(Trigger, 'set_'+key, setter)
