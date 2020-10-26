from telegram.ext import Updater

from telegram_ecommerce.database.db_wrapper import db
from telegram_ecommerce.utils.consts import credentials
from telegram_ecommerce.utils.log import logger
from telegram_ecommerce.handlers.commands import (
    start,
    help_command,
    register,
    register_query_step_1,
    register_query_step_2) 


token = credentials["token"]
admins = credentials["admins_username"]


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher


    dp.add_handler(start)
    dp.add_handler(help_command)
    dp.add_handler(register)
    dp.add_handler(register_query_step_1)
    dp.add_handler(register_query_step_2)


    logger.info("bot started")
    updater.start_polling()
    updater.idle()
    db.close()
    logger.info("bot closed")


if __name__ == '__main__':
    main()


