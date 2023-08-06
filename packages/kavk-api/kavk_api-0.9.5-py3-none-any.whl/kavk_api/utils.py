from random import randint

def get_random_id() -> int:
    return randint(-2**31, (2**31)-1)

class DotDict(dict):
    """
    https://stackoverflow.com/questions/13520421/recursive-dotdict
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


__all__ = ('get_random_id', 'DotDict')
