import sys, math
import numpy

from pynwn.maths.quaternion import Quaternion
from pynwn.util.binary_reader import BinaryReader as BinReader
from pynwn.util.helper import chunks

def read_array(f):
    return (BinReader.u32(f) + 0xC,
            BinReader.u32(f),
            BinReader.u32(f))

class Controller:
    types = {
        'position'             : 8,
        'orientation'          : 20,
        'scale'                : 36,
        'color'                : 76,
        'radius'               : 88,
        'shadowradius'         : 96,
        'verticaldisplacement' : 100,
        'multiplier'           : 140,
        'alphaend'             : 80,
        'alphastart'           : 84,
        'birthrate'            : 88,
        'bounce_co'            : 92,
        'colorend'             : 96,
        'colorstart'           : 108,
        'combinetime'          : 120,
        'drag'                 : 124,
        'fps'                  : 128,
        'frameend'             : 132,
        'framestart'           : 136,
        'grav'                 : 140,
        'lifeexp'              : 144,
        'mass'                 : 148,
        'p2p_bezier2'          : 152,
        'p2p_bezier3'          : 156,
        'particlerot'          : 160,
        'randvel'              : 164,
        'sizestart'            : 168,
        'sizeend'              : 172,
        'sizestart_y'          : 176,
        'sizeend_y'            : 180,
        'spread'               : 184,
        'threshold'            : 188,
        'velocity'             : 192,
        'xsize'                : 196,
        'ysize'                : 200,
        'blurlength'           : 204,
        'lightningdelay'       : 208,
        'lightningradius'      : 212,
        'lightningscale'       : 216,
        'detonate'             : 228,
        'alphamid'             : 464,
        'colormid'             : 468,
        'percentstart'         : 480,
        'percentmid'           : 481,
        'percentend'           : 482,
        'sizemid'              : 484,
        'sizemid_y'            : 488,
        'selfillumcolor'       : 100,
        'alpha'                : 128
    }

    type_ids = dict(zip(types.values(),types.keys()))

    def __init__(self):
        self.data = []
        self.keys = []
        self.type = ''
        self.columns = 0
        self.rows = 0
        self.time_index = 0
        self.data_index = 0
        self.rotationMatrix = []

    @staticmethod
    def from_file(f, data):
        cont = Controller()

        # Header
        t = BinReader.u32(f)

        if not t in Controller.type_ids:
            print 'warning, unknown node controller type', t
        else:
            cont.type = Controller.type_ids[t]

        cont.rows       = BinReader.u16(f)
        cont.time_index = BinReader.u16(f)
        cont.data_index = BinReader.u16(f)
        cont.columns    = BinReader.u8(f)
        f.seek(1,1)

        # Data
        end = cont.data_index + cont.rows * cont.columns
        cont.data = data[cont.data_index:end]
        cont.keys = data[end:end + cont.rows]

        if cont.type == 'orientation':
            quat = list(cont.getValue())
            quat.insert(0,quat.pop())
            q = Quaternion(quat)
            cont.rotationMatrix = q.matrix

        return cont

    def getTimeKeys(self):
        return self.keys

    def getValue(self, i = 0):
        start = self.columns * i
        stop  = start + self.columns + 1
        return self.data[start : stop]

