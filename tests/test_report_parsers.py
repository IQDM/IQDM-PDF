#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_report_parsers.py
"""unittest cases for delta4 parser."""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from tests.test_data.expected_report_data import TestDataHelper
from IQDMPDF.pdf_reader import convert_pdf_to_txt
from IQDMPDF.parsers import sncpatient
from IQDMPDF.parsers import delta4
from IQDMPDF.parsers import verisoft

TestDataHelper.__test__ = False

PARSERS = {
    "sncpatient": sncpatient.SNCPatientReport,
    "delta4": delta4.Delta4Report,
    "sncpatient2020": sncpatient.SNCPatientReport2020,
    "verisoft": verisoft.VeriSoftReport,
}


class TestReportParserBase:
    """Base class for report parser testing, so not to repeat code"""

    def do_setup_for_vendor(self, vendor):
        print("Running Unit Test for %s" % vendor)
        self.vendor = vendor
        self.parser = self.get_parser()
        self.test_data = self.get_test_data()
        self.text = self.get_text()
        self.other_text = self.get_other_text()

    def get_parser(self):
        """Return an initialized parser"""
        return PARSERS[self.vendor]()

    def get_test_data(self):
        """Get a TestDataHelper class for this vendor"""
        return TestDataHelper(self.vendor)

    def get_text(self):
        """Convert test PDFs into text"""
        return {
            key: convert_pdf_to_txt(path)
            for key, path in self.test_data.file_paths.items()
        }

    def get_other_text(self):
        """Collect the file paths for other vendors"""
        return [
            convert_pdf_to_txt(path)
            for path in self.test_data.other_file_paths
        ]

    def test_is_text_valid(self):
        """Check that identifiers are valid and do not work on others"""
        if hasattr(self, "text"):  # make sure class is initialized
            for text in self.text.values():
                self.assertTrue(self.parser.is_text_data_valid(text))
            for text in self.other_text:
                self.assertFalse(self.parser.is_text_data_valid(text))

    def test_example_data(self):
        """Verify example data is parsed correctly"""
        if hasattr(self, "text"):  # make sure class is initialized
            for case_key in self.test_data.expected_data.keys():
                print("Running example data test: case_key %s" % case_key)
                self.parser(self.test_data.file_paths[case_key])
                data = self.parser.summary_data
                for key, value in self.test_data.expected_data[
                    case_key
                ].items():
                    self.assertEqual(data[key], value)


class TestSNCPatient(TestReportParserBase, unittest.TestCase):
    def setUp(self):
        self.do_setup_for_vendor("sncpatient")


class TestSNCPatient2020(TestReportParserBase, unittest.TestCase):
    def setUp(self):
        self.do_setup_for_vendor("sncpatient2020")

    def test_append_column_to_existing_ignore(self):
        """Test that column gets assigned to a pre-existing ignored array """
        parser = PARSERS["sncpatient2020"]()
        column = "Patient Name"
        parser.LUT[column]["ignored"] = []
        parser._assign_ignored(column, parser.LUT[column])
        self.assertEqual(parser.LUT[column]["ignored"], [column])


class TestDelta4(TestReportParserBase, unittest.TestCase):
    def setUp(self):
        self.do_setup_for_vendor("delta4")


class TestVerisoft(TestReportParserBase, unittest.TestCase):
    def setUp(self):
        self.do_setup_for_vendor("verisoft")


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
