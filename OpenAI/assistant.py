import os

import openai
from aiogram.types import Message

from OpenAI.tokenizer import num_tokens_from_messages

openai.api_key = os.environ['OPEN_AI_API_KEY']


class OpenAIAssistant:
    def __init__(self):
        self.message_history = {}

    def create_completion_from_message(self, message: Message, user_chat_settings):
        user_id = message.from_user.id
        this_message = {'role': 'user', 'content': message.text}
        if user_id in self.message_history:
            self.message_history[user_id].append(this_message)
            history_size = num_tokens_from_messages(self.message_history[user_id])
            while history_size > 3072:
                self.delete_first_message_from_history(user_id)
                if self.message_history[user_id]:
                    history_size = num_tokens_from_messages(self.message_history[user_id])
                else:
                    return None
        else:
            self.message_history[user_id] = [this_message]
        completion = openai.ChatCompletion.acreate(model="gpt-3.5-turbo",
                                                   messages=self.message_history[user_id],
                                                   max_tokens=user_chat_settings['max_tokens'],
                                                   stream=True,
                                                   temperature=user_chat_settings['temperature'],
                                                   user=f"{message.from_user.id}"
                                                   )
        return completion

    def clear_message_history(self, user_id):
        self.message_history[user_id] = []

    def get_history_len(self, user_id):
        return len(self.message_history[user_id])

    def delete_first_message_from_history(self, user_id):
        if self.message_history[user_id]:
            self.message_history[user_id].pop(0)

    def put_promt_result_to_history(self, user_id, promt_result):
        self.message_history[user_id].append({'role': 'assistant', 'content': promt_result})

    @staticmethod
    def create_image_from_message(message: Message, user_picture_settings):
        image_response = openai.Image.create(
            prompt=message.text,
            n=user_picture_settings['num_outputs'],
            size=user_picture_settings['image_dimensions'],
            user=f"{message.from_user.id}"
        )
        return image_response