class Node:
    indent = 0
    def __init__(self):
        self.texture_names = []
        self.flags = 0L
        self.name = ''
        self.children = []
        self.controllers = {}
        self.alpha = 1.0
        self.normals = []
        self.position = None
        self.scale = None
        self.orientation = None
        self.bounding_box = numpy.array([3*[0.0],3*[0.0]])
        self.shininess = None
        self.ambientColour = None
        self.diffuseColour = None
        self.specularColour = None
        self.faces = None
        self.vertex_index_lists = None
        self.inheritColour = None
        self.nodeNumber = None

        self.parentGeomPointer = None
        self.parentNodePointer = None
        self.childrenArray = None
        self.controllerKeysArray = None
        self.controllerVArray = None

    def getName(self):
        return self.name

    @staticmethod
    def from_file(mdl, offset):
        n = Node()
        n.parent_mdl = mdl

        f = mdl.file
        f.seek(offset)

        # header
        f.seek(24,1)
        n.inherit_colour  = BinReader.u32(f)
        n.node_number     = BinReader.u32(f)
        n.name            = BinReader.str(f, 32)
        n.name            = n.name[:n.name.find('\0')]
        n.parent_geom_ptr = BinReader.u32(f)
        n.parent_node_ptr = BinReader.u32(f)
        n.child_array     = read_array(f)
        n.cont_key_array  = read_array(f)
        n.cont_val_array  = read_array(f)
        n.flags = BinReader.u32(f)

        if n.has_mesh():
            Node.read_mesh_header(n, f)

        Node.read_children(n, f)
        Node.read_controllers(n, f)

        return n

    @staticmethod
    def read_children(node, f):
        f.seek(node.child_array[0])
        child_offsets = BinReader.u32(f, node.child_array[1])
        if node.child_array[1] == 1:
            child_offsets = [child_offsets + 0xC]
        else:
            child_offsets = [p + 0xC for p in child_offsets]

        node.children = []

        for o in child_offsets:
            node.children.append(Node.from_file(node.parent_mdl, o))

        node.child_array = None

    @staticmethod
    def read_controllers(node, f):
        f.seek(node.cont_val_array[0])
        data = BinReader.f32(f, node.cont_val_array[1])

        f.seek(node.cont_key_array[0])
        node.controllers = {}
        for i in xrange(node.cont_key_array[1]):
            node.add_controller(Controller.from_file(f, data))

        if node.has_mesh():
            node.ambient_colour += [node.alpha]
            node.diffuse_colour += [node.alpha]
            node.specular_colour += [node.alpha]

    def add_controller(self, c):
        ctype = c.type
        if ctype not in self.controllers:
            self.controllers[ctype] = [c]
        else:
            self.controllers[ctype].append(c)

        if ctype == 'alpha':
            self.alpha = c.getValue(0)[0]
        elif ctype == 'position':
            self.position = c.getValue()
        elif ctype == 'orientation':
            self.orientation = c.rotationMatrix
        elif ctype == 'scale':
            self.scale = c.getValue()[0]

    def has_controller(self, ctype):
        return ctype in self.controllers

    def get_controllers(self, ctype):
        return self.controllers.get(ctype, [])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        def type_to_str(node):
            sl = []
            if self.is_dummy():
                sl.append("Dummy")
            if self.is_light():
                sl.append("Light")
            if self.is_emitter():
                sl.append("Emitter")
            if self.is_reference():
                sl.append("Reference")
            if self.is_trimesh():
                sl.append("Tri")
            if self.is_skinmesh():
                sl.append("Skin")
            if self.is_animmesh():
                sl.append("Anim")
            if self.is_danglymesh():
                sl.append("Dangly")
            if self.is_aabbmesh():
                sl.append("AABB")
            if self.has_mesh():
                sl.append("Mesh")
            return '-'.join(sl)


        def cont_to_str(node):
            strings = []
            for cl in node.controllers.values():
                for c in cl:
                    strings.append(c.type)
            return '-'.join(strings)

        def helper(node, strings):
            s = Node.indent * ' '
            s += '"%s" %s (%s)' % (node.name, type_to_str(node), cont_to_str(node))
            strings.append(s)
            Node.indent += 4
            for c in node.children:
                helper(c, strings)
            Node.indent -= 4

        strings = []
        helper(self, strings)
        return '\n'.join(strings)

    def get_textures(self):
        def helper(node):
            res = set(node.texture_names)
            for c in node.children:
                res = res | helper(c)
            return res

        result = helper(self)
        return result

    @staticmethod
    def read_mesh_header(node, f):
        f.seek(8,1)
        node.face_array = read_array(f)
        values = BinReader.u32(f, 20)
        node.bounding_box = numpy.array([values[0:3],values[3:6]])
        node.alpha = 1.0 #changeable via controller
        node.radius = values[6]
        node.center_of_mass = values[7:10]
        node.diffuse_colour = list(values[10:13])
        node.ambient_colour = list(values[13:16])
        node.specular_colour = list(values[16:19])
        node.shininess = values[19]

        node.shadow_flag,  \
        node.beaming_flag, \
        node.render_flag,  \
        node.transparency_hint = BinReader.u32(f, 4)

        node.texture_names = []
        f.seek(4,1)
        s = BinReader.str(f, 64)
        node.texture_names.append(s[:s.find('\0')])

        s = BinReader.str(f, 64)
        node.texture_names.append(s[:s.find('\0')])

        s = BinReader.str(f, 64)
        node.texture_names.append(s[:s.find('\0')])

        s = BinReader.str(f, 64)
        node.texture_names.append(s[:s.find('\0')])

        node.tile_fade = BinReader.u32(f)
        f.seek(24,1)
        node.vertex_index_count = read_array(f)
        node.raw_vertex_offsets = read_array(f)
        f.seek(8,1)
        node.triangle_mode = BinReader.u8(f)
        f.seek(7,1)

        node.raw_vertex_ptr = BinReader.u32(f)
        node.vertex_count  = BinReader.u16(f)
        node.texture_count = BinReader.u16(f)

        node.texure_vertex_ptrs = list(BinReader.u32(f, 4))
        node.vertex_normal_ptr = BinReader.u32(f)

        # raw data offset
        raw_offset = node.parent_mdl.raw_offset

        if node.raw_vertex_ptr != 0xFFFFFFFFL:
            f.seek(raw_offset + node.raw_vertex_ptr + 0xC)
            b = f.read(node.vertex_count * 12)
            node.vertices = [BinReader.f32(chunk, 3)
                             for chunk in chunks(b, 12)]
        else:
            node.vertices = []

        if node.vertex_normal_ptr != 0xFFFFFFFFL:
            f.seek(node.vertex_normal_ptr + 0xC + raw_offset)
            node.normals = [BinReader.f32(f, 3)
                            for i in xrange(node.vertex_count)]
        else:
            node.normals = []

        if node.texure_vertex_ptrs[0] != 0xFFFFFFFFL:
            f.seek(raw_offset + node.texure_vertex_ptrs[0] + 0xC)
            node.texture0_vertices = [BinReader.f32(f, 2)
                                      for i in xrange(node.vertex_count)]
        else:
            node.texture0_vertices = []

        f.seek(node.raw_vertex_offsets[0])
        pointers = BinReader.u32(f, node.raw_vertex_offsets[1])
        if node.raw_vertex_offsets[1] == 1:
            pointers = [pointers]
        else:
            pointers = list(pointers)

        f.seek(node.vertex_index_count[0])
        lengths = BinReader.u32(f, node.vertex_index_count[1])
        if node.vertex_index_count[1] == 1:
            lengths = [lengths]
        else:
            lengths = list(lengths)

        node.vertex_index_lists = []
        for p, l in zip(pointers, lengths):
            f.seek(raw_offset + p + 0xC)
            node.vertex_index_lists.append(BinReader.u16(f))

        #print 'vertexIndexList for node', node.name, node.vertex_index_lists

    def max_bounding_box(self, nodelist):
        self.bounding_box = numpy.array([3 * [float(sys.maxint)],
                                         3 * [-float(sys.maxint)]])
        for n in nodelist:
            for i in range(3):
                if n.bounding_box[0][i] < self.bounding_box[0][i]:
                    self.bounding_box[0][i] = n.bounding_box[0][i]
                if n.bounding_box[1][i] > self.bounding_box[1][i]:
                    self.bounding_box[1][i] = n.bounding_box[1][i]

    def recalculate_bounding_box(self):
        if not self.is_trimesh():
            self.max_bounding_box(self.children)
        else:
            self.bounding_box = numpy.array([3 * [float(sys.maxint)],
                                             3 * [-float(sys.maxint)]])
            for v in self.vertices:
                for i in range(3):
                    if v[i] < self.bounding_box[0][i]:
                        self.bounding_box[0][i] = v[i]
                    if v[i] > self.bounding_box[1][i]:
                        self.bounding_box[1][i] = v[i]

        self.bounding_sphere = [[0,0,0],0]
        self.bounding_sphere[0] = (self.bounding_box[1] + self.bounding_box[0]) / 2.0
        r = self.bounding_box[0] - self.bounding_sphere[0]
        r = numpy.dot(r,r)
        self.bounding_sphere[1] = math.sqrt(r)

    def is_dummy(self):
        return self.flags == 0x1

    def is_light(self):
        return self.flags == 0x3

    def is_emitter(self):
        return self.flags == 0x5

    def is_reference(self):
        return self.flags == 0x11

    def is_trimesh(self):
        return self.flags == 0x21

    def is_skinmesh(self):
        return self.flags == 0x61

    def is_animmesh(self):
        return self.flags == 0xA1

    def is_danglymesh(self):
        return self.flags == 0x121

    def is_aabbmesh(self):
        return self.flags == 0x221

    def has_anim(self):
        return self.flags & 0x80

    def has_mesh(self):
        return self.flags & 0x20

    def has_dangly(self):
        return self.flags & 0x120

    def has_skin(self):
        return self.flags & 0x40

class Model:
    def __init__(self):
        self.classification = "Unknown"
        self.root_node = None
        self.bounding_box = numpy.array([[0.0,0.0,0.0],[1.0,1.0,1.0]])
        self.valid_nounding_box = False
        self.anim_scale = 1.0
        self.node_count = 0
        self.preprocessed = False

    def get_name(self):
        return self.root_node.name

    def recalculate_bounding_boxes(self):
        def helper(node):
            node.recalculate_bounding_box()
            for n in node.children:
                helper(n)

        helper(self.root_node)

    def setPreprocessed(self,p):
        self.preprocessed = p

    def getPreprocessed(self):
        return self.preprocessed

    def get_textures(self):
        s = self.root_node.get_textures()
        s.remove('')
        return s

    def __str__(self):
        strings = []
        strings.append('class: %s' % self.classification)
        strings.append('bbox: %s' % str(self.bounding_box))
        strings.append('Anim Scale: %d' % self.anim_scale)
        if self.root_node:
            strings.append(str(self.root_node))
        return '\n'.join(strings)

    def __repr__(self):
        return self.__str__()
