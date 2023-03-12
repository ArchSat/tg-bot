import asyncio

import aiogram
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Text, Command
from aiogram.types import Message

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
    if len(result) > 1:
        media = []
        for link in result:
            media.append(aiogram.types.input_media_photo.InputMediaPhoto(media=link))
        await aiogram.methods.send_media_group.SendMediaGroup(chat_id=message.chat.id, media=media)
    else:
        await message.answer_photo(photo=result[0])
