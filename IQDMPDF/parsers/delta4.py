#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# delta4.py
"""Delta4 QA report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.parsers.generic import ParserBase
from IQDMPDF.pdf_reader import CustomPDFReader


class Delta4Report(ParserBase):
    """Custom Delta4 report parser"""

    def __init__(self):
        """Initialize SNCPatientCustom class"""
        ParserBase.__init__(self)

        self.report_type = "Delta4Custom"
        self.columns = [
            "Patient Name",
            "Patient ID",
            "Plan Date",
            "Plan Name",
            "Meas Date",
            "Radiation Dev",
            "Energy",
            "Daily Corr",
            "Norm Dose",
            "Dev",
            "DTA",
            "Dose Dev",
            "Gamma-Index",
            "Gamma Pass Criteria",
            "Gamma Dose Criteria",
            "Gamma Dist Criteria",
            "Threshold",
            "Beam Count",
        ]
        self.identifiers = [
            "ScandiDos AB",
            "Treatment Summary",
            "Acceptance Limits",
            "Daily corr",
            "Selected Detectors",
            "Parameter Definitions & Acceptance Criteria, Detectors",
        ]
        self.analysis_columns = {
            "uid": [0, 1, 2, 3, 4],
            "date": 4,
            "criteria": [13, 14, 15, 16],
            "y": [
                {"index": 12, "ucl_limit": 100, "lcl_limit": 0},
                {"index": 11, "ucl_limit": None, "lcl_limit": None},
                {"index": 10, "ucl_limit": 100, "lcl_limit": 0},
                {"index": 9, "ucl_limit": 100, "lcl_limit": 0},
                {"index": 8, "ucl_limit": None, "lcl_limit": 0},
                {"index": 7, "ucl_limit": None, "lcl_limit": 0},
            ],
        }

    def __call__(self, report_file_path):
        """Process an IMRT QA report PDF

        Parameters
        ----------
        report_file_path : str
            File path pointing to an IMRT QA report
        """
        super().__call__(report_file_path)
        laparams_kwargs = {"line_margin": 2, 'char_margin': 100}
        self.data = CustomPDFReader(report_file_path, laparams_kwargs)

        keys = [
            "Plan:",
            "Treatment Summary",
            "Parameter Definitions",
        ]
        self.anchors = {
            key: self.data.get_bbox_of_data(
                key, return_all=True, include_text=True
            )[0]
            for key in keys
        }

        raw = self.anchors["Plan:"]["text"].split("\n")
        start = 0
        for i, row in enumerate(raw):
            if "Plan:" in row:
                start = i
                break
        stop = raw.index("Treatment Summary") if "Treatment Summary" in raw else -1
        self.plan_block = raw[start:] if stop == -1 else raw[start:stop]

        raw = self.anchors["Treatment Summary"]["text"].split("\n")
        start = raw.index("Treatment Summary") + 1
        stop = raw.index("Histograms") if "Histograms" in raw else -1
        self.treatment_summary_block = raw[start:] if stop == -1 else raw[start:stop]

        raw = self.anchors["Parameter Definitions"]["text"].split("\n")
        start = raw.index("Parameter Definitions & Acceptance Criteria, Detectors") + 2
        self.params_block = raw[start:]

        r = -1
        for r, row in enumerate(self.params_block):
            row_split = row.split(' ')
            if "Gamma" in {row_split[0], row_split[1]}:
                break
        row = self.params_block[r]
        while '  ' in ' ':
            row = row.replace('  ', ' ')
        self.gamma_index_row = row.strip().split(' ')

        self.patient_info_block = self.data.page[0].data["text"][1]
        if "Clinic: " in self.patient_info_block:
            self.patient_info_block = None

    ###########################################################################
    # Patient block
    ###########################################################################
    @property
    def patient_name(self):
        """Get the patient name

        Returns
        ----------
        str
            Patient name

        """
        if self.patient_info_block:
            if '\n' in self.patient_info_block:
                return self.patient_info_block.split('\n')[0]
            return self.patient_info_block[0]
        return ''

    @property
    def patient_id(self):
        """Get the patient ID

        Returns
        ----------
        str
            Patient ID
        """
        if self.patient_info_block:
            if '\n' in self.patient_info_block:
                return self.patient_info_block.split('\n')[1]
        return ''

    ###########################################################################
    # Plan block
    ###########################################################################
    @property
    def plan_name(self):
        """Get the plan name

        Returns
        ----------
        str
            Plan name from DICOM
        """
        for row in self.plan_block:
            if 'Plan: ' in row:
                return row.split('Plan: ')[1].strip()
        return ""

    @property
    def plan_date(self):
        """Get the plan date

        Returns
        ----------
        str
            Plan date from DICOM
        """
        return self._get_plan_block_date('Planned: ')

    @property
    def measured_date(self):
        """Get the measured name

        Returns
        ----------
        str
            Date of QA measurement
        """
        return self._get_plan_block_date('Measured: ')

    @property
    def accepted_date(self):
        """Get the QA accepted date

        Returns
        ----------
        str
            QA Accepted date from DICOM
        """
        return self._get_plan_block_date('Accepted: ')

    def _get_plan_block_date(self, key):
        """Get a date from the plan_block

        Parameters
        ----------
        key : str
            Either 'Planned: ', 'Measured: ', or 'Accepted: '

        Returns
        -------
        str
            Date for the given key
        """
        for row in self.plan_block:
            if key in row:
                info = row.split(key)[1].strip()
                while '  ' in info:
                    info = info.replace('  ', ' ').strip()
                if ' AM' in info or ' PM' in info:
                    date_str = ' '.join(info.split(' ')[:3])
                else:
                    date_str = ' '.join(info.split(' ')[:2])
                if date_str.count(".") > 1:
                    date_split = date_str.split(".")
                    month, day = date_split[1], date_split[0]
                    date_str = f"{month}/{day}/{''.join(date_split[2:])}"
                if ':' not in date_str:
                    return date_str.split(' ')[0]
                return date_str

        return ""

    ###########################################################################
    # Treatment Summary block
    ###########################################################################
    @property
    def radiation_dev(self):
        """Get the radiation device

        Returns
        ----------
        str
            Radiation device per DICOM-RT Plan
        """
        for row in self.treatment_summary_block:
            if row.startswith('Radiation Device: '):
                return row.split('Radiation Device: ')[1].strip()
        return ""

    @property
    def beam_count(self):
        """Get the number of delivered beams in the report

        Returns
        ----------
        int
            The number of beams
        """
        for r, row in enumerate(self.treatment_summary_block):
            if 'Gy' in row:
                return len(self.treatment_summary_block) - r - 1

    @property
    def composite_tx_summary_data(self):
        """Get the composite analysis data

        Returns
        ----------
        dict
            'norm_dose', 'dev', 'dta', 'gamma_index', and 'dose_dev'
        """
        for row in self.treatment_summary_block:
            if 'Gy' in row:
                units = 'cGy' if 'cGy' in row else 'Gy'
                text = row.split(units)
                pass_rate_data = text[1].strip().split('%')
                return {
                    "norm_dose": text[0].strip().split(' ')[-1] + " " + units,
                    "dev": pass_rate_data[-5].strip() + '%',
                    "dta": pass_rate_data[-4].strip() + '%',
                    "gamma_index": pass_rate_data[-3].strip() + '%',
                    "dose_dev": pass_rate_data[-2].strip() + '%',
                }

    @property
    def energy(self):
        """Beam energy

        Returns
        ----------
        str
            Energy of the first reported beam
        """
        for row in self.treatment_summary_block:
            if row.count('°') == 2:
                data = row.split('°')[-1].strip()
                data = ' '.join(data.split(' ')[:-6])
                while data[-1].isnumeric() or data[-1] == '.':
                    data = data[:-1]
                return data.strip()
        return ""

    @property
    def daily_corr(self):
        """Get the daily correction factor

        Returns
        ----------
        str
            The daily correction factor
        """
        for row in self.treatment_summary_block:
            if row.count('°') == 2:
                init_data = row.split('°')[-1].strip()
                data = ' '.join(init_data.split(' ')[:-6])
                if not data[-1].isnumeric():
                    data = ' '.join(init_data.split(' ')[:-5])
                daily_corr = ''
                while data[-1].isnumeric() or data[-1] == '.':
                    daily_corr = data[-1] + daily_corr
                    data = data[:-1]
                if daily_corr.replace('.', '').isnumeric():
                    return daily_corr
        return ""

    ###########################################################################
    # Parameter block
    ###########################################################################
    @property
    def gamma_dose(self):
        """Get the Gamma Analysis dose criteria

        Returns
        ----------
        str
            Gamma dose criteria
        """
        return self.gamma_index_row[7].replace('±', '')

    @property
    def gamma_distance(self):
        """Get the gamma distance criteria

        Returns
        ----------
        str
            Gamma analysis distance criteria
        """
        return self.gamma_index_row[8] + " " + self.gamma_index_row[9]

    @property
    def gamma_pass_criteria(self):
        """Get the gamma analysis pass-rate criteria

        Returns
        -----------
        str
            Gamma pass-rate criteria
        """
        return self.gamma_index_row[10]

    @property
    def threshold(self):
        """Get the minimum dose (%) included in analysis

        Returns
        ----------
        str
            Minimum dose threshold
        """
        return self.gamma_index_row[4]

    @property
    def summary_data(self):
        """A summary of data from the QA report

        Returns
        ----------
        dict
            Keys will match "column" elements Values are of type str
        """
        comp_tx_data = self.composite_tx_summary_data
        return {
            "Patient Name": self.patient_name,
            "Patient ID": self.patient_id,
            "Plan Date": self.plan_date,
            "Plan Name": self.plan_name,
            "Meas Date": self.measured_date,
            "Accepted Date": self.accepted_date,
            "Radiation Dev": self.radiation_dev,
            "Energy": self.energy,
            "Daily Corr": self.daily_corr,
            "Norm Dose": comp_tx_data["norm_dose"],
            "Dev": comp_tx_data["dev"],
            "DTA": comp_tx_data["dta"],
            "DTA Criteria": 'TODO',
            "Dose Dev": comp_tx_data["dose_dev"],
            "Gamma-Index": comp_tx_data["gamma_index"],
            "Gamma Pass Criteria": self.gamma_pass_criteria,
            "Gamma Dose Criteria": self.gamma_dose,
            "Gamma Dist Criteria": self.gamma_distance,
            "Threshold": self.threshold,
            "Beam Count": self.beam_count,
        }
