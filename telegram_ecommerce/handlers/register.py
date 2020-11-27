from telegram.ext import (
    Filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler)

from ..language import get_text
from ..tamplates.buttons import login_keyboard
from ..filters.decorators import execute_if_user_dont_exist
from ..database.query import (
    user_exist,
    get_password)
from ..database.manipulation import (
    hash_user_password,
    append_password,
    create_account, 
    delete_account)


(END, RUNING) = [-1, 1]


PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD = "register_step_1_"
PATTERN_TO_CATCH_THE_DIGITS                           = "register_step_2_"
PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD    = "register_step_3_"


@execute_if_user_dont_exist
def start_register(update, context):
    user_id = update.effective_user.id
    register_callback(update, context)
    return RUNING


def register_callback(update, context):
    markup = login_keyboard(
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD,
        context)["step_1"]
    update.message.reply_text(
        get_text("ask_if_want_create_a_password", context), 
        reply_markup=markup)
    return RUNING


def register_callback_query_step_2(update, context):
    query = update.callback_query
    if query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD +
        "cancel_loging_process"):
        cancel_register(update, context)
    elif query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_IF_USER_WANT_A_PASSWORD +
        "next_step_1_login_process"): 
        create_account(query.from_user)
        markup = login_keyboard(
            PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
        query.edit_message_text(
            get_text("type_password", context), 
            reply_markup=markup)
        return RUNING
    return END


def register_callback_query_step_3(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    if query.data == (
        PATTERN_TO_CATCH_THE_DIGITS + "cancel_numeric_keyboard"):
        delete_account(user_id)
        cancel_register(update, context)
    elif query.data == (
        PATTERN_TO_CATCH_THE_DIGITS + "end_numeric_keyboard"): 
        markup = login_keyboard(
            PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD,
            context)["step_3"]
        password = get_password(user_id)
        query.edit_message_text(
            "\"" + password + "\", " + 
            get_text("this_are_the_typed_password", context) + 
            get_text("ask_if_its_all_ok", context), 
            reply_markup=markup)
        return RUNING
    elif PATTERN_TO_CATCH_THE_DIGITS + "digit_" in query.data: 
        register_callback_query_number_in_numeric_keyboard(update, context)
        return RUNING
    return END


def register_callback_query_number_in_numeric_keyboard(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    digit = query.data.replace(PATTERN_TO_CATCH_THE_DIGITS + "digit_", "")
    append_password(user_id, digit)
    markup = login_keyboard(PATTERN_TO_CATCH_THE_DIGITS, context)["step_2"]
    query.edit_message_text(
        get_text("typing", context) + get_password(user_id),
        reply_markup=markup)
    return RUNING


def register_callback_query_step_4(update, context):
    query = update.callback_query
    if query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD +
        "cancel_loging_process"):
        user_id = query.from_user.id
        delete_account(user_id)
        cancel_register(update, context)
    elif query.data == (
        PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD + 
        "end_login_process"):
        query.edit_message_text(get_text("user_password_has_stored", context))
        user_id = query.from_user.id
        hash_user_password(user_id)
    return END


def cancel_register(update, context):
    query = update.callback_query
    if update.message:
        update.message.reply_text(get_text("canceled_operation", context))
    elif query:
        query.edit_message_text(get_text("canceled_operation", context))
    return END


register_command = (
    CommandHandler("register", start_register))


register = ConversationHandler(
    entry_points = [register_command],
    states = {
        RUNING : [
        MessageHandler(
            Filters.all,
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
    fallbacks = [MessageHandler(Filters.all, cancel_register)],
    )


