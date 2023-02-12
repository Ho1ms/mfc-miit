from os.path import join
from os import getenv, getcwd
from aiogram.types import FSInputFile


def get_token() -> str:
    return getenv('BOT_TOKEN')


def get_static(file_name:str) -> str:
    return FSInputFile(path=join(getenv('static_folder'), 'messages', file_name))


def get_lang(m, LANGUAGE_CODES):
    return m.from_user.language_code if m.from_user.language_code in LANGUAGE_CODES else 'ru'


