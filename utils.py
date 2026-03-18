from telegram.ext import *
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton
from emoji import emojize 
from random import choice
import settings


def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(choice(settings.USER_EMOJI), language='alias')
        return user_data['smile']

def get_keyboard():
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([

        ['Прислать котика', 'Сменить аватарку'],
        [contact_button, location_button],
        ['Заполнить анкету']
                                       ], resize_keyboard=True)
    return my_keyboard