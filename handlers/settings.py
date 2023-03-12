from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.types import Message

from config.default_settings import default_chatgpt_settings, default_stable_diffusion_settings
from database.quick_commands import select_user_chat_settings,\
    select_user_pictures_settings, update_user_chat_settings, is_registered

router = Router()


def get_settings_text(user_id):
    user_custom_settings = is_registered(user_id)
    pictures_settings = default_stable_diffusion_settings.copy()
    chat_settings = default_chatgpt_settings.copy()
    if user_custom_settings:
        user_pictures_settings = select_user_pictures_settings(user_id)
        user_chat_settings = select_user_chat_settings(user_id)
        pictures_settings.update(user_pictures_settings)
        chat_settings.update(user_chat_settings)

    text = f"""\n
    Настройки текста:\n
    Максимальная длина запоминаемых сообщений: {chat_settings['max_memory_messages']}\n
    Максимальное число токенов в ответе: {chat_settings['max_tokens']}\n
    Температура: {chat_settings['temperature']}\n
    \n
    Настройки изображений:\n
    Разрешение изображений: {pictures_settings['image_dimensions']}\n
    Количество сообщений на запрос: {pictures_settings['num_outputs']}\n
    Количество шагов вывода: {pictures_settings['num_inference_steps']}\n
    guidance_scale: {pictures_settings['guidance_scale']}\n
    scheduler: {pictures_settings['scheduler']}\n"""
    return text


def get_settings_buttons():
    kb = [
        [types.InlineKeyboardButton(text="Редактировать настройки текста", callback_data="edit_text_settings")],
        [types.InlineKeyboardButton(text="Редактировать настройки изображений", callback_data="edit_image_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def get_text_settings_buttons():
    kb = [
        [types.InlineKeyboardButton(text="max_memory_messages", callback_data="edit_max_memory_messages")],
        [types.InlineKeyboardButton(text="max_tokens", callback_data="edit_max_tokens")],
        [types.InlineKeyboardButton(text="temperature", callback_data="edit_temperature")],
        [types.InlineKeyboardButton(text="back", callback_data="settings_main")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.message(Command(commands=["settings"]))
async def cmd_settings(message: Message):
    text = get_settings_text(message.from_user.id)
    await message.answer(text, reply_markup=get_settings_buttons())


@router.callback_query(Text("settings_main"))
async def btn_settings(callback: types.CallbackQuery):
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_settings_buttons())


@router.callback_query(Text("edit_text_settings"))
async def btn_settings(callback: types.CallbackQuery):
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons())


def get_edit_max_memory_messages_btns():
    kb = [
        [types.InlineKeyboardButton(text="5", callback_data=f"set_max_memory_5")],
        [types.InlineKeyboardButton(text="10", callback_data="set_max_memory_10")],
        [types.InlineKeyboardButton(text="15", callback_data="set_max_memory_15")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_text_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_max_memory_messages"))
async def edit_max_memory_messages(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_max_memory_messages_btns())


@router.callback_query(Text(startswith="set_max_memory_"))
async def set_max_memory_messages(callback: types.CallbackQuery):
    value = int(callback.data.replace('set_max_memory_', ''))
    update_user_chat_settings(user_id=callback.from_user.id, setting_name='max_memory_messages', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons())


def get_edit_max_tokens_btns():
    kb = [
        [types.InlineKeyboardButton(text="256", callback_data=f"set_max_tokens_256")],
        [types.InlineKeyboardButton(text="512", callback_data=f"set_max_tokens_512")],
        [types.InlineKeyboardButton(text="1024", callback_data="set_max_tokens_1024")],
        [types.InlineKeyboardButton(text="2048", callback_data="set_max_tokens_2048")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_text_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_max_tokens"))
async def edit_max_tokens(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_max_tokens_btns())


@router.callback_query(Text(startswith="set_max_tokens_"))
async def set_max_tokens(callback: types.CallbackQuery):
    value = int(callback.data.replace('set_max_tokens_', ''))
    update_user_chat_settings(user_id=callback.from_user.id, setting_name='max_tokens', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons())


def get_edit_temperature_btns():
    kb = [
        [types.InlineKeyboardButton(text="0.5", callback_data=f"set_temperature_0.5")],
        [types.InlineKeyboardButton(text="1", callback_data=f"set_temperature_1.0")],
        [types.InlineKeyboardButton(text="1.5", callback_data="set_temperature_1.5")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_text_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_temperature"))
async def edit_max_tokens(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_temperature_btns())


@router.callback_query(Text(startswith="set_temperature_"))
async def set_max_tokens(callback: types.CallbackQuery):
    value = float(callback.data.replace('set_temperature_', ''))
    update_user_chat_settings(user_id=callback.from_user.id, setting_name='temperature', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons())


@router.callback_query(Text("edit_image_settings"))
async def edit_max_tokens(callback: types.CallbackQuery):
    await callback.message.answer('Временно не реализовано')
