"""Natural-language catalog entry point for messages outside command flows."""

from telegram.ext import MessageHandler, filters

from telegram_ecommerce.agent.catalog import answer_catalog_question
from telegram_ecommerce.language import get_text
from telegram_ecommerce.utils.log import logger


async def answer_message(update, context):
    try:
        answer = await answer_catalog_question(update.message.text)
    except Exception:
        logger.exception("Catalog assistant failed")
        answer = get_text("catalog_assistant_unavailable", context)
    await update.message.reply_text(answer)


catalog_assistant = MessageHandler(filters.TEXT & ~filters.COMMAND, answer_message)
