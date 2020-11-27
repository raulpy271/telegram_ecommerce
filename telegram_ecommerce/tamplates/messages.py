from ..language import get_text
from .buttons import (
    boolean_question,
    rating_tamplate)

def reply(update, context, text):
    update.message.reply_text(text)


def ask_a_boolean_question(
    update, 
    context, 
    pattern_identifier="", 
    question=None):
    if question:
        text = question
    else:
        text = get_text("ask_if_its_all_ok", context)
    markup = boolean_question(pattern_identifier, context)
    update.message.reply_text(text, reply_markup=markup)


def send_a_rating_message(update, context, pattern_identifier=""):
    text = get_text("ask_for_the_rating", context)
    markup = rating_tamplate(pattern_identifier, context)
    if update.message:
        update.message.reply_text(text, reply_markup=markup)
    else:
        update.callback_query.edit_message_text(text, reply_markup = markup)


