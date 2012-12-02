# coding=utf-8

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
