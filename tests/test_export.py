import pytest
import csv
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from pubmed_scout.export_to_csv import article_to_csv


class TestArticleToCSV:
    """Test cases for article_to_csv function."""
    
    def test_export_with_filename(self):
        """Test CSV export with specified filename."""
        articles = [
            {
                "PubmedID": "12345",
                "Title": "Test Article 1",
                "Publication Date": "2023 Jan 15",
                "Non-Academic Authors": "John Doe",
                "Company Affiliations": "BioTech Corp",
                "Corresponding Author Email": "john@biotech.com"
            },
            {
                "PubmedID": "67890",
                "Title": "Test Article 2",
                "Publication Date": "2023 Feb 20",
                "Non-Academic Authors": "Jane Smith",
                "Company Affiliations": "Pharma Inc",
                "Corresponding Author Email": "jane@pharma.com"
            }
        ]
        
        with NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as tmp_file:
            filename = tmp_file.name
        
        try:
            article_to_csv(articles, filename)
            
            # Verify the file contents
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                assert len(rows) == 2
                assert rows[0]["PubmedID"] == "12345"
                assert rows[1]["PubmedID"] == "67890"
        finally:
            os.unlink(filename)
    
    def test_export_default_filename(self):
        """Test CSV export with default filename."""
        articles = [
            {
                "PubmedID": "12345",
                "Title": "Sample Study on BioTech Innovations",
                "Publication Date": "2025 July 30",
                "Non-Academic Authors": "John Doe",
                "Company Affiliations": "BioTech Corp",
                "Corresponding Author Email": "john@biotech.com"
            }
        ]
        
        try:
            article_to_csv(articles, "")
            
            # Verify if default file was created
            assert os.path.exists("output.csv")
            
            with open("output.csv", 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                assert len(rows) == 1
        finally:
            if os.path.exists("output.csv"):
                os.unlink("output.csv")
    
    @patch('pubmed_scout.export_to_csv.typer.echo')
    def test_export_empty_articles(self, mock_echo):
        """Test export with empty articles list."""
        article_to_csv([], "test.csv")
        
        mock_echo.assert_called_with("No articles to export.")