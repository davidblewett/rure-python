#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import unittest

import rure


class TestRegexObject(unittest.TestCase):
    def test_search(self):
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
        self.assertItemsEqual(results.group(0),
                              stdlib_results.group(0))
