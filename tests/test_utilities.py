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
from os.path import join


class TestUtilities(unittest.TestCase):
    """Unit tests for Utilities."""

    def setUp(self):
        """Setup files and base data for utility testing."""
        pass

    def test_are_all_strings_in_text(self):
        """Test are_all_strings_in_text"""
        strings = ["Hello", "World"]
        text = "Hello World! This is a unit test!"
        self.assertTrue(utilities.are_all_strings_in_text(text, strings))
        strings.append("FAIL")
        self.assertFalse(utilities.are_all_strings_in_text(text, strings))

    def test_get_csv_row(self):
        """Test test_get_csv_row"""
        data = {"a": 0, "b": "test,", "c": 3.54, "d": "ignore me!"}
        columns = ["b", "a", "c"]
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

    def test_bbox_to_pos(self):
        """Test the bounding box to position converter"""
        bbox = [0, 1, 2, 3]

        expected = {
            "bottom-left": [0, 1],
            "bottom-center": [1, 1],
            "bottom-right": [2, 1],
            "center-left": [0, 2],
            "center-center": [1, 2],
            "center": [1, 2],
            "center-right": [2, 2],
            "top-left": [0, 3],
            "top-center": [1, 3],
            "top-right": [2, 3],
        }
        for mode, exp_pos in expected.items():
            pos = utilities.bbox_to_pos(bbox, mode)
            self.assertEqual(pos[0], exp_pos[0])
            self.assertEqual(pos[1], exp_pos[1])

    def test_get_relative_path(self):
        """Test tool to extract relative path"""
        test_path = ["this", "is", "a", "test", "path"]
        exp_path = join(*test_path[-2:])
        test_path = join(*test_path)
        rel_test_path = utilities.get_relative_path(test_path, "test")
        self.assertEqual(exp_path, rel_test_path)

    def test_csv_to_list(self):
        """Test the csv to list function"""
        test_csv = 'this,is,a,test,with,a,"comma,",and,empty,final,value,'
        test_list = utilities.csv_to_list(test_csv)
        self.assertEqual(test_list[0], "this")
        self.assertEqual(test_list[6], "comma,")
        self.assertEqual(test_list[-1], "")

        test_csv = "this,is,a,test,with,a,nonempty,final,value"
        test_list = utilities.csv_to_list(test_csv)
        self.assertEqual(test_list[-1], "value")

    def test_create_arg_parser(self):
        """Test arg parser creation"""
        arg_parser = utilities.create_arg_parser().parse_args([])
        expected_args = [
            "ignore_extension",
            "output_dir",
            "output_file",
            "print_version",
            "no_recursive_search",
            "init_directory",
        ]
        for arg in expected_args:
            self.assertTrue(arg in arg_parser.__dict__.keys())


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
