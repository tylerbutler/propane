# coding=utf-8
from __future__ import absolute_import
import collections

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'


def count_iterable(iter):
    return sum(1 for i in iter)


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
