from telegram.ext import CommandHandler

from ..utils.consts import TEXT


def start_callback(update, context):
    text = TEXT["start"]
    update.message.reply_text(text)


start = CommandHandler("start", start_callback)


