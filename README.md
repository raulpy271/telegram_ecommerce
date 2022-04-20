# telegram ecommerce

This is a telegram bot made using the python language. To connect with the telegram API I use the [python-telegram-bot](https://python-telegram-bot.org/) wrapper and on the database side, I use MySQL.


## what this bot can do?

A telegram bot that can sell products and the salespeople can add, delete, and manage them. 

The fallowing are instructions of how use this bot:

 - type `/show_categories` to see products by category.

 - To search to something you can use the command `/search`.

 - To buy something you need to register a password. To do this type `/register`.

 - The admins can add products and categories with the commands `/add_product` and `/add_category`. 

## screenshot

### Register Command

![Using the register command](/assets/register_command.gif)

### Seeing products

![Seeing products](/assets/show_categories_command.gif)

### Making a payment

![Making a payment](/assets/payment.gif)

### Searching for a product

![Searching a product](/assets/search.gif)

### Changing the language

![Changing the language used](/assets/changing_the_language.gif)

## how to setup

First of all, see the dependencies in the requirements file or type `pip install -r requirements.txt` to install the dependencies automatically.

The second process is to create a bot with the [Bot Father](https://core.telegram.org/bots#6-botfather) and get your bot token and to make test payments you should have a token from a payment provider, learn more about this in the [telegram payment page](https://core.telegram.org/bots/payments).

Now, put your tokens in the file `/telegram_ecommerce/utils/user_credentials.json`, in this file you can put the admin's usernames and the credentials of your MySQL database. Moreover, you can change some settings in the `consts.py` file, like the default language.

After all, you can run the bot typing:

```sh
 $ python bot.py
```

## Disclaimer

This project it's just a demo, it's only have learning propose. To be ready for production, many features are need to be added. So I don't have the proposal to make it production-ready.


## TODO

 - Add feature to change password
 - Add salt when storing the password
 - Add full support to the Portuguese language 
 - Add support to other language
 - Ask to the user the password when the user wants to make a purchase
 - The handler that add product in database dont check if the description of the products have more char than the description column have
 - When the user select the command `\show_categories` more than one time the bot only show products one time
 - Add an filter to block non admins commands like these: `/add_product` and `/add_category`


