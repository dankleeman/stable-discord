# Stable Discord
Stable Discord is a python library for running Stable Diffusion models using a Discord bot as a front end. This allows users to utilize their consumer GPUs to have a collaborative generative AI experience that they can share with their friends or run with their own custom checkpoints from the Stable Diffusion community.

## Installation
Stable Discord uses poetry to manage dependencies and installation. 

### Linux / MacOS
A user may run the following steps manually or if they have `make` installed they may run `make setup`.

	python3 -m pip install poetry
	poetry install

### Windows
A user may run the following steps manually or if they have `make` installed they may run `make setup.windows`.

	poetry install
	poetry run pip install torch==1.13.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html

## Setting Up Discord
The discord functionality for this project makes heavy use of `discord.py`: https://discordpy.readthedocs.io/en/stable/

Follow the steps recommended by discord.py to create a Bot Account and retrieve a Discord API token: https://discordpy.readthedocs.io/en/stable/discord.html

When at the "Inviting Your Bot" step and selecting permissions the minimum permissions that your bot will need are as follows.

**General Permissions:**
- Read Messages/View Channels

**Text Permissions**
- Send Messages
- Read Message History
- Add Reactions
- Attach Files
## Configuration with config.toml
Stable Discord is intended to require only changes to the single `config.toml` for the vast majority of users. Further, the defaults are such that most users should only have to add their discord token to the `discord_token` entry.

While the config file also has comments, we describe each section and the options therein in detail here.

**Note:** Keep in mind that Stable Discord reads the configuration file at startup. For any changes to be reflected, the program needs to be restarted.
### \[auth\]
- `discord_token`

### \[discord.settings\]
One of the key features of the bot is to be able to control where it is listening and two whom it is listening. Because this bot is running on hardware the user controls, if the user cannot limit who the bot acknowledges, then a user is susceptible to spam or other types of griefing.

By default the bot listens on all channels to which it is invited and to messages from all users other than itself.

If neither of the channel level settings are set, the bot will listen on all channels to which it is invited.
- `listen_channels` - A list of channels that the bot listens to. Specify in case-sensitive `[server:channel, server:channel]` format. Defaults to empty.
- `ignore_channels`  A list of channels that the bot ignores. Specify in case-sensitive `[server:channel, server:channel]` format. Defaults to empty.

If neither are set, the bot will listen to all members, but never itself.
- `listen_users` - A list of users to which the bot listens and responds. Specify in case-sensitive `[username#id, username#id]` format. Defaults to empty.
- `ignore_users` - A list of users that the bot ignores. Specify in case-sensitive `[username#id, username#id]` format. Defaults to empty.

- `wake_word` - The string that a message must start with to invoke the bot to generate art.
### \[discord.style\]
The following settings are small quality-of-life improvements so that users get some kind of feedback about what the bot is doing. This way users can tell if the bot missed their message for some reason and may need to be added to the `listen_users` list or of the bot is still just busy, for example.
- `ack_emoji` - The emoji reaction the bot uses to indicate that it has noticed a user's message. Defaults to 👍.
- `in_prog_emoji` - The emoji reaction the bot uses to indicate that it is currently working on a user's request. Defaults to ⏱️.
- `done_emoji` - he emoji reaction the bot uses to indicate that it has completed a user's request. Defaults to 💯.
### \[diffuser.settings\]
- `use_gpu` - A boolean flag indicating if the diffusion model should expect to use a GPU for accelerated processing. Defaults to `True`.
- `use_half_precision` - A boolean flag indicating if the diffusion model should use half precision floating point numbers. This will improve speed while reducing image quality. Defaults to `True`.
- `enable_xformers_attention` - A boolean flag indicating if the diffusion model should use the [xFormers](https://github.com/facebookresearch/xformers) library for accelerated attention. Defaults to `True`.
### \[misc_settings\]
- `log_dir`  - A path to the desired logging directory. Defaults to `logs`

## Execution
Stable Discord may be started by running the following in the root directory of the repository:
`poetry run python launch.py`

## Message Parameters
To give a command to the bot a user begins their message with the `wake_word` which defaults to `/art`. Text after that is interpreted as the prompt, except for some special cases where the user can add parameters.

- `--cfg 7.5` - Adding `--cfg` to the prompt followed by a number alters the CFG parameter passed to the diffusion model. If not specified, this value defaults to 7.5.
- `--steps 50` Adding `--steps` followed by an integer influences the number of diffusion steps the model takes. If not specified this value defaults to 50.
# Example Behavior

## Changelog
See `CHANGELOG.md` file in the root directory of this repository. 
## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
See the `LICENSE` file in the root directory of this repository. 
## Notes
### Conventions
README - https://www.makeareadme.com/
Semantic Versioning - https://semver.org/
Conventional Commits - https://www.conventionalcommits.org/en/v1.0.0/

### Other References
This program uses emojis that can be referenced here: https://unicode.org/emoji/charts/full-emoji-list.html
Licensing for Open Source: https://choosealicense.com/
