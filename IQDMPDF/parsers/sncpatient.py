#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sncpatient.py
"""SNC Patient report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.parsers.generic import GenericReport, ParserBase
from IQDMPDF.pdf_reader import CustomPDFReader
from IQDMPDF.paths import DIRECTORIES
from os.path import join


class SNCPatientReport2020(GenericReport):
    """SNCPatientReport parser for the new format released in 2020"""

    def __init__(self):
        """Initialization of a SNCPatientReport class"""
        template = join(DIRECTORIES["REPORT_TEMPLATES"], "sncpatient2020.json")
        GenericReport.__init__(self, template)
        self.analysis_columns = {
            "uid": [0, 1, 2, 5],
            "date": 2,
            "criteria": [14, 8, 11, 13, 9, 10, 12],
            "y": [
                {"index": 15, "ucl_limit": 100, "lcl_limit": 0},
                {"index": 16, "ucl_limit": None, "lcl_limit": 0},
                {"index": 17, "ucl_limit": None, "lcl_limit": 0},
                {"index": 18, "ucl_limit": None, "lcl_limit": 0},
                {"index": 7, "ucl_limit": None, "lcl_limit": 0},
            ],
        }


# class SNCPatientReport(GenericReport):
#     """SNCPatientReport parser for the new format released prior to 2020"""
#
#     def __init__(self):
#         """Initialization of a SNCPatientReport class"""
#         template = join(DIRECTORIES["REPORT_TEMPLATES"], "sncpatient.json")
#         GenericReport.__init__(self, template, text_cleaner=self.text_cleaner)
#
#     @staticmethod
#     def text_cleaner(text):
#         """This is called on each text element
#
#         Parameters
#         ----------
#         text : str
#             Text element to be cleaned
#
#         Returns
#         ----------
#         str
#             The text element with " :" removed, then str.strip() called
#         """
#         return text.replace(" :", "").strip()
#
#     @property
#     def summary_data(self):
#         """Override GenericReport.summary_data for SNCPatientReport
#
#         Returns
#         ----------
#         dict
#             GenericReport.summary_data with customized edits to QA Date,
#             Dose Type, and Summary Type
#         """
#         data = super().summary_data
#         data["QA Date"] = data["QA Date"].split(": ")[1].strip()
#         data["Dose Type"] = (
#             data["Dose Type"]
#             .split("\n")[0]
#             .replace("Dose Comparison", "")
#             .strip()
#         )
#
#         data["Summary Type"] = (
#             data["Summary Type"].split("(")[1].split("Analysis")[0].strip()
#         )
#
#         return data


