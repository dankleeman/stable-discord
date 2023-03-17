import logging
import os

import discord

from stable_discord.diffuser import Diffuser
from stable_discord.parser import PromptParser

logger = logging.getLogger(__name__)


# TODO: Look into unblocking some of these steps: https://stackoverflow.com/questions/65881761/discord-gateway-warning-shard-id-none-heartbeat-blocked-for-more-than-10-second
class StableDiscordBot(discord.Client):
    # TODO: Standardize emojis
    ack_emoji = "\N{THUMBS UP SIGN}"
    in_prog_emoji = "\N{STOPWATCH}"
    done_emoji = "💯"  # TODO: Pick a check mark that shows up green on discord
    prompt_parser = PromptParser()
    diffuser = Diffuser()

    def __init__(self, wake_word="/art", *, intents, **options):
        super().__init__(intents=intents, **options)
        self.wake_word = wake_word
        self.seen_channels = []

    def clean_message(self, s):
        return s.lstrip().replace(self.wake_word, "")

    async def help_response(self, message):
        await message.channel.send(self.prompt_parser.help_text)
        await message.add_reaction(self.done_emoji)

    async def process_prompt(self, message):
        logger.debug("Processing prompt")
        cleaned_message_text = self.clean_message(message.content)
        logger.info("Processing prompt '%s'", cleaned_message_text)
        known_args, unknown_args = self.prompt_parser.parse_prompt(cleaned_message_text)

        await message.channel.send(f"Parsed args: {known_args}")

        if unknown_args:
            await message.channel.send(f"Skipping unknown args: {unknown_args}")

        await message.add_reaction(self.in_prog_emoji)
        self.diffuser.make_image(**known_args)
        await message.channel.send(file=discord.File("img.png"))
        await message.add_reaction(self.done_emoji)
        # TODO: Look up how to remove reactions

    async def on_ready(self):
        # TODO: Hook into discord logging
        logger.info("Logged on as %s!", self.user)
        for guild in self.guilds:
            for channel in guild.text_channels:
                logger.info("Announcing login in channel: %s", channel)
                self.seen_channels.append(channel)
                await channel.send("I'm here!")

    async def sign_off(self):
        logger.info("Signing off.")
        for channel in self.seen_channels:
            logger.info("Signing off in channel: %s", channel)
            await channel.send("I'm done for now.")

    async def on_message(self, message):
        logger.debug("Seen message '%s' from %s", message.content, message.author)

        if message.author == self.user:
            logger.debug("Message was from this bot. Ignoring.")
            return

        if message.content.startswith(self.wake_word):
            logger.debug("Wake-word detected.")
            await message.add_reaction(self.ack_emoji)

            if "--help" in message.content:
                await self.help_response(message)
                return

            await self.process_prompt(message)


# TODO: Fold this into the bot class
def launch_bot(bot_client):
    intents = discord.Intents(value=68608)
    intents.message_content = True
    intents.messages = True
    intents.guilds = True

    bot = bot_client(intents=intents)
    try:
        bot.run(os.getenv("DISCORD_TOKEN"))
    finally:
        pass
