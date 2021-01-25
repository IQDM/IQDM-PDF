#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# paths.py
"""Paths for IMRT QA PDF report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

import sys
from os.path import join, dirname

SCRIPT_DIR = dirname(__file__)
# PyInstaller compatibility
PARENT_DIR = getattr(sys, "_MEIPASS", dirname(SCRIPT_DIR))
LICENSE_PATH = join(PARENT_DIR, "LICENSE")
PARSERS_DIR = join(SCRIPT_DIR, "parsers")
REPORT_TEMPLATES_DIR = join(SCRIPT_DIR, "report_templates")
TESTS_DIR = join(PARENT_DIR, "tests")
TEST_DATA_DIR = join(TESTS_DIR, "test_data")
EXAMPLE_PDF_DIR = join(TEST_DATA_DIR, "example_reports")
EXAMPLE_CSV_DIR = join(TEST_DATA_DIR, "example_csv_output")

# Example PDF directories by vendor
DELTA4_EXAMPLES_DIR = join(EXAMPLE_PDF_DIR, "delta4")
SNCPATIENT_EXAMPLES_DIR = join(EXAMPLE_PDF_DIR, "sncpatient")
SNCPATIENT2020_EXAMPLES_DIR = join(EXAMPLE_PDF_DIR, "sncpatient2020")
VERISOFT_EXAMPLES_DIR = join(EXAMPLE_PDF_DIR, "verisoft")

DIRECTORIES = {
    key[:-4]: value for key, value in locals().items() if key.endswith("_DIR")
}
