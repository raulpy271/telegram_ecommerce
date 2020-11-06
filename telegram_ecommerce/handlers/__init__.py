from .add_category import add_category
from .start import start
from .help import help_command
from .register import register


all_handlers = [
    start,
    help_command,
    register,
    add_category] 


