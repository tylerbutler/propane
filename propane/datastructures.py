# coding=utf-8
from __future__ import absolute_import
import itertools
import collections

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

class CaseInsensitiveDict(collections.MutableMapping):
    """A dict whose keys are not case-sensitive."""

    def __init__(self, d):
        self._d = d
        self._s = dict((k.lower(), k) for k in d)

    def __contains__(self, key):
        return key.lower() in self._s

    def __len__(self):
        return len(self._s)

    def __iter__(self):
        return iter(self._s)

    def __getitem__(self, key):
        return self._d[self._s[key.lower()]]

    def __setitem__(self, key, value):
        self._d[key] = value
        self._s[key.lower()] = key

    def __delitem__(self, key):
        if key in self._d:
            del self._d[key]
        del self._s[key.lower()]

    def actual_key_case(self, key):
        return self._s.get(key.lower())


# setonce class from Ian Bicking: http://blog.ianbicking.org/easy-readonly-attributes.html
_setonce_count = itertools.count()

class setonce(object):
    """
    Allows an attribute to be set once (typically in __init__), but
    be read-only afterwards.

    Example::

        >>> class A(object):
        ...     x = setonce()
        >>> a = A()
        >>> a.x
        Traceback (most recent call last):
        ...
        AttributeError: 'A' object has no attribute '_setonce_attr_0'
        >>> a.x = 10
        >>> a.x
        10
        >>> a.x = 20
        Traceback (most recent call last):
        ...
        AttributeError: Attribute already set
        >>> del a.x
        >>> a.x = 20
        >>> a.x
        20

    You can also force a set to occur::

        >>> A.x.set(a, 30)
        >>> a.x
        30
    """

    def __init__(self, doc=None):
        self._count = _setonce_count.next()
        self._name = '_setonce_attr_%s' % self._count
        self.__doc__ = doc

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        try:
            getattr(obj, self._name)
        except AttributeError:
            setattr(obj, self._name, value)
        else:
            raise AttributeError, "Attribute already set"

    def set(self, obj, value):
        setattr(obj, self._name, value)

    def __delete__(self, obj):
        delattr(obj, self._name)
