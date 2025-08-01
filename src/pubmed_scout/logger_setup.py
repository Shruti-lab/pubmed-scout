import logging
from pathlib import Path
import os


# Configure logging
def setup_logging(debug: bool = False) -> None:
    """Setup logging configuration."""
    # Get the current file's directory (src/pubmed_scout/)
    current_file_dir = Path(__file__).parent

    # Go up two levels to reach project root: src/pubmed_scout/ -> src/ -> project_root/
    project_root = current_file_dir.parent.parent

    # Create logs directory in project root
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)


    log_file = log_dir / "pubmed_scout.log"

    level = logging.DEBUG if debug else logging.INFO
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Clear any existing handlers to avoid duplicates
    logging.getLogger().handlers.clear()

    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )

    if debug:
        logging.getLogger().info(f"Debug logging enabled. Log file: {log_file}")