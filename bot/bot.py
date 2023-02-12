from os import getenv
from os.path import join
from asyncio import run
from database import create_connect
from aiogram import Bot, Dispatcher, types
from modules import get_token, get_lang, get_static
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(token=get_token(), parse_mode="HTML")
dp = Dispatcher()
_type = type

MESSAGES = {}
FAQ_MESSAGES = {}
MARKUPS = {}
LANGUAGE_CODES = []


def message_handle(m:types.Message, type):
    lang = get_lang(m, LANGUAGE_CODES)
    return MESSAGES[lang][type]['title'] == m.text

def faq_handle(c:types.CallbackQuery):
    lang = get_lang(c, LANGUAGE_CODES)
    return c.data.startswith('faq_') and FAQ_MESSAGES[lang].get(int(c.data.split('_')[-1])) is not None


async def send(message, type, messages=None):
    messages = messages or MESSAGES
    lang_code = get_lang(message, LANGUAGE_CODES)

    current_message = messages[lang_code][type]
    text = current_message.get('text')
    markup = MARKUPS[lang_code].get(type)

    if current_message.get('attachment'):
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=get_static(current_message.get('attachment')),
            caption=text,
            reply_markup=markup.as_markup(resize_keyboard=True) if markup else None
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=text,
            reply_markup=markup.as_markup(resize_keyboard=True) if markup else None
        )


async def load_buttons():
    global LANGUAGE_CODES, MESSAGES, MARKUPS

    db = await create_connect()

    LANGUAGE_CODES = [i['code'] for i in await db.fetch('SELECT code FROM localisations ORDER BY id')]
    messages = await db.fetch("SELECT messages.id, text, title, code, type, attachment FROM messages INNER JOIN localisations l on l.id = messages.locale_id ORDER BY priority")

    await db.close()

    for m in messages:
        MARKUPS.setdefault(m['code'], {})
        MARKUPS[m['code']].setdefault('start', ReplyKeyboardBuilder())
        MARKUPS[m['code']].setdefault('faq_main', InlineKeyboardBuilder())

        if m['type'] in ['about', 'faq_main', 'service', 'ticket']:
            MARKUPS[m['code']]['start'].add(KeyboardButton(text=m['title']))
            MARKUPS[m['code']]['start'].adjust(2)
        elif m['type'] == 'faq':
            FAQ_MESSAGES.setdefault(m['code'],{})
            FAQ_MESSAGES[m['code']][m['id']] = m

            MARKUPS[m['code']]['faq_main'].add(InlineKeyboardButton(text=m['title'],callback_data=f'faq_{m["id"]}'))
            if len(m['title']) > 25:
                MARKUPS[m['code']]['faq_main'].adjust(2)

        MESSAGES.setdefault(m['code'], {})
        MESSAGES[m['code']][m['type']] = {
            'attachment': m['attachment'],
            'text': m['text'],
            'title': m['title']
        }


@dp.message(commands=['start'])
async def process_start_command(message: types.Message):

    await send(message, 'start')

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


@dp.message(lambda m: message_handle(m,'about'))
async def about_us(message: types.Message):

    await send(message, 'about')


@dp.message(lambda m: message_handle(m, 'faq_main'))
async def faq_main(message:types.Message):
    await send(message, 'faq_main')


@dp.callback_query(lambda c: faq_handle(c))
async def faq_handler(call:types.CallbackQuery):
    faq_id = int(call.data.split('_')[-1])
    await send(call, faq_id, FAQ_MESSAGES)


if __name__ == '__main__':
    run(load_buttons())
    print('RUN BOT')

    dp.run_polling(bot)
