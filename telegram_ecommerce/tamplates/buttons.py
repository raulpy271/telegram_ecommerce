
from telegram import (
    KeyboardButton as Button,
    ReplyKeyboardMarkup,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardMarkup)

from ..utils.consts import TEXT


def boolean_question(pattern_identifier):
    return InlineKeyboardMarkup([
        [
            InlineButton(TEXT["cancel"], 
                callback_data=pattern_identifier + 'cancel'),
            InlineButton(TEXT["OK"], 
                callback_data=pattern_identifier + 'OK')
        ]
    ])


def numeric_keyboard(pattern_identifier):
    return (InlineKeyboardMarkup([
    [
        InlineButton("1", callback_data=pattern_identifier + 'digit_1'),
        InlineButton("2", callback_data=pattern_identifier + 'digit_2'),
        InlineButton("3", callback_data=pattern_identifier + 'digit_3')
    ],
    [
        InlineButton("4", callback_data=pattern_identifier + 'digit_4'),
        InlineButton("5", callback_data=pattern_identifier + 'digit_5'),
        InlineButton("6", callback_data=pattern_identifier + 'digit_6')
    ],
    [
        InlineButton("7", callback_data=pattern_identifier + 'digit_7'),
        InlineButton("8", callback_data=pattern_identifier + 'digit_8'),
        InlineButton("9", callback_data=pattern_identifier + 'digit_9')
    ],
    [
        InlineButton(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_numeric_keyboard'),
        InlineButton("0", callback_data=pattern_identifier + 'digit_0'),
        InlineButton(TEXT["next"], 
            callback_data=pattern_identifier + 'end_numeric_keyboard')
    ]]))


def login_keyboard(pattern_identifier): 
    return ({
    "step_1": InlineKeyboardMarkup([
    [
        InlineButton(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_loging_process'),
        InlineButton(TEXT["next"], 
            callback_data=pattern_identifier + 'next_step_1_login_process'),
    ]]),
    "step_2": numeric_keyboard(pattern_identifier),
    "step_3": InlineKeyboardMarkup([
    [
        InlineButton(TEXT["cancel"], 
            callback_data=pattern_identifier + 'cancel_loging_process'),
        InlineButton(TEXT["next"],
            callback_data=pattern_identifier + 'end_login_process'),
    ]]) })


def get_list_of_buttons(pattern_identifier, *names_in_buttons):
    list_of_buttons = []
    for name_of_the_button in names_in_buttons:
        list_of_buttons.append(
            [
                Button(name_of_the_button)
            ]
        )
    return ReplyKeyboardMarkup(list_of_buttons)


