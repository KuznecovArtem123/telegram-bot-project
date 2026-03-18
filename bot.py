from telegram.ext import *
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton
import os
from dotenv import load_dotenv
import logging
from glob import glob
from random import choice
from emoji import emojize 
import settings

# кирилл 931448223

logging.basicConfig(
    format="%(asctime)s - %(name)s %(levelname)s - %(message)s",
    level=logging.INFO,
    filename='bot.log',
    encoding='utf-8',

)

logging.getLogger('httpx').setLevel(logging.WARNING)

load_dotenv()

def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(choice(settings.USER_EMOJI), language='alias')
        return user_data['smile']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    smile = get_user_smile(context.user_data)
    text = f'Hello! Welcome To Our Chat! {smile}'
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([

        ['Прислать котика', 'Сменить аватарку'],
        [contact_button, location_button]
                                       ], resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=my_keyboard)
    logging.info(text)

async def change_avatar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'smile' in context.user_data:
        del context.user_data['smile']
    smile = get_user_smile(context.user_data)
    await update.message.reply_text(f'Готово: {smile}')
    logging.info('Сменили аватар %s', smile)


async def talkToMe(update: Update, context):
    user_text = f'Привет {update.message.chat.username} написал {update.message.text}'
    print(user_text)
    await context.bot.send_message(chat_id=update.message.chat_id, text=user_text)
    # await update.message.reply_text(user_text)

    logging.info("User:%s, Chat id: %s, Message: %s", 
        update.message.chat.username,
        update.message.chat.id,
        update.message.text
    )
    
async def send_cat_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_list = glob('images/cat*.jpg')
    cat_pic = choice(cat_list)

    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'))
    logging.info('Отправили фото: %s',cat_pic)

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.contact)
    await update.message.reply_text(f'Готово:{context.user_data['smile']}')

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.location)
    await update.message.reply_text(f'Готово:{context.user_data['smile']}')

def main():
    logging.info('Бот Стартовал')
    print('starting')
    application = (
        Application.builder()
        .token(os.getenv('TOKEN'))
        .build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cat', send_cat_picture))
    application.add_handler(CommandHandler('cat', send_cat_picture))
    application.add_handler(MessageHandler(filters.Regex('^(Прислать котика)$'), send_cat_picture))
    application.add_handler(MessageHandler(filters.Regex('^(Сменить аватарку)$'), change_avatar))
    application.add_handler(MessageHandler(filters.CONTACT, get_contact))
    application.add_handler(MessageHandler(filters.LOCATION, get_location))
    application.add_handler(MessageHandler(filters.TEXT, talkToMe))
    application.run_polling()

main()