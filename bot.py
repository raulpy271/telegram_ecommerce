
from telegram.ext import ApplicationBuilder

from telegram_ecommerce.utils.consts import credentials
from telegram_ecommerce.utils.log import logger
from telegram_ecommerce.handlers import (
    all_public_commands_descriptions, 
    all_handlers)


token = credentials["token"]
admins = credentials["admins_username"]

async def post_init(app):
    await app.bot.set_my_commands(all_public_commands_descriptions)

def main():
    app = ApplicationBuilder().token(token).post_init(post_init).build()

    for handler in all_handlers:
        app.add_handler(handler)


    logger.info("bot started")
    app.run_polling()
    logger.info("bot closed")


if __name__ == "__main__":
    main()


