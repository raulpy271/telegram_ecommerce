from telegram.ext import Updater

from telegram_ecommerce.database.db_wrapper import db
from telegram_ecommerce.utils.consts import credentials
from telegram_ecommerce.utils.log import logger
from telegram_ecommerce.handlers import all_handlers


token = credentials["token"]
admins = credentials["admins_username"]


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher


    for handler in all_handlers:
        dp.add_handler(handler)


    logger.info("bot started")
    updater.start_polling()
    updater.idle()
    db.close()
    logger.info("bot closed")


if __name__ == '__main__':
    main()


