#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_main.py
"""unittest cases for main."""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from IQDMPDF import main
from IQDMPDF.paths import DIRECTORIES
from os import listdir, unlink
from os.path import join


class TestMain(unittest.TestCase):
    """Unit tests for Utilities."""

    def setUp(self):
        """Setup files and base data for utility testing."""
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
        main.process_file(pdf_path, output_file, output_dir=output_dir)
        unlink(join(output_dir, "SNCPatient_" + output_file))

    def test_process_files(self):
        """Test process_files with example reports"""
        main.process_files(
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
        main.process_files(directory, no_recursive_search=True)
        test_files = [
            f
            for f in listdir()
            if f.startswith("SNCPatient_results_") and f.endswith(".csv")
        ]
        for file in test_files:
            unlink(file)

    def test_create_arg_parser(self):
        """Test arg parser creation"""
        arg_parser = main.create_arg_parser().parse_args([])
        expected_args = [
            "ignore_extension",
            "output_dir",
            "output_file",
            "print_version",
            "no_recursive_search",
            "directory",
        ]
        for arg in expected_args:
            self.assertTrue(arg in arg_parser.__dict__.keys())

    def test_main(self):
        """Test remainder of main.main"""
        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")
        args = main.create_arg_parser().parse_args(["-v"])
        main.main(args)
        args = main.create_arg_parser().parse_args([])
        main.main(args)
        args = main.create_arg_parser().parse_args(
            [directory, "--version", "-of", "test"]
        )
        main.main(args)
        unlink("SNCPatient_test")


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
