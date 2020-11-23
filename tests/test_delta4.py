#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_delta4.py
"""unittest cases for delta4 parser."""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from IQDMPDF.parsers import delta4
from IQDMPDF.pdf_reader import convert_pdf_to_txt
from os.path import join


BASEDATA_DIR = join("tests", "test_data", "example_reports")


EXAMPLE_DATA = [
    join(BASEDATA_DIR, 'delta4', "UChicago", "DCAM_example_1.pdf")
]


OTHER_REPORTS = [
    join(BASEDATA_DIR, 'sncpatient', "UChicago", "DCAM_example_1.pdf")
]

class TestDelta4(unittest.TestCase):
    """Unit tests for delta4."""

    def setUp(self):
        self.parser = delta4.Delta4Report()
        self.text = [convert_pdf_to_txt(path) for path in EXAMPLE_DATA]
        self.other_text = [convert_pdf_to_txt(path) for path in OTHER_REPORTS]

    def test_is_text_valid(self):
        """Check that identifiers are valid and do not work on others"""
        for text in self.text:
            self.assertTrue(self.parser.is_text_data_valid(text))
        for text in self.other_text:
            self.assertFalse(self.parser.is_text_data_valid(text))

    def test_example_data_0(self):
        """Verify example data is parsed correctly: Example data index 0"""
        self.parser(EXAMPLE_DATA[0])
        data = self.parser.summary_data
        expected = {
            "Patient Name": "UCM, TG119",
            "Patient ID": "0097",
            "Plan Date": "5/19/2020  4:17 PM",
            "Energy": "6 MV, FFF",
            "Daily Corr": "1.039",
            "Norm Dose": "186 cGy",
            "Dev": "98.8%",
            "DTA": "96.3%",
            "Gamma-Index": "91.0%",
            "Dose Dev": "-0.3%",
            "Radiation Dev": "TrueBeamSN1203",
            "Gamma Pass Criteria": "95%",
            "Gamma Dose Criteria": "2.0%",
            "Gamma Dist Criteria": "2.0 mm",
            "Beam Count": 2,
        }
        for key, value in expected.items():
            self.assertEqual(value, data[key])


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
