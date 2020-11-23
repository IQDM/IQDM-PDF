IQDMPDF
=======


What does it do?
----------------
Scans a directory for IMRT QA reports and parses data into a CSV


Other information
-----------------

-  Free software: MIT License
-  Documentation: TBD
-  Tested on Python TBD


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

    usage: iqdmpdf [-h] [-ie] [-od OUTPUT_DIR] [-rd RESULTS_DIR] [-all]
                   [-of OUTPUT_FILE] [-ver] [-nr] [-df]
                   [file_path]

    Command line interface for IQDM

    positional arguments:
      file_path             Initiate scan if directory, launch dashboard if
                            results file

    optional arguments:
      -h, --help            show this help message and exit
      -ie, --ignore-extension
                            Script will check all files, not just ones with .pdf
                            extensions
      -od OUTPUT_DIR, --output-dir OUTPUT_DIR
                            Output stored in local directory by default, specify
                            otherwise here
      -rd RESULTS_DIR, --results-dir RESULTS_DIR
                            Results assumed to be stored in local directory by
                            default, specify otherwise here
      -all, --process-all   Process all identified report files, otherwise only
                            new reports will be analyzed
      -of OUTPUT_FILE, --output-file OUTPUT_FILE
                            Output will be saved as <report_type>_results_<time-
                            stamp>.csv by default. Define this tag to customize
                            file name after <report_type>_
      -ver, --version       Print the IQDM version
      -nr, --no-recursive-search
                            Include this flag to skip sub-directories
      -df, --day-first      Assume day first for ambiguous dates in trending
                            dashboard

Vendor Compatibility
--------------------

* `Sun Nuclear <http://sunnuclear.com>`__: *SNC Patient*
* `ScandiDos <http://scandidos.com>`__: *Delta4*

