from telegram.ext import *
import os
from dotenv import load_dotenv
import logging
from handlers import *
# кирилл 931448223

logging.basicConfig(
    format="%(asctime)s - %(name)s %(levelname)s - %(message)s",
    level=logging.INFO,
    filename='bot.log',
    encoding='utf-8',
)

logging.getLogger('httpx').setLevel(logging.WARNING)

load_dotenv()

def main():
    logging.info('Бот Стартовал')
    print('starting')
    application = (
        Application.builder()
        .token(os.getenv('TOKEN'))
        .build()
    )
    anketa = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^(Заполнить анкету)$'), anketa_start)],
        states={
            'name': [MessageHandler(filters.TEXT, anketa_get_name)],
            'rating': [MessageHandler(filters.Regex('^(1|2|3|4|5)$'), anketa_rating)],
            'comment': [
                        CommandHandler('skip', anketa_skip_comment),
                        MessageHandler(filters.TEXT, anketa_comment),
                        ]
        },
        fallbacks=[CommandHandler('exit', anketa_exit)]
    )
    application.add_handler(anketa)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cat', send_cat_picture))
    application.add_handler(MessageHandler(filters.Regex('^(Прислать котика)$'), send_cat_picture))
    application.add_handler(MessageHandler(filters.Regex('^(Сменить аватарку)$'), change_avatar))
    application.add_handler(MessageHandler(filters.CONTACT, get_contact))
    application.add_handler(MessageHandler(filters.LOCATION, get_location))
    application.add_handler(MessageHandler(filters.TEXT, talkToMe))
    application.run_polling()

main()