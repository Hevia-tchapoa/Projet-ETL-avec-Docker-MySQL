import mysql.connector
import pandas as pd


"""
La fonction create_load_data() établit une connexion aux bases de données MySQL Hevia et Jobboard.
Elle crée les tables Users, Categories, Companies, Jobs et Applications.
Ensuite, elle insère les données dans la base Hevia, puis effectue une copie de ces données vers la base Jobboard.

"""

def create_load_data():
    #Connexion to MySQL 
    bd_hevia = mysql.connector.connect( 
        host="localhost",
        port=3306,
        user="hevia",
        password="hevia",
        database="mysql_hevia"
    )

    bd_joboard = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="hevia",
        password="hevia",
        database="mysql_joboard"
    )
    cursor_hevia = bd_hevia.cursor()
    cursor_joboard = bd_joboard.cursor()
    print(bd_hevia)
    print(bd_joboard)
    print("✅ Connecté à MySQL avec succès")

    #Create Tables

    create_query =  [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            role VARCHAR(100) NOT NULL   
        )
        """, #ENUM('candidate', 'recruiter') NOT NULL
        """
        CREATE TABLE IF NOT EXISTS companies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            location VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            location VARCHAR(100),
            company_id INT,
            category_id INT,
            FOREIGN KEY (company_id) REFERENCES companies(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            job_id INT,
            cover_letter TEXT,
            date_applied DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
        """,

    ]
    # Execute the query
    for query in create_query:
        cursor_hevia.execute(query)
        cursor_joboard.execute(query)


    bd_hevia.commit()
    bd_joboard.commit()
    print("✅ Tables created successfully")

    #Insert Data
    ### Insert users
    insert_users = "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)"
    users = [
        ("Alice Dupont", "alice@gmail.com", "candidate"),
        ("Bob Martin", "bob@gmail.com", "candidate"),
        ("Caroline Dubois", "caroline@recrutech.com", "recruiter"),
        ("Daniel Lemoine", "daniel@talentify.io", "recruiter"),
    ]
    cursor_hevia.executemany(insert_users, users)
    bd_hevia.commit()
    print("✅ Users inserted successfully")

    ### Insert Companies
    insert_companies = "INSERT INTO companies (name, location) VALUES (%s, %s)"
    companies = [
        ("Tech Innovators", "Paris"),
        ("Recrutech Solutions", "Lyon"),
        ("Talentify", "Marseille"),
    ]           
    cursor_hevia.executemany(insert_companies, companies)
    bd_hevia.commit()
    print("✅ Companies inserted successfully")

    #### Insert Categories
    insert_categories = "INSERT INTO categories (name) VALUES (%s)"
    categories = [
        ("Développement Web",),
        ("Marketing Digital",),
        ("Data Science",),
        ("Ressources Humaines",)
    ]
    cursor_hevia.executemany(insert_categories,categories)
    bd_hevia.commit()
    print("✅ Categories inserted successfully")

    ## Insert Jobs
    insert_jobs = """
    INSERT INTO jobs (title, description, location, company_id, category_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    jobs = [
        ("Développeur Python", "Poste full remote", "Remote", 1, 1),
        ("Chargé de Marketing", "SEO/SEA + contenus", "Lyon", 2, 2),
        ("Data Analyst Junior", "Analyse des données clients", "Paris", 1, 3),
    ]
    cursor_hevia.executemany(insert_jobs, jobs)
    bd_hevia.commit()
    print("✅ Jobs inserted successfully")


    ##Insert Applications
    insert_applications= """
    INSERT INTO applications (user_id, job_id, cover_letter, date_applied)
    VALUES (%s, %s, %s, %s)
    """
    applications = [
        (1, 1, "Je suis passionné par le développement Python.", "2025-07-01"),
        (2, 3, "J’ai une forte appétence pour les données.", "2025-07-02"),
    ]
    cursor_hevia.executemany(insert_applications, applications)
    bd_hevia.commit()
    print("✅  Applications inserted successfully")

    # Display data from hevia database
    print("Data from hevia database:")
    cursor_hevia.execute("SELECT * FROM users")
    print("Users:", cursor_hevia.fetchall())

    cursor_hevia.execute("SELECT * FROM jobs")
    print("Jobs:", cursor_hevia.fetchall())

    cursor_hevia.execute("SELECT * FROM companies")
    print("Companies:", cursor_hevia.fetchall())

    cursor_hevia.execute("SELECT * FROM categories")
    print("Categories:", cursor_hevia.fetchall())

    cursor_hevia.execute("SELECT * FROM applications")
    print("Applications:", cursor_hevia.fetchall())

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
        try:
            cursor_joboard.executemany(query, data)
            bd_joboard.commit()
            print(f"✅ Data copied sucessful to the bd Jobboard for table {table}.")
        except Exception as e:
            print(f"❌ Error, table copy lost  {table}: {e}")

    # Close the cursor and connection
    cursor_hevia.close()
    cursor_joboard.close()
    bd_hevia.close()
    bd_joboard.close()
    print("✅ Connections closed successfully.")



# ...existing code...
if __name__ == "__main__":
    create_load_data()
    
