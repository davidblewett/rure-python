import os
import sys
from collections import namedtuple

from rure._ffi import ffi
from rure import exceptions
from rure.decorators import accepts_bytes


CASEI = 1 << 0
MULTI = 1 << 1
DOTNL = 1 << 2
SWAP_GREED = 1 << 3
SPACE = 1 << 4
UNICODE = 1 << 5
DEFAULT_FLAGS = UNICODE


RureMatch = namedtuple("RureMatch", ("start", "end"))


def find_library():
    libname = "rure"
    if sys.platform == 'win32':
        prefix = ''
        suffix = 'dll'
    elif sys.platform == 'darwin':
        prefix = 'lib'
        suffix = 'dylib'
    else:
        prefix = 'lib'
        suffix = 'so'
    cur_dir = os.path.dirname(__file__)
    return os.path.join(cur_dir, "{}{}.{}".format(prefix, libname, suffix))


_lib = ffi.dlopen(find_library(), ffi.RTLD_NODELETE)


def checked_call(fn, err, *args):
    all_args = list(args) + [err]
    res = fn(*all_args)
    msg = ffi.string(_lib.rure_error_message(err))
    if msg == b'no error':
        return res
    elif msg.startswith(b'Error parsing regex'):
        raise exceptions.RegexSyntaxError(msg)
    elif msg.startswith(b'Compiled regex exceeds size limit'):
        raise exceptions.CompiledTooBigError(msg)
    else:
        msg = bytes(msg, 'utf8')
        raise exceptions.RegexError(msg)


