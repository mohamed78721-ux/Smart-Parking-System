
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# قراءة بيانات الاتصال من ملف .env
load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )

        if connection.is_connected():
            print("Database connected successfully!")
            return connection

    except Error as error:
        print("Database connection failed:", error)

    return None
