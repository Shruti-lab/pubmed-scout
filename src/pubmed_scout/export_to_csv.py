import csv
import typer
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def article_to_csv(articles: List[Dict[str, Any]], filename: Optional[str]) -> None:
    """
    Export a list of articles to a CSV file.

    Args:
        articles (List[Dict[str, Any]]): A list of dictionaries containing article details.
        filename (Optional[str]): The name of the output CSV file. If empty/None, defaults to 'output.csv'.
    
    Raises:
        SystemExit: If there's an error writing to the file.
    """
    if not articles:
        logger.info("No articles provided for export")
        typer.echo("No articles to export.")
        return
    
    # Get the current file's directory (src/pubmed_scout/)
    current_file_dir = Path(__file__).parent
    
    # Go up two levels to reach project root: src/pubmed_scout/ -> src/ -> project_root/
    project_root = current_file_dir.parent.parent

    output_dir = project_root / "pubmed_scout_output"
    output_dir.mkdir(exist_ok=True)


    # Determine output filename 
    output_filename = filename if filename and filename.strip() else "output.csv"
    

    try:
        # Create directory if it doesn't exist
        output_path = output_dir / output_filename

        logger.debug(f"Writing {len(articles)} articles to {output_filename}")

        with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = articles[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(articles)  # Write the data rows

        logger.info(f"Successfully exported {len(articles)} articles to {output_filename}")
        typer.echo(f"Exported {len(articles)} articles to {output_filename}.")
    
    except PermissionError as e:
        logger.error(f"Permission denied writing to {output_filename}: {e}")
        typer.echo(f"Permission denied: Cannot write to {output_filename}")
        raise typer.Exit(1)
    except OSError as e:
        logger.error(f"OS error writing to {output_filename}: {e}")
        typer.echo(f"Error writing file {output_filename}: {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during CSV export: {e}")
        typer.echo(f"Unexpected error during export: {e}")
        raise typer.Exit(1)

