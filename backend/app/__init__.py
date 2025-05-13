from .core.config import settings

# Initialize logging
import logging
import logging.config
from pathlib import Path

# Set up logging
log_config = Path(__file__).parent / "logging.conf"
if log_config.exists():
    logging.config.fileConfig(log_config, disable_existing_loggers=False)
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

logger = logging.getLogger(__name__)
logger.info("Initializing application...")