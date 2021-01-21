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
        """Initialize columns and identifiers"""
        self.columns = []
        self.identifiers = []

    def __call__(self, file_path):
        """"Save file path and text"""
        self.file_path = file_path
        self.text = convert_pdf_to_txt(file_path).split("\n")

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
    def csv(self):
        """Get a CSV of summary_data for all columns

        Returns
        ----------
        str
            Output from ``utilities.get_csv_row``. File path automatically
            appended to data
        """
        return get_csv_row(self.summary_data, self.columns)


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
            an integer or a list of integers (i.e., [x_tol, y_tol]). Also,
            specifying 'numeric' with a boolean value will ensure the value is
            or is not numeric (and return an empty string if not met). The
            JSON object can also have "alternates" which contains an array of
            data like items that will be checked until a value for a column is
            found. "ignored" is another option, if a value is returned that is
            in this array, an empty string will be returned instead. The value
            of "column" is automatically added to the "ignored" array.
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
            el["column"]: {
                key: value for key, value in el.items() if key != "column"
            }
            for el in self.json_data["data"]
        }
        self._process_ignored_from_json(self.LUT)

        self.text_cleaner = text_cleaner

        self.missing_columns = []

    def _process_ignored_from_json(self, LUT):
        """Add column to ignored key in each json_data data item

        Parameters
        ----------
        LUT : dict
            Processed dictionary from self.json_data["data"] or
            self.json_data["alternates"] where keys are values from "column"

        """
        for column, data in LUT.items():
            self._assign_ignored(column, data)

    @staticmethod
    def _assign_ignored(column, data):
        """Ensure data has ignored key, ensure column is in data['ignored']"""
        if "ignored" in data.keys():
            if column not in data["ignored"]:
                data["ignored"].append(column)
        else:
            data["ignored"] = [column]

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

        self._process_block_data(data)
        self._apply_alternates(data)

        return data

    def _process_block_data(self, data):
        """Get the first item in data blocks, update missing_columns

        Parameters
        ----------
        data : dict
            Has values of the return from CustomPDFReader.get_block_data

        """
        for key in list(data):
            data[key] = data[key][0] if len(data[key]) else ""
            if data[key] == "":
                self.missing_columns.append(key)

    def _apply_alternates(self, data):
        """Check json_data["alternates"] for alternate instructions. Unlike
        json_data["data"], multiple instances of a column can exist in
        alternates. The code will check each item in alternate until a value
        is found for that column (if a value isn't already found).

        Parameters
        ----------
        data : dict
            Data from CustomPDFReader.get_block_data

        Returns
        -------
        dict
            data edited by alternates if value is an empty string
        """
        if "alternates" in self.json_data:
            for alternate in self.json_data["alternates"]:
                key = alternate["column"]
                alt = {k: v for k, v in alternate.items() if k != "column"}
                self._assign_ignored(key, alt)
                alt["ignored"].extend(self.LUT[key])
                if key in self.missing_columns:
                    data[key] = self.data.get_block_data(
                        **alt, text_cleaner=self.text_cleaner
                    )
                    data[key] = data[key][0] if len(data[key]) else ""
                    if data[key] != "":
                        self.missing_columns.pop(
                            self.missing_columns.index(key)
                        )
