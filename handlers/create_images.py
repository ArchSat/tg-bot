import asyncio
import io

import aiogram
from PIL import Image
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Text, Command
from aiogram.types import Message, BufferedInputFile

from StableDiffusion.assistant import StableDiffusionAssistant
from database.quick_commands import select_user_pictures_settings
from filters.chat_type import ChatTypeFilter

router = Router()

stable_diffusion = StableDiffusionAssistant()


@router.message(Command(commands=['image']), ChatTypeFilter('private'))
@router.message(Text(contains='нарисуй', ignore_case=True), ChatTypeFilter('private'))
async def images_handler(message: Message):
    await aiogram.methods.send_chat_action.SendChatAction(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    user_chat_settings = select_user_pictures_settings(message.from_user.id)
    result = await asyncio.get_event_loop().run_in_executor(None, stable_diffusion.create_image_from_message,
                                                            message, user_chat_settings)
    if result.status_code != 200:
        return await message.answer(f'При обращении к Stable Diffusion произошла ошибка: {result.text}')
    else:
        temp_image = io.BytesIO()
        image = Image.open(io.BytesIO(result.content))
        temp_image.name = 'image.jpeg'
        image.save(temp_image, 'png')
        temp_image.seek(0)
        return await message.answer_photo(photo=BufferedInputFile(file=temp_image.getvalue(), filename='SD21.png'))
