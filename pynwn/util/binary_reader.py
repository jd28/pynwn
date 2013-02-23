import struct

class BinaryReader(object):
    @staticmethod
    def unpack(pattern, buf, count = 1, endian = '<'):
        pattern = pattern * count

        # If not a string assume IO object.
        if not isinstance(buf, str):
            size = struct.calcsize(pattern)
            buf  = buf.read(size)

        pattern = endian + pattern
        result = struct.unpack(pattern, buf)
        # Don't return a single element tuble.
        return result[0] if count == 1 else result

    @staticmethod
    def char(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('c', buf, count)

    @staticmethod
    def i8(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('b', buf, count)

    @staticmethod
    def u8(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('B', buf, count)

    @staticmethod
    def i16(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('h', buf, count)

    @staticmethod
    def u16(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('H', buf, count)

    @staticmethod
    def i32(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('i', buf, count)

    @staticmethod
    def u32(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('I', buf, count)

    @staticmethod
    def i64(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('q', buf, count)

    @staticmethod
    def u64(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('Q', buf, count)

    @staticmethod
    def f32(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('f', buf, count)

    @staticmethod
    def f64(buf, count = 1, endian = '<'):
        return BinaryReader.unpack('d', buf, count)

    @staticmethod
    def str(buf, count = 1, endian = '<'):
        """String is needs to be extracted from tuple"""
        result = BinaryReader.unpack('%ds' % count, buf, 1)
        return result
