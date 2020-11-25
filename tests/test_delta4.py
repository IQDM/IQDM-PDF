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
from IQDMPDF.paths import DIRECTORIES
from IQDMPDF.pdf_reader import convert_pdf_to_txt
from os.path import join


EXAMPLE_DATA = {
    0: join(DIRECTORIES["DELTA4_EXAMPLES"], "UChicago", "DCAM_example_1.pdf"),
    1: join(DIRECTORIES["DELTA4_EXAMPLES"], "UChicago", "DCAM_example_2.pdf"),
}
OTHER_REPORTS = {
    0: join(
        DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago", "DCAM_example_1.pdf"
    ),
    1: join(
        DIRECTORIES["SNCPATIENT_EXAMPLES"],
        "Northwestern_Memorial",
        "ArcCheck_Example_1.pdf",
    ),
    2: join(
        DIRECTORIES["SNCPATIENT_EXAMPLES"],
        "Northwestern_Memorial",
        "ArcCheck_Example_2.pdf",
    ),
}

EXPECTED = {
    0: {
        "Patient Name": "UCM, TG119",
        "Patient ID": "0097",
        "Plan Date": "5/19/2020  4:17 PM",
        "Meas Date": "5/20/2020  4:25 PM",
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
    },
    1: {
        "Patient Name": "",
        "Patient ID": "",
        "Plan Date": "11/20/2020",
        "Meas Date": "11/20/2020",
        "Energy": "6 MV",
        "Daily Corr": "1.081",
        "Norm Dose": "303 cGy",
        "Dev": "95.4%",
        "DTA": "87.4%",
        "Gamma-Index": "92.1%",
        "Dose Dev": "2.0%",
        "Radiation Dev": "UC_M120",
        "Gamma Pass Criteria": "95%",
        "Gamma Dose Criteria": "3.0%",
        "Gamma Dist Criteria": "2.0 mm",
        "Beam Count": 4,
    },
}


class TestDelta4(unittest.TestCase):
    """Unit tests for delta4."""

    def setUp(self):
        self.parser = delta4.Delta4Report()
        self.text = {
            key: convert_pdf_to_txt(path) for key, path in EXAMPLE_DATA.items()
        }
        self.other_text = {
            key: convert_pdf_to_txt(path)
            for key, path in OTHER_REPORTS.items()
        }

    def test_is_text_valid(self):
        """Check that identifiers are valid and do not work on others"""
        for text in self.text.values():
            self.assertTrue(self.parser.is_text_data_valid(text))
        for text in self.other_text.values():
            self.assertFalse(self.parser.is_text_data_valid(text))

    def test_example_data(self):
        """Verify example data is parsed correctly"""
        for key in EXPECTED.keys():
            self.run_example_data_test(key)

    def run_example_data_test(self, index):
        print("Running example data test: index %s" % index)
        self.parser(EXAMPLE_DATA[index])
        data = self.parser.summary_data
        for key, value in EXPECTED[index].items():
            self.assertEqual(data[key], value)


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
