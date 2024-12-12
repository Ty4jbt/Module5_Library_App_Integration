
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        user="root",
        host="127.0.0.1",
        password="Full-Stack-dev97",
        database="library_db"
    )