class Rure(object):
    """ A compiled regular expression for matching Unicode strings.

    It is represented as either a sequence of bytecode instructions (dynamic)
    or as a specialized Rust function (native). It can be used to search,
    split or replace text. All searching is done with an implicit .*?
    at the beginning and end of an expression. To force an expression to match
    the whole string (or a prefix or a suffix), you must use an anchor
    like ^ or $ (or \A and \z).

    While this crate will handle Unicode strings (whether in the regular
    expression or in the search text), all positions returned are byte indices.
    Every byte index is guaranteed to be at a Unicode code point boundary.
    """

    def __init__(self, re, _pointer=None,
                 flags=DEFAULT_FLAGS, **options):
        """ Compiles a regular expression. Once compiled, it can be used
        repeatedly to search, split or replace text in a string.

        :param re:      Bytestring expression to compile
        :param flags:   Bitmask of flags
        :param kwargs:  Config options to pass (size_limit, dfa_size_limit)
        """
        if not isinstance(re, bytes):
            raise TypeError("'rure.lib.Rure' must be instantiated with a "
                            "bytestring as first argument.")

        self._err = ffi.gc(_lib.rure_error_new(), _lib.rure_error_free)
        self._opts = ffi.gc(_lib.rure_options_new(), _lib.rure_options_free)

        self.options = options
        if 'size_limit' in options:
            _lib.rure_options_size_limit(self._opts, options['size_limit'])
        if 'dfa_size_limit' in options:
            _lib.rure_options_dfa_size_limit(self._opts,
                                             options['dfa_size_limit'])

        if re:
            s = checked_call(
                _lib.rure_compile,
                self._err,
                re,
                len(re),
                flags,
                self._opts
            )
        else:
            s = _pointer
        self._ptr = ffi.gc(s, _lib.rure_free)
        self.capture_cls = namedtuple(
            'Captures',
            [i.decode('utf8') if i else u'' for i in self.capture_names()],
            rename=True
        )

    @accepts_bytes
    def capture_name_index(self, name):
        """ Returns the capture index for the name given.
        If no such named capturing group exists in re, then -1 is returned.

        The capture index may be used with captures_at.

        This function never returns 0 since the first capture group always
        corresponds to the entire match and is always unnamed.
        """
        return _lib.rure_capture_name_index(self._ptr, name)

    def capture_names(self):
        """ An iterator over the names of all possible captures.
        None indicates an unnamed capture; the first element (capture 0,
        the whole matched region) is always unnamed.
        """
        cn_iter = ffi.gc(_lib.rure_iter_capture_names_new(self._ptr),
                         _lib.rure_iter_capture_names_free)
        ptr = ffi.new('char **')
        while _lib.rure_iter_capture_names_next(cn_iter, ptr):
            name = ffi.string(ptr[0])
            if name:
                yield name
            else:
                yield None

    @accepts_bytes
    def is_match(self, haystack, start=0):
        """ Returns true if and only if the regex matches the string given.

        It is recommended to use this method if all you need to do is test
        a match, since the underlying matching engine may be able to do less
        work.
        """
        return bool(_lib.rure_is_match(
            self._ptr,
            haystack,
            len(haystack),
            start
        ))

    @accepts_bytes
    def find(self, haystack, start=0):
        """ Returns the start and end byte range of the leftmost-first match
        in text. If no match exists, then None is returned.

        Note that this should only be used if you want to discover the position
        of the match. Testing the existence of a match is faster if you use
        is_match.
        """
        match = ffi.new('rure_match *')
        if _lib.rure_find(
            self._ptr,
            haystack,
            len(haystack),
            start,
            match
        ):
            return RureMatch(match.start, match.end)

    @accepts_bytes
    def find_iter(self, haystack, start=0):
        """Returns the capture groups corresponding to the leftmost-first match
        in text. Capture group 0 always corresponds to the entire match.
        If no match is found, then None is returned.

        You should only use captures if you need access to submatches.
        Otherwise, find is faster for discovering the location of the overall
        match.
        """
        hlen = len(haystack)
        find_iter = ffi.gc(_lib.rure_iter_new(self._ptr),
                           _lib.rure_iter_free)

        match = ffi.new('rure_match *')
        while _lib.rure_iter_next(find_iter,
                                  haystack,
                                  hlen,
                                  match):
            yield RureMatch(match.start, match.end)

    @accepts_bytes
    def captures(self, haystack, start=0):
        """Returns the capture groups corresponding to the leftmost-first match
        in text. Capture group 0 always corresponds to the entire match.
        If no match is found, then None is returned.

        You should only use captures if you need access to submatches.
        Otherwise, find is faster for discovering the location of the overall
        match.
        """
        hlen = len(haystack)
        captures = ffi.gc(_lib.rure_captures_new(self._ptr),
                          _lib.rure_captures_free)
        match = ffi.new('rure_match *')
        if _lib.rure_find_captures(
            self._ptr,
            haystack,
            hlen,
            start,
            captures
        ):
            return self.capture_cls(*[
                RureMatch(match.start, match.end)
                    if _lib.rure_captures_at(captures, i, match) else None
                for i in range(0, _lib.rure_captures_len(captures))
            ])

    @accepts_bytes
    def captures_iter(self, haystack, start=0):
        """Returns an iterator over all the non-overlapping capture groups
        matched in text. This is operationally the same as find_iter,
        except it yields information about submatches.
        """
        hlen = len(haystack)
        captures = ffi.gc(_lib.rure_captures_new(self._ptr),
                          _lib.rure_captures_free)
        captures_iter = ffi.gc(_lib.rure_iter_new(self._ptr),
                               _lib.rure_iter_free)
        match = ffi.new('rure_match *')
        while _lib.rure_iter_next_captures(captures_iter,
                                           haystack,
                                           hlen,
                                           captures):
            yield self.capture_cls(*[
                RureMatch(match.start, match.end)
                    if _lib.rure_captures_at(captures, i, match) else None
                for i in range(0, _lib.rure_captures_len(captures))
            ])

    @accepts_bytes
    def shortest_match(self, haystack, start=0):
        """Returns end location if and only if re matches anywhere in
        text. The end location is the place at which the regex engine
        determined that a match exists, but may occur before the end of
        the proper leftmost-first match.
        """
        hlen = len(haystack)
        end = ffi.new('size_t *')
        if _lib.rure_shortest_match(self._ptr, haystack, hlen, start, end):
            return end[0]
