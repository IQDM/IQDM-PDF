#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_utilities.py
"""unittest cases for utilities."""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from IQDMPDF import utilities


class TestUtilities(unittest.TestCase):
    """Unit tests for Utilities."""

    def setUp(self):
        """Setup files and base data for utility testing."""
        pass

    def test_are_all_strings_in_text(self):
        """Test are_all_strings_in_text"""
        strings = ['Hello', 'World']
        text = 'Hello World! This is a unit test!'
        self.assertTrue(utilities.are_all_strings_in_text(text, strings))
        strings.append('FAIL')
        self.assertFalse(utilities.are_all_strings_in_text(text, strings))

    def test_get_csv_row(self):
        """Test test_get_csv_row"""
        data = {'a': 0, 'b': "test,", 'c': 3.54, 'd': "ignore me!"}
        columns = ['b', 'a', 'c']
        expected = '"test,",0,3.54'
        self.assertEqual(utilities.get_csv_row(data, columns), expected)

    def test_get_sorted_indices(self):
        """Test get_sorted_indices"""
        some_list = [1, 4, 2, 5]
        expected = [0, 2, 1, 3]
        ans = utilities.get_sorted_indices(some_list)
        for i, val in enumerate(expected):
            self.assertEqual(ans[i], expected[i])

    def test_is_in_tol(self):
        """Test is_in_tol"""
        self.assertTrue(utilities.is_in_tol(10, 12, 3))
        self.assertFalse(utilities.is_in_tol(10.1, 12.1, 1))


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
