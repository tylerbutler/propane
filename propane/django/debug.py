# coding=utf-8
from __future__ import absolute_import, print_function

from six import string_types

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

try:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from django.core import urlresolvers
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from django.http import HttpResponse
except ImportError:
    print("Django is required but cannot be imported.")
    raise

intro_text = """Named URL patterns for the {% url %} tag
========================================

e.g. {% url pattern-name %}
or   {% url pattern-name arg1 %} if the pattern requires arguments

"""


# noinspection PyUnusedLocal
def show_url_patterns(request, **kwargs):
    patterns = _get_named_patterns()
    r = HttpResponse(intro_text, content_type='text/plain')
    longest = max([len(pair[0]) for pair in patterns])
    for key, value in patterns:
        r.write('%s %s\n' % (key.ljust(longest + 1), value))
    return r


def _get_named_patterns():
    """Returns list of (pattern-name, pattern) tuples"""
    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([(key, value[0][0][0])
                       for key, value in resolver.reverse_dict.items()
                       if isinstance(key, string_types)
                       ])
    return patterns
