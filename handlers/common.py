import time
from traceback import print_tb

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from OpenAI.assistant import OpenAIAssistant

router = Router()

openai = OpenAIAssistant()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer(
        text="Тут обязательно что-то будет"
    )


@router.message(Command(commands=["clear_context"]))
async def cmd_start(message: Message):
    openai.clear_message_history(message.from_user.id)
    await message.answer(text="История сообщений удалена!")


@router.message()
async def message_handler(message: Message):
    completion = openai.create_completion_from_message(message)
    if not completion:
        return await message.answer('Сообщение содержит слишком много информации для обработки!')
    answer = None
    last_send = time.time()
    buffer = ''
    answer_text = ''
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
                        answer = await answer.edit_text(answer.text + buffer)
                        answer_text = answer.text
                    else:
                        answer = await message.answer(buffer)
                        answer_text += answer.text
                    last_send = time.time()
                buffer = ''

        except Exception as e:
            print_tb(e.__traceback__)
    if not answer:
        answer = await message.answer(buffer)
        answer_text += answer.text
    else:
        answer = await answer.edit_text(answer.text + buffer)
        answer_text = answer.text
    openai.put_promt_result_to_history(message.from_user.id, answer_text)
