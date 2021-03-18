============
How It Works
============

IQDM-PDF uses `pdfminer.six <https://github.com/pdfminer/pdfminer.six>`__ to
extract text and coordinates from IMRT QA PDF files.

Step 1: Match Report Parser
============================
Each report parser has an ``identifiers`` property which contains words and
phrases used to uniquely pair a PDF to a report parser. If all of the
identifiers are found in the PDF text, that report parser will be
selected.

Step 2: Parse Data by Text Box Coordinates
===========================================
The text data is collected with the selected report parser, which is stored by
page and bounding box coordinates. Report parsers can look up a text value by
page and coordinate.

Step 3: Apply Template
======================
Unless customized logic is needed, a `GenericParser <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#module-IQDMPDF.parsers.generic>`__
class can be used, which reads in a  JSON file containing three keys:
``report type``, ``identifiers``, and ``data``. Required keys of ``data``
are ``column``, ``page``, and ``pos``. For further customization, see
the `get_block_data <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#IQDMPDF.pdf_reader.CustomPDFReader.get_block_data>`__
function documentation in ``CustomPDFReader``. All keys from ``data`` (except
``column``) are passed.

Check out the `report templates <https://github.com/IQDM/IQDM-PDF/tree/master/IQDMPDF/report_templates>`__
on GitHub for examples.

In the simplest case, a report parser class looks something like the following
`[source] <https://iqdm-pdf.readthedocs.io/en/latest/_modules/IQDMPDF/parsers/sncpatient.html#SNCPatientReport2020>`__:

.. code-block:: python

    class SNCPatientReport2020(GenericReport):
        """SNCPatientReport parser for the new format released in 2020"""

        def __init__(self):
            """Initialization of a SNCPatientReport class"""
            template = join(DIRECTORIES["REPORT_TEMPLATES"], "sncpatient2020.json")
            GenericReport.__init__(self, template)


Then update the ``REPORT_CLASSES`` list in `parser.py <https://iqdm-pdf.readthedocs.io/en/latest/_modules/IQDMPDF/parsers/parser.html>`__
to include the new report parser class.

Step 4: Iterate
===============
From the command-line, you can iterate over all files in a provided directory,
and save the results into a CSV file per vendor/template:

    $ iqdmpdf your/initial/dir

Or from a python console:

.. code-block:: python

    >>> from IQDMPDF.file_processor import process_files
    >>> process_files("your/initial/dir")


Non-Template Based Parsing
==========================
If the data in the reports have varying coordinates, the code needs more
customization. See the `Delta4 <https://iqdm-pdf.readthedocs.io/en/latest/_modules/IQDMPDF/parsers/delta4.html#Delta4Report>`__
report parser for examples/inspiration.

Generally speaking, the `LAParams for pdfminer.six <https://pdfminersix.readthedocs.io/en/latest/reference/composable.html#api-laparams>`__
are customized (e.g., ``char_margin``, ``line_margin``) to get sections of the
IMRT QA report text to be collected into one block. Then key words are used to
connect data to variable names. Another trick is to look up the positions
boxes containing key words, then use the y-position to search for another
block of text laterally (used frequently in the `PTW Verisoft <https://iqdm-pdf.readthedocs.io/en/latest/_modules/IQDMPDF/parsers/verisoft.html#VeriSoftReport>`__ parser).

These methods are needed if reports have variable templates, fonts, or font
sizes. So far, all of IQDM-PDF's parsers are non-template based, with the
exception of the new SNC Patient format introduced in 2020.

Building a New Template
=======================
Currently, building a new JSON template requires some python scripting to
determine coordinates. The output from the following code will show all text
bounding box coordinates and contents.

.. code-block:: python

    >>> from IQDMPDF.pdf_reader import CustomPDFReader
    >>> data = CustomPDFReader("path/to/report.pdf")
    >>> print(data)

Below is a sample of the output from:
`example_reports/sncpatient/UChicago/DCAM_example_1.pdf`

.. code-block:: python

    page_index: 0, data_index: 21
    bbox: [6.24, 445.18, 140.33, 463.88]
    Absolute Dose Comparison
    Difference (%)

    page_index: 0, data_index: 22
    bbox: [79.2, 445.18, 88.84, 452.14]
     : 2

    page_index: 0, data_index: 23
    bbox: [6.24, 432.94, 51.47, 439.9]
    Distance (mm)

    page_index: 0, data_index: 24
    bbox: [79.2, 432.94, 88.84, 439.9]
     : 2

    page_index: 0, data_index: 25
    bbox: [6.24, 420.7, 49.8, 427.66]
    Threshold (%)

    page_index: 0, data_index: 26
    bbox: [79.2, 420.7, 98.37, 427.66]
     : 10.0

The ``data`` object in the resulting JSON file for this data would look like:

.. code-block:: json

    [
        {"column": "Difference (%)", "page": 0, "pos": [79.2, 441.02]},
        {"column": "Distance (mm)", "page": 0, "pos": [79.2, 432.94]},
        {"column": "Threshold (%)", "page": 0, "pos": [79.2, 420.7]}
    ]

Note that the value for ``column`` doesn't need to match any text in the PDF.


The ``pos`` element is assumed to be the bottom left corner of the bounding
box by default. If the PDF layout has centered or right-aligned elements, you
can specify ``mode`` to be any combination of bottom/center/top and
left/center/right. (*e.g.*, ``top-right`` or ``center-left``;
``center`` is equivalent to ``center-center``).

For example, if an element is more consistently found at the center of a
bounding box, the ``data`` element could look like:

.. code-block:: json

    {
      "column": "Difference (%)",
      "page": 0,
      "pos": [88.79, 424.18],
      "mode": "center"
    }