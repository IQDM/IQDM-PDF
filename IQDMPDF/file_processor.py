#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file_processor.py
"""Process IMRT QA file(s) into CSV file(s)"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from IQDMPDF.parsers.parser import ReportParser
from IQDMPDF.utilities import get_files
from datetime import datetime
from os.path import isfile, join


def process_files(
    init_directory,
    ignore_extension=False,
    output_file=None,
    output_dir=None,
    no_recursive_search=False,
    callback=None,
):
    """Process all pdf files into parser classes, write data to csv

    Parameters
    ----------
    init_directory : str
        initial scanning directory
    ignore_extension : bool, optional
        Set to True to catch pdf files that are missing .pdf extension
    output_file : str, optional
       Report type in file name will be prepended to this value
    output_dir : str, optional
        Save results to this directory, default is local directory
    no_recursive_search : bool, optional
        Ignore sub-directories it True
    callback : callable
        Pointer to a function to be called before each process_file call. The
        parameter will be dict with keys of "label" and "gauge".
    """

    time_stamp = str(datetime.now()).replace(":", "-").replace(".", "-")
    if output_file is None:
        output_file = "results_%s.csv" % time_stamp

    extension = None if ignore_extension else ".pdf"
    search_sub_dir = not no_recursive_search
    files = get_files(init_directory, search_sub_dir, extension)

    for i, file in enumerate(files):
        if callback is not None:
            label = "Processing (%s of %s): %s" % (i + 1, len(files), file)
            gauge = float(i) / float(len(files))
            callback({"label": label, "gauge": gauge})
        process_file(file, output_file, output_dir)


def process_file(file_path, output_file, output_dir=None):
    """Process a pdf file into a parser class, write data to csv

    Parameters
    ----------
    file_path : str
        PDF file to processed
    output_file : str
       Report type in file name will be prepended to this value
    output_dir : str, optional
        Save results to this directory, default is local directory
    """
    parser = ReportParser(file_path)
    if parser.report is not None:
        row = parser.csv
        current_file = "%s_%s" % (
            parser.report_type,
            output_file,
        )  # prepend report type to file name
        if output_dir is not None:
            current_file = join(output_dir, current_file)
        if row:
            if not isfile(
                current_file
            ):  # if file doesn't exist, need to write columns
                with open(current_file, "w") as csv:
                    csv.write(",".join(parser.columns) + "\n")
            with open(current_file, "a") as csv:  # write the processed data
                csv.write(row + "\n")
    else:
        print("Skipping: %s" % file_path)
