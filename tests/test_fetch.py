import pytest
import requests
from unittest.mock import patch, Mock
from xml.etree import ElementTree as ET
from pubmed_scout.fetch import search_pubmed_IDs, fetch_article_details
import typer

class TestSearchPubmedIDs:
    """Test cases for search_pubmed_IDs function."""
    
    @patch('pubmed_scout.fetch.requests.get')
    def test_search_success(self, mock_get):
        """Test successful search returns correct PMIDs."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "esearchresult": {
                "idlist": ["40741195","40741182"],
                "count": "2"
            }
        }
        mock_get.return_value = mock_response
        
        result = search_pubmed_IDs("cancer", retmax=5)

        assert result == ["40741195", "40741182"]
        mock_get.assert_called_once()
    
    @patch('pubmed_scout.fetch.requests.get')
    def test_search_empty_results(self, mock_get):
        """Test search with no results."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "esearchresult": {
                "idlist": [],
                "count": "0"
            }
        }
        mock_get.return_value = mock_response
        
        result = search_pubmed_IDs("nonexistent_query")
        
        assert result == []
    
    def test_search_empty_query(self):
        """Test search with empty query raises Exit."""
        with pytest.raises(SystemExit) as e:  # typer.Exit raises SystemExit
            search_pubmed_IDs("")
        assert e.value.code == 1
    
    @patch('pubmed_scout.fetch.requests.get')
    @patch('pubmed_scout.fetch.typer.Exit')
    def test_search_api_failure(self, mock_exit, mock_get):
        """Test API failure handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_get.return_value = mock_response

        with pytest.raises(typer.Exit) as e:
            search_pubmed_IDs("cancer")

        print(f"----------------------------------------------{e.type}-----------------------------------")
        assert e.value.code == 1


class TestFetchArticleDetails:
    """Test cases for fetch_article_details function."""
    
    @patch('pubmed_scout.fetch.requests.get')
    def test_fetch_success(self, mock_get):
        """Test successful article fetch."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<PubmedArticleSet><PubmedArticle></PubmedArticle></PubmedArticleSet>'
        mock_get.return_value = mock_response
        
        result = fetch_article_details(["40741182"])
        
        assert isinstance(result, ET.Element)
        assert result.tag == "PubmedArticleSet"
    

    @patch('pubmed_scout.fetch.typer.Exit')
    def test_fetch_empty_pmid_list(self):
        """Test fetch with empty PMID list."""
        with pytest.raises(SystemExit) as e:
            fetch_article_details([])
        assert e.value.code == 1

    def test_fetch_invalid_pmids(self):
        """Test fetch with invalid PMIDs."""
        with pytest.raises(SystemExit) as e:
            fetch_article_details(["invalid", "not_a_number"])
        assert e.value.code == 1

    @patch('pubmed_scout.fetch.requests.get')
    @patch('pubmed_scout.fetch.typer.Exit')
    def test_fetch_api_failure(self, mock_exit, mock_get):
        """Test API failure handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with pytest.raises(SystemExit) as e:
            fetch_article_details(["40741182"])

        assert e.value.code == 1