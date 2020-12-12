from .db_wrapper import db
from ..utils.consts import credentials
from ..utils.utils import (
    write_file,
    extract_value_from_a_query,
    extract_list_of_values_from_a_query,
    hash_password)


def user_exist(user_id):
    command = "SELECT * FROM customers WHERE id = %s"
    user_exist = bool(db.execute_a_query(command, (user_id,)))
    return user_exist


def is_admin(user_id):
    command = "SELECT is_admin FROM customers WHERE id = %s"
    user_is_admin = db.execute_a_query(command, (user_id,))
    user_exist = bool(user_is_admin)
    if user_exist:
        return extract_value_from_a_query(user_is_admin)
    else: return False


def get_password(user_id):
    command = "SELECT password_hash FROM customers WHERE id = %s"
    user_password = db.execute_a_query(command, (user_id,))
    return extract_value_from_a_query(user_password)


def check_password(user_id, password):
    return hash_password(password) == get_password(user_id)


def user_in_credentials_file(username):
    admins = credentials["admins_username"]
    return username in admins


def extract_blob(photo_id):
    command = "SELECT image_blob FROM photo WHERE id = %s"
    blob = bytes(
        extract_value_from_a_query(
        db.execute_a_query(command, (photo_id,)))
        )
    return blob


def save_photo_in_file(photo_id, file_path):
    blob = extract_blob(photo_id)
    write_file(blob, file_path)


def get_name_of_all_categories():
    command = "SELECT name FROM category"
    all_names_query = db.execute_a_query(command)
    names = extract_list_of_values_from_a_query(all_names_query)
    return names 


def get_category_id_from_name(name):
    command = "SELECT id FROM category WHERE name = %s"
    category_id = db.execute_a_query(command, (name,))
    return extract_value_from_a_query(category_id)


def get_all_available_by_category_id(category_id):
    command = """ SELECT * FROM products 
        WHERE category_id = %s AND quantity_in_stock > 0"""
    products_with_category_id = db.execute_a_query(
        command, (category_id,))
    return products_with_category_id


def get_all_available_by_category_name(name):
    category_id = get_category_id_from_name(name)
    return get_all_available_by_category_id(category_id)


def get_quantity_in_stock(product_id):
    command = "SELECT quantity_in_stock FROM products WHERE id = %s"
    quantity_in_stock = db.execute_a_query(command, (product_id,))
    return extract_value_from_a_query(quantity_in_stock)


def get_quantity_purchased(product_id):
    command = "SELECT quantity_purchased FROM products WHERE id = %s"
    quantity_purchased = db.execute_a_query(command, (product_id,))
    return extract_value_from_a_query(quantity_purchased)


def get_ratings_of_a_product(product_id):
    command = """ SELECT rating FROM orders
        WHERE product_id = %s AND rating IS NOT NULL"""
    ratings_query = db.execute_a_query(command, (product_id,))
    return extract_list_of_values_from_a_query(ratings_query)


def count_occurrence_of_specified_rating(product_id, rating):
    all_ratings = get_ratings_of_a_product(product_id)
    return all_ratings.count(rating)


def search_products(string_to_search):
    command = """SELECT * FROM products 
        WHERE MATCH(name, description) AGAINST(%s)"""
    products_that_match = (
        db.execute_a_query(command, (string_to_search,)))
    return products_that_match 


