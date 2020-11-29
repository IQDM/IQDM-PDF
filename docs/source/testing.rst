============
Unit Testing
============

IQDM-PDF employs unit testing to ensure that updates don't break previous
examples. It also ensures that the identifiers assigned to a report parser
are sufficiently unique.

New Example PDFs
================
Any modifications to report parsers require an example PDF to be included in
`tests/test_data/examples_reports <https://github.com/IQDM/IQDM-PDF/tree/master/tests/test_data/example_reports>`__.
The expected results should be added to `tests/test_data/expected_report_data.py <https://github.com/IQDM/IQDM-PDF/blob/master/tests/test_data/expected_report_data.py>`__.

Expected Report Data
====================
The variable ``TEST_DATA`` in `expected_report_data.py <https://github.com/IQDM/IQDM-PDF/blob/master/tests/test_data/expected_report_data.py>`__ contains exepected
data and paths to PDFs for all vendors. An example output from
`TEST_DATA[vendor][example_description]`:


.. code-block:: python

    {
      "path": join(DIRECTORIES["DELTA4_EXAMPLES"], "UChicago", "DCAM_example_1.pdf"),
      "data": summary_data
    }

Where ``summary_data`` is the output from the report parser's property
``summary_data``.  It's important to use ``IQDMPDF.paths.DIRECTORIES`` to ensure source
code and installed versions know where the test data is.

If adding a new vendor or report template, a new unit testing class can be
added to `tests/test_report_parsers.py <https://github.com/IQDM/IQDM-PDF/blob/master/tests/test_report_parsers.py>`__
in a fashion similar to below:

.. code-block:: python

    class TestNewVendor(TestReportParserBase, unittest.TestCase):
        def setUp(self):
            self.do_setup_for_vendor("new_vendor")


Then just update ``PARSERS`` near the top of `test_report_parsers.py`
with a "new_vendor" key pointing to the new report parser.