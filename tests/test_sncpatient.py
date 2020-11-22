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
from IQDMPDF.parsers import sncpatient
from IQDMPDF.paths import DIRECTORIES
from IQDMPDF.pdf_reader import convert_pdf_to_txt
from os.path import join


EXAMPLE_DATA = [
    join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago", "DCAM_example_1.pdf")
]

OTHER_REPORTS = [
    join(DIRECTORIES["DELTA4_EXAMPLES"], "UChicago", "DCAM_example_1.pdf")
]


class TestDelta4(unittest.TestCase):
    """Unit tests for sncpatient."""

    def setUp(self):
        self.parser = sncpatient.SNCPatientReport()
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
        expected = {"Patient Name": '',
                    "Patient ID": 'WP-001',
                    "QA Date": '9/25/2020',
                    "Plan Date": '2020-09-25',
                    "Energy": '6x',
                    "Angle": '',
                    "SSD": '100.0',
                    "SDD": '',
                    "Depth": '',
                    "Dose Type": 'Absolute',
                    "Difference (%)": '',
                    "Distance (mm)": '2',
                    "Threshold (%)": '10.0',
                    "Meas Uncertainty": 'No',
                    "Use Global (%)": 'Yes',
                    "Summary Type": 'Gamma',
                    "Total Points": '68',
                    "Pass": '68',
                    "Fail": '0',
                    "Pass (%)": '100',
                    "Notes": '2% 2mm TB4',
                    "Meas File": '...\\5by5 6x.txt',
                    "Plan File": '...\\Water_...'}
        for key, value in expected.items():
            self.assertEqual(data[key], value)


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
