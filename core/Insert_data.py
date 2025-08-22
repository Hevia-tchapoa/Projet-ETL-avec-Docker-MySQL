import mysql.connector
from faker import Faker
import pandas as pd



#Class insert Users    
class InsertUsers:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def insert_users(self, users_list):
            """Insert users into the users table."""
            try:
                query = "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)"
                self.cursor.execute(query, users_list)
                self.cursor._connection.commit()
                
                return True
            except mysql.connector.Error as e:
                print(f"❌ Error inserting user: {e}")
            return False
