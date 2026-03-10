from telegram.ext import *
from telegram import Update
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s %(levelname)s - %(message)s",
    level=logging.INFO,
    filename='bot.log',
    encoding='utf-8'
)

load_dotenv()

async def start(update: Update, context):
    await update.message.reply_text('Hello! Welcome To Our Chat!')
    await print(update)

async def talkToMe(update: Update, context):
    user_text = f'Привет {update.message.chat.username} написал {update.message.text}'
    print(user_text)
    await context.bot.send_message(chat_id=931448223, text=user_text)
    # await update.message.reply_text(user_text)

    logging.info("User:%s, Chat id: %s, Message: %s", 
        update.message.chat.username,
        update.message.chat.id,
        update.message.text
    )
    

def main():
    logging.info('Бот Стартовал')
    print('starting')
    application = (
        Application.builder()
        .token(os.getenv('TOKEN'))
        .build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, talkToMe))
    application.run_polling()

main()