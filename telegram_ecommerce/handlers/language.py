from telegram import ReplyKeyboardRemove
from telegram.ext import (
    filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler)

from telegram_ecommerce.tamplates.buttons import get_list_of_buttons
from telegram_ecommerce.language import (TEXT, get_text)
from telegram_ecommerce.utils.utils import get_key


(END, SELECTING_THE_LANGUAGE) = [-1, 1]


all_language = list(TEXT.suported_languages)
all_message_for_each_language = list(
    map((
        lambda language : TEXT.get_text(language, TEXT.default_language) 
        ), all_language))


def get_selected_language(text):
    dict_with_all_messages = TEXT.all_text[TEXT.default_language]
    return get_key(dict_with_all_messages, text)


async def change_language_callback(update, context):
    markup = get_list_of_buttons(*all_message_for_each_language)
    await update.message.reply_text(
        get_text("choose_language", context), 
        reply_markup=markup)
    return SELECTING_THE_LANGUAGE


async def selecting_the_language(update, context):
    try: 
        selected_language = get_selected_language(update.message.text)
        context.user_data['language'] = selected_language
        text = get_text("selected_language", context)
        await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    except:
        text = get_text("language_dont_exist", context)
        await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    finally:
        return END


async def cancel_language(update, context):
    query = update.callback_query
    if update.message:
        await update.message.reply_text(get_text("canceled_operation", context))
    elif query:
        await query.edit_message_text(get_text("canceled_operation", context))
    return END


language_command = (
    CommandHandler("language", change_language_callback))


language = ConversationHandler(
    entry_points = [language_command],
    states = {
        SELECTING_THE_LANGUAGE : [
        MessageHandler(
            filters.TEXT,
            selecting_the_language
            )
        ]
    },
    fallbacks = [MessageHandler(filters.ALL, cancel_language)]
    )


