import html

from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.types import Message

from config.default_settings import default_chatgpt_settings, default_stable_diffusion_settings
from database.quick_commands import select_user_chat_settings, \
    select_user_pictures_settings, update_user_chat_settings, is_registered, update_user_pictures_settings

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
    <b>Настройки текста:</b>\n
    ├ max_memory_messages: {chat_settings['max_memory_messages']}\n
    ├ max_tokens: {chat_settings['max_tokens']}\n
    └ temperature: {chat_settings['temperature']}\n
    \n
    <b>Настройки изображений:</b>\n
    ├ image_dimensions: {pictures_settings['image_dimensions']}\n
    ├ num_outputs: {pictures_settings['num_outputs']}\n
    ├ num_inference_steps: {pictures_settings['num_inference_steps']}\n
    ├ guidance_scale: {pictures_settings['guidance_scale']}\n
    └ scheduler: {pictures_settings['scheduler']}\n
    """
    return text.replace('\\', '\\\\').replace('`', '\`')


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
    await message.answer(text, reply_markup=get_settings_buttons(), parse_mode='HTML')


@router.callback_query(Text("settings_main"))
async def btn_settings(callback: types.CallbackQuery):
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_settings_buttons(), parse_mode='HTML')


@router.callback_query(Text("edit_text_settings"))
async def btn_settings(callback: types.CallbackQuery):
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons(), parse_mode='HTML')


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
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons(), parse_mode='HTML')


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
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons(), parse_mode='HTML')


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
async def edit_temperature(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_temperature_btns())


@router.callback_query(Text(startswith="set_temperature_"))
async def set_temperature(callback: types.CallbackQuery):
    value = float(callback.data.replace('set_temperature_', ''))
    update_user_chat_settings(user_id=callback.from_user.id, setting_name='temperature', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_text_settings_buttons(), parse_mode='HTML')


def get_image_settings_buttons():
    kb = [
        [types.InlineKeyboardButton(text="image_dimensions", callback_data="edit_image_dimensions")],
        [types.InlineKeyboardButton(text="num_outputs", callback_data="edit_num_outputs")],
        [types.InlineKeyboardButton(text="num_inference_steps", callback_data="edit_num_inference_steps")],
        [types.InlineKeyboardButton(text="guidance_scale", callback_data="edit_guidance_scale")],
        [types.InlineKeyboardButton(text="scheduler", callback_data="edit_scheduler")],
        [types.InlineKeyboardButton(text="back", callback_data="settings_main")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_image_settings"))
async def btn_settings(callback: types.CallbackQuery):
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_image_settings_buttons(), parse_mode='HTML')


def get_edit_image_dimensions_btns():
    kb = [
        [types.InlineKeyboardButton(text="768x768", callback_data=f"set_image_dimensions_768")],
        [types.InlineKeyboardButton(text="512x512", callback_data=f"set_image_dimensions_512")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_image_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_image_dimensions"))
async def edit_image_dimensions(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_image_dimensions_btns())


@router.callback_query(Text(startswith="set_image_dimensions_"))
async def set_image_dimensions(callback: types.CallbackQuery):
    value = int(callback.data.replace('set_image_dimensions_', ''))
    update_user_pictures_settings(user_id=callback.from_user.id, setting_name='image_dimensions',
                                  value=f'{value}x{value}')
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_image_settings_buttons(), parse_mode='HTML')


def get_edit_num_outputs_btns():
    kb = [
        [types.InlineKeyboardButton(text="1", callback_data=f"set_num_outputs_1")],
        [types.InlineKeyboardButton(text="2", callback_data=f"set_num_outputs_2")],
        [types.InlineKeyboardButton(text="3", callback_data=f"set_num_outputs_3")],
        [types.InlineKeyboardButton(text="4", callback_data=f"set_num_outputs_4")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_image_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_num_outputs"))
async def edit_num_outputs(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_num_outputs_btns())


@router.callback_query(Text(startswith="set_num_outputs_"))
async def set_num_outputs(callback: types.CallbackQuery):
    value = int(callback.data.replace('set_num_outputs_', ''))
    update_user_pictures_settings(user_id=callback.from_user.id, setting_name='num_outputs', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_image_settings_buttons(), parse_mode='HTML')


def get_edit_num_inference_steps_btns():
    kb = [
        [types.InlineKeyboardButton(text="50", callback_data=f"set_num_inference_steps_50")],
        [types.InlineKeyboardButton(text="100", callback_data=f"set_num_inference_steps_100")],
        [types.InlineKeyboardButton(text="200", callback_data=f"set_num_inference_steps_200")],
        [types.InlineKeyboardButton(text="300", callback_data=f"set_num_inference_steps_300")],
        [types.InlineKeyboardButton(text="400", callback_data=f"set_num_inference_steps_400")],
        [types.InlineKeyboardButton(text="500", callback_data=f"set_num_inference_steps_500")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_image_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_num_inference_steps"))
async def edit_num_inference_steps(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_num_inference_steps_btns())


@router.callback_query(Text(startswith="set_num_inference_steps_"))
async def set_num_inference_steps(callback: types.CallbackQuery):
    value = int(callback.data.replace('set_num_inference_steps_', ''))
    update_user_pictures_settings(user_id=callback.from_user.id, setting_name='num_inference_steps', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_image_settings_buttons(), parse_mode='HTML')


def get_edit_guidance_scale_btns():
    kb = []
    for i in range(10):
        kb.append([types.InlineKeyboardButton(text=f"{i + 1}", callback_data=f"set_guidance_scale_{i + 1}")])
    kb.append([types.InlineKeyboardButton(text="back", callback_data="edit_image_settings")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_guidance_scale"))
async def edit_guidance_scale(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_guidance_scale_btns())


@router.callback_query(Text(startswith="set_guidance_scale_"))
async def set_guidance_scale(callback: types.CallbackQuery):
    value = float(callback.data.replace('set_guidance_scale_', ''))
    update_user_pictures_settings(user_id=callback.from_user.id, setting_name='guidance_scale', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_image_settings_buttons(), parse_mode='HTML')


def get_edit_scheduler_btns():
    kb = [
        [types.InlineKeyboardButton(text="DDIM", callback_data=f"set_scheduler_DDIM")],
        [types.InlineKeyboardButton(text="K_EULER", callback_data=f"set_scheduler_K_EULER")],
        [types.InlineKeyboardButton(text="DPMSolverMultistep", callback_data=f"set_scheduler_DPMSolverMultistep")],
        [types.InlineKeyboardButton(text="K_EULER_ANCESTRAL", callback_data=f"set_scheduler_K_EULER_ANCESTRAL")],
        [types.InlineKeyboardButton(text="PNDM", callback_data=f"set_scheduler_PNDM")],
        [types.InlineKeyboardButton(text="KLMS", callback_data=f"set_scheduler_KLMS")],
        [types.InlineKeyboardButton(text="back", callback_data="edit_image_settings")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


@router.callback_query(Text("edit_scheduler"))
async def edit_scheduler(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_scheduler_btns())


@router.callback_query(Text(startswith="set_scheduler_"))
async def set_scheduler(callback: types.CallbackQuery):
    value = callback.data.replace('set_scheduler_', '')
    update_user_pictures_settings(user_id=callback.from_user.id, setting_name='scheduler', value=value)
    text = get_settings_text(callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=get_image_settings_buttons(), parse_mode='HTML')
