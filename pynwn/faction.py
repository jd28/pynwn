from pynwn.file.gff import Gff

class Faction(object):
    def __init__(self, resref, container):
        if resref[-4:] != '.fac':
            resref = resref+'.fac'

        if container.has_file(resref):
            self.gff = container[resref]
            self.gff = Gff(self.gff)
        else:
            raise ValueError("Container does not contain: %s" % resref)

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
