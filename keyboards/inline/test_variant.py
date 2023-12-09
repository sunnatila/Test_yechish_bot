import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def variants_buttons(test: list):
    res1 = InlineKeyboardButton(text=test[2], callback_data='true')
    res2 = InlineKeyboardButton(text=test[3], callback_data='false')
    res3 = InlineKeyboardButton(text=test[4], callback_data='false')
    res4 = InlineKeyboardButton(text=test[5], callback_data='false')
    inlines = random.sample([res1, res2, res3, res4], 4)
    variants = InlineKeyboardMarkup(row_width=2)
    variants.add(inlines[0], inlines[1])
    variants.add(inlines[2], inlines[3])
    return variants
