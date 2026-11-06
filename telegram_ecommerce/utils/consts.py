
from os import environ

default_language = "en"
currency = "USD"
bot_token = environ["BOT_TOKEN"]
provider_token = environ.get("PROVIDER_TOKEN")
admins = {
    int(value.strip())
    for value in environ.get("ADMIN_USER_IDS", "").split(",")
    if value.strip()
}
BAD_RATING = 0
REGULAR_RATING = 5
GOOD_RATING = 10


