from pynwn.gff import Gff

from pynwn.obj.scripts import *
from pynwn.obj.vars import *
from pynwn.obj.locstring import *

from pynwn.obj.item import RepositoryItem

class Store(NWObjectVarable):
    def __init__(self, resref, container, instance=False):
        self._scripts = None
        self._vars = None
        self._locstr = {}

        self.is_instance = instance
        if not instance:
            if resref[-4:] != '.utm':
                resref = resref+'.utm'

            if container.has_file(resref):
                self.gff = container[resref]
                self.gff = Gff(self.gff)
            else:
                raise ValueError("Container does not contain: %s" % resref)
        else:
            self.gff = resref
            self._utm = resref.val

        NWObjectVarable.__init__(self, self.gff)

    def __getattr__(self, name):
        if name == 'utm':
            if not self._utm: self._utm = self.gff.structure
            return self._utm

    def __getitem__(self, name):
        return self.utm[name].val

    @property
    def resref(self):
        return self['ResRef']

    @property
    def name(self):
        if not self._locstr.has_key('name'):
            self._locstr['name'] = LocString(self.are['LocalizedName'])

        return self._locstr['name']

    @property
    def tag(self):
        return self['Tag']

    @propety
    def mark_up(self):
        return self['MarkUp']

    @propety
    def mark_down(self):
        return self['MarkDown']

    @propety
    def black_market(self):
        return self['BlackMarket']

    @propety
    def mark_down_bm(self):
        return self['BM_MarkDown']

    @propety
    def price_id(self):
        return self['IdentifyPrice']

    @propety
    def price_max_buy(self):
        return self['MaxBuyPrice']

    @propety
    def gold(self):
        return self['StoreGold']

    def script(self):
        if self._scripts: return self._scripts

        lbls = {}
        lbls[Event.OPEN] = 'OnOpenStore'
        lbls[Event.CLOSE] = 'OnStoreClosed'

        self._scripts = NWObjectScripts(self.utm, lbls)

        return self._scripts

    @propety
    def will_not_buy(self):
        return [i['BaseItem'] for i in self['WillNotBuy']]

    @propety
    def will_only_buy(self):
        return [i['BaseItem'] for i in self['WillOnlyBuy']]

    @property
    def items(self):
        """items returns a two dimensional array with the format:
        [<store page>][<repository item list>]
        """
        res = []
        for page in self['StoreList']:
            items = []
            try:
                items = [RepositoryItem(i) for i in page['ItemList']]
            except Exception:
                pass

            res.append( items )

        return res

    @propety
    def palette_id(self):
        return self['ID']

    @propety
    def comment(self):
        return self['Comment']

class StoreInstance(Store):
    """A store instance is one placed in an area in the toolset.
    As such it's values are derived from its parent GFF structure.
    """
    def __init__(self, gff):
        Store.__init__(self, gff, None, True)
        self.is_instance = True
