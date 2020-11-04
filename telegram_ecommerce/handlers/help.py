from telegram.ext import CommandHandler

from ..utils.consts import TEXT
from ..database.query import is_admin


def help_callback(update, context):
    text = TEXT["help"]
    user = update.effective_user
    user_is_admin = is_admin(user.id)
    if user_is_admin:
        text += TEXT["help_admin"]
    update.message.reply_text(text)


help_command = CommandHandler("help", help_callback)


