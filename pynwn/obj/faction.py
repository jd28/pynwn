from pynwn.gff import Gff

class Faction(object):
    def __init__(self, resref, container):
        if resref[-4:] != '.fac':
            resref = resref+'.fac'

        if container.has_file(resref):
            self.gff = container[resref]
            self.gff = Gff(self.gff)
        else:
            raise ValueError("Container does not contain: %s" % resref)

    def __getattr__(self, name):
        if name == 'fac':
            if not self._fac: self._fac = self.gff.structure
            return self._fac

    def __getitem__(self, name):
        return self.fac[name].val

    @property
    def factions(self):
        res = []
        for f in self['FactionList']:
            res.append( (f['FactionParentID'], f['FactionName'], f['FactionGlobal']) )

        return res
    
    @property
    def reputations(self):
        res = []
        for f in self['RepList']:
            res.append( (f['FactionID1'], f['FactionID2'], f['FactionRep']) )

        return res
