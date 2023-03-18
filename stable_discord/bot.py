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
    wake_word: str
    prompt_parser: PromptParser
    diffuser: Diffuser
    discord_token: str
    allowed_channels: set[discord.TextChannel]
    config_settings: dict
    allowed_users: set[str]
    disallowed_users: set[str]

    def __init__(self, wake_word: str = "/art"):
        intents = discord.Intents(value=68608)
        intents.message_content = True
        intents.messages = True
        intents.guilds = True

        super().__init__(intents=intents)
        self.wake_word = wake_word
        self.config_settings = config["discord"]["settings"]
        self.allowed_users = self.config_settings['listen_users']
        self.disallowed_users = self.config_settings['ignore_users']
        
        logger.info("Allowed users: %s", self.allowed_users)
        logger.info("Disallowed users: %s", self.disallowed_users)

        self.seen_channels = []
        self.prompt_parser = PromptParser()
        self.diffuser = Diffuser()

    def set_allowed_channels(self):
        """Look through the channels available to the bot and apply rules from the config file to decide which
        channels to take input from.

        1. If "listen_channels" has values then set the allowed_channels to be a set of those channel objects
        2. If "listen_channels" is not present and "ignore_channels" is then set the allowed_channels to be a set of
            available channels not in the "ignore_channels" list.
        3. Otherwise, allowed_channels is set to be a set of all seen channels.
        """
        channels_dict = {
            f"{guild.name}:{channel.name}": channel for guild in self.guilds for channel in guild.text_channels
        }

        if self.config_settings["listen_channels"]:
            self.allowed_channels = {
                channels_dict[key] for key in channels_dict if key in self.config_settings["listen_channels"]
            }
        elif self.config_settings["ignore_channels"]:
            self.allowed_channels = {
                channels_dict[key] for key in channels_dict if key not in self.config_settings["ignore_channels"]
            }
        else:
            self.allowed_channels = set(channels_dict.values())

    async def on_ready(self) -> None:
        """An event-driven function that runs when the bot is first initialized."""
        logger.info("Logged on as %s!", self.user)
        self.set_allowed_channels()
        for channel in self.allowed_channels:
            logger.info("Announcing login in server:channel - '%s:%s'", channel.guild.name, channel)
            await channel.send("I'm here!")

    def clean_message(self, user_input: str) -> str:
        """A short helper function that cleans a user message. Here, clean means removing the "wake word" and stripping
            away leading whitespace.

        Args:
            user_input: The raw user message.

        Returns:
            str: The cleaned user message.
        """
        return user_input.replace(self.wake_word, "").lstrip()

    async def help_response(self, message: discord.Message) -> None:
        """A short helper function to handle responding to a user that asked for help.

        Args:
            message (discord.Message): The user message object.

        """
        await message.reply(self.prompt_parser.help_text)
        await message.add_reaction(self.done_emoji)

    async def handle_user_input(self, message: discord.Message) -> None:
        """A function that handles passing a user message to the parser and then to the diffuser.

        Args:
            message (discord.Message): The user message object.
        """
        logger.debug("Processing prompt")
        cleaned_message_text = self.clean_message(message.content)

        logger.info("Processing prompt '%s' from %s", cleaned_message_text, message.author)
        try:
            known_args, unknown_args = self.prompt_parser.parse_input(cleaned_message_text)
        except ValueError as e:
            if e.args[0] == 'No closing quotation':
                await message.reply("Prompt has open quotation with no closing quotation. Please fix and try again.")
            else:
                await message.reply("Prompt has unspecified syntax error. Please fix and try again.")
            return
        except SystemExit as e:
            if e.args[0] == 2:
                await message.reply("Prompt has invalid integer input on integer argument. Please fix and try again.")
            else:
                await message.reply("Prompt has unspecified syntax error. Please fix and try again.")
            return

        if unknown_args:
            await message.reply(f"Skipping unknown args: {unknown_args}")

        if not known_args["prompt"]:
            await message.reply("Skipping request with empty prompt.")

        await message.add_reaction(self.in_prog_emoji)
        file_name = self.diffuser.make_image(**known_args)
        logger.info("for prompt: %s, generated_image: %s", known_args, file_name)
        await message.reply(file=discord.File(file_name), content=f"Parsed args: {known_args}")
        await message.remove_reaction(self.in_prog_emoji, self.user)
        await message.add_reaction(self.done_emoji)

    def user_is_allowed(self, user: discord.User) -> bool:
        """Decide if the given user should be allowed to send input to the diffuser.

        In all cases the bot itself is not allowed.
        1. If allowed_users has values then the user is allowed if their "name#id" string is in allowed_users
        2. If allowed_users is empty and disallowed_users has values then the user is allowed if their "name#id" is not
            in the disallowed_users.
        3. Otherwise, the user is allowed.

        Args:
            user (discord.User): The user to be checked for is_allowed status.

        Returns:
            bool: Whether the user is allowed to send input to the diffuser.
        """
        if self.allowed_users:
            return f'{user.name}#{user.discriminator}' in self.allowed_users and user != self.user

        if self.disallowed_users:
            return f'{user.name}#{user.discriminator}' not in self.disallowed_users and user != self.user

        return user != self.user

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
            message.content.startswith(self.wake_word)
            and message.channel in self.allowed_channels
            and self.user_is_allowed(message.author)
        ):
            logger.debug("Wake-word detected in message on allowed channel.")
            await message.add_reaction(self.ack_emoji)

            if "--help" in message.content:
                await self.help_response(message)
                return

            await self.handle_user_input(message)
