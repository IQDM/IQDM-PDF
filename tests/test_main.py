#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_main.py
"""unittest cases for main."""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution, also


import unittest
from IQDMPDF import main
from IQDMPDF.paths import DIRECTORIES
from os import unlink
from os.path import join


class TestMain(unittest.TestCase):
    """Unit tests for Utilities."""

    def setUp(self):
        """Setup files and base data for utility testing."""
        pass

    def test_create_arg_parser(self):
        """Test arg parser creation"""
        arg_parser = main.create_arg_parser().parse_args([])
        expected_args = [
            "ignore_extension",
            "output_dir",
            "output_file",
            "print_version",
            "no_recursive_search",
            "init_directory",
        ]
        for arg in expected_args:
            self.assertTrue(arg in arg_parser.__dict__.keys())

    def test_main(self):
        """Test remainder of main.main"""
        directory = join(DIRECTORIES["SNCPATIENT_EXAMPLES"], "UChicago")

        # test main with no args
        main.main()

        # Test print version, using arg parser
        args = main.create_arg_parser().parse_args(["-v"])
        main.main(**vars(args))

        # test main with multiple args
        args = main.create_arg_parser().parse_args(
            [directory, "--version", "-of", "test"]
        )
        main.main(**vars(args))

        unlink("SNCPatient_test")


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
