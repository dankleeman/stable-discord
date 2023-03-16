from diffusers import StableDiffusionPipeline
import torch
import logging

logger = logging.getLogger(__name__)
class Diffuser:
    def __init__(self, model_name = "stabilityai/stable-diffusion-2-1"):
        logger.debug('CUDA is available: %s', torch.cuda.is_available())
        self.cuda_is_available = torch.cuda.is_available()
        self.pipeline = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
        self.pipeline.enable_attention_slicing()
        self.pipeline.to("cuda")

    def make_image(self, prompt, cfg, steps):
        image = self.pipeline(prompt=prompt, guidance_scale=cfg, num_inference_steps=steps).images[0]
        image.save('img.png')
