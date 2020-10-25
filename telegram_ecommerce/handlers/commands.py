from telegram.ext import (
    CommandHandler)

from .callbacks import (
    start_callback,
    help_callback,
    show_categories_callback,
    register_callback)

start = CommandHandler("start", start_callback)

help_command = CommandHandler("help", help_callback)

register = CommandHandler("register", register_callback)


