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
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from io import StringIO
from IQDMPDF.utilities import get_sorted_indices, is_in_tol

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

    def __init__(self, file_path, verbose=False):
        """Initialize a CustomPDFReader object

        Parameters
        ----------
        file_path : str
            Absolute file path to the PDF to be read
        verbose : bool
            Print each line of the PDF as it is parsed
        """
        self.page = []
        self.file_path = file_path
        self.convert_pdf_to_text(verbose=verbose)
        self.data = []

    def print(self):
        """Print each page of the PDF to the console"""
        for p, page in enumerate(self.page):
            print("Page %s" % (p + 1))
            page.print()

    def print_block(self, page, index):
        """Print a specific block using PDFPageParser.print_block

        Parameters
        ----------
        page : int
            The index of the PDF page
        index : int
            The index of the text block
        """
        self.page[page].print_block(index)

    def get_block_data_by_index(self, page, index):
        """Get the text block data

        Parameters
        ----------
        page : int
            The index of the PDF page
        index : int
            The index of the text block

        Returns
        ----------
        float, float, str
            A tuple of x, y, text
        """
        return self.page[page].get_block_data_by_index(index)

    def get_block_data(self, page, pos, tol=TOLERANCE, text_cleaner=None):
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

        Returns
        ----------
        list of str
            All text data that meet the input constraints
        """
        return self.page[page].get_block_data(
            pos, tol, text_cleaner=text_cleaner
        )

    def convert_pdf_to_text(self, verbose=False):
        """ "Extract text and coordinates from a PDF

        Parameters
        ----------
        verbose : bool
            Print each line of the PDF as it is parsed
        """

        # Open a PDF file.
        fp = open(self.file_path, "rb")

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

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
            page_data = {"x": [], "y": [], "text": []}
            self.page.append(
                PDFPageParser(layout._objs, page_data, verbose=verbose)
            )


class PDFPageParser:
    """Custom PDF Page Parsing module"""

    def __init__(self, lt_objs, page_data, verbose=False):
        """Initialization of PDFPageParser

        Parameters
        ----------
        lt_objs : list
            A layout object from PDFPageAggregator.get_result()._objs
        page_data : dict
            A dictionary of lists, with keys 'x', 'y', 'text'
        verbose : bool
            Print each line of the PDF as it is parsed
        """
        self.lt_objs = lt_objs
        self.data = page_data
        self.verbose = verbose

        self.parse_obj(lt_objs)
        self.sort_all_data_by_y()
        self.sub_sort_all_data_by_x()

    def parse_obj(self, lt_objs):
        """Extract x, y, and text data from a layout objects

        Parameters
        ----------
        lt_objs : list
            A layout object from PDFPageAggregator.get_result()._objs
        """
        # loop over the object list
        for obj in lt_objs:
            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                if self.verbose:
                    print(
                        "%6d, %6d, %s"
                        % (
                            obj.bbox[0],
                            obj.bbox[1],
                            obj.get_text().replace("\n", "_"),
                        )
                    )
                self.data["x"].append(round(obj.bbox[0], 2))
                self.data["y"].append(round(obj.bbox[1], 2))
                # self.data['text'].append(obj.get_text().replace('\n', '_'))
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

    def get_coordinates(self, index):
        """Get the x and y coordinates by text block index

        Parameters
        ----------
        index : int
            The index of the text block

        Returns
        ----------
        list
            [x-coordinate, y-coordinate]
        """
        return [self.data[key][index] for key in ["x", "y"]]

    def print(self):
        """Print the coordinates and text value for all text blocks"""
        for index, text in enumerate(self.data["text"]):
            coord = self.get_coordinates(index)
            print("x:%s\ty:%s\n%s" % (coord[0], coord[1], text))

    def print_block(self, index):
        """Print the coordinates and text value for the given index

        Parameters
        ----------
        index : int
            The index of the text block
        """
        coord = self.get_coordinates(index)
        print(
            "x:%s\ty:%s\n%s" % (coord[0], coord[1], (self.data["text"][index]))
        )

    def get_block_data_by_index(self, index):
        """Get the text block data by index

        Parameters
        ----------
        index : int
            The index of the text block

        Returns
        ----------
        float, float, str
            A tuple of x, y, text
        """
        coord = self.get_coordinates(index)
        return coord[0], coord[1], self.data["text"][index]

    def get_block_data(self, pos, tol, text_cleaner=None):
        """Get the text block data by x,y coordinates

        Parameters
        ----------
        pos : tuple of int, float
            The (x,y) coordinates of the text block to be retrieved
        tol : int, float, tuple
            Maximum distance a block's x or y-coordinate may be from pos.
            If a tuple is provided, first value is the x_tolerance,
            2nd is y_tolerance
        text_cleaner : callable, optional
            A function called on each text element (e.g., remove leading ':')

        Returns
        ----------
        list of str
            All text data that meet the input constraints
        """

        tol = tol if isinstance(tol, tuple) else (tol, tol)

        block_data = []
        for i, data in enumerate(self.data["text"]):
            valid_x = is_in_tol(int(self.data["x"][i]), pos[0], tol[0])
            valid_y = is_in_tol(int(self.data["y"][i]), pos[1], tol[1])
            if valid_x and valid_y:
                data_clean = (
                    data.strip()
                    if text_cleaner is None
                    else text_cleaner(data)
                )
                if data_clean:
                    block_data.append(data_clean)
        return block_data
