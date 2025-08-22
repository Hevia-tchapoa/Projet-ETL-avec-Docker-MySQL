import mysql.connector
from faker import Faker
import random
import pandas as pd



class CreateTables:
    """Class to create tables in the database."""
    def __init__(self, cursor:mysql.connector.cursor.MySQLCursor)-> None:
        self.cursor = cursor

    def create_user_table(self)-> None:
        """Create the user table."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                role VARCHAR(100)
            )
        """)
        print("✅ User table created successfully")
    def create_company_table(self):
        """Create the company table."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL
            )
        """)
        print("✅ companies table created successfully") 

    def create_category_table(self):
        """Create the category table."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """)
        print("✅ Category table created successfully")  
            
    def create_job_table(self):
        """Create the job table."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                company_id INT, 
                category_id INT,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (category_id) REFERENCES categories(id) 
            )
        """)
        print("✅ Job table created successfully")
    
    def create_application_table(self):
        """Create the application table."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                job_id INT,
                status VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        print("✅ Application table created successfully")  




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


## Class coppy data from hevia to joboard
class CopyData:
    def __init__(self, cursor_hevia, cursor_joboard):
        self.cursor_hevia = cursor_hevia
        self.cursor_joboard = cursor_joboard

    def copy_data_to_joboard(self):
        """Copy data from Hevia database to Joboard database.  """
        try:
            #list of tables to copy
            tables =['applications', 'categories', 'companies', 'jobs', 'users']

            # Copy data from hevia to joboard
            for table in tables:
                print(table)
                self.cursor_hevia.execute(f"SELECT * FROM {table}")
                results = self.cursor_hevia.fetchall()
                columns = [i[0] for i in self.cursor_hevia.description]
                # Exclude 'id' if it's auto-increment
                if 'id' in columns:
                    columns_no_id = [col for col in columns if col != 'id']
                    job_df = pd.DataFrame(results, columns=columns)
                    data = job_df[columns_no_id].values.tolist()
                    columns_sql = ", ".join(columns_no_id)
                    values = ", ".join(["%s"] * len(columns_no_id))
                else:
                    job_df = pd.DataFrame(results, columns=columns)
                    data = job_df.values.tolist()
                    columns_sql = ", ".join(columns)
                    values = ", ".join(["%s"] * len(columns))
                query = f"INSERT INTO {table} ({columns_sql}) VALUES ({values})"
                self.cursor_joboard.executemany(query, data)
            print("✅ Data copied successfully from Hevia to Joboard")
        except mysql.connector.Error as e:
            print(f"❌ Error copying data: {e}")


    
    
def main():
    bd_hevia, cursor_hevia  = ConnnectToDB(host = "localhost",port = 3306, user = "root", password = "root", database = "mysql_hevia").connect()
    bd_joboard, cursor_joboard = ConnnectToDB(host = "localhost", port = 3307, user = "hevia", password = "hevia", database = "mysql_joboard").connect()

    # Create Tables

    create_table_hevia= CreateTables(cursor_hevia)

    create_table_hevia.create_user_table()
    create_table_hevia.create_company_table()
    create_table_hevia.create_category_table()    
    create_table_hevia.create_job_table()
    create_table_hevia.create_application_table()
    print("✅ Tables created successfully in Hevia database")
    # Create Tables in Joboard database
    create_table_joboard= CreateTables(cursor_joboard)

    create_table_joboard.create_user_table()
    create_table_joboard.create_company_table()
    create_table_joboard.create_category_table()
    create_table_joboard.create_job_table() 
    create_table_joboard.create_application_table()
    print("✅ Tables created successfully in Joboard database")

    # Insert Users

    user = InsertUsers(cursor_hevia, bd_hevia)
    users_data = [
        ("Alice Smith", "exemple1@gmail.com", "recruiter"),
        ("Bob Johnson", "exemple3@gmail.com", "candidate"), 
        ("Charlie Brown", "exmple4@gmail.com", "recruiter")
    ]
    # Insert users into the Hevia database
    for user_data in users_data:
        if user.insert_users(user_data):
            print(f"✅ User {user_data[0]} inserted successfully")
        else:
            print(f"❌ Failed to insert user {user_data[0]}")

    print("✅ All users insertion completed")

    #user.insert_users(users_data)

    print("✅ User inserted successfully in Hevia database")

    #Copy data from Hevia to Joboard
    if bd_hevia and cursor_hevia and bd_joboard and cursor_joboard:
        copy_data = CopyData(cursor_hevia, cursor_joboard)
        copy_data.copy_data_to_joboard()
        bd_joboard.commit()
        print("✅ Data copied successfully to Joboard database")
    else:
        print("❌ Failed to connect to one or both databases for copying data. Exiting.")




   




if __name__ == "__main__":
    main()




        


  
    
    