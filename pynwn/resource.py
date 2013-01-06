import fnmatch, os

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
    9996: 'ids',
    9997: 'erf',
    9998: 'bif',
    9999: 'key',
}

class ContentObject(object):
    """A ContentObject is an abstraction of any particular NWN resource object
    either in NWN container (i.e. a hak, mod, or erf) or in a file.

    """
    def __init__(self, resref, res_type, io = None, offset = None, size=None):
        self.resref = resref.lower()

        if not ResTypes.has_key(res_type):
            raise ValueError("Invalid Resource Type: %d!" % res_type)
        self.res_type = res_type

        self.io = io
        self.offset = offset or 0
        self.size = size

    @staticmethod
    def from_file(filename):
        """Instantiates a ContentObject from a file.
        """
        if not os.path.isfile(filename): raise ValueError("%s does not exist!" % filename)

        abspath = os.path.abspath(filename)
        basename = os.path.basename(abspath)
        basename, ext = os.path.splitext(basename)
        ext = ext[-3:]
        if not Extensions.has_key(ext): raise ValueError("Invalid Resource Type: %s!" % ext)

        size = os.path.getsize(abspath)

        return ContentObject(basename, Extensions[ext], abspath, 0, size)

    def get(self):
        """Returns the actual data.
        """
        with open(self.io, 'rb') as f:
            f.seek(self.offset)
            return f.read(self.size)

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

class Container(object):
    """A basic container for ContentObjects
    """
    def __init__(self):
        self.content = []
        self.filenames = {}

    def __getitem__(self, name):
        """Get a content object associated with a file name or integer
        index.
        """

        if isinstance(name, str):
            if not self.filenames.has_key(name): raise ValueError("No ContentObject exists for %s" % name)
            return self.filenames[name]
        elif isinstance(name, int):
            return self.content[name]

    def add(self, content_obj):
        """Add a content object to a container.
        """
        self.filenames[content_obj.get_filename()] = content_obj
        self.content.append(content_obj)

    def add_file(self, fname):
        """Add a content object from a file to a container.
        """

        self.add(ContentObject.from_file(fname))

    def get_filenames(self):
        """Gets a list of the filenames of all content objects.
        """

        return self.filenames.keys()

    def get_content_data(self, name):
        """Get content object data by file name or integer index
        """
        co = self[name]
        return co.get()

    def glob(self, glob_pattern):
        """Returns a list of files matching a glob pattern...
        i.e. Unix shell-style wildcards: \*.utc
        Note: all file names are converted to lowercase.
        """
        return fnmatch.filter(self.get_filenames(), glob_pattern.lower())

    def has_file(self, fname):
        """Determines if container has a content object associated with
        a given filename.
        """
        return self.filenames.has_key(fname)

class DirectoryContainer(Container):
    """A Container that directly wraps a directory (e.g. override/).
    Does not update on changes - caches the directory entries on initialize.
    """
    def __init__(self, path, only_nwn=True):
        super(DirectoryContainer, self).__init__()
        if not os.path.isdir(path):
            msg = "Path: %s is not a directory!" % path
            raise ValueError(msg)
        self.path = path
        for dirname, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                if not only_nwn or Extensions.has_key(os.path.splitext(filename)[1][1:]):
                    self.add_file(os.path.join(dirname, filename))

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

        result = []
        for con in self.containers:
            result += con.glob(glob_pattern)

        return result
