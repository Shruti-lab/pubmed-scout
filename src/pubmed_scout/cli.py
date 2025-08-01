import typer
from typing import List, Optional
from typing_extensions import Annotated
from .fetch import search_pubmed_IDs, fetch_article_details
from .parse import parse_fetch_response
from .export_to_csv import article_to_csv
import logging
from .logger_setup import setup_logging

logger = logging.getLogger(__name__)

app = typer.Typer()

@app.command()
def get_papers(query: str,
               retmax: Annotated[int, typer.Option(help="Maximum number of results to return")] = 5,
               filename: Annotated[str, typer.Option( "--filename", "-f", help="Provide filename or default is output.csv")]="",
               debug: Optional[bool] = typer.Option(False, "--debug", "-d", help="Enable debug mode for detailed output"),
               ) -> None:
    """
    Search PubMed with the given query and export results to CSV.
    
    Args:
        query (str): The PubMed search query.
        retmax (int): Maximum number of results to return.
        filename (str): Output CSV filename. Defaults to 'output.csv' if empty.
        debug (bool): Enable debug logging.
    Returns:
        None: The function prints results to console or exports to CSV.

    Outputs:
        Files are saved to ./pubmed_scout_output/ directory by default.
        Logs are saved to ./logs/ directory by default.
    """
    

    # Setup logging based on debug flag
    setup_logging(debug)

    logger.info(f"Starting PubMed Scout with query: '{query}', retmax: {retmax}")
    typer.echo(f"Running PubMed Scout with query: {query}")


    if debug:
        logger.debug("Debug mode enabled")
        typer.echo("[DEBUG] Debug mode enabled - check pubmed_scout.log for detailed logs")
    
    try:
        # Step 1: Search for PMIDs
        logger.debug("Step 1: Searching for PMIDs")
        search_results = search_pubmed_IDs(query,retmax=retmax)
        
        if not search_results:
            logger.warning("No search results found")
            typer.echo("No results found for the given query.")
            return
        
        logger.info(f"Found {len(search_results)} PMIDs")
        typer.echo(f"Found {len(search_results)} results for query '{query}'.")

        
        # Step 2: Fetch article details
        logger.debug("Step 2: Fetching article details")
        typer.echo("Fetching article details...")
        root = fetch_article_details(search_results)

        # Step 3: Parse response
        logger.debug("Step 3: Parsing article details")
        articles = parse_fetch_response(root)

        if not articles:
            logger.warning("No articles parsed from response")
            typer.echo("No articles could be parsed from the response.")
            return

        # Step 4: Display or export results
        if not filename or filename.strip() == "":
            logger.debug("No filename provided, displaying results to console")
            for article in articles:
                typer.echo(f"PubmedID: {article['PubmedID']}")
                typer.echo(f"Title: {article['Title']}")
                typer.echo(f"Publication Date: {article['Publication Date']}")
                typer.echo(f"Non-Academic Authors: {article['Non-Academic Authors']}")
                typer.echo(f"Company Affiliations: {article['Company Affiliations']}")
                typer.echo(f"Corresponding Author Email: {article['Corresponding Author Email']}")
                typer.echo("-" * 50)

        # Step 5: Export to CSV. If no filename is provided it is by default saved to output.csv for ease to extract than just console output.
        logger.debug("Step 5: Exporting to CSV")
        article_to_csv(articles, filename)

        logger.info("PubMed Scout execution completed successfully!!!!!!!!!!!!!!!!!!")
        
    except typer.Exit:
        # Re-raise typer exits
        raise
    except Exception as e:
        logger.error(f"Unexpected error during execution: {e}")
        typer.echo(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main entry point for the PubMed Scout CLI.
    """
    app()


if __name__ == "__main__":
    typer.run(main)

"""
This script serves as the command-line interface for the PubMed Scout application.
It uses the Typer library to create a user-friendly CLI.
"""
