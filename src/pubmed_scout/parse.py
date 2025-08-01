import typer
import logging
from typing import List, Dict, Any, Set, Optional
from xml.etree import ElementTree as ET
import re

logger = logging.getLogger(__name__)


# ACADEMIC_KEYWORDS = [
#     "university", "college", "hospital", "institute", "faculty", "school",
#     "center", "centre", "department", "clinic","clínic","med school"
# ]


# def is_non_academic(affiliation: str) -> bool:
#     return not any(keyword in affiliation.lower() for keyword in ACADEMIC_KEYWORDS)

COMPANY_KEYWORDS = [
    "inc", "ltd", "llc", "gmbh", "corp", "corporation", "biotech", "pharma", "therapeutics"
]

EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
)

def is_company_affiliation(affiliation: str) -> bool:
    """
    Check if an affiliation text contains company-related keywords.
    
    Args:
        affiliation (str): The affiliation text to check.
    
    Returns:
        bool: True if the affiliation contains company keywords, False otherwise.
    """
    if not affiliation:
        return False

    return any(keyword in affiliation.lower() for keyword in COMPANY_KEYWORDS)


def parse_publication_date(pub_date_element: Optional[ET.Element]) -> str:
    """
    Parse publication date from XML element.
    
    Args:
        pub_date_element (Optional[ET.Element]): The publication date XML element.
    
    Returns:
        str: Formatted publication date string.
    """
    if pub_date_element is None:
        return "No publication date available"
    
    year = pub_date_element.findtext('Year', '').strip()
    month = pub_date_element.findtext('Month', '').strip()
    day = pub_date_element.findtext('Day', '').strip()
    
    date_parts = [part for part in [year, month, day] if part]
    return ' '.join(date_parts) if date_parts else "No publication date available"



def extract_emails_from_text(text: str) -> List[str]:
    """
    Extract all email addresses from a given text.
    
    Args:
        text (str): The text to search for email addresses.
    
    Returns:
        List[str]: A list of unique email addresses found in the text.
    """
    if not text:
        return []

    emails = EMAIL_PATTERN.findall(text)
    return list(set(emails))  # Remove duplicates



def parse_fetch_response(root: ET.Element) -> List[Dict[str, Any]]:
    """
    Parse the response from the fetch function to extract relevant information.

    Args:
        root (ET.Element): The root element of the XML response from the fetch request.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing parsed article data.
    
    Raises:
        SystemExit: If root is None or parsing fails.
    """
    if root is None:
        logger.error("No data to parse - root element is None")
        typer.echo("No data to parse from the fetch response.")
        raise typer.Exit(1)


    articles: List[Dict[str, Any]] = []
    
    try:
        article_elements = root.findall(".//PubmedArticle")
        logger.debug(f"Found {len(article_elements)} articles to parse")
        
        for article in article_elements:
            try:
                pmid_element = article.find(".//PMID")
                if pmid_element is None:
                    logger.warning("Article found without PMID, skipping")
                    continue

                pmid = pmid_element.text
                if not pmid:
                    logger.warning("Empty PMID found, skipping article")
                    continue


                # Extract article information
                title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No title available"
                pub_date = article.find(".//PubDate")
                pub_date_str = parse_publication_date(pub_date)

                # Process authors and affiliations
                non_academic_authors: Set[str] = set()
                company_affiliations: Set[str] = set()
                author_emails: Set[str] = set()

                for author in article.findall(".//AuthorList/Author"):
                    first_name = author.findtext("ForeName", "").strip()
                    last_name = author.findtext("LastName", "").strip()
                    # Skip authors without last name in case
                    if not last_name:  
                            continue
                        
                    name = f"{first_name} {last_name}".strip()

                    for aff_info in author.findall(".//AffiliationInfo"):
                        aff_element = aff_info.find(".//Affiliation")
                        if aff_element is None:
                            continue
                            
                        aff_text = aff_element.text
                        if not aff_text:
                            continue
                            
                        if is_company_affiliation(aff_text):
                            non_academic_authors.add(name)
                            company_affiliations.add(aff_text.strip())
                                
                            # Extract emails from affiliation text
                            emails = extract_emails_from_text(aff_text)
                            author_emails.update(emails)

                articles.append({
                    "PubmedID":pmid,
                    "Title": title,
                    "Publication Date": pub_date_str,
                    "Non-Academic Authors": "; ".join(non_academic_authors),
                    "Company Affiliations": "; ".join(company_affiliations),
                    "Corresponding Author Email": "; ".join((author_emails)) if author_emails else "NO-EMAIL"
                })

                logger.debug(f"Successfully parsed article PMID: {pmid}")

            except Exception as e:
                logger.warning(f"Error parsing individual article: {e}")
                continue

        logger.info(f"Successfully parsed {len(articles)} articles")
        typer.echo(f"Fetched details for {len(articles)} articles.")

        return articles
        
    except Exception as e:
        logger.error(f"Critical error during parsing: {e}")
        typer.echo(f"Error parsing fetch response: {e}")
        raise typer.Exit(1)
  


