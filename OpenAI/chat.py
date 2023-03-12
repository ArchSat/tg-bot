import os

import openai
from aiogram.types import Message

from OpenAI.assistant import OpenAIAssistant

openai.api_key = os.environ['OPEN_AI_API_KEY']


def create_text_from_promt(messages):
    completion = openai.ChatCompletion.acreate(model="gpt-3.5-turbo",
                                               messages=messages,
                                               max_tokens=1024,
                                               stream=True
                                               )

    return completion


