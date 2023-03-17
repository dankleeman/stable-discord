import logging

import discord

from stable_discord.config import config
from stable_discord.diffuser import Diffuser
from stable_discord.parser import PromptParser

logger = logging.getLogger(__name__)


class StableDiscordBot(discord.Client):
    """A class that handles interacting with the users on discord and coordinating between the different parts
    of the stable-discord system"""

    ack_emoji: str = "\N{THUMBS UP SIGN}"
    in_prog_emoji: str = "\N{STOPWATCH}"
    done_emoji: str = "💯"
    prompt_parser: PromptParser
    diffuser: Diffuser
    discord_token: str
    allowed_channels: set[discord.TextChannel]

    def __init__(self, wake_word: str = "/art"):
        intents = discord.Intents(value=68608)
        intents.message_content = True
        intents.messages = True
        intents.guilds = True

        super().__init__(intents=intents)
        self.wake_word = wake_word
        self.seen_channels = []
        self.prompt_parser = PromptParser()
        # self.diffuser = Diffuser()

    def clean_message(self, user_input: str) -> str:
        """A short helper function that cleans a user message. Here, clean means removing the "wake word" and stripping
            away leading whitespace.

        Args:
            user_input: The raw user message.

        Returns:
            str: The cleaned user message.
        """
        return user_input.lstrip().replace(self.wake_word, "")

    async def help_response(self, message: discord.Message) -> None:
        """A short helper function to handle responding to a user that asked for help.

        Args:
            message (discord.Message): The user message object.

        """
        await message.channel.send(self.prompt_parser.help_text)
        await message.add_reaction(self.done_emoji)

    async def process_prompt(self, message: discord.Message) -> None:
        """A function that handles passing a user message to the parser and then to the diffuser.

        Args:
            message (discord.Message): The user message object.
        """
        logger.debug("Processing prompt")
        cleaned_message_text = self.clean_message(message.content)
        logger.info("Processing prompt '%s'", cleaned_message_text)
        known_args, unknown_args = self.prompt_parser.parse_input(cleaned_message_text)

        if unknown_args:
            await message.channel.send(f"Skipping unknown args: {unknown_args}")

        await message.add_reaction(self.in_prog_emoji)
        file_name = self.diffuser.make_image(**known_args)
        await message.channel.send(file=discord.File(file_name), content=f"Parsed args: {known_args}")
        await message.add_reaction(self.done_emoji)

    async def on_ready(self) -> None:
        """An event-driven function that runs when the bot is first initialized."""
        logger.info("Logged on as %s!", self.user)
        self.set_allowed_channels()
        for channel in self.allowed_channels:
            logger.info("Announcing login in server:channel - '%s:%s'", channel.guild.name, channel)
            await channel.send("I'm here!")

    def set_allowed_channels(self):
        channels_dict = {
            f"{guild.name}:{channel.name}": channel for guild in self.guilds for channel in guild.text_channels
        }

        if config["discord_settings"]["listen_channels"]:
            self.allowed_channels = {
                channels_dict[key] for key in channels_dict if key in config["discord_settings"]["listen_channels"]
            }
        elif config["discord_settings"]["ignore_channels"]:
            self.allowed_channels = {
                channels_dict[key] for key in channels_dict if key not in config["discord_settings"]["ignore_channels"]
            }
        else:
            self.allowed_channels = set(channels_dict.values())

    async def on_message(self, message: discord.Message) -> None:
        """An event-driven function that runs whenever the bot sees a message on a channel it is in.

        Args:
            message (discord.Message): The user message object.
        """
        logger.debug(
            "Seen message '%s' from %s on %s channel on %s server",
            message.content,
            message.author,
            message.channel,
            message.channel.guild,
        )

        if (
            message.channel in self.allowed_channels
            and message.author != self.user
            and message.content.startswith(self.wake_word)
        ):
            logger.debug("Wake-word detected in message on allowed channel.")
            await message.add_reaction(self.ack_emoji)

            if "--help" in message.content:
                await self.help_response(message)
                return

            await self.process_prompt(message)
