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
    """Delta4 IMRT QA report parser"""

    def __init__(self):
        """Initialize Delta4Report class"""
        ParserBase.__init__(self)

        self.report_type = "Delta4"
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
            "DTA Criteria",
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
            "Treatment Summary",
            "Histograms",
            "Parameter Definitions & Acceptance Criteria",
        ]
        self.anchors = {key: self.data.get_bbox_of_data(key) for key in keys}

    @property
    def patient_demo_block(self):
        """Patient name and ID data block

        Returns
        ----------
        list
            A list of str from the patient demographics block
        """
        demo_block = self.data.get_block_data(
            page=0, pos=[536.42, 700.18], mode="top-right"
        )
        if demo_block:
            return demo_block[0].split("\n")
        return ["", ""]  # Redacted report

    @property
    def patient_name(self):
        """Get the patient name

        Returns
        ----------
        str
            Patient name
        """
        return self.patient_demo_block[0]

    @property
    def patient_id(self):
        """Get the patient ID

        Returns
        ----------
        str
            Patient ID
        """
        return self.patient_demo_block[1]

    @property
    def meas_plan_info_block(self):
        """Plan name/date and meas date block

        Returns
        ----------
        list
            A list of str from the plan info block
        """
        return self.data.get_block_data(
            page=0, pos=[147.77, 618.77], mode="top-left"
        )[0].split("\n")

    @property
    def plan_name(self):
        """Get the plan name

        Returns
        ----------
        str
            Plan name from DICOM
        """
        return self.meas_plan_info_block[0]

    def find_nth_date_in_block(self, n):
        """Find the nth date from meas_plan_info_block

        Parameters
        ----------
        n : int
            The index of date lines in meas_plan_info_block

        Returns
        ----------
        str
            The nth date in meas_plan_info_block
        """
        plan_info = self.meas_plan_info_block
        indices = self.find_date_indices(plan_info)
        if n < len(indices):
            index = indices[n]
            if index < len(plan_info):
                return plan_info[index]
        return ""

    @staticmethod
    def find_date_indices(lines):
        """Search through a list of strings for a date time

        Parameters
        ----------
        lines : list
            A list of strings, some of which have date and time

        Returns
        ----------
        list
            A list of indices of lines that contain date times
        """
        indices = []
        for i, line in enumerate(lines):
            if ":" in line:
                if line.count("/") == 2 or line.count(".") == 2:
                    indices.append(i)
            elif line.count("/") == 2 or line.count(".") == 2:
                indices.append(i)
        return indices

    @property
    def plan_date(self):
        """Get the plan date

        Returns
        ----------
        str
            Plan date from DICOM
        """
        return self.find_nth_date_in_block(0)

    @property
    def meas_date(self):
        """Get the measured name

        Returns
        ----------
        str
            Date of QA measurement
        """
        return self.find_nth_date_in_block(1)

    @property
    def accepted_date(self):
        """Get the QA accepted date

        Returns
        ----------
        str
            QA Accepted date from DICOM
        """
        return self.find_nth_date_in_block(2)

    @property
    def radiation_dev(self):
        """Get the radiation device

        Returns
        ----------
        str
            Radiation device per DICOM-RT Plan
        """
        anchor = self.anchors["Treatment Summary"]
        pos = [80.88, anchor["bbox"][1] - 8.57]  # 519.36 - 510.79
        return (
            self.data.get_block_data(page=0, pos=pos, mode="top-left")[0]
            .split("\n")[0]
            .split(": ")[1]
        )

    @property
    def daily_corr_block(self):
        """Get the daily correction block (may contain energy too)

        Returns
        ----------
        list
            A list of str from the energy info block
        """
        anchor = self.anchors["Treatment Summary"]
        pos = [209.68, anchor["bbox"][1] - 83.52]
        block = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-left"
        )
        if not len(block):  # [250.08, 414.35, 482.18, 470.45]
            pos = [250.08, anchor["bbox"][1] - 48.96]
            block = self.data.get_block_data(
                page=anchor["page"], pos=pos, mode="top-left"
            )

        return block[0].split("\n")

    @property
    def energy_block(self):
        """Get the energy block (if energy not in daily corr block)

        Returns
        ----------
        list
            A list of str from the energy info block
        """
        anchor = self.anchors["Treatment Summary"]
        pos = [209.68, anchor["bbox"][1] - 48.89]  # 519.36 - 470.47
        block = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-left"
        )
        if not len(block):  # Energy at end of beam names
            return []

        return block[0].split("\n")

    @property
    def gantry_block(self):
        """Get the gantry block

        Returns
        ----------
        list
            A list of str from the gantry info block
        """
        anchor = self.anchors["Treatment Summary"]
        pos = [141.31, anchor["bbox"][1] - 83.52]  # 519.36 - 435.89
        block = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-left"
        )
        if not len(block):  # Energy at end of beam names
            return []

        return block[0].split("\n")

    @property
    def beam_name_block(self):
        """Get the beam name block

        Returns
        ----------
        list
            A list of str from the beam name info block
        """
        # [80.88, 425.86, 221.6, 458.92]
        anchor = self.anchors["Treatment Summary"]
        pos = [80.88, anchor["bbox"][1] - 72.0]  # 530.93 - 458.92
        block = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-left"
        )

        return block[0].split("\n")

    @property
    def energy(self):
        """Get the energy block (may contain daily corr too)

        Returns
        ----------
        str
            All energies found in report (CSV if multiple)
        """
        lines = self.daily_corr_block
        if (
            lines[0].replace(".", "").strip().isnumeric()
            or "daily corr" in lines[0].lower()
        ):  # no energy
            lines = self.energy_block
            if not lines:
                lines = self.gantry_block
                if not lines:
                    lines = self.beam_name_block
                    lines = [line for line in lines if "°" in line]

        # Energy block is missing Composite/Fraction row
        if "energy" in lines[0].lower() or "daily corr" in lines[0].lower():
            anchor = self.anchors["Treatment Summary"]
            pos = [250.05, anchor["bbox"][1] - 83.52]  # 519.41 - 435.89
            block = self.data.get_block_data(
                page=anchor["page"], pos=pos, mode="top-left"
            )
            if block:
                lines = block[0].split("\n")

        for i in range(len(lines)):
            if "to" in lines[i] and "°" in lines[i]:
                lines[i] = lines[i].split("°")[2].strip()
            if "FFF" in lines[i]:
                lines[i] = lines[i].split("FFF")[0] + "FFF"
        return ", ".join(list(set(lines)))

    @property
    def daily_corr(self):
        """Get the daily correction factor

        Returns
        ----------
        str
            The daily correction factor
        """

        daily_corr = self.process_daily_corr_lines(self.daily_corr_block)
        if daily_corr is not None:
            return daily_corr

        # if the above fails, check the energy_block

        daily_corr = self.process_daily_corr_lines(self.energy_block)
        if daily_corr is not None:
            return daily_corr

        anchor = self.anchors["Treatment Summary"]
        pos = [274.92, anchor["bbox"][1] - 83.45]  # 519.36 - 435.91
        lines = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-right"
        )[0].split("\n")
        return self.process_daily_corr_lines(lines)

    @staticmethod
    def process_daily_corr_lines(lines):
        for line in lines:
            if line.replace(".", "").isnumeric():
                return line
            if str(line[-1]).isdigit():
                return line.split("MV")[1].replace(", FFF", "").strip()

    @property
    def tx_summary_data_block(self):
        """Get the tx summary block

        Returns
        ----------
        list
            A list of str from the Treatment Summary block
        """
        anchor = self.anchors["Treatment Summary"]
        pos = [482.18, anchor["bbox"][1] - 48.96]  # 553.97 - 505.01
        block = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-right"
        )
        if block[1].startswith("Energy"):
            return block

        pos = [274.92, anchor["bbox"][1] - 83.45]  # 519.36 - 435.91
        block = self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-right"
        )
        if not str(block[0]).replace(".", "").replace("\n", "").isnumeric():
            return block

        # the above block is daily correction factors
        # [250.08, 425.69, 482.19, 481.97]
        pos = [482.19, anchor["bbox"][1] - 48.96]  # 530.93 - 481.97
        return self.data.get_block_data(
            page=anchor["page"], pos=pos, mode="top-right"
        )

    @property
    def beam_count(self):
        """Get the number of delivered beams in the report

        Returns
        ----------
        int
            The number of beams
        """
        daily_corr_block = self.daily_corr_block
        daily_corr = self.process_daily_corr_lines(daily_corr_block)
        if daily_corr is not None:
            return len(daily_corr_block)
        energy_block = self.energy_block
        if len(energy_block):
            return len(self.energy_block)
        return len(self.beam_name_block) - 1

    @property
    def composite_tx_summary_data(self):
        """Get the composite analysis data

        Returns
        ----------
        dict
            'norm_dose', 'dev', 'dta', 'gamma_index', and 'dose_dev'
        """
        for block in self.tx_summary_data_block:
            split = block.split("\n")
            for text in split:
                if "%" in text:
                    dose_data = text.split(" ")
                    pass_rate_data = text.split(dose_data[1])[1].split("%")
                    return {
                        "norm_dose": dose_data[0] + " " + dose_data[1],
                        "dev": pass_rate_data[0].strip() + "%",
                        "dta": pass_rate_data[1].strip() + "%",
                        "gamma_index": pass_rate_data[2].strip() + "%",
                        "dose_dev": pass_rate_data[3].strip() + "%",
                    }

    @property
    def threshold(self):
        """Get the minimum dose (%) included in analysis

        Returns
        ----------
        str
            Minimum dose threshold
        """
        anchor = self.anchors["Parameter Definitions & Acceptance Criteria"]
        pos = [169.37, anchor["bbox"][1] - 41.7]  # 152.93 - 111.23
        data = self.data.get_block_data(page=anchor["page"], pos=pos)
        if len(data) == 0:
            pos = [169.42, anchor["bbox"][1] - 53.22]  # 152.93 - 99.71
            data = self.data.get_block_data(page=anchor["page"], pos=pos)
        for item in data[0].split("\n"):
            if "Dose from" in item:
                split = item.strip().split(" ")
                return split[2]

    @property
    def distance_block(self):
        """Distance column of data from acceptance criteria

        Returns
        ----------
        list
            A list of strings for the distance criteria
        """
        anchor = self.anchors["Parameter Definitions & Acceptance Criteria"]
        pos = [347.15, anchor["bbox"][1] - 53.22]  # 152.93 - 99.71
        return self.data.get_block_data(page=anchor["page"], pos=pos)[0].split(
            "\n"
        )

    @property
    def gamma_distance(self):
        """Get the gamma distance criteria

        Returns
        ----------
        str
            Gamma analysis distance criteria
        """
        return self.distance_block[-1]

    @property
    def dta_criteria(self):
        """Get the DTA distance criteria

        Returns
        ----------
        str
            DTA analysis distance criteria
        """
        return self.distance_block[-2]

    @property
    def gamma_dose(self):
        """Get the Gamma Analysis dose criteria

        Returns
        ----------
        str
            Gamma dose criteria
        """
        anchor = self.anchors["Parameter Definitions & Acceptance Criteria"]
        pos = [169.42, anchor["bbox"][1] - 53.22]  # 152.93 - 99.71
        data = self.data.get_block_data(page=anchor["page"], pos=pos)[0]
        if "±" in data and "Dose from" in data:
            return data.split("±")[1]
        pos = [295.42, anchor["bbox"][1] - 8.57]  # 445.92 - 437.35
        return (
            self.data.get_block_data(
                page=anchor["page"], pos=pos, mode="top-left"
            )[0]
            .split("\n")[-1]
            .replace("±", "")
        )

    @property
    def acceptance_limits(self):
        """Get the acceptance limits data block

        Returns
        ----------
        list
            A list of strings for the acceptance limits
        """
        anchor = self.anchors["Parameter Definitions & Acceptance Criteria"]
        pos = [399.0, anchor["bbox"][1] - 53.22]  # 152.93 - 99.71
        return self.data.get_block_data(page=anchor["page"], pos=pos)[0].split(
            "\n"
        )

    @property
    def gamma_pass_criteria(self):
        """Get the gamma analysis pass-rate criteria

        Returns
        -----------
        str
            Gamma pass-rate criteria
        """
        return self.acceptance_limits[-1].split(" ")[0]

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
            "Plan Date": self.plan_date.strip(),
            "Plan Name": self.plan_name,
            "Meas Date": self.meas_date.strip(),
            "Accepted Date": self.accepted_date.strip(),
            "Radiation Dev": self.radiation_dev,
            "Energy": self.energy,
            "Daily Corr": self.daily_corr,
            "Norm Dose": comp_tx_data["norm_dose"],
            "Dev": comp_tx_data["dev"],
            "DTA": comp_tx_data["dta"],
            "DTA Criteria": self.dta_criteria,
            "Dose Dev": comp_tx_data["dose_dev"],
            "Gamma-Index": comp_tx_data["gamma_index"],
            "Gamma Pass Criteria": self.gamma_pass_criteria,
            "Gamma Dose Criteria": self.gamma_dose,
            "Gamma Dist Criteria": self.gamma_distance,
            "Threshold": self.threshold,
            "Beam Count": self.beam_count,
        }
