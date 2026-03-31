import logging
from telegram.ext import *
from telegram.constants import ParseMode
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton, ReplyKeyboardRemove
from glob import glob
from utils import *
from random import choice
from db_models import *


async def start(update, context):
    current_user = get_or_create_user(users, update.effective_user, update.message)
    print(current_user)

    smile = get_user_smile(users, current_user)
    text = f'Hello! Welcome To Our Chat! {smile}'
   
    await update.message.reply_text(text, reply_markup=get_keyboard())
    logging.info(text)

async def change_avatar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_user = get_or_create_user(users, update.effective_user, update.message)

    if current_user.smile:
        with engine.begin() as connection:
            upd = db.update(users).where(users.c.id == current_user.id).values({'smile': None})
            connection.execute(upd)
    smile = get_user_smile(users, current_user)
    
    text = f'Готово! {smile}'
    await update.message.reply_text(text)



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
        """, reply_markup=ReplyKeyboardRemove())
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

async def dontknow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите число")

async def my_test(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=1232719883, text='Нагиев рассказал секрет, как он оставляет его в состояние.....<a href="penis.com">Читать дальше---->>></a>' ,parse_mode=ParseMode.HTML)

async def my_test_schedule_end(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=1232719883, text='No more spam')
    context.job.schedule_removal()

async def my_test_schedule(context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(callback=my_test, interval=3, last=10)
    context.job_queue.run_once(callback=my_test_schedule_end, when=10)


subscribers = set()

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_user = get_or_create_user(users, update.effective_user, update.message)

    if not current_user.is_subscribed:
        toggle_subscription(users, current_user)
        await update.message.reply_text('Вы подписались')
    

async def send_updates(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in subscribers:
        await context.bot.send_message(chat_id=chat_id, text='BUZZ!')

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_user = get_or_create_user(users, update.effective_user, update.message)

    if current_user.is_subscribed:
        toggle_subscription(users, current_user)
        await update.message.reply_text('Вы отписались')
    else:
        await update.message.reply_text('Вы еще не подписаны, /subscribe')
    

async def set_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = abs(int(context.args[0]))
        context.job_queue.run_once(callback=alarm, when=seconds, chat_id=update.message.chat_id)
    except(IndexError, ValueError):
        await update.message.reply_text('Введите число секунд после команды /alarm')

async def alarm(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text='Сработал будильник!')