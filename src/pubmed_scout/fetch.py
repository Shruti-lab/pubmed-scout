import requests
import typer
from .constants import BASE_URL, PUBMED_DATABASE
from typing_extensions import Annotated
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET
import logging

logger = logging.getLogger(__name__)



def search_pubmed_IDs(query: str, retmax: Optional[int] = 5) -> List[str]:
    """
    Search PubMed with the given query using Esearch. The function uses the Entrez Esearch API to find IDs (PMIDs)
    matching a query. It supports full PubMed query syntax (Boolean operators, filters, field tags)

    Args:
        query (str): The search query string.
        retmax (int): Maximum number of results to return.

    Returns:
        List[str]: A list of PubMed IDs (PMIDs).

    Raises:
        HTTPError: If the request to the PubMed API fails.
    
    This function constructs a URL for the Esearch endpoint of the PubMed API,
    sends a GET request, and parses the XML response to extract PubMed IDs.
    It supports full PubMed query syntax including Boolean operators, filters, and field tags.

    Example:
        >>> search_pubmed_IDs("cancer AND (treatment OR therapy)", retmax=10)
        ['12345678', '87654321']

    """
    if not query or not query.strip():
        logger.error("Empty or invalid query provided", stack_info=True, exc_info=True)
        typer.echo("[ERROR] Query cannot be empty.")
        raise typer.Exit(1)
    
    # check if retmax is a positive value. Also put a cap on retmax to avoid excessive requests
    if retmax and (retmax <= 0 or retmax > 10000):
        logger.warning(f"Invalid retmax value: {retmax}, using default 5", stack_info=True, exc_info=True)
        retmax = 5


    ESEARCH_URL = f"{BASE_URL}esearch.fcgi?db={PUBMED_DATABASE}&term={query}&retmax={retmax}&retmode=json"
    try:
        logger.debug(f"Making API request to: {ESEARCH_URL}")
        response = requests.get(ESEARCH_URL, timeout=30)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            search_result = data.get("esearchresult", {})
            id_list = search_result.get("idlist", [])

            logger.info(f"Search completed: found {len(id_list)} total results, returning {len(id_list)} IDs")
            typer.echo(f"Search results for query '{query}': {data.get('esearchresult', {}).get('count', 0)} results found.")

            return id_list
        else:
            typer.echo(f"Error fetching data: {response.status_code} - {response.text}")
            raise typer.Exit(1)
        # raise requests.HTTPError(f"Failed to fetch data: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        typer.echo(f"Error fetching data: {e}")
        raise typer.Exit(1)
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing API response: {e}")
        typer.echo(f"Error parsing response: {e}")
        raise typer.Exit(1)



def fetch_article_details(pmid_list: List[str]) -> ET.Element:
    """
    Fetch article details from PubMed using Efetch.

    Args:
        pmid_list (List[str]): A list of PubMed IDs (PMIDs) to fetch details for.

    Returns:
        ET.Element: The root element of the XML response containing article details.

    Raises:
        SystemExit: If the request to the PubMed API fails or PMIDs list is empty.
    
    Example:
        >>> fetch_article_details(["12345678", "87654321"])
        <Element 'PubmedArticleSet' at 0x...>
    """
    if not pmid_list or pmid_list == []:
        logger.error("No PMIDs provided for fetching article details")
        typer.echo("No PMIDs provided for fetching article details.")
        raise typer.Exit(1)
    
    # Validate PMIDs
    valid_pmids = [pmid for pmid in pmid_list if pmid and pmid.isdigit()]
    if not valid_pmids:
        logger.error("No valid PMIDs found in the provided list")
        typer.echo("No valid PMIDs found.")
        raise typer.Exit(1)
    

    if len(valid_pmids) != len(pmid_list):
        logger.warning(f"Filtered {len(pmid_list) - len(valid_pmids)} invalid PMIDs")

    EFETCH_URL = f"{BASE_URL}efetch.fcgi?db={PUBMED_DATABASE}&id={','.join(valid_pmids)}&retmode=xml"
    
    try:
        logger.debug(f"Fetching article details for {len(valid_pmids)} PMIDs")
        response = requests.get(EFETCH_URL, timeout=60)  # Longer timeout for larger requests
        response.raise_for_status()

        root = ET.fromstring(response.content)
        logger.info(f"Successfully fetched and parsed article details")
        typer.echo(f"Fetching article details for PMIDs: {', '.join(valid_pmids)}")
        
        return root

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch article details: {e}")
        typer.echo(f"Error fetching article details: {e}")
        raise typer.Exit(1)
    except ET.ParseError as e:
        logger.error(f"Error parsing XML response: {e}")
        typer.echo(f"Error parsing XML response: {e}")
        raise typer.Exit(1)





    """
        data = {                                                                                                                             │          │
│ │               │   'header': {'type': 'esearch', 'version': '0.3'},                                                                          │          │
│ │               │   'esearchresult': {                                                                                                        │          │
│ │               │   │   'count': '296300',                                                                                                    │          │
│ │               │   │   'retmax': '5',                                                                                                        │          │
│ │               │   │   'retstart': '0',                                                                                                      │          │
│ │               │   │   'idlist': ['40741195', '40741182', '40741141', '40741009', '40740944'],                                               │          │
│ │               │   │   'translationset': [                                                                                                   │          │
│ │               │   │   │   {                                                                                                                 │          │
│ │               │   │   │   │   'from': 'cancer',                                                                                             │          │
│ │               │   │   │   │   'to': '"cancer\'s"[All Fields] OR "cancerated"[All Fields] OR "canceration"[All Fields] '+188                 │          │
│ │               │   │   │   }                                                                                                                 │          │
│ │               │   │   ],                                                                                                                    │          │
│ │               │   │   'querytranslation': '("cancer s"[All Fields] OR "cancerated"[All Fields] OR "canceration"[All Fields]'+213            │          │
│ │               │   }                                                                                                                         │          │
│ │               }                                                                                                                             │          │
│ │ ESEARCH_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer'+31                                         │          │
│ │       query = 'cancer AND 2023'                                                                                                             │          │
│ │    response = <Response [200]>                                                                                                              │          │
│ │      retmax = 5                  """