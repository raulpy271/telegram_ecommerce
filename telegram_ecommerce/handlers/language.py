"""Language selection through native names or BCP 47 language tags."""

from telegram import ReplyKeyboardRemove
from telegram.ext import filters, ConversationHandler, CommandHandler, MessageHandler

from telegram_ecommerce.tamplates.buttons import get_list_of_buttons
from telegram_ecommerce.language import TEXT, get_text, normalize_locale


(END, SELECTING_THE_LANGUAGE) = [-1, 1]


def language_options():
    return [f"{TEXT.display_name(code)} ({code})" for code in sorted(TEXT.suported_languages)]


def get_selected_language(value):
    """Accept a displayed option or a supported language tag."""
    value = value.strip()
    for code in TEXT.suported_languages:
        if value == f"{TEXT.display_name(code)} ({code})":
            return code
    code = normalize_locale(value)
    if code and code in TEXT.suported_languages:
        return code
    raise ValueError("Unsupported language")


async def change_language_callback(update, context):
    options = language_options()
    # Large catalogs remain usable by entering a language tag directly.
    markup = get_list_of_buttons(*options) if len(options) <= 12 else ReplyKeyboardRemove()
    prompt = get_text("choose_language", context)
    if len(options) > 12:
        prompt += "\n" + get_text("language_enter_code", context)
        prompt += "\n" + ", ".join(sorted(TEXT.suported_languages))
    await update.message.reply_text(prompt, reply_markup=markup)
    return SELECTING_THE_LANGUAGE


async def selecting_the_language(update, context):
    try:
        selected_language = get_selected_language(update.message.text)
    except (AttributeError, ValueError):
        text = get_text("language_dont_exist", context)
    else:
        context.user_data["language"] = selected_language
        text = get_text("selected_language", context)
    await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return END


async def cancel_language(update, context):
    query = update.callback_query
    if update.message:
        await update.message.reply_text(get_text("canceled_operation", context))
    elif query:
        await query.edit_message_text(get_text("canceled_operation", context))
    return END


language_command = CommandHandler("language", change_language_callback)
language = ConversationHandler(
    entry_points=[language_command],
    states={SELECTING_THE_LANGUAGE: [MessageHandler(filters.TEXT, selecting_the_language)]},
    fallbacks=[MessageHandler(filters.ALL, cancel_language)],
)
