from .db_wrapper import db


def set_password(user_id, password):
    command = "UPDATE customers SET password_hash = %s WHERE user_id = %s"
    db.execute_a_data_manipulation(command, (password, user_id))


