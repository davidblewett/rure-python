#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import unittest

import rure
from rure.lib import RureMatch


class TestRegexObject(unittest.TestCase):

    def test_search(self):
        pattern = rure.compile(u"d")
        self.assertTrue(pattern.search(u"dog"))
        self.assertFalse(pattern.search(u"dog", 1))

    def test_match(self):
        pattern = rure.compile(u"o")
        self.assertFalse(pattern.match(u"dog"))
        self.assertTrue(pattern.match(u"dog", 1))

    def test_findall(self):
        haystack = u"abc xyz"
        pattern = rure.compile(u"\\w+(\\w)")
        matches = pattern.findall(haystack)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches, [u'c', u'z'])

    def test_finditer(self):
        haystack = u"abc xyz"
        pattern = rure.compile(u"\\w+(\\w)")
        gen = pattern.finditer(haystack)
        match = next(gen)
        self.assertIsNotNone(match)
        self.assertEqual(match.captures[0], RureMatch(0, 3))
        match = next(gen)
        self.assertIsNotNone(match)
        self.assertEqual(match.captures[-1], RureMatch(6, 7))

    def test_nonmatching_captures(self):
        ptn = u"(re).*(ger)"
        email = u"tony@tiremove_thisger.net"
        results = rure.search(ptn, email)
        stdlib_results = re.search(ptn, email)
        self.assertIsNotNone(results)
        self.assertEqual(len(results.groups()),
                         len(stdlib_results.groups()))

        ptn = u"(re)|(ger)"
        results = rure.search(ptn, email)
        stdlib_results = re.search(ptn, email)
        self.assertIsNotNone(results)
        self.assertEqual(len(results.groups()),
                         len(stdlib_results.groups()))
        self.assertEqual(results.group(0),
                         stdlib_results.group(0))
