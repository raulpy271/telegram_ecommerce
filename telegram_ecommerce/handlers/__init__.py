from .add_category import add_category
from .register import (
    register_step_1,
    register_step_2,
    register_step_3,
    register_step_3_numeric,
    register_step_4) 


all_handlers = [
    register_step_1,
    register_step_2,
    register_step_3,
    register_step_3_numeric,
    register_step_4,
    add_category] 


