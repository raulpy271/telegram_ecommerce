
from telegram import (
    InlineKeyboardButton as Button,
    InlineKeyboardMarkup)

from ..utils.consts import TEXT

def numeric_keyboard(pattern_identifier):
    return (InlineKeyboardMarkup([
    [
        Button("1", callback_data=pattern_identifier + 'digit_1'),
        Button("2", callback_data=pattern_identifier + 'digit_2'),
        Button("3", callback_data=pattern_identifier + 'digit_3')
    ],
    [
        Button("4", callback_data=pattern_identifier + 'digit_4'),
        Button("5", callback_data=pattern_identifier + 'digit_5'),
        Button("6", callback_data=pattern_identifier + 'digit_6')
    ],
    [
        Button("7", callback_data=pattern_identifier + 'digit_7'),
        Button("8", callback_data=pattern_identifier + 'digit_8'),
        Button("9", callback_data=pattern_identifier + 'digit_9')
    ],
    [
        Button(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_numeric_keyboard'),
        Button("0", callback_data=pattern_identifier + 'digit_0'),
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

