
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

import os, struct
import chardet
import cStringIO
import pynwn.resource as res
from pynwn.helper import chunks

class GffElement( object ):
    def __init__(self, type, value, struct_id, parent_gff):
        self.type = type
        self.val_ = value
        self.id = struct_id
        self.parent = parent_gff

    @property
    def val(self):
        return self.val_

    @val.setter
    def val(self, value):
        self.val_ = value

    def __getitem__(self, name):
        return self.val[name].val

    def __setitem__(self, name, value):
        self.val[name].val = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "GffElement { 'type': %s, 'value': %s }" % (self.type, self.val)

class Gff( object ):
    """Represents a GFF file."""

    # current GFF version
    Version = 'V3.2'

    # gff type ids
    Byte, Char, Word, Short, Dword, Int, Dword64, Int64, Float = 0, 1, 2, 3, 4, 5, 6, 7, 8
    Double, CExoString, ResRef, CExoLocString, Void, Struct, List = 9, 10, 11, 12, 13, 14, 15

    # gff type names
    Types = [
        'byte', 'char', 'word', 'short', 'dword', 'int', 'dword64', 'int64', 'float',
        'double', 'cexostring', 'resref', 'cexolocstring', 'void', 'struct', 'list' ]

    # struct patterns
    HeaderPattern = '4s4s12I'
    StructPattern = '3I'
    LabelPattern  = '16s'
    FieldPattern  = '2I'
    DwordPattern  = 'I'

    def __init__( self, content_object ):
        """Constructor."""

        # associate specified aspects and prepare state
        self.co = content_object
        self.filename = self.co.get_filename()
        self.filetype = self.co.get_extension().upper()
        self._structure = None

    def __getitem__(self, name):
        return self.structure[name].val

    def __setitem__(self, name, value):
        self.structure[name].val = value

    def has_field(self, name):
        return name in self.structure

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

    def load( self ):
        """Loads the source of the associated gff file."""

        # attempt to open the gff file and load its header
        self.source = cStringIO.StringIO(self.co.get())

        header = struct.unpack( self.HeaderPattern, self.source.read( struct.calcsize( self.HeaderPattern ) ) )
        if header[ 0 ].rstrip() == self.filetype and header[ 1 ] == self.Version:
            self.structoffset, self.structcount = header[ 2:4 ]
            self.fieldoffset, self.fieldcount = header[ 4:6 ]
            self.labeloffset, self.labelcount = header[ 6:8 ]
            self.dataoffset, self.datasize = header[ 8:10 ]
            self.indiceoffset, self.indicesize = header[ 10:12 ]
            self.listoffset, self.listsize = header[ 12:14 ]
        else:
            if header[ 1 ] != self.Version:
                raise ValueError, "File: %s: gff file version '%s' does not match current valid version '%s'" % ( self.co.get_filename(), header[ 1 ], self.Version )
            else:
                raise ValueError, "File: %s: gff file type '%s' does not match specified file type '%s'" % ( self.co.get_filename(), header[ 0 ].rstrip(), self.filetype )

        # position the source file at the struct array and prepare structs list
        self.source.seek( self.structoffset )
        self.structs = []

        # parse the gff struct array
        size = struct.calcsize( self.StructPattern )
        rd = self.source.read( self.structcount * size )
        for chunk in chunks(rd, size):
            type, offset, count = struct.unpack( self.StructPattern, chunk)
            if offset == 0xffffffff:
                self.structs.append( [ type, -1 ] )
            elif count == 1:
                self.structs.append( [ type, offset ] )
            else:
                pattern = "%dI" % count
                indexes = struct.unpack( pattern, self.scan( self.indiceoffset + offset, struct.calcsize( pattern ) ) )
                self.structs.append( [ type, list( indexes ) ] )

        # position the source file at the label array and prepare labels list
        self.source.seek( self.labeloffset )
        self.labels = []

        # parse the gff label array
        size = struct.calcsize( self.LabelPattern )
        rd = self.source.read( size * self.labelcount )
        for chunk in chunks(rd, size):
            label = struct.unpack( self.LabelPattern, chunk )[ 0 ]
            self.labels.append( label.rstrip( '\x00' ) )

        # position the source file at the field array and prepare fields list
        self.source.seek( self.fieldoffset )
        self.fields = []

        # parse the gff field array
        size = struct.calcsize( self.FieldPattern )
        dwordsize = struct.calcsize( self.DwordPattern )
        for index in range( 0, self.fieldcount ):
            type, label = struct.unpack( self.FieldPattern, self.source.read( size ) )
            recipe = self.Recipes[ type ]
            if recipe[ 0 ] is True:
                value = self.scan( struct.unpack( self.DwordPattern, self.source.read( dwordsize ) )[ 0 ], recipe[ 2 ] )
                data = struct.unpack( recipe[ 1 ], value )[ 0 ]
            elif recipe[ 0 ] is False:
                data = struct.unpack( recipe[ 1 ], self.source.read( recipe[ 2 ] ) )[ 0 ]
                if recipe[ 2 ] < 4:
                    self.source.seek( self.source.tell() + ( 4 - recipe[ 2 ] ) )
            else:
                offset = struct.unpack( self.DwordPattern, self.source.read( dwordsize ) )[ 0 ]
                data = recipe[ 1 ]( self, offset )
            self.fields.append( [ self.Types[ type ], self.labels[ label ], data ] )

        # close the source file and build the gff structure, then indicate status
        self.source.close()
        self._structure = self.build_struct( 0 )
        return True

    def save( self ):
        """Saves the current version of the gff structure to the associated file."""

        #print "Attempting to save %s" % (self.co.get_filename())

        # prepare the intermediate lists and parse the gff structure into the fields and structs lists
        self.fields, self.labels, self.structs = [], [], []
        self.structs.append( [ 0xFFFFFFFFL, [] ] )
        topfields = self.build_fields( self._structure )
        self.structs[ 0 ][ 1 ] = topfields

        # parse labels out and replace with label indices
        for field in self.fields:
            if field[ 1 ] not in self.labels:
                self.labels.append( field[ 1 ] )
            field[ 1 ] = self.labels.index( field[ 1 ] )

        # generate the structs and field indices arrays
        structs, indices = '', ''
        for structtype, structfields in self.structs:
            if len( structfields ) == 1:
                structs += struct.pack( '<3I', structtype, structfields[ 0 ], 1 )
            else:
                structs += struct.pack( '<3I', structtype, len( indices ), len( structfields ) )
                for fieldid in structfields:
                    indices += struct.pack( 'I', fieldid )

        # generate the fields, field data and list indices arrays
        fields, fielddata, lists = '', '', ''
        for type, labelidx, data in self.fields:
            fields += struct.pack( '2I', type, labelidx )
            recipe = self.Recipes[ type ]
            if type == self.List:
                fields += struct.pack( 'I', len( lists ) )
                lists += struct.pack( 'I', len( data ) )
                for structid in data:
                    lists += struct.pack( 'I', structid )
            elif type == self.Struct:
                fields += struct.pack( 'I', data )
            elif recipe[ 0 ] is True:
                fields += struct.pack( 'I', len( fielddata ) )
                fielddata += struct.pack( recipe[ 1 ], data )
            elif recipe[ 0 ] is False:
                pattern = recipe[ 1 ]
                if recipe[ 2 ] < 4:
                    pattern += "%dx" % ( 4 - recipe[ 2 ] )
                fields += struct.pack( pattern, data )
            else:
                fields += struct.pack( 'I', len( fielddata ) )
                fielddata += recipe[ 2 ]( self, data )

        # generate the labels array
        labels = ''
        for label in self.labels:
            length = len( label )
            pattern = "%ds" % length
            if length < 16:
                pattern += "%dx" % ( 16 - length )
            labels += struct.pack( pattern, label )

        # generate the header and concat the file content
        content = ''
        header = struct.pack( '8s', "%s %s" % ( self.filetype, self.Version ) )
        header += struct.pack( '2I', 56, len( self.structs ) )
        content += structs
        header += struct.pack( '2I', ( 56 + len( content ) ), len( self.fields ) )
        content += fields
        header += struct.pack( '2I', ( 56 + len( content ) ), len( self.labels ) )
        content += labels
        header += struct.pack( '2I', ( 56 + len( content ) ), len( fielddata ) )
        content += fielddata
        header += struct.pack( '2I', ( 56 + len( content ) ), len( indices ) )
        content += indices
        header += struct.pack( '2I', ( 56 + len( content ) ), len( lists ) )
        content = header + content + lists

        self.co.io = cStringIO.StringIO(content)
        self.co.offset = 0
        self.co.size = len(content)
        self.co.modified = True

        # Temporary hack.  Sadly it seems the save() function has side-effects
        # so None it on when saved so that it can be reloaded on next access.
        self._structure = None

        return True

    def scan( self, offset, length ):
        """Scans the specified length from the specified offset in the open file, then returns to the previous position."""

        # mark the current position, scan the specified data, and return to the current position
        position = self.source.tell()
        self.source.seek( offset )
        data = self.source.read( length )
        self.source.seek( position )
        return data

    def build_struct( self, sid ):
        """Builds a structural representation of the specified struct id."""

        # assemble the fields of the specified struct
        structure = {}

        # Modified the following lines.  Python is unable to iterate over
        # int, which is what the struct contains if there is only one field/
        fields = self.structs[ sid ][ 1 ]
        if not isinstance(fields, list): fields = [fields]

        for field in fields:
            ftype, label, value = self.fields[ field ]
            if ftype == 'struct':
                stype, sid = self.structs[ value ]
                structure[ label ] = GffElement(stype, self.build_struct( value ), value, self)
            elif ftype == 'list':
                group = []
                for structid in value:
                    stype, sid = self.structs[ structid ]
                    group.append(GffElement(stype, self.build_struct( structid ), structid, self))
                structure[ label ] = GffElement('list', group, -1, self)
            else:
                structure[ label ] = GffElement(ftype, value, -1, self)

        # return the completed structure
        return structure

    def build_fields( self, structure ):
        """Build a field list from the specified structure."""

        # identify and parse the fields of the specified structure
        ids = []
        for label, value in structure.iteritems():
            type, data = value.type, value.val

            if type == 'list':
                idlist = []
                for d in data:
                    structid, structdata = d.type, d.val
                    structids = self.build_fields( structdata )
                    self.structs.append( [ structid, structids ] )
                    idlist.append( len( self.structs ) - 1 )
                self.fields.append( [ self.Types.index( 'list' ), label, idlist ] )
                ids.append( len( self.fields ) - 1 )
            elif type in self.Types:
                self.fields.append( [ self.Types.index( type ), label, data ] )
                ids.append( len( self.fields ) - 1 )
            else:
                structid, structdata = type, data
                structids = self.build_fields( structdata )
                self.structs.append( [ structid, structids ] )
                self.fields.append( [ self.Types.index( 'struct' ), label, len( self.structs ) - 1] )
                ids.append( len( self.fields ) - 1 )

        # return the field id list
        return ids

    def parse_cexostring( self, offset ):
        """Parses a gff cexostring."""

        # identify the current position, read and parse the cexostring, and return to the current position
        position = self.source.tell()
        self.source.seek( self.dataoffset + offset )
        length = struct.unpack( self.DwordPattern, self.source.read( 4 ) )[ 0 ]
        pattern = "%ds" % length
        data = struct.unpack( pattern, self.source.read( struct.calcsize( pattern ) ) )[ 0 ]
        self.source.seek( position )
        return data

    def write_cexostring( self, data ):
        """Writes the specified data as a cexostring and returns it."""

        length = len( data )
        pattern = "I%ds" % length
        return struct.pack( pattern, length, data )

    def parse_resref( self, offset ):
        """Parses a gff resref."""

        # identify the current position, read and parse the resref, and return to the current position
        position = self.source.tell()
        self.source.seek( self.dataoffset + offset )
        length = struct.unpack( 'B', self.source.read( 1 ) )[ 0 ]
        if length == 0:
            self.source.seek( position )
            return ''
        pattern = "%ds" % length
        data = struct.unpack( pattern, self.source.read( struct.calcsize( pattern ) ) )[ 0 ]
        self.source.seek( position )
        return data

    def write_resref( self, data ):
        """Writes the specified data as a resref and returns it."""

        length = len( data )
        pattern = "B%ds" % length
        return struct.pack( pattern, length, data )

    def parse_cexolocstring( self, offset ):
        """Parses a gff cexolocstring."""

        # identify the current position, read and parse the cexolocstring, and return to the current position
        position = self.source.tell()
        self.source.seek( self.dataoffset + offset )
        length, stringref, count = struct.unpack( '3I', self.source.read( 12 ) )
        result = [ stringref ]
        if count > 0:
            for substring in range( 0, count ):
                id, length = struct.unpack( '2I', self.source.read( 8 ) )
                pattern = "%ds" % length
                data = struct.unpack( pattern, self.source.read( struct.calcsize( pattern ) ) )[ 0 ]
                result.append( [ id, data ] )
        self.source.seek( position )

        return result

    def write_cexolocstring( self, data ):
        """Writes the specified data as a cexolocstring and returns it."""

        if len( data ) == 1:
            return struct.pack( '3I', 8, data[ 0 ], 0 )

        stringref = data.pop( 0 )
        content = struct.pack( '2I', stringref, len( data ) )
        for substring in data:
            length = len( substring[ 1 ] )
            pattern = "2I%ds" % length
            content += struct.pack( pattern, substring[ 0 ], length, substring[ 1 ] )
            return struct.pack( 'I', len( content ) ) + content

    def parse_void( self, offset ):
        """Parses a gff void."""

        # identify the current position, read and parse the void, and return to the current position
        position = self.source.tell()
        self.source.seek( self.dataoffset + offset )
        length = struct.unpack( self.DwordPattern, self.source.read( 4 ) )[ 0 ]
        data = self.source.read( length )
        self.source.seek( position )
        return data

    def write_void( self, data ):
        """Writes the specified data as a void and returns it."""

        length = len( data )
        pattern = "I%dB" % length
        return struct.pack( pattern, length, data )

    def parse_list( self, offset ):
        """Parses a gff list."""

        # identify the current position, read and parse the list, and return to the current position
        position = self.source.tell()
        self.source.seek( self.listoffset + offset )
        count = struct.unpack( self.DwordPattern, self.source.read( 4 ) )[ 0 ]
        pattern = "%dI" % count
        data = struct.unpack( pattern, self.source.read( struct.calcsize( pattern ) ) )
        self.source.seek( position )
        return data

    def parse_struct( self, offset ):
        """Parses a gff struct."""

        return offset

    # type recipes      ( offset?, pattern, size ) or ( None, function )
    Recipes = {
        Byte:           ( False, 'B', 1 ),
        Char:           ( False, 'c', 1 ),
        Word:           ( False, 'H', 2 ),
        Short:          ( False, 'h', 2 ),
        Dword:          ( False, 'I', 4 ),
        Int:            ( False, 'i', 4 ),
        Dword64:        ( True,  'Q', 8 ),
        Int64:          ( True,  'q', 8 ),
        Float:          ( False, 'f', 4 ),
        Double:         ( True,  'd', 8 ),
        CExoString:     ( None,  parse_cexostring, write_cexostring ),
        ResRef:         ( None,  parse_resref, write_resref ),
        CExoLocString:  ( None,  parse_cexolocstring, write_cexolocstring ),
        Void:           ( None,  parse_void, write_void ),
        Struct:         ( None,  parse_struct, None ),
        List:           ( None,  parse_list, None )
    }

    def dump( self ):
        """Returns a string representation of the gff structure."""

        # ensure structure exists
        if self._structure is None:
            self.load()

        # dump the header
        size = self.co.size
        content = '%s: %s (%d bytes)\n' % ( self.filetype, self.filename, size )
        content += '[%d structs at %d, %d fields at %d, %d labels at %d]\n\n' % ( self.structcount, self.structoffset, self.fieldcount, self.fieldoffset, self.labelcount, self.labeloffset )

        # dump the structure itself
        content += self.dump_struct( self._structure, 0 )

        # return the dumped structure
        return content

    def dump_struct( self, reference, indent ):
        """Dumps a specific struct in the gff structure."""

        # dump the fields and values of the struct
        content = ''
        for label, value in reference.iteritems():
            type, data = value
            if type == 'list':
                content += ( ' ' * indent ) + '%s: [list] %d members...\n' % ( label, len( data ) )
                index = 0
                for item in data:
                    content += ( ' ' * indent ) + ' (%d) => struct %s\n' % ( index, item[ 0 ] )
                    content += self.dump_struct( item[ 1 ], indent + 2 )
                    index += 1
            elif type in self.Types:
                content += ( ' ' * indent ) + '%s: %s  [%s]\n' % ( label, repr( data ), type )
            else:
                content += ( ' ' * indent ) + '%s: [struct] %d...\n' % ( label, data[ 0 ] )
                content += self.dump_struct( data[ 1 ], indent + 2 )

        # return content
        return content
