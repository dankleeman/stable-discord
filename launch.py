import argparse
import os

from stable_discord import bot, utils

logger = utils.setup_logger()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--logging-level", dest="logging_level", default="INFO")
    args = vars(parser.parse_args())
    logger.setLevel(args.pop("logging_level"))

    bot_client = bot.StableDiscordBot()
    bot_client.run(os.getenv("DISCORD_TOKEN"))
