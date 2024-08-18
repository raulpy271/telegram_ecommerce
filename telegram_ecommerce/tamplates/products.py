from telegram import InputMediaPhoto

from telegram_ecommerce.language import get_text
from telegram_ecommerce.database.query import count_occurrence_of_specified_rating
from telegram_ecommerce.tamplates.buttons import (
    get_list_of_buttons,
    tamplate_for_show_a_list_of_products,
    tamplate_for_show_a_detailed_product)


class ListProductIterator():
    def __init__(self, *list_of_products):
        self.list_of_products = list_of_products
        self.iter = -1 
    
    def actual(self):
        actual_product = self.list_of_products[self.iter]
        return actual_product


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


    def is_empty(self):
        if self.list_of_products:
            return False
        return True


async def send_a_product(update, context, product, pattern_identifier):
    query = update.callback_query
    markup = tamplate_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    await query.message.edit_media(
        media = InputMediaPhoto(product.image_id, text),
        reply_markup = markup)


async def send_a_detailed_product(update, context,  product, pattern_identifier):
    query = update.callback_query
    markup = tamplate_for_show_a_detailed_product(
        pattern_identifier, context)
    text = get_text_for_detailed_product(product, context)
    await query.message.edit_media(
        media = InputMediaPhoto(product.image_id, text),
        reply_markup = markup)


async def send_a_inline_with_a_list_of_products(
    update, 
    context,
    text,
    list_of_names):
    buttons_with_list_of_names = get_list_of_buttons(*list_of_names)
    await update.message.reply_text(text, reply_markup=buttons_with_list_of_names)


def get_text_for_product(product, context):
    text = (product.name + "\n\n" + 
        get_text("price", context) + str(product.price))
    return text


def get_text_for_detailed_product(product, context):
    product_id = product.id
    text = (product.name + "\n\n" +
        get_text("price", context) + str(product.price) + '\n\n' +
        str(product.description) + '\n\n' + 
        get_text("purchased", context) + 
        str(product.quantity_purchased) + '\n\n' +
        get_text("rating", context) + '\n' + 
        str(count_occurrence_of_specified_rating(product_id, 10)) + ' ' +
        get_text("good", context) + '\n' + 
        str(count_occurrence_of_specified_rating(product_id, 5)) + ' ' +
        get_text("regular", context) + '\n' + 
        str(count_occurrence_of_specified_rating(product_id, 0)) + ' ' +
        get_text("bad", context) 
        )
    return text

