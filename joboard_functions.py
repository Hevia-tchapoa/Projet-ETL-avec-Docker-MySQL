import mysql.connector
from faker import Faker
import random
import pandas as pd


"""
Ce fichier comprend un ensemble de fonctions permettant de

    - Établir la connexion aux bases MySQL Hevia et Jobboard.

    - Créer les tables nécessaires : Users, Categories, Companies, Jobs et Applications.

    - Insérer les données initiales dans la base Hevia.

    - Répliquer ces données de la base Hevia vers la base Jobboard.

"""


def connect_to_db(host:str, port:int, user: str, password:str, database:str)-> tuple[str,str]|tuple[None,None]: # type: ignore
    """Connect to a MySQL database and return the connection and cursor.""" #DOCSTRING
    try:
        bd = mysql.connector.connect(
            host=host,
            port= port,
            user= user,
            password=password,
            database=database
        ) 
        cursor = bd.cursor()
        print(f"✅ Database {database} connected successfully")
        return bd, cursor  
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to {database}  database: {e}")
        return None, None


# Function to create tables in the database
def create_tables(cursor:mysql.connector.cursor.MySQLCursor) -> bool:
    """Create tables in the database if they do not exist."""
    try:
        create_queries = [  
            """CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                role VARCHAR(100)
            )""",
            """CREATE TABLE IF NOT EXISTS compagnies(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                localisation VARCHAR(100)
            )""",
            """CREATE TABLE IF NOT EXISTS categories(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100)
            )""",
            """CREATE TABLE IF NOT EXISTS jobs(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100),
                description TEXT,  
                location VARCHAR(100),
                company_id INT, 
                category_id INT,
                FOREIGN KEY (company_id) REFERENCES compagnies(id),
                FOREIGN KEY (category_id) REFERENCES categories(id) 
            )""",
            """CREATE TABLE IF NOT EXISTS applications(
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                job_id INT,
                status VARCHAR(100),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )"""
        ]
        for query in create_queries:
            cursor.execute(query)
        print("✅ Tables created successfully")
    except mysql.connector.Error as e:
        print(f"❌ Error creating tables: {e}")
        return False


def generate_fake_users(bd:mysql.connector.connection.MySQLConnection,cursor: mysql.connector.cursor.MySQLCursor, num_users=1) -> bool:
    """Generate and insert fake user data into the users table."""
    fake = Faker()
    data = []
    try:           
        for _ in range(num_users):
            name = fake.name()
            email = fake.email()
            role = random.choice(["candidate", "recruiter"])
            data.append((name, email, role))
            print(data)
            insert_users = "INSERT IGNORE INTO users (name, email, role) VALUES (%s, %s, %s)"
            cursor.executemany(insert_users, data)
            bd.commit()
        print(f"✅ {num_users} fake users generated")
    except mysql.connector.Error as e:
        print(f"❌ Error generating fake users: {e}")
        return False
    return True


# Generation of fake Categories data
def generate_fake_category(bd:mysql.connector.connection.MySQLConnection,cursor: mysql.connector.cursor.MySQLCursor, num_category=10) -> bool:
    """Generate and insert fake category data into the categories table."""
    fake = Faker()
    data = []
    try:           
        for _ in range(num_category):
            name = fake.job()
            data.append((name))
            print(data)
            insert_categories = "INSERT INTO categories (name) VALUES (%s)"
            cursor.executemany(insert_categories, data)
            bd.commit()
        print(f"✅ {num_category} fake categories generated")
    except mysql.connector.Error as e:
        print(f"❌ Error generating fake categories: {e}")
        return False
    return True

#Generation of fake Companies data
def generate_fake_companies(bd:mysql.connector.connection.MySQLConnection,cursor: mysql.connector.cursor.MySQLCursor, num_companies=2) -> bool:
    """Generate and insert fake company data into the companies table."""
    fake = Faker()
    data = []
    try:           
        for _ in range(num_companies):
            name = fake.company()
            localisation = fake.city()
            data.append((name, localisation))
            print(data)
            insert_companies = "INSERT INTO compagnies (name, localisation) VALUES (%s, %s)"
            cursor.executemany(insert_companies, data)
            bd.commit()
        print(f"✅ {num_companies} fake companies generated")
    except mysql.connector.Error as e:
        print(f"❌ Error generating fake companies: {e}")
        return False
    return True 

