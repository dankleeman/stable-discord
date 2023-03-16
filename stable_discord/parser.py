import argparse
import logging
import shlex

logger = logging.getLogger(__name__)


class PromptParser:
    # TODO: Standardize emojis
    ack_emoji = "\N{THUMBS UP SIGN}"
    in_prog_emoji = "\N{STOPWATCH}"
    done_emoji = "✔"

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="StableDiscord", add_help=False)
        self.parser.add_argument(
            "prompt",
            nargs="*",
            help=(
                "The prompt is a positional argument meaning text not assigned to an argument is presumed to be"
                "the prompt."
            ),
        )
        self.parser.add_argument(
            "--cfg",
            type=float,
            default=7.5,
            help=(
                "A float value for the 'Context Free Guidance' parameter. Sometimes called 'style' in other models."
                " (Defaults to 7.5)"
            ),
        )
        self.parser.add_argument(
            "--steps",
            type=int,
            default=50,
            help=(
                "The number of diffusion steps. More will take longer, but usually returns better results."
                " (Defaults to 50)"
            ),
        )

    @property
    def help_text(self):
        return self.parser.format_help()

    def parse_prompt(self, prompt):
        logger.debug("Parsing args from: %s", prompt)
        known_args, unknown_args = self.parser.parse_known_args(shlex.split(prompt))
        known_args = vars(known_args)

        known_args["prompt"] = " ".join(known_args["prompt"])
        unknown_args = " ".join(unknown_args)
        logger.debug("Parsed known args: %s", known_args)
        logger.debug("Parsed unknown args: %s", unknown_args)

        return known_args, unknown_args
