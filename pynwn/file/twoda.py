import re
import itertools
import os, io
from pynwn.util.helper import convert_to_number
from pynwn.resource import ContentObject

import csv
from prettytable import PrettyTable, PLAIN_COLUMNS

def quote(string):
    return '"' + string + '"' if ' ' in string else string

class TwoDA:
    """2da Files.
    """

    ROW_NUM_RE = re.compile('^\d+\s+(.*)')
    DEFAULT_RE = re.compile('^DEFAULT:\s+(.*)')

    def __init__(self, source):
        if isinstance(source, str):
            source = ContentObject.from_file(source)
        elif not isinstance(source, ContentObject):
            raise ValueError("Unsupported source type %s!" % type(source))

        self.columns = []
        self.rows = []
        self.max = None
        self.newline = "\n"
        self.default = None
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
        """Returns repr of the 2da as a string
        """
        return str(self.to_StringIO().getvalue())

    def __str__(self):
        """Returns a valid 2da as a string
        """
        return self.to_StringIO().getvalue()

    def get(self, row, col):
        """Gets a 2da entry by row and column label or column index.
        """
        col = self.get_column_index(col)
        return self.rows[row][col]

    def to_ContentObject(self):
        """Returns 2da as a ContentObject.  It's .io contents
        are cStringIO buffer.
        """
        sio = self.to_StringIO()
        resref = self.co.resref
        res_type = 2017
        sio.seek(0, os.SEEK_END)
        size = sio.tell()
        return ContentObject(resref, res_type, sio, 0, size)

    def to_StringIO(self):
        """Returns 2da written in a cStringIO buffer.
        """
        result = io.StringIO()
        result.write("2DA V2.0")
        result.write(self.newline)

        if self.default:
            result.write("DEFAULT: %s" % self.default)

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
        """Gets a 2da entry by row and column label or column index as a float.
        """
        return float(self.get(row, col))

    def get_int(self, row, col):
        """Gets a 2da entry by row and column label or column index as an int.
        """
        return int(self.get(row, col))

    def parse(self, io):
        """Parses a 2da file.
        """
        io = io.replace('\t', ' ')

        lines = [l.strip() for l in iter(io.splitlines()) if len(l.strip())]
        if len(lines) == 0:
            raise ValueError("Invalid 2da file!")

        if not re.match("2DA\s+V2.0", lines[0]):
            raise ValueError("Invalid 2da file, no 2DA header!")

        col_line = 1
        m = self.DEFAULT_RE.match(lines[1])
        if m:
            self.default = m.group(1)
            # If this was default then column header has to be next.
            col_line = 2

        csvreader = csv.reader(lines[col_line:], delimiter=' ', skipinitialspace=True)
        for row in csvreader:
            self.rows.append(row)

        self.columns = [''] + self.rows[0]
        self.rows = self.rows[1:]

    def set(self, row, col, val):
        """Sets a 2da entry by row and column label or column index.
        The value passed is automatically coerced to str.
        """

        col = self.get_column_index(col)
        self.rows[row][col] = str(val)

    def add_padding(self, start, stop):
        pad = ['****'] * (len(self.columns) - 1)
        for i in range(start, stop+1):
            self.rows.append([str(i)] + pad)


    def merge_2dx(self, twodx):
        highest = 0
        for r in twodx.rows:
            highest = max(highest, int(r[0]))

        if highest > 0 and highest > len(self.rows):
            self.add_padding(len(self.rows), highest)

        for r in twodx.rows:
            self.rows[int(r[0])] = r

    def has_column(self, col):
        return col in self.columns

    def add_column(self, col):
        self.columns.append(col)
        for r in self.rows:
            r.append('****')
