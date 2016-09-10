# coding=utf-8
from __future__ import absolute_import, print_function

import re
from unicodedata import normalize


# noinspection PyPep8Naming
def space_out_camel_case(stringAsCamelCase):
    """
    Adds spaces to a camel case string.  Failure to space out string returns the original string.

    >>> space_out_camel_case('DMLSServicesOtherBSTextLLC')
    'DMLS Services Other BS Text LLC'
    """
    pattern = re.compile(r'([A-Z][A-Z][a-z])|([a-z][A-Z])')

    if stringAsCamelCase is None:
        return None

    return pattern.sub(lambda m: m.group()[:1] + " " + m.group()[1:], stringAsCamelCase)


_punctuation_regex = re.compile(r'[\t :!"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
_available_unicode_handlers = []
try:
    # noinspection PyUnresolvedReferences
    import translitcodec


    def _translit_handler(word):
        return word.encode('translit/long')


    _available_unicode_handlers.append(_translit_handler)
except ImportError:
    pass

try:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from unidecode import unidecode


    def _unidecode_handler(word):
        return unidecode(word)


    _available_unicode_handlers.append(_unidecode_handler)
except ImportError:
    pass


def _unicodedata_handler(word):
    return normalize('NFKD', word).encode('ascii', 'ignore')


_available_unicode_handlers.append(_unicodedata_handler)


def slugify(text, length_limit=0, delimiter=u'-'):
    """Generates an ASCII-only slug of a string."""
    result = []
    for word in _punctuation_regex.split(text.lower()):
        word = _available_unicode_handlers[0](word)
        if word:
            result.append(word)
    slug = delimiter.join(result)
    if length_limit > 0:
        return slug[0:length_limit]
    return slug
