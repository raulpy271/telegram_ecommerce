from telegram import BotCommand

from .add_category import add_category
from .start import start
from .help import help_command
from .register import register
from ..utils.consts import TEXT


all_handlers = [
    start,
    help_command,
    register,
    add_category] 


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
