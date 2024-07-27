from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..filters.decorators import execute_if_user_exist
from ..tamplates.buttons import tamplate_for_show_a_list_of_products
from ..tamplates.buy_callbacks import send_a_shipping_message
from ..database.query import search_products
from ..language import get_text
from ..tamplates.products import (
    send_a_product,
    send_a_detailed_product,
    send_a_inline_with_a_list_of_products,
    get_text_for_product,
    ListProductIterator)


(END                            ,
ASK_FOR_TERM_TO_SEARCH          ,
GET_LIST_OF_PRODUCTS            ,
SHOW_LIST_OF_PRODUCT_THAT_MATCH ,
BUY_PROCESS                     ) = range(-1, 4)


products_data_key = "list_of_products"
products_data = {
    'products' : []}


pattern_identifier = "response_from_buttons_in_products_that_match"
PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT = 'previus_product'
PATTERN_TO_CATCH_THE_NEXT_PRODUCT = 'next_product'
PATTERN_TO_CATCH_THE_VIEW_DETAILS = 'product_details'
PATTERN_TO_CATCH_THE_BUY_BUTTON = 'buy_product'


def put_products_data_in_user_data(user_data):
    user_data[products_data_key] = products_data


def save_products_in_user_data(user_data, string_to_search):
    products_from_a_search_query = search_products(string_to_search)
    products = ListProductIterator.create_a_list_from_a_query(
        products_from_a_search_query)
    user_data[products_data_key]["products"] = products


async def ask_for_term_to_search(update, context):
    put_products_data_in_user_data(context.user_data)
    text = get_text("ask_for_term_to_search", context)
    await update.message.reply_text(text)
    return GET_LIST_OF_PRODUCTS


async def get_list_of_products_that_match(update, context):
    string_to_search = update.message.text
    save_products_in_user_data(context.user_data, string_to_search)
    if not context.user_data[products_data_key]["products"].is_empty():
        text = get_text("OK", context)
        await update.message.reply_text(text)
        await show_list_of_product_that_match(update, context)
        return SHOW_LIST_OF_PRODUCT_THAT_MATCH
    else:
        text = get_text("without_product_in_this_search", context)
        await update.message.reply_text(text)
        await cancel_search(update, context)
        return END


async def show_list_of_product_that_match(update, context):
    product = context.user_data[products_data_key]["products"].next()
    markup = tamplate_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    await update.message.reply_photo(
        product.image_id,
        caption = text,
        reply_markup=markup) 
    return SHOW_LIST_OF_PRODUCT_THAT_MATCH


async def catch_previus(update, context):
    product = context.user_data[products_data_key]["products"].previus()
    await send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCT_THAT_MATCH


async def catch_next(update, context):
    product = context.user_data[products_data_key]["products"].next()
    await send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCT_THAT_MATCH


async def catch_details(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    await send_a_detailed_product(update, context, product, pattern_identifier)
    return BUY_PROCESS 


@execute_if_user_exist
async def send_a_shipping_message_callback(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    await send_a_shipping_message(update, context, product, pattern_identifier)
    return END


async def cancel_search(update, context):
    text = get_text("canceled_operation", context)
    await update.message.reply_text(text) 
    return END


search_command = (
    CommandHandler("search", ask_for_term_to_search))


search = ConversationHandler(
    entry_points = [search_command],
    states = {
        ASK_FOR_TERM_TO_SEARCH : [
            MessageHandler(
                filters.TEXT,
                ask_for_term_to_search)
            ],
        GET_LIST_OF_PRODUCTS : [
            MessageHandler(
                filters.TEXT, 
                get_list_of_products_that_match)
            ],
        SHOW_LIST_OF_PRODUCT_THAT_MATCH : [
            MessageHandler(
                filters.TEXT, 
                show_list_of_product_that_match),
            CallbackQueryHandler(
                catch_next, 
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_NEXT_PRODUCT),
            CallbackQueryHandler(
                catch_previus, 
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT),
            CallbackQueryHandler(
                catch_details,
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_VIEW_DETAILS)
            ],
        BUY_PROCESS : [
            CallbackQueryHandler(
                catch_previus, 
                pattern = pattern_identifier +
                PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT),
            CallbackQueryHandler(
                send_a_shipping_message_callback, 
                pattern = pattern_identifier + 
                PATTERN_TO_CATCH_THE_BUY_BUTTON)
            ]
        },
    fallbacks = [MessageHandler(filters.ALL, cancel_search)]
    )


