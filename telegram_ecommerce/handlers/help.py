from telegram.ext import CommandHandler

from telegram_ecommerce.language import get_text
from telegram_ecommerce.database.query import is_admin


async def help_callback(update, context):
    text = get_text("help", context)
    user = update.effective_user
    user_is_admin = is_admin(user.id)
    if user_is_admin:
        text += get_text("help_admin", context)
    await update.message.reply_text(text)


help_command = CommandHandler("help", help_callback)


