IQDM-PDF
========

|build| |Docs| |pypi| |python-version| |lgtm| |lgtm-cq| |Codecov| |lines| |repo-size| |code-style|

What does it do?
----------------
Scans a directory for IMRT QA reports and parses data into a CSV.


Other information
-----------------
This library is part of the IMRT QA Data Mining (IQDM) project for
the `AAPM's IMRT Working Group (WGIMRT) <https://www.aapm.org/org/structure/?committee_code=WGIMRT>`__.

-  Free software: `MIT license <https://github.com/IQDM/IQDM-PDF/blob/master/LICENSE>`__
-  Documentation: `Read the docs <https://iqdm-pdf.readthedocs.io>`__
-  Tested on Python 3.6, 3.7, 3.8, 3.9


Dependencies
------------

* `pdfminer.six <https://github.com/pdfminer/pdfminer.six>`__
* `tqdm <https://github.com/tqdm/tqdm>`__


Install
-------

Latest PyPI release:

    $ pip install iqdmpdf

Install from source:

    $ python setup.py install

If you do not have a C++ compiler installed, you might have issues with
installing the latest version of pdfminer.six. The following might resolve
your issue:

    $ pip install pdfminer.six==20200726


Usage
-----

To scan a directory for IMRT QA report files and generate a results .csv file
into your current directory:

    $ iqdmpdf [init_directory]

As of v0.2.2, multi-threading is enabled. For example, you can enable 4
simultaneous threads with the following:

    $ iqdmpdf [init_directory] -n 4

.. code-block:: console

    usage: iqdmpdf [-h] [-ie] [-od OUTPUT_DIR] [-of OUTPUT_FILE] [-ver] [-nr]
                   [-re] [-n PROCESSES]
                   [init_directory]

    Command line interface for IQDM-PDF

    positional arguments:
      init_directory        Initiate scan here

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
      -re, --raise-errors   Allow failed file parsing to halt the program
      -n PROCESSES, --processes PROCESSES
                            Enable multiprocessing, set number of parallel
                            processes




Vendor Compatibility
--------------------

We plan to support many vendors. If the report is very consistent, a new JSON
file in the `report_templates <https://github.com/IQDM/IQDM-PDF/tree/master/IQDMPDF/report_templates>`__
is essentially all that is needed. Additional documentation for custom
templates can be found `here <https://iqdm-pdf.readthedocs.io/en/latest/methods.html#building-a-new-template>`__.

* `Sun Nuclear <http://sunnuclear.com>`__: *SNC Patient*
* `ScandiDos <http://scandidos.com>`__: *Delta4*
* `PTW <https://www.ptwdosimetry.com/>`__: *VeriSoft*


Credits
-------

----------------
Development Lead
----------------

* Dan Cutright

------------
Contributors
------------

* Marc Chamberland
* Aditya Panchal


---------
Test Data
---------
Example IMRT QA reports used for unit testing and design are available `here <https://github.com/IQDM/IQDM-PDF/tree/master/tests/test_data/example_reports>`__.

* Dan Cutright, University of Chicago Hospital
    * delta4/UChicago
    * sncpatient/UChicago

* Serpil Kucuker Dogan, Nortwestern Memorial Hospital
    * sncpatient/Northwestern_Memorial
    * sncpatient2020/Northwestern_Memorial

* Aditya Panchal, AMITA Health
    * verisoft/AMITA_Health


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
.. |lines| image:: https://img.shields.io/tokei/lines/github/iqdm/iqdm-pdf
   :target: https://img.shields.io/tokei/lines/github/iqdm/iqdm-pdf
   :alt: Lines of code
.. |repo-size| image:: https://img.shields.io/github/languages/code-size/iqdm/iqdm-pdf
   :target: https://img.shields.io/github/languages/code-size/iqdm/iqdm-pdf
   :alt: Repo Size
.. |code-style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black