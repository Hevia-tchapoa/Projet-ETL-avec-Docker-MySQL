import mysql.connector
from faker import Faker
import pandas as pd


class CreateTables:
    """Class to create tables in the database."""

    def __init__(self, cursor: mysql.connector.cursor.MySQLCursor) -> None:
        self.cursor = cursor

    def create_user_table(self) -> None:
        """Create the user table."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                role VARCHAR(100) 
            )
        """
        )
        print("✅ User table created successfully")

    def create_company_table(self):
        """Create the company table."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL
            )
        """
        )
        print("✅ companies table created successfully")

    def create_category_table(self):
        """Create the category table."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """
        )
        print("✅ Category table created successfully")

    def create_job_table(self):
        """Create the job table."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                company_id INT, 
                category_id INT,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (category_id) REFERENCES categories(id) 
            )
        """
        )
        print("✅ Job table created successfully")

    def create_application_table(self):
        """Create the application table."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                job_id INT,
                status VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """
        )
        print("✅ Application table created successfully")
