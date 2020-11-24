#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sncpatient.py
"""SNC Patient report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.parsers.generic import GenericReport
from IQDMPDF.paths import DIRECTORIES
from os.path import join


class SNCPatientReport2020(GenericReport):
    """SNCPatientReport parser for the new format released in 2020"""

    def __init__(self):
        """Initialization of a SNCPatientReport class"""
        template = join(DIRECTORIES["REPORT_TEMPLATES"], "sncpatient2020.json")
        GenericReport.__init__(self, template)


class SNCPatientReport(GenericReport):
    """SNCPatientReport parser for the new format released prior to 2020"""

    def __init__(self):
        """Initialization of a SNCPatientReport class"""
        template = join(DIRECTORIES["REPORT_TEMPLATES"], "sncpatient.json")
        GenericReport.__init__(self, template, text_cleaner=self.text_cleaner)

    @staticmethod
    def text_cleaner(text):
        """This is called on each text element

        Parameters
        ----------
        text : str
            Text element to be cleaned

        Returns
        ----------
        str
            The text element with " :" removed, then str.strip() called
        """
        return text.replace(" :", "").strip()

    @property
    def summary_data(self):
        """Override GenericReport.summary_data for SNCPatientReport

        Returns
        ----------
        dict
            GenericReport.summary_data with customized edits to QA Date,
            Dose Type, and Summary Type
        """
        data = super().summary_data
        data["QA Date"] = data["QA Date"].split(": ")[1].strip()
        data["Dose Type"] = (
            data["Dose Type"]
            .split("\n")[0]
            .replace("Dose Comparison", "")
            .strip()
        )

        data["Summary Type"] = (
            data["Summary Type"].split("(")[1].split("Analysis")[0].strip()
        )

        return data
