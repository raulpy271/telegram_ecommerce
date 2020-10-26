
from telegram import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup)

from ..utils.consts import TEXT

def numeric_keyboard(pattern_identifier):
    return (InlineKeyboardMarkup([
    [
        Button("1", callback_data=pattern_identifier + '1'),
        Button("2", callback_data=pattern_identifier + '2'),
        Button("3", callback_data=pattern_identifier + '3')
    ],
    [
        Button("4", callback_data=pattern_identifier + '4'),
        Button("5", callback_data=pattern_identifier + '5'),
        Button("6", callback_data=pattern_identifier + '6')
    ],
    [
        Button("7", callback_data=pattern_identifier + '7'),
        Button("8", callback_data=pattern_identifier + '8'),
        Button("9", callback_data=pattern_identifier + '9')
    ],
    [
        Button(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_numeric_keyboard'),
        Button("0", callback_data=pattern_identifier + '0'),
        Button(TEXT["next"], 
            callback_data=pattern_identifier + 'end_numeric_keyboard')
    ]]))



def login_keyboard(pattern_identifier): 
    return ({
    "step_1": InlineKeyboardMarkup([
    [
        Button(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_loging_process'),
        Button(TEXT["next"], 
            callback_data=pattern_identifier + 'next_step_1_login_process'),
    ]]),
    "step_2": numeric_keyboard(pattern_identifier),
    "step_3": InlineKeyboardMarkup([
    [
        Button(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_loging_process'),
        Button(TEXT["next"],
            callback_data=pattern_identifier + 'end_login_process'),
    ]]) })

