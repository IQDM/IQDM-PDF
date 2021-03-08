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
                "Plan Date": "09/05/2019  2:26 PM",
                "Plan Name": "1-2 RUL",
                "Meas Date": "09/05/2019  7:05 PM",
                "Accepted Date": "09/05/2019  7:15 PM",
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
        "AM/PM in date, month/day swapped": {
            "path": join(
                DIRECTORIES["DELTA4_EXAMPLES"],
                "UChicago",
                "DCAM_example_9.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "Plan Date": "11/22/2017  11:01 AM",
                "Plan Name": "D4QA 1-1",
                "Meas Date": "11/22/2017  3:57 PM",
                "Radiation Dev": "UC_M120",
                "Energy": "6 MV",
                "Daily Corr": "1.053",
                "Norm Dose": "261 cGy",
                "Dev": "99.6%",
                "DTA": "99.6%",
                "DTA Criteria": "n.a.",
                "Dose Dev": "0.6%",
                "Gamma-Index": "99.6%",
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
                "Rotation Angle": "N/A",
                "Meas Uncertainty": "No",
                "Use Global (%)": "Yes",
                "Dose Diff Thresh": "N/A",
                "Use VanDyk": "N/A",
                "Summary Type": "Summary (Gamma Analysis)",
                "Total Points": "68",
                "Pass": "68",
                "Fail": "0",
                "Pass (%)": "100",
                "Notes": "2% 2mm TB4",
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
                "Rotation Angle": "N/A",
                "Meas Uncertainty": "No",
                "Use Global (%)": "No",
                "Dose Diff Thresh": "N/A",
                "Use VanDyk": "N/A",
                "Summary Type": "Summary (GC Analysis)",
                "Total Points": "567",
                "Pass": "512",
                "Fail": "55",
                "Pass (%)": "90.3",
                "Notes": "bst1 \npelvis\nSLC",
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
                "Rotation Angle": "N/A",
                "Meas Uncertainty": "No",
                "Use Global (%)": "No",
                "Dose Diff Thresh": "N/A",
                "Use VanDyk": "N/A",
                "Summary Type": "Summary (GC Analysis)",
                "Total Points": "2197",
                "Pass": "1940",
                "Fail": "257",
                "Pass (%)": "88.3",
                "Notes": "Fields 1-2\nPelvis=Cervix+PM+LNs\nSLF",
            },
        },
        "UVermontHealth1": {
            "path": join(
                DIRECTORIES["SNCPATIENT_EXAMPLES"],
                "UVermontHealthNetwork",
                "ArcCheck_Example_1.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "QA Date": "7/9/2018",
                "Plan Date": "7/9/2018",
                "Energy": "10 MV",
                "Angle": "",
                "SSD": "",
                "SDD": "N/A",
                "Depth": "",
                "Dose Type": "Absolute",
                "Difference (%)": "2",
                "Distance (mm)": "3.0",
                "Threshold (%)": "10.0",
                "Rotation Angle": "0.0 Degs",
                "Meas Uncertainty": "Yes",
                "Use Global (%)": "N/A",
                "Dose Diff Thresh": "0.0 cGy",
                "Use VanDyk": "Yes",
                "Summary Type": "Summary (Gamma Analysis)",
                "Total Points": "1386",
                "Pass": "1323",
                "Fail": "63",
                "Pass (%)": "95.5",
                "Notes": "19E",
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
        "UChicagoExample1": {
            "path": join(
                DIRECTORIES["SNCPATIENT2020_EXAMPLES"],
                "UChicago",
                "DCAM_example_1.pdf",
            ),
            "data": {
                "Patient Name": "",
                "Patient ID": "",
                "QA Date": "",
                "Plan Date": "",
                "Plan Name": "",
                "Plan ID": "",
                "Verified Plan UID": "",
                "Total MU": "3352.99",
                "Comparison Type": "Absolute Dose Comparison (DTA/Gamma using 2D Mode)",
                "Threshold (%)": "10",
                "Use Global (%)": "Yes",
                "Difference (%)": "3",
                "Meas Uncertainty": "No",
                "Distance (mm)": "2.0",
                "Summary Type": "Summary (Gamma Analysis)",
                "Pass (%)": "92.3",
                "Pass": "717",
                "Fail": "60",
                "Total Points": "777",
                "Notes": "2-1 Composite",
            },
        },
    },
    "verisoft": {
        "ABMC1": {
            "path": join(
                DIRECTORIES["VERISOFT_EXAMPLES"],
                "AMITA_Health",
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
                "Set Zero X": "0.8",
                "Set Zero X Units": "mm",
                "Set Zero Y": "0.8",
                "Set Zero Y Units": "mm",
                "Gamma Dist.": "3.0mm",
                "Gamma Dose": "3.0%",
                "Gamma Dose Info": "Dose difference with ref. to max. dose of calculated volume",
                "Threshold": "5.0%",
                "Threshold Info": "of max. dose of calculated volume",
                "Gamma (Min)": "0.001",
                "Gamma (Mean)": "0.175",
                "Gamma (Median)": "0.167",
                "Gamma (Max)": "0.734",
                "Gamma Min Position X": "100.0",
                "Gamma Min Position Y": "20.0",
                "Gamma Max Position X": "0.0",
                "Gamma Max Position Y": "10.0",
                "Gamma Min Position X Units": "mm",
                "Gamma Min Position Y Units": "mm",
                "Gamma Max Position X Units": "mm",
                "Gamma Max Position Y Units": "mm",
                "Abs Dose (Min)": "0.015",
                "Abs Dose (Mean)": "3.854",
                "Abs Dose (Median)": "2.316",
                "Abs Dose (Max)": "60.338",
                "Abs Dose (Min Units)": "cGy",
                "Abs Dose (Mean Units)": "cGy",
                "Abs Dose (Median Units)": "cGy",
                "Abs Dose (Max Units)": "cGy",
                "Abs Dose Min Position X": "100.0",
                "Abs Dose Min Position Y": "20.0",
                "Abs Dose Max Position X": "130.0",
                "Abs Dose Max Position Y": "0.0",
                "Abs Dose Min Position X Units": "mm",
                "Abs Dose Min Position Y Units": "mm",
                "Abs Dose Max Position X Units": "mm",
                "Abs Dose Max Position Y Units": "mm",
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
                "AMITA_Health",
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
                "Set Zero X": "N/A",
                "Set Zero X Units": "N/A",
                "Set Zero Y": "N/A",
                "Set Zero Y Units": "N/A",
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
                "Gamma Min Position X Units": "N/A",
                "Gamma Min Position Y Units": "N/A",
                "Gamma Max Position X Units": "N/A",
                "Gamma Max Position Y Units": "N/A",
                "Abs Dose (Min)": "N/A",
                "Abs Dose (Mean)": "N/A",
                "Abs Dose (Median)": "N/A",
                "Abs Dose (Max)": "N/A",
                "Abs Dose (Min Units)": "N/A",
                "Abs Dose (Mean Units)": "N/A",
                "Abs Dose (Median Units)": "N/A",
                "Abs Dose (Max Units)": "N/A",
                "Abs Dose Min Position X": "N/A",
                "Abs Dose Min Position Y": "N/A",
                "Abs Dose Max Position X": "N/A",
                "Abs Dose Max Position Y": "N/A",
                "Abs Dose Min Position X Units": "N/A",
                "Abs Dose Min Position Y Units": "N/A",
                "Abs Dose Max Position X Units": "N/A",
                "Abs Dose Max Position Y Units": "N/A",
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
                "AMITA_Health",
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
                "Set Zero X": "0.3",
                "Set Zero X Units": "mm",
                "Set Zero Y": "1.1",
                "Set Zero Y Units": "mm",
                "Gamma Dist.": "3.0mm",
                "Gamma Dose": "3.0%",
                "Gamma Dose Info": "Dose difference with ref. to max. dose of calculated volume",
                "Threshold": "5.0%",
                "Threshold Info": "of max. dose of calculated volume",
                "Gamma (Min)": "0.000",
                "Gamma (Mean)": "0.192",
                "Gamma (Median)": "0.171",
                "Gamma (Max)": "0.933",
                "Gamma Min Position X": "90.0",
                "Gamma Min Position Y": "30.0",
                "Gamma Max Position X": "-10.0",
                "Gamma Max Position Y": "20.0",
                "Gamma Min Position X Units": "mm",
                "Gamma Min Position Y Units": "mm",
                "Gamma Max Position X Units": "mm",
                "Gamma Max Position Y Units": "mm",
                "Abs Dose (Min)": "0.001",
                "Abs Dose (Mean)": "2.789",
                "Abs Dose (Median)": "1.456",
                "Abs Dose (Max)": "72.278",
                "Abs Dose (Min Units)": "cGy",
                "Abs Dose (Mean Units)": "cGy",
                "Abs Dose (Median Units)": "cGy",
                "Abs Dose (Max Units)": "cGy",
                "Abs Dose Min Position X": "90.0",
                "Abs Dose Min Position Y": "30.0",
                "Abs Dose Max Position X": "130.0",
                "Abs Dose Max Position Y": "20.0",
                "Abs Dose Min Position X Units": "mm",
                "Abs Dose Min Position Y Units": "mm",
                "Abs Dose Max Position X Units": "mm",
                "Abs Dose Max Position Y Units": "mm",
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
        "ACI_NoAirCalibration": {
            "path": join(
                DIRECTORIES["VERISOFT_EXAMPLES"],
                "AMITA_Health",
                "ANON0004.pdf",
            ),
            "data": {
                "Patient Name": "N/A",
                "Patient ID": "N/A",
                "Institution": "N/A",
                "Physicist": "N/A",
                "Comment": "N/A",
                "Date": "2021-01-25 12:30:46",
                "Version": "VeriSoft 6.2",
                "Data Set A": "J:\\RadOnc-HIN\\Physics\\IMRT QA\\2021 IMRT QA\\Grid Test\\QA1\\PA-753 mu solid P.dcm",
                "Data Set B": "Data Set B\nJ:\\RadOnc-HIN\\Physics\\IMRT QA\\2021 IMRT QA\\Grid Test\\QA1\\PA.xcc",
                "Calibrate Air Density": "",
                "Set Zero X": "-0.6",
                "Set Zero X Units": "mm",
                "Set Zero Y": "-0.2",
                "Set Zero Y Units": "mm",
                "Gamma Dist.": "3.0mm",
                "Gamma Dose": "3.0%",
                "Gamma Dose Info": "Dose difference with ref. to max. dose of selected slice",
                "Threshold": "10.0%",
                "Threshold Info": "of max. dose of selected slice",
                "Gamma (Min)": "0.008",
                "Gamma (Mean)": "0.421",
                "Gamma (Median)": "0.382",
                "Gamma (Max)": "1.157",
                "Gamma Min Position X": "-15.0",
                "Gamma Min Position X Units": "mm",
                "Gamma Min Position Y": "-35.0",
                "Gamma Min Position Y Units": "mm",
                "Gamma Max Position X": "-10.0",
                "Gamma Max Position X Units": "mm",
                "Gamma Max Position Y": "-30.0",
                "Gamma Max Position Y Units": "mm",
                "Abs Dose (Min)": "0.114",
                "Abs Dose (Min Units)": "cGy",
                "Abs Dose (Mean)": "30.493",
                "Abs Dose (Mean Units)": "cGy",
                "Abs Dose (Median)": "29.017",
                "Abs Dose (Median Units)": "cGy",
                "Abs Dose (Max)": "71.911",
                "Abs Dose (Max Units)": "cGy",
                "Abs Dose Min Position X": "-15.0",
                "Abs Dose Min Position X Units": "mm",
                "Abs Dose Min Position Y": "-35.0",
                "Abs Dose Min Position Y Units": "mm",
                "Abs Dose Max Position X": "20.0",
                "Abs Dose Max Position X Units": "mm",
                "Abs Dose Max Position Y": "20.0",
                "Abs Dose Max Position Y Units": "mm",
                "Number of Dose Points": "1,405",
                "Evaluated Dose Points": "520",
                "Evaluated Dose Points (%)": "37.0%",
                "Passed Points": "519",
                "Passed Points (%)": "99.8%",
                "Failed Points": "1",
                "Failed Points (%)": "0.2%",
                "Pass Rate": "99.8",
                "Pass Result Color": "Green",
                "Passing Criteria": "Gamma ≤ 1.0",
                "Passing Green": "95.0%",
                "Passing Yellow": "93.0%",
                "Passing Red": "0.0%",
            },
        },
    },
}
