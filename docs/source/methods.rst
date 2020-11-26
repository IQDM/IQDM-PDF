============
How it Works
============

IQDM-PDF uses `pdfminer.six <https://github.com/pdfminer/pdfminer.six>`__ to
extract text and coordinates from IMRT QA PDF files.

Step 1: Match Report Parser
============================
All of the text is extacted from the PDF into a simple string. Each report
parser has an `identifiers` property which is a list of strings. If all of
the identifier strings are found in the extracted text, that report parser
will be selected.

Step 2: Parse Data by Text Box Coordinates
===========================================
The text data is collected with the selected report parser, stored by page
along with the bounding box coordinates.  Report parsers can look up a text
value by page and coordinate with the `get_block_data <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#IQDMPDF.pdf_reader.CustomPDFReader.get_block_data>`__
function.

Step 3: Apply Template
======================
Unless customized logic is needed, a `GenericParser <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#module-IQDMPDF.parsers.generic>`__
class can be used that relies solely on a JSON template file. The JSON
template file requires three keys: `report type`, `identifiers`, and `data`.
Required keys of `data` are `column`, `page`, and `pos`. For further
customization, all keys in each item of `data` (except `column`) are passed
into `get_block_data <https://iqdm-pdf.readthedocs.io/en/latest/iqdmpdf.html#IQDMPDF.pdf_reader.CustomPDFReader.get_block_data>`__.

You can check out the `report templates <https://github.com/IQDM/IQDM-PDF/tree/master/IQDMPDF/report_templates>`__
on GitHub for examples.

In the simplest case, a report parser class looks something like this `[source] <https://iqdm-pdf.readthedocs.io/en/latest/_modules/IQDMPDF/parsers/sncpatient.html#SNCPatientReport2020>`__:

.. code-block:: python

    class SNCPatientReport2020(GenericReport):
        """SNCPatientReport parser for the new format released in 2020"""

        def __init__(self):
            """Initialization of a SNCPatientReport class"""
            template = join(DIRECTORIES["REPORT_TEMPLATES"], "sncpatient2020.json")
            GenericReport.__init__(self, template)


Step 4: Iterate
===============
From the command-line, you can iterate over all files in a provided directory,
and save the results (per vendor/template) into a .csv file:

    $ iqdmpdf your/initial/dir