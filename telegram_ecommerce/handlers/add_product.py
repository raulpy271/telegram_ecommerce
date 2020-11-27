from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..language import get_text
from ..tamplates.messages import ask_a_boolean_question
from ..tamplates.buttons import get_list_of_buttons
from ..utils.utils import float_from_user_input
from ..database.query import (
    get_category_id_from_name,
    get_name_of_all_categories)
from ..database.manipulation import (
    add_product as add_product_in_db,
    add_photo)


(END                        ,
ASK_FOR_PRODUCT_DESCRIPTION ,
ASK_FOR_PRODUCT_PRICE       ,
ASK_FOR_QUANTITY_IN_STOCK   ,
ASK_FOR_CATEGORY_NAME       ,
ASK_FOR_PRODUCT_PHOTO       ,
ASK_IF_ITS_ALL_OK           ) = range(-1, 6)


product_data_key = "product_data"
product_data = {
    "name"               : "",
    "description"        : "",
    "unit_price"         : 0,
    "quantity_in_stock"  : 0,
    "quantity_purchased" : 0,
    "category_id"        : 0,
    "photo"              : None}


pattern_to_save_everything = "boolean_response"


def put_product_data_in_user_data(user_data):
    user_data[product_data_key] = product_data


def delete_product_data_from_user_data(user_data):
    user_data[product_data_key] = {}


def save_name_in_user_data(user_data, name):
    user_data[product_data_key]["name"] = name


def save_description_in_user_data(user_data, description):
    user_data[product_data_key]["description"] = description


def save_price_in_user_data(user_data, price):
    price = float_from_user_input(price)
    user_data[product_data_key]["unit_price"] = price


def save_quantity_in_stock_in_user_data(user_data, quantity):
    user_data[product_data_key]["quantity_in_stock"] = int(quantity)


def save_category_id_in_user_data(user_data, category_name):
    category_id = get_category_id_from_name(category_name)
    user_data[product_data_key]["category_id"] = category_id


def save_photo_in_user_data(update, context):
    photo = update.message.photo[0]
    photo = photo.get_file()
    context.user_data[product_data_key]["photo"] = photo


def save_product_info_in_db(update, context):
    product_data = context.user_data[product_data_key] 
    photo = product_data["photo"]
    add_photo(
        photo.file_id,
        photo.download_as_bytearray())
    add_product_in_db(
        product_data["name"],
        product_data["description"],
        product_data["unit_price"],
        product_data["quantity_in_stock"],
        product_data["quantity_purchased"],
        product_data["category_id"],
        photo.file_id)


def ask_for_product_name(update, context):
    put_product_data_in_user_data(context.user_data)
    text = get_text("ask_for_product_name", context)
    update.message.reply_text(text)
    return ASK_FOR_PRODUCT_DESCRIPTION


def ask_for_product_description(update, context):
    save_name_in_user_data(context.user_data, update.message.text)
    text = get_text("ask_for_product_description", context)
    update.message.reply_text(text)
    return ASK_FOR_PRODUCT_PRICE


def ask_for_product_price(update, context):
    save_description_in_user_data(context.user_data, update.message.text)
    text = get_text("ask_for_product_price", context)
    update.message.reply_text(text)
    return ASK_FOR_QUANTITY_IN_STOCK


def ask_for_quantity_in_stock(update, context):
    try:
        save_price_in_user_data(context.user_data, update.message.text)
        text = get_text("ask_for_quantity_in_stock", context)
        update.message.reply_text(text)
        return ASK_FOR_CATEGORY_NAME
    except:
        text = get_text("this_is_not_a_number", context)
        update.message.reply_text(text)
        cancel_add_product(update, context)
        return END


def ask_for_category_name(update, context):
    try:
        save_quantity_in_stock_in_user_data(
            context.user_data, update.message.text)
        text = get_text("ask_for_category_name_of_the_product", context)
        buttons_with_list_of_all_names = (
            get_list_of_buttons(*(get_name_of_all_categories())))
        update.message.reply_text(text, 
            reply_markup=buttons_with_list_of_all_names)
        return ASK_FOR_PRODUCT_PHOTO
    except:
        text = get_text("this_is_not_a_integer", context)
        update.message.reply_text(text)
        cancel_add_product(update, context)
        return END


def ask_for_product_photo(update, context):
    try:
        save_category_id_in_user_data(context.user_data, update.message.text)
        text = get_text("ask_for_product_photo", context)
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return ASK_IF_ITS_ALL_OK
    except:
        text = get_text("this_is_not_a_valid_category", context)
        update.message.reply_text(text)
        cancel_add_product(update, context)
        return END


def ask_if_its_all_ok(update, context):
    try:
        save_photo_in_user_data(update, context)
        ask_a_boolean_question(update, context, pattern_to_save_everything)
    except:
        text = get_text("error_when_storing_photo", context)
        update.message.reply_text(text)
        cancel_add_product(update, context)
        return END


def catch_response(update, context):
    query = update.callback_query
    if query.data == pattern_to_save_everything + "OK":
        save_product_info_in_db(update, context)
        text = get_text("information_stored", context)
    else:
        text = get_text("canceled_operation", context)
    query.edit_message_text(text)
    delete_product_data_from_user_data(context.user_data)
    return END


def cancel_add_product(update, context):
    delete_product_data_from_user_data(context.user_data)
    text = get_text("canceled_operation", context)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return END


add_product_command = (
    CommandHandler("add_product", ask_for_product_name))


add_product = ConversationHandler(
    entry_points = [add_product_command],
    states = {
        ASK_FOR_PRODUCT_DESCRIPTION : [
            MessageHandler(
                Filters.text,
                ask_for_product_description)
            ],
        ASK_FOR_PRODUCT_PRICE : [
            MessageHandler(
                Filters.text, 
                ask_for_product_price)
            ],
        ASK_FOR_QUANTITY_IN_STOCK : [
            MessageHandler(
                Filters.text, 
                ask_for_quantity_in_stock)
            ],
        ASK_FOR_CATEGORY_NAME : [
            MessageHandler(
                Filters.text, 
                ask_for_category_name)
            ],
        ASK_FOR_PRODUCT_PHOTO : [
            MessageHandler(
                Filters.text, 
                ask_for_product_photo)
            ],
        ASK_IF_ITS_ALL_OK : [
            MessageHandler(
                Filters.photo,
                ask_if_its_all_ok),
            CallbackQueryHandler(
                catch_response,
                pattern=pattern_to_save_everything
                )
            ]
        },
    fallbacks = [MessageHandler(Filters.all, cancel_add_product)]
    )


