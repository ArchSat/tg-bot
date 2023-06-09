import asyncio
import io

import aiogram
from PIL import Image
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Text, Command
from aiogram.types import Message, BufferedInputFile

from OpenAI.assistant import OpenAIAssistant
from StableDiffusion.assistant import StableDiffusionAssistant
from database.quick_commands import select_user_pictures_settings
from filters.chat_type import ChatTypeFilter

router = Router()

stable_diffusion = StableDiffusionAssistant()

openai = OpenAIAssistant()


@router.message(Command(commands=['image']), ChatTypeFilter('private'))
@router.message(Text(contains='нарисуй', ignore_case=True), ChatTypeFilter('private'))
async def images_handler(message: Message):
    await aiogram.methods.send_chat_action.SendChatAction(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    user_chat_settings = select_user_pictures_settings(message.from_user.id)
    orig_result = await asyncio.get_event_loop().run_in_executor(None, openai.create_image_from_message,
                                                            message, user_chat_settings)
    result = orig_result.get('data', None)
    if result:
        if len(result) > 1:
            media = []
            for link in result:
                media.append(aiogram.types.input_media_photo.InputMediaPhoto(media=link['url']))
            await aiogram.methods.send_media_group.SendMediaGroup(chat_id=message.chat.id, media=media)
        else:
            await message.answer_photo(photo=result[0]['url'])
    else:
        await message.answer(f'Произошла ошибка при генерации изображения: {orig_result}')
