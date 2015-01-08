import fnmatch, os
import io

from itertools import chain
from pynwn.file.tlk import TlkTable

Extensions = {
    'res': 0,
    'bmp': 1,
    'mve': 2,
    'tga': 3,
    'wav': 4,
    'wfx': 5,
    'plt': 6,
    'ini': 7,
    'mp3': 8,
    'mpg': 9,
    'txt': 10,
    'plh': 2000,
    'tex': 2001,
    'mdl': 2002,
    'thg': 2003,
    'fnt': 2005,
    'lua': 2007,
    'slt': 2008,
    'nss': 2009,
    'ncs': 2010,
    'mod': 2011,
    'are': 2012,
    'set': 2013,
    'ifo': 2014,
    'bic': 2015,
    'wok': 2016,
    '2da': 2017,
    'tlk': 2018,
    'txi': 2022,
    'git': 2023,
    'bti': 2024,
    'uti': 2025,
    'btc': 2026,
    'utc': 2027,
    'dlg': 2029,
    'itp': 2030,
    'btt': 2031,
    'utt': 2032,
    'dds': 2033,
    'bts': 2034,
    'uts': 2035,
    'ltr': 2036,
    'gff': 2037,
    'fac': 2038,
    'bte': 2039,
    'ute': 2040,
    'btd': 2041,
    'utd': 2042,
    'btp': 2043,
    'utp': 2044,
    'dft': 2045,
    'gic': 2046,
    'gui': 2047,
    'css': 2048,
    'ccs': 2049,
    'btm': 2050,
    'utm': 2051,
    'dwk': 2052,
    'pwk': 2053,
    'btg': 2054,
    'utg': 2055,
    'jrl': 2056,
    'sav': 2057,
    'utw': 2058,
    '4pc': 2059,
    'ssf': 2060,
    'hak': 2061,
    'nwm': 2062,
    'bik': 2063,
    'ndb': 2064,
    'ptm': 2065,
    'ptt': 2066,
    'bak': 2067,
    'osc': 3000,
    'usc': 3001,
    'trn': 3002,
    'utr': 3003,
    'uen': 3004,
    'ult': 3005,
    'sef': 3006,
    'pfx': 3007,
    'cam': 3008,
    'lfx': 3009,
    'bfx': 3010,
    'upe': 3011,
    'ros': 3012,
    'rst': 3013,
    'ifx': 3014,
    'pfb': 3015,
    'zip': 3016,
    'wmp': 3017,
    'bbx': 3018,
    'tfx': 3019,
    'wlk': 3020,
    'xml': 3021,
    'scc': 3022,
    'ptx': 3033,
    'ltx': 3034,
    'trx': 3035,
    'mdb': 4000,
    'mda': 4001,
    'spt': 4002,
    'gr2': 4003,
    'fxa': 4004,
    'fxe': 4005,
    'jpg': 4007,
    'pwc': 4008,

    #custom
    '2dx': 4009,

    'ids': 9996,
    'erf': 9997,
    'bif': 9998,
    'key': 9999,
}

