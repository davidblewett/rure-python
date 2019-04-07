#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest

from rure.exceptions import CompiledTooBigError, RegexSyntaxError
from rure.lib import CASEI, Rure


class TestRure(unittest.TestCase):
    def test_is_match(self):
        haystack = b"snowman: \xE2\x98\x83"
        re = Rure(b"\\p{So}$")
        self.assertIsNotNone(re.is_match(haystack))

    def test_shortest_match(self):
        haystack = b"aaaaa"
        re = Rure(b"a+")
        end = re.shortest_match(haystack)
        self.assertIsNotNone(end)
        self.assertEqual(end, 1,
                         "Expected match end location 1 but got {}".format(end))

    def test_find(self):
        haystack = b"snowman: \xE2\x98\x83"
        re = Rure(b"\\p{So}$")
        match = re.find(haystack)
        self.assertIsNotNone(match)

        expect_start = 9
        expect_end = 12
        self.assertEqual(
            (match.start, match.end), (expect_start, expect_end),
            "Expected match at ({}, {}) but got match at ({}, {})".format(
                expect_start, expect_end, match.start, match.end)
        )

    def test_captures(self):
        haystack = b"snowman: \xE2\x98\x83"
        re = Rure(b".(.*(?P<snowman>\\p{So}))$")
        captures = re.captures(haystack)
        self.assertIsNotNone(captures)

        expect_capture_index = 2
        capture_index = re.capture_name_index(b"snowman")
        self.assertEqual(
            capture_index, expect_capture_index,
            "Expected capture index {} for name 'snowman', but got {}".format(
                expect_capture_index, capture_index)
        )

        expect_start = 9
        expect_end = 12
        match = captures[2]
        self.assertEqual(
            (match.start, match.end), (expect_start, expect_end),
            "Expected match at ({}, {}) but got match at ({}, {})".format(
                expect_start, expect_end, match.start, match.end)
        )

    def test_iter(self):
        haystack = b"abc xyz"
        re = Rure(b"\\w+(\\w)")
        match = next(re.find_iter(haystack))
        self.assertIsNotNone(match)

        expect_start = 0
        expect_end = 3
        self.assertEqual(
            (match.start, match.end), (expect_start, expect_end),
            "Expected match at ({}, {}) but got match at ({}, {})".format(
                expect_start, expect_end, match.start, match.end)
        )

        # find_iter and captures_iter use distinct iterators;
        # emulate by advancing captures an additional time
        c_iter = re.captures_iter(haystack)
        next(c_iter)
        captures = next(c_iter)
        self.assertIsNotNone(captures)

        match = captures[1]
        expect_start = 6
        expect_end = 7
        self.assertEqual(
            (match.start, match.end), (expect_start, expect_end),
            "Expected match at ({}, {}) but got match at ({}, {})".format(
                expect_start, expect_end, match.start, match.end)
        )

    def test_iter_capture_names(self):
        re = Rure(b"(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})")
        cn_iter = re.capture_names()
        self.assertIsNone(next(cn_iter))

        for word in [b"year", b"month", b"day"]:
            next_match = next(cn_iter)
            self.assertEqual(
                word, next_match,
                "Expected first capture name '{}', got '{}'.".format(
                    word, next_match
                )
            )

    def test_flags(self):
        """Test whether we can set the flags correctly.

        In this case, we disable all flags, which includes disabling
        Unicode mode. When we disable Unicode mode, we can match
        arbitrary possibly invalid UTF-8 bytes, such as \xFF.
        (When Unicode mode is enabled, \xFF won't match .)
        """
        pattern = b"."
        haystack = b"\xFF"
        re = Rure(pattern, flags=CASEI)
        self.assertTrue(re.is_match(haystack))

    def test_compile_error(self):
        try:
            Rure(b"(")
        except RegexSyntaxError as err:
            self.assertIn("unclosed group", err.message.lower())

    def test_compile_error_size_limit(self):
        try:
            Rure(b"\\w{100}", size_limit=0)
        except CompiledTooBigError as err:
            self.assertIn("exceeds size", err.message)
