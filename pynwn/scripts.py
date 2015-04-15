from pynwn.util.helper import enum

Event = enum('ATTACKED',
             'BLOCKED',
             'CLICK',
             'CLOSE',
             'CONVERSATION',
             'CUTSCENE_ABORT',
             'DAMAGED',
             'DEATH',
             'DISTURBED',
             'DYING',
             'END_COMBAT_ROUND',
             'ENTER',
             'EXHAUSTED',
             'EXIT',
             'FAIL_TO_OPEN',
             'HEARTBEAT',
             'ITEM_ACQUIRED',
             'ITEM_ACTIVATED',
             'ITEM_EQUIPPED',
             'ITEM_UNACQUIRED',
             'ITEM_UNEQUIPPED',
             'LEVELUP',
             'LOAD',
             'LOCK',
             'OPEN',
             'PERCEPTION',
             'RESPAWN',
             'REST',
             'SPAWN',
             'SPELL_CAST_AT',
             'TRAP_DISARMED',
             'TRAP_TRIGGERED',
             'UNLOCK',
             'USED',
             'USER_DEFINED')

class NWObjectScripts:
    def __init__(self, obj, label_map, gff = None):
        self.gff = gff or obj.gff
        self.map = label_map
        self.parent = obj

    def __getitem__(self, label):
        return self.gff[self.map[label]]

    def __setitem__(self, label, value):
        self.gff[self.map[label]] = value
        if self.parent:
            self.parent.stage()
