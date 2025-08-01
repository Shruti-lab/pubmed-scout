==============
PubMed Scout
==============

A command-line tool for fetching PubMed papers with biotech/pharma affiliations and exporting them to CSV format. This tool helps researchers identify academic publications authored by individuals affiliated with pharmaceutical and biotechnology companies.

.. contents:: Table of Contents
   :depth: 2
   :local:

Project Description
===================

PubMed Scout searches the PubMed database using custom queries and filters results to identify papers with authors from non-academic institutions (specifically biotech and pharmaceutical companies). The tool extracts key information including author details, company affiliations, and contact emails, then exports the data to a structured CSV format for further analysis.

Key Features
------------

- **Targeted Search**: Search PubMed with custom queries using full PubMed syntax
- **Company Affiliation Detection**: Automatically identifies biotech/pharma company affiliations
- **Email Extraction**: Extracts author email addresses from affiliation text
- **CSV Export**: Exports results to CSV format for easy data analysis
- **Debug Mode**: Comprehensive logging for troubleshooting and monitoring
- **Robust Error Handling**: Graceful handling of API failures and invalid data

Project Structure
=================

.. code-block:: text

    pubmed-scout/
    ├── README.md
    ├── README.rst
    ├── pyproject.toml               # Project configuration and dependencies
    ├── poetry.lock                  # Lock file for reproducible builds
    ├── .gitignore                   # Git ignore patterns
    ├── logs/                        # Application logs (created at runtime)
    │   └── pubmed_scout.log
    ├── pubmed_scout_output/         # CSV output files (created at runtime)
    │   └── output.csv
    ├── src/
    │   └── pubmed_scout/
    │       ├── __init__.py
    │       ├── cli.py               # Command-line interface and main entry point
    │       ├── constants.py         # API endpoints and configuration constants
    │       ├── fetch.py             # PubMed API interaction functions
    │       ├── parse.py             # XML parsing and data extraction logic
    │       ├── export_to_csv.py     # CSV export functionality
    │       └── logger_setup.py      # Logging configuration
    └── tests/
        ├── __init__.py
        ├── test_fetch.py            # Tests for API interaction
        ├── test_parse.py            # Tests for XML parsing
        └── test_export.py           # Tests for CSV export


Code Organization
-----------------

**cli.py**
    Main command-line interface using Typer, orchestrates the entire workflow

**fetch.py**
    Handles all interactions with PubMed's E-utilities API (Esearch and Efetch)

**parse.py**
    Parses XML responses and extracts relevant article information

**export_to_csv.py**
    Handles CSV file generation and export functionality

**constants.py**
    Centralized configuration and API endpoints

**logger_setup.py**
    Configurable logging system with debug support


Output Directories
------------------

