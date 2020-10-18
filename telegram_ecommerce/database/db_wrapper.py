
import mysql.connector as connector

class DBWrapper():
    def __init__(self, db_credentials):
        self.connection = connector.connect(**db_credentials)


    def close_db(self):
        self.connection.close()


    def create_db(self):
        pass


    def execute_a_query(self, command, params=()):
        cursor = self.connection.cursor()
        cursor.execute(command, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows


    def execute_a_data_manipulation(self, command, params=()):
        cursor = self.connection.cursor()
        cursor.execute(command, params)
        self.connection.commit()
        cursor.close()


