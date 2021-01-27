#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# run_tests.py
"""unittest test suite so freeze_support can be called globally"""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also

import unittest
from tests.test_file_processor import TestFileProcessor
from tests.test_pdf_reader import TestPDFReader
from tests.test_report_parsers import (
    TestSNCPatient,
    TestSNCPatient2020,
    TestDelta4,
    TestVerisoft,
)
from tests.test_utilities import TestUtilities


test_classes = [
    TestUtilities,
    TestFileProcessor,
    TestPDFReader,
    TestSNCPatient,
    TestSNCPatient2020,
    TestDelta4,
    TestVerisoft,
]


class TestSuite:
    def __init__(self):
        """Init test suite can run"""
        self.suite = unittest.TestSuite()
        self.add_tests()
        self.run()

    def add_tests(self):
        """Add test classes"""
        for test in test_classes:
            self.suite.addTest(unittest.makeSuite(test))

    def run(self):
        """Run tests"""
        runner = unittest.TextTestRunner()
        runner.run(self.suite)


if __name__ == "__main__":
    import sys
    from multiprocessing import freeze_support

    freeze_support()  # Needed for macOS python >=3.8 and Windows
    sys.exit(unittest.main())
