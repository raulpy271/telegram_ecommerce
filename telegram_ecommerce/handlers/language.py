from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler)

from ..tamplates.buttons import get_list_of_buttons
from ..language import (TEXT, get_text)
from ..utils.utils import (
    get_key,
    get_lang)


(END, SELECTING_THE_LANGUAGE) = [-1, 1]


all_language = list(TEXT.suported_languages)
all_message_for_each_language = list(
    map((
        lambda language : TEXT.get_text(language, TEXT.default_language) 
        ), all_language))


def get_selected_language(text):
    dict_with_all_messages = TEXT.all_text[TEXT.default_language]
    return get_key(dict_with_all_messages, text)


def change_language_callback(update, context):
    markup = get_list_of_buttons(*all_message_for_each_language)
    update.message.reply_text(
        get_text("choose_language", context), 
        reply_markup=markup)
    return SELECTING_THE_LANGUAGE


def selecting_the_language(update, context):
    try: 
        selected_language = get_selected_language(update.message.text)
        context.user_data['language'] = selected_language
        text = get_text("selected_language", context)
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    except:
        text = get_text("language_dont_exist", context)
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    finally:
        return END


def cancel_language(update, context):
    query = update.callback_query
    if update.message:
        update.message.reply_text(get_text("canceled_operation", context))
    elif query:
        query.edit_message_text(get_text("canceled_operation", context))
    return END


language_command = (
    CommandHandler("language", change_language_callback))


language = ConversationHandler(
    entry_points = [language_command],
    states = {
        SELECTING_THE_LANGUAGE : [
        MessageHandler(
            Filters.text,
            selecting_the_language
            )
        ]
    },
    fallbacks = [MessageHandler(Filters.all, cancel_language)]
    )


