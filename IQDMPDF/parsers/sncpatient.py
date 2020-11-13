# -*- coding: utf-8 -*-
"""
SNC Patient Report class
Created on Fri Jun 21 2019
@author: Dan Cutright, PhD
@contributor: Marc J.P. Chamberland, PhD
"""

from IQDMPDF.utilities import get_csv
from IQDMPDF.pdf_to_text_data import CustomPDFParser
import re


class SNCPatientReport2020:
    def __init__(self):
        self.report_type = 'sncpatient2020'
        self.columns = ['Patient Name', 'Patient ID', 'QA Date', 'Plan Date',
                        'Plan Name', 'Plan ID', 'Verified Plan UID', 'Total MU',
                        'Comparison Type',  'Threshold (%)', 'Difference (%)',
                        'Distance (mm)', 'Use Global (%)', 'Meas Uncertainty',
                        'Cavity Dose', 'Summary Type', 'Pass (%)', 'Pass', 'Fail', 'Total Points']
        self.identifiers = ['SNC Patient QA of Dose Distribution', 'Hospital', 'QA Date',
                            'QA Parameters', 'Summary', 'Plan ID', 'Verified Plan UID']
        self.text = None
        self.data = None

        self.LUT = {'Patient Name': {'page': 0, 'x': 135.72, 'y': 649.46},
                    'Patient ID': {'page': 0, 'x': 135.72, 'y': 627.35},
                    'QA Date': {'page': 0, 'x': 101.23, 'y': 708.23},
                    'Plan Date': {'page': 0, 'x': 135.72, 'y': 560.18},
                    'Plan Name': {'page': 0, 'x': 135.72, 'y': 605.25},
                    'Plan ID': {'page': 0, 'x': 135.72, 'y': 582.28},
                    'Verified Plan UID': {'page': 0, 'x': 135.72, 'y': 537.57},
                    'Total MU': {'page': 0, 'x': 135.72, 'y': 514.53},
                    'Comparison Type': {'page': 0, 'x': 28.44, 'y': 483.01},
                    'Threshold (%)': {'page': 0, 'x': 152.14, 'y': 463.12},
                    'Use Global (%)': {'page': 0, 'x': 450.58, 'y': 463.12},
                    'Difference (%)': {'page': 0, 'x': 154.94, 'y': 441.02},
                    'Meas Uncertainty': {'page': 0, 'x': 452.74, 'y': 441.02},
                    'Distance (mm)': {'page': 0, 'x': 154.94, 'y': 418.91},
                    'Cavity Dose': {'page': 0, 'x': 450.79, 'y': 418.91},
                    'Summary Type': {'page': 0, 'x': 28.44, 'y': 386.32},
                    'Pass (%)': {'page': 0, 'x': 152.14, 'y': 367.22},
                    'Pass': {'page': 0, 'x': 153.5, 'y': 345.11},
                    'Fail': {'page': 0, 'x': 156.31, 'y': 323.01},
                    'Total Points': {'page': 0, 'x': 153.5, 'y': 300.91}}

    def process_data(self, file_path):
        self.data = CustomPDFParser(file_path)

    @property
    def summary_data(self):
        return {c: self.data.get_block_data(**self.LUT[c]) for c in self.columns}

    @property
    def csv(self):
        return get_csv(self.summary_data, self.columns)


