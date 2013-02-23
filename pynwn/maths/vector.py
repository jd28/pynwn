"""Utilities for processing arrays of vectors"""
import numpy
numpy.seterr(divide='raise', invalid='raise')

def crossProduct(set1, set2):
    """Compute element-wise cross-product of two arrays of vectors.

       I{set1, set2} -- sequence objects with 1 or more
       3-item vector values.  If both sets are
       longer than 1 vector, they must be the same
       length.

       returns a double array with x elements,
       where x is the number of 3-element vectors
       in the longer set
    """
    set1 = numpy.asarray( set1, 'd')
    set1 = numpy.reshape( set1, (-1, 3))
    set2 = numpy.asarray( set2, 'd')
    set2 = numpy.reshape( set2, (-1, 3))
    ux = set1[:, 0]
    uy = set1[:, 1]
    uz = set1[:, 2]
    vx = set2[:, 0]
    vy = set2[:, 1]
    vz = set2[:, 2]
    result = numpy.zeros((len(set1), 3), 'd')
    result[:,0] = (uy*vz) - (uz*vy)
    result[:,1] = (uz*vx) - (ux*vz)
    result[:,2] = (ux*vy) - (uy*vx)
    return result

def crossProduct4( set1, set2 ):
    """Cross-product of 3D vectors stored in 4D arrays

    Identical to crossProduct otherwise.
    """
    set1 = numpy.asarray( set1, 'd')
    set1 = numpy.reshape( set1, (-1, 4))
    set2 = numpy.asarray( set2, 'd')
    set2 = numpy.reshape( set2, (-1, 4))
    ux = set1[:,0]
    uy = set1[:,1]
    uz = set1[:,2]
    vx = set2[:,0]
    vy = set2[:,1]
    vz = set2[:,2]
    result = numpy.zeros((len(set1), 4), 'd')
    result[:,0] = (uy*vz)-(uz*vy)
    result[:,1] = (uz*vx)-(ux*vz)
    result[:,2] = (ux*vy)-(uy*vx)
    return result


def magnitude( vectors ):
    """Calculate the magnitudes of the given vectors

    I{vectors} -- sequence object with 1 or more
    3-item vector values.

    @return: a double array with x elements,
             where x is the number of 3-element vectors
    """
    vectors = numpy.asarray(vectors, 'd')
    if (not (len(numpy.shape(vectors)) == 2 and
        numpy.shape(vectors)[1] in (3,4))):
        vectors = numpy.reshape( vectors, (-1,3))

    result = vectors * vectors
    result = numpy.sqrt(numpy.sum(result, axis=1))
    return result

def normalise( vectors ):
    """Get normalised versions of the vectors.

    I{vectors} -- sequence object with 1 or more
    3-item vector values.

    Will raise ZeroDivisionError if there are 0-magnitude
    vectors in the set.

    @return: a double array with x 3-element vectors,
             where x is the number of 3-element vectors in "vectors"
    """
    vectors = numpy.asarray( vectors, 'd')
    vectors = numpy.reshape( vectors, (-1,3))
    mags = numpy.reshape( magnitude( vectors ), (-1, 1))

    result = numpy.divide(vectors, mags)
    return result


if __name__ == "__main__":
    def test():

        data = numpy.array( [
                [0,0,0],[1,0,0],[0,1,0],
                [1,0,0],[0,0,0],[0,1,0],
        ],'d')
        print magnitude( data )

        try:
            normalise( data )
        except FloatingPointError as e:
            print e
        data = numpy.array( [
                [1,1,0],[1,0,0],[0,1,0],
                [1,0,1],[0,1,1],[1,1,0],
        ],'d')
        print normalise( data )
        print normalise( [2.0,2.0,0.0] )
        print crossProduct( data, [-1,0,0])
        print crossProduct( [0,0,1], [-1,0,0])
    test()
