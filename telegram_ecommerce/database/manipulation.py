from .db_wrapper import db
from ..utils.utils import hash_password
from .query import (
    get_password,
    user_in_credentials_file, 
    get_quantity_in_stock,
    get_quantity_purchased)


def create_account(user):
    user_id = user.id
    username = user.username
    user_is_admin = user_in_credentials_file(username)
    command = "UPDATE customers SET password_hash = %s WHERE id = %s"
    command = ("""
        INSERT INTO customers 
            (id, username, password_hash, is_admin) 
            VALUES (%s, %s, %s, %s)""")
    command_args = (user_id, username, "", user_is_admin)
    db.execute_a_data_manipulation(command, command_args)


def delete_account(user_id):
    command = "DELETE FROM customers WHERE id = %s"
    db.execute_a_data_manipulation(command, (user_id,))


def set_password(user_id, password):
    command = "UPDATE customers SET password_hash = %s WHERE id = %s"
    db.execute_a_data_manipulation(command, (password, user_id))


def append_password(user_id, password):
    old_password = get_password(user_id)
    new_password = str(old_password) + str(password)
    set_password(user_id, new_password)


def hash_user_password(user_id):
    password = get_password(user_id)
    password_hash = hash_password(password)
    set_password(user_id, password_hash)


def update_photo(photo_id, blob):
    command = "UPDATE photo SET image_blob = %s WHERE id = %s"
    command_args = (bytes(blob), photo_id)
    db.execute_a_data_manipulation(command, command_args)


def add_photo(photo_id, bytes_of_photo):
    command = "INSERT INTO photo (id) VALUES (%s)"
    command_args = (photo_id,)
    db.execute_a_data_manipulation(command, command_args)
    update_photo(photo_id, bytes_of_photo)


def add_category(name, description, tags=None, image_id=None):
    command = (""" INSERT INTO category
        (name, description, tags, image_id)
        VALUES (%s, %s, %s, %s)""")
    command_args = (name, description, tags, image_id)
    db.execute_a_data_manipulation(command, command_args)


def add_product(
    name, 
    description,
    unit_price=0, 
    quantity_in_stock=0, 
    quantity_purchased=0,
    category_id=None, 
    image_id=None):
    command = ("""
        INSERT INTO products
            (name, 
            description,
            price, 
            quantity_in_stock, 
            quantity_purchased,
            category_id, 
            image_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""")
    command_args = (
        name, 
        description,
        float(unit_price), 
        int(quantity_in_stock), 
        int(quantity_purchased),
        int(category_id), 
        image_id)
    db.execute_a_data_manipulation(command, command_args)
    

def add_orders(
    order_id,
    price,
    user_id,
    product_id,
    rating = None):
    command = ("""INSERT INTO orders 
        (id, price, user_id, product_id, rating)
        VALUES (%s, %s, %s, %s, %s)""")
    command_args = (
        order_id, 
        price,
        int(user_id), 
        int(product_id), 
        rating)
    db.execute_a_data_manipulation(command, command_args)


def product_has_purchased(product_id):
    quantity_in_stock = get_quantity_in_stock(product_id) - 1
    quantity_purchased = get_quantity_purchased(product_id) + 1
    command = ("""
        UPDATE products SET 
            quantity_in_stock = %s,
            quantity_purchased = %s
        WHERE id = %s""")
    command_args = (quantity_in_stock, quantity_purchased, product_id)
    db.execute_a_data_manipulation(command, command_args)


def add_rating_to_an_order(order_id, rating):
    command = ("""
        UPDATE orders SET
            rating = %s
        WHERE id = %s""")
    command_args = (int(rating), order_id)
    db.execute_a_data_manipulation(command, command_args)


