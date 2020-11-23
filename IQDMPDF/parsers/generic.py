#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# generic.py
"""Generic IMRT QA report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.utilities import get_csv_row, are_all_strings_in_text
from IQDMPDF.pdf_reader import CustomPDFReader, convert_pdf_to_txt
import json


class ParserBase:
    """Base class for all Report Parser classes, not to be used alone"""

    def __init__(self):
        self.columns = []
        self.identifiers = []

    def __call__(self, file_path):
        """"Save file path and text"""
        self.file_path = file_path
        self.text = convert_pdf_to_txt(file_path).split("\n")

    def print(self):
        if hasattr(self, "data"):
            self.data.print()

    def is_text_data_valid(self, text):
        """Check that all identifiers are in text

        Parameters
        ----------
        text : str
            Output from pdf_reader.convert_pdf_to_txt

        Returns
        ----------
        bool
            True if and only if all identifiers are found in text
        """
        return are_all_strings_in_text(text, self.identifiers)

    @property
    def summary_data(self):
        """Should be overwritten in child class

        Returns
        ----------
        dict
            Keys will match "column" elements from the JSON file. Values are
            of type str
        """
        return {}

    @property
    def csv(self):
        """Get a CSV of summary_data for all columns

        Returns
        ----------
        str
            Output from utilities.get_csv_row. File path automatically
            appended to data
        """
        data = {key: value for key, value in self.summary_data.items()}
        data["file_path"] = self.file_path
        return get_csv_row(data, self.columns + ["file_path"])


class GenericReport(ParserBase):
    """Generic IMRT QA PDF report parser based on page, x, y values"""

    def __init__(self, json_file_path, text_cleaner=None):
        """Initialization of a GenericReport class

        Parameters
        ----------
        json_file_path : str
            File path to a JSON file describing the PDF report.
            It should contain these keys (type): report_type (str),
            identifiers (list of str), and data (list).
            The format of each data element should be
            {'column': [str], 'page': [int], 'pos': [float, float]}.
            Optionally, you can also supply 'tol', which is either
            an integer or a list of integers (i.e., [x_tol, y_tol]).
        text_cleaner : callable, optional
            A function called on each text element (e.g., remove leading ':')
        """

        ParserBase.__init__(self)

        with open(json_file_path, "r") as f:
            self.json_data = json.load(f)

        self.report_type = self.json_data["report_type"]
        self.identifiers = self.json_data["identifiers"]
        self.columns = [el["column"] for el in self.json_data["data"]]
        self.LUT = {
            el["column"]: {"page": el["page"], "pos": el["pos"]}
            for el in self.json_data["data"]
        }
        self.text_cleaner = text_cleaner

    def __call__(self, report_file_path):
        """Process an IMRT QA report PDF

        Parameters
        ----------
        report_file_path : str
            File path pointing to an IMRT QA report
        """
        super().__call__(report_file_path)
        self.data = CustomPDFReader(report_file_path)

    @property
    def summary_data(self):
        """A summary of data from the QA report

        Returns
        ----------
        dict
            Keys will match "column" elements from the JSON file. Values are
            of type str
        """
        data = {
            c: self.data.get_block_data(
                **self.LUT[c], text_cleaner=self.text_cleaner
            )
            for c in self.columns
        }
        for key in list(data):
            data[key] = data[key][0] if len(data[key]) else ""
        return data
