#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup.py

from setuptools import setup, find_packages
from IQDMPDF._version import __version__, __author__


with open("requirements.txt") as doc:
    requires = [line.strip() for line in doc]

with open("README.rst") as doc:
    long_description = doc.read()


CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Science/Research",
    "Natural Language :: English",
    "Development Status :: 2 - Pre-Alpha",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
    "Topic :: Scientific/Engineering :: Physics",
]


setup(
    name="IQDMPDF",
    version=__version__,
    include_package_data=True,
    python_requires=">3.5",
    packages=find_packages(),
    description="Scans a directory for IMRT QA results",
    author=__author__,
    maintainer=__author__,
    url="https://github.com/IQDM/IQDM-PDF",
    download_url="https://github.com/IQDM/IQDM-PDF.git",
    license="MIT License",
    keywords=["data mining", "radiation oncology", "IMRT QA"],
    classifiers=CLASSIFIERS,
    install_requires=requires,
    long_description=long_description,
    test_suite="tests",
    tests_require=[],
    entry_points={
        "console_scripts": [
            "IQDMPDF=IQDMPDF.main:main",
        ],
    },
)
