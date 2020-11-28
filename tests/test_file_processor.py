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
from os.path import join, isdir


class TestFileProcessor(unittest.TestCase):
    """Unit tests for file_processor."""

    def setUp(self):
        """Setup files and base data for file_processor testing."""
        pass

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
        """Test process_files"""
        file_processor.process_files(
            DIRECTORIES["TEST_DATA"], output_file="unittest.csv"
        )
        test_files = [f for f in listdir() if f.endswith("_unittest.csv")]
        for file in test_files:
            # Over-kill to compare data with a saved report? Requires
            # maintenance everytime new examples are made, plus OS issues
            # with file path names.

            # with open(file, "r") as f:
            #     test_data = f.read().split("\n")
            #
            #     # Overkill to compare data since each report type has its own
            #     # tests? This causes file path issues between OSs
            #     for r, row in enumerate(test_data[1:]):
            #         test_data_split = csv_to_list(row)
            #         # find file name relative to test_data dir
            #         test_data_rel_path = get_relative_path(
            #             test_data_split[-1], "test_data"
            #         )
            #         if test_data_rel_path is not None:
            #             # find row of expected data with same relative path
            #             for exp_r, exp_row in enumerate(self.csv_data[file][1:]):
            #                 csv_data_split = csv_to_list(exp_row)
            #                 csv_data_rel_path = get_relative_path(
            #                     csv_data_split[-1], "test_data"
            #                 )
            #                 if test_data_rel_path == csv_data_rel_path:
            #                     # csv_data and test_data rows have been matched
            #                     for c, col in enumerate(test_data_split[:-1]):
            #                         self.assertEqual(csv_data_split[c], col)

            unlink(file)

        # no recursive search
        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")
        file_processor.process_files(
            directory, no_recursive_search=True, callback=self.mock_callback
        )
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

    def test_process_files_raise_errors_kwarg(self):
        """Check that errors raised by process_file are addressed by kwarg"""
        bad_dir = "this doesn't exist!#anywhee^&*)"
        while isdir(bad_dir):
            bad_dir = bad_dir + "0"

        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")

        with self.assertRaises(FileNotFoundError):
            file_processor.process_files(
                directory,
                no_recursive_search=True,
                output_dir=bad_dir,
                raise_errors=True,
            )
        file_processor.process_files(
            directory,
            no_recursive_search=True,
            output_dir=bad_dir,
        )


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