class SNCPatientReport:
    def __init__(self):
        self.report_type = 'sncpatient'
        self.columns = ['Patient Last Name', 'Patient First Name', 'Patient ID', 'Plan Date', 'Energy', 'Angle', 'Dose Type', 'Difference (%)', 'Distance (mm)',
                        'Threshold (%)', 'Meas Uncertainty', 'Analysis Type', 'Total Points', 'Passed', 'Failed',
                        '% Passed', 'Min', 'Max', 'Average', 'Std Dev', 'X offset (mm)', 'Y offset (mm)', 'Notes']
        self.identifiers = ['QA File Parameter', 'Threshold', 'Notes', 'Reviewed By :', 'SSD', 'Depth', 'Energy']
        self.text = None
        self.data = {}

    def process_data(self, text_data):
        self.text = text_data.split('\n')
        self.data['date'], self.data['hospital'] = [], []
        for row in self.text:
            if row.find('Date: ') > -1:
                self.data['date'] = row.strip('Date: ')
            if row.find('Hospital Name: ') > -1:
                self.data['hospital'] = row.split('Hospital Name: ', 1)[-1]

            if self.data['date'] and self.data['hospital']:
                break

        self.data['qa_file_parameter'] = self.get_group_results('QA File Parameter')

        x_offset = '0'
        y_offset = '0'
        try:
            plan_index = self.text.index('Plan')
            if self.text[plan_index + 2].find('CAX') > -1:
                x_offset, y_offset = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?',
                                                self.text[plan_index + 2])
        except ValueError:
            pass

        self.data['cax_offset'] = {'X offset': str(x_offset), 'Y offset': str(y_offset)}

        # Dose Comparison Block
        try:
            self.text.index('Absolute Dose Comparison')
            self.data['dose_comparison_type'] = 'Absolute Dose Comparison'
        except ValueError:
            self.data['dose_comparison_type'] = 'Relative Comparison'
        self.data['dose_comparison'] = self.get_group_results(self.data['dose_comparison_type'])
        if '% Diff' in list(self.data['dose_comparison']):  # Alternate for Difference (%) for some versions of report?
            self.data['dose_comparison']['Difference (%)'] = self.data['dose_comparison']['% Diff']
        if 'Threshold' in list(self.data['dose_comparison']):  # Alternate for Threshold (%) for some versions of report?
            self.data['dose_comparison']['Threshold (%)'] = self.data['dose_comparison']['Threshold']

        # Summary Analysis Block
        try:
            self.text.index('Summary (Gamma Analysis)')
            self.data['analysis_type'] = 'Gamma'
        except ValueError:
            try:
                self.data['analysis_type'] = 'DTA'
            except ValueError:
                self.data['analysis_type'] = 'GC'  # Gradient Correction

        self.data['summary'] = self.get_group_results('Summary (%s Analysis)' % self.data['analysis_type'])

        # Gamma Index Summary Block
        try:
            self.text.index('Gamma Index Summary')
            self.data['gamma_stats'] = self.get_gamma_statistics('Gamma Index Summary')
        except ValueError:
            self.data['gamma_stats'] = {'Minimum': 'n/a', 'Maximum': 'n/a', 'Average': 'n/a',  'Stdv': 'n/a'}

        self.data['notes'] = self.text[self.text.index('Notes') + 1]

    def get_gamma_statistics(self, stats_delimiter):
        gamma_stats = {}
        stats_fields = ['Minimum', 'Maximum', 'Average', 'Stdv']

        group_start = self.text.index(stats_delimiter)

        for field in stats_fields:
            field_start = self.text[group_start:-1].index(field) + 1
            gamma_stats[field] = self.text[group_start:-1][field_start]

        return gamma_stats

    def get_group_results(self, data_group):
        """
        SNC Patient reports contain three blocks of results. data_group may be among the following:
            'QA File Parameter'
            'Absolute Dose Comparison' or 'Relative Comparison'
            'Gamma' or 'DTA'
        """
        group_start = self.text.index(data_group)
        var_name_start = group_start + 1
        data_start = self.text[var_name_start:-1].index('') + 1 + var_name_start
        data_count = data_start - var_name_start

        # If patient name is too long, sometimes the pdf parsing gets off-set
        if self.text[data_start] == 'Set1':
            data_start += 1

        group_results = {}
        for i in range(data_count):
            if self.text[var_name_start+i]:
                group_results[self.text[var_name_start+i]] = self.text[data_start+i].replace(' : ', '')

        return group_results

    @property
    def summary_data(self):
        """
        Collect the parsed data into a dictionary with keys corresponding to columns
        :return: parsed data
        :rtype: dict
        """
        patient_name = self.data['qa_file_parameter']['Patient Name'].replace('^', ' ').split(', ')
        if len(patient_name) > 1:
            last_name = patient_name[0].title()
            first_name = patient_name[1].title()
        elif len(patient_name) == 1:
            last_name = patient_name[0].title()
            first_name = 'n/a'
        else:
            last_name = 'n/a'
            first_name = 'n/a'

        return {'Patient Last Name': last_name,
                'Patient First Name': first_name,
                'Patient ID': self.data['qa_file_parameter']['Patient ID'],
                'Plan Date': self.data['qa_file_parameter']['Plan Date'],
                'Energy': self.data['qa_file_parameter']['Energy'],
                'Angle': self.data['qa_file_parameter']['Angle'],
                'Dose Type': self.data['dose_comparison_type'],
                'Difference (%)': self.data['dose_comparison']['Difference (%)'],
                'Distance (mm)': self.data['dose_comparison']['Distance (mm)'],
                'Threshold (%)': self.data['dose_comparison']['Threshold (%)'],
                'Meas Uncertainty': self.data['dose_comparison']['Meas Uncertainty'],
                'Analysis Type': self.data['analysis_type'],
                'Total Points': self.data['summary']['Total Points'],
                'Passed': self.data['summary']['Passed'],
                'Failed': self.data['summary']['Failed'],
                '% Passed': self.data['summary']['% Passed'],
                'Min': self.data['gamma_stats']['Minimum'],
                'Max': self.data['gamma_stats']['Maximum'],
                'Average': self.data['gamma_stats']['Average'],
                'Std Dev': self.data['gamma_stats']['Stdv'],
                'X offset (mm)': self.data['cax_offset']['X offset'],
                'Y offset (mm)':self.data['cax_offset']['Y offset'],
                'Notes': self.data['notes']}

    @property
    def csv(self):
        return get_csv(self.summary_data, self.columns)
