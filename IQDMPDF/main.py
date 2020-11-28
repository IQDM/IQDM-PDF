#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
"""Main program for IMRT QA PDF report parser"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution


from IQDMPDF.utilities import create_arg_parser
from IQDMPDF.file_processor import process_files, validate_kwargs


def main():
    """Call process_files with validated kwargs"""

    parser = create_arg_parser()
    args = parser.parse_args()
    validated_kwargs = validate_kwargs(vars(args))
    if validated_kwargs:
        process_files(**validated_kwargs)


if __name__ == "__main__":
    main()