class SNCPatientCustom(ParserBase):
    """Custom SNCPatient report parser"""

    def __init__(self):
        """Initialize SNCPatientCustom class"""
        ParserBase.__init__(self)

        self.report_type = "SNCPatientCustom"
        self.columns = [
            "Patient Name",
            "Patient ID",
            "QA Date",
            "Plan Date",
            "Energy",
            "Angle",
            "SSD",
            "SDD",
            "Depth",
            "Dose Type",
            "Difference (%)",
            "Distance (mm)",
            "Threshold (%)",
            "Rotation Angle",
            "Meas Uncertainty",
            "Use Global (%)",
            "Dose Diff Thresh",
            "Use VanDyk",
            "Summary Type",
            "Total Points",
            "Pass",
            "Fail",
            "Pass (%)",
            "Notes",
        ]
        self.identifiers = [
            "QA File Parameter",
            "Threshold",
            "Notes",
            "Reviewed By :",
            "SSD",
            "Depth",
            "Energy",
        ]
        self.analysis_columns = {
            "uid": [0, 1, 2],
            "date": 2,
            "criteria": [18, 9, 10, 11, 12, 16, 15, 14, 17],
            "y": [
                {"index": 22, "ucl_limit": 100, "lcl_limit": 0},
                {"index": 20, "ucl_limit": None, "lcl_limit": 0},
                {"index": 21, "ucl_limit": None, "lcl_limit": 0},
                {"index": 19, "ucl_limit": None, "lcl_limit": 0},
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
        laparams_kwargs = {"line_margin": 1}
        self.data = CustomPDFReader(report_file_path, laparams_kwargs)

        keys = [
            "Date:",
            "QA File Parameter",
            "Dose Comparison",
            "Summary",
            "Notes",
        ]
        self.anchors = {
            key: self.data.get_bbox_of_data(
                key, return_all=True, include_text=True
            )[0]
            for key in keys
        }

        self.file_param_block = self._get_lateral_block("QA File Parameter")
        while len(self.file_param_block) < 7:  # in case redaction removed ':'
            self.file_param_block.insert(0, ":")

        self.comparison_block = self.anchors["Dose Comparison"]["text"]
        if self.comparison_block.count(":") < 3:
            self.comparison_block = self._get_lateral_block("Dose Comparison")
        else:
            self.comparison_block = [
                row for row in self.comparison_block.split("\n") if ":" in row
            ]

        self.summary_block = self.anchors["Summary"]["text"]
        if self.summary_block.count(":") < 3:
            self.summary_block = self._get_lateral_block("Summary", y_tol=20)
        else:
            self.summary_block = [
                row for row in self.summary_block.split("\n") if ":" in row
            ]

        self.block_lut = {
            "QA File Parameter": self.file_param_block,
            "Dose Comparison": self.comparison_block,
            "Summary": self.summary_block,
        }

    ########################################################################
    # Utilities
    ########################################################################
    def _get_lateral_block(self, anchor_key, y_tol=10):
        """Search for data laterally from an anchor / header block

        Parameters
        ----------
        anchor_key : str
            Key to SNCPatientCustom.anchors
        y_tol : int
            tolerance in y direction for CustomPDFReader.get_block_data

        Returns
        -------
        list, None
            Get the text data laterally from column headers in V

        """
        anchor = self.anchors[anchor_key]
        if anchor is not None:
            data = self.data.get_block_data(
                anchor["page"],
                (anchor["bbox"][0], anchor["bbox"][1]),
                tol=(100, y_tol),
            )

            for el in data:
                if anchor_key not in el:
                    return el.split("\n")

    @staticmethod
    def _get_block_element(block, index):
        """Get Value of block[index], or return 'N/A' if block is ``None``

        Parameters
        ----------
        block : list
            text block data (e.g, gamma_results_block)
        index : int
            index of block to return

        Returns
        -------
        str
            Value of ``block``[``index``] of "N/A"
        """
        try:
            return block[index].replace(":", "").strip()
        except Exception:
            return "N/A"

    def _get_row_index(self, anchor_key, keyword):
        """Look up the block index based on its variable name

        Parameters
        ----------
        anchor_key : str
            key for ``SNCPatient.anchors`` (i.e., "Date:", "QA File Parameter",
            "Dose Comparison", "Summary", "Dose Values in", "Notes")
        keyword : str
            variable name (or partial name)

        Returns
        -------
        int
            index of data block for the given keyword (header row ignored)
        """
        text = self.anchors[anchor_key]["text"].split("\n")
        text = [row for row in text if ":" not in row]
        for i, row in enumerate(text[1:]):
            if keyword in row:
                return i

    def _get_block_element_by_key(self, anchor_key, keyword):
        """Get the block element value based on a variable name

        Parameters
        ----------
        anchor_key : str
            key for ``SNCPatient.anchors`` (i.e., "Date:", "QA File Parameter",
            "Dose Comparison", "Summary", "Dose Values in", "Notes")
        keyword : str
            variable name or partial variable name (e.g., 'Distance', Passed)

        Returns
        -------
        str
            value on right side of report table

        """
        index = self._get_row_index(anchor_key, keyword)
        block = self.block_lut[anchor_key]
        return self._get_block_element(block, index)

    ########################################################################
    # Report Header Block
    ########################################################################
    @property
    def qa_date(self):
        """Date in top-left of the report

        Returns
        -------
        str
            QA report date
        """
        return self.anchors["Date:"]["text"].split("Date:")[1].strip()

    ########################################################################
    # File Param Block
    ########################################################################
    @property
    def patient_name(self):
        """Patient name in QA File Parameter table

        Returns
        -------
        str
            Patient name
        """
        return self._get_block_element_by_key(
            "QA File Parameter", "Patient Name"
        )

    @property
    def patient_id(self):
        """Patient ID in QA File Parameter table

        Returns
        -------
        str
            Patient ID
        """
        return self._get_block_element_by_key(
            "QA File Parameter", "Patient ID"
        )

    @property
    def plan_date(self):
        """Plan date in QA File Parameter table

        Returns
        -------
        str
            Plan date
        """
        return self._get_block_element_by_key("QA File Parameter", "Plan Date")

    @property
    def ssd(self):
        """SSD in QA File Parameter table

        Returns
        -------
        str
            SSD
        """
        return self._get_block_element_by_key("QA File Parameter", "SSD")

    @property
    def sdd(self):
        """SDD in QA File Parameter table

        Returns
        -------
        str
            SDD
        """
        return self._get_block_element_by_key("QA File Parameter", "SDD")

    @property
    def depth(self):
        """Depth in QA File Parameter table

        Returns
        -------
        str
            Depth
        """
        return self._get_block_element_by_key("QA File Parameter", "Depth")

    @property
    def energy(self):
        """Energy in QA File Parameter table

        Returns
        -------
        str
            Energy
        """
        return self._get_block_element_by_key("QA File Parameter", "Energy")

    @property
    def angle(self):
        """Angle in QA File Parameter table

        Returns
        -------
        str
            Angle
        """
        return self._get_block_element_by_key("QA File Parameter", "Angle")

    ########################################################################
    # Dose Comparison Block
    ########################################################################
    @property
    def dose_comparison_type(self):
        """Dose comparison type based on table title

        Returns
        -------
        str
            Dose comparison type (e.g., Absolute)
        """
        return (
            self.anchors["Dose Comparison"]["text"]
            .split("\n")[0]
            .split(" ")[0]
            .strip()
        )

    @property
    def dose_diff_param(self):
        """Dose difference criteria

        Returns
        -------
        str
            Dose difference criteria for analysis
        """
        ans = self._get_block_element_by_key(
            "Dose Comparison", "Difference (%)"
        )
        if ans == "N/A":
            return self._get_block_element_by_key("Dose Comparison", "% Diff")
        return ans

    @property
    def dist_param(self):
        """Distance criteria

        Returns
        -------
        str
            Distance criteria for analysis
        """
        return self._get_block_element_by_key("Dose Comparison", "Distance")

    @property
    def threshold_param(self):
        """Dose threshold criteria

        Returns
        -------
        str
            Minimum dose threshold for analysis
        """
        return self._get_block_element_by_key("Dose Comparison", "Threshold")

    @property
    def meas_uncertainty(self):
        """Measurement Uncertainty

        Returns
        -------
        str
            Whether or not measurement uncertainty is turned on
        """
        return self._get_block_element_by_key(
            "Dose Comparison", "Meas Uncertainty"
        )

    @property
    def use_global(self):
        """Use Global %

        Returns
        -------
        str
            Whether or not Use Global % is turned on
        """
        return self._get_block_element_by_key("Dose Comparison", "Use Global")

    @property
    def rotation_angle(self):
        """Rotation angle

        Returns
        -------
        str
            Rotation angle applied to data for analysis
        """
        return self._get_block_element_by_key(
            "Dose Comparison", "Rotation Angle"
        )

    @property
    def dose_diff_threshold(self):
        """Dose Diff Threshold

        Returns
        -------
        str
            Dose Difference Threshold for analysis
        """
        return self._get_block_element_by_key("Dose Comparison", "Dose Diff")

    @property
    def use_van_dyk(self):
        """Use VanDyk

        Returns
        -------
        str
            Whether or not Van Dyk criteria is turned on
        """
        return self._get_block_element_by_key("Dose Comparison", "VanDyk")

    ########################################################################
    # Summary Block
    ########################################################################
    @property
    def summary_type(self):
        """Title of the dose comparison table

        Returns
        -------
        str
            Dose comparison type (e.g., Absolute)
        """
        return self.anchors["Summary"]["text"].split("\n")[0].strip()

    @property
    def total_points(self):
        """Total Points

        Returns
        -------
        str
            Total number of points/detectors used for analysis
        """
        return self._get_block_element(self.summary_block, 0)

    @property
    def passed_points(self):
        """Number of points passing analysis

        Returns
        -------
        str
            Number of points/detectors meeting analysis criteria
        """
        return self._get_block_element(self.summary_block, 1)

    @property
    def failed_points(self):
        """Number of points failing analysis

        Returns
        -------
        str
            Number of points/detectors not meeting analysis criteria
        """
        return self._get_block_element(self.summary_block, 2)

    @property
    def pass_rate(self):
        """Passing rate of points

        Returns
        -------
        str
            Percentage of points/detectors meeting analysis criteria
        """
        return self._get_block_element(self.summary_block, 3)

    ########################################################################
    # Notes Block
    ########################################################################
    @property
    def notes(self):
        """Custom note entered by report author

        Returns
        -------
        str
            Text from the Notes block

        """
        anchor = self.anchors["Notes"]
        text = anchor["text"]

        # If Notes gets blended in Dose Values,
        # but actual notes in another block
        data = self.data.get_block_data(
            anchor["page"],
            (anchor["bbox"][0], anchor["bbox"][1]),
            tol=(20, 50),
        )
        if len(data) > 1:
            if "Notes" in data[1]:
                return data[1].split("Notes")[1].strip()
            return data[1].strip()

        # If the notes are at end of Dose Values block
        if "Notes" in text:
            return text.split("Notes")[1].strip()

    @property
    def summary_data(self):
        """A summary of data from the QA report

        Returns
        ----------
        dict
            Keys will match "column" elements Values are of type str
        """

        return {
            "Patient Name": self.patient_name,
            "Patient ID": self.patient_id,
            "QA Date": self.qa_date,
            "Plan Date": self.plan_date,
            "Energy": self.energy,
            "Angle": self.angle,
            "SSD": self.ssd,
            "SDD": self.sdd,
            "Depth": self.depth,
            "Dose Type": self.dose_comparison_type,
            "Difference (%)": self.dose_diff_param,
            "Distance (mm)": self.dist_param,
            "Threshold (%)": self.threshold_param,
            "Rotation Angle": self.rotation_angle,
            "Meas Uncertainty": self.meas_uncertainty,
            "Use Global (%)": self.use_global,
            "Dose Diff Thresh": self.dose_diff_threshold,
            "Use VanDyk": self.use_van_dyk,
            "Summary Type": self.summary_type,
            "Total Points": self.total_points,
            "Pass": self.passed_points,
            "Fail": self.failed_points,
            "Pass (%)": self.pass_rate,
            "Notes": self.notes,
        }
