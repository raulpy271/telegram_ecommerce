
from os import environ

from telegram_ecommerce.utils.utils import create_admins_set

default_language = "en"
currency = "USD"
bot_token = environ["BOT_TOKEN"]
provider_token = environ.get("PROVIDER_TOKEN")
admins = create_admins_set(environ.get("ADMINS", ""))
BAD_RATING = 0
REGULAR_RATING = 5
GOOD_RATING = 10


