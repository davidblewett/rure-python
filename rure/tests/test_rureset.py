#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest

from rure.exceptions import CompiledTooBigError, RegexSyntaxError
from rure.lib import CASEI, RureSet


class TestRureSet(unittest.TestCase):

    def test_type_check(self):
        with self.assertRaises(TypeError):
            RureSet(b"baz", u"bar", b"foo")

    def test_is_match(self):
        haystack = b"snowman: \xE2\x98\x83"
        res = RureSet(b"\\p{So}")
        self.assertIsNotNone(res.is_match(haystack))

    def test_matches(self):
        haystack = b"foobar"
        res = RureSet(b"baz", b"bar", b"foo")
        self.assertEqual(res.matches(haystack), [False, True, True])

    def test_set_len(self):
        res = RureSet(b"baz", b"bar", b"foo")
        self.assertEqual(len(res), 3)

    def test_flags(self):
        """Test whether we can set the flags correctly.

        In this case, we disable all flags, which includes disabling
        Unicode mode. When we disable Unicode mode, we can match
        arbitrary possibly invalid UTF-8 bytes, such as \xFF.
        (When Unicode mode is enabled, \xFF won't match .)
        """
        pattern = b"."
        haystack = b"\xFF"
        res = RureSet(pattern, flags=CASEI)
        self.assertTrue(res.is_match(haystack))

    def test_compile_error(self):
        try:
            RureSet(b"(")
        except RegexSyntaxError as err:
            self.assertIn("unclosed group", err.message.lower())

    def test_compile_error_size_limit(self):
        try:
            RureSet(b"\\w{100}", size_limit=0)
        except CompiledTooBigError as err:
            self.assertIn("exceeds size", err.message.lower())
