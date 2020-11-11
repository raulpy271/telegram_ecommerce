from telegram.ext import CommandHandler

from ..language import get_text
from ..database.query import is_admin


def help_callback(update, context):
    text = get_text("help", update)
    user = update.effective_user
    user_is_admin = is_admin(user.id)
    if user_is_admin:
        text += get_text("help_admin", context)
    update.message.reply_text(text)


help_command = CommandHandler("help", help_callback)


