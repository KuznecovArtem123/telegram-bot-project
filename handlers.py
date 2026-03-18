import logging
from telegram.ext import *
from telegram.constants import ParseMode
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton, ReplyKeyboardRemove
from glob import glob
from utils import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    smile = get_user_smile(context.user_data)
    text = f'Hello! Welcome To Our Chat! {smile}'
    
    await update.message.reply_text(text, reply_markup=get_keyboard())
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

async def anketa_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ФИ', reply_markup=ReplyKeyboardRemove())
    return 'name'

async def anketa_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.text
    if len(user.split(' ')) != 2 :
        await update.message.reply_text('Пожалуйста введите имя фамилию')
        return 'name'
    else:
        context.user_data['anketa_name'] = user
        reply_keyboard = [['1', '2', '3', '4' ,'5']]

        await update.message.reply_text('Оцените нашего бота от 1 до 5', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        return 'rating'

async def anketa_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['anketa_rating'] = update.message.text
    await update.message.reply_text(
        """Пожалуйста, Напишите отзыв в свободной форме 
        или /skip чтобы пропустить этот шаг
        """)
    return 'comment'

async def anketa_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['anketa_comment'] = update.message.text
    text = (
        f"<b>Фамилия Имя :</b> {context.user_data['anketa_name']}\n "
        f"<b>Оценка :</b> {context.user_data['anketa_rating']}\n "
        f"<b>Комментарий :</b> {context.user_data['anketa_comment']}"
    )
    await update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

async def anketa_skip_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"<b>Фамилия Имя :</b> {context.user_data['anketa_name']}\n "
        f"<b>Оценка :</b> {context.user_data['anketa_rating']}\n "
    )
    await update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

async def anketa_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END
