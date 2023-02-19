from os import getenv
from os.path import join
from asyncio import run
from database import create_connect
from aiogram import Bot, Dispatcher, types
from modules import get_token, get_lang, get_static
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

bot = Bot(token=get_token(), parse_mode="HTML")
dp = Dispatcher()
_type = type

MESSAGES = {}
FAQ_MESSAGES = {}
MARKUPS = {}
LANGUAGE_CODES = []


def message_handle(m: types.Message, type):
    lang = get_lang(m, LANGUAGE_CODES)
    return MESSAGES[lang][type]['title'] == m.text


def faq_handle(c: types.CallbackQuery):
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

    messages = await db.fetch(
        "SELECT type, code, title, text, attachment "
        "FROM messages "
        "INNER JOIN localisation l on messages.id = l.message_id "
        "INNER JOIN languages l2 on l2.id = l.language_id "
        "ORDER BY priority"
    )
    faq_messages = await db.fetch("SELECT faq.id, title, text, code, attachment FROM faq INNER JOIN languages l on l.id = faq.language")
    languages = await db.fetch('SELECT code FROM languages ORDER BY id')
    for lang in languages:
        lang = lang['code']

        MARKUPS[lang] = {
            'faq_main': InlineKeyboardBuilder(),
            'start': ReplyKeyboardBuilder(),
            'service': InlineKeyboardBuilder()
        }
        FAQ_MESSAGES[lang] = {}
        MESSAGES[lang] = {}

        LANGUAGE_CODES.append(lang)

    await db.close()

    for faq in faq_messages:
        FAQ_MESSAGES[faq['code']][faq['id']] = faq

        MARKUPS[faq['code']]['faq_main'].add(
            InlineKeyboardButton(text=faq['title'], callback_data=f'faq_{faq["id"]}')
        )

    for message in messages:

        if message['type'] in ['about', 'faq_main', 'service', 'ticket']:
            MARKUPS[message['code']]['start'].add(KeyboardButton(text=message['title']))

        if message['type'] == 'service_buttons':
            MARKUPS[message['code']]['service'].row(
                InlineKeyboardButton(text=message['title'], web_app=WebAppInfo(url=message['text']))
            )
            continue

        MESSAGES[message['code']][message['type']] = {
            'attachment': message['attachment'],
            'text': message['text'],
            'title': message['title']
        }

    for lang in LANGUAGE_CODES:
        MARKUPS[lang]['start'].adjust(2)
        MARKUPS[lang]['faq_main'].adjust(2)


@dp.message(commands=['start'])
async def process_start_command(message: types.Message):
    await send(message, 'start')

    profile_pictures = await bot.get_user_profile_photos(message.from_user.id, limit=1)
    avatars = profile_pictures.photos

    if len(avatars) > 0:
        file = await bot.get_file(avatars[0][-1].file_id)

        await bot.download_file(
            file.file_path,
            join(
                getenv('static_folder'), 'img',
                'avatars', f'avatar_{message.from_user.id}.jpg'
            )
        )

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


@dp.message(lambda m: message_handle(m, 'about'))
async def about_us(message: types.Message):
    await send(message, 'about')


@dp.message(lambda m: message_handle(m, 'faq_main'))
async def faq_main(message: types.Message):
    await send(message, 'faq_main')


@dp.message(lambda m: message_handle(m, 'ticket'))
async def ticket_handler(message: types.Message):
    await send(message, 'ticket')


@dp.message(lambda m: message_handle(m, 'service'))
async def service_handler(message: types.Message):
    await send(message, 'service')


@dp.callback_query(lambda c: faq_handle(c))
async def faq_handler(call: types.CallbackQuery):
    faq_id = int(call.data.split('_')[-1])
    await send(call, faq_id, FAQ_MESSAGES)


@dp.message(commands=['refresh_buttons'])
async def refresh_buttons(message: types.Message):
    db = await create_connect()

    authorize_user = await db.fetch("SELECT COUNT(*) cnt FROM users WHERE id=$1 AND role_id is not NULL", message.from_user.id)
    await db.close()

    if authorize_user == 0:
        return await message.answer('У вас нет доступа!')

    await bot.send_message(message.chat.id,'Перезагружаю...')

    await load_buttons()
    await bot.send_message(message.chat.id, 'Конфиг успешно перезагружен...')



if __name__ == '__main__':
    run(load_buttons())
    print('RUN BOT')

    dp.run_polling(bot)
