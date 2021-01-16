#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_file_processor.py
"""unittest cases for file_processor."""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from IQDMPDF import file_processor
from IQDMPDF.paths import DIRECTORIES
from os import listdir, unlink
from os.path import join, isdir

SIMPLE_PDF = join(DIRECTORIES["TEST_DATA"], "simple_test.pdf")


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

    def test_process_file_worker(self):
        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")
        file_path = listdir(directory)[0]
        pdf_path = join(directory, file_path)
        data = file_processor.process_file_worker(pdf_path)
        self.assertEqual(data["report_type"], "SNCPatient")

        data = file_processor.process_file_worker(SIMPLE_PDF)
        self.assertIsNone(data["report_type"])
        self.assertIsNone(data["columns"])
        self.assertIsNone(data["data"])

        data = file_processor.process_file_worker("non_existent_file.pdf")
        self.assertIsNone(data["report_type"])
        self.assertIsNone(data["columns"])
        self.assertIsNone(data["data"])

    def test_process_files(self):
        """Test process_files"""
        file_processor.process_files(
            DIRECTORIES["TEST_DATA"], output_file="unittest.csv"
        )
        test_files = [f for f in listdir() if f.endswith("_unittest.csv")]
        for file in test_files:
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

    def test_process_files_multiprocessing(self):
        """Test process_files with multiprocessing"""
        file_processor.process_files(
            DIRECTORIES["TEST_DATA"],
            output_file="unittest.csv",
            output_dir=".",
            processes=4,
        )
        test_files = [f for f in listdir() if f.endswith("_unittest.csv")]
        for file in test_files:
            unlink(file)

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

    def test_validate_kwargs(self):
        """Test validate kwargs"""
        kwargs = {"init_directory": None, "print_version": True}
        file_processor.validate_kwargs(kwargs)

        kwargs["print_version"] = False
        file_processor.validate_kwargs(kwargs)

        kwargs["init_directory"] = "."
        file_processor.validate_kwargs(kwargs)

    def test_print_callback(self):
        """Test the simple print message callback"""
        with self.assertRaises(KeyError):
            file_processor.print_callback({"bad_test": "some string"})
        file_processor.print_callback({"label": "success!"})


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
