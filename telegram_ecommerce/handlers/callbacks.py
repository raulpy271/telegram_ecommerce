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
    update.message.reply_text(
        TEXT["ask_if_want_create_a_password"], 
        reply_markup=login_keyboard["step_1"])


def show_categories_callback(update, context):
    pass


