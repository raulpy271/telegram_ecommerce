from .add_category import add_category
from .start import start
from .help import help_command
from .register import (
    register_step_1,
    register_step_2,
    register_step_3,
    register_step_3_numeric,
    register_step_4) 


all_handlers = [
    start,
    help_command,
    register_step_1,
    register_step_2,
    register_step_3,
    register_step_3_numeric,
    register_step_4,
    add_category] 