ResTypes = {
    0: 'res',
    1: 'bmp',
    2: 'mve',
    3: 'tga',
    4: 'wav',
    5: 'wfx',
    6: 'plt',
    7: 'ini',
    8: 'mp3',
    9: 'mpg',
    10: 'txt',
    2000: 'plh',
    2001: 'tex',
    2002: 'mdl',
    2003: 'thg',
    2005: 'fnt',
    2007: 'lua',
    2008: 'slt',
    2009: 'nss',
    2010: 'ncs',
    2011: 'mod',
    2012: 'are',
    2013: 'set',
    2014: 'ifo',
    2015: 'bic',
    2016: 'wok',
    2017: '2da',
    2018: 'tlk',
    2022: 'txi',
    2023: 'git',
    2024: 'bti',
    2025: 'uti',
    2026: 'btc',
    2027: 'utc',
    2029: 'dlg',
    2030: 'itp',
    2031: 'btt',
    2032: 'utt',
    2033: 'dds',
    2034: 'bts',
    2035: 'uts',
    2036: 'ltr',
    2037: 'gff',
    2038: 'fac',
    2039: 'bte',
    2040: 'ute',
    2041: 'btd',
    2042: 'utd',
    2043: 'btp',
    2044: 'utp',
    2045: 'dft',
    2046: 'gic',
    2047: 'gui',
    2048: 'css',
    2049: 'ccs',
    2050: 'btm',
    2051: 'utm',
    2052: 'dwk',
    2053: 'pwk',
    2054: 'btg',
    2055: 'utg',
    2056: 'jrl',
    2057: 'sav',
    2058: 'utw',
    2059: '4pc',
    2060: 'ssf',
    2061: 'hak',
    2062: 'nwm',
    2063: 'bik',
    2064: 'ndb',
    2065: 'ptm',
    2066: 'ptt',
    2067: 'bak',
    3000: 'osc',
    3001: 'usc',
    3002: 'trn',
    3003: 'utr',
    3004: 'uen',
    3005: 'ult',
    3006: 'sef',
    3007: 'pfx',
    3008: 'cam',
    3009: 'lfx',
    3010: 'bfx',
    3011: 'upe',
    3012: 'ros',
    3013: 'rst',
    3014: 'ifx',
    3015: 'pfb',
    3016: 'zip',
    3017: 'wmp',
    3018: 'bbx',
    3019: 'tfx',
    3020: 'wlk',
    3021: 'xml',
    3022: 'scc',
    3033: 'ptx',
    3034: 'ltx',
    3035: 'trx',
    4000: 'mdb',
    4001: 'mda',
    4002: 'spt',
    4003: 'gr2',
    4004: 'fxa',
    4005: 'fxe',
    4007: 'jpg',
    4008: 'pwc',

    #custom
    4009: '2dx',

    9996: 'ids',
    9997: 'erf',
    9998: 'bif',
    9999: 'key',
}

class ContentObject(object):
    """A ContentObject is an abstraction of any particular NWN resource object
    either in NWN container (i.e. a hak, mod, or erf) or in a file.

    NOTE: Parameter abspath is ONLY used when the content object is in a DirectoryContainer.  Since
    modifications to content objects are not immediately written to disk, if ``io``
    is changed from a file to cStringIO, it's necessary to know where to write
    the file when DirectoryContainer.save() is called.

    :param resref: Template resref name.
    :param res_type: Resource type.
    :param io: Either a file name or cStringIO.
    :param offset: Data offest in ``io``.
    :param size: Data size.
    :param abspath: Absolute path to the file if one is contained in ``io``.
    """

    def __init__(self, resref, res_type, io = None, offset = None, size=None, abspath=None):
        self.resref = resref.lower()
        if len(self.resref) > 16:
            raise ValueError("Resref of file (%s) is too large!" % self.resref)

        if not res_type in ResTypes:
            raise ValueError("Invalid Resource Type: %d!" % res_type)
        self.res_type = res_type
        self.modified = False
        self.abspath = abspath
        self.io = io
        self.offset = offset or 0
        self.size = size

    def __hash__(self):
        return self.get_filename().__hash__()

    @staticmethod
    def from_file(filename):
        """Instantiates a ContentObject from a file.
        """
        if not os.path.isfile(filename): raise ValueError("%s does not exist!" % filename)

        abspath = os.path.abspath(filename)
        basename = os.path.basename(abspath)
        basename, ext = os.path.splitext(basename)
        if len(basename) > 16:
            raise ValueError("Resref of file (%s) is too large!" % filename)

        ext = ext[1:]
        if not ext in Extensions: raise ValueError("Invalid Resource Type: %s!" % filename)

        size = os.path.getsize(abspath)

        return ContentObject(basename, Extensions[ext], abspath, 0, size, abspath)

    def get(self, mode = 'rb'):
        """Returns the actual data.
        """
        mode = 'rb' if mode is None else mode
        if isinstance(self.io, str):
            with open(self.io, mode) as f:
                f.seek(self.offset)
                return f.read(self.size)
        else:
            return self.io.getvalue()

    def to_io(self):
        if isinstance(self.io, str):
            return io.StringIO(self.get())
        else:
            return io

    def get_extension(self):
        """Determines the ContentObject's file extention by resource
        type.
        """

        return ResTypes[self.res_type]

    def get_filename(self):
        """Determines the ContentObject's base file name: <resref>.<ext>
        """
        return "%s.%s" % (self.resref, self.get_extension())

    def write_to(self, path):
        with open(path, 'wb') as f:
            f.write(self.get())

