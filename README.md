# PubMed Scout

A command-line tool for fetching PubMed papers with biotech/pharma affiliations and exporting them to CSV format. This tool helps researchers identify academic publications authored by individuals affiliated with pharmaceutical and biotechnology companies.

## Project Description

PubMed Scout searches the PubMed database using custom queries and filters results to identify papers with authors from non-academic institutions (specifically biotech and pharmaceutical companies). The tool extracts key information including author details, company affiliations, and contact emails, then exports the data to a structured CSV format for further analysis.

### Key Features

- **Targeted Search**: Search PubMed with custom queries using full PubMed syntax
- **Company Affiliation Detection**: Automatically identifies biotech/pharma company affiliations
- **Email Extraction**: Extracts author email addresses from affiliation text
- **CSV Export**: Exports results to CSV format for easy data analysis
- **Debug Mode**: Comprehensive logging for troubleshooting and monitoring
- **Robust Error Handling**: Graceful handling of API failures and invalid data

## Project Structure

```
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
```

### Code Organization

- **`cli.py`**: Main command-line interface using Typer, orchestrates the entire workflow
- **`fetch.py`**: Handles all interactions with PubMed's E-utilities API (Esearch and Efetch)
- **`parse.py`**: Parses XML responses and extracts relevant article information
- **`export_to_csv.py`**: Handles CSV file generation and export functionality
- **`constants.py`**: Centralized configuration and API endpoints
- **`logger_setup.py`**: Configurable logging system with debug support

### Output Directories

- **`logs/`**: Application logs are written here (created automatically)
- **`pubmed_scout_output/`**: CSV output files are saved here (created automatically)

## Installation and Setup

### Prerequisites

- Python 3.13 or higher
- Poetry (for dependency management)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pubmed-scout
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies:**
   ```bash
   poetry install
   ```

4. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

## Usage

### Basic Usage

Search for papers and export to CSV:
```bash
poetry run get-papers-list "biotech AND cancer AND 2023"
```

### Advanced Usage

**Specify number of results:**
```bash
poetry run get-papers-list "pharma AND COVID-19" --retmax 10
```

**Custom output filename:**
```bash
poetry run get-papers-list "therapeutics AND diabetes" -f "diabetes_research.csv"
```

**Enable debug mode:**
```bash
poetry run get-papers-list "biotech AND 2024" --debug
```

**Combined options:**
```bash
poetry run get-papers-list "pharma AND oncology" --retmax 20 -f "oncology_papers.csv" --debug
```

### Command Options

- `query`: PubMed search query (required)
- `--retmax`: Maximum number of results to return (default: 5)
- `--filename, -f`: Output CSV filename (default: "output.csv")
- `--debug, -d`: Enable debug mode for detailed logging

### Output

The tool generates files in the following locations:

**CSV Output** (`./pubmed_scout_output/`):
- **PubmedID**: Unique PubMed identifier
- **Title**: Article title
- **Publication Date**: Publication date
- **Non-Academic Authors**: Authors affiliated with companies
- **Company Affiliations**: Company/organization names
- **Corresponding Author Email**: Contact email addresses

**Logs** (`./logs/`):
- Application logs with detailed execution information
- Debug logs when `--debug` flag is used

---

## Testing

Run the test suite:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=pubmed_scout
```

## Tools and Libraries Used

### Core Dependencies
- **[Typer](https://typer.tiangolo.com/)**: Modern CLI framework for building command-line applications
- **[Requests](https://docs.python-requests.org/)**: HTTP library for API interactions
- **[Python Standard Library](https://docs.python.org/3/library/)**:
  - `xml.etree.ElementTree`: XML parsing
  - `csv`: CSV file handling
  - `logging`: Comprehensive logging system
  - `re`: Regular expressions for email extraction

### Development Tools
- **[Poetry](https://python-poetry.org/)**: Dependency management and packaging
- **[pytest](https://docs.pytest.org/)**: Testing framework
- **[Python 3.13](https://www.python.org/)**: Latest Python version with enhanced type hints

### APIs Used
- **[PubMed E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25497/)**: 
  - Esearch: For searching PubMed database
  - Efetch: For retrieving detailed article information


## Error Handling

The application includes comprehensive error handling for:
- Invalid API responses
- Network connectivity issues
- Malformed XML data
- File system permissions
- Invalid user inputs

Debug mode provides detailed logging to `./logs/pubmed_scout.log` for troubleshooting.

### Ignored Files
The following files and directories are excluded from version control:
- `logs/` - Application logs
- `pubmed_scout_output/` - CSV output files
- `__pycache__/` - Python bytecode
- `.pytest_cache/` - Pytest cache files

### Cleaning Up
To clean output and log files:
```bash
# Remove output files
rm -rf pubmed_scout_output/
rm -rf logs/

# Remove cache files
rm -rf __pycache__/
rm -rf .pytest_cache/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License. See the `pyproject.toml` file for details.


## Examples

### Sample Output Structure

After running a search, your directory will look like:
```
pubmed-scout/
├── logs/
│   └── pubmed_scout.log         # Application logs
├── pubmed_scout_output/
│   └── output.csv               # Search results
└── ... (other project files)
```

### Sample CSV Content
```csv
PubmedID,Title,Publication Date,Non-Academic Authors,Company Affiliations,Corresponding Author Email
40745406,Comparison of outcomes in autoimmune acquired factor XIII deficiency...,2025 Jul 31,Hu Zhou; Bingjie Ding,Department of Hematology Henan Cancer hospital...,tigerzhoupumc@163.com
```