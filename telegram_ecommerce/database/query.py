from ..utils.utils import extract_value_from_a_query
from .db_wrapper import db


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
    return str(password) == str(get_password(user_id))


