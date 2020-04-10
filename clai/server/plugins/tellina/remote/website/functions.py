"""
Standard python package file with syntax comaptible with python3.5 and above.
"""

import collections
import inspect

from functools import partial, wraps


def first(coll): # rewrite to use frozen dict
    """Return the first item in a dictionary, list, or tuple."""
    if not coll:
        return None
    try:
        return dict((coll.items()[0],))
    except AttributeError:
        return coll[0]


def last(coll): # rewrite to use frozen dict
    """Return the last item in a dictionary, list, or tuple."""
    try:
        return dict((coll.items()[-1],))
    except AttributeError:
        return coll[-1]


def rest(coll): # rewrite to use frozen dict
    """Return the remaining items in a dictionary, list, or tuple."""
    try:
        return dict(coll.items()[1:])
    except AttributeError:
        return coll[1:]


def none(*args, **kwargs):
    return None


identity = lambda x: x


def is_seq(x):
    """Return True if x is iterable."""
    return (not hasattr(x, "strip") and
            hasattr(x, "__getitem__") or
            hasattr(x, "__iter__"))


def fmap(f, coll):
    """Apply a function to each item in a dictionary, list, or tuple."""
    try:
        return {k: f(v) for k, v in coll.iteritems()}
    except AttributeError:
        return tuple(f(v) for v in coll)


def walk(inner, outer, data):
    """Traverse an arbitrary data structure and apply a function to each node."""
    def process_node(inner, k, v):
        if not isinstance(v, collections.Iterable) or isinstance(v, basestring):
            return inner(k, v)
        if isinstance(v, collections.Sequence):
            rows = tuple(walk(inner, identity, row) for row in v)
            rv = tuple(filter(lambda row: row, rows))
        else:
            rv = walk(inner, identity, v)
        return (k, rv) if rv else None
    if isinstance(data, collections.Sequence):
        return outer(tuple(map(lambda x: walk(inner, identity, x), data)))
    nodes = tuple(map(lambda kv: process_node(inner, kv[0], kv[1]),
                      data.iteritems()))
    return outer(dict(filter(lambda node: node is not None, nodes)))


def cons(x, seq):
    """Return a tuple where x is the first element and seq is the rest."""
    return (x,) + tuple(seq)


def thread(x, form):
    if isinstance(form, tuple):
        f, args = first(form), rest(form)
        return f(x, *args)
    return form(x)


def threadfirst(x, form, *more):
    """Thread the expression through the forms."""
    if not more:
        return thread(x, form)
    return thread_first(*cons(thread(x, form), more))


def compose(*funcs):
    def compose2(f, g):
        if not callable(f):
            foo = partial(*f)
        else:
            foo = f
        if not callable(g):
            bar = partial(*g)
        else:
            bar = g
        return lambda x: foo(bar(x))
    return reduce(compose2, reversed(funcs))


def threadlast(x, *funcs):
    return compose(*funcs)(x)


def thread_first(x, form, *more):
    return threadfirst(x, form, *more)


def thread_last(x, *funcs):
    return threadlast(x, *funcs)


def memoize(f):
    """Return a memoized version of a function."""
    cache = {}

    @wraps(f)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        rv = f(*args)
        cache[args] = rv
        return rv
    return wrapper


def frozendict(*keyvals):
    """Return an immutable dictionary"""
    return frozenset(keyvals)


def zipdict(keys, vals):
    """Return an immutable dictionary with keys mapped to corresponding
    values"""
    return frozendict(*zip(keys, vals))


def get(fdict, key, default=None):
    """Return the value mapped to a key, default or None if key not present"""
    if fdict is None:
        return default
    try:
        return dict(fdict)[key]
    except KeyError:
        return default


def contains(fdict, key):
    return key in dict(fdict)


def find(fdict, key):
    try:
        return (key, dict(fdict)[key])
    except KeyError:
        return None


def keys(fdict):
    return tuple(dict(fdict).keys())


def vals(fdict):
    return tuple(dict(fdict).values())


def merge(*fdicts):
    """Merge two or more frozen dictionaries."""
    def items(fdict):
        return tuple(dict(fdict).items())
    if len(fdicts) == 2:
        return dict(items(first(fdicts)) + items(last(fdicts)))
    return merge(first(fdicts), apply(merge, rest(fdicts)))


def walk_replace(smap, data):
    def replace_at(k, v):
        if k in smap:
            return (smap[k], v)
        return (k, v)

    def process_node(k, v):
        if not isinstance(v, collections.Iterable) or isinstance(v, basestring):
            return replace_at(k, v)
        if isinstance(v, collections.Sequence):
            rows = ()
            for row in v:
                if isinstance(row, basestring):
                    rows += (row,)
                else:
                    rows += (walk_replace(smap, row),)
            rv = tuple(filter(lambda row: row, rows))
        else:
            rv = walk_replace(smap, v)
        return replace_at(k, rv) if rv else None

    if isinstance(data, collections.Sequence):
        return tuple(map(lambda x: walk_replace(smap, x), data))
    try:
        nodes = tuple(map(lambda kv: process_node(kv[0], kv[1]), data.iteritems()))
        return dict(filter(lambda node: node is not None, nodes))
    except AttributeError:
        return data


def union(*sets):
    return first(sets).union(*rest(sets))


def intersection(x, y):
    return tuple(set(x).intersection(y))


def dict_invert(dict):
    return {v: k for (k, v) in dict.iteritems()}


def flatten(dict):
    return reduce(merge, [{k: last(item) for k in first(item)}
                          for item in dict.items()])


# not tested with frozen dicts, just regular ones
def assoc(fdict, key, val, *kvs):
    keyvals = (key, val) + kvs
    return merge(fdict, dict(zip(keyvals[0::2], keyvals[1::2])))


# not tested with frozen dicts, just regular ones
def dissoc(fdict, key, *ks):
    keys = (key,) + ks
    return {k: v for k, v in fdict.iteritems() if k not in keys}


def hash_map(*keyvals):
    i = iter(keyvals)
    return dict(zip(i, i))


def format(fmt, *args, **kwargs):
    if kwargs:
        return fmt.format(**kwargs)
    else:
        return fmt.format(*args)


def select_keys(fdict, keys):
    return {k: fdict[k] for k in keys if k in fdict}


def destructure(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        params = select_keys(first(args), inspect.getargspec(f).args)
        return f(**(merge(kwargs, params)))
    return wrapper
