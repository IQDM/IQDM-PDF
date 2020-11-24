#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
"""Main program for IMRT QA PDF report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution


import argparse
from datetime import datetime
from os.path import isfile, join, splitext, dirname
from pathlib import Path
from os import walk, listdir
from IQDMPDF._version import __version__
from IQDMPDF.parsers.parser import ReportParser


SCRIPT_DIR = dirname(__file__)


def pdf_to_qa_result(file_path):
    """Process a PDF into CSV data

    Parameters
    ----------
    file_path : str
        Absolute file path to the PDF to be read

    Returns
    ----------
    dict
        report (CSV data), report_type, columns
    """

    report_obj = ReportParser(file_path)
    if report_obj.report is not None:
        return {
            "report": report_obj.csv,
            "report_type": report_obj.report_type,
            "columns": report_obj.columns,
        }


def process_files(
    init_directory,
    ignore_extension=False,
    output_file=None,
    output_dir=None,
    no_recursive_search=False,
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
    """

    time_stamp = str(datetime.now()).replace(":", "-").replace(".", "-")
    if output_file is None:
        output_file = "results_%s.csv" % time_stamp

    if no_recursive_search:
        for file_name in listdir(init_directory):
            if ignore_extension or splitext(file_name)[1].lower() == ".pdf":
                file_path = join(init_directory, file_name)
                process_file(file_path, output_file, output_dir)
    else:
        for dirName, subdirList, fileList in walk(init_directory):
            for file_name in fileList:
                if (
                    ignore_extension
                    or splitext(file_name)[1].lower() == ".pdf"
                ):
                    file_path = join(dirName, file_name)
                    process_file(file_path, output_file, output_dir)


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
    results = pdf_to_qa_result(file_path)  # process file
    if results is not None:
        row = results["report"]
        report_type = results["report_type"]
        columns = results["columns"]
        current_file = "%s_%s" % (
            report_type,
            output_file,
        )  # prepend report type to file name
        if output_dir is not None:
            current_file = join(output_dir, current_file)
        current_file = Path(current_file).resolve()
        if row:
            if not isfile(
                current_file
            ):  # if file doesn't exist, need to write columns
                with open(current_file, "w") as csv:
                    csv.write(",".join(columns) + "\n")
            with open(current_file, "a") as csv:  # write the processed data
                csv.write(row + "\n")
            print("Processed: %s" % file_path)
    else:
        print("Skipping: %s" % file_path)


def create_arg_parser():
    cmd_parser = argparse.ArgumentParser(
        description="Command line interface for IQDM"
    )
    cmd_parser.add_argument(
        "-ie",
        "--ignore-extension",
        dest="ignore_extension",
        help="Script will check all files, not just ones with .pdf extensions",
        default=False,
        action="store_true",
    )
    cmd_parser.add_argument(
        "-od",
        "--output-dir",
        dest="output_dir",
        help="Output stored in local directory by default, specify otherwise here",
        default=None,
    )
    cmd_parser.add_argument(
        "-of",
        "--output-file",
        dest="output_file",
        help="Output will be saved as <report_type>_results_<time-stamp>.csv by default. "
        "Define this tag to customize file name after <report_type>_",
        default=None,
    )
    cmd_parser.add_argument(
        "-ver",
        "--version",
        dest="print_version",
        help="Print the IQDM version",
        default=False,
        action="store_true",
    )
    cmd_parser.add_argument(
        "-nr",
        "--no-recursive-search",
        dest="no_recursive_search",
        help="Include this flag to skip sub-directories",
        default=False,
        action="store_true",
    )
    cmd_parser.add_argument("directory", nargs="?", help="Initiate scan here")
    return cmd_parser


def main(args):
    """Main program to be called from a console"""

    path = args.directory
    if not path or len(path) < 2:
        if args.print_version:
            print("IMRT-QA-Data-Miner: IQDM-PDF v%s" % __version__)
            return
        else:
            print("Initial directory not provided!")
            return

    process_files(
        args.directory,
        ignore_extension=args.ignore_extension,
        output_file=args.output_file,
        output_dir=args.output_dir,
        no_recursive_search=args.no_recursive_search,
    )

    if args.print_version:
        print("IMRT-QA-Data-Miner: IQDM-PDF v%s" % __version__)


if __name__ == "__main__":
    args = create_arg_parser().parse_args()
    main(args)
