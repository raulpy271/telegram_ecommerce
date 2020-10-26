from ..utils.consts import TEXT
from ..database.query import is_admin
from ..tamplates.buttons import login_keyboard

def start_callback(update, context):
    text = TEXT["start"]
    update.message.reply_text(text)


def help_callback(update, context):
    text = TEXT["help"]
    user = update.effective_user
    user_is_admin = is_admin(user.id)
    if user_is_admin:
        text += TEXT["help_admin"]
    update.message.reply_text(text)


def register_callback(update, context):
    pattern_identifier = "register_step_1_"
    markup = login_keyboard(pattern_identifier)["step_1"]
    update.message.reply_text(
        TEXT["ask_if_want_create_a_password"], 
        reply_markup=markup)


def register_callback_query_step_2(update, context):
    query = update.callback_query
    if query.data == "register_step_1_cancel_loging_process":
        query.edit_message_text(TEXT["canceled_operation"])
    elif query.data == "register_step_1_next_step_1_login_process": 
        pattern_identifier = "register_step_2_"
        markup = login_keyboard(pattern_identifier)["step_2"]
        query.edit_message_text(
            TEXT["type_password"], 
            reply_markup=markup)
    else: 
        return


def register_callback_query_step_3(update, context):
    query = update.callback_query
    if query.data == "register_step_2_cancel_numeric_keyboard":
        query.edit_message_text(TEXT["canceled_operation"])
    elif query.data == "register_step_2_end_numeric_keyboard": 
        pattern_identifier = "register_step_3_"
        markup = login_keyboard(pattern_identifier)["step_3"]
        password = "1234"
        query.edit_message_text(
            password + 
            TEXT["this_are_the_typed_password"] + 
            TEXT["ask_if_its_all_ok"], 
            reply_markup=markup)
    else: 
        return

def show_categories_callback(update, context):
    pass


