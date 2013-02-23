from pynwn.file.gff import Gff

class DialogNode(object):
    def __init__(self, gff, pointer_type):
        self.gff = gff
        self.pointer = pointer_type

    @property
    def animation(self):
        return self.gff['Animation']

    @property
    def animation_loop(self):
        return self.gff['AnimLoop']

    @property
    def comment(self):
        return self.gff['Comment']

    @property
    def delay(self):
        return self.gff['Delay']

    @property
    def script(self):
        return self.gff['Script']

    @property
    def sound(self):
        return self.gff['Sound']

    @property
    def speaker(self):
        return self.gff['Speaker']

    @property
    def text(self):
        if not self._locstr.has_key('text'):
            self._locstr['text'] = LocString(self.gff['Text'])

        return self._locstr['text']

    @property
    def quest(self):
        return self.gff['Quest']

    @property
    def pointers(self):
        return [DialogPointer(p, self.pointer) for p in self.gff[self.pointer]]


class DialogPointer(object):
    def __init__(self, gff, pointer_type):
        self.gff = gff
        self.pointer = pointer_type

    @property
    def active(self):
        return self.gff['Active']

    @property
    def index(self):
        return self.gff['Index']

    @property
    def is_child(self):
        return self.gff['IsChild']

    @property
    def link_comment(self):
        return self.gff['LinkComment']

class Dialog(object):
    def __init__(self, resref, container):
        if resref[-4:] != '.dlg':
            resref = resref+'.dlg'

        if container.has_file(resref):
            self.dlg = container[resref]
            self.dlg = Gff(self.dlg)
        else:
            raise ValueError("Container does not contain: %s" % resref)

    @property
    def delay_entry(self):
        return self.dlg['DelayEntry']

    @property
    def delay_entry(self):
        return self.dlg['DelayEntry']

    @property
    def entries(self):
        return [DialogNode(n, 'RepliesList') for n in self.dlg['EntryList']]

    @property
    def prevent_zoom(self):
        return self.dlg['PreventZoomIn']

    @property
    def replies(self):
        return [DialogNode(n, 'EntriesList') for n in self.dlg['ReplyList']]

    @property
    def script_abort(self):
        """Conversation abort script"""
        return self.dlg['EndConverAbort']

    @property
    def script_end(self):
        """Conversation end script"""
        return self.dlg['EndConversation']

    @property
    def starts(self):
        pass

    @property
    def word_count(self):
        """Conversation word count."""
        return self.dlg['NumWords']
