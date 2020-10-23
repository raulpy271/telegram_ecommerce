from ..utils.consts import text_en

def start_callback(update, context):
    text = text_en["start"]
    update.message.reply_text(text)


def help_callback(update, context):
    text = text_en["help"]
    user_is_admin = False
    if user_is_admin:
        text += text_en["help_admin"]
    update.message.reply_text(text)


def login(update, context):
    pass


def show_categories_callback(update, context):
    pass


