from pynwn.gff import Gff, GffElement
import pprint

VARIABLE_TYPE_INT      = 1
VARIABLE_TYPE_FLOAT    = 2
VARIABLE_TYPE_STRING   = 3
VARIABLE_TYPE_OBJECT   = 4
VARIABLE_TYPE_LOCATION = 5

def convert(vartype, val):
    if vartype == VARIABLE_TYPE_INT: return int(val)
    elif vartype == VARIABLE_TYPE_FLOAT: return float(val)
    elif vartype == VARIABLE_TYPE_STRING: return str(val)
    elif vartype == VARIABLE_TYPE_OBJECT: return int(val)
    #elif vartype == VARIABLE_TYPE_LOCATION: return 'location'
    else:
        raise ValueError("Unable to convert type to type name: %d" % vartype)

# not sure what the type names for object and location are...
def get_name(vartype):
    if vartype == VARIABLE_TYPE_INT: return 'int'
    elif vartype == VARIABLE_TYPE_FLOAT: return 'float'
    elif vartype == VARIABLE_TYPE_STRING: return 'cexostring'
    #elif vartype == VARIABLE_TYPE_OBJECT: return 'object'
    #elif vartype == VARIABLE_TYPE_LOCATION: return 'location'
    else:
        raise ValueError("Unable to convert type to type name: %d" % vartype)

class NWVariable(object):
    """NWVariable abstracts over a particular type of local variable type.
    Currently it can only access values, not set them.
    """
    def __init__(self, gff_struct, var_type, default):
        self.gff = gff_struct
        self.type = var_type
        self.default = default

        if isinstance(self.gff, Gff):
            self.has_vars = self.gff.has_field('VarTable')
        else:
            self.has_vars = 'VarTable' in self.gff.val

    def __getitem__(self, name):
        if not self.has_vars: return self.default
        vs = self.gff['VarTable']
        res = [v['Value'] for v in vs if v['Type'] == self.type and v['Name'] == name]
        if len(res) == 0: return self.default

        return res[0]

    def __setitem__(self, name, value):
        if not self.has_vars:
            if isinstance(self.gff, Gff):
                self.gff.structure['VarTable'] = GffElement('list', [], -1, self.gff)
            else:
                self.gff.val['VarTable'] = GffElement('list', [], -1, self.gff)

        if self.has_var(name):
            v = self.get_var(name)
            v['Value'] = convert(self.type, value)
        else:
            res = GffElement(0,
                             {'Type': GffElement('dword', self.type, -1, self.gff),
                              'Name': GffElement('cexostring', name, -1, self.gff),
                              'Value': GffElement(get_name(self.type),
                                                  convert(self.type, value),
                                                  -1, self.gff)},
                            0, self.gff)

            self.gff['VarTable'].append(res)


    def get_var(self, name):
        vs = self.gff['VarTable']
        res = [v for v in vs if v['Type'] == self.type and v['Name'] == name]
        if len(res) == 0:
            raise ValueError("Variable Table has no variable with name %s for type %d" % (name, self.type))
        else:
            return res[0]

    def has_var(self, name):
        if not self.has_vars: return False

        vs = self.gff['VarTable']
        res = [v for v in vs if v['Type'] == self.type and v['Name'] == name]
        return len(res) > 0

    def list_vars(self):
        if not self.has_vars: return []

        vs = self.gff['VarTable']
        res = [(v['Name'], v['Value']) for v in vs if v['Type'] == self.type]
        return res

class NWObjectVarable(object):
    """NWObjectVarable is an interface for other objects to inherit the ability to \
    read / write local variables stored in a GFF.
    """

    def __init__(self, gff_struct):
        self.gff = gff_struct
        self._floats = None
        self._ints = None
        self._objs = None
        self._locs = None
        self._strings = None

    @property
    def local_floats(self):
        if self._floats: return self._floats

        self._floats = NWVariable(self.gff, VARIABLE_TYPE_FLOAT, 0.0)
        return self._floats

    @property
    def local_ints(self):
        if self._ints: return self._ints

        self._ints = NWVariable(self.gff, VARIABLE_TYPE_INT, 0)
        return self._ints

    @property
    def local_locations(self):
        if self._locs: return self._locs

        self._locs = NWVariable(self.gff, VARIABLE_TYPE_LOCATION, 0)
        return self._locs

    @property
    def local_strings(self):
        if self._strings: return self._strings

        self._strings = NWVariable(self.gff, VARIABLE_TYPE_STRING, '')
        return self._strings
