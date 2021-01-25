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
                "Accepted Date": "",
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
                "Accepted Date": "11/20/2020",
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
                "Accepted Date": "",
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
        "Dates with . and energy/daily_corr swap": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_4.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Date": "05.09.2019  2:26 PM",
                "Plan Name": "1-2 RUL",
                "Meas Date": "05.09.2019  7:05 PM",
                "Accepted Date": "05.09.2019  7:15 PM",
                "Radiation Dev": "TrueBeam1",
                "Energy": "6 MV, FFF",
                "Daily Corr": "1.010",
                "Norm Dose": "1151 cGy",
                "Dev": "94.7%",
                "DTA": "99.6%",
                "DTA Criteria": "n.a.",
                "Dose Dev": "-1.0%",
                "Gamma-Index": "99.5%",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "3.0%",
                "Gamma Dist Criteria": "3.0 mm",
                "Threshold": "10%",
                "Beam Count": 3,
            },
        },
        "Energy in beam name": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_5.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Date": "1/19/2018  2:20 PM",
                "Plan Name": "D4 QA 1-1",
                "Meas Date": "1/19/2018  4:42 PM",
                "Accepted Date": "1/19/2018  4:44 PM",
                "Radiation Dev": "UC_M120",
                "Energy": "6 MV",
                "Daily Corr": "1.016",
                "Norm Dose": "248 cGy",
                "Dev": "99.1%",
                "DTA": "99.0%",
                "DTA Criteria": "n.a.",
                "Dose Dev": "-0.3%",
                "Gamma-Index": "99.3%",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "3.0%",
                "Gamma Dist Criteria": "3.0 mm",
                "Threshold": "10%",
                "Beam Count": 2,
            },
        },
        "TxSummary block returns daily corr": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_6.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Date": "6/13/2016  8:13 PM",
                "Plan Name": "1-2",
                "Meas Date": "6/14/2016  5:57 PM",
                "Accepted Date": "6/14/2016  6:33 PM",
                "Radiation Dev": "UCTB_92",
                "Energy": "6 MV",
                "Daily Corr": "1.016",
                "Norm Dose": "235 cGy",
                "Dev": "87.2%",
                "DTA": "99.6%",
                "DTA Criteria": "n.a.",
                "Dose Dev": "-1.4%",
                "Gamma-Index": "95.5%",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "3.0%",
                "Gamma Dist Criteria": "3.0 mm",
                "Threshold": "10%",
                "Beam Count": 2,
            },
        },
        "Date index search": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_7.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Date": "12/28/2015  4:59 PM",
                "Plan Name": "D4QA",
                "Meas Date": "12/29/2015  6:50 PM",
                "Accepted Date": "12/29/2015  6:52 PM",
                "Radiation Dev": "UCTB_92",
                "Energy": "6 MV",
                "Daily Corr": "1.033",
                "Norm Dose": "958 cGy",
                "Dev": "98.0%",
                "DTA": "100.0%",
                "DTA Criteria": "n.a.",
                "Dose Dev": "-0.4%",
                "Gamma-Index": "100.0%",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "2.0%",
                "Gamma Dist Criteria": "2.0 mm",
                "Threshold": "10%",
                "Beam Count": 1,
            },
        },
        "No Composite/Fraction in Energy Block": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_8.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Date": "8/28/2019  10:04 AM",
                "Plan Name": "1-2 HN 75Gy",
                "Meas Date": "8/28/2019  5:48 PM",
                "Radiation Dev": "UC_M120",
                "Energy": "6 MV",
                "Daily Corr": "1.033",
                "Norm Dose": "146 cGy",
                "Dev": "91.0%",
                "DTA": "97.0%",
                "DTA Criteria": "n.a.",
                "Dose Dev": "0.0%",
                "Gamma-Index": "98.3%",
                "Gamma Pass Criteria": "95%",
                "Gamma Dose Criteria": "3.0%",
                "Gamma Dist Criteria": "3.0 mm",
                "Threshold": "10%",
                "Beam Count": 2,
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
    "sncpatient2020": {
        "NorthwesternArcCheck1": {
            "path": join(
                DIRECTORIES["SNCPATIENT2020_EXAMPLES"],
                "Northwestern_Memorial",
                "ArcCheck_Example_1.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "QA Date": "26 Nov 2020 12:01:19",
                "Plan Date": "19 Mar 2019 11:16:38",
                "Plan Name": "qa1",
                "Plan ID": "",
                "Verified Plan UID": "",
                "Total MU": "700.3",
                "Comparison Type": "Absolute Dose Comparison (GC/Gamma using 3D Mode)",
                "Threshold (%)": "20.0",
                "Use Global (%)": "No",
                "Difference (%)": "2.0",
                "Meas Uncertainty": "No",
                "Distance (mm)": "2",
                "Summary Type": "Summary (GC Analysis)",
                "Pass (%)": "90.3",
                "Pass": "512",
                "Fail": "55",
                "Total Points": "567",
                "Notes": "Bst1",
            },
        },
        "NorthwesternArcCheck2": {
            "path": join(
                DIRECTORIES["SNCPATIENT2020_EXAMPLES"],
                "Northwestern_Memorial",
                "ArcCheck_Example_2.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "QA Date": "26 Nov 2020 12:21:27",
                "Plan Date": "04 Apr 2019 16:31:58",
                "Plan Name": "qa2",
                "Plan ID": "",
                "Verified Plan UID": "",
                "Total MU": "675.5",
                "Comparison Type": "Absolute Dose Comparison (GC/Gamma using 3D Mode)",
                "Threshold (%)": "20.0",
                "Use Global (%)": "No",
                "Difference (%)": "2.0",
                "Meas Uncertainty": "No",
                "Distance (mm)": "2",
                "Summary Type": "Summary (GC Analysis)",
                "Pass (%)": "91.3",
                "Pass": "454",
                "Fail": "43",
                "Total Points": "497",
                "Notes": "bst2",
            },
        },
        "NorthwesternArcCheck3": {
            "path": join(
                DIRECTORIES["SNCPATIENT2020_EXAMPLES"],
                "Northwestern_Memorial",
                "ArcCheck_Example_3.pdf",
            ),
            "data": {
                "Patient Name": "H M",
                "Patient ID": "00000000003",
                "QA Date": "12 Jan 2021 09:36:50",
                "Plan Date": "12 Jan 2021 06:59:10",
                "Plan Name": "Pelvis 3-6",
                "Plan ID": "",
                "Verified Plan UID": "",
                "Total MU": "2196.4",
                "Comparison Type": "Absolute Dose Comparison (GC/Gamma using 3D Mode)",
                "Threshold (%)": "20.0",
                "Use Global (%)": "No",
                "Difference (%)": "2.0",
                "Meas Uncertainty": "No",
                "Distance (mm)": "2.0",
                "Summary Type": "Summary (GC Analysis)",
                "Pass (%)": "91.8",
                "Pass": "1024",
                "Fail": "91",
                "Total Points": "1115",
                "Notes": "6X SLF",
            },
        },
    },
    "verisoft": {
        "ABMC1": {
            "path": join(
                DIRECTORIES["VERISOFT_EXAMPLES"],
                "AmitaHealth",
                "ANON0001.pdf",
            ),
            "data": {
                "Patient Name": "ANON0001 F, H 600",
                "Patient ID": "ANON0001 F, H 600",
                "Institution": "ABMC",
                "Physicist": "ME",
                "Comment": "cGy/fx @ 100% IDL",
                "Date": "2021-01-11 11:47:33",
                "Version": "VeriSoft 6.2",
                "Data Set A": "M:\\Eclipse Physics - Cancer Institute\\ABMC\\External Beam\\Point Dose QA\\RapidArc QA\\2021\\F, H\\Composite.dcm",
                "Data Set B": "Data Set B\nAdded Data Sets:\nA.mcc\nB.mcc",
                "Calibrate Air Density": "1.032",
                "Gamma Dist.": "3.0mm",
                "Gamma Dose": "3.0%",
                "Gamma Dose Info": "Dose difference with ref. to max. dose of calculated volume",
                "Threshold": "5.0%",
                "Threshold Info": "of max. dose of calculated volume",
                "Gamma (Min)": "0.001",
                "Gamma (Mean)": "0.175",
                "Gamma (Median)": "0.167",
                "Gamma (Max)": "0.734",
                "Gamma Min Position X": "100.0mm",
                "Gamma Min Position Y": "20.0mm",
                "Gamma Max Position X": "0.0mm",
                "Gamma Max Position Y": "10.0mm",
                "Abs Dose (Min)": "0.015 cGy",
                "Abs Dose (Mean)": "3.854 cGy",
                "Abs Dose (Median)": "2.316 cGy",
                "Abs Dose (Max)": "60.338 cGy",
                "Abs Dose Min Position X": "100.0mm",
                "Abs Dose Min Position Y": "20.0mm",
                "Abs Dose Max Position X": "130.0mm",
                "Abs Dose Max Position Y": "0.0mm",
                "Number of Dose Points": "1,405",
                "Evaluated Dose Points": "340",
                "Evaluated Dose Points (%)": "24.2%",
                "Passed Points": "340",
                "Passed Points (%)": "100.0%",
                "Failed Points": "0",
                "Failed Points (%)": "0.0%",
                "Pass Rate": "100.0",
                "Pass Result Color": "Green",
                "Passing Criteria": "Gamma ≤ 1.0",
                "Passing Green": "93.0%",
                "Passing Yellow": "90.0%",
                "Passing Red": "0.0%",
            },
        },
        "ABMC2": {
            "path": join(
                DIRECTORIES["VERISOFT_EXAMPLES"],
                "AmitaHealth",
                "ANON0002.pdf",
            ),
            "data": {
                "Patient Name": "D, M",
                "Patient ID": "ANON0002",
                "Institution": "ABMC",
                "Physicist": "JP",
                "Comment": "200 cGy/fx @ 100% IDL",
                "Date": "2021-01-15 12:56:44",
                "Version": "VeriSoft 6.2",
                "Data Set A": "M:\\Eclipse Physics - Cancer Institute\\ABMC\\External Beam\\Point Dose QA\\RapidArc QA\\2021\\D, M\\Composite.dcm",
                "Data Set B": "Data Set B\nAdded Data Sets:\nA.mcc\nB.mcc",
                "Calibrate Air Density": "1.040",
                "Gamma Dist.": "3.0mm",
                "Gamma Dose": "3.0%",
                "Gamma Dose Info": "Dose difference with ref. to max. dose of selected slice",
                "Threshold": "5.0%",
                "Threshold Info": "of max. dose of selected slice",
                "Gamma (Min)": "N/A",
                "Gamma (Mean)": "N/A",
                "Gamma (Median)": "N/A",
                "Gamma (Max)": "N/A",
                "Gamma Min Position X": "N/A",
                "Gamma Min Position Y": "N/A",
                "Gamma Max Position X": "N/A",
                "Gamma Max Position Y": "N/A",
                "Abs Dose (Min)": "N/A",
                "Abs Dose (Mean)": "N/A",
                "Abs Dose (Median)": "N/A",
                "Abs Dose (Max)": "N/A",
                "Abs Dose Min Position X": "N/A",
                "Abs Dose Min Position Y": "N/A",
                "Abs Dose Max Position X": "N/A",
                "Abs Dose Max Position Y": "N/A",
                "Number of Dose Points": "1,405",
                "Evaluated Dose Points": "891",
                "Evaluated Dose Points (%)": "63.4%",
                "Passed Points": "891",
                "Passed Points (%)": "100.0%",
                "Failed Points": "0",
                "Failed Points (%)": "0.0%",
                "Pass Rate": "100.0",
                "Pass Result Color": "Green",
                "Passing Criteria": "Gamma ≤ 1.0",
                "Passing Green": "93.0%",
                "Passing Yellow": "90.0%",
                "Passing Red": "0.0%",
            },
        },
        "ABMC3": {
            "path": join(
                DIRECTORIES["VERISOFT_EXAMPLES"],
                "AmitaHealth",
                "ANON0003.pdf",
            ),
            "data": {
                "Patient Name": "C, R",
                "Patient ID": "ANON0003",
                "Institution": "ABMC",
                "Physicist": "ME",
                "Comment": "250 cGy/fx @ 100% IDL",
                "Date": "2021-01-18 09:43:32",
                "Version": "VeriSoft 6.2",
                "Data Set A": "M:\\Eclipse Physics - Cancer Institute\\ABMC\\External Beam\\Point Dose QA\\RapidArc QA\\2021\\C, R\\Composite.dcm",
                "Data Set B": "Data Set B\nAdded Data Sets:\nA.mcc\nB.mcc",
                "Calibrate Air Density": "1.039",
                "Gamma Dist.": "3.0mm",
                "Gamma Dose": "3.0%",
                "Gamma Dose Info": "Dose difference with ref. to max. dose of calculated volume",
                "Threshold": "5.0%",
                "Threshold Info": "of max. dose of calculated volume",
                "Gamma (Min)": "0.000",
                "Gamma (Mean)": "0.192",
                "Gamma (Median)": "0.171",
                "Gamma (Max)": "0.933",
                "Gamma Min Position X": "90.0mm",
                "Gamma Min Position Y": "30.0mm",
                "Gamma Max Position X": "-10.0mm",
                "Gamma Max Position Y": "20.0mm",
                "Abs Dose (Min)": "0.001 cGy",
                "Abs Dose (Mean)": "2.789 cGy",
                "Abs Dose (Median)": "1.456 cGy",
                "Abs Dose (Max)": "72.278 cGy",
                "Abs Dose Min Position X": "90.0mm",
                "Abs Dose Min Position Y": "30.0mm",
                "Abs Dose Max Position X": "130.0mm",
                "Abs Dose Max Position Y": "20.0mm",
                "Number of Dose Points": "1,405",
                "Evaluated Dose Points": "668",
                "Evaluated Dose Points (%)": "47.5%",
                "Passed Points": "668",
                "Passed Points (%)": "100.0%",
                "Failed Points": "0",
                "Failed Points (%)": "0.0%",
                "Pass Rate": "100.0",
                "Pass Result Color": "Green",
                "Passing Criteria": "Gamma ≤ 1.0",
                "Passing Green": "93.0%",
                "Passing Yellow": "90.0%",
                "Passing Red": "0.0%",
            },
        },
    },
}
