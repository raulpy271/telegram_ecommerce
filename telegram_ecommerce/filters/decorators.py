
from functools import wraps

from telegram_ecommerce.language import get_text
from telegram_ecommerce.database.query import user_exist
from telegram_ecommerce.utils.consts import admins


END = -1


async def warning_the_user_that_already_have_an_account(update, context):
    text = get_text("user_have_account", context)
    await update.message.reply_text(text)
    return END


async def warning_the_user_that_he_dont_have_an_account(update, context):
    text = get_text("user_dont_have_account", context)
    await update.effective_message.reply_text(text)
    return END


def execute_if_user_exist(callback):
    @wraps(callback)
    async def execute_warning_if_user_dont_exist(update, context):
        user_id = update.effective_user.id
        if user_exist(user_id):
            return await callback(update, context)

        return await warning_the_user_that_he_dont_have_an_account(update, context)
    return execute_warning_if_user_dont_exist


def execute_if_user_dont_exist(callback):
    @wraps(callback)
    async def execute_warning_if_user_exist(update, context):
        user_id = update.effective_user.id
        if user_exist(user_id):
            return await warning_the_user_that_already_have_an_account(
                update, context)
        return await callback(update, context)
    return execute_warning_if_user_exist


def execute_if_admin(callback):
    @wraps(callback)
    async def check_admin(update, context):
        user_id = update.effective_user.id
        if user_id in admins and user_exist(user_id):
            return await callback(update, context)
        await update.effective_message.reply_text(get_text("admin_only", context))
        return END
    return check_admin


