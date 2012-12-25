import resource as res
import struct, os
from helper import chunks

class Bif:
    """A Bif object encapsulates an open file handle pointing
    to a .bif file. It's contents are indexed on first access,
    not on creation by NWN::Key::Key (to speed up things).
    """

    def __init__(self, key, io):
        # The Key object this Bif belongs to.
        self.key = key

        # The IO object pointing to the .bif file.
        self.io = io

        # A hash containing the resources contained. Usually not needed,
        # accessed by the encapsulating Key object.
        self.contained = {}

        header = self.io.read(4 + 4 + 3 * 4)
        hs = struct.unpack("<4s 4s L L L", header)

        self.file_type = hs[0]
        self.file_version = hs[1]
        self.var_res_count = hs[2]
        self.fix_res_count = hs[3]
        self.var_table_offset = hs[4]

        self.io.seek(self.var_table_offset)
        data = self.io.read(self.var_res_count * 16)

        for c in chunks(data, 16):
            if len(c) != 16: break

            rid, offset, size, restype = struct.unpack("<L L L L", c)
            rid &= 0xfffff
            self.contained[rid] = (offset, size, restype)

    def __getitem__(self, id):
        offset, size, restype = self.contained[id]
        self.io.seek(offset)
        return self.io.read(size)

    def has_res(self, id):
        """Determine if Bif contains a resource by an resoure ID.

        :param id: A resource ID.
        :type id: int

        """
        return self.contained.has_key(id)

class Key(res.Container):
    """...

    :param io: File handle.
    :param data_path: Path to your NWN installation directory.  e.g: C:/NeverwinterNights/NWN/
    """    
    def __init__(self, io, data_path):
        super(Key, self).__init__()

        self.root = data_path
        self.bif = []

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
            name = struct.unpack("%ds" % name_size, name)[0].rstrip(' \t\r\n\0')
            name = os.path.join(self.root, name.replace('\\', os.sep))
            name = os.path.abspath(name)
            self.bif.append( Bif(self, open(name, 'rb')) )
            self.file_table.append((size, name, drives))

        self.key_table = {}
        io.seek(offset_to_key_table)
        data = io.read(22 * key_count)

        for c in chunks(data, 22):
            if len(c) != 22: break
            resref, res_type, res_id = struct.unpack("<16s hL", c)
            self.key_table[res_id] = (resref.rstrip(' \t\r\n\0'), res_type)

        self.fn_to_co = {}
        for res_id, (resref, res_type) in self.key_table.items():
            bif_idx = res_id >> 20
            bif = self.bif[bif_idx]
            res_id = res_id & 0xfffff

            #print res_id, resref, res_type, bif_idx
            if not bif.contained.has_key(res_id):
                msg = "%s does not have %d" % (bif.io.name, res_id)
                raise ValueError(msg)

            ofs, sz, _rt = bif.contained[res_id]
            o = res.ContentObject(resref, res_type, bif.io, ofs, sz)

            fn = o.get_filename()
            if self.fn_to_co.has_key(fn) and self.fn_to_co[fn][2] < bif_idx:
                oo, biff = self.fn_to_co[fn]
                print "%s, in %s shadowed by file in %s" % (fn, biff.io.name, biff.io.name)
                self.content.remove(oo)

            self.fn_to_co[fn] = (o, bif, bif_idx)
            self.add(o)