def construct(co, cont):
    if co.res_type == 2027:
        from pynwn.creature import Creature
        return Creature((co, cont))
    elif co.res_type == 2025:
        from pynwn.item import Item
        return Item((co, cont))
    elif co.res_type == 2042:
        from pynwn.door import Door
        return Door((co, cont))
    elif co.res_type == 2032:
        from pynwn.trigger import Trigger
        return Trigger((co, cont))
    elif co.res_type == 2035:
        from pynwn.sound import Sound
        return Sound((co, cont))
    elif co.res_type == 2040:
        from pynwn.encounter import Encounter
        return Encounter((co, cont))
    elif co.res_type == 2044:
        from pynwn.placeable import Placeable
        return Placeable((co, cont))
    elif co.res_type == 2051:
        from pynwn.store import Store
        return Store((co, cont))
    elif co.res_type == 2058:
        from pynwn.waypoint import Waypoint
        return Waypoint((co, cont))
    elif co.res_type == 2029:
        from pynwn.dialog import Dialog
        return Dialog((co, cont))

    return None

class Container(object):
    """A basic container for ContentObjects
    """
    def __init__(self):
        self.content = []
        self.filenames = {}
        self.saves = set([])

    def __getitem__(self, name):
        """Get a content object associated with a file name or integer
        index.
        """
        co = None
        if isinstance(name, str):
            if not name in self.filenames:
                raise ValueError("No ContentObject exists for %s" % name)
            co = self.filenames[name]
        elif isinstance(name, int):
            co = self.content[name]

        res = construct(co, self)
        return res if res else co

    def __len__(self):
        return len(self.content)

    def add(self, content_obj):
        """Add a content object to a container.
        """
        self.filenames[content_obj.get_filename()] = content_obj
        self.content.append(content_obj)

    def add_file(self, fname):
        """Add a content object from a file to a container.
        """

        self.add(ContentObject.from_file(fname))

    def add_to_saves(self, obj):
        self.saves.add(obj)

    def pre_save(self):
        for obj in self.saves:
            obj.save()
        saves = set([])

    def has_modified_content_objects(self):
        for co in self.content:
            if co.modified: return True

        return False

    def get_filenames(self):
        """Gets a list of the filenames of all content objects.
        """

        return self.filenames.keys()

    def get_content_data(self, name):
        """Get content object data by file name or integer index
        """
        co = self.get_content_object(name)
        return co.get()

    def get_content_object(self, name):
        co = None
        if isinstance(name, str):
            if not name in self.filenames:
                raise ValueError("No ContentObject exists for %s" % name)
            co = self.filenames[name]
        elif isinstance(name, int):
            co = self.content[name]
        return co


    def glob(self, glob_pattern):
        """Returns a list of objects or content objects for file names matching the glob pattern.
        i.e. Unix shell-style wildcards: \*.utc
        Note: all file names are converted to lowercase.
        """
        return [self[f] for f in fnmatch.filter(self.get_filenames(), glob_pattern.lower())]

    def has_file(self, fname):
        """Determines if container has a content object associated with
        a given filename.
        """
        return fname in self.filenames

class DirectoryContainer(Container):
    """A Container that directly wraps a directory (e.g. override/).

    :param path: Directory path.
    :param only_nwn: default ``True``, If ``False`` the ``DirectoryContainer`` will attempt to load all files,
                     even those that are not NWN resource types.

    """
    def __init__(self, path, only_nwn=True):
        super(DirectoryContainer, self).__init__()
        if not os.path.isdir(path):
            msg = "Path: %s is not a directory!" % path
            raise ValueError(msg)
        self.path = path
        for dirname, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                if not only_nwn or os.path.splitext(filename)[1][1:] in Extensions:
                    self.add_file(os.path.join(dirname, filename))

    def save(self):
        if self.has_modified_content_objects():
            for co in self.content:
                if co.modified:
                    co.write_to(co.abspath)
                    co.modified = False

