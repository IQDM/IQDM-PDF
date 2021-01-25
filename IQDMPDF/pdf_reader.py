#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pdf_reader.py
"""Read PDF files into python objects"""
#
# Copyright (c) 2020 Dan Cutright
# This file is part of IQDM-PDF, released under a MIT license.
#    See the file LICENSE included with this distribution
#
# Code adapted from Mark Amery's answer at:
# https://stackoverflow.com/questions/22898145/how-to-extract-text-and-text-coordinates-from-a-pdf-file
# Accessed August 8, 2019


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from io import StringIO
from IQDMPDF.utilities import (
    get_sorted_indices,
    is_in_tol,
    bbox_to_pos,
    is_numeric,
)

# Search tolerance for get_block_data
TOLERANCE = 10


def convert_pdf_to_txt(path):
    """Extract text from a PDF

    Parameters
    ----------
    path : str
        Absolute file path to the PDF to be read

    Returns
    ----------
    str
        The text content of the PDF
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, "rb")
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(
        fp,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=True,
    ):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


class CustomPDFReader:
    """Custom PDF Parsing module"""

    def __init__(self, file_path):
        """Initialize a CustomPDFReader object

        Parameters
        ----------
        file_path : str
            Absolute file path to the PDF to be read
        """
        self.page = []
        self.file_path = file_path
        self.convert_pdf_to_text()
        self.data = []

    def __str__(self):
        """Get str rep for each page of the PDF"""
        return "\n".join([str(page) for page in self.page])

    def __repr__(self):
        """Return the str rep"""
        return self.__str__()

    def get_block_data(
        self,
        page,
        pos,
        tol=TOLERANCE,
        text_cleaner=None,
        numeric=None,
        ignored=None,
        mode="bottom-left",
    ):
        """Use PDFPageParser.get_block_data for the provided page

        Parameters
        ----------
        page : int
            The index of the PDF page
        pos : tuple of int, float
            The (x,y) coordinates of the text block to be retrieved
        tol : int, float, tuple
            Maximum distance a block's x or y-coordinate may be from pos.
            If a tuple is provided, first value is the x_tolerance,
            2nd is y_tolerance
        text_cleaner : callable, optional
            A function called on each text element (e.g., remove leading ':')
        numeric : bool, optional
            If true, only return value if it is numeric. If false, only return
            value if it is not numeric. Leave as None to ignore this feature.
        ignored : list, optional
            Optionally provide a list of strings that should be ignored. If
            the value of the block data is in this list, the value will become
            an empty string instead
        mode : str, optional
            Options are combinations of top/center/bottom and
            right/center/left, e.g., 'top-right', 'center-right'.
            'center' is assumed to be 'center-center'. Default is
            'bottom-left'.

        Returns
        ----------
        list of str
            All text data that meet the input constraints
        """
        return self.page[page].get_block_data(
            pos,
            tol,
            text_cleaner=text_cleaner,
            numeric=numeric,
            ignored=ignored,
            mode=mode,
        )

    def convert_pdf_to_text(self):
        """Extract text and coordinates from a PDF"""

        # Open a PDF file.
        fp = open(self.file_path, "rb")

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        # if not document.is_extractable:
        #     raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # loop over all pages in the document
        for p, page in enumerate(PDFPage.create_pages(document)):
            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()

            # extract text from this object
            keys = ["bbox", "x", "y", "text"]
            page_data = {key: [] for key in keys}
            self.page.append(
                PDFPageParser(layout._objs, page_data, page_index=p)
            )

        device.close()
        fp.close()
        parser.close()

    def get_bbox_of_data(self, text, return_all=False, include_text=False):
        """Get the bounding box for a given string

        Parameters
        ----------
        text : str
            Check all parsed data for this string. Return the first bounding
            box that contains this text. Meant to search for a unique str
        return_all : bool
            If true, then return a list containing all matches, in the order
            pdfminer.six found them
        include_text : bool
            If true, also return the text data

        Returns
        ----------
        dict, list
             "page"->int and "bbox"->[x0, y0, x1, y1]. If include_data is true,
             "text"->str will contain the text data. If return_all is true,
             return a list of these dict objects.

        """
        ans = []
        for p, page in enumerate(self.page):
            for i, stored_text in enumerate(page.data["text"]):
                if text in stored_text:
                    this_ans = {"page": p, "bbox": page.data["bbox"][i]}
                    if include_text:
                        this_ans["text"] = stored_text
                    if not return_all:
                        return this_ans
                    ans.append(this_ans)
        return ans if ans else None


class PDFPageParser:
    """Custom PDF Page Parsing module"""

    def __init__(self, lt_objs, page_data, page_index=0):
        """Initialization of PDFPageParser

        Parameters
        ----------
        lt_objs : list
            A layout object from PDFPageAggregator.get_result()._objs
        page_data : dict
            A dictionary of lists, with keys 'x', 'y', 'text'
        page_index : int, optional
            The index of the page
        """
        self.lt_objs = lt_objs
        self.data = page_data
        self.page_index = page_index

        self.parse_obj(lt_objs)
        self.sort_all_data_by_y()
        self.sub_sort_all_data_by_x()

    def __str__(self):
        """Get the coordinates and text value for all text blocks"""
        ans = []
        for index, text in enumerate(self.data["text"]):
            ans.append(
                "page_index: %s, data_index: %s\nbbox: %s\n%s"
                % (self.page_index, index, self.data["bbox"][index], text)
            )
        return "\n".join(ans)

    def __repr__(self):
        """Return the str rep"""
        return self.__str__()

    def parse_obj(self, lt_objs):
        """Extract x, y, and text data from a layout objects

        Parameters
        ----------
        lt_objs : list
            A layout object from PDFPageAggregator.get_result()._objs
        """
        # loop over the object list
        for obj in lt_objs:
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                bbox = [round(i, 2) for i in obj.bbox]
                self.data["bbox"].append(bbox)
                self.data["x"].append(bbox[0])
                self.data["y"].append(bbox[1])
                self.data["text"].append(obj.get_text())
            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs)

    def sort_all_data_by_y(self):
        """Sort parsed data by y coordinate"""
        self.sort_all_data("y", reverse=True)

    def sub_sort_all_data_by_x(self):
        """Sort each row of data by x-coordinate, keeping y order"""
        for y in set(self.data["y"]):
            indices, x, text = [], [], []
            for i, y_ in enumerate(self.data["y"]):
                if y_ == y:
                    indices.append(i)
                    x.append(self.data["x"][i])
                    text.append(self.data["text"][i])

            for sort_index, data_index in enumerate(get_sorted_indices(x)):
                self.data["x"][indices[sort_index]] = x[data_index]
                self.data["text"][indices[sort_index]] = text[data_index]

    def sort_all_data(self, sort_key, reverse=False):
        """Sort all parsed data by sort_key

        Parameters
        ----------
        sort_key : str
            Either 'x' or 'y'
        reverse : bool
            Passes into standard library sorted() function
        """
        sorted_indices = get_sorted_indices(
            self.data[sort_key], reverse=reverse
        )

        for key in list(self.data):
            self.data[key] = [self.data[key][i] for i in sorted_indices]

    def get_block_data(
        self,
        pos,
        tol,
        text_cleaner=None,
        numeric=None,
        ignored=None,
        mode="bottom-left",
    ):
        """Get the text block data by x,y coordinates

        Parameters
        ----------
        pos : list of int, float
            The (x,y) coordinates of the text block to be retrieved
        tol : int, float, tuple
            Maximum distance a block's x or y-coordinate may be from pos.
            If a tuple is provided, first value is the x_tolerance,
            2nd is y_tolerance
        text_cleaner : callable, optional
            A function called on each text element (e.g., remove leading ':')
        numeric : bool, optional
            If true, only return value if it is numeric. If false, only return
            value if it is not numeric. Leave as None to ignore this feature.
        ignored : list, optional
            Optionally provide a list of strings that should be ignored. If
            the value of the block data is in this list, the value will become
            an empty string instead
        mode : str, optional
            Options are combinations of top/center/bottom and
            right/center/left, e.g., 'top-right', 'center-right'.
            'center' is assumed to be 'center-center'. Default is
            'bottom-left'.

        Returns
        ----------
        list of str
            All text data that meet the input constraints
        """

        tol = tol if isinstance(tol, tuple) else (tol, tol)

        block_data = []
        for i, data in enumerate(self.data["text"]):
            data_pos = bbox_to_pos(self.data["bbox"][i], mode)
            valid_x = is_in_tol(data_pos[0], pos[0], tol[0])
            valid_y = is_in_tol(data_pos[1], pos[1], tol[1])
            if valid_x and valid_y:
                data_clean = (
                    data.strip()
                    if text_cleaner is None
                    else text_cleaner(data)
                )

                if ignored is not None and data_clean in ignored:
                    data_clean = ""

                if data_clean and numeric is not None:
                    data_is_numeric = is_numeric(data_clean)
                    if (numeric and not data_is_numeric) or (
                        not numeric and data_is_numeric
                    ):
                        data_clean = ""

                if data_clean:
                    block_data.append(data_clean)
        return block_data
