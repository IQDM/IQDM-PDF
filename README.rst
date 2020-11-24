IQDMPDF
=======

|build| |Docs| |pypi| |python-version| |lgtm| |lgtm-cq| |Codecov|

What does it do?
----------------
Scans a directory for IMRT QA reports and parses data into a CSV


Other information
-----------------

-  Free software: `MIT license <https://github.com/IQDM/IQDM-PDF/blob/master/LICENSE>`__
-  Documentation: `Read the docs <https://iqdm-pdf.readthedocs.io>`__
-  Tested on Python 3.6, 3.7, 3.8, 3.9


Dependencies
------------

-  `pdfminer.six <https://github.com/pdfminer/pdfminer.six>`__
-  `python-dateutil <http://scikit-learn.org>`__
-  `chardet <https://pypi.org/project/regressors/>`__
-  `pathvalidate <http://matplotlib.org>`__


How to run
----------

To scan a directory for IMRT QA report files and genereate a results .csv file:

`iqdmpdf <initial-scan-dir>`



Command line usage
------------------

.. code-block:: console

    usage: IQDMPDF [-h] [-ie] [-od OUTPUT_DIR] [-of OUTPUT_FILE] [-ver] [-nr]
                   [directory]

    Command line interface for IQDM

    positional arguments:
      directory             Initiate scan here

    optional arguments:
      -h, --help            show this help message and exit
      -ie, --ignore-extension
                            Script will check all files, not just ones with .pdf
                            extensions
      -od OUTPUT_DIR, --output-dir OUTPUT_DIR
                            Output stored in local directory by default, specify
                            otherwise here
      -of OUTPUT_FILE, --output-file OUTPUT_FILE
                            Output will be saved as <report_type>_results_<time-
                            stamp>.csv by default. Define this tag to customize
                            file name after <report_type>_
      -ver, --version       Print the IQDM version
      -nr, --no-recursive-search
                            Include this flag to skip sub-directories


Vendor Compatibility
--------------------

* `Sun Nuclear <http://sunnuclear.com>`__: *SNC Patient*
* `ScandiDos <http://scandidos.com>`__: *Delta4*


.. |build| image:: https://github.com/IQDM/IQDM-PDF/workflows/build/badge.svg
   :target: https://github.com/IQDM/IQDM-PDF/actions
   :alt: build
.. |pypi| image:: https://img.shields.io/pypi/v/IQDMPDF.svg
   :target: https://pypi.org/project/IQDMPDF
   :alt: PyPI
.. |python-version| image:: https://img.shields.io/pypi/pyversions/IQDMPDF.svg
   :target: https://pypi.org/project/IQDMPDF
   :alt: Python Version
.. |lgtm-cq| image:: https://img.shields.io/lgtm/grade/python/g/IQDM/IQDM-PDF.svg?logo=lgtm&label=code%20quality
   :target: https://lgtm.com/projects/g/IQDM/IQDM-PDF/context:python
   :alt: lgtm code quality
.. |lgtm| image:: https://img.shields.io/lgtm/alerts/g/IQDM/IQDM-PDF.svg?logo=lgtm
   :target: https://lgtm.com/projects/g/IQDM/IQDM-PDF/alerts
   :alt: lgtm
.. |Codecov| image:: https://codecov.io/gh/IQDM/IQDM-PDF/branch/master/graph/badge.svg?token=C1B5689HQH
   :target: https://codecov.io/gh/IQDM/IQDM-PDF
   :alt: Codecov
.. |Docs| image:: https://readthedocs.org/projects/iqdm-pdf/badge/?version=latest
   :target: https://iqdm-pdf.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
