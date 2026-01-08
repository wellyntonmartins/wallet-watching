import os
import mysql.connector

def get_db_connection():
    host = os.getenv("MYSQLHOST")
    if not host:
        raise ValueError("MYSQLHOST environment variable not set!")
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )
