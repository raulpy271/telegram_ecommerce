from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..language import get_text
from ..tamplates.buttons import (
    get_list_of_buttons,
    tamplate_for_show_a_list_of_products)
from ..tamplates.products import (
    send_a_product,
    get_text_for_product,
    ListProductIterator)
from ..database.query import (
    get_products_by_category_name,
    get_name_of_all_categories)


(END                  ,
ASK_FOR_CATEGORY_NAME , 
GET_LIST_OF_PRODUCTS  ,
SHOW_LIST_OF_PRODUCTS ) = range(-1, 3)


products_data_key = "list_of_products"
products_data = {
    'products' : []}


pattern_identifier = "pattern_to_catch_response_from_callbacks"
PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT = 'previus_product'
PATTERN_TO_CATCH_THE_NEXT_PRODUCT = 'next_product'
PATTERN_TO_CATCH_THE_VIEW_DETAILS = 'product_details'


def put_products_data_in_user_data(user_data):
    user_data[products_data_key] = products_data


def save_products_in_user_data(user_data, products):
    user_data[products_data_key]["products"] = products


def delete_list_of_products(user_data):
    user_data[products_data_key] = {}


def ask_for_category_name(update, context):
    put_products_data_in_user_data(context.user_data)
    text = get_text("ask_for_category_name_of_the_product", context)
    buttons_with_list_of_all_names = (
        get_list_of_buttons(*(get_name_of_all_categories())))
    update.message.reply_text(text, 
        reply_markup=buttons_with_list_of_all_names)
    return GET_LIST_OF_PRODUCTS


def get_list_of_products(update, context):
    try:
        products_from_a_category_query = get_products_by_category_name(
            update.message.text)
        print(products_from_a_category_query)
        products = ListProductIterator.create_a_list_from_a_query(
            products_from_a_category_query)
        save_products_in_user_data(context.user_data, products)
        text = get_text("OK", context)
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return SHOW_LIST_OF_PRODUCTS
    except:
        text = get_text("this_is_not_a_valid_category", context)
        update.message.reply_text(text)
        cancel_show_categories(update, context)
        return END


def get_list_of_products(update, context):
    products_from_a_category_query = get_products_by_category_name(
        update.message.text)
    products = ListProductIterator.create_a_list_from_a_query(
        products_from_a_category_query)
    save_products_in_user_data(context.user_data, products)
    text = get_text("OK", context)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return SHOW_LIST_OF_PRODUCTS


def show_list_of_products(update, context):
    product = context.user_data[product_data_key]["products"].next()
    markup = tamplate_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    update.message.reply_photo(
        product.image_id,
        caption = text,
        reply_markup=markup) 
    return SHOW_LIST_OF_PRODUCTS


def catch_previus(update, context):
    product = context.user_data[product_data_key]["products"].previus()
    send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCTS


def catch_next(update, context):
    product = context.user_data[product_data_key]["products"].next()
    send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCTS


def catch_details(update, context):
    pass


def cancel_show_categories(update, context):
    delete_list_of_products(context.user_data)
    text = get_text("canceled_operation", context)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
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
                PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT)
            ]
        },
    fallbacks = [MessageHandler(Filters.all, cancel_show_categories)]
    )


