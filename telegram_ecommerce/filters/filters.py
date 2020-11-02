from telegram.ext import BaseFilter

from ..database.query import (
    user_exist,
    get_password,
    is_admin)


class Filter_with_a_boolean_function(BaseFilter):
    def __init__(self, filter_function):
        self.filter_function = filter_function


    def filter(self, message):
        return self.filter_function(message) 


def sender_of_message_is_admin(message):
    return is_admin(message.from_user.id)


filters_admins = Filter_with_a_boolean_function(sender_of_message_is_admin)


