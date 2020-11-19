#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
"""Main program for IMRT QA PDF report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.utilities import get_csv_row
from IQDMPDF.pdf_reader import CustomPDFReader
import json


class GenericReport:
    """Generic IMRT QA PDF report parser based on page, x, y values"""
    def __init__(self, json_file_path):
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
        """

        with open(json_file_path, 'r') as f:
            self.json_data = json.load(f)

        self.report_type = self.json_data['report_type']
        self.identifiers = self.json_data['identifiers']
        self.columns = [el["column"] for el in self.json_data['data']]
        self.LUT = {el["column"]: {"page": el["page"], "pos": el["pos"]}
                    for el in self.json_data['data']}

    def __call__(self, report_file_path):
        """Process an IMRT QA report PDF

        Parameters
        ----------
        report_file_path : str
            File path pointing to an IMRT QA report
        """
        self.data = CustomPDFReader(report_file_path)

    @property
    def summary_data(self):
        """Return a dictionary of parsed data, with columns for keys"""
        return {
            c: self.data.get_block_data(**self.LUT[c]) for c in self.columns
        }

    @property
    def csv(self):
        """Get a CSV of summary_data for all columns"""
        return get_csv_row(self.summary_data, self.columns)
