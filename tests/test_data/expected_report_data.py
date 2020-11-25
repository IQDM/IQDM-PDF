# expected_report_data.py
"""unittest case data for PDF reader."""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also

from IQDMPDF.paths import DIRECTORIES
from os.path import join


class TestDataHelper:
    def __init__(self, vendor):
        """Used to collect data for unit testing

        Parameters
        ----------
        vendor : str
            Collect data for this vendor, assign other vendors to
            other_file_paths
        """
        self.test_data = TEST_DATA
        self.vendor = vendor

    @property
    def file_paths(self):
        """File paths of test data for this vendor

        Returns
        ----------
        dict
            Test data repot paths for this vendor as defined in
            expected_report_data.py
        """

        return {
            key: case_data["path"]
            for key, case_data in self.test_data[self.vendor].items()
        }

    @property
    def other_file_paths(self):
        """Get file paths to all other reports

        Returns
        ----------
        list
            File paths of reports for other vendors
        """
        paths = []
        for vendor in self.test_data.keys():
            if vendor != self.vendor:
                for case_data in self.test_data[vendor].values():
                    paths.append(case_data["path"])
        return paths

    @property
    def expected_data(self):
        """Get the test data for this vendor

        Returns
        ----------
        dict
            Test data for this vendor as defined in expected_report_data.py

        """
        return {
            key: case_data["data"]
            for key, case_data in self.test_data[self.vendor].items()
        }


TEST_DATA = {
    "delta4": {
        "6 MV, FFF": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_1.pdf",
            ),
            "data": {
                "Patient Name": "UCM, TG119",
                "Patient ID": "0097",
                "Plan Name": "1 Prostate-6FFF-TB2",
                "Plan Date": "5/19/2020  4:17 PM",
                "Meas Date": "5/20/2020  4:25 PM",
                "Energy": "6 MV, FFF",
                "Daily Corr": "1.039",
                "Norm Dose": "186 cGy",
                "Dev": "98.8%",
                "DTA": "96.3%",
                "Gamma-Index": "91.0%",
                "Dose Dev": "-0.3%",
                "Radiation Dev": "TrueBeamSN1203",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "2.0%",
                "Gamma Dist Criteria": "2.0 mm",
                "Beam Count": 2,
            },
        },
        "6 MV": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_2.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Name": "1-2 Pelvis",
                "Plan Date": "11/20/2020",
                "Meas Date": "11/20/2020",
                "Energy": "6 MV",
                "Daily Corr": "1.081",
                "Norm Dose": "303 cGy",
                "Dev": "95.4%",
                "DTA": "87.4%",
                "Gamma-Index": "92.1%",
                "Dose Dev": "2.0%",
                "Radiation Dev": "UC_M120",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "3.0%",
                "Gamma Dist Criteria": "2.0 mm",
                "Beam Count": 4,
            },
        },
        "2ndPageTxSummary": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_3.pdf",
            ),
            "data": {
                "Patient Name": "UCM, TG119",
                "Patient ID": "0097",
                "Plan Name": "4 CShape50-D4",
                "Plan Date": "11/20/2019  2:30 PM",
                "Meas Date": "11/21/2019  6:46 PM",
                "Energy": "6 MV",
                "Daily Corr": "1.000",
                "Norm Dose": "261 cGy",
                "Dev": "100.0%",
                "DTA": "99.3%",
                "Gamma-Index": "99.5%",
                "Dose Dev": "0.1%",
                "Radiation Dev": "TrueBeamSN1203",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "2.0%",
                "Gamma Dist Criteria": "2.0 mm",
                "Beam Count": 3,
            },
        },
    },
    "sncpatient": {
        "FirstUChicago": {
            "path": join(
                DIRECTORIES["SNCPATIENT_EXAMPLES"],
                "UChicago",
                "DCAM_example_1.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "WP-001",
                "QA Date": "9/25/2020",
                "Plan Date": "2020-09-25",
                "Energy": "6x",
                "Angle": "",
                "SSD": "100.0",
                "SDD": "",
                "Depth": "",
                "Dose Type": "Absolute",
                "Difference (%)": "2",
                "Distance (mm)": "2",
                "Threshold (%)": "10.0",
                "Meas Uncertainty": "No",
                "Use Global (%)": "Yes",
                "Summary Type": "Gamma",
                "Total Points": "68",
                "Pass": "68",
                "Fail": "0",
                "Pass (%)": "100",
                "Notes": "2% 2mm TB4",
                "Meas File": "...\\5by5 6x.txt",
                "Plan File": "...\\Water_...",
            },
        },
        "FirstNorthwestern": {
            "path": join(
                DIRECTORIES["SNCPATIENT_EXAMPLES"],
                "Northwestern_Memorial",
                "ArcCheck_Example_1.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "QA Date": "2/5/2020",
                "Plan Date": "2/5/2020",
                "Energy": "6X",
                "Angle": "",
                "SSD": "",
                "SDD": "",
                "Depth": "",
                "Dose Type": "Absolute",
                "Difference (%)": "2.0",
                "Distance (mm)": "2.0",
                "Threshold (%)": "20.0",
                "Meas Uncertainty": "No",
                "Use Global (%)": "No",
                "Summary Type": "GC",
                "Total Points": "567",
                "Pass": "512",
                "Fail": "55",
                "Pass (%)": "90.3",
                "Notes": "Notes\nbst1 \npelvis\nSLC",
                "Meas File": "",
                "Plan File": "",
            },
        },
        "MergedDataNorthwestern": {
            "path": join(
                DIRECTORIES["SNCPATIENT_EXAMPLES"],
                "Northwestern_Memorial",
                "ArcCheck_Example_2.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "QA Date": "2/5/2020",
                "Plan Date": "2/5/2020",
                "Energy": "6X",
                "Angle": "",
                "SSD": "",
                "SDD": "",
                "Depth": "",
                "Dose Type": "Absolute",
                "Difference (%)": "2.0",
                "Distance (mm)": "2.0",
                "Threshold (%)": "20.0",
                "Meas Uncertainty": "No",
                "Use Global (%)": "No",
                "Summary Type": "GC",
                "Total Points": "2197",
                "Pass": "1940",
                "Fail": "257",
                "Pass (%)": "88.3",
                "Notes": "Notes\nFields 1-2\nPelvis=Cervix+PM+LNs\nSLF",
                "Meas File": "",
                "Plan File": "",
            },
        },
    },
}
