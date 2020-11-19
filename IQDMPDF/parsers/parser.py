# -*- coding: utf-8 -*-
"""
main program for IMRT QA PDF report parser
Created on Thu May 30 2019
@author: Dan Cutright, PhD
"""

from IQDMPDF.pdf_reader import convert_pdf_to_txt
from IQDMPDF.utilities import are_all_strings_in_text
from IQDMPDF.parsers.delta4 import Delta4Report
from IQDMPDF.parsers.sncpatient import SNCPatientReport

# These classes will be checked in ReportParser.get_report()
REPORT_CLASSES = [Delta4Report, SNCPatientReport]


class ReportParser:
    """
    This class determines which Report class to use and subsequently processes the data.

    Use of this class requires each report class listed in REPORT_CLASSES contains the following properties:
        identifiers:    this is a list of strings that collectively are uniquely found in a report type
        columns:        a list of strings indicating the columns of the csv to be output
        csv:            a string of values for each column, delimited with DELIMITER in utilities.py
        report_type:    a string describing the report, this will be used in the results filename created in main.py

    This class also requires the a __call__ method that accepts a file path to process the file.
    Processing the data does not occur until this is called

    If ReportParser.report is None, the input text was not identified to be any of the report classes listed in
    REPORT_CLASSES
    """

    def __init__(self, file_path):
        self.text = convert_pdf_to_txt(file_path)
        self.report = self.get_report(file_path)
        if self.report:
            self.columns = self.report.columns
            self.csv = self.report.csv
            self.report_type = self.report.report_type

    def get_report(self, file_path):
        for report_class in REPORT_CLASSES:
            parser = report_class()  # initialize class
            if are_all_strings_in_text(self.text, parser.identifiers):
                parser(file_path)  # parse the data
                return parser
