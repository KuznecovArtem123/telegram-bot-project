from telegram.ext import *
from telegram import Update, ReplyKeyboardMarkup,KeyboardButton


def get_keyboard():
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([

        ['Прислать котика', 'Сменить аватарку'],
        [contact_button, location_button],
        ['Заполнить анкету']
                                       ], resize_keyboard=True)
    return my_keyboard