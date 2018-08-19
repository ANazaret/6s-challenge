import numpy as np
from decorator import decorator, decorate


@decorator
def tuplify(func, *args, **kwargs):
    return (func(*args, **kwargs),)


def register(func, *args, **kwargs):
    """Annotate the function as 'operator' for core module"""
    func.__annotations__['operator'] = True
    return decorate(func, lambda f, *args, **kwargs: f(*args, **kwargs))


def protect(min_output=None,
            max_output=None,
            min_input=None,
            max_input=None,
            integer_input=None,
            integer_output=None,
            nonzero_input=None,
            nonnan_output=None):
    @decorator
    def annotation(func, *args, **kwargs):
        check("min_input", lambda x: x >= min_input, args, min_input)
        check("max_input", lambda x: x <= max_input, args, max_input)
        check("integer_input", lambda x: type(x) == int or x.is_integer(), args, integer_input)
        check("nonzero_input", lambda x: x != 0, args, nonzero_input)

        res = func(*args, **kwargs)

        check("integer_output", lambda x: type(x) == int or x.is_integer(), res, integer_output)
        check("min_output", lambda x: x >= min_output, res, min_output)
        check("max_output", lambda x: x <= max_output, res, max_output)
        check("nonnan_output", lambda x: not np.isnan(x), res, nonzero_input)

        if integer_output:
            res = tuple([int(x) for x in res])
        return res

    return annotation


class ProtectionException(Exception):
    def __init__(self, msg):
        self.msg: str = msg

    def __str__(self):
        return self.msg


def check(name, condition, data, test_none):
    if test_none is None:
        return
    for v in data:
        if not condition(v):
            raise ProtectionException(
                'Protection "%s(%s)" activated - Value %s in %s is illegal' % (name, test_none, repr(v), repr(data)))


def memoize_fibonacci(f):
    f.cache = dict([(0, 0), (1, 1)])

    def aux(func, key):
        cache = func.cache
        if key not in cache:
            cache[key] = func(key)
        return cache[key]

    return decorate(f, aux)
