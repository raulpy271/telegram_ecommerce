from telegram import BotCommand

from ..language import get_text
from .language import language
from .start import start
from .help import help_command
from .register import register
from .add_category import add_category
from .add_product import add_product 
from .show_categories import show_categories


all_handlers = [
    start,
    help_command,
    register,
    add_category, 
    add_product, 
    language,
    show_categories] 


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
        "register", 
        get_text("register_description")
        ),
    BotCommand(
        "language", 
        get_text("language_description")
        )
    ]


