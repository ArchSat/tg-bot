from typing import Union

from sqlalchemy.exc import IntegrityError

from config.default_settings import default_chatgpt_settings, default_stable_diffusion_settings
from database.shemas.user import User, session


def register_user(user_id, chat_settings=None, pictures_settings=None):
    if pictures_settings is None:
        pictures_settings = {}
    if chat_settings is None:
        chat_settings = {}
    user = User(id=int(user_id), chat_settings=chat_settings, pictures_settings=pictures_settings)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def is_registered(user_id):
    count = session.query(User).filter(User.id == user_id).count()
    return bool(count)


def get_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def select_user_chat_settings(user_id):
    settings = session.query(User.chat_settings).filter(User.id == user_id).first()
    user_chat_settings = default_chatgpt_settings.copy()
    try:
        user_chat_settings.update(settings[0])
    except IndexError:
        pass
    return user_chat_settings


def select_user_pictures_settings(user_id):
    settings = session.query(User.pictures_settings).filter(User.id == user_id).first()
    user_stable_diffusion_settings = default_stable_diffusion_settings.copy()
    try:
        user_stable_diffusion_settings.update(settings[0])
    except IndexError:
        pass
    return user_stable_diffusion_settings


def update_user_chat_settings(user_id, setting_name, value):
    user: Union[User, None] = get_user(user_id)
    if user:
        user_chat_settings = user.chat_settings.copy()
        user_chat_settings.update({setting_name: value})
        if default_chatgpt_settings.get(setting_name, None) == value:
            user_chat_settings.pop(setting_name)
        user.chat_settings = user_chat_settings
        session.commit()
    elif default_chatgpt_settings.get(setting_name, None) != value:
        register_user(user_id=user_id, chat_settings={setting_name: value})


def update_user_pictures_settings(user_id, setting_name, value):
    user: Union[User, None] = get_user(user_id)
    if user:
        user_pictures_settings = user.pictures_settings.copy()
        user_pictures_settings.update({setting_name: value})
        if default_stable_diffusion_settings.get(setting_name, None) == value:
            user_pictures_settings.pop(setting_name)
        user.user_pictures_settings = user_pictures_settings
        session.commit()
    elif default_stable_diffusion_settings.get(setting_name, None) == value:
        register_user(user_id=user_id, pictures_settings={setting_name: value})
