from pynwn.file.gff import Gff

class Faction(object):
    def __init__(self, resource):
        self.is_file = False

        if isinstance(resource, str):
            from resource import ContentObject
            co = ContentObject.from_file(resource)
            self.gff = Gff(co)
            self.is_file = True
        else:
            self.container = resource[1]
            self.gff = Gff(resource[0])

    def stage(self):
        """Stages changes to GFF structure.
        """
        if self.gff.is_loaded():
            self.container.add_to_saves(self.gff)

    @property
    def factions(self):
        res = []
        for f in self.gff['FactionList']:
            res.append( (f['FactionParentID'],
                         f['FactionName'],
                         f['FactionGlobal']) )

        return res

    @property
    def reputations(self):
        res = []
        for f in self.gff['RepList']:
            res.append( (f['FactionID1'],
                         f['FactionID2'],
                         f['FactionRep']) )

        return res
