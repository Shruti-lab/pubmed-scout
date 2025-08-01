"""
PubMed Scout - A tool for fetching PubMed papers with biotech/pharma affiliations.

This package provides functionality to search PubMed, identify papers with 
biotech/pharmaceutical company affiliations, and export the results to CSV format.
"""

__version__ = "0.1.0"
__author__ = "Shruti-lab"
__description__ = "Fetch PubMed papers with biotech/pharma affiliations and export them to CSV"

from .cli import main, get_papers
from .fetch import search_pubmed_IDs, fetch_article_details
from .parse import parse_fetch_response, is_company_affiliation
from .export_to_csv import article_to_csv

__all__ = [
    "main",
    "get_papers", 
    "search_pubmed_IDs",
    "fetch_article_details",
    "parse_fetch_response",
    "is_company_affiliation",
    "article_to_csv",
]