# from NEVEREDIT...

import sys, math, copy
import numpy

from pynwn.model import Controller, Node, Model
from pynwn.maths import utilities
from pynwn.maths.quaternion import Quaternion
from pynwn.util.binary_reader import BinaryReader as BinReader

def read_array(f):
    return (BinReader.u32(f) + 0xC,
            BinReader.u32(f),
            BinReader.u32(f))

class BinaryMDL(object):
    def __init__(self, f):
        self.raw_offset = 0
        self.raw_size = 0
        self.total_size = 0
        self.file = f
        self.model = Model()

    def read(self, f):
        self.raw_offset = BinReader.u32(f)
        self.raw_size = BinReader.u32(f)

        self.geometry_header = GeometryHeader.from_file(f)

        f.seek(2,1)

        classification = BinReader.u8(f)
        if classification == 0x01:
            self.model.classification = "Effect"
        elif classification == 0x02:
            self.model.classification = "Tile"
        elif classification == 0x04:
            self.model.classification = "Character"
        elif classification == 0x08:
            self.model.classification = "Door"
        else:
            print "unknown model classification:",classification
            self.model.classification = "None"
            # this seems to include waypoint models

        self.model.fogged = BinReader.u8(f)
        f.seek(4,1)

        self.anim_header_ptrs = read_array(f)
        self.parent_ptr = BinReader.u32(f)

        self.model.bounding_box = numpy.array([BinReader.f32(f, 3),
                                               BinReader.f32(f, 3)])
        self.model.radius       = BinReader.f32(f)
        self.model.anim_scale   = BinReader.f32(f)
        s  = BinReader.str(f, 64)
        self.super_model_name  = s[:s.find('\0')]
        #print 'supermodel:', self.super_model_name

        self.model.node_count = self.geometry_header.node_count
        offset = self.geometry_header.root_node_offset
        self.model.root_node = Node.from_file(self, offset)
        return self.model

class GeometryHeader:
    def __init__(self):
        self.name = ''
        self.root_node_offset = 0
        self.node_count = 0
        self.ref_count = 0
        self.type = 0

    @staticmethod
    def from_file(f):
        gh = GeometryHeader()
        f.seek(8,1)

        s = BinReader.str(f, 64)
        gh.name = s[:s.find('\0')]
        #print 'name:',self.name

        gh.root_node_offset = BinReader.u32(f) + 0xC
        gh.node_count = BinReader.u32(f)
        f.seek(24,1)
        gh.ref_count = BinReader.u32(f)
        gh.type = BinReader.u8(f)
        f.seek(3,1)

        return gh

