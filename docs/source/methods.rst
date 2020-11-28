============
How It Works
============

IQDM-PDF uses `pdfminer.six <https://github.com/pdfminer/pdfminer.six>`__ to
extract text and coordinates from IMRT QA PDF files.

Step 1: Match Report Parser
============================
All of the text is extracted from the PDF into a simple string. Each report
parser has an ``identifiers`` property which is a list of strings. If all of
the identifier strings are found in the extracted text, that report parser
will be selected.

Step 2: Parse Data by Text Box Coordinates
===========================================
The text data is collected with the selected report parser, stored by page
along with the bounding box coordinates.  Report parsers can look up a text
value by page and coordinate.

Step 3: Apply Template
======================
Unless customized logic is needed, a `GenericParser <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#module-IQDMPDF.parsers.generic>`__
class can be used, which reads in a  JSON file containing three keys:
``report type``, ``identifiers``, and ``data``. Required keys of ``data``
are ``column``, ``page``, and ``pos``. For further customization, ``tolerance``
and ``mode`` can be specified. All keys from ``data`` (except ``column``) are
passed into the `get_block_data <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#IQDMPDF.pdf_reader.CustomPDFReader.get_block_data>`__
function in ``CustomPDFReader``.

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


Building a New Template
=======================
Currently, building a new template requires some python coding. The output
from the following code will show all text bounding box coordinates and
contents.

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


The ``pos`` element is assumed to be the bottom left corner of the bounding
box by default. If the PDF layout has centered or right-aligned, you can
also specify ``mode`` to be any combination of bottom/center/top and
left/center/right. For example, ``top-right`` or ``center-left``;
``center`` is equivalent to ``center-center``.

For example, if an element is more consistently found at the center of a
bounding box, the ``data`` element could look like:

.. code-block:: json

    {
      "column": "Difference (%)",
      "page": 0,
      "pos": [88.79, 424.18],
      "mode": "center"
    }