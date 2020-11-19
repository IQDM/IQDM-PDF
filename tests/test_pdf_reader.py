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
from IQDMPDF import pdf_reader
from os.path import join


base_data_dir = join("tests", "test_data")
example_data = join(base_data_dir, "simple_test.pdf")


class TestPDFReader(unittest.TestCase):
    """Unit tests for PDF Reader."""

    def setUp(self):
        """Setup files and base data for utility testing."""
        self.expected_data = ["Hello World!!!",
                              "This is a simple PDF used to test IQDM-PDF.",
                              "Mid-page test data",
                              "2nd page data!"]

    def test_convert_pdf_to_txt(self):
        """Test are_all_strings_in_text"""
        text = pdf_reader.convert_pdf_to_txt(example_data)
        text_split = text.split('\n')
        data = [text_split[0],
                text_split[10],
                text_split[44],
                text_split[46]]
        self.assertEqual(len(text_split), 49)
        for i, expected in enumerate(self.expected_data):
            self.assertEqual(data[i].strip(), expected)

    def test_custom_pdf_reader(self):
        """Test CustomPDFReader"""
        reader = pdf_reader.CustomPDFReader(example_data)
        tests = [{'page': 0, 'pos': [252.0, 675.97]},
                 {'page': 0, 'pos': [72.0, 514.93]},
                 {'page': 0, 'pos': [432.0, 529.57]},
                 {'page': 1, 'pos': [72.0, 705.25]}]
        self.assess_custom_pdf_test_data(reader, tests, self.assertEqual)

        # Modify tests by adding 10 to each positional dimension
        for i in range(len(tests)):
            tests[i]['pos'] = [v + 10 for v in tests[i]['pos']]
        self.assess_custom_pdf_test_data(reader, tests, self.assertEqual)

        # Modify tests by adding 11 to each positional dimension
        for i in range(len(tests)):
            tests[i]['pos'] = [v + 11 for v in tests[i]['pos']]
        self.assess_custom_pdf_test_data(reader, tests, self.assertEqual)

    def assess_custom_pdf_test_data(self, reader, tests, test_func):
        data = [reader.get_block_data(**test) for test in tests]
        for i, expected in enumerate(self.expected_data):
            if len(data[i]):
                test_func(data[i][0], expected)


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
