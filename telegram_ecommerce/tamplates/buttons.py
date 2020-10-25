
from telegram import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup)

from ..utils.consts import TEXT

numeric_keyboard = InlineKeyboardMarkup([
    [
        Button("1", callback_data='1'),
        Button("2", callback_data='2'),
        Button("3", callback_data='3')
    ],
    [
        Button("4", callback_data='4'),
        Button("5", callback_data='5'),
        Button("6", callback_data='6')
    ],
    [
        Button("7", callback_data='7'),
        Button("8", callback_data='8'),
        Button("9", callback_data='9')
    ],
    [
        Button(TEXT["cancel"], 
            callback_data='cancel_numeric_keyboard'),
        Button("0", callback_data='0'),
        Button(TEXT["next"], 
            callback_data='end_numeric_keyboard')
    ]])


login_keyboard = {
    "step_1": InlineKeyboardMarkup([
    [
        Button(TEXT["cancel"], callback_data='cancel_loging_process'),
        Button(TEXT["next"], callback_data='next_step_1_login_process'),
    ]]),
    "step_2": numeric_keyboard,
    "step_3": InlineKeyboardMarkup([
    [
        Button(TEXT["cancel"], callback_data='cancel_loging_process'),
        Button(TEXT["next"], callback_data='end_login_process'),
    ]])
}



