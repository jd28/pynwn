
#  NeverWinter Nights: GFF File Format Reader/Writer
#  [gff.py, v1.2 (BETA), 2004-03-08, jrm]
#
#  ----------------------------------------------------------------------------
#  Copyright (C) 2003-2004 Jordan McCoy. All Rights Reserved.
#  Copyright (C) 2012-2013 Joshua Dean.
#
#  This GFF format software is free software; you can use, redistribute, and/or
#  modify it under the terms of the GNU General Public License, as published by
#  the Free Software Foundation, using either version 2 of the license or later
#  available versions.
#
#  THIS GFF FORMAT SOFTWARE IS PROVIDED BY ITS AUTHORS "AS IS", AND ANY EXPRESS
#  OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT ARE
#  DISCLAIMED. IN NO EVENT SHALL ITS AUTHORS, CONTRIBUTORS OR TESTERS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTIAL, CONSEQUENTIAL OR EXEMPLARY DAMAGES OR
#  CLAIMS HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER CONTRACT, TORT
#  OR STRICT LIABILITY ARISING IN ANY WAY OUT OF THE DISTRIBUTION, MODIFICATION
#  AND/OR OTHER USE OF THIS SOFTWARE EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
#  DAMAGE. SEE THE GNU GENERAL PUBLIC LICENSE FOR MORE DETAILS.
#
#  The GNU General Public License should be available with this distribution as
#  a file named 'LICENSE'; if not, write to the Free Software Foundation, Inc.,
#  59 Temple Place, Suite 300, Boston, MA, 02111-1307 USA. For more information
#  on the terms of this license, please see <http://www.gnu.org/>.
#
#  NeverWinter Nights and all attendent content, as well as the GFF file format
#  remains the copyright of Bioware.

import os, struct, sys
import chardet
import io
import pynwn.resource as res
from pynwn.util.helper import chunks
from pynwn.nwn.types import *

def make_gff_property(attr, name):
    def getter(self):
        gff = getattr(self, attr)

        # Ensure that the correct types have been passed.
        if (not isinstance(gff, Gff) and
            not isinstance(gff, GffInstance)):
            raise ValueError("""ERROR: make_gff_property can only operate on
                             Gffs and GffInstances!""")

        return gff[name[0]]

    def setter(self, val):
        gff = getattr(self, attr)

        # Ensure that the correct types have been passed.
        if (not isinstance(gff, Gff) and
            not isinstance(gff, GffInstance)):
            raise ValueError("""ERROR: make_gff_property can only operate on
                             Gffs and GffInstances!""")

        gff[name[0]] = val
        self.stage()

    return property(getter, setter, None, name[1])

def make_gff_locstring_property(attr, name):
    def getter(self, lang=None):
        gff = getattr(self, attr)

        # Ensure that the correct types have been passed.
        if (not isinstance(gff, Gff) and
            not isinstance(gff, GffInstance)):
            raise ValueError("""ERROR: make_gff_property can only operate on
                             Gffs and GffInstances!""")

        ls = gff[name[0]]
        if lang is None:
            return ls.strref
        else:
            return ls[lang]


    def setter(self, lang=None, string=None):
        gff = getattr(self, attr)

        # Ensure that the correct types have been passed.
        if (not isinstance(gff, Gff) and
            not isinstance(gff, GffInstance)):
            raise ValueError("""ERROR: make_gff_property can only operate on
                             Gffs and GffInstances!""")

        ls = gff[name[0]]
        if string is None:
            ls.strref = lang
        else:
            ls[lang] = string

        self.stage()

    return (getter, setter)


class GffInstance(object):
    """GFF Instance Object.

    This object creats a view into a parent GFF
    """
    def __init__(self, parent_gff, list_name, list_index):
        self.parent = parent_gff
        self.field  = list_name
        self.index  = list_index

    def __getitem__(self, name):
        try:
            res = self.parent[self.field][self.index][name]
        except KeyError:
            return None
        if (isinstance(res, list) or
            isinstance(res, dict) or
            isinstance(res, NWLocalizedString)):
            return res

        return res.value

    def __setitem__(self, name, value):
        res = self.parent[self.field][self.index][name]
        if (isinstance(res, list) or
            isinstance(res, dict) or
            isinstance(res, NWLocalizedString)):
            raise ValueError("""Unable to set List, Struct, or
                             NWLocalizedString types""")

        res.value = value

    def add_field(self, name, value):
        self.parent[self.field][self.index][name] = value

    def has_field(self, name):
        return name in self.parent[self.field][self.index]

    def get_structure(self):
        return self.parent[self.field][self.index]

