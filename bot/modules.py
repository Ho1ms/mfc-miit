from os.path import join
from os import getenv, getcwd
from aiogram.types import FSInputFile


def get_token() -> str:
    return getenv('BOT_TOKEN')


def get_static(file_name:str) -> str:
    return FSInputFile(path=join(getenv('static_folder'), 'messages', file_name))


def get_lang(m, LANGUAGE_CODES):
    return m.from_user.language_code if m.from_user.language_code in LANGUAGE_CODES else 'ru'


async def send(bot, message, type, MAIN_MESSAGES, LANGUAGE_CODES, MARKUP):
    lang_code = get_lang(message, LANGUAGE_CODES)

    current_message = MAIN_MESSAGES[lang_code][type]
    text = current_message.get('description')

    if current_message.get('attachment'):
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=get_static(current_message.get('attachment')),
            caption=text,
            reply_markup=MARKUP[type][lang_code].as_markup()
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=text,
            reply_markup=MARKUP[type][lang_code].as_markup()
        )