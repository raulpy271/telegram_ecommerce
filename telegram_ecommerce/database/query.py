from ..utils.utils import extract_value_from_a_query
from .db_wrapper import db
from ..utils.consts import credentials
from ..utils.utils import (
    write_file,
    extract_list_of_values_from_a_query,
    hash_password)


def user_exist(user_id):
    command = "SELECT * FROM customers WHERE user_id = %s"
    user_exist = bool(db.execute_a_query(command, (user_id,)))
    return user_exist


def is_admin(user_id):
    command = "SELECT is_admin FROM customers WHERE user_id = %s"
    user_is_admin = db.execute_a_query(command, (user_id,))
    user_exist = bool(user_is_admin)
    if user_exist:
        return extract_value_from_a_query(user_is_admin)
    else: return False


def get_password(user_id):
    command = "SELECT password_hash FROM customers WHERE user_id = %s"
    user_password = db.execute_a_query(command, (user_id,))
    return extract_value_from_a_query(user_password)


def check_password(user_id, password):
    return hash_password(password) == get_password(user_id)


def user_in_credentials_file(username):
    admins = credentials["admins_username"]
    return username in admins


def extract_blob(photo_id):
    command = "SELECT image FROM photo WHERE photo_id = %s"
    blob = bytes(
        extract_value_from_a_query(
        db.execute_a_query(command, (photo_id,)))
        )
    return blob


def save_photo_in_file(photo_id, file_path):
    blob = extract_blob(photo_id)
    write_file(blob, file_path)


def get_name_of_all_categories():
    command = "SELECT category_name FROM category"
    all_names_query = db.execute_a_query(command)
    names = extract_list_of_values_from_a_query(all_names_query)
    return names 


def get_category_id_from_name(name):
    command = "SELECT category_id FROM category WHERE category_name = %s"
    category_id = db.execute_a_query(command, (name,))
    return extract_value_from_a_query(category_id)


