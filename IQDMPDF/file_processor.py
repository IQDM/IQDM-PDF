#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file_processor.py
"""Process IMRT QA file(s) into CSV file(s)"""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from datetime import datetime
from os.path import isfile, join
import csv
from IQDMPDF.parsers.parser import ReportParser
from IQDMPDF.utilities import get_files, run_multiprocessing
from IQDMPDF._version import __version__


def process_files(
    init_directory,
    ignore_extension=False,
    output_file=None,
    output_dir=None,
    no_recursive_search=False,
    callback=None,
    raise_errors=False,
    processes=1,
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
    raise_errors : bool
        Set to True to allow errors to be raised (useful for debugging)
    processes : int
        Number of parallel processes allowed
    """

    time_stamp = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    if output_file is None:
        output_file = "results_%s.csv" % time_stamp

    extension = None if ignore_extension else ".pdf"
    search_sub_dir = not no_recursive_search
    files = get_files(init_directory, search_sub_dir, extension)

    if processes == 1:
        for i, file in enumerate(files):
            if callback is not None:
                label = "Processing (%s of %s): %s" % (i + 1, len(files), file)
                gauge = float(i) / float(len(files))
                callback({"label": label, "gauge": gauge})
            try:
                process_file(file, output_file, output_dir)
            except Exception as e:
                if raise_errors:
                    raise e
                else:
                    print(str(e))
    else:
        # Multiprocessing
        print("Processing %s file(s) ..." % len(files))
        all_data = run_multiprocessing(process_file_worker, files, processes)

        print("Writing results to file(s) ...")

        # remove failed parsing
        all_data = [row for row in all_data if row["report_type"] is not None]

        report_types = list(set([row["report_type"] for row in all_data]))

        sorted_data = {key: [] for key in report_types}
        columns = {}
        for row in all_data:
            report_type = row["report_type"]
            sorted_data[report_type].append(row["data"])
            if report_type not in columns.keys():
                columns[report_type] = row["columns"]

        for report_type, data in sorted_data.items():
            current_file = "%s_%s" % (report_type, output_file)
            if output_dir is not None:
                current_file = join(output_dir, current_file)

            output = [columns[report_type]]
            output.extend(data)
            write_csv(current_file, output)

            print("%s data written to %s" % (report_type, current_file))


def process_file_worker(file_path):
    """Mutliprocessing worker function

    Parameters
    ----------
    file_path : str
        PDF file to be passed to ReportParser

    Returns
    -------
    dict
        {"data": ReportParser.csv_data, "report_type": ReportParser.report_type,
        "columns": ReportParser.columns}
    """
    data, report_type, columns = None, None, None
    try:
        parser = ReportParser(file_path)
        if parser.report is not None:
            data = parser.csv_data
            report_type = parser.report_type
            columns = parser.columns
    except Exception:
        pass
    return {"data": data, "report_type": report_type, "columns": columns}


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
        row = parser.csv_data
        current_file = "%s_%s" % (
            parser.report_type,
            output_file,
        )  # prepend report type to file name
        if output_dir is not None:
            current_file = join(output_dir, current_file)
        if row:
            # if file doesn't exist, need to write columns
            if not isfile(current_file):
                write_csv(current_file, [parser.columns])
            # write the processed data
            write_csv(current_file, [row], mode="a")
    else:
        print("Skipping: %s" % file_path)


def write_csv(file_path, rows, mode="w", newline=""):
    """Create csv.writer, call writerows(rows)

    Parameters
    ----------
    file_path : str
        path to file
    rows : list, iterable
        Items to be written to file_pointer (input for csv.writer.writerows)
    mode : str
        optional string that specifies the mode in which the file is opened
    newline : str
        controls how universal newlines mode works.
        It can be None, '', '\n', '\r', and '\r\n'
    """
    with open(file_path, mode, encoding="utf-8", newline=newline) as f:
        writer = csv.writer(
            f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerows(rows)


def validate_kwargs(kwargs, add_print_callback=True):
    """Process kwargs from main for process_files

    Parameters
    ----------
    kwargs : dict
        Keyword arguments for main. See main.create_arg_parser for
        valid arguments
    add_print_callback : bool
        If true, add simple print function at the start of each process_file
        call

    Returns
    ----------
    dict
        Returns a dict containing only keywords applicable to process_files, or
        an empty dict if "init_directory" is missing or "print_version" is
        True and "init_directory" is missing
    """
    if not kwargs["init_directory"] or len(kwargs) < 2:
        if kwargs["print_version"]:
            print("IMRT-QA-Data-Miner: IQDM-PDF v%s" % __version__)
        else:
            print("Initial directory not provided!")
        return {}

    if add_print_callback:
        kwargs["callback"] = print_callback

    # command line args are strings
    try:
        kwargs["processes"] = int(float(kwargs["processes"]))
    except Exception:
        kwargs["processes"] = 1

    keys = [
        "init_directory",
        "ignore_extension",
        "output_file",
        "output_dir",
        "no_recursive_search",
        "raise_errors",
        "callback",
        "processes",
    ]
    return {key: kwargs[key] for key in keys if key in list(kwargs)}


def print_callback(msg):
    """Simple print callback for process_files

    Parameters
    ----------
    msg : dict
        The message sent from process_files
    """
    print(msg["label"])
