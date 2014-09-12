import re
import itertools
import os, io
from pynwn.util.helper import convert_to_number
from pynwn.resource import ContentObject

import csv
from prettytable import PrettyTable, PLAIN_COLUMNS

def quote(string):
    return '"' + string + '"' if ' ' in string else string

class TwoDX:
    """2dx Files.
    """

    ROW_NUM_RE = re.compile('^\d+\s+(.*)')
    TLK_RE = re.compile('^TLK:\s+([0-9]+)\s+\((.*)\)')

    def __init__(self, source):
        if isinstance(source, str):
            source = ContentObject.from_file(source)
        elif not isinstance(source, ContentObject):
            raise ValueError("Unsupported source type %s!" % type(source))

        self.columns = []
        self.rows = []
        self.max = None
        self.newline = "\n"
        self.tlk_columns = None
        self.tlk_offset = None
        self.co = source
        self.parse(source.get('r'))

    def __getitem__(self, i):
        if isinstance(i, int):
            if i >= len(self.rows) or i < 0:
                raise ValueError("Invalid row index!")
            return self.rows[i]
        elif isinstance(i, slice):
            pass

    def __repr__(self):
        """Returns repr of the 2dx as a string
        """
        return str(self.to_StringIO().getvalue())

    def __str__(self):
        """Returns a valid 2dx as a string
        """
        return self.to_StringIO().getvalue()

    def get(self, row, col):
        """Gets a 2dx entry by row and column label or column index.
        """
        col = self.get_column_index(col)
        return self.rows[row][col]

    def set(self, row, col, val):
        """Gets a 2dx entry by row and column label or column index.
        """
        col = self.get_column_index(col)
        self.rows[row][col] = val

    def to_ContentObject(self):
        """Returns 2dx as a ContentObject.  It's .io contents
        are cStringIO buffer.
        """
        sio = self.to_StringIO()
        resref = self.co.resref
        res_type = 2017
        sio.seek(0, os.SEEK_END)
        size = sio.tell()
        return ContentObject(resref, res_type, sio, 0, size)

    def to_StringIO(self):
        """Returns 2dx written in a cStringIO buffer.
        """
        result = io.StringIO()
        result.write("2DX V2.0")
        result.write(self.newline)

        if self.tlk_offset:
            result.write("TLK: %d" % self.tlk_offset)
            if self.tlk_columns:
                result.write("(%s)" % ",".join(self.tlk_columns))
        result.write(self.newline)

        x = PrettyTable(self.columns)
        x.set_style(PLAIN_COLUMNS)
        x.align = 'l'
        x.right_padding_width = 4

        for rs in self.rows:
            x.add_row([quote(word) for word in rs])
        result.write(x.get_string())

        return result

    def get_column_index(self, col):
        """Gets the column index from a column label.
        """

        if isinstance(col, str):
            col = self.columns.index(col)
        else:
            col += 1

        return col

    def get_float(self, row, col):
        """Gets a 2dx entry by row and column label or column index as a float.
        """
        return float(self.get(row, col))

    def get_int(self, row, col):
        """Gets a 2dx entry by row and column label or column index as an int.
        """
        return int(self.get(row, col))

    def parse(self, io):
        """Parses a 2dx file.
        """

        lines = [l.strip() for l in iter(io.splitlines()) if len(l.strip())]
        if len(lines) == 0:
            raise ValueError("Invalid 2dx file!")

        if not re.match("2DX\s+V2.0", lines[0]):
            raise ValueError("Invalid 2dx file, no 2DX header!")

        col_line = 1
        m = self.TLK_RE.match(lines[1])
        if m:
            self.tlk_offset = m.group(1)
            self.tlk_columns = m.group(2)
            if self.tlk_columns:
                self.tlk_columns = [int(s.strip()) for s in self.tlk_columns.split(',')]
            # If this was default then column header has to be next.
            col_line = 2

        csvreader = csv.reader(lines[col_line:], delimiter=' ', skipinitialspace=True)
        for row in csvreader:
            self.rows.append(row)

        self.columns = [''] + self.rows[0]
        self.rows = self.rows[1:]

        if self.tlk_columns and len(self.tlk_columns):
            self.update_tlks()

    def update_tlks(self):
        offset = self.tlk_offset
        for c in self.tlk_columns:
            for i in range(len(self.rows)):
                cur = self.get(i, c)
                if cur != '****':
                    self.set(i, c, str(int(cur) + int(self.tlk_offset) + 0x01000000))

    def set(self, row, col, val):
        """Sets a 2dx entry by row and column label or column index.
        The value passed is automatically coerced to str.
        """

        col = self.get_column_index(col)
        self.rows[row][col] = str(val)
