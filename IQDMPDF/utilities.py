#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# utilities.py
"""Common functions for IQDM-PDF"""
#
# Copyright (c) 2021 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from os.path import join, splitext, normpath, getctime
from os import walk, listdir, sep, stat
import platform
import argparse
from multiprocessing import Pool
from tqdm import tqdm


def are_all_strings_in_text(text, list_of_strings):
    """Check that all strings in list_of_strings exist in text

    Parameters
    ----------
    text : str
        output from IQDMPDF.pdf_reader.convert_pdf_to_text
    list_of_strings : list of str
        a list of strings used to identify document type

    Returns
    ----------
    bool
        Returns true if every string in list_of_strings is found in text data
    """
    for str_to_find in list_of_strings:
        if str_to_find not in text:
            return False
    return True


def get_sorted_indices(some_list, reverse=False):
    """Get sorted indices of some_list

    Parameters
    ----------
    some_list : list
        Any list compatible with sorted()
    reverse : bool
        Reverse sort if True
    """
    return [
        i[0]
        for i in sorted(
            enumerate(some_list), key=lambda x: x[1], reverse=reverse
        )
    ]


def is_in_tol(value, expected_value, tolerance):
    """Is the provided value within expected_value +/- tolerance

    Parameters
    ----------
    value : int, float
        Value of interest
    expected_value : int, float
        Expected value
    tolerance : int, float
        Allowed deviation from expected_value

    Returns
    ----------
    bool
        True if value is within within expected_value +/- tolerance, exclusive
    """
    return expected_value + tolerance > value > expected_value - tolerance


def bbox_to_pos(bbox, mode):
    """Convert a bounding box to an x-y position

    Parameters
    ----------
    bbox : list
        Bounding box from pdf_reader layout object, which is a list of
        four floats [x0, y0, x1, y1]
    mode : str
        Options are combinations of top/center/bottom and right/center/left,
        e.g., 'top-right', 'center-left'. 'center' is assumed to be
        'center-center'
    """

    mode = "center-center" if mode == "center" else mode

    mode = {dim: mode.split("-")[i] for i, dim in enumerate(["y", "x"])}
    pos = {
        "x": {
            "left": bbox[0],
            "right": bbox[2],
            "center": (bbox[0] + bbox[2]) / 2.0,
        },
        "y": {
            "bottom": bbox[1],
            "top": bbox[3],
            "center": (bbox[1] + bbox[3]) / 2.0,
        },
    }

    return [pos[dim][mode[dim]] for dim in ["x", "y"]]


def get_files(init_dir, search_sub_dir=True, extension=None):
    """Collect paths of all files in a director

    Parameters
    ----------
    init_dir : str
        Initial directory to begin scanning
    search_sub_dir : bool
        Recursively search through sub-directories if True
    extension : str, optional
        Collect file paths with only this extension (e.g., '.pdf')

    Returns
    ----------
    list
        List of file paths
    """
    files = []
    if not search_sub_dir:
        append_files(files, init_dir, listdir(init_dir), extension)
    else:
        for dir_name, _, file_list in walk(init_dir):
            append_files(files, dir_name, file_list, extension)
    return files


def append_files(files, dir_name, files_to_append, extension=None):
    """Helper function for get_files

    Parameters
    ----------
    files : list
        Accumulate file paths into this list
    dir_name : str
        The base path of the files in file_list
    files_to_append : list
        A list of file paths to loop accumulate
    extension : str, optional
        Collect file paths with only this extension (e.g., '.pdf')
    """
    for file_name in files_to_append:
        if extension is None or splitext(file_name)[1].lower() == extension:
            files.append(join(dir_name, file_name))


def get_relative_path(path, relative_base):
    """Return a partial path with the specified base

    Parameters
    ----------
    path : str
        A path with relative_base as a sub-component
    relative_base : str
        A directory within path

    Returns
    ----------
    str
        The path with all components prior to relative_base removed
    """
    path = normpath(path)
    relative_base = normpath(relative_base)
    path_split = path.split(sep)
    if relative_base in path_split:
        index = path_split.index(relative_base)
        return join(*path_split[index:])


def create_arg_parser():
    """Create an argument parser

    Returns
    ----------
    argparse.ArgumentParser
        Argument parsers for command-line use of IQDM-PDF
    """
    cmd_parser = argparse.ArgumentParser(
        description="Command line interface for IQDM-PDF"
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
    cmd_parser.add_argument(
        "init_directory", nargs="?", help="Initiate scan here"
    )
    cmd_parser.add_argument(
        "-re",
        "--raise-errors",
        dest="raise_errors",
        help="Allow failed file parsing to halt the program",
        default=False,
        action="store_true",
    )
    cmd_parser.add_argument(
        "-n",
        "--processes",
        dest="processes",
        help="Enable multiprocessing, set number of parallel processes",
        default=1,
    )
    return cmd_parser


def run_multiprocessing(worker, queue, processes, callback=None):
    """Parallel processing

    Parameters
    ----------
    worker : callable
        single parameter function to be called on each item in queue
    queue : iterable
        A list of arguments for worker
    processes : int
        Number of processes for multiprocessing.Pool
    callback : callable
        Optional call back function on progress update, accepts str rep of
        tqdm object. Final call sent with 'complete'

    Returns
    -------
    list
        List of returns from worker

    """
    progress_kwargs = {
        "total": len(queue),
        "bar_format": "{desc:<5.5}{percentage:3.0f}%|{bar:30}{r_bar}",
    }
    data = []
    with Pool(processes=processes) as pool:
        with tqdm(**progress_kwargs) as pbar:
            for item in pool.imap_unordered(worker, queue):
                data.append(item)
                pbar.update()
                if callback is not None:
                    callback(str(pbar))
    if callback is not None:
        callback("complete")
    return data


def is_numeric(val):
    """Check if value is numeric (float or int)

    Parameters
    ----------
    val : any
        Any value

    Returns
    -------
    bool
        Returns true if float(val) doesn't raise a ValueError
    """
    try:
        float(val)
        return True
    except ValueError:
        return False


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.

    Parameters
    ----------
    path_to_file : str
        Path to any file

    Returns
    -------
    float
        Time stamp of file

    """
    if platform.system() == 'Windows':
        return getctime(path_to_file)
    else:
        stat_ = stat(path_to_file)
        return getattr(stat_, 'st_birthtime', stat_.st_mtime)