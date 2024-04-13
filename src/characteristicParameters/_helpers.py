import math

class InvalidInputError(Exception):
    pass

def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(math.isclose(first, x) for x in iterator)


