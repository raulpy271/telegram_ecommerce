from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..language import get_text
from ..tamplates.messages import ask_a_boolean_question
from ..database.manipulation import (
    add_category as add_category_in_db,
    add_photo)


(END                         ,
ASK_FOR_CATEGORY_DESCRIPTION ,
ASK_FOR_CATEGORY_TAGS        ,
ASK_FOR_CATEGORY_PHOTO       ,
ASK_IF_ITS_ALL_OK            ) = range(-1, 4)


category_data_key = "category_data"
category_data = {
    "name"        : "",
    "description" : "",
    "tags"        : "",
    "photo"       : ""}


pattern_to_save_everything = "boolean_response"


def put_category_data_in_user_data(user_data):
    user_data[category_data_key] = category_data


def delete_category_data_from_user_data(user_data):
    user_data[category_data_key] = {}


def save_name_in_user_data(user_data, name):
    user_data[category_data_key]["name"] = name


def save_description_in_user_data(user_data, description):
    user_data[category_data_key]["description"] = description


def save_tags_in_user_data(user_data, tags):
    user_data[category_data_key]["tags"] = tags


def save_photo_in_user_data(update, context):
    photo = update.message.photo[0]
    photo = photo.get_file()
    context.user_data[category_data_key]["photo"] = photo


def save_category_info_in_db(update, context):
    category_data = context.user_data[category_data_key] 
    photo = category_data["photo"]
    add_photo(
        photo.file_id,
        photo.download_as_bytearray())
    add_category_in_db(
        category_data["name"],
        category_data["description"],
        category_data["tags"],
        photo.file_id)


def ask_for_category_name(update, context):
    put_category_data_in_user_data(context.user_data)
    text = get_text("ask_for_category_name", context)
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_DESCRIPTION


def ask_for_category_description(update, context):
    save_name_in_user_data(context.user_data, update.message.text)
    text = get_text("ask_for_category_description", context)
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_TAGS


def ask_for_category_tags(update, context):
    save_description_in_user_data(context.user_data, update.message.text)
    text = get_text("ask_for_category_tags", context)
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_PHOTO


def ask_for_category_photo(update, context):
    save_tags_in_user_data(context.user_data, update.message.text)
    text = get_text("ask_for_category_photo", context)
    update.message.reply_text(text)
    return ASK_IF_ITS_ALL_OK


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
        save_category_info_in_db(update, context)
        text = get_text("information_stored", context)
    else:
        text = get_text("canceled_operation", context)
    query.edit_message_text(text)
    return END


def cancel_add_category(update, context):
    delete_category_data_from_user_data(context.user_data)
    text = get_text("canceled_operation", context)
    update.message.reply_text(text)
    return END


add_category_command = (
    CommandHandler("add_category", ask_for_category_name))


add_category = ConversationHandler(
    entry_points = [add_category_command],
    states = {
        ASK_FOR_CATEGORY_DESCRIPTION : [
            MessageHandler(
                Filters.text, 
                ask_for_category_description)
            ],
        ASK_FOR_CATEGORY_TAGS : [
            MessageHandler(
                Filters.text, 
                ask_for_category_tags)
            ],
        ASK_FOR_CATEGORY_PHOTO : [
            MessageHandler(
                Filters.text, 
                ask_for_category_photo)
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
    fallbacks = [MessageHandler(Filters.all, cancel_add_category)]
    )


