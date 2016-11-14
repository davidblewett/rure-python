#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys

from rure.exceptions import CompiledTooBigError, RegexSyntaxError
from rure.lib import Rure


DEBUG = os.getenv('DEBUG', False)


def test_is_match():
    passed = True
    haystack = "snowman: \xE2\x98\x83"

    re = Rure("\\p{So}$")
    matched = re.is_match(haystack)
    if not matched:
        if DEBUG:
            print("[test_is_match] expected match, but got no match\n",
                  file=sys.stderr)

        passed = False

    return passed


def test_shortest_match():
    passed = True
    haystack = "aaaaa"

    re = Rure("a+")
    end = re.shortest_match(haystack)
    if end is None:
        if DEBUG:
            print("[test_shortest_match] expected match, "
                  "but got no match\n",
                  file=sys.stderr)

        passed = False

    expect_end = 1
    if end != expect_end:
        if DEBUG:
            print("[test_shortest_match] expected match end location %s "
                  "but got %s\n" % (expect_end, end),
                  file=sys.stderr)

        passed = False

    return passed


def test_find():
    passed = True
    haystack = "snowman: \xE2\x98\x83"

    re = Rure("\\p{So}$")
    match = re.find(haystack)
    if not match:
        if DEBUG:
            print("[test_find] expected match, but got no match\n",
                  file=sys.stderr)

        passed = False

    expect_start = 9
    expect_end = 12
    if (match.start != expect_start or match.end != expect_end):
        if DEBUG:
            print("[test_find] expected match at (%d, %d), but "
                  "got match at (%d, %d)\n" % (expect_start, expect_end,
                                               match.start, match.end),
                  file=sys.stderr)

        passed = False

    return passed


def test_captures():
    passed = True
    haystack = "snowman: \xE2\x98\x83"

    re = Rure(".(.*(?P<snowman>\\p{So}))$")
    captures = re.captures(haystack)
    if not captures:
        if DEBUG:
            print("[test_captures] expected match, but got no match\n",
                  file=sys.stderr)

        passed = False

    expect_capture_index = 2
    capture_index = re.capture_name_index("snowman")
    if capture_index != expect_capture_index:
        if DEBUG:
            print("[test_captures] "
                  "expected capture index %d for name 'snowman', but "
                  "got %d\n" % (expect_capture_index, capture_index),
                  file=sys.stderr)

        passed = False

    expect_start = 9
    expect_end = 12
    match = captures[2]
    if (match.start != expect_start or match.end != expect_end):
        if DEBUG:
            print("[test_captures] "
                  "expected capture 2 match at (%d, %d), "
                  "but got match at (%d, %d)\n" % (expect_start, expect_end,
                                                   match.start, match.end),
                  file=sys.stderr)

        passed = False

    return passed


def test_iter():
    passed = True
    haystack = "abc xyz"

    re = Rure("\\w+(\\w)")

    match = next(re.find_iter(haystack))
    if not match:
        if DEBUG:
            print("[test_iter] expected first match, but got no match\n",
                  file=sys.stderr)

        passed = False

    expect_start = 0
    expect_end = 3
    if (match.start != expect_start or match.end != expect_end):
        if DEBUG:
            print("[test_iter] expected first match at (%d, %d), but "
                  "got match at (%d, %d)\n" % (expect_start, expect_end,
                                               match.start, match.end),
                  file=sys.stderr)

        passed = False

    # find_iter and captures_iter use distinct iterators;
    # emulate by advancing captures an additional time
    c_iter = re.captures_iter(haystack)
    next(c_iter)
    captures = next(c_iter)
    if not captures:
        if DEBUG:
            print("[test_iter] expected second match, but got no match\n",
                  file=sys.stderr)

        passed = False

    match = captures[1]
    expect_start = 6
    expect_end = 7
    if (match.start != expect_start or match.end != expect_end):
        if DEBUG:
            print("[test_iter] expected second match at (%s, %s), but "
                  "got match at (%s, %s)\n" % (expect_start, expect_end,
                                               match.start, match.end),
                  file=sys.stderr)

        passed = False

    return passed


def test_iter_capture_name(expect, given):
    passed = True
    if expect != given:
        if DEBUG:
            print("[test_iter_capture_name] expected first capture name '%s' "
                  "got '%s'\n" % (expect, given),
                  file=sys.stderr)

        passed = False

    return passed


def test_iter_capture_names():
    passed = True

    re = Rure("(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})")

    cn_iter = re.capture_names()
    result = next(cn_iter)
    if result is not None:
        if DEBUG:
            print("[test_iter_capture_names] expected None for the first unnamed capture\n",
                  file=sys.stderr)

        passed = False

    name = next(cn_iter)
    passed = test_iter_capture_name("year", name)

    name = next(cn_iter)
    passed = test_iter_capture_name("month", name)

    name = next(cn_iter)
    passed = test_iter_capture_name("day", name)

    return passed


# This tests whether we can set the flags correctly. In this case, we disable
# all flags, which includes disabling Unicode mode. When we disable Unicode
# mode, we can match arbitrary possibly invalid UTF-8 bytes, such as \xFF.
# (When Unicode mode is enabled, \xFF won't match .)
def test_flags():
    passed = True
    pattern = "."
    haystack = b"\xFF"

    re = Rure(pattern, flags=1)
    matched = re.is_match(haystack)
    if not matched:
        if DEBUG:
            print("[test_flags] expected match, but got no match\n",
                  file=sys.stderr)

        passed = False

    return passed


def test_compile_error():
    passed = True
    # FIXME: not sure this is a reasonable test for Python
    #if (re != NULL):
    #    if DEBUG:
    #        print(stderr,
    #                "[test_compile_error] "
    #                "expected NULL regex pointer, but got non-NULL pointer\n")

    #    passed = False
    #    rure_free(re)
    try:
        re = Rure("(")
        passed = False
    except RegexSyntaxError as err:
        if "Unclosed parenthesis" not in err.message:
            if DEBUG:
                print("[test_compile_error] "
                      "expected an 'unclosed parenthesis' error message, but "
                      "got this instead: '%s'\n" % err.message,
                      file=sys.stderr)

            passed = False

    return passed


def test_compile_error_size_limit():
    passed = True
    # FIXME: not sure this is a reasonable test for Python
    #if (re != NULL):
    #    if DEBUG:
    #        print(stderr,
    #                "[test_compile_error_size_limit] "
    #                "expected NULL regex pointer, but got non-NULL pointer\n")
    #
    #    passed = False
    #    rure_free(re)
    try:
        re = Rure("\\w{100}", size_limit=0)
        passed = False
    except CompiledTooBigError as err:
        if "exceeds size" not in err.message:
            if DEBUG:
                print("[test_compile_error] "
                      "expected an 'exceeds size' error message, but "
                      "got this instead: '%s'\n" % err.message,
                      file=sys.stderr)

            passed = False

    return passed


def run_test(test_func):
    if test_func():
        print("PASSED: %s" % test_func.__name__, file=sys.stderr)
    else:
        print("FAILED: %s" % test_func.__name__, file=sys.stderr)


if __name__ == "__main__":
    tests = [
        test_is_match,
        test_shortest_match,
        test_find,
        test_captures,
        test_iter,
        test_iter_capture_names,
        test_flags,
        test_compile_error,
        test_compile_error_size_limit,
    ]
    results = [
        run_test(f)
        for f in tests
    ]

    if len([res for res in results if res]) != len(tests):
        sys.exit(1)

    sys.exit(0)
