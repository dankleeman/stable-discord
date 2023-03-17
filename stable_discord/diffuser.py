import logging
import random

import torch
from diffusers import StableDiffusionPipeline

logger = logging.getLogger(__name__)


class Diffuser:  # pylint: disable=too-few-public-methods
    """
    A container to encapsulate

    Args:
        model_name (str): The huggingface model name to use for image generation.
    """

    def __init__(self, model_name: str = "stabilityai/stable-diffusion-2-1") -> None:
        logger.debug("CUDA is available: %s", torch.cuda.is_available())
        self.cuda_is_available = torch.cuda.is_available()
        self.pipeline = StableDiffusionPipeline.from_pretrained(model_name)
        self.pipeline.to("cuda")

    def make_image(self, prompt: str, cfg: float, steps: int) -> str:
        """Call the huggingface pipeline with several arguments and save the resulting image to disk as "img.png"

        Args:
            prompt (str): The prompt string.
            cfg (float): The float indicating the strength for "context free guidance".
            steps (int): The number of diffusion steps to perform.

        Return:
            str: The file_name string
        """

        image = self.pipeline(prompt=prompt, guidance_scale=cfg, num_inference_steps=steps).images[0]
        file_name = f"output_images/img_{random.randint(1, 10**6)}.png"
        image.save(file_name)
        return file_name
