from telegram import LabeledPrice

from telegram.ext import (
    filters,
    PreCheckoutQueryHandler,
    MessageHandler)

from telegram_ecommerce.language import get_text
from telegram_ecommerce.utils.consts import provider_token, currency
from telegram_ecommerce.tamplates.rating import ask_if_user_want_avaluate_the_product
from telegram_ecommerce.database.manipulation import (
    add_orders,
    product_has_purchased)


products_data_key = "list_of_products"


def add_pre_checkout_query_to_user_data(context, query):
    context.user_data["last_order"] = query


async def send_a_shipping_message(update, context, product , pattern_identifier):
    title = product.name
    description = product.description
    payload = str(product.id)
    prices = [LabeledPrice("Price", int( 100 * product.price))]


    await context.bot.send_invoice(
        update.effective_chat.id, 
        title, 
        description, 
        payload, 
        provider_token, 
        currency,
        prices,
        need_name = True,
        need_phone_number = True, 
        need_email = True, 
        need_shipping_address = True
    )


def process_order(query, product, context):
    PROCESS_OK, PROCESS_FAIL = (True, False)
    if query.invoice_payload != str(product.id):
        return (PROCESS_FAIL, get_text("information_dont_match", context))
    try:
        add_orders(
            query.id,
            (query.total_amount / 100),
            query.from_user.id,
            product.id)
        product_has_purchased(product.id)
        return (PROCESS_OK, None) 
    except:
        return (PROCESS_FAIL, get_text("error_in_orders", context))


async def pre_checkout_callback(update, context):
    query = update.pre_checkout_query
    add_pre_checkout_query_to_user_data(context, query)
    product = context.user_data[products_data_key]["products"].actual()
    (status, error_message) = process_order(query, product, context)
    if status:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message=error_message)


async def successful_payment_callback(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    await update.message.reply_text(get_text("successful_payment", context))
    await ask_if_user_want_avaluate_the_product(update, context, product)


pre_checkout_handler = PreCheckoutQueryHandler(pre_checkout_callback)


successful_payment_handler = MessageHandler(
    filters.SUCCESSFUL_PAYMENT, successful_payment_callback)


