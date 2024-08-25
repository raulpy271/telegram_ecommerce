# 🤖 Telegram e-commerce

This is a Telegram bot made using the Python language. To connect with the Telegram API, I use the python-telegram-bot wrapper, and on the database side, I use MySQL.
## 💖 All Contributors

<a href="https://github.com/raulpy271/telegram_ecommerce/graphs/contributors">
 <img alt="All Contributors" src="https://contrib.rocks/image?repo=raulpy271/telegram_ecommerce"/>
</a>

## 🛠️ TODO

- Add a feature to change password.
- Add salt when storing the password.
- Add support for other languages.
- Add password confirmation when a user buys a product.
- The handler that adds a product in the database doesn't check if the description of the product has more characters than the description column has.
- When the user selects the command \show_categories more than once, the bot only shows products one time.
- Add a filter to block non-admin commands like /add_product and /add_category.

## ❓What can this bot do ?

This is a Telegram bot where you can buy items.

Sellers can add, delete, and manage them.

The following are instructions on how to use this bot:

- Type /show_categories to see products by category.
- To search for something, you can use the command /search.
- To buy something, you need to register a password. To do this, type /register.
- The admins can add products and categories with the commands /add_product and /add_category.

## 🚸 Tutorial

### Register Command

![Using the register command](./assets/register_command.gif)

### Seeing products

![Seeing products](./assets/show_categories_command.gif)

### Making a payment

![Making a payment](./assets/payment.gif)

### Searching for a product

![Searching a product](./assets/search.gif)

### Changing the language

![Changing the language used](./assets/changing_the_language.gif)

## ⚙️ How to set up ?

To setup the bot for testing and development is used Docker along with the command `docker compose`. This tool is recommended because it's more easy to setup the bot and it's database. However, if you don't want to use Docker you still can run the bot anyway, if it's your case after reading this topic you can jump to [Setup in local machine](#setup-in-local-machine).

To have a Telegram Bot, you need to open a chat with the Bot Father in Telegram, this bot will create a token that's needed to run your created bot. To make test payments, you should have a token from a payment provider as well. Learn more about payments on the [Telegram payment page](https://core.telegram.org/bots/payments). To learn more about Bot Token read [How Do I Create a Bot?](https://core.telegram.org/bots#how-do-i-create-a-bot).

The two tokens created need to be placed in the file `.env`, create this file using the template file `.env.example` which already comes with some settings filled. The created `.env` file is where you can change some settings and place private data as your tokens.

### Setup with Docker

First of all, install Docker Engine (or Docker Desktop, if you on Windows), [Install Docker Engine](https://docs.docker.com/engine/install/).

With docker installed, run the following commands to build the application and create the database schema needed:

```sh
# Build the application
docker compose build

# Run the application in background
docker compose up -d

# Use alembic to create the database structure in the MySQL database running on docker.
docker compose exec app alembic upgrade head

# Run the application again inside the terminal(it will print logs to help you identify if it's all working)
docker compose down && docker compose up
```

The database connection is already filled in the `.env.example`, this connection is to the database created in a docker container using the commands above.

### Setup in local machine

First of all, see the dependencies in the requirements file or type `pip3 install -r requirements.txt` to install the dependencies automatically.

In this method you should setup a MySQL database, it can be run on your machine or hosted on a cloud provider. After the database setup, you should put in the `.env` the database connection settings.

In a nearly created database you should create the schema(tables) used in the Bot, to do it use the alembic command below:

```sh
alembic upgrade head
```

Finally, you can run the Bot in your machine:

```py
python3 bot.py
```

## 🛑 Disclaimer

This project is a demo, it's only for learning purposes. To be ready for production, many features need to be added.


