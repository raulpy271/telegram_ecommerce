from telegram import (
    InlineKeyboardButton as InlineButton,
    InlineKeyboardMarkup)


def get_product(
    update, 
    context,
    name, 
    price, 
    rating, 
    image_id, 
    pattern_identifier) 
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
    pattern_identifier) 
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


