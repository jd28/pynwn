from pynwn.file.gff import Gff

class QuestEntry(object):
    def __init__(self, gff):
        self.gff = gff

    @property
    def end(self):
        return self.gff['End']

    @property
    def id(self):
        return self.gff['ID']

    @property
    def text(self):
        if 'text' not in self._locstr:
            self._locstr['text'] = LocString(self.gff['Text'])

        return self._locstr['text']

class JournalQuest(object):
    def __init__(self, gff):
        self.gff = gff

    @property
    def comment(self):
        return self.gff['Comment']

    @property
    def entries(self):
        return [QuestEntry(e) for e in self.gff['EntryList']]

    @property
    def name(self):
        if 'name' not in self._locstr:
            self._locstr['name'] = LocString(self.gff['Name'])

        return self._locstr['name']

    @property
    def picture(self):
        return self.gff['Picture']

    @property
    def priority(self):
        return self.gff['Priority']

    @property
    def tag(self):
        return self.gff['tag']

    @property
    def xp(self):
        return self.gff['XP']

class Journal(object):
    """ There is only one journal file.
    """
    def __init__(self, resref, container):
        if resref[-4:] != '.jrl':
            resref = resref+'.jrl'

        if container.has_file(resref):
            self.gff = container[resref]
            self.gff = Gff(self.gff)
        else:
            raise ValueError("Container does not contain: %s" % resref)

    def __getitem__(self, name):
        for c in self.jrl['Categories']:
            if c['Tag'] == name:
                return JournalQuest(c)

    @property
    def quests(self):
        return [JournalQuest(c) for c in self.jrl['Categories']]
