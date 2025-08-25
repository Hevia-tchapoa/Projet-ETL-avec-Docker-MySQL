import mysql.connector
from faker import Faker
import pandas as pd



#Class insert Users    
class InsertUsers:
    """Class to insert users into the database Hevia."""
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def insert_users(self, users_list:tuple) -> bool:
            """Insert users into the users table."""
            try:
                query = "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)"
                self.cursor.execute(query, users_list)
                self.cursor._connection.commit()
                
                return True
            except mysql.connector.Error as e:
                print(f"❌ Error inserting user: {e}")
            return False
    
#insert fake data into companies table
class InsertCompanies:
    """Class to insert companies into the database Hevia."""
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def generate_fake_companies(self, num_companies:int) -> bool:
        """Generate and insert fake company data into the companies table."""
        fake = Faker()
        data = []
        try:           
            for _ in range(num_companies):
                name = fake.company()
                localisation = fake.city()
                data.append((name, localisation))
                print(data)
                insert_companies = "INSERT INTO companies (name, location) VALUES (%s, %s)"
                self.cursor.executemany(insert_companies, data)
                self.cursor._connection.commit()
            print(f"✅ {num_companies} fake companies generated")
        except mysql.connector.Error as e:
            print(f"❌ Error generating fake companies: {e}")
            return False
        return True







