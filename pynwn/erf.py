import resource as res
import datetime
import struct
from helper import chunks

VALID_TYPES = ['ERF', 'HAK', 'MOD']

class Erf(res.Container):
    def __init__(self, io=None):
        super(Erf, self).__init__()
        self.container = res.Container()

        self.localized_strings = {}
        self.io = io
        self.ftype, fversion = "ERF", "V1.0"
        self.desc_strref = 0xffffffff

        now = datetime.datetime.now()
        self.year = now.year - 1900
        self.day_of_year = now.timetuple().tm_yday


    @staticmethod
    def from_io(io):
        new_erf = Erf(io)

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

            str = struct.unpack("8x %ds" % strsz, lstr)[0] #
            if strsz != len(str):
                print "Expected locstr size does not match actual string size"

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
            co = res.ContentObject(resref.rstrip(' \t\r\n\0'), res_type, io)
            new_erf.add(co)

        resourcelist_entry_size = 4 + 4
        io.seek(offset_to_res)
        resourcelist = io.read(resourcelist_entry_size * entry_count)
        resourcelist = struct.unpack("I I" * entry_count, resourcelist)
        _index = -1
        for offset, size in chunks(resourcelist, 2):
            _index += 1
            co = new_erf.get_content_obj(_index)
            co.offset = offset
            co.size = size

        return new_erf

    @staticmethod
    def filename_length(version):
        if version == "V1.0":
            return 16
        elif version == "V1.1":
            return 32
        else:
            raise ValueError("Invalid ERF Version: %s" % version)
