#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# utilities.py
"""Common functions for IQDM-PDF"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution


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
    return delimiter.join(clean_str_data)


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
