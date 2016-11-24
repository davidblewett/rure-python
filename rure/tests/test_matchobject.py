#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest

import rure


class TestMatchObject(unittest.TestCase):

    def test_match_is_boolean(self):
        pattern = rure.compile(u"d")
        self.assertTrue(pattern.search(u"dog"))
        self.assertFalse(pattern.search(u"dog", 1))

    def test_group(self):
        m = rure.match(u"(\\w+) (\\w+)", u"Isaac Newton, physicist")
        self.assertEqual(m.group(0), u'Isaac Newton')
        self.assertEqual(m.group(1), u'Isaac')
        self.assertEqual(m.group(2), u'Newton')
        self.assertEqual(m.group(1, 2), ('Isaac', 'Newton'))

    def test_complicated_group(self):
        m = rure.match(u"(?P<first_name>\\w+) (?P<last_name>\\w+)",
                       u"Malcolm Reynolds")
        self.assertEqual(m.group(u'first_name'), u'Malcolm')
        self.assertEqual(m.group(u'last_name'), u'Reynolds')

        self.assertEqual(m.group(1), u'Malcolm')
        self.assertEqual(m.group(2), u'Reynolds')

    def test_group_last_match(self):
        m = rure.match(u"(..)+", u"a1b2c3")
        self.assertEqual(m.group(1), u'c3')

    def test_groups(self):
        m = rure.match(u"(\\d+)\\.(\\d+)", u"24.1632")
        self.assertEqual(m.groups(), ('24', '1632'))

    def test_groups_optional(self):
        m = rure.match(u"(\\d+)\\.?(\\d+)?", u"24")
        self.assertEqual(m.groups(), (u'24', None))
        self.assertEqual(m.groups(u'0'), (u'24', u'0'))

    def test_groupdict(self):
        m = rure.match(u"(?P<first_name>\\w+) (?P<last_name>\\w+)",
                       u"Malcolm Reynolds")
        self.assertEqual(m.groupdict(), {u'first_name': u'Malcolm',
                                         u'last_name': u'Reynolds'})

    def test_start_end(self):
        m = rure.search(u"remove_this", u"tony@tiremove_thisger.net")
        self.assertEqual((m.string[:m.start()] + m.string[m.end():]).decode('utf8'),
                         u'tony@tiger.net')
