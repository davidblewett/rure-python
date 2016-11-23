#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest

import rure


class TestRegexObject(unittest.TestCase):
    def test_search(self):
        ptn = u"(re).*(ger)"
        email = u"tony@tiremove_thisger.net"
        results = rure.search(ptn, email)
        self.assertIsNotNone(results)
        self.assertEqual(len(results.groups()), 2)

        ptn = u"(re)|(ger)"
        results = rure.search(ptn, email)
        self.assertIsNotNone(results)
        self.assertEqual(len(results.groups()), 1)
        self.assertItemsEqual(results.group(0), (u're',))
