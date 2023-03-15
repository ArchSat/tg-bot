import os
from wsgiref import headers

from aiogram.types import Message

# import replicate
import requests
import io
from PIL import Image


class StableDiffusionAssistant:
    def __init__(self):
        # self.model = replicate.models.get("stability-ai/stable-diffusion")
        # self.version = self.model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
        self.API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        self.headers = {"Authorization": f"Bearer {os.environ['huggingface_api_token']}"}

    # def create_image_from_message(self, message: Message, settings):
    # inputs = {
    #     'prompt': message.text,
    #     'image_dimensions': settings['image_dimensions'],
    #     'num_outputs': settings['num_outputs'],
    #     'num_inference_steps': settings['num_inference_steps'],
    #     'guidance_scale': settings['guidance_scale'],
    #     'scheduler': settings['scheduler'],
    # 'negative_prompt': settings['negative_prompt'],
    # 'seed': settings['seed'],
    # }
    # if not inputs['seed']:
    #     inputs.pop('seed')
    # if not inputs['negative_prompt']:
    #     inputs.pop('negative_prompt')
    # return self.version.predict(**inputs)

    def create_image_from_message(self, message: Message, settings):
        payload = {
            "inputs": f"{message.text}",
            "parameters": {
                "num_inference_steps": settings['num_inference_steps'],
                "guidance_scale": settings['guidance_scale'],
                "height": settings['image_dimensions'].split('x')[0],
                "width": settings['image_dimensions'].split('x')[1],
            }
        }
        response = requests.post(self.API_URL, headers=headers, json=payload)
        image = Image.open(io.BytesIO(response.content))
        return image


