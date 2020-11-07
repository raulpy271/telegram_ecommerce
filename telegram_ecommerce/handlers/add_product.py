from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..utils.consts import TEXT
from ..tamplates.messages import ask_a_boolean_question
from ..database.query import get_category_id_from_name
from ..utils.utils import float_from_user_input
from ..database.manipulation import (
    add_product as add_product_in_db,
    add_photo)


(END                      ,
ASK_FOR_PRODUCT_PRICE     ,
ASK_FOR_QUANTITY_IN_STOCK ,
ASK_FOR_CATEGORY_NAME     ,
ASK_FOR_PRODUCT_PHOTO     ,
ASK_IF_ITS_ALL_OK         ) = range(-1, 5)


product_data_key = "product_data"
product_data = {
    "name"               : "",
    "unit_price"         : 0,
    "rating"             : 0,
    "quantity_in_stock"  : 0,
    "quantity_purchased" : 0,
    "category_id"        : 0,
    "photo"              : None}


pattern_to_save_everything = "boolean_response"


def put_product_data_in_user_data(user_data):
    user_data[product_data_key] = product_data


def delete_product_data_from_user_data(user_data):
    del user_data[product_data_key] 


def save_name_in_user_data(user_data, name):
    user_data[product_data_key]["name"] = name


def save_price_in_user_data(user_data, price):
    user_data[product_data_key]["unit_price"] = price


def save_quantity_in_stock_in_user_data(user_data, quantity):
    quantity = float_from_user_input(quantity)
    user_data[product_data_key]["quantity_in_stock"] = quantity


def save_category_id_in_user_data(user_data, category_name):
    category_id = get_category_id_from_name(category_name)
    user_data[product_data_key]["category_id"] = category_id


def save_photo_in_user_data(update, context):
    photo = update.message.photo[0]
    photo = photo.get_file()
    context.user_data[product_data_key]["photo"] = photo


def save_category_info_in_db(update, context):
    category_data = context.user_data[product_data_key] 
    photo = category_data["photo"]
    add_photo(
        photo.file_id,
        photo.download_as_bytearray())
    add_product_in_db(
        category_data["name"],
        category_data["unit_price"],
        category_data["rating"],
        category_data["quantity_in_stock"],
        category_data["quantity_purchased"],
        category_data["category_id"],
        photo.file_id)


def ask_for_product_name(update, context):
    put_product_data_in_user_data(context.user_data)
    text = TEXT["ask_for_product_name"]
    update.message.reply_text(text)
    return ASK_FOR_PRODUCT_PRICE


def ask_for_product_price(update, context):
    save_name_in_user_data(context.user_data, update.message.text)
    text = TEXT["ask_for_product_price"]
    update.message.reply_text(text)
    return ASK_FOR_QUANTITY_IN_STOCK


def ask_for_quantity_in_stock(update, context):
    save_price_in_user_data(context.user_data, update.message.text)
    text = TEXT["ask_for_quantity_in_stock"]
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_NAME


def ask_for_category_name(update, context):
    save_quantity_in_stock_in_user_data(
        context.user_data, update.message.text)
    text = TEXT["ask_for_category_name_of_the_product"]
    update.message.reply_text(text)
    return ASK_FOR_PRODUCT_PHOTO


def ask_for_product_photo(update, context):
    save_category_id_in_user_data(context.user_data, update.message.text)
    text = TEXT["ask_for_product_photo"]
    update.message.reply_text(text)
    return ASK_IF_ITS_ALL_OK


def ask_if_its_all_ok(update, context):
    save_photo_in_user_data(update, context)
    ask_a_boolean_question(update, context, pattern_to_save_everything)


def catch_response(update, context):
    query = update.callback_query
    if query.data == pattern_to_save_everything + "OK":
        save_category_info_in_db(update, context)
        text = TEXT["information_stored"]
    else:
        text = TEXT["canceled_operation"]
    query.edit_message_text(text)
    delete_product_data_from_user_data(context.user_data)
    return END


def cancel_add_product(update, context):
    delete_product_data_from_user_data(context.user_data)
    text = TEXT["canceled_operation"]
    update.message.reply_text(text)
    return END


add_product_command = (
    CommandHandler("add_product", ask_for_product_name))


add_product = ConversationHandler(
    entry_points = [add_product_command],
    states = {
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


