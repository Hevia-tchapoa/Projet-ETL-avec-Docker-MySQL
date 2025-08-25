import mysql.connector
from faker import Faker
import random
import pandas as pd
from core.Mysqlsource import ConnnectToDB
from core.Create_tables import CreateTables
from core.Insert_data import InsertUsers
from core.Insert_data import InsertCompanies
from core.Load_data import CopyData



    
def main():
    """Main function to set up databases, create tables, insert data, and copy data between databases.  """

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



    # call the function to generate fake companies

    num_companies = 5
    companie = InsertCompanies(cursor_hevia, bd_hevia)
    companie.generate_fake_companies(num_companies)
    print("✅ Fake companies data inserted successfully")




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




        


  
    
    