import math


class InvalidInputError(Exception):
    pass

class CodingError(Exception):
    pass

def all_are_close(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(math.isclose(first, x) for x in iterator)
