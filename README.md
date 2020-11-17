# telegram ecommerce

This is a telegram bot made using the python language. To connect with the telegram API I use the [python-telegram-bot](https://python-telegram-bot.org/) wrapper and on the database side, I use MySQL.

## what this bot can do?

## screenshot

### Register Command

![Using the register command](/assets/register_command.gif)

### Seeing products

![Seeing products](/assets/show_categories_command.gif)

### Changing the language

![Changing the language used](/assets/changing_the_language.gif)

## how to setup

First of all, see the dependencies in the requirements file or type `pip install -r requirements.txt` to install the dependencies automatically.

The second process is to create a bot with the [Bot Father](https://core.telegram.org/bots#6-botfather) and get your token. Now, put your token in the file `/telegram_ecommerce/utils/user_credentials.json`, in this file you can put the admin's usernames and the credentials of your MySQL database. Moreover, you can change some settings in the `consts.py` file, like the default language.

After all, you can run the bot typing:

```sh
 $ python bot.py
```

## TODO

 - Add feature to change password
 - Add salt when storing the password
 - Add full suport to the portuguese language 
 - Add suport to other language