class ASCIIModel(object):
    def __init__(self):
        self.model = Model()

    def read(self, f):
        line = f.readline()
        nodes = {}
        firstNode = True
        while line:
            parts = line.split()
            if not parts:
                line = f.readline()
                continue
            if parts[0] == 'classification':
                s = parts[1]
                s = s[:1].upper() + s[1:].lower()
                self.model.classification = s
            if parts[0] == 'setsupermodel':
                self.super_model_name = parts[2]
                #print self.super_model_name
            elif parts[0] == 'node':
                n = self.read_node(parts[1],parts[2],nodes,f)
                self.model.node_count += 1
                if firstNode:
                    self.model.root_node = n
                    firstNode = False
                nodes[n.name] = n
            elif parts[0] == 'newmodel':
                self.name = parts[1]
            line = f.readline()
        return self.model

    def read_node(self, type, name, nodes, f):
        n = Node()
        if type == 'dummy':
            n.flags |= 0x1
        elif type == 'reference':
            n.flags |= 0x11
        elif type == 'trimesh':
            n.flags |= 0x21
        elif type == 'light':
            n.flags |= 0x3
        elif type == 'emitter':
            n.flags |= 0x5
        elif type == 'skinmesh':
            n.flags |= 0x61
        elif type == 'animmesh':
            n.flags |= 0xa1
        elif type == 'danglymesh':
            n.flags |= 0x121
        elif type == 'aabb':
            n.flags |= 0x221
        else:
            print 'Unknown node type:',type

        n.name = name
        n.faces = None
        n.vertices = []
        
        parts = f.readline().split()
        while parts[0] != 'endnode':
            if parts[0] == 'parent':
                if parts[1] in nodes:
                    nodes[parts[1]].children.append(n)
                elif parts[1] != 'NULL':
                    print 'cannot find parent node for',n.name,':',parts[1]
            elif parts[0] == 'ambient':
                n.ambient_colour = [float(parts[1]), float(parts[2]),
                                    float(parts[3])]
            elif parts[0] == 'diffuse':
                n.diffuse_colour = [float(parts[1]),float(parts[2]),
                                    float(parts[3])]
            elif parts[0] == 'specular':
                n.specular_colour = [float(parts[1]),float(parts[2]),
                                     float(parts[3])]
            elif parts[0] == 'shininess':
                n.shininess = float(parts[1])
            elif parts[0] == 'bitmap':
                n.texture_names = [parts[1], '', '', '']
            elif parts[0] in Controller.types:
                c = Controller()
                c.type = parts[0]
                if parts[0] == 'position':
                    c.columns = 3
                    c.data = [float(parts[1]),float(parts[2]),float(parts[3])]
                elif parts[0] == 'alpha':
                    c.columns = 1
                    c.data = [float(parts[1])]
                elif parts[0] == 'orientation':
                    c.columns = 4
                    c.data = [float(parts[1]), float(parts[2]),
                              float(parts[3]), float(parts[4])]
                    if c.data[0] == c.data[1] == c.data[2] == c.data[3] == 0.0:
                        #this is strange. in ASCII models they seem to specify
                        #quaternions with elements all 0?
                        c.data[3] = 1.0
                    quat = copy.copy(c.data)
                    quat.insert(0,quat.pop())
                    q = Quaternion(quat)
                    c.rotationMatrix = q.matrix
                elif parts[0] == 'scale':
                    c.columns = 1
                    c.data = [float(parts[1])]
                n.add_controller(c)
            elif parts[0] == 'verts':
                num = int(parts[1])
                n.vertices = []
                for i in xrange(num):
                    n.vertices.append(numpy.array([float(val)
                                                     for val
                                                     in f.readline().split()]))
            elif parts[0] == 'faces':
                num = int(parts[1])
                n.faces = []
                for i in xrange(num):
                    face = [int(val)
                         for val in f.readline().split()]
                    n.faces.append([face[:3],face[3],face[4:7],face[7]])
            elif parts[0] == 'tverts':
                num = int(parts[1])
                n.texture0_vertices = []
                for i in xrange(num):
                    n.texture0_vertices.append([float(val)
                                               for val
                                               in f.readline().split()][:2])
            parts = f.readline().split()
        if n.faces:
            n.vertex_index_lists = [[]]
            n.normals = []
            for f in n.faces:
                points = [n.vertices[i] for i in f[0]]
                n.vertex_index_lists[0].extend(f[0])
                #tpoints = [n.texture0Vertices[i] for i in f[2]]
                normal = numpy.array(utilities.crossProduct(points[2]
                                                            -points[1],
                                                            points[0]
                                                            -points[1]))
                normal /= math.sqrt(numpy.dot(normal,normal))
                n.normals.append(normal)

        return n

class MDLFile(object):
    def __init__(self):
        pass

    @staticmethod
    def from_file(f):
        if BinReader.u32(f) == 0:
            model  = BinaryMDL(f).read(f)
        else:
            model  = ASCIIModel().read(f)
            model.recalculate_bounding_boxes()
        #print 'recalculated bounding box for', model.root_node.name, model.bounding_box
        return model


if __name__ == '__main__':
    mdl = MDLFile()
    f = open(sys.argv[1],'rb')
    model = mdl.from_file(f)
    print model.get_name()
    print model
    print model.get_textures()
