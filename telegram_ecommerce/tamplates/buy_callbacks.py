"""Telegram invoice callbacks and payment reconciliation."""

from decimal import Decimal, ROUND_HALF_UP

from telegram import LabeledPrice
from telegram.ext import PreCheckoutQueryHandler, MessageHandler, filters

from telegram_ecommerce.language import get_text
from telegram_ecommerce.utils.consts import provider_token, currency
from telegram_ecommerce.tamplates.rating import ask_if_user_want_avaluate_the_product
from telegram_ecommerce.database.manipulation import (
    complete_paid_order,
    get_product_for_payment,
    validate_checkout,
)
from telegram_ecommerce.utils.log import logger


def _product_id(payload):
    try:
        product_id = int(payload)
    except (TypeError, ValueError):
        return None
    return product_id if product_id > 0 else None


async def send_a_shipping_message(update, context, product, pattern_identifier):
    amount = int((Decimal(str(product.price)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    await context.bot.send_invoice(
        update.effective_chat.id,
        product.name,
        product.description,
        str(product.id),
        provider_token,
        currency,
        [LabeledPrice("Price", amount)],
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
    )


async def pre_checkout_callback(update, context):
    query = update.pre_checkout_query
    product_id = _product_id(query.invoice_payload)
    try:
        valid = product_id is not None and validate_checkout(
            product_id,
            query.from_user.id,
            query.total_amount,
            query.currency,
            currency,
        )
    except Exception:
        logger.exception("Pre-checkout validation failed")
        valid = False
    if valid:
        await query.answer(ok=True)
    else:
        await query.answer(
            ok=False,
            error_message=get_text("information_dont_match", context),
        )


async def successful_payment_callback(update, context):
    payment = update.message.successful_payment
    product_id = _product_id(payment.invoice_payload)
    if product_id is None:
        logger.error("Received payment with invalid product payload")
        await update.message.reply_text(get_text("error_in_orders", context))
        return

    order_id = payment.telegram_payment_charge_id
    try:
        status = complete_paid_order(
            order_id,
            product_id,
            update.effective_user.id,
            payment.total_amount,
            payment.currency,
            currency,
        )
    except Exception:
        logger.exception("Could not record successful Telegram payment %s", order_id)
        await update.message.reply_text(get_text("error_in_orders", context))
        return

    context.user_data["last_paid_order_id"] = order_id
    if status == "needs_review":
        await update.message.reply_text(get_text("payment_needs_review", context))
        return

    await update.message.reply_text(get_text("successful_payment", context))
    product = get_product_for_payment(product_id)
    if product is not None:
        await ask_if_user_want_avaluate_the_product(update, context, product)


pre_checkout_handler = PreCheckoutQueryHandler(pre_checkout_callback)
successful_payment_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
