import logging

import pytest

from stable_discord import utils


def test_base_setup_logger():
    logger = utils.setup_logger()
    assert isinstance(logger, logging.Logger)


def test_setup_logger_null_input():
    with pytest.warns(match="Empty log_dir set in config.toml so defaulting to logs/ as logs_dir."):
        logger = utils.setup_logger("")
    assert isinstance(logger, logging.Logger)
