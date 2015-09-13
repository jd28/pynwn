import struct, os, sys

import pynwn.resource as res
from pynwn.util.helper import chunks, get_encoding

class Bif:
    """ Bif.
    """

    def __init__(self, key, io):
        # The Key object this Bif belongs to.
        self.key = key

        # Path to .bif file.
        self.io = io

        # A hash containing the resources contained. Usually not needed,
        # accessed by the encapsulating Key object.
        self.contained = {}

        with open(self.io, 'rb') as f:
            header = f.read(4 + 4 + 3 * 4)
            hs = struct.unpack("<4s 4s L L L", header)

            self.file_type = hs[0]
            self.file_version = hs[1]
            self.var_res_count = hs[2]
            self.fix_res_count = hs[3]
            self.var_table_offset = hs[4]

            f.seek(self.var_table_offset)
            data = f.read(self.var_res_count * 16)

            for c in chunks(data, 16):
                if len(c) != 16: break

                rid, offset, size, restype = struct.unpack("<L L L L", c)
                rid &= 0xfffff
                self.contained[rid] = (offset, size, restype)

    def __getitem__(self, id):
        with open(self.io, 'rb') as f:
            offset, size, restype = self.contained[id]
            f.seek(offset)
            return f.read(size)

    def has_res(self, id):
        """Determine if Bif contains a resource by an resoure ID.

        :param id: A resource ID.
        :type id: int

        """
        return id in self.contained

class Key(res.Container):
    """...

    :param io: File handle.
    :param data_path: Path to your NWN installation directory.  e.g: C:/NeverwinterNights/NWN/
    """
    def __init__(self, fname, data_path):
        super(Key, self).__init__()

        self.root = data_path
        self.bif = []

        with open(fname, 'rb') as io:
            header = io.read(8 + (4 * 6) + 32)
            hs = struct.unpack("<4s 4s LLLLLL 32s", header)

            self.ftype = hs[0]
            self.fvers = hs[1]

            bif_count = hs[2]
            key_count = hs[3]
            offset_to_file_table = hs[4]
            offset_to_key_table = hs[5]

            self.year = hs[6]
            self.day_of_year = hs[7]
            reserved = hs[8]

            io.seek(offset_to_file_table)
            data = io.read(12 * bif_count)

            self.file_table = []
            for c in chunks(data, 12):
                if len(c) != 12: break

                size, name_offset, name_size, drives = struct.unpack("LLhh", c)
                io.seek(name_offset)
                name = io.read(name_size)
                name = struct.unpack("%ds" % name_size, name)[0]
                name = name.decode(get_encoding())
                name = name.rstrip(' \t\r\n\0')
                name = os.path.join(self.root, name.replace('\\', os.sep))
                name = os.path.abspath(name)
                self.bif.append( Bif(self, name) )
                self.file_table.append((size, name, drives))

            self.key_table = {}
            io.seek(offset_to_key_table)
            data = io.read(22 * key_count)

            for c in chunks(data, 22):
                if len(c) != 22: break
                resref, res_type, res_id = struct.unpack("<16s hL", c)
                resref = resref.decode(get_encoding())
                self.key_table[res_id] = (resref.rstrip(' \t\r\n\0'), res_type)

            self.fn_to_co = {}
            for res_id, (resref, res_type) in self.key_table.items():
                bif_idx = res_id >> 20
                bif = self.bif[bif_idx]
                res_id = res_id & 0xfffff

                #print res_id, resref, res_type, bif_idx
                if not res_id in bif.contained:
                    msg = "%s does not have %d" % (bif.io.name, res_id)
                    raise ValueError(msg)

                ofs, sz, _rt = bif.contained[res_id]
                o = res.ContentObject(resref, res_type, bif.io, ofs, sz)

                fn = o.get_filename()
                if fn in self.fn_to_co and self.fn_to_co[fn][2] < bif_idx:
                    oo, biff, unused = self.fn_to_co[fn]
                    print("%s, in %s shadowed by file in %s" % (fn, biff.io, biff.io))
                    self.content.remove(oo)

                self.fn_to_co[fn] = (o, bif, bif_idx)
                self.add(o)
