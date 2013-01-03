from pynwn.helper import enum

Event = enum('ATTACKED',
             'BLOCKED',
             'CLICK',
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
             'PERCEPTION',
             'RESPAWN',
             'REST',
             'SPAWN',
             'SPELL_CAST_AT',
             'TRAP_DISARMED',
             'TRAP_TRIGGERED',
             'USED',
             'USER_DEFINED')

class NWObjectScripts:
    def __init__(self, gff_struct, label_map):
        self.gff = gff_struct
        self.map = label_map

    def __getitem__(self, label):
        return self.gff[self.map[label]]
