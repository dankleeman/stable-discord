import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(path="logs/stable-discord.log"):
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=logging.INFO,
        handlers=[TimedRotatingFileHandler(path, "midnight", backupCount=7), logging.StreamHandler()],
    )
    logger = logging.getLogger()

    return logger
