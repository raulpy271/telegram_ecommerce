
from ..tamplates.products import (
    send_a_detailed_product)


def process_of_buy_a_product(update, context, product, pattern_identifier):
    send_a_detailed_product(update, context, product, pattern_identifier)


def send_a_shipping_message(update, context, product , pattern_identifier):
    pass


