from telegram import (
    InlineKeyboardButton as InlineButton,
    InputMediaPhoto,
    InlineKeyboardMarkup)
from telegram.ext import (
    Filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler)

from ..language import get_text
from .buttons import tamplate_for_show_a_list_of_products


(END, RUNING) = [-1, 1]
PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT = 'previus_product'
PATTERN_TO_CATCH_THE_NEXT_PRODUCT = 'next_product'
PATTERN_TO_CATCH_THE_VIEW_DETAILS = 'product_details'


class Product():
    def __init__(
        self, 
        product_id,
        name,
        price, 
        rating,
        quantity_in_stock,
        quantity_purchased,
        category_id,
        image_id = None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.rating = rating
        self.quantity_in_stock = quantity_in_stock
        self.quantity_purchased = quantity_purchased
        self.category_id = category_id
        self.image_id = image_id


class ListProductIterator():
    def __init__(self, *list_of_products):
        self.list_of_products = list_of_products
        self.iter = -1 


    def next(self):
        self.__increment_iter__()
        actual_product = self.list_of_products[self.iter]
        return actual_product


    def previus(self):
        self.__decrement_iter__()
        actual_product = self.list_of_products[self.iter]
        return actual_product


    def __increment_iter__(self):
        if self.iter == len(self.list_of_products) - 1:
            self.iter = 0
        else: 
            self.iter += 1


    def __decrement_iter__(self):
        if self.iter <= 0:
            self.iter = len(self.list_of_products) - 1
        else:
            self.iter -= 1


def send_a_product(update, context, product, pattern_identifier):
    query = update.callback_query
    markup = tamplate_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    query.message.edit_media(
        media = InputMediaPhoto(product.image_id, text),
        reply_markup = markup)


def show_rating(rating):
    return str(rating)


def get_text_for_product(product, context):
    text = product.name + ", " + get_text("price", context) + \
           str(product.price) + '\n' + \
           get_text("rating", context) + show_rating(product.rating)
    return text


def get_text_for_detailed_product(product, context):
    text = product.name + ", " + get_text("price", context) + \
           str(product.price) + '\n' + \
           product.description + '\n' + \
           get_text("rating", context) + show_rating(product.rating) + '\n' + \
           get_text("purchased", context) + str(product.quantity_purchased)


def get_a_handler_with_a_list_of_products(products, pattern_identifier):


    def entry_point_callback(update, context):
        product = products.next()
        markup = tamplate_for_show_a_list_of_products(
            pattern_identifier, context)
        text = get_text_for_product(product, context)
        update.message.reply_photo(
            product.image_id,
            caption = text,
            reply_markup=markup) 
        return RUNING


    def catch_previus(update, context):
        product = products.previus()
        send_a_product(update, context, product, pattern_identifier)
        return RUNING


    def catch_next(update, context):
        product = products.next()
        send_a_product(update, context, product, pattern_identifier)
        return RUNING


    def catch_details(update, context):
        pass


    def cancel_list_of_products(update, context):
        query = update.callback_query
        if update.message:
            update.message.reply_text(get_text("canceled_operation", context))
        elif query:
            query.edit_message_text(get_text("canceled_operation", context))
        return END


    return ConversationHandler(
    entry_points = [CommandHandler("list", entry_point_callback)],
    states = {
        RUNING : [
            CallbackQueryHandler(
                catch_next, 
                pattern = pattern_identifier +
                    PATTERN_TO_CATCH_THE_NEXT_PRODUCT),
            CallbackQueryHandler(
                catch_previus, 
                pattern = pattern_identifier +
                    PATTERN_TO_CATCH_THE_PREVIUS_PRODUCT)
        ]},
    fallbacks = [MessageHandler(Filters.all, cancel_list_of_products)]
    )


