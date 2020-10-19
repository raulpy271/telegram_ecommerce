
import mysql.connector as connector

from ..utils.utils import load_sql_file
from ..utils.consts import db_credentials


class DBWrapper():
    def __init__(self, db_credentials):
        self.database_name = "ecommerce"
        self.connection = connector.connect(**db_credentials)
        self.connection.get_warnings = True
        self.create_db()
        self.use_this_db()
        self.create_tables()


    def close_db(self):
        self.connection.close()


    def execute_a_query(self, command, params=(), multi=False):
        cursor = self.connection.cursor()
        cursor.execute(command, params, multi)
        rows = cursor.fetchall()
        cursor.close()
        return rows


    def execute_a_data_manipulation(self, command, params=(), multi=False):
        cursor = self.connection.cursor()
        cursor.execute(command, params, multi)
        self.connection.commit()
        cursor.close()


    def create_db(self):
        create_db_command = "CREATE DATABASE ecommerce"
        self.execute_a_data_manipulation(create_db_command)


    def use_this_db(self):
        create_db_command = "USE ecommerce"
        self.execute_a_data_manipulation(create_db_command)


    def create_tables(self):
        pass


