import re
import shlex
import itertools
import os, shutil, cStringIO
from pynwn.util.helper import convert_to_number
from pynwn.resource import ContentObject

def make_row(lst, max):
    return ''.join([s.ljust(m + 4) for s, m in itertools.izip(lst, max)])

def max_array(current_max, add):
    if not current_max: return add
    return [max(x, y) for x, y in zip(current_max, add)]

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
        self.parse(source.get())


    def __getitem__(self, index):
        if isinstance(index, int):
            if i >= len(self.rows) or i < 0:
                raise ValueError("Invalid row index!")
            return self.rows[i]
        elif isinstance(index, slice):
            pass

    def __repr__(self):
        """Returns repr of the 2da as a string
        """
        return repr(self.to_StringIO().getvalue())
        
    def __str__(self):
        """Returns a valid 2da as a string
        """
        return self.to_StringIO().getvalue()

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
        result = cStringIO.StringIO()
        result.write("2DA V2.0")
        result.write(self.newline)

        num_adj = len(str(len(self.max)))

        if self.default:
            result.write("DEFAULT: %s" % self.default)

        result.write(self.newline)

        head = [s.ljust(m + 4) for s, m in itertools.izip(self.columns, self.max)]
        result.write(''.ljust(num_adj+4) + ''.join(head))
        result.write(self.newline)

        for i, r in enumerate(self.rows):
            result.write(str(i).ljust(num_adj + 4) + make_row(r, self.max))
            result.write(self.newline)

        return result

    def get_column_index(self, col):
        """Gets the column index from a column label.
        """

        if isinstance(col, str):
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

        lines = [l.strip() for l in iter(io.splitlines()) if l.strip() != '']

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
        self.max = [len(s) for s in self.columns]
        self.rows = [self.parse_row(r) for r in it]

    def parse_row(self, row, strip_row_number=True):
        """Parses a 2da row.  Currently this is implimented by using the
        Python shlex package which parses a superset of 2da row format.
        So it could parse things that are not legal 2da rows.
        """
        if strip_row_number:
            m = self.ROW_NUM_RE.match(row)
            if m: row = m.group(1)

        splitter = shlex.shlex(row, posix=False)
        splitter.whitespace_split = True
        lst = list(splitter)

        self.max = max_array(self.max, [len(s) for s in lst])

        return lst

    def set(self, row, col, val):
        """Sets a 2da entry by row and column label or column index.
        The value passed is automatically coerced to str.
        """

        col = self.get_column_index(col)
        self.rows[row][col] = str(val)

    def write_to(io):
        pass
