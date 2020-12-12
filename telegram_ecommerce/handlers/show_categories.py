from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..language import get_text
from ..filters.decorators import execute_if_user_exist
from ..tamplates.buttons import tamplate_for_show_a_list_of_products
from ..tamplates.buy_callbacks import send_a_shipping_message
from ..database.query import (
    get_all_available_by_category_name,
    get_name_of_all_categories)
from ..tamplates.products import (
    send_a_product,
    send_a_detailed_product,
    send_a_inline_with_a_list_of_products,
    get_text_for_product,
    ListProductIterator)


(END                  ,
ASK_FOR_CATEGORY_NAME , 
GET_LIST_OF_PRODUCTS  ,
SHOW_LIST_OF_PRODUCTS ,
BUY_PROCESS           ) = range(-1, 4)


products_data_key = "list_of_products"
products_data = {
    'products' : []}


pattern_identifier = "pattern_to_catch_response_from_callbacks"
PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT = 'previus_product'
PATTERN_TO_CATCH_THE_NEXT_PRODUCT = 'next_product'
PATTERN_TO_CATCH_THE_VIEW_DETAILS = 'product_details'
PATTERN_TO_CATCH_THE_BUY_BUTTON = 'buy_product'


def put_products_data_in_user_data(user_data):
    user_data[products_data_key] = products_data


def save_products_in_user_data(user_data, message):
    products_from_a_category_query = (
        get_all_available_by_category_name(message))
    products = ListProductIterator.create_a_list_from_a_query(
        products_from_a_category_query)
    user_data[products_data_key]["products"] = products


def delete_list_of_products(user_data):
    user_data[products_data_key] = {}


def ask_for_category_name(update, context):
    put_products_data_in_user_data(context.user_data)
    text = get_text("ask_for_category_name_of_the_product", context)
    name_of_all_categories = get_name_of_all_categories()
    if name_of_all_categories:
        send_a_inline_with_a_list_of_products(
            update, 
            context, 
            text,
            name_of_all_categories)
        return GET_LIST_OF_PRODUCTS
    else:
        update.message.reply_text(get_text("stock_empty", context))
        return END


def get_list_of_products(update, context):
    category_name = update.message.text
    name_of_all_categories = get_name_of_all_categories()
    if category_name in name_of_all_categories:
        save_products_in_user_data(context.user_data, category_name)
        if not context.user_data[products_data_key]["products"].is_empty():
            text = get_text("OK", context)
            update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
            show_list_of_products(update, context)
            return SHOW_LIST_OF_PRODUCTS
        else:
            text = get_text("without_product_in_this_category", context)
    else:
        text = get_text("this_is_not_a_valid_category", context)
    update.message.reply_text(text)
    cancel_show_categories(update, context)
    return END


def show_list_of_products(update, context):
    product = context.user_data[products_data_key]["products"].next()
    markup = tamplate_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    update.message.reply_photo(
        product.image_id,
        caption = text,
        reply_markup=markup) 
    return SHOW_LIST_OF_PRODUCTS


def catch_previus(update, context):
    product = context.user_data[products_data_key]["products"].previus()
    send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCTS


def catch_next(update, context):
    product = context.user_data[products_data_key]["products"].next()
    send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCTS


def catch_details(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    send_a_detailed_product(update, context, product, pattern_identifier)
    return BUY_PROCESS 


@execute_if_user_exist
def send_a_shipping_message_callback(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    send_a_shipping_message(update, context, product, pattern_identifier)
    return END


def cancel_show_categories(update, context):
    delete_list_of_products(context.user_data)
    query = update.callback_query
    if update.message:
        update.message.reply_text(
            get_text("canceled_operation", context),
            reply_markup = ReplyKeyboardRemove()
            )
    elif query:
        query.edit_message_text(
            get_text("canceled_operation", context),
            reply_markup = ReplyKeyboardRemove()
            )
    return END


show_categories_command = CommandHandler("show_categories",
    ask_for_category_name)


show_categories = ConversationHandler(
    entry_points = [show_categories_command],
    states = {
        ASK_FOR_CATEGORY_NAME : [
            MessageHandler(
                Filters.text, 
                ask_for_category_name)
            ],
        GET_LIST_OF_PRODUCTS : [
            MessageHandler(
                Filters.text, 
                get_list_of_products)
            ],
        SHOW_LIST_OF_PRODUCTS : [
            MessageHandler(
                Filters.text, 
                show_list_of_products
                ),
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
    fallbacks = [MessageHandler(Filters.all, cancel_show_categories)]
    )


