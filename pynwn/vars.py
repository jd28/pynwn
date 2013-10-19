from pynwn.file.gff import Gff
from pynwn.nwn.types import *

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
    def __init__(self, parent_obj, gff_struct, var_type, class_type, default):
        self.parent_obj = parent_obj
        self.gff        = gff_struct
        self.type       = var_type
        self.class_type = class_type
        self.default    = default

    def has_vars(self):
        return self.gff.has_field('VarTable')

    def __getitem__(self, name):
        if not self.has_vars: return self.default
        v = self.get_var(name)
        if v is None:
            return default
        else:
            return v['Value'].val

    def __setitem__(self, name, value):
        if not self.has_vars():
            self.gff.add_field('VarTable', [])

        if self.has_var(name):
            v = self.get_var(name)
            v['Value'] = self.class_type(value)
        else:
            res = { '_STRUCT_TYPE_' : 0,
                    'Type' : NWDword(self.type),
                    'Name' : NWString(name),
                    'Value' : self.class_type(value) }

            self.gff['VarTable'].append(res)
        self.parent_obj.stage()

    def get_var(self, name):
        vs = self.gff['VarTable']
        res = []
        for v in vs:
            if v['Type'].val == self.type and v['Name'].val == name:
                return v

        return None

    def has_var(self, name):
        return not self.get_var(name) is None

    def list_vars(self):
        if not self.has_vars: return []
        vs = self.gff['VarTable']
        res = []
        for v in vs:
            if v['Type'].val == self.type:
                res.append((v['Name'].val, v['Value'].val))

        return res

class NWObjectVarable(object):
    """NWObjectVarable is an interface for other objects to
    read / write local variables stored in a GFF.
    """

    def __init__(self, parent_obj, gff_struct):
        self.gff = gff_struct
        self.parent_obj = parent_obj
        self._floats = None
        self._ints = None
        self._objs = None
        self._locs = None
        self._strings = None

    @property
    def local_floats(self):
        if self._floats: return self._floats

        self._floats = NWVariable(self, self.gff, VARIABLE_TYPE_FLOAT, NWFloat, 0.0)
        return self._floats

    @property
    def local_ints(self):
        if self._ints: return self._ints

        self._ints = NWVariable(self, self.gff, VARIABLE_TYPE_INT, NWInt, 0)
        return self._ints

    @property
    def local_locations(self):
        if self._locs: return self._locs

        self._locs = NWVariable(self, self.gff, VARIABLE_TYPE_LOCATION, None, 0)
        return self._locs

    @property
    def local_strings(self):
        if self._strings: return self._strings

        self._strings = NWVariable(self, self.gff, VARIABLE_TYPE_STRING, NWString, '')
        return self._strings
