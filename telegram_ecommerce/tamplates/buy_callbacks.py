from telegram import LabeledPrice

from ..utils.consts import (
    provider_token,
    currency)
from ..tamplates.products import (
    send_a_detailed_product)


def process_of_buy_a_product(update, context, product, pattern_identifier):
    send_a_detailed_product(update, context, product, pattern_identifier)


def send_a_shipping_message(update, context, product , pattern_identifier):
    title = product.name
    description = product.description
    payload = "Custom-Payload"
    start_parameter = "test-payment"
    prices = [LabeledPrice("Price", product.price)]


    context.bot.send_invoice(
        update.message.chat_id, 
        title, 
        description, 
        payload, 
        provider_token, 
        start_parameter, 
        currency,
        prices,
        need_name = True,
        need_phone_number = True, 
        need_email = True, 
        need_shipping_address = True
    )


