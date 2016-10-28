from rure.lib import Rure
from rure.lib import DEFAULT_FLAGS
from rure.lib import CASEI, MULTI, DOTNL, SWAP_GREED, SPACE, UNICODE
from rure.regex import RegexObject


__all__ = [
    "Rure", "RegexObject",
    "compile", "search", "is_match", "match", "findall", "finditer",
    "DEFAULT_FLAGS",
    "CASEI", "MULTI", "DOTNL", "SWAP_GREED", "SPACE", "UNICODE",
]


def compile(pattern, flags=0, **options):
    return RegexObject(pattern, flags=flags, **options)


def search(pattern, string, flags=0, **options):
    return RegexObject(pattern, flags=flags, **options).search(string)


def is_match(pattern, string, flags=0, **options):
    return RegexObject(pattern, flags=flags, **options).is_match(string)


def match(pattern, string, flags=0, **options):
    return RegexObject(pattern, flags=flags, **options).match(string)


def findall(pattern, string, flags=0, **options):
    return RegexObject(pattern, flags=flags, **options).findall(string)


def finditer(pattern, string, flags=0, **options):
    return RegexObject(pattern, flags=flags, **options).finditer(string)
