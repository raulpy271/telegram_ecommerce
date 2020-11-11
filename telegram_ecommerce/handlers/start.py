from telegram.ext import CommandHandler

from ..language import get_text


def start_callback(update, context):
    text = get_text("start", context)
    update.message.reply_text(text)


start = CommandHandler("start", start_callback)


