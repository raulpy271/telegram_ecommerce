
from .db_wrapper import db

def is_admin(user_id):
    command = "SELECT is_admin FROM customers WHERE user_id = %s"
    user_is_admin = db.execute_a_query(command, (user_id,))
    user_exist = bool(user_is_admin)
    if user_exist:
        extracing_boolean_values_from_list_of_tuples = bool(
            user_is_admin[0][0])
        return extracing_boolean_values_from_list_of_tuples
    else: return False
