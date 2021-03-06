#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# parser.py
"""Unified IMRT QA report parser"""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.pdf_reader import convert_pdf_to_txt
from IQDMPDF.parsers.delta4 import Delta4Report
from IQDMPDF.parsers.sncpatient import SNCPatientCustom, SNCPatientReport2020
from IQDMPDF.parsers.verisoft import VeriSoftReport
from IQDMPDF.utilities import creation_date

# These classes will be checked in ReportParser.get_report()
REPORT_CLASSES = [
    Delta4Report,
    SNCPatientCustom,
    SNCPatientReport2020,
    VeriSoftReport,
]


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
        self.creation_date = creation_date(file_path)

    def get_report(self):
        """Determine the report_class, then return class with data processed

        Returns
        ----------
        ParserBase inherited class
            Searches for a Report Class with matching identifiers, processes
            the file and returns the Report Class
        """
        for report_class in REPORT_CLASSES:
            parser = report_class()  # initialize class
            if parser.is_text_data_valid(self.text):
                parser(self.file_path)  # parse the data
                return parser

    @property
    def columns(self):
        """Get columns headers for csv

        Returns
        ----------
        list
            Report columns + "report_file_creation" + "report_file_path"
        """
        columns = getattr(self.report, "columns", None)
        file_info = ["report_file_creation", "report_file_path"]
        return columns + file_info if columns else []

    @property
    def csv_data(self):
        """Get a csv string from the selected ReportParser

        Returns
        ----------
        str
            Report columns + "report_file_creation" + "report_file_path"
        """
        csv_data = getattr(self.report, "csv_data", None)
        file_info = [self.creation_date, self.file_path]
        return csv_data + file_info if csv_data else [""]

    @property
    def report_type(self):
        """Get report type of the selected ReportParser

        Returns
        ----------
        str
            Get ReportParser.report_type
        """
        return getattr(self.report, "report_type", "")
