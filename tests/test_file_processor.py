#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_file_processor.py
"""unittest cases for file_processor."""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from IQDMPDF import file_processor
from IQDMPDF.paths import DIRECTORIES
from os import listdir, unlink
from os.path import join


class TestFileProcessor(unittest.TestCase):
    """Unit tests for file_processor."""

    def setUp(self):
        """Setup files and base data for file_processor testing."""
        csv_dir = DIRECTORIES["EXAMPLE_CSV"]
        self.csv_data = {}
        for file in listdir(csv_dir):
            with open(join(csv_dir, file), "r") as f:
                self.csv_data[file] = f.read().split("\n")

    def test_process_file(self):
        """Test process_file with example reports"""
        # no recursive search
        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")
        file_path = listdir(directory)[0]
        output_dir = DIRECTORIES["TEST_DATA"]
        output_file = "test_process_file.txt"
        pdf_path = join(directory, file_path)
        file_processor.process_file(pdf_path, output_file, output_dir)
        unlink(join(output_dir, "SNCPatient_" + output_file))

    def test_process_files(self):
        """Test process_files with example reports"""
        file_processor.process_files(
            DIRECTORIES["TEST_DATA"], output_file="unittest.csv"
        )
        test_files = [f for f in listdir() if f.endswith("_unittest.csv")]
        for file in test_files:
            with open(file, "r") as f:
                test_data = f.read().split("\n")
                for r, row in enumerate(test_data):
                    new_data_split = self.csv_data[file][r].split(",")
                    # skip report_file_path column
                    for c, col in enumerate(row.split(",")[:-1]):
                        self.assertEqual(new_data_split[c], col)
            unlink(file)

        # no recursive search
        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")
        file_processor.process_files(directory, no_recursive_search=True, callback=self.mock_callback)
        test_files = [
            f
            for f in listdir()
            if f.startswith("SNCPatient_results_") and f.endswith(".csv")
        ]
        for file in test_files:
            unlink(file)

    def mock_callback(self, msg):
        self.assertTrue("label" in msg.keys())
        self.assertTrue("gauge" in msg.keys())
        self.assertTrue(isinstance(msg["label"], str))
        self.assertTrue(isinstance(msg["gauge"], float))


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
