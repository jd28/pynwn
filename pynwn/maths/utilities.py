'''Simple utility functions that should really be in a C module'''

import math
import numpy
import vector

def rotMatrix( (x,y,z,a) ):
    """Given rotation as x,y,z,a (a in radians), return rotation matrix

    Returns a 4x4 rotation matrix for the given rotation,
    the matrix is a Numeric Python array.

    x,y,z should be a unit vector.
    """
    c = math.cos(a)
    s = math.sin(a)
    t = 1-c
    R = numpy.array( [
        [t*x*x+c,   t*x*y+s*z, t*x*z-s*y, 0],
        [t*x*y-s*z, t*y*y+c,   t*y*z+s*x, 0],
        [t*x*z+s*y, t*y*z-s*x, t*z*z+c,   0],
        [0,         0,         0,         1]
    ])
    return R

def crossProduct( first, second ):
    """Given 2 4-item vectors, return the cross product as a 4-item vector"""
    x,y,z = vector.crossProduct( first, second )[0]
    return [x,y,z,0]

def magnitude( vector ):
    """Given a 3 or 4-item vector, return the vector's magnitude"""
    return vector.magnitude( vector[:3] )[0]

def normalise(xs):
    """Given a 3 or 4-item vector, return a 3-item unit vector"""
    return vector.normalise(xs[:3])[0]

def pointNormal2Plane( point, normal ):
    """Create parametric equation of plane from point and normal
    """
    point = numpy.asarray(point,'d')
    normal = normalise(normal)
    result = zeros((4,),'d')
    result[:3] = normal
    result[3] = - dot(normal, point)
    return result

def plane2PointNormal( (a,b,c,d) ):
    """Get a point and normal from a plane equation"""
    return numpy.asarray((-d*a,-d*b,-d*c), 'd'), numpy.asarray((a,b,c), 'd')

if __name__ == "__main__":
    for p, n in [([0,1,0], [0,-1,0]),
                 ([1,0,0], [1,0,0]),
                 ([0,0,1], [0,0,1])]:
        plane = pointNormal2Plane(p,n)
        print 'plane', plane
        p1,n1 = plane2PointNormal(plane)
        print 'p', p, p1
        print 'n', n, n1
        assert allclose(p, p1)
        assert allclose(n, n1)
