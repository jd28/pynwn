import re
import shlex
import itertools
import os, shutil
import yaml
from helper import convert_to_number

class TwoDA:
    """2da Files.
    """

    ROW_NUM_RE = re.compile('^\d+\s+(.*)')
    DEFAULT_RE = re.compile('^DEFAULT:\s+(.*)')

    def __init__(self, io):
        self.columns = []
        self.rows = []
        self.newline = "\n"
        self.io = io
        self.parse(io)
        self.default = None

    def __getitem__(self, i):
        if i >= len(self.rows) or i < 0:
            raise ValueError("Invalid row index!")

        return self.rows[i]

    def expload(self, out_dir='.'):
        """Extracts each line from a tlk and creates a yaml file.
        """
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)

        clean_rows = [r for r in self.rows if self.label_valid(r[self.label_pos])]

        for cr in clean_rows:
            d = {
                'type': self.type,
                'entries': dict(itertools.izip(self.columns, [convert_to_number(e) for e in cr]))
            }

            name = d['entries'][self.label_name]
            if len(name) > 0:
                path = os.path.join(out_dir, cr[self.label_pos] + '.yaml')
                with open(path, 'w') as f:
                    yaml.dump(d, f, indent=4, default_flow_style=False)

        # Write the label file
        path = os.path.join(out_dir, self.twoda+'.2da')
        with open(path, 'w') as f:
            f.write("2DA V2.0" + self.newline)
            if self.default:
                f.write("DEFAULT: %s" % self.default)
            else:
                f.write(self.newline)

            f.write("\t\t"+self.columns[self.label_pos]+self.newline)
            for i, r in enumerate(self.rows):
                f.write("%d\t\t%s%s" % (i, r[self.label_pos], self.newline))


    def get(self, row, col):
        """Gets a 2da entry by row and column label or column index.
        """
        col = self.get_column_index(col)
        return self.rows[row][col]

    def get_column_index(self, col):
        """Gets the column index from a column label.
        """

        if type(col) is str:
            col = self.columns.index(col)

        return col

    def get_float(self, row, col):
        """Gets a 2da entry by row and column label or column index as a float.
        """
        return float(self.get(row, col))

    def get_int(self, row, col):
        """Gets a 2da entry by row and column label or column index as an int.
        """
        return int(self.get(row, col))

    def label_valid(self, lbl):
        """Deterimnes if a 2da label is valid.
        """
        return not lbl in self.invalid_labels

    def parse(self, io):
        """Parses a 2da file.
        """

        lines = [l.strip() for l in io if l.strip() != '']

        if len(lines) == 0:
            raise ValueError("Invalid 2da file!")

        it = iter(lines)
        head = it.next()
        if not re.match("2DA\s+V2.0", head):
            raise ValueError("Invalid 2da file!")

        # Next line could be a Default line or the column header.
        # Since we've ridded ourselves of all empty lines.
        colname = it.next()

        m = self.DEFAULT_RE.match(colname)
        if m:
            self.default = m.group(1)
            # If this was default then column header has to be next.
            colname = it.next()

        self.columns = self.parse_row(colname, False)
        self.rows = [self.parse_row(r) for r in it]

    def parse_row(self, row, strip_row_number=True):
        """Parses a 2da row.  Currently this is implimented by using the
        Python shlex package which parses a superset of 2da row format.
        So it could parse things that are not legal 2da rows.
        """
        if strip_row_number:
            m = self.ROW_NUM_RE.match(row)
            if m: row = m.group(1)

        splitter = shlex.shlex(row, posix=True)
        splitter.whitespace_split = True
        return list(splitter)

    def set(self, row, col, val):
        """Sets a 2da entry by row and column label or column index.
        The value passed is automatically coerced to str.
        """

        col = self.get_column_index(col)
        self.rows[row][col] = str(val)
