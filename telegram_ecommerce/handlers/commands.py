from telegram.ext import (
    CommandHandler)

from .callbacks import (
    start_callback,
    help_callback,
    show_categories_callback)

start = CommandHandler("start", start_callback)

help_command = CommandHandler("help", help_callback)


