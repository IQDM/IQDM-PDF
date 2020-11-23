#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# parser.py
"""Unified IMRT QA report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.pdf_reader import convert_pdf_to_txt
from IQDMPDF.parsers.delta4 import Delta4Report
from IQDMPDF.parsers.sncpatient import SNCPatientReport, SNCPatientReport2020

# These classes will be checked in ReportParser.get_report()
REPORT_CLASSES = [Delta4Report, SNCPatientReport, SNCPatientReport2020]


class ReportParser:
    """Determines which Report class to use, then processes the data."""

    def __init__(self, file_path):
        """Initialization class for ReportParser

        Parameters
        ----------
        file_path : str
            File path pointing to an IMRT QA report
        """
        self.file_path = file_path
        self.text = convert_pdf_to_txt(file_path)
        self.report = self.get_report()
        if self.report:
            self.columns = self.report.columns
            self.csv = self.report.csv
            self.report_type = self.report.report_type

    def get_report(self):
        """Determine the report_class, then return class with data processed"""
        for report_class in REPORT_CLASSES:
            parser = report_class()  # initialize class
            if parser.is_text_data_valid(self.text):
                parser(self.file_path)  # parse the data
                return parser
