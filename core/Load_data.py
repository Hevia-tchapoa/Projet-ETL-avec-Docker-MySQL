import mysql.connector
from faker import Faker
import pandas as pd
import random


####dtftt


class CopyData:
    """This class copies data from Hevia database to joboard database."""

    def __init__(self, cursor_hevia, cursor_joboard):
        self.cursor_hevia = cursor_hevia
        self.cursor_joboard = cursor_joboard

    def copy_data_to_joboard(self):
        """Copy data from Hevia database to Joboard database."""
        try:
            tables = ["applications", "categories", "companies", "jobs", "users"]

            """ Copy data from hevia to joboard"""
            for table in tables:
                print(table)
                self.cursor_hevia.execute(f"SELECT * FROM {table}")
                results = self.cursor_hevia.fetchall()
                columns = [i[0] for i in self.cursor_hevia.description]
                """Exclude 'id' if it's auto-increment"""
                if "id" in columns:
                    columns_no_id = [col for col in columns if col != "id"]
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
