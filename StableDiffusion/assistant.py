from aiogram.types import Message

import replicate


class StableDiffusionAssistant:
    def __init__(self):
        self.model = replicate.models.get("stability-ai/stable-diffusion")
        self.version = self.model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

    def create_image_from_message(self, message: Message, settings):
        inputs = {
            'prompt': message.text,
            'image_dimensions': settings['image_dimensions'],
            'negative_prompt': settings['negative_prompt'],
            'num_outputs': settings['num_outputs'],
            'num_inference_steps': settings['num_inference_steps'],
            'guidance_scale': settings['guidance_scale'],
            'scheduler': settings['scheduler'],
            'seed': settings['seed'],
        }
        if not inputs['seed']:
            inputs.pop('seed')
        if not inputs['negative_prompt']:
            inputs.pop('negative_prompt')
        return self.version.predict(**inputs)
