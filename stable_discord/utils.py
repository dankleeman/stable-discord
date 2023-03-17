import logging
from logging.handlers import TimedRotatingFileHandler

from stable_discord.config import config


def setup_logger(dir_path: str = f"{config['misc_settings']['log_dir']}/stable-discord.log") -> logging.Logger:
    """Set up the logger including the formatting and logging both to a file with rotating logs and I/O stream

    Args:
        dir_path: The file path for the logging directory

    Returns:
        logging.Logger: The logger object.
    """
    if not dir_path:
        dir_path = config.get_or()
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=logging.INFO,
        handlers=[TimedRotatingFileHandler(dir_path, "midnight", backupCount=7), logging.StreamHandler()],
    )
    logger = logging.getLogger()

    return logger
