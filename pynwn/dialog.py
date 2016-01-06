from pynwn.file.gff import Gff, make_gff_property, make_gff_locstring_property
from pynwn.file.gff import GffInstance


class DialogPointer(object):
    """Pointer to dialog node.

    Note that starting node pointers have been combined with
    the general dialog node pointer.  They are limited in a couple ways:

    #. No comments.
    #. They can never be links.

    """

    def __init__(self, gff, pointer_type, parent, is_start=False):
        self.gff = gff
        self.parent = parent
        self.pointer = pointer_type
        self._is_start = is_start

    @property
    def is_start(self):
        """Distinguishes starting node pointers from regular node
        pointers.
        """
        return self._is_start

    def get_node(self, i):
        """Gets a node in the dialog.

        :returns: DialogNode based on pointer type.
        """
        if self.pointer == 'RepliesList':
            return self.parent.replies[i]
        else:
            return self.parent.entries[i]


DIALOG_PTR_TABLE = {
    'script': ('Active', 'Text appears when... script'),
    'index': ('Index', 'Index'),
    'comment': ('Comment', 'Comment'),
    'is_link': ('IsChild', 'Linked flag.'),
    'link_comment': ('LinkComment', 'Link comment.'),
}

for key, val in DIALOG_PTR_TABLE.items():
    setattr(DialogPointer, key, make_gff_property('gff', val))


class DialogNode(object):
    """Node in a dialog.

    These are distinguised internally by their pointer types.
    Entry nodes have reply pointers and vice-versa
    """

    def __init__(self, gff, pointer_type, parent):
        self.gff = gff
        self.pointer = pointer_type
        self.parent = parent

    @property
    def pointers(self):
        """Dialog pointers

        :returns: List of DialogPointers
        """

        result = []
        i = 0
        for p in self.gff[self.pointer]:
            gff_inst = GffInstance(self.gff, self.pointer, i)
            st_inst = DialogPointer(gff_inst, self.pointer, self.parent)
            result.append(st_inst)
            i += 1

        return result

    def stage(self):
        self.parent.stage()


DIALOG_NODE_TABLE = {
    'animation': ('Animation', 'Animation'),
    'animation_loop': ('AnimLoop', 'Animation loop'),
    'comment': ('Comment', 'Comment'),
    'delay': ('Delay', 'Delay'),
    'script': ('Script', 'Action attaken script.'),
    'sound': ('Sound', 'Sound'),
    'speaker': ('Speaker', 'Speaker'),
    'quest': ('Quest', 'Quest'),
}

DIALOG_NODE_LOCSTRINGS = {
    'text': ('Text', 'Text')
}

for key, val in DIALOG_NODE_TABLE.items():
    setattr(DialogNode, key, make_gff_property('gff', val))

for key, val in DIALOG_NODE_LOCSTRINGS.items():
    getter, setter = make_gff_locstring_property('gff', val)
    setattr(getter, '__doc__', val[1])
    setattr(setter, '__doc__', val[1])
    setattr(DialogNode, 'get_' + key, getter)
    setattr(DialogNode, 'set_' + key, setter)


class Dialog(object):
    """Abstracts .dlg GFF files.
    """

    def __init__(self, resource):
        self.is_file = False
        self.reply_cache = None
        self.entry_cache = None

        if isinstance(resource, str):
            from pynwn import ContentObject
            co = ContentObject.from_file(resource)
            self.gff = Gff(co)
            self.is_file = True
        else:
            self.container = resource[1]
            co = resource[0]
            self.gff = Gff(co)

        self._resref = co.resref

    def stage(self):
        """Stages changes to the dialog's GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def resref(self):
        """Resref

        Dialogs don't store their resref internally.
        """
        return self._resref

    @property
    def entries(self):
        """Entries

        :returns: List of DialogNodes
        """
        if self.entry_cache is None:
            result = []
            i = 0
            for p in self.gff['EntryList']:
                gff_inst = GffInstance(self.gff, 'EntryList', i)
                st_inst = DialogNode(gff_inst, 'RepliesList', self)
                result.append(st_inst)
                i += 1
            self.entry_cache = result
        return self.entry_cache

    @property
    def replies(self):
        """Replies

        :returns: List of DialogNodes
        """

        if self.reply_cache is None:
            result = []
            i = 0
            for p in self.gff['ReplyList']:
                gff_inst = GffInstance(self.gff, 'ReplyList', i)
                st_inst = DialogNode(gff_inst, 'EntriesList', self)
                result.append(st_inst)
                i += 1

            self.reply_cache = result

        return self.reply_cache

    @property
    def starts(self):
        """Starts

        These are limited pointers in the entry list to the
        topmost level of dialog in a concersation.

        :returns: List of DialogPointers
        """
        result = []
        i = 0
        for p in self.gff['StartingList']:
            gff_inst = GffInstance(self.gff, 'StartingList', i)
            st_inst = DialogPointer(gff_inst, 'EntriesList', self, True)
            result.append(st_inst)
            i += 1

        return result


DIALOG_TABLE = {
    'delay_entry': ('DelayEntry', 'DelayEntry.'),
    'prevent_zoom': ('PreventZoomIn', 'No zoom flag.'),
    'script_abort': ('EndConverAbort', 'Conversation abort script.'),
    'script_end': ('EndConversation', 'Conversation end script.'),
    'word_count': ('NumWords', 'Word count.'),
}

for key, val in DIALOG_TABLE.items():
    setattr(Dialog, key, make_gff_property('gff', val))
