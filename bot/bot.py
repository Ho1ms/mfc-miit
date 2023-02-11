from os import getenv
from os.path import join
from asyncio import run
from database import create_connect
from aiogram import Bot, Dispatcher, types
from modules import get_token, get_lang, send
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(token=get_token(), parse_mode="HTML")
dp = Dispatcher()

MESSAGES = {}
FAQ_MESSAGES = {}
MARKUPS = {}
LANGUAGE_CODES = []

def message_handle(m:types.Message, type):
    lang = get_lang(m, LANGUAGE_CODES)
    return MESSAGES[lang][type]['title'] == m.text


async def load_buttons():
    global LANGUAGE_CODES, MESSAGES

    db = await create_connect()

    LANGUAGE_CODES = [i['code'] for i in await db.fetch('SELECT code FROM localisations ORDER BY id')]
    messages = await db.fetch("SELECT * FROM messages INNER JOIN localisations l on l.id = messages.locale_id")
    markups = await db.fetch("SELECT * FROM markups INNER JOIN buttons b on markups.id = b.markup_id INNER JOIN localisations l on l.id = b.locale_id")

    await db.close()

    for markup in markups:
        MARKUPS.setdefault(markup['code'], {})
        MARKUPS[markup['code']].setdefault(markup['type'], ReplyKeyboardBuilder())
        MARKUPS[markup['code']][markup['type']].add(KeyboardButton(text=markup['title']))
        MARKUPS[markup['code']][markup['type']].adjust(2)

    for m in messages:
        MESSAGES.setdefault(m['code'], {})
        MESSAGES[m['code']][m['type']] = {
            'attachment': m['attachment'],
            'text': m['text']
        }



@dp.message(commands=['start'])
async def process_start_command(message: types.Message):
    lang_code = get_lang(message, LANGUAGE_CODES)

    await bot.send_message(
        chat_id=message.from_user.id,
        text=MESSAGES[lang_code]['start']['text'],
        reply_markup=MARKUPS[lang_code]['start'].as_markup(resize_keyboard=True)
    )

    profile_pictures = await bot.get_user_profile_photos(message.from_user.id, limit=1)
    avatars = profile_pictures.photos

    if len(avatars) > 0:
        file = await bot.get_file(avatars[0][-1].file_id)
        await bot.download_file(file.file_path, join(getenv('static_folder'), 'img', 'avatars', f'avatar_{message.from_user.id}.jpg'))
        avatar = f'avatar_{message.from_user.id}.jpg'
    else:
        avatar = f'unknown_user.jpg'

    db = await create_connect()

    await db.execute(
        """INSERT INTO bot_users (id, username, last_name, first_name, avatar) 
        VALUES ($1, $2, $3, $4, $5) 
        ON CONFLICT (id) DO UPDATE SET username=$2, last_name=$3, first_name=$4""",
        message.from_user.id, message.from_user.username,
        message.from_user.last_name, message.from_user.first_name,
        avatar
    )

    await db.close()



if __name__ == '__main__':
    run(load_buttons())
    print('RUN BOT')
    dp.run_polling(bot)
