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
from os.path import dirname
from IQDMPDF._version import __version__
from IQDMPDF.file_processor import process_files


SCRIPT_DIR = dirname(__file__)


def create_arg_parser():
    """Create an argument parser

    Returns
    ----------
    argparse.ArgumentParser
        Argument parsers for command-line use of IQDM-PDF
    """
    cmd_parser = argparse.ArgumentParser(description="Command line interface for IQDM")
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
    cmd_parser.add_argument("init_directory", nargs="?", help="Initiate scan here")
    return cmd_parser


def validate_kwargs(kwargs):
    """Process kwargs for file_processor.process_files

    Parameters
    ----------
    kwargs : dict
        Keyword arguments for main. See main.create_arg_parser for
        valid arguments

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

    keys = [
        "init_directory",
        "ignore_extension",
        "output_file",
        "output_dir",
        "no_recursive_search",
        "callback=None",
    ]
    return {key: kwargs[key] for key in keys if key in list(kwargs)}


def main(**kwargs):
    """Main program to be called from a console"""

    validated_kwargs = validate_kwargs(kwargs)
    if validated_kwargs:
        process_files(**validated_kwargs)


if __name__ == "__main__":
    params = vars(create_arg_parser().parse_args())
    main(**params)
