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


EXAMPLE_DATA = {
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

OTHER_REPORTS = {
    0: join(DIRECTORIES["DELTA4_EXAMPLES"], "UChicago", "DCAM_example_1.pdf"),
    1: join(DIRECTORIES["DELTA4_EXAMPLES"], "UChicago", "DCAM_example_2.pdf"),
}

EXPECTED = {
    0: {
        "Patient Name": "",
        "Patient ID": "WP-001",
        "QA Date": "9/25/2020",
        "Plan Date": "2020-09-25",
        "Energy": "6x",
        "Angle": "",
        "SSD": "100.0",
        "SDD": "",
        "Depth": "",
        "Dose Type": "Absolute",
        "Difference (%)": "2",
        "Distance (mm)": "2",
        "Threshold (%)": "10.0",
        "Meas Uncertainty": "No",
        "Use Global (%)": "Yes",
        "Summary Type": "Gamma",
        "Total Points": "68",
        "Pass": "68",
        "Fail": "0",
        "Pass (%)": "100",
        "Notes": "2% 2mm TB4",
        "Meas File": "...\\5by5 6x.txt",
        "Plan File": "...\\Water_...",
    },
    1: {
        "Patient Name": "",
        "Patient ID": "",
        "QA Date": "2/5/2020",
        "Plan Date": "2/5/2020",
        "Energy": "6X",
        "Angle": "",
        "SSD": "",
        "SDD": "",
        "Depth": "",
        "Dose Type": "Absolute",
        "Difference (%)": "2.0",
        "Distance (mm)": "2.0",
        "Threshold (%)": "20.0",
        "Meas Uncertainty": "No",
        "Use Global (%)": "No",
        "Summary Type": "GC",
        "Total Points": "567",
        "Pass": "512",
        "Fail": "55",
        "Pass (%)": "90.3",
        "Notes": "Notes\nbst1 \npelvis\nSLC",
        "Meas File": "",
        "Plan File": "",
    },
    2: {
        "Patient Name": "",
        "Patient ID": "",
        "QA Date": "2/5/2020",
        "Plan Date": "2/5/2020",
        "Energy": "6X",
        "Angle": "",
        "SSD": "",
        "SDD": "",
        "Depth": "",
        "Dose Type": "Absolute",
        "Difference (%)": "2.0",
        "Distance (mm)": "2.0",
        "Threshold (%)": "20.0",
        "Meas Uncertainty": "No",
        "Use Global (%)": "No",
        "Summary Type": "GC",
        "Total Points": "2197",
        "Pass": "1940",
        "Fail": "257",
        "Pass (%)": "88.3",
        "Notes": "Notes\nFields 1-2\nPelvis=Cervix+PM+LNs\nSLF",
        "Meas File": "",
        "Plan File": "",
    },
}


class TestSNCPatient(unittest.TestCase):
    """Unit tests for sncpatient."""

    def setUp(self):
        self.parser = sncpatient.SNCPatientReport()
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
