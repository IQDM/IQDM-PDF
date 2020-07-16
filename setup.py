from setuptools import setup, find_packages
from IQDMPDF._version import __version__

requires = [
    'pdfminer.six',
    'pdfminer > 19',
    'numpy',
    'python-dateutil',
    'chardet == 3.0.4',
    'pathvalidate',
    'python-dateutil',
    'pathvalidate'
]

with open('README.md', 'r') as doc:
    long_description = doc.read()

setup(
    name='IQDMPDF',
    include_package_data=True,
    packages=find_packages(),
    version=__version__,
    description='Scans a directory for IMRT QA results',
    author='Dan Cutright',
    author_email='dan.cutright@gmail.com',
    url='https://github.com/IQDM/IQDM-PDF',
    download_url='https://github.com/IQDM/IQDM-PDF/archive/master.zip',
    license="MIT License",
    keywords=['radiation therapy', 'qa', 'research'],
    classifiers=[],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'IQDMPDF=IQDMPDF.main:main',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)