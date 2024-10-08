from telegram.ext import (
    filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler)

from telegram_ecommerce.language import get_text
from telegram_ecommerce.tamplates.buttons import login_keyboard
from telegram_ecommerce.filters.decorators import execute_if_user_dont_exist
from telegram_ecommerce.database.query import get_password
from telegram_ecommerce.database.manipulation import (
    hash_user_password,
    append_password,
    create_account, 
    delete_account)


(END, RUNING) = [-1, 1]


PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD = "register_step_1_"
PATTERN_TO_CATCH_THE_DIGITS                           = "register_step_2_"
PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD    = "register_step_3_"


@execute_if_user_dont_exist
async def start_register(update, context):
    user_id = update.effective_user.id
    await register_callback(update, context)
    return RUNING


async def register_callback(update, context):
    markup = login_keyboard(
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD,
        context)["step_1"]
    await update.message.reply_text(
        get_text("ask_if_want_create_a_password", context), 
        reply_markup=markup)
    return RUNING


async def register_callback_query_step_2(update, context):
    query = update.callback_query
    if query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD +
        "cancel_loging_process"):
        await cancel_register(update, context)
    elif query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD +
        "next_step_1_login_process"): 
        create_account(query.from_user)
        markup = login_keyboard(
            PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
        await query.edit_message_text(
            get_text("type_password", context), 
            reply_markup=markup)
        return RUNING
    return END


async def register_callback_query_step_3(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    if query.data == (
        PATTERN_TO_CATCH_THE_DIGITS + "cancel_numeric_keyboard"):
        delete_account(user_id)
        await cancel_register(update, context)
    elif query.data == (
        PATTERN_TO_CATCH_THE_DIGITS + "end_numeric_keyboard"): 
        markup = login_keyboard(
            PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD,
            context)["step_3"]
        password = get_password(user_id)
        await query.edit_message_text(
            "\"" + password + "\", " + 
            get_text("this_are_the_typed_password", context) + 
            get_text("ask_if_its_all_ok", context), 
            reply_markup=markup)
        return RUNING
    elif PATTERN_TO_CATCH_THE_DIGITS + "digit_" in query.data: 
        await register_callback_query_number_in_numeric_keyboard(update, context)
        return RUNING
    return END


async def register_callback_query_number_in_numeric_keyboard(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    digit = query.data.replace(PATTERN_TO_CATCH_THE_DIGITS + "digit_", "")
    append_password(user_id, digit)
    markup = login_keyboard(PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
    await query.edit_message_text(
        get_text("typing", context) + get_password(user_id),
        reply_markup=markup)
    return RUNING


async def register_callback_query_step_4(update, context):
    query = update.callback_query
    if query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD +
        "cancel_loging_process"):
        user_id = query.from_user.id
        delete_account(user_id)
        await cancel_register(update, context)
    elif query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD + 
        "end_login_process"):
        await query.edit_message_text(get_text("user_password_has_stored", context))
        user_id = query.from_user.id
        hash_user_password(user_id)
    return END


async def cancel_register(update, context):
    query = update.callback_query
    if update.message:
        await update.message.reply_text(get_text("canceled_operation", context))
    elif query:
        await query.edit_message_text(get_text("canceled_operation", context))
    return END


register_command = (
    CommandHandler("register", start_register))


register = ConversationHandler(
    entry_points = [register_command],
    states = {
        RUNING : [
        MessageHandler(
            filters.ALL,
            register_callback
            ),
        CallbackQueryHandler(
            register_callback_query_step_2,
            pattern=PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD
            ),
        CallbackQueryHandler(
            register_callback_query_step_3,
            pattern=PATTERN_TO_CATCH_THE_DIGITS
            ),
        CallbackQueryHandler(
            register_callback_query_step_4,
            pattern=PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD
            )
        ]
    },
    fallbacks = [MessageHandler(filters.ALL, cancel_register)],
    )


