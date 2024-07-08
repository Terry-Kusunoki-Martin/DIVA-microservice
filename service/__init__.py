import sys
from pathlib import Path

from loguru import logger

from service.config import AppConfig

config = AppConfig()

log_path = str(Path(config.log_dir, config.application_name + ".log"))

# Log configuration
logger.remove()
if config.debug_enabled:
    logger.add(sys.stderr, level="DEBUG")
else:
    logger.add(sys.stderr, level="INFO")
    logger.add(
        log_path,
        level="INFO",
        serialize=True,
        rotation="00:00",
        retention="10 days",
        compression="zip",
    )
logger.debug(f"config = {config}")
# TODO: GPU check: availability, architecture compatibility, and available memory
