
from .utils import load_json_file

credentials_path = "telegram_ecommerce/utils/.user_credentials.json"
credentials = load_json_file(credentials_path)
db_credentials = credentials["db_credentials"]

text_en = ({
    "start" : 
"""hello, I'm a bot that will help you buy products in this e-commerce. 
type /show_categories to see categories.
type /login to autenticate your account.
type /help for more information.""",
    "help" : 

"""The fallowing are instructions of how use this bot:

type /show_categories to see products by category.

type /show_products to see products by a especified category.
The syntax are:
/show_products product name

To search to something you can use the commands:
/search_product and /search_category.
The syntax are:
/search_product product name
/search_category category name
And these commands will show you a list with the thing you want buy.

To buy something you need to register a password. 
To do this type /login.""",
    "help_admin":
"""

"""
})