#Generation of fake Jobs data
def generate_fake_jobs(bd:mysql.connector.connection.MySQLConnection,cursor: mysql.connector.cursor.MySQLCursor, num_jobs=2) -> bool:
    """Generate and insert fake job data into the jobs table."""
    fake = Faker()
    data = []
    try:           
        for _ in range(num_jobs):
            title = fake.job()
            description = fake.text(max_nb_chars=200)
            location = fake.city()
            company_id = random.randint(1, 5)  # Assuming there are 5 companies
            category_id = random.randint(1, 4)  # Assuming there are 4 categories
            data.append((title, description, location, company_id, category_id))
            print(data)
            insert_jobs = """
            INSERT INTO jobs (title, description, location, company_id, category_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_jobs, data)
            bd.commit()
        print(f"✅ {num_jobs} fake jobs generated")
    except mysql.connector.Error as e:
        print(f"❌ Error generating fake jobs: {e}")
        return False
    return True 

#  #Generation of fake Applications data
# def generate_fake_applications(bd:mysql.connector.connection.MySQLConnection,cursor: mysql.connector.cursor.MySQLCursor, num_applications=5) -> bool:
#     """Generate and insert fake application data into the applications table."""
#     fake = Faker()
#     data = []
#     try:           
#         for _ in range(num_applications):
#             user_id = random.randint(1, 5)  # Assuming there are 5 users
#             job_id = random.randint(1, 10)  # Assuming there are 10 jobs
#             status = random.choice(["applied", "interviewed", "hired", "rejected"])
#             data.append((user_id, job_id, status))
#             print(data)
#             insert_applications = "INSERT INTO applications (user_id, job_id, status) VALUES (%s, %s, %s)"
#             cursor.executemany(insert_applications, data)
#             bd.commit()
#         print(f"✅ {num_applications} fake applications generated")
#     except mysql.connector.Error as e:
#         print(f"❌ Error generating fake applications: {e}")
#         return False
#     return True


                       

#Function coppy data from hevia to joboard
def copy_data_to_joboard(cursor_hevia:mysql.connector.cursor.MySQLCursor, cursor_joboard:mysql.connector.cursor.MySQLCursor)->None:
    """Copy data from Hevia database to Joboard database.  """
    try:
        #list of tables to copy
        tables =['applications', 'categories', 'companies', 'jobs', 'users']

        # Copy data from hevia to joboard
        for table in tables:
            print(table)
            cursor_hevia.execute(f"SELECT * FROM {table}")
            results = cursor_hevia.fetchall()
            columns = [i[0] for i in cursor_hevia.description]
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
            cursor_joboard.executemany(query, data)
        print("✅ Data copied successfully from Hevia to Joboard")
    except mysql.connector.Error as e:
        print(f"❌ Error copying data: {e}")







def main()-> None:
    """Main function to connect to databases, create tables, and generate fake data."""
    bd_hevia, cursor_hevia =  connect_to_db(host="localhost", port=3306, user="root", password="root", database="mysql_hevia") #"connect_to_hevia_db()"
    bd_joboard, cursor_joboard =  connect_to_db(host="localhost", port=3307, user="root", password="root", database="mysql_joboard") #connect_to_joboard_db()
    
    if bd_hevia and cursor_hevia and bd_joboard and cursor_joboard:
        create_tables(cursor_hevia)
        create_tables(cursor_joboard)
        bd_hevia.commit()
        bd_joboard.commit()
        print("✅ Changes committed successfully")
    else:
        print("❌ Failed to connect to one or both databases. Exiting.")

    
    # call the function to generate fake users
    if bd_hevia and cursor_hevia:
        generate_fake_users(bd_hevia,cursor_hevia, num_users=5)
        print("✅ Fake users data inserted successfully")
    else:
        print("❌ Failed to connect to Hevia database for inserting fake users. Exiting.")

    # call the function to generate fake companies
    if bd_hevia and cursor_hevia:
        generate_fake_companies(bd_hevia,cursor_hevia, num_companies=5)
        print("✅ Fake companies data inserted successfully")
    else:
        print("❌ Failed to connect to Hevia database for inserting fake companies. Exiting.")
    
    # call the function to generate fake categories
    if bd_hevia and cursor_hevia:
        generate_fake_category(bd_hevia,cursor_hevia, num_category=5)
        print("✅ Fake categories data inserted successfully")
    else:
        print("❌ Failed to connect to Hevia database for inserting fake categories. Exiting.")
    
    # call the function to generate fake jobs
    if bd_hevia and cursor_hevia:
        generate_fake_jobs(bd_hevia,cursor_hevia, num_jobs=5)
        print("✅ Fake jobs data inserted successfully")
    else:
        print("❌ Failed to connect to Hevia database for inserting fake jobs. Exiting.")
    
    
    
    # Copy data from hevia to joboard
    if bd_hevia and cursor_hevia and bd_joboard and cursor_joboard:
        copy_data_to_joboard(cursor_hevia, cursor_joboard)
        bd_joboard.commit()
        print("✅ Data copied successfully to Joboard database")
    else:
        print("❌ Failed to connect to one or both databases for copying data. Exiting.")




if __name__ == "__main__":
    main()

    