**logs/**
    Application logs are written here (created automatically)

**pubmed_scout_output/**
    CSV output files are saved here (created automatically)


Installation and Setup
======================

Prerequisites
-------------

- Python 3.13 or higher
- Poetry (for dependency management)

Installation Steps
------------------

1. **Clone the repository:**

   .. code-block:: bash

      git clone <repository-url>
      cd pubmed-scout

2. **Install Poetry** (if not already installed):

   .. code-block:: bash

      curl -sSL https://install.python-poetry.org | python3 -

3. **Install dependencies:**

   .. code-block:: bash

      poetry install

4. **Activate the virtual environment:**

   .. code-block:: bash

      poetry shell

Usage
=====

Basic Usage
-----------

Search for papers and export to CSV:

.. code-block:: bash

   poetry run get-papers-list "biotech AND cancer AND 2023"

Advanced Usage
--------------

**Specify number of results:**

.. code-block:: bash

   poetry run get-papers-list "pharma AND COVID-19" --retmax 10

**Custom output filename:**

.. code-block:: bash

   poetry run get-papers-list "therapeutics AND diabetes" -f "diabetes_research.csv"

**Enable debug mode:**

.. code-block:: bash

   poetry run get-papers-list "biotech AND 2024" --debug

**Combined options:**

.. code-block:: bash

   poetry run get-papers-list "pharma AND oncology" --retmax 20 -f "oncology_papers.csv" --debug

Command Options
---------------

- ``query``: PubMed search query (required)
- ``--retmax``: Maximum number of results to return (default: 5)
- ``--filename, -f``: Output CSV filename (default: "output.csv")
- ``--debug, -d``: Enable debug mode for detailed logging

Output
------

The tool generates files in the following locations:

**CSV Output** (``./pubmed_scout_output/``):

- **PubmedID**: Unique PubMed identifier
- **Title**: Article title
- **Publication Date**: Publication date
- **Non-Academic Authors**: Authors affiliated with companies
- **Company Affiliations**: Company/organization names
- **Corresponding Author Email**: Contact email addresses

**Logs** (``./logs/``):

- Application logs with detailed execution information
- Debug logs output on console when ``--debug`` flag is used


Testing
=======

Run the test suite:

.. code-block:: bash

   poetry run pytest

Run tests with coverage:

.. code-block:: bash

   poetry run pytest --cov=pubmed_scout

Run specific test modules:

.. code-block:: bash

   poetry run pytest tests/test_fetch.py -v
   poetry run pytest tests/test_parse.py -v
   poetry run pytest tests/test_export.py -v


Tools and Libraries Used
========================

Core Dependencies
-----------------

- `Typer <https://typer.tiangolo.com/>`_: Modern CLI framework for building command-line applications
- `Requests <https://docs.python-requests.org/>`_: HTTP library for API interactions
- `Python Standard Library <https://docs.python.org/3/library/>`_:
  
  - ``xml.etree.ElementTree``: XML parsing
  - ``csv``: CSV file handling
  - ``logging``: Comprehensive logging system
  - ``re``: Regular expressions for email extraction

Development Tools
-----------------

- `Poetry <https://python-poetry.org/>`_: Dependency management and packaging
- `pytest <https://docs.pytest.org/>`_: Testing framework
- `pytest-cov <https://pytest-cov.readthedocs.io/>`_: Coverage reporting
- `Python 3.13 <https://www.python.org/>`_: Latest Python version with enhanced type hints

APIs Used
---------

- `PubMed E-utilities API <https://www.ncbi.nlm.nih.gov/books/NBK25497/>`_:
  
  - **Esearch**: For searching PubMed database
  - **Efetch**: For retrieving detailed article information


Error Handling
==============

The application includes comprehensive error handling for:

- Invalid API responses
- Network connectivity issues
- Malformed XML data
- File system permissions
- Invalid user inputs

Debug mode provides detailed logging to ``./logs/pubmed_scout.log`` for troubleshooting.

File Management
===============

Ignored Files
-------------

The following files and directories are excluded from version control:

- ``logs/`` - Application logs
- ``pubmed_scout_output/`` - CSV output files
- ``__pycache__/`` - Python bytecode
- ``.pytest_cache/`` - Pytest cache files

Cleaning Up
-----------

To clean output and log files:

.. code-block:: bash

   # Remove output files
   rm -rf pubmed_scout_output/
   rm -rf logs/

   # Remove cache files
   rm -rf __pycache__/
   rm -rf .pytest_cache/


Contributing
============

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

License
=======

This project is licensed under the MIT License. See the ``pyproject.toml`` file for details.

Examples
========

Search Examples
---------------

**Search for cancer research from biotech companies:**

.. code-block:: bash

   poetry run get-papers-list "cancer AND biotech" --retmax 10

**Search for COVID-19 papers from pharmaceutical companies:**

.. code-block:: bash

   poetry run get-papers-list "COVID-19 AND (pharma OR pharmaceutical)" -f "covid_pharma.csv"

**Search with specific year filter:**

.. code-block:: bash

   poetry run get-papers-list "therapeutics AND 2024[PDAT]" --debug

**Advanced search with multiple keywords:**

.. code-block:: bash

   poetry run get-papers-list "(biotech OR biotechnology) AND (cancer OR oncology) AND 2023[PDAT]" --retmax 20

Sample Output
-------------

.. code-block:: text

   Running PubMed Scout with query: biotech AND cancer
   Search results for query 'biotech AND cancer': 1234 results found.
   Found 5 results for query 'biotech AND cancer'.
   Fetching article details...
   Fetched details for 3 articles.
   Exported 3 articles to output.csv.

The resulting CSV will contain structured data about papers with biotech/pharma affiliations, making it easy to analyze industry-academic collaborations and identify potential research partnerships.

Sample Output Structure
-----------------------

After running a search, your directory will look like:

.. code-block:: text

   pubmed-scout/
   ├── logs/
   │   └── pubmed_scout.log         # Application logs
   ├── pubmed_scout_output/
   │   └── output.csv               # Search results
   └── ... (other project files)

Sample CSV Content
------------------

.. code-block:: text

   PubmedID,Title,Publication Date,Non-Academic Authors,Company Affiliations,Corresponding Author Email
   40745406,Comparison of outcomes in autoimmune acquired factor XIII deficiency...,2025 Jul 31,Hu Zhou; Bingjie Ding,Department of Hematology Henan Cancer hospital...,tigerzhoupumc@163.com


API Reference
=============

For detailed information about the PubMed E-utilities API used by this tool, refer to:

- `E-utilities Quick Start <https://www.ncbi.nlm.nih.gov/books/NBK25500/>`_
- `E-utilities Help <https://www.ncbi.nlm.nih.gov/books/NBK25497/>`_
- `PubMed Search Field Descriptions <https://pubmed.ncbi.nlm.nih.gov/help/#search-tags>`_