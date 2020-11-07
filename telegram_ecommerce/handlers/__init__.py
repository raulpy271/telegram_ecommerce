from telegram import BotCommand

from .start import start
from .help import help_command
from .register import register
from .add_category import add_category
from .add_product import add_product 
from ..utils.consts import TEXT


all_handlers = [
    start,
    help_command,
    register,
    add_category, 
    add_product] 


all_public_commands_descriptions = [
    BotCommand(
        "start", 
        TEXT["start_description"]
        ),
    BotCommand(
        "help", 
        TEXT["help_description"]
        ),
    BotCommand(
        "register", 
        TEXT["register_description"]
        )
    ]


