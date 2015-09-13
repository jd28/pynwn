import datetime, os, struct, shutil, sys, tempfile, re

import pynwn.resource as res
from pynwn.util import chunks, get_encoding

class Erf(res.Container):
    """Reads/Writes NWN ERF formats: erf, hak, and mod.
    """

    TYPES = ['ERF', 'HAK', 'MOD']
    VERSIONS = ['V1.0', 'V1.1']

    def __init__(self, erf_type, version='V1.0'):
        super(Erf, self).__init__()
        assert(erf_type in self.TYPES)
        assert(version in self.VERSIONS)
        self.localized_strings = {}
        self.ftype = erf_type
        self.fversion = version
        self.desc_strref = 0xffffffff

        now = datetime.datetime.now()
        self.year = now.year - 1900
        self.day_of_year = now.timetuple().tm_yday

    def save(self):
        self.pre_save()

        if self.has_modified_content_objects():
            self.write_to(self.io)

    def description(self, lang=0):
        """Gets description, by language.

        :param lang: See Bioware's TLK language constants.
        """
        if not lang in self.localized_strings: return ""
        return self.localized_strings[lang]

    def set_description(self, text, lang=0):
        """Sets description, by language.

        :param text: New description.
        :param lang: See Bioware's TLK language constants.
        """
        self.localized_strings[lang] = text

    def add_file(self, file):
        basename = os.path.basename(file)
        basename, ext = os.path.splitext(basename)
        ext = ext[1:].lower()
        fnlen = Erf.filename_length(self.fversion)
        if len(basename) > fnlen:
            raise ValueError("Error: Unable to add file '%s', it is too long!" % file)
        elif re.match('^[a-zA-Z0-9_]+$', basename) is None:
            raise ValueError("Error: Unable to add file '%s', invalid resref!" % file)

        res.Container.add_file(self, file)

    # Note about the following... Python doesn't seem to auto-pad strings in the way that
    # ruby does, nor strip trailing NULLs... so this is a little less nice than it should
    # be
    def write_to(self, io):
        """Writes ERF to file.

        :param io: A file path.
        """
        out = io
        io, path = tempfile.mkstemp()
        fnlen = Erf.filename_length(self.fversion)
        lstr_iter = iter(sorted(self.localized_strings.items()))
        locstr = []
        for k, v in lstr_iter:
            locstr.append(struct.pack("<L L %ds x" % len(v), k, len(v)+1, v.encode(get_encoding())))
        locstr = b''.join(locstr)

        keylist = []
        for i, co in enumerate(self.content):
            pad = 0
            max = len(co.resref)
            if len(co.resref) > fnlen:
                print("truncating filename %s, longer than %d" % (co.resref, fnlen), file=sys.stderr)
                max = fnlen
            else:
                pad = fnlen - len(co.resref)

            keylist.append(struct.pack("<%ds %dx L h h" % (len(co.resref), pad),
                                       co.resref.encode(get_encoding()),
                                       i, co.res_type, 0))
        keylist = b''.join(keylist)

        offset = 160 + len(locstr) + len(keylist) + 8 * len(self.content)

        reslist = []
        for co in self.content:
            reslist.append(struct.pack("< L L", offset, co.size))
            offset += co.size

        reslist = b''.join(reslist)

        offset_to_locstr = 160
        offset_to_keylist = offset_to_locstr + len(locstr)
        offset_to_resourcelist = offset_to_keylist + len(keylist)

        header = struct.pack("8s LL LL LL LL L 116x",
                             (self.ftype+' '+self.fversion).encode(get_encoding()),
                              len(self.localized_strings),
                             len(locstr), len(self.content), offset_to_locstr, offset_to_keylist,
                             offset_to_resourcelist, self.year, self.day_of_year, self.desc_strref)

        os.write(io, header)
        os.write(io, locstr)
        os.write(io, keylist)
        os.write(io, reslist)

        for co in self.content:
            os.write(io, co.get())

        os.close(io)
        shutil.copy(path, out)
        os.remove(path)

    @staticmethod
    def from_file(fname):
        """Create an Erf from a file handle.

        :param io: A file handle.

        """
        with open(fname, 'rb') as io:
            header = io.read(160)
            hs = struct.unpack("< 4s 4s LL LL LL LL L 116s", header)

            ftype = hs[0].decode(get_encoding()).strip()
            if not ftype in Erf.TYPES: raise ValueError("Invalid file type!")

            fvers = hs[1].decode(get_encoding())
            fname_len = Erf.filename_length(fvers)

            new_erf = Erf(ftype, fvers)
            new_erf.io = fname

            lstr_count = hs[2]
            lstr_size = hs[3]
            entry_count = hs[4]
            offset_to_lstr = hs[5]
            offset_to_keys = hs[6]
            offset_to_res = hs[7]
            new_erf.year = hs[8]
            new_erf.day_of_year = hs[9]
            new_erf.desc_strref = hs[10]

            io.seek(offset_to_lstr)
            lstr = io.read(lstr_size)

            for ls in range(lstr_count):
                if len(lstr) == 0:
                    print("locstr table: not enough entries (expected: %d, got: %d)" % (lstr_count, ls), file=sys.stderr)
                    break

                if len(lstr) < 8:
                    print("locstr table: not enough entries (expected: %d, got: %d)" % (lstr_count, ls) + " partial data: " + lstr, file=sys.stderr)
                    break

                lid, strsz = struct.unpack("<L L", lstr[:8])
                if strsz > len(lstr) - 8:
                    strsz = len(lstr) - 8

                # Necessary for hacking around the fact that erf.exe adds an extra null
                # to the end of the description string.
                try:
                    str = struct.unpack("8x %ds" % strsz, lstr)[0].decode(get_encoding()) #
                except struct.error as e:
                    str = struct.unpack("8x %ds" % (strsz + 1,), lstr)[0].decode(get_encoding()) #

                new_erf.localized_strings[lid] = str.rstrip(' \t\r\n\0')
                lstr = lstr[8 + len(str):]

            keylist_entry_size = fname_len + 4 + 2 + 2
            io.seek(offset_to_keys)
            keylist = io.read(keylist_entry_size * entry_count)

            fmt = "%ds I h h" % fname_len
            fmt = fmt * entry_count
            fmt = '<' + fmt

            keylist = struct.unpack(fmt, keylist)

            for resref, res_id, res_type, unused in chunks(keylist, 4):
                co = res.ContentObject(resref.decode(get_encoding()).rstrip(' \t\r\n\0'),
                                       res_type, fname)
                new_erf.add(co)

            resourcelist_entry_size = 4 + 4
            io.seek(offset_to_res)
            resourcelist = io.read(resourcelist_entry_size * entry_count)
            resourcelist = struct.unpack("I I" * entry_count, resourcelist)
            _index = -1
            for offset, size in chunks(resourcelist, 2):
                _index += 1
                try:
                    co = new_erf.content[_index]
                    co.offset = offset
                    co.size = size
                except IndexError as e:
                    print("WARNING: Attempt to index invalid content object in '%s' at offset %X" % (fname, offset), file=sys.stderr)

        return new_erf

    @staticmethod
    def filename_length(version):
        """Determine maximum ResRef length.

        :param version: ERF version. Only "V1.0" and "V1.1" are valid parameters.
        :type name: str.

        """
        if version == "V1.0":
            return 16
        elif version == "V1.1":
            return 32
        else:
            raise ValueError("Invalid ERF Version: %s" % version)
