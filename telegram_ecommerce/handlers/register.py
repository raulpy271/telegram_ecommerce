"""Registration with a temporary in-memory PIN draft and a hashed database value."""

from telegram.ext import (
    filters, ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler,
)

from telegram_ecommerce.language import get_text
from telegram_ecommerce.tamplates.buttons import login_keyboard
from telegram_ecommerce.database.query import user_exist
from telegram_ecommerce.database.manipulation import create_account


(END, RUNING) = [-1, 1]
PIN_KEY = "registration_pin"
MIN_PIN_LENGTH = 6
MAX_PIN_LENGTH = 12

PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD = "register_step_1_"
PATTERN_TO_CATCH_THE_DIGITS = "register_step_2_"
PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD = "register_step_3_"


async def start_register(update, context):
    if user_exist(update.effective_user.id):
        await update.message.reply_text(get_text("user_have_account", context))
        return END
    context.user_data.pop(PIN_KEY, None)
    return await register_callback(update, context)


async def register_callback(update, context):
    markup = login_keyboard(
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD, context,
    )["step_1"]
    await update.message.reply_text(
        get_text("ask_if_want_create_a_password", context), reply_markup=markup,
    )
    return RUNING


async def register_callback_query_step_2(update, context):
    query = update.callback_query
    if query.data == PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD + "cancel_loging_process":
        return await cancel_register(update, context)
    if query.data == PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD + "next_step_1_login_process":
        context.user_data[PIN_KEY] = ""
        markup = login_keyboard(PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
        await query.edit_message_text(get_text("type_password", context), reply_markup=markup)
        return RUNING
    return END


async def register_callback_query_step_3(update, context):
    query = update.callback_query
    if query.data == PATTERN_TO_CATCH_THE_DIGITS + "cancel_numeric_keyboard":
        return await cancel_register(update, context)
    if query.data == PATTERN_TO_CATCH_THE_DIGITS + "end_numeric_keyboard":
        pin = context.user_data.get(PIN_KEY, "")
        if len(pin) < MIN_PIN_LENGTH:
            markup = login_keyboard(PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
            await query.edit_message_text(
                get_text("pin_too_short", context), reply_markup=markup,
            )
            return RUNING
        markup = login_keyboard(
            PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD, context,
        )["step_3"]
        await query.edit_message_text(
            get_text("pin_confirmation", context).format(length=len(pin)),
            reply_markup=markup,
        )
        return RUNING
    if query.data.startswith(PATTERN_TO_CATCH_THE_DIGITS + "digit_"):
        return await register_callback_query_number_in_numeric_keyboard(update, context)
    return END


async def register_callback_query_number_in_numeric_keyboard(update, context):
    query = update.callback_query
    digit = query.data.removeprefix(PATTERN_TO_CATCH_THE_DIGITS + "digit_")
    pin = context.user_data.get(PIN_KEY)
    if pin is None or len(digit) != 1 or digit not in "0123456789":
        return END
    if len(pin) >= MAX_PIN_LENGTH:
        text = get_text("pin_too_long", context)
    else:
        pin += digit
        context.user_data[PIN_KEY] = pin
        text = get_text("typing", context) + "•" * len(pin)
    markup = login_keyboard(PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
    await query.edit_message_text(text, reply_markup=markup)
    return RUNING


async def register_callback_query_step_4(update, context):
    query = update.callback_query
    if query.data == PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD + "cancel_loging_process":
        return await cancel_register(update, context)
    if query.data == PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD + "end_login_process":
        pin = context.user_data.pop(PIN_KEY, None)
        if pin is None or not MIN_PIN_LENGTH <= len(pin) <= MAX_PIN_LENGTH or not pin.isascii() or not pin.isdigit():
            await query.edit_message_text(get_text("canceled_operation", context))
            return END
        if user_exist(query.from_user.id):
            await query.edit_message_text(get_text("user_have_account", context))
            return END
        create_account(query.from_user, pin)
        await query.edit_message_text(get_text("user_password_has_stored", context))
    return END


async def cancel_register(update, context):
    context.user_data.pop(PIN_KEY, None)
    query = update.callback_query
    if update.message:
        await update.message.reply_text(get_text("canceled_operation", context))
    elif query:
        await query.edit_message_text(get_text("canceled_operation", context))
    return END


register_command = CommandHandler("register", start_register)
register = ConversationHandler(
    entry_points=[register_command],
    states={RUNING: [
        MessageHandler(filters.ALL, cancel_register),
        CallbackQueryHandler(register_callback_query_step_2, pattern=PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD),
        CallbackQueryHandler(register_callback_query_step_3, pattern=PATTERN_TO_CATCH_THE_DIGITS),
        CallbackQueryHandler(register_callback_query_step_4, pattern=PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD),
    ]},
    fallbacks=[MessageHandler(filters.ALL, cancel_register)],
)
