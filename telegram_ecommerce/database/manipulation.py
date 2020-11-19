from .db_wrapper import db
from ..utils.utils import hash_password
from .query import (
    get_password,
    user_in_credentials_file)


def create_account(user):
    user_id = user.id
    username = user.username
    user_is_admin = user_in_credentials_file(username)
    command = "UPDATE customers SET password_hash = %s WHERE user_id = %s"
    command = ("""
        INSERT INTO customers 
            (user_id, username, password_hash, is_admin) 
            VALUES (%s, %s, %s, %s)""")
    command_args = (user_id, username, "", user_is_admin)
    db.execute_a_data_manipulation(command, command_args)


def delete_account(user_id):
    command = "DELETE FROM customers WHERE user_id = %s"
    db.execute_a_data_manipulation(command, (user_id,))


def set_password(user_id, password):
    command = "UPDATE customers SET password_hash = %s WHERE user_id = %s"
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
    command = "UPDATE photo SET image = %s WHERE photo_id = %s"
    command_args = (bytes(blob), photo_id)
    db.execute_a_data_manipulation(command, command_args)


def add_photo(photo_id, bytes_of_photo):
    command = ("""
        INSERT INTO photo
               (photo_id)
        VALUES (%s)""")
    command_args = (photo_id,)
    db.execute_a_data_manipulation(command, command_args)
    update_photo(photo_id, bytes_of_photo)


def add_category(name, description, tags=None, image_id=None):
    command = ("""
        INSERT INTO category
               (category_name, category_description, tags, image_id)
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
            product_description,
            unit_price, 
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
    

