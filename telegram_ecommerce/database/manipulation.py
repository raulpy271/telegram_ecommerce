from .db_wrapper import db
from .query import get_password


def set_password(user_id, password):
    command = "UPDATE customers SET password_hash = %s WHERE user_id = %s"
    db.execute_a_data_manipulation(command, (password, user_id))


def append_password(user_id, password):
    old_password = get_password(user_id)
    new_password = str(old_password) + str(password)
    set_password(user_id, new_password)


