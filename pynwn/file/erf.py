import pynwn.resource as res
import datetime
import struct
from pynwn.util.helper import chunks

VALID_TYPES = ['ERF', 'HAK', 'MOD']

class Erf(res.Container):
    """Reads/Writes NWN ERF formats: erf, hak, and mod.
    """

    def __init__(self, io):
        super(Erf, self).__init__()

        self.io = io
        self.localized_strings = {}
        self.ftype, self.fversion = "ERF", "V1.0"
        self.desc_strref = 0xffffffff

        now = datetime.datetime.now()
        self.year = now.year - 1900
        self.day_of_year = now.timetuple().tm_yday

    def save(self):
        self.pre_save()

        if self.has_modified_content_objects():
            with open(self.io, 'rb+') as f:
                self.write_to(f)

    # Note about the following... Python doesn't seem to auto-pad strings in the way that
    # ruby does, nor strip trailing NULLs... so this is a little less nice than it should
    # be
    def write_to(self, io):
        """Writes ERF file to file handle.

        :param io: A file handle.

        """
        fnlen = Erf.filename_length(self.fversion)
        lstr_iter = iter(sorted(self.localized_strings.iteritems()))
        locstr = []
        for k, v in lstr_iter:
            locstr.append(struct.pack("<L L %ds x" % len(v), k, len(v)+1, v))
        locstr = ''.join(locstr)

        keylist = []
        for i, co in enumerate(self.content):
            pad = 0
            max = len(co.resref)
            if len(co.resref) > fnlen:
                print "truncating filename %s, longer than %d" % (co.resref, fnlen)
                max = fnlen
            else:
                pad = fnlen - len(co.resref)

            keylist.append(struct.pack("<%ds %dx L h h" % (len(co.resref), pad), co.resref, i, co.res_type, 0))
        keylist = ''.join(keylist)

        offset = 160 + len(locstr) + len(keylist) + 8 * len(self.content)

        reslist = []
        for co in self.content:
            reslist.append(struct.pack("< L L", offset, co.size))
            offset += co.size

        reslist = ''.join(reslist)

        offset_to_locstr = 160
        offset_to_keylist = offset_to_locstr + len(locstr)
        offset_to_resourcelist = offset_to_keylist + len(keylist)

        header = struct.pack("8s LL LL LL LL L 116x", self.ftype+' '+ self.fversion, len(self.localized_strings),
                             len(locstr), len(self.content), offset_to_locstr, offset_to_keylist,
                             offset_to_resourcelist, self.year, self.day_of_year, self.desc_strref)

        io.write(header)
        io.write(locstr)
        io.write(keylist)
        io.write(reslist)

        for co in self.content:
            io.write(co.get())

    @staticmethod
    def from_file(fname):
        """Create an Erf from a file handle.

        :param io: A file handle.

        """
        with open(fname, 'rb') as io:
            new_erf = Erf(fname)

            header = io.read(160)
            hs = struct.unpack("< 4s 4s LL LL LL LL L 116s", header)

            ftype = hs[0].strip()
            if not ftype in VALID_TYPES: raise ValueError("Invalid file type!")
            new_erf.ftype = ftype

            fname_len = Erf.filename_length(hs[1])
            new_erf.fversion = hs[1]

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
                    print "locstr table: not enough entries (expected: %d, got: %d)" % (lstr_count, ls)
                    break

                if len(lstr) < 8:
                    print "locstr table: not enough entries (expected: %d, got: %d)" % (lstr_count, ls) + " partial data: " + lstr
                    break

                lid, strsz = struct.unpack("<L L", lstr[:8])
                if strsz > len(lstr) - 8:
                    strsz = len(lstr) - 8

                # Temporary hack around the fact that the erf.exe adds an extra null to the end of
                # the description string.
                fubar = """Created by "erf", the command-line ERF utility.\nCopyright (C) 2003-2009, Gareth Hughes and Doug Swarin"""
                if fubar in lstr:
                    strsz += 1

                str = struct.unpack("8x %ds" % strsz, lstr)[0] #

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
                co = res.ContentObject(resref.rstrip(' \t\r\n\0'), res_type, fname)
                new_erf.add(co)

            resourcelist_entry_size = 4 + 4
            io.seek(offset_to_res)
            resourcelist = io.read(resourcelist_entry_size * entry_count)
            resourcelist = struct.unpack("I I" * entry_count, resourcelist)
            _index = -1
            for offset, size in chunks(resourcelist, 2):
                _index += 1
                co = new_erf[_index]
                co.offset = offset
                co.size = size

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
