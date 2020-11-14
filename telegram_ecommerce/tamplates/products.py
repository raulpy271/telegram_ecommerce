from telegram import (
    InlineKeyboardButton as InlineButton,
    InlineKeyboardMarkup)


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
        self.iter = 0 


    def __next__(self):
        actual_product = self.list_of_products[self.iter]
        self.__increment_iter__()
        return actual_product


    def __increment_iter__(self):
        if self.iter == len(self.list_of_products) - 1:
            self.iter = 0
        else: 
            self.iter += 1



def get_product(
    update, 
    context,
    name, 
    price, 
    rating, 
    image_id, 
    pattern_identifier):
    markup = InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("previus_product", context),
                callback_data=pattern_identifier + 'previus_product'),
            InlineButton(
                get_text("product_details", context),
                callback_data=pattern_identifier + 'product_details'),
            InlineButton(
                get_text("next_product", context),
                callback_data=pattern_identifier + 'next_product')
        ]])
    text = name + " por " + str(price) + \
           "\nAvaliações: 3.0 ❤️❤️❤️🤍🤍"
    update.message.reply_photo(
        image_id,
        caption = text, 
        reply_markup=markup) 


def get_product_details(
    update, 
    context,
    name, 
    description,
    price, 
    rating, 
    quantity_purchased,
    image_id, 
    pattern_identifier):
    markup = InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("previus_step", context),
                callback_data=pattern_identifier + 'previus_step'),
            InlineButton(
                get_text("buy", context),
                callback_data=pattern_identifier + 'buy_product')
        ]])
    text = name + " por " + str(price) + '\n' + \
           description + '\n' + \
           "Avaliações: 3.0 ❤️❤️❤️🤍🤍" + '\n'  + \
           "Foi comprado: 30 unidades" 
    update.message.reply_photo(
        image_id,
        caption = text, 
        reply_markup=markup) 


