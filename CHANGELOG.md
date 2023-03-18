# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - '???'
### Added
    - Added discord.settings and diffuser.settings to config file so that the user can influence bot and diffuser behavior without editing code
    - Added listen_channels and ignore_channels lists to config file so bot can be configured to only respond on a subset of available channels
    - Added use_gpu, use_half_precision, and enable_xformers_attention to config file
    - Added check to have the bot ignore empty prompts.
### Changed
    - Changed bot messaging so that it replies to users messages for increased clarity
    - Downgraded pytorch dependency from 2.0.0 to 1.3.0 to allow xformers compatibility
## [0.4.0] - '2023-03-18'
### Added
    - Added output_images directory.
    - Added random nonce to file names to avoid collisions on async requests for saving vs sending an image.
    - Updated bot response to send prompt text and image at the same time.
    - Added more tests covering error-causing user inputs.
## [0.3.0] - '2023-03-17'
### Added
    - Unit tests for the parser module.
    - Unit tests to the CI pipeline.
    - Lint checks passing.
    - Lint checks to the CI pipeline.
    - Added config.toml for human-friendly updating of settings.
### Fixed
    - A bug where a user prompt including a single quote broke the argument parser as it expected a close quote.
## [0.2.0] - '2023-03-17'
### Added 
    - Diffuser class to allow image generation based on prompts
    - Passing CFG and steps arguments to diffuser to allow some user control over output
    - Set torch precision to 16bit from 32bit to allow for more efficient testing on a local machine
    - Turned on sliced attention to allow for more efficient testing
## [0.1.0] - '2023-03-16'
### Added
    - This changelog, MIT License, and project scaffolding like Makefile, pyproject.toml, setup.cfg
    - Bot module to capture all functionality pertaining to interacting with discord.
    - First draft prototype for discord bot including emoji reactions, image messages, and help text.
    - Parser module to capture all functionality pertaining to parsing prompt text for arguments.
    - First draft prototype for parser class based on argparse to handle arbitray input prompts.
    - Diffuser module as empty placeholder to capture all functionality pertaining to diffusion models.
    - Support for time-based rotating logs.
    - Detailed debug logs covering the bot module.
    - Github action to run format checks on every change to main.
