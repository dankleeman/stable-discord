import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(path: str = "logs/stable-discord.log") -> logging.Logger:
    """Set up the logger including the formatting and logging both to a file with rotating logs and I/O stream

    Args:
        path: The file path for the initial logfile to be saved.

    Returns:
        logging.Logger: The logger object.
    """
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=logging.INFO,
        handlers=[TimedRotatingFileHandler(path, "midnight", backupCount=7), logging.StreamHandler()],
    )
    logger = logging.getLogger()

    return logger