class ResourceManager(object):
    """A container for Container objects.
    """
    def __init__(self):
        self.containers = []
        self.filenames = None

    def add_container(self, container):
        """Adds a container
        """

        self.containers.append(container)

    def __getitem__(self, fname):
        """Gets a ContentObject by file name.
        The order of search is the order in which add_container was called.
        I.e. the first added will have the highest priority
        """
        for con in self.containers:
            if con.has_file(fname):
                return con[fname]

        raise ValueError("No ContentObject exists for %s" % fname)

    @staticmethod
    def from_module(mod, use_override=False, include_bioware=True, path = "C:\\NeverwinterNights\\NWN\\"):
        """Creates a ResourceManager object from a module or module director.

        :param mod: Path to module or module directory.
        :param use_override: default False, If true the overried directory in ``path`` will be used.
        :param include_bioware: default True, If false Bioware NWN BIF files will not be used.
        :param path: default "C:\\NeverwinterNights\\NWN\\", Path to NWN directory.

        **NOTES:**

        * If a directory is passed in ``mod`` it **must** contain a ``module.ifo`` file.
        * If ``include_bioware`` is ``False``, ``path`` can be any working directory
          that has the same directory stucture as the default NWN installation. I.e.
          hak files are in the subdirectory 'hak', overrides in directory 'override'.
        * When loading the module's HAKs .hak files will attempt to be loaded first.
          If no file exists, then a directory with the ``.hak`` files name will attempt
          to be loaded.


        """
        from pynwn.file.key import Key
        from pynwn.file.erf import Erf
        from pynwn.module import Module as Mod

        mgr = ResourceManager()

        # Override
        if use_override:
            mgr.add_container(DirectoryContainer(os.path.join(path, 'override')))

        # Module
        mgr.module = Mod(mod)
        mgr.add_container(mgr.module.container)

        dialog = os.path.join(path, 'dialog.tlk')
        custom = os.path.join(path, 'tlk', mgr.module.tlk + '.tlk')
        mgr.tlktable = TlkTable(open(dialog, 'rb'),
                                open(custom, 'rb'))

        # All custom haks
        for hak in mgr.module.haks:
            h_path = os.path.join(path, 'hak', hak)
            h_file = h_path + '.hak'
            if os.path.isfile(h_file):
                print("Adding HAK %s..." % (h_file))
                mgr.add_container(Erf.from_file(h_file))
            elif os.path.isdir(h_path):
                mgr.add_container(DirectoryContainer(h_path))
                print("Adding HAK directory %s..." % h_path)
            else:
                print("Error no HAK file or HAK directory found: %s" % hak)


        # First, all the base data files.
        if include_bioware:
            for key in ['xp3.key', 'xp2patch.key', 'xp2.key', 'xp1.key', 'chitin.key']:
                mgr.add_container(Key(os.path.join(path, key), path))

        return mgr


    def has_file(self, fname):
        """Determines if a file exists in one of the containers.
        """
        return fname in self.get_filenames()

    def get_filenames(self):
        """Gets a list of all file names.
        """
        if self.filenames: return self.filenames

        self.filenames = []
        for con in self.containers:
            self.filenames += con.get_filenames()

        return self.filenames

    def get_content_data(self, fname):
        """Gets the contents of a ContentObject that is contained
        in one of the containers.
        """
        return self.get_content_object(fname).get()

    def glob(self, glob_pattern):
        """Returns a list of files matching a glob pattern...
        i.e. Unix shell-style wildcards: \*.utc
        Note: all file names are converted to lowercase.
        """

        # Due to some things being returned as constructed NWN objects
        # and some as ContentObjects...  Probably was a bad idea.
        ugh = {}
        for con in self.containers:
            for co in con.glob(glob_pattern):
                if isinstance(co, ContentObject):
                    if not co.get_filename() in ugh:
                        ugh[co.get_filename()] = co
                elif not co.co.get_filename() in ugh:
                    ugh[co.co.get_filename()] = co

        return ugh.values()

    def creatures(self, glob = None):
        """Returns a list of Creature objects contained in
        all of the resource managers containers."""

        from pynwn.obj.creature import Creature

        glob = glob or '*.utc'
        res = self.glob(glob)

        result = [Creature(x, cont) for cont, xs in res
                  for x in xs]
        return result