class Gff(object):
    """Represents a GFF file."""

    # current GFF version
    Version = 'V3.2'
    LABEL_LENGTH = 16

    Classes = [NWByte, NWChar, NWWord, NWShort, NWDword, NWInt, NWDword64,
               NWInt64, NWFloat, NWDouble, NWString, NWResref,
               NWLocalizedString, NWVoid, NWStruct, NWList]

    # gff type names
    TypeNames = [c.type for c in Classes]

    # struct patterns
    HeaderPattern = '4s4s12I'
    StructPattern = '3I'
    LabelPattern  = '16s'
    FieldPattern  = '2I'
    DwordPattern  = 'I'

    def __init__(self, content_object):
        """Constructor."""

        # associate specified aspects and prepare state
        self.co = content_object
        self.filename = self.co.get_filename()
        self.filetype = self.co.get_extension().upper()
        self._structure = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.structure)

    def __getitem__(self, name):
        if not self.is_loaded: self.load()
        res = self.structure[name]
        if (isinstance(res, list) or
            isinstance(res, dict) or
            isinstance(res, NWLocalizedString)):
            return res

        return res.value

    def __setitem__(self, name, value):
        res = self.structure[name]
        if (isinstance(res, list) or
            isinstance(res, dict) or
            isinstance(res, NWLocalizedString)):
            raise ValueError('Unable to set List, Struct, or NWLocalizedString types')

        res.value = value

    def has_field(self, name):
        return name in self.structure

    def get_field(self, name):
        if not self.is_loaded:
            self.load()
        return self.structure[name]

    def add_field(self, name, value):
        if not self.is_loaded:
            self.load()
        self.structure[name] = value


    @property
    def structure(self):
        """Gets the structure, loading it if necessary."""

        # load the source file if necessary
        if self._structure is None:
            self.load()

        # return the structure
        return self._structure

    def is_loaded(self):
        return not self._structure is None

    def load(self):
        """Loads the source of the associated gff file."""

        # attempt to open the gff file and load its header
        self.source = io.BytesIO(self.co.get())

        header = struct.unpack(self.HeaderPattern,
                               self.source.read(struct.calcsize(self.HeaderPattern)))

        if (header[0].decode(sys.stdout.encoding).rstrip() == self.filetype
            and header[1].decode(sys.stdout.encoding) == self.Version):
            self.structoffset, self.structcount = header[2:4]
            self.fieldoffset, self.fieldcount = header[4:6]
            self.labeloffset, self.labelcount = header[6:8]
            self.dataoffset, self.datasize = header[8:10]
            self.indiceoffset, self.indicesize = header[10:12]
            self.listoffset, self.listsize = header[12:14]
        else:
            if header[1].decode(sys.stdout.encoding) != self.Version:
                raise ValueError("File: %s: gff file version '%s' does not match current valid version '%s'" % (self.co.get_filename(), header[1], self.Version))
            else:
                raise ValueError("File: %s: gff file type '%s' does not match specified file type '%s'" % (self.co.get_filename(), header[0].rstrip(), self.filetype))

        # position the source file at the struct array and prepare structs list
        self.source.seek(self.structoffset)
        self.structs = []

        # parse the gff struct array
        size = struct.calcsize(self.StructPattern)
        rd = self.source.read(self.structcount * size)

        for chunk in chunks(rd, size):
            type, offset, count = struct.unpack(self.StructPattern, chunk)
            if offset == 0xffffffff:
                self.structs.append([type, -1])
            elif count == 1:
                self.structs.append([type, offset])
            else:
                pattern = "%dI" % count
                position = self.source.tell()
                self.source.seek(self.indiceoffset + offset)
                data = self.source.read(struct.calcsize(pattern))
                self.source.seek(position)

                indexes = struct.unpack(pattern, data)
                self.structs.append([type, list(indexes)])


        # position the source file at the label array and prepare labels list
        self.source.seek(self.labeloffset)
        self.labels = []

        # parse the gff label array
        size = struct.calcsize(self.LabelPattern)
        rd = self.source.read(size * self.labelcount)
        for chunk in chunks(rd, size):
            label = struct.unpack(self.LabelPattern, chunk)[0].decode(sys.stdout.encoding)
            self.labels.append(label.rstrip('\x00'))

        # position the source file at the field array and prepare fields list
        self.source.seek(self.fieldoffset)
        self.fields = []

        # parse the gff field array
        size = struct.calcsize(self.FieldPattern)
        dwordsize = struct.calcsize(self.DwordPattern)
        for index in range(0, self.fieldcount):
            type, label = struct.unpack(self.FieldPattern,
                                        self.source.read(size))
            Type = self.Classes[type]

            position = None
            # False indicates there is no offset
            if not Type.at_offset is False:
                offset = struct.unpack('I', self.source.read(4))[0]
                position = self.source.tell()

            if Type.at_offset == 'data':
                offset += self.dataoffset
            elif Type.at_offset == 'list':
                offset += self.listoffset

            if position:
                data = Type.unpack(self.source, offset)
                self.source.seek(position)
            else:
                data = Type.unpack(self.source)

            type_name  = Type.type
            label_name = self.labels[label]
            self.fields.append([type_name, label_name, data])

        # close the source file and build the gff structure, then indicate
        # status
        self.source.close()
        self._structure = self.build_struct(0)
        return True

    def save(self):
        """Saves the current version of the gff structure to the associated
        file.
        """

        print("Attempting to save %s" % (self.co.get_filename()))

        # prepare the intermediate lists and parse the gff structure into the
        # fields and structs lists
        self.fields, self.labels, self.structs = [], [], []
        self.structs.append([0xFFFFFFFF, []])
        topfields = self.build_fields(self._structure)
        self.structs[0][1] = topfields

        # parse labels out and replace with label indices
        for field in self.fields:
            if field[1] not in self.labels:
                self.labels.append(field[1])
            field[1] = self.labels.index(field[1])

        # generate the structs and field indices arrays
        structs, indices = '', ''
        for structtype, structfields in self.structs:
            if len(structfields) == 1:
                structs += struct.pack('<3I', structtype, structfields[0], 1)
            else:
                structs += struct.pack('<3I', structtype, len(indices),
                                       len(structfields))
                for fieldid in structfields:
                    indices += struct.pack('I', fieldid)

        # generate the fields, field data and list indices arrays
        fields, fielddata, lists = '', '', ''
        for type, labelidx, data in self.fields:

            fields += struct.pack('2I', type, labelidx)

            if type == NWList.type_id:
                fields += struct.pack('I', len(lists))
                lists += struct.pack('I', len(data))
                for structid in data:
                    lists += struct.pack('I', structid)

            elif type == NWStruct.type_id:
                fields += struct.pack('I', data)

            else:
                Type = self.Classes[type]

                if Type.at_offset is False:
                    fields += data.pack()
                else:
                    fields += struct.pack('I', len(fielddata))
                    fielddata += data.pack()

        # generate the labels array
        labels = ''
        for label in self.labels:
            length = len(label)
            pattern = "%ds" % length
            if length < Gff.LABEL_LENGTH:
                pattern += "%dx" % (Gff.LABEL_LENGTH - length)
            labels += struct.pack(pattern, label)

        # generate the header and concat the file content
        content = ''
        header = struct.pack('8s', "%s %s" % (self.filetype, self.Version))
        header += struct.pack('2I', 56, len(self.structs))
        content += structs
        header += struct.pack('2I', 56 + len(content), len(self.fields))
        content += fields
        header += struct.pack('2I', 56 + len(content), len(self.labels))
        content += labels
        header += struct.pack('2I', 56 + len(content), len(fielddata))
        content += fielddata
        header += struct.pack('2I', 56 + len(content), len(indices))
        content += indices
        header += struct.pack('2I', 56 + len(content), len(lists))
        content = header + content + lists

        self.co.io = cStringIO.StringIO(content)
        self.co.offset = 0
        self.co.size = len(content)
        self.co.modified = True

        # Temporary hack.  Sadly it seems the save() function has side-effects
        # so None it on when saved so that it can be reloaded on next access.
        self._structure = None

        return True

    def scan(self, offset, length):
        """Scans the specified length from the specified offset in the open
        file, then returns to the previous position.
        """

        # mark the current position, scan the specified data, and return to the
        # current position
        position = self.source.tell()
        self.source.seek(offset)
        data = self.source.read(length)
        self.source.seek(position)
        return data

    def build_struct(self, sid):
        """Builds a structural representation of the specified struct id."""

        # assemble the fields of the specified struct
        structure = {}

        # Modified the following lines.  Python is unable to iterate over
        # int, which is what the struct contains if there is only one field
        fields = self.structs[sid][1]
        if not isinstance(fields, list): fields = [fields]

        for field in fields:
            ftype, label, value = self.fields[field]
            if ftype == 'struct':
                stype, sid = self.structs[value]
                result = self.build_struct(value)
                result['_STRUCT_TYPE_'] = stype
                structure[label] = result
            elif ftype == 'list':
                group = []
                for structid in value:
                    stype, sid = self.structs[structid]
                    result     = self.build_struct(structid)
                    result['_STRUCT_TYPE_'] = stype
                    group.append(result)
                structure[label] = group
            else:
                structure[label] = value

        # return the completed structure
        return structure

    def build_fields(self, structure):
        """Build a field list from the specified structure."""

        # identify and parse the fields of the specified structure
        ids = []
        for label, value in structure.iteritems():
            if label == '_STRUCT_ID_' or label == '_STRUCT_TYPE_':
                continue

            if isinstance(value, list):
                idlist = []
                for d in value:
                    structid, structdata = d['_STRUCT_TYPE_'], d
                    structids = self.build_fields(structdata)
                    self.structs.append([structid, structids])
                    idlist.append(len(self.structs) - 1)
                type, value = NWList.type_id, idlist
            elif isinstance(value, dict):
                structid, structdata = value['_STRUCT_TYPE_'], value
                structids = self.build_fields(structdata)
                self.structs.append([structid, structids])
                type, value = NWStruct.type_id, len(self.structs) - 1
            elif value.type in self.TypeNames:
                type, value = value.type_id, value
            else:
                raise ValueError("Unknown Type")

            self.fields.append([type, label, value])
            ids.append(len(self.fields) - 1)

        # return the field id list
        return ids
