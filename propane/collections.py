# coding=utf-8
from __future__ import absolute_import, print_function

from collections import Mapping, MutableMapping, Iterable
from itertools import chain, islice
from six import iteritems, string_types

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def chunk(seq, chunksize, process=iter):
    it = iter(seq)
    while True:
        yield process(chain([it.next()], islice(it, chunksize - 1)))


def count_iterable(iterable):
    return sum(1 for _ in iterable)


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
            if isinstance(dict1[key], Mapping):
                assert isinstance(value, Mapping)
                update_additive(dict1[key], value)
            else:  # value is not a mapping type
                assert not isinstance(value, Mapping)
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


def flatten_dict(d, parent_key='', separator='_'):
    """
    Flattens any nested dict-like object into a non-nested form.

    The resulting dict will have keys of the form ``k1_nestedk2_nestedk3`` for nested keys. You can change the
    separator by passing in a value to ``separator``.

    Example::

        >>> d = { 'a': 1,
        ...       'b': { 'a': 2,
        ...              'b': 3 },
        ...       'c': { 'a': 4,
        ...              'b': { 'a': 5,
        ...                     'b': 6 },
        ...              'c': { 'a': 7 }
        ...            }
        ...     }
        >>> flatten_dict(d) == {'a': 1, 'b_a': 2, 'b_b': 3, 'c_a': 4, 'c_b_a': 5, 'c_b_b': 6, 'c_c_a': 7}
        True
    """
    items = []
    for k, v in iteritems(d):
        new_key = parent_key + separator + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_iterable(l):
    """
    Flattens a nested iterable into a single layer. Generator.

    Example::

        >>> nested_iterable = (('t1', 't2'), ['l1', 'l2', ('l1', 'l2')])
        >>> list(flatten_iterable(nested_iterable))
        ['t1', 't2', 'l1', 'l2', 'l1', 'l2']
        >>> set(flatten_iterable(nested_iterable)) == {'t1', 't2', 'l1', 'l2'}
        True
    """
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, string_types):
            for sub in flatten_iterable(el):
                yield sub
        else:
            yield el
