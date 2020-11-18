from telegram import InputMediaPhoto

from ..language import get_text
from .buttons import (
    tamplate_for_show_a_list_of_products,
    tamplate_for_show_a_detailed_product)


class Product():
    def __init__(
        self, 
        product_id,
        name,
        price, 
        quantity_in_stock,
        quantity_purchased,
        category_id,
        image_id = None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.quantity_purchased = quantity_purchased
        self.category_id = category_id
        self.image_id = image_id


    def create_a_instance_of_this_class_from_a_list_of_properties(
            properties):
        return Product(*properties)


class ListProductIterator():
    def __init__(self, *list_of_products):
        self.list_of_products = list_of_products
        self.iter = -1 

    
    def create_a_list_from_a_query(query):
        list_of_instances_of_Product_class = list(map(
            Product.create_a_instance_of_this_class_from_a_list_of_properties,
            query))
        return ListProductIterator(
            *list_of_instances_of_Product_class)


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


def send_a_product(update, context, product, pattern_identifier):
    query = update.callback_query
    markup = tamplate_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    query.message.edit_media(
        media = InputMediaPhoto(product.image_id, text),
        reply_markup = markup)


def send_a_detailed_product(update, context,  product, pattern_identifier):
    query = update.callback_query
    markup = tamplate_for_show_a_detailed_product(
        pattern_identifier, context)
    text = get_text_for_detailed_product(product, context)
    query.message.edit_media(
        media = InputMediaPhoto(product.image_id, text),
        reply_markup = markup)


def get_text_for_product(product, context):
    text = product.name + ", " + get_text("price", context) + \
           str(product.price) + '\n'  
    return text


def get_text_for_detailed_product(product, context):
    text = product.name + ", " + get_text("price", context) + \
           str(product.price) + '\n' + \
           get_text("purchased", context) + str(product.quantity_purchased)
    return text


