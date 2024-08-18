from telegram import BotCommand

from telegram_ecommerce.language import get_text
from telegram_ecommerce.handlers.language import language
from telegram_ecommerce.handlers.start import start
from telegram_ecommerce.handlers.help import help_command
from telegram_ecommerce.handlers.register import register
from telegram_ecommerce.handlers.add_category import add_category
from telegram_ecommerce.handlers.add_product import add_product 
from telegram_ecommerce.handlers.show_categories import show_categories
from telegram_ecommerce.handlers.search import search
from telegram_ecommerce.tamplates.rating import rating_precess_handlers
from telegram_ecommerce.tamplates.buy_callbacks import (
    pre_checkout_handler,
    successful_payment_handler)


all_handlers = ([
    start,
    help_command,
    register,
    add_category, 
    add_product, 
    language,
    search,
    show_categories, 
    pre_checkout_handler, 
    successful_payment_handler] +
    rating_precess_handlers)


all_public_commands_descriptions = [
    BotCommand(
        "start", 
        get_text("start_description")
        ),
    BotCommand(
        "help", 
        get_text("help_description")
        ),
    BotCommand(
        "search", 
        get_text("search_description")
        ),
    BotCommand(
        "register", 
        get_text("register_description")
        ),
    BotCommand(
        "language", 
        get_text("language_description")
        ),
    BotCommand(
        "show_categories", 
        get_text("show_categories_description")
        )
    ]


