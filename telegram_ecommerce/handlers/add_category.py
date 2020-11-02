from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler)

from ..utils.consts import TEXT
from ..database.manipulation import add_category as add_category_in_db


(ASK_FOR_CATEGORY_NAME       ,
ASK_FOR_CATEGORY_DESCRIPTION ,
ASK_FOR_CATEGORY_TAGS        ,
ASK_FOR_CATEGORY_PHOTO       ,
ASK_IF_ITS_ALL_OK            ) = range(5)


def ask_for_category_name(update, context):
    text = TEXT["ask_for_category_name"]
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_DESCRIPTION


def ask_for_category_description(update, context):
    category_name = update.message.text
    context.user_data["category_name"] = category_name
    text = TEXT["ask_for_category_description"]
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_TAGS


def ask_for_category_tags(update, context):
    category_description = update.message.text
    context.user_data["category_description"] = category_description
    text = TEXT["ask_for_category_tags"]
    update.message.reply_text(text)
    return ASK_FOR_CATEGORY_PHOTO


def ask_for_category_photo(update, context):
    category_tags = update.message.text
    context.user_data["category_tags"] = category_tags
    text = TEXT["ask_for_category_photo"]
    update.message.reply_text(text)
    return ASK_IF_ITS_ALL_OK


def ask_if_its_all_ok(update, context):
    text = TEXT["OK"]
    update.message.reply_text(text)
    add_category_in_db(
        context.user_data["category_name"],
        context.user_data["category_description"],
        context.user_data["category_tags"])

    return ConversationHandler.END


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
                Filters.text, 
                ask_if_its_all_ok)
            ]
        },
    fallbacks = [
        MessageHandler(
            Filters.text, 
            ask_if_its_all_ok)
        ]

    )


