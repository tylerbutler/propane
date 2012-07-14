# coding=utf-8
import sys

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

def get_class(class_string):
    """Given a string representing a path to a class, instantiates that class."""
    parts = class_string.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def add_to_path_if_needed(path):
    """
    Adds *path* to the system path if it is not already on it.

    Prevents unnecessary 'pollution' of the path with a bunch of redundant entries.
    """
    if path not in sys.path:
        sys.path.append(path)


def dict_to_querystring(dictionary):
    """Converts a dict to a querystring suitable to be appended to a URL."""
    s = u""
    for d in dictionary.keys():
        s = unicode.format(u"{0}{1}={2}&", s, d, dictionary[d])
    return s[:-1]
