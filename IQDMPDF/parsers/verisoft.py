#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# verisoft.py
"""PTW VeriSoft report parser"""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.parsers.generic import ParserBase
from IQDMPDF.pdf_reader import CustomPDFReader


class VeriSoftReport(ParserBase):
    """PTW VeriSoft IMRT QA report parser"""

    def __init__(self):
        """Initialize VeriSoftReport class"""
        ParserBase.__init__(self)

        self.report_type = "VeriSoft"
        self.columns = [
            "Patient Name",
            "Patient ID",
            "Institution",
            "Physicist",
            "Comment",
            "Date",
            "Version",
            "Data Set A",
            "Data Set B",
            "Calibrate Air Density",
            "Gamma Dist.",
            "Gamma Dose",
            "Gamma Dose Info",
            "Threshold",
            "Threshold Info",
            "Gamma (Min)",
            "Gamma (Mean)",
            "Gamma (Median)",
            "Gamma (Max)",
            "Gamma Min Position X",
            "Gamma Min Position Y",
            "Gamma Max Position X",
            "Gamma Max Position Y",
            "Abs Dose (Min)",
            "Abs Dose (Mean)",
            "Abs Dose (Median)",
            "Abs Dose (Max)",
            "Abs Dose Min Position X",
            "Abs Dose Min Position Y",
            "Abs Dose Max Position X",
            "Abs Dose Max Position Y",
            "Number of Dose Points",
            "Evaluated Dose Points",
            "Evaluated Dose Points (%)",
            "Passed Points",
            "Passed Points (%)",
            "Failed Points",
            "Failed Points (%)",
            "Pass Rate",
            "Pass Result Color",
            "Passing Criteria",
            "Passing Green",
            "Passing Yellow",
            "Passing Red",
        ]
        self.identifiers = [
            "PTW",
            "VeriSoft",
            "Administrative Data",
            "Data Set A",
            "Data Set B",
            "Settings",
            "Institution",
            "Physicist",
        ]

    def __call__(self, report_file_path):
        """Process an IMRT QA report PDF

        Parameters
        ----------
        report_file_path : str
            File path pointing to an IMRT QA report
        """
        super().__call__(report_file_path)
        self.data = CustomPDFReader(report_file_path)

        keys = [
            "Administrative Data",
            "Data Set A",
            "Set Zero",
            "Calibrate Air Density",
            "Gamma 2D",
            "Statistics",
            "Settings",
            "Date: ",
            "PTW",
            "Absolute Difference",
        ]
        self.anchors = {
            key: self.data.get_bbox_of_data(
                key, return_all=True, include_text=True
            )
            for key in keys
        }

        for key in keys:
            if key != "Gamma 2D" and self.anchors[key] is not None:
                self.anchors[key] = self.anchors[key][0]

        # Split the two blocks containing "Gamma 2D" (possibly)
        gamma_results_index = None
        for i, gamma_block in enumerate(self.anchors["Gamma 2D"]):
            if "Gamma 2D - Parameters" in gamma_block["text"]:
                self.anchors["Gamma 2D - Parameters"] = gamma_block
            elif "Gamma 2D" in gamma_block["text"]:
                gamma_results_index = i

        key = "Gamma 2D"
        self.anchors[key] = (
            self.anchors[key][gamma_results_index]
            if gamma_results_index is not None
            else None
        )

        self.admin_block = self._get_lateral_block("Administrative Data", 20)
        self.data_set_block = self.anchors["Data Set A"]["text"].split("\n")
        self.stats_block = self._get_lateral_block("Statistics")
        self.settings_block = self._get_lateral_block("Settings")
        self.gamma_results_block = self._get_lateral_block("Gamma 2D")
        self.abs_diff_block = self._get_lateral_block("Absolute Difference")

        self.gamma_param_block = self.anchors["Gamma 2D - Parameters"][
            "text"
        ].split("\n")

        self._set_manipulations_data()

    ########################################################################
    # Utilities
    ########################################################################
    def _get_lateral_block(self, anchor_key, y_tol=10):
        """Search for data laterally from an anchor / header block

        Parameters
        ----------
        anchor_key : str
            Key to VeriSoftReport.anchors
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
                tol=(1000, y_tol),
            )

            for el in data:
                if anchor_key not in el:
                    return el.split("\n")

    @staticmethod
    def _get_block_element(block, index):
        return block[index] if block is not None else "N/A"

    def _get_diff_position(self, key, index):
        x, y = ["N/A", ""], ["N/A", ""]
        anchor = self.anchors[key]
        if anchor is not None:
            text_block = anchor["text"].split("\n")
            split = text_block[index].split("(")[1].replace(")", "").split(";")
            x = split[0].split('=')[1].strip().split(' ')
            y = split[1].split('=')[1].strip().split(' ')
        return {"x": x[0]+x[1], "y": y[0]+y[1]}

    def _set_manipulations_data(self):
        key = "Calibrate Air Density"
        data = self.data.get_block_data(
            self.anchors[key]["page"],
            (self.anchors[key]["bbox"][0], self.anchors[key]["bbox"][1]),
            tol=(1000, 10),
        )
        parameters, values = [], []
        for block in data:
            if "Parameters" in block:
                parameters = block.strip().split('\n')[1:]
            elif "Value" in block:
                values = block.strip().split('\n')[1:]

        if parameters and values:
            data = {param: values[i].strip() for i, param in enumerate(parameters)}
            self.manipulations_data = data
        else:
            self.manipulations_data = None

    ########################################################################
    # Admin Block
    ########################################################################
    @property
    def institution(self):
        return self.admin_block[0].strip()

    @property
    def physicist(self):
        return self.admin_block[1].strip()

    @property
    def patient_id(self):
        return self.admin_block[2].strip()

    @property
    def patient_name(self):
        return self.admin_block[-2].strip()

    @property
    def comment(self):
        return self.admin_block[-1].strip()

    ########################################################################
    # Dataset Block
    ########################################################################
    @property
    def data_set_b_index(self):
        for i, line in enumerate(self.data_set_block):
            if "Data Set B" in line:
                return i

    @property
    def data_set_a(self):
        i = self.data_set_b_index
        if i is not None:
            return ''.join(self.data_set_block[1:i]).strip()

    @property
    def data_set_b(self):
        i = self.data_set_b_index
        if i is not None:
            return '\n'.join(self.data_set_block[i:]).strip()

    ########################################################################
    # Manipulations Block
    ########################################################################
    @property
    def calibrate_air_density(self):
        if self.manipulations_data is not None:
            if 'kUser' in self.manipulations_data.keys():
                return self.manipulations_data['kUser']
        return ''

    ########################################################################
    # Gamma Param Block
    ########################################################################
    @property
    def gamma_dist(self):
        return "".join(self.gamma_param_block[1].strip().split(" ")[0:2])

    @property
    def gamma_dose(self):
        return "".join(self.gamma_param_block[2].strip().split(" ")[0:2])

    @property
    def gamma_dose_info(self):
        return " ".join(self.gamma_param_block[2].strip().split(" ")[2:])

    @property
    def threshold(self):
        return "".join(self.gamma_param_block[4].strip().split(" ")[3:5])

    @property
    def threshold_info(self):
        return " ".join(self.gamma_param_block[4].strip().split(" ")[5:])

    ########################################################################
    # Gamma Results Block
    ########################################################################
    @property
    def gamma_diff(self):
        return {
            key: self._get_block_element(self.gamma_results_block, i)
            for i, key in enumerate(["mean", "min", "max", "median"])
        }

    @property
    def gamma_min_pos(self):
        return self._get_diff_position("Gamma 2D", 2)

    @property
    def gamma_max_pos(self):
        return self._get_diff_position("Gamma 2D", 3)

    ########################################################################
    # Absolute Dose Diff Block
    ########################################################################
    @property
    def abs_diff(self):
        return {
            key: self._get_block_element(self.abs_diff_block, i)
            for i, key in enumerate(["mean", "min", "max", "median"])
        }

    @property
    def abs_diff_min_pos(self):
        return self._get_diff_position("Absolute Difference", 2)

    @property
    def abs_diff_max_pos(self):
        return self._get_diff_position("Absolute Difference", 3)

    ########################################################################
    # Statistics Block
    ########################################################################
    @property
    def num_dose_points(self):
        return self.stats_block[0]

    @property
    def eval_dose_points(self):
        return self.stats_block[1].split(" ")[0]

    @property
    def eval_dose_points_percent(self):
        return self.stats_block[1].split("(")[1].strip().split(" ")[0] + "%"

    @property
    def passed_points(self):
        return self.stats_block[2]

    @property
    def passed_points_percent(self):
        return self.stats_block[2].split("(")[1].strip().split(" ")[0] + "%"

    @property
    def failed_points(self):
        return self.stats_block[3]

    @property
    def failed_points_percent(self):
        return self.stats_block[3].split("(")[1].strip().split(" ")[0] + "%"

    @property
    def pass_rate(self):
        return self.stats_block[4].split(" ")[0]

    @property
    def pass_result_color(self):
        return self.stats_block[4].split("(")[1].split(")")[0]

    ########################################################################
    # Settings Block
    ########################################################################
    @property
    def passing_criteria(self):
        return self.settings_block[0].strip()

    @property
    def passing_green(self):
        return self.settings_block[1].split(" ")[0] + "%"

    @property
    def passing_yellow(self):
        return self.settings_block[2].split(" ")[0] + "%"

    @property
    def passing_red(self):
        return self.settings_block[3].split(" ")[0] + "%"

    ########################################################################
    # Footer Info
    ########################################################################
    @property
    def date(self):
        return self.anchors["Date: "]["text"].replace("Date: ", "").strip()

    @property
    def version(self):
        return self.anchors["PTW"]["text"].split(" - ")[1].strip()

    @property
    def summary_data(self):
        """A summary of data from the QA report

        Returns
        ----------
        dict
            Keys will match "column" elements Values are of type str
        """
        gamma_diff = self.gamma_diff
        gamma_min_pos = self.gamma_min_pos
        gamma_max_pos = self.gamma_max_pos

        abs_diff = self.abs_diff
        abs_min_pos = self.abs_diff_min_pos
        abs_max_pos = self.abs_diff_max_pos

        return {
            "Patient Name": self.patient_name,
            "Patient ID": self.patient_id,
            "Institution": self.institution,
            "Physicist": self.physicist,
            "Comment": self.comment,
            "Date": self.date,
            "Version": self.version,
            "Data Set A": self.data_set_a,
            "Data Set B": self.data_set_b,
            "Calibrate Air Density": self.calibrate_air_density,
            "Gamma Dist.": self.gamma_dist,
            "Gamma Dose": self.gamma_dose,
            "Gamma Dose Info": self.gamma_dose_info,
            "Threshold": self.threshold,
            "Threshold Info": self.threshold_info,
            "Gamma (Min)": gamma_diff["min"],
            "Gamma (Mean)": gamma_diff["mean"],
            "Gamma (Median)": gamma_diff["median"],
            "Gamma (Max)": gamma_diff["max"],
            "Gamma Min Position X": gamma_min_pos["x"],
            "Gamma Min Position Y": gamma_min_pos["y"],
            "Gamma Max Position X": gamma_max_pos["x"],
            "Gamma Max Position Y": gamma_max_pos["y"],
            "Abs Dose (Min)": abs_diff["min"],
            "Abs Dose (Mean)": abs_diff["mean"],
            "Abs Dose (Median)": abs_diff["median"],
            "Abs Dose (Max)": abs_diff["max"],
            "Abs Dose Min Position X": abs_min_pos["x"],
            "Abs Dose Min Position Y": abs_min_pos["y"],
            "Abs Dose Max Position X": abs_max_pos["x"],
            "Abs Dose Max Position Y": abs_max_pos["y"],
            "Number of Dose Points": self.num_dose_points,
            "Evaluated Dose Points": self.eval_dose_points,
            "Evaluated Dose Points (%)": self.eval_dose_points_percent,
            "Passed Points": self.passed_points,
            "Passed Points (%)": self.passed_points_percent,
            "Failed Points": self.failed_points,
            "Failed Points (%)": self.failed_points_percent,
            "Pass Rate": self.pass_rate,
            "Pass Result Color": self.pass_result_color,
            "Passing Criteria": self.passing_criteria,
            "Passing Green": self.passing_green,
            "Passing Yellow": self.passing_yellow,
            "Passing Red": self.passing_red,
        }
