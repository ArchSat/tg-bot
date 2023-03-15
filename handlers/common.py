import time
from traceback import print_tb

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message

from OpenAI.assistant import OpenAIAssistant
from database.quick_commands import select_user_chat_settings
from filters.chat_type import ChatTypeFilter

router = Router()

openai = OpenAIAssistant()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    await message.answer('Данный бот представляет собой обертку для ChatGPT\-3.5\-turbo модели.\n'
                         'Включена поддержка Stable Diffusion 2.1 по ключевому слову "нарисуй" '
                         '(или с помощью команды /image)\n'
                         'Взаимодействия с ботом будут быстрее при использовании английского языка.\n'
                         'Создание изображений занимает значительное время.\n'
                         'Для создания персональных настроек бота используйте команду /settings\n'
                         'Исходный код проекта можно найти [тут](https://github.com/ArchSat/tg\-bot)',
                         parse_mode="MarkdownV2")


@router.message(Command(commands=["clear_context"]))
async def cmd_start(message: Message):
    openai.clear_message_history(message.from_user.id)
    await message.answer(text="История сообщений удалена!")


@router.message(~Text(contains='нарисуй', ignore_case=True), ~Command(commands=['image']), ChatTypeFilter('private'))
async def message_handler(message: Message):
    user_chat_settings = select_user_chat_settings(message.from_user.id)
    completion = openai.create_completion_from_message(message, user_chat_settings)
    if not completion:
        return await message.answer('Сообщение содержит слишком много информации для обработки!')
    answer = None
    last_send = time.time()
    buffer = ''
    async for resp in await completion:
        buffer += resp['choices'][0]['delta']._previous.get('content', '')
        try:
            if not buffer:
                buffer += '\n'
                continue
            if time.time() - last_send < 1:
                continue
            else:

                if answer is None:
                    answer = await message.answer(buffer)
                    last_send = time.time()

                else:
                    if len(answer.text + buffer) < 2048:
                        try:
                            answer = await answer.edit_text(answer.text + buffer)
                        except:
                            pass
                    else:
                        answer = await message.answer(buffer)
                    last_send = time.time()
                buffer = ''

        except Exception as e:
            print_tb(e.__traceback__)
    try:
        if not answer:
            answer = await message.answer(buffer)
        else:
            answer = await answer.edit_text(answer.text + buffer)
    except:
        pass
    answer_text = answer.text
    openai.put_promt_result_to_history(message.from_user.id, answer_text)
    while openai.get_history_len(message.from_user.id) > user_chat_settings.get('max_memory_messages'):
        openai.delete_first_message_from_history(message.from_user.id)
