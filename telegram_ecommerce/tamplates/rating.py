from telegram.ext import CallbackQueryHandler

from telegram_ecommerce.language import get_text
from telegram_ecommerce.tamplates.messages import ask_a_boolean_question, send_a_rating_message
from telegram_ecommerce.database.manipulation import add_rating_to_an_order


PATTERN_TO_CATCH_THE_RATE = "rate_response_"
PATTERN_TO_CATCH_IF_USER_WANT_RATE_THE_PRODUCT = (
    "response_if_want_rate_product_")


def store_rating_response(context, rating):
    pre_checkout_query = context.user_data["last_order"] 
    order_id = pre_checkout_query.id
    add_rating_to_an_order(order_id, rating)


async def ask_if_user_want_avaluate_the_product(update, context, product):
    await ask_a_boolean_question(
        update, 
        context,
        PATTERN_TO_CATCH_IF_USER_WANT_RATE_THE_PRODUCT,
        get_text("ask_if_user_want_avaluate_the_product", context))


async def catch_the_response_if_user_want_evaluate(update, context):
    query = update.callback_query
    if query.data == (PATTERN_TO_CATCH_IF_USER_WANT_RATE_THE_PRODUCT + 'OK'):
        await send_a_rating_message(
            update, 
            context,
            PATTERN_TO_CATCH_THE_RATE)
    elif query.data == (
        PATTERN_TO_CATCH_IF_USER_WANT_RATE_THE_PRODUCT + 'cancel'):
        await query.edit_message_text(get_text("OK", context))


async def catch_the_rating_response_callback(update, context):
    query = update.callback_query
    try:
        rating = int(query.data.replace(PATTERN_TO_CATCH_THE_RATE, ""))
        store_rating_response(context, rating)
        await query.edit_message_text(get_text("thanks_opinion", context))
    except: 
        await query.edit_message_text(get_text("canceled_operation", context))


catch_the_response_if_user_want_evaluate_handler = CallbackQueryHandler(
    catch_the_response_if_user_want_evaluate, 
    pattern = PATTERN_TO_CATCH_IF_USER_WANT_RATE_THE_PRODUCT)


catch_the_rating_handler = CallbackQueryHandler(
    catch_the_rating_response_callback, 
    pattern = PATTERN_TO_CATCH_THE_RATE)


rating_precess_handlers = [catch_the_rating_handler,
    catch_the_response_if_user_want_evaluate_handler]


