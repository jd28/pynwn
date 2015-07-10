class TwoDXMerger:
    def __init__(self, twoda, twodx, default=None):
        self.twoda = twoda
        self.twodx = twodx
        self.default = default

    def merge(self):
        highest = 0
        nrows = len(self.twoda.rows)
        for r in self.twodx.rows:
            if r[0] == "#":
                r[0] = nrows
                nrows += 1

        for r in self.twodx.rows:
            highest = max(highest, int(r[0]))

        if highest > 0 and highest >= len(self.twoda.rows):
            self.twoda.add_padding(len(self.twoda.rows), highest)

        for c in self.twodx.columns[1:]:
            if not self.twoda.has_column(c):
                self.twoda.add_column(c)

        for r in self.twodx.rows:
            row = int(r[0])
            for c in self.twodx.columns[1:]:
                col = self.twodx.get_column_index(c)
                new = r[col]
                if new == '####': continue
                if (self.default
                    and row < len(self.default.rows)
                    and self.default.get_column_index(c) >= 0):
                    orig = self.default.get(row, c)
                    cur  = self.twoda.get(row, c)
                    if orig == cur:
                        self.twoda.set(row, c, new)
                else:
                    self.twoda.set(row, c, new)

        if 'column_rename' in self.twodx.metadata:
          for old, new in self.twodx.metadata['column_rename'].items():
            old = old.lower()
            for i, col in enumerate(self.twoda.columns):
              if col.lower() == old:
                self.twoda.columns[i] = new
                break
