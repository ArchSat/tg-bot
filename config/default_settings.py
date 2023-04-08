
default_chatgpt_settings = {
    'max_memory_messages': 10,
    'max_tokens': 1024,
    'temperature': 1
}


default_delle_settings = {
    'image_dimensions': '512x512',
    'num_outputs': 1,
}

default_stable_diffusion_settings = {
    'image_dimensions': '768x768',
    # 'num_outputs': 1,
    'num_inference_steps': 100,
    'guidance_scale': 7.5,
    # 'scheduler': 'DPMSolverMultistep',
    # 'negative_prompt': None,
    # 'seed': None
}
