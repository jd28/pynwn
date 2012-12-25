def chunks(l, n):
    """Cut a slicable object into N length pieces.
    """
    return [l[i:i+n] for i in range(0, len(l), n)]

def convert_to_number(val):
    """Attempts to coerce value to int, if that fails float, and if
    that fails it returns the original value.
    """
    try:
        return int(val)
    except:
        try:
            return float(val)
        except:
            return val
