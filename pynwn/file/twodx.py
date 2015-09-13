import re
import itertools
import os, io
from pynwn.util import convert_to_number
from pynwn.resource import ContentObject

import yaml
import csv
from prettytable import PrettyTable, PLAIN_COLUMNS

def quote(string):
    return '"' + string + '"' if ' ' in string else string

class TwoDX:
    """2dx Files.
    """

    ROW_NUM_RE = re.compile('^\d+\s+(.*)')
    TLK_RE = re.compile('^TLK:\s+([0-9]+)\s+\((.*)\)')
    DESC_RE = re.compile('^DESCRIPTION: (.*)')

    def __init__(self, source):
        if isinstance(source, str):
            source = ContentObject.from_file(source)
        elif not isinstance(source, ContentObject):
            raise ValueError("Unsupported source type %s!" % type(source))

        self.columns = []
        self.rows = []
        self.max = None
        self.newline = "\n"
        self.metadata = {}
        self.tlk_columns = None
        self.tlk_offset = None
        self.co = source
        self.description = None
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
        result.write("2DX V2.1")
        result.write("---")
        result.write(yaml.dump(self.metadata))
        result.write("---")

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

    def parse20Header(self, lines):
        i = 1
        while True:
            m = self.TLK_RE.match(lines[i])
            if m:
                self.metadata["tlk"] = {}
                self.tlk_offset = m.group(1)
                self.tlk_columns = m.group(2)
                if self.tlk_columns:
                    for s in self.tlk_columns.split(','):
                        self.metadata["tlk"][s.strip()] = self.tlk_offset
                i += 1
                continue
            m = self.DESC_RE.match(lines[i])
            if m:
                self.metadata["description"] = m.group(1)
                i += 1
                continue

            break
        return i

    def parse21Header(self, lines):
        i = 1
        holder = []
        if lines[i].startswith("---"):
            i += 1
            while not lines[i].startswith("---"):
                holder.append(lines[i])
                i += 1
                if i >= len(lines):
                    raise RuntimeError("Unterminated YAML header!")
            i += 1
            holder = '\n'.join(holder)
            try:
                self.metadata = yaml.load(holder)
            except:
                raise RuntimeError("Invalid YAML header!")

        return i
    def parse(self, io):
        """Parses a 2dx file.
        """

        lines = [l for l in iter(io.splitlines())]
        if len(lines) == 0:
            raise ValueError("Invalid 2dx file!")

        if re.match("2DX\s+V2.0", lines[0]):
          self.version = lines[0]
          col_line = self.parse20Header(lines)
        elif re.match("2DX\s+V2.1", lines[0]):
          col_line = self.parse21Header(lines)
          self.version = lines[0]
        else:
            raise ValueError("Invalid 2dx file, no 2DX header!")

        lines = [l.strip() for l in lines[col_line:] if len(l.strip()) > 0]
        csvreader = csv.reader(lines, delimiter=' ', skipinitialspace=True)
        for row in csvreader:
            self.rows.append(row)

        # 2dx doesn't need to have any rows/labels.  All changes can be in the metadata.
        if not len(self.rows): return

        self.columns = [''] + self.rows[0]
        self.rows = self.rows[1:]

        if 'tlk' in self.metadata:
            self.update_tlks()

    def update_tlks(self):
        offset = self.tlk_offset
        for c, off in self.metadata['tlk'].items():
            for i in range(len(self.rows)):
                cur = self.get(i, c)
                if cur != '****':
                    self.set(i, c, str(int(cur) + int(off) + 0x01000000))

    def set(self, row, col, val):
        """Sets a 2dx entry by row and column label or column index.
        The value passed is automatically coerced to str.
        """

        col = self.get_column_index(col)
        self.rows[row][col] = str(val)
