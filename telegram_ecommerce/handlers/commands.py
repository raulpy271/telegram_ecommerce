from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler)

from .callbacks import (
    start_callback,
    help_callback,
    show_categories_callback,
    register_callback,
    register_callback_query_step_2,
    register_callback_query_step_3,
    register_callback_query_step_4)


start = CommandHandler("start", start_callback)

help_command = CommandHandler("help", help_callback)

register = CommandHandler("register", register_callback)

register_query_step_1 = CallbackQueryHandler(
    register_callback_query_step_2,
    pattern="register_step_1_")

register_query_step_2 = CallbackQueryHandler(
    register_callback_query_step_3,
    pattern="register_step_2_")

register_query_step_3 = CallbackQueryHandler(
    register_callback_query_step_4,
    pattern="register_step_3_")
