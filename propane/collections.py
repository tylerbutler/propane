# coding=utf-8
from __future__ import absolute_import, print_function

import collections
from itertools import chain, islice

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def chunk(seq, chunksize, process=iter):
    it = iter(seq)
    while True:
        yield process(chain([it.next()], islice(it, chunksize - 1)))


# noinspection PyShadowingBuiltins
def count_iterable(iter):
    return sum(1 for _ in iter)


def update_additive(dict1, dict2):
    """
    A utility method to update a dict or other mapping type with the contents of another dict.

    This method updates the contents of ``dict1``, overwriting any existing key/value pairs in ``dict1`` with the
    corresponding key/value pair in ``dict2``. If the value in ``dict2`` is a mapping type itself, then
    ``update_additive`` is called recursively. This ensures that nested maps are updated rather than simply
    overwritten.

    This method should be functionally equivalent to ``dict.update()`` except in the case of values that are
    themselves nested maps. If you know that ``dict1`` does not have nested maps,
    or you want to overwrite all values with the exact content of then you should simply use ``dict.update()``.
    """
    for key, value in dict2.items():
        if key not in dict1:
            dict1[key] = value
        else:  # key in dict1
            if isinstance(dict1[key], collections.Mapping):
                assert isinstance(value, collections.Mapping)
                update_additive(dict1[key], value)
            else:  # value is not a mapping type
                assert not isinstance(value, collections.Mapping)
                dict1[key] = value


def wrap_list(item):
    """
    Returns an object as a list.

    If the object is a list, it is returned directly. If it is a tuple or set, it
    is returned as a list. If it is another object, it is wrapped in a list and
    returned.
    """
    if item is None:
        return []
    elif isinstance(item, list):
        return item
    elif isinstance(item, (tuple, set)):
        return list(item)
    else:
        return [item]
