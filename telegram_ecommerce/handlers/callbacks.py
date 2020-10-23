

def start_callback(update, context):
    text = (
"""hello, I'm a bot that will help you buy products in this e-commerce. 
type \show_categories to see products by category.
type \login to autenticate your account.
type \help for more information.""")
    update.message.reply_text(text)


def help_callback(update, context):
    text = (
"""hello, I'm a bot that will help you buy products in this e-commerce. 
type \show_categories to see products by category.
Or type \help for more information.""")
    update.message.reply_text(text)


def show_categories_callback(update, context):
    pass


