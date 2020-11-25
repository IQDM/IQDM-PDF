#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# utilities.py
"""Common functions for IQDM-PDF"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution

from os.path import join, splitext
from os import walk, listdir


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


def get_csv_row(data, columns, delimiter=","):
    """Convert a dictionary of data into a row for a csv file

    Parameters
    ----------
    data : dict
        a dictionary with values with str representations
    columns : list
        a list of keys dictating the order of the csv
    delimiter : str
        Optionally use the provided delimiter rather than a comma

    Returns
    ----------
    str
        a csv string delimited by delimiter
    """
    str_data = [str(data[c]) for c in columns]
    clean_str_data = ['"%s"' % s if delimiter in s else s for s in str_data]
    clean_str_data = [s.replace("\n", "<>") for s in clean_str_data]
    return delimiter.join(clean_str_data)


def csv_to_list(csv_str, delimiter=","):
    """Split a CSV into a list

    Parameters
    ----------
    csv_str : str
        A comma-separated value string (with double quotes around values
        containing the delimiter)
    delimiter : str
        The str separator between values

    Returns
    ----------
    list
       csv_str split by the delimiter
    """
    if '"' not in csv_str:
        return csv_str.split(delimiter)

    next_value, csv_str = next_csv_element(csv_str, delimiter)
    ans = [next_value.replace("<>", "\n")]
    while csv_str:
        next_value, csv_str = next_csv_element(csv_str, delimiter)
        ans.append(next_value.replace("<>", "\n"))
    return ans


def next_csv_element(csv_str, delimiter=","):
    """Helper function for csv_to_list

    Parameters
    ----------
    csv_str : str
        A comma-separated value string (with double quotes around values
        containing the delimiter)
    delimiter : str
        The str separator between values

    Returns
    ----------
    str, str
        Return a tuple, the next value and remainder of csv_str
    """
    if csv_str.startswith('"'):
        split = csv_str[1:].find('"') + 1
        return csv_str[1:split], csv_str[split + 1 :]

    next_delimiter = csv_str.find(delimiter)
    if next_delimiter == -1:
        return csv_str, ""
    return csv_str[:next_delimiter], csv_str[next_delimiter + 1 :]


